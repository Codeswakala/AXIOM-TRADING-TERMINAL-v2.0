# AXIOM V2 — Frontend and Terminal Roadmap (UPDATED EDITION U2)

| Field | Value |
|---|---|
| Document ID | AXIOM-V2-FE-ROADMAP-002 |
| Supersedes | AXIOM-V2-FE-ROADMAP-001 (on Operator adoption of this edition) |
| Status | **UPDATED EDITION U2 — PENDING OPERATOR ADOPTION** |
| Relationship to V1 | Evolves the existing terminal; preserves supported V1 routes/capabilities unless an explicit breaking change is approved |
| Implementation authority | **NONE conferred by this document** |
| Approval chain (per unit) | Operator adoption of this roadmap → unit Build Order → DA design plan → fail-first evidence → DA implementation + evidence pack → **Operator visual approval (evidence-shaped)** → ITRGA determination → only then the next unit |
| Authorship note | Consolidated by ITRGA hand, 2026-09-10, integrating the Operator's serial one-surface method; bands FE-0…FE-10 preserved in substance from -001 |
| Reference custody | The "supplied visual-reference consultation set" (UI prototypes) is **absent from the ITRGA corpus** (full-tree search, 2026-09-10); pending Operator transmission. Until absorbed: references register as PENDING; AXIOM-identity defaults govern; no unit may cite them as review inputs |

---

## PREAMBLE — What this edition changes (changelog R-1…R-5)

- **R-1 — Serial one-surface cadence, elevated to law (§A).** Units are exactly one surface wide; at most one unit is ever in build; the Operator approves the rendered output of each unit before the next opens. This is the Operator's deliberate correction of the v1 wave-batching failure mode, recorded as deliberate.
- **R-2 — Sign-in inserted as the first build unit (FE-U01).** -001 mapped the sign-in surface as Adopt/adapt without owning it in a band; it is now an explicit unit, first in sequence.
- **R-3 — Panel-level unit sequence pinned (§C).** Bands FE-0…FE-10 are re-sliced into eighteen single-surface units FE-U01…FE-U18. Three units (paper, broker, live) remain GATE-BLOCKED behind their backend authorizations.
- **R-4 — Governance/evidence coverage closed (FE-U17).** -001's adoption matrix carried a governance/evidence control room that no band owned; the unit is now explicit, including the **live-execution corridor console** — closing the evidence-pinned gap: the fielded BE-12 surface (21 paths / 22 operations per mount, 2 mounts) has zero UI. Read-only, register-true, GET-only; needs no gated authorization; independently schedulable.
- **R-5 — Register alignment:** band references follow the adopted 2026-09-06 re-enumeration (BE-9 broker visibility: OPERATING · BE-11 paper bridge: IN COMMISSIONING · BE-12 live-exec capability: CLOSED, capability-complete, lane locked · the parked live-activation campaign: **its band id re-keys at its own adjudication** — the BE-13 number belongs to Governed External AI Provider Adapters per the amendment).

---

## §A. THE SERIAL CADENCE LAW (new — governs everything below)

1. **One surface = one unit.** A unit owns exactly one rendered surface (one route or one anchored panel family). Nothing else is implemented, restyled, or touched.
2. **One unit at a time.** A new unit's Build Order may not issue while any unit is in build. FE-U01 opens first.
3. **The unit loop (complete, in order):** unit Build Order → DA design plan → fail-first tests → DA implementation → DA evidence pack → **Operator visual approval** → ITRGA determination → closure → next unit.
4. **Approval is evidence-shaped (self-proving):** each unit BO pins — the surface contract; viewport pins (1440×900 desktop, 390×844 narrow, unless amended); the interaction script; the state matrix (loading / empty / error / denied / stale / degraded / unknown); prohibition scans; V1 route regression. The DA's evidence pack = captured renders + script transcript + scans. **Operator visual approval is recorded as an Operator Decision naming the evidence pack id** — approval attaches to artifacts, never to recollection. ITRGA determination follows on that same pack.
5. **No silent rejection loops:** if the Operator's eye rejects the output, the DA responds with a corrective cycle under the same unit — the loop does not advance and does not widen scope.
6. **V1 preservation stands:** V1 routes must not silently break; each unit ships its V1 regression evidence.

