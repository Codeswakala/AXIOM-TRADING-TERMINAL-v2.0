# ITRGA INDEPENDENT REVIEW — W4-U06 (Professional Signal Validation Extension)

| Field | Value |
|---|---|
| Reviewing authority | **AXIOM Independent Technical Review & Governance Authority (ITRGA)** |
| Unit | **W4-U06** — Professional Signal Validation Extension |
| Wave | 4 — Institutional Intelligence |
| Build Order | `docs/BUILD_ORDER_W4-U06.md` |
| Evidence | `uploads/DELIVERY_REPORT_W4-U06.md` + `uploads/operator results.md` (1,418 lines) |
| DA-claimed platform | 0.36.0 |
| Review date | 2026-07-16 |
| **VERDICT** | **✅ APPROVED — CLEAN.** Platform advances to **v0.36.0** |
| Confidence | **HIGH** — both keystones (no-cherry-picking, raw-score-exclusion) proven on target; outcome-data honesty upheld |

> **We don't guess. We prove.** Validation runs over the full declared scope, strips the raw score even when it's present upstream, and refuses to invent performance where no governed outcome exists. Approved.

---

## 1. Bottom line

W4-U06 evaluates advisory-signal quality **honestly**: over a **declared, full scope (no cherry-picking)**,
with **raw model score excluded** (proven present-upstream/absent-downstream), **uncertainty on every metric**,
and an **honest `outcome_data_status: not_available`** that fabricates no realized performance. Look-ahead-safe
(R-2), non-signal (R-6), persisted with the **inline raw-SELECT + no-orphan audit (R-4)**, read-only
(401/list-200/detail-200/POST-405), pure-Python. All 8 named tests pass; full suite 233. **APPROVED, CLEAN.**

---

## 2. Keystone 1 — No cherry-picking (R18) — PROVEN ✅

- Named test `test_signal_validation_full_declared_scope_no_cherry_picking_deterministic PASSED` — the
  validation includes the full declared, as-of-bounded scope with no silent exclusions and is deterministic on
  the same scope (scope/filters persisted in the artifact).
- Metrics computed over the declared n=4 set: `clean_advisory_rate 0.25`, `guardrail_intervention_rate 0.75`,
  `calibrated_confidence_coverage 0.75` — each with a **Wilson interval + sample_count**. No selective window.

## 3. Keystone 2 — Raw-score-exclusion — PROVEN (strongest form) ✅

- Source signals seeded with `raw_score=0.987654`; report echoes `UNCALIBRATED_SCORE_EXCLUDED: True`.
- The persisted report + API payload contain **neither the `raw_score` key nor the value `0.987654`** — only
  `model_score_policy: uncalibrated_score_excluded_from_validation_output`,
  `uncalibrated_model_score_excluded: true`, and the note *"uncalibrated score excluded; no forward outcomes
  fabricated."* Present upstream, **provably stripped** downstream (the W3-U07 standard).
- Named tests `test_signal_validation_raw_score_present_upstream_absent_downstream PASSED` +
  `test_signal_validation_schema_is_inert_no_raw_score_order_or_signal_payload PASSED`.

## 4. Outcome-data honesty — UPHELD ✅

`OUTCOME_DATA_STATUS: not_available`; note "no forward outcomes fabricated"; `economic_verdict not_assessed`
(independent, R-5). No realized performance/returns are invented where governed outcome data does not exist —
exactly the honesty the Build Order demanded.

## 5. Other controls — PROVEN on target ✅

| Control | Evidence |
|---|---|
| Build identity + migration | v0.36.0; Alembic `20260716_0022 → 20260716_0023 (head)` |
| **R-2 no look-ahead** | `test_..._no_lookahead_future_signal_excluded PASSED`; `EXCLUDED_FUTURE_SIGNAL_COUNT: 1` |
| **GR-7 + R-5** | Wilson uncertainty + sample_count per metric; independent `economic_usefulness not_assessed`; bare rejected (`test_..._metrics_uncertainty_economic_and_outcome_status PASSED`) |
| **R-6 non-signal / no mutation** | `test_..._persisted_audited_no_signal_or_model_mutation PASSED`; grep benign |
| **R-4 persistence (INLINE)** | raw `SELECT FROM signal_validation_reports` → 1 row (`5f3189c8…`, metrics JSON, `not_available`, research_only) + audit `signal_validation_report.created` + **`orphan_signal_validation_report_count: 0`** |
| Read-only API | `UNAUTH 401`; **detail 200** (`DETAIL_OUTCOME_STATUS: not_available`); `POST 405` |
| Dependency discipline | pure-Python/Wilson; `test_..._no_unspiked_dependencies_or_execution_path PASSED`; no unspiked import |
| Gate / bright-line | broker gate passing; Gate CLOSED; wave-wide grep benign |
| Regression + CI | backend **233 passed**, frontend **11/25**, ruff clean, npm audit 0; **CI via `& "C:\Program Files\Git\bin\bash.exe" scripts/local_ci.sh` → marker + `LOCAL_CI_EXIT_CODE: 0`** (transcript labelled W4-U06) |
| No UI | correctly stated |
| D-W2-001 | no per-market model / symbol-identity feature |

---

## 6. Findings ledger

| ID | Severity | Status |
|---|---|---|
| — | — | No-cherry-picking (full declared scope, deterministic) ✅ |
| — | — | Raw-score-exclusion (present-upstream/absent-downstream) ✅ |
| — | — | Outcome-data honesty (`not_available`, no fabrication) ✅ |
| — | — | R-2 / GR-7 / R-5 / R-6 / R-4-inline / API 401·list200·detail200·405 / dep-discipline / gate-closed / 233 tests / CI exit 0 ✅ |

**No CRITICAL/HIGH. No unmet mandatory evidence. No open residual.** All acceptance criteria met on target.

---

## 7. Disposition & next step

- **W4-U06 — ✅ APPROVED, CLEAN.** Platform **v0.35.0 → v0.36.0**.
- Commendation: both hard-won project lessons upheld — **no cherry-picking** (full declared scope) and
  **raw-score-exclusion** proven with the raw score present upstream and absent downstream — plus genuine
  **outcome-data honesty** (refusing to fabricate performance). Every persistence/CI lesson held.
- **Next:** ITRGA recommends **W4-U07 — Institutional Intelligence Dashboard / Chart Context**, the first
  Wave-4 **operator-facing UI**: presentation-only (GR-8, no client recompute), displays the persisted W4
  reports (correlation/regime/scenario/portfolio-risk/signal-validation) with uncertainty + research/
  not-guaranteed framing, **no execution controls (R-3)**, read-only API. **Browser evidence is MANDATORY**
  (W3-U05 UI precedent — never approve UI on report-claims/sandbox-only; reachable served session). On operator
  authorization ITRGA issues `BUILD_ORDER_W4-U07.md`.
- After U07 → **W4-U08** (Closeout & Hardening → "Institutional Intelligence Layer Complete" milestone).
- DA does not self-authorize W4-U07, adopt an unspiked dep, add execution/broker, or open the Gate.

> **We don't guess. We prove.** — ITRGA
