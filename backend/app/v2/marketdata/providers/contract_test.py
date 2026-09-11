"""V2 BE-3 P2 bounded contract-test runner — BO-V2-BE-3-P2-001 §§3.4–3.7.

Reachable ONLY through the authenticated endpoint dependency chain.
Implements: 5-precondition default-deny gate, AttemptBudget(35) with fixed
retry allocation, durable pre-call audit sequence with indeterminate
classification, transient-body-only handling, and the bounded request
planner (AUTH / BARS-DEEP / SYMBOL-SWEEP / QUOTE / SYMBOLS-NEG).

No provider payload is ever persisted; bodies are hashed/validated in
memory and discarded (E.5 schema fields only).
"""

from __future__ import annotations

import hashlib
import os
from dataclasses import dataclass
from typing import Any, Final

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.v2_provider import V2MdProvider
from app.v2.audit.contract import V2AuditEventCreate
from app.v2.audit.repository import V2AuditRepository
from app.v2.errors.contract import V2Error
from app.v2.marketdata.providers.contract import PlannedRequest, plan_request
from app.v2.marketdata.providers.twelvedata.normalize import (
    normalize_quote,
    normalize_time_series,
)
from app.v2.marketdata.providers.twelvedata.symbols import CANONICAL_TO_TD

AUTHORITY_REF: Final[str] = "BO-V2-BE-3-P2-001"
MAX_ATTEMPTS: Final[int] = 35

#: §3.6 fixed retry allocation — totals exactly 35 theoretical attempts.
RETRY_ALLOCATION: Final[dict[str, int]] = {
    "AUTH": 0,
    "BARS-DEEP": 3,
    "SYMBOL-SWEEP": 1,
    "QUOTE": 1,
    "SYMBOLS-NEG": 0,
}

BARS_DEEP_INSTRUMENTS: Final[tuple[str, ...]] = (
    "forex.eurusd",  # FX major
    "crypto.btcusd",  # crypto
    "metal.xauusd",  # metal
)

CALL_STATE_COMPLETED = "completed"
CALL_STATE_REFUSED = "refused-before-call"
CALL_STATE_INDETERMINATE = "indeterminate-after-start"


class AttemptBudget:
    """Run-scoped, single-threaded token budget (§3.6). Debits BEFORE every
    network attempt including AUTH probes and retries; refuses at zero."""

    def __init__(self, max_attempts: int = MAX_ATTEMPTS) -> None:
        self._max = max_attempts
        self._used = 0

    @property
    def remaining(self) -> int:
        return self._max - self._used

    def debit(self) -> int | None:
        """Returns attempt number, or None when exhausted (REFUSED)."""
        if self._used >= self._max:
            return None
        self._used += 1
        return self._used


@dataclass(frozen=True, slots=True)
class PreconditionResult:
    name: str
    satisfied: bool


async def check_preconditions(
    session: AsyncSession, *, credential_state: str, mode: str
) -> list[PreconditionResult]:
    """§3.4 — all five must pass; any failure → refusal, no network attempt."""
    results: list[PreconditionResult] = []
    results.append(
        PreconditionResult(
            "authority_ref",
            os.environ.get("AXIOM_TD_P2_AUTHORITY_REF") == AUTHORITY_REF,
        )
    )
    row = (
        await session.execute(
            select(V2MdProvider).where(V2MdProvider.provider_id == "twelvedata")
        )
    ).scalar_one_or_none()
    results.append(
        PreconditionResult(
            "entitlement_verified",
            row is not None and row.entitlement_status == "verified",
        )
    )
    results.append(PreconditionResult("secret_present", credential_state == "present"))
    results.append(
        PreconditionResult(
            "enablement_flag",
            os.environ.get("AXIOM_TD_CONTRACT_TEST_ENABLED", "").lower() == "true",
        )
    )
    results.append(PreconditionResult("mode_valid", mode in ("RESEARCH", "SIMULATION")))
    return results


@dataclass(frozen=True, slots=True)
class PlannedCall:
    request_class: str
    instrument_id: str | None
    planned: PlannedRequest
    expect_error: bool = False


