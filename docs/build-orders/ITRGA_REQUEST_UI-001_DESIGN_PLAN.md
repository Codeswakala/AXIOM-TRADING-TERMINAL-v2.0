# ITRGA REQUEST FOR UI-001 ENGINEERING DESIGN PLAN — "INSTITUTIONAL WORKSPACE SHELL"

**From:** AXIOM Independent Technical Review & Governance Authority (ITRGA)
**To:** Development Authority (DA), via Operator
**Document type:** Pre-workstream Design Plan Request + Pre-registered UI Guardrails
**Date:** 2026-07-19
**Programme:** Institutional UI Transformation · **Workstream:** UI-001 — Institutional Workspace Shell (Phase I foundation)
**Platform baseline:** v0.62.0 · Alembic head `20260717_0037` · backend **413 passed** · frontend **21 files / 67 tests** · Gate CLOSED · Waves 0–7 CLOSED
**Governing docs (collective, in precedence):** `12_INSTITUTIONAL_UI_TRANSFORMATION_PLAN.md` → `13_UI_TRANSFORMATION_MASTER_PLAN.md` → `14_UI-001_TECHNICAL_DESIGN_SPECIFICATION.md` → `15_UI-001_IMPLEMENTATION_SPECIFICATION.md`; subordinate to the existing constitutional hierarchy + `11_PRODUCTION_READINESS_CERTIFICATION.md`.
**Motto:** *We don't guess. We prove.*

---

## 0. Status & Instruction

ITRGA has assumed constitutional oversight of the UI Transformation Programme. Per the established wave-opening pattern (every wave opened with pre-registered guardrails + an ITRGA-requested Design Plan reviewed **before** any Build Order), **no UI-001 Build Order will be issued until the DA delivers a UI-001 Engineering Design Plan and the ITRGA has reviewed and accepted it** (accept-with-refinements pattern).

UI-001 is the **permanent structural backbone of AXIOM v1.x** (Doc 14 §10 Acceptance Objective). It is **presentation infrastructure only** — it must reveal existing capability through a cohesive institutional workstation **without expanding v1.0 scope** and **without opening the Governance Gate.** The DA shall treat every guardrail below as a first-class acceptance criterion.

---

## 1. PRE-REGISTERED UI-001 GUARDRAILS (binding acceptance criteria)

**Constitutional (carried from Waves 0–7 + Doc 12 §5 / Doc 15 §6-§7):**
- **UG-1 — Gate stays CLOSED / no execution.** The shell introduces **no** execution/order/broker/account/go-live/actuation control or path; no live-execution capability. Any change to Gate state remains a governed act (GOVERNANCE_AMENDMENTS + Operator + ITRGA), never a UI change.
- **UG-2 — Presentation-only; no scope expansion.** No new trading/analysis capability, no new business logic, no new research module, no external AI/LLM, no external service. The shell **consumes** existing capabilities (Doc 15 §7), it does not add them.
- **UG-3 — Backend / API / schema / governance / ML untouched.** No backend business-logic change; no API-contract change without separate approval; no ML-workflow change; no governance-behaviour change; existing DB schema preserved. Prove by diff/grep.
- **UG-4 — No regression of approved capabilities.** All Wave-0–7 features/tests remain green (backend **413**, frontend **21f/67t** baseline); existing routes/pages still function; auth/RBAC/audit/operator-scoping intact.

**Architecture (Doc 14):**
- **UG-5 — One integrated environment (Doc 14 §10, PROHIBITED):** no page-specific navigation; no duplicated application headers; no independent sidebars; no workspace-specific design languages; no competing layout systems; no inconsistent panel behaviour. The shell is the single frame.
- **UG-6 — Regions A–F as specified:** A Global Header · B Navigation Dock · C Primary Workspace · D Context Panel · E Activity Dock · F Overlay Layer — with the composition/hierarchy of Doc 14 §4/§5/§7.
- **UG-7 — State ownership (Doc 14 §10):** Shell owns navigation/layout/routing/auth/notifications/theme; Workspaces own business/research state; Components own presentation/temporary state. No component assumes higher-level state; no business logic in the shell.
- **UG-8 — Routing & persistence integrity:** stable workspace routing; workspace persistence restores the previous session after login (panel visibility/sizes/dock positions/workspace selection/expanded-collapsed). **Persistence reuse note (see R-flags):** any operator-preference persistence should reuse the existing **`operator_workspace_preferences`** (W7-U02) семantics/table where applicable — a NEW table requires the standing persistence-capture control (raw psql SELECT + no-orphan audit JOIN + `operator_id → operators.id`) and justification.

**Institutional UI/UX + non-functional (Doc 12 Part V + Doc 14 §7/§13/§17):**
- **UG-9 — Design-system compliance:** semantic color (green=positive, red=adverse, blue=info, amber=attention, purple=AI/intelligence, gray=neutral) and **never color alone** to convey meaning; typography hierarchy L1 workspace-title→L5 metadata; reusable components belong to the institutional design system; design-token integration.
- **UG-10 — Accessibility foundation (mandatory checkpoint):** full **keyboard navigation** (incl. the global Command Palette), focus management, color-contrast, ARIA/roles; no mouse-only path. Prove.
- **UG-11 — Responsiveness (Doc 14 §13):** progressive adaptation Large-Desktop → Standard → Laptop (Activity Dock collapsed) → Tablet (Context Panel slide-over), preserving workflow continuity; multi-monitor readiness not precluded.
- **UG-12 — Performance foundation:** low navigation latency, predictable behaviour, performant under increasing complexity; no heavy regression in bundle/render.

