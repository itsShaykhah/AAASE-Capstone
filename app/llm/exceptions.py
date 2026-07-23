"""Exception types owned by the LLM layer."""

from __future__ import annotations


class LLMConfigurationError(Exception):
    """A provider was selected but is missing required configuration (e.g. an API key)."""


class LLMInvocationError(Exception):
    """A provider call failed at the transport/API level (timeout, rate limit, etc.)."""
