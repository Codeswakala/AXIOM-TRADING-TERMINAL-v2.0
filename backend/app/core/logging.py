"""Structured logging foundation for AXIOM.

Log categories align with the Development Authority manual:
SYSTEM, API, DATABASE, ML, MARKET, BROKER, SECURITY, GOVERNANCE, AUDIT.
"""

from __future__ import annotations

import json
import logging
import sys
from datetime import datetime, timezone
from typing import Any

from app.core.config import Settings
from app.services.observability_service import get_correlation_id, redact


class CategoryLoggerAdapter(logging.LoggerAdapter):
    """Attach a governance log category to every record."""

    def process(self, msg: str, kwargs: Any) -> tuple[str, Any]:
        extra = kwargs.setdefault("extra", {})
        extra.setdefault("category", self.extra.get("category", "SYSTEM"))
        extra.setdefault("component", self.extra.get("category", "SYSTEM"))
        return msg, kwargs


class JsonFormatter(logging.Formatter):
    """JSON log formatter with correlation ID and redaction."""

    def format(self, record: logging.LogRecord) -> str:
        exception = None
        if record.exc_info:
            exception = redact(self.formatException(record.exc_info))
        payload = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "component": getattr(record, "component", getattr(record, "category", "SYSTEM")),
            "category": getattr(record, "category", "SYSTEM"),
            "correlation_id": getattr(record, "correlation_id", None) or get_correlation_id(),
            "message": redact(record.getMessage()),
        }
        if exception:
            payload["exception"] = exception
        return json.dumps(payload, ensure_ascii=True)


class TextFormatter(logging.Formatter):
    """Human-readable formatter for local development."""

    def format(self, record: logging.LogRecord) -> str:
        category = getattr(record, "category", "SYSTEM")
        timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        correlation = getattr(record, "correlation_id", None) or get_correlation_id() or "-"
        message = redact(record.getMessage())
        return (
            f"{timestamp} | {record.levelname:<8} | {category:<10} | "
            f"cid={correlation} | {record.name} | {message}"
        )


def configure_logging(settings: Settings) -> None:
    """Configure root logging once for the application process."""
    root = logging.getLogger()
    root.handlers.clear()
    root.setLevel(settings.log_level)

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(settings.log_level)
    handler.setFormatter(JsonFormatter() if settings.log_json else TextFormatter())
    root.addHandler(handler)

    # Reduce noise from third-party libraries in development.
    logging.getLogger("uvicorn.access").setLevel(logging.INFO)
    logging.getLogger("uvicorn.error").setLevel(logging.INFO)


def get_logger(name: str, category: str = "SYSTEM") -> CategoryLoggerAdapter:
    """Return a category-aware logger adapter."""
    return CategoryLoggerAdapter(logging.getLogger(name), {"category": category})
