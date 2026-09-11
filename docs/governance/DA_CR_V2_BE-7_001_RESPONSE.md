# DA CORRECTION PACK — CR-V2-BE-7-001
# AXIOM-V2-BE-7-CR-001 · v1.0.0 · 2026-09-04 · AXIOM Trading Terminal v2.0
# Band: BE-7 · Responds to: ITRGA-DET-V2-BE-7-FINAL-001 (ACCEPTED WITH CORRECTIONS)
# Chain: … → INT (PASS) → DA-INT-ACK → FINAL (F-1, F-2; OBS-A…E) → THIS PACK
# Author: Replacement Development Authority (DA)
# Status: SUBMITTED FOR ITRGA TARGETED RE-VERIFICATION (FINAL §5 item 2)

---

## §1 — Pack contents (the five FINAL §5.1 items, in order)

| FINAL §5.1 item | Delivered as |
|---|---|
| (i) `registry.py` F-1 gate | `register_cost_model` unit-vocabulary gate (§2 below) |
| (ii) F-1 regression test | `test_cost_model_unknown_unit_refused_f1` in `test_v2_be7_jobs.py` |
| (iii) F-2 ×3 assertion | `test_annex_deterministic_byte_identical` now `s1 == s2 == s3` |
| (iv) DR v1.0.1 | `DELIVERY_REPORT_V2_BE-7.md` re-stamped: §0 revision note + OBS-A disclosure (§7.7) + OBS-D guidance (§7.8) + §5 table extended + accounting 61/972 |
| (v) delta testrun evidence | **full** raw `-v` re-run chosen (welcome form): `V2_BE-7_CR1_TESTRUN_TRANSCRIPT.txt` — **972 passed / 0 failed** |

Plus the REM-001 source transcript for the diff surface:
`V2_BE-7_CR1_SOURCE_TRANSCRIPT.md` (5 changed files, literal bodies, full
MD5+SHA-256 manifest, compver disclosure).

## §2 — F-1 implementation (behavioral contract as ordered)

**(a) Registration-time vocabulary gate.** `contracts.py` gains
`COST_UNITS_V1 = ("price", "fraction")` — the exact unit set
`replay.apply_costs` implements. `register_cost_model` now refuses any
component (`spread`/`commission`/`slippage`) whose `unit ∉ COST_UNITS_V1`,
appending a typed reason `{failing: "<key>.unit", value: <unit>,
allowed: ["price","fraction"]}` and flowing through the **existing**
`cost_model.refused` durable-audit path (C-1 commit-before-return law,
unchanged). No row is written on refusal.

**(b) Regression test.** `test_cost_model_unknown_unit_refused_f1`
registers a cost model with `unit: "bogus"` through the real API and
asserts all four ordered properties: outcome `refused`; reasons name
`spread.unit` and the allowed vocabulary; **zero** `v2_cost_model` rows
written; durable `cost_model.refused` audit present post-session.

**(c) Defense-in-depth (optional item — taken).** `runner.run_job` now
catches engine `ValueError` beside the existing `LeakageRefused` catch and
routes it through the same `_fail` typed path: job `failed` with
`{failing: "engine_vocabulary"}`, attempt-ledger row minted, `job.failed`
durably audited. The commit law of the runner/API is unchanged. The
untyped-500 path described in F-1 is now unreachable both at the gate
(no lawful registration can carry an unknown unit) and at the engine
boundary (a pre-gate row would still fail typed).

## §3 — F-2 implementation

`test_annex_deterministic_byte_identical` executes the ANNEX-R replay
**three** times and asserts total equality of the canonical JSON
summaries (`s1 == s2 == s3`) — the BO T-9 ×3 pin, exactly. No
production-code change.

## §4 — Changed-file manifest (full hashes; nothing else touched)

