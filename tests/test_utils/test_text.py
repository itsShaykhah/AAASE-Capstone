from __future__ import annotations

from app.utils.text import slugify


def test_slugify_basic():
    assert slugify("Acme Widget Pro!") == "acme-widget-pro"


def test_slugify_falls_back_when_nothing_alphanumeric():
    assert slugify("???") == "campaign"
