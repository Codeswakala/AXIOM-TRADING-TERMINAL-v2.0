# AXIOM — Backend Operationalization Roadmap (v2 · Operator-Reconciled)
## Turning the scaffolded analytical core into an operable, evidence-backed platform

| Item | Value |
|------|-------|
| Document class | **ITRGA sequencing recommendation** — revision 2, reconciled against Operator Review (2026-08-19) |
| Status | **DRAFT — not an Operator directive, not a DA engineering design plan, not a Build Order, not self-authorization** |
| Date | 2026-08-19 |
| Baseline | backend v0.62.0 · 18 routers · 161 OpenAPI paths · 37 Alembic migrations |

---

## 0. Authority boundary (Operator finding §23 — reconciled)

This document is **only** a sequencing recommendation. It is explicitly **not**:

- the Operator's directive (the Operator issues directives);
- the DA's engineering design plan (the DA produces design plans per unit, within scope);
- a Build Order (Build Orders are issued separately through the governed lifecycle).

The binding lifecycle remains:

```
Operator Directive
   ↓
DA Engineering / Design Planning
   ↓
ITRGA Independent Review
   ↓
Build Order
   ↓
DA Implementation + Evidence
   ↓
ITRGA Independent Review
   ↓
Approval / Correction
```

ITRGA may recommend sequencing; it does not thereby author, design, or implement. No unit is authorized by this document.

---

## 0.1 Guiding principles (bind every unit)

1. **Non-actuation is permanent.** No unit introduces order placement, execution, broker mutation, or gate-opening. The Governance Gate stays CLOSED.
2. **Evidence over assertion.** A declaration of completion is **not** evidence of completion. Every unit closes with reproducible evidence (test output, runtime probe, SHA, DB row counts).
3. **Provenance discipline.** Every unit lands with an exact commit ref; Delivery Reports cite real SHAs. No "landed" claim without the ref.
4. **Governed model eligibility.** A model advances through the governed gate; nothing self-promotes. Report existence ≠ scientific acceptability (see B-02).
5. **Independent review.** DA builds and evidences; ITRGA verifies. No self-approval.
6. **Repository / custody model (Operator finding §24).** This roadmap does **not** imply unlimited DA repository access, direct ITRGA access to the DA workspace, per-unit GitHub publication, or continuous repo sync. Repository publication remains an **Operator-controlled custody action**. Repository evidence is required only where the applicable evidence/custody mechanism requires it.

---

## 0.2 Programme-wide data honesty (Operator finding §22 — reconciled)

Every data-driven output — backend or frontend — must identify its source as one of:

```
synthetic · simulated · historical real · live · stale/cached · unavailable
```

**Synthetic/simulated data may prove the pipeline works. It may not, silently or otherwise, substantiate real-world market or trading conclusions.** This rule applies to charts, signals, intelligence, scenarios, alerts, reports, and assistant responses.

---

## Dependency map (programme-wide, reconciled)

```
                        BASELINE
                           │
              ┌────────────┴─────────────┐
              │                          │
           BACKEND                    FRONTEND
              │                          │
             B-00                      F-00
              │                          │
             B-01                      F-01 ──(final acceptance needs B-06.1)
              │                          │
             B-02                        │
              │                          │
             B-03 ───────────────────► F-02
              │
             B-04 ───────────────────► F-03
              │
             B-05 ───────────────────► F-04
              │
         B-02..B-05 ────────────────► F-05
              │                          │
              └────────────┬─────────────┘
                           ▼
                    B-07 + F-06
                           │
                           ▼
                X-01 END-TO-END VERIFICATION
```

---

## Phase B-00 — Integrity & reproducible baseline

### B-00.1 — Fix simulated clock chronology
- **Problem:** `app/market/adapters/simulated.py:157` produces future-dated bars (~30× real time). Violates the as-of/no-look-ahead discipline.
- **Scope:** bind simulated bar time to wall-clock (no future bars) **or** label an explicit "accelerated synthetic clock" as a distinct non-live state.
- **Acceptance:** soak run with zero candles where `open_time > utc_now()`; chronology guard passes; invariant test pinned. *(Retained unchanged per Operator §4.2.)*

### B-00.2 — Dependency & supply-chain remediation *(reconciled: severity/exception policy)*
- **Replaces** the earlier unconditional "audit clean" wording (Operator §4.1).
- **Acceptance model:**
  - No **unaccepted** critical/high findings;
  - all remaining findings classified (transitive / dev-only / no-fix / false-positive);
  - permitted exceptions documented and formally accepted;
  - lockfiles updated;
  - the security gate passes.
- **Ownership note:** frontend dependency remediation is owned by **F-00** (Operator §11.1). B-00.2 references it as a shared baseline dependency only.

