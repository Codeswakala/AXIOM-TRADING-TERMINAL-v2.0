"""V2 BE-3 P1 resilience state machine — PURE IN-MEMORY fixture logic.

PLAN-006 boundary: transitions are NOT persisted, NOT audited, and introduce
NO new exception type or schema change. Thresholds come only from
SyntheticPolicy fixtures labelled ``synthetic:test-policy`` — never provider
figures (PLAN-003). Persisted provider-health events are P2+ scope.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from app.v2.temporal.validation import require_utc, utc_now


@dataclass(frozen=True, slots=True)
class SyntheticPolicy:
    """Test-only policy. ``label`` MUST be 'synthetic:test-policy'."""

    label: str
    max_requests_per_window: int
    window_seconds: int
    max_retries: int
    backoff_base_seconds: float
    breaker_failure_threshold: int
    breaker_cooldown_seconds: int

    def __post_init__(self) -> None:
        if self.label != "synthetic:test-policy":
            raise ValueError(
                "P1 resilience accepts synthetic test policies only (PLAN-003)"
            )


class TokenBucket:
    """Pre-emptive rate limiter. Exhaustion → honest refusal, never queuing."""

    def __init__(self, policy: SyntheticPolicy) -> None:
        self._policy = policy
        self._window_start: datetime | None = None
        self._count = 0

    def try_acquire(self, *, now: datetime | None = None) -> bool:
        current = now if now is not None else utc_now()
        require_utc(current, boundary="rate-limit clock")
        if (
            self._window_start is None
            or (current - self._window_start).total_seconds() >= self._policy.window_seconds
        ):
            self._window_start = current
            self._count = 0
        if self._count >= self._policy.max_requests_per_window:
            return False
        self._count += 1
        return True


def backoff_schedule(policy: SyntheticPolicy) -> list[float]:
    """Deterministic exponential schedule (jitter excluded for testability)."""
    return [
        policy.backoff_base_seconds * (2**attempt)
        for attempt in range(policy.max_retries)
    ]


def should_retry(status_class: str, attempt: int, policy: SyntheticPolicy) -> bool:
    """Retry transport/5xx/429 only; never 4xx entitlement/auth errors."""
    if attempt >= policy.max_retries:
        return False
    return status_class in {"transport", "5xx", "429"}


class CircuitBreaker:
    """CLOSED → OPEN → HALF_OPEN → CLOSED. In-memory only (PLAN-006)."""

    CLOSED = "closed"
    OPEN = "open"
    HALF_OPEN = "half_open"

    def __init__(self, policy: SyntheticPolicy) -> None:
        self._policy = policy
        self._state = self.CLOSED
        self._consecutive_failures = 0
        self._opened_at: datetime | None = None

    @property
    def state(self) -> str:
        return self._state

    def allow(self, *, now: datetime | None = None) -> bool:
        current = now if now is not None else utc_now()
        if self._state == self.CLOSED:
            return True
        if self._state == self.OPEN:
            assert self._opened_at is not None
            if (current - self._opened_at).total_seconds() >= self._policy.breaker_cooldown_seconds:
                self._state = self.HALF_OPEN
                return True  # single probe
            return False
        return True  # HALF_OPEN probe in flight

    def record_success(self) -> None:
        self._consecutive_failures = 0
        self._state = self.CLOSED
        self._opened_at = None

    def record_failure(self, *, now: datetime | None = None) -> None:
        current = now if now is not None else utc_now()
        self._consecutive_failures += 1
        if self._state == self.HALF_OPEN or (
            self._consecutive_failures >= self._policy.breaker_failure_threshold
        ):
            self._state = self.OPEN
            self._opened_at = current

    def degraded_view(self) -> dict[str, str]:
        """Honest degraded-state mapping onto BE-2 vocabulary."""
        if self._state == self.OPEN:
            return {"availability": "unavailable", "freshness": "unknown"}
        if self._state == self.HALF_OPEN:
            return {"availability": "partial", "freshness": "unknown"}
        return {"availability": "available", "freshness": "fresh"}


@dataclass(slots=True)
class SourceHealth:
    """In-memory health surface (P1: fixture-derived only; not persisted)."""

    state: str = "unknown"  # healthy | degraded | outage | unknown
    rolling_latency_ms: float | None = None
    last_success_at: datetime | None = None
