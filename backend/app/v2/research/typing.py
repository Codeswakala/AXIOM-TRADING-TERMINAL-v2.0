"""BE-4 typed observation contract — spec §15 layers + band claim classes.

The four layers and four claim classes are TYPED FIELDS, not prose
(plan §2; BG-5). Coupling rules and the cross-timeframe rule are enforced
here (single enforcement point) and re-proved by tests.

BE-4 emits NO ``statistical``/``prediction`` elements (predictive ML is
BE-5/BE-11 territory); the types exist so the discipline is structural,
and any BE-4 emission of either is refused here — hence a test failure.
"""

from __future__ import annotations

from dataclasses import dataclass, field

# --- Closed vocabularies (schema CHECKs mirror these) ------------------------
LAYERS = ("observed", "derived", "contextual", "statistical")
CLAIM_TYPES = (
    "fact",
    "derived_observation",
    "contextual_interpretation",
    "prediction",
)

# Layer → permitted claim types (plan §2 coupling constraint).
LAYER_CLAIM_COUPLING: dict[str, tuple[str, ...]] = {
    "observed": ("fact",),
    "derived": ("derived_observation",),
    "contextual": ("contextual_interpretation",),
    "statistical": ("prediction",),
}

# BE-4 band ceiling: statistical/prediction NEVER emitted (plan §2/§4).
BE4_FORBIDDEN_LAYERS = ("statistical",)
BE4_FORBIDDEN_CLAIM_TYPES = ("prediction",)

# The ten observation families of spec §14 (plan §3 table).
FAMILIES = (
    "prevailing_trend",
    "structural_state",
    "protected_swing",
    "structural_break",
    "liquidity_context",
    "key_levels",
    "session_context",
    "volatility_state",
    "momentum_state",
    "timeframe_relationships",
)

# --- R-4: fixed timeframe_relationships rule table ---------------------------
# Permitted cross-timeframe statement classes (plan §2 ceiling; BO §3 R-4).
# Class → (layer, claim_type). Anything not listed is refused.
TIMEFRAME_RELATIONSHIP_RULES: dict[str, tuple[str, str]] = {
    # Alignment of the same family's state across two timeframes — a
    # relationship computed from typed inputs: derived.
    "trend_alignment": ("derived", "derived_observation"),
    "momentum_alignment": ("derived", "derived_observation"),
    "volatility_alignment": ("derived", "derived_observation"),
    # Statements that read a higher-timeframe state as context for a lower
    # one — interpretation by construction: contextual.
    "higher_tf_context": ("contextual", "contextual_interpretation"),
    "structure_nesting": ("contextual", "contextual_interpretation"),
}


class TypingViolation(Exception):
    """Typed refusal — a BE-4 element violated the typing contract."""


@dataclass(frozen=True)
class Observation:
    """One typed observation element (plan §3 contract)."""

    observation_id: str
    family: str
    timeframe: str
    layer: str
    claim_type: str
    statement: dict
    contributing_observation_ids: tuple[str, ...] = ()
    # observed rows carry the indicator basis instead of contributions
    indicator_basis: dict | None = None
    relationship_class: str | None = None  # timeframe_relationships only


def validate_observation(
    obs: Observation, *, known_ids: frozenset[str], known_timeframes: dict[str, str]
) -> None:
    """Enforce the full typing contract for one element. Raises
    ``TypingViolation`` (typed refusal) — never silently drops or coerces.

    ``known_ids``: ids of observations already accepted into the report.
    ``known_timeframes``: id → timeframe for cross-timeframe checks.
    """
    if obs.layer not in LAYERS:
        raise TypingViolation(f"unknown layer: {obs.layer}")
    if obs.claim_type not in CLAIM_TYPES:
        raise TypingViolation(f"unknown claim_type: {obs.claim_type}")
    if obs.family not in FAMILIES:
        raise TypingViolation(f"unknown family: {obs.family}")

    # BE-4 band ceiling — zero statistical/prediction emissions.
    if obs.layer in BE4_FORBIDDEN_LAYERS or obs.claim_type in BE4_FORBIDDEN_CLAIM_TYPES:
        raise TypingViolation(
            "BE-4 emits no statistical/prediction elements"
            f" (got layer={obs.layer}, claim_type={obs.claim_type})"
        )

    # Layer/claim coupling (plan §2).
    if obs.claim_type not in LAYER_CLAIM_COUPLING[obs.layer]:
        raise TypingViolation(
            f"layer/claim coupling violated: {obs.layer} cannot carry {obs.claim_type}"
        )

    # Basis rules: observed rows carry an indicator basis; all others carry
    # a non-empty, resolvable contribution set (plan §3).
    if obs.layer == "observed":
        if obs.indicator_basis is None:
            raise TypingViolation("observed element requires indicator_basis")
    else:
        if not obs.contributing_observation_ids:
            raise TypingViolation(
                f"{obs.layer} element requires non-empty contributing_observation_ids"
            )
        unresolved = [
            cid for cid in obs.contributing_observation_ids if cid not in known_ids
        ]
        if unresolved:
            raise TypingViolation(
                f"unresolvable contributing observation ids: {unresolved}"
            )

    # Cross-timeframe rule (plan §2, enforced + tested; R-4 rule table).
    contributing_tfs = {
        known_timeframes[cid]
        for cid in obs.contributing_observation_ids
        if cid in known_timeframes
    }
    crosses = len(contributing_tfs) > 1
    if crosses:
        if obs.layer == "observed":
            raise TypingViolation(
                "cross-timeframe element may never be layer=observed"
            )
        if obs.claim_type == "fact":
            raise TypingViolation("cross-timeframe element may never claim fact")
        if obs.family == "timeframe_relationships":
            if obs.relationship_class not in TIMEFRAME_RELATIONSHIP_RULES:
                raise TypingViolation(
                    f"unpermitted timeframe relationship class: {obs.relationship_class}"
                )
            req_layer, req_claim = TIMEFRAME_RELATIONSHIP_RULES[obs.relationship_class]
            if (obs.layer, obs.claim_type) != (req_layer, req_claim):
                raise TypingViolation(
                    f"relationship class {obs.relationship_class} requires"
                    f" ({req_layer},{req_claim}); got ({obs.layer},{obs.claim_type})"
                )
    elif obs.family == "timeframe_relationships":
        raise TypingViolation(
            "timeframe_relationships element must span more than one timeframe"
        )


@dataclass
class TypedOutcomes:
    """Insufficient-data accounting — a typed outcome, never an error
    (plan §6). Collected per family, mapped to BE-1 status at report level."""

    insufficient: list[dict] = field(default_factory=list)

    def record(self, family: str, timeframe: str, required: int | None,
               available: int | None) -> None:
        self.insufficient.append(
            {
                "outcome": "insufficient_data",
                "family": family,
                "timeframe": timeframe,
                "required_bars": required,
                "available_bars": available,
            }
        )
