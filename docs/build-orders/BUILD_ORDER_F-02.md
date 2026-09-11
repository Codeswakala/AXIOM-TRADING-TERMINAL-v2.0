# AXIOM — BUILD ORDER F-02
## Signal Presentation — Two Families (Structural + Predictive)

| Item | Value |
|------|-------|
| Build Order ID | `BO-F-02` |
| Programme | Frontend Operationalization (Visual Blueprint approved) |
| Authorizing authority | **Operator** (directive 2026-08-21: "authorized") |
| Predecessors | F-01 CLOSED · B-03 (predictive signals — gated/deferred) · Reconciliation Determination (CA-RECON-2) |
| Governing documents | `VISUAL_BLUEPRINT.md` · Reconciliation Determination §11/§13 (two signal families) · `08_UI_UX_SPEC.md` §Signal Center |
| Implementer | Development Authority (DA) |
| Reviewer | ITRGA |
| Status | **ISSUED — awaiting DA implementation** |
| Governance Gate | CLOSED (unchanged) · Production NOT CERTIFIED (unchanged) |

---

## 0. Purpose and framing

The Reconciliation Determination (CA-RECON-2) established a binding clarification:

> AXIOM contains **two signal families with different eligibility and dependency rules** — **structural signals** (deterministic, from the market-structure/indicator layer, already operational, no ML dependency) and **predictive signals** (ML-derived, gated on a promoted model). The terminal must **not** collapse them into a single undifferentiated "AI signal."

Current state (verified):

- **Predictive signals** are already rendered by `TerminalSignalStream.tsx` (state filters, verbatim `signal_state`, confidence, rationale, eligibility) — but the predictive track is **deferred** (no promoted model), so the stream is honest-empty, and it is **not yet labeled as the "Predictive (ML)" family**.
- **Structural signals** exist only as **chart overlays** (`IndicatorPane`, `ConfluenceStrip`, `TerminalChartStage` render BoS/CHoCH/FVG/structure as geometry). There is **no structural-signal event surface** — no panel listing "BOS occurred on EURUSD H1 at 12:00" as a discrete signal.

This order: (1) labels and completes the **predictive family** with an honest deferred-empty state, and (2) adds the **structural family** as a distinct, deterministic event surface — both derived from the already-computed server data (no backend change).

---

## 1. Objective

1. Present signals as **two clearly-distinguished families** — Structural and Predictive — never merged.
2. Complete the predictive family: label it "Predictive (ML)", and show an **honest** empty state reflecting the predictive-track deferral (no eligible model).
3. Add the structural family: surface the deterministic market-structure events (BoS / CHoCH / FVG / structure change / swing) as discrete signals, derived from the existing indicator-series data.

---

## 2. Scope

### F-02.1 — Two-family framing (binding)
- A signal surface that separates **Structural** (deterministic) and **Predictive (ML)** — either as two labeled tabs/segments of the existing signal stream, or a family chip/badge on each entry. The two must never be visually indistinguishable.
- The family distinction is derived from **data origin**, not presentation: structural events come from the indicator layer; predictive entries come from `GET /signals/history` (advisory signals). No invented third category.

