"""Provider interface every LLM adapter must implement."""

from __future__ import annotations

from abc import ABC, abstractmethod

from langchain_core.language_models.chat_models import BaseChatModel


class BaseLLMProvider(ABC):
    """Builds LangChain chat model instances for one provider."""

    @abstractmethod
    def build_chat_model(self, model_name: str) -> BaseChatModel:
        """Return a configured chat model for `model_name`.

        Implementations must set `max_retries=0` on the underlying client —
        retries are owned by app/guardrails/retry.py so failures are visible
        to the observability layer instead of being silently retried inside
        the SDK.
        """
        raise NotImplementedError
