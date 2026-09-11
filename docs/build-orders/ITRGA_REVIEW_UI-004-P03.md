# ITRGA REVIEW — UI-004-P03
## Intelligence Report Viewers & Drilldowns (progressive disclosure · no recompute · first-party)

**Authority:** Institutional Technical Review & Governance Authority (ITRGA)
**Programme:** AXIOM Institutional UI Transformation · **Workstream:** UI-004 · **Phase:** P03
**Build Order:** `BUILD_ORDER_UI-004-P03.md`
**Evidence pack:** `DELIVERY_REPORT_UI-004-P03.md`, `operator results.md` (correct UI-004-P03 transcript, 2350 lines), 4 served-session screenshots.
**Determination:** ✅ **APPROVED** (CI env-flake waived by operator)
**Authorizes:** `BUILD_ORDER_UI-004-P04` (Validation & Economic-Usefulness Integrity Panels).
**Motto:** *We don't guess. We prove.*

---

## 0. Build-identity — PASS
Correct P03 pack: Phase UI-004-P03; transcript **89** P03 refs / **29** P02b refs; **40** named-test hits. DA does not self-approve.

## 1. Verification matrix (Level-I, line-by-line)
| # | Requirement | Evidence (line) | Verdict |
|---|---|---|---|
| (b) Five named tests displayed passing | verbose reporter | report_viewers_render_existing_intelligence_reports_only (L121) · **drilldowns_disclose_stored_fields_without_recomputation** (L122) · **report_viewers_preserve_lineage_uncertainty_limitations_and_hashes** (L123) · report_viewers_use_first_party_components_no_new_dependency (L124) · report_viewers_are_keyboard_and_screen_reader_accessible (L125) | **PASS** |
| **(c) 🔴 No-recompute / drilldown-disclosure (R-6 §7.2)** | disclose stored fields, no recompute | viewer markers present (`IntelligenceReportViewer`/`Progressive report drilldowns`/`Source lineage and report integrity`, L132); grep `inferSignal\|recompute\|recalculat\|deriveConfidence\|reclassif\|summariz.*(ai\|llm\|gpt)\|new .*Engine\|/api/v1/orders` → **"Expected: no output above."** (L747–748); drilldown test ✓ | **PASS** |
| **(d) Verbatim integrity** | hashes/uncertainty/limitations/lineage as-stored | `report_hash` rendered `className="mono"` (L155, L164); reports keyed off stored `report_id`/`report_hash` (L681) not recomputed; `preserve_lineage_uncertainty_limitations_and_hashes` ✓ | **PASS** |
| (e) First-party / no new dependency | UG-15 | `use_first_party_components_no_new_dependency` ✓; `npm ci` = existing **142 packages**; only existing `lightweight-charts` | **PASS** |
| (f) No-actuation source grep | clean | included in the clean grep block (L747–748) | **PASS** |
| (g) No-drift + no new endpoint/table + no registry change | head + greps | no-backend-expansion grep (`/api/v1/*`/`CREATE TABLE`/`op.create_table`/`new_table`/`createWorkspacePreference`, L755); `alembic current` = `20260717_0037 (head)` (L762); registry unchanged | **PASS** |
| (h) Full-suite regression + growth (R-7) | ≥39f/165t, no test lost | full `vitest run` → **40 files / 170 tests passed** (L1175–1176; Tee'd file L1196–1197) = +1 file/+5 tests, no loss; prior P01/P02/P02b no-recompute tests re-shown passing (L1154/1162/1172); backend **414 passed** (L1717, L2336) | **PASS** |
| (i) 🔴 Doc 16 brand (B-1…B-7) | palette/typography/institutional | `className="mono"` for hashes/ids; palette tokens; institutional report-viewer framing; keyboard/SR accessibility test ✓ | **PASS** |
| (j) Browser (served) — R-7 | viewers/drilldowns + integrity | shots: research workspace in-shell + data-source inventory (Report Viewers source = existing W4/W7 report payloads and hashes) + advisory context; report cards with lineage/hashes/limitations (P01 corroboration); Gate CLOSED/research framing | **PASS** |
| Constitutional line | Gate CLOSED, no recompute/reclassify/AI | R-6 grep+tests; drilldown=disclosure; no external AI/LLM summary | **PASS** |
| (k) Local CI | exit 0 or waived | `LOCAL_CI_EXIT_CODE: 1` — offline `npm audit` `getaddrinfo ENOTFOUND` AFTER **backend 414 + full frontend 40f/170t green** = TD-W6-CI-AUDIT env-flake | **WAIVED by operator** |

## 2. Determination & rationale
**APPROVED (clean; CI env-flake waived).** Intelligence report viewers and drilldowns are delivered as **first-party progressive disclosure of stored fields**: the drilldown test proves stored fields are disclosed **without recomputation**, `report_hash`/`method_version`/lineage/uncertainty/limitations render **verbatim** (mono, keyed off stored ids not recomputed), the no-recompute/reclassify/**AI-summary** grep is clean, and no external report/renderer dependency was added (first-party test + manifests unchanged). No new endpoint/table, head unchanged, no registry change, full-suite regression grew to **40f/170t with no test lost**, backend 414, **Doc 16 brand (B-1…B-7) passes**. The sole non-green item is the offline-audit CI exit-1 — recurring TD-W6-CI-AUDIT — **waived by operator**.

Per the vocabulary, **Approved authorizes progression.** → **`BUILD_ORDER_UI-004-P04` (Validation & Economic-Usefulness Integrity Panels) is authorized** — the verbatim-verdict surface (plan §2.2 permitted-vs-forbidden rendering: stored verdicts shown, never reclassified/upgraded), carrying **R-6** + **R-7**.

Baseline of record: v0.62.0 · head `20260717_0037` · backend **414** · frontend **40f·170t**. Residuals unchanged & non-blocking: TD-W7-U07-RATE-GUARD, TD-W6-CI-AUDIT, UI-002-P04b.

*We don't guess. We prove.*
