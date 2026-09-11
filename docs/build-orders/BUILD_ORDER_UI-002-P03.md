# BUILD ORDER — UI-002-P03
## Command Palette Extension · Quick-Action Catalogue (navigation/UI-toggle only — R-5)

**Issuing authority:** Institutional Technical Review & Governance Authority (ITRGA)
**To:** Development Authority (DA)
**Programme:** AXIOM Institutional UI Transformation · **Workstream:** UI-002 · **Phase:** P03
**Predecessor:** `ITRGA_REVIEW_UI-002-P02.md` — **APPROVED WITH OBSERVATIONS** (authorizes this order)
**Governing:** Doc 12 §4; Doc 15 Part IV §13 (Command Palette); design plan §7/§8/§10 (UI-002-P03); binding refinements **R-4/R-5/R-6**; the ITRGA-vetted **§8 28-action catalogue**.
**Baseline (must be unchanged):** v0.62.0 · Alembic head `20260717_0037` · backend 414 · frontend 28f/109t.
**Motto:** *We don't guess. We prove.*

---

## 1. Objective
Extend the **existing UI-001 Command Palette** with a typed `CommandRegistry` and the **ITRGA-vetted quick-action catalogue** — **navigation / UI-toggle only.** No second palette. Presentation/navigation only: **no new backend/API/schema/ML/governance, no execution/actuation, Gate CLOSED.** This is the most constitutionally sensitive UI-002 phase (it adds *actionable* palette commands); R-5 is the spine of acceptance.

## 2. Scope IN (per accepted plan UI-002-P03)
1. **Typed `CommandRegistry`** — command type **restricted to `"navigation" | "ui-toggle"`** (type-enforced, mirroring the UI-001 palette guarantee). Business/execution command types are **unrepresentable**.
2. **Quick-action catalogue implementation** — implements **only the 28 ITRGA-vetted items** from the accepted Design Plan §8 (16 navigation + 12 ui-toggle). **No item outside the vetted catalogue** may be registered; any addition requires a revised catalogue re-vetted by ITRGA.
3. **Existing `CommandPalette` consumes the registry** — **no second palette, no second overlay** (R-4). Command grouping by workflow stage.
4. **Rejection tests** for prohibited command classes (business/trading/execution/order/broker/account/Gate/external-AI/plugin).

## 3. Scope OUT (do NOT implement)
- Global search (P04/P04b — R-2), context-aware suggestions beyond P02.
- **Any command that is not one of the 28 vetted quick actions**; any business/execution/order/broker/account/Gate/AI/plugin command.
- Any new route/backend/API/schema/migration/column/dependency; any second palette/overlay/command system.

## 4. Constitutional & architectural guardrails (binding)
- **🔴 R-5 (spine)** — quick actions are **navigation/UI-toggle only**; registry **rejects** business/trading/execution/broker/account/Gate actions (type-enforced + explicit rejection test). Global-search-style "hidden action surface" risk applies to the palette here.
- **R-4** — one overlay infra + one command system; extend the existing palette, never a second one.
- **UG-1/UG-2/R-3(UI-002)** — no execution/actuation anywhere (grep + tests).
- **UG-3/UG-15** — no backend/API/schema change; no new dependency without a spike; head `20260717_0037`; UI-only diff.
- **Doc 14 §10** — one integrated environment; the palette is the single global palette.
- **Accessibility first-class** (Doc 15 Part VIII §15 / Part IV §13) — palette keyboard-operable, focus trap, ESC + focus-restore, ARIA.
- **No regression** — every route + all UI-001/UI-002-P01/P02 tests still green.

## 5. MANDATORY EVIDENCE (operator-run on target; blank/errored grep = R7 non-result)
**(a) Build-identity** — `sed -n '1,15p'` of the P03 delivery report; confirm it is OF UI-002-P03.
**(b) Catalogue-fidelity proof** — grep/test showing the registered commands are **exactly the 28 vetted items** (ids `qa.*`), no extras; command grouping present.
**(c) Type-enforcement + rejection proof (R-5)** — source showing `commandType: "navigation" | "ui-toggle"` (no third type); a **rejection test** proving a business/execution/broker/account/Gate command is refused by the registry.
**(d) No-second-palette/overlay proof (R-4)** — grep/test showing the existing `CommandPalette` consumes the registry; no second palette/overlay created.
**(e) No-actuation source grep (R-5)** — palette/command source (tests excluded): `buy|sell|place_order|execute|go-live|connect-broker|account_id|order_ticket|open_gate|allow_execution` → clean.
**(f) Named tests (MUST be DISPLAYED passing by name — verbose reporter):**
  - `test_ui002_command_palette_extends_existing_palette_not_second_palette`
  - `test_ui002_command_registry_accepts_only_navigation_or_ui_toggle_commands`
  - `test_ui002_quick_action_catalogue_is_itemized_and_registered`
  - `test_ui002_quick_actions_are_navigation_or_ui_toggle_only`
  - `test_ui002_command_registry_rejects_business_trading_execution_broker_account_gate_actions`
  - `test_ui002_command_palette_keyboard_focus_and_escape_restore`
**(g) Accessibility** — palette keyboard/focus-trap/ESC/focus-restore test (above) + browser keyboard walkthrough.
**(h) Regression** — backend `pytest -q` **≥414 passed**; frontend Vitest **>28f/109t** all passing; TS clean; build + bundle delta.
**(i) 🔴 UI-only diff + head (folds OBS-P02(UI002)-1)** — **scoped** `git diff --name-only -- backend\app backend\alembic backend\pyproject.toml backend\requirements.txt frontend\package.json frontend\package-lock.json` Tee'd to a file + `Select-String` → **clean, readable "no matching filenames"** (avoid CRLF-warning interleaving); `alembic current` printing **`20260717_0037`**. Prefer `git diff --stat HEAD` (committed baseline) to isolate the P03 delta.
**(j) Browser (served session) — R-6** — shots: command palette open showing **navigation + UI-toggle quick actions grouped by workflow stage**; keyboard focus + ESC; a UI-toggle action (e.g. theme/panel) taking effect; Gate CLOSED/research framing; logged-out block.
**(k) Networked CI (R-6)** — `scripts/local_ci.sh` → `==> Local CI equivalent complete` + `LOCAL_CI_EXIT_CODE: 0`.

## 6. Acceptance criteria (Determination: Approved · Approved with Observations · Corrective Actions Required · Rejected)
**Approved** requires: build-identity confirmed; (b) catalogue-fidelity (exactly the 28 vetted items); (c) type-enforcement + **rejection test** proving business/execution commands refused (R-5); (d) no second palette/overlay (R-4); (e) no-actuation grep clean; (f) all six named tests displayed passing; (g) palette accessibility proven; (h) regression green with actual totals; **(i) clean scoped UI-only diff + `alembic current` = 20260717_0037 (closes OBS-P02(UI002)-1)**; (j) browser palette/quick-actions/keyboard + framing/logged-out; (k) networked CI exit 0 + sentinel; no barred/unspiked dependency. **Only Approved / Approved-with-Observations authorizes `BUILD_ORDER_UI-002-P04` (Global Search Framework; binds R-2 first-slice = workspace+signals+journal+research-collections, read-only jump-to).**

*We don't guess. We prove.*
