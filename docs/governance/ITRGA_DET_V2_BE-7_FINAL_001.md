# ITRGA FINAL DETERMINATION — BE-7 FULL-DEPTH SOURCE REVIEW
# ITRGA-DET-V2-BE-7-FINAL-001 · v1.0.0 · 2026-09-04 · AXIOM Trading Terminal v2.0
# Band: BE-7 (Backtesting, Simulation, Replay, and Governed Research Jobs)
# Reviewed: AXIOM-V2-BE-7-DR-001 + full 17-file source transcript (hash-locked, §2)
# Chain: CN-V2-BE-7-001 → REQ-V2-BE-7-PLAN-001 → PRV (ACCEPTED) → BO-V2-BE-7-001
#        → DR → INT-V2-BE-7-DR-001 (PASS) → DA-INT-ACK-001 → THIS FINAL DETERMINATION
# Office: ITRGA · review depth: full source (every line of all 17 delivered files read
#         and checked against BO-V2-BE-7-001 T-1…T-14, Pins P-1…P-10, C1–C4,
#         and the scan-token condition)

---

## §0 — Verdict

**DETERMINATION: ACCEPTED WITH CORRECTIONS — correction cycle CR-V2-BE-7-001 required before band acceptance.**

The delivery is substantively complete and of high governance quality: all 17 files were read in full; 13 of 14 terminal-state items are proven at depth by the delivered evidence; the sixty new tests are real tests against independent literals, not echoes. **Two corrections are required** (F-1: a lawful-path untyped failure; F-2: an evidence-pin shortfall), both small, bounded, and test-visible. Neither touches determinism, leakage law, custody, or schema. Three informational observations are carried forward (OBS-A/B/C/D).

**Acceptance is conditional on:** delivery of the CR-V2-BE-7-001 correction pack (§5), its targeted re-verification by this office, and updated evidence. **The 0047 working-DB application remains un-authorized until THEN and remains a separate sanctioned act even after acceptance** (chain-end instrument act; E-0046-DUP startup-hygiene law inherited).

## §1 — Material reviewed and method

All 17 manifest files were extracted with per-file SHA-256 re-verification against the manifest (17/17 byte-exact), then read line-by-line:

- U-1: `app/db/models/v2_research_jobs.py` (214 ln) · migration `20260903_0047_v2_be7_research_jobs.py` (390 ln)
- U-2: `contracts.py` (70) · `leakage.py` (125) · `replay.py` (169)
- U-3: `registry.py` (218) — merged U-3 scope (OBS-A)
- U-4: `queue.py` (170) · `runner.py` (233) · `__init__.py` (9)
- U-5: `api.py` (355)
- U-6: `test_v2_be7_replay.py` (17 items) · `test_v2_be7_migration.py` (11 items: 10 defs, drift parametrized ×2 revs) · `test_v2_be7_jobs.py` (25) · `test_v2_be7_boundaries.py` (7)
- Modified (additive-only vs floor, **+6/−0, +55/−0, +31/−0** — difflib-verified): `v2/api/router.py`, `v2/rbac/permissions.py`, `db/models/__init__.py`

Evidence transcripts were consumed as corroboration (INT-3/INT-4 already verified independently); where source and evidence could disagree, source-level live tests were weighed heavier (they *execute* the claims on tmp-chain databases built from the real migration files).

## §2 — Hash-lock of the reviewed material

Reviewed bytes were re-hashed from the SOURCE_TRANSCRIPT at extraction (17/17 match declared full SHA-256), the four artifact hashes match DR §5 (INT-1 record), and the DA independently re-executed INT-6's rolling-hash recipe on its disk state, reproducing RPE `1499343d48b778af17065e8bf1eaabcffc116880fa6967ab442db1255992b178` and RJE `f01e3041a060e96cfcdcc9650d2458f84512e2d1bb2e2509fe668a9d3704ed7c` — a three-way agreement (transcript literals ≡ ITRGA replication ≡ DA disk). The line-count convention note on DR §5 (122 vs 123, final-line handling) is recorded and closed; hashes byte-match, nothing to chase.

## §3 — Terminal-state ledger (T-1…T-14)

**T-1 ✔ PROVEN.** `revision="20260903_0047"`, `down_revision="20260903_0046"`, single head; `alembic current → 20260903_0047 (head)` (API transcript §5); `test_0047_downgrade_cycle_content_based` + `no_touch_protected_state` prove symmetric upgrade/downgrade **content-based** (not row-count-based): permission tokens deleted by exact `:p` bind, compver rows deleted scoped `component+version`, compver delete-guard dropped/recreated with count-assertion fail-closed, six indexes dropped then six tables in reverse dependency order.