## §B. Frontend invariants (from -001, unamended — every unit preserves all nine)

1. One terminal, not disconnected products — stable global shell, shared design system, consistent terminology, predictable navigation.
2. Truthful mode and provenance — `RESEARCH`/`SIMULATION`/`PAPER`/`LIVE` from authoritative backend state only; source/freshness visible where material.
3. No fabricated UI state — empty/stale/unavailable/denied/unknown/degraded visibly distinct from real results.
4. Presentation is not authority — the frontend never calculates authoritative analytics, risk, account, order, model, or execution state.
5. No direct provider/broker/AI-secret connection from browser code.
6. Execution controls absent until backend authority exists — an attractive order ticket is still prohibited until the dedicated backend and governance gates permit it.
7. Assistant is non-actuating.
8. Accessibility and responsive behavior are baseline, not polish.
9. Visual references require AXIOM adaptation — no copied brand, vendor claim, real quote, market state, provider label, P&L, account, or certification content.

## §C. THE UNIT SEQUENCE (pinned default; amendable only by instrument)

| # | Unit | Source band | Gate |
|---|---|---|---|
| FE-U01 | **Sign-in surface** (AXIOM identity, approved auth flows, no unsupported SSO/reset claims; mode/posture visible at the door) | -001 §4 / FE-1 | none |
| FE-U02 | **Global chrome** (header: identity, command/search, operator identity, time, mode badge, global health · left nav rail, keyboard, collapse, role-aware · route announcements · tokens/primitives consumed by all later units) | FE-1 | none |
| FE-U03 | **Home terminal** (chart-first research home; watchlist w/ source+freshness; instrument context header; first-run onboarding of no-actuation posture; deep-link orientation) | FE-2 | none |
| FE-U04 | **Chart stage** (timeframes, indicators, drawing, annotations, contextual inspector; simulated/live source state truthful) | FE-3 | none |
| FE-U05 | **Market table + feed-health** (sortable quote table w/ provenance; availability/source states; health surface over actual supported instruments) | FE-3 | none |
| FE-U06 | **Signals workspace** (structural/predictive separation, guardrails, freshness, calibration, withholding/refusal) | FE-4 | none |
| FE-U07 | **Intelligence workspace** (correlation/regime/scenario/risk/validation/diagnostics; metadata: source/as-of/version/sample/uncertainty/limitation) | FE-4 | none |
| FE-U08 | **Investigation workspace** (signal rationale, market context, lineage/trace inspector, linked artifacts) | FE-4 | none |
| FE-U09 | **Scenario comparison** (existing persisted reports) | FE-5 | none |
| FE-U10 | **Research management / artifact explorer** (search/filters/collections/tags/metadata/lineage) | FE-5 | none |
| FE-U11 | **Journal + trade-plan research notes** (governed write UX only against audited mutation contracts) | FE-5 | none |
| FE-U12 | **Hypothetical portfolio / risk workspace** | FE-6 | none |
| FE-U13 | **Backtest / replay / simulation workspace** (classification law: backtest ≠ simulation ≠ paper ≠ live, always legible) | FE-6 | none |
| FE-U17 | **Governance & evidence control room** incl. **live-execution corridor console** (read-only, GET-only, register-true: register line, election posture, lock battery with fielded witnesses, door probe with honest absent/present/refused typology) | R-4 | **independently schedulable** — may be advanced by Operator decision without renumbering |
| FE-U14 | **Paper trading UX** (persistent PAPER identity; order-intent form; validation/risk display; explicit confirmation; lifecycle/fill/position/balance/P&L research views) | FE-7 | **GATE-BLOCKED**: paper backend + risk gateway + environment-isolation bands authorized (BE-11 line) |
| FE-U15 | **Broker account visibility + reconciliation UX** (read-first; severity/timestamp/correlation discrepancies; redaction by entitlement) | FE-8 | **GATE-BLOCKED**: broker-visibility backend scope authorized for UI (BE-9 line) |
| FE-U16 | **Controlled live execution UX** (high-salience LIVE identity; confirmation/step-up; lifecycle vocabulary; reconciliation + kill-switch status) | FE-9 | **GATE-BLOCKED + FUTURE**: the parked live-activation campaign adjudicated and built; production certification; separate Operator authorization |
| FE-U18 | **Contextual assistant evolution** (grounded explanation, refusal language, read-only; external provider by separate authorization only) | FE-10 | conditional per -001 FE-10 |

