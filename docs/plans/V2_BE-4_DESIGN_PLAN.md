# AXIOM V2 BE-4 — ENGINEERING DESIGN PLAN
## Market Context, Chart Intelligence, and Research Read Models

| Field | Value |
|---|---|
| Document ID | AXIOM-V2-BE-4-DA-PLAN-001 |
| Version | 1.0.0 |
| Date | 2026-08-31 |
| Author | Development Authority (DA) |
| Source request | `ITRGA-REQ-V2-BE-4-001` (per `AXIOM-V2-OD-BE-4-007`: SD-1 = A, SD-2 = A) |
| Governing band | `AXIOM-V2-BE-ROADMAP-001` Band BE-4 |
| Governing requirements | `ITRGA-ASS-V2-BE-4-SCOPE-001` §6 (items 1–12, addressed item-for-item) · guardrails BG-1…BG-12 |
| Platform baseline | Alembic head `20260829_0042` · **750 tests** (552 V1 + 78 BE-1 + 45 BE-2 + 33 P1 + 25 P2 + 17 transition) · provider `twelvedata` `contract_tested` in force (`verified` / persistence `false`) · drift = exactly the inherited V1 9-token set |
| Status | **SUBMITTED FOR ITRGA PLAN REVIEW** |

**Standing discipline: we don't guess. We prove.**

This plan authorizes nothing. Implementation authority arises only from a
Build Order after ITRGA plan approval and Operator authorization
(roadmap §3). No repository change accompanies this submission.

---

## 0. Fixed parameters and reading order

- **SD-1 = A (binding):** labelled-synthetic data basis — BE-2 normalized
  model fed by the V1 simulator adapter; pipeline-validation tier
  (roadmap §0.2); `persistence_permitted` stays `false`; **no provider
  network call in any test**; no credential read/set/use. Real-data
  research validation is a separate, later-governed act and does not block
  BE-4 closure.
- **SD-2 = A (binding):** API-level evidence closure; **browser evidence is
  a recorded residual** (FE band / X-01 joint gate).
- Every section below is mapped to its §6 item and the guardrails it
  satisfies. Evidence classification is stated per claim (Level I =
  runtime/DB/file fact; Level II = executed inspection/collection on the
  machine; Level III = document; Level IV = assertion — not used for
  acceptance-bearing claims).

---

## 1. Reuse and versioning (§6.1; BG-6, BG-9)

### 1.1 V1 deterministic surface — inventory (Level II, executed 2026-08-31)

The inventory below was produced by AST parse of the live workspace files
(not from memory). SHA-256 prefixes pin the exact surface the plan reuses;
full hashes will be embedded in the implementation transcript.

| Module | Size | Public surface | SHA-256 (16) |
|---|---|---|---|
| `app/services/indicators.py` | 971 lines | 22 functions: `sma`, `ema`, `rsi`, `macd`, `bollinger`, `atr`, `hma`, `supertrend`, `ichimoku`, `stochastic`, `cci`, `roc`, `adx_dmi`, `keltner`, `donchian`, `pivot_points`, `camarilla`, `prev_day_levels`, `session_levels`, `zscore`, `percentile_rank`, `linear_regression`; dataclasses `LinePoint`, `BandPoint`, `MacdPoint`, `IndicatorSeries` | `af661b52edd15e44` |
| `app/services/market_structure.py` | 283 lines | 6 functions: `swings`, `struct`, `bos`, `choch`, `fvg`, `order_block_pattern` | `bd83c67279ba2e26` |
| `app/services/indicator_registry.py` | 187 lines | `INDICATOR_REGISTRY` — **29 registered `IndicatorDefinition` entries** (SMA20 … REGCHAN20, incl. the structure family SWINGS55/STRUCT55/BOS55/CHOCH55/FVG3/OBPATTERN); `known_indicator_ids()`; per-definition `disclosure` field (CHART-P03 M8) for labels that could imply institutional behaviour | `02d2e98185bb89b4` |

