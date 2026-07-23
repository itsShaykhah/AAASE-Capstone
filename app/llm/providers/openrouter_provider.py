"""OpenRouter provider adapter.

OpenRouter exposes an OpenAI-compatible API, so we reuse `ChatOpenAI` from
langchain-openai pointed at OpenRouter's base URL rather than depending on
a separate SDK. The `HTTP-Referer`/`X-Title` headers are OpenRouter's
attribution convention for free-tier usage.
"""

from __future__ import annotations

from langchain_openai import ChatOpenAI

from app.llm.providers.base import BaseLLMProvider


class OpenRouterProvider(BaseLLMProvider):
    def __init__(self, api_key: str, base_url: str, app_name: str, timeout_seconds: int) -> None:
        self._api_key = api_key
        self._base_url = base_url
        self._app_name = app_name
        self._timeout_seconds = timeout_seconds

    def build_chat_model(self, model_name: str) -> ChatOpenAI:
        return ChatOpenAI(
            model=model_name,
            api_key=self._api_key,
            base_url=self._base_url,
            timeout=self._timeout_seconds,
            max_retries=0,
            default_headers={
                "HTTP-Referer": "https://github.com/ai-marketing-team",
                "X-Title": self._app_name,
            },
        )
