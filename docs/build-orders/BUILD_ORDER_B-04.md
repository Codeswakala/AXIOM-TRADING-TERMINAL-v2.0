# AXIOM — BUILD ORDER B-04
## Institutional Intelligence Generation

| Item | Value |
|------|-------|
| Build Order ID | `BO-B-04` |
| Programme | Backend Operationalization (reconciled v2; per Operator decision, predictive track deferred) |
| Authorizing authority | **Operator** (directive of 2026-08-20: "authorized") |
| Predecessors | B-00 · B-01 · B-02 · B-DATA · B-ML · B-ML2 (all APPROVED WITH OBSERVATIONS) · Reconciliation Determination · Operator predictive-deferral decision |
| Governing documents | `05_SYSTEM_ARCHITECTURE.md` v2.0 §36–48 · `07_ML_SPEC.md` · `VALIDATION_TIER_SEPARATION.md` · `SUBSTANTIVE_THRESHOLD_FRAMEWORK.md` (thresholds apply to any model-derived content; none here) |
| Implementer | Development Authority (DA) |
| Reviewer | ITRGA |
| Status | **ISSUED — awaiting DA implementation** |
| Governance Gate | CLOSED (unchanged) · Production NOT CERTIFIED (unchanged) |

---

## 0. Purpose and honest framing

The institutional-intelligence layer has five **fully-implemented computation services** (`CorrelationReportService`, `RegimeReportService`, `ScenarioReportService`, `PortfolioRiskReportService`, `SignalValidationReportService`), each with a complete `create_report` and its input models — but the API router exposes **only `list`/`get`**, so the services are **never invoked** and every surface returns `[]` (verified: zero POST endpoints in `intelligence.py`; this was the FIND-2 gap in the original capability audit).

This order **wires generation**: it adds governed, operator-authenticated generation endpoints (and the supporting request/response contracts) so the reports can actually be produced, persisted with provenance, and read by the existing read-only surfaces. It produces **research artifacts**, not trading actuation (per Reconciliation §11 and the B-04 semantic boundary).

The five families are **deterministic** — they do not depend on any ML model (verified in code: `ModelArtifact` imports are lineage references, not inference). This order is therefore fully unblocked by the predictive-track deferral.

---

## 1. Objective

1. Expose governed generation endpoints for the five intelligence families.
2. Persist generated reports with as-of bounding, uncertainty, sample counts, provenance, and audit lineage.
3. Leave the existing list/get surfaces read-only and unchanged in contract.
4. Prove the tier rule and the "research-artifact generation ≠ actuation" boundary hold throughout.

---

## 2. Scope

### B-04.1 — Correlation reports
- **Input:** two `CorrelationSeriesSpec` (left/right) + `as_of_start`/`as_of_end`.
- **Output:** persisted correlation report (coefficient, Fisher interval, sample count, uncertainty, lineage).
- **Generation endpoint:** `POST /api/v1/intelligence/correlation-reports` (operator-authenticated).

### B-04.2 — Regime detection reports
- **Input:** `RegimeSeriesSpec` + window.
- **Output:** persisted regime report (classification, confidence, normalized features, explanation).
- **Endpoint:** `POST /api/v1/intelligence/regime-reports`.

### B-04.3 — Scenario simulation reports
- **Input:** `ScenarioSeriesSpec` + `ScenarioAssumptions` + window.
- **Output:** persisted hypothetical scenario report (assumptions, uncertainty, economic-usefulness field).
- **Endpoint:** `POST /api/v1/intelligence/scenario-reports`.

### B-04.4 — Portfolio/risk reports
- **Input:** `PortfolioRiskSeriesSpec` + `PortfolioRiskAssumptions` + window.
- **Output:** persisted hypothetical market-series risk report (uncertainty, sample count, **no account/broker/position linkage**).
- **Endpoint:** `POST /api/v1/intelligence/portfolio-risk-reports`.

### B-04.5 — Signal-validation reports
- **Input:** `SignalValidationScope` (declared advisory-signal scope) + actor.
- **Output:** persisted validation report (raw-score exclusion, honest outcome-data status).
- **Endpoint:** `POST /api/v1/intelligence/signal-validation-reports`.

### B-04.6 — Shared generation contract (binding)
Every generation endpoint must:
- require operator authentication (Bearer) and honor RBAC;
- persist the report with `as_of` bounding, `source`/data-class label, uncertainty/sample counts, and audit lineage (correlation id + actor);
- **fail honestly** on insufficient data (return a structured "insufficient data" result, not a fabricated report);
- **never** mutate broker/account/trading/execution/gate state, and **never** emit a signal;
- remain **presentation-consistent** with the existing read models (no client recompute).

---

## 3. Exclusions (out of scope — do NOT do)

