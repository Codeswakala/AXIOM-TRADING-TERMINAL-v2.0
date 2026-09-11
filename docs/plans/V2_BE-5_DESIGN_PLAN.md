# AXIOM V2 BE-5 — ENGINEERING DESIGN PLAN
## Predictive ML, Signal, and Research Governance Expansion

| Field | Value |
|---|---|
| Document ID | AXIOM-V2-BE-5-DA-PLAN-001 |
| Version | 1.0.0 |
| Date | 2026-09-02 |
| Author | Development Authority (DA) |
| Source request | `ITRGA-REQ-V2-BE-5-PLAN-001` (checklist §1.1–§1.9 addressed item-for-item) |
| Governing band | `AXIOM-V2-BE-ROADMAP-001` Band BE-5 |
| Governing spec | `docs/governance/07_ML_SPEC.md` (cited per contract in §3) |
| Platform baseline | working DB head **`20260831_0043`** (in force, ITRGA-DET-V2-0043-APPLY-001) · **789 tests** · drift = exactly the 9 inherited V1 tokens · RESEARCH/SIMULATION only · FE blocked |
| Status | **SUBMITTED FOR ITRGA PLAN REVIEW** |

**Standing discipline: we don't guess. We prove.**

This plan authorizes nothing and executes nothing. It is a document.
Implementation begins only after ITRGA plan review, Operator approval, and
per-unit Build Orders (§3 delivery model). No credential is prompted for
or used anywhere in this band (§6.3).

---

## 0. Reading map (request checklist → plan section)

§1.1 → Part 1 · §1.2 → Parts 2–5 · §1.3 → Part 6 · §1.4 → Part 7 ·
§1.5 → Part 8 · §1.6 → Part 9 · §1.7 → Part 10 · §1.8 → Part 11 ·
§1.9 → Part 12. Known limitations: Part 13.

---

## Part 1 — Band decomposition and unit structure (§1.1)

### 1.0 V1 surface inventory (Level II, AST-parsed + hashed this session)

BE-5 is an **additive governance overlay** on the existing V1 ML research
surface — reused, never rewritten (charter §3):

| V1 asset | Content | Pin (sha256-16) |
|---|---|---|
| Tables (V1, untouched) | `model_artifacts`, `experiments`, `dataset_snapshots` (+3 dataset satellites), `feature_definitions`, `feature_quality_reports`, `advisory_signals`, `signal_validation_reports` | schema per V1 migrations (immutable) |
| `app/ml/validation/service.py` | `ValidationConfig`, `StatisticalValidationService` (walk-forward, OOS, bootstrap, significance) | `029f3f36fa13fc27` |
| `app/ml/calibration/service.py` | `CalibrationConfig`, `CalibrationService` | `5cc28c6e13a7752a` |
| `app/ml/economic/service.py` | `CostProvenance`, `CostInput`, `CostScenario`, `HypotheticalTrade` | `c49527ed12f4d2ca` |
| `app/ml/{models,experiments,features,dataset,generalization}` | baseline/harness/experiment services | full hashes at delivery (REM-001) |

Full SHA-256 of every reused file lands in the implementation transcript
(the BE-4 OBS-1 pattern).

### 1.1 Units (sequence, dependencies, single responsibility)

| Unit | Kind | Responsibility | Depends on |
|---|---|---|---|
| **U-1** | Migration **0044** + models | ML governance registry overlay: `v2_ml_governance_record` + `v2_ml_lifecycle_event` (+ guards, permissions) | 0043 head |
| **U-2** | Services + contracts | Eligibility / calibration / freshness / economic-validation / rollback **decision contracts** bound to 07_ML_SPEC (no new math — V1 services reused as evaluators) | U-1 |
| **U-3** | Migration **0045** + models | Signal contracts: `v2_signal_record` (structural/predictive separately typed; withheld/expired/refused permanent states) + `v2_signal_state_event` (+ guards, permissions) | U-1 |
| **U-4** | Services + read API | Signal lineage/uncertainty/limitation emission + the single governed signal writer; read-only endpoints under `/v2/research-governance` | U-2, U-3 |
| **U-5** | Services + read API | Research reports / model diagnostics evidence artifacts (reuse `v2_market_context_report` pattern; audit+lineage hooks) | U-1 |
| **U-6** | Evidence | Delivery Report + transcripts + register sync | all |

