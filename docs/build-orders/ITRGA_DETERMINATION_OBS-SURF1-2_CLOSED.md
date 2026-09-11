# ITRGA DETERMINATION — `OBS-SURF1-2` CLOSED

**Reviewing body:** Independent Technical Review & Governance Authority
**Subject:** Stage-view panel collapse — corrective patch
**Date:** 2026-08-17
**Base:** `34f4c62` + item3 + item5 + item6 + item4 Rev B + SURF-P01
**Verification:** `/tmp/fix` — pristine clone → full chain → `surf_p01_obs1-2` applied

| Artifact | sha256 | Size |
|---|---|---|
| `surf_p01_obs1-2.patch.txt` | `69964afec17b9c0f` | 293 lines · 4 files |
| `SURF-P01_CAPTURE_VERIFICATION.json.txt` (Rev C) | `429e6d1b6d76828e` | — |
| `SURF-P01_04_..._SCROLLED.png` | `2b68fce51e8dfac4` | 1920×1080 |

---

## 1. DETERMINATION

# `OBS-SURF1-2` — CLOSED
# `OBS-SURF1-1` — CLOSED

Both findings are discharged. The fix is correct at the root, minimal in scope, regression-tested, and **visually proven**.

`git apply --check` exit 0 on the stated chain; declared capture hash `2b68fce5…` matches the transmitted PNG exactly.

---

## 2. THE FIX — CORRECT, AND MY DIAGNOSIS WAS INCOMPLETE

Four lines of CSS:

```css
/* OBS-SURF1-2 (2026-08-17): the stage scroll containers are flex columns,
   and flex-shrink compresses direct panel children to their 120px
   min-height — the inner grids then overflow behind the next panel's opaque
   background (the collapsed band observed in SURF-P01 captures 01/03/04). */
.research-stage-scroll > *,
.stage-view-scroll > * {
  flex-shrink: 0;
}
```

**I attributed the collapse to `grid-column: span 12` being inert outside a grid container.** That observation was true but was not the operative cause. The actual mechanism is **default `flex-shrink: 1`** on direct children of a flex column: the panels were compressed to their `min-height: 120px` floor, and the inner `.artifact-source-grid` then overflowed *behind the next panel's opaque background*. That is why the section appeared to terminate mid-content rather than simply clip.

The DA diagnosed it more precisely than I did and fixed the actual cause. `flex-shrink: 0` is the correct remedy and is **consistent with existing practice in the same stylesheet** — `.terminal-ticker-region:40` and `.terminal-slot-bottom:337` already use it for the same reason. No new pattern was invented.

**Scope is proportionate:** one CSS rule, one regression test, two capture scripts. No component logic touched.

### Regression test

```
test_surf_p01_obs1_2_stage_panels_keep_intrinsic_height_rule_present
```

Added at `ExecutionResearchDegradation.test.tsx:337`, alongside the five existing R3/R4/S2 tests. The finding cannot silently regress.

---

## 3. VISUAL PROOF — THE ERROR ROW IS NOW LEGIBLE

Capture 04 (`2b68fce5…`) shows the Source Status panel rendering at full height with all six cards:

```
Simulated runs     3 rows loaded      Simulated fills    0 rows loaded
Paper ledger       Failed to fetch    Risk reports       0 rows loaded    ← in red
Replay experiments 0 rows loaded      Analytics reports  0 rows loaded
```

**`Paper ledger — Failed to fetch` is readable, in error red, with the other five seams reporting genuine counts** and `PERSISTED SIMULATED ARTIFACTS` rendering fully below. This is the R4 evidence the Build Order required: one seam fails, five report honestly, the surface holds.

The other four captures are re-shot and consistent — capture 01 now shows the evidence-link buttons and full Source Status; capture 03 shows all six group panels with their absence markers (`No simulated runs returned.`, `No risk reports returned.`, etc.) and per-group `SIMULATED · NON-ACTUATING` badges; capture 02 shows the detail record; capture 05 the redirect.

