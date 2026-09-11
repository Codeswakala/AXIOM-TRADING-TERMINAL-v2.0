# ITRGA REVIEW — `OBS-SURF1-1` CORRECTION

**Reviewing body:** Independent Technical Review & Governance Authority
**Subject:** DA correction to the SURF-P01 capture-04 evidence defect
**Date:** 2026-08-17

| Artifact | sha256 | Lines |
|---|---|---|
| `SURF-P01_CAPTURE_VERIFICATION.json.txt` (Rev B) | `bae4108a4f893e0c` | 151 |
| *(superseded Rev A)* | `8fdcce6050a59b4a` | 139 |

---

## 1. DETERMINATION

# PARTIALLY DISCHARGED — INSTRUMENT FIXED, IMAGE NOT TRANSMITTED

The finding had two halves. **The harder one is fixed.** The other is one attachment away.

| Half | State |
|---|---|
| The viewport-visibility check returned `true` for an off-screen element | **CORRECTED** |
| Capture 04 must show the error row in frame | **NOT VERIFIABLE — image not transmitted** |

---

## 2. THE INSTRUMENT FIX — ACCEPTED

Rev A recorded `scrollTop: 0` while asserting `errorRowVisibleInViewport: true`. That assertion was inconsistent with the rendered frame, and a measurement that can affirm an invisible element cannot discharge a visual requirement.

Rev B replaces it with a **geometric containment check**:

```json
{"label": "capture04_scroll_before_explicit_scroll", "value": 0}
{"label": "capture04_scroll_metrics", "scrollTop": 93, "scrollHeight": 2822, "clientHeight": 798}
{"label": "capture04_errorRowWithinContainer",
 "withinContainer": true, "rowTop": 426.72, "rowBottom": 533.34,
 "containerTop": 81, "containerBottom": 879}
{"label": "capture04_scrollTop_after_screenshot", "value": 93}
```

This is a materially better instrument, for three reasons:

1. **It reports real geometry, not a boolean.** `426.72 → 533.34` sits inside `81 → 879`, so the claim is independently checkable rather than self-asserted. Rev A's boolean could not be audited.
2. **It records the scroll actually happened** — `before: 0`, `metrics: 93`, `after: 93`. The `_SCROLLED` filename is now backed by evidence; in Rev A it was contradicted by `scrollTop: 0`.
3. **`scrollTop_after_screenshot` guards a real failure mode** — a container scrolling back before capture. Confirming the position held *through* the screenshot is a check I did not ask for.

The `capture04_single_seam_failure` record is unchanged and still corroborates R4: `errorRows: 1, readyRows: 5, hubStillRenders: true, ledgerErrorText: "Paper ledgerFailed to fetch"`.

**This is the correct response to an evidence-instrument defect: fix the measurement so it cannot lie, rather than re-running until the number is favourable.**

---

## 3. WHY IT IS NOT FULLY DISCHARGED

Rev B declares a **new** capture-04 image:

```
JSON declares:  62d5c85b14c36b93e469cb7976e2548d04b9787667dd4cfc38a5876dba77a1d6
```

The gallery on file (`SURF-P01_CAPTURES.html`, `4e5c9cf839010fb0`) still holds the **Rev A** set:

```
a1372592 · d81d5ade · aa43bd95 · 1ad1cdf4 · 78b91290
                                  ^^^^^^^^ superseded capture 04
```

**`62d5c85b…` is not present in any transmitted artifact.** The declared hash proves a new image was produced; it does not transmit it.

`OBS-SURF1-1` exists because a capture was offered as proof of something not in its frame. **I cannot close it on a hash.** The metrics make the claim highly credible — and I have accepted that credibility as sufficient for SURF-P01's approval, which stands unchanged — but the finding itself asks whether the error row is *visible*, and only the image answers that.

---

## 4. REQUIRED TO CLOSE

Re-transmit `SURF-P01_CAPTURES.html` (Rev B) containing the updated capture 04, base64-embedded as before. I will verify the extracted bytes hash to `62d5c85b…` and confirm the `Paper ledger / Failed to fetch` row is in frame.

Nothing else is outstanding. The other four captures are sound and need not be resent — though including them keeps the gallery a single coherent artifact.

---

## 5. STATUS

| Item | State |
|---|---|
| **SURF-P01** | **APPROVED WITH OBSERVATIONS** — unchanged |
| `OBS-SURF1-1` — viewport check | **CORRECTED** |
| `OBS-SURF1-1` — capture 04 image | **Open** — one attachment |
| `OBS-5` bundle 697.62 kB | Open — POLISH-P01 |
| `OBS-CONV2-5` seeded fixtures | Open |
| `F-BRAND-1` | Open — GA-173 |

**SURF-P02 remains unauthorized.** When authorized, I will inventory the alerts endpoints — including the *acknowledge* write path, which unlike the five POSTs excluded from SURF-P01 is named in Blueprint §5 as in-scope — and issue the Build Order before any implementation.

---

Gate **CLOSED**.
Production **NOT CERTIFIED**.
This review does not alter the SURF-P01 determination and is not authorization for any further phase.

**We don't guess. We prove.**
