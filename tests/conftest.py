"""Shared pytest fixtures.

`mock_settings` is used by almost every test in this suite: it forces
`mock_mode`, so the whole pipeline runs deterministically with zero API
keys and zero network calls (see app/llm/fallback_content.py).
"""

from __future__ import annotations

import pytest

from app.config.settings import Settings


@pytest.fixture
def mock_settings() -> Settings:
    return Settings(
        mock_mode=True,
        groq_api_key=None,
        openrouter_api_key=None,
        tavily_api_key=None,
        serper_api_key=None,
    )
