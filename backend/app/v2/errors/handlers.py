"""V2 Error Handlers — secure error response builders.

Per 17_INSTITUTIONAL_SECURITY_STANDARD.md §10.14:
- 500 errors never expose stack traces to clients
- Internal details are logged but never returned
"""

from __future__ import annotations

from datetime import datetime, timezone

from fastapi.responses import JSONResponse

from app.core.logging import get_logger
from app.services.observability_service import get_correlation_id
from app.v2.errors.contract import V2Error, V2ErrorCode

logger = get_logger(__name__, category="SECURITY")


def v2_error_response(error: V2Error) -> JSONResponse:
    """Build a structured V2 error response."""
    return JSONResponse(
        status_code=error.status_code,
        content={
            "error_code": error.code.value,
            "detail": error.detail,
            "correlation_id": get_correlation_id(),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        },
    )


def v2_internal_error_response(exc: Exception) -> JSONResponse:
    """Build a safe 500 error response that never exposes internal details."""
    logger.exception("Unhandled V2 exception: %s", type(exc).__name__)
    return JSONResponse(
        status_code=500,
        content={
            "error_code": V2ErrorCode.INTERNAL_ERROR.value,
            "detail": "Internal server error",
            "correlation_id": get_correlation_id(),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        },
    )