Each unit is separately implementable under its own future Build Order (or
one BO covering all units, at the Operator's choice — the plan supports
both).

### 1.2 U-1 — Migration `20260902_0044_v2_be5_ml_governance` (exact DDL)

`down_revision = "20260831_0043"`. All PKs uuid4 `TEXT(36)`.

**Table `v2_ml_governance_record`** — the V2 governance overlay row for a
V1 model artifact (additive; references by id, never alters V1):

| Column | Type | Constraint |
|---|---|---|
| `id` | String(36) | PK |
| `model_artifact_id` | String(36) | NOT NULL; UNIQUE (`uq_v2_mlgov_artifact`) — one governance record per artifact |
| `registry_version` | String(64) | NOT NULL |
| `eligibility_status` | String(32) | NOT NULL CHECK IN (`unevaluated`,`eligible`,`ineligible`,`expired`) |
| `calibration_status` | String(32) | NOT NULL CHECK IN (`unevaluated`,`calibrated`,`miscalibrated`,`stale`) |
| `freshness_status` | String(32) | NOT NULL CHECK IN (`fresh`,`stale`,`expired`,`unknown`) |
| `economic_status` | String(32) | NOT NULL CHECK IN (`unevaluated`,`viable`,`unviable`) — **independent of statistical status per 07_ML_SPEC Economic Validation** ("Both conclusions shall be reported independently") |
| `statistical_status` | String(32) | NOT NULL CHECK IN (`unevaluated`,`significant`,`not_significant`) |
| `deployment_class` | String(32) | NOT NULL CHECK IN (`research`,`shadow`,`champion`,`challenger`,`retired`) — shadow/champion/challenger metadata (§1.2) |
| `rollback_target_version` | String(64) | NULL (07_ML_SPEC Model Registry: "rollback version") |
| `data_class` | String(32) | NOT NULL CHECK IN (`synthetic`,`simulated`,`historical_real`,`live`,`stale_cached`,`unavailable`) — §0.2 taxonomy, Part 6.7 |
| `evidence_refs` | JSON | NOT NULL — report ids backing each status (report existence necessary, never sufficient — the statuses are set only by the U-2 decision contracts) |
| `mode`, `operator_id`, `correlation_id` | String | NOT NULL (BE-1 contract) |
| `created_at`, `updated_at_event_id` | DateTime / String(36) | NOT NULL; `updated_at_event_id` = FK-by-value to the latest lifecycle event (state changes ONLY via events) |

**Table `v2_ml_lifecycle_event`** — append-only decision log:

| Column | Type | Constraint |
|---|---|---|
| `id` | String(36) | PK |
| `governance_record_id` | String(36) | NOT NULL, indexed (`ix_v2_mlev_record`) |
| `event_type` | String(48) | NOT NULL CHECK IN (`registered`,`eligibility_evaluated`,`calibration_evaluated`,`freshness_evaluated`,`economic_evaluated`,`statistical_evaluated`,`promoted`,`demoted`,`refused`,`rolled_back`,`retired`) |
| `from_value` / `to_value` | String(64) | NOT NULL (content-exact state transition) |
| `decision_basis` | JSON | NOT NULL — thresholds applied + report ids + spec citation string |
| `mode`, `actor_id`, `operator_id`, `correlation_id` | String | NOT NULL |
| `created_at` | DateTime(tz) | NOT NULL |

**Guard triggers (R-2 pattern, exact refusal messages):**

| Trigger | Fires | Message (exact) |
|---|---|---|
| `v2_ml_lifecycle_event_immutable_update` | UPDATE ON `v2_ml_lifecycle_event` | `V2 ML lifecycle events are immutable; UPDATE prohibited` |
| `v2_ml_lifecycle_event_immutable_delete` | DELETE ON `v2_ml_lifecycle_event` | `V2 ML lifecycle events are immutable; DELETE prohibited` |
| `v2_ml_governance_record_immutable_delete` | DELETE ON `v2_ml_governance_record` | `V2 ML governance records are immutable; DELETE prohibited` |

(The governance record permits UPDATE **only** through the repository that
simultaneously appends the lifecycle event — enforced by repository design
+ a dedicated test; DELETE is DB-refused. Rationale: the record is a
current-state projection; the event log is the truth. If ITRGA prefers a
DB-level UPDATE guard + insert-new-row versioning instead, the DA flags
this as **FP-1** for the plan review to pin.)

