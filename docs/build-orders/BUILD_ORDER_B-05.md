# AXIOM — BUILD ORDER B-05
## Monitoring & Alerts Emission

| Item | Value |
|------|-------|
| Build Order ID | `BO-B-05` |
| Programme | Backend Operationalization (reconciled v2; predictive track deferred per Operator decision) |
| Authorizing authority | **Operator** (directive of 2026-08-20: "authorized") |
| Predecessors | B-00 → B-04 (all APPROVED WITH OBSERVATIONS) · Reconciliation Determination · predictive deferral |
| Governing documents | `05_SYSTEM_ARCHITECTURE.md` v2.0 §26, §83 · `07_ML_SPEC.md` §Drift Monitoring · `11_PRODUCTION_READINESS_CERTIFICATION.md` |
| Implementer | Development Authority (DA) |
| Reviewer | ITRGA |
| Status | **ISSUED — awaiting DA implementation** |
| Governance Gate | CLOSED (unchanged) · Production NOT CERTIFIED (unchanged) |

---

## 0. Purpose and honest framing

The monitoring layer has **alert-creation methods that are never invoked**: `create_drift_alert`, `create_inference_health_alert`, `create_live_data_stale_alert`, `create_signal_withheld_alert` exist in `MonitoringAlertService`, but a code search confirms **zero callers** — so `GET /alerts` returns `[]` (verified). This is the same "written but unwired" gap B-04 just closed for intelligence.

This order **wires emission**: it connects real trigger conditions to alert creation, so alerts appear when conditions genuinely occur, and remain **inert** (read-state-only acknowledgement, no auto-action, no remediation, no retraining, no actuation).

Two honest scoping facts:

1. **The predictive track is deferred** (Operator decision). Therefore `create_inference_health_alert` and `create_signal_withheld_alert` — which concern the inference/model/signal path — will be **wired for completeness and triggered by explicit health/staleness conditions where those exist**, but will not fire from live model inference (there is no promoted model). Their wiring is proven by tests, not by live predictive events.
2. **Drift detection is itself only partially present** — there is `record_drift_signal` → `DriftMonitoringRecord`, but no automatic drift-detection loop. This order wires alert *emission* from the conditions that exist (data staleness, ingestion health, explicit drift records), and does **not** invent a drift-detection algorithm (that belongs to a future unit if the predictive track resumes).

---

## 1. Objective

1. Wire alert creation to real trigger conditions: data staleness, ingestion/infrastructure health, and (where records exist) drift and inference-health.
2. Preserve the inert/read-state-only acknowledgement semantics.
3. Prove the non-actuation invariant: alerts inform; they never trigger action.
4. Leave the existing list/get/ack surface contract unchanged.

---

## 2. Scope

### B-05.1 — Stale-data alert emission
- **Condition:** the live/simulated market feed's most recent persisted candle is older than a configured staleness threshold (a real, as-of-bounded condition over the W1 live seam).
- **Behavior:** emit `create_live_data_stale_alert` when the condition is met; do **not** spam (deduplicate by condition-key within a cooldown window).
- **Trigger:** an explicit, governed health/staleness check path (endpoint or startup-scoped checker) — on-request or lightweight scheduled check, not a background actor that could drift into actuation.

### B-05.2 — Inference-health & drift alert emission (wired, test-proven)
- **Inference-health:** wire `create_inference_health_alert` to fire on an explicit health-degradation input (test-pinned), and on any real inference-health event that exists. With the predictive track deferred, this fires from *explicit* degraded inputs in tests and the health-check path, not from live inference.
- **Drift:** wire `create_drift_alert` to fire from an existing `DriftMonitoringRecord` whose `drift_detected` is true. Where a drift record is produced by the existing `record_drift_signal` path, an alert is emitted. No new drift-detection algorithm is created.

### B-05.3 — Signal-withheld alert emission (wired, test-proven)
- **Condition:** a signal is withheld at emit (guardrail). With the predictive track deferred, this is wired and test-pinned against explicit withhold inputs; it will not fire from live inference until a model is promoted.

### B-05.4 — Shared emission contract (binding)
Every emitted alert must:
- carry severity, source lineage, timestamp, and a stable condition-key (for deduplication);
- be persisted and audited (actor + correlation id);
- **mutate alert read-state only** — never trading, account, broker, model, analytical-source, or execution state;
- never trigger auto-action, auto-retraining, or remediation;
- remain readable through the existing `GET /alerts` + `ack` surface.

---

## 3. Exclusions (out of scope — do NOT do)

- **No** auto-action, auto-remediation, auto-retraining, or any actuation triggered by an alert.
- **No** new drift-detection or inference algorithm (predictive track deferred).
- **No** broker/account/execution/order surface.
- **No** background actor that could autonomously mutate state — the staleness check is a bounded, governed check path only.
- **No** ML model, prediction, or promotion.
- **No** weakening of the threshold gate, tier rule, or chronology guard.
- **No** frontend changes (F-04 presentation comes later).
- **No** modification of the governance hierarchy or constitutional documents.
- **No** repository publication (custody model).

