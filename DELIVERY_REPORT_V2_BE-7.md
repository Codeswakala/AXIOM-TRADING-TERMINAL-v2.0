# DELIVERY REPORT — AXIOM V2 BE-7: Backtesting, Simulation, Replay, and Governed Research Jobs

| Field | Value |
|---|---|
| Document ID | AXIOM-V2-BE-7-DR-001 |
| Version | **1.0.1** (CR-V2-BE-7-001 revision — see §0) |
| Build Order | BO-V2-BE-7-001 |
| Governing plan | AXIOM-V2-BE-7-DA-PLAN-001 v1.0.0 (ACCEPTED zero corrections — ITRGA-PRV-V2-BE-7-PLAN-001) + conditions C1–C4 + the scan-token condition |
| Review contract | ITRGA-REQ-V2-BE-7-PLAN-001 §1.1–§1.13 · Pins P-1…P-10 · roadmap §0 |
| Date | 2026-09-04 (v1.0.0: 2026-09-03) |
| Author | Development Authority (DA) |
| Status | **CORRECTION PACK CR-V2-BE-7-001 SUBMITTED — awaiting ITRGA targeted re-verification** |
| Baseline in | head `20260903_0046` · 911 tests · triggers 32 · permissions 41 · compver 6 |
| Baseline out | migration `20260903_0047` (**DA test chains only** — working-DB application separate) · **972 tests** (971 + 1 F-1 regression) · triggers **42** · permissions **49** · compver **8** — all pins hit exactly |

**Standing discipline: we don't guess. We prove.**

## §0 — Revision note (v1.0.0 → v1.0.1, CR-V2-BE-7-001)

Issued per `ITRGA-DET-V2-BE-7-FINAL-001` (ACCEPTED WITH CORRECTIONS).
Changes in this revision:

1. **F-1 correction implemented** — cost-unit vocabulary typed at
   registration: `COST_UNITS_V1 = ('price','fraction')` added to
   `contracts.py`; `register_cost_model` refuses any component whose
   `unit ∉ COST_UNITS_V1` (typed reasons incl. the allowed set, durable
   `cost_model.refused` audit via the existing C-1 commit-before-return
   path, no row written); defense-in-depth per FINAL §4 F-1(c):
   `runner.run_job` catches engine `ValueError` into the existing `_fail`
   typed path (`engine_vocabulary` failing class, ledger row + `job.failed`
   audit) — an unknown unit can no longer surface as an untyped 500 on any
   path. Regression test `test_cost_model_unknown_unit_refused_f1` added
   (refused + reasons + no-row + durable audit asserted). Suite floor
   moves 971 → **972**.
2. **F-2 correction implemented** — `test_annex_deterministic_byte_identical`
   now executes the annex **three** times and asserts `s1 == s2 == s3`
   (BO T-9 ×3 pin). No production-code change.
3. **OBS-A disclosure (the §7 omission, now §7 item 7)** — plan U-3 named
   `app/v2/research_jobs/{registry,costs,strategy}.py`; the delivery
   implements all three U-3 scopes in the single module `registry.py`
   (packaging merge only; no scope change; compver file sets unaffected).
4. **Compver disclosure (C-2 law)** — `runner.py` ∈ `_RJE_FILES`, so the
   apply-time RJE hash moves with this correction: new value
   `8f107d174e081dc0a1527fea841b89dfb73744e3f16eba2d29c60521158c0598`
   (was `f01e3041a060e96cfcdcc9650d2458f84512e2d1bb2e2509fe668a9d3704ed7c`).
   RPE unchanged:
   `1499343d48b778af17065e8bf1eaabcffc116880fa6967ab442db1255992b178`.
   The 0047 application act pins the NEW RJE value.
5. §5 evidence table extended with the CR-pack artifacts; test accounting
   updated (26 jobs-module tests; totals 61 new / 972 suite).

No other section of v1.0.0 is altered in substance; original evidence
artifacts remain byte-frozen and on the record.

---

## 1. Executive Summary

Band BE-7 implemented in full: six units, T-1…T-14 satisfied with executed
evidence, Pins P-1…P-10 honored, conditions C1–C4 + the scan-token
condition encoded and test-asserted. **971 executed, 971 passed, 0
failed** = 911 + **60 new tests** (the exact plan budget). Zero V1 diffs
(six reused files re-hash-asserted **inside the suite**); BE-2…BE-6
protected state proven untouched; zero network attempts; **no credential
prompted for or used anywhere**.

**Tier declaration:** every result carries the mandatory
`performance_disclaimer`; all evidence pipeline-validation on labelled
synthetic input; **no backtest/simulation result is or can be presented as
live or future performance** (structural: NOT-NULL contract + Level I
sample).

## 2. Terminal-state contract T-1…T-14 (item-for-item)

