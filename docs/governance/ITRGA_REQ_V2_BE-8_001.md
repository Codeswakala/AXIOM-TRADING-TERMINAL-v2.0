# ITRGA DESIGN REQUEST — BAND BE-8: PAPER TRADING, PAPER ACCOUNT, RISK GATEWAY
# ITRGA-REQ-V2-BE-8-001 · v1.1.0 · 2026-09-04 · AXIOM Trading Terminal v2.0
# From: ITRGA · To: Replacement Development Authority (DA) · Via: Operator
# Basis: V2_BACKEND_ROADMAP "Band BE-8 — Paper Trading, Paper Account, and
# Risk Gateway" · operator authorization 2026-09-04 · BE-7 closed
# (ITRGA-CLO-V2-0047-BE7-ACT-001, sealed ITRGA-SEAL-V2-0047-BE7-001).
# DELIVERABLE ASKED: a DESIGN DOCUMENT ONLY. No code, no migration, no
# register edits beyond the design doc. (Zero-code rule in force.)

## §1 — Mandated objective (roadmap, verbatim)
"Introduce paper trading only as an isolated, governed environment after a
dedicated paper-trading and execution-security design is approved."
This request IS the trigger for that dedicated design. The design must
specify: paper account model; paper order intent & immutable order lifecycle;
pre-trade risk gateway; paper execution simulator; simulated fills, positions,
balances, margin, P&L and account reconciliation; order status state machine;
environment isolation and audit; operator permissions and confirmation
requirements.

## §2 — Non-negotiable controls (roadmap verbatim — the design must honor each)
N1. Paper credentials, accounts, routes, identifiers, secrets, and adapters
    are separated from Live.
N2. A paper order cannot reach a live broker adapter by configuration error,
    API substitution, or UI mutation.
N3. Every order carries mode, actor, account, correlation ID, idempotency
    key, risk decision, and audit lineage.
N4. Simulator fills are permanently identified as paper/simulated, never
    broker-confirmed.
Be advised: at this planning horizon NO live execution adapter exists or will
exist (BE-10 is distant); N2 therefore binds the *architecture*: the paper
domain must be structurally incapable of referencing any non-paper execution
route — isolation by type/routing table/sealed registries, not by convention.

## §3 — Precedent law the design must reuse (prior bands, binding patterns)
- BE-1 contracts: safe structured error responses (V2Error envelope), generic
  permission denials without vocabulary leakage, response envelope
  (mode/correlation_id/timestamp), classification/clearance redaction model.
- BE-3 P2: status/lifecycle transition governance (contract_tested in force);
  immutability triggers discipline for append-only artifacts.
- BE-4/5/6: market-context, market-data providers, news — the simulator's
  price/time inputs must come from governed, replayable sources (see Q4).
- BE-7 (research jobs): mutation queue & idempotency patterns, deterministic
  replay semantics with declared time basis, lineage on every artifact,
  RBAC-capability registry style, 'no silent mutation of institutional
  artifacts; retries idempotent and audited'.
- Environment law (new, PGF-021-informed): no behavior conditional on
  filesystem/UI state; environment decisions are config-driven and explicit.

## §4 — Required design sections (every section mandatory; cite where each
roadmap scope bullet and §2 control is satisfied)
S1  Domain & data model: paper account(s), order intent, order lifecycle
    records, fills, positions, balances, margin, P&L snapshots,
    reconciliation records. Table-by-table DDL sketch, immutability triggers,
    seed/compver plan (compver hash additions — RPE law: append-only).
S2  Order intent & lifecycle state machine: states, legal transitions,
    terminal states, timeout/unknown-state policy; state transitions are
    append-only and audited (draft -> validation -> risk decision ->
    simulated execution -> fill/settled; rejected/cancelled/partial).
S3  Pre-trade risk gateway: decision surface (inputs, limits, sources),
    pass/block/hold semantics, risk decision record (immutable, referenced
    by every order per N3), default-deny posture, configuration governance.
S4  Paper execution simulator: fill model (full/partial), price source,
    latency/time model, determinism & replay contract, identification of
    fills as paper/simulated (N4, structural — a fill row CANNOT be read as
    broker-confirmed by any consumer query).
S5  Positions/balances/margin/P&L engine: derivation rules, reconciliation
    cadence, rounding/currency law, tie-in to portfolio surfaces.
