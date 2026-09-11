# BUILD ORDER — UI-002-P04
## Global Search Framework · Read-Only Source Adapters · Search Overlay (R-2 / R-5)

**Issuing authority:** Institutional Technical Review & Governance Authority (ITRGA)
**To:** Development Authority (DA)
**Programme:** AXIOM Institutional UI Transformation · **Workstream:** UI-002 · **Phase:** P04
**Predecessor:** `ITRGA_REVIEW_UI-002-P03.md` — **APPROVED WITH OBSERVATIONS** (authorizes this order)
**Governing:** Doc 12 §4; Doc 15 Part V §11 (searchable entities); design plan §5/§10 (UI-002-P04); binding refinements **R-2/R-5/R-6**; hard intake gate **OBS-P03(UI002)-1**.
**Baseline (must be unchanged):** v0.62.0 · Alembic head `20260717_0037` · backend 414 · frontend 29f/115t.
**Motto:** *We don't guess. We prove.*

---

## 0. 🔴 HARD INTAKE GATE (OBS-P03(UI002)-1) — supply FIRST, or review does not begin
Before any substantive P04 review, the `operator results.md` MUST contain, as its **first evidence lines**, cleanly-printed:
- `SCOPED_DIFF_NO_MATCHING_FILENAMES` — from scoped `git diff --name-only -- backend\app backend\alembic backend\pyproject.toml backend\requirements.txt frontend\package.json frontend\package-lock.json` (run as a **single simple command** → file → `type`/`Get-Content`; NOT a multi-line block that trips `NativeCommandError`).
- `alembic current` output line matching **`20260717_0037`**.

If these two outputs are absent, ITRGA returns **Corrective Actions Required** without evaluating the rest (this gap has recurred twice).

## 1. Objective
Provide **global search** over registered workspaces and **existing read-only artifacts** — **read-only jump-to navigation results only** — with **no backend expansion.** Presentation/navigation only: no new backend/API/schema/ML/governance, no execution/actuation, Gate CLOSED.

## 2. Scope IN (per accepted plan UI-002-P04 + R-2)
1. **`GlobalSearchResult` model** — type-enforced `resultAction: "navigate"`, `readonly: true`; no executable callback other than route navigation; no secret/privileged payload.
2. **First-party search ranking/index utility** — ephemeral **client-side** index (debounce, min query length, caps, in-memory TTL, AbortController); **first-party deterministic matching, NO fuzzy-search dependency** (UG-15).
3. **🔴 R-2 — FIRST SLICE SOURCES LIMITED to: workspace (registry) + signals + journal + research-collections.** The remaining adapters (intelligence, scenario, portfolio, chart-annotations, trade-plans, execution-research) are **P04b**, added only after this slice's read-only pattern is accepted. Sources use **existing read APIs only**.
4. **Region-F global search overlay/search mode** — reuse the single UI-001 overlay family (R-4); no independent search shell.
5. **Keyboard + screen-reader behavior** — result list keyboard-navigable; result announcement; focus management.

## 3. Scope OUT (do NOT implement)
- **Any backend search index, new endpoint, table, migration, or column** — search is client-side over existing read APIs (a backend index would require a separate dedicated persistence/endpoint review, not this order).
- Sources beyond the R-2 first slice (that's P04b); context-aware completion (P05).
- Any mutation/action from a search result; any execution/actuation/AI/plugin; any new dependency; any second overlay/search shell.

## 4. Constitutional & architectural guardrails (binding)
- **🔴 R-5 (top risk — hidden action surface)** — search results are **read-only navigation targets**; result selection must not POST/PUT/PATCH/DELETE/execute/approve/connect/place/size/allocate/open-Gate. Type-enforced + named tests + no-actuation grep.
- **R-2** — first-slice sources only (workspace/signals/journal/research-collections).
- **R-4** — one overlay infra; search overlay reuses Region-F; no second overlay/command system.
- **UG-3/UG-15** — no backend/API/schema change; **no new dependency** (esp. no fuzzy-search lib) without a spike; head `20260717_0037`; UI-only diff.
- **No query/artifact persistence** — search query text and artifact payloads are **never persisted** (consistent with R-3).
- **Accessibility first-class**; **no regression** (all UI-001/UI-002-P01/P02/P03 tests green).

## 5. MANDATORY EVIDENCE (operator-run on target; blank/errored grep = R7 non-result)
**(a) 🔴 OBS-P03(UI002)-1 intake gate** — the two cleanly-printed outputs from §0 (scoped-diff sentinel + `alembic current` = `20260717_0037`), FIRST.
**(b) Build-identity** — `sed -n '1,15p'` of the P04 delivery report; confirm it is OF UI-002-P04.
**(c) Read-only result model proof (R-5)** — source showing `GlobalSearchResult` with `resultAction:"navigate"` / `readonly:true` and no non-navigation callback; a test asserting no mutation/action result can be registered.
**(d) R-2 first-slice proof** — grep/test showing search sources are exactly **workspace + signals + journal + research-collections** (no other adapters wired this phase); sources use existing read APIs (no new endpoint).
**(e) No-backend-expansion proof** — grep over search source for `fetch(`-to-new-endpoint / new-table / `/api/v1/<new>` shows only existing read APIs; **no new search endpoint/table/migration**; empty backend/schema diff.
**(f) No-actuation + no-persistence grep** — search source (tests excluded): `buy|sell|place_order|execute|...|open_gate` → clean; and no persistence of query text/artifact payloads.
**(g) Named tests (MUST be DISPLAYED passing by name — verbose reporter):**
  - `test_ui002_global_search_returns_read_only_navigation_results`
  - `test_ui002_global_search_uses_workspace_registry_and_existing_read_sources`
  - `test_ui002_global_search_never_registers_mutation_or_actuation_results`
  - `test_ui002_global_search_does_not_persist_query_text_or_artifact_payloads`
  - `test_ui002_global_search_accessibility_keyboard_and_result_announcement`
  - `test_ui002_global_search_adds_no_backend_schema_or_dependency_change`
**(h) No new dependency (UG-15)** — `package.json`/`package-lock.json` unchanged (no fuzzy-search lib); first-party matching.
**(i) Regression** — backend `pytest -q` **≥414 passed**; frontend Vitest **>29f/115t** all passing; TS clean; build + bundle delta.
**(j) Browser (served session) — R-6** — shots: global search overlay open; a query returning **read-only jump-to** results across **workspace + ≥3 of {signals, journal, research-collections}**; selecting a result **navigates only** (lands on the route, no mutation); keyboard operation; Gate CLOSED/research framing; logged-out block.
**(k) Networked CI (R-6)** — `scripts/local_ci.sh` → `==> Local CI equivalent complete` + `LOCAL_CI_EXIT_CODE: 0`.

## 6. Acceptance criteria (Determination: Approved · Approved with Observations · Corrective Actions Required · Rejected)
**Approved** requires: **(a) OBS-P03(UI002)-1 intake gate satisfied** (else Corrective, no further eval); build-identity confirmed; (c) read-only result model (R-5) + no-mutation test; (d) R-2 first-slice sources only; (e) no-backend-expansion + empty backend/schema diff; (f) no-actuation + no-query-persistence grep clean; (g) all six named tests displayed passing; (h) no new dependency; (i) regression green with actual totals; (j) browser read-only jump-to across the first-slice sources + framing/logged-out; (k) networked CI exit 0 + sentinel. **Only Approved / Approved-with-Observations authorizes `BUILD_ORDER_UI-002-P05` (Context-Aware Workflow Integration & UI-002 Completion Checkpoint) — and/or a P04b for the remaining search adapters.**

*We don't guess. We prove.*
