# AXIOM — BUILD ORDER X-01
## End-to-End Platform Verification (Backend Tier)

| Item | Value |
|------|-------|
| Build Order ID | `BO-X-01` |
| Programme | Backend + Frontend operationalization — the joint verification gate |
| Authorizing authority | **Operator** (directive of 2026-08-20: "authorized") |
| Predecessors | B-00 → B-07 (all APPROVED WITH OBSERVATIONS) · Reconciliation Determination · predictive deferral |
| Governing documents | `11_PRODUCTION_READINESS_CERTIFICATION.md` · Reconciliation Determination §20–21 · `05_SYSTEM_ARCHITECTURE.md` v2.0 §59 |
| Implementer | Development Authority (DA) |
| Reviewer | ITRGA |
| Status | **ISSUED — awaiting DA implementation** |
| Governance Gate | CLOSED (unchanged) · Production NOT CERTIFIED (unchanged) |

---

## 0. Purpose and honest framing (read first — this determines the scope)

X-01 is the **joint verification gate** — the question it answers is:

> *Can an operator perform the intended AXIOM workflow end-to-end using real, traceable data while all security, research-only, and non-actuation controls remain intact?*

**A verified sequencing fact scopes this order (verified by ITRGA against the current code):**

- The **backend is complete** (B-00 → B-07).
- The **frontend presentation units (F-01 → F-06) were never executed.** Specifically: the frontend intelligence surface calls only **GET (list)**, not the B-04 generation POSTs; the assistant surface is **read-only** (no ask path — F-01 not built); the alerts center, lineage view, and a11y/perf polish (F-02 → F-06) are not built over the new backend seams.

Therefore a **terminal-level** end-to-end pass (operator clicks through the full UI workflow) **cannot be honestly passed yet** — it depends on F-01 → F-06. This order therefore scopes X-01 as its **Backend Tier**:

- **X-01 Backend Tier (this order):** verify the complete operator workflow at the **API/data level** — the full chain from market data → chart/structural analysis → intelligence → alerts → assistant → governance, over real data, with traceability and non-actuation proven at every hop. This is **fully achievable now** and proves the platform's *capability* end-to-end.
- **X-01 Terminal Tier (deferred):** the full UI click-through workflow, sequenced **after** the F-01 → F-06 frontend units are built. It is named here as the remaining step, not attempted prematurely.

**This order does not certify production.** Certification remains a separate Operator/ITRGA decision under Doc 11.

---

## 1. Objective

Prove, with reproducible Level-I/II evidence, that the **backend platform** supports the complete governed operator workflow over real data, and name every remaining gap honestly.

---

## 2. Scope — the verification workflow (each hop must be evidenced)

The DA must execute and evidence this end-to-end chain over the real corpus (`historical:real`):

1. **Market data** — real corpus present, `market_series_metadata` authoritative, ingestion runs/stats non-zero.
2. **Chart / structural analysis** — deterministic indicator-series (including the SMC/ICT structural set: BoS/CHoCH/FVG/structure/swings) computed over real data, no ML dependency.
3. **Research artifacts** — dataset snapshot(s) + split manifest(s) + feature records over real data, tier = research_validation.
4. **Intelligence** — generate (POST) each of the five B-04 families; read back via GET; verify uncertainty/lineage/data-class fields.
5. **Alerts** — trigger emission (staleness/drift/withheld/inference-health); verify dedup; verify ack is read-state-only.
6. **Assistant** — a grounded ask over a real artifact (with source ids + audit); each refusal class; empty-grounding refusal.
7. **Governance & evidence** — audit events present with correlation ids; Doc 11 inventory reflects the executed evidence; posture Gate CLOSED · NOT CERTIFIED.
8. **Non-actuation, end-to-end** — across every hop, verify no order/broker/account/execution/gate mutation and no external network calls (assistant/ML).

---

## 3. Exclusions (out of scope — do NOT do)

