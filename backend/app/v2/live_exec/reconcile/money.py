"""BE-12E — THE DR-F2 CONVERSION LAW LOCUS (BO-V2-BE12E-001 §1.b).

ONE LOCUS: this module is the SINGLE designated conversion module for
the entire band. No other module, engine, coupon, or card converts
money representations (coupon-scanned: the entry-point token
`to_canonical_money` appears only here and at call sites).

ONE DIRECTION: conversion runs fact -> canonical AT THE PARITY BOUNDARY
ONLY. Nothing converts back; nothing converts "for display"; engines
and coupons never hand-convert.

THE FOUR PINS (coupon-pinned):
- interior representation `decimal.Decimal` ONLY — float is BANNED
  anywhere in the live_exec money path;
- rounding mode NAMED: ROUND_HALF_EVEN, applied exactly once at
  quantize-to-canonical, DELEGATED to the standing band convention —
  this locus imports `quantize_2dp` from the fielded paper-bridge
  engine (`app.v2.paper_bridge.engine`, compver pbr-1.0.0), whose body
  reads verbatim:
      return str(value.quantize(Decimal("0.01"), rounding=ROUND_HALF_EVEN))
  The BE-9 projection layer itself carries string-decimal facts with
  NO named rounding convention (enumerated: `str(info.balance)` at the
  provider seam; exact-compare in reconcile.py) — so the nearest
  standing NAMED convention in the band's money lineage is the bridge's
  D-B10-2DP mirror, and the locus DELEGATES to it rather than invent
  (BO §1.b.3 delegation clause; the DR discloses this enumeration).
- canonical form: fixed-point string at exactly 2dp; no exponent; no
  leading '+'; leading zeros stripped except the single leading zero
  of |x|<1; sign only when negative. Equality of canonical strings IS
  parity at the money seam.

Quantities that are NOT money are OUT OF SCOPE of this locus and ride
the standing projection discipline (exact string-decimal compare, the
BE-9 reconcile law).
"""

from __future__ import annotations

from decimal import Decimal, InvalidOperation

from app.v2.paper_bridge.engine import quantize_2dp


class MoneyNotCanonicalizable(Exception):
    """Typed: the input cannot enter the money seam (never a float)."""

    def __init__(self, reason: str, value):
        self.reason = reason
        self.value_repr = repr(value)
        super().__init__(reason)


def to_canonical_money(value) -> str:
    """THE entry point. Accepts str/int/Decimal fact representations;
    floats are REFUSED (the float ban is a law, not a preference —
    a float has already lost the fact). Returns the canonical 2dp
    fixed-point string via the delegated ROUND_HALF_EVEN quantize."""
    if isinstance(value, float):
        raise MoneyNotCanonicalizable("money_float_banned", value)
    try:
        interior = Decimal(str(value))
    except (InvalidOperation, TypeError, ValueError):
        raise MoneyNotCanonicalizable(
            "money_not_decimal", value) from None
    canonical = quantize_2dp(interior)  # delegated; ROUND_HALF_EVEN once
    # normalize the sign-zero edge (the canonical form has no -0.00)
    if canonical == "-0.00":
        canonical = "0.00"
    return canonical


def money_parity(fact_a, fact_b) -> bool:
    """Parity at the money seam: canonical-string equality, nothing else."""
    return to_canonical_money(fact_a) == to_canonical_money(fact_b)
