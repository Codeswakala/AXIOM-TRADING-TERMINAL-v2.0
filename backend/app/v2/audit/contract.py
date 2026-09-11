"""V2 Audit Contract — append-only audit event definitions.

Per 17_INSTITUTIONAL_SECURITY_STANDARD.md:
- Append-only (DB trigger enforced)
- Sensitive fields redacted before storage
- Operator-scoped reads
- Classification-based access
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any


@dataclass(frozen=True, slots=True)
class V2AuditEventCreate:
    """Contract for creating a V2 audit event."""

    domain: str
    action: str
    actor_id: str
    actor_type: str  # "operator", "system", "job"
    mode: str  # "RESEARCH" or "SIMULATION"
    resource_type: str | None = None
    resource_id: str | None = None
    details: dict[str, Any] | None = None
    classification: str = "internal"  # "public", "internal", "confidential", "secret"
    operator_id: str | None = None
    correlation_id: str | None = None
    causation_id: str | None = None


@dataclass(frozen=True, slots=True)
class V2AuditEventRead:
    """Contract for reading a V2 audit event."""

    id: str
    domain: str
    action: str
    actor_id: str
    actor_type: str
    mode: str
    resource_type: str | None
    resource_id: str | None
    details: dict[str, Any] | None
    classification: str
    operator_id: str | None
    correlation_id: str | None
    causation_id: str | None
    created_at: datetime


# Classification levels for access control
CLASSIFICATION_LEVELS = {
    "public": 0,
    "internal": 1,
    "confidential": 2,
    "secret": 3,
}

# BE-1 storable classifications (ITRGA-ACC-V2-BE-1-INTAKE-001 §2 R-9.4):
# secret-classified audit events are refused at write time. Storage or
# retrieval of SAL-4/secret audit content requires a separate approved
# security design and Build Order.
STORABLE_CLASSIFICATIONS = frozenset({"public", "internal", "confidential"})

# Role clearance levels
ROLE_CLEARANCE = {
    "admin": 3,  # Can read up to secret
    "operator": 1,  # Can read up to internal only
}


def get_role_clearance(role: str) -> int:
    """Get the clearance level for a role."""
    return ROLE_CLEARANCE.get(role, 0)


def can_access_classification(
    user_role: str,
    resource_classification: str,
) -> bool:
    """Check if a user can access a resource based on classification."""
    user_level = get_role_clearance(user_role)
    resource_level = CLASSIFICATION_LEVELS.get(resource_classification, 0)
    return user_level >= resource_level


def filter_details_by_classification(
    details: dict | None,
    classification: str,
    user_role: str,
) -> dict | None:
    """Filter/redact details based on classification and user role.

    If user cannot access the classification, details are redacted.
    """
    if details is None:
        return None
    if can_access_classification(user_role, classification):
        return details
    # Redact details for insufficient clearance
    return {"_redacted": True, "reason": "Insufficient clearance for this classification level"}
