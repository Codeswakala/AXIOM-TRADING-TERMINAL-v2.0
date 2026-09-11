# AXIOM V2 BE-8 — PAPER TRADING, PAPER ACCOUNT, AND RISK GATEWAY
# DEDICATED PAPER-TRADING AND EXECUTION-SECURITY DESIGN

| Field | Value |
|---|---|
| Document ID | AXIOM-V2-BE-8-DESIGN-001 |
| Version | 1.1.0 (C-1/C-2 amendment per ITRGA-REV-V2-BE-8-DESIGN-001 — change-note §16) |
| Date | 2026-09-04 |
| Author | Replacement Development Authority (DA) |
| Requested by | ITRGA-REQ-V2-BE-8-001 v1.1.0 (via Operator, 2026-09-04) |
| Roadmap contract | `V2_BACKEND_ROADMAP.md` §"Band BE-8 — Paper Trading, Paper Account, and Risk Gateway" |
| Baseline | head `20260903_0047` · suite 972/0 · triggers 42 · permissions 49 · compver 8 · BE-7 OPERATIONAL (ITRGA-CLO-V2-0047-BE7-ACT-001, sealed) |
| Status | DESIGN DOCUMENT ONLY — zero-code rule in force; no code, no migration, no register edits beyond this document |

**Standing discipline: we don't guess. We prove.** Every assumption is
marked `ASSUMPTION`; every reused precedent is cited; every §2 control
(N1–N4) and roadmap scope bullet is mapped where satisfied; §6 questions
Q1–Q8 are each answered in S13 with recommendation + rationale.

---

## §0 — Design thesis (one paragraph)

Paper trading lands as a **parallel, sealed, deterministic v2 domain**
(`app/v2/paper_trading/`, tables `v2_paper_*`), never as an extension of
any research or V1 surface. Isolation is **structural, not conventional**
(REQ §2 advisory): the paper domain has no adapter interface, no secret,
no network path, and no type that any non-paper execution route could
accept — there is nothing to misroute *to* (BE-10 does not exist) and,
by construction, nothing to misroute *with*. Every order is an immutable
intent + an append-only event ledger + a mandatory immutable risk
decision; every fill is schema-locked `paper_simulated`; the simulator is
a deterministic replay consumer of governed market-data snapshots under
the BE-7 time-basis law. Where BE-8 must touch standing law (mode
vocabulary, permission-marker guard), this design says so explicitly and
proposes the narrowest lawful amendment — nothing is smuggled.

---

## S1 — Domain & data model

**Module:** `app/v2/paper_trading/{contracts,accounts,orders,risk,simulator,ledger,reconciliation,api}.py`
+ `app/db/models/v2_paper_trading.py` (PG-002: registered in
`app/db/models/__init__.py` in the same unit).

### S1.1 Tables (DDL sketch; all rows carry the BE-1 structural regime: `mode`, `operator_id`, `correlation_id`, `created_at` — precedent: every band since BE-1)

| # | Table | Nature | Key columns (beyond id + regime) | Uniques / CHECKs |
|---|---|---|---|---|
| 1 | `v2_paper_account` | Versioned-immutable (BE-6 `record_seq`+`supersedes` pattern) | `account_id`, `record_seq`, `supersedes`, `name`, `base_currency` (CHECK closed set, v1: `('USD')`), `initial_balance` (NUMERIC as TEXT-decimal, S5 rounding law), `margin_params` (JSON, citation law), `lifecycle_state` CHECK `('active','frozen','closed')`, `confirmation_ref` NOT NULL | uq `(account_id, record_seq)` |
| 2 | `v2_paper_order_intent` | **Immutable** (write-once, C1 heritage) | `intent_id`, `account_id` FK, `instrument_id`, `side` CHECK `('buy','sell')`, `order_type` CHECK `('market','limit')` (v1 closed set), `quantity`, `limit_price` NULL, `time_in_force` CHECK `('replay_window')` (v1: single value — see S4), `idempotency_key`, `snapshot_ref` (governed price source, S4), `time_basis` (JSON, BE-7 law), `confirmation_ref` (S7), `actor_id` | uq `(account_id, idempotency_key)` — **the N3/S8 anchor**; CHECK `quantity > 0`; CHECK (`order_type='limit'`) = (`limit_price IS NOT NULL`) |
| 3 | `v2_paper_risk_decision` | **Immutable** | `intent_id` FK **UNIQUE**, `decision` CHECK `('pass','block','hold')`, `evaluated_limits` (JSON: every limit + observed value + threshold — measured, not asserted), `reasons` (JSON), `risk_config_version`, `decided_at_basis`, `confirmation_ref` (C-1b: CHECK — NOT NULL **iff** `decision='hold'`, both directions) | uq `(intent_id)` — **exactly-once risk evaluation is a schema fact** (S8) |
| 4 | `v2_paper_order_event` | **Append-only ledger** (BE-7 attempt-ledger pattern, P-10) | `intent_id` FK, `event_index` (monotone), `from_state`, `to_state` (both CHECK against S2 vocabulary), `event_class` CHECK closed set, `details` (JSON), `actor_id` | uq `(intent_id, event_index)` |
| 5 | `v2_paper_fill` | **Immutable** | `fill_id`, `intent_id` FK, `fill_index`, `quantity`, `raw_price`, `effective_price`, `cost_model_ref` (BE-7 citation-law reuse), `fill_class` **CHECK — single-value closed set `('paper_simulated')`** (N4 structural, S4.4), `simulator_version`, `snapshot_ref`, `time_basis` | uq `(intent_id, fill_index)` |
| 6 | `v2_paper_position_snapshot` | Immutable derived artifact | `account_id`, `as_of_basis`, `positions` (JSON), `derivation_inputs_hash`, `engine_versions_hash` | uq determinism anchor `(account_id, derivation_inputs_hash, engine_versions_hash)` (BE-7 anchor law) |
| 7 | `v2_paper_balance_snapshot` | Immutable derived artifact | `account_id`, `as_of_basis`, `cash`, `equity`, `margin_used`, `margin_available`, `unrealized_pnl`, `realized_pnl`, same anchor columns | same anchor uq |
| 8 | `v2_paper_reconciliation` | **Immutable** | `account_id`, `run_basis`, `outcome` CHECK `('consistent','discrepant')`, `discrepancies` (JSON; empty iff consistent), `inputs_hash` | — |

