"""V2 RBAC Tests — permission enforcement, default-deny, forbidden markers."""

from __future__ import annotations

from app.v2.rbac.permissions import (
    V2_FORBIDDEN_PERMISSION_MARKERS,
    V2_PERMISSION_SEED,
    assert_permission_vocabulary_safe,
    has_permission,
    permissions_for_role,
)


class TestV2RBAC:
    """Test V2 RBAC permissions."""

    def test_admin_has_all_permissions(self):
        """Admin role has all V2 permissions."""
        admin_perms = permissions_for_role("admin")
        assert "v2.mode.read" in admin_perms
        assert "v2.capability.read" in admin_perms
        assert "v2.audit.read" in admin_perms
        assert "v2.audit.read_all" in admin_perms
        assert "v2.lineage.read" in admin_perms
        assert "v2.lineage.read_all" in admin_perms
        assert "v2.error.read" in admin_perms

    def test_operator_has_limited_permissions(self):
        """Operator role has limited V2 permissions."""
        operator_perms = permissions_for_role("operator")
        assert "v2.mode.read" in operator_perms
        assert "v2.capability.read" in operator_perms
        assert "v2.audit.read" in operator_perms
        assert "v2.lineage.read" in operator_perms
        assert "v2.error.read" in operator_perms

    def test_operator_lacks_read_all(self):
        """Operator role does NOT have read_all permissions."""
        operator_perms = permissions_for_role("operator")
        assert "v2.audit.read_all" not in operator_perms
        assert "v2.lineage.read_all" not in operator_perms

    def test_unknown_role_default_deny(self):
        """Unknown roles get empty permissions (default-deny)."""
        unknown_perms = permissions_for_role("unknown")
        assert len(unknown_perms) == 0

    def test_has_permission_returns_true_for_valid(self):
        """has_permission returns True for valid role/permission."""
        assert has_permission("admin", "v2.mode.read") is True
        assert has_permission("operator", "v2.mode.read") is True

    def test_has_permission_returns_false_for_missing(self):
        """has_permission returns False for missing permission."""
        assert has_permission("operator", "v2.audit.read_all") is False
        assert has_permission("unknown", "v2.mode.read") is False

    def test_vocabulary_safe(self):
        """Permission vocabulary does not contain forbidden markers."""
        # Should not raise
        assert_permission_vocabulary_safe()

    def test_forbidden_markers_include_execution_terms(self):
        """Forbidden markers include execution-related terms."""
        assert "execution" in V2_FORBIDDEN_PERMISSION_MARKERS
        assert "order" in V2_FORBIDDEN_PERMISSION_MARKERS
        assert "broker" in V2_FORBIDDEN_PERMISSION_MARKERS
        assert "account" in V2_FORBIDDEN_PERMISSION_MARKERS
        assert "position" in V2_FORBIDDEN_PERMISSION_MARKERS
        assert "live" in V2_FORBIDDEN_PERMISSION_MARKERS

    def test_permission_seed_data_not_empty(self):
        """Permission seed data is not empty."""
        assert len(V2_PERMISSION_SEED) > 0

    def test_permission_seed_has_admin_and_operator(self):
        """Permission seed data includes admin and operator roles."""
        roles = {p["role"] for p in V2_PERMISSION_SEED}
        assert "admin" in roles
        assert "operator" in roles
