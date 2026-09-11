# ITRGA REVIEW — UI-001-P06 (FINAL PHASE — attempt 1)
## Legacy `TerminalLayout` Retirement · Migration Completion · UI-001 Completion Checkpoint

**Authority:** Institutional Technical Review & Governance Authority (ITRGA)
**Programme:** AXIOM Institutional UI Transformation · **Workstream:** UI-001 · **Phase:** P06 (final)
**Build Order under review:** `BUILD_ORDER_UI-001-P06.md`
**Evidence pack submitted:** `DELIVERY_REPORT_UI-001-P05.md` (**WRONG — P05 report, not P06**), `operator results.md` (**P05-dominant / P06-partial run that halted on a failing test**), 6 served-session screenshots (P06-relevant, workspaces in-shell).
**Determination:** ⛔ **CORRECTIVE ACTIONS REQUIRED**
**Authorizes:** *nothing* — UI-001 is **NOT** complete; no completion declared.
**Motto:** *We don't guess. We prove.*

---

## 0. Build-identity verification (done FIRST) — TWO FAILURES
| Artifact | Identity check | Status |
|---|---|---|
| Delivery report | File is **`DELIVERY_REPORT_UI-001-P05.md`**, self-declares **Phase P05**. The **P06 delivery report was not attached.** | ⛔ **WRONG PACK** |
| `operator results.md` | **71** `UI-001-P05` refs vs **12** `UI-001-P06`; **0** of the three mandatory P06 named tests; the command header re-runs the **P05** evidence set (`Get-Content DELIVERY_REPORT_UI-001-P05.md`, tests P05 overlay files). It transitions into a P06-style frontend run that **halts on a failing test**. | ⛔ **P05-dominant / P06-partial** |
| 6 screenshots | Workspaces rendered in-shell (research-management, portfolio-research, execution-research, journal, compare-scenarios, charts) — P06-relevant and useful | ✅ P06-relevant |

Per the mandatory-evidence rule, ITRGA cannot conduct the P06 completion review against a P05 report + a partial run. **However**, the operator flagged "I got some errors" — those errors are a genuine P06 finding and are surfaced below rather than deferred.

---

## 1. 🔴 SUBSTANTIVE FINDING — the P06 retirement is INCOMPLETE (a failing gate, not a footnote)
The transcript's frontend run shows:

```
Test Files  1 failed | 25 passed (26)
Tests       1 failed | 96 passed (97)
```

The failing test is the **retirement gate itself**, `InstitutionalWorkspaceShell.test.tsx:240`:
```js
expect(sourceText).not.toContain("TerminalLayout");   // ❌ FAILS
expect(sourceText).toContain("InstitutionalWorkspaceShell");
```

Root cause, proven in the same transcript:
- **`Test-Path frontend\src\layouts\TerminalLayout.tsx`** → the file **STILL EXISTS**: `export function TerminalLayout()` (L4), full JSX body (`<div className="app-shell">`, `<header className="top-nav">`, `<aside className="sidebar">`, L8–29).
- The DA authored the correct assertion (source must not contain `TerminalLayout`) **but did not perform the removal** — so the test correctly fails.
- Build shows **73 modules** (P05 was 62) and **bundle grew** (CSS 33.64 / JS 456.61) — the legacy file and its dependencies are **still bundled**, the opposite of the expected dead-code *decrease*.

**Severity — contained (mitigating):** `TerminalLayout` is **NOT imported anywhere** (no `import`/`<TerminalLayout` reference found) — it is an **orphaned dead file**, not a reachable competing frame. The active frame is correctly `InstitutionalWorkspaceShell` (App.tsx L16). So there is **no dual-frame / constitutional violation** — but the P06 *objective* (retire = remove) is **not met**, and the DA's own sole-frame gate is **red**.

Per R1/R12, a failing/red gate is a finding; a **single failing test ⇒ not Approved**.

## 2. What is missing for the P06 completion review
None of the P06 completion-checkpoint evidence is present (grep count 0): no `DELIVERY_REPORT_UI-001-P06.md`; the three P06 named tests were not completed (the run halted on the failure); no Part IX §13 8-subsystem regression sign-off; no §14 operator-acceptance walkthrough narrative; no §15 constitutional-validation self-check; no networked-CI exit line for P06. (The 6 browser shots do show workspaces mounted in-shell, which is encouraging for §14, but cannot substitute for the retirement + completion evidence.)

## 3. Determination & required corrective actions
**CORRECTIVE ACTIONS REQUIRED.** Two correctives:

> **CA-P06-1 — Complete the retirement.** Actually **remove `frontend/src/layouts/TerminalLayout.tsx`** (and any now-dead legacy layout/nav/CSS it solely owned). Re-run so that `InstitutionalWorkspaceShell.test.tsx:240` (`not.toContain("TerminalLayout")`) **passes** and the full frontend suite is **green** (currently 1 failed / 96 passed). Expect module count and bundle size to **decrease**. Grep `frontend/src` for `TerminalLayout` → no output (or tombstone-comment only).

> **CA-P06-2 — Resubmit the CORRECT P06 pack:** `DELIVERY_REPORT_UI-001-P06.md` (not the P05 report) + a P06 `operator results.md` containing inline command+output for the full Build-Order §5 evidence: (b) TerminalLayout retired grep/Test-Path→False; (c) sole-frame + the three P06 named tests **displayed passing** (`test_terminal_layout_retired_shell_is_sole_frame`, `test_all_routes_mount_only_through_workspace_shell_no_regression`, `test_shell_contains_no_execution_or_actuation_after_retirement`); (d) UI-only removal diff + empty backend/dep diff + head `20260717_0037`; (e) Part IX §13 regression 8 subsystems (backend ≥414); (g) whole-shell no-actuation grep; (j) networked CI exit 0 + sentinel; (k) §11 completion conditions + §15 constitutional self-check.

No constitutional violation is alleged (Gate CLOSED, no execution surface, orphaned dead file only). This determination is **evidence-completeness + one failing retirement test**. Once `TerminalLayout.tsx` is removed (suite green) and the correct P06 pack is supplied, ITRGA expects to complete the review and — if the §15 constitutional validation is clean — **declare 🏛️ UI-001 COMPLETE**.

**No progression / no completion.** Baseline unchanged: v0.62.0 / head `20260717_0037` / backend 414 / frontend 26f/94t (last-good = the P05 approval; this P06 attempt is 1-failing and not accepted). Residuals unchanged: TD-W7-U07-RATE-GUARD, TD-W6-CI-AUDIT.

*We don't guess. We prove.*
