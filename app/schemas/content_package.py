"""Output contract for the Content Generation Agent (mermaid nodes C1-C11).

The agent does not publish anything — it produces this package, which the
UI renders for a human to review, edit, and export.
"""

from __future__ import annotations

from pydantic import BaseModel, Field


class BrandVoice(BaseModel):
    tone: str
    style_keywords: list[str] = Field(default_factory=list, max_length=8)
    voice_description: str


class EmailCampaign(BaseModel):
    subject_line: str
    body: str


class ContentPackage(BaseModel):
    """Every platform-specific asset generated for one campaign."""

    brand_voice: BrandVoice
    instagram_caption: str
    x_post: str = Field(max_length=280, description="Kept under the X character limit.")
    linkedin_post: str
    email_campaign: EmailCampaign
    ad_headlines: list[str] = Field(default_factory=list, max_length=6)
    hashtags: list[str] = Field(default_factory=list, max_length=15)
    call_to_action: str
