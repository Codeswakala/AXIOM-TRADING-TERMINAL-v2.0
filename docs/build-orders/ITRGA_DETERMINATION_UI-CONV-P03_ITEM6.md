# ITRGA DETERMINATION — UI-CONV-P03 · ITEM 6

**Reviewing body:** Independent Technical Review & Governance Authority
**Subject:** `SignalInvestigationPage` → signal drill-down extension · **plus an unauthorized item-4 submission**
**Date:** 2026-08-15
**Base:** `34f4c62` + item-3 (`b7b4c4f7…`) + item-5 (`4c03910c…`)
**Verification:** `/tmp/i6` — pristine clone → item3 → item5 → item6 → (item4 applied separately for inspection)

| Artifact | sha256 | Lines |
|---|---|---|
| `item3.patch.txt` | `b7b4c4f74f3016cb` | 1,609 — **matches previously verified** |
| `item5.patch.txt` | `4c03910c76fdcbf2` | 1,689 — **matches previously verified** |
| `item6.patch.txt` | `f65da5c3ce8433ec` | 2,019 |
| `item4.patch.txt` | `f50fd70eb345ec56` | 1,138 — **NOT AUTHORIZED** |
| `OPERATOR RESULTS.md` | `d8e5ab522d71a9c3` | transcripts + item-4 diff |

---

## 1. DETERMINATION

# ITEM 6 — APPROVED WITH OBSERVATIONS
# ITEM 4 — NOT REVIEWED · SUBMITTED WITHOUT AUTHORIZATION

Item 6 meets every mandatory requirement and is verified in applied source. It is the cleanest delivery of this phase.

**Item 4 was submitted without a Build Directive having been issued for it.** I have not reviewed it as a delivery and I will not approve it in this determination. §6 explains what I did with it and why.

---

## 2. ITEM 6 — VERIFIED

### M1 — Extended, not duplicated ✓

The correct disposition. The existing drill-down grew from five sections to eight; no parallel implementation was created.

```
signal-detail-rationale-        signal-detail-guardrails-       (pre-existing)
signal-detail-lineage-          signal-detail-explainability-   (pre-existing)
signal-detail-risk-                                             (pre-existing)
signal-detail-report-ids-       signal-detail-evidence-links-   (NEW — item 6)
signal-detail-intelligence-                                     (NEW — item 6)
```

All three gap capabilities are in `TerminalSignalStream.tsx` — the one surface that already owned the drill-down. Sections 2–7 remain single-implementation.

### M2 — Absence markers preserved ✓

```
:360  Statistical:     {sig.statistical_report_id     ?? "—"}
:363  Calibration:     {sig.calibration_report_id     ?? "—"}
:366  Economic:        {sig.economic_report_id        ?? "—"}
:369  Generalization:  {sig.generalization_report_id  ?? "—"}
:409  <span className="muted">No reports returned.</span>
```

Verbatim. The rule is also stated in the module docblock at :64 — *"never fabricated"*.

### M3 — Backend constitutional guard re-pointed, non-vacuously ✓

This was the subtle risk in the directive and it was handled exactly right:

```python
# test_signal_investigation_workspace.py
# UI-CONV-P03 item 6 (M3): the investigation surface was absorbed into the
# terminal signal drill-down. This guard must point at the module that
# ACTUALLY renders the drill-down, or the T-1 assertion would pass vacuously.
frontend_path = root / "frontend" / "src" / "components" / "terminal" / "TerminalSignalStream.tsx"
```

The guard now scans the file that genuinely renders the investigation UI, so the T-1 assertion — no `place_order`, `broker.`, `allow_execution`, `gate_open` — retains its force. The DA restated the vacuous-pass hazard in the code comment rather than silently re-pointing.

### M4 — Frontend suites re-pointed, none deleted ✓

`InvestigationPlanningCompletion`, `InvestigationPlanningFrame`, `SignalInvestigationLineage`, and `accessibilityAudit` all present. Residual `pages/SignalInvestigationPage` references are **two provenance comments only**. Accessibility coverage survives the move.