### B-00.3 — Establish the true test/evidence baseline
- **Scope:** run backend `pytest` and frontend `vitest`; record **executed** pass/fail counts; reconcile against `PROJECT_STATE.md` (162 suites / 736 tests). Distinguish inventory vs executed result.
- **Acceptance:** committed baseline report with run output (Level-II evidence), not a count assertion.

### B-00.4 — Provenance/landing protocol
- **Scope:** define and enforce "a unit is landed only when its SHA is cited and its Delivery Report references the canonical registers."
- **Acceptance:** applied to every subsequent unit.

---

## Phase B-01 — Data foundation *(reconciled: validation-tier separation)*

### B-01.1 — Honest historical corpus
- **Scope:** ingest a real (or explicitly-labeled synthetic) multi-market corpus through the existing ingestion seam; populate metadata, quality scores, provenance.
- **Acceptance:** non-zero ingestion/runs, stats, candle-counts with source labels.

### B-01.1a — Validation-tier separation *(Operator §4.3 — major clarification)*
The programme must **never** let synthetic data silently reach a research conclusion. Tiers:

| Tier | Data required | Purpose |
|------|---------------|---------|
| **Pipeline validation** | Synthetic permitted | Prove the pipeline works |
| **Research validation** | Real historical data | Substantive market conclusions |
| **Economic validation** | Real historical + realistic cost assumptions | Economic viability |
| **Generalization validation** | Real hold-out data | Cross-market robustness |

**Acceptance:** each downstream ML/report unit states its tier and its data class; a synthetic corpus may only close *pipeline-validation* units.

### B-01.2 — Dataset snapshots & temporal splits
- **Scope:** execute snapshot builder + split engine over real series → `dataset_snapshots`, `split_manifests`. Random splits and label-horizon leakage remain rejected.
- **Acceptance:** rows exist; split boundaries verified no-look-ahead.

### B-01.3 — Feature store population
- **Scope:** compute features over the corpus; persist `feature_records` + quality reports; enforce causal/no-symbol-identity boundary.
- **Acceptance:** non-zero feature records with lineage; no symbol-identity leakage detected.

---

## Phase B-02 — ML research executed *(reconciled: explicit acceptance logic)*

### B-02.1 — Train a baseline market-agnostic model
- **Scope:** run `app/ml/models/` harness/baseline over the corpus; register a `model_artifact`.
- **Acceptance:** model artifact row with full registry metadata.

### B-02.2 — Walk-forward statistical validation
- **Acceptance:** `validation_reports` with metrics + uncertainty; no leakage.

### B-02.3 — Calibration
- **Acceptance:** `calibration_reports` (Brier/ECE, reliability bins, miscalibration warnings).

### B-02.4 — Economic validation
- **Acceptance:** `economic_reports`; statistical vs economic verdicts held distinct.

### B-02.5 — Cross-market generalization *(reconciled: distinct governed research question)*
- **Scope:** hold-out market evaluation → `generalization_reports`.
- **Governance condition (Operator §6):** cross-market evaluation is a **new research question**, independently identified, governed, and evaluated. It must **not** retroactively reopen or alter the outcome of previously closed experiments.
- **Acceptance:** report row; governance record separates this from prior closed work.

### B-02.6 — Governed model promotion (the gate) *(reconciled: substance, not existence)*
- **Replaces** the "required reports exist = eligible" implication (Operator §5 — major).
- **Required eligibility logic:**

```
Required evidence exists
   + Statistical criteria satisfied
   + Calibration criteria satisfied
   + Economic criteria satisfied
   + Generalization criteria satisfied
   + Limitations acceptable
   + Governed approval
   = Eligible model
```

- The B-02 Build Order must **reference the governing ML thresholds, sample requirements, rejection conditions, and interpretation rules** (from `07_ML_SPEC.md` and the calibration/economic/generalization frameworks). Report existence is necessary, **not sufficient**.
- **Acceptance:** an eligible model exists with a documented pass of each criterion; promotion evidence independently reviewed by ITRGA (no self-approval).

---

## Phase B-03 — Live inference & signals

### B-03.1 — Wire the live inference adapter
- **Problem:** `LiveMarketInferenceAdapter` is imported but **never instantiated**.
- **Scope:** invoke it from the live-market lifecycle on each completed, as-of-bounded window (`live:simulated` source only).
- **Acceptance:** inference windows with `effective_as_of_time ≤ now`; no future candles.

### B-03.2 — Signal production with guardrails
- **Scope:** `AdvisorySignalService.produce()` from the adapter; operating-domain, calibration, economic, staleness guardrails enforced.
- **Acceptance:** `advisory_signals` rows with guardrail fields; withheld signals recorded, not silently dropped.

