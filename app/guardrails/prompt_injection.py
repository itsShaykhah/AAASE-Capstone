"""Prompt-injection detection (mermaid node GR2).

This is a lightweight, regex/heuristic layer — not a model-based classifier.
It catches the common, unsophisticated attacks (the ones this capstone's
own guide calls out: "ignore previous instructions...") and documents
plainly that a paraphrased attack can still slip through. That honesty is
intentional: see resources-from-instrcutor-do-not-modify/01_BUILD_THE_AGENT.md
Milestone 6, which flags this as the expected limitation of a regex-based
guardrail rather than something to over-engineer around for a v1 prototype.
"""

from __future__ import annotations

import re

_INJECTION_PATTERNS: list[re.Pattern[str]] = [
    re.compile(r"ignore (all )?(previous|prior|above) instructions", re.IGNORECASE),
    re.compile(r"disregard (the )?(system|previous) prompt", re.IGNORECASE),
    re.compile(r"you are now (a|an|no longer)", re.IGNORECASE),
    re.compile(r"reveal (your|the) (system prompt|instructions)", re.IGNORECASE),
    re.compile(r"act as (if you (are|were)|an? unrestricted)", re.IGNORECASE),
    re.compile(r"forget (everything|all) (you|above)", re.IGNORECASE),
    re.compile(r"\bDAN\b|do anything now", re.IGNORECASE),
    re.compile(r"<\|.*?\|>"),  # fake special tokens
    re.compile(r"system\s*:\s*", re.IGNORECASE),
]


def detect_prompt_injection(text: str) -> list[str]:
    """Return the list of matched injection patterns found in `text` (empty if none)."""
    if not text:
        return []
    return [pattern.pattern for pattern in _INJECTION_PATTERNS if pattern.search(text)]


def contains_prompt_injection(text: str) -> bool:
    return bool(detect_prompt_injection(text))
