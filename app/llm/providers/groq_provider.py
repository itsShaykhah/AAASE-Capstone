"""Groq provider adapter.

Groq is the default provider: it's free-tier friendly and fast, which
matters for a multi-agent pipeline that makes four sequential LLM calls
per run.
"""

from __future__ import annotations

from langchain_groq import ChatGroq

from app.llm.providers.base import BaseLLMProvider


class GroqProvider(BaseLLMProvider):
    def __init__(self, api_key: str, timeout_seconds: int) -> None:
        self._api_key = api_key
        self._timeout_seconds = timeout_seconds

    def build_chat_model(self, model_name: str) -> ChatGroq:
        return ChatGroq(
            model=model_name,
            api_key=self._api_key,
            timeout=self._timeout_seconds,
            max_retries=0,
        )
