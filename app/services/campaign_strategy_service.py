"""Business logic for the Campaign Strategy Agent (mermaid S1-S7).

A single structured-output call turns the market research into a full
CampaignStrategy — goal, channels, calendar, themes, and budget split.
"""

from __future__ import annotations

from app.config.settings import Settings
from app.guardrails.exceptions import OutputValidationError
from app.llm.exceptions import LLMInvocationError
from app.llm.factory import LLMFactory
from app.llm.fallback_content import fallback_campaign_strategy
from app.llm.structured_output import generate_structured_response
from app.observability.context import ObservabilityContext
from app.prompts.campaign_strategy import build_system_prompt, build_user_prompt
from app.schemas.campaign_request import CampaignRequest
from app.schemas.campaign_strategy import CampaignStrategy
from app.schemas.enums import AgentKey
from app.schemas.market_intelligence import MarketIntelligenceReport


class CampaignStrategyService:
    def __init__(self, llm_factory: LLMFactory, settings: Settings) -> None:
        self._llm_factory = llm_factory
        self._settings = settings

    def generate(
        self,
        request: CampaignRequest,
        research: MarketIntelligenceReport,
        observability: ObservabilityContext,
    ) -> CampaignStrategy:
        with observability.observe_agent(AgentKey.CAMPAIGN_STRATEGY) as agent_context:
            if self._settings.mock_mode:
                agent_context["provider"] = "mock"
                return fallback_campaign_strategy(request, research)

            try:
                strategy, llm_config = generate_structured_response(
                    llm_factory=self._llm_factory,
                    agent_key=AgentKey.CAMPAIGN_STRATEGY,
                    system_prompt=build_system_prompt(),
                    user_prompt=build_user_prompt(request, research),
                    schema=CampaignStrategy,
                    max_retries=self._settings.llm_max_retries,
                )
            except (OutputValidationError, LLMInvocationError) as exc:
                observability.metrics.record_error(f"{AgentKey.CAMPAIGN_STRATEGY.value}: {exc}")
                observability.event_logger.log(
                    "agent_degraded", agent=AgentKey.CAMPAIGN_STRATEGY.value, reason=str(exc)
                )
                agent_context["provider"] = "fallback"
                return fallback_campaign_strategy(request, research)

            agent_context["provider"] = f"{llm_config.provider.value}:{llm_config.model}"
            return strategy
