"""Small, dependency-free helpers shared across the app.

Nothing that touches config, LLMs, or schemas belongs here — if a helper
needs `Settings` or a Pydantic model, it belongs in the layer that owns
that concept instead.
"""
