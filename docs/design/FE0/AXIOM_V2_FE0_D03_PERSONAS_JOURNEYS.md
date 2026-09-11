# FE-0 / D0-3 — Personas + Journey Map (Classification-Lawful)

| Field | Value |
|---|---|
| Document ID | AXIOM-V2-FE0-D03-001 |
| Parent | AXIOM-V2-FE0-DESIGN-PLAN-001 (under AXIOM-V2-DPR-001) |
| Author | DA · 2026-09-10 |
| Vocabulary law | Research / simulation / paper vocabulary only. LIVE appears solely as a governance FACT (REGISTERED-LOCKED posture displayed truthfully), never as a journey the UI offers |

## 1. Personas (research-grade; grounded in the as-built role model)

### P-1 — The Operator (constitutional approver) — role `admin`
The programme's sole custody and adoption authority; also the U3 §A.4 visual approver.
- Uses the terminal as its most demanding reviewer: every rendered claim must be traceable to backend state (his own standing law: evidence-shaped approval, pack-id-named decisions).
- Journey-critical needs: mode/posture visibility everywhere; governance/evidence surfaces that read like the registers he adjudicates; zero fabricated state (he will reject on sight — §A.5 exists because he does).
- RBAC: all 16 workspaces (`admin` ∈ every `allowedRoles`).

### P-2 — Research analyst — role `operator`
Daily-driver persona: markets → signals → intelligence → investigation → journal.
- Needs: chart-first home, provenance/freshness on every figure, structural/predictive separation (FE-U06 law), bounded analytical language (no entry/stop/target/Buy-Sell — FE-4 guardrails).
- Never sees an execution control: the platform posture is research/simulation; paper UX arrives only at FE-U14 under its own BO, PAPER-branded beyond mistake.

### P-3 — Simulation/backtest engineer — role `operator`
Runs backtests, replays, simulated-execution research (BE-7 surfaces; `/execution-research`).
- Needs: the FE-U13 classification law legible at all times (backtest ≠ simulation ≠ paper ≠ live); run/fill/ledger views labeled SIMULATED at the component level (as-built pattern already does this — carried forward).

### P-4 — Governance reviewer (ITRGA-shaped consumer) — role `operator` (read-oriented), or `admin`
Reads evidence, audit events, registers, capability maturity; future primary consumer of FE-U17 (uncommissioned; explicit Operator decision only).
- Needs: register-true renders, honest absent/present/refused typology, citation-grade timestamps/hashes displayed verbatim.

### P-5 — Unprivileged/aspirant session — role `unprivileged`
Exists in the type system; default `allowedRoles` excludes it from all 16 workspaces.
- Journey is short and must be honest: sign-in succeeds → every route renders the truthful ACCESS DENIED element (AAE-003). No fake-empty dashboards.

## 2. Journey map (core flows; each names its owning unit)

### J-1 — Arrival and sign-in (FE-U01)
`/login` → AXIOM identity → credentials (username/password only — the backend's actual contract; no SSO/reset affordances, ruling §2) → error path: typed 401 detail rendered as error state (never "try again later" fiction) → success → session established → redirect to `state.from` or `/`.
Posture at the door: mode/posture visibility per the D0-4 truthful-posture pattern (backend-sourced fact or explicitly-unverified label — never a hardcoded claim).

### J-2 — Orientation (FE-U02 → FE-U03)
Global chrome: identity, command/search, operator identity, clock, mode badge (backend-sourced), global health → home terminal: chart-first, watchlist with source+freshness, first-run onboarding of the no-actuation posture.

### J-3 — Market study (FE-U04 → FE-U05)
Chart stage (timeframes/indicators/drawings/annotations, source state truthful) → market table with provenance and feed-health over actually-supported instruments; unavailable ≠ empty ≠ stale, visibly.

### J-4 — Signal-to-conviction research loop (FE-U06 → FE-U07 → FE-U08)
Signals (structural/predictive separated; withholding/refusal rendered as first-class states) → intelligence (correlation/regime/scenario/risk with as-of/version/sample/uncertainty metadata) → investigation (rationale, lineage/trace, linked artifacts). No trade-quality/execution CTA vocabulary anywhere (FE-4 guardrails).

### J-5 — Scenario and record-keeping (FE-U09 → FE-U10 → FE-U11)
Compare persisted scenario reports → artifact explorer (search/collections/tags/lineage) → journal + trade-plan research notes: governed write UX against the audited collaboration contracts, RBAC-checked, no false approval labels.

### J-6 — Hypothetical portfolio and simulation (FE-U12 → FE-U13)
Hypothetical portfolio/risk (no real account/balances/margin — FE-6 exclusions) → backtest/replay/simulation workspace with the classification law legible per row and per panel.

### J-7 — Paper journey (FE-U14 — dependency satisfied, NOT scheduled here)
Recorded for map completeness only: persistent unmistakable PAPER identity end-to-end. Opens exclusively by its own BO + ITRGA mode-safety review.

### J-8 — Governance reading (FE-U17 — named exception, uncommissioned)
Register line, standing election posture, lock battery witnesses, door-probe typology (absent/present/refused honestly distinct). GET-only. Exists in the map so no other unit quietly absorbs its scope.

## 3. Cross-journey laws (bind every map row)

1. Mode badge truth-chain: badge value ← authoritative backend state (`/api/v1/v2/mode` for authed surfaces) — never a literal.
2. Every figure: API-sourced, classified (research/simulated/paper), freshness-stamped where material.
3. Denial ≠ empty ≠ error ≠ stale ≠ unknown — five different renders, all present in every unit's state matrix.
4. The assistant (FE-U18 future) explains; it never acts (§B.7).
