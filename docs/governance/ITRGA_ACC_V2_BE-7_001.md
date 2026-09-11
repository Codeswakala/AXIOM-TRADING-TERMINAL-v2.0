# ITRGA ACCEPTANCE INSTRUMENT — BAND BE-7
# ITRGA-ACC-V2-BE-7-001 · v1.0.0 · 2026-09-04 · AXIOM Trading Terminal v2.0
# Band: BE-7 (Backtesting, Simulation, Replay, and Governed Research Jobs)
# Chain: CN-V2-BE-7-001 → REQ → PRV (ACCEPTED) → BO-V2-BE-7-001 → DR v1.0.0
#        → INT (PASS) → DA-INT-ACK → FINAL (ACCEPTED W/ CORRECTIONS: F-1, F-2)
#        → DA CR-001 pack (DR v1.0.1 + CR1 transcripts) → TARGETED RE-VERIFICATION
#        → THIS ACCEPTANCE
# Office: ITRGA · act class: band acceptance (post-correction-cycle, FINAL §5 item 3)

---

## §0 — Determination

**BAND BE-7 IS ACCEPTED.** The correction cycle **CR-V2-BE-7-001 is CLOSED**: both required corrections (F-1, F-2) are delivered, verified, and proven by executed evidence; all carried observations are resolved or honorably registered. The band's delivery state is hereby certified as the BE-7 floor:

- migration `20260903_0047` (`down_revision="20260903_0046"`), on DA test chains — **the working-DB application remains a separate sanctioned act (§5)**;
- executed suite floor **972 passed / 0 failed** (911 + 61: replay 17 · migration 11 · jobs **26** · boundaries 7; V1 552 intact);
- v2 trigger census **42** (32 + 10; job table unguarded by design) · permission rows **49** (41 + 8) · computation-version rows **8** (6 + 2);
- drift declaration unchanged: exactly the 9 inherited V1 tokens, zero BE-7/V2 tokens (both-heads proven);
- determinism anchor, idempotency, leakage law, typed-outcome law: as certified in `ITRGA-DET-V2-BE-7-FINAL-001` §3 and unchanged by this cycle (diff-surface verification §2).

## §1 — Correction-cycle material (identities, ITRGA-recomputed)

| Artifact | MD5 (recomputed) | SHA-256 (recomputed) |
|---|---|---|
| `DELIVERY_REPORT_V2_BE-7.md` **v1.0.1** (13,176 B) | `63c29cd7ba2214295ece7d7dcbc70396` | `30d96ee12554711d96036cb1a25529ec9747c810412da7648d928d5ad5f86027` |
| `V2_BE-7_CR1_SOURCE_TRANSCRIPT.md` (63,267 B) | `a3175bc47e5fbea9e7a661936867b9a0` | `868690957481cecf9b8a3472db44805ca2c4df9ccf721387f7ac0ed262cb85b3` |
| `V2_BE-7_CR1_TESTRUN_TRANSCRIPT.txt` (96,090 B) | `d554845cb94ad36e7204b3a2d442fa0a` | `1b17bf6e27fdab68d8a71d96679b53c839bbc3729929319ac7c3b9dbfb284c99` |

All recomputed values byte-match the DA CR-001 §6 table and DR v1.0.1 §5. CR1 manifest bodies: 5/5 extracted literals hash to declared full SHA-256. The v1.0.0 evidence artifacts remain byte-frozen on the record (pins unchanged and re-verified). DR v1.0.0 → v1.0.1 revision is exactly the FINAL §5 directed editorial: §0 revision note + OBS-A disclosure (§7 item 7) + OBS-D guidance (§7 item 8) + §5 table extension + accounting 61/972; no other section altered in substance.

## §2 — Targeted re-verification ledger (FINAL §5 item 2)

**Bounded-diff law: VERIFIED.** The cycle touched exactly five files — `contracts.py` (+5/−0), `registry.py` (+8/−0), `runner.py` (+8/−0), `test_v2_be7_jobs.py` (+28/−0), `test_v2_be7_replay.py` (+3/−1) — and **nothing else** (unified-diff against the FINAL-hash-locked baseline reviewed at depth; the twelve untouched files retain their certified bytes; no migration/schema/guard/seed/V1 change).