**Permission seeds (revision-local literals; SAL-aligned):**
`admin`: `v2.research.ml_governance.read` (SAL-2),
`v2.research.ml_governance.decide` (SAL-3 — the single decision-writer
gate), `v2.research.signal.read` (SAL-2, seeded here for U-3/U-4 reads),
plus `operator`: both `.read` permissions.
**Expected `v2_permission` total after 0044: 27 + 5 = 32.**

**Data seeds:** none (no fabricated governance state — records are created
only by the governed writer at runtime). **Downgrade:** symmetric — drops
the two tables, three triggers, five permission rows, nothing else.
**Post-unit drift declaration:** `alembic check` at the 0044 head =
**exactly the 9 inherited V1 tokens; zero `v2_*` token** (models registered
in `app/db/models/__init__.py` in the same unit — PG-002 lesson).

### 1.3 U-3 — Migration `20260902_0045_v2_be5_signal_contracts` (exact DDL)

`down_revision = 0044`.

**Table `v2_signal_record`:**

| Column | Type | Constraint |
|---|---|---|
| `id` | String(36) | PK |
| `family` | String(16) | NOT NULL CHECK IN (`structural`,`predictive`) — **separately typed families; no third value** |
| `signal_type` | String(64) | NOT NULL |
| `instrument_id`, `timeframe` | String | NOT NULL |
| `state` | String(16) | NOT NULL CHECK IN (`emitted`,`withheld`,`expired`,`refused`) — **withheld/expired/refused are permanent typed states, never silent drops** |
| `state_reason` | JSON | NOT NULL when state != `emitted` (typed reason contract; enforced by writer + test) |
| `payload` | JSON | NULL when withheld/refused (nothing fabricated); NOT NULL when emitted |
| `uncertainty` | JSON | NOT NULL for `predictive` (interval + calibration ref); structural rows carry `{"basis":"deterministic"}` |
| `limitations` | JSON | NOT NULL (07_ML_SPEC research-integrity: uncertainty, not only point estimates) |
| `source_family_refs` | JSON | NOT NULL — lineage: structural → BE-4 observation ids; predictive → `v2_ml_governance_record` id + dataset/feature/model versions |
| `governance_record_id` | String(36) | NULL for structural; NOT NULL for predictive (a predictive signal without an eligible governance record is REFUSED by the writer) |
| `data_class` | String(32) | NOT NULL (same CHECK as 0044) |
| `as_of`, `expires_at` | DateTime(tz) | NOT NULL / NULL |
| `mode`, `operator_id`, `correlation_id`, `created_at` | | NOT NULL |

**Table `v2_signal_state_event`** — append-only state transitions
(emitted→expired etc.), columns mirroring `v2_ml_lifecycle_event`.

**Guard triggers:** `v2_signal_record_immutable_update/_delete` →
`V2 signal records are immutable; UPDATE prohibited` / `…DELETE
prohibited`; `v2_signal_state_event_immutable_update/_delete` →
`V2 signal state events are immutable; UPDATE prohibited` / `…DELETE
prohibited`. (Signal records are fully immutable — state progression is
event-append + a new projection read, not row mutation.)

**Permission seeds:** `admin`: `v2.research.signal.emit` (SAL-3).
**Expected total after 0045: 33.** Data seeds: none. Downgrade:
symmetric. **Post-unit drift declaration: exactly the 9 inherited
tokens.**

### 1.4 Non-migration units — artifact sets

| Unit | New artifacts (land under) | Versioning |
|---|---|---|
| U-2 | `app/v2/research_governance/{contracts,decisions}.py` (+ tests) | component `ml_governance_engine` = `mge-1.0.0`, hash-pinned in `v2_computation_version` (0044 seeds the row — mirrors plan §1.2 BE-4 pattern) |
| U-4 | `app/v2/research_governance/{signals,api}.py`; router mount (1 additive line in `app/v2/api/router.py`) | component `signal_engine` = `sge-1.0.0` |
| U-5 | `app/v2/research_governance/diagnostics.py` (+ read endpoints) | rides `mge` version |

## Part 2 — Registry evolution contract (§1.2.a)