Roadmap scope bullets satisfied: *paper account model* → T1;
*order intent & immutable order lifecycle* → T2+T4; *pre-trade risk
gateway* → T3 (+S3); *simulated fills/positions/balances/margin/P&L/
reconciliation* → T5–T8 (+S5); *order status state machine* → T4+S2.

### S1.2 Immutability triggers (BE-3 P2 / BE-7 discipline)

UPDATE+DELETE guard pairs on **all 8 tables** (accounts included:
supersession is INSERT-new-record_seq, so the base rows are guarded
too) = **16 triggers**, census 42 → **58**. Message pattern per
household law: `V2 paper order intents are immutable; UPDATE prohibited`
etc., sqlite dialect of record verbatim-tested, postgresql
parametrized-generic (OBS-C carried). The only mutable state in the
whole domain is: **none — zero UPDATE anywhere.** Order state lives in
the append-only event ledger; "current state" is derived (S2.3). This
is stricter than BE-7 (which had one mutable table) and is deliberate:
an order-lifecycle domain warrants it.

### S1.3 Seeds & compver (append-only law)

- compver 8 → **10**: `paper_execution_simulator = pxs-1.0.0` (files
  `{simulator,ledger}.py`), `paper_risk_gateway = prg-1.0.0` (files
  `{risk,contracts}.py`) — rolling-hash recipe identical to 0047
  (`ref‖0x00‖bytes‖0x00`), hashed from disk at apply time,
  `evidence_ref` = the future BE-8 BO id. RPE/RJE untouched (append-only
  RPE law honored).
- Permission seeds: S7 (49 → **57**, +8).
- No data seeds: accounts are created by governed operator action only,
  never migration-seeded (an account is an auditable act, not a fixture).

---

## S2 — Order intent & lifecycle state machine

### S2.1 States (closed vocabulary)

`draft → validated → risk_passed | risk_blocked | risk_hold →
executing → filled | partially_filled → settled`
plus terminals/branches: `rejected` (validation), `cancelled`
(operator, pre-execution only), `expired` (timeout law S2.4),
`quarantined_unknown` (S2.5 / Q6).

**Terminal states:** `settled`, `rejected`, `risk_blocked`, `cancelled`,
`expired`, `quarantined_unknown`. `risk_hold` is non-terminal and
resolves **only by operator confirm/cancel** (a recorded, audited event)
— never by silent re-evaluation, which the S3/S8 exactly-once law
(uq on the decision row) makes structurally impossible anyway.

### S2.2 Legal transitions (complete table; anything absent is a typed refusal)

| From | To | Trigger |
|---|---|---|
| draft | validated / rejected | validation writer (schema+instrument+account checks) |
| validated | risk_passed / risk_blocked / risk_hold | risk gateway (S3), exactly once |
| risk_hold | risk_passed / cancelled | operator confirmation / cancellation (C-1 mechanism, S2.6; audited) |
| risk_passed | executing | simulator invocation (governed writer; precondition = the S2.6 derived rule) |
| executing | filled / partially_filled / expired / quarantined_unknown | simulator outcome (deterministic; S4) |
| partially_filled | settled | settlement writer (remaining qty explicitly voided, recorded) |
| filled | settled | settlement writer |
| draft/validated | cancelled | operator cancel (pre-risk or pre-execution only) |

Every transition = one `v2_paper_order_event` row + one audit event
(BE-7 "ledger + audit mirrored" law) + lineage record. Cancel after
`executing` is a **typed refusal** (BE-7 terminal-cancel precedent).

### S2.3 Current state = derivation law

Current state is the `to_state` of the max `event_index` — a query, not
a mutable column. No UPDATE target exists; the race class "state column
vs ledger disagree" is structurally impossible. (PGF-012 content-based
spirit applied to runtime.)

