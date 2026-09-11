# BUILD DIRECTIVE — UI-CONV-P03 · ITEM 6

**Issuing authority:** Independent Technical Review & Governance Authority
**Date:** 2026-08-15
**Scope:** Item 6 only — `SignalInvestigationPage` → signal drill-down details surface
**Base:** `34f4c62` **+ item-3 patch** (`b7b4c4f7…`) **+ item-5 patch** (`4c03910c…`)
**Parent Build Order:** `BUILD_ORDER_UI-CONV-P03` §3 item 6 — *"Details dock, opened from a signal card"*

---

## 1. THE SURFACE

`frontend/src/pages/SignalInvestigationPage.tsx` · **425 lines** · **0 `data-testid`** · 2 endpoints
`fetchAdvisorySignals` · `fetchInstitutionalIntelligenceBundle`

Exports: `UI005_INVESTIGATION_PLANNING_SOURCES` (:49) · `SignalInvestigationWorkspace` (:163) · `SignalInvestigationPage` (:376)

---

## 2. ⚠ READ FIRST — HALF THIS SURFACE ALREADY EXISTS IN THE TERMINAL

`TerminalSignalStream.tsx` already implements a click-to-expand drill-down on each signal card, delivered under `B-CONV2-2`. It renders **five** detail sections with test hooks:

```
signal-detail-rationale-{id}         signal-detail-guardrails-{id}
signal-detail-lineage-{id}           signal-detail-explainability-{id}
signal-detail-risk-{id}
```

Mapping the page's ten capability groups against what the dock already provides:

| # | Page capability | Status |
|---|---|---|
| 1 | Signal Investigation Workspace (frame) | Frame only |
| 2 | Persisted signals | **Already in dock** — the signal list |
| 3 | Investigation Detail | **Already in dock** — expanded card |
| 4 | Rationale | **Already in dock** — `signal-detail-rationale` |
| 5 | Guardrail states | **Already in dock** — `signal-detail-guardrails` |
| 6 | Lineage | **Already in dock** — `signal-detail-lineage` |
| 7 | Safe explainability summary | **Already in dock** — `signal-detail-explainability` |
| 8 | **Linked validation and report ids** | **GAP** — `statistical_report_id`, `calibration_report_id`, `economic_report_id`, `generalization_report_id`, each `?? "—"` |
| 9 | **Related evidence links** | **GAP** — navigation affordances (see §4) |
| 10 | **Linked intelligence reports** | **GAP** — `REPORT_GROUPS` from `fetchInstitutionalIntelligenceBundle`, with an explicit *"No reports returned."* empty state |

**Item 6 is therefore a three-capability extension of an existing drill-down, not a 425-line re-home.** Do not rebuild sections 2–7; they exist, they are tested, and duplicating them would create exactly the parallel-implementation hazard the turn-56 reframe forbids.

**M1 — Extend, do not duplicate.** Add capabilities 8, 9, 10 to the existing expanded signal card (or a details view it opens). If the DA concludes a separate details surface is genuinely better, state the reasoning and explain how duplication of sections 2–7 is avoided.

**M2 — Preserve the `?? "—"` absence markers** on all four report ids (`:323-326`) and the *"No reports returned."* empty state (`:361`). These are honest-absence markers of the same class as `reasonCodeFor`'s `"—"`. Never substitute a plausible-looking id.

---

## 3. ⚠ A BACKEND CONSTITUTIONAL GUARD PINS THIS FILE PATH

Unlike items 3 and 5, a **backend** test hardcodes this page's path:

```python
# backend/tests/test_signal_investigation_workspace.py:151
def test_signal_investigation_workspace_has_no_mutation_or_execution_path() -> None:
    frontend_path = root / "frontend" / "src" / "pages" / "SignalInvestigationPage.tsx"
    ...
    forbidden = ("advisory_status =", "model.status =", "emit_signal", "place_order",
                 "update_signal", "override_guardrail", "broker.", "allow_execution", "gate_open")
```

**M3 — Re-point this test to the new module path in the same patch.**

This is not bookkeeping. It is a **constitutional guard** asserting the investigation surface contains no mutation or execution path — `place_order`, `broker.`, `allow_execution`, `gate_open`. If the file is deleted and the test is not re-pointed, `pytest` fails on a missing file, which is loud and safe. **But if it is re-pointed to a file that does not contain the investigation UI, the guard passes vacuously and the platform loses a T-1 assertion silently.** Point it at the module that actually renders the drill-down.

`backend/tests/test_research_management.py:482` pins `frontend/src/pages` similarly — that one belongs to item 4, not this item. Do not touch it.

**Frontend coupling — re-point, do not delete (M4):**

```
pages/SignalInvestigationPage.test.tsx
workstation/accessibility/accessibilityAudit.test.tsx
workstation/investigation/InvestigationPlanningCompletion.test.tsx
workstation/investigation/InvestigationPlanningFrame.test.tsx
workstation/investigation/SignalInvestigationLineage.test.tsx
workstation/registry/workspaceRegistry.tsx
```

Five suites plus the registry. `accessibilityAudit.test.tsx` imports the page — accessibility coverage of this surface must survive the move.

---

