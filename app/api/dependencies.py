"""FastAPI dependency providers.

Cached with `lru_cache` so the (moderately expensive to construct)
CampaignCoordinator — which builds the LLM factory and search service — is
built once per process, not once per request. Tests bypass this entirely
by constructing `CampaignCoordinator(settings=...)` directly with whatever
Settings they need.
"""

from __future__ import annotations

from functools import lru_cache

from app.config.settings import get_settings
from app.graph.coordinator import CampaignCoordinator
from app.guardrails.manager import GuardrailManager


@lru_cache
def get_coordinator() -> CampaignCoordinator:
    return CampaignCoordinator(get_settings())


@lru_cache
def get_guardrail_manager() -> GuardrailManager:
    return GuardrailManager()
