# BUILD ORDER — UI-002-P02
## Workspace Switcher · Context-Navigation Seam · Recent-Workspace Persistence (R-3)

**Issuing authority:** Institutional Technical Review & Governance Authority (ITRGA)
**To:** Development Authority (DA)
**Programme:** AXIOM Institutional UI Transformation · **Workstream:** UI-002 · **Phase:** P02
**Predecessor:** `ITRGA_REVIEW_UI-002-P01.md` — **APPROVED (CLEAN)** (authorizes this order)
**Governing:** Doc 12 §4; Doc 15 Part VII §11–§14 (context/deep-link/history); design plan §6/§10 (UI-002-P02); binding refinements **R-3/R-4/R-5/R-6**.
**Baseline (must be unchanged):** v0.62.0 · Alembic head `20260717_0037` · backend 414 · frontend 27f/103t.
**Motto:** *We don't guess. We prove.*

---

## 1. Objective
Let operators **switch registered workspaces by workflow** and see **read-only related-workflow suggestions**, while UI-001 remains the sole shell owner. Presentation/navigation only: **no new backend/API/schema/ML/governance, no execution/actuation, Gate CLOSED.** Any persistence reuses the existing `operator_workspace_preferences` seam (R-3) — **no new table/migration/column.**

## 2. Scope IN (per accepted plan UI-002-P02)
1. **`WorkspaceSwitcher` in Region A** — driven by **RBAC-visible Workspace Registry entries** (reuse UI-001 registry + permission filtering; no second nav).
2. **Context-navigation seam** — a **static** context-navigation map surfaced through the **existing Context Panel / PanelHost** (Region D); suggests **read-only registered routes** only; no business state, no artifact mutation.
3. **Keyboard support + focus restoration** — switcher fully keyboard-operable; focus returns correctly on close.
4. **Recent/previous workspace ids (optional, R-3-governed)** — if implemented, store **route ids only** in the **existing `operator_workspace_preferences.layout_config`** via the P04(UI-001) shell-preference path. **NEVER persist search queries or artifact/business payloads.**

## 3. Scope OUT (do NOT implement)
- Global search (P04/P04b — R-2), command-palette extension & quick-actions (P03 — R-5), context-aware suggestions requiring backend computation.
- Any new route; **any new table/migration/column** (R-3 no schema creep); any new dependency; any execution/actuation/AI/plugin.
- Any modification to UI-001 registry/nav-dock/palette/overlay/token architectural responsibilities.

## 4. Constitutional & architectural guardrails (binding)
- **R-3** — recents persist in **existing `operator_workspace_preferences.layout_config`** only; **no search queries / no artifact payloads**; no schema creep (head unchanged; `information_schema` proof if a column is alleged).
- **R-4** — one overlay infra + one command system; switcher/context-nav reuse existing shell surfaces (no second palette/overlay).
- **R-5** — no execution/actuation in switcher or context-nav (grep + named test); context suggestions are read-only navigation targets.
- **UG-3/UG-15** — no backend/API/schema change; no new dependency without a spike; head `20260717_0037`; UI-only diff.
- **Doc 14 §10** — one integrated environment; switcher in existing Region A, context-nav in existing Region D; no competing layout/duplicate header.
- **Accessibility first-class** (Doc 15 Part VIII §15) — keyboard operation, ARIA, focus restoration.
- **No regression** — every route + all UI-001/UI-002-P01 tests still green.

## 5. MANDATORY EVIDENCE (operator-run on target; blank/errored grep = R7 non-result)
**(a) Build-identity** — `sed -n '1,15p'` of the P02 delivery report; confirm it is OF UI-002-P02 (grep markers; not stale/wrong pack — I will check).
**(b) 🔴 R-3 persistence discipline** — TWO cases, whichever applies, stated explicitly:
  - **If recents ARE persisted:** raw `psql SELECT` on `operator_workspace_preferences` showing the shell-pref row's `layout_config` contains **route ids only** (e.g. a `recent_workspaces` array of route/id strings) and **NO** search queries / artifact payloads / business fields; **no new column** (`alembic current` = `20260717_0037`; `information_schema.columns` on `operator_workspace_preferences` unchanged); reuse of the existing write path (no new endpoint/table). If this is a *new row-shape*, include the no-orphan audit JOIN + `operator_id→operators.id` JOIN (orphan_count 0) — else confirm it rides the existing shell-pref row.
  - **If recents are NOT persisted this phase:** a test/grep proving no persistence write occurs (in-memory/session only), deferring durable recents.
  - **In BOTH cases:** a named test asserting **no search queries or business payloads are persisted**.
**(c) Named tests (MUST be DISPLAYED passing by name — verbose reporter):**
  - `test_ui002_workspace_switcher_uses_registry_and_rbac_visible_entries`
  - `test_ui002_workspace_switcher_preserves_single_ui001_shell_frame`
  - `test_ui002_context_navigation_suggests_read_only_registered_routes_only`
  - `test_ui002_workspace_switching_is_keyboard_operable`
  - `test_ui002_navigation_recents_do_not_persist_search_queries_or_business_payloads`
  - `test_ui002_context_navigation_contains_no_business_actions`
**(d) No-actuation source grep (R-5)** — switcher/context-nav source (tests excluded) → clean.
**(e) No-duplicate-nav / single-shell proof (R-4)** — grep/test showing switcher reuses registry + single shell frame; no second nav/palette/overlay.
**(f) Regression** — backend `pytest -q` **≥414 passed** (incl. `test_workspace_preferences.py` green if recents persist); frontend Vitest **>27f/103t** all passing; TS clean; build + bundle delta.
**(g) UI-only diff + head unchanged** — empty `git diff -- backend\app backend\alembic backend\pyproject backend\requirements frontend\package.json frontend\package-lock.json`; `alembic current` = `20260717_0037`.
**(h) Browser (served session) — R-6** — shots: workspace switcher open (RBAC-visible entries); **keyboard-only** switching; context-panel related-workflow suggestions; if recents persist, show recents restored after re-login; Gate CLOSED/research framing; logged-out block.
**(i) Networked CI (R-6)** — `scripts/local_ci.sh` → `==> Local CI equivalent complete` + `LOCAL_CI_EXIT_CODE: 0`.

## 6. Acceptance criteria (Determination: Approved · Approved with Observations · Corrective Actions Required · Rejected)
**Approved** requires: build-identity confirmed; **(b) R-3 persistence discipline satisfied** (route-ids-only in existing table w/ raw psql if persisted, OR proven non-persistence; no schema creep; no search/business payload) — *a persisted-but-unproven or schema-creeping recents ⇒ Corrective*; (c) all six named tests displayed passing; (d) no-actuation grep clean; (e) single-shell/no-duplicate-nav proven; (f) regression green with actual totals; (g) UI-only diff + head unchanged; (h) browser switcher/keyboard/context + framing/logged-out; (i) networked CI exit 0 + sentinel; no barred/unspiked dependency. **Only Approved / Approved-with-Observations authorizes `BUILD_ORDER_UI-002-P03` (Command Palette Extension & Quick-Action Catalogue; binds R-5 no-mutation).**

*We don't guess. We prove.*