**Sequence rule:** units run in table order; FE-U17 floats by Operator decision; the three GATE-BLOCKED units may not open before their named backend gates — no frontend cue may imply their capability before it exists.

## §D. BAND INDEX (preserved; the units inherit these scopes/guardrails verbatim)

- **FE-0 — V2 UX governance, research, design plan** (docs-only band): inventory; Adopt/Adapt/Exclude register; personas/journeys; page contracts; **final confirmation of the §C sequence as its exit evidence**; evidence-baseline definition. Excludes all visual implementation.
- **FE-1 — Shared shell/design-system evolution** → U02 (+U01's chrome).
- **FE-2 — Research/simulation home terminal** → U03 (required behaviors: route-specific context announcements; no fabricated data; simulated visibly distinct).
- **FE-3 — Market data & chart intelligence surfaces** → U04/U05 (conditional provider states only after authorized contracts; exclusions: no trade panel/order book/order entry/broker connection/real-venue claim/unlabelled external data).
- **FE-4 — Intelligence/signals/investigation/evidence** → U06/U07/U08 (guardrails: no entry/stop/target/R:R/trade-quality/Buy-Sell/execution CTA; bounded analytical language; every figure API-sourced and classified).
- **FE-5 — Scenario/research/journal/artifact** → U09/U10/U11 (guarded mutation UX only with audited contracts + RBAC + specific BO; no false approval labelling).
- **FE-6 — Hypothetical portfolio/risk/backtest/simulation** → U12/U13 (no real account/holdings/balances/margin/positions/live-P&L/order ticket; never as promise).
- **FE-7 — Paper trading UX** → U14 (non-negotiable UX controls incl. unmistakable PAPER identity; ITRGA mode-safety review).
- **FE-8 — Broker visibility/reconciliation UX** → U15 (no credential display; no browser→broker; no order mutation; entitlement redaction).
- **FE-9 — Controlled live execution UX** → U16 (absolute prohibitions incl. no auto-execution, no success without authoritative confirmation, no hidden risk-block/timeout/unknown).
- **FE-10 — Contextual assistant V2** → U18 (permanent prohibitions incl. no execution authority, no hidden provider, no advice framing).

## §E. Required quality gates per unit (from -001 §5, applies to every U-unit)

Approved page/component contract · token/reuse assessment · route/RBAC/feature-flag behavior · browser evidence at the BO's pinned viewports · keyboard, focus, screen-reader announcements, contrast, reduced motion, error/empty states · visual-regression baseline · API-state mapping (loading/ready/stale/unavailable/denied/degraded/unknown) · mode/provenance/uncertainty/limitation visibility where applicable · prohibition scans (trading vocabulary/secret/provider endpoints per the unit's scope) · V1 regression · Delivery Report + evidence index + technical-debt and project-state updates.

## §F. Completion condition (from -001 §6, unamended)

The V2 terminal is not complete when it resembles a professional trading interface. It is complete only when its rendered UI truthfully represents the authorized backend capability, current mode, source, permissions, uncertainty, risk and execution state — and each approved workflow is accessible, evidenced, secure, and governable.

## §G. OPEN ITEMS REGISTERED AT EDITION TIME

1. **Operator adoption of this edition** — pending; nothing herein authorizes anything until then.
2. **UI prototypes reference set** — awaiting Operator transmission; FE-0's Adopt/Adapt/Exclude register records PENDING until absorbed.
3. **Custody (pre-DA cleanliness):** five unauthorized code changes authored in the frontend tree by the ITRGA instance during transgression of 2026-09-10 (enumerated 2026-09-10) — **REVERT recommended before FE-U01's Build Order issues**; disposition word pending with the Operator.
4. **Live-activation campaign band id** — re-keys at its own adjudication (collision with adopted BE-13 = Governed External AI Provider Adapters is hereby avoided in this document's references).