V1 registries (`model_artifacts`, `dataset_snapshots`, `feature_definitions`,
`experiments`) are **not altered** — the 07_ML_SPEC Model Registry fields
already exist there (id, version, datasets, feature version,
hyperparameters, metrics, status, rollback). BE-5 adds the **governance
overlay** (0044) that V2 requires and V1 lacks: typed statuses, append-only
decision provenance, mode/actor/correlation, and SAL-gated writers.
Versioning contract: `registry_version` on every governance record;
`v2_computation_version` rows for both new engines; any engine change =
new version row + new records (old rows immutable).

## Part 3 — Eligibility / calibration / freshness / economic / rollback contracts (§1.2.b — bound to 07_ML_SPEC)

Each contract is a **pure decision function** over existing V1 evaluator
outputs; report existence is **necessary, never sufficient** — the decision
function checks content against the spec-cited conditions:

| Contract | Governing 07_ML_SPEC section (cited in `decision_basis`) | Decision conditions (pinned at implementation from the spec + V1 service configs) |
|---|---|---|
| Eligibility | *Statistical Validation* + *Deployment Policy* | requires: walk-forward + OOS + bootstrap results present AND significance satisfied AND uncertainty intervals present ("Results shall include uncertainty—not only point estimates"); any missing element ⇒ `ineligible` with typed reason |
| Calibration | *Statistical Validation* (calibration) | requires a `CalibrationService` report within freshness bound; miscalibration threshold from `CalibrationConfig` (pinned constant in the contract, cited to the V1 config value) |
| Freshness | *Drift Monitoring* + *Continuous Learning* | evaluation age vs declared bound; drift report presence; `unknown` is an allowed typed outcome |
| Economic | *Economic Validation* | requires `CostScenario` evaluation under spread/commission/slippage/latency/liquidity; **`economic_status` independent of `statistical_status`** — both reported, never merged |
| Rollback | *Model Registry* ("rollback version") + *Deployment Policy* ("rollback availability") | promotion to `shadow`+ REFUSED unless `rollback_target_version` set and resolvable; `rolled_back` event restores the prior class with full provenance |

Promotion ladder (all transitions events, all audited): `research` →
`shadow` → (`champion` | `challenger`) → `retired`; every step requires
eligibility + calibration + freshness + economic + statistical all in
their passing states **and** the SAL-3 permission **and** RESEARCH mode;
any other path = `refused` event with typed reason. **No promotion by UI
state or manual change is possible: the writer is the only path, and it is
audited** (§1.3 restated in Part 6).

## Part 4 — Shadow / champion / challenger metadata (§1.2.c)

`deployment_class` on the governance record (0044 CHECK) + lifecycle
events carrying from/to. Constraint enforced by writer + test: at most one
`champion` per (`model_type`, `instrument_class`) scope; `challenger`
requires an active `champion` reference in `decision_basis`; `shadow`
carries no serving implication anywhere (research-only band).

## Part 5 — Research reports / diagnostics / evidence artifacts (§1.2.e)

U-5 emits **model diagnostic reports** (eligibility/calibration/economic
summaries with full input refs) as immutable artifact rows reusing the
0043 `v2_market_context_report` architecture: content-hash determinism
anchor, `engine_versions` + hash, audit event
(`research.ml_diagnostics.computed`) + `v2_lineage_record` row
(artifact_type `ml_diagnostic_report`, `input_snapshot_id` = the evaluated
report set hash, `computation_version` = engine versions hash). Storage:
diagnostics land in `v2_market_context_report`? **No** — separate table is
NOT needed either: U-5 stores diagnostics as `v2_ml_lifecycle_event`
`decision_basis` (already immutable + auditable) plus a read-only
**projection endpoint**; no new table. (If the plan review prefers a
dedicated artifact table, the DA flags **FP-2** — one table, same R-2
pattern, added to 0045.)

## Part 6 — Hard boundaries (§1.3, in substance)

1. **No execution authority from any signal.** No signal row, state,
   endpoint, or event grants, triggers, or references any order/execution
   capability. The forbidden-permission-marker guard
   (`V2_FORBIDDEN_PERMISSION_MARKERS`) continues to reject any
   execution-vocabulary permission at import time.
2. **No live strategy authorization.** `deployment_class` values carry no
   serving semantics; `live` never appears in any CHECK vocabulary of this
   band except the data-class taxonomy label (which BE-5 artifacts may not
   carry at first landing — see 7 below).
3. **No performance claim without classification.** Every metric-bearing
   artifact carries `data_class` + mode + validation tier; economic and
   statistical conclusions are separate columns, reported independently.
