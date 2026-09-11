# AXIOM V2 BE-6 — ENGINEERING DESIGN PLAN
## Portfolio and Risk Research Domain

| Field | Value |
|---|---|
| Document ID | AXIOM-V2-BE-6-DA-PLAN-001 |
| Version | 1.0.0 |
| Date | 2026-09-03 |
| Author | Development Authority (DA) |
| Commissioning | `ITRGA-CN-V2-BE-6-001` (Operator authorization 2026-09-03) |
| Governing band | `AXIOM-V2-BE-ROADMAP-001` Band BE-6 (§0 — verbatim contract embedded) |
| Platform baseline | head `20260902_0045` (single) · next migration **0046** · **856 tests / 0 failed** (pytest 8.4.2 certified pin) · drift = exactly the 9 inherited V1 tokens · 28 v2 triggers · 35 permissions · 5 compver rows · bands BE-0…BE-5 closed, registers Rev-13 synced |
| Status | **SUBMITTED FOR ITRGA PLAN REVIEW** |

**Standing discipline: we don't guess. We prove.**

This plan authorizes nothing and executes nothing. Sequencing disclosure
(honest): the commissioning record §2 awaited transmission of the roadmap
Band BE-6 section before the ITRGA authors `ITRGA-REQ-V2-BE-6-PLAN-001`.
That section is **already in the governed workspace** —
`uploads/V2_BACKEND_ROADMAP.md` (repo-resident since the V2 clone; the
same file the BE-5 REQ was built from) — and is quoted verbatim in §0 so
the ITRGA can verify zero divergence. This plan is authored against that
band contract plus the BE-5 REQ structure (whose checklist the
commissioning says carries by default) and the carried Pins P-1…P-5. If
the forthcoming REQ adds items, the DA answers them by plan revision —
the standard correction path.

---

## 0. Band contract (verbatim from `AXIOM-V2-BE-ROADMAP-001`, Band BE-6)

> **Objective.** Introduce portfolio and risk capabilities initially as
> governed research/read models, independent of live account access or
> execution.
>
> **Scope.** hypothetical portfolios, allocations, exposures,
> concentration, factor/risk, scenario and stress-test read models; risk
> metric contracts with method, input, uncertainty, limitations, and time
> basis; report-preview/export contracts only where separately
> authorized; portfolio/risk artifact lineage.
>
> **Explicit exclusions.** No real account state, broker balances,
> orders, positions, or live P&L in this band; no action-oriented risk
> recommendation that bypasses governance.
>
> **Exit evidence.** numerical method tests and independent recomputation
> samples; uncertainty/assumption visibility; data-source and as-of
> validation; UI/API evidence distinguishing hypothetical research from
> account state.

Source: `uploads/V2_BACKEND_ROADMAP.md` (in-repo). ITRGA verification:
diff the §0 quote against that file's Band BE-6 section.

## Part 1 — Band decomposition and unit structure

### 1.0 V1 surface inventory (Level II — AST-parsed + hashed this session)

Reused read-only as computational reference and lineage targets; never
rewritten (charter §3):

| V1 asset | Content | sha256-16 |
|---|---|---|
| `app/execution_research/risk.py` | `ExecutionRiskResearchReportService` (existing V1 execution-risk research reports) | `6940509097b65e6f` |
| `app/execution_research/analytics.py` | `SimulatedExecutionAnalyticsReportService` | `b2fe2fdb06e49ca7` |
| `app/execution_research/ledger.py` | `SimulatedPaperLedgerService` (simulated ledger entries — a legitimate *simulated* holdings source) | `6ec97a72aea910bf` |
| `app/execution_research/simulation.py` | deterministic simulated fills | `f163e610ba1a6215` |
| V1 tables (untouched) | `portfolio_risk_reports`, `execution_risk_research_reports`, `simulated_paper_ledger_entries` | V1 migrations (immutable) |
| BE-2 read model + BE-4 MCE outputs | bar series (labelled synthetic) and volatility observations — price inputs for risk computation | accepted bands |