Entry-point contract (Level II, read in source): every indicator consumes
`list[_Bar] | list[dict]` (OHLCV bars), is a pure function of its inputs
(no I/O, no wall clock, no randomness — verified by module read; the test
strategy in §11 re-proves this at band level), and returns an
`IndicatorSeries` of typed points.

**Reuse rule (BG-9):** BE-4 **imports and calls** this surface. It does not
modify, rewrite, or fork any V1 module. Zero diffs under `app/services/`
and every other V1 path; the V1 552-test regression set stays green.

### 1.2 Computation-versioning contract (spec §53)

New registry table `v2_computation_version` (§5) records each versioned
component with its source pin:

| Component | Initial version | Source pin |
|---|---|---|
| `indicator_engine` | `v1-reuse-1.0.0` | SHA-256 of `indicators.py` + `market_structure.py` + `indicator_registry.py` (recorded at migration seed time; a hash mismatch at compute time is a typed refusal, not a silent proceed) |
| `market_context_engine` | `mce-1.0.0` | SHA-256 of the new MCE module set |
| `chart_intelligence_engine` | `cie-1.0.0` | SHA-256 of the new CIE module set |

Rules: versions are **registered before first use**, immutable once
referenced by any report, independent per component (spec §53), and every
report row and lineage record carries the exact versions used. Inputs are
immutable: a report references its input snapshot (BE-2 series state,
§1.3) and can be recomputed byte-identically from it (determinism test,
§11).

### 1.3 Input snapshot contract

Input = BE-2 read model (`v2_md_bar` series via the accepted read
repositories), bounded `as_of` (existing `require_utc(boundary="as_of")`
discipline, no-future rule). The **input snapshot identity** is the tuple
`(instrument_id, timeframe, source_id, as_of, bar_count, last_open_time,
input_content_hash)` where `input_content_hash` = SHA-256 over the
canonical serialization of the consumed bars. It is stored on the report
row and in the lineage record (`input_snapshot_id`), making
"output → source snapshot" a checkable fact, not prose (BG-7).

---

## 2. Multi-timeframe model (§6.2; BG-5, BG-6)

Spec §15's four layers are **typed schema fields**, not prose:

- Every observation row/JSON element carries `layer TEXT NOT NULL CHECK
  (layer IN ('observed','derived','contextual','statistical'))`.
- Every observation additionally carries `claim_type TEXT NOT NULL CHECK
  (claim_type IN ('fact','derived_observation','contextual_interpretation',
  'prediction'))` (band control: the four claim classes separately typed).
- Coupling constraint (enforced in the engine and by CHECK where
  expressible; always by test): `layer='observed' ⇔ claim_type='fact'`;
  `layer='statistical' ⇒ claim_type='prediction'`. **BE-4 emits no
  `statistical`/`prediction` rows at all** (predictive ML is BE-5/BE-11
  territory); the types exist in the schema so the discipline is
  structural from day one, and a BE-4 emission of either type is a test
  failure.

**No-unsupported-cross-timeframe-conclusion rule (enforced + tested):**
an observation whose `contributing_observation_ids` span more than one
timeframe (a) MUST have `layer IN ('derived','contextual')` — never
`observed`; (b) MUST have `claim_type != 'fact'`; (c) MUST list every
contributing observation id, each resolvable within the same report. The
engine refuses (typed outcome, §6) any cross-timeframe synthesis whose
contributing set is incomplete. A dedicated test constructs the violation
and proves refusal.

---

## 3. Market-context output model (§6.3; BG-5, BG-6, BG-7)

The ten observation families of spec §14, each mapped to its V1
deterministic inputs (all from the §1.1 inventory — no new deterministic
math in BE-4 v1 scope):

