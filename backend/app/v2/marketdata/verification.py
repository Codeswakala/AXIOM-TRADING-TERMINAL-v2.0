"""V2 BE-2 As-Of Verification Record builder (plan E.1 — Option B).

TAMPER-EVIDENCE ONLY. A verification record proves whether the underlying V1
rows in scope changed after record creation. It is NOT a snapshot: it cannot
reconstruct or replay original rows. Every API response carries
``reconstructive: false`` / ``capability: "verification-only"``.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import Any, Sequence

from app.v2.errors.contract import V2Error, V2ErrorCode
from app.v2.temporal.validation import require_utc

CAPABILITY = "verification-only"
RECONSTRUCTIVE = False


@dataclass(frozen=True, slots=True)
class VerificationScopeItem:
    instrument_id: str
    timeframe: str
    source_id: str


def _canonical_row(row: Any) -> str:
    """Canonical serialization of one V1 candle row for hashing.

    Natural key + OHLCV, pipe-joined, Decimal normalized. Deterministic and
    recomputable.
    """
    def dec(value: Any) -> str:
        if value is None:
            return ""
        return str(Decimal(str(value)).normalize())

    return "|".join(
        (
            str(row.market_class),
            str(row.symbol),
            str(row.timeframe),
            row.open_time.isoformat(),
            dec(row.open),
            dec(row.high),
            dec(row.low),
            dec(row.close),
            dec(row.volume),
        )
    )


def compute_content_hash(rows: Sequence[Any]) -> str:
    """SHA-256 over ordered canonical rows (ordered by natural key)."""
    ordered = sorted(
        rows,
        key=lambda r: (str(r.market_class), str(r.symbol), str(r.timeframe), r.open_time),
    )
    digest = hashlib.sha256()
    for row in ordered:
        digest.update(_canonical_row(row).encode("utf-8"))
        digest.update(b"\n")
    return digest.hexdigest()


def validate_scope(scope: Sequence[VerificationScopeItem], as_of: datetime) -> None:
    require_utc(as_of, boundary="as_of")
    if not scope:
        raise V2Error(
            code=V2ErrorCode.VALIDATION_FAILED,
            detail="Verification scope must not be empty",
            status_code=400,
        )
    if len(scope) > 20:
        raise V2Error(
            code=V2ErrorCode.VALIDATION_FAILED,
            detail="Verification scope exceeds bounded size",
            status_code=400,
        )