### F-02.2 — Structural signal family (the new work)
- Derive a **structural event list** from the already-computed indicator series (`fetchIndicatorSeries` with the SMC/ICT set: `BOS55`, `CHOCH55`, `FVG3`, `STRUCT55`, `SWINGS55`) over the active symbol/timeframe.
- Each event renders as a discrete signal: **type** (BOS / CHoCH / FVG / structure-change / swing), **direction** (up/down / bullish/bearish), **time**, **symbol/timeframe**.
- A structural event is **descriptive, not predictive**: it reports "structure broke up at 12:00," never "price will rise." The surface must carry a "structural / descriptive — not a prediction" framing (per the Blueprint's honesty discipline).
- Honest empty state: "no structure events in the current window" when the indicator series yields none.

### F-02.3 — Predictive family completion
- Label the existing `TerminalSignalStream` as the **Predictive (ML)** family.
- Add an **honest deferred-empty state**: with no promoted model, the stream shows "No predictive signals — the predictive track is deferred (no eligible model); deterministic structural signals remain available" rather than a bare empty list.
- Preserve the existing behavior (state filters, verbatim `signal_state`, confidence/uncertainty, rationale, eligibility, non-actuating "no BUY/SELL").

### F-02.4 — Non-actuation + honesty (binding)
- **No** execution/buy/sell/order controls anywhere.
- Neither family may fabricate entries — structural events come only from server-computed indicator series; predictive entries only from persisted advisory signals. No mock data shipped.

---

## 3. Exclusions (out of scope — do NOT do)

- **No** backend change — this consumes the existing indicator-series and advisory-signal read APIs only.
- **No** generation of predictive signals (B-03 remains gated; no model to promote).
- **No** collapsing the two families; **no** relabeling structural events as ML or vice versa.
- **No** actuation controls; **no** external LLM.
- **No** weakening of accessibility or the design language (F-00 tokens/themes).
- **No** modification of the governance hierarchy or constitutional documents.
- **No** repository publication (custody model).

---

## 4. Exact deliverables

1. Two-family signal framing (Structural vs Predictive, visually distinct).
2. Structural-signal event surface (derived from indicator series; descriptive framing).
3. Predictive-family label + honest deferred-empty state.
4. Tests (new/churn): family distinction, structural-event derivation, honest empty states, no-actuation, no fabricated entries.
5. Delivery Report (§9) with relay-accurate manifest + register-in-patch rows.

---

## 5. Dependencies

- **Upstream:** F-01 (design language) · existing `fetchIndicatorSeries` + `fetchAdvisorySignals` clients · B-DATA (real corpus for structural derivation).
- **Downstream:** F-03 → F-06; X-01 Terminal Tier.

---

## 6. Allowed files / components

- `frontend/src/components/terminal/TerminalSignalStream.tsx` (family framing + predictive label).
- A new structural-signal component (e.g. under `frontend/src/components/terminal/`) or extension of the existing dock.
- `frontend/src/api/indicatorRegistry.ts` + `client.ts` (consume existing fetchers; no new backend surface).
- `frontend/src/test/**` + relevant `*.test.tsx` (new/churn).
- `docs/governance/TECHNICAL_DEBT_REGISTER.md` (register-in-patch — **required**).
- The Delivery Report.

Anything outside this list is **not authorized**.

---

## 7. Security & integrity constraints (binding)

- No actuation; no fabricated entries; no external calls beyond the existing local API.
- Structural events must be derived from server-computed indicator series (deterministic, as-of-bounded) — never client-side reinterpretation that could mislabel.
- Accessibility and theme conformance preserved (F-00).
- The predictive empty state must be honest about the deferral, not misleading.

---

## 8. Acceptance criteria

- [ ] Signals present as two distinct families (Structural vs Predictive), visually separable (test-pinned).
- [ ] Structural events render from real indicator-series data (type/direction/time/symbol), with descriptive "not a prediction" framing (test-pinned).
- [ ] Structural empty state is honest ("no structure events") — no fabricated entries.
- [ ] Predictive family labeled; deferred-empty state states the deferral honestly.
- [ ] Existing predictive-stream behavior preserved (filters, verbatim state, confidence, no BUY/SELL).
- [ ] No-actuation invariant (test-pinned).
- [ ] Register rows ship in the patch (register-in-patch).
- [ ] Full frontend suite green (`npm test`) + typecheck green (`tsc -b`); executed output supplied.

---

## 9. Evidence requirements (custody model + CA-TRANSMIT-1 + register-in-patch)

**Binding:** CA-TRANSMIT-1 (relay-accurate manifest) + register-in-patch.

| Item | Class | Form |
|------|-------|------|
| Patch artifact + per-file SHAs + `git apply --check` transcript | Level I | patch + transcript |
| Executed frontend test output + typecheck | Level II | run transcript |
| Screenshot captures (two-family view, structural events, deferred-empty predictive) | Level I | images |
| Transmission manifest (relay-accurate) | — | table in Delivery Report |
| Delivery Report | Level III | §10 structure |

---

## 10. Delivery Report structure (required)

1. Claimed scope vs. this Build Order
2. What changed (files + SHAs + chain position)
3. Two-family framing description
4. Structural-signal derivation (indicator series → event list)
5. Predictive deferred-empty state description
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

**Next authorization state:** upon ITRGA approval of F-02, **F-03 (intelligence presentation)** may be issued.

---

**End of Build Order F-02**