### B-03.3 — Verify signal read surface
- **Acceptance:** `GET /signals/history` (+`/{id}`) returns populated, guardrail-bearing records (runtime probe).

---

## Phase B-04 — Institutional intelligence generation *(reconciled: artifact vs actuation)*

- **B-04.1** Correlation · **B-04.2** Regime · **B-04.3** Scenario · **B-04.4** Portfolio/risk · **B-04.5** Signal validation.

**Generation model (Operator §8 — architectural clarification):**

```
Authorized research operation
   ↓
Server-side report generation
   ↓
Persist research artifact
   ↓
Audit / lineage
   ↓
Read-only UI consumption
```

Generation is **research-artifact generation only**. It must **not** mutate broker state, account state, trading state, execution state, or governance gates. List/get remain read-only; no client-side recompute; no signal emission or execution path.

**Shared acceptance:** each family returns non-empty, uncertainty-bearing, as-of-bounded rows; read-only posture preserved; provenance labeled per §0.2.

---

## Phase B-05 — Monitoring & alerts emission *(reconciled: ack semantics)*

- **B-05.1** Wire `create_drift_alert` / `create_inference_health_alert` / `create_live_data_stale_alert` / `create_signal_withheld_alert` to their triggering conditions.
- **B-05.2** Verify `GET /alerts` + `ack` populated; alerts remain inert.

**Ack semantics (Operator §9):** acknowledgement **may modify alert read-state only** and must **not** mutate trading, account, broker, model, analytical-source, or execution state.

**Acceptance:** alerts appear on real conditions; ack changes read-state only; no actuation.

---

## Phase B-06 — Governed assistant ask path *(reconciled: mutation boundary)*

- **B-06.1** `POST /api/v1/collaboration/assistant-respond` over `RuleBasedGroundedAssistant` — deterministic, local, **no external LLM**, non-actuating.
- **B-06.2** Grounding bundles from **real** artifacts (summaries, lineage, source ids).
- **B-06.3** Persist responses **and** refusals with hash/lineage + audit correlation.

**Mutation boundary (Operator §10):** the POST is a bounded assistant-response request, **not** a generic mutation endpoint. It must **not** permit orders, broker changes, account changes, governance changes, arbitrary tool execution, or hidden state mutation.

**Acceptance:** ask → grounded response or classed refusal (`ORDER_INSTRUCTION_REFUSED`, `GATE_OPEN_INSTRUCTION_REFUSED`, `SECRET_EXFILTRATION_REFUSED`, `UNBOUNDED_TOOL_REQUEST_REFUSED`, `GROUNDING_REQUIRED`); auditable records; no state mutation; no actuation; no external network calls.

---

## Phase B-07 — Cross-cutting hardening & certification-prep

- **B-07.1** Observability: metrics/traces/logs with correlation IDs for every new pipeline.
- **B-07.2** Security review of all new endpoints: RBAC, input validation, rate limiting (close the W7-U07 "formally deferred" gap), secret-marker redaction, 401 handling, no hidden actuation.
- **B-07.3** Performance/load: concurrency, WS fan-out, DB indexing for report queries.
- **B-07.4** Assemble Doc 11 evidence (security, secrets, state, error, deployment, performance, UX, operational). **Certification itself remains a separate Operator/ITRGA decision.**

---

## X-01 — End-to-end platform verification (joint gate, reconciled §20)

Added per Operator finding §20 — the most important recommendation. Neither "backend complete" nor "frontend complete" proves the platform works. A final joint gate must demonstrate the **operator workflow end-to-end**:

```
Market data → Data/Feature pipeline → Model → Inference → Signals
   → Intelligence → Alerts → Terminal presentation → Research/Evidence
   → Assistant → Governance/Security
```

**Acceptance question:** *Can the operator perform the intended AXIOM workflow end-to-end using real, traceable data while all security, research-only, and non-actuation controls remain intact?*

**Product-level completion workflow (Operator §21):**

```
Select instrument → Market info loads → Chart renders → Technical context available
   → Signal available or honestly withheld → Intelligence available
   → Research available → Evidence/lineage traceable → Risk context where supported
   → Assistant grounded where authorized → Uncertainty/limitations visible
   → No actuation pathway exists
```

---

## Sequencing summary

| Order | Units | Notes |
|-------|-------|-------|
| 1 | B-00 + B-06 | B-06 off critical path; start in parallel |
| 2 | B-01 → B-02 | strictly ordered |
| 3 | B-03 | after B-02.6 |
| 4 | B-04 | families parallel, after B-02/B-03 |
| 5 | B-05 | after B-03 |
| 6 | B-07 | continuous from B-03 |
| 7 | **X-01** | joint, after B-07 + F-06 |

**Critical path:** B-00 → B-01 → B-02 → B-03 → (B-04/B-05) → B-07 → X-01.
