"""AXIOM FastAPI application entrypoint (W0-U08 security enforcement)."""

from __future__ import annotations

import sys
import time
from contextlib import asynccontextmanager
from pathlib import Path
from typing import AsyncIterator

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

from app import __version__
from app.api.router import api_router
from app.auth.security import safe_decode
from app.auth.service import AuthService
from app.core.config import clear_settings_cache, get_settings, load_and_validate_settings
from app.core.logging import configure_logging, get_logger
from app.core.rate_limit import OperatorRateGuard, route_group
from app.db.session import close_db, create_schema, get_session_factory, init_db
from app.market.live_service import get_live_market_service
from app.services.observability_service import (
    get_observability_service,
    new_correlation_id,
    reset_correlation_id,
    set_correlation_id,
)
from app.v2.mode.contract import get_mode as get_v2_mode
from app.v2.errors.contract import V2Error, ModeError, PermissionError, TemporalError
from app.v2.errors.handlers import v2_error_response, v2_internal_error_response

logger = get_logger(__name__, category="SYSTEM")

REPO_ROOT = Path(__file__).resolve().parents[2]
FRONTEND_DIST = REPO_ROOT / "frontend" / "dist"


def pipeline_event(method: str, path: str) -> tuple[str, str] | None:
    """BO-B-07.3 — pipeline taxonomy derived from the request shape.

    Returns (category, action) for the platform's governed pipelines; None
    for plain HTTP traffic (which is already covered by the HTTP metrics).
    """
    if method.upper() != "POST":
        return None
    # Both router mounts (bare + /api/v1) share the taxonomy.
    normalized = path
    if normalized.startswith("/api/v1/"):
        normalized = normalized[len("/api/v1"):]
    if normalized.startswith("/intelligence/"):
        families = {
            "/correlation-reports": "correlation_report_generated",
            "/regime-reports": "regime_report_generated",
            "/scenario-reports": "scenario_report_generated",
            "/portfolio-risk-reports": "portfolio_risk_report_generated",
            "/signal-validation-reports": "signal_validation_report_generated",
        }
        for family, action in families.items():
            if normalized == f"/intelligence{family}":
                return ("intelligence", action)
        return None
    if normalized == "/alerts/check":
        return ("monitoring", "alert_check_executed")
    if normalized == "/alerts/inference-health":
        return ("monitoring", "inference_health_reported")
    if normalized == "/collaboration/assistant-respond":
        return ("assistant", "ask_responded")
    if normalized in ("/ingestion/csv", "/ingestion/sample"):
        return ("market", "ingestion_requested")
    return None


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncIterator[None]:
    try:
        settings = load_and_validate_settings()
    except RuntimeError as exc:
        logger.error("Security configuration refused: %s", exc)
        raise SystemExit(str(exc)) from exc

    configure_logging(settings)
    if settings.allow_insecure_dev:
        logger.warning(
            "AXIOM_ALLOW_INSECURE_DEV=true — local/test escape hatch active; "
            "never enable outside isolated development"
        )
    logger.info(
        "Starting %s v%s env=%s db=%s",
        settings.app_name,
        settings.version,
        settings.environment,
        settings.database_backend_name,
    )
    init_db(settings)
    # Alembic is schema authority; create_all only when explicitly enabled (tests/dev)
    if settings.database_auto_create_schema:
        if settings.is_production:
            raise SystemExit("AUTO_CREATE_SCHEMA forbidden in production")
        await create_schema()

    factory = get_session_factory()
    async with factory() as session:
        auth = AuthService(session, settings)
        try:
            await auth.ensure_bootstrap_admin()
            await session.commit()
        except RuntimeError as exc:
            await session.rollback()
            logger.error("Bootstrap refused: %s", exc)
            raise SystemExit(str(exc)) from exc

    live = get_live_market_service()
    if settings.live_market_enabled and settings.live_market_auto_start:
        await live.start()
        logger.info("Live market auto-started")

    # V2 mode initialization
    v2_mode = get_v2_mode()
    logger.info("V2 mode initialized: %s", v2_mode)

    yield

    try:
        await live.stop()
    except Exception:  # noqa: BLE001
        logger.exception("Error stopping live market service")
    await close_db()
    clear_settings_cache()
    logger.info("Shutting down %s", settings.app_name)