| T | Evidence (executed) |
|---|---|
| T-1 | `20260903_0047 (head)` single head (API transcript §5); literal-revision upgrades; symmetric downgrade proven (`test_downgrade_cycle_content_based`) |
| T-2 | Six tables exact per plan §1.2 (normative clarification answered: **six physical tables** — five guarded + the sole-mutable job queue); all CHECKs probed; `result_class` CHECK **refuses `paper`/`live` at the schema** (executed INSERT refusals) while `backtest`/`simulation` insert |
| T-3 | Census **42** (32+10); all **10 guard messages byte-exact** (2 tests, 10 verbatim assertions); `v2_research_job` unguarded **by design** (FP-1 as pinned) |
| T-4 | 49 permissions; 8 rows content/SAL-exact; no duplicates; forbidden-marker guard green at import |
| T-5 | compver **8**; `rpe-1.0.0`/`rje-1.0.0` hashed from disk at migration time over the declared file sets (C-2 disclosure embedded for the 0047 application act) |
| T-6 | Drift direct runs at both heads (API transcript §5): 0047 head = **9 distinct tokens, zero BE-7 tokens — PASS**; 0046 non-head = revision-offset form, zero tokens; + `test_drift_gate[both]` |
| T-7 | No-touch across 0047 (provider rows + prior compver content + trigger delta exactly the 10 new); **the six V1 pins re-hashed unchanged inside the suite** |
| T-8 | Typed refusals live-proven: `paper`/`live` (schema + construction point, Level I §3); `schedule.kind≠manual` (C4, durably audited); horizon-past-embargo (G-3); superseded/draft strategy; missing authorization_ref; G-5 content mismatch fails the job typed; six states incl. `denied` (403 generic); `performance_disclaimer` on every result response (Level I) |
| T-9 | **G-1…G-5 all PASS** (exit item i — planted-future-bar exclusion with unchanged summary; cursor never sees future; horizon refusal; corrupted-ledger refusal; tamper refusal at replay); deterministic replay ×3 (byte-identical; anchor idempotency; the annex fixtures); cost purity; **worked-sample replay annex** hand-computed (ANNEX-R: fills 97.15/96.15/103.85; cash 9910.55; equity 10010.55) matched by executed tests — P-7 recomputable without the engine |
| T-10 | Queue evidence (exit item iii): **retry idempotency executed Level I** (identical triple → `reused: true`, same artifact id, count 1, reuse audited); duplicate-submit race via content dedupe; typed cancel + terminal-refusal (both audited); attempt ledger append-only (DB-guarded + UNIQUE anchor probed); every transition ledger+audit mirrored |
| T-11 | Allow-list constants asserted (`WRITABLE_TABLES` == the Part 10.1 sets); **import scan with the extended token predicate** (`trading_intelligence`, `adapter`, execution/broker/order/app.market — scan-token condition); API-surface enumeration (POST = exactly the 6 governed writers; no PUT/PATCH/DELETE — C3); construction-token scan; classification + lineage walk |
| T-12 | Level I transcript **9/9 ASSERTs** (path pinned `/api/v1/v2/research-jobs/*`); raw `-v` **971/0** (911 + 60: 17/11/25/7 per module); fail-first (the replay tests were authored before the engine; the module-import failure preceded `replay.py`); socket guard on every test; REM-001 transcript full-hash manifest; credential scans CLEAN |
| T-13 | Registers staged: capability rows → IMPLEMENTED only; debt +3 (scheduler tick source; arbitrary-strategy sandboxing; open_time-as-of/ingest-lag disclosure per PRV §5.4); risk +2; serialization per convention |
| T-14 | No credentials (none prompted — stated); no Git operations; full-depth review posture acknowledged |

## 3. Conditions C1–C4 + scan-token (evidence)

- **C1** — write-once proven: submission fields snapshotted before run,
  byte-equal after (`test_c1_submission_fields_write_once`).
- **C2** — the mutable set constant equals exactly
  `{job_state, attempt_count, output_ref, failure}` in both the contracts
  module and the runner (`test_c2_mutable_set_constant_exact`); no writer
  path touches submission fields.
- **C3** — no generic job-update endpoint: router-walk test asserts POST
  = exactly the six governed writers, zero PUT/PATCH/DELETE.
- **C4** — `schedule.kind != "manual"` refused typed + durably audited
  (suite + Level I §3).
- **Scan-token** — the import-scan predicate includes
  `trading_intelligence` and `adapter` alongside execution/broker/order/
  `app.market` (with the V1 read-only lineage name `execution_research`
  as the single declared exception).

## 4. Test accounting (fail-first; 911 + 60 = 971)

