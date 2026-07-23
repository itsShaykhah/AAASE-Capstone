"""Centralized application settings.

Design rationale
----------------
Every piece of configuration the system needs — API keys, which LLM
provider/model each agent should use, search provider keys, server ports —
is declared here as a typed field on a single `Settings` object. This is the
*only* place that reads environment variables (via pydantic-settings). That
constraint is what makes "change the provider/model via configuration, not
code" actually true: nothing downstream ever calls `os.environ` itself, it
asks `get_settings()` for a resolved value.

Per-agent overrides
--------------------
Each agent may optionally use a different provider/model than the global
default (e.g. a cheaper model for content generation, a stronger one for
QA). If an agent-specific env var isn't set, we fall back to the global
default. This is resolved by `resolve_llm_config`, so the LLM factory and
agents never need to know about the fallback rules themselves.
"""

from __future__ import annotations

from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from app.schemas.enums import AgentKey, LLMProvider


def _dedupe_keys(raw_keys: list[str | None]) -> list[str]:
    """Strip, drop blanks, and drop duplicates while preserving order."""
    seen: set[str] = set()
    result: list[str] = []
    for key in raw_keys:
        if not key:
            continue
        stripped = key.strip()
        if stripped and stripped not in seen:
            seen.add(stripped)
            result.append(stripped)
    return result


class LLMConfig:
    """Resolved (provider, model) pair for a single agent."""

    __slots__ = ("provider", "model")

    def __init__(self, provider: LLMProvider, model: str) -> None:
        self.provider = provider
        self.model = model

    def __repr__(self) -> str:  # pragma: no cover - debugging aid only
        return f"LLMConfig(provider={self.provider!r}, model={self.model!r})"


