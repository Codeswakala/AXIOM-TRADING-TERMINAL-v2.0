# AXIOM V2 — Frontend and Terminal Roadmap (CORRECTED EDITION U3)

| Field | Value |
|---|---|
| Document ID | AXIOM-V2-FE-ROADMAP-003 |
| Supersedes | AXIOM-V2-FE-ROADMAP-002 (U2) · AXIOM-V2-FE-ROADMAP-001 — each on Operator adoption of this edition |
| Status | **CORRECTED EDITION U3 — RETURNED FOR FINAL OPERATOR ADOPTION** (responds to Operator adjudication of 2026-09-10: *AMENDMENT REQUIRED — fourteen rulings*, all incorporated) |
| Relationship to V1 | Evolves the existing terminal; preserves supported V1 routes/capabilities unless an explicit breaking change is approved |
| Implementation authority | **NONE conferred by this document** |
| Approval chain (per unit) | Operator adoption of this roadmap → unit Build Order → DA design plan → fail-first evidence → DA implementation + evidence pack → **Operator visual approval (evidence-shaped)** → ITRGA determination → only then the next unit |
| Authorship note | Consolidated by ITRGA hand, 2026-09-10, edition 3: U2 + the Operator's adjudication amendments |
| Reference custody (Operator ruling §9, HOLD adopted) | The visual-reference consultation set (UI prototypes) remains **absent from the ITRGA corpus**. The Adopt/Adapt/Exclude register stays **PENDING** until the references are actually transmitted and absorbed; no unit may claim them as review inputs before that; **AXIOM identity and existing approved design rules remain the governing defaults** |

---

## 0. ADJUDICATION DISPOSITION (Operator rulings of 2026-09-10 → this edition)

| Ruling | Verdict | Disposition in U3 |
|---|---|---|
| §1 Serial cadence | ADOPT | §A unchanged (already exact) |
| §2 FE-U01 sign-in first | ADOPT | §C table row 1; unsupported SSO/reset/identity claims prohibited (§B.9, U01 scope) |
| §3 BE-11 state was stale | AMEND | **BE-11 OPERATING · SEEDS ARMED**, first cited paper intent witnessed — updated in §Preamble R-5, §C, §D |
| §4 FE-U14 dependency semantics | AMEND | §C gate: **DEPENDENCY SATISFIED … own Build Order required** (backend present; frontend NOT thereby authorized); PAPER identity + mode-safety preserved |
| §5 FE-U15 dependency semantics | AMEND | Same treatment (BE-9 OPERATING); no direct broker access/credentials/broker-write (§B.5) |
| §6 FE-U16 current gate | ADOPT | Remains FUTURE-GATED (parked live-activation campaign F01/unadjudicated + certification + separate authorization); prohibitions preserved in §D |
| §7 FE-U17 scheduling rule | AMEND | **Removed from the ordered chain**; standalone exception block (§C.2): commissionable ONLY by explicit Operator decision |
| §8 Backend dependency semantics | AMEND | New §C.1 state model, applied throughout |
| §9 Visual-reference HOLD | ADOPT | Header custody line §0-table; §G.2 |
| §10 Custody/clean baseline | AMEND/HOLD | **RESOLVED 2026-09-10** — evidence §G.3; recorded as pre-FE-U01 state |
| §11 Nine invariants | ADOPT | §B unamended |
| §12 Completion condition | ADOPT | §F unamended |
| §13 Final intended sequence | (informative) | §C.3 diagram mirrors the Operator's intended sequence verbatim |
| §14 Authorization boundary | ADOPT | Header authority lines; §G.1 |

## PREAMBLE — Edition changelog

- **R-1 — Serial one-surface cadence, law** (§A), per Operator adoption §1.
- **R-2 — Sign-in is the first build unit (FE-U01)** (adopted §2).
- **R-3 — Panel-level slicing:** bands re-cut into eighteen single-surface units (§C).
- **R-4 — Governance/evidence coverage closed:** FE-U17 established, including the live-execution corridor console (read-only, GET-only, register-true).
- **R-5 — Register alignment (as amended §3):** backend states are named at their CURRENT authoritative values: **BE-9 broker visibility: OPERATING · BE-11 paper bridge: OPERATING · SEEDS ARMED (first cited paper intent witnessed) · BE-12 live-exec capability: CLOSED, capability-complete, lane REGISTERED-LOCKED** · the parked live-activation campaign remains at **F01, unadjudicated** *(nomenclature note §G.4)*.
- **ADJ-1 — Backend dependency semantics (§8 ruling):** the state model of §C.1 is binding across this document.

