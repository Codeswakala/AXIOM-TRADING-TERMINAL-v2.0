# DELIVERY REPORT — AXIOM V2 BE-5: Predictive ML, Signal, and Research Governance Expansion

| Field | Value |
|---|---|
| Document ID | AXIOM-V2-BE-5-DR-001 |
| Revision | **v1.0.1** — C-1 applied per `ITRGA-INT-V2-BE-5-DR-001` (single column rename `superseded_by` → `supersedes`; one surfaced-defect fix + regression test; suite 855 → **856**) |
| Build Order | BO-V2-BE-5-001 |
| Governing plan | AXIOM-V2-BE-5-DA-PLAN-001 v1.0.0 **as amended by ITRGA-PRV-V2-BE-5-PLAN-001 Review Pins P-1…P-5** (the BO prevails on any difference — honored) |
| Date | 2026-09-02 |
| Author | Development Authority (DA) |
| Status | **RE-SUBMITTED (v1.0.1) — C-1 closed; evidence package attached with FULL hashes** |
| Baseline in | head `20260831_0043` (working DB, untouched) · 789 tests · triggers 18 · permissions 27 · compver 3 |
| Baseline out | migrations `20260902_0044` + `20260902_0045` (**DA test chains only** — working-DB application is a separate sanctioned act, BO §3) · **856 tests** · triggers 18→24→28 · permissions 27→34→35 · compver 3→4→5 (all P-5 pins hit exactly) |

**Standing discipline: we don't guess. We prove.**

---

## 1. Executive Summary

Band BE-5 is implemented in full: all six units (U-1…U-6), all five Review
Pins applied, all twelve terminal-state items T-1…T-12 satisfied with
executed evidence. **856 executed, 856 passed, 0 failed** = 789 baseline +
**67 new tests** (≥ +64 per P-5; fail-first order stated in §3; +1 C-1 regression test). Zero V1
diffs; BE-3 + BE-4 state proven byte-identical across both migrations;
zero network attempts; **no credential of any kind prompted for or used
anywhere in the band** (T-12 declaration).

**Data-honesty declaration:** every BE-5 artifact carries the 6-class
`data_class` taxonomy; at first landing only `synthetic`/`simulated` are
reachable — `historical_real`/`live` are **refused with typed reasons**
(executed evidence in the API transcript). Validation tier:
**pipeline-validation**. No market conclusion is claimed or claimable;
real-data research validation remains corpus-track-gated (plan Part 11).

## 2. Terminal-state contract — item-for-item (BO §2)

| T | Pinned expectation | Evidence (executed) |
|---|---|---|
| T-1 | 0044 (`down_revision='20260831_0043'`) → 0045; literal-revision upgrades; models registered same-unit | Migration files (transcript §3); every test chain upgrades by literal revision; `app/db/models/__init__.py` registers all 5 models |
| T-2 | 0044 tables with P-1 (`record_seq`, `superseded_by`, no `updated_at_event_id`, `UNIQUE(model_artifact_id, record_seq)`), P-3 (`model_type`, `instrument_class`), P-2 (`v2_ml_diagnostic_report` full 0043 pattern); CHECK vocabularies exact | `test_0044_tables_seeds_triggers` (columns asserted present/absent; versioned uniqueness proven behaviorally: same (artifact,seq) refused, next seq allowed); `test_0044_check_vocabularies` |
| T-3 | 24 triggers after 0044; 6 exact names/messages | Trigger count + name-set asserted; **all 6 messages byte-exact** (`test_0044_guard_messages_verbatim`) |
| T-4 | 34 permissions after 0044 (7 additive, SAL-aligned, no duplicates) | Content-exact set comparison incl. SAL; duplicate check |
| T-5 | compver 4 after 0044; `mge-1.0.0` hash pinned from the co-delivered U-2 engine | Migration hashes the three engine files **from disk at upgrade time** (P-4); 64-char hash asserted; ITRGA recomputes from transcript literals |
| T-6 | 0045: signal tables; family/state CHECKs exact; 28 triggers; 35 permissions; compver 5 (`sge-1.0.0`) | `test_0045_tables_seeds_triggers`, `test_0045_guard_messages_and_checks` (messages byte-exact; `hybrid` family and `active` state refused by CHECK) |
| T-7 | Six pure decision contracts; spec citations in `decision_basis`; ≥1 pass + ≥1 typed refusal each; economic ⊥ statistical; ladder + rollback + champion-scope (P-3) enforced | 24 decision tests + 7 ladder/boundary tests; independence test (`significant` + `unviable` coexist); `test_promotion_refused_without_rollback`, `test_champion_scope_at_most_one`, `test_stale_record_seq_refused` |
| T-8 | Signal writer: predictive-without-eligible-governance → permanent refused; withheld/expired/refused permanent (event-append, zero row mutation); payload NULL on refusal; uncertainty mandatory for predictive; lineage refs mandatory; data-class refusals; reads read-only; typed `denied`; socket guard | 14 API tests + 16 lifecycle tests; expiry proven as event-append with the record row untouched and the projection carrying the truth; Level I transcript samples |
| T-9 | integrity ok, journal delete, no sidecars; working DB untouched | DA test-chain posture; **no working-DB write in the band** (BO §3) |
| T-10 | Drift at both heads | Direct runs in the API transcript §5: 0045 head = **9 distinct tokens, zero BE-5/V2 — PASS**; 0044 (non-head) = revision-offset form with zero BE-5 tokens (PGF-014 format-independent); + `test_drift_gate[0044/0045]` |
| T-11 | No-touch + floor ≥853 | `test_no_touch_be3_be4_state` (provider row, history, BE-4 compver rows content-identical; trigger delta = exactly the 10 new); **856 ≥ 853**; no position-based assertions |
| T-12 | Mode/audit/credential law | Every row carries mode/actor/correlation; audit inventory `ml.promotion.decided/.refused`, `ml.diagnostics.computed`, `signal.emitted/.refused` (+ withheld/expired vocab); redaction gate + forbidden-marker guard untouched and re-asserted at import; **credential scan CLEAN on all artifacts; no credential prompted or used** |