4. **No promotion by UI state or undocumented manual change.** The single
   SAL-3 writer + DB guards + append-only events are the only mutation
   path; direct SQL is refused by triggers.
5. **No broker/account/order/execution/credential domain touched**
   (BE-8…BE-10). **No external AI** (BE-11). No provider network call in
   any test (socket-guard pattern continues).
6. **RESEARCH mode only** for decisions and emissions (writer-enforced;
   SIMULATION read-back permitted per the platform mode scope); all reads
   read-only; unknown/insufficient is a typed outcome everywhere.
7. **Data honesty (§0.2 + request §1.3):** every BE-5 artifact carries the
   six-value `data_class` tag. **At first landing BE-5 artifacts may
   legitimately contain ONLY `synthetic` and `simulated` classes** (the
   BE-2 simulator basis — pipeline-validation tier). `historical_real` and
   `live` are structurally present in the taxonomy but **unreachable until
   the corpus track lands** (Part 11); the writer refuses them with a typed
   reason until a future governed act unlocks them. **No fabricated
   research results:** no seed data, no synthetic "performance" rows, no
   demo models.

## Part 7 — Mode, audit, security integration (§1.4)

- Every new row carries `mode`, `operator_id`/`actor_id`,
  `correlation_id` per the BE-1 contract; timestamps UTC via the
  established `require_utc`/`_utc_from_store` discipline.
- Audit events (append-oriented, `domain="v2.research_governance"`):
  `ml.governance.registered`, `ml.eligibility.evaluated`,
  `ml.promotion.decided`, `ml.promotion.refused`, `ml.rollback.executed`,
  `signal.emitted`, `signal.withheld`, `signal.refused`,
  `signal.expired`, plus sensitive-read audit on `read_all`-class reads.
- **Credential law: this band prompts for NO credential** — stated
  explicitly here and to be restated in every unit's evidence. Model
  metadata redaction: hyperparameters/paths pass the existing audit
  redaction gate (`app/v2/audit/redaction.py`); artifact paths are
  workspace-relative only; no absolute user paths in logs or artifacts.

## Part 8 — Test plan (§1.5)

Fail-first per unit (each unit's first commit is its failing contract
tests). **Floor: 789 never decreases; projected new floor: 789 + 58 =
847** (budget, itemized):

| Unit | New tests (budget) | Groups |
|---|---|---|
| U-1 | 12 | migration-up content assertions (0043 pattern: upgrade to revision + schema/seed/trigger checks); C-1/C-2/C-3-style guard refusal tests (exact messages); downgrade cycle (content-based; **no position-based assertions** — PGF-012); drift gate; permission totals (27→32) |
| U-2 | 14 | one pass + one typed-refusal test per contract (eligibility/calibration/freshness/economic/rollback); report-existence-insufficient test; economic/statistical independence test; promotion-ladder refusals |
| U-3 | 10 | migration-up; guards (4 messages exact); family CHECK; state CHECK; permission total (33); drift gate; downgrade |
| U-4 | 14 | structural vs predictive emission; predictive-without-eligible-governance refused; withheld/expired/refused permanence (state events, no row mutation); lineage walk (signal → governance → V1 artifact; signal → BE-4 observation); RBAC incl. `denied`; mode enforcement; socket guard; data-class refusal (`historical_real` refused at first landing) |
| U-5 | 6 | diagnostics projection; audit+lineage rows; redaction |
| Regression | 2 | full-suite green; no-touch group (BE-3 provider state + BE-4 report tables byte-identical across 0044/0045) |

Leakage/walk-forward/calibration/economic evidence strategy: BE-5 tests
exercise the **decision contracts** against V1 evaluator outputs computed
on labelled synthetic fixtures — **pipeline-validation tier declared**;
research-validation on real data is out of band (Part 11). No leakage
test can honestly pass on synthetic data as a market claim and none will
be presented as one.

## Part 9 — Evidence plan for ITRGA review (§1.6)

Per unit, content-exact probes the ITRGA can recompute independently
(BE-4 compver-pin pattern):

- **DB probes:** exact `SELECT` of seeds (permission rows with SAL;
  `v2_computation_version` rows with source hashes recomputable from the
  transcript's literal files); trigger name enumeration (expected totals:
  18 → **21** after 0044 → **25** after 0045); guard-refusal probes with
  byte-exact expected messages; CHECK-vocabulary probes.
