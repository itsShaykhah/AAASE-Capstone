"""Output contract for the Quality Assurance Agent (mermaid nodes Q1-Q7)."""

from __future__ import annotations

from pydantic import BaseModel, Field

from app.schemas.content_package import ContentPackage
from app.schemas.enums import QualityCheckStatus


class QualityCheckResult(BaseModel):
    check_name: str
    status: QualityCheckStatus
    notes: str = ""


class QualityAssessment(BaseModel):
    """What the QA LLM call actually returns.

    Deliberately does not include the content package itself — asking a
    model to reproduce every field of a package it's merely reviewing would
    be slow, costly, and a chance to silently corrupt content. Formatting
    fixes (hashtags, length trims) are applied deterministically in
    QualityAssuranceService instead; see QualityReview.final_content.
    """

    checks: list[QualityCheckResult] = Field(default_factory=list)
    overall_approved: bool
    final_notes: str


class QualityReview(BaseModel):
    """Result of the QA pass, including the final, possibly-corrected content."""

    checks: list[QualityCheckResult] = Field(default_factory=list)
    overall_approved: bool
    final_notes: str
    final_content: ContentPackage = Field(
        description="The content package after QA's deterministic fixes (hashtag formatting, "
        "length trims, etc.) have been applied."
    )
