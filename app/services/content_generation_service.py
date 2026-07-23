"""Business logic for the Content Generation Agent (mermaid C1-C11).

A single structured-output call produces every platform asset together
(brand voice, captions, posts, email, ad headlines, hashtags, CTA) so the
whole package shares one consistent voice, rather than generating each
asset with a separate call that could drift in tone.
"""

from __future__ import annotations

from app.config.settings import Settings
from app.guardrails.exceptions import OutputValidationError
from app.llm.exceptions import LLMInvocationError
from app.llm.factory import LLMFactory
from app.llm.fallback_content import fallback_content_package
from app.llm.structured_output import generate_structured_response
from app.observability.context import ObservabilityContext
from app.prompts.content_generation import build_system_prompt, build_user_prompt
from app.schemas.campaign_request import CampaignRequest
from app.schemas.campaign_strategy import CampaignStrategy
from app.schemas.content_package import ContentPackage
from app.schemas.enums import AgentKey


class ContentGenerationService:
    def __init__(self, llm_factory: LLMFactory, settings: Settings) -> None:
        self._llm_factory = llm_factory
        self._settings = settings

    def generate(
        self,
        request: CampaignRequest,
        strategy: CampaignStrategy,
        observability: ObservabilityContext,
    ) -> ContentPackage:
        with observability.observe_agent(AgentKey.CONTENT_GENERATION) as agent_context:
            if self._settings.mock_mode:
                agent_context["provider"] = "mock"
                return fallback_content_package(request, strategy)

            try:
                content, llm_config = generate_structured_response(
                    llm_factory=self._llm_factory,
                    agent_key=AgentKey.CONTENT_GENERATION,
                    system_prompt=build_system_prompt(),
                    user_prompt=build_user_prompt(request, strategy),
                    schema=ContentPackage,
                    max_retries=self._settings.llm_max_retries,
                )
            except (OutputValidationError, LLMInvocationError) as exc:
                observability.metrics.record_error(f"{AgentKey.CONTENT_GENERATION.value}: {exc}")
                observability.event_logger.log(
                    "agent_degraded", agent=AgentKey.CONTENT_GENERATION.value, reason=str(exc)
                )
                agent_context["provider"] = "fallback"
                return fallback_content_package(request, strategy)

            agent_context["provider"] = f"{llm_config.provider.value}:{llm_config.model}"
            return content