### S2.4 Timeout policy

v1 scope is deterministic-replay execution (Q3): the simulator runs
synchronously inside a governed invocation, so wall-clock timeout means
*invocation death*, handled by S2.5. `expired` exists for the declared
replay-window law: an intent whose snapshot window cannot satisfy the
order within the replayed bars terminates `expired` (typed, evented,
audited) — never silently open.

### S2.5 Unknown-state policy (Q6, concrete)

Crash-mid-fill: the event ledger shows `executing` without a terminal;
on next governed invocation the runner finds the completed-fill anchor
(fills are written before the terminal event, idempotent by
`(intent_id, fill_index)`): if fills complete → append terminal event
(convergence, audited `order.recovered`); if not reproducible → append
`quarantined_unknown` terminal + audit; the account excludes quarantined
intents from balance derivation and reconciliation flags them
(E-0046-DUP spirit: a marker means STOP-and-rule, never delete).
Duplicate webhook-style events: no webhooks exist in v1 (no network);
duplicate *invocations* dedupe on the idempotency anchor with audit
`order.reused` (BE-7 `result.reused` precedent). Replay of a settled id:
typed refusal + audit (completed-run-marker law).

---

### S2.6 The hold/confirmation seam — full mechanism (C-1 specification, ITRGA-REV-V2-BE-8-DESIGN-001 §3)

**Governing fact restated:** `v2_paper_risk_decision` is immutable with
uq(intent_id) — exactly one decision row per intent, ever. A confirmed
hold therefore writes **no second decision row**; resolution lives
entirely in the append-only event ledger. Everything below is derivable
from ledger + decision row; **no mutable marker exists anywhere.**

**(C-1a) The executing-writer full precondition — single derived rule,
stated once, owned by one function (`may_execute(intent) -> bool`),
consumed by the transition writer and by tests; no duplicated logic:**

> An intent may transition to `executing` iff its (unique) risk decision
> row satisfies: `decision = 'pass'`, **OR** (`decision = 'hold'` **AND**
> the event ledger contains a `hold.confirmed` event whose
> `details.confirmation_ref` equals the single `confirmation_ref` minted
> by that decision's `hold.issued` event **AND** no `hold.cancelled`
> event exists for the intent). In all other cases (`block`, unresolved
> `hold`, cancelled `hold`, no decision row) the transition is a typed
> refusal.

`risk_hold → risk_passed` in S2.2 is thus a **ledger event**
(`hold.confirmed` + state event `risk_hold → risk_passed`), not a
decision mutation: the decision row stays `hold` forever; the *effective*
pass is the derived rule's output. Current-state derivation (S2.3) is
unchanged — the max-event_index state is `risk_passed` after
confirmation.

**(C-1b) Confirmation-ref lifecycle (creation → storage → consumption →
refusals):**

1. **Creation:** when the gateway issues `hold`, the same governed act
   appends the `hold.issued` event carrying a freshly minted
   `confirmation_ref` (a `v2_identifiers`-style opaque id) in
   `details`, and the ref is stored on the intent's decision row column
   `confirmation_ref` (NOT NULL iff `decision='hold'`; NULL for
   pass/block — CHECK enforces the iff both directions). One ref per
   hold, minted exactly once, immutable with the row.
2. **Storage law (NOT NULL columns):** `v2_paper_risk_decision.
   confirmation_ref` as above; on the confirm act nothing is written to
   any mutable column anywhere — consumption is a ledger fact.
3. **"Consumed" — structural definition (ledger-derived, preferred form
   per the review):** a ref is *consumed* iff a `hold.confirmed` or
   `hold.cancelled` event citing it exists in the ledger. Because the
   ledger is append-only with uq `(intent_id, event_index)` and the
   confirm writer refuses when a consuming event already exists, a ref
   can be consumed at most once — single-use is a derivation over
   immutable rows, not a flag.