class Settings(BaseSettings):
    """Typed application configuration, populated from environment variables
    (and a local .env file during development). See .env.example for the
    full list of supported variables and their defaults.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
        populate_by_name=True,
    )

    # --- General application settings -----------------------------------
    app_env: str = Field(default="development", alias="APP_ENV")
    log_level: str = Field(default="INFO", alias="LOG_LEVEL")
    mock_mode: bool = Field(default=False, alias="MOCK_MODE")

    # --- LLM provider defaults -------------------------------------------
    llm_default_provider: LLMProvider = Field(default=LLMProvider.GROQ, alias="LLM_DEFAULT_PROVIDER")
    llm_default_model: str = Field(default="llama-3.1-8b-instant", alias="LLM_DEFAULT_MODEL")
    llm_max_retries: int = Field(default=2, alias="LLM_MAX_RETRIES")
    llm_request_timeout_seconds: int = Field(default=60, alias="LLM_REQUEST_TIMEOUT_SECONDS")

    # A team commonly has several free-tier keys (one per member) for the
    # same provider. All configured keys for a provider are tried in order
    # (GROQ_API_KEY, then GROQ_API_KEY1, GROQ_API_KEY2, ...) before moving
    # on to the next provider — see LLMFactory.get_chat_model_candidates.
    groq_api_key: str | None = Field(default=None, alias="GROQ_API_KEY")
    groq_api_key_1: str | None = Field(default=None, alias="GROQ_API_KEY1")
    groq_api_key_2: str | None = Field(default=None, alias="GROQ_API_KEY2")
    groq_api_key_3: str | None = Field(default=None, alias="GROQ_API_KEY3")

    llm_openrouter_fallback_model: str = Field(
        default="meta-llama/llama-3.1-8b-instruct:free", alias="OPENROUTER_FALLBACK_MODEL"
    )
    openrouter_api_key: str | None = Field(default=None, alias="OPENROUTER_API_KEY")
    openrouter_api_key_1: str | None = Field(default=None, alias="OPENROUTER_API_KEY1")
    openrouter_api_key_2: str | None = Field(default=None, alias="OPENROUTER_API_KEY2")
    openrouter_api_key_3: str | None = Field(default=None, alias="OPENROUTER_API_KEY3")
    openrouter_api_key_4: str | None = Field(default=None, alias="OPENROUTER_API_KEY4")
    openrouter_base_url: str = Field(default="https://openrouter.ai/api/v1", alias="OPENROUTER_BASE_URL")
    openrouter_app_name: str = Field(default="AI Marketing Team", alias="OPENROUTER_APP_NAME")

    # --- Per-agent overrides (optional; fall back to the defaults above) -
    market_intelligence_provider: LLMProvider | None = Field(default=None, alias="MARKET_INTELLIGENCE_PROVIDER")
    market_intelligence_model: str | None = Field(default=None, alias="MARKET_INTELLIGENCE_MODEL")

    campaign_strategy_provider: LLMProvider | None = Field(default=None, alias="CAMPAIGN_STRATEGY_PROVIDER")
    campaign_strategy_model: str | None = Field(default=None, alias="CAMPAIGN_STRATEGY_MODEL")

    content_generation_provider: LLMProvider | None = Field(default=None, alias="CONTENT_GENERATION_PROVIDER")
    content_generation_model: str | None = Field(default=None, alias="CONTENT_GENERATION_MODEL")

    quality_assurance_provider: LLMProvider | None = Field(default=None, alias="QUALITY_ASSURANCE_PROVIDER")
    quality_assurance_model: str | None = Field(default=None, alias="QUALITY_ASSURANCE_MODEL")

    # --- Search providers --------------------------------------------------
    tavily_api_key: str | None = Field(default=None, alias="TAVILY_API_KEY")
    serper_api_key: str | None = Field(default=None, alias="SERPER_API_KEY")
    search_max_results: int = Field(default=5, alias="SEARCH_MAX_RESULTS")
    search_request_timeout_seconds: int = Field(default=20, alias="SEARCH_REQUEST_TIMEOUT_SECONDS")

    # --- API / server --------------------------------------------------
    api_host: str = Field(default="0.0.0.0", alias="API_HOST")
    api_port: int = Field(default=8000, alias="API_PORT")
    cors_allow_origins: str = Field(default="*", alias="CORS_ALLOW_ORIGINS")

    # --- Frontend --------------------------------------------------
    api_base_url: str = Field(default="http://127.0.0.1:8000", alias="API_BASE_URL")

    def _overrides_for(self, agent_key: AgentKey) -> tuple[LLMProvider | None, str | None]:
        mapping: dict[AgentKey, tuple[LLMProvider | None, str | None]] = {
            AgentKey.MARKET_INTELLIGENCE: (self.market_intelligence_provider, self.market_intelligence_model),
            AgentKey.CAMPAIGN_STRATEGY: (self.campaign_strategy_provider, self.campaign_strategy_model),
            AgentKey.CONTENT_GENERATION: (self.content_generation_provider, self.content_generation_model),
            AgentKey.QUALITY_ASSURANCE: (self.quality_assurance_provider, self.quality_assurance_model),
        }
        return mapping[agent_key]

    def resolve_llm_config(self, agent_key: AgentKey) -> LLMConfig:
        """Resolve the (provider, model) pair a given agent should use.

        Falls back to the global default whenever an agent-specific
        override isn't configured. This is the single source of truth for
        "which model does agent X use" — nothing else should hardcode it.
        """
        override_provider, override_model = self._overrides_for(agent_key)
        provider = override_provider or self.llm_default_provider
        model = override_model or self.llm_default_model
        return LLMConfig(provider=provider, model=model)

    @property
    def groq_api_keys(self) -> list[str]:
        """All configured Groq keys, in try-order, deduplicated."""
        return _dedupe_keys([self.groq_api_key, self.groq_api_key_1, self.groq_api_key_2, self.groq_api_key_3])

    @property
    def openrouter_api_keys(self) -> list[str]:
        """All configured OpenRouter keys, in try-order, deduplicated."""
        return _dedupe_keys(
            [
                self.openrouter_api_key,
                self.openrouter_api_key_1,
                self.openrouter_api_key_2,
                self.openrouter_api_key_3,
                self.openrouter_api_key_4,
            ]
        )

    @property
    def cors_origins_list(self) -> list[str]:
        if self.cors_allow_origins == "*":
            return ["*"]
        return [origin.strip() for origin in self.cors_allow_origins.split(",") if origin.strip()]


@lru_cache
def get_settings() -> Settings:
    """Return the process-wide Settings singleton.

    Cached so environment parsing happens once; tests that need different
    configuration should construct `Settings(...)` directly instead of
    mutating the cached instance.
    """
    return Settings()
