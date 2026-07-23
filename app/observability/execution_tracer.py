"""Execution tracing (mermaid node O2 — Execution Tracer).

Records an ordered timeline of named steps (one per agent, typically) with
start time, duration, and success/failure status — independent of the
logging concern in event_logger.py. Separating "what happened, in order,
with timing" (this file) from "narrative log lines" (EventLogger) keeps
each class small and lets the UI render a timeline without parsing logs.
"""

from __future__ import annotations

import time
from contextlib import contextmanager
from datetime import datetime, timezone
from typing import Iterator


class ExecutionTracer:
    """Builds an ordered list of {name, status, duration_ms, ...} steps."""

    def __init__(self) -> None:
        self._steps: list[dict] = []

    @contextmanager
    def trace(self, step_name: str) -> Iterator[None]:
        """Time a block of code and record it as one step, success or not."""
        started_at = datetime.now(timezone.utc)
        start = time.perf_counter()
        status = "success"
        try:
            yield
        except Exception:
            status = "error"
            raise
        finally:
            duration_ms = (time.perf_counter() - start) * 1000
            self._steps.append(
                {
                    "step": step_name,
                    "status": status,
                    "started_at": started_at.isoformat(),
                    "duration_ms": round(duration_ms, 2),
                }
            )

    @property
    def steps(self) -> list[dict]:
        return list(self._steps)