## §A. THE SERIAL CADENCE LAW (Operator §1 — adopted)

1. **One surface = one unit.** A unit owns exactly one rendered surface (one route or one anchored panel family). Nothing else is implemented, restyled, or touched.
2. **One unit at a time.** A new unit's Build Order may not issue while any unit is in build. FE-U01 opens first.
3. **The unit loop (complete, in order):** unit Build Order → DA design plan → fail-first tests → DA implementation → DA evidence pack → **Operator visual approval** → ITRGA determination → closure → next unit.
4. **Approval is evidence-shaped (self-proving):** each unit BO pins the surface contract; viewport pins (1440×900 desktop, 390×844 narrow, unless amended); the interaction script; the state matrix (loading / empty / error / denied / stale / degraded / unknown); prohibition scans; V1 route regression. The DA's evidence pack = captured renders + script transcript + scans. **Operator visual approval is recorded as an Operator Decision naming the evidence pack id.** ITRGA determination follows on that same pack.
5. **No silent widening:** scope never grows mid-unit; if the Operator's eye rejects the output, the unit takes corrective cycles under the same scope.
6. **V1 preservation stands:** V1 routes must not silently break; each unit ships V1 regression evidence.

## §B. FRONTEND INVARIANTS (Operator §11 — adopted; unamended)

1. One terminal, not disconnected products — stable global shell, shared design system, consistent terminology, predictable navigation.
2. Truthful mode and provenance — `RESEARCH`/`SIMULATION`/`PAPER`/`LIVE` from authoritative backend state only; source/freshness visible where material.
3. No fabricated UI state — empty/stale/unavailable/denied/unknown/degraded visibly distinct from real results.
4. Presentation is not authority — the frontend never calculates authoritative analytics, risk, account, order, model, or execution state.
5. No direct provider/broker/AI-secret connection from browser code.
6. Execution controls absent until backend authority exists — an attractive order ticket is prohibited until the dedicated backend and governance gates permit it.
7. Assistant is non-actuating.
8. Accessibility and responsive behavior are baseline requirements, not polish.
9. Visual references require AXIOM adaptation — no copied brand identity, vendor claim, real quote, market state, provider label, P&L, account, or certification content.

## §C. THE UNIT SEQUENCE

### §C.1 BACKEND DEPENDENCY SEMANTICS (Operator §8 — binding)

```text
BACKEND CAPABILITY ABSENT          →  GATE-BLOCKED
BACKEND CAPABILITY PRESENT         →  DEPENDENCY SATISFIED
FRONTEND IMPLEMENTATION            →  OWN BUILD ORDER REQUIRED
                                   →  OWN EVIDENCE / OPERATOR VISUAL APPROVAL
                                   →  ITRGA DETERMINATION
```

A backend **operating** state is never frontend implementation authorization. It changes only the dependency column — every unit still requires its own complete loop (§A.3).

### §C.2 The ordered chain (FE-U01 … FE-U18) + one named exception

