"""Application configuration package.

Everything that varies between environments (API keys, providers, model
names, ports) lives here and nowhere else. No other module should read
`os.environ` directly — they should import `get_settings()` instead. That
single chokepoint is what lets us swap providers/models purely through
configuration, per the project's LLM design requirement.
"""

from app.config.settings import Settings, get_settings

__all__ = ["Settings", "get_settings"]
