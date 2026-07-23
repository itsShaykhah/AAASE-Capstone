"""Structured event logging (mermaid node O1 — Event Logger).

Every event is a flat JSON-serializable dict stamped with the run's trace
ID. Events are both written through the standard `logging` module (so they
show up in normal server logs / Render logs) and kept in memory for the
duration of the run so the UI can render an observability timeline without
needing a log-aggregation backend.
"""

from __future__ import annotations

import json
import logging
from datetime import datetime, timezone
from typing import Any

logger = logging.getLogger("ai_marketing_team.events")


class EventLogger:
    """Collects and emits structured events for a single trace ID."""

    def __init__(self, trace_id: str) -> None:
        self._trace_id = trace_id
        self._events: list[dict[str, Any]] = []

    def log(self, event: str, **fields: Any) -> dict[str, Any]:
        """Record one structured event and emit it as a JSON log line."""
        record = {
            "trace_id": self._trace_id,
            "event": event,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            **fields,
        }
        self._events.append(record)
        logger.info(json.dumps(record, default=str))
        return record

    @property
    def events(self) -> list[dict[str, Any]]:
        """All events logged so far, in chronological order."""
        return list(self._events)
