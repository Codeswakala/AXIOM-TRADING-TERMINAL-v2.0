# AXIOM — BUILD ORDER F-03
## Intelligence Presentation (all five families + governed generation)

| Item | Value |
|------|-------|
| Build Order ID | `BO-F-03` |
| Programme | Frontend Operationalization (Visual Blueprint approved) |
| Authorizing authority | **Operator** (directive 2026-08-21: "authorized") |
| Predecessors | F-02 CLOSED · B-04 (intelligence generation endpoints — delivered, no frontend caller) |
| Governing documents | `VISUAL_BLUEPRINT.md` · `08_UI_UX_SPEC.md` §Research Workspace · Reconciliation Determination (research-artifact generation ≠ actuation) |
| Implementer | Development Authority (DA) |
| Reviewer | ITRGA |
| Status | **ISSUED — awaiting DA implementation** |
| Governance Gate | CLOSED (unchanged) · Production NOT CERTIFIED (unchanged) |

---

## 0. Purpose and framing

B-04 delivered five **generation** endpoints (`POST /intelligence/{correlation,regime,scenario,portfolio-risk,signal-validation}-reports`) plus their read surfaces. The frontend, however:

- has **no generation client** (verified: the only POSTs are alerts-ack, workspace prefs, collections, journal, trade-plans, annotations — none for intelligence);
- renders only **3 of 5 families** in `TerminalIntelligenceCards` (regime, correlation, signal-validation) — **scenario and portfolio-risk are absent**;
- has a read bundle (`fetchInstitutionalIntelligenceBundle`) but no trigger to produce reports.

This order completes the intelligence presentation: all five families rendered (with uncertainty/limitations/lineage), plus a **governed generation surface** that calls the B-04 POSTs. Generation is **research-artifact creation only** — it never actuates, never emits a signal, and is framed as such.

---

## 1. Objective

1. Render all five intelligence families over real data, each with uncertainty, sample counts, limitations, lineage, and `data-class` labels.
2. Add a governed generation surface (trigger → B-04 POST → persisted report → re-read).
3. Preserve the research-only framing and the honest empty/insufficient-data states.

---

## 2. Scope

### F-03.1 — Generation client
- Add `generateCorrelationReport`, `generateRegimeReport`, `generateScenarioReport`, `generatePortfolioRiskReport`, `generateSignalValidationReport` (Bearer, correct request schemas, structured 4xx/insufficient-data mapping) to `client.ts`.

### F-03.2 — Five-family rendering
- Extend `TerminalIntelligenceCards` (or a companion) to render **all five**: correlation (r + CI + n), regime (label + confidence), scenario (name + hypothetical return + assumptions), portfolio-risk (max drawdown + vol + stress loss), signal-validation (sample + outcome status).
- Each card carries: uncertainty (where present), sample count, limitations, `data-class` label, lineage (source artifact ids / report hash prefix), and the research-only framing ("not a signal, not causation, not a prediction, not financial advice").

### F-03.3 — Governed generation surface
- A "Generate" affordance per family (or one intelligence-wide trigger), calling the B-04 POSTs, then re-reading via the existing bundle.
- Generation is framed as **research-artifact creation**: the UI must state the research-only boundary and never present it as an action/trade/actuation.
- **Honest insufficient-data handling:** render the structured 422 (`insufficient_data: true`) as an honest notice, not a crash or fabricated report.
- No background/automatic generation (on-request only, matching B-04).

### F-03.4 — Non-actuation + honesty (binding)
- No execution/broker/account/signal controls anywhere in the intelligence surface.
- No client-side recomputation of metrics (render server-stored values only — already a standing invariant).
- No fabricated reports while loading or on error.

---

## 3. Exclusions (out of scope — do NOT do)

- **No** backend change (pure consumer of B-04).
- **No** ML model/prediction/promotion (predictive track deferred).
- **No** signal emission, alert emission, or actuation of any kind from generation.
- **No** background/scheduled generation.
- **No** weakening of accessibility, themes, or the design language (F-00).
- **No** modification of the governance hierarchy or constitutional documents.
- **No** repository publication (custody model).

