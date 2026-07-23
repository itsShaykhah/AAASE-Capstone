"""Pydantic/TypedDict data contracts shared across the system.

Every module boundary in this project (agent -> agent, graph -> API,
API -> UI) passes one of these schemas rather than a loose dict, so that
`X_json_schema()` doubles as living documentation and structured-output
validation (see app/guardrails/output_validation.py) has something concrete
to check against.
"""