**Note:** all five capture hashes changed. That is expected — the layout fix altered every frame.

---

## 4. THE INSTRUMENT NOW DETECTS COLLAPSE — `OBS-SURF1-1` FULLY DISCHARGED

Rev C adds a measurement that would have caught this defect:

```json
{"label": "capture04_source_status_legibility",
 "panelTop": 311, "panelBottom": 640, "panelH": 329,
 "innerGridH": 197, "cardCount": 6,
 "cardRects": [{"top":427,"bottom":533,"h":107} ×4,
               {"top":547,"bottom":623,"h":76} ×2],
 "cardsFullyInsidePanel": true}
```

This is the third revision of this instrument, and it is now sound:

| Rev | Measurement | Would it have caught the collapse? |
|---|---|---|
| A | `errorRowVisibleInViewport: true` (boolean) | **No** — asserted visibility it could not substantiate |
| B | Geometric containment vs viewport | **No** — layout box was genuinely in-viewport while content was collapsed |
| C | **Per-card rendered heights + containment within the panel** | **Yes** — `h: 107` / `h: 76` are non-degenerate; a collapsed card would report `h ≈ 0` |

The decisive addition is `innerGridH: 197` against `panelH: 329` with six non-zero card heights. **A collapsed panel cannot produce those numbers.** The instrument no longer measures a proxy for legibility — it measures rendered extent.

This closes the second half of `OBS-SURF1-1`. I raised it because a measurement returned `true` for something not in frame; it now reports auditable geometry that fails when content collapses.

---

## 5. RECORDED — THE EVIDENCE LESSON OF THIS PHASE

Three instrument revisions were needed before the picture and the measurement agreed.

- **Rev A** asserted a boolean that could not be audited.
- **Rev B** measured real geometry — correctly — but the wrong property.
- **Rev C** measures rendered extent, which is what "legible" actually means.

The defect was found by **looking at the image**, not by any automated check, and not by the 1,201 passing tests. That is now the second time in this programme: item 3's `pointer-events` click-transparency was likewise invisible to jsdom and to a static screenshot that looked correct.

**Standing evidence rule, reaffirmed:** for visual requirements, the image is primary and instruments are corroboration. A measurement that agrees with a wrong conclusion is not evidence — it is a second opinion from the same blind spot.

---

## 6. STATUS

| Item | State |
|---|---|
| **SURF-P01** | **APPROVED WITH OBSERVATIONS** — unchanged |
| `OBS-SURF1-1` transport + instrument | **CLOSED** |
| `OBS-SURF1-2` panel collapse | **CLOSED** |
| `OBS-5` bundle 697.62 kB | Open — POLISH-P01 |
| `OBS-CONV2-5` seeded fixtures | Open |
| `F-BRAND-1` | Open — GA-173 |

**No open findings against SURF-P01.**

**Artifacts of record** (`/home/user/uploads/`), applying clean in order:

```
item3.patch.txt          b7b4c4f74f3016cb
item5.patch.txt          4c03910c76fdcbf2
item6.patch.txt          f65da5c3ce8433ec
item4.patch (1).txt      a516c2c144c1f2f6
surf_p01.patch.txt       62c4d021e5b6f0a0
surf_p01_obs1-2.patch.txt 69964afec17b9c0f
```

**Next:** SURF-P02 — Alerts, closing `TD-061`. Left-rail badge with unread count, dock tab, acknowledge action, severity styling. **Not authorized.** On authorization I will inventory the alerts endpoints — particularly the **acknowledge write path**, which unlike SURF-P01's excluded POSTs is named in Blueprint §5 as in-scope — and issue the Build Order before implementation.

---

Gate **CLOSED**.
Production **NOT CERTIFIED**.
This determination closes two observations against SURF-P01. It is not authorization for SURF-P02, SURF-P03, DATA, CHART or POLISH.

**We don't guess. We prove.**
