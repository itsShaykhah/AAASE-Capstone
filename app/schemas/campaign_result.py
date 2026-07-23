"""The final, aggregated deliverable returned by the API and rendered by the UI.

This is the single object that flows: Coordinator -> API response -> Streamlit
session state -> exporter. Keeping it as one schema means the export service
and the UI never need to reach back into the graph state.
"""

from __future__ import annotations

from datetime import datetime, timezone

from pydantic import BaseModel, Field

from app.schemas.campaign_request import CampaignRequest
from app.schemas.campaign_strategy import CampaignStrategy
from app.schemas.content_package import ContentPackage
from app.schemas.enums import CampaignStatus
from app.schemas.market_intelligence import MarketIntelligenceReport
from app.schemas.quality_review import QualityReview


class ObservabilitySummary(BaseModel):
    """A UI-friendly rollup of the observability layer for one run."""

    trace_id: str
    total_duration_ms: float
    agent_durations_ms: dict[str, float] = Field(default_factory=dict)
    provider_used: dict[str, str] = Field(default_factory=dict)
    errors: list[str] = Field(default_factory=list)
    events: list[dict] = Field(default_factory=list)


class CampaignResult(BaseModel):
    """Everything generated for one campaign run, ready to display or export."""

    trace_id: str
    status: CampaignStatus
    request: CampaignRequest
    market_intelligence: MarketIntelligenceReport | None = None
    campaign_strategy: CampaignStrategy | None = None
    content_package: ContentPackage | None = None
    quality_review: QualityReview | None = None
    observability: ObservabilitySummary
    generated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
