"""BE-4 Chart Intelligence Engine (CIE) — spec §16 pipeline (plan §4).

deterministic detection → market context (referenced by report id, never
recomputed inline) → chart intelligence → annotations + interpretation.

Annotations: geometry-bound statements — claim_type fact/derived only.
Interpretations: contextual narrative — claim_type contextual_interpretation
always; each MUST reference ≥1 basis id; empty basis = typed refusal.
Predictions: none (schema type exists; emission is a violation).
"""

from __future__ import annotations

from dataclasses import dataclass

from app.v2.research.typing import TypingViolation

ANNOTATION_CLAIM_TYPES = ("fact", "derived_observation")


class _IdGen:
    """Deterministic per-artifact id sequence (plan §11.1 determinism)."""

    def __init__(self, prefix: str) -> None:
        self._prefix = prefix
        self._n = 0

    def next(self) -> str:
        self._n += 1
        return f"{self._prefix}-{self._n:04d}"


@dataclass(frozen=True)
class Annotation:
    annotation_id: str
    kind: str  # level | zone | swing_marker | break_marker
    claim_type: str
    geometry: dict  # e.g. {"price": "...", "time": "..."}
    basis_observation_ids: tuple[str, ...]


@dataclass(frozen=True)
class Interpretation:
    interpretation_id: str
    claim_type: str  # always contextual_interpretation
    text_statement: dict
    basis_ids: tuple[str, ...]  # annotation or observation ids; NEVER empty


@dataclass(frozen=True)
class ChartIntelligenceResult:
    status: str
    annotations: list[Annotation]
    interpretations: list[Interpretation]


def _validate_annotation(a: Annotation, known_obs_ids: frozenset[str]) -> None:
    if a.claim_type not in ANNOTATION_CLAIM_TYPES:
        raise TypingViolation(
            f"annotation claim_type must be fact/derived_observation; got {a.claim_type}"
        )
    if not a.basis_observation_ids:
        raise TypingViolation("annotation requires a non-empty observation basis")
    unresolved = [b for b in a.basis_observation_ids if b not in known_obs_ids]
    if unresolved:
        raise TypingViolation(f"annotation basis unresolvable: {unresolved}")


def _validate_interpretation(i: Interpretation, known_ids: frozenset[str]) -> None:
    if i.claim_type != "contextual_interpretation":
        raise TypingViolation(
            "interpretation claim_type must be contextual_interpretation;"
            f" got {i.claim_type}"
        )
    if not i.basis_ids:
        # plan §4: an interpretation with an empty basis set is refused
        raise TypingViolation("interpretation with empty basis set is refused")
    unresolved = [b for b in i.basis_ids if b not in known_ids]
    if unresolved:
        raise TypingViolation(f"interpretation basis unresolvable: {unresolved}")


def compute_chart_intelligence(observations: list[dict]) -> ChartIntelligenceResult:
    """Derive annotations + interpretations from a market-context report
    body (the observations JSON — referenced, never recomputed).

    Deterministic: pure function of the input list.
    """
    known_obs_ids = frozenset(o["observation_id"] for o in observations)
    annotations: list[Annotation] = []
    interpretations: list[Interpretation] = []
    ann_ids = _IdGen("ann")
    int_ids = _IdGen("int")

    for obs in observations:
        family = obs["family"]
        statement = obs["statement"]
        oid = obs["observation_id"]

        if family == "key_levels" and obs["layer"] == "observed":
            if statement.get("value") is not None:
                annotations.append(Annotation(
                    annotation_id=ann_ids.next(),
                    kind="level",
                    claim_type="fact",
                    geometry={"price": statement["value"],
                              "timeframe": obs["timeframe"]},
                    basis_observation_ids=(oid,),
                ))
        elif family == "protected_swing" and obs["layer"] == "derived":
            annotations.append(Annotation(
                annotation_id=ann_ids.next(),
                kind="swing_marker",
                claim_type="derived_observation",
                geometry={"swing_high": statement.get("swing_high"),
                          "swing_high_time": statement.get("swing_high_time"),
                          "swing_low": statement.get("swing_low"),
                          "swing_low_time": statement.get("swing_low_time"),
                          "timeframe": obs["timeframe"]},
                basis_observation_ids=(oid,),
            ))
        elif family == "structural_break" and obs["layer"] == "derived":
            if statement.get("breaks_detected"):
                annotations.append(Annotation(
                    annotation_id=ann_ids.next(),
                    kind="break_marker",
                    claim_type="derived_observation",
                    geometry={"timeframe": obs["timeframe"]},
                    basis_observation_ids=(oid,),
                ))

    # Interpretations — one per trend derivation, grounded in its annotation
    # or observation basis (facts distinguished from interpretations).
    for obs in observations:
        if obs["family"] == "prevailing_trend" and obs["layer"] == "derived":
            interpretations.append(Interpretation(
                interpretation_id=int_ids.next(),
                claim_type="contextual_interpretation",
                text_statement={
                    "interpretation": (
                        f"On {obs['timeframe']}, the computed trend basis"
                        f" ({obs['statement'].get('basis')}) currently reads"
                        f" {obs['statement'].get('trend')}."
                    ),
                    "epistemic_note": (
                        "Interpretation of deterministic observations on"
                        " labelled synthetic input; no market conclusion,"
                        " no prediction."
                    ),
                },
                basis_ids=(obs["observation_id"],),
            ))

    known_ids = known_obs_ids | frozenset(a.annotation_id for a in annotations)
    for a in annotations:
        _validate_annotation(a, known_obs_ids)
    for i in interpretations:
        _validate_interpretation(i, known_ids)

    status = "available" if annotations or interpretations else "unavailable"
    return ChartIntelligenceResult(
        status=status, annotations=annotations, interpretations=interpretations
    )


def cie_to_json(result: ChartIntelligenceResult) -> dict:
    return {
        "annotations": [
            {
                "annotation_id": a.annotation_id,
                "kind": a.kind,
                "claim_type": a.claim_type,
                "geometry": a.geometry,
                "basis_observation_ids": list(a.basis_observation_ids),
            }
            for a in result.annotations
        ],
        "interpretations": [
            {
                "interpretation_id": i.interpretation_id,
                "claim_type": i.claim_type,
                "text_statement": i.text_statement,
                "basis_ids": list(i.basis_ids),
            }
            for i in result.interpretations
        ],
    }
