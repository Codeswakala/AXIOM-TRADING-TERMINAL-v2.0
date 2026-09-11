# BUILD ORDER — UI-001-P05
## Overlay Layer (Region F) · Notification Service · Command Palette · Accessibility & Token Hardening

**Issuing authority:** Institutional Technical Review & Governance Authority (ITRGA)
**To:** Development Authority (DA)
**Programme:** AXIOM Institutional UI Transformation · **Workstream:** UI-001 · **Phase:** P05
**Predecessor:** `ITRGA_REVIEW_UI-001-P04.md` — **APPROVED WITH OBSERVATIONS** (authorizes this order)
**Governing spec:** `15_UI-001_IMPLEMENTATION_SPECIFICATION.md` **Part IV §11–§13** (Overlay / Notification / Command Palette), **Part VIII §4–§5, §15–§16** (Tokens / Color / Accessibility / Theme), Part V §15; Doc 14 §4 Region F; Doc 12 Part V semantic color.
**Baseline (must be unchanged):** platform v0.62.0 · Alembic head `20260717_0037` · backend 414 · frontend 25f/89t.
**Motto:** *We don't guess. We prove.*

---

## 1. Objective
Complete the **shell overlay family** and make the shell **fully accessible** and **fully token-driven**. This closes the two long-carried observations: **OBS-P01-4** (Region F is the three-layer overlay family: Overlay · Global Dialog · Notification) and **OBS-P01-5** (11 token categories / 18 semantic color roles). Presentation only: **no new backend/API/schema/ML/governance, no new capability, Gate CLOSED, no execution/actuation anywhere.**

## 2. Scope IN
1. **Region F — three-layer overlay family (closes OBS-P01-4 / F-2)** — the shell owns and renders: **Overlay Layer** (drawers/context-menus/confirmation prompts/modal windows — Part IV §11), **Global Dialog Layer**, **Notification Layer**. Workspaces **must not implement independent overlay systems** (§11).
2. **Centralized Notification Service** (Part IV §12) — single service emitting the six types: **Information · Success · Warning · Error · Governance · System**, visually consistent with the Design System; **never color alone** (Doc 12 Part V — pair color with icon/label).
3. **Command Palette** (Part IV §13) — globally accessible (⌘K/Ctrl+K); capabilities limited to **workspace switching · search · navigation · UI toggles (panel/overlay/theme) · operator shortcuts**. 🔴 **CONSTITUTIONAL: "Commands/Quick actions" are NAVIGATION/UI-TOGGLE ONLY — never business, trading, execution, order, broker, account, or Gate actions.** Future workspaces register commands via the Workspace Registration Contract (Part V).
4. **Accessibility hardening (closes R-6 to full, Part VIII §15 / Part V §15)** — WCAG-oriented: keyboard accessibility across overlays/palette (focus trap in modal, ESC to close, focus return), screen-reader support (ARIA roles/labels for dialog/alert/menu), **color contrast**, **reduced-motion** support, focus management, scalable typography.
5. **Token architecture hardening (closes OBS-P01-5 / F-3)** — complete the **11 token categories** (Color, Typography, Spacing, Sizing, Border, Elevation, Shadow, Motion, Opacity, Radius, Icon) and the **18 semantic color roles** (Background, Surface, Primary, Secondary, Accent, Success, Warning, Critical, Information, Border, Disabled, Focus, Selection, Charts, **Governance, Research, Execution Research, Intelligence**). Enforce **"no component defines independent color values"** — grep for hardcoded hex/rgb in shell/overlay/notification source should be clean (tokens only).
6. **Theme infrastructure seam** (Part VIII §16) — Institutional Dark (existing) + a **Light theme** token set; operator theme preference **reuses `operator_workspace_preferences`** (P04 path, `theme_config`) — **NO new table/schema** (R-4). Automatic switching optional/out.

## 3. Scope OUT (do NOT implement)
- Legacy `TerminalLayout` retirement & migration completion — **P06** (final phase).
- Any new table/migration/schema/column (theme pref reuses existing `operator_workspace_preferences.theme_config`).
- Any execution/actuation/broker/account/Gate surface; external AI; new business capability; new business panels.