- **No** ML model, prediction, or promotion (predictive track is deferred per Operator decision).
- **No** signal emission, alert emission, or actuation of any kind.
- **No** broker/account/position/execution state linkage (portfolio-risk remains hypothetical market-series).
- **No** real-time streaming or scheduled/background generation (on-request generation only, unless a scheduled hook is separately justified and approved — see §9).
- **No** modification of the five computation services' *math* (this order wires them; it does not rewrite their algorithms).
- **No** weakening of the chronology guard, tier rule, or threshold gate.
- **No** frontend changes (F-03 presentation comes later).
- **No** modification of the governance hierarchy or constitutional documents.
- **No** repository publication (custody model).

---

## 4. Exact deliverables

1. Generation endpoints (5 × POST) + request/response contracts.
2. Persisted-report evidence: non-empty rows per family with provenance/uncertainty fields.
3. Insufficient-data handling evidence (structured, honest, no fabrication).
4. Tests (new/churn) covering: auth, RBAC, happy path, insufficient-data, no-actuation invariants.
5. Delivery Report (§9) with relay-accurate transmission manifest.

---

## 5. Dependencies

- **Upstream:** B-DATA (real corpus to generate over) · B-01 (tier rule) · B-00 (provenance protocol).
- **Downstream:** F-03 (intelligence presentation) renders these reports; X-01 end-to-end verification includes them.
- **Independent of:** any promoted model (verified). Predictive-track deferral does not affect this order.

---

## 6. Allowed files / components

- `backend/app/api/routes/intelligence.py` (add generation endpoints).
- `backend/app/models/*` and `backend/app/db/models/*` (request/response schemas; read models only — no schema migration unless strictly required and justified).
- `backend/app/institutional_intelligence/*` (consume `create_report`; no math changes).
- `backend/tests/**` (new/churn tests).
- `backend/docs/**` (any ADR for the generation contract).
- The Delivery Report.

Anything outside this list is **not authorized**.

---

## 7. Security & integrity constraints (binding)

- All generation endpoints operator-authenticated; RBAC enforced; no public/unauth generation.
- Input validation on every request (symbol/timeframe/window bounds); as-of bounded; no look-ahead.
- No secrets/credentials; no new external network surface (generation is local over already-ingested data).
- Tier rule honored: reports generated over `historical:real` data at research tier; synthetic-labeled inputs quarantined per the existing authority classification.
- The non-actuation boundary is absolute: generation is research-artifact creation only.

---

## 8. Acceptance criteria

- [ ] 5 POST endpoints exist, authenticated, RBAC-gated.
- [ ] Each generates and persists a report with: as-of bounds, source/data-class label, uncertainty, sample count, lineage/audit correlation.
- [ ] Insufficient-data path returns a structured honest result (no fabricated report).
- [ ] Non-actuation invariant: no signal emission, no broker/account/execution/gate mutation (test-pinned).
- [ ] Existing list/get surfaces still return the newly persisted rows with unchanged contract.
- [ ] Full backend suite green; new tests executed with output.

---

## 9. Evidence requirements (custody model + CA-TRANSMIT-1, hard gate)

**Binding (CA-TRANSMIT-1, escalated):** the transmission step is part of the evidence chain. Before this delivery is accepted for review, the artifacts must actually be uploaded to the review channel and confirmed against it — not the DA's disk. A declared-but-untransmitted artifact is an automatic CORRECTION REQUIRED, and the review will not proceed until the set is complete.

| Item | Class | Form |
|------|-------|------|
| Patch artifact + per-file SHAs + `git apply --check` transcript | Level I | patch + transcript |
| Executed test output (new/churn) | Level II | run transcript |
| Generation evidence (POST → persisted report, per family, with fields) | Level I | API probe output |
| Insufficient-data evidence (structured honest result) | Level I | API probe output |
| Transmission manifest (relay-accurate, CA-TRANSMIT-1) | — | table in Delivery Report |
| Delivery Report | Level III | §10 structure |

---

## 10. Delivery Report structure (required)

1. Claimed scope vs. this Build Order
2. What changed (files + SHAs + chain position)
3. Per-family generation description (endpoint, input, output fields)
4. Generation evidence (POST → persisted rows, with provenance/uncertainty)
5. Insufficient-data handling evidence
6. Non-actuation invariant evidence
7. Test evidence (executed)
8. Deviations register
9. Transmission manifest (relay-accurate)
10. Known limitations / technical debt

---

## 11. Rollback / containment

- New endpoints + report rows are additive; revert = drop rows, revert patch.
- No schema migration authorized by default.
- No data produced affects production (Gate CLOSED).

---

## 12. Completion condition

Complete when: all §8 criteria met, evidence (§9) transmitted and verified (relay-accurate manifest complete), the Delivery Report submitted, **and ITRGA issues its independent determination**. A DA declaration of completion is not evidence and does not close this unit.

**Next authorization state:** upon ITRGA approval of B-04, B-05 (Monitoring & Alerts) may be issued, and F-03 (intelligence presentation) is unblocked to render these reports.

---

**End of Build Order B-04**
