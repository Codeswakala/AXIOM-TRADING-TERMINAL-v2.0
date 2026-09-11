"""V2 BE-2 reference-data seed — closed, versioned, hash-manifested (plan C.4).

The seed inventory is the single reviewable source of truth for instrument,
symbol-map, and source reference rows. The migration embeds these values;
tests assert DB contents match this module and SEED_MANIFEST_HASH — any
undocumented edit changes the hash and fails Level-II evidence.

Governed change process: Build Order / accepted correction + new additive
migration + updated SEED_MANIFEST_HASH recorded in the Delivery Report.
"""

from __future__ import annotations

import hashlib
import json

# --- sources (exactly two; no reserved rows seeded in BE-2) -------------------

V2_MD_SOURCE_SEED: tuple[dict[str, object], ...] = (
    {
        "source_id": "sim.local",
        "kind": "simulator",
        "authority": "live:simulated",
        "mode_scope": "RESEARCH",
        "active": True,
    },
    {
        "source_id": "seed.local",
        "kind": "seed",
        "authority": "seed:synthetic",
        "mode_scope": "RESEARCH",
        "active": True,
    },
)

# --- instruments: exactly the V1 simulator base-price symbol set --------------
# (LiveMarketService._base_price defaults + _infer_class mapping; DATA-P01 S1)

_INSTRUMENTS: tuple[tuple[str, str, str, int], ...] = (
    # (instrument_id, market_class, display_symbol, precision)
    ("forex.eurusd", "forex", "EURUSD", 5),
    ("forex.gbpusd", "forex", "GBPUSD", 5),
    ("forex.usdjpy", "forex", "USDJPY", 3),
    ("forex.audusd", "forex", "AUDUSD", 5),
    ("forex.usdcad", "forex", "USDCAD", 5),
    ("forex.usdchf", "forex", "USDCHF", 5),
    ("forex.nzdusd", "forex", "NZDUSD", 5),
    ("forex.eurgbp", "forex", "EURGBP", 5),
    ("crypto.btcusd", "crypto", "BTCUSD", 2),
    ("crypto.ethusd", "crypto", "ETHUSD", 2),
    ("crypto.solusd", "crypto", "SOLUSD", 2),
    ("metal.xauusd", "metal", "XAUUSD", 2),
)

V2_MD_INSTRUMENT_SEED: tuple[dict[str, object], ...] = tuple(
    {
        "instrument_id": iid,
        "market_class": cls,
        "display_symbol": sym,
        "precision": prec,
    }
    for iid, cls, sym, prec in _INSTRUMENTS
)

# --- symbol maps: exact-match rows per (seeded source x seeded instrument) ----

V2_MD_SYMBOL_MAP_SEED: tuple[dict[str, object], ...] = tuple(
    {
        "source_id": source["source_id"],
        "source_symbol": inst["display_symbol"],
        "instrument_id": inst["instrument_id"],
    }
    for source in V2_MD_SOURCE_SEED
    for inst in V2_MD_INSTRUMENT_SEED
)


def compute_seed_manifest_hash() -> str:
    """Deterministic SHA-256 over the canonically-serialized seed set."""
    canonical = json.dumps(
        {
            "sources": V2_MD_SOURCE_SEED,
            "instruments": V2_MD_INSTRUMENT_SEED,
            "symbol_maps": V2_MD_SYMBOL_MAP_SEED,
        },
        sort_keys=True,
        separators=(",", ":"),
        default=str,
    )
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


SEED_MANIFEST_HASH: str = compute_seed_manifest_hash()