---

## 4. Exact deliverables

1. Alert-emission wiring (stale-data, inference-health, drift, withheld-signal) with deduplication cooldown.
2. A governed staleness/health check path (endpoint or startup-scoped checker).
3. Persisted-alert evidence: alerts appear when conditions are met, with severity/lineage/timestamp/condition-key.
4. Non-actuation + read-state-only evidence (test-pinned).
5. Tests (new/churn) for: emission, dedup, ack read-state-only, no-actuation.
6. Delivery Report (§9) with relay-accurate transmission manifest.

---

## 5. Dependencies

- **Upstream:** B-00 (provenance) · B-01 (data) · B-02 (threshold gate, unchanged) · B-04 (intelligence generation — alerts may reference report-family health).
- **Downstream:** F-04 (alerts center presentation) · X-01 (end-to-end).
- **Independent of:** any promoted model. Predictive deferral does not block this order (B-05.2/B-05.3 are wired and test-proven, not live-inference-dependent).

---

## 6. Allowed files / components

- `backend/app/trading_intelligence/monitoring/*` (emission wiring; no alert *semantics* weakening).
- `backend/app/api/routes/monitoring_alerts.py` (add the governed check/emit path; list/get/ack unchanged).
- `backend/app/market/live_service.py` and `backend/app/ingestion/*` (read-only staleness/health inputs; no feed mutation).
- `backend/app/core/config.py` (staleness threshold + cooldown settings, if needed).
- `backend/tests/**` (new/churn tests).
- `backend/docs/**` (any ADR for the emission contract).
- The Delivery Report.

Anything outside this list is **not authorized**.

---

## 7. Security & integrity constraints (binding)

- All alert/check endpoints operator-authenticated; no unauth emission or acknowledgement.
- Alerts are **inert**: ack mutates read-state only; no auto-action; no remediation; no retraining.
- Deduplication must be bounded (cooldown window) to avoid unbounded alert spam.
- No secrets/credentials; no new external network surface.
- The threshold gate, tier rule, and chronology guard are unaffected and unchanged.

---

## 8. Acceptance criteria

- [ ] Stale-data alert fires when the persisted-feed staleness threshold is genuinely exceeded; deduped within cooldown.
- [ ] Inference-health and drift alerts fire from explicit (test-proven) inputs; signal-withheld fires from explicit withhold inputs.
- [ ] Every emitted alert carries severity, lineage, timestamp, condition-key.
- [ ] `ack` mutates read-state only (test-pinned); no auto-action/actuation (test-pinned).
- [ ] Existing `GET /alerts` + `ack` surface returns emitted alerts unchanged in contract.
- [ ] Full backend suite green; new tests executed with output.

---

## 9. Evidence requirements (custody model + CA-TRANSMIT-1, hard gate)

**Binding (CA-TRANSMIT-1):** artifacts must be uploaded and confirmed against the review channel. A declared-but-untransmitted artifact is an automatic CORRECTION REQUIRED. B-04 demonstrated the discipline; it is now the standing standard.

| Item | Class | Form |
|------|-------|------|
| Patch artifact + per-file SHAs + `git apply --check` transcript | Level I | patch + transcript |
| Executed test output (new/churn) | Level II | run transcript |
| Emission evidence (condition → persisted alert, with fields) | Level I | API/query probe output |
| Dedup evidence (repeat condition → no duplicate within cooldown) | Level I | probe output |
| Transmission manifest (relay-accurate) | — | table in Delivery Report |
| Delivery Report | Level III | §10 structure |

---

## 10. Delivery Report structure (required)

1. Claimed scope vs. this Build Order
2. What changed (files + SHAs + chain position)
3. Per-condition emission description (trigger, threshold, dedup key)
4. Emission evidence (condition → persisted alert)
5. Non-actuation + read-state-only evidence
6. Dedup evidence
7. Test evidence (executed)
8. Deviations register
9. Transmission manifest (relay-accurate)
10. Known limitations / technical debt (incl. the deferral note for inference/withheld firing)

---

## 11. Rollback / containment

- Alert rows are additive; revert = drop rows, revert patch.
- No schema migration authorized by default.
- No data produced affects production (Gate CLOSED).

---

## 12. Completion condition

Complete when: all §8 criteria met, evidence (§9) transmitted and verified, the Delivery Report submitted, **and ITRGA issues its independent determination**. A DA declaration of completion is not evidence and does not close this unit.

**Next authorization state:** upon ITRGA approval of B-05, B-06 (Governed Assistant ask path) may be issued, and F-04 (alerts center) is unblocked.

---

**End of Build Order B-05**