- **API probes:** endpoint-path pins (Level I executed transcript, BE-4
  RSR-1 format — all six BE-1 states + the typed signal states);
  claim/status field verbatim samples.
- **Run evidence:** raw full-suite `-v` output (RSR-2 format) with the
  itemized delta vs 789.
- **DR mapping:** requirement→evidence table (this checklist §1.1–§1.9,
  item-for-item), plus REM-001 literal transcript of every changed file,
  hash manifest, credential scan, and drift direct-run output per
  migration unit.

## Part 10 — Register impacts (§1.7)

| Register | Change |
|---|---|
| Capability maturity | `ML Research Expansion`: DESIGNED → **IMPLEMENTED** at U-2 closure, **COMPLETE** at band determination; `Signal Architecture V2`: DESIGNED → **IMPLEMENTED** at U-4, **COMPLETE** at determination — evidence type: executed tests + Level I API transcript per unit |
| Risk register | add: signal-truthfulness-on-synthetic-data risk (mitigated by data_class refusals + tier declaration); governance-writer-bypass risk (mitigated by triggers + single-writer + audit) |
| Tech debt | add: `historical_real`/`live` data classes structurally present but unreachable (deliberate, corpus-gated); diagnostics-as-events (if FP-2 resolves to no-table) |
| `V2_CURRENT_STATE.md` | version bumps per unit; test floor 789→847 projection; head 0043→0045 (DA test chains only — **working-DB application of 0044/0045 is a separate sanctioned act** per the 0043 precedent) |

## Part 11 — Boundaries vs neighbours (§1.8)

| Stays OUT of BE-5 | Belongs to | Why |
|---|---|---|
| Portfolio/risk aggregation over signals | BE-6 | different domain; BE-5 emits signals, never aggregates exposure |
| Backtesting engine, historical replay, scheduled jobs | BE-7 | BE-5 consumes V1 evaluator outputs; running new backtests is BE-7's engine work |
| Real historical data acquisition/corpus | **B-01/B-02 corpus track** (V1-era data foundation) | **Signal truthfulness depends on honest data.** Items that cannot be honestly evidenced without the corpus: real-data leakage/walk-forward claims, `historical_real` governance statuses, any economic conclusion presented as market-valid. **Deferral mechanics:** the taxonomy carries the classes; the writers refuse them with typed reasons; the tier declaration marks every BE-5 artifact pipeline-validation; unlocking is a future governed act after the corpus track — nothing is silently mislabelled |
| Signal serving to UI, alerting | FE bands / X-01 | sequencing directive |
| Model serving/inference infrastructure | BE-11 territory + deployment | research-only band |

## Part 12 — Package size / review volume (§1.9)

Projected: 2 migrations (~250 lines each) · ~6 new modules (~1,600 lines)
· ~5 model classes · ~58 tests (~2,200 lines) · 3 modified files
(router mount, models `__init__`, `rbac/permissions.py` — the exact
BE-4 OBS-1 set, enumerated here up front per the ITRGA process note) ·
source transcript ~150 KB · API + test-run transcripts ~90 KB · DR ~14 KB.
Review loop: the DA proposes unit-by-unit delivery (U-1+U-2 first
package, U-3+U-4 second, U-5+U-6 third) or a single band package — the
Operator/ITRGA choose; evidence discipline is identical either way.

## Part 13 — Known limitations / open items (honest)

- **FP-1** (Part 1.2): governance-record UPDATE mechanics — repository-
  gated UPDATE + DELETE trigger (proposed) vs full immutability with
  row-versioning. Plan review pins it.
- **FP-2** (Part 5): diagnostics as lifecycle-event payloads (proposed) vs
  a dedicated artifact table. Plan review pins it.
- Decision-contract threshold constants (calibration bound, freshness
  bound) will be pinned at implementation **from the V1 service configs
  with citations**; the plan deliberately does not invent numbers here.
- All BE-5 evidence is pipeline-validation tier; **no market conclusion
  will be claimed or claimable** — "BE-5 governance decides correctly on
  real models" remains NOT PROVEN until the corpus track exists.
- Working-DB application of 0044/0045 is out of scope (separate sanctioned
  acts per the 0043 pattern).
- OBS-9 (BE-4 record) remains the Operator's administrative item;
  unaffected by this band.

---

*We don't guess. We prove.*
**— Development Authority, 2026-09-02**
**End of AXIOM-V2-BE-5-DA-PLAN-001 v1.0.0**
