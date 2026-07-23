"""Quality Assurance Agent — LangGraph adapter (mermaid A4)."""

from __future__ import annotations

from app.llm.fallback_content import fallback_quality_review
from app.schemas.enums import AgentKey
from app.schemas.graph_state import CampaignGraphState
from app.services.quality_assurance_service import QualityAssuranceService


class QualityAssuranceAgent:
    def __init__(self, service: QualityAssuranceService) -> None:
        self._service = service

    def run(self, state: CampaignGraphState) -> dict:
        observability = state["observability"]
        strategy = state["campaign_strategy"]
        content = state["content_package"]

        try:
            review = self._service.review(strategy, content, observability)
        except Exception as exc:  # noqa: BLE001 - last-resort safety net, see agents/__init__.py
            observability.event_logger.log(
                "agent_unhandled_error", agent=AgentKey.QUALITY_ASSURANCE.value, error=str(exc)
            )
            return {
                "quality_review": fallback_quality_review(content),
                "errors": [f"quality_assurance: unhandled error - {exc}"],
            }

        return {"quality_review": review}
