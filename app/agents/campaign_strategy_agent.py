"""Campaign Strategy Agent — LangGraph adapter (mermaid A2)."""

from __future__ import annotations

from app.llm.fallback_content import fallback_campaign_strategy
from app.schemas.enums import AgentKey
from app.schemas.graph_state import CampaignGraphState
from app.services.campaign_strategy_service import CampaignStrategyService


class CampaignStrategyAgent:
    def __init__(self, service: CampaignStrategyService) -> None:
        self._service = service

    def run(self, state: CampaignGraphState) -> dict:
        observability = state["observability"]
        request = state["request"]
        research = state["market_intelligence"]

        try:
            strategy = self._service.generate(request, research, observability)
        except Exception as exc:  # noqa: BLE001 - last-resort safety net, see agents/__init__.py
            observability.event_logger.log(
                "agent_unhandled_error", agent=AgentKey.CAMPAIGN_STRATEGY.value, error=str(exc)
            )
            return {
                "campaign_strategy": fallback_campaign_strategy(request, research),
                "errors": [f"campaign_strategy: unhandled error - {exc}"],
            }

        return {"campaign_strategy": strategy}
