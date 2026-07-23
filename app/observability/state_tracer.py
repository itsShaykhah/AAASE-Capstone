"""Graph state snapshots (mermaid node O4 — State Tracer).

Captures a cheap, shallow view of the LangGraph state after each node runs
— which keys are populated, not their full contents — so a failure can be
localized to "state after campaign_strategy already had no research data"
without dumping potentially large objects into logs on every step.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Mapping


class StateTracer:
    """Records which state keys are populated after each node execution."""

    def __init__(self) -> None:
        self._snapshots: list[dict] = []

    def snapshot(self, node_name: str, state: Mapping[str, Any]) -> None:
        populated_keys = sorted(key for key, value in state.items() if value not in (None, [], {}))
        self._snapshots.append(
            {
                "node": node_name,
                "populated_keys": populated_keys,
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
        )

    @property
    def snapshots(self) -> list[dict]:
        return list(self._snapshots)
