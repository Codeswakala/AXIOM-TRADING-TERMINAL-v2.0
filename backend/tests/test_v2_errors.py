"""V2 Errors Tests — error taxonomy and response builders."""

from __future__ import annotations

from app.v2.errors.contract import (
    ModeError,
    PermissionError,
    TemporalError,
    V2DomainStatus,
    V2Error,
    V2ErrorCode,
)


class TestV2ErrorCode:
    """Test V2 error codes."""

    def test_error_codes_are_strings(self):
        """Error codes are string enums."""
        assert isinstance(V2ErrorCode.DATA_UNAVAILABLE, str)
        assert V2ErrorCode.DATA_UNAVAILABLE == "data.unavailable"

    def test_mode_error_codes_exist(self):
        """Mode error codes exist."""
        assert V2ErrorCode.MODE_NOT_AUTHORIZED == "mode.not_authorized"
        assert V2ErrorCode.MODE_MISMATCH == "mode.mismatch"

    def test_auth_error_codes_exist(self):
        """Auth error codes exist."""
        assert V2ErrorCode.AUTH_DENIED == "auth.denied"
        assert V2ErrorCode.AUTH_INSUFFICIENT_PERMISSION == "auth.insufficient_permission"


class TestV2DomainStatus:
    """Test V2 domain status values."""

    def test_domain_statuses(self):
        """All domain statuses are defined."""
        assert V2DomainStatus.AVAILABLE == "available"
        assert V2DomainStatus.UNAVAILABLE == "unavailable"
        assert V2DomainStatus.STALE == "stale"
        assert V2DomainStatus.DEGRADED == "degraded"
        assert V2DomainStatus.UNKNOWN == "unknown"
        assert V2DomainStatus.DENIED == "denied"


class TestV2Errors:
    """Test V2 error classes."""

    def test_v2_error_has_code_and_detail(self):
        """V2Error has code and detail."""
        err = V2Error(V2ErrorCode.DATA_UNAVAILABLE, "No data", status_code=404)
        assert err.code == V2ErrorCode.DATA_UNAVAILABLE
        assert err.detail == "No data"
        assert err.status_code == 404

    def test_mode_error_has_mode(self):
        """ModeError includes mode value."""
        err = ModeError(V2ErrorCode.MODE_NOT_AUTHORIZED, "PAPER")
        assert err.mode == "PAPER"
        assert err.status_code == 403

    def test_permission_error_has_permission(self):
        """PermissionError includes permission string."""
        err = PermissionError("v2.audit.read_all")
        assert err.permission == "v2.audit.read_all"
        assert err.status_code == 403

    def test_temporal_error_has_detail(self):
        """TemporalError includes detail."""
        err = TemporalError("Naive datetime rejected")
        assert err.code == V2ErrorCode.TEMPORAL_VIOLATION
        assert err.status_code == 400