Full SHA-256 of every reused file lands in the delivery transcript
(REM-001 / OBS-1 pattern).

### 1.1 Units

| Unit | Kind | Responsibility | Depends on |
|---|---|---|---|
| **U-1** | Migration **0046** + models | `v2_portfolio_definition` (versioned-immutable, P-1 pattern) + `v2_portfolio_risk_report` (immutable artifact, P-2/0043 pattern) + guards + permission/compver seeds | 0045 head |
| **U-2** | Risk engine (`app/v2/portfolio_research/`) | Deterministic metric computations with the **risk-metric contract**: method · inputs · value · uncertainty · limitations · time basis, per metric | U-1 |
| **U-3** | API | Read-only surface + two governed writers (define-portfolio, compute-risk-report), all under `/portfolio-research` on the V2 aggregate router | U-1, U-2 |
| **U-4** | Evidence | Delivery Report + transcripts + register sync | all |

Delivery packaging: single package (one Build Order) proposed — the band
is one migration; per-unit packaging remains available at the Operator's
choice.

### 1.2 U-1 — Migration `20260903_0046_v2_be6_portfolio_research` (exact DDL)

`down_revision = "20260902_0045"`. PKs uuid4 `TEXT(36)`.

**Table `v2_portfolio_definition`** — hypothetical portfolios only;
versioned-immutable (P-1: `record_seq` + `supersedes` forward link;
edits = successor rows; currency = greatest `record_seq`):

| Column | Type | Constraint |
|---|---|---|
| `id` | String(36) | PK |
| `portfolio_id` | String(64) | NOT NULL; `UNIQUE(portfolio_id, record_seq)` (`uq_v2_pfdef_id_seq`) |
| `record_seq` | Integer | NOT NULL |
| `supersedes` | String(36) | NULL — successor holds predecessor id (C-1 vocabulary) |
| `name` | String(128) | NOT NULL |
| `basis` | String(16) | NOT NULL CHECK IN (`hypothetical`) — **single-value CHECK by design**: the band's exclusion made structural; a future band widens it, this band cannot |
| `allocations` | JSON | NOT NULL — `[{instrument_id, weight}]`; writer validates weights sum to 1.0 ± 1e-9 and are each ≥ 0 (long-only v1 scope, disclosed) |
| `base_currency` | String(8) | NOT NULL |
| `data_class` | String(32) | NOT NULL CHECK (6-value taxonomy — same literal as 0044/0045) |
| `assumptions` | JSON | NOT NULL — free-form declared assumptions (visibility law: never empty; writer refuses `{}` without at least a declared `none_beyond_defaults: true`) |
| `mode`, `operator_id`, `correlation_id`, `created_at` | | NOT NULL / NULL per BE-1 contract (O-3 posture carried: `correlation_id` nullable at schema, writer-minted) |

**Table `v2_portfolio_risk_report`** — immutable artifact (P-2 / 0043
pattern):