**Evidence (carried standing):**
- **UG-13 — UI judged in the browser:** mandatory served-session screenshots (shell + regions A–F, navigation, panel dock/resize/persist-restore, responsive tiers, keyboard/command-palette, **no execution/actuation controls**, logged-out block). Sandbox-only/report-claim shots ⇒ Corrective Actions Required.
- **UG-14 — Level-I operator-run evidence + CI:** frontend Vitest + backend regression green (raw transcripts); build succeeds; Git-Bash CI `LOCAL_CI_EXIT_CODE: 0` (offline-`npm audit` = TD-W6-CI-AUDIT env class — fix path/CA or disclose+waive, never `strict-ssl false`). Persistence-capture (raw psql) for any new table — API read-back never substitutes.
- **UG-15 — No unspiked dependency:** any new UI/layout/state/a11y library owes a compatibility + security/no-leak review + ITRGA note; no broker SDK / external-AI package (barred by UG-1/UG-2).

---

## 2. What the Design Plan must contain

The DA shall deliver `UI-001_ENGINEERING_DESIGN_PLAN.md` (or equivalent) containing:

1. **Scope & non-scope** confirmation — mapped to Doc 15 §2 (in: shell/header/nav-dock/primary-workspace/context-panel/activity-dock/overlay/routing/state/panel/persistence/design-tokens/a11y/perf; out: new business/trading/research capability, external service, production deploy/cert) and Doc 14 §8 (out: chart/II/research/governance-workspace/navigator-assistant/artifact-explorer/market-workspace/execution-research redesign + visual refinement — later workstreams).
2. **Region architecture (A–F)** — component decomposition + the composition/hierarchy per Doc 14 §4/§5/§7, and how it replaces the current per-page shell **without** duplicated headers / independent sidebars / competing layouts (UG-5).
3. **Migration strategy** — "incremental migration before wholesale replacement" (Doc 15 §4): how existing pages (Operations, Live Market, Advisory Signals, Institutional Intelligence, Signal Investigation, Scenario Comparison, Trade Planning, Research Journal, Execution Research, Portfolio Research, Research Management, Workspace Customization, Chart Workspace) mount into the shell **without regression**.
4. **State-ownership & routing model** — Shell vs Workspace vs Component ownership (UG-7); routing architecture; workspace-persistence restore.
5. **Persistence plan** — reuse `operator_workspace_preferences` vs. new table; if new, the persistence-capture plan + Alembic head progression from `20260717_0037`.
6. **Design-system + token plan** — semantic color, typography hierarchy, token integration (UG-9).
7. **Accessibility & keyboard plan** — command palette, focus/ARIA, contrast (UG-10); browser-evidence plan (UG-13).
8. **Responsive + performance plan** — the four tiers (UG-11); perf budget/measurement (UG-12).
9. **Unit decomposition** — controlled engineering phases (Doc 15 §9), each independently buildable/testable with checkpoint evidence (Doc 15 §10). **Recommend UI-001's first phase = the shell skeleton + region scaffolding + routing/state seam that proves "one integrated environment" and no-regression BEFORE migrating feature pages** ("prove the frame before hanging the pictures").
10. **Dependency declaration** — any new UI/state/a11y lib + spike/security plan; explicit "no backend/API/schema/governance/ML change; no execution; no external AI" statement.
11. **Regression & evidence plan** — how backend 413 + frontend 21f/67t stay green; browser-evidence matrix (regions, responsive tiers, keyboard, no-actuation, logged-out); CI.

---

## 3. Process from here

1. **DA → Operator → ITRGA:** deliver the UI-001 Engineering Design Plan.
2. **ITRGA:** review line-by-line across all 18 dimensions → `ITRGA_REVIEW_UI-001_DESIGN_PLAN.md` (Approved / Approved-with-Observations / Corrective-Actions-Required / Rejected; binding refinements R-n pre-registered).
3. **On operator authorization (after an Approved/Approved-with-Observations plan):** `BUILD_ORDER_UI-001.md` (first phase — smallest safe slice = shell skeleton + routing/state seam + no-regression proof).
4. **Per phase thereafter:** on "authorized" issue the next phase Build Order; on delivery, verify Level-I evidence + browser shots + verdict + onboarding bump + present. **Only an Approved determination authorizes progression.**

---

## 4. Reviewer posture reminder

- Presentation-only: **Gate CLOSED, no execution/actuation, no scope expansion, no backend/API/schema change, no regression** — a single such violation ⇒ **Rejected** (or Corrective Actions Required for a fixable gap).
- Approval only on **objective, operator-run (Level-I) evidence**; **UI judged in the browser**; report-claims alone are the lowest tier.
- Verify build-identity FIRST (workstream id + version; watch stale/concatenated re-attachments; verify probe tokens before trusting status codes).
- ITRGA issues **corrective observations, not architectural redesign**, unless a constitutional violation requires broader intervention.

---

*We don't guess. We prove.*
**— AXIOM ITRGA**
