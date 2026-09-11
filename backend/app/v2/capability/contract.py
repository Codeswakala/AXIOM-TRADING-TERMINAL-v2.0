"""V2 Capability Contract — read-only seeded capability registry.

No runtime mutation. No enabled column. No feature flags.
Registry is seeded from seed.py during migration.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True, slots=True)
class V2CapabilityRecordRead:
    """Contract for reading a V2 capability record."""

    id: str
    capability_id: str
    domain: str
    band: str
    maturity: str
    artifact_status: str
    version: str
    created_at: datetime


# Maturity states
class CapabilityMaturity:
    DESIGNED = "designed"
    IMPLEMENTED = "implemented"
    TESTED = "tested"
    VERIFIED = "verified"
    APPROVED = "approved"
    AUTHORIZED = "authorized"
    PRODUCTION_CERTIFIED = "production_certified"