### M5 / `OBS-CONV3-10` — CLOSED ✓

```
:387  <Link className="btn" to="/?dock=intelligence">
:390  <Link className="btn" to="/?dock=signals">
:393  <Link className="btn" to="/?view=chart">
```

Zero raw `<a href>` remain. In-app navigation now targets post-absorption destinations directly, no longer bouncing through legacy redirects with a full page reload. The defect I found in already-approved work is fixed in the cycle I assigned it to.

### Standing requirements

| Req | Result |
|---|---|
| **R2** `/investigate` no 404 | `SignalInvestigationRedirect` :58; registry `Component:` :291 ✓ |
| **R4** testids | **23** on the stream (was 5 sections' worth) ✓ |
| **R6** RBAC | 16/16 wrappers, roles unchanged ✓ |
| **Deletion discipline** | `SignalInvestigationPage.tsx` **and** its test deleted ✓ |
| **`OBS-CONV3-4`** | No stage claim made by item 6 ✓ |

### Execution evidence

```
Test Files  165 passed (165)
     Tests  770 passed (770)      ← +8 vs item 5
tsc exit: 0        pytest: 415 passed
build: index-CJcY0n7k.js 684.07 kB │ gzip 185.59 kB
```

**1,185 tests green.** Bundle **687.56 → 684.07 kB (−3.49 kB)** — a *decrease*, consistent with three page deletions across the chain. This is the first cycle to show the reduction `OBS-5` anticipated.

The DA also reports the verify-tree build hash `ba4c1bb73b360f33…` matching its own working tree. Reproducibility corroborated.

---

## 3. OBSERVATION — `OBS-CONV3-9` PERSISTS

**No capture gallery was attached for item 6.** The only HTML in uploads is `UI-CONV-P03-ITEM3_CAPTURES.html` from a prior cycle.

Directive §6.7 required captures, explicitly citing item 5's failure to transmit them. This is the **second consecutive cycle** with no Level-I evidence.

Also therefore unmet:

- **`OBS-CONV3-5`** — empty-state capture scrolled to the empty state. **Open across four cycles.** The *"No reports returned."* path is verified in source at :409 but has never been seen rendering.
- **Interactivity evidence** — directive §6.7 required an interaction trace or an explicit statement that hit-testing was verified in a real browser. Not supplied. This matters precisely because the item-3 `pointer-events` defect passed acceptance on jsdom-passing tests plus a static screenshot.

**Not blocking.** Every item-6 acceptance criterion is verified in source, and 1,185 passing tests exercise the logic. But three consecutive determinations have now been issued without visual confirmation, and the one defect that escaped this programme's testing was invisible to exactly that method.

**No delivery report accompanied item 6** — only patches and a transcript block. Prior cycles supplied one; §6 of the directive required disposition reasoning. I reconstructed the disposition from source. Recorded as part of `OBS-CONV3-9`.

---

## 4. ITEM 6 — STATUS

**APPROVED WITH OBSERVATIONS.** Findings closed: `OBS-CONV3-10`. Carried: `OBS-CONV3-9`, `OBS-CONV3-5`.

---

## 5. UI-CONV-P03 PHASE POSITION

| Item | Surface | State |
|---|---|---|
| 1 | Portfolio Research → PORTFOLIO dock | APPROVED |
| 2 | Scenario Comparison → SCENARIOS dock | APPROVED |
| 3 | Workspace Customization → settings overlay | APPROVED |
| 5 | Governance Evidence → governance overlay | APPROVED |
| 6 | Signal Investigation → drill-down extension | **APPROVED** |
| 4 | Research Management → `?view=research` stage | **NOT AUTHORIZED — see §6** |

Five of six items approved. **The phase cannot close until item 4 is properly authorized and reviewed.**

---

## 6. ITEM 4 — SUBMITTED WITHOUT AUTHORIZATION

`item4.patch.txt` (`f50fd70eb345ec56`, 1,138 lines, 19 files) was transmitted. **No Build Directive for item 4 has been issued.** The Operator authorized item 6; the standing rule is *"no implementation before the next Build Order is formally issued."*

### What I did

I applied it to the item-6 tree **for inspection only**, to determine whether it creates immediate risk. I did **not** review it against acceptance criteria and I am **not** approving it.

### What inspection shows

Encouragingly, the `OBS-CONV3-4` trap appears to be handled:

```
TradingTerminalWorkspace.tsx:176   stageView === "research" ? (
                            :177     <div className="research-stage-scroll" data-testid="research-stage-scroll">
                            :178       <ResearchHubView />
```

The research stage now **renders**, not merely parses — the B-4 extension I set. `/research-management` is converted to `ResearchManagementRedirect` (:63, :377) and the page is deleted. All **11 capability groups** and all **10 endpoint consumers** are present in `ResearchHubView.tsx`, with 19 testids.

`git apply --check` exit 0; the combined tree reports 770 tests passing.

**This is a promising submission.** That is an observation from inspection, not a determination.

### Why I am not simply approving it

1. **Authorization is not a formality.** Every other item received a directive that inventoried the surface, identified coupling, and set mandatory requirements *before* implementation. Those directives caught the vacuous-guard hazard (M3, item 6), the write-path requirements (M1–M3, item 3), and the six-suite coupling (M1, item 5). Reviewing item 4 without that groundwork means reviewing against criteria I derived *after* seeing the solution — which is not independent review.

2. **Item 4 is the largest and most coupled surface in the phase** — 1,391 lines, 10 endpoints, 11 capability groups, plus `backend/tests/test_research_management.py:482` pinning `frontend/src/pages` with the same vacuous-pass hazard as item 6. It carries the approved disposition note and the B-4 condition. It warrants the same discipline as the smaller items, not less.

3. **I have not verified the backend guard re-point**, the eight dependent test suites, capability-by-capability preservation, or the empty-state behaviour of ten fetches.

### Required

**Operator authorization for item 4.** On authorization I will issue the directive — most of the inventory is already done — and review the submitted patch against it. If the patch is as sound as inspection suggests, that should be a single cycle.

**No re-work is implied.** The submitted patch remains the candidate artifact.

---

## 7. STANDING RISK — `OBS-CONV3-8`

Origin remains `34f4c62`. **Five items of verified work now exist only as patches**, held in this workspace and the DA sandbox:

```
item3.patch.txt  b7b4c4f74f3016cb   item5.patch.txt  4c03910c76fdcbf2
item6.patch.txt  f65da5c3ce8433ec   item4.patch.txt  f50fd70eb345ec56  (unreviewed)
```

`/tmp` has already been cleared once between turns. I hold reconstructable copies in `/home/user/uploads/`, which is a mitigation, not a repository. The patches apply in a clean chain — that property should be banked before it decays.

---

## 8. STATUS

| Finding | State |
|---|---|
| **Item 6** | **APPROVED WITH OBSERVATIONS** |
| `OBS-CONV3-10` raw `<a href>` navigation | **CLOSED** |
| `OBS-CONV3-9` captures + delivery report not transmitted | **Open — second cycle** |
| `OBS-CONV3-5` empty-state capture | **Open — fourth cycle** |
| `OBS-CONV3-4` research stage inert | **Appears addressed in the unreviewed item-4 patch** |
| `OBS-CONV3-8` work outside the repository | **Open — five items** |
| `OBS-PROV-2`, `OBS-5`, `F-BRAND-1`, `OBS-CONV2-5` | Open |
| P02 closures ×4 | Verified intact |

---

Gate **CLOSED**.
Production **NOT CERTIFIED**.
This determination approves **item 6 only**. It is **not** authorization or approval for item 4, and not authorization for SURF, DATA, CHART or POLISH.

**We don't guess. We prove.**
