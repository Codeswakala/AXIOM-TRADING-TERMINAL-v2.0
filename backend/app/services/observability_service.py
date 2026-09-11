"""Observability service — telemetry, redaction, correlation, and metrics.

This service is intentionally read-only with respect to AXIOM domain state. It
records/exposes operational telemetry and never makes business decisions.
"""

from __future__ import annotations

import os
import re
import time
from collections import defaultdict, deque
from contextvars import ContextVar, Token
from dataclasses import dataclass, field
from threading import Lock
from typing import Any
from uuid import uuid4

SENSITIVE_PATTERNS: tuple[tuple[re.Pattern[str], str], ...] = (
    (
        re.compile(r"(?i)(authorization\s*[:=]\s*bearer\s+)[A-Za-z0-9._~+/=-]+"),
        r"\1[REDACTED]",
    ),
    (re.compile(r"(?i)(bearer\s+)[A-Za-z0-9._~+/=-]+"), r"\1[REDACTED]"),
    (
        re.compile(r"(?i)(password\s*[:=]\s*)([^\s,;}&]+)"),
        r"\1[REDACTED]",
    ),
    (
        re.compile(r"(?i)(refresh_token|access_token|token|ticket)(\s*[:=]\s*)([^\s,;}&]+)"),
        r"\1\2[REDACTED]",
    ),
    (
        re.compile(r"(?i)(postgresql(?:\+asyncpg)?://[^:\s/@]+:)([^@\s]+)(@)"),
        r"\1[REDACTED]\3",
    ),
)

_correlation_id: ContextVar[str | None] = ContextVar("axiom_correlation_id", default=None)


def new_correlation_id() -> str:
    return uuid4().hex


def get_correlation_id() -> str | None:
    return _correlation_id.get()


def set_correlation_id(value: str) -> Token[str | None]:
    return _correlation_id.set(value)


def reset_correlation_id(token: Token[str | None]) -> None:
    _correlation_id.reset(token)


def redact(value: Any) -> Any:
    """Redact secrets from strings and recursively from simple containers."""
    if value is None:
        return None
    if isinstance(value, str):
        redacted = value
        for pattern, replacement in SENSITIVE_PATTERNS:
            redacted = pattern.sub(replacement, redacted)
        return redacted
    if isinstance(value, dict):
        return {str(k): redact(v) for k, v in value.items()}
    if isinstance(value, list):
        return [redact(v) for v in value]
    if isinstance(value, tuple):
        return tuple(redact(v) for v in value)
    return value


@dataclass(slots=True)
class RequestMetric:
    method: str
    path: str
    status_code: int
    duration_ms: float
    correlation_id: str | None
    timestamp: float = field(default_factory=time.time)


class ObservabilityService:
    """Single-responsibility telemetry service."""

    def __init__(self) -> None:
        self._started_at = time.time()
        self._lock = Lock()
        self._requests_total = 0
        self._errors_total = 0
        self._status_counts: dict[str, int] = defaultdict(int)
        self._path_counts: dict[str, int] = defaultdict(int)
        self._latency_total_ms = 0.0
        self._latency_max_ms = 0.0
        self._governance_gate_refusals_total = 0
        self._governance_gate_refusals_by_action: dict[str, int] = defaultdict(int)
        # BO-B-07.3: per-pipeline counters (category → action → count) and
        # resource-utilization series (stdlib-only; no new dependency).
        self._pipeline_counts: dict[str, dict[str, int]] = defaultdict(
            lambda: defaultdict(int)
        )
        self._recent: deque[RequestMetric] = deque(maxlen=100)

    @property
    def uptime_seconds(self) -> float:
        return max(0.0, time.time() - self._started_at)

    def record_http_request(
        self,
        *,
        method: str,
        path: str,
        status_code: int,
        duration_ms: float,
        correlation_id: str | None,
    ) -> None:
        """Record request metrics without storing payloads, headers, or secrets."""
        safe_path = path.split("?", 1)[0]
        metric = RequestMetric(
            method=method.upper(),
            path=safe_path,
            status_code=status_code,
            duration_ms=duration_ms,
            correlation_id=correlation_id,
        )
        with self._lock:
            self._requests_total += 1
            if status_code >= 500:
                self._errors_total += 1
            self._status_counts[str(status_code)] += 1
            self._path_counts[f"{metric.method} {safe_path}"] += 1
            self._latency_total_ms += duration_ms
            self._latency_max_ms = max(self._latency_max_ms, duration_ms)
            self._recent.append(metric)

    def record_governance_gate_refusal(self, *, action: str) -> None:
        """Record a governance gate refusal metric."""
        with self._lock:
            self._governance_gate_refusals_total += 1
            self._governance_gate_refusals_by_action[action] += 1

    def record_pipeline(self, *, category: str, action: str) -> None:
        """BO-B-07.3: count one pipeline event (category/action), no payloads."""
        with self._lock:
            self._pipeline_counts[category][action] += 1

    def pipeline_snapshot(self) -> dict[str, dict[str, int]]:
        with self._lock:
            return {
                category: dict(actions)
                for category, actions in self._pipeline_counts.items()
            }

    def resource_snapshot(self) -> dict[str, float | int | None]:
        """Process resource utilization (stdlib only; None where the platform
        does not expose the value)."""
        import os

        try:
            import resource

            usage = resource.getrusage(resource.RUSAGE_SELF)
            return {
                "process_cpu_user_seconds": usage.ru_utime,
                "process_cpu_system_seconds": usage.ru_stime,
                "process_max_rss_kb": usage.ru_maxrss,
            }
        except (ImportError, OSError):
            return {
                "process_cpu_user_seconds": None,
                "process_cpu_system_seconds": None,
                "process_max_rss_kb": None,
                "pid": os.getpid(),
            }

    def snapshot(self) -> dict[str, Any]:
        """Return read-only telemetry snapshot."""
        with self._lock:
            average_latency = (
                self._latency_total_ms / self._requests_total if self._requests_total else 0.0
            )
            recent = [
                {
                    "method": item.method,
                    "path": item.path,
                    "status_code": item.status_code,
                    "duration_ms": round(item.duration_ms, 3),
                    "correlation_id": item.correlation_id,
                }
                for item in list(self._recent)[-10:]
            ]
            return {
                "process": {
                    "pid": os.getpid(),
                    "uptime_seconds": round(self.uptime_seconds, 3),
                },
                "http": {
                    "requests_total": self._requests_total,
                    "errors_total": self._errors_total,
                    "status_counts": dict(self._status_counts),
                    "path_counts": dict(self._path_counts),
                    "latency_avg_ms": round(average_latency, 3),
                    "latency_max_ms": round(self._latency_max_ms, 3),
                    "recent": recent,
                },
                "governance": {
                    "gate_refusals_total": self._governance_gate_refusals_total,
                    "gate_refusals_by_action": dict(self._governance_gate_refusals_by_action),
                },
                # BO-B-07.3: per-pipeline counters + resource utilization.
                "pipelines": {
                    category: dict(actions)
                    for category, actions in self._pipeline_counts.items()
                },
                "resources": self.resource_snapshot(),
            }


_observability_service = ObservabilityService()


def get_observability_service() -> ObservabilityService:
    return _observability_service
