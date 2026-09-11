# ITRGA REVIEW — UI-004-P02
## Advisory Signals Integration (read-only · calibrated-confidence · non-actionable — R-3 split, advisory only)

**Authority:** Institutional Technical Review & Governance Authority (ITRGA)
**Programme:** AXIOM Institutional UI Transformation · **Workstream:** UI-004 · **Phase:** P02
**Build Order:** `BUILD_ORDER_UI-004-P02.md`
**Evidence pack:** `DELIVERY_REPORT_UI-004-P02.md`, `operator results.md` (correct UI-004-P02 transcript, 2260 lines), 5 served-session screenshots.
**Determination:** ✅ **APPROVED** (CI env-flake waived by operator)
**Authorizes:** `BUILD_ORDER_UI-004-P02b` (Performance Analytics integration; no-cherry-picking focus).
**Motto:** *We don't guess. We prove.*

---

## 0. Build-identity — PASS
Correct P02 pack: `DELIVERY_REPORT_UI-004-P02.md` Phase UI-004-P02; transcript **41** P02 refs / **26** P01 refs. **R-3 honored** — report L60: "No performance analytics integration was added in P02. P02b remains separate per R-3." DA does not self-approve.

## 1. Verification matrix (Level-I, line-by-line)
| # | Requirement | Evidence (line) | Verdict |
|---|---|---|---|
| **R-3 split (advisory only)** | analytics deferred to P02b | report L60/L128; no analytics integration in P02 | **PASS** |
| (b) Named tests displayed passing (full suite) | verbose reporter | signals_render_existing_records_read_only_with_guardrails (L118) · **signals_show_calibrated_confidence_not_raw_score** (L263) · signal_analytics_accessibility_and_brand_markers_hold (L544) · **signals_and_analytics_do_not_recompute_or_cherry_pick** (L1098) · **signal_surfaces_contain_no_execution_order_or_gate_path** (L1101) — all ✓ with timings in full run (the `↓` at L120/121 were filtered `-t` runs, not skips in the full suite) | **PASS (all 5)** |
| **(c) 🔴 No-recompute + calibrated-confidence (R-6)** | fetch-only, no re-derivation | signal source uses `fetchAdvisorySignals` only (L611); no-recompute/execution grep → **"Expected: no output above."** (L39–40); advisory source declares `posture: "Read-only signal context; calibrated confidence only"` (L1) | **PASS** |
| (d) No-actuation source grep | clean | `buy\|sell\|place_order\|execute\|...\|open_gate` → no output | **PASS** |
| (e) Guardrail/disclaimer render | preserved | grep `not financial advice\|not a trade instruction\|operator decides\|state_reason\|operating_domain_status\|calibration_status\|economic_verdict\|model_artifact_id\|...report_id` present; browser shows STORED GUARDRAILS + LINEAGE + disclaimers | **PASS** |
| (f) No-drift + no registry change | head + registry | `alembic current` = `20260717_0037`; package manifests unchanged; no registry change; no new endpoint | **PASS** |
| (g) Full-suite regression + growth (R-7) | ≥37f/156t, no test lost | full `vitest run` → **38 files / 161 tests passed** (L1081–1082; Tee'd file L1105–1106) = +1 file/+5 tests, no loss; backend **414 passed** (L1627, L2247) | **PASS** |
| **(h) 🔴 Doc 16 brand (B-1…B-7)** | palette/typography/institutional | `--ix-color-*` tokens + `--font-mono`; institutional-not-retail advisory posture copy; no-hardcoded-color grep clean; `signal_analytics_accessibility_and_brand_markers_hold` ✓ | **PASS** |
| (i) Browser (served) — R-7 | advisory read-only + calibrated | shots: **ADVISORY SIGNAL RESEARCH CONTEXT** "Advisory posture: Read-only · Calibrated confidence · Non-actionable"; signal cards with state reasons (EXPIRED/WITHHELD/WARNING), **calibrated confidence ("50.0% calibrated"/"Not calibrated" — never raw score)**, freshness, economic verdict; STORED GUARDRAILS; LINEAGE AND CONTEXT LINKS (model artifact/version/experiment/report ids); nav-only "Open advisory signal/investigation workspace" (non-actionable); "not financial advice… operator decides"; Gate CLOSED/research framing | **PASS** |
| Constitutional line | Gate CLOSED, read-only, no recompute/execution | R-6 grep+tests; calibrated-not-raw; non-actionable | **PASS** |
| (j) Local CI | exit 0 or waived | `LOCAL_CI_EXIT_CODE: 1` — offline `npm audit` `getaddrinfo ENOTFOUND` AFTER **backend 414 + full frontend 38f/161t green** = TD-W6-CI-AUDIT env-flake | **WAIVED by operator** |

## 2. Determination & rationale
**APPROVED (clean; CI env-flake waived).** UI-004-P02 integrates advisory signals as a **read-only, calibrated-confidence, non-actionable** research surface with the no-recompute spine intact: signals are fetched (not re-derived), **calibrated confidence is shown never raw score** (named test + source posture + browser "50.0% calibrated"/"Not calibrated"), state reasons (EXPIRED/WITHHELD/WARNING) and guardrails/lineage/disclaimers render honestly (no-cherry-picking), and there is no execution/actuation (nav-only workspace links). **R-3 was honored** — analytics correctly deferred to P02b. All five named tests pass in the full suite; full-suite regression grew to **38f/161t with no test lost**; backend 414; head unchanged; no dependency/registry change; **Doc 16 brand (B-1…B-7) passes**. The sole non-green item is the offline-audit CI exit-1 — recurring TD-W6-CI-AUDIT — **waived by operator**.

Per the vocabulary, **Approved authorizes progression.** → **`BUILD_ORDER_UI-004-P02b` (Performance Analytics integration) is authorized** — the no-cherry-picking surface, carrying **R-6** (no-recompute) + **R-7** (Level-I + Doc 16 + full-suite ≥ baseline) with emphasis on sample-counts/uncertainty/limitations/scope visibility and no aggregate computed from displayed rows.

Baseline of record: v0.62.0 · head `20260717_0037` · backend **414** · frontend **38f·161t**. Residuals unchanged & non-blocking: TD-W7-U07-RATE-GUARD, TD-W6-CI-AUDIT, UI-002-P04b.

*We don't guess. We prove.*