| # | Family (`family` field value) | Deterministic inputs (V1 surface) | Layer ceiling |
|---|---|---|---|
| 1 | `prevailing_trend` | `sma`, `ema`, `hma`, `supertrend`, `adx_dmi`, `linear_regression` | derived |
| 2 | `structural_state` | `struct`, `swings` | derived |
| 3 | `protected_swing` | `swings` | derived |
| 4 | `structural_break` | `bos`, `choch` | derived |
| 5 | `liquidity_context` | `fvg`, `order_block_pattern` (V1 `disclosure` text propagated verbatim — structural outputs do not imply institutional order flow) | contextual |
| 6 | `key_levels` | `pivot_points`, `camarilla`, `prev_day_levels`, `donchian` | observed/derived |
| 7 | `session_context` | `session_levels`, `app/services/timeframes.py` session rules | observed/derived |
| 8 | `volatility_state` | `atr`, `bollinger`, `keltner`, `zscore` | derived |
| 9 | `momentum_state` | `rsi`, `macd`, `stochastic`, `cci`, `roc` | derived |
| 10 | `timeframe_relationships` | cross-timeframe composition of families 1–9 (§2 rule applies in full) | contextual |

Every emitted observation carries: `observation_id` (uuid4),
`family`, `timeframe`, `layer`, `claim_type`,
`contributing_observation_ids` (possibly empty only for `observed` rows
whose contribution is the raw indicator output, which then carries the
indicator id + parameters + engine version), `computation_version`
(per-component, §1.2), `as_of` (UTC, bounded), `mode` (explicit; RESEARCH/
SIMULATION only), and the input snapshot reference. Traceability is
therefore a stored graph — lineage from any output to contributing
observations to indicator invocations to the input snapshot (BG-7),
recorded both inside the report artifact and as `v2_lineage_record` rows
on the accepted BE-1 contract (`computation_version`,
`input_snapshot_id`, `source_artifact_ids` fields already exist —
Level II, model read).

---

## 4. Chart-intelligence model (§6.4; BG-5)

Spec §16 pipeline, each stage a separate, versioned step with typed
output:

```
deterministic detection (V1 surface, reused)
        → market context (§3 report, referenced by id — never recomputed inline)
        → chart intelligence (CIE)
        → annotations + interpretation
```

- **Annotations** (`annotation` elements): geometry-bound statements
  (level, zone, swing marker, break marker) — each bound to the
  observation(s) it renders; `claim_type` = `fact` or
  `derived_observation` only.
- **Interpretations** (`interpretation` elements): contextual narrative
  statements — `claim_type='contextual_interpretation'` always; each MUST
  reference ≥1 annotation or observation id; an interpretation with an
  empty basis set is refused (typed outcome + test).
- **Predictions:** none in BE-4 (schema type exists; emission is a test
  failure — §2).
- Facts vs interpretations vs predictions are therefore enforced **at
  schema level** (CHECK constraints on element `claim_type` + basis-set
  NOT-EMPTY rule for interpretations), and re-proved by API evidence
  (§12: the response contract exposes the typing verbatim).

---

## 5. Research read-model expansion (§6.5; BG-8)

### 5.1 New tables (one migration, §9)

Naming note (disclosed): the BE-0 architecture-reference names are plural
(`v2_market_context_reports`, `v2_chart_intelligence_reports`); the
accepted V2 physical convention is singular (`v2_md_provider`,
`v2_audit_event`, `v2_lineage_record` — Level I, current schema). The
plan follows the **accepted singular convention**; the assessment states
final naming is the plan's.

| Table | Purpose | Key columns (all PKs uuid4 `TEXT(36)` — BG-8) |
|---|---|---|
| `v2_computation_version` | Registered component versions (§1.2) | `id` PK; `component` + `version` UNIQUE; `source_hash`; `registered_at`; `evidence_ref` |
| `v2_market_context_report` | Immutable market-context report artifacts | `id` PK; `instrument_id`; `timeframe_set` (JSON); `as_of`; `mode`; `status` (BE-1 model, §6); `input_snapshot_id`; `input_content_hash`; `observations` (JSON, §3 element contract); `engine_versions` (JSON of §1.2 versions); `created_at`; UNIQUE(`instrument_id`,`input_content_hash`,`engine_versions_hash`) — determinism anchor: same input + versions ⇒ same report content |
| `v2_chart_intelligence_report` | Immutable chart-intelligence artifacts | `id` PK; `market_context_report_id` FK→`v2_market_context_report.id`; `as_of`; `mode`; `status`; `annotations` (JSON); `interpretations` (JSON); `engine_versions` (JSON); `created_at` |

