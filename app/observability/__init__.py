"""Lightweight observability: trace IDs, structured event logs, metrics,
execution tracing, and state snapshots.

Design rationale
----------------
Every graph run gets one `ObservabilityContext` (see context.py), created by
the coordinator and threaded through every node. That single object is the
public API the rest of the codebase uses — agents never touch
`EventLogger`/`MetricsCollector`/etc. directly, they call
`context.observe_agent(...)`. This keeps the four "O1-O5" components from
the architecture diagram cohesive as one facade while still letting each
one stay a small, single-purpose class underneath.
"""

from app.observability.context import ObservabilityContext
from app.observability.logging_config import configure_logging
from app.observability.trace_id import new_trace_id

__all__ = ["ObservabilityContext", "configure_logging", "new_trace_id"]
