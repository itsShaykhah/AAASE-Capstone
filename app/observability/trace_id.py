"""Trace ID generation (mermaid node O5 — Trace ID Manager).

A trace ID ties together every log line, metric, and traced step produced
by a single campaign run, so a run can be grep'd out of the logs end to end.
"""

from __future__ import annotations

import uuid


def new_trace_id() -> str:
    """Generate a new, URL-safe trace identifier for one pipeline run."""
    return uuid.uuid4().hex
