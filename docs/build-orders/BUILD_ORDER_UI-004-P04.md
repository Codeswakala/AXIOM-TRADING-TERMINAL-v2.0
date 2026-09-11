# BUILD ORDER — UI-004-P04
## Validation & Economic-Usefulness Integrity Panels (verbatim verdicts · no re-derivation · no-cherry-picking)

**Issuing authority:** Institutional Technical Review & Governance Authority (ITRGA)
**To:** Development Authority (DA)
**Programme:** AXIOM Institutional UI Transformation · **Workstream:** UI-004 · **Phase:** P04
**Predecessor:** `ITRGA_REVIEW_UI-004-P03.md` — **APPROVED** (authorizes this order)
**Governing:** Doc 12 §6; W2/W4 validation + economic-usefulness constitution; design plan **§2.2 (verbatim rendering table)** / §7.1 / §7.3 / §12 (UI-004-P04); binding refinements **R-6/R-7**; **Doc 16 brand gate (B-1…B-7)**.
**Baseline (must be unchanged):** v0.62.0 · Alembic head `20260717_0037` · backend 414 · frontend 40f/170t.
**Motto:** *We don't guess. We prove.*

---

## 1. Objective
Provide dedicated **validation & economic-usefulness integrity panels** that render **stored verdicts VERBATIM** and preserve the **no-cherry-picking** discipline. This is the verbatim-verdict surface — the highest-risk *interpretation* boundary of UI-004. Presentation only: no re-derivation/reinterpretation/upgrade of any verdict, no client-side analytics engine, no new backend/API/schema/dependency, no execution, no external AI, Gate CLOSED.

## 2. Scope IN (per accepted plan UI-004-P04)
1. **Validation / economic-usefulness sections** for selected signals/reports (from existing read APIs / report payloads).
2. **Stored statuses/verdicts visible verbatim** — per plan §2.2: `research_only`→"Research-only" (NOT tradable/executable); `not_assessed`→"Not assessed" (NOT economically usable); `warning:POORLY_CALIBRATED`→"Warning: poorly calibrated" (NOT approved/reliable). **Warning states remain warnings.**
3. **Limitations / sample counts / scope visible** (no-cherry-picking).
4. **No status reinterpretation** — the UI may explain where a value came from + show limitations; it may **not** reclassify/relabel/normalize into stronger claims or infer higher-confidence.

## 3. Scope OUT (do NOT implement)
- Research artifacts/collections/saved-view persistence — P05 (R-2/R-4). Completion checkpoint — P06.
- Any re-derivation/recompute/upgrade/reclassification of validation or economic-usefulness verdicts; any client-side analytics engine; any new backend/API/schema/dependency; any execution; any external AI; any registry change.

## 4. Constitutional & architectural guardrails (binding)
- **🔴 R-6 verbatim / no-re-derivation (spine)** — validation statuses + economic-usefulness verdicts rendered **exactly as stored**; **no re-derivation / no upgrade / no reclassification** (grep + named tests). Forbidden-rendering (per §2.2) must be impossible: a stored `not_assessed` can never present as "economically usable," etc.
- **No client-side analytics engine** — panels compute nothing; a named test asserts no analytics engine in the panel path.
- **No-cherry-picking** — sample counts / scope / limitations visible; warnings preserved as warnings.
- **Research-only disclaimers** preserved.
- **Extend-not-duplicate** — reuse UI-001/UI-002 shell/nav + existing read APIs; Design System tokens only.
- **UG-3/UG-15** — no backend/API/schema change; no new dependency; head `20260717_0037`; no registry change; UI-only (no-drift substitute).
- **🔴 Doc 16 brand (B-1…B-7)** — palette / typography+monospace (verdicts/statuses/sample-counts) / iconography / institutional-not-retail / a11y (non-color status labels — never color alone).
- **Accessibility first-class**; **no regression**.

## 5. MANDATORY EVIDENCE (operator-run on target; blank/errored grep = R7 non-result)
**(a) Build-identity** — `sed -n '1,15p'` of the P04 delivery report; confirm it is OF UI-004-P04.
**(b) Named tests (MUST be DISPLAYED passing by name — verbose reporter):**
  - `test_ui004_validation_statuses_are_rendered_verbatim_from_existing_artifacts`
  - `test_ui004_economic_usefulness_verdicts_are_not_rederived_or_upgraded`
  - `test_ui004_no_cherry_picking_sample_counts_scope_and_limitations_visible`
  - `test_ui004_validation_economic_panels_contain_no_client_side_analytics_engine`
  - `test_ui004_validation_economic_panels_preserve_research_only_disclaimers`
**(c) 🔴 Verbatim / no-re-derivation proof (R-6 §2.2)** — grep/test: panel source renders stored verdict/status fields as-is; no `recompute|recalculat|reclassif|deriveConfidence|upgrade.*verdict|normaliz.*(verdict|status)|new .*Engine|/api/v1/orders`; a **named test proving a stored `not_assessed`/`research_only`/`warning:*` is NOT reclassified/upgraded**.
**(d) No-cherry-picking proof** — grep/test that sample counts + scope + limitations render; warnings remain warnings; no aggregate computed from displayed rows.
**(e) No-actuation source grep** — validation/economic panel source → clean.
**(f) No-drift substitute (R-7)** — per-phase no-backend/schema/dep test; `alembic current` = `20260717_0037`; package manifests unchanged; no-new-endpoint grep; no registry change.
**(g) Regression (R-7)** — backend `pytest -q` **≥414 passed**; frontend Vitest **FULL SUITE ≥40f/170t all passing, NO test lost** (verify the full-suite total); TS clean; build + bundle delta.
**(h) 🔴 Doc 16 brand (B-1…B-7)** — grep/test + browser: palette/typography+monospace/iconography/institutional-not-retail; **never color alone** (non-color status labels); no-hardcoded-color grep clean.
**(i) Browser (served session) — R-7** — shots: validation + economic-usefulness panels rendering **verbatim verdicts** (`research_only`/`not_assessed`/`warning:*` shown as-is), sample counts + limitations + scope visible, warnings preserved, research-only disclaimers; no action controls; Gate CLOSED/research framing + brand; logged-out block.
**(j) Networked CI (R-7)** — `scripts/local_ci.sh` → `==> Local CI equivalent complete` + `LOCAL_CI_EXIT_CODE: 0` (or the TD-W6-CI-AUDIT offline-audit env-flake AFTER substantive gates green — record; disposition via operator).

## 6. Acceptance criteria (Determination: Approved · Approved with Observations · Corrective Actions Required · Rejected)
**Approved** requires: build-identity confirmed; (b) all five named tests displayed passing; (c) verbatim / no-re-derivation proven (**a reclassified/upgraded verdict ⇒ Corrective**); (d) no-cherry-picking (sample counts/scope/limitations visible; warnings preserved); (e) no-actuation grep clean; (f) no-drift + head unchanged + no dep + no registry change; (g) full-suite regression **≥40f/170t, no test lost** + backend ≥414; (h) Doc 16 brand (B-1…B-7, never color alone); (i) browser verbatim verdicts + integrity fields + framing + brand + logged-out; (j) networked CI exit 0 + sentinel (or waived env-flake). **Only Approved / Approved-with-Observations authorizes `BUILD_ORDER_UI-004-P05` (Research Artifacts, Collections & Saved-View Preferences; binds R-2 raw-psql if saved-state, R-4 collections read-only).**

*We don't guess. We prove.*