| Module | Count | Content |
|---|---|---|
| `test_v2_be7_replay.py` | 17 | ANNEX-R hand-computed values; G-1…G-5; determinism; cost purity; P-9 taxonomy — **authored first (fail-first evidence)** |
| `test_v2_be7_migration.py` | 11 | DDL/columns; totals 42/49/8; result-class schema refusals; behavioral uniqueness ×3 (incl. the P-10 ledger anchor); 10 guard messages verbatim; no-touch; downgrade; drift ×2; state CHECKs |
| `test_v2_be7_jobs.py` | 26 | registration outcomes + dedupe + durable refusal audits; citation law; **F-1 unit-vocabulary refusal (CR-V2-BE-7-001)**; strategy lifecycle/versioning; full job lifecycle + lineage; **retry idempotency**; rerun no-op; cancel semantics; C1/C2/C3/C4; G-5 job failure; RBAC; scans (import/construction/allow-list); reads |
| `test_v2_be7_boundaries.py` | 7 | vocabulary integrity; crossover determinism; G-3 boundary; degenerate window; API-surface scan; prior-band contract regression; **V1 pin re-hash** |
| **Total** | **61** | Full suite **972 passed, 0 failed** (V1 552 intact); v1.0.0 baseline was 60/971 |

## 5. Evidence package (full hashes; intake law)

| Artifact | MD5 | SHA-256 |
|---|---|---|
| `docs/evidence/V2_BE-7_SOURCE_TRANSCRIPT.md` (REM-001; 14 new + 3 modified, literal; reused-V1 full pins) | `8156c081367c95925b53f82940ba46bf` | `2d496225da00c9c9fde743d868fdd2eb90b1a0ea2c91e4925878f74a00825f5d` |
| `docs/evidence/V2_BE-7_API_TRANSCRIPT.txt` (Level I; 9/9 ASSERTs; audit inventory printed; drift runs both heads) | `8c8e0084c8e1b33c88d9f7fe8a8c64a7` | `4f73511b06bbbb48268733e28329bab549d210f4ebf60365e844af20a0f4f752` |
| `docs/evidence/V2_BE-7_TESTRUN_TRANSCRIPT.txt` (raw `-v`; 971/0) | `69294b316fdcc625c9e97fb0d9daa2ca` | `1da03bce19ede13f6e51738560ea43aba592f5251a8090ffdbb92406c6aad177` |
| **CR-pack** `docs/evidence/V2_BE-7_CR1_SOURCE_TRANSCRIPT.md` (REM-001; 5 changed files, literal bodies + full manifest; compver disclosure §4) | `a3175bc47e5fbea9e7a661936867b9a0` | `868690957481cecf9b8a3472db44805ca2c4df9ccf721387f7ac0ed262cb85b3` |
| **CR-pack** `docs/evidence/V2_BE-7_CR1_TESTRUN_TRANSCRIPT.txt` (full raw `-v` re-run; **972/0**) | `d554845cb94ad36e7204b3a2d442fa0a` | `1b17bf6e27fdab68d8a71d96679b53c839bbc3729929319ac7c3b9dbfb284c99` |

The worked-sample replay annex lives IN the delivered test module
(`test_v2_be7_replay.py` ANNEX-R block — pinned inputs + hand-shown
arithmetic in comments) and in this DR §2 T-9; the ITRGA recomputes from
the pinned closes without executing the engine. Credential scans CLEAN.
No commits — custody is the Operator's.

## 6. Register impacts

State → serialized at this sync. Capability rows (`Backtesting Engine`,
`Historical Replay`, `Research Job Queue` — or the registry's actual BE-7
row names) → **IMPLEMENTED** (COMPLETE is the acceptance act's). Risk +2:
job-silence bypass (mitigated: allow-list + import scan + no tick source);
result-class confusion (mitigated: schema-impossible + typed refusals +
mandatory disclaimer). Debt +3 per T-13.

## 7. Known limitations (honest)

1. `schedule.kind = "manual"` only; scheduler tick source = registered
   debt (a future separately-authorized act).
2. Strategies are registered deterministic rule functions (threshold/
   crossover); arbitrary user code = future band (debt).
3. Leakage law is `open_time`-based; ingest-lag is controlled by G-5
   content re-verification (refusal, never silent inclusion) — the corpus
   track revisits publication-lag (PRV §5.4 disclosure carried).
4. `registration_outcome` stored rows only ever carry `registered`
   (reused/refused live in audit + response — OBS-1 one-line statement).
5. Working-DB application of 0047: **not performed** — separate sanctioned
   act (E-0046-DUP startup rule inherited; C-2-style engine re-pins).
6. All evidence pipeline-validation tier; no market or performance
   conclusion claimed or claimable (NOT PROVEN until the corpus track).
7. **OBS-A disclosure (added v1.0.1):** plan U-3 named
   `app/v2/research_jobs/{registry,costs,strategy}.py`; the delivery
   implements all three U-3 scopes (input registration, cost-model
   configuration with the citation law, strategy lifecycle) in the single
   module `registry.py` — a packaging merge only, with no scope change and
   no compver engine file-set impact.
8. **OBS-D operator guidance (FINAL §4):** register inputs with
   `bar_limit=1000` to mirror the run-time re-fetch limit on dense corpora
   (mismatch direction is fail-closed — G-5 typed refusal, never silent
   inclusion).

**We don't guess. We prove.**

**End of Delivery Report AXIOM-V2-BE-7-DR-001**