Both report tables are **append-only**: no UPDATE path exists in any
repository; immutability is asserted by tests (repository surface audit +
absence-of-writer test), not by new DB triggers — trigger-guarding remains
the provider registry's mechanism and BE-4 does not touch it (BG-3). If
ITRGA prefers DB-level guards on the report tables, the DA flags this as
**open item OI-2** (§14) rather than assuming either way.

### 5.2 Audit and lineage

Every report creation emits: one `v2_audit_event`
(`research.market_context.computed` / `research.chart_intelligence.computed`,
domain `v2.research`, explicit mode, correlation id) and one
`v2_lineage_record` (artifact_type `market_context_report` /
`chart_intelligence_report`, `computation_version`, `input_snapshot_id`,
`source_artifact_ids` = contributing artifact ids). Existing BE-1
contracts; no schema change to BE-1 tables.

---

## 6. Typed outcomes (§6.6; BG-5)

`insufficient_data` is a **first-class typed outcome**, not an error:

| Condition | Report `status` (BE-1 model) | Behaviour |
|---|---|---|
| Enough bars for every requested family | `available` | Full report |
| Some families computable, some short of `required_bars` | `degraded` | Partial report; each missing family present as a typed `insufficient_data` element naming the shortfall (`required_bars` vs supplied — from the V1 registry's own `required_bars`, Level II §1.1) |
| No family computable / empty series | `unavailable` | Report row with zero observations and the typed reason |
| Input series staleness beyond the declared bound at `as_of` | `stale` | Report emitted with staleness disclosure fields |
| Snapshot/version resolution impossible | `unknown` | Typed unknown — allowed state, never guessed over |
| RBAC denial | `denied` | No report row; audited refusal |

All six BE-1 states (`available`, `unavailable`, `stale`, `degraded`,
`unknown`, `denied`) are reachable and each is covered by a dedicated test
(§11). Unknown is an allowed state; no state is fabricated (charter
invariant — no fabricated state).

---

## 7. Endpoints (§6.7; BG-2) — and one flagged interpretation point

Read-only surface, mounted on the accepted V2 aggregate router
(`app/v2/api/router.py`, prefix `/v2` — Level II, source read), new
sub-router prefix `/market-context`:

| Endpoint | Method | Contract |
|---|---|---|
| `/market-context/reports` | GET | List market-context report metadata (filters: instrument, timeframe, mode, status; paginated) |
| `/market-context/reports/{id}` | GET | Full report — observations with `layer`/`claim_type` typing exposed verbatim |
| `/market-context/chart-intelligence/{id}` | GET | Chart-intelligence artifact — annotations vs interpretations separately arrayed, basis ids included |
| `/market-context/versions` | GET | Registered computation versions |

All responses carry the standard V2 envelope: explicit `mode`,
`correlation_id`, typed `status`, provenance/authority labels
(`live:simulated` / `seed:synthetic` propagated from the BE-2 source —
labelled synthetic is visible end-to-end, BG-4). No client-side
authoritative computation: the terminal renders; it never derives.

**Flagged for ITRGA (FP-1, honest tension — not resolved unilaterally):**
reports must be *created* by some governed path, and BG-2 says the band
exposes read-only endpoints. Two compliant designs exist; the DA
recommends (a):

- **(a) Recommended — one governed computation writer** `W-MC`: a single
  `POST /market-context/compute` endpoint, RBAC-gated by a new
  `v2.research.market_context.compute` permission (admin, SAL-aligned),
  mode-enforced (RESEARCH/SIMULATION only), fully audited, idempotent by
  the §5.1 determinism anchor (same input + versions ⇒ the existing report
  is returned, not duplicated). Precedent: BE-2's accepted governed writer
  (W-1 catalog refresh). All *read model* endpoints remain strictly GET.
- **(b) Alternative — materialize-on-first-read:** GET deterministically
  computes and persists on first access. Rejected by the DA as a
  recommendation because a side-effecting GET blurs the audit contract.

The plan proceeds on (a) unless the plan review directs (b) or another
form. Permission additions: `v2.research.market_context.read`,
`v2.research.chart_intelligence.read`, `v2.research.market_context.compute`
(seeded in the §9 migration, revision-local literal rows — DEL-004
lesson).

---

## 8. Data basis (§6.8; BG-4) — SD-1 = A, binding

- Input exclusively via the BE-2 normalized model with the **V1 simulator
  adapter (labelled synthetic)**; authority labels `live:simulated` /
  `seed:synthetic` propagate into every report and response.
- **Validation tier declared (roadmap §0.2): pipeline-validation.** The
  band's evidence proves the *pipeline* (determinism, temporal integrity,
  lineage, typing); it substantiates **no market conclusion**. This
  declaration is embedded in the plan, the report artifacts (a
  `validation_tier` field), and the eventual Delivery Report.