## 3. Test accounting (fail-first; 789 + 66 = 855, itemized, no double counting)

| Module | Count | Written before implementation? |
|---|---|---|
| `test_v2_be5_decisions.py` | 24 | **Yes** — authored first, failed on missing module (fail-first evidence: the module import error preceded `decisions.py`) |
| `test_v2_be5_migration.py` | 9 | Contract pins authored with the DDL; guard/CHECK/no-touch/downgrade/drift |
| `test_v2_be5_api.py` | 15 | Writers, states, RBAC |
| `test_v2_be5_diagnostics.py` | 3 | P-2 artifact + determinism anchor + audit/lineage |
| `test_v2_be5_lifecycle.py` | 16 | Expiry semantics, ladder variants, boundary values, vocabulary integrity |
| **Total new** | **67** | Full suite: **856 passed, 0 failed** (V1 552 green) |

## 4. Review-Pin satisfaction (P-1…P-5)

- **P-1 + C-1** — full immutability + row versioning implemented; the
  supersession column is now **`supersedes`** per correction C-1
  (`ITRGA-INT-V2-BE-5-DR-001` §2): the successor row holds the
  predecessor's id and reads forward ("this row supersedes that one");
  currency = greatest `record_seq` projection. **C-1 additionally surfaced
  two latent defects, both fixed and tested:** (a) the `current_only` read
  filter used `IS NULL` on the link column — correct under the old
  backlink naming's genesis semantics but wrong as a currency filter;
  replaced with the record_seq max-projection subquery; (b) the signal
  writer's governance-currency check was latently inverted — replaced with
  an explicit is-current resolution, and a new regression test
  (`test_predictive_superseded_generation_refused`) proves a
  superseded-generation governance record refuses predictive emission
  (also proven Level I in the API transcript §2). Honest note: C-1's
  correction scope was one column name; the two fixes above exceeded it
  because the rename surfaced real defects — concealing them was not an
  option. Both are disclosed here and in the transcript revision note for
  the ITRGA to judge.
- **P-2** — `v2_ml_diagnostic_report` in 0044 with the full 0043 pattern
  (anchor proven idempotent by test; audit + lineage rows verified);
  U-5 is services + read projections over the table.