S6  Environment isolation architecture: the N2 mechanism (sealed paper-only
    routing registry; mode gating consistent with AXIOM_V2_MODE law;
    secrets separation), plus a documented attack table: every conceivable
    reach-across vector (config error, adapter substitution, UI mutation,
    helper misuse) and its structural countermeasure.
S7  RBAC & confirmations: capability/permission rows for paper trading
    (place/cancel/view/confirm), confirmation requirements where mandated,
    audit events on every privileged action.
S8  Idempotency & concurrency: idempotency-key scheme (BE-7 style),
    duplicate/replay/order-race handling incl. exactly-once risk evaluation;
    concurrent-order determinism.
S9  API surface: versioned V2 routes, request/response contracts (BE-1
    envelope), denial/refusal vocabulary review.
S10 Migration plan: alembic chain position (single new head after
    20260903_0047; recounts), drift-gate cleanliness, downgrade completeness,
    seeds. (Authoring of the migration itself comes only after design
    acceptance + BO — this section is the plan, not the artifact.)
S11 Test plan mapped to exit evidence §5 (each evidence item -> concrete
    test inventory incl. negative tests).
S12 Threat model & security review pre-read: assets, actors, abuse cases
    (esp. N2/N4 violations), mitigations; the ITRGA determination input.
S13 Open questions: each Q1..Q8 in §6 answered with the DA's recommended
    resolution + rationale (roadmap citations prioritized).

## §5 — Exit evidence the design must be able to produce (roadmap)
E1 End-to-end paper lifecycle evidence: draft → validation → risk decision →
   simulated fill → position → account → portfolio → audit.
E2 Duplicate/replay/order-race tests.
E3 Failed-risk, rejected, partial-fill, timeout, unknown-state tests.
E4 Environment-isolation proof (S6 attack table must be test-backed where
   executable).
E5 Security review and ITRGA determination (design must supply the review
   surface; determination is mine after implementation acceptance).

## §6 — Open design questions (DA must answer in S13)
Q1 V1 coexistence: the V1 simulation/paper-ledger surface
   (test_simulated_paper_ledger et al.) — supersede, assimilate, or coexist
   with clear boundary? Recommend with rationale; supersession preferred
   where honest.
Q2 Paper-account cardinality: single shared account per operator vs multiple
   named accounts? State the model and its audit consequences.
Q3 Simulator time/pacing: wall-clock async vs deterministic replay clock
   aligned with BE-7 time_basis law? Deterministic-with-explicit-time-basis
   is favored; justify any deviation.
Q4 Fill price source: attached research/market-data snapshots (BE-4/5/6
   replayable sets) vs live latest ticks? Note the replay determinism
   consequences of the latter.
Q5 Margin model: simplified static margin vs parameterized rule set? Keep
   it explainable; the risk gateway and margin engine must not silently
   compete.
Q6 Unknown-state policy: what, concretely, does the simulator/ledger do on
   crash-mid-fill, duplicate webhook-style events, replay of a settled id?
Q7 Confirmation requirements (roadmap mentions them): which actions need
   human confirmation inside paper (if any) and how is it recorded?
Q8 Boundary to portfolios/analytics: do paper positions mix with V1
   analytics tables, or are they a parallel v2_* domain end-to-end?
   (Parallel-domain default is favored.)

## §7 — Process and gates
1. DA delivers: docs/design/AXIOM-V2-BE-8-DESIGN-001.md (exact ID; version
   1.0.0; every §4 section present; §6 questions each answered; byte-count
   and sha256 declared in your delivery note).
2. ITRGA full-depth review follows; corrections are issued on evidence;
   acceptance precedes any planning of implementation.
3. Only after design acceptance: CN/PLAN/BO for implementation; code and
   migration may be proposed only by BO amendment thereafter. No code now.
4. Register edits: none in this phase beyond any DA-side design-doc entry;
   the live register (AXIOM-V2-STATE-001 v43.0.0) may record the design
   phase as OPENED at the DA's discretion (DA-owned edit).

Standing rules for the DA: cite prior-band precedent where reused (§3);
measure, don't assert; mark every assumption; keep the design honest about
what it chooses NOT to do. We don't guess. We prove.

— ITRGA-REQ-V2-BE-8-001 · v1.1.0 · 2026-09-04
