# ITRGA-PRV-V2-BE-7-PLAN-001 — Full-depth plan review, Band BE-7

| Item | Value |
|---|---|
| Document Id | **ITRGA-PRV-V2-BE-7-PLAN-001** |
| Date | 2026-09-03 (ITRGA) |
| Artifact under review | `AXIOM-V2-BE-7-DA-PLAN-001` v1.0.0 (received via the Operator custody channel; 362 lines, 21,753 B; MD5 `52293c345d759e090383bbe1f7076ad6`; SHA-256 `e53799d46bbec834ed8b5dd3ff7b25da2507b326d3a75c174093dbf35f0f72e2`) |
| Authority | `ITRGA-CN-V2-BE-7-001` (Operator BE-7 authorization, 2026-09-03) |
| Review contract | `ITRGA-REQ-V2-BE-7-PLAN-001` (REQ-1.1…1.13; Pins P-1…P-10; roadmap §0 verbatim contract) |

## Verdict

**ACCEPTED — zero corrections.** The plan answers every REQ item in map order, honours all ten pins, adopts the roadmap §0 contract verbatim, declares its own open flag honestly (FP-1 — resolved in §5.1), and survives independent corroboration of every claim it makes about existing state (§4). Two conditions and four observations (§5) are **Build-Order bindings**, not plan defects; no re-issue of the plan is required. The verdict frees **BO-V2-BE-7-001** under the standing commissioning authorization.

## 1. REQ compliance map (contract §1.1–§1.13)

| REQ | Plan part | Verdict |
|---|---|---|
| 1.1 Decomposition / migration arithmetic | Part 1 (U-1…U-6; 0047 with `down_revision="20260903_0046"`; exact DDL; 10 guards; 8+2 seeds; totals 32→42 / 41→49 / 6→8; drift declaration; symmetric downgrade) | **COMPLIANT** |
| 1.2 Replay with as-of boundaries | Part 2 (`as_of ≥ window_end`; only-bar-source BE-2; cursor cutoff; pure determinism; pinned seed rule; `replay_of`) | **COMPLIANT** |
| 1.3 Input/version registration | Part 3 + T1 (content-hash dedupe with typed `reused`; `record_seq`/`supersedes`; durable C-1-law refusals) | **COMPLIANT** |
| 1.4 Cost-model configuration | Part 4 + T2 (`{value,unit,citation}` per parameter; V1 vocabulary citations; pure `apply_costs`; per-result generation reference) | **COMPLIANT** |
| 1.5 Temporal-leakage structural | Part 5 (G-1…G-5: named code paths **and** the five future-leakage tests — exit-evidence item i) | **COMPLIANT** |
| 1.6 Strategy lifecycle | Part 6 + T3 (typed-permanent `draft/registered/retired`; only registered-current jobable; structural absence of execution fields) | **COMPLIANT** |
| 1.7 Job queue | Part 7 + T4/T4b (DB-backed decision **justified** as the contract demanded; manual tick v1; `UNIQUE(job_id, attempt_index)` idempotency anchor; typed cancel; audit-mirrored transitions) | **COMPLIANT** (architecture row 89 decision delivered) |
| 1.8 Typed result classes | Part 8 + T5 (CHECK admits only `backtest`/`simulation`; `paper`/`live` schema-impossible + typed refusals at construction points) | **COMPLIANT** |
| 1.9 Determinism anchors | Part 9 + T5 (anchor triple; `engine_versions`(+hash, OBS-3-law canonical serialization); compver per engine; C-2 disclosure) | **COMPLIANT** |
| 1.10 Job-silence structural | Part 10 (writable-table allow-list asserted by test; import/dependency scan; no tick source in v1) | **COMPLIANT** — token-set condition §5.4 |
| 1.11 Mode/audit/security | Part 11 (BE-1 columns; full audit inventory incl. refusal events; lineage rows; RBAC; redaction untouched; no credentials — stated) | **COMPLIANT** |
| 1.12 Data honesty | Part 12 (6-class on all five tables; first landing synthetic/simulated; mandatory `performance_disclaimer`; V2-TD-18 continuity) | **COMPLIANT** |
| 1.13 Test plan + annex | Part 13 (fail-first; budgets 12/15/10/15/6/2 = 60 → floor **≥ 971**; the five exit-evidence items each owned by named tests; no-live-effect scan methodology four-part declared; **worked-sample annex** hand-replayable without the engine) | **COMPLIANT** |
| Boundaries | Part 14 (BE-8…BE-10 / BE-11 / corpus / production scheduler / FE / preview-export — all excluded; V1 lineage read-only) | **COMPLIANT** |
| Honest limitations | Part 15 (FP-1 flagged for the review; scheduler debt; rule-function-only strategies; pipeline-validation tier; 0047 as separate sanctioned act) | **COMPLIANT** |

Reading-map audit: the plan's stated map (REQ→Part) **matches the actual content** of every Part; §0 is the REQ §0 verbatim contract adopted by reference — sound.

## 2. Pins map

P-1…P-7 carried and located: P-1/P-2/P-4/P-6/P-7 in §1.2/Parts 8–9/13; P-3/P-5 in Parts 11–12 and the refusal/guard inventories. New pins structurally placed as declared: **P-8** = Part 5 (five named guards with named code paths + probe tests); **P-9** = T5 CHECK + Part 8 construction points + Part 13 scan; **P-10** = T4b attempt ledger + Part 7 retry economics + Part 10 allow-list.

