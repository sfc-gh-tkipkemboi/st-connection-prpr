from types import ModuleType
from typing import Sequence
from openai import ChatCompletion, Completion

from streamlit_openai.base_connection import BaseConnection
from streamlit.runtime.caching import cache_data
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


    def client(self) -> ModuleType:
        return self._instance


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

        @cache_data(ttl=ttl, max_entries=max_entries, show_spinner='Asking GPT...')
        def _get_completion(model: str, prompt: str, **kwargs) -> str:
            response = self._instance.Completion.create(
                model=model,
                prompt=prompt,
                **kwargs
            )
            return response.choices[0].text

        return _get_completion(self.model, prompt, **kwargs)

    
    @retry(
            wait=wait_fixed(3),
            stop=stop_after_attempt(4),
            reraise=True,
            before=_reset_on_retry_failure
            )
    def get_embedding(self, text: str, ttl=3600, max_entries=None) -> Sequence[float]:
        """Get an embedding vector (list of floats) for the provided text."""

        @cache_data(ttl=ttl, max_entries=max_entries, show_spinner='Asking GPT...')
        def _get_embedding(model: str, text: str, **kwargs) -> Sequence[float]:
            response = self._instance.Embedding.create(
                input = [text],
                model=model,
                **kwargs
            )
            return response['data'][0]['embedding']

        return _get_embedding(self.embedding_model, text)
    