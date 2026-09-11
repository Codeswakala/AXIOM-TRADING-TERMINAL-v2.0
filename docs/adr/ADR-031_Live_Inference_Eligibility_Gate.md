# ADR-031 — Live Inference Engine and Governed Model Eligibility Gate

| Field | Value |
|-------|-------|
| ID | ADR-031 |
| Title | Deterministic backend-only live inference with governed advisory eligibility |
| Date | 2026-07-15 |
| Status | Accepted |
| Deciders | Development Authority under Build Order W3-U01 |
| Domain | Trading Intelligence / Live Research Advisor / Governance |

---

## Context

W3-U01 is the first Wave-3 unit and the first step toward operator-facing advisory signals. Before any signal surface exists, AXIOM must prove deterministic inference and a strict governed-model eligibility gate. Only fully Wave-2-governed and explicitly advisory-approved models may ever become signal-eligible.

## Decision

Implement a backend-only inference foundation:

- `LiveInferenceEngine` returns deterministic `InferenceResult` with score and `inference_input_hash`;
- `GovernedModelEligibilityGate` checks experiment approval, U07/U08/U09/U10 report links, feature-version match, advisory approval, operating domain, chronology/as-of sanity, and identity-free input;
- `model_artifacts` gains advisory lifecycle fields: `advisory_status`, `advisory_approved_at`, `advisory_approved_by`;
- advisory promotion requires explicit approver, UTC timestamp, complete lineage, and audit event;
- W3-U01 creates no signal table, no UI, no alert, no WebSocket signal stream, and no execution path.

## Alternatives Considered

| Option | Outcome | Rationale |
|--------|---------|-----------|
| Add signal persistence immediately | Deferred | W3-U01 is the safety slice; signal contract is W3-U02. |
| Let research_only models score | Rejected | Advisory approval must be explicit and audited. |
| Add live UI/dashboard | Deferred | UI is later Wave-3 after backend gate is proven. |
| Use probabilistic/random scoring | Rejected | 05 v2.0 requires deterministic inference. |

## Consequences

- Future signal units can depend on a proven eligibility gate.
- Ungoverned models are refused before any operator surface exists.
- The no-execution boundary remains clear.
- Advisory status promotion becomes a persisted/audited governance action.

## Compliance

Supports `05_SYSTEM_ARCHITECTURE.md` v2.0 §6, §15, §16, §42, §77; preserves D-W2-001; respects Wave-3 design plan bright-line boundary.

---

**End ADR-031**