## 3. Arithmetic audit (independent)

Guards +10 ⇒ triggers **32 → 42** ✓. Seeds +8 ⇒ permissions **41 → 49** ✓. compver +2 ⇒ **6 → 8** ✓. Tests +60 (12+15+10+15+6+2) ⇒ floor **911 → ≥ 971** ✓. Chain literals (`20260903_0046` / `0047`) ✓.

## 4. Independent corroboration record (this session, against the repository floor)

| Claim | ITRGA verification | Result |
|---|---|---|
| V1 file pins §1.0 (6 files, sha256-16) | recomputed on the repository: `7dbc665dc4b43f31` / `e893b92c6ccce188` / `b08ef4b1dec07567` / `6c5d72a8942050b4` / `f163e610ba1a6215` / `c49527ed12f4d2ca` | **6/6 BYTE-EXACT** |
| Cited classes exist (`ChronologyGuard`, `validate_temporal_split`, `TemporalSplitEngine/Config`, `ReproducibleSnapshotBuilder`, `DatasetService`, `DeterministicSimulatedFillModel`, `SimulatedExecutionService`, `CostInput`, `CostScenario`) | greps | **ALL PRESENT** |
| BE-2 `V2MdBarReadBoundary` as bar source with no-future enforcement | `app/v2/marketdata/api/reads.py` (boundary class in reads+writers; `as_of may not be in the future` raise; UTC-required) | **VERIFIED** |
| Import-scan surfaces | `app/market/`, `app/api/routes/` exist; additional execution-suggestive module `app/trading_intelligence/` exists (§5.4 condition) | **VERIFIED + condition** |
| New-object collision census (6 table names, 6 `uq_v2_*` tokens) | grep over `alembic/versions` + `app/` | **ZERO COLLISIONS** |
| Permission namespace | `v2.research.jobs/registry/results.*` absent from the 41-row census; BE-4 family tokens (`v2.research.market_context.*`, `v2.research.chart_intelligence*`) are non-colliding relatives | **CLEAN** |
| "O-3 posture" (correlation_id nullable/writer-minted) | `ITRGA-DET-V2-BE-5-FINAL-001` §O-3 documents the accepted deviation verbatim | **ACCURATE CITATION** |

## 5. Review findings

### 5.1 FP-1 (plan-flagged; the review pins it) — RESOLVED AS PROPOSED, with BO-binding conditions

The `v2_research_job` mutable-row-with-immutable-ledger model is **accepted** over the fully-versioned alternative: the job row is operational queue state, not an institutional artifact; instantiating "no silent mutation" requires only that no transition is silent — which the design guarantees via the immutable attempt ledger plus audit per transition. Fully-versioned job rows were weighed and rejected: queue reads would require generation-walks for a fact the ledger already preserves immutably. Conditions (Build Order must encode):

- **C1** submission-time fields (`owner`, `authorization_ref`, `inputs`, `schedule`) are **write-once**: no writer path updates them after INSERT; a test asserts this.
- **C2** the mutable column set on `v2_research_job` is exactly `{job_state, attempt_count, output_ref, failure}` (the Part 10.1 allow-list constant names exactly this UPDATE set; asserted by test).
- **C3** a job transition exists only via the governed runner/submit/cancel surfaces — **no generic job-update endpoint** (U-5 test asserted); every transition mints its attempt-ledger row and audit event.
- **C4** the U-5 submit writer refuses `schedule.kind != "manual"` with a typed, durably-audited refusal (v1 scope per Part 7).

### 5.2 OBS-1 (non-blocking): T1 `registration_outcome` column

Stored rows can only ever carry `'registered'` (reused/refused outcomes live in audit + response by design). The closed CHECK set is harmless; keep it, and the DR should state the column's stored-range reality in one line.

### 5.3 OBS-2 (non-blocking): job-level `inputs JSON` lineage

Job rows reference registry/strategy/cost inputs as a JSON id-array while result rows carry the lineage triple as columns. v2-consistent (0046 pattern); fine — the API walk (Part 13, exit item iv) demonstrates it.

### 5.4 OBS-3 (non-blocking disclosure supplement; BO-binding on the scan): leakage-law scope

The as-of law is open_time-based (explicit). **Ingest-lag** (a bar inside the window ingested only after `as_of`) is controlled not by the as-of filter but by the G-5 content-hash re-verification at replay time — refusal, never silent inclusion. Acceptable and honest for the band's data classes; the corpus track will revisit publication-lag explicitly. Separately, the Part 10.2 import scan names two paths; its **token predicate must include `trading_intelligence` (and any `*adapter*` module) alongside execution/broker/order** so the scan cannot miss by path enumeration (BO-binding; same scan class as BE-3 P1's forbidden-import test).

## 6. Sequencing

Verdict frees **BO-V2-BE-7-001** under `ITRGA-CN-V2-BE-7-001`; the §5.1/§5.4 conditions enter the BO as bindings. The working-DB application of migration `0047` remains a separate sanctioned act at chain end (instrument lineage per 0043/0045/0046, E-0046-DUP startup rule inherited).

— ITRGA, 2026-09-03
