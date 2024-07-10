import json, requests, time
from typing import Any, List, Mapping, Optional, Literal, Union, TypedDict

class OpenRouter:
    """OpenRouter.
    https://openrouter.ai/docs#models
    https://openrouter.ai/docs#llm-parameters
    """

    Message_Type = TypedDict('Message', { 'role': Literal['user', 'assistant', 'system', 'tool'], 'content': str })
    ProviderPreferences_Type = TypedDict(
        'ProviderPreferences', {
            'allow_fallbacks': Optional[bool],
            'require_parameters': Optional[bool],
            'data_collection': Union[Literal['deny'], Literal['allow'], None],
            'order': Optional[List[Literal[
                'OpenAI', 'Anthropic', 'HuggingFace', 'Google', 'Together', 'DeepInfra', 'Azure', 'Modal',
                'AnyScale', 'Replicate', 'Perplexity', 'Recursal', 'Fireworks', 'Mistral', 'Groq', 'Cohere',
                'Lepton', 'OctoAI', 'Novita', 'DeepSeek', 'Infermatic', 'AI21', 'Featherless', 'Mancer',
                'Mancer 2', 'Lynn 2', 'Lynn'
            ]]]
        }, total=False
    )

    def __init__(self,
        api_key: str,
        provider: Optional[ProviderPreferences_Type] | None = None,
        model: str = "microsoft/wizardlm-2-7b",
        max_tokens: int = 0,
        temperature: Optional[float] | None = 1.0,
        top_k: Optional[int] | None = 0.0,
        top_p: Optional[float] = 1.0,
        presence_penalty: Optional[float] = 0.0,
        frequency_penalty: Optional[float] = 0.0,
        repetition_penalty: Optional[float] = 1.0,
        min_p: Optional[float] = 0.0,
        top_a: Optional[float] = 0.0,
        seed: Optional[int] | None = None,
        logit_bias: Optional[Mapping[int, int]] | None = None,
        response_format: Optional[Mapping[str, str]] | None = None,
        stop: Optional[Mapping[str, str]] | None = None,
        set_p50: bool = False,
        set_p90: bool = False,
        api_url: str = "https://openrouter.ai/api/v1/chat/completions",
        timeout: int = 3600,
        ):

        self.api_url = api_url
        self.api_key = api_key
        self.provider = provider
        self.model = model
        self.max_tokens = max_tokens
        self.seed = seed
        self.logit_bias = logit_bias
        self.response_format = response_format
        self.stop = stop
        self.timeout = timeout

        # Get the top LLM sampling parameter configurations used by users on OpenRouter.
        # https://openrouter.ai/docs/parameters-api
        if (set_p90 or set_p50):
            parameters_url = f'https://openrouter.ai/api/v1/parameters/{self.model}'
            headers = {
                'accept': 'application/json',
                'Authorization': f'Bearer {self.api_key}'
            }
            params = requests.get(parameters_url, headers=headers).json()["data"]
            # I am so sorry
            self.temperature = params["temperature_p50"] if set_p50 else params["temperature_p90"]
            self.top_k = params["top_k_p50"] if set_p50 else params["top_k_p90"]
            self.top_p = params["top_p_p50"] if set_p50 else params["top_p_p90"]
            self.presence_penalty = params["presence_penalty_p50"] if set_p50 else params["presence_penalty_p90"]
            self.frequency_penalty = params["frequency_penalty_p50"] if set_p50 else params["frequency_penalty_p90"]
            self.repetition_penalty = params["repetition_penalty_p50"] if set_p50 else params["repetition_penalty_p90"]
            self.min_p = params["min_p_p50"] if set_p50 else params["min_p_p90"]
            self.top_a = params["top_a_p50"] if set_p50 else params["top_a_p90"]
        else: 
            self.temperature = temperature 
            self.top_k = top_k 
            self.top_p = top_p 
            self.presence_penalty = presence_penalty 
            self.frequency_penalty = frequency_penalty 
            self.repetition_penalty = repetition_penalty 
            self.min_p = min_p 
            self.top_a = top_a 

    def set_params(self,
        max_tokens: Optional[int] | None = None,
        presence_penalty: Optional[float] | None = None,
        frequency_penalty: Optional[float] | None = None,
        repetition_penalty: Optional[float] | None = None,
        response_format: Optional[Mapping[str, str]] | None = None,
        temperature: Optional[float] | None = None,
        seed: Optional[int] | None = None,
        top_k: Optional[int] | None = None,
        top_p: Optional[float] | None = None,
        min_p: Optional[float] | None = None,
        top_a: Optional[float] | None = None,
        ):

        if max_tokens is not None: self.max_tokens = max_tokens
        if presence_penalty is not None: self.presence_penalty = presence_penalty
        if frequency_penalty is not None: self.frequency_penalty = frequency_penalty
        if repetition_penalty is not None: self.repetition_penalty = repetition_penalty
        if response_format is not None: self.response_format = response_format
        if temperature is not None: self.temperature = temperature
        if seed is not None: self.seed = seed
        if top_k is not None: self.top_k = top_k
        if top_p is not None: self.top_p = top_p
        if min_p is not None: self.min_p = min_p
        if top_a is not None: self.top_a = top_a
    def ensure_array(self,
            input_msg: List[Message_Type] | Message_Type
        ) -> List[Message_Type]:
        if isinstance(input_msg, (list, tuple)):
            return input_msg
        else:
            return [input_msg]

    def chat(self,
            messages: Message_Type,
            max_retries: int = 10,
            seed: int = None
    ):
        messages = self.ensure_array(messages)
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            'HTTP-Referer': 'https://github.com/datacrystals/AIStoryWriter',
            'X-Title': 'StoryForgeAI',
        }
        body={
            "model": self.model,
            "messages": messages,
            "max_token": self.max_tokens,
            "temperature": self.temperature,
            "top_k": self.top_k,
            "top_p": self.top_p,
            "presence_penalty": self.presence_penalty,
            "frequency_penalty": self.frequency_penalty,
            "repetition_penalty": self.repetition_penalty,
            "min_p": self.min_p,
            "top_a": self.top_a,
            "seed": self.seed if seed is None else seed,
            "logit_bias": self.logit_bias,
            "response_format": self.response_format,
            "stop": self.stop,
            "provider": self.provider,
            "stream": False,
        }

        retries = 0
        while retries < max_retries:
            try:
                response = requests.post(url=self.api_url, headers=headers, data=json.dumps(body), timeout=self.timeout, stream=False)
                response.raise_for_status()  # Raises an HTTPError if the HTTP request returned an unsuccessful status code
                if 'choices' in response.json():
                    # Return result from request
                    return response.json()["choices"][0]["message"]["content"]
                elif 'error' in response.json():
                    print(f"Openrouter returns error '{response.json()['error']['code']}' with message '{response.json()['error']['message']}', retry attempt {retries + 1}.")
                    if response.json()['error']['code'] == 400:
                        print("Bad Request (invalid or missing params, CORS)")
                    if response.json()['error']['code'] == 401:
                        raise Exception ("Invalid credentials (OAuth session expired, disabled/invalid API key)")
                    if response.json()['error']['code'] == 402:
                        raise Exception ("Your account or API key has insufficient credits. Add more credits and retry the request.")   
                    if response.json()['error']['code'] == 403:
                        print("Your chosen model requires moderation and your input was flagged")
                    if response.json()['error']['code'] == 408:
                        print("Your request timed out")
                    if response.json()['error']['code'] == 429:
                        print("You are being rate limited")
                        print("Waiting 10 seconds")
                        time.sleep(10)
                    if response.json()['error']['code'] == 502:
                        print("Your chosen model is down or we received an invalid response from it")
                    if response.json()['error']['code'] == 503:
                        print("There is no available model provider that meets your routing requirements")
                else:
                    from pprint import pprint
                    print(f"Response without error but missing choices, retry attempt {retries + 1}.")
                    pprint(response.json())
            except requests.exceptions.HTTPError as http_err:
                # HTTP error status code
                print(f"HTTP error occurred: '{http_err}' - Status Code: '{http_err.response.status_code}', retry attempt {retries + 1}.")
                # Funny Cloudflare being funny.
                # This is a lie: https://community.cloudflare.com/t/community-tip-fixing-error-524-a-timeout-occurred/42342
                if http_err.response.status_code == 524:
                    time.sleep(10)
            except (requests.exceptions.Timeout, requests.exceptions.TooManyRedirects) as err:
                # timeouts and redirects
                print(f"Retry attempt {retries + 1} after error: '{err}'")
            except requests.exceptions.RequestException as req_err:
                # any other request errors that haven't been caught by the previous except blocks
                print(f"An error occurred while making the request: '{req_err}', retry attempt {retries + 1}.")
            except Exception as e:
                # all other exceptions
                print(f"An unexpected error occurred: '{e}', retry attempt {retries + 1}.")
            retries += 1
