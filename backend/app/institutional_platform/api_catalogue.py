"""Versioned research API catalogue generation (W7-U04)."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Iterable

from fastapi.routing import APIRoute
from starlette.routing import BaseRoute

CATALOGUE_VERSION = "w7-u04.research_api_catalogue.v1"
API_ROUTE_VERSION = "v1"

CATALOGUED_TAGS = frozenset(
    {
        "advisory-analytics",
        "advisory-signals",
        "collaboration",
        "execution-research",
        "institutional-intelligence",
        "institutional-platform",
        "monitoring-alerts",
    }
)

MUTATION_METHODS = frozenset({"POST", "PUT", "PATCH", "DELETE"})


@dataclass(frozen=True, slots=True)
class ApiCatalogueRoute:
    """Public descriptor for one authenticated research API route."""

    path: str
    methods: tuple[str, ...]
    permission: str
    version: str
    description: str
    tags: tuple[str, ...]
    auth_required: bool
    operator_scoped: bool
    mutation: bool


def build_api_catalogue(routes: Iterable[BaseRoute], *, api_prefix: str) -> dict[str, object]:
    """Build a sanitized catalogue of versioned research/institutional API routes."""

    entries = sorted(
        (
            _route_descriptor(route, effective_path=effective_path)
            for route, effective_path in _iter_api_routes(routes)
            if _is_catalogued_route(route, effective_path=effective_path, api_prefix=api_prefix)
        ),
        key=lambda item: (item.path, item.methods),
    )
    return {
        "service": "institutional_platform_api_catalogue",
        "catalogue_version": CATALOGUE_VERSION,
        "api_version": API_ROUTE_VERSION,
        "routes": [asdict(entry) for entry in entries],
        "route_count": len(entries),
        "actuation_surface_present": False,
        "governance_gate_capability_present": False,
        "abuse_guard": {
            "status": "deferred",
            "reason": (
                "No rate limiter added in W7-U04; authenticated access and "
                "role/operator scopes remain active."
            ),
        },
        "persistence": {
            "catalogue_table_persisted": False,
            "alembic_head_expected": "20260717_0037",
        },
    }


def _iter_api_routes(
    routes: Iterable[BaseRoute], *, prefix: str = ""
) -> Iterable[tuple[APIRoute, str]]:
    for route in routes:
        if isinstance(route, APIRoute):
            yield route, f"{prefix}{route.path}"
            continue
        if type(route).__name__ == "_IncludedRouter":
            include_context = getattr(route, "include_context", None)
            original_router = getattr(route, "original_router", None)
            nested_routes = getattr(original_router, "routes", None)
            nested_prefix = getattr(include_context, "prefix", "") if include_context else ""
            if nested_routes is not None:
                yield from _iter_api_routes(nested_routes, prefix=f"{prefix}{nested_prefix}")


def _is_catalogued_route(
    route: BaseRoute, *, effective_path: str, api_prefix: str
) -> bool:
    if not isinstance(route, APIRoute):
        return False
    if not effective_path.startswith(api_prefix):
        return False
    return bool(CATALOGUED_TAGS.intersection(route.tags or ()))


def _route_descriptor(route: APIRoute, *, effective_path: str) -> ApiCatalogueRoute:
    methods = tuple(sorted(method for method in route.methods if method not in {"HEAD", "OPTIONS"}))
    tags = tuple(sorted(str(tag) for tag in route.tags or ()))
    return ApiCatalogueRoute(
        path=effective_path,
        methods=methods,
        permission=_permission_for_route(route.path, methods=methods),
        version=API_ROUTE_VERSION,
        description=route.summary or route.name,
        tags=tags,
        auth_required=True,
        operator_scoped=_operator_scoped(route.path),
        mutation=any(method in MUTATION_METHODS for method in methods),
    )


def _permission_for_route(path: str, *, methods: tuple[str, ...]) -> str:
    if path.endswith("/api-catalogue"):
        return "institutional.api_catalogue.read"
    if "/institutional-platform/route-inventory" in path:
        return "institutional.route_inventory.read"
    if "/institutional-platform/rbac/permissions" in path:
        return "institutional.rbac.read"
    if "GET" in methods and len(methods) == 1:
        return "operator.authenticated.read"
    return "operator.authenticated.write"


def _operator_scoped(path: str) -> bool:
    operator_scoped_markers = (
        "/institutional-platform/operator-scope-records",
        "/institutional-platform/workspace-preferences",
        "/institutional-platform/research-collections",
        "/institutional-platform/research-tags",
        "/institutional-platform/portfolio-research",
        "/collaboration/chart-annotations",
        "/collaboration/trade-plans",
        "/collaboration/journal-entries",
        "/execution-research/simulated-runs",
        "/execution-research/simulated-ledger-entries",
        "/execution-research/execution-experiments",
    )
    return any(marker in path for marker in operator_scoped_markers)
