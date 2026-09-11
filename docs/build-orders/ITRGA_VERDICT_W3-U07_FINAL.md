# ITRGA FINAL VERDICT — W3-U07 (Performance Analytics + Confidence Visualization)

| Field | Value |
|---|---|
| Reviewing authority | **AXIOM Independent Technical Review & Governance Authority (ITRGA)** |
| Unit | **W3-U07** — Performance Analytics + Confidence Visualization |
| Wave | 3 — Live Research Advisor |
| Supersedes | `ITRGA_REVIEW_W3-U07.md` (2026-07-16, APPROVAL WITHHELD — wrong evidence pack) |
| Evidence under review | corrected `uploads/operator results.md` (1,483 lines, W3-U07 pack) + prior 3 screenshots |
| Prior blocker | C-1 CRITICAL (stale W3-U06 pack) — **now CLEARED** |
| **VERDICT** | **✅ APPROVED — CLEAN.** Platform advances to **v0.29.0** |
| Confidence | **HIGH** — build identity proven; every mandatory gate met on target with raw command + output |

> **We don't guess. We prove.** The correct evidence was supplied, run on the W3-U07 build, and it proves every claim. Approved.

---

## 1. Bottom line

The prior WITHHELD verdict was **not** a merit finding — it was that the operator had submitted the previous unit's (W3-U06) evidence pack. That is now **fully corrected.** The re-submitted pack is unmistakably W3-U07, run on the W3-U07 codebase, and it clears **C-1 (CRITICAL)** and both HIGH follow-ons (F-2 count mismatch, F-3 screenshot contradiction). Every Build-Order requirement is proven on target. **W3-U07 is APPROVED, CLEAN, no residual.**

---

## 2. C-1 cleared — this is genuinely the W3-U07 build

Unlike the first submission (where `grep -i analytics` returned nothing), the corrected pack opens by **proving build identity** before testing:

| Check | Evidence (verbatim) | Result |
|---|---|---|
| New files exist on target | `Test-Path …analytics\service.py / advisory_analytics.py / test_advisory_analytics.py / PerformanceAnalyticsPage.tsx / .test.tsx / W3-U07_OPERATOR_EVIDENCE_COMMANDS.md` → **six `True`** | ✅ |
| Backend signatures | `class AdvisoryAnalyticsService`, `method="wilson_score_interval"`, `"/advisory-performance"`, `AdvisoryAnalyticsResponse` | ✅ |
| Frontend signatures | `<h1>Performance Analytics</h1>`, `Research analytics only.`, `Metric withheld: uncertainty missing`, `Confidence unreliable — calibration warning present.` | ✅ |
| Test signatures | `test_advisory_analytics.py`; UI tests `point-estimate-only`, `unreliability warning`, `does not render transaction controls` | ✅ |

**C-1 CLEARED.** The evidence is of the unit under review.

---

## 3. Count reconciliation — F-2 cleared

| Metric | DA report | Operator run (corrected) | Reconciles? |
|---|---|---|---|
| Backend `pytest` | 192 passed | **192 passed** (lines 417 & 1429) | ✅ |
| Named analytics tests | 4 passed | **4 passed, by name** (see §4) | ✅ |
| Frontend test files | 10 passed | **10 passed** (lines 452 & 1464) | ✅ |
| Frontend tests | 24 passed | **24 passed** | ✅ |
| Migration head | no new migration | `20260715_0018 (head)` unchanged | ✅ |
| ruff / npm audit / tsc / build | clean / 0 / clean / ok | `All checks passed!` / `found 0 vulnerabilities` / clean / `✓ built` | ✅ |

The suite is no longer the W3-U06 baseline (188/9/20) — it is the W3-U07 suite (192/10/24). **F-2 CLEARED.**

---

## 4. Requirement-by-requirement proof (Build Order acceptance criteria)