def create_app() -> FastAPI:
    # Validate early so import-time misconfig fails fast in production entrypoints.
    # Tests set env before import/create_app.
    try:
        settings = load_and_validate_settings()
    except RuntimeError as exc:
        # Allow module import for tooling; re-validate on lifespan/create in workers.
        # For create_app used by uvicorn, fail hard.
        if "pytest" not in sys.modules:
            raise SystemExit(str(exc)) from exc
        from app.core.config import get_settings as _fallback_get_settings

        clear_settings_cache()
        settings = _fallback_get_settings()

    application = FastAPI(
        title=settings.app_name,
        version=__version__,
        description=(
            "AXIOM — Institutional multi-market AI research and trading intelligence platform. "
            "Wave 7 Institutional Platform: closeout and whole-project "
            "completion checkpoint."
        ),
        lifespan=lifespan,
        docs_url="/docs" if not settings.is_production else None,
        redoc_url="/redoc" if not settings.is_production else None,
    )

    application.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origin_list,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # BO-B-07.1: operator-keyed rate guard on the authenticated write
    # surfaces. Unauth requests pass through (the endpoints 401 themselves);
    # fail-safe deny on misconfiguration; minimal 429 body (no identity).
    # The guard instance is keyed by its configuration so runtime config
    # changes rebuild it while in-flight state persists across requests
    # sharing the same configuration.
    _rate_guard_state: dict[str, object] = {"config_key": None, "guard": None}

    def _rate_guard(guard_settings) -> OperatorRateGuard:
        config_key = (
            guard_settings.rate_limit_window_seconds,
            guard_settings.rate_limit_global_ceiling,
            guard_settings.rate_limit_per_route_ceiling,
        )
        if _rate_guard_state["config_key"] != config_key:
            _rate_guard_state["guard"] = OperatorRateGuard(
                window_seconds=guard_settings.rate_limit_window_seconds,
                global_ceiling=guard_settings.rate_limit_global_ceiling,
                per_route_ceiling=guard_settings.rate_limit_per_route_ceiling,
            )
            _rate_guard_state["config_key"] = config_key
        return _rate_guard_state["guard"]  # type: ignore[return-value]

    @application.middleware("http")
    async def rate_limit_middleware(request: Request, call_next):
        guard_settings = get_settings()
        if (
            not guard_settings.rate_limit_enabled
            or request.method not in {"POST", "PUT", "PATCH", "DELETE"}
        ):
            return await call_next(request)
        group = route_group(request.url.path)
        if group is None:
            return await call_next(request)
        authorization = request.headers.get("authorization") or ""
        operator_id = None
        if authorization.lower().startswith("bearer "):
            claims = safe_decode(authorization.split(" ", 1)[1], guard_settings)
            if claims is not None:
                # The token carries the operator username as an extra claim;
                # the allowlist is therefore username-based (the BO's "small
                # admin allowlist" intent), with sub as fallback.
                operator_id = str(claims.get("username") or claims.get("sub") or "")
        if not operator_id:
            return await call_next(request)  # unauthenticated → the endpoint 401s
        allowlist = {
            item.strip()
            for item in guard_settings.rate_limit_admin_allowlist.split(",")
            if item.strip()
        }
        if operator_id in allowlist:
            return await call_next(request)
        if not _rate_guard(guard_settings).allow(operator=operator_id, group=group):
            return JSONResponse(
                status_code=429,
                content={"detail": "Rate limit exceeded. Retry after the window."},
            )
        return await call_next(request)

    # BO-B-07.2: baseline security headers. Each header is independently
    # configurable; HSTS is off unless HTTPS is configured; CSP is applied to
    # API responses (the swagger/docs surfaces require inline assets and are
    # excluded with that justification — and are disabled in production).
    @application.middleware("http")
    async def security_headers_middleware(request: Request, call_next):
        response = await call_next(request)
        header_settings = get_settings()
        if not header_settings.security_headers_enabled:
            return response
        response.headers.setdefault("X-Content-Type-Options", "nosniff")
        response.headers.setdefault("X-Frame-Options", "DENY")
        response.headers.setdefault("Referrer-Policy", "strict-origin-when-cross-origin")
        if header_settings.security_hsts_enabled:
            response.headers.setdefault(
                "Strict-Transport-Security",
                "max-age=31536000; includeSubDomains",
            )
        frontend_path = (
            FRONTEND_DIST.is_dir()
            and request.url.path not in ("/api", "/api/", "/docs", "/redoc", "/openapi.json", "/health", "/ready")
            and not request.url.path.startswith(("/api/", "/ws", "/system"))
        )
        if header_settings.security_csp_enabled and frontend_path:
            response.headers.setdefault(
                "Content-Security-Policy",
                "default-src 'self'; base-uri 'self'; frame-ancestors 'none'; "
                "object-src 'none'; script-src 'self'; style-src 'self' 'unsafe-inline'; "
                "img-src 'self' data: blob:; font-src 'self' data:; connect-src 'self' ws: wss:",
            )
        elif header_settings.security_csp_enabled and request.url.path not in (
            "/docs",
            "/redoc",
            "/openapi.json",
        ):
            response.headers.setdefault(
                "Content-Security-Policy", header_settings.security_csp_value
            )
        return response


    @application.middleware("http")
    async def observability_middleware(request: Request, call_next):
        correlation_id = request.headers.get("x-correlation-id") or new_correlation_id()
        token = set_correlation_id(correlation_id)
        started = time.perf_counter()
        status_code = 500
        path = request.url.path
        try:
            response = await call_next(request)
            status_code = response.status_code
            response.headers["X-Correlation-ID"] = correlation_id
            return response
        except Exception:
            logger.exception("Unhandled HTTP exception method=%s path=%s", request.method, path)
            raise
        finally:
            duration_ms = (time.perf_counter() - started) * 1000.0
            get_observability_service().record_http_request(
                method=request.method,
                path=path,
                status_code=status_code,
                duration_ms=duration_ms,
                correlation_id=correlation_id,
            )
            # BO-B-07.3: per-pipeline counters derived from the request shape
            # (no router edits required — the middleware owns the taxonomy).
            pipeline = pipeline_event(method=request.method, path=path)
            if pipeline is not None:
                category, action = pipeline
                get_observability_service().record_pipeline(
                    category=category, action=action
                )
                logger.info(
                    "Pipeline event category=%s action=%s cid=%s",
                    category,
                    action,
                    correlation_id,
                )
            logger.info(
                "HTTP request method=%s path=%s status=%s duration_ms=%.2f",
                request.method,
                path,
                status_code,
                duration_ms,
            )
            reset_correlation_id(token)

    # V2 mode initialization
    application.state.v2_mode = get_v2_mode()

    # V2 error handlers — structured safe responses for V2 errors
    @application.exception_handler(V2Error)
    async def v2_error_handler(request: Request, exc: V2Error):
        return v2_error_response(exc)

    @application.exception_handler(ModeError)
    async def v2_mode_error_handler(request: Request, exc: ModeError):
        return v2_error_response(exc)

    @application.exception_handler(PermissionError)
    async def v2_permission_error_handler(request: Request, exc: PermissionError):
        return v2_error_response(exc)

    @application.exception_handler(TemporalError)
    async def v2_temporal_error_handler(request: Request, exc: TemporalError):
        return v2_error_response(exc)

    # V2 internal-error containment (DEF-BE1-05): unhandled exceptions on V2
    # routes return the safe structured V2 internal-error contract instead of
    # propagating to default/V1 behaviour. Scoped strictly to V2 paths so V1
    # error behaviour is unchanged.
    v2_path_prefixes = ("/v2", f"{settings.api_prefix}/v2")

    @application.middleware("http")
    async def v2_internal_error_middleware(request: Request, call_next):
        path = request.url.path
        if not any(
            path == prefix or path.startswith(prefix + "/")
            for prefix in v2_path_prefixes
        ):
            return await call_next(request)
        try:
            return await call_next(request)
        except V2Error as exc:
            # Structured V2 errors keep their registered safe contract.
            return v2_error_response(exc)
        except Exception as exc:  # noqa: BLE001 — containment boundary
            return v2_internal_error_response(exc)

    application.include_router(api_router)
    application.include_router(api_router, prefix=settings.api_prefix)

    @application.get("/api", tags=["root"], include_in_schema=False)
    @application.get("/api/", tags=["root"], include_in_schema=False)
    async def api_root() -> dict[str, str]:
        return {
            "service": settings.app_name,
            "version": settings.version,
            "status": "online",
            "docs": "/docs",
            "health": "/health",
            "ready": "/ready",
            "auth_login": f"{settings.api_prefix}/auth/login",
            "live_status": f"{settings.api_prefix}/market/live/status",
            "charts": "/charts",
        }

    if FRONTEND_DIST.is_dir() and (FRONTEND_DIST / "index.html").is_file():
        assets_dir = FRONTEND_DIST / "assets"
        if assets_dir.is_dir():
            application.mount(
                "/assets",
                StaticFiles(directory=str(assets_dir)),
                name="frontend-assets",
            )

        @application.get("/{full_path:path}", include_in_schema=False)
        async def spa_fallback(full_path: str) -> FileResponse:
            reserved = ("api", "docs", "redoc", "openapi.json", "health", "ready", "ws")
            first = full_path.split("/", 1)[0]
            if first in reserved:
                return FileResponse(FRONTEND_DIST / "index.html")
            candidate = FRONTEND_DIST / full_path
            if candidate.is_file():
                return FileResponse(candidate)
            return FileResponse(FRONTEND_DIST / "index.html")

        logger.info("Frontend dist mounted from %s", FRONTEND_DIST)
    else:

        @application.get("/", tags=["root"])
        async def root() -> dict[str, str]:
            return {
                "service": settings.app_name,
                "version": settings.version,
                "status": "online",
                "docs": "/docs",
                "health": "/health",
                "ready": "/ready",
                "auth_login": f"{settings.api_prefix}/auth/login",
                "charts": "/charts",
                "frontend": "not built — run: cd frontend && npm run build",
            }

    return application


app = create_app()