## 4. 🔴 DEFECT IN ALREADY-APPROVED WORK — `OBS-CONV3-10`

Found during this inventory. **Not caused by item 6; item 6 is the right place to fix it.**

The page's "Related evidence links" are raw anchors:

```
<a className="btn" href="/charts">        →  registry: ChartWorkspaceRedirect
<a className="btn" href="/signals">       →  registry: AdvisorySignalsRedirect
<a className="btn" href="/intelligence">  →  registry: InstitutionalIntelligencePage
```

Two problems:

1. **`<a href>` triggers a full browser page load**, tearing down and re-mounting the SPA — losing terminal state, dock selection and stage view. Everything else in the codebase navigates via `react-router-dom`.
2. **`/charts` and `/signals` are now redirect-only** post-CONV-P02. A full reload to a redirect route means: load app → resolve route → `<Navigate>` → land on the terminal. It "works" while being the slowest and most state-destructive path available.

**M5 — Convert these to in-app navigation** (`Link` / `useNavigate`) targeting the post-absorption destinations directly — `/?view=chart`, `/?dock=signals`, `/?dock=intelligence` — rather than bouncing through legacy redirects.

This is the same class as `OBS-CONV2-7`: a link that appears functional while doing the wrong thing underneath.

---

## 5. STANDING REQUIREMENTS

**R2 — `/investigate` must not 404.** Follow the established pattern (`GovernanceRedirect` :52-53 is the current model). Note `/investigate` currently routes to a real component, so this is a conversion.

**R3 — No fabricated fallbacks.** Report ids and intelligence reports render verbatim or as explicit absence. Per M2.

**R4 — `data-testid` on every new region.** Baseline 0 on the page; the dock's five existing hooks stay. Deliveries so far: 8, 10, 20, 17.

**R6 — RBAC.** 16/16 `protectedWorkspace()` wrappers, `ALL_AUTHENTICATED_ROLES = ["admin","operator"]`, no per-entry override. Do not widen.

**R7 — Suite green.** Current verified: **762 frontend / 415 backend = 1,177**. New capability requires new tests. **Never delete a failing test to reach green.**

**R8 — `npm ci` before `tsc -b`.**

**Deletion discipline.** Delete `SignalInvestigationPage.tsx` and its test in the same cycle once superseded — after M3/M4 re-pointing. Items 3 and 5 both held this standard.

**`OBS-CONV3-4` — no stage claim** unless the rendering branch is built and proven by a named test. Item 5 correctly declined; the same reasoning applies.

---

## 6. DELIVERY REQUIREMENTS

**Transport — the method now works; repeat it.** Item 3 reconciled to `b7b4c4f7…`, item 5 to `4c03910c…`. Both applied first time.

```bash
git diff <base> > item6.patch
git apply --check item6.patch ; echo "exit=$?"
sha256sum item6.patch
```

Paste the **entire patch inline**, transcripts alongside. **LF endings, terminating newline.** **State the base explicitly** — `34f4c62 + item3 + item5` — as item 5 did.

**Report must contain:**

1. Chosen disposition + reasoning, explicitly addressing §2: which capabilities were **added** vs **already present**, and how duplication of sections 2–7 was avoided.
2. Capability disposition table for all ten groups.
3. Confirmation the backend guard (M3) is re-pointed at the module that renders the drill-down, and still passes.
4. Confirmation all five frontend suites re-pointed and green (M4).
5. `OBS-CONV3-10` disposition (M5).
6. **Raw console transcripts** — vitest, tsc -b, vite build, pytest.
7. **Level-I captures, attached** — `OBS-CONV3-9`: item 5's gallery was described with hashes but never transmitted. Include:
   - expanded signal card showing the three new capability groups,
   - **an empty-state capture scrolled to the affected region** — *"No reports returned."* with an empty bundle. `OBS-CONV3-5` is now **open across three cycles**; every empty-state capture so far has been cropped above the empty state,
   - an interaction trace or explicit statement that hit-testing was verified in a real browser — jsdom cannot hit-test, which is how the item-3 `pointer-events` defect passed acceptance,
   - `/investigate` redirect landing.
8. Exact wording: *deleted* / *relocated* / *copied* / *extended*.

---

## 7. ACCEPTANCE

1. Capabilities 8, 9, 10 present and reachable from a signal card.
2. Sections 2–7 **not duplicated** — one implementation each.
3. M2 absence markers preserved (`"—"`, *"No reports returned."*).
4. M3 backend guard re-pointed at the real drill-down module, passing non-vacuously.
5. M4 five frontend suites re-pointed and green, incl. accessibility.
6. M5 evidence links use in-app navigation to post-absorption destinations.
7. `/investigate` resolves.
8. `data-testid` on every new region.
9. Suite green ≥ 1,177; nothing deleted to force green.
10. `tsc -b` clean; `vite build` succeeds.
11. RBAC not widened.
12. `SignalInvestigationPage.tsx` + test deleted once superseded.
13. Captures **attached**, incl. correctly scrolled empty state and interactivity evidence.

---

Gate **CLOSED**.
Production **NOT CERTIFIED**.
This directive authorizes **item 6 only**. It is not authorization for item 4 or any later programme.

**We don't guess. We prove.**