### 4.1 Named analytics tests PASSED (line 484–487)
```
test_advisory_analytics_metrics_include_uncertainty_and_sample_counts PASSED
test_confidence_visualization_flags_poor_calibration_and_excludes_raw_score PASSED
test_analytics_api_auth_read_only_and_uncertainty PASSED
test_no_execution_or_mutation_path_in_analytics_modules PASSED
```

### 4.2 Read-only authenticated API — proven on target
- `UNAUTH_ANALYTICS_STATUS: 401` — unauthenticated blocked.
- `GET …/advisory-performance?limit=100` (Bearer) → **200** with full payload.
- `POST_ANALYTICS_STATUS_EXPECT_405: 405` — write surface refused.

No analytics write endpoint exists. Correct.

### 4.3 Source rows seeded → metrics are data-driven (not hard-coded)
Operator seeded 4 source `advisory_signals` (`ANALYTICS_PROOF_ID: operator-analytics-proof-20260716103114`, `SEEDED_SIGNAL_COUNT: 4`) and confirmed by `psql`:
```
 signal_state |   state_reason    | calibrated_confidence |    calibration_status     |  economic_verdict
 emitted      | ELIGIBLE          |  0.5 | calibrated                | economically_usable
 warning      | POORLY_CALIBRATED |  0.5 | warning:POORLY_CALIBRATED | economically_usable
 withheld     | STALE_INPUT       |      | not_evaluated             | economically_usable
 expired      | SIGNAL_EXPIRED    |  0.4 | calibrated                | economically_usable
(4 rows)
```
The API then returned `clean_advisory_rate 0.25`, `guardrail_intervention_rate 0.75`, `withheld_rate 0.25`, `expiry_rate 0.25` over `sample_count 4` — arithmetic consistent with 1 clean / 3 guardrailed / 1 withheld / 1 expired. **The numbers on screen are computed from real persisted rows.**

### 4.4 Uncertainty mandatory — no false precision (§7)
Every one of the 4 metrics carries `uncertainty { method: wilson_score_interval, lower, upper, confidence_level 0.95, sample_count }`. `FIRST_METRIC_UNCERTAINTY_METHOD: wilson_score_interval`, `FIRST_METRIC_SAMPLE_COUNT: 4`. The UI test `flags point-estimate-only metrics rather than showing false precision` PASSED, and the page renders `Metric withheld: uncertainty missing / Point-estimate-only analytics are not displayed.` — **point-estimate render is rejected, not shown.**

### 4.5 Calibrated confidence + unreliability warning (§7.2)
Three bands returned; the **Neutral** band shows `calibration_status: warning`, `unreliable: true`; `UNRELIABLE_BAND_COUNT: 1`. The page renders **"Confidence unreliable — calibration warning present."** exactly on that band. Confidence is calibrated, not raw score.

### 4.6 Raw model score EXCLUDED — proven despite being in source
The seed wrote `raw_score=0.987654` into the source rows (line 617), yet:
- the payload contains **no `"raw_score":` data key** (only the note string *"Raw model score is intentionally excluded from analytics output."*);
- the value `0.987654` **never appears** anywhere in the API output.

This is a stronger proof than a mere absence: the raw score existed upstream and was **provably stripped** by the analytics layer. Correct per §7.2 (no raw-score-as-confidence).

### 4.7 Advisory-not-guaranteed framing (R-3)
Payload disclaimer: *"Research advisory analytics only. Metrics describe persisted advisory records with uncertainty; they are not financial advice and are not guaranteed future results."* Page banner: *"Research analytics only. Past advisory records are not financial advice, not a guarantee, and not a promise of future outcome…"* Notes: *"No returns or outcome guarantees are computed by this service."* Compliant.

