"""BE-10 typed contracts (BO B-1.2; laws L5/L6).

Closed verdict enum — STATE NOUNS ONLY (the wording law): every verdict
names what IS, never what to do. No verb of action (buy/sell/add/reduce/
close/enter/exit) may appear in the vocabulary, the field names, or the
response surfaces; the wording-law scan enforces this over the band.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Final

# L5: the closed verdict enum (BO-sealed; sealed order preserved).
ALIGNMENT_VERDICTS: Final = (
    "aligned",                 # held direction agrees with the live signal
    "opposed",                 # held direction disagrees with the live signal
    "unsignalled_holding",     # position held; no live signal on the instrument
    "signal_without_holding",  # live signal present; book is flat there
    "flat_no_signal",          # flat AND no signal - distinct named state (R-3.5)
    "indeterminate",           # signal present but direction/expiry unusable
    "unmapped",                # broker symbol lacks a seeded canonical mapping (L6)
)

# Refusal taxonomy (typed; BE-1 envelope carried).
REFUSAL_CLASSES: Final = (
    "account_context.no_basis",               # no complete sync ever (L4)
    "account_context.mapping_artifact_absent",  # 0050 seeds not present
)

# Signal states considered LIVE for the join (BE-5 vocabulary subset).
LIVE_SIGNAL_STATES: Final = ("emitted",)

ENGINE_VERSION: Final = "ace-1.0.0"

_DOMAIN = "v2.account_context"


@dataclass(frozen=True)
class AlignmentRow:
    """One matrix row — state facts only (wording law)."""

    instrument_ext_id: str
    instrument_id: str | None      # canonical; None iff verdict == unmapped
    posture: str                   # 'long' | 'short' | 'flat' | 'mixed'
    units_long: str
    units_short: str
    signal_state: str              # 'live' | 'none' | 'expired' | 'indeterminate'
    signal_direction: str | None   # 'up' | 'down' | None
    verdict: str                   # ALIGNMENT_VERDICTS member
    basis_sync_run_id: str
    basis_age_hours: float


@dataclass(frozen=True)
class AlignmentMatrix:
    rows: tuple = ()
    basis_sync_run_id: str = ""
    basis_age_hours: float = 0.0
    staleness: str = "fresh"       # 'fresh' | 'stale' (Q7/L8 banner law)
    banner: str | None = None
    digest: str = ""
    engine_version: str = ENGINE_VERSION
    unmapped_count: int = 0        # L6: unmapped is VISIBLE, never filtered


class AccountContextRefused(Exception):
    """Typed refusal; class + reasons; never improvised."""

    def __init__(self, refusal_class: str, reasons: list) -> None:
        assert refusal_class in REFUSAL_CLASSES
        self.refusal_class = refusal_class
        self.reasons = reasons
        super().__init__(f"{refusal_class}: {reasons}")


@dataclass(frozen=True)
class ContextSummary:
    """The census read (GET /summary): counts only, provenance-pinned."""

    verdict_counts: dict = field(default_factory=dict)
    total_rows: int = 0
    unmapped_count: int = 0
    basis_sync_run_id: str = ""
    basis_age_hours: float = 0.0
    staleness: str = "fresh"
    banner: str | None = None
    digest: str = ""
