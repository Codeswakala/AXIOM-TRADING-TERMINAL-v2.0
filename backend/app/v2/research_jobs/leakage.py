"""BE-7 U-2 structural leakage guards — P-8 (plan Part 5, G-1…G-5).

Pure validation functions; no I/O, no clock (as_of/now always parameters).
The V1 ChronologyGuard/TemporalSplitEngine lineage (pinned §1.0) is the
vocabulary reference; these guards are the band's own enforced structure.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from datetime import datetime, timedelta


class LeakageRefused(Exception):
    """Typed leakage refusal — carries the guard id and reasons."""

    def __init__(self, guard: str, reasons: list) -> None:
        self.guard = guard
        self.reasons = reasons
        super().__init__(f"leakage guard {guard} refused: {reasons}")


@dataclass(frozen=True)
class ReplayWindow:
    """The as-of model (plan Part 2): as_of >= window_end enforced."""

    window_start: datetime
    window_end: datetime
    as_of: datetime

    def validate(self) -> None:
        reasons = []
        if self.window_start >= self.window_end:
            reasons.append({"failing": "window_order",
                            "start": self.window_start.isoformat(),
                            "end": self.window_end.isoformat()})
        if self.as_of < self.window_end:
            reasons.append({"failing": "as_of_before_window_end",
                            "as_of": self.as_of.isoformat(),
                            "window_end": self.window_end.isoformat(),
                            "rule": "as_of >= window_end (plan Part 2)"})
        if reasons:
            raise LeakageRefused("G-1:window", reasons)


def filter_bars_g1(bars: list[dict], window: ReplayWindow) -> list[dict]:
    """G-1 — the as-of cutoff at input assembly: only bars with
    open_time <= as_of AND inside the window survive. This function is the
    ONLY path from raw bars into a replay input set."""
    window.validate()
    kept = [
        b for b in bars
        if window.window_start <= b["open_time"] <= window.window_end
        and b["open_time"] <= window.as_of
    ]
    return sorted(kept, key=lambda b: b["open_time"])


def validate_horizon_g3(*, label_horizon: timedelta, embargo: timedelta,
                        window: ReplayWindow) -> None:
    """G-3 — label-horizon/embargo rejection at submission: a horizon
    whose labels would extend past window_end - embargo is refused."""
    latest_label_ts = window.window_end - embargo
    if label_horizon > timedelta(0):
        # a decision at t needs labels at t + horizon; the last legal
        # decision time is latest_label_ts - horizon, which must lie
        # inside the window
        last_legal = latest_label_ts - label_horizon
        if last_legal <= window.window_start:
            raise LeakageRefused("G-3:horizon", [{
                "failing": "label_horizon_past_embargo",
                "label_horizon_s": label_horizon.total_seconds(),
                "embargo_s": embargo.total_seconds(),
                "window_end": window.window_end.isoformat(),
                "rule": "horizon must leave a non-empty decision window"
                        " before window_end - embargo",
            }])


def validate_decision_ordering_g4(ledger: list[dict]) -> None:
    """G-4 — decision-vs-data timestamp ordering: every recorded decision's
    data refs must have open_time <= decision_ts."""
    violations = []
    for entry in ledger:
        decision_ts = entry["decision_ts"]
        for ref_ts in entry.get("data_ref_ts", []):
            if ref_ts > decision_ts:
                violations.append({
                    "decision_ts": decision_ts.isoformat(),
                    "data_ref_ts": ref_ts.isoformat()})
    if violations:
        raise LeakageRefused("G-4:ordering", violations)


def content_hash(bars: list[dict], window: ReplayWindow,
                 series_refs: dict) -> str:
    """The registered-input content hash (G-5 basis; REQ-1.3)."""
    payload = {
        "window": [window.window_start.isoformat(),
                   window.window_end.isoformat()],
        "series_refs": series_refs,
        "bars": [
            {"open_time": b["open_time"].isoformat(),
             "open": str(b["open"]), "high": str(b["high"]),
             "low": str(b["low"]), "close": str(b["close"]),
             "volume": str(b.get("volume", "0"))}
            for b in bars
        ],
    }
    return hashlib.sha256(
        json.dumps(payload, sort_keys=True, separators=(",", ":"))
        .encode("utf-8")).hexdigest()


def verify_content_g5(*, stored_hash: str, recomputed_hash: str) -> None:
    """G-5 — registered-input immutability re-proof at replay time:
    mismatch = typed refusal, never silent inclusion (also the ingest-lag
    control per PRV §5.4 — a bar ingested after as_of changes the content
    hash and refuses)."""
    if stored_hash != recomputed_hash:
        raise LeakageRefused("G-5:content", [{
            "failing": "content_hash_mismatch",
            "stored": stored_hash, "recomputed": recomputed_hash}])