| Column | Type | Constraint |
|---|---|---|
| `id` | String(36) | PK |
| `portfolio_definition_id` | String(36) | NOT NULL, indexed (`ix_v2_pfrisk_def`) |
| `as_of` | DateTime(tz) | NOT NULL — no-future rule enforced by writer |
| `time_basis` | JSON | NOT NULL — window start/end, bar timeframe, observation count (the contract's "time basis", per metric AND report-level) |
| `input_refs` | JSON | NOT NULL — series identifiers + BE-4 observation ids consumed (lineage inputs) |
| `inputs_hash` | String(64) | NOT NULL — SHA-256 over canonical serialized inputs |
| `metrics` | JSON | NOT NULL — list of metric objects, each carrying the **full risk-metric contract**: `{metric, method, method_citation, inputs, value, uncertainty, limitations, time_basis, insufficient: bool}` |
| `scenarios` | JSON | NOT NULL — stress/scenario results, same contract shape; empty list allowed with typed reason |
| `status` | String(16) | NOT NULL CHECK IN (`available`,`degraded`,`unavailable`,`stale`,`unknown`,`denied`) — BE-1 model |
| `basis_label` | String(32) | NOT NULL CHECK IN (`hypothetical-research`) — **every artifact self-declares non-account-state** (exit-evidence item 4 made structural) |
| `data_class` | String(32) | NOT NULL CHECK (6-value) |
| `engine_versions` / `engine_versions_hash` | JSON / String(64) | NOT NULL — OBS-3 canonical serialization |
| `mode`, `operator_id`, `correlation_id`, `created_at` | | per BE-1 contract |
| UNIQUE | (`portfolio_definition_id`, `inputs_hash`, `engine_versions_hash`) | `uq_v2_pfrisk_determinism_anchor` — same input + versions ⇒ existing report returned (R-1 idempotency pattern) |

**Guard triggers (4; exact messages):**

| Trigger | Message |
|---|---|
| `v2_portfolio_definition_immutable_update` | `V2 portfolio definitions are immutable; UPDATE prohibited` |
| `v2_portfolio_definition_immutable_delete` | `V2 portfolio definitions are immutable; DELETE prohibited` |
| `v2_portfolio_risk_report_immutable_update` | `V2 portfolio risk reports are immutable; UPDATE prohibited` |
| `v2_portfolio_risk_report_immutable_delete` | `V2 portfolio risk reports are immutable; DELETE prohibited` |

**Permission seeds (revision-local literals; SAL-aligned):**
admin: `v2.research.portfolio.read` (SAL-2), `v2.research.portfolio.define`
(SAL-3), `v2.research.portfolio_risk.read` (SAL-2),
`v2.research.portfolio_risk.compute` (SAL-3); operator:
`v2.research.portfolio.read`, `v2.research.portfolio_risk.read` — 6 rows.
No `account`/`position`/`order` vocabulary anywhere (the forbidden-marker
guard enforces this at import; note the band deliberately avoids the word
"position" in permissions AND schema — "allocations"/"exposures" only).

**compver seed (P-4):** `portfolio_risk_engine = pre-1.0.0`, source hash
computed at migration time over the co-delivered U-2 files (C-2
discipline: the future application-act instrument re-pins these files;
recorded now).

**Data seeds:** none (no fabricated portfolios). **Downgrade:** symmetric
(2 tables, 4 triggers, 6 permission rows, 1 compver row — compver delete
via the established guard drop/recreate/verify pattern).

**Post-unit pinned expectations (P-5):**

| Measure | Before | After 0046 |
|---|---|---|
| v2 triggers (exact names enumerated at evidence) | 28 | **32** |
| `v2_permission` rows | 35 | **41** |
| `v2_computation_version` rows | 5 | **6** |
| `alembic check` drift at head | 9 inherited V1 tokens | **unchanged; zero BE-6 tokens** |

### 1.3 Non-migration artifact sets

| Unit | New files | Versioning |
|---|---|---|
| U-2 | `app/v2/portfolio_research/{__init__,contracts,metrics,scenarios}.py` | `pre-1.0.0` compver (P-4 co-delivery) |
| U-3 | `app/v2/portfolio_research/api.py`; 1 additive mount line in `app/v2/api/router.py` | rides `pre` |
| Modified (enumerated up front, OBS-1 law) | `app/v2/api/router.py` · `app/v2/rbac/permissions.py` (4 constants + grants + SAL) · `app/db/models/__init__.py` (2 model imports) | additive only |

## Part 2 — Risk-metric contract set (each designed, not named)

Every metric is a **pure deterministic function** (no wall clock, no
randomness — seeded/fixed where any sampling exists; v1 scope uses closed-
form and historical methods only, zero sampling). Every output carries
the full contract; a metric that cannot be honestly computed returns a
**typed `insufficient` entry** (required vs available observations), never
a fabricated value.

| Metric family | Method (v1 scope; citation string in every output) | Uncertainty field |
|---|---|---|
| Exposures | per-instrument weight × basis; gross/net (long-only v1: equal) | exact (arithmetic) — uncertainty = `{"basis":"deterministic"}` |
| Concentration | Herfindahl–Hirschman index over weights; top-N share | exact |
| Volatility | sample stdev of portfolio log returns over the declared window (BE-2 bars, weighted) | CI via chi-square bounds at the cited confidence level |
| Drawdown | max peak-to-trough on the hypothetical value series | exact over the window; window-dependence declared in limitations |
| VaR | **historical** (empirical quantile) AND **parametric-normal** — both reported, never merged (the BE-5 economic⊥statistical lesson applied to methods) | quantile-order-statistic interval (historical); normality assumption declared as a limitation (parametric) |
| Factor/risk decomposition | v1 scope: market-class grouping shares (forex/crypto/metal per the BE-2 instrument registry) — declared as **grouping, not regression**; regression-based factors are future-band | exact |
| Scenario / stress | declared deterministic shocks (e.g. `{instrument_class: pct_shock}`) applied to allocations; result = re-valued portfolio delta | exact given the shock; shock realism NOT claimed (limitation field mandatory) |

**Method-citation law:** each output's `method_citation` names the formula
and its source constant(s); thresholds/confidence levels are cited from
existing V1/V2 config where they exist (`ValidationConfig.confidence_level`
= 0.95 — the established citation) and declared band-level otherwise —
no invented numbers presented as spec values.

**Independent-recomputation design (exit-evidence item 1):** the DR ships
a **worked-sample annex** — one pinned portfolio + pinned synthetic input
series + every metric's expected value to stated precision, so the ITRGA
recomputes by hand/script without executing the engine. The determinism
anchor guarantees the engine reproduces the same bytes.

## Part 3 — Hard boundaries (band exclusions made structural)

1. **No real account state, broker balances, orders, positions, live
   P&L:** no such table, column, endpoint, or vocabulary; `basis` CHECK
   admits only `hypothetical`; `basis_label` only `hypothetical-research`;
   the forbidden-permission-marker guard remains active; the V1
   `simulated_paper_ledger` is read-only reference and clearly labelled
   simulated wherever consumed.
2. **No action-oriented risk recommendation:** outputs are observations
   and computed metrics only — no `recommendation`, `action`, `hedge`,
   `rebalance` field exists in any schema or response; a construction-
   token test asserts their absence in the band's modules.
3. **RESEARCH mode only** for writers; reads read-only; typed outcomes
   everywhere; unknown is an allowed state.
4. Data honesty: 6-class taxonomy on both tables; **first landing =
   `synthetic`/`simulated` only** (corpus-gated refusal of
   `historical_real`/`live` with typed reasons — V2-TD-18 continuity).
5. No network in tests (socket guard); no credential anywhere (the band
   prompts for none — stated per the T-12 pattern); no Git by the DA.
6. Report **preview/export contracts: EXCLUDED** — the roadmap authorizes
   them "only where separately authorized"; no such authorization exists;
   explicitly out of scope (boundary registered).

## Part 4 — Mode, audit, security integration

BE-1 contract columns on every row. Audit events
(`domain="v2.portfolio_research"`): `portfolio.defined`,
`portfolio.superseded`, `portfolio_risk.computed`,
`portfolio_risk.compute.reused`, `portfolio_risk.compute.unknown`, plus
generic denial on RBAC refusal. Lineage rows per artifact
(`artifact_type`: `portfolio_definition`, `portfolio_risk_report`;
`input_snapshot_id` = inputs hash; `computation_version` = engine versions
hash; `source_artifact_ids` = definition id + consumed BE-4 observation
ids). Redaction gate untouched.

## Part 5 — Test plan (fail-first; floor 856 → projected ≥ 906)

| Unit | Budget | Groups |
|---|---|---|
| U-1 | 10 | migration-up content (0043 pattern); 4 guard messages verbatim; CHECK vocabularies (incl. the single-value `basis` CHECK refusing `real`); P-5 totals (32/41/6); downgrade cycle content-based; drift gates at head; no-touch across 0046 (BE-3/BE-4/BE-5 state byte-identical) |
| U-2 | 22 | per-metric: ≥1 correctness test against hand-computed values (the worked-sample annex fixtures) + ≥1 typed-insufficient test; determinism (byte-identical recomputation); both-VaR-methods-reported test; no wall-clock/randomness construction-token scan; weight-validation refusals (sum≠1, negative) |
| U-3 | 16 | define/supersede versioning (P-1 semantics; currency projection); compute + anchor idempotency; six BE-1 states; `basis_label` on every response (hypothetical-vs-account evidence); data-class refusal; forbidden-token absence (no recommendation fields); RBAC incl. `denied` + unauthenticated; as-of no-future; socket guard |
| Regression | 2 | full suite green; V1 552 intact |
| **Total** | **50** | **floor ≥ 906** |

## Part 6 — Evidence plan

RSR-1-format Level I API transcript (endpoint path pin under
`/api/v1/v2/portfolio-research/*`; inline ASSERTs; six states; the
hypothetical-label evidence; drift direct runs at the 0046 head) ·
RSR-2-format raw `pytest -v` (count + itemization vs 856) · REM-001
source transcript (full manifest + literals; reused-V1 full hashes) ·
**worked-sample annex** for independent recomputation (Part 2) · full
MD5+SHA-256 on every artifact (intake-§4 law) · credential scans CLEAN ·
DR requirement map: band contract §0 items + Pins P-1…P-5 + the
forthcoming REQ checklist item-for-item.

## Part 7 — Register impacts

Maturity: `Portfolio Research` + `Risk Research` → IMPLEMENTED at
delivery (COMPLETE is the acceptance act's). Risk register: +2 (hypothetical-
mistaken-for-account-state — mitigated by structural labels; metric-
overtrust — mitigated by mandatory uncertainty/limitations). Debt: +2
(long-only v1 allocations scope; grouping-not-regression factor scope).
State-file serialization per the 30.x convention.

## Part 8 — Boundaries vs neighbours

| Out of BE-6 | Belongs to | Why |
|---|---|---|
| Backtesting engines, replay, scheduled jobs | BE-7 | BE-6 computes present-state hypothetical risk from existing series; running strategies is BE-7 |
| Real accounts/balances/orders/positions/live P&L | BE-8…BE-10 | band exclusion; structurally impossible here |
| External AI commentary on risk | BE-11 | boundary |
| Real historical data for risk inputs | corpus track | data-honesty gate (V2-TD-18); declared tiers only |
| Report preview/export | separate authorization | roadmap conditional not granted |
| Regression-based factor models, short/leveraged allocations | future BE-6 extension band | v1 scope honesty (Part 7 debt rows) |

## Part 9 — Package size / review volume

1 migration (~230 lines) · 5 modules (~1,300 lines) · 2 model classes ·
~50 tests (~1,900 lines) · 3 modified files (enumerated §1.3) · source
transcript ~140 KB · API/testrun transcripts ~90 KB · worked-sample annex
~8 KB · DR ~12 KB. Single review package.

## Part 10 — Known limitations (honest)

- Long-only, weights-sum-to-1 allocations; parametric VaR carries the
  declared normality assumption; factor decomposition is grouping-only —
  all declared in `limitations` per output and registered as debt.
- All BE-6 evidence is pipeline-validation tier on labelled synthetic
  inputs; **no risk conclusion about real markets is claimed or
  claimable** (NOT PROVEN until the corpus track).
- The plan may be re-reviewed against `ITRGA-REQ-V2-BE-6-PLAN-001` once
  issued; deltas resolve by plan revision.

---

*We don't guess. We prove.*
**— Development Authority, 2026-09-03**
**End of AXIOM-V2-BE-6-DA-PLAN-001 v1.0.0**
