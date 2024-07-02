import json, requests
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
        provider: ProviderPreferences_Type | None = None,
        model: str = "mistralai/mixtral-8x7b-instruct",
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

    def ensure_array(self,
            input_msg: List[Message_Type] | Message_Type
        ) -> List[Message_Type]:
        if isinstance(input_msg, (list, tuple)):
            return input_msg
        else:
            return [input_msg]

    def chat(self,
            messages: Message_Type,
            max_retries: int = 3,
            seed: int = None
    ):
        messages = self.ensure_array(messages)
        headers = {
            "Authorization": f"Bearer {self.api_key}",
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
                break
            except requests.exceptions.HTTPError as http_err:
                # HTTP error status code
                print(f'HTTP error occurred: {http_err} - Status Code: {http_err.response.status_code}')
                if 'error' in response.json():
                    print(response.json()['error']['message'])
                break
            except (requests.exceptions.Timeout, requests.exceptions.TooManyRedirects) as err:
                # timeouts and redirects
                print(f"Retry attempt {retries + 1} after error: {err}")
                retries += 1
            except requests.exceptions.RequestException as req_err:
                # any other request errors that haven't been caught by the previous except blocks
                print(f'An error occurred while making the request: {req_err}')
                retries += 1
            except Exception as e:
                # all other exceptions
                print(f'An unexpected error occurred: {e}')
                break
            
        return response.json()["choices"][0]["message"]["content"]