| # | Unit | Source band | Dependency state (§C.1) |
|---|---|---|---|
| FE-U01 | **Sign-in surface** — AXIOM identity; approved auth flows; mode/posture visible at the door; no unsupported SSO/reset/identity claims | §D FE-1/§4 | DEPENDENCY SATISFIED (auth service) — own BO required |
| FE-U02 | **Global chrome** — header (identity, command/search, operator identity, time, mode badge, global health) · left nav rail (keyboard, collapse, role-aware) · route announcements · token/primitive foundation consumed by later units | FE-1 | DEPENDENCY SATISFIED — own BO required |
| FE-U03 | **Home terminal** — chart-first research home; watchlist w/ source+freshness; instrument context header; first-run onboarding of no-actuation posture; deep-link orientation | FE-2 | DEPENDENCY SATISFIED — own BO required |
| FE-U04 | **Chart stage** — timeframes, indicators, drawing, annotations, contextual inspector; simulated/source state truthful | FE-3 | DEPENDENCY SATISFIED (simulated/historical contracts) — own BO required |
| FE-U05 | **Market table + feed-health** — sortable quote table w/ provenance; availability/source states over actual supported instruments | FE-3 | DEPENDENCY SATISFIED — own BO required |
| FE-U06 | **Signals workspace** — structural/predictive separation, guardrails, freshness, calibration, withholding/refusal | FE-4 | DEPENDENCY SATISFIED — own BO required |
| FE-U07 | **Intelligence workspace** — correlation/regime/scenario/risk/validation/diagnostics with metadata (source/as-of/version/sample/uncertainty/limitation) | FE-4 | DEPENDENCY SATISFIED — own BO required |
| FE-U08 | **Investigation workspace** — signal rationale, market context, lineage/trace inspector, linked artifacts | FE-4 | DEPENDENCY SATISFIED — own BO required |
| FE-U09 | **Scenario comparison** — existing persisted reports | FE-5 | DEPENDENCY SATISFIED — own BO required |
| FE-U10 | **Research management / artifact explorer** | FE-5 | DEPENDENCY SATISFIED — own BO required |
| FE-U11 | **Journal + trade-plan research notes** — governed write UX only against audited mutation contracts | FE-5 | DEPENDENCY SATISFIED — own BO required |
| FE-U12 | **Hypothetical portfolio / risk workspace** | FE-6 | DEPENDENCY SATISFIED — own BO required |
| FE-U13 | **Backtest / replay / simulation workspace** — classification law: backtest ≠ simulation ≠ paper ≠ live, always legible | FE-6 | DEPENDENCY SATISFIED — own BO required |
| FE-U14 | **Paper trading UX** — persistent unmistakable PAPER identity; order-intent form; validation/risk display; explicit confirmation; lifecycle/fill/position/balance/P&L research views | FE-7 | **DEPENDENCY SATISFIED — BE-11 OPERATING · SEEDS ARMED (first cited paper intent witnessed). Frontend implementation NOT thereby authorized: own Build Order + complete loop required. ITRGA mode-safety review at its gate.** |
| FE-U15 | **Broker account visibility + reconciliation UX** — read-first; discrepancy severity/timestamp/correlation; entitlement redaction | FE-8 | **DEPENDENCY SATISFIED — BE-9 OPERATING. Own Build Order + complete loop required. No direct broker access, no credentials, no broker-write (§B.5).** |
| FE-U16 | **Controlled live execution UX** — high-salience LIVE identity; confirmation/step-up; lifecycle vocabulary; reconciliation + kill-switch status | FE-9 | **FUTURE-GATED** — parked live-activation campaign (F01, unadjudicated) adjudicated AND built AND production-certified + separate Operator authorization. Until then: ABSENT → GATE-BLOCKED. No UI may imply availability. |
| FE-U18 | **Contextual assistant evolution** — grounded explanation, refusal language, read-only; external provider only by separate authorization | FE-10 | DEPENDENCY SATISFIED for pre-external scope — own BO required; conditional scope per §D FE-10 |

### §C.3 FE-U17 — the named exception (Operator §7 — the authoritative rule)

> **FE-U17 (Governance & evidence control room, incl. the live-execution corridor console) is an explicitly independently schedulable exception to the table sequence and may be commissioned ONLY by an explicit Operator decision. Its position in any table does not imply execution between FE-U13 and FE-U14 or at any other place. Dependency state: DEPENDENCY SATISFIED (read-only, GET-only surfaces; no gated backend capability required) — its own Build Order and complete loop still apply.**

Scope (unchanged): register line; the standing election (zero-row posture); lock battery with fielded witnesses; census law (21 paths / 22 operations per mount, 2 mounts = 42); door probe with honest absent / present / refused typology. Read-only, register-true, mutating nothing.

### §C.4 The Operator's intended sequence (ruling §13 — mirrored)

```text
CLEAN FRONTEND BASELINE
        ↓
FE-0 GOVERNANCE / DESIGN FOUNDATION
        ↓
FE-U01 SIGN-IN → FE-U02 GLOBAL CHROME → FE-U03 HOME TERMINAL
        ↓
FE-U04 CHART → FE-U05 MARKET TABLE → FE-U06 SIGNALS → FE-U07 INTELLIGENCE
        ↓
FE-U08 INVESTIGATION → FE-U09 SCENARIO → FE-U10 RESEARCH / ARTIFACTS
        ↓
FE-U11 JOURNAL / RESEARCH NOTES → FE-U12 PORTFOLIO / RISK
        ↓
FE-U13 BACKTEST / REPLAY / SIMULATION → FE-U14 PAPER
        ↓
FE-U15 BROKER VISIBILITY → FE-U16 LIVE EXECUTION → FE-U18 CONTEXTUAL ASSISTANT

FE-U17 GOVERNANCE / EVIDENCE: independently schedulable by explicit Operator decision
```

This sequence remains subordinate to the unit-by-unit governance loop (§A.3).

## §D. BAND INDEX (preserved; units inherit scopes/guardrails verbatim)

