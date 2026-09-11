"""BE-4 computation versioning — spec §53 contract (plan §1.2).

Registered versions; immutable inputs; independent versioning per
component. The reused V1 surface is pinned by SHA-256 at migration seed
time; a hash mismatch at compute time is a typed refusal, never a silent
proceed (BO-V2-BE-4-001 D-1).
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

# --- Component identifiers (independent versioning, spec §53) ---------------
COMPONENT_INDICATOR_ENGINE = "indicator_engine"
COMPONENT_MARKET_CONTEXT_ENGINE = "market_context_engine"
COMPONENT_CHART_INTELLIGENCE_ENGINE = "chart_intelligence_engine"

# --- Initial registered versions (plan §1.2) ---------------------------------
INDICATOR_ENGINE_VERSION = "v1-reuse-1.0.0"
MARKET_CONTEXT_ENGINE_VERSION = "mce-1.0.0"
CHART_INTELLIGENCE_ENGINE_VERSION = "cie-1.0.0"

# The reused V1 surface (plan §1.1 — never modified by BE-4).
_V1_SURFACE_FILES = (
    "app/services/indicators.py",
    "app/services/market_structure.py",
    "app/services/indicator_registry.py",
)

# BE-4 engine module sets (hashed for their own component pins).
_MCE_FILES = (
    "app/v2/research/versioning.py",
    "app/v2/research/typing.py",
    "app/v2/research/market_context.py",
)
_CIE_FILES = ("app/v2/research/chart_intelligence.py",)


def _backend_dir() -> Path:
    return Path(__file__).resolve().parents[3]


def _hash_files(relative_paths: tuple[str, ...]) -> str:
    """SHA-256 over the concatenated bytes of the named files, in order."""
    digest = hashlib.sha256()
    base = _backend_dir()
    for rel in relative_paths:
        digest.update(rel.encode("utf-8"))
        digest.update(b"\x00")
        digest.update((base / rel).read_bytes())
        digest.update(b"\x00")
    return digest.hexdigest()


def compute_indicator_engine_hash() -> str:
    return _hash_files(_V1_SURFACE_FILES)


def compute_mce_hash() -> str:
    return _hash_files(_MCE_FILES)


def compute_cie_hash() -> str:
    return _hash_files(_CIE_FILES)


def engine_versions() -> dict[str, str]:
    """The version set stamped on every report (plan §1.2)."""
    return {
        COMPONENT_INDICATOR_ENGINE: INDICATOR_ENGINE_VERSION,
        COMPONENT_MARKET_CONTEXT_ENGINE: MARKET_CONTEXT_ENGINE_VERSION,
        COMPONENT_CHART_INTELLIGENCE_ENGINE: CHART_INTELLIGENCE_ENGINE_VERSION,
    }


def engine_versions_hash(versions: dict[str, str]) -> str:
    """OBS-3 pin (BO D-1): SHA-256 over the canonical serialization of
    ``engine_versions`` — JSON with keys sorted lexicographically, no
    whitespace."""
    canonical = json.dumps(versions, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


class ComputationVersionMismatch(Exception):
    """Typed refusal: the registered source hash does not match the live
    surface (BO D-1 — never a silent proceed)."""

    def __init__(self, component: str, registered: str, actual: str) -> None:
        self.component = component
        self.registered = registered
        self.actual = actual
        super().__init__(
            f"computation version source-hash mismatch for {component}:"
            f" registered {registered[:16]}… != actual {actual[:16]}…"
        )
