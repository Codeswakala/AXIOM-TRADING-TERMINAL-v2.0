"""BO-B-07.1 — bounded in-memory sliding-window rate limiter.

Closes the W7-U07 rate-guard deferral (TD-W7-U07-RATE-GUARD) with a
dependency/storage-spiked design: pure standard library, per-process
in-memory state, operator-keyed, per-route + global ceilings.

Fail-safe semantics (binding): an invalid configuration (non-positive
window/ceiling) DENIES every request — misconfiguration can never silently
open the guard.

Scope note (disclosed residual deferral): the state is per-process; a
multi-instance deployment would need a shared store (a separately-governed
future unit). No new dependency; no schema migration; state is removable by
process restart.
"""

from __future__ import annotations

import threading
import time
from collections import deque

# The BO-B-07.1 write surfaces (operator-authenticated POST/PUT/PATCH/DELETE
# under these prefixes). Auth login is deliberately excluded (it is not an
# authenticated write surface; it 401s unauth requests itself).
RATE_LIMITED_PREFIXES: tuple[str, ...] = (
    "/api/v1/ingestion/",
    "/api/v1/intelligence/",
    "/api/v1/collaboration/",
    "/api/v1/alerts/",
)


def route_group(path: str) -> str | None:
    """Return the rate-limit group for a path, or None if not scoped.

    The API router is mounted twice (bare + ``/api/v1``); both mounts are
    guarded by normalizing the prefix away before matching.
    """
    normalized = path
    if normalized.startswith("/api/v1/"):
        normalized = normalized[len("/api/v1"):]
    for prefix in RATE_LIMITED_PREFIXES:
        family = prefix[len("/api/v1"):]
        if normalized.startswith(family):
            return family
    return None


class SlidingWindowRateLimiter:
    """Monotonic-clock sliding window with a hard per-key ceiling."""

    def __init__(self, *, window_seconds: int, ceiling: int) -> None:
        self._window = float(window_seconds)
        self._ceiling = int(ceiling)
        self._hits: dict[str, deque[float]] = {}
        self._lock = threading.Lock()

    def config_valid(self) -> bool:
        return self._window >= 1.0 and self._ceiling >= 1

    def allow(self, key: str) -> bool:
        if not self.config_valid():
            return False  # fail-safe: deny on misconfiguration
        now = time.monotonic()
        with self._lock:
            window = self._hits.setdefault(key, deque())
            while window and now - window[0] > self._window:
                window.popleft()
            if len(window) >= self._ceiling:
                return False
            window.append(now)
            return True

    def reset(self) -> None:
        with self._lock:
            self._hits.clear()


class OperatorRateGuard:
    """Per-operator guard: every write must pass BOTH the global bucket and
    its route group bucket (per-route + global ceilings, per BO-B-07.1)."""

    def __init__(
        self,
        *,
        window_seconds: int,
        global_ceiling: int,
        per_route_ceiling: int,
    ) -> None:
        self._global = SlidingWindowRateLimiter(
            window_seconds=window_seconds, ceiling=global_ceiling
        )
        self._per_route: dict[str, SlidingWindowRateLimiter] = {
            prefix[len("/api/v1"):]: SlidingWindowRateLimiter(
                window_seconds=window_seconds, ceiling=per_route_ceiling
            )
            for prefix in RATE_LIMITED_PREFIXES
        }

    def config_valid(self) -> bool:
        return self._global.config_valid() and all(
            limiter.config_valid() for limiter in self._per_route.values()
        )

    def allow(self, *, operator: str, group: str) -> bool:
        if not self.config_valid():
            return False  # fail-safe
        route_limiter = self._per_route.get(group)
        if route_limiter is None:
            return False
        if not route_limiter.allow(operator):
            return False
        return self._global.allow(operator)