---

## 4. Exact deliverables

1. Five generation client functions + typed request schemas.
2. Five-family rendering (with uncertainty/limitations/lineage/data-class).
3. Governed generation surface + honest insufficient-data handling.
4. Tests (new/churn): generation call contract, five-family render, uncertainty/lineage presence, insufficient-data, no-actuation, no-fabrication.
5. Delivery Report (§9) with relay-accurate manifest + register-in-patch rows.

---

## 5. Dependencies

- **Upstream:** B-04 generation + read endpoints · F-02 (design language, terminal context) · B-DATA (real corpus to generate over).
- **Downstream:** F-04 (alerts), F-05 (lineage), X-01 Terminal Tier.

---

## 6. Allowed files / components

- `frontend/src/api/client.ts` (generation client functions).
- `frontend/src/components/terminal/TerminalIntelligenceCards.tsx` (+ its stylesheet if needed).
- `frontend/src/test/**` + relevant `*.test.tsx` (new/churn).
- `docs/governance/TECHNICAL_DEBT_REGISTER.md` (register-in-patch — **required**).
- The Delivery Report.

Anything outside this list is **not authorized**.

---

## 7. Security & integrity constraints (binding)

- Bearer JWT on generation; 401 handled gracefully.
- Generation is research-artifact creation only; no actuation, no signal, no state mutation beyond the report.
- No client-side metric recomputation (render server values only).
- Accessibility and theme conformance preserved.

---

## 8. Acceptance criteria

- [ ] Five generation client functions post to the correct B-04 endpoints with Bearer auth.
- [ ] All five families render with uncertainty/sample/limitations/lineage/data-class (test-pinned).
- [ ] Generation trigger produces a persisted report and re-reads it (test-pinned, mocked or live).
- [ ] Insufficient-data (structured 422) renders honestly (test-pinned).
- [ ] Research-only framing present; no actuation controls (test-pinned no-actuation scan).
- [ ] No fabricated metrics (server-values-only invariant).
- [ ] Register rows ship in the patch (register-in-patch).
- [ ] Full frontend suite green (`npm test`) + typecheck green (`tsc -b`); executed output supplied.

---

## 9. Evidence requirements (custody model + CA-TRANSMIT-1 + register-in-patch)

**Binding:** CA-TRANSMIT-1 (relay-accurate manifest) + register-in-patch.

| Item | Class | Form |
|------|-------|------|
| Patch artifact + per-file SHAs + `git apply --check` transcript | Level I | patch + transcript |
| Executed frontend test output + typecheck | Level II | run transcript |
| Screenshot captures (five families over real data; generation; insufficient-data) | Level I | images |
| Transmission manifest (relay-accurate) | — | table in Delivery Report |
| Delivery Report | Level III | §10 structure |

---

## 10. Delivery Report structure (required)

1. Claimed scope vs. this Build Order
2. What changed (files + SHAs + chain position)
3. Generation client description (5 functions + schemas)
4. Five-family rendering description (uncertainty/limitations/lineage/data-class)
5. Governed generation surface + insufficient-data handling
6. Screenshot evidence
7. Non-actuation + no-fabrication evidence
8. Test evidence (executed)
9. Deviations register
10. Register rows in patch (confirmed) + transmission manifest (relay-accurate)

---

## 11. Rollback / containment

- Frontend-only; revert = revert patch. No backend change, no schema change, no new dependency.

---

## 12. Completion condition

Complete when: all §8 criteria met, evidence (§9) transmitted and verified, the Delivery Report submitted, **and ITRGA issues its independent determination**. A DA declaration of completion is not evidence and does not close this unit.

**Next authorization state:** upon ITRGA approval of F-03, **F-04 (alerts center)** may be issued.

---

**End of Build Order F-03**
