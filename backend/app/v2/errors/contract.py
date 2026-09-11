"""V2 Error Taxonomy — structured error codes and domain status.

Per 17_INSTITUTIONAL_SECURITY_STANDARD.md §10.14, §12.10:
- Error responses protect confidential information
- Error responses do not expose internal implementation details
- Error responses preserve system integrity
- Error responses support auditability
"""

from __future__ import annotations

from enum import Enum


class V2ErrorCode(str, Enum):
    """Structured V2 error codes."""

    # Data
    DATA_UNAVAILABLE = "data.unavailable"
    DATA_STALE = "data.stale"
    DATA_INSUFFICIENT = "data.insufficient"

    # Authorization
    AUTH_DENIED = "auth.denied"
    AUTH_EXPIRED = "auth.expired"
    AUTH_INSUFFICIENT_PERMISSION = "auth.insufficient_permission"

    # Mode
    MODE_MISMATCH = "mode.mismatch"
    MODE_NOT_AUTHORIZED = "mode.not_authorized"

    # Validation
    VALIDATION_FAILED = "validation.failed"
    TEMPORAL_VIOLATION = "temporal.violation"

    # General
    INTERNAL_ERROR = "internal.error"
    NOT_IMPLEMENTED = "not.implemented"


class V2DomainStatus(str, Enum):
    """Domain status values for V2 API responses."""

    AVAILABLE = "available"
    UNAVAILABLE = "unavailable"
    STALE = "stale"
    DEGRADED = "degraded"
    UNKNOWN = "unknown"
    DENIED = "denied"


class V2Error(Exception):
    """Base V2 error with structured code."""

    def __init__(
        self,
        code: V2ErrorCode,
        detail: str,
        *,
        status_code: int = 400,
    ) -> None:
        super().__init__(detail)
        self.code = code
        self.detail = detail
        self.status_code = status_code


class ModeError(V2Error):
    """Mode-related error."""

    def __init__(self, code: V2ErrorCode, mode: str) -> None:
        super().__init__(
            code=code,
            detail=f"Mode not authorized: {mode}",
            status_code=403,
        )
        self.mode = mode


class PermissionError(V2Error):
    """Permission-related error."""

    def __init__(self, permission: str) -> None:
        super().__init__(
            code=V2ErrorCode.AUTH_INSUFFICIENT_PERMISSION,
            detail="Permission denied",
            status_code=403,
        )
        self.permission = permission  # Internal only, not in response


class TemporalError(V2Error):
    """Temporal validation error."""

    def __init__(self, detail: str) -> None:
        super().__init__(
            code=V2ErrorCode.TEMPORAL_VIOLATION,
            detail=detail,
            status_code=400,
        )


class AuditWriteRejectedError(V2Error):
    """Audit event write refused by classification/secret policy.

    Per ITRGA-ACC-V2-BE-1-INTAKE-001 §2 (R-9.4):
    - BE-1 stores only public/internal/confidential audit classifications.
    - secret-classified writes and payloads bearing unremovable secret
      material are rejected with a safe generic response that never
      echoes the offending value.
    """

    def __init__(self) -> None:
        super().__init__(
            code=V2ErrorCode.VALIDATION_FAILED,
            detail="Audit event rejected by classification policy",
            status_code=400,
        )
