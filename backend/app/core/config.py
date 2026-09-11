"""Environment-aware application configuration (W0-U08 hardened)."""

from __future__ import annotations

from functools import lru_cache
from typing import Literal

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

EnvironmentName = Literal["development", "testing", "staging", "production"]

# Known insecure defaults — must never be accepted outside explicit local-dev allow.
INSECURE_JWT_MARKERS = (
    "CHANGE-ME",
    "change-me",
    "secret",
    "dev-only",
    "not-for-production",
    "axiom-jwt-secret",
)

DEFAULT_BOOTSTRAP_PASSWORD = "admin123"


class Settings(BaseSettings):
    """Runtime settings for the AXIOM backend."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_prefix="AXIOM_",
        case_sensitive=False,
        extra="ignore",
    )

    app_name: str = Field(default="AXIOM")
    environment: EnvironmentName = Field(default="development")
    debug: bool = Field(default=False)
    api_prefix: str = Field(default="/api/v1")
    host: str = Field(default="0.0.0.0")
    port: int = Field(default=8000, ge=1, le=65535)
    log_level: str = Field(default="INFO")
    log_json: bool = Field(default=False)
    cors_origins: str = Field(default="http://localhost:5173,http://127.0.0.1:5173")
    version: str = Field(default="0.62.0")

    database_url: str = Field(default="sqlite+aiosqlite:///./axiom_dev.db")
    database_echo: bool = Field(default=False)
    database_pool_size: int = Field(default=5, ge=1, le=100)
    database_max_overflow: int = Field(default=10, ge=0, le=100)
    database_pool_timeout: int = Field(default=30, ge=1)
    # W0-U08: default False — production must use Alembic only (OBS-4).
    # Tests set AXIOM_DATABASE_AUTO_CREATE_SCHEMA=true explicitly.
    database_auto_create_schema: bool = Field(default=False)

    # Auth — no insecure defaults baked as silent production path
    jwt_secret_key: str = Field(
        default="",
        description="HMAC secret for JWT. Required; set AXIOM_JWT_SECRET_KEY.",
    )
    jwt_algorithm: str = Field(default="HS256")
    access_token_expire_minutes: int = Field(default=30, ge=1)
    refresh_token_expire_days: int = Field(default=7, ge=1)
    # Explicit local-dev escape hatch for weak secrets / bootstrap (must be true intentionally)
    allow_insecure_dev: bool = Field(
        default=False,
        description="When true (and env=development|testing), allow weak JWT / default bootstrap.",
    )
    bootstrap_admin_username: str = Field(default="")
    bootstrap_admin_password: str = Field(default="")
    bootstrap_admin_enabled: bool = Field(
        default=False,
        description="Create bootstrap admin only when true AND credentials are explicitly set.",
    )
    protect_ingestion_stats: bool = Field(default=True)
    # WS: prefer short-lived ticket over JWT in query string
    ws_ticket_expire_seconds: int = Field(default=60, ge=10, le=300)
    ws_allow_query_jwt: bool = Field(
        default=False,
        description="Legacy: allow ?token=<access JWT>. Default false after W0-U08.",
    )

    # Advisory signal guardrails (W3-U03)
    signal_max_input_staleness_seconds: int = Field(default=300, ge=0)
    signal_validity_seconds: int = Field(default=300, ge=0)
    signal_calibration_warning_ece_threshold: float = Field(default=0.15, ge=0.0, le=1.0)
    # BO-B-05: monitoring alert emission thresholds (bounded, configurable).
    monitoring_alert_staleness_threshold_seconds: int = Field(
        default=3600, ge=60, le=604800
    )
    monitoring_alert_dedup_cooldown_seconds: int = Field(
        default=86400, ge=60, le=604800
    )
    # BO-B-07.1: rate limiting (closes TD-W7-U07-RATE-GUARD). In-memory
    # sliding-window, operator-keyed; applied to the authenticated write
    # surfaces only. Fail-safe: an invalid window/ceiling while enabled
    # denies (never silently open).
    rate_limit_enabled: bool = Field(default=True)
    rate_limit_window_seconds: int = Field(default=60, ge=1, le=86400)
    rate_limit_global_ceiling: int = Field(default=1200, ge=1, le=1_000_000)
    rate_limit_per_route_ceiling: int = Field(default=400, ge=1, le=1_000_000)
    rate_limit_admin_allowlist: str = Field(default="")
    # BO-B-07.2: baseline security headers (each independently togglable).
    security_headers_enabled: bool = Field(default=True)
    security_hsts_enabled: bool = Field(default=False)
    security_csp_enabled: bool = Field(default=True)
    security_csp_value: str = Field(
        default="default-src 'none'; frame-ancestors 'none'; base-uri 'none'"
    )

    # Live market
    live_market_enabled: bool = Field(default=True)
    live_market_auto_start: bool = Field(default=False)
    live_market_class: str = Field(default="forex")
    live_market_symbol: str = Field(default="EURUSD")
    # DATA-P01: the simulated feed now covers all eleven SUPPORTED_INSTRUMENTS
    # (8 forex pairs + 3 crypto pairs). Reference data for the simulator only.
    live_market_symbols: str = Field(
        default="EURUSD,GBPUSD,USDJPY,AUDUSD,USDCAD,USDCHF,NZDUSD,EURGBP,BTCUSD,ETHUSD,SOLUSD"
    )
    live_market_timeframe: str = Field(default="M1")
    live_market_interval_seconds: float = Field(default=2.0, ge=0.05, le=3600.0)

    @property
    def live_market_symbols_list(self) -> list[str]:
        raw = self.live_market_symbols or self.live_market_symbol
        symbols = [s.strip().upper() for s in raw.split(",") if s.strip()]
        return symbols or [self.live_market_symbol.upper()]

    @field_validator("log_level")
    @classmethod
    def normalize_log_level(cls, value: str) -> str:
        return value.upper()

    @property
    def cors_origin_list(self) -> list[str]:
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]

    @property
    def is_production(self) -> bool:
        return self.environment == "production"

    @property
    def is_testing(self) -> bool:
        return self.environment == "testing"

    @property
    def is_sqlite(self) -> bool:
        return self.database_url.startswith("sqlite")

    @property
    def is_postgres(self) -> bool:
        return self.database_url.startswith("postgresql")

    @property
    def database_backend_name(self) -> str:
        if self.is_postgres:
            return "postgresql"
        if self.is_sqlite:
            return "sqlite"
        return "other"

    @property
    def jwt_secret_is_insecure(self) -> bool:
        secret = (self.jwt_secret_key or "").strip()
        if len(secret) < 32:
            return True
        lower = secret.lower()
        return any(m.lower() in lower for m in INSECURE_JWT_MARKERS)

    def validate_security_or_raise(self) -> None:
        """Refuse to run with weak secrets outside explicit local/test allow."""
        # Production: never allow insecure
        if self.is_production:
            if self.jwt_secret_is_insecure or not self.jwt_secret_key.strip():
                raise RuntimeError(
                    "AXIOM_JWT_SECRET_KEY is missing or weak. "
                    "Production requires a secret with length >= 32 and no default markers."
                )
            if self.database_auto_create_schema:
                raise RuntimeError(
                    "AXIOM_DATABASE_AUTO_CREATE_SCHEMA must be false in production "
                    "(use Alembic only)."
                )
            if self.allow_insecure_dev:
                raise RuntimeError("AXIOM_ALLOW_INSECURE_DEV cannot be true in production.")
            return

        # Staging: same as production for secrets
        if self.environment == "staging":
            if self.jwt_secret_is_insecure or not self.jwt_secret_key.strip():
                raise RuntimeError(
                    "AXIOM_JWT_SECRET_KEY is missing or weak for staging."
                )
            return

        # development: require secret unless allow_insecure_dev
        if self.environment == "development":
            if self.jwt_secret_is_insecure or not self.jwt_secret_key.strip():
                if not self.allow_insecure_dev:
                    raise RuntimeError(
                        "AXIOM_JWT_SECRET_KEY is missing or weak. "
                        "Set a strong secret (len>=32), or set AXIOM_ALLOW_INSECURE_DEV=true "
                        "for local development only."
                    )
            return

        # Testing allows empty secret only through explicit local/test escape hatch.
        if self.is_testing:
            if self.jwt_secret_is_insecure or not self.jwt_secret_key.strip():
                if not self.allow_insecure_dev:
                    raise RuntimeError(
                        "Testing requires AXIOM_JWT_SECRET_KEY or AXIOM_ALLOW_INSECURE_DEV=true."
                    )


@lru_cache
def get_settings() -> Settings:
    return Settings()


def clear_settings_cache() -> None:
    get_settings.cache_clear()


def load_and_validate_settings() -> Settings:
    """Load settings and enforce security policy (call at process start)."""
    clear_settings_cache()
    settings = get_settings()
    settings.validate_security_or_raise()
    return settings
