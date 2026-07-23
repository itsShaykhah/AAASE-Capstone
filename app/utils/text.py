"""Plain string helpers with no dependency on the rest of the app."""

from __future__ import annotations

import re

_SLUG_PATTERN = re.compile(r"[^a-z0-9]+")


def slugify(text: str) -> str:
    """Turn arbitrary text into a filesystem/URL-safe slug, e.g. for export filenames."""
    slug = _SLUG_PATTERN.sub("-", text.lower()).strip("-")
    return slug or "campaign"
