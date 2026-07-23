"""Market Intelligence Agent — LangGraph adapter (mermaid A1)."""

from __future__ import annotations

from app.llm.fallback_content import fallback_market_intelligence
from app.schemas.enums import AgentKey
from app.schemas.graph_state import CampaignGraphState
from app.services.market_intelligence_service import MarketIntelligenceService


class MarketIntelligenceAgent:
    def __init__(self, service: MarketIntelligenceService) -> None:
        self._service = service

    def run(self, state: CampaignGraphState) -> dict:
        observability = state["observability"]
        request = state["request"]

        try:
            report = self._service.generate(request, observability)
        except Exception as exc:  # noqa: BLE001 - last-resort safety net, see module docstring
            observability.event_logger.log(
                "agent_unhandled_error", agent=AgentKey.MARKET_INTELLIGENCE.value, error=str(exc)
            )
            return {
                "market_intelligence": fallback_market_intelligence(request),
                "errors": [f"market_intelligence: unhandled error - {exc}"],
            }

        return {"market_intelligence": report}