- **P-3** — scope columns present; at-most-one-champion enforced by writer
  + dedicated tests (same-scope refused; different-scope allowed); no
  partial unique index (per the pin's mechanics note).
- **P-4** — compver rows seeded only with their co-delivered engines,
  hashed **from disk at migration time**; no row precedes/follows its
  package boundary.
- **P-5** — every pinned total hit exactly (see Baseline out); budget
  ≥ +64 satisfied at +66.

## 5. Threshold citations (BO §3 — no invented numbers)

| Constant | Value source | Citation |
|---|---|---|
| `CALIBRATION_ECE_WARNING` | `CalibrationConfig.warning_threshold_ece` (0.15) | `app/ml/calibration/service.py` — asserted equal to a live default instance by `test_threshold_constants_cite_v1_configs` |
| `CONFIDENCE_LEVEL` / `SIGNIFICANCE_P_BOUND` | `ValidationConfig.confidence_level` (0.95 → p ≤ 0.05) | `app/ml/validation/service.py` — same test |
| `BOOTSTRAP_SAMPLES_MIN` | `ValidationConfig.bootstrap_samples` (200) | same |
| Freshness bounds (30/90 days) | **Band-level declared bounds** (no V1 config exists for these) — disclosed in every outcome's `thresholds`; a future governed change may replace them without schema change | plan Part 13 posture |

## 6. Evidence package (BO §4)

All artifacts Revision 2 (regenerated against the post-C-1 tree). FULL
hashes per intake §4:

| Artifact | Content | MD5 (full) | SHA-256 (full) |
|---|---|---|---|
| `docs/evidence/V2_BE-5_SOURCE_TRANSCRIPT.md` (Rev 2) | REM-001 literals: 15 new + 4 modified files; SHA-256 manifest; reused-V1 pins; §0 revision note itemizing every C-1-scope change | `36e59d51e8f1af32abfd8b21c2b25222` | `e59ee582f069c553e3a7f9bfa0259c547e109cea99ce707f366769d8615fba8d` |
| `docs/evidence/V2_BE-5_API_TRANSCRIPT.txt` (Rev 2) | Level I executed: endpoint path pinned; typed permanent states; data-honesty refusal; **superseded-generation refusal (C-1) executed**; P-1 versioned promotion; ladder/rollback refusals; RBAC denied; drift direct runs at both heads; **12/12 inline ASSERTs True** | `78f1f65dd69981e90201b9aa91432cc7` | `843bce50c4124a0e08f2592334dcbd73af21acb331edd9de931e4a01d93bbb03` |
| `docs/evidence/V2_BE-5_TESTRUN_TRANSCRIPT.txt` (Rev 2) | Raw `pytest -v`: command, environment + no-network posture, **856 PASSED / 0 FAILED**, summary line | `ed87d43fc5cd3f9d7d8f8c317db4e2ec` | `c886381eec7045ed8c77cde25ef09f7349745fb27b4c6a257af3324119d2e135` |
| This DR | Requirement map: REQ §1.1–§1.9 (via the plan, reviewed COMPLIANT) + P-1…P-5 (§4) + T-1…T-12 (§2) | — |

Credential scan CLEAN on every artifact. All commits belong to the
Operator — none made.

## 7. Register impacts (per plan Part 10)

`V2_CURRENT_STATE.md` → v27.0.0. Capability maturity: `ML Research
Expansion` and `Signal Architecture V2` → **IMPLEMENTED** (evidence:
executed tests + Level I transcript; **COMPLETE** is the determination's
to grant, not the DA's). Risk register: +2 rows (signal-truthfulness,
governance-writer-bypass — both mitigated). Tech debt: +3 honest rows
(unreachable data classes corpus-gated; declared freshness bounds;
backlink-vs-forward-link naming pending ITRGA view, §4 P-1).

## 8. Known limitations (honest)

1. ~~P-1 backlink naming~~ — **resolved by C-1** (`supersedes`; §4).
2. Freshness bounds are band-declared, not V1-cited (§5 — disclosed).
3. `withheld` state is structurally complete (CHECK + writer vocabulary +
   permanence semantics) but no v1 emitter path produces it — the writer
   emits/refuses; withholding logic arrives with future evaluator
   integration. Zero-emission discipline verified; recorded as debt-class
   disclosure, not hidden.
4. Working-DB application of 0044/0045: **not performed** — separate
   sanctioned acts (BO §3). **C-2 acknowledged:** the application act's
   instrument must pin the six engine files by hash pre-upgrade and assert
   post-upgrade compver content against those pins (recorded for that
   act's scope assessment; no migration change — the pinning lives in the
   instrument).
5. Real-data research validation: corpus-track-gated; NOT PROVEN and not
   claimed.
6. OBS-9 (BE-4 record) remains the Operator's administrative item.

**We don't guess. We prove.**

**End of Delivery Report AXIOM-V2-BE-5-DR-001**
