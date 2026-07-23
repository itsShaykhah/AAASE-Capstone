"""LLM Factory / Model Manager.

This is the abstraction the whole project's LLM design hinges on: agents
and services ask for chat models *by agent key*, never by provider or
model name. Where those models actually come from — which provider, which
key, which model string — is entirely a function of `Settings`
(app/config/settings.py), so changing providers/models/keys is a
configuration change, never a code change.

Multi-key, multi-provider failover
-----------------------------------
A team commonly ends up with several free-tier keys per provider (one per
member). `get_chat_model_candidates` returns every usable (chat model,
resolved config) pair in try-order: all configured Groq keys first, then
all configured OpenRouter keys. `generate_structured_response`
(app/llm/structured_output.py) walks this list, moving to the next
candidate whenever one is rate-limited, unauthorized, or otherwise
unreachable — so one exhausted key degrades to the next key, then the
next provider, before the pipeline ever falls back to deterministic
content.
"""

from __future__ import annotations

from langchain_core.language_models.chat_models import BaseChatModel

from app.config.settings import LLMConfig, Settings
from app.llm.exceptions import LLMConfigurationError
from app.llm.providers.groq_provider import GroqProvider
from app.llm.providers.openrouter_provider import OpenRouterProvider
from app.schemas.enums import AgentKey, LLMProvider

_ChatModelCandidate = tuple[BaseChatModel, LLMConfig]


class LLMFactory:
    """Builds the ordered list of chat-model candidates for each agent."""

    def __init__(self, settings: Settings) -> None:
        self._settings = settings

    def get_chat_model_candidates(self, agent_key: AgentKey) -> list[_ChatModelCandidate]:
        """Return every usable chat model for `agent_key`, in try-order.

        If an agent has an explicit OpenRouter override configured, that
        provider is used exclusively (respecting the explicit choice). By
        default, every configured Groq key is tried before falling
        through to every configured OpenRouter key.
        """
        resolved = self._settings.resolve_llm_config(agent_key)

        if resolved.provider == LLMProvider.OPENROUTER:
            candidates = self._openrouter_candidates(resolved.model)
        else:
            candidates = self._groq_candidates(resolved.model) + self._openrouter_candidates(
                self._settings.llm_openrouter_fallback_model
            )

        if not candidates:
            raise LLMConfigurationError(
                "No Groq or OpenRouter API keys are configured. Set GROQ_API_KEY and/or "
                "OPENROUTER_API_KEY in .env, or set MOCK_MODE=true to run without any provider."
            )
        return candidates

    def _groq_candidates(self, model: str) -> list[_ChatModelCandidate]:
        return [
            (
                GroqProvider(api_key=key, timeout_seconds=self._settings.llm_request_timeout_seconds).build_chat_model(model),
                LLMConfig(provider=LLMProvider.GROQ, model=model),
            )
            for key in self._settings.groq_api_keys
        ]

    def _openrouter_candidates(self, model: str) -> list[_ChatModelCandidate]:
        return [
            (
                OpenRouterProvider(
                    api_key=key,
                    base_url=self._settings.openrouter_base_url,
                    app_name=self._settings.openrouter_app_name,
                    timeout_seconds=self._settings.llm_request_timeout_seconds,
                ).build_chat_model(model),
                LLMConfig(provider=LLMProvider.OPENROUTER, model=model),
            )
            for key in self._settings.openrouter_api_keys
        ]
