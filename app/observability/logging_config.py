"""Root logging configuration.

Without this, Python's default logging setup only surfaces WARNING and
above to the console — so EventLogger's `logger.info(...)` calls (see
event_logger.py) would silently never reach stdout/Render logs, even
though every event is still captured in-memory and returned to callers.
`configure_logging` is called once at process startup (see
app/api/main.py) to make the "logged" part of "structured event logging"
actually true for anyone tailing server logs, not just API consumers.
"""

from __future__ import annotations

import logging

_CONFIGURED = False


def configure_logging(level: str) -> None:
    global _CONFIGURED
    if _CONFIGURED:
        return
    logging.basicConfig(
        level=level.upper(),
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )
    _CONFIGURED = True