## 4. Constitutional & architectural guardrails (binding)
- **UG-1/UG-2/R-3 + R-2** — **no execution/actuation anywhere**, and the **command palette is navigation/UI-toggle only** (the R-2 test `test_command_palette_navigation_only_no_business_actions` must remain green + strengthened for the full palette).
- **UG-3/R-1 + R-4** — no backend/API/alembic/schema change; head `20260717_0037` unchanged; theme pref via existing `operator_workspace_preferences` only (no schema creep — prove head + information_schema if alleged).
- **Doc 14 §10 / Part IV §11** — one integrated overlay system; workspaces do not build their own overlays.
- **Doc 12 Part V — never color alone**; semantic roles only; no page-specific colors.
- **UG-15** — no new dependency without a spike (prefer first-party overlay/palette; if a headless a11y primitive lib is proposed, it needs a dependency spike + ITRGA sign-off).
- **No regression** — every route + all P01–P04 tests still green.

## 5. MANDATORY EVIDENCE (operator-run on target; blank/errored grep = R7 non-result)
**(a) Build-identity** — `sed -n '1,15p'` of the P05 delivery report; confirm it is OF P05 (grep P05 markers, not a stale re-attach — I will check).
**(b) Region-F three-layer proof (OBS-P01-4)** — grep/source showing the shell renders Overlay + Global Dialog + Notification layers as shell-owned; a test asserting workspaces cannot mount an independent overlay system.
**(c) Notification service proof** — the six types (Information/Success/Warning/Error/Governance/System) from one centralized service; each pairs color with icon/label (never color alone).
**(d) Command-palette navigation-only proof** — grep + test showing palette entries are navigation/toggle only; **no** execute/order/broker/account/Gate command registered.
**(e) Token hardening (OBS-P01-5)** — grep listing the 11 token categories + 18 semantic color roles present; **no-hardcoded-color grep** over shell/overlay/notification source (tests excluded) → clean (tokens only).
**(f) Accessibility proof (R-6 to full)** — tests + evidence for: focus trap + ESC + focus-return in modal/palette; ARIA roles (dialog/alert/menu); reduced-motion honored; contrast check note. Keyboard-only walkthrough in browser.
**(g) Named tests (MUST be DISPLAYED passing by name — verbose reporter):**
  - `test_region_f_overlay_dialog_notification_all_shell_owned`
  - `test_notification_service_centralized_six_types_never_color_alone`
  - `test_command_palette_navigation_only_no_business_actions` (strengthened; must stay green)
  - `test_overlay_accessibility_focus_trap_esc_and_aria_roles`
  - `test_no_hardcoded_color_all_visual_values_from_tokens`
**(h) Theme via existing table (R-4)** — if theme pref persists, raw psql showing it lives in `operator_workspace_preferences.theme_config` (no new table); `alembic current` = `20260717_0037`.
**(i) Regression** — backend `pytest -q` **≥414 passed**; frontend Vitest **>25f/89t** all passing; TS clean; build + bundle delta.
**(j) Browser (served session)** — shots: command palette open (navigation-only, focus visible); a notification of each/representative types; a modal/dialog with focus trap; **Light theme** applied (if delivered) + persistence across reload; Gate CLOSED/research framing; logged-out block.
**(k) Local CI — NETWORKED (closes OBS-P04-1)** — `& "C:\Program Files\Git\bin\bash.exe" scripts/local_ci.sh` on a connected network → `==> Local CI equivalent complete` + `LOCAL_CI_EXIT_CODE: 0` (audit clean). If offline flake recurs, record — disposition via operator.

## 6. Acceptance criteria (Determination: Approved · Approved with Observations · Corrective Actions Required · Rejected)
**Approved** requires: build-identity confirmed; (b) Region-F three-layer shell-owned (**OBS-P01-4 closed**); (c) centralized 6-type notifications never-color-alone; (d) palette navigation-only proven (constitutional); (e) 11 categories/18 roles + no-hardcoded-color grep clean (**OBS-P01-5 closed**); (f) accessibility focus-trap/ARIA/reduced-motion proven (**R-6 to full**); (g) all five named tests displayed passing; (h) theme (if any) via existing table, head unchanged; (i) regression green with actual totals; (j) browser confirms overlays/notifications/palette/theme/framing/logged-out; no barred/unspiked dependency; (k) networked CI exit 0 + sentinel (**OBS-P04-1 closed**). **Only Approved / Approved-with-Observations authorizes `BUILD_ORDER_UI-001-P06` (Legacy TerminalLayout retirement & UI-001 completion).**

*We don't guess. We prove.*
