# ITRGA REVIEW — UI-001-P02
## Navigation Dock & Workflow Routing (registry-driven, permission-aware)

**Authority:** Institutional Technical Review & Governance Authority (ITRGA)
**Programme:** AXIOM Institutional UI Transformation · **Workstream:** UI-001 · **Phase:** P02
**Build Order under review:** `BUILD_ORDER_UI-001-P02.md`
**Evidence pack submitted:** `DELIVERY_REPORT_UI-001-P02.md` (correct), `operator results.md` (**STALE — P01 transcript**), 4 served-session screenshots (P02-relevant).
**Determination:** ⛔ **CORRECTIVE ACTIONS REQUIRED**
**Authorizes:** *nothing* — `BUILD_ORDER_UI-001-P03` is **NOT** authorized until corrected.
**Motto:** *We don't guess. We prove.*

---

## 0. Build-identity verification (done FIRST) — FAILED on the operator evidence
Per standing precedent (operator has previously attached the **previous turn's** `operator results.md`), build-identity is checked before judging pass/fail. Result:

| Artifact | Identity check | Status |
|---|---|---|
| `DELIVERY_REPORT_UI-001-P02.md` | Self-declares Phase **P02**, references `BUILD_ORDER_UI-001-P02.md` + P01 predecessor review | ✅ **OF P02** |
| 4 screenshots | Show P02 Navigation Dock, "Collapse navigation" control, registry metadata in Context Panel | ✅ **P02-relevant** |
| **`operator results.md`** | **865 lines, byte-length identical to the P01 run.** References `BUILD_ORDER_UI-001-P01.md`, `DELIVERY_REPORT_UI-001-P01.md`, `UI-001-P01_ALEMBIC_CURRENT.txt`, `UI-001-P01_FRONTEND_TESTS_VERBOSE.txt`, `UI-001-P01_BROWSER\...`, `UI-001-P01_LOCAL_CI_TRANSCRIPT.txt`. **Zero** of the four mandatory P02 named tests present (`grep -c` = 0). Tail is the P01 CI run. | ⛔ **STALE — P01 TRANSCRIPT** |

**Governing rule (mandatory-evidence):** operator-run evidence on the target is MANDATORY; report-claims alone are Level-IV (lowest tier) and can NEVER approve; a stale/mismatched pack is a **non-result (R7)**. ITRGA will **not** evaluate P02 against P01 evidence. Accordingly, none of the P02 engineering gates can be marked proven.

---

## 1. What the delivery report CLAIMS (Level-IV — noted, not accepted as proof)
The `DELIVERY_REPORT_UI-001-P02.md` is coherent and correctly scoped. It claims:
- Registry widened to the **14 canonical fields** (`id, displayName, navigationCategory, route, icon, rbac, defaultLayout, contextPanel, activityDock, search, keyboardShortcut, telemetryId, workspaceVersion, featureFlag`) + guard fields `requiresAuth`/`noActuation`; all 15 routes registered.
- `navigation/navigationGenerator.ts` (`canAccessWorkspace`, `featureFlagEnabled`, `visibleWorkspaces`, `generateNavigationSections`, `createWorkspaceActivationEvent`).
- `navigation/NavigationDock.tsx` + `.test.tsx` (category grouping, active indicator, expand/collapse, ArrowUp/Down keyboard, RBAC/feature filtering, no actuation).
- Deterministic activation seam in the shell.

These are **claims**, not evidence. Under the constitution they cannot substitute for operator-run proof.

## 2. What the SCREENSHOTS positively corroborate (partial, browser-only)
Genuinely useful and consistent with the claims:
- **Navigation Dock (Region B)** rendered with **"Collapse navigation"** control + MONITOR/RESEARCH **category grouping** + active-workspace indicator.
- **14-field registry is visibly exercised**: Context Panel surfaces per-route registry metadata — `/` → Category **Monitor**, Shortcut **Alt+O**, Telemetry `workspace.monitor.operations`; `/research-management` → Category **Review**, Shortcut **Alt+T**, Telemetry `workspace.review.research_management`; `/signals` → Category **Research**, Shortcut **Alt+S**, Telemetry `workspace.research.advisory_signals`.
- **Gate CLOSED / RESEARCH-ONLY** framing (R-5) intact; **logged-out `/login` block** (R-6) intact; no actuation controls visible.

This raises confidence the implementation is real and on the right track — but the browser view **cannot** demonstrate: the four named tests passing, no-manual-nav grep, no-actuation *source* grep, backend/frontend regression totals, alembic head, empty backend diff, or CI. Those require the operator transcript.

## 3. Evidence gaps blocking Approval (all because the P02 transcript is missing)
Not proven (stale pack): **(d)** four named tests displayed passing — `test_navigation_generated_from_registry_not_hardcoded`, `test_navigation_dock_contains_no_execution_or_actuation`, `test_navigation_permission_filtering_hides_unauthorized_workspaces`, `test_workspace_activation_is_deterministic_for_all_routes`; **(b)** 14-field registry type grep; **(c)** navigation-registry-generated / manual-nav-absent grep; **(e)** no-actuation source grep clean; **(f)** backend ≥413 + frontend grown regression; **(g)** `alembic current` = `20260717_0037` + empty backend diff (**OBS-P01-2**); **(h) OBS-P01-1** verbose display of `test_shell_hosts_only_no_business_logic_in_shell`; **(j)** local CI exit line.

## 4. Determination & required corrective action
**CORRECTIVE ACTIONS REQUIRED** — single corrective:

> **CA-P02-1 — Resubmit the CORRECT P02 `operator results.md`** produced by running `docs/evidence/UI-001-P02_OPERATOR_EVIDENCE_COMMANDS.md` (P02 pack) on the target. It MUST contain, inline with command + output: (b) 14-field registry grep; (c) navigation-generated / no-manual-nav grep; (d) all four P02 named tests **displayed passing by name** (verbose reporter); (e) no-actuation grep on nav/dock **source** (test files excluded) → clean; (f) backend `pytest -q` **≥413 passed** + frontend Vitest **>22f/76t** all passing + TS clean + build + bundle delta; (g) `alembic current` printing **`20260717_0037`** + empty `git diff -- backend\app backend\alembic ...`; (h) verbose Vitest **displaying `test_shell_hosts_only_no_business_logic_in_shell` passing by name** (closes carried OBS-P01-1); (j) `LOCAL_CI_EXIT_CODE:` line.

No constitutional or substantive-implementation defect is alleged — the browser evidence is encouraging. This determination is purely **evidence-completeness / build-identity**: the mandatory operator-run proof for P02 was not supplied (the P01 transcript was re-attached). Re-attach the correct file and ITRGA will complete the review, expected to resolve to **Approved** or **Approved with Observations** if the transcript matches the claims.

**No progression:** `BUILD_ORDER_UI-001-P03` remains un-authorized. Baseline unchanged: v0.62.0 / head `20260717_0037` / backend 413 / frontend 22f/76t. Residuals unchanged: TD-W7-U07-RATE-GUARD, TD-W6-CI-AUDIT.

*We don't guess. We prove.*
