"""Wave-4 scientific dependency policy (W4-U01)."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ScientificDependencyCandidate:
    package: str
    import_name: str
    purpose: str
    compiled: bool = True


WAVE4_CANDIDATE_DEPENDENCIES: tuple[ScientificDependencyCandidate, ...] = (
    ScientificDependencyCandidate("numpy", "numpy", "array math and vectorized statistics"),
    ScientificDependencyCandidate("pandas", "pandas", "tabular research artifact analysis"),
    ScientificDependencyCandidate(
        "scipy", "scipy", "statistical intervals and correlation support"
    ),
)

# Empty until operator-run Windows/Python 3.14.6 spike evidence is accepted by ITRGA.
APPROVED_COMPILED_DEPENDENCIES: tuple[str, ...] = ()

SCIENTIFIC_DEPENDENCY_POLICY = (
    "No Wave-4 application code may import a compiled scientific dependency unless that dependency "
    "has passed the W4-U01 Windows/Python 3.14.6 install/import/smoke spike "
    "and is recorded as approved. "
    "Pure-Python fallbacks remain available for candidates that fail or remain unapproved."
)