**F-1 — CLOSED.**
- (a) Vocabulary gate: `contracts.COST_UNITS_V1 = ("price","fraction")` — placed in the contracts module (single source of truth, exactly the set `apply_costs` implements); `register_cost_model` refuses any component with `unit ∉ COST_UNITS_V1` via typed reasons `{failing: "<key>.unit", value, allowed: ['price','fraction']}` flowing through the **existing** `cost_model.refused` durable-audit path (C-1 commit-before-return unchanged; no row written).
- (b) Regression test `test_cost_model_unknown_unit_refused_f1` asserts all four ordered properties through the real API: outcome `refused`; reasons name `spread.unit` AND the allowed vocabulary; **zero** `v2_cost_model` rows; durable `cost_model.refused` audit present post-session. **PASSED** (CR1 testrun line 729).
- (c) Defense-in-depth (optional item — taken): `runner.run_job` catches engine `ValueError` beside `LeakageRefused` into the existing `_fail` typed path (`engine_vocabulary` failing class; attempt-ledger row; `job.failed` durable audit). The untyped-500 path of the FINAL's F-1 is now unreachable on both gates.

**F-2 — CLOSED.** `test_annex_deterministic_byte_identical` executes the ANNEX-R replay three times with total equality `s1 == s2 == s3` — the BO T-9 ×3 pin. **PASSED** (CR1 testrun line 766).

**Executed evidence: VERIFIED.** Full raw `-v` re-run (welcome form): **972 passed, 0 failed**, 473.47s; module accounting 26+17+11+7 = 61; 911+61 = 972 ✓. Compver destiny re-pinned by this office from first principles: rolling-hash over (unchanged `queue.py` + corrected `runner.py`) reproduces the DA's pre-declared **new RJE `8f107d174e081dc0a1527fea841b89dfb73744e3f16eba2d29c60521158c0598`** exactly; RPE unchanged `1499343d48b778af17065e8bf1eaabcffc116880fa6967ab442db1255992b178`.

## §3 — Observation dispositions (final)

**OBS-A CLOSED** — the missing DR §7 disclosure now lands in DR v1.0.1 §7 item 7 exactly as ordered (the ACK line-map was verified at depth in the FINAL). **OBS-B CLOSED** (prior). **OBS-C registered** for a future postgresql-deployment act. **OBS-D CLOSED** — operator guidance landed in DR v1.0.1 §7 item 8 (`bar_limit=1000`; fail-closed direction noted). **OBS-E registered** — DA commits to shipping a dedicated failing-run transcript in future bands' fail-first evidence.

## §4 — Register synchronization (staged; DA owns the edits per the correction of record)

At acceptance the DA applies the register content staged in DR §6 with the acceptance consequence: capability rows **`Backtesting Engine`, `Historical Replay`, `Research Job Queue` → COMPLETE** (citation: this instrument, ITRGA-ACC-V2-BE-7-001; delivery citation BO-V2-BE-7-001 + DR v1.0.1); the **+3 debt rows** as staged (scheduler tick source v2-scope; arbitrary-strategy sandboxing; open_time-as-of / ingest-lag disclosure); risk rows as declared; serialization per the register conventions. ITRGA supplies this content instruction only; the DA performs the register edits.

## §5 — The remaining chain act (0047 working-DB application)

Acceptance closes the band; it does **NOT** authorize the database application. The 0047 working-DB application on the operator's environment (`backend\axiom_dev.db`, alembic 1.19.0) remains a **separate sanctioned act** at chain end, to be executed by instrument with: (i) initialization-refusal if any PASS marker exists (E-0046-DUP startup-hygiene law); (ii) compver re-pin at apply time whose pre-declared expectations are now fixed: **RPE `1499343d…` (unchanged) · RJE `8f107d17…` (CR-001 value)** — the migration hashes from disk, correct-by-construction, with these values as the verify gate; (iii) transcript-witnessed literals; (iv) the household V1→V2 verify supersession rule; (v) ASCII-only console output. Awaiting operator authorization to issue that instrument.

## §6 — Band floor of record (post-acceptance)

Bands BE-0…BE-7 closed at delivery-chain state; working lineage nominally `20260903_0047`, pending its application act. Suite floor **972**; triggers **42**; permissions **49**; compver **8**; drift = 9 inherited V1 tokens, zero band tokens. Commission closure line updated accordingly.

— ITRGA-ACC-V2-BE-7-001 · v1.0.0 · 2026-09-04 (Africa/Nairobi) · **We don't guess. We prove.**
