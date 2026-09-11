# BUILD ORDER — UI-004-P03
## Intelligence Report Viewers & Drilldowns (progressive disclosure · no recompute · first-party)

**Issuing authority:** Institutional Technical Review & Governance Authority (ITRGA)
**To:** Development Authority (DA)
**Programme:** AXIOM Institutional UI Transformation · **Workstream:** UI-004 · **Phase:** P03
**Predecessor:** `ITRGA_REVIEW_UI-004-P02b.md` — **APPROVED** (authorizes this order)
**Governing:** Doc 12 §6; W4/W7 report constitution (uncertainty/lineage/report_hash/method-version/limitations); design plan §7.1/§7.2/§12 (UI-004-P03); binding refinements **R-6/R-7**; **Doc 16 brand gate (B-1…B-7)**.
**Baseline (must be unchanged):** v0.62.0 · Alembic head `20260717_0037` · backend 414 · frontend 39f/165t.
**Motto:** *We don't guess. We prove.*

---

## 1. Objective
Create **first-party institutional report viewers and drilldowns** over **existing W4/W7 report payloads** — a drilldown being **progressive disclosure of stored fields**, never recomputation/re-derivation/reclassification/external-renderer/LLM-summary. Presentation only: no new backend/API/schema/dependency, no execution, no external AI, Gate CLOSED.

## 2. Scope IN (per accepted plan UI-004-P03)
1. **Report family navigation** — over existing report families (correlation/regime/scenario/portfolio-risk/validation/calibration/economic/generalization) from existing read APIs.
2. **Report detail viewer** — first-party institutional viewer rendering the **stored payload** (JSON/report) as-is.
3. **Lineage/integrity fields** — source-artifact ids, **report hashes**, method/version, limitations, uncertainty rendered verbatim.
4. **Progressive-disclosure drilldowns** — summary card → selected artifact → detail panel → source/lineage/limitations (plan §7.2). **A drilldown is NOT recompute / model-explanation-generated-in-browser / external-NL-summary / reclassification / signal-generation.**
5. **First-party components** — no external report/renderer dependency.

## 3. Scope OUT (do NOT implement)
- Validation/economic-usefulness integrity panels — P04. Research artifacts/collections/saved-views — P05 (R-2/R-4). 
- Any report **generation**; any recompute/re-derivation/reclassification of stored verdicts; any external renderer/AI/LLM summary; any new backend/API/schema/dependency; any execution; any registry change.

## 4. Constitutional & architectural guardrails (binding)
- **🔴 R-6 no-recompute / drilldown = disclosure (spine)** — viewers render stored report fields as-is; drilldowns disclose stored fields only; **no recompute / no reclassification / no browser/AI-generated summary** (grep + named test).
- **Verbatim integrity** — report hashes, uncertainty, limitations, lineage rendered as stored; no normalization into stronger claims.
- **First-party / UG-15** — no new dependency (no external report/chart/table/markdown/AI renderer); prove via package manifests unchanged.
- **Extend-not-duplicate** — reuse UI-001 shell/panels/overlay + UI-002 nav + existing read APIs; no second nav/palette/overlay; no browser-side analytics engine; Design System tokens only.
- **UG-3** — no backend/API/schema change; head `20260717_0037`; no registry change; UI-only (no-drift substitute).
- **🔴 Doc 16 brand (B-1…B-7)** — palette / typography+monospace (ids/hashes/uncertainty/method-versions) / iconography / institutional-not-retail / a11y (dense report tables + drilldown navigation).
- **Accessibility first-class** (report viewers + drilldowns keyboard/screen-reader); **no regression**.

## 5. MANDATORY EVIDENCE (operator-run on target; blank/errored grep = R7 non-result)
**(a) Build-identity** — `sed -n '1,15p'` of the P03 delivery report; confirm it is OF UI-004-P03.
**(b) Named tests (MUST be DISPLAYED passing by name — verbose reporter):**
  - `test_ui004_report_viewers_render_existing_intelligence_reports_only`
  - `test_ui004_drilldowns_disclose_stored_fields_without_recomputation`
  - `test_ui004_report_viewers_preserve_lineage_uncertainty_limitations_and_hashes`
  - `test_ui004_report_viewers_use_first_party_components_no_new_dependency`
  - `test_ui004_report_viewers_are_keyboard_and_screen_reader_accessible`
**(c) 🔴 No-recompute / drilldown-disclosure proof (R-6)** — grep/test: viewer/drilldown source uses existing report read APIs only; no `inferSignal|runInference|authoritativeRecompute|recompute|recalculat|deriveConfidence|reclassif|summariz.*(ai|llm|gpt)|new .*Engine|/api/v1/orders`; drilldown discloses stored fields (progressive) without recomputation (named test).
**(d) Verbatim-integrity proof** — grep/test that report_hash / uncertainty / limitations / lineage / source_artifact_ids / method-version render as stored (not reclassified).
**(e) First-party / no-new-dependency proof** — `package.json`/`package-lock.json` unchanged (no external report/renderer/markdown/AI lib); first-party viewer components.
**(f) No-actuation source grep** — viewer/drilldown source → clean.
**(g) No-drift substitute (R-7)** — per-phase no-backend/schema/dep test; `alembic current` = `20260717_0037`; no-new-endpoint grep; no registry change.
**(h) Regression (R-7)** — backend `pytest -q` **≥414 passed**; frontend Vitest **FULL SUITE ≥39f/165t all passing, NO test lost** (verify the full-suite total); TS clean; build + bundle delta.
**(i) 🔴 Doc 16 brand (B-1…B-7)** — grep/test + browser: palette/typography+monospace/iconography/institutional-not-retail; no-hardcoded-color grep clean.
**(j) Browser (served session) — R-7** — shots: report family navigation → report detail viewer → **progressive-disclosure drilldown** (summary → artifact → detail → source/lineage/limitations); report hashes/uncertainty/limitations visible; keyboard/screen-reader drilldown; no action controls; Gate CLOSED/research framing + brand; logged-out block.
**(k) Networked CI (R-7)** — `scripts/local_ci.sh` → `==> Local CI equivalent complete` + `LOCAL_CI_EXIT_CODE: 0` (or the TD-W6-CI-AUDIT offline-audit env-flake AFTER substantive gates green — record; disposition via operator).

## 6. Acceptance criteria (Determination: Approved · Approved with Observations · Corrective Actions Required · Rejected)
**Approved** requires: build-identity confirmed; (b) all five named tests displayed passing; (c) no-recompute + drilldown-disclosure proven; (d) verbatim integrity (hashes/uncertainty/limitations/lineage) proven; (e) first-party / no new dependency; (f) no-actuation grep clean; (g) no-drift + head unchanged + no registry change; (h) full-suite regression **≥39f/165t, no test lost** + backend ≥414; (i) Doc 16 brand (B-1…B-7); (j) browser viewers/drilldowns + integrity fields + framing + brand + logged-out; (k) networked CI exit 0 + sentinel (or waived env-flake). **Only Approved / Approved-with-Observations authorizes `BUILD_ORDER_UI-004-P04` (Validation & Economic-Usefulness Integrity Panels — verbatim, no re-derivation).**

*We don't guess. We prove.*
