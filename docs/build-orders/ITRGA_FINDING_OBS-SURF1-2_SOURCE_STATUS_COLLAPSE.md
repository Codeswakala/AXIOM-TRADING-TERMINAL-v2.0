# ITRGA FINDING — `OBS-SURF1-2` · Source Status panel collapses in the stage view

**Reviewing body:** Independent Technical Review & Governance Authority
**Date:** 2026-08-17
**Arising from:** `OBS-SURF1-1` correction review
**Affects:** SURF-P01 — `ExecutionResearchView.tsx` / `TerminalMultiPane.css`

---

## 1. `OBS-SURF1-1` — TRANSPORT AND INSTRUMENT: DISCHARGED

The five raw PNGs were transmitted directly, bypassing the `.html` upload problem.

```
SURF-P01_04_SINGLE_SEAM_FAILURE_DEGRADATION_SCROLLED.png
sha256 62d5c85b14c36b93e469cb7976e2548d04b9787667dd4cfc38a5876dba77a1d6
declared 62d5c85b14c36b93e469cb7976e2548d04b9787667dd4cfc38a5876dba77a1d6
→ FULL 64-CHARACTER MATCH · 1920×1080 · valid PNG · 281,678 B
```

The Rev B instrument fix stands as accepted: geometric containment reporting, `scroll_before`/`after` records, and the post-screenshot scroll check are all materially better than the Rev A boolean.

**The image is now verified as authentic. What it shows is the problem.**

---

## 2. THE CAPTURE STILL DOES NOT SHOW THE ERROR ROW — AND THE REASON IS A UI DEFECT

Rev B recorded the container scrolled to `scrollTop: 93` and the error row at `rowTop 426.72 → rowBottom 533.34` inside `containerTop 81 → containerBottom 879`. Geometrically inside the viewport.

**The rendered frame contradicts it.** In the transmitted capture, `SOURCE STATUS` renders its heading and its descriptive paragraph, and then the section **terminates**. The six source cards — including `Paper ledger / Failed to fetch` — occupy a band roughly 20 px high before `PERSISTED SIMULATED ARTIFACTS` begins. Faint vertical card edges are discernible at the section's lower boundary; the card content is not.

**This is not a scrolling failure and not a capture failure. The panel is collapsing.**

### Root cause

```
.panel-grid  { display: grid; grid-template-columns: repeat(12, 1fr); }   global.css:170
.span-12,
.panel.span-12 { grid-column: span 12; }                                  global.css:202-205
```

`grid-column: span 12` is meaningful **only inside a grid container**. In the stage view, the workspace root is a React Fragment:

```tsx
export function ExecutionResearchWorkspace({ ... }) {
  return (
    <>
      <div className="page-header" ...>
```

so the `.panel.span-12` sections become direct children of the stage scroll container:

```
.research-stage-scroll / .stage-view-scroll {
  display: flex;  flex-direction: column;  flex: 1 1 auto;
  min-height: 0;  height: 100%;  overflow-y: auto;
}                                              TerminalMultiPane.css:895-915
```

**A flex column, not a grid.** `grid-column` is inert here, and `min-height: 0` — correct for enabling scroll — removes the flex floor that would otherwise preserve intrinsic height. `.panel { min-height: 120px }` applies to the section, which is why the heading and paragraph render, but the inner `.artifact-source-grid` (an `auto-fit minmax(240px, 1fr)` grid) is free to compress toward zero.

The same class of collapse is visible in capture 01 at the same section, and in capture 03 where `PERSISTED SIMULATED ARTIFACTS` metric cards are clipped mid-height.

### Why the instrument reported `true` honestly

`getBoundingClientRect()` returns layout geometry, which is real — the element occupies that box in the layout tree. The card's *content* is visually collapsed within it. **The measurement was not wrong; it was measuring the wrong thing.** A containment check cannot detect a visually collapsed element, which is why the DA's Rev B fix — a genuine improvement — still could not surface this.

**This is the second time an evidence instrument has been correct in its own terms while the rendered result differed.** The first was item 3's `pointer-events` defect, invisible to jsdom. The lesson is consistent: **automated geometry and passing tests do not substitute for looking at the picture.**

---

## 3. FINDING

| Field | Content |
|---|---|
| **Finding ID** | `OBS-SURF1-2` |
| **Requirement** | Build Order SURF-P01 R4 — independent per-source degradation must be **presented**; turn-56 reframe — built capability surfaced in the best possible way. |
| **Evidence** | Capture 04 (`62d5c85b…`, verified authentic): `SOURCE STATUS` heading and description render; the six `.artifact-source-card` elements are collapsed to a hairline band. Same in captures 01 and 03. |
| **Failure** | `.panel.span-12` relies on `grid-column: span 12`, but the stage-view parent is `display: flex; flex-direction: column` with `min-height: 0`. The grid directive is inert and the inner grid compresses. The operator cannot read which seam failed. |
| **Consequence** | R4 is implemented correctly in logic — six independent error states, `errorRows: 1, readyRows: 5, hubStillRenders: true` — but **is not legible to the operator**. A degradation indicator that cannot be read does not discharge its purpose. |
| **Severity** | **Presentation defect, not a data-honesty defect.** No fabricated values; `Ledger 0` renders honestly. Nothing is misstated — some things are unreadable. |
| **Required Correction** | Give the stage-view panels a working layout context: wrap the stage-view children in a `.panel-grid`, or add a flex-context rule so `.panel.span-12` and inner grids retain intrinsic height under `min-height: 0`. Verify at 1920×1080 that all six source cards, the metric cards, and the group panels render at full height. |
| **Closure Evidence** | Re-capture 04 with the six source cards legible, `Paper ledger / Failed to fetch` readable in frame. Confirm captures 01 and 03 sections are not clipped. |
| **Owner** | DA |

---

## 4. STATUS

| Item | State |
|---|---|
| **SURF-P01** | **APPROVED WITH OBSERVATIONS** — unchanged |
| `OBS-SURF1-1` transport | **CLOSED** — full hash match on direct PNG |
| `OBS-SURF1-1` instrument | **CLOSED** — Rev B geometric reporting accepted |
| `OBS-SURF1-2` panel collapse | **NEW** — presentation defect |
| `OBS-5` bundle 697.62 kB | Open — POLISH-P01 |
| `OBS-CONV2-5`, `F-BRAND-1` | Open |

**SURF-P01 approval is not withdrawn.** Every acceptance criterion was verified in source, the POST exclusion held, the M1 guard closed a real constitutional gap, and 1,201 tests pass. This is a layout defect in a surface that is otherwise correctly built.

**Fix disposition:** `OBS-SURF1-2` is a CSS-scope correction. It may be folded into SURF-P02 rather than run as its own cycle — the same treatment given `OBS-CONV3-3` and `OBS-CONV3-10`. If the DA judges it a one-line stylesheet change, a standalone patch is also acceptable.

**SURF-P02 remains unauthorized.** The *acknowledge* write path will be inventoried before any Build Order is issued.

---

Gate **CLOSED**.
Production **NOT CERTIFIED**.
This finding does not alter the SURF-P01 determination and is not authorization for any further phase.

**We don't guess. We prove.**