| File | MD5 | SHA-256 |
|---|---|---|
| `backend/app/v2/research_jobs/contracts.py` | `8220eea42ee9567e381ba22b873a5a40` | `b8d0c5313c2c7a035a90167ece78cbdcda792f1a9bf706a447fa261eb7b7783e` |
| `backend/app/v2/research_jobs/registry.py` | `eeafa50e60fce65e85a9df16dce96b5e` | `bb3540221f92a688e272e09dc48983a51d248c58636e20ce9f65845e65d6ab4d` |
| `backend/app/v2/research_jobs/runner.py` | `3148c9210679d25dd989df4e127b02e8` | `8d0032cb92c1dc52fc09f40788c738dd1ae4f1ead3fb7b8136606bf704c68fda` |
| `backend/tests/test_v2_be7_jobs.py` | `1aea66feb0e78e78d2a40de00ea75350` | `4c9c33c2eb72d086964e529e27d255044ef0f9ff1baf445eb7a6572373c31c19` |
| `backend/tests/test_v2_be7_replay.py` | `36070156e771edfe079149aaf2da22b1` | `521bf5632d2dfa154e494e79090e796066474b5fc3b257ea6962c1324700dfcd` |

Zero files added/deleted; no migration, schema, guard, seed, or V1 change;
the 12 unchanged manifest files retain their FINAL §2 hash-locked bytes.
Ruff clean over the band + test modules.

## §5 — Compver movement disclosure (C-2 law)

`runner.py` ∈ `_RJE_FILES` ⇒ the apply-time RJE hash moves:

- RPE — **UNCHANGED**: `1499343d48b778af17065e8bf1eaabcffc116880fa6967ab442db1255992b178`
- RJE — **NEW**: `8f107d174e081dc0a1527fea841b89dfb73744e3f16eba2d29c60521158c0598`
  (was `f01e3041a060e96cfcdcc9650d2458f84512e2d1bb2e2509fe668a9d3704ed7c`)

The 0047 working-DB application act must pin the NEW RJE value (the
migration hashes from disk at apply time — correct-by-construction per
OBS-B; this section gives the act its pre-declared expectation).

## §6 — Evidence artifacts (full hashes; intake law)

| Artifact | Bytes | MD5 | SHA-256 |
|---|---|---|---|
| `docs/evidence/V2_BE-7_CR1_SOURCE_TRANSCRIPT.md` | 63,267 | `a3175bc47e5fbea9e7a661936867b9a0` | `868690957481cecf9b8a3472db44805ca2c4df9ccf721387f7ac0ed262cb85b3` |
| `docs/evidence/V2_BE-7_CR1_TESTRUN_TRANSCRIPT.txt` (raw `-v`, 972/0) | 96,090 | `d554845cb94ad36e7204b3a2d442fa0a` | `1b17bf6e27fdab68d8a71d96679b53c839bbc3729929319ac7c3b9dbfb284c99` |
| `DELIVERY_REPORT_V2_BE-7.md` **v1.0.1** | 13,176 | `63c29cd7ba2214295ece7d7dcbc70396` | `30d96ee12554711d96036cb1a25529ec9747c810412da7648d928d5ad5f86027` |

Credential scan: CLEAN (the two test-fixture placeholders in the jobs test
body are the household synthetic auth constants — classification per the
BE-5 intake law). v1.0.0 evidence artifacts remain byte-frozen on the
record; nothing re-stamped except the DR, exactly as the FINAL directed.

## §7 — Observation dispositions acknowledged

- **OBS-A** — disclosure landed in DR v1.0.1 §7.7 (the FINAL's editorial
  order; the INT-ACK line-map already verified by ITRGA at depth).
- **OBS-B** — CLOSED by ITRGA; no action.
- **OBS-C** — acknowledged; postgresql message-parity revisit belongs to a
  future postgresql deployment act (no current action).
- **OBS-D** — operator guidance recorded in DR v1.0.1 §7.8
  (`bar_limit=1000`); fail direction remains closed (G-5 typed refusal).
- **OBS-E** — acknowledged; the DA will ship a dedicated failing-run
  transcript as a fortifying artifact in future bands' fail-first
  evidence.

## §8 — Posture

New suite floor **972** (971 + 1). No Git operations; working DB
untouched; 0047 application remains un-authorized until the ACCEPTANCE
instrument (FINAL §5.3) and stays a separate sanctioned act thereafter.
Awaiting ITRGA targeted re-verification (intake-lite) per FINAL §5.2.

**We don't guess. We prove.**

— AXIOM-V2-BE-7-CR-001 · v1.0.0 · 2026-09-04