- **FE-0 — V2 UX governance, research, design plan** (docs-only): inventory; Adopt/Adapt/Exclude register (**PENDING** reference-set transmission, per §9 ruling); personas/journeys; page contracts; final confirmation of the §C sequence; evidence-baseline definition. Excludes all visual implementation.
- **FE-1 — Shared shell/design-system evolution** → U02 (+U01's chrome).
- **FE-2 — Research/simulation home terminal** → U03: route-specific context announcements; no fabricated data; simulated visibly distinct from any future real source.
- **FE-3 — Market data & chart intelligence** → U04/U05: conditional provider states only after authorized contracts; exclusions — no trade panel, order book, order entry, broker connection, real-venue claim, unlabelled external-market data.
- **FE-4 — Intelligence/signals/investigation/evidence** → U06/U07/U08: no entry/stop/target/R:R/trade-quality/Buy-Sell/execution CTA; bounded analytical language; every figure API-sourced and classified.
- **FE-5 — Scenario/research/journal/artifact** → U09/U10/U11: guarded mutation UX only with audited contracts + RBAC + specific BO; no false approval/certification labelling.
- **FE-6 — Hypothetical portfolio/risk/backtest/simulation** → U12/U13: no real account/holdings/balances/margin/positions/live-P&L/order ticket; never as promise.
- **FE-7 — Paper trading UX** → U14: non-negotiable UX controls incl. unmistakable PAPER identity in shell, header, ticket, confirmation, status, account, position, reports, assistant context; ITRGA review of mode-safety behavior.
- **FE-8 — Broker visibility/reconciliation UX** → U15: no credential display; no browser→broker traffic; no order create/cancel/modify; entitlement redaction.
- **FE-9 — Controlled live execution UX** → U16: absolute prohibitions — no automatic execution from signal/chart/model/assistant/UI state; no "success" without authoritative backend/broker confirmation; no generic default account/provider selection; no hiding risk blocks, discrepancy, timeout, or unknown states.
- **FE-10 — Contextual assistant V2** → U18: permanent prohibitions — no execution authority; no order verbs via natural language; no broker secrets/accounts in prompts beyond governed minimized context; no hidden external provider; no unsupported advice framing.

## §E. REQUIRED QUALITY GATES PER UNIT (unamended)

Approved page/component contract · token/reuse assessment · route/RBAC/feature-flag behavior · browser evidence at the BO's pinned viewports · keyboard, focus, screen-reader announcements, contrast, reduced motion, error/empty states · visual-regression baseline · API-state mapping (loading/ready/stale/unavailable/denied/degraded/unknown) · mode/provenance/uncertainty/limitation visibility where applicable · prohibition scans per unit scope · V1 regression · Delivery Report + evidence index + technical-debt and project-state updates.

## §F. COMPLETION CONDITION (Operator §12 — adopted; unamended)

The V2 terminal is not complete when it resembles a professional trading interface. It is complete only when its rendered UI truthfully represents the authorized backend capability, current mode, source, permissions, uncertainty, risk and execution state — and each approved workflow is accessible, evidenced, secure, and governable.

## §G. OPEN ITEMS AT EDITION TIME

1. **Final Operator adoption of this U3 edition** — pending; nothing herein authorizes anything until then (Operator ruling §14 carried: adoption establishes programme structure only; every unit still requires its own Build Order and complete loop).
2. **UI prototypes reference set** — HOLD (ruling §9): register stays PENDING until transmission and absorption; AXIOM identity/approved design rules govern in the meantime.
3. **Custody — RESOLVED 2026-09-10 (pre-FE-U01 state of record):** the five unauthorized frontend code changes of the 2026-09-10 transgression were reverted/removed this date; evidence: `git status --short -- frontend/` → **empty (clean baseline)** · zero residual corridor references in `frontend/src` (grep). Forthcoming factors recorded alongside: a pre-existing unrelated modification to `docs/governance/ITRGA_PRACTICE_NOTE_V2_PACK_DISCIPLINE_001.md` exists in the working tree (NOT part of the transgression, untouched by the cleanup; Owner: Operator/DA for its own disposition); the review record `FRONTEND_STATE_MAP_2026-09-10.md` remains at repo root as an ITRGA state-read document (retention/deletion at Operator election — it is not code).
4. **Nomenclature reconciliation (register note):** the Operator's adjudication references the parked campaign as the "BE-13 live-activation campaign"; the adopted 2026-09-06 backend amendment keys **BE-13 = Governed External AI Provider Adapters**. Both statements stand in their texts; the campaign's band id is formally reconciled at its own adjudication (substance unaffected: F01 parked, unadjudicated, no code movement).
