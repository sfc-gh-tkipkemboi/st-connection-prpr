from types import ModuleType
from typing import Sequence
from openai import ChatCompletion, Completion

from base_connection import BaseConnection
from streamlit.runtime.caching import cache_data, cache_resource
from tenacity import retry, wait_fixed, stop_after_attempt, RetryCallState


def _reset_on_retry_failure(retry_state: RetryCallState):
    if retry_state.attempt_number > 1:
        print("Something went wrong, retrying")
        self = retry_state.args[0]
        self.reset()


class OpenAIConnection(BaseConnection[ModuleType]):
    _default_connection_name = "openai"

    def _secrets_as_dict(self) -> dict:
        secrets = self.get_secrets()
        return {k: v for k, v in secrets.items()}


    def connect(self, **kwargs) -> ModuleType:
        import openai

        merged_args = {**self._secrets_as_dict(), **kwargs}
        openai.api_key = merged_args.pop('api_key')

        self.model = merged_args.get('model', 'text-davinci-003')
        self.embedding_model = merged_args.get('embedding_model', 'text-embedding-ada-002')
        self.max_tokens = merged_args.get('max_tokens', 256)
        self.temperature = merged_args.get('temperature', 1.0)

        return openai

    ## Basic Completion ##
    @staticmethod
    def _get_completion(_instance: ModuleType, model: str, prompt: str, **kwargs) -> str:
        response = _instance.Completion.create(
            model=model,
            prompt=prompt,
            **kwargs
        )
        return response.choices[0].text
    
    @retry(
            wait=wait_fixed(3),
            stop=stop_after_attempt(4),
            reraise=True,
            before=_reset_on_retry_failure
            )
    def get_completion(self, prompt: str, ttl=3600, max_entries=None) -> str:
        """Get a completion (text) for the provided prompt."""
        kwargs = dict(
            max_tokens=self.max_tokens,
            n=1,
            stop=None,
            temperature=self.temperature,
        )

        if ttl is None or ttl > 0 or max_entries is None or max_entries > 0:
            return cache_data(
                self._get_completion,
                ttl=ttl,
                max_entries=max_entries,
                show_spinner='Asking GPT...'
                )(
                self._instance,
                model=self.model,
                prompt=prompt,
                **kwargs
            )
        return self._get_completion(self._instance, self.model, prompt, **kwargs)

    ## Embeddings ##
    @staticmethod
    def _get_embedding(_instance: ModuleType, model: str, text: str, **kwargs) -> str:
        response = _instance.Embedding.create(
            input = [text],
            model=model,
            **kwargs
        )
        return response['data'][0]['embedding']
    
    @retry(
            wait=wait_fixed(3),
            stop=stop_after_attempt(4),
            reraise=True,
            before=_reset_on_retry_failure
            )
    def get_embedding(self, text: str, ttl=3600, max_entries=None) -> Sequence[float]:
        """Get an embedding vector (list of floats) for the provided text."""
        if ttl is None or ttl > 0 or max_entries is None or max_entries > 0:
            return cache_data(
                self._get_embedding,
                ttl=ttl,
                max_entries=max_entries,
                show_spinner='Asking GPT...'
                )(
                self._instance,
                model=self.embedding_model,
                text=text,
            )
        return self._get_embedding(self._instance, self.embedding_model, text)
    

    # TODO(sfc-gh-jcarroll): Clean this up. I think there's a slick little ChatConnection
    # class that will preserve history in here.
    @cache_data(max_entries=10000, show_spinner='Asking GPT...')
    # @retry(delay=1, backoff=2, max_delay=4)
    def get_chat_completion(self, messages) -> ChatCompletion:
        """Get a chat completion, given a bunch of previous messages."""
        return self._instance.ChatCompletion.create(
            model=self.model,
            messages=messages,
            max_tokens=self.max_tokens,
        )
    
    def client(self) -> ModuleType:
        return self._instance


def connect_openai(name: str = "default", ttl = 3600, **kwargs):
    "Connect to OpenAI and return an initialized OpenAIConnection."
    if ttl is None or ttl > 0:
        return cache_resource(OpenAIConnection, ttl=ttl)(name, **kwargs)
    else:
        return OpenAIConnection(name, **kwargs)
    