def build_call_plan() -> list[PlannedCall]:
    """§3.7 bounded request planner — 16 planned calls, no more."""
    calls: list[PlannedCall] = []
    # AUTH: valid-key probe + deliberately-absent-key probe
    calls.append(
        PlannedCall(
            "AUTH", None,
            plan_request(
                "/time_series",
                {"symbol": "EUR/USD", "interval": "1min", "outputsize": "1"},
            ),
        )
    )
    calls.append(
        PlannedCall(
            "AUTH", None,
            plan_request(
                "/time_series",
                {"symbol": "EUR/USD", "interval": "1min", "outputsize": "1"},
            ),
            expect_error=True,  # executed WITHOUT key → documented 401 shape
        )
    )
    # BARS-DEEP: 3 representative instruments
    for instrument_id in BARS_DEEP_INSTRUMENTS:
        calls.append(
            PlannedCall(
                "BARS-DEEP", instrument_id,
                plan_request(
                    "/time_series",
                    {
                        "symbol": CANONICAL_TO_TD[instrument_id],
                        "interval": "1min",
                        "outputsize": "5",
                    },
                ),
            )
        )
    # SYMBOL-SWEEP: remaining 9 canonical instruments
    remaining = [i for i in CANONICAL_TO_TD if i not in BARS_DEEP_INSTRUMENTS]
    for instrument_id in sorted(remaining):
        calls.append(
            PlannedCall(
                "SYMBOL-SWEEP", instrument_id,
                plan_request(
                    "/time_series",
                    {
                        "symbol": CANONICAL_TO_TD[instrument_id],
                        "interval": "1min",
                        "outputsize": "1",
                    },
                ),
            )
        )
    # QUOTE
    calls.append(
        PlannedCall(
            "QUOTE", "forex.eurusd", plan_request("/quote", {"symbol": "EUR/USD"})
        )
    )
    # SYMBOLS-NEG: unknown symbol
    calls.append(
        PlannedCall(
            "SYMBOLS-NEG", None,
            plan_request(
                "/time_series",
                {"symbol": "ZZZ/ZZZ", "interval": "1min", "outputsize": "1"},
            ),
            expect_error=True,
        )
    )
    assert len(calls) == 16
    return calls


@dataclass(slots=True)
class CallRecord:
    """E.5 evidence schema — the ONLY persistable per-call artifact."""

    request_class: str
    instrument_id: str | None
    redacted_request: str
    response_status: int | None
    body_sha256: str | None
    schema_verdict: str
    error_category: str
    attempt_number: int | None
    budget_remaining: int
    call_state: str
    latency_ms: float | None


def validate_body(
    body: bytes, call: PlannedCall
) -> tuple[str, str, str]:
    """Transient-body validation: returns (sha256, schema_verdict,
    error_category). The body is NOT retained by this function's caller
    beyond hashing/validation."""
    body_hash = hashlib.sha256(body).hexdigest()
    import json

    try:
        payload = json.loads(body.decode("utf-8"))
    except (ValueError, UnicodeDecodeError):
        return body_hash, "delta-finding:unparseable", "transport"
    try:
        if call.request_class == "QUOTE":
            normalize_quote(payload, requested_instrument_id=call.instrument_id or "")
            return body_hash, "pass", "none"
        if call.request_class in ("BARS-DEEP", "SYMBOL-SWEEP", "AUTH"):
            if call.expect_error:
                # documented error shape expected (401 / unknown symbol)
                if payload.get("status") == "error" or "code" in payload:
                    return body_hash, "pass:error-shape", (
                        "auth" if call.request_class == "AUTH" else "symbol"
                    )
                return body_hash, "delta-finding:expected-error-missing", "none"
            normalize_time_series(
                payload,
                requested_instrument_id=call.instrument_id or "forex.eurusd",
                requested_timeframe="M1",
            )
            return body_hash, "pass", "none"
    except V2Error as exc:
        if exc.status_code == 502:
            return body_hash, "pass:error-shape", "rate-limit" if b"429" in body[:200] else "auth"
        return body_hash, f"delta-finding:{exc.code.value}", "none"
    return body_hash, "delta-finding:unknown-class", "none"


async def _durable_audit(
    session: AsyncSession,
    *,
    action: str,
    actor_id: str,
    mode: str,
    correlation_id: str,
    details: dict[str, Any],
) -> None:
    """Persist one audit event as its OWN COMMITTED transaction unit.

    DEL-001 correction: a flush is NOT durable. Each audit event here is
    appended and then ``session.commit()`` is awaited, ending the current
    transaction — the event is durable in the database before this function
    returns. The caller (contract-test endpoint) invokes this for
    ``call_started`` BEFORE any transport attempt, so no provider contact
    can occur without a committed attributable record. A commit failure
    propagates and the caller refuses/aborts per the approved sequence.
    """
    repo = V2AuditRepository(session)
    await repo.append(
        V2AuditEventCreate(
            domain="v2.marketdata",
            action=action,
            actor_id=actor_id,
            actor_type="operator",
            mode=mode,
            operator_id=actor_id,
            classification="internal",
            correlation_id=correlation_id,
            details=details,
        )
    )
    await session.commit()


def classify_transport_exception(exc: Exception) -> str:
    """Deterministic non-payload error category for transport failures
    (DEL-002): timeout / connection / cancellation-adjacent / unexpected."""
    name = type(exc).__name__.lower()
    if "timeout" in name:
        return "transport:timeout"
    if "connect" in name or "network" in name or "dns" in name:
        return "transport:connection"
    if "cancel" in name:
        return "transport:cancelled"
    return "transport:error"