- No provider network call in any test (existing socket-guard pattern from
  BE-3 P1 reused in the BE-4 test module); no credential read/set/use; the
  Four Secrets untouched; `persistence_permitted` stays `false` and is
  **asserted untouched** by a no-touch test (§11).

## 9. Migrations (§6.9; BG-8)

- **One new revision:** `20260831_0043_v2_be4_research_read_models`
  (`down_revision = "20260829_0042"`). Creates the three §5.1 tables +
  indexes, seeds `v2_computation_version` initial rows and the three §7
  permissions (revision-local literal rows). **Touches nothing else** — in
  particular no guarded table, no BE-1/BE-2/BE-3 object (BG-3).
- `upgrade`/`downgrade` symmetric; downgrade drops only the three new
  tables and the revision's own seed rows. Rollback evidence: an executed
  upgrade→downgrade→upgrade cycle in the test module, with
  content-based row comparison (**no position-based row assertions** —
  PGF-012 lesson, honoured across every BE-4 test and any future pack).
- `alembic check` at the new head = **exactly** the inherited V1 9-token
  set, zero BE-4 tokens — a dedicated drift-gate test asserts this
  (pattern proven in the transition band).
- PKs: uuid4 `TEXT(36)` everywhere (BG-8). SQLite-only DA workspace
  (`AXIOM-V2-BE-1-PG-EXCEPTION-001`); dialect-neutral DDL via SQLAlchemy
  types; timezone normalization via the accepted `_utc_from_store`
  pattern.

## 10. No-touch list (§6.10; BG-3, BG-9)

BE-4 does **not** change:

- `v2_md_provider`, `v2_md_provider_status_history` (in-force
  `contract_tested` state; guards remain; **no** new provider status, no
  history append, no write to the BE-3 P2 audit domain);
- the provider ladder (`integrated`+ is a separate chain; the transition
  authority string was consumed);
- `persistence_permitted` (stays `false`);
- any BE-1/BE-2/BE-3 table, seed, trigger, or migration;
- any V1 module (`app/services/`, `app/api/routes/`, models, migrations —
  extension only, zero rewrites);
- deployment/SAL configuration; the Four Secrets;
- Git state (no Git/GitHub operation — Operator custody, deferred).

A **no-touch test group** proves the provider row, history count, guard
trigger set, and `persistence_permitted` are byte-identical before/after
the full BE-4 suite runs.

## 11. Test strategy (§6.11; BG-12)

New module(s) `tests/test_v2_be4_*.py`. Groups, each mapped to exit
evidence (§12):

1. **Determinism/reproducibility:** same input snapshot + versions ⇒
   byte-identical observations JSON (hash compare); recompute after
   engine-version bump ⇒ new report, old immutable.
2. **Temporal integrity:** `as_of`-bounded computation; a bar after
   `as_of` present in the DB is provably excluded (no-future); wall-clock
   independence (no `now()` in the deterministic core — asserted by
   construction-token scan of the MCE/CIE modules, path-exact pattern from
   the accepted P2 test).
3. **Lineage:** for a sampled output, walk output →
   contributing_observation_ids → indicator invocation → input snapshot;
   assert the `v2_lineage_record` row matches.
