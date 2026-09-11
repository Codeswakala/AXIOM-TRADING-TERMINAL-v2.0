"""V2 Identifiers Tests — ID generation and validation."""

from __future__ import annotations

from uuid import UUID

import pytest

from app.v2.identifiers import new_correlation_id, new_id, validate_id


class TestV2Identifiers:
    """Test V2 identifier generation and validation."""

    def test_new_id_returns_valid_uuid(self):
        """new_id returns a valid UUID string."""
        id_val = new_id()
        UUID(id_val)  # Should not raise

    def test_new_id_is_unique(self):
        """new_id generates unique IDs."""
        ids = {new_id() for _ in range(100)}
        assert len(ids) == 100

    def test_new_correlation_id_returns_hex(self):
        """new_correlation_id returns a hex string."""
        corr_id = new_correlation_id()
        assert len(corr_id) == 32  # UUID4 hex is 32 chars
        int(corr_id, 16)  # Should not raise

    def test_validate_id_accepts_valid_uuid(self):
        """validate_id accepts valid UUID strings."""
        valid_id = new_id()
        assert validate_id(valid_id) == valid_id

    def test_validate_id_rejects_invalid(self):
        """validate_id rejects invalid UUID strings."""
        with pytest.raises(ValueError, match="Invalid ID format"):
            validate_id("not-a-uuid")
