# Build Order Intake — W4-U01

| Field | Value |
|---|---|
| Build Order | W4-U01 — Scientific Dependency Compatibility + Intelligence Artifact Foundation |
| Wave | 4 — Institutional Intelligence |
| Intake date | 2026-07-16 |
| Authority | ITRGA Build Order after Wave-4 Design Plan acceptance |
| Source build order | `docs/build-orders/BUILD_ORDER_W4-U01.md` |

## DA Intake Confirmation

The Development Authority confirms receipt of `docs/build-orders/BUILD_ORDER_W4-U01.md`.

The Build Order states that the Wave-4 Design Plan was accepted with refinements R-1…R-8. The separate ITRGA design-plan review artifact was not attached in this turn; DA therefore implements only the explicit W4-U01 scope stated in the Build Order and the pre-registered Wave-4 guardrails.

## Authorized Scope

1. Scientific dependency compatibility spike framework and operator evidence commands for candidate compiled dependencies.
2. Institutional Intelligence bounded-context skeleton.
3. Common inert intelligence artifact/report contract with lineage, uncertainty, sample count, research status, audit correlation, and deterministic hash.
4. Pure-Python fallback primitives for early Wave-4 statistical needs if compiled dependencies fail or remain unapproved.
5. Policy tests and documentation/register updates.

## Explicit Implementation Decisions

- Candidate compiled dependencies for W4-U01 evidence: `numpy`, `pandas`, `scipy`.
- `scikit-learn` is not adopted in W4-U01; any future use requires a separate passed spike or future authorization.
- No compiled dependency is added to runtime project dependencies in this unit.
- No persisted `scientific_dependency_spikes` table is added; spike evidence is file-recorded through operator evidence artifacts.
- No schema migration is added.

## Explicit Boundaries

- No analytical feature for operator consumption.
- No correlation/regime/scenario/risk report implementation.
- No operator UI capability.
- No endpoint.
- No execution, order, broker, paper trading, or position behavior.
- No Governance Gate change.
- No unspiked compiled dependency import in application code.

## DA Non-Approval Statement

DA may implement and validate W4-U01 but does not self-approve it. Acceptance requires operator-run target evidence and ITRGA review.