4. **Typing:** layer/claim_type CHECKs; cross-timeframe rule violation
   refused (§2); interpretation-without-basis refused (§4); zero
   `prediction`/`statistical` emissions.
5. **Typed outcomes:** each of the six BE-1 states reached (§6 table).
6. **No-touch/guards:** §10 group; immutability of report rows (no
   repository UPDATE surface).
7. **Migration:** upgrade/downgrade/re-upgrade with content-based
   comparison; drift gate; permission seeds present exactly once.
8. **RBAC + network denial:** endpoint permission enforcement incl.
   `denied`; socket-guard proves zero network attempts.
9. **Regression:** full suite green; **test delta against the 750
   baseline reported explicitly** in the Delivery Report (750 + N, N
   itemized per group; no double counting).

## 12. Evidence plan + exit-evidence mapping (§6.12; BG-10, BG-12)

Discipline per run: single transcript; `-File` execution for any
Operator-side script; MD5/SHA self-check on the machine; credential scan
CLEAN before every archive; REM-001 literal-contents transcript for every
changed file; distinct non-duplicated test accounting.

| Roadmap exit-evidence item | Artifact |
|---|---|
| Deterministic/reproducibility tests | §11.1 group, executed in the delivery transcript |
| Temporal-integrity tests | §11.2 group |
| Lineage output→snapshot+version | §11.3 group + sampled Level I DB walk in the evidence annex |
| Direct **API** evidence of facts vs interpretation | Executed API transcript: report + chart-intelligence responses showing `claim_type` separation verbatim (SD-2 = A closure) |
| Direct **browser** evidence | **RECORDED RESIDUAL** (SD-2 = A) — declared here, to be carried into the Delivery Report and determination; verified at the FE band / X-01 joint gate |

## 13. Explicit exclusions (assessment §5, in the plan's own words)

No actuation of any kind (no order/execution/broker/account/position/P&L
path or state — execution stays default-deny). No external AI. No
provider network call anywhere in the band; no credential use. No
frontend work (sequencing directive; SD-2 residual recorded instead). No
Git operation. No change to the BE-3 P2 in-force state; no `integrated`
or higher ladder step; no persistence permission. No predictive/ML
output (BE-5/BE-11). No performance or market-conclusion claim from
synthetic-input evidence (tier discipline).

## 14. Known limitations / open items (honest; unknown is an allowed state)

- **FP-1 (§7):** report-creation path — governed writer (recommended) vs
  materialize-on-read; ITRGA plan review decides.
- **OI-2 (§5.1):** DB-level immutability guards on the new report tables —
  DA proposes repository-level append-only + tests; ITRGA may direct
  triggers.
- **OI-3:** route-table reference `/api/v2/market-context/` vs the actual
  accepted mount (`/v2` aggregate router under the V1 app prefix). The
  plan follows the **accepted physical mount** and records the reference
  discrepancy; no route migration is proposed in BE-4.
- **OI-4:** exact `timeframe_relationships` composition rules (which
  cross-timeframe statements are permitted as `derived` vs `contextual`)
  will be enumerated as a fixed rule table in the implementation and
  asserted by tests; the plan pins the ceiling (§2) and the refusal
  behaviour now.
- Session/timezone semantics for `session_context` on synthetic 24×7
  simulator data are label-only (no venue claim) — disclosed in the
  report artifact.
- "BE-4 read models work" remains **NOT PROVEN** until the band's evidence
  exists; synthetic input proves the pipeline, never market conclusions.

## 15. Delivery phasing (plan-level ordering; the Build Order governs)

M1 migration + version registry → M2 MCE (families 1–9) → M3 timeframe
relationships (§2 rules) → M4 CIE → M5 endpoints + RBAC → M6 evidence
pack + Delivery Report. Single band, single Delivery Report; internal
milestones exist for review traceability only.

---

*We don't guess. We prove.*
**— Development Authority, 2026-08-31**
**End of AXIOM-V2-BE-4-DA-PLAN-001 v1.0.0**
