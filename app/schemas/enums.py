"""Shared enumerations used across config, schemas, and agents.

Kept in one place (rather than redefined per-module) so that, for example,
`AgentKey` means the same thing to `Settings.resolve_llm_config`, the
observability layer, and the LangGraph node names.
"""

from __future__ import annotations

from enum import StrEnum


class LLMProvider(StrEnum):
    """Supported LLM providers. Add a new provider by adding a value here,
    a matching adapter under app/llm/providers/, and one branch in
    LLMFactory._build_provider — nothing else needs to change.

    Note: "mock" is intentionally not a provider here. Offline/no-API-key
    operation is a cross-cutting execution mode (`Settings.mock_mode`)
    handled once in app/llm/structured_output.py, not a fake provider
    agents would need to know about.
    """

    GROQ = "groq"
    OPENROUTER = "openrouter"


class AgentKey(StrEnum):
    """Identifies each agent in the pipeline. Used for per-agent config
    overrides, observability tagging, and LangGraph node naming.
    """

    MARKET_INTELLIGENCE = "market_intelligence"
    CAMPAIGN_STRATEGY = "campaign_strategy"
    CONTENT_GENERATION = "content_generation"
    QUALITY_ASSURANCE = "quality_assurance"


class CampaignObjective(StrEnum):
    """Objectives a user can pick for a campaign in the UI."""

    BRAND_AWARENESS = "brand_awareness"
    LEAD_GENERATION = "lead_generation"
    SALES_CONVERSION = "sales_conversion"
    PRODUCT_LAUNCH = "product_launch"
    CUSTOMER_ENGAGEMENT = "customer_engagement"


class CampaignStatus(StrEnum):
    """Overall lifecycle status of a campaign run, surfaced to the UI."""

    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    BLOCKED = "blocked"


class QualityCheckStatus(StrEnum):
    """Outcome of a single QA check."""

    PASSED = "passed"
    NEEDS_ATTENTION = "needs_attention"
    FAILED = "failed"
