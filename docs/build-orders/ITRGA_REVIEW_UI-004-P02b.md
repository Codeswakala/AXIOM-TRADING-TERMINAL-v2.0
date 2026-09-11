# ITRGA REVIEW — UI-004-P02b
## Performance Analytics Integration (no-cherry-picking · no-recompute · read-only)

**Authority:** Institutional Technical Review & Governance Authority (ITRGA)
**Programme:** AXIOM Institutional UI Transformation · **Workstream:** UI-004 · **Phase:** P02b
**Build Order:** `BUILD_ORDER_UI-004-P02b.md`
**Evidence pack:** `DELIVERY_REPORT_UI-004-P02b.md`, `operator results.md` (correct UI-004-P02b transcript, 2377 lines), 4 served-session screenshots.
**Determination:** ✅ **APPROVED** (CI env-flake waived by operator)
**Authorizes:** `BUILD_ORDER_UI-004-P03` (Intelligence Report Viewers & Drilldowns).
**Motto:** *We don't guess. We prove.*

---

## 0. Build-identity — PASS
Correct P02b pack: Phase UI-004-P02b; transcript **86** P02b refs. DA does not self-approve.

## 1. Verification matrix (Level-I, line-by-line)
| # | Requirement | Evidence (line) | Verdict |
|---|---|---|---|
| (b) Four named tests displayed passing | verbose reporter | analytics_render_existing_metrics_with_uncertainty_and_sample_counts (L118) · **analytics_do_not_recompute_or_cherry_pick** (L123) · analytics_surfaces_contain_no_execution_order_or_gate_path (L124) · analytics_accessibility_and_brand_markers_hold (L125) | **PASS** |
| **(c) 🔴 No-recompute + no-cherry-picking (R-6 + W6)** | fetch-only, no aggregate from rows | analytics source uses `fetchAdvisoryAnalytics` + reads `sample_count`/`uncertainty`/`limitations`/`source_artifact_ids`/`included_scope` + "Unreliable calibration warning preserved" (L132); no-recompute/actuation grep → **"Expected: no output above."** (L401–402); `analytics_do_not_recompute_or_cherry_pick` ✓; browser "**No selective performance claim** · Sample counts · uncertainty · limitations visible" + "does not infer, rescore, or produce a browser-side performance metric from displayed signal rows" | **PASS** |
| No-cherry-picking scope visible | sample counts/uncertainty/limitations | browser Stored Metrics: Clean advisory rate 50.0% · Interval 18.8%–81.2% · **Sample count 6** · Method `wilson_score_interval`; Guardrail intervention rate with interval+sample-count | **PASS** |
| (d) No-actuation source grep | clean | InstitutionalIntelligencePage scan → no output (L401–402) | **PASS** |
| (e) No-drift + no new endpoint/table + no registry change | head + greps | `alembic current` = `20260717_0037 (head)` (L782); no-backend-expansion grep (`/api/v1/*`/`CREATE TABLE`/`op.create_table`/`new_table`/`createWorkspacePreference`) L775; registry pre-existing `/intelligence`, no new route (L799–800) | **PASS** |
| (f) Full-suite regression + growth (R-7) | ≥38f/161t, no test lost | full `vitest run` → **39 files / 165 tests passed** (L1033–1034; Tee'd file L1049–1050) = +1 file/+4 tests, no loss; backend **414 passed** (L1744, L2364) | **PASS** |
| **(g) 🔴 Doc 16 brand (B-1…B-7)** | palette/typography/institutional | brand grep (L806): "No selective performance claim" / `className="mono"` / `research-analytics-card-grid`; token grep (L807): `--ix-color-*` + `--font-mono` + `@media (max-width:760px)`; `analytics_accessibility_and_brand_markers_hold` ✓ | **PASS** |
| (h) Browser (served) — R-7 | analytics + uncertainty/samples/warnings | shots: **PERFORMANCE ANALYTICS RESEARCH CONTEXT** "No selective performance claim"; "Research advisory analytics only… not guaranteed future results"; Stored Metrics with intervals + sample counts + `wilson_score_interval`; signal→analytics context; no action controls; Gate CLOSED/research framing | **PASS** |
| Constitutional line | Gate CLOSED, no recompute/execution | R-6 grep+test; no aggregate from rows; no external AI | **PASS** |
| (i) Local CI | exit 0 or waived | `LOCAL_CI_EXIT_CODE: 1` — offline `npm audit` `getaddrinfo ENOTFOUND` AFTER **backend 414 + full frontend 39f/165t green** = TD-W6-CI-AUDIT env-flake | **WAIVED by operator** |

## 2. Determination & rationale
**APPROVED (clean; CI env-flake waived).** Performance Analytics — the no-cherry-picking surface — is integrated read-only with the discipline held decisively: metrics come from `fetchAdvisoryAnalytics` (not recomputed), **sample counts / uncertainty (Wilson intervals) / limitations / included scope are visible**, the panel explicitly makes **"No selective performance claim"** and "does not infer, rescore, or produce a browser-side performance metric from displayed signal rows," and the named `analytics_do_not_recompute_or_cherry_pick` test passes. No execution/actuation, no new endpoint/table, no registry change (R-1), full-suite regression grew to **39f/165t with no test lost**, backend 414, head unchanged, **Doc 16 brand (B-1…B-7) passes**. The sole non-green item is the offline-audit CI exit-1 — recurring TD-W6-CI-AUDIT — **waived by operator**.

Per the vocabulary, **Approved authorizes progression.** → **`BUILD_ORDER_UI-004-P03` (Intelligence Report Viewers & Drilldowns) is authorized**, carrying **R-6** (drilldown = progressive disclosure of stored fields, NOT recompute/LLM-summary/reclassification — plan §7.2) + **R-7** (Level-I + Doc 16 + full-suite ≥ baseline).

Baseline of record: v0.62.0 · head `20260717_0037` · backend **414** · frontend **39f·165t**. Residuals unchanged & non-blocking: TD-W7-U07-RATE-GUARD, TD-W6-CI-AUDIT, UI-002-P04b.

*We don't guess. We prove.*
