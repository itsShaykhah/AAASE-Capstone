"""The input contract: a product brief submitted by a user.

This is the one schema the outside world (the UI, the API caller) needs to
know about to use the system. Everything else in app/schemas is produced
internally as the pipeline runs.
"""

from __future__ import annotations

from pydantic import BaseModel, Field, field_validator

from app.schemas.enums import CampaignObjective


class CampaignRequest(BaseModel):
    """A user's product brief and campaign parameters.

    Field length limits exist for two reasons: they keep prompts a small
    model can handle within context, and they're the first line of the
    guardrail layer (an oversized field is rejected before it ever reaches
    an LLM).
    """

    product_name: str = Field(..., min_length=2, max_length=120)
    product_description: str = Field(..., min_length=10, max_length=2000)
    campaign_objective: CampaignObjective
    target_audience: str | None = Field(
        default=None,
        max_length=500,
        description="Optional. If omitted, the Market Intelligence agent infers it from research.",
    )
    campaign_duration_days: int | None = Field(default=None, ge=1, le=365)
    brand_tone: str | None = Field(default=None, max_length=200)
    additional_notes: str | None = Field(default=None, max_length=1000)

    @field_validator("product_name", "product_description", "target_audience", "brand_tone", "additional_notes")
    @classmethod
    def _strip_whitespace(cls, value: str | None) -> str | None:
        return value.strip() if isinstance(value, str) else value