4. **Typed refusals (each + durable audit, C-1 commit-before-return
   law):** **double-confirm** — a consuming event exists → refusal
   `paper.confirmation.already_consumed`; **wrong-ref** — supplied ref ≠
   the decision row's `confirmation_ref` → `paper.confirmation.
   ref_mismatch` (generic message on the wire, exact class in audit);
   **stale-ref after cancel** — `hold.cancelled` exists → `paper.
   confirmation.cancelled`; **confirm on non-hold** — decision is
   pass/block or absent → `paper.confirmation.not_confirmable`.

**(C-1c) Exact event + audit rows per act (closed class names):**

| Act | Ledger event(s) (`event_class`, from→to) | Audit event(s) |
|---|---|---|
| Gateway issues hold | `hold.issued` (validated → risk_hold; details: confirmation_ref, banded limits) | `paper.risk.hold_issued` |
| Operator confirms hold | `hold.confirmed` (risk_hold → risk_passed; details: confirmation_ref, confirming actor) | `paper.order.hold_confirmed` |
| Operator cancels hold | `hold.cancelled` (risk_hold → cancelled; details: confirmation_ref, cancelling actor) | `paper.order.hold_cancelled` |
| Refused confirmation (all four C-1b.4 classes) | **no state event** (ledger unchanged) | `paper.order.confirm_refused` (refusal class + reasons in details; durable) |

**(C-1d) `risk_block` unreachable by confirmation — typed terminal, no
path:** `block` decisions mint **no** `confirmation_ref` (NULL by CHECK);
the confirm writer's precondition requires `decision='hold'`, so any
confirm attempt against a blocked intent is the `not_confirmable` typed
refusal; no ledger event class exists whose from-state is `risk_blocked`
(S2.2 table is exhaustive — absence is refusal). Tests assert **both
arms**: (arm 1) confirm on blocked intent → typed refusal + durable
audit + ledger unchanged; (arm 2) no legal-transition row from
`risk_blocked` exists in the vocabulary constant (content assertion),
and a forged `risk_blocked → executing` event append is refused typed.

This closes the E3 hold→confirm / hold→cancel test-authoring gap: every
test's expected rows are enumerated above deterministically.

## S3 — Pre-trade risk gateway

**Default-deny** (REQ S3): an intent with no `v2_paper_risk_decision`
row cannot reach `executing` — enforced by the transition writer
(refuses without a `pass` decision row) AND testable at the DB (the
decision row's uq(intent_id) FK is required by the executing-event
writer). Decision surface inputs, all measured and recorded in
`evaluated_limits` (value + threshold + verdict per limit):

| Limit | Source | v1 default (ASSUMPTION — Operator-configurable at BO) |
|---|---|---|
| max order quantity | risk config | 10,000 units |
| max order notional | qty × snapshot ref price | 100,000 base-currency units |
| instrument allow-list | governed instrument registry (BE-2/BE-3 lineage) | seeded instruments only |
| sufficient margin | S5 engine (advisory input; gateway decides — Q5) | margin_available ≥ required |
| position concentration | current derived positions | ≤ 25% equity per instrument |
| account lifecycle | account record | `active` only |
| rate limit | intents per account per window | 100 per replay session |

**Decision semantics (C-2 exact wording, ITRGA-REV §4):** decision rows
are immutable and written exactly once per intent; `block` is terminal
with no confirmation path (C-1d — no ref minted, no event class exists);
`hold` resolves only through the S2.6/S7.2 confirmation mechanism;
`pass` is the only decision that can reach `executing` — directly, or
effectively via the C-1a derived rule for a confirmed hold. `hold` is
issued when a limit is in its declared confirmation band (S7) — e.g.
notional within [80%, 100%] of max. Risk config is a versioned governed artifact (`risk_config_version`
recorded on every decision; config changes are audited writer acts, not
env vars — PGF-021 environment law). The decision row is immutable and
referenced by every order (N3 ✔: mode/actor/account/correlation/
idempotency-key live on the intent; risk decision + audit lineage by FK
and event ledger).

---

## S4 — Paper execution simulator

### S4.1 Price source (Q4)

**Governed replayable snapshots only** — the intent pins `snapshot_ref`
(content-hashed market-data set from the BE-2/BE-7 governed lineage) and
`time_basis` (BE-7 law: explicit window + as-of). G-5-style content
re-verification before execution (hash mismatch = typed refusal, never
silent). No live ticks (Q4 rationale: live is corpus-gated V2-TD-18;
determinism dies with latest-tick reads; replay evidence E2 requires
byte-stable inputs).

### S4.2 Fill model

Deterministic single-pass over the snapshot bars within the window:
market orders fill at first bar close after the declared decision
cursor; limit orders fill when the limit price is touched (bar
low ≤ limit ≤ bar high law, side-adjusted); **partial fills** when
declared bar liquidity (a snapshot-carried, citation-law parameter —
never invented) is below remaining quantity; costs via the BE-7
cost-model citation law (spread/commission/slippage `{value, unit ∈
('price','fraction'), citation}` — CR-V2-BE-7-001 vocabulary reuse,
same `apply_costs` semantics, worked-sample annex mandatory in the DR
per BE-6/BE-7 P-7 precedent).

### S4.3 Determinism & replay contract

`(intent bytes + snapshot content hash + cost model + simulator
version)` → identical fills, byte-identical derived snapshots, ×3
attestation (BO T-9 ×3 law, learned in CR-V2-BE-7-001 F-2 — designed-in
this time). Engine versions hashed into compver (S1.3);
`engine_versions_hash` on every derived artifact.

### S4.4 N4 — structural, not conventional

`v2_paper_fill.fill_class` CHECK admits **exactly one value:**
`'paper_simulated'`. There is no `broker_confirmed`, no `venue`, no
`external_ref`, no status column a consumer could read as broker
provenance — the schema cannot express the concept. (Same mechanism
that made paper/live schema-impossible in BE-7's result table — the
strongest control we have shipped, reused.) API responses embed the
BE-7-style unconditional disclaimer: fills/P&L are paper-simulated,
never broker-confirmed, no live or future performance claim.

---

## S5 — Positions / balances / margin / P&L engine

- **Derivation rules:** positions = signed sum of fills per instrument;
  cash = initial − Σ(buy effective) + Σ(sell effective); equity = cash +
  Σ(position × mark) where mark = last bar close **of the pinned
  snapshot** (never a live read); unrealized P&L from marks, realized
  P&L on closing fills (average-cost method, v1 — ASSUMPTION, closed
  alternatives list: FIFO deferred as debt).
- **Rounding/currency law:** all money as `Decimal` over TEXT-decimal
  columns (BE-7 replay precedent — no float anywhere); round half-even
  at 2 decimals only at presentation; single base currency `USD` v1
  (multi-currency = registered debt).
- **Margin (Q5):** simplified static parameterized rule set —
  `margin_used = Σ |position notional| × margin_rate` with rates from
  the account's `margin_params` (citation law). The margin engine
  **computes; only the risk gateway decides** — one decision authority,
  no silent competition (Q5 requirement honored by interface: margin
  engine exposes pure functions consumed by S3).
- **Reconciliation cadence:** on every settlement + on demand
  (governed read-writer): recompute positions/balances from the full
  fill ledger from genesis, compare to latest snapshots
  (**content-based comparison, PGF-012**), write `v2_paper_reconciliation`
  row; `discrepant` outcome is a first-class alarm surface (audit +
  typed API state), never auto-corrected.
- **Portfolio tie-in (Q8):** none in v1 — parallel domain end-to-end;
  read-only projection into portfolio-research surfaces is a future
  separately-authorized act.

---

## S6 — Environment isolation architecture (N1/N2 — the mechanism)

### S6.1 The sealed routing registry

`app/v2/paper_trading/contracts.py` declares:

- `EXECUTION_BACKENDS: Final = MappingProxyType({"paper": "v2.paper_trading.simulator"})`
  — an immutable single-entry registry. There is **no registration
  function**, no plugin path, no entry-point scan, no config file that
  can add a key. Adding a backend requires editing this literal — a
  source change caught by the source-transcript hash manifest and the
  import scan.
- Order flow is **typed end-to-end**: the simulator's entry accepts only
  `PaperOrderIntent` (a frozen dataclass constructed exclusively by the
  intent writer after risk pass); no dict-shaped order can cross the
  seam.
- **No adapter interface exists.** The design deliberately does NOT
  create an `ExecutionAdapter` ABC "for later" — an abstraction with one
  paper implementation is precisely the substitution surface N2 forbids.
  BE-10 will design its own gateway under its own law.

### S6.2 Mode law

`VALID_MODES` extends to `("RESEARCH","SIMULATION","PAPER")` —
**a standing-law amendment this design declares openly** (current
`app/v2/mode/contract.py` defers PAPER to BE-8; this is that act).
Paper writers require `mode == "PAPER"` explicitly; `LIVE` remains
deferred/refused. Config-driven and explicit (PGF-021 environment law:
no filesystem/UI-state conditionals anywhere in the domain — the CB-001
lesson, now statute).

### S6.3 Secrets separation (N1)

The paper domain requires **zero credentials** — structural absence is
the separation. The import scan bans secret-manager/credential modules
inside `v2/paper_trading/`; no env var read except the mode gate.

### S6.4 Attack table (every conceivable reach-across vector)

| # | Vector | Structural countermeasure | Test-backed (E4) |
|---|---|---|---|
| 1 | Config error points paper at a live route | No route configuration exists; registry is a frozen literal with one key | scan + registry census test |
| 2 | API substitution (swap adapter impl) | No adapter interface; simulator imported by literal module path; compver hash pins engine bytes | compver pin + import-scan test |
| 3 | UI mutation posts to a live endpoint | No live endpoint exists in the codebase (BE-10 distant); paper routes namespaced `/api/v1/v2/paper/*`; C3 law: no generic update endpoint | API-surface census test |
| 4 | Helper misuse (calling simulator with forged fill class) | `fill_class` single-value CHECK; fills written only by the simulator writer; triggers forbid UPDATE | schema refusal test (raw INSERT of any other class) |
| 5 | Import of broker/execution code into the paper domain | Import-scan with the BE-7 extended token predicate (`execution`,`broker`,`order`-adapters,`adapter`,`trading_intelligence`,`app.market`,`live_service`) over `v2/paper_trading/`; sole named exception rule re-declared | scan test (executed) |
| 6 | Permission-vocabulary leak grants live-sounding capability | S7 marker-law amendment is namespace-scoped; forbidden markers still reject everything outside `v2.paper.` | vocabulary guard test |
| 7 | Mode confusion (paper writer in RESEARCH mode) | Explicit mode gate typed refusal on every writer | negative mode test |
| 8 | Event-ledger forgery advances state without risk decision | Executing-transition writer enforces the single S2.6/C-1a derived rule (`pass`, or confirmed `hold` per ledger derivation); ledger append-only; uq(intent_id) on decisions; `block` structurally confirmation-proof (C-1d) | transition refusal test + C-1d both-arms tests |
| 9 | Future band silently widens the fill-class CHECK | Generational drift-gate + migration test asserts the CHECK's literal single-value set | migration test |
| 10 | Filesystem-conditional behavior (CB-001 class) | PGF-021: no `Path.exists()`-style branching in the domain; statute-screened at review | source scan |

---

## S7 — RBAC & confirmations

### S7.1 Permissions (8 new; namespace `v2.paper.*`)

| Permission | Roles | SAL |
|---|---|---|
| `v2.paper.accounts.read` | admin, operator | SAL-2 |
| `v2.paper.accounts.manage` (create/freeze/close, confirmation-gated) | admin | SAL-3 |
| `v2.paper.orders.read` | admin, operator | SAL-2 |
| `v2.paper.orders.place` | admin | SAL-3 |
| `v2.paper.orders.cancel` | admin | SAL-3 |
| `v2.paper.orders.confirm` (hold-resolution + threshold confirmations) | admin | SAL-3 |
| `v2.paper.fills.read` | admin, operator | SAL-2 |
| `v2.paper.risk.read` | admin, operator | SAL-2 |

**Marker-law collision, declared honestly:** the tokens `account`,
`order`, `margin`, `position` sit in `V2_FORBIDDEN_PERMISSION_MARKERS`
(BE-1 law) and would reject these rows at import. Proposed narrowest
amendment: the guard exempts **exactly** permissions with prefix
`v2.paper.` while continuing to reject the markers everywhere else;
the exemption itself is test-asserted (a `v2.research.order.x` must
still die). This amendment requires explicit ITRGA approval in the
review of this design — flagged as **DECISION-1**.

### S7.2 Confirmation requirements (Q7)

Human confirmation (a second, explicit, audited API act by a
confirm-capable actor) is mandatory for: (a) account create/freeze/
close; (b) `risk_hold` resolution; (c) any order whose notional exceeds
the declared confirmation band (S3). Mechanism — **the S2.6/C-1
machinery is the single mechanism for all three surfaces**: the primary
act returns `pending_confirmation` with a single-use `confirmation_ref`
(creation, storage, ledger-derived consumption, and the four typed
refusal classes exactly per C-1b); the confirm act cites it; both acts
are audit events (C-1c class names for orders; the account-lifecycle
twins `paper.account.confirm_*` for accounts); the ref lands on the
decision/account row (NOT NULL where mandated, iff-CHECKed on the
decision row). No self-confirmation:
`confirmed_by != initiated_by` when more than one eligible actor exists
(v1 single-operator reality: recorded as a documented limitation, not
silently waived — ASSUMPTION the Operator remains sole human).

---

## S8 — Idempotency & concurrency

- **Idempotency key:** client-supplied, uq `(account_id,
  idempotency_key)` (BE-7 style). Duplicate submission → the existing
  intent is returned, `order.reused` audited, no second risk evaluation,
  no state advance (E2 evidence).
- **Exactly-once risk evaluation:** uq `(intent_id)` on
  `v2_paper_risk_decision` — a second evaluation attempt is a
  constraint-refused write surfaced as a typed refusal + audit. Not a
  convention; a schema fact.
- **Order races:** SQLite single-writer serializes (BE-7 T-10
  precedent); the design-level answer is the anchor set: duplicate
  intents converge on one row; duplicate invocations converge on one
  fill set (uq `(intent_id, fill_index)`); the event ledger's uq
  `(intent_id, event_index)` makes double-append a refusal. Concurrent
  distinct intents are lawful and independent.
- **Deterministic outcome under retry:** S4.3 replay contract — a
  re-run after crash converges byte-identically or quarantines (S2.5),
  never diverges silently.

---

## S9 — API surface

Namespace `/api/v1/v2/paper/*`, mounted in `v2/api/router.py`. BE-1
envelope on every response (`mode`/`correlation_id`/`timestamp`);
V2Error safe structured refusals; generic `"Permission denied"` (no
vocabulary leakage); 401/403 negative tests mandatory.

**Governed writers (POST only — C3 law, zero PUT/PATCH/DELETE):**
`/accounts` (create, confirmation flow), `/accounts/confirm`,
`/orders` (intent), `/orders/confirm`, `/orders/cancel`,
`/orders/{id}/run` (governed simulator invocation, manual — Q3/BE-7
C4 precedent: no tick source). Reads: `/accounts`, `/orders`,
`/orders/{id}/events`, `/fills`, `/positions`, `/balances`,
`/risk-decisions`, `/reconciliations`. Exact census asserted by an
API-surface test (BE-7 T-8/INT-8 precedent).

Refusal vocabulary review: all refusals typed
(`paper.violation` family + reuse of `temporal.violation`,
`permission.denied`); no refusal message names live/broker concepts
(they don't exist to name).

---

## S10 — Migration plan (plan only; authoring gated on design acceptance + BO)

- **Chain:** `20260904_0048_v2_be8_paper_trading.py`, `down_revision =
  "20260903_0047"`, single head after apply.
- **Recounts:** triggers 42 → **58** (+16: 8 tables × UPDATE/DELETE);
  permissions 49 → **57** (+8, S7 seeds, DEL-004 revision-local
  literals, existing-set filter — no deleted-reinsertion); compver
  8 → **10** (+2, S1.3, apply-time disk hashing).
- **Drift gate:** PGF-014 format-independent both-heads discipline;
  the acceptable drift remains exactly the 9 inherited V1 tokens; zero
  BE-8 tokens. Generational scoping applied to 0047's drift test when
  0048 becomes head (established law).
- **Downgrade:** symmetric content-based teardown (0047 pattern):
  permission tokens by exact bind, compver rows scoped
  component+version, guard-triggered drop order, tables reverse-
  dependency. `test_0048_downgrade_cycle` + no-touch test (provider
  rows, prior compver, trigger delta exactly the 16 names).
- **Working-DB application:** separate sanctioned act at chain end,
  per the 0043/0045/0046/0047 lineage — E-0046-DUP startup law,
  pre-declared compver expectations, PGF-020…024 statute screening
  (new battery), ASCII console law.

---

## S11 — Test plan mapped to exit evidence (§5)

Projected budget ~70 new tests, 4 modules (final counts fixed at BO;
BE-7 lesson: module split disclosed up front). **Fail-first with a
shipped failing-run transcript** (OBS-E commitment, now designed-in).

| Exit item | Test inventory (concrete) |
|---|---|
| **E1** end-to-end lifecycle | Level-I API transcript: account create+confirm → intent → validation → risk pass (decision row content asserted) → run → fills (class + costs vs a hand-computed ANNEX-P worked sample, P-7 law) → position/balance snapshots (anchor asserted) → reconciliation `consistent` → audit inventory printed; + the same as an executed test |
| **E2** duplicate/replay/race | idempotency-key reuse (same intent, `order.reused` audit, one risk row); double-run convergence (same fills, ×3 byte-identical); settled-id replay typed refusal; event-append race → uq refusal typed |
| **E3** failure taxonomy | risk `block` (limit named + measured in reasons); validation `rejected`; partial fill → settled with voided remainder recorded; `expired` window exhaustion; crash-mid-fill quarantine + recovery convergence (S2.5 both arms); `hold` → confirm and `hold` → cancel with row-exact expectations from the S2.6/C-1c table; the four confirmation refusal classes (double-confirm, wrong-ref, stale-after-cancel, not-confirmable) each typed + durably audited; C-1d both arms (block unreachable by confirmation; forged `risk_blocked → executing` append refused) |
| **E4** isolation proof | every S6.4 row's test column executed: import scan, registry census, API census, fill-class schema refusal (raw INSERT), mode-gate refusals, marker-law scoped-exemption both arms, PGF-021 source scan |
| **E5** security review surface | S12 threat model + the S6.4 table + scans = the review input; migration tests: DDL/CHECK literals, censuses 58/57/10, guards verbatim ×16, downgrade, no-touch, drift ×2 |
| Regression | full suite ≥ 972 + budget, 0 failed; V1 pins re-hash (six BE-7 pins + `test_simulated_paper_ledger` surface untouched per Q1); prior-band contract vocabulary regression |

---

## S12 — Threat model & security review pre-read

- **Assets:** account integrity (balances not forgeable), order/fill
  provenance (never readable as broker-confirmed), risk-decision
  integrity (no bypass), audit completeness, mode boundary.
- **Actors:** operator (trusted, confirmable), admin (trusted),
  future code (the real adversary — guarded by schema CHECKs, frozen
  registry, scans, statutes), compromised UI client (bounded: RBAC +
  confirmations + no live surface to reach).
- **Abuse cases:** the S6.4 table rows 1–10 (each with countermeasure +
  test); plus: P&L misrepresentation (disclaimer + fill_class + no
  realized-language on simulated artifacts — V1 W6 precedent);
  risk-config tampering (versioned governed artifact, decisions pin the
  version); audit suppression (C-1 commit-before-raise durable-refusal
  law on every refused writer).
- **Explicitly out of scope (honest):** live execution (BE-10), broker
  reads (BE-9), multi-user confirmation segregation (single-operator
  reality documented), network hardening (no network in the domain).
- **Residual risks for the determination:** DECISION-1 (marker-law
  amendment) and the mode-law extension are the two standing-law edits;
  both are narrow, both are test-asserted, both need explicit ITRGA
  sanction.

---

## S13 — Open questions Q1–Q8 (recommendation + rationale)

| Q | Recommendation | Rationale |
|---|---|---|
| **Q1** V1 coexistence | **Supersede-with-frozen-boundary.** The V1 simulated/paper-ledger surface (`test_simulated_paper_ledger` et al., `execution_research` lineage) stays byte-frozen read-only V1 lineage — exactly the BE-7 treatment of `execution_research` (named exception, pins re-hashed in suite). The v2 paper domain is the sole authoritative paper surface. No assimilation (dishonest: V1 ledger lacks risk gateway, account model, N-controls); no V1 writes ever. | Supersession preferred where honest (REQ Q1); BE-7 named-exception precedent works and is already statute-screened |
| **Q2** Account cardinality | **Schema supports multiple named accounts; v1 operation grants one per operator** (creation confirmation-gated, admin-only). | Multi-account audit semantics (who/which/why) come free from the BE-1 regime + account_id on every row; restricting v1 operation keeps the reconciliation surface small while not baking a false uniqueness into DDL |
| **Q3** Time/pacing | **Deterministic replay clock, explicit `time_basis`, manual governed invocation** (BE-7 C4 twin: no tick source, no wall-clock async). Wall-clock exists only as audit metadata. | Favored by the REQ; E2 determinism evidence is impossible under wall-clock async; scheduler remains registered debt (V2-TD-24 family) |
| **Q4** Fill price source | **Governed replayable snapshots pinned per intent** (content-hashed, G-5-style re-verification). No live/latest ticks. | Live ticks destroy replay determinism and violate the corpus gate (V2-TD-18); the REQ itself notes the consequence |
| **Q5** Margin model | **Simplified static parameterized rules** (`margin_params` with citations); margin engine computes, **risk gateway solely decides**. | Explainability mandate; single decision authority prevents the silent competition the REQ warns of; parameterization leaves room without new law |
| **Q6** Unknown-state | S2.5 verbatim: ledger-anchored convergence or `quarantined_unknown` terminal + reconciliation flag; duplicate events dedupe on anchors with `*.reused` audits; settled-id replay = typed refusal. | E-0046-DUP marker law + BE-7 P-10 idempotent-retry pattern, both battle-tested |
| **Q7** Confirmations | S7.2: account lifecycle acts, `risk_hold` resolution, above-band notionals — two-act confirmation with single-use `confirmation_ref`, both acts audited, ref stored NOT NULL where mandated. | Roadmap mandates confirmation requirements; the two-act pattern gives Level-I evidence of the human in the loop |
| **Q8** Portfolio boundary | **Parallel `v2_paper_*` domain end-to-end.** No mixing with V1 analytics tables; no BE-6 portfolio-research writes. Read-only projection = future separately-authorized act (registered as design debt). | Favored default in the REQ; mixing would launder simulated P&L into research surfaces and break the result-class wall BE-7 built |

---

## §14 — What this design chooses NOT to do (honesty register)

1. No live/broker anything (BE-9/BE-10) — no adapter interface even as
   an abstraction (S6.1 rationale).
2. No scheduler/tick source (manual invocation; debt family V2-TD-24).
3. No multi-currency, no FIFO lot accounting (average-cost v1; debt).
4. No webhooks/streaming (no network in the domain).
5. No paper→portfolio projection (Q8; future act).
6. No migration/code in this phase (zero-code rule honored: this
   document is the entire deliverable).

## §15 — Assumptions register

A-1 (S3) v1 risk limits are DA-proposed defaults; Operator sets real
values at BO. A-2 (S7.2) single-operator reality: confirmation
segregation documented, not enforceable. A-3 (S5) average-cost realized
P&L acceptable for v1. A-4 (S1) USD single currency v1. A-5 (S11) ~70
test budget refined at BO. Each assumption is a review surface, not a
decision.

## §16 — Change-note v1.0.0 → v1.1.0 (ONLY these edits; per ITRGA-REV-V2-BE-8-DESIGN-001 §8)

1. **C-1 (§3 of the review) — new section S2.6** specifying the
   hold/confirmation seam in full: (a) the executing-writer precondition
   as a single derived rule (`may_execute`), decision-row + ledger based,
   owned once; (b) confirmation-ref lifecycle — creation at `hold.issued`,
   storage on the decision row (`confirmation_ref` NOT-NULL-iff-hold
   CHECK), consumption as a ledger-derived fact (no mutable marker), and
   the four typed refusal classes (double-confirm / wrong-ref /
   stale-after-cancel / not-confirmable), each durably audited; (c) the
   exact ledger-event + audit-event class table for hold-issued /
   confirmed / cancelled / refused acts; (d) `risk_block`
   confirmation-proof structurally (no ref minted by CHECK; no event
   class from `risk_blocked`; both-arms tests named).
   Consequential cross-reference edits: S1.1 row 3 (decision-row DDL
   gains the iff-CHECKed `confirmation_ref` column), S2.2 (two rows now
   cite S2.6), S6.4 row 8 (countermeasure cites the derived rule + C-1d),
   S7.2 (single-mechanism statement; account-lifecycle audit twins
   named), S11 E3 (row-exact test expectations + the four refusal
   classes + C-1d arms).
2. **C-2 (§4 of the review) — S3 wording replaced** with the exact
   mandated paragraph: decisions immutable and exactly-once; `block`
   terminal with no confirmation path; `hold` resolves only via
   S2.6/S7.2; `pass` the only decision reaching `executing` (directly or
   via the C-1a derived rule).
3. Version/header bump and this change-note. **No other section
   altered.** D-1/D-2 rulings (approved-scoped / approved) require no
   text change: the design already carried the narrowest-scope proposals
   the rulings sanction; their binding conditions (single literal prefix
   test; both-arms + boundary `v2.paperwork.*` negative; contract-comment
   + register line at BO) are noted for the BO phase.

**We don't guess. We prove.**

**End of AXIOM-V2-BE-8-DESIGN-001 v1.1.0**
