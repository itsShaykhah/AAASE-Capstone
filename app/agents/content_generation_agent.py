"""Content Generation Agent — LangGraph adapter (mermaid A3)."""

from __future__ import annotations

from app.llm.fallback_content import fallback_content_package
from app.schemas.enums import AgentKey
from app.schemas.graph_state import CampaignGraphState
from app.services.content_generation_service import ContentGenerationService


class ContentGenerationAgent:
    def __init__(self, service: ContentGenerationService) -> None:
        self._service = service

    def run(self, state: CampaignGraphState) -> dict:
        observability = state["observability"]
        request = state["request"]
        strategy = state["campaign_strategy"]

        try:
            content = self._service.generate(request, strategy, observability)
        except Exception as exc:  # noqa: BLE001 - last-resort safety net, see agents/__init__.py
            observability.event_logger.log(
                "agent_unhandled_error", agent=AgentKey.CONTENT_GENERATION.value, error=str(exc)
            )
            return {
                "content_package": fallback_content_package(request, strategy),
                "errors": [f"content_generation: unhandled error - {exc}"],
            }

        return {"content_package": content}
