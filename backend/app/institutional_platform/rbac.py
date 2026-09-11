"""Default-deny RBAC and route-scope contracts for Wave 7."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from fastapi import HTTPException, status

from app.auth.dependencies import CurrentOperatorDep
from app.db.models.operator import Operator

InstitutionalPermission = Literal[
    "institutional.route_inventory.read",
    "institutional.rbac.read",
    "institutional.operator_scope.read",
    "institutional.api_catalogue.read",
    "institutional.plugin_contracts.read",
]

FORBIDDEN_PERMISSION_MARKERS = (
    "gate",
    "execution",
    "execute",
    "order",
    "broker",
    "account",
    "position",
    "live",
    "capital",
    "margin",
)

INSTITUTIONAL_ROLE_PERMISSIONS: dict[str, frozenset[InstitutionalPermission]] = {
    "admin": frozenset(
        {
            "institutional.route_inventory.read",
            "institutional.rbac.read",
            "institutional.operator_scope.read",
            "institutional.api_catalogue.read",
            "institutional.plugin_contracts.read",
        }
    ),
    "operator": frozenset(
        {
            "institutional.operator_scope.read",
            "institutional.api_catalogue.read",
            "institutional.plugin_contracts.read",
        }
    ),
}

INSTITUTIONAL_ROUTE_INVENTORY: tuple[dict[str, object], ...] = (
    {
        "path": "/api/v1/institutional-platform/route-inventory",
        "methods": ["GET"],
        "permission": "institutional.route_inventory.read",
        "description": "Read institutional platform route inventory.",
    },
    {
        "path": "/api/v1/institutional-platform/rbac/permissions",
        "methods": ["GET"],
        "permission": "institutional.rbac.read",
        "description": "Read default-deny institutional RBAC vocabulary.",
    },
    {
        "path": "/api/v1/institutional-platform/api-catalogue",
        "methods": ["GET"],
        "permission": "institutional.api_catalogue.read",
        "description": "Read authenticated versioned research API catalogue.",
    },
    {
        "path": "/api/v1/institutional-platform/plugin-contracts",
        "methods": ["GET"],
        "permission": "institutional.plugin_contracts.read",
        "description": "Read published plugin extension contracts and capability allowlist.",
    },
    {
        "path": "/api/v1/institutional-platform/portfolio-research/dashboard",
        "methods": ["GET"],
        "permission": "institutional.operator_scope.read",
        "description": "Read current operator portfolio research dashboard.",
    },
    {
        "path": "/api/v1/institutional-platform/portfolio-research/report",
        "methods": ["GET"],
        "permission": "institutional.operator_scope.read",
        "description": "Read current operator advanced research report preview.",
    },
    {
        "path": "/api/v1/institutional-platform/operator-scope-records",
        "methods": ["GET"],
        "permission": "institutional.operator_scope.read",
        "description": "Read current operator's institutional scope record only.",
    },
    {
        "path": "/api/v1/institutional-platform/operator-scope-records/{operator_id}",
        "methods": ["GET"],
        "permission": "institutional.operator_scope.read",
        "description": "Read one institutional scope record if it belongs to current operator.",
    },
    {
        "path": "/api/v1/institutional-platform/workspace-preferences",
        "methods": ["GET", "POST"],
        "permission": "institutional.operator_scope.read",
        "description": "List or create current operator workspace preferences.",
    },
    {
        "path": "/api/v1/institutional-platform/workspace-preferences/{preference_id}",
        "methods": ["GET", "PUT"],
        "permission": "institutional.operator_scope.read",
        "description": "Read or update one current-operator workspace preference.",
    },
    {
        "path": "/api/v1/institutional-platform/research-management",
        "methods": ["GET"],
        "permission": "institutional.operator_scope.read",
        "description": "Read current-operator reference-only research management bundle.",
    },
    {
        "path": "/api/v1/institutional-platform/research-collections",
        "methods": ["GET", "POST"],
        "permission": "institutional.operator_scope.read",
        "description": "List or create current-operator research collections.",
    },
    {
        "path": "/api/v1/institutional-platform/research-collections/{collection_id}",
        "methods": ["GET", "DELETE"],
        "permission": "institutional.operator_scope.read",
        "description": "Read or delete one current-operator research collection.",
    },
    {
        "path": "/api/v1/institutional-platform/research-collections/{collection_id}/members",
        "methods": ["GET", "POST"],
        "permission": "institutional.operator_scope.read",
        "description": "List or add reference-only artifact members.",
    },
    {
        "path": (
            "/api/v1/institutional-platform/research-collections/"
            "{collection_id}/members/{member_id}"
        ),
        "methods": ["DELETE"],
        "permission": "institutional.operator_scope.read",
        "description": "Remove one reference-only artifact member.",
    },
    {
        "path": "/api/v1/institutional-platform/research-tags",
        "methods": ["GET", "POST"],
        "permission": "institutional.operator_scope.read",
        "description": "List or create current-operator research tags.",
    },
    {
        "path": "/api/v1/institutional-platform/research-tags/{tag_id}",
        "methods": ["GET", "DELETE"],
        "permission": "institutional.operator_scope.read",
        "description": "Read or delete one current-operator research tag.",
    },
)


@dataclass(frozen=True, slots=True)
class InstitutionalScopeRecord:
    """Derived per-operator institutional scope record backed by operators."""

    operator_id: str
    username: str
    role: str
    record_type: str = "institutional_operator_scope"
    research_status: str = "research_only"

    @classmethod
    def from_operator(cls, operator: Operator) -> "InstitutionalScopeRecord":
        return cls(operator_id=operator.id, username=operator.username, role=operator.role)


def permissions_for_role(role: str) -> frozenset[InstitutionalPermission]:
    """Return permissions for a role; unknown roles default-deny."""
    return INSTITUTIONAL_ROLE_PERMISSIONS.get(role, frozenset())


def assert_permission_vocabulary_safe() -> None:
    """Refuse permission vocabularies that encode forbidden execution powers."""
    for permission_set in INSTITUTIONAL_ROLE_PERMISSIONS.values():
        for permission in permission_set:
            lower = permission.lower()
            if any(marker in lower for marker in FORBIDDEN_PERMISSION_MARKERS):
                raise ValueError(f"INSTITUTIONAL_PERMISSION_FORBIDDEN:{permission}")


def require_institutional_permission(permission: InstitutionalPermission):
    async def _checker(operator: CurrentOperatorDep) -> Operator:
        assert_permission_vocabulary_safe()
        if permission not in permissions_for_role(operator.role):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Institutional permission denied by default-deny policy",
            )
        return operator

    return _checker

