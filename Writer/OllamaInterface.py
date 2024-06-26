import Writer.Config

import ollama



def InitClient(_ClientHost:str = "http://10.1.65.4:11434"):
    return ollama.Client(host=_ClientHost)


def ChatAndStreamResponse(_Client, _Logger, _Messages, _Model:str="llama3", _SeedOverride:int=-1):

    # Calculate Seed Information
    Seed = Writer.Config.SEED
    if (_SeedOverride != -1):
        Seed = _SeedOverride

    # Disallow empty garbage responses
    if (Writer.Config.DEBUG):
        print("--------- Message History START ---------")
        print("[")
        for Message in _Messages:
            print(f"{Message},\n----\n")
        print("]")
        print("--------- Message History END --------")

    while True:

        # Calculate Num Tokens (ish)
        TotalChars = len(str(_Messages))
        AvgCharsPerToken = 5 # got this off of some random dude on the internet
        EstimatedTokens = TotalChars / AvgCharsPerToken
        _Logger.Log(f"Using Model '{_Model}' | (Est. ~{EstimatedTokens}tok Context Length)", 4)

        # Log if there's a large estimated tokens of context history
        if EstimatedTokens > 24000:
            _Logger.Log(f"Warning, Detected High Token Context Length of est. ~{EstimatedTokens}tok", 6)

        # Now actually stream the response from ollama
        Stream = _Client.chat(
            model=_Model,
            messages=_Messages,
            stream=True,
            options=dict(seed=Seed)
        )
        ThisMessage:str = StreamResponse(Stream)

        # Check if it's empty
        if not ThisMessage["content"].isspace():
            _Messages.append(ThisMessage)
            _Logger.SaveLangchain("Generator", _Messages)
            return _Messages
        else:
            _Logger.Log("Model Returned Only Whitespace, Attempting Regeneration", 6)
            _Messages.append(BuildUserQuery("Sorry, but you returned an empty string, please try again!"))


def StreamResponse(_Stream):
  
    Response:str = ""
    for chunk in _Stream:
        ChunkText = chunk['message']['content']
        Response += ChunkText

        print(ChunkText, end='', flush=True)

    if (Writer.Config.DEBUG):
        print("\n\n\n")
    else:
        print("")
    
    return {'role': 'assistant', 'content': Response}

def BuildUserQuery(_Query:str):
    return {'role': 'user', 'content': _Query}

def BuildSystemQuery(_Query:str):
    return {'role': 'system', 'content': _Query}

def BuildAssistantQuery(_Query:str):
    return {'role': 'assistant', 'content': _Query}

def GetLastMessageText(_Messages:list):
    return _Messages[-1]["content"]