**T-2 ✔ PROVEN.** All six tables with exact plan §1.2 DDL; model↔migration parity verified column-by-column (sets, types, nullability): `v2_backtest_input` (uq `input_id,record_seq` + uq `content_hash`, closed registration-outcome CHECK), `v2_cost_model`, `v2_strategy_version` (closed lifecycle CHECK), `v2_research_job` (closed job-state CHECK; sole-mutable), `v2_research_job_attempt` (uq `(job_id,attempt_index)`, closed outcome CHECK; the BE-1-column variance — `actor_id` instead of the data_class set — is deliberate and plan-consistent), `v2_research_result` (`result_class ∈ ('backtest','simulation')` closed CHECK — `paper`/`live` **schema-impossible**; uq determinism anchor; `replay_of`; `time_basis`). 6-class `data_class` literal identical across tables and to the prior-band lineage. Nothing beyond the enumerated columns.

**T-3 ✔ PROVEN.** `_TRIGGERS` tuple: ten entries, five pairs, exact BO-quoted messages on the sqlite dialect of record; `v2_research_job` absent from the guard set **by design** (FP-1). Live-proof: `test_0047_guard_messages_verbatim_registries` and `…_ledger_results` execute raw UPDATE/DELETE against every guarded table and assert the exception string **equals an independent test-local literal** — the ITRGA passed this literal through `ast.literal_eval` and byte-compared all 10 against the BO T-3 form: **10/10 exact**. Census asserted 32 (pre) → 42 (post) as a **set difference equal to exactly the ten names**. (OBS-C notes the postgresql form's parametrized-generic message, household pattern since 0044.)

**T-4 ✔ PROVEN.** Eight seed rows with exact tokens: `v2.research.{jobs.read, jobs.submit, jobs.cancel, registry.read, registry.write, results.read}` admin (SAL-2 reads / SAL-3 writers) + `jobs.read`/`results.read` operator (SAL-2); the seed skips already-existing `(role, permission)` pairs — **no deleted-reinsertion**; totals asserted `== 49` plus distinctness and subset assertions in the migration test; the `V2_FORBIDDEN_PERMISSION_MARKERS` guard remains in force (present in the cumulative `permissions.py`, additive-diff clean).

**T-5 ✔ PROVEN.** compver 6→8 asserted with `(replay_engine, rpe-1.0.0, 64)` and `(research_job_engine, rje-1.0.0, 64)` rows; recipe `_rolling_hash` replicated by ITRGA from transcript literals and independently re-executed by the DA on disk — three-way agreement (§2). `evidence_ref="BO-V2-BE-7-001"` on both seeds.

**T-6 ✔ PROVEN.** pytest-side `test_drift_gate` parametrized over `[REV_0046, REV_0047]` (both heads, PGF-014 law) **and** the API transcript carries direct runs at both heads: non-head clean (revision-offset refusal form, no BE-7 tokens), head = **9 distinct inherited tokens, zero BE-7 tokens, DRIFT GATE: PASS**, format-independent census.

**T-7 ✔ PROVEN.** `no_touch_protected_state` upgrades a 0046-chain tmp DB and asserts: provider-table content byte-identical pre/post; compver prior rows byte-identical pre/post (engine rows excluded from the comparand, so only prior components); trigger delta == exactly the 10 names. `test_regression_v1_reuse_pins_unchanged` **re-hashes the six pinned V1 files live at test time** against hard sha-16 pins (prefixes of the full attestations the ITRGA byte-verified at INT-2). `test_regression_prior_band_contracts_untouched` asserts BE-4/5/6 contract vocabularies by content (incl. `PORTFOLIO_BASES == ("hypothetical",)`).

**T-8 ✔ PROVEN** (six states + every enumerated refusal scenario live-tested): succeeded (`submit_run_succeed_full_lineage` — full lineage), failed (leakage-typed; lineage-resolution), cancelled + terminal-cancel-refused (`cancel_queued_then_terminal_refusal`), denied-by-RBAC (`rbac_denied_and_reads`: operator 403 generic `"Permission denied"` on all writer probes; 401 unauthenticated), plus queued→running transition visibility. Refusal inventory: `paper`/`live` schema-impossible (migration CHECK test inserts raw `paper` and asserts DB-level refusal) **and** writer-typed at the run construction point (verbatim `ResultClassRefused` message observed live in the API transcript == contracts source); C4 non-manual typed+audited (`submit_nonmanual_schedule_refused_c4`, refusal note "C4 — v1 scope is manual invocation only" == queue.py source == transcript body); G-3 horizon-past-embargo (`g3_horizon_past_embargo_refused` + `g3_boundary_exactness`); non-registered-current strategy (draft refused; superseded generation refused — the current-generation check is newest-record_seq equality, correct); missing `authorization_ref`; G-5 content-hash mismatch end-to-end through the API (`leakage_refusal_fails_job_typed`: tamper + typed `failed` + `G-5` in reasons). `performance_disclaimer` is unconditionally embedded by the engine in every result summary ("pipeline-validation tier on labelled synthetic input; NOT live or future performance; no market conclusion") and surfaces verbatim in the results read; API ASSERT 68 confirms presence on response.

**T-9 ⚠ PROVEN WITH ONE PIN SHORTFALL (F-2).** G-1 (two tests incl. planted-future-bar summary invariance and the as_of-before-end window refusal), G-2 cursor-slice adversarial test, G-3 (refusal + legal-horizon pass), G-4 corrupted-ledger refusal, G-5 (unit + through-API) — all five guard families transcript-visible ✔ (exit item i). Cost-application purity + sidedness ✔. Anchor input-sensitivity + canonical engine-hash tests ✔. ANNEX-R: fill count/sides, effective prices exact, summary exact — and the ITRGA independently recomputed the annex from pins alone at INT-5: **9,910.55 / 10,010.55 reproduced exactly**. **SHORTFALL:** `test_annex_deterministic_byte_identical` executes the annex **twice** (`s1 == s2`); BO T-9 pins the evidence as **retry ×3 byte-identical**. Correction F-2 (§4).

**T-10 ✔ PROVEN.** Pre-compute anchor lookup: a retried identical attempt finds the existing artifact, sets `succeeded` + `output_ref`, mints a ledger row (`idempotent_reuse`, anchor named), audits `result.reused` — no second artifact (API transcript: same id, count 1); `rerun_succeeded_job_returns_existing` ✔. Typed cancel incl. terminal refusal with durable `job.cancel.refused` audit ✔. Failure typed on every governed failure path (lineage resolution, result-class construction, LeakageRefused) with ledger row + `job.failed` audit ✔ — **with the F-1 exception (§4)** on the unknown-cost-unit path. Attempt ledger append-only (guarded table + sequential `attempt_index`); every governed transition mirrored by ledger + audit (13-event inventory transcript-proven, source-verified). The BO's "duplicate-submit race" is answered by construction + the idempotency suite: two submissions are lawful distinct jobs; identical determinism anchors converge on one artifact (SQLite single-writer; no literal concurrent test exists — noted as the design-level answer, acceptable).

**T-11 ✔ PROVEN.** Writable-table allow-list asserted at constants level **and** at `WRITABLE_TABLES` exactly ({result, attempt, audit, lineage} ∪ {job}); `JOB_UPDATE_COLUMNS == JOB_MUTABLE_COLUMNS == {job_state, attempt_count, output_ref, failure}` asserted (C2); C1 proven behaviorally (write-once snapshot invariant across a state-moving run, both halves asserted). Import-scan test walks the module graph with banned tokens `("execution","broker","order","adapter","trading_intelligence","market.live","app.market","paper","live_service")` and exactly one name-scoped exception `("execution_research",)` — the declared V1 read-only lineage name ✔ (scan-token condition MET). Construction-token scan + API-surface enumeration with no execution vocabulary ✔. Lineage walk: `submit_run_succeed_full_lineage` + `anchor_inputs_hash_sensitivity` ✔.

**T-12 ✔ PROVEN (one evidence-form observation).** Level I transcript 9/9 ASSERTs, path pinned `/api/v1/v2/research-jobs/*`; raw `-v` 971/0 in 499.11s with 17/11/25/7 module accounting math-checking to 911+60; socket guard autouse in the replay module and deny-fixtures elsewhere; REM-001 full-hash manifest re-verified by this office. Fail-first: attested by construction (engine-unit tests import the not-yet-existing module — authoring order documented in DR §4; module-import failure precedes engine availability); a dedicated failing-run transcript would be a stronger artifact — registered as **OBS-E**, non-blocking, consistent with the household form accepted since BE-4.

**T-13 ✔ STAGED.** DR §6 supplies the staged register content (capability rows → IMPLEMENTED at delivery; +3 debt rows: scheduler tick source v2-scope, arbitrary-strategy sandboxing, open_time-as-of/ingest-lag disclosure). Register mutation itself remains DA-side at acceptance per the operator's correction of record; the staged content is complete and honest.

**T-14 ✔ HONORED.** No Git operations anywhere in the delivery chain; zero credential material in all 17 files (scan CLEAN — the two fixture hits are synthetic test-auth constants, the household form for RBAC testing through the real login path); full-depth review executed; corrections issued below for DA answer.

## §4 — Findings (corrections and observations)

### F-1 — CORRECTION REQUIRED · typed-failure law breach on a lawful path (cost-unit vocabulary)
**Where:** `registry.register_cost_model` validates *presence* of `{value, unit, citation}` per component but not the unit vocabulary; `replay.apply_costs` raises a bare `ValueError` for any unit other than `'price'`/`'fraction'`; neither `runner.run_job` nor `api_run_job` catches it.
**Effect:** an operator can lawfully register a cost model with `unit: "bogus"`, submit, and run — the job then dies as an **untyped HTTP 500** with session rollback: no typed failure, no attempt-ledger row, no `job.failed` audit. This breaches the band's typed-permanent-failure law (P-5, T-10 "failure typed") on an operator-reachable path. The DB remains consistent (rollback) — severity minor-structural, not a leakage/determinism/custody defect.
**Required correction (behavioral contract, DA owns the code):** (a) registration-time vocabulary gate — `register_cost_model` refuses any component whose `unit ∉ ('price','fraction')`, typed with reasons, durably audited via the existing `cost_model.refused` path (commit-before-return, C-1 law); (b) regression test in `test_v2_be7_jobs.py`: register with a bogus unit → outcome refused + durable audit present + no row written; (c) optional defense-in-depth: catch `ValueError` in `run_job` into the existing `_fail` typed path. Runner/API commit law unchanged.

### F-2 — CORRECTION REQUIRED · determinism evidence pin (×3, not ×2)
`test_annex_deterministic_byte_identical` runs the annex twice; BO T-9 pins retry **×3** byte-identical summaries. Required: three executions with pairwise/total equality (`s1 == s2 == s3`); no production-code change.

### OBS-A (carried from INT; depth-verified, closes on CR-pack DR editorial)
U-3 delivered as merged `registry.py` — ITRGA verified the ACK §3 line-map exactly (`register_input@42`, `register_cost_model@110`, `register_strategy@162`) and all claimed tests exist and assert the claimed laws. The missing DR §7 disclosure must land in the DR **v1.0.1** editorial revision riding the CR-pack (DA proposed exactly this; accepted).

### OBS-B (carried from INT; CLOSED)
`_RPE_FILES` includes `__init__.py` (fail-loud export-surface pinning; disclosed by the migration literal itself). No action.

### OBS-C (new; informational)
postgresql trigger messages are parametrized-generic (`…% prohibited on %`) via the household shared-function pattern — T-3's verbatim literals bind the sqlite dialect of record, which the tests prove. No action; a future postgresql deployment should revisit message parity.

### OBS-D (new; informational · operator guidance)
Registration path honours `bar_limit` (default 500); `api_run_job` re-fetches with a hardcoded `limit=1000`. On a corpora denser than the register-time limit inside one window, re-fetch can assemble a larger set → G-5 typed refusal (fail-**closed** direction — safe). Operator guidance for the working corpus: register with `bar_limit=1000` to mirror. No code action required.

### OBS-E (new; informational · evidence form)
Fail-first is attested by import-order construction (module-level imports of the not-yet-built units) rather than a shipped failing-run transcript; consistent with the household form since BE-4. A failing-run transcript is welcome as a fortifying artifact in future bands but is not required.

## §5 — Correction cycle CR-V2-BE-7-001 (protocol)

1. **DA** delivers a **bounded correction pack**: (i) `registry.py` F-1 gate; (ii) new F-1 regression test; (iii) F-2 ×3 assertion; (iv) revised `DELIVERY_REPORT_V2_BE-7.md` → **v1.0.1** carrying the OBS-A disclosure + the CR-cycle §0 revision note + re-hashed §5 table; (v) delta testrun transcript segment showing the two new/updated tests passing (targeted `-v` run is sufficient; a full re-run is welcome but not mandated given the package's hash discipline).
2. **ITRGA** performs **targeted re-verification** (intake-lite): hash-pin the changed files against a declared manifest, re-review ONLY the diff surface + the two test bodies, re-run the acceptance checklist for F-1/F-2, then issue the **ACCEPTANCE instrument** (ITRGA-ACC-V2-BE-7-001) which sets band acceptance and stages register sync.
3. **Only after acceptance** may the chain's terminal act proceed: the **0047 working-DB application instrument** (separate sanctioned act; startup-hygiene per E-0046-DUP law: refuse-if-PASS-marker; transcript-witnessed; compver re-pin per C-2 disclosure).

## §6 — Disposition

Band BE-7 delivery **AXIOM-V2-BE-7-DR-001: ACCEPTED WITH CORRECTIONS.** The corpus stands on its evidence: immutability proven live against independent literals, leakage guards proven structurally and adversarially, determinism anchored and independently recomputed, idempotency proven behaviorally and structurally, surface minimal and uniformly governed, V1 floor byte-preserved. F-2 is evidence hygiene; F-1 is a genuine but small breach of the band's own typed-failure law on a lawful path — both well inside a bounded correction cycle.

— ITRGA-DET-V2-BE-7-FINAL-001 · v1.0.0 · 2026-09-04 (Africa/Nairobi) · **We don't guess. We prove.**
