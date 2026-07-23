"""The LangGraph state contract.

This TypedDict is the only thing every node reads and writes — it is the
contract of the graph. Keeping it in app/schemas (next to the domain models
it references) rather than inside app/graph keeps a clean dependency
direction: graph depends on schemas, not the other way around.

`errors` and `execution_events` use the `operator.add` reducer so that if a
future revision adds parallel branches, LangGraph merges contributions from
each branch instead of one overwriting another.
"""

from __future__ import annotations

import operator
from typing import Annotated, TypedDict

from app.observability.context import ObservabilityContext
from app.schemas.campaign_request import CampaignRequest
from app.schemas.campaign_strategy import CampaignStrategy
from app.schemas.content_package import ContentPackage
from app.schemas.market_intelligence import MarketIntelligenceReport
from app.schemas.quality_review import QualityReview


class CampaignGraphState(TypedDict, total=False):
    trace_id: str
    request: CampaignRequest
    observability: ObservabilityContext

    market_intelligence: MarketIntelligenceReport | None
    campaign_strategy: CampaignStrategy | None
    content_package: ContentPackage | None
    quality_review: QualityReview | None

    errors: Annotated[list[str], operator.add]
    execution_events: Annotated[list[dict], operator.add]
