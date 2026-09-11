"""V2 Audit Tests — redaction, immutability, operator-scoping."""

from __future__ import annotations

from app.v2.audit.redaction import has_sensitive_content, redact


class TestV2AuditRedaction:
    """Test V2 audit redaction."""

    def test_redacts_bearer_token(self):
        """Bearer tokens are redacted."""
        value = "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.test"
        result = redact(value)
        assert "eyJ" not in result
        assert "[REDACTED]" in result

    def test_redacts_password(self):
        """Passwords are redacted."""
        value = "password=supersecret123"
        result = redact(value)
        assert "supersecret123" not in result
        assert "[REDACTED]" in result

    def test_redacts_api_key(self):
        """API keys are redacted."""
        value = "api_key=sk-1234567890abcdef"
        result = redact(value)
        assert "sk-1234567890abcdef" not in result
        assert "[REDACTED]" in result

    def test_redacts_db_connection_string(self):
        """DB connection strings are redacted."""
        value = "postgresql+asyncpg://user:secretpass@localhost/db"
        result = redact(value)
        assert "secretpass" not in result
        assert "[REDACTED]" in result

    def test_redacts_nested_dict(self):
        """Redaction works recursively on nested dicts."""
        value = {"auth": "Bearer abc123def456", "nested": {"key": "password=supersecret"}}
        result = redact(value)
        assert "[REDACTED]" in result["auth"]
        assert "[REDACTED]" in result["nested"]["key"]

    def test_redacts_list(self):
        """Redaction works on lists."""
        value = ["password=secret", "normal_value"]
        result = redact(value)
        assert result[0] == "password=[REDACTED]"
        assert result[1] == "normal_value"

    def test_preserves_none(self):
        """None is preserved."""
        assert redact(None) is None

    def test_preserves_non_string(self):
        """Non-string values are preserved."""
        assert redact(42) == 42
        assert redact(True) is True

    def test_has_sensitive_content_detects_bearer(self):
        """has_sensitive_content detects bearer tokens."""
        assert has_sensitive_content("Authorization: Bearer abc123") is True

    def test_has_sensitive_content_rejects_clean(self):
        """has_sensitive_content returns False for clean strings."""
        assert has_sensitive_content("normal log message") is False

class TestV2AuditClassification:
    """Unit tests for clearance and classification filtering (DEF-BE1-03)."""

    def test_admin_clearance_is_secret(self):
        from app.v2.audit.contract import get_role_clearance
        assert get_role_clearance("admin") == 3

    def test_operator_clearance_is_internal(self):
        from app.v2.audit.contract import get_role_clearance
        assert get_role_clearance("operator") == 1

    def test_unknown_role_clearance_is_zero(self):
        from app.v2.audit.contract import get_role_clearance
        assert get_role_clearance("stranger") == 0

    def test_admin_can_access_all_classifications(self):
        from app.v2.audit.contract import can_access_classification
        for classification in ("public", "internal", "confidential", "secret"):
            assert can_access_classification("admin", classification) is True

    def test_operator_cannot_access_confidential_or_secret(self):
        from app.v2.audit.contract import can_access_classification
        assert can_access_classification("operator", "public") is True
        assert can_access_classification("operator", "internal") is True
        assert can_access_classification("operator", "confidential") is False
        assert can_access_classification("operator", "secret") is False

    def test_filter_details_returns_full_for_authorized(self):
        from app.v2.audit.contract import filter_details_by_classification
        details = {"key": "value"}
        assert filter_details_by_classification(details, "internal", "operator") == details

    def test_filter_details_redacts_for_unauthorized(self):
        from app.v2.audit.contract import filter_details_by_classification
        result = filter_details_by_classification({"key": "value"}, "confidential", "operator")
        assert result == {
            "_redacted": True,
            "reason": "Insufficient clearance for this classification level",
        }

    def test_filter_details_preserves_none(self):
        from app.v2.audit.contract import filter_details_by_classification
        assert filter_details_by_classification(None, "confidential", "operator") is None

    def test_storable_classifications_exclude_secret(self):
        from app.v2.audit.contract import STORABLE_CLASSIFICATIONS
        assert STORABLE_CLASSIFICATIONS == {"public", "internal", "confidential"}
        assert "secret" not in STORABLE_CLASSIFICATIONS