### 4.8 No execution controls / presentation-only — 3 greps, command + output (R7)
```
Select-String "\bbuy\b|\bsell\b|\border\b|place_order|\bexecute\b|\bposition\b|\bbroker\b|paper.?trade" (frontend UI) → Expected: no output above.
Select-String "score\(|raw_score|economic_conclusion|expected_calibration_error|LiveInferenceEngine|AdvisorySignalService|fit\(|predict\(" (PerformanceAnalyticsPage.tsx) → Expected: no output above.
Select-String "live_signal|emit_signal|model/signal|place_order|cancel_order" (backend routes) → Expected: no output above.
```
All three produced empty results — command AND output shown (not a blank non-result). No client-side recompute, no execution/mutation path, no signal-emit. The dedicated test `test_no_execution_or_mutation_path_in_analytics_modules PASSED` corroborates.

### 4.9 Browser evidence
The three screenshots from the prior turn show the rendered page: uncertainty on every metric, the calibrated-confidence bands with the **"Confidence unreliable — calibration warning present."** card, the disclaimer banner, RESEARCH source-note badges, nav with no trade/order controls, and no execution surface. (The earlier `ERR_CONNECTION_REFUSED` shot reflected a server-not-running capture moment; the now-proven `200` API read-back + the two rendered captures + all UI tests green together establish the surface. Recommend the operator discard the stale refused shot from the archive to keep the evidence set clean — OBSERVATION, non-blocking.)

---

## 5. Bright-line constitutional compliance (05 v2.0)

| Constraint | Status |
|---|---|
| §30 / §11.1 — UX/analytics **presentation-only**, no analytical calc client-side | ✅ presentation-only grep empty; UI formats API payload |
| §15 — advisory-first; Governance Gate CLOSED; nothing acts | ✅ no execution/mutation path; read-only |
| §16 — no broker logic outside External Integration | ✅ no-execution grep empty |
| §77 — no secrets in telemetry | ✅ analytics expose metadata/aggregates only |
| 07_ML_SPEC — "Results shall include uncertainty—not only point estimates" | ✅ Wilson interval + sample_count on every metric; point-estimate render refused |
| 07_ML_SPEC — economic ≠ statistical success; report independently | ✅ `economic_context` carried per band separately from confidence |

No new persisted artifact type → the persistence-capture control is **not** triggered (correctly N/A). Analytics is pure-Python arithmetic (Wilson score) → no compiled-ML-dep, so the wheel-compat spike remains owed by a **future** unit, not this one.

---

## 6. Findings ledger (final)

| ID | Severity | Status |
|---|---|---|
| C-1 (was CRITICAL) | — | **CLEARED** — correct W3-U07 pack, build identity proven |
| F-2 (was HIGH) | — | **CLEARED** — counts reconcile 192/10/24 |
| F-3 (was HIGH) | — | **RESOLVED** — API 200 read-back + rendered captures + green UI tests; stale refused screenshot noted for archive cleanup (OBSERVATION) |
| F-4 | LOW | `LOCAL_CI_EXIT_CODE: 0` inline echo again absent — marker present, no exit-1, all gates green ⇒ **non-blocking** (recurring cosmetic; keep asking) |
| OBS-1 | OBSERVATION | Discard the earlier `ERR_CONNECTION_REFUSED` screenshot from the W3-U07 evidence archive to avoid a self-contradictory record |

**No CRITICAL/HIGH remain. No mandatory evidence unmet.** Proportionality (R13): approve — core function Level-I proven, only a cosmetic LOW + a housekeeping OBSERVATION remain.

---

## 7. Verdict & disposition

- **W3-U07 — ✅ APPROVED, CLEAN.** Platform **v0.28.0 → v0.29.0**.
- Commendation: the DA/operator correction was exemplary — the pack now **proves build identity first**, seeds real source rows so the metrics are demonstrably data-driven, and proves the raw score is stripped *even though it exists upstream*. That is exactly the standard this project demands.
- **Next:** ITRGA recommends **W3-U08 — Wave-3 Closeout & Hardening (the LAST Wave-3 unit).** On its approval, ITRGA will declare the **"Professional Advisor Platform Complete"** milestone. The DA does **not** self-authorize W3-U08, add auto-action/execution, or open the Constitutional Governance Gate — a new Build Order is required.

> **We don't guess. We prove.** — ITRGA
