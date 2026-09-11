"""V2 Identifiers — versioned domain IDs, correlation, causation, actor context.

All V2 identifiers are UUID-based. Correlation IDs propagate through requests.
Causation IDs link triggering events to resulting events.
Actor IDs identify the authenticated identity performing an action.
"""

from __future__ import annotations

from uuid import uuid4


def new_id() -> str:
    """Generate a new V2 domain identifier (UUID4)."""
    return str(uuid4())


def new_correlation_id() -> str:
    """Generate a new correlation ID for request tracing."""
    return uuid4().hex


def validate_id(value: str) -> str:
    """Validate that a string is a valid UUID. Returns the value if valid."""
    from uuid import UUID

    try:
        UUID(value)
        return value
    except ValueError as exc:
        raise ValueError(f"Invalid ID format: {value}") from exc