- **No** production certification claim (X-01 evidences; it does not certify).
- **No** terminal-level UI verification (that is the deferred Terminal Tier, after F-01 → F-06).
- **No** new features, endpoints, or capabilities — X-01 verifies what exists; it builds nothing.
- **No** ML model training/promotion (predictive track deferred).
- **No** weakening of any gate/guard/tier/refusal invariant.
- **No** fabrication of workflow steps — every hop must use real persisted data, not synthetic scaffolding (the B-DATA corpus is the source).
- **No** frontend changes (F-units are separate).
- **No** modification of the governance hierarchy or constitutional documents.
- **No** repository publication (custody model).

---

## 4. Exact deliverables

1. A **verification report** (§9) walking the eight-hop workflow with per-hop evidence.
2. Evidence artifacts: API probes/logs per hop (generation, alerts, assistant, audit), executed test output, and the honest gap list.
3. The gap list explicitly naming: (a) the deferred Terminal Tier dependency on F-01 → F-06; (b) the predictive-track deferral (no promoted model → predictive signals gated); (c) any other residual deferrals (per-process rate-limit store, multi-instance deployment, load/soak).

---

## 5. Dependencies

- **Upstream:** B-00 → B-07 (all complete) + B-DATA (real corpus).
- **Downstream:** the deferred **X-01 Terminal Tier** (after F-01 → F-06); any future Doc 11 certification decision.

---

## 6. Allowed files / components

- **No code changes are expected or authorized.** This is a verification order. If the verification surfaces a genuine defect, it is **reported as a finding**, not silently fixed — a corrective Build Order would then be issued separately.
- The only new artifact is the verification report + evidence logs (under `backend/docs/` or the review channel).
- The Delivery Report.

---

## 7. Security & integrity constraints (binding)

- The verification must not weaken or bypass any control while exercising it.
- Evidence must be Level I (direct output) or Level II (executed) — not prose assertions.
- The verification report must be honest: a failed hop is a named gap, not a papered-over pass.
- No secrets/credentials in any evidence artifact.

---

## 8. Acceptance criteria

- [ ] All eight workflow hops evidenced with real data (Level I/II), in the stated order.
- [ ] Non-actuation and no-external-calls proven at every applicable hop (assistant, ML).
- [ ] Intelligence generation → read-back → uncertainty/lineage fields verified.
- [ ] Alert emission → dedup → read-state-only ack verified.
- [ ] Assistant grounded ask + all refusal classes + empty-grounding verified.
- [ ] Audit/evidence trail present with correlation ids.
- [ ] Honest gap list produced (Terminal Tier dependency, predictive deferral, residual deferrals).
- [ ] No code changes introduced; any defect reported as a finding, not silently fixed.
- [ ] Full backend suite still green (executed, output supplied).

---

## 9. Evidence requirements (custody model + CA-TRANSMIT-1, hard gate)

**Binding (CA-TRANSMIT-1):** artifacts uploaded and confirmed against the review channel.

| Item | Class | Form |
|------|-------|------|
| Verification report (8-hop walk + gap list) | Level III | document |
| Per-hop evidence (API probes, generation/alert/assistant/audit logs) | Level I | probe/log output |
| Executed test output (full suite still green) | Level II | run transcript |
| Transmission manifest (relay-accurate) | — | table in Delivery Report |
| Delivery Report | Level III | §10 structure |

---

## 10. Delivery Report structure (required)

1. Claimed scope vs. this Build Order
2. Verification report (the eight-hop walk, per-hop evidence)
3. Non-actuation + no-external-calls summary
4. Gap list (Terminal Tier dependency, predictive deferral, residual deferrals)
5. Any defects found (as findings, not fixes)
6. Test evidence (executed)
7. Transmission manifest (relay-accurate)
8. Known limitations

---

## 11. Completion condition

Complete when: the eight-hop verification is evidenced, the honest gap list is produced, the Delivery Report is submitted, **and ITRGA issues its independent determination**. A DA declaration of completion is not evidence.

**Next authorization state:** upon ITRGA approval of the X-01 Backend Tier:
- The **F-01 → F-06 frontend units** are the remaining work before the **X-01 Terminal Tier** (the full UI click-through).
- Production certification, if ever sought, remains a separate Doc 11 Operator/ITRGA decision.

---

**End of Build Order X-01**
