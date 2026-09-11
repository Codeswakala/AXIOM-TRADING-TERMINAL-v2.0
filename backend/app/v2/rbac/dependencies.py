"""V2 RBAC Dependencies — FastAPI dependencies for permission enforcement.

Per 17_INSTITUTIONAL_SECURITY_STANDARD.md Part VI:
- Default Deny
- Explicit Permission Grant
- Least Privilege
- Sensitive reads are audited
"""

from __future__ import annotations

from typing import Annotated

from fastapi import Depends, HTTPException, Request, status

from app.auth.dependencies import CurrentOperatorDep
from app.db.models.operator import Operator
from app.v2.rbac.permissions import has_permission


def require_v2_permission(permission: str):
    """Dependency factory: require a specific V2 permission.

    Public denial is generic ("Permission denied"). The required permission,
    actor, role, route, correlation ID, and decision are retained in internal
    security logs only (DEF-BE1-04).
    """

    async def _checker(request: Request, operator: CurrentOperatorDep) -> Operator:
        if not has_permission(operator.role, permission):
            # Log internally but don't expose permission name to client
            from app.core.logging import get_logger
            logger = get_logger(__name__, category="SECURITY")
            logger.warning(
                "V2 permission denied: permission=%s role=%s operator=%s "
                "route=%s method=%s correlation_id=%s decision=deny",
                permission,
                operator.role,
                operator.username,
                request.url.path,
                request.method,
                getattr(request.state, "correlation_id", None),
            )
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Permission denied",
            )
        return operator

    return _checker


# Pre-built dependencies for common V2 permissions
RequireV2ModeRead = Annotated[
    Operator, Depends(require_v2_permission("v2.mode.read"))
]
RequireV2CapabilityRead = Annotated[
    Operator, Depends(require_v2_permission("v2.capability.read"))
]
RequireV2AuditRead = Annotated[
    Operator, Depends(require_v2_permission("v2.audit.read"))
]
RequireV2AuditReadAll = Annotated[
    Operator, Depends(require_v2_permission("v2.audit.read_all"))
]
RequireV2LineageRead = Annotated[
    Operator, Depends(require_v2_permission("v2.lineage.read"))
]
RequireV2LineageReadAll = Annotated[
    Operator, Depends(require_v2_permission("v2.lineage.read_all"))
]
RequireV2ErrorRead = Annotated[
    Operator, Depends(require_v2_permission("v2.error.read"))
]
RequireV2MarketDataRead = Annotated[
    Operator, Depends(require_v2_permission("v2.marketdata.read"))
]
RequireV2MarketDataReadAll = Annotated[
    Operator, Depends(require_v2_permission("v2.marketdata.read_all"))
]
RequireV2MarketDataVerify = Annotated[
    Operator, Depends(require_v2_permission("v2.marketdata.verify"))
]
RequireV2MarketDataCatalogRefresh = Annotated[
    Operator, Depends(require_v2_permission("v2.marketdata.catalog.refresh"))
]
RequireV2ProviderRead = Annotated[
    Operator, Depends(require_v2_permission("v2.marketdata.provider.read"))
]
RequireV2ProviderReadHistory = Annotated[
    Operator, Depends(require_v2_permission("v2.marketdata.provider.read_history"))
]
