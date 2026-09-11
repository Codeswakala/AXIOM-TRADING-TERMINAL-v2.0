# AXIOM — BUILD ORDER X-01 TERMINAL TIER
## End-to-End Platform Verification (Full Operator Workflow Through the Terminal)

| Item | Value |
|------|-------|
| Build Order ID | `BO-X-01-TERMINAL` |
| Programme | The final verification gate — the "full working UI" milestone |
| Authorizing authority | **Operator** (directive 2026-08-22: "authorized") |
| Predecessors | Backend B-00 → B-07 + X-01 Backend Tier + B-AUDIT · Frontend F-00 → F-06 (all APPROVED WITH OBSERVATIONS) |
| Governing documents | `11_PRODUCTION_READINESS_CERTIFICATION.md` · Reconciliation §20–21 (product workflow) · `05_SYSTEM_ARCHITECTURE.md` §59 |
| Implementer | Development Authority (DA) |
| Reviewer | ITRGA |
| Status | **ISSUED — awaiting DA implementation** |
| Governance Gate | CLOSED (unchanged) · Production NOT CERTIFIED (unchanged) |

---

## 0. Purpose and honest framing

This is the **final verification** of the programme. The X-01 Backend Tier already proved the API/data-level workflow; the frontend is now complete (F-00 → F-06). This order proves the **terminal-level** question:

> *Can an operator open AXIOM, select an instrument, understand the market, inspect the chart, investigate signals, review intelligence and research, inspect evidence and risk, use the governed assistant for explanation, and retain complete awareness of uncertainty, provenance, governance, and non-actuation boundaries — all without leaving the terminal?*

This is the "full working UI" milestone the Operator set as the gate for resuming predictive trials. It **does not certify production** (that remains a separate Doc 11 decision).

---

## 1. Objective

Execute and evidence the complete governed operator workflow **through the running terminal**, over real data, with traceability and non-actuation proven at every hop — and name any remaining gap honestly.

---

## 2. Scope — the workflow (each hop evidenced at the UI level)

The DA must execute and evidence, in a real browser against the real dev stack:

1. **Login** — the wave-animated login (reduced-motion honored), governance chips visible, auth succeeds.
2. **Navigation legibility** — the six-theme nav (icons + visible labels); theme switch persists across reload.
3. **Instrument selection → watchlist → chart** — real symbol loads; candlestick chart renders; indicator/structural overlays (BoS/CHoCH/FVG) compute.
4. **Structural signals** — the Structural family lists real derived events with provenance ("not a prediction").
5. **Predictive signals** — the Predictive (ML) family renders the honest deferred-empty state.
6. **Intelligence** — generate + read all five report families (correlation/regime/scenario/portfolio-risk/signal-validation) with uncertainty/lineage/data-class.
7. **Alerts** — alerts render with domain filter + timestamp + lineage; ack is read-state-only.
8. **Lineage/evidence** — a lineage panel renders for a real artifact (persisted-only, no fabrication).
9. **Assistant** — a grounded ask over a real artifact; a classed refusal; honest GROUNDING_REQUIRED.
10. **Governance & non-actuation, end-to-end** — Gate CLOSED posture visible; no order/broker/execution/account surface anywhere; audit trail present.

---

## 3. Exclusions (out of scope — do NOT do)

- **No** production certification claim.
- **No** code changes (verification only; defects are reported as findings, not silently fixed).
- **No** new features, endpoints, or capabilities.
- **No** ML model training/promotion (predictive track deferred).
- **No** weakening of any invariant.
- **No** fabrication of workflow steps (real data; honest empty states where applicable).
- **No** repository publication (custody model).

---

## 4. Exact deliverables

1. A **terminal-tier verification report** walking the ten-hop workflow with per-hop UI evidence (screenshots + assertions + backend log correlation).
2. Evidence artifacts: browser-capture log, per-hop screenshots, the audit/backend log cross-references.
3. The honest **gap list** (predictive deferral; any UI gaps found; the performance raw-evidence follow-up from OBS-F06-1).

---

## 5. Dependencies

- **Upstream:** F-00 → F-06 (frontend complete) · X-01 Backend Tier (API-level proof) · B-DATA (real corpus).
- **Downstream:** the Operator's decision to resume predictive trials (the deferred track) — and any future Doc 11 certification.

---

## 6. Allowed files / components

- **No code changes.** Verification scripts/logs/screenshots only (under `docs/evidence/` or the review channel).
- The Delivery Report.
- If the verification surfaces a defect, it is a **finding** (a corrective order follows separately).

---

## 7. Security & integrity constraints (binding)

- The verification must not weaken or bypass any control while exercising it.
- Level I (screenshots, browser assertions, backend logs) or Level II (executed output) — not prose assertions.
- Honest: a failed hop is a named gap, not a papered-over pass.
- No secrets/credentials in any evidence artifact.

---

## 8. Acceptance criteria

- [ ] All ten workflow hops evidenced at the UI level with real data (Level I/II), in order.
- [ ] Navigation legibility + theme persistence verified in-browser.
- [ ] Structural signals render real derived events; predictive signals render the honest deferred state.
- [ ] All five intelligence families generate + render; insufficient-data handled honestly.
- [ ] Alerts render + filter + ack read-state-only.
- [ ] Lineage panel renders persisted-only provenance.
- [ ] Assistant grounded ask + refusal + GROUNDING_REQUIRED verified.
- [ ] Non-actuation end-to-end (no order/broker/execution/account surface) verified.
- [ ] Honest gap list produced.
- [ ] No code changes; any defect reported as a finding.

---

## 9. Evidence requirements (custody model + CA-TRANSMIT-1)

**Binding (CA-TRANSMIT-1):** artifacts uploaded and confirmed against the review channel. **Also:** transmit the F-06 performance raw evidence (`f06_performance.log`, `f06_performance_raw.json`, `f06_cloneside_vitest.log.txt`) to close OBS-F06-1 with this delivery.

| Item | Class | Form |
|------|-------|------|
| Terminal-tier verification report (ten-hop walk + gap list) | Level III | document |
| Browser-capture log (per-hop assertions) | Level I | log |
| Per-hop screenshots | Level I | images |
| Backend log cross-references | Level I | log |
| F-06 performance raw evidence (OBS-F06-1 closure) | Level II | log + JSON |
| Transmission manifest (relay-accurate) | — | table in Delivery Report |
| Delivery Report | Level III | §10 structure |

---

## 10. Delivery Report structure (required)

1. Claimed scope vs. this Build Order
2. Verification report (ten-hop walk, per-hop UI evidence)
3. Non-actuation end-to-end summary
4. Gap list (predictive deferral + any UI gaps)
5. Any defects found (as findings, not fixes)
6. F-06 performance raw evidence (OBS-F06-1 closure)
7. Transmission manifest (relay-accurate)

---

## 11. Completion condition

Complete when: the ten-hop workflow is evidenced at the UI level, the honest gap list is produced, OBS-F06-1 is closed, the Delivery Report is submitted, **and ITRGA issues its independent determination**. A DA declaration of completion is not evidence.

**Next authorization state:** upon ITRGA approval of X-01 Terminal Tier, **the programme is complete**: the platform is operational with a full working UI — the Operator's stated gate for resuming predictive trials. Production certification, if ever sought, remains a separate Doc 11 decision.

---

**End of Build Order X-01 Terminal Tier**
