"""FastAPI gateway.

This is the "BACKEND" box in the architecture diagram: Request Validation
(FastAPI's own Pydantic parsing) -> Guardrail Manager -> Coordinator. The
API layer's only job is HTTP plumbing — request/response shapes, status
codes, dependency wiring — it never contains agent or LLM logic itself.
"""
