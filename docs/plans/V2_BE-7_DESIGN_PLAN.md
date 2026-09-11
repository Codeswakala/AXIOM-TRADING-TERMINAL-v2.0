# AXIOM V2 BE-7 — ENGINEERING DESIGN PLAN
## Backtesting, Simulation, Replay, and Governed Research Jobs

| Field | Value |
|---|---|
| Document ID | AXIOM-V2-BE-7-DA-PLAN-001 |
| Version | 1.0.0 |
| Date | 2026-09-03 |
| Author | Development Authority (DA) |
| Review contract | `ITRGA-REQ-V2-BE-7-PLAN-001` (REQ §1.1–§1.13 item-for-item; Pins P-1…P-10) |
| Governing band | `AXIOM-V2-BE-ROADMAP-001` Band BE-7 (REQ §0 verbatim contract — adopted as the plan's contract) |
| Platform baseline | working lineage **`20260903_0046`** (ITRGA-DET-V2-BE-6-CLOSE-001) · triggers **32** · permissions **41** · compver **6** · floor **911** · drift = 9 inherited tokens |
| Status | **SUBMITTED FOR ITRGA PLAN REVIEW** |

**Standing discipline: we don't guess. We prove.** This plan authorizes
nothing and executes nothing.

Reading map: REQ-1.1→Part 1 · 1.2→Part 2 · 1.3→Part 3 · 1.4→Part 4 ·
1.5→Part 5 · 1.6→Part 6 · 1.7→Part 7 · 1.8→Part 8 · 1.9→Part 9 ·
1.10→Part 10 · 1.11→Part 11 · 1.12→Part 12 · 1.13→Part 13 ·
boundaries→Part 14 · limitations→Part 15.

---

## Part 1 — Decomposition and unit structure (REQ-1.1)

### 1.0 V1 surface inventory (Level II — AST-parsed + hashed this session; reused, never rewritten)

| V1 asset | Content | sha256-16 |
|---|---|---|
| `app/ml/dataset/chronology_guard.py` | `ChronologyGuard` — as-of/no-future record gate, `validate_temporal_split`, embargo support | `7dbc665dc4b43f31` |
| `app/ml/dataset/split_engine.py` | `TemporalSplitEngine`, `TemporalSplitConfig` (W2-U04 lineage) | `e893b92c6ccce188` |
| `app/ml/dataset/snapshot_builder.py` | `ReproducibleSnapshotBuilder` | `b08ef4b1dec07567` |
| `app/ml/dataset/service.py` | `DatasetService` (snapshot registration) | `6c5d72a8942050b4` |
| `app/execution_research/simulation.py` | `DeterministicSimulatedFillModel`, `SimulatedExecutionService` | `f163e610ba1a6215` |
| `app/ml/economic/service.py` | `CostInput`/`CostScenario` (cost vocabulary source) | `c49527ed12f4d2ca` |
| V2 BE-2 read model + BE-6 engine | bar series (as-of-bounded reads); metric functions | accepted bands |

**Consumed-vs-built declaration (REQ-1.2 tail):** consumed — the V1
chronology/split/snapshot lineage (W2-U04) as the *leakage-law reference
implementation* and the BE-2 `V2MdBarReadBoundary` as the only bar source;
built new — the replay window assembler, the input registry, the cost-model
registry, the strategy registry, the job queue, and the result artifacts.
No V1 file is modified.

### 1.1 Units

| Unit | Kind | Responsibility | Depends |
|---|---|---|---|
| **U-1** | Migration **0047** (`down_revision="20260903_0046"`; date prefix at issuance) + models | 5 tables + guards + seeds (all DDL in §1.2) | 0046 |
| **U-2** | `app/v2/research_jobs/leakage.py` + `replay.py` | As-of input assembly (structural leakage guards, P-8) + deterministic replay engine | U-1 |
| **U-3** | `app/v2/research_jobs/{registry,costs,strategy}.py` | Input registration, cost-model configuration, strategy lifecycle | U-1 |
| **U-4** | `app/v2/research_jobs/{queue,runner}.py` | Governed job queue + attempt-idempotent runner (P-10) | U-1…U-3 |
| **U-5** | `app/v2/research_jobs/api.py` + router mount | Read surface + governed writers | U-1…U-4 |
| **U-6** | Evidence | DR, transcripts, worked-sample replay annex, register sync | all |

Packaging: single package proposed (one migration); per-unit split remains
the Operator's option.

### 1.2 U-1 — Migration 0047 exact DDL

All PKs uuid4 `TEXT(36)`; BE-1 columns (`mode`, `operator_id`,
`correlation_id` NULL-at-schema/writer-minted per the accepted O-3
posture, `created_at`) on every table; 6-class `data_class` CHECK (same
literal as 0044–0046) on every table.

**T1 `v2_backtest_input`** (versioned-immutable input registry, REQ-1.3):
`input_id String(64)` + `record_seq Integer` + `supersedes String(36) NULL`
(P-1/C-1 vocabulary); `UNIQUE(input_id, record_seq)`
(`uq_v2_btin_id_seq`); `content_hash String(64) NOT NULL` +
`UNIQUE(content_hash)` (`uq_v2_btin_content` — content-addressed dedupe:
re-registering identical content is an idempotent return, not a new row);
`series_refs JSON NOT NULL` (BE-2 tables + instrument/timeframe/source +
as-of consumed); `window_start/window_end DateTime(tz) NOT NULL`;
`registration_outcome String(16) CHECK IN ('registered','reused','refused')`.

**T2 `v2_cost_model`** (REQ-1.4): `cost_model_id String(64)` +
`record_seq` + `supersedes` + `UNIQUE(cost_model_id, record_seq)`
(`uq_v2_cost_id_seq`); `spread/commission/slippage JSON NOT NULL` (value +
unit + citation per parameter); `latency_ms Integer NOT NULL`;
`risk_limits JSON NOT NULL`; `citations JSON NOT NULL` (every constant's
source: V1 `CostInput`/`CostScenario` vocabulary where applicable,
band-declared-with-unit otherwise — **no invented numbers as spec
values**).

**T3 `v2_strategy_version`** (REQ-1.6): `strategy_id String(64)` +
`record_seq` + `supersedes` + `UNIQUE(strategy_id, record_seq)`
(`uq_v2_strat_id_seq`); `name`; `parameters JSON NOT NULL`;
`lifecycle_state String(16) CHECK IN
('draft','registered','retired')` — typed-permanent (state change = new
generation row, never mutation); `no_execution_binding` — **not a column:
a structural absence** — the table carries no credential, adapter, order,
or account field by design (P-9; the CHECK census proves the column set).

**T4 `v2_research_job`** (REQ-1.7): the contract fields exactly — `owner
String(128) NOT NULL`; `authorization_ref String(128) NOT NULL` (the
commissioning citation — a job without one is refused); `inputs JSON NOT
NULL` (input-registry ids + strategy version + cost model version);
`schedule JSON NOT NULL` (`{"kind":"manual"}` v1 scope — §7);
`output_ref String(36) NULL`; `failure JSON NULL` (typed);
`job_state String(16) CHECK IN
('queued','running','succeeded','failed','cancelled')`;
`attempt_count Integer NOT NULL DEFAULT 0`.
**T4b `v2_research_job_attempt`** (append-only attempt ledger):
`job_id` indexed; `attempt_index Integer` + `UNIQUE(job_id, attempt_index)`
(`uq_v2_jobatt_idx` — the idempotency anchor: a retry that would
double-apply collides here and is refused); `outcome String(16) CHECK IN
('succeeded','failed','cancelled')`; `artifact_ref String(36) NULL`;
`reason JSON NOT NULL`; `actor_id`.

**T5 `v2_research_result`** (REQ-1.8/1.9): `result_class String(16)
CHECK IN ('backtest','simulation')` — **the closed constructible set;
`paper`/`live` are absent from the CHECK itself** (schema-impossible, not
just writer-refused; the four-class taxonomy lives in the contracts module
with the two non-constructible classes mapped to typed refusals at every
construction point); `job_id`/`attempt_index` (which attempt produced it);
`strategy_version_id`, `input_registry_id`, `cost_model_id` (lineage
triple); `inputs_hash String(64)`; `engine_versions JSON` +
`engine_versions_hash String(64)`;
`UNIQUE(strategy_version_id, inputs_hash, engine_versions_hash)`
(`uq_v2_result_determinism_anchor`); `summary JSON NOT NULL` (typed
metrics — never presented as live/future performance; a mandatory
`performance_disclaimer` field carries the tier statement); `replay_of
String(36) NULL` (replay artifacts reference their original);
`time_basis JSON NOT NULL`.

**Guard triggers (10; exact messages):**

| Trigger pair (UPDATE/DELETE) on | Messages |
|---|---|
| `v2_backtest_input` | `V2 backtest inputs are immutable; UPDATE prohibited` / `…DELETE prohibited` |
| `v2_cost_model` | `V2 cost models are immutable; UPDATE prohibited` / `…DELETE prohibited` |
| `v2_strategy_version` | `V2 strategy versions are immutable; UPDATE prohibited` / `…DELETE prohibited` |
| `v2_research_job_attempt` | `V2 research job attempts are immutable; UPDATE prohibited` / `…DELETE prohibited` |
| `v2_research_result` | `V2 research results are immutable; UPDATE prohibited` / `…DELETE prohibited` |

(`v2_research_job` is the ONE mutable row set — `job_state`/
`attempt_count`/`output_ref`/`failure` progress via the single governed
runner; every transition mirrored by an immutable attempt-ledger row +
audit event. Flagged as the band's sole mutability decision — **FP-1** for
the review to pin: mutable-job-row-with-immutable-ledger (proposed) vs
fully versioned job rows.)

**Permission seeds (8 rows; revision-local literals):** admin:
`v2.research.jobs.read` SAL-2 · `v2.research.jobs.submit` SAL-3 ·
`v2.research.jobs.cancel` SAL-3 · `v2.research.registry.read` SAL-2 ·
`v2.research.registry.write` SAL-3 · `v2.research.results.read` SAL-2;
operator: `v2.research.jobs.read` · `v2.research.results.read`.
No execution/order/account vocabulary (forbidden-marker guard).

**compver seeds (2; P-4 co-delivery):** `replay_engine = rpe-1.0.0` (over
U-2 files) and `research_job_engine = rje-1.0.0` (over U-4 files), hashed
from disk at migration time; C-2 disclosure: the 0047 application-act
instrument re-pins both engine file sets.

**Data seeds:** none. **Downgrade:** symmetric (5 tables, 10 triggers,
8 permission rows, 2 compver rows via the guard drop/recreate/verify
pattern).

**Post-unit pins (before → after 0047):** triggers **32 → 42** ·
permissions **41 → 49** · compver **6 → 8** · drift = exactly the 9
inherited V1 tokens, zero band tokens · floor from **911** (Part 13).

## Part 2 — Historical replay with as-of boundaries (REQ-1.2)

Replay = deterministic re-execution of a strategy over a registered input
window. The **as-of model**: every replay carries `(window_start,
window_end, as_of)` with `as_of >= window_end` enforced at assembly;
input assembly reads ONLY bars with `open_time <= as_of` AND
`open_time ∈ [window_start, window_end]` through the BE-2 boundary (which
already enforces no-future); the decision loop receives bars strictly in
`open_time` order and at step *t* can observe only bars with
`open_time <= t` (the cursor is the structural cutoff — P-8). Determinism:
replay is a pure function of (input registry content, strategy parameters,
cost model, engine versions) — no wall clock, no randomness (any stochastic
strategy parameter must carry a pinned seed in `parameters`); same inputs ⇒
byte-identical `summary` (anchor-enforced, byte-comparable). Replay
artifacts are `v2_research_result` rows (`replay_of` set), immutable, with
the determinism anchor (REQ-1.9).

## Part 3 — Backtest input/version registration (REQ-1.3)

Registration writer: resolves the requested series through BE-2, computes
`content_hash` (SHA-256 over the canonical serialized bars + window +
series refs), then: identical hash ⇒ typed `reused` outcome returning the
existing row (content-addressed idempotency); same `input_id`, new content
⇒ `record_seq + 1` with `supersedes` (never mutation); invalid window/
series/data-class ⇒ typed `refused` with reasons + durable audit
(the BE-6 C-1 law applied from birth: **every writer refusal in this band
is durably audited via commit-before-raise**). Lineage: `series_refs`
names the BE-2 tables/instruments/timeframes/sources and the as-of used.

## Part 4 — Cost-model configuration (REQ-1.4)

Declared data with citations: each of spread/commission/slippage carries
`{value, unit, citation}`; citations reference the V1
`CostInput`/`CostScenario` field vocabulary (`app/ml/economic/service.py`,
pinned §1.0) where the concept exists there, else
`band-declared: <rationale>` with unit — no invented numbers presented as
spec values. Application is a pure function
`apply_costs(fill_price, side, cost_model) -> effective_price` in the
replay engine; versions immutable; **every result row references its exact
`cost_model_id` generation**.

## Part 5 — Temporal-leakage prevention, structural (REQ-1.5; P-8)

| Guard | Structure (code path named) | Future-leakage test |
|---|---|---|
| G-1 as-of cutoff at assembly | `replay.py::assemble_inputs` — the ONLY bar-fetch path; filters `open_time <= as_of` at the query boundary (BE-2 `read_bars(as_of=…)`) | plant a bar after `as_of` in the fixture DB; assert it is absent from assembled inputs AND the summary is unchanged vs the un-planted run |
| G-2 decision-cursor ordering | `replay.py::run_replay` — the strategy callback receives an immutable window slice ending at the cursor; no API exposes bars beyond it | instrument a probe strategy that records the max `open_time` visible at each step; assert `<= cursor` at every step |
| G-3 label-horizon/embargo rejection | `leakage.py::validate_horizon` — a strategy whose declared label horizon extends past `window_end - embargo` is refused (typed) at job submission | submit with horizon > window_end − embargo; assert typed refusal + durable audit |
| G-4 decision-vs-data timestamp ordering | attempt ledger records `decision_ts = cursor`; validator asserts every recorded decision's data refs have `open_time <= decision_ts` | corrupt a synthetic ledger fixture; assert the validator refuses |
| G-5 registered-input immutability | inputs content-hashed + DB-immutable; replay re-verifies `content_hash` before running (mismatch = typed refusal) | tamper the fixture content post-registration (guard dropped in test setup); assert refusal |

V1 `ChronologyGuard`/`TemporalSplitEngine` are the reference lineage
(consumed for vocabulary and embargo semantics); BE-7's guards are new
code at the named paths — enforced structure, provable by the five tests.

## Part 6 — Strategy-version lifecycle (REQ-1.6)

Versioned-immutable per §1.2 T3; currency = greatest `record_seq`;
`draft → registered → retired` progress by new generation rows (typed-
permanent); a job may reference only a `registered`-state current
generation (submission-time check, typed refusal otherwise). Metadata
carries parameters only — no credential, adapter, or execution binding
exists in the schema (structural absence, P-9).

## Part 7 — Governed research job queue (REQ-1.7)

**Queue technology decision (ARCH row 89): DATABASE-BACKED, in-process
execution.** Justification: RESEARCH-mode constraints forbid external
services and new infrastructure credentials; the queue's truth must live
in the governed, guarded, audited store — a broker would duplicate state
outside governance; job volumes are research-scale. `v2_research_job` is
the queue (state machine `queued → running → succeeded|failed|cancelled`);
the runner is invoked **manually via the governed API in v1 scope**
(`schedule.kind = "manual"` only — a scheduler *tick source* is declared
out of v1 scope and registered as debt; no production scheduler, per
REQ-1.10). Retries: `attempt_index` increments; the attempt ledger's
`UNIQUE(job_id, attempt_index)` plus the result determinism anchor make a
retry **provably idempotent** — a retried attempt either collides on the
anchor (returns the existing artifact; no double-apply) or writes attempt
N+1 with its own ledger row. Cancel: typed transition, refusing when
terminal, always audited with actor + reason. Every transition = audit
event + ledger row (P-10).

## Part 8 — Typed result classes (REQ-1.8; P-9)

Contracts module declares the four-class taxonomy
`('backtest','simulation','paper','live')`; the T5 CHECK admits **only**
`('backtest','simulation')` — `paper`/`live` are schema-impossible, and
every construction point (writer, runner, engine) refuses them with a
typed reason before the DB is even reached. Construction scan test:
no band module constructs, names, or imports any execution/paper/live
result path; the no-live-effect scan (Part 13) covers the API surface.

## Part 9 — Immutable artifacts + determinism anchors (REQ-1.9; P-2/P-4)

Per §1.2 T5: anchor `(strategy_version_id, inputs_hash,
engine_versions_hash)` with idempotent return; `engine_versions` +
canonical-serialization hash (OBS-3 law) on every artifact; compver rows
per §1.2 with C-2 disclosure. Replay artifacts carry `replay_of`;
re-replaying the same triple returns the existing artifact.

## Part 10 — Job-silence control, structural (REQ-1.10)

1. **Writable-table allow-list per writer**: the runner's artifact writer
   may INSERT into exactly `{v2_research_result, v2_research_job_attempt,
   v2_audit_event, v2_lineage_record}` and UPDATE exactly
   `{v2_research_job}` — declared as a module constant and asserted by a
   test that inspects the module's SQL/ORM surface; every other
   institutional artifact table is DB-guard-protected anyway (32 existing
   + 10 new triggers).
2. **No execution-adapter path**: an import/dependency scan test walks the
   band's module graph and asserts no reachable import of execution/
   broker/adapter modules (incl. V1 live adapter modules under
   `app/market/`, `app/api/routes/` execution surfaces) — the same
   construction-scan class as BE-3 P1's forbidden-import test.
3. **Tick source**: none in v1 scope (manual invocation only, §7) — no
   production/infra scheduler; a future scheduler is a separately
   authorized act.

## Part 11 — Mode/audit/security (REQ-1.11)

BE-1 columns everywhere. Audit inventory (`domain="v2.research_jobs"`):
`input.registered/.reused/.refused` · `cost_model.registered/.refused` ·
`strategy.registered/.superseded/.refused` · `job.submitted/.started/
.succeeded/.failed/.cancelled/.retry` · `result.created/.reused` ·
refusal events durably committed (C-1 law from birth). Lineage rows:
results → (input registry id, strategy version, cost model, attempt);
inputs → BE-2 series refs. RBAC per §1.2 seeds with `denied` typed;
redaction gate untouched; **the band prompts for no credential** — stated
here and to be restated in every evidence artifact.

## Part 12 — Data honesty (REQ-1.12)

6-class taxonomy on all five tables; first landing `synthetic`/`simulated`
only, `historical_real`/`live` refused with typed reasons (V2-TD-18
continuity); every evidence outcome declares pipeline-validation tier;
`summary.performance_disclaimer` is mandatory on every result — **no
backtest/simulation result is presented as live or future performance**,
structurally (the field is NOT NULL in the writer contract and asserted
by test).

## Part 13 — Test plan + worked-sample annex (REQ-1.13)

Fail-first per unit. Budget (floor 911 → **≥ 971**):

| Unit | Budget | Groups |
|---|---|---|
| U-1 | 12 | migration-up content (0043/0046 pattern); 10 guard messages verbatim; CHECK probes incl. **result-class CHECK refusing `paper` and `live`**; versioned-uniqueness behavioral ×3; content-hash dedupe; downgrade cycle; drift gate; totals 42/49/8 |
| U-2 | 15 | **the five G-1…G-5 future-leakage tests** (exit item i); deterministic replay ×3 (byte-identical summary; anchor idempotency; seed-pinned stochastic param) — exit item ii; cost-application purity; annex-value tests |
| U-3 | 10 | registration outcomes (registered/reused/refused + durable audits); cost-model citations present; strategy lifecycle (draft/registered/retired generations; only registered-current jobable) |
| U-4 | 15 | queue lifecycle; **retry idempotency** (double-apply collision → existing artifact); duplicate-submit race (content-addressed); cancel semantics (typed; terminal-refusal); failure typed; attempt ledger append-only — exit item iii |
| U-5 | 6 | RBAC incl. denied; result-class + lineage walk (exit item iv); allow-list + import-scan (Part 10) |
| Regression | 2 | full suite green; no-touch across 0047 (BE-2…BE-6 protected state) |
| **Total** | **60** | |

**Worked-sample replay annex (P-7 continuity; exit item ii):** pinned
synthetic series (10 bars, hand-listed), pinned strategy (deterministic
threshold rule, parameters listed), pinned cost model (cited constants),
and the **hand-computed expected outputs to stated precision** (each fill,
each effective price after costs, the final summary metrics) — sufficient
for the ITRGA to replay by hand without executing the engine. The engine's
annex tests assert the same values.

**No-live-effect source/API scan (exit item v) — methodology declared:**
(a) construction-token scan over band modules (no order/execute/broker/
paper/live-construction vocabulary); (b) import-graph walk (Part 10.2);
(c) API surface enumeration test — every band route is GET except the
enumerated governed writers, and no route path or response field contains
execution vocabulary; (d) the forbidden-permission-marker guard (import-
time). All four executed in the suite and echoed in the Level I
transcript.

## Part 14 — Boundaries (REQ closing)

OUT of BE-7: paper-order lifecycle (BE-8…BE-10 — `paper` is a typed
refusal here); live anything; external AI (BE-11); real-data backtests
(corpus track; V2-TD-18); production scheduler/infrastructure (future
authorized act — v1 is manual-invocation); FE surfaces (sequencing
directive); report preview/export (ungranted). The V1 dataset/split/
simulation lineage is consumed read-only.

## Part 15 — Known limitations (honest)

- **FP-1** (§1.2): job-row mutability model — mutable-row-with-immutable-
  ledger (proposed) vs fully versioned job rows; review pins it.
- `schedule.kind = "manual"` only; scheduler tick source deferred (debt).
- Strategy callbacks in v1 scope are registered deterministic rule
  functions (threshold/crossover class over BE-6/BE-4 metric vocabulary),
  not arbitrary user code — sandboxing arbitrary strategies is a future
  band (debt).
- All evidence pipeline-validation tier; no market/performance conclusion
  claimed or claimable (NOT PROVEN until the corpus track).
- 0047 working-DB application = separate sanctioned act (E-0046-DUP
  startup rule inherited by its instrument).

---

*We don't guess. We prove.*
**— Development Authority, 2026-09-03 · End of AXIOM-V2-BE-7-DA-PLAN-001 v1.0.0**
