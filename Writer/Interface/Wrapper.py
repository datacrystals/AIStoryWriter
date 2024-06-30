import Writer.Config
import dotenv
import ollama
import inspect
import os
import time

import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold


dotenv.load_dotenv()


class Interface:

    def __init__(
        self,
        Models: list = [],
    ):
        self.Clients: dict = {}
        self.History = []
        OllamaModels = None
        for Model in Models:
            if Model in self.Clients:
                continue
            else:
                Provider, ProviderModel = self.GetModelAndProvider(Model)
                print(f"DEBUG: Loading Model {ProviderModel} from {Provider}")
                if Provider == "ollama":
                    # Get ollama models (only once)
                    if OllamaModels is None:
                        OllamaModelList = ollama.Client(
                            host=Writer.Config.OLLAMA_HOST
                        ).list()
                        OllamaModels = [m["name"] for m in OllamaModelList["models"]]

                    # check if the model is in the list of models
                    if (
                        ProviderModel not in OllamaModels
                        and not ProviderModel + ":latest" in OllamaModels
                    ):
                        print(
                            f"Model {ProviderModel} not found in Ollama models. Downloading..."
                        )
                        OllamaDownloadStream = ollama.Client(
                            host=Writer.Config.OLLAMA_HOST
                        ).pull(ProviderModel, stream=True)
                        for chunk in OllamaDownloadStream:
                            if "completed" in chunk and "total" in chunk:
                                # {'status': 'pulling 232a79463bc4', 'digest': 'sha256:232a79463bc4bcf9a76b1691a7b7beb9c08f5c3a109fedcebff422d7a71fba71', 'total': 7598928672, 'completed': 1042274720}
                                OllamaDownloadProgress = (
                                    chunk["completed"] / chunk["total"]
                                )
                                completedSize = chunk["completed"] / 1024**3
                                totalSize = chunk["total"] / 1024**3
                                print(
                                    f"Downloading {ProviderModel}: {OllamaDownloadProgress * 100:.2f}% ({completedSize:.3f}GB/{totalSize:.3f}GB)",
                                    end="\r",
                                )
                            else:
                                print(f"{chunk['status']} {ProviderModel}", end="\r")
                        print("\n\n\n")
                        OllamaModels.append(ProviderModel)

                    self.Clients[Model] = ollama.Client(host=Writer.Config.OLLAMA_HOST)
                    print(f"OLLAMA Host is '{Writer.Config.OLLAMA_HOST}'")

                elif Provider == "google":
                    # Validate Google API Key
                    if (
                        not "GOOGLE_API_KEY" in os.environ
                        or os.environ["GOOGLE_API_KEY"] == ""
                    ):
                        raise Exception(
                            "GOOGLE_API_KEY not found in environment variables"
                        )
                    genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
                    self.Clients[Model] = genai.GenerativeModel(
                        model_name=ProviderModel
                    )

                elif Provider == "openai":
                    raise NotImplementedError("OpenAI API not supported")

                elif Provider == "Anthropic":
                    raise NotImplementedError("Anthropic API not supported")

                else:
                    print(f"Warning, ")
                    raise Exception(f"Model Provider {Provider} for {Model} not found")

    def ChatAndStreamResponse(
        self,
        _Logger,
        _Messages,
        _Model: str = "llama3",
        _SeedOverride: int = -1,
        _Format: str = None,
    ):
        Provider, ProviderModel = self.GetModelAndProvider(_Model)

        # Calculate Seed Information
        Seed = Writer.Config.SEED if _SeedOverride == -1 else _SeedOverride

        # Log message history if DEBUG is enabled
        if Writer.Config.DEBUG:
            print("--------- Message History START ---------")
            print("[")
            for Message in _Messages:
                print(f"{Message},\n----\n")
            print("]")
            print("--------- Message History END --------")

        StartGeneration = time.time()

        # Calculate estimated tokens
        TotalChars = len(str(_Messages))
        AvgCharsPerToken = 5  # estimated average chars per token
        EstimatedTokens = TotalChars / AvgCharsPerToken
        _Logger.Log(
            f"Using Model '{ProviderModel}' from '{Provider}' | (Est. ~{EstimatedTokens}tok Context Length)",
            4,
        )

        # Log if there's a large estimated tokens of context history
        if EstimatedTokens > 24000:
            _Logger.Log(
                f"Warning, Detected High Token Context Length of est. ~{EstimatedTokens}tok",
                6,
            )

        if Provider == "ollama":
            if _Format == "json":
                _Logger.Log("Using Ollama JSON Format", 4)
            Stream = self.Clients[_Model].chat(
                model=ProviderModel,
                messages=_Messages,
                stream=True,
                options=dict(seed=Seed, format=_Format),
            )
            MaxRetries = 3
            while True:
                try:
                    _Messages.append(self.StreamResponse(Stream, Provider))
                    break
                except Exception as e:
                    if MaxRetries > 0:
                        _Logger.Log(
                            f"Exception During Generation '{e}', {MaxRetries} Retries Remaining",
                            7,
                        )
                        MaxRetries -= 1
                    else:
                        _Logger.Log(
                            f"Max Retries Exceeded During Generation, Aborting!", 7
                        )
                        raise Exception(
                            "Generation Failed, Max Retires Exceeded, Aborting"
                        )

        elif Provider == "google":
            # replace "content" with "parts" for google
            _Messages = [{"role": m["role"], "parts": m["content"]} for m in _Messages]
            for m in _Messages:
                if "content" in m:
                    m["parts"] = m["content"]
                    del m["content"]
                if "role" in m and m["role"] == "assistant":
                    m["role"] = "model"
                    # Google doesn't support "system" role while generating content (only while instantiating the model)
                if "role" in m and m["role"] == "system":
                    m["role"] = "user"

            MaxRetries = 3
            while True:
                try:
                    Stream = self.Clients[_Model].generate_content(
                        contents=_Messages,
                        stream=True,
                        safety_settings={
                            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
                            HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
                            HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
                            HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
                        },
                    )
                    _Messages.append(self.StreamResponse(Stream, Provider))
                    break
                except Exception as e:
                    if MaxRetries > 0:
                        _Logger.Log(
                            f"Exception During Generation '{e}', {MaxRetries} Retries Remaining",
                            7,
                        )
                        MaxRetries -= 1
                    else:
                        _Logger.Log(
                            f"Max Retries Exceeded During Generation, Aborting!", 7
                        )
                        raise Exception(
                            "Generation Failed, Max Retires Exceeded, Aborting"
                        )

            # Replace "parts" back to "content" for generalization
            # and replace "model" with "assistant"
            for m in _Messages:
                if "parts" in m:
                    m["content"] = m["parts"]
                    del m["parts"]
                if "role" in m and m["role"] == "model":
                    m["role"] = "assistant"

        elif Provider == "openai":
            raise NotImplementedError("OpenAI API not supported")

        elif Provider == "Anthropic":
            raise NotImplementedError("Anthropic API not supported")

        else:
            raise Exception(f"Model Provider {Provider} for {_Model} not found")

        # Log the time taken to generate the response
        EndGeneration = time.time()
        _Logger.Log(
            f"Generated Response in {round(EndGeneration - StartGeneration, 2)}s (~{round(EstimatedTokens / (EndGeneration - StartGeneration), 2)}tok/s)",
            4,
        )
        # Check if the response is empty and attempt regeneration if necessary
        if _Messages[-1]["content"].isspace():
            _Logger.Log("Model Returned Only Whitespace, Attempting Regeneration", 6)
            _Messages.append(
                self.BuildUserQuery(
                    "Sorry, but you returned an empty string, please try again!"
                )
            )
            return self.ChatAndStreamResponse(_Logger, _Messages, _Model, _SeedOverride)

        CallStack: str = ""
        for Frame in inspect.stack()[1:]:
            CallStack += f"{Frame.function}."
        CallStack = CallStack[:-1].replace("<module>", "Main")
        _Logger.SaveLangchain(CallStack, _Messages)
        return _Messages

    def StreamResponse(self, _Stream, _Provider: str):
        Response: str = ""
        for chunk in _Stream:
            if _Provider == "ollama":
                ChunkText = chunk["message"]["content"]
            elif _Provider == "google":
                ChunkText = chunk.text
            else:
                raise ValueError(f"Unsupported provider: {_Provider}")

            Response += ChunkText
            print(ChunkText, end="", flush=True)

        print("\n\n\n" if Writer.Config.DEBUG else "")
        return {"role": "assistant", "content": Response}

    def BuildUserQuery(self, _Query: str):
        return {"role": "user", "content": _Query}

    def BuildSystemQuery(self, _Query: str):
        return {"role": "system", "content": _Query}

    def BuildAssistantQuery(self, _Query: str):
        return {"role": "assistant", "content": _Query}

    def GetLastMessageText(self, _Messages: list):
        return _Messages[-1]["content"]

    def GetModelAndProvider(self, _Model: str):
        # Early check for ollama, since sometimes models have username/model
        # so the full path is going to be `ollama/username/model:size`
        if _Model.lower().startswith("ollama"):
            Model = _Model.replace("ollama/", "")
            return "ollama", Model

        # Now do the proper check for other providers
        Provider = _Model.lower().split("/")[0] if "/" in _Model else "ollama"
        Model = _Model.lower().split("/")[1] if "/" in _Model else _Model
        return Provider, Model
