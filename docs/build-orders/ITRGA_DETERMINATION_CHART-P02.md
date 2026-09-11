# ITRGA DETERMINATION — CHART-P02

**Reviewing body:** Independent Technical Review & Governance Authority
**Subject:** CHART-P02 — indicator breadth at scale (Trend · Momentum · Volatility · Levels · Statistics)
**Date:** 2026-08-18
**Base of record:** 13-element chain (through `chart_p01.patch.txt`)

| Artifact | Declared | Transmitted |
|---|---|---|
| `chart_p02.patch` sha256 `084b03c333c9c7cc…` | ✅ | 🔴 **NO** |
| `CHART-P02_CAPTURE_VERIFICATION.json` sha256 `7da21fadd4c5b2b5…` | ✅ | 🔴 **NO** |
| Capture 08 (insufficient on 1D) sha256 `9622a0a56734d720…` | ✅ | 🔴 **NO** |
| Captures 01–07 | ✅ | ✅ all seven, **all hashes match** |
| `DELIVERY_REPORT_CHART-P02.md` | — | ✅ |

---

## 1. DETERMINATION

# RETURN FOR RE-SUBMISSION

**Not on the merits.** On transmission.

The **patch is the artifact of record for this programme**, and it was not transmitted. Neither was the capture verification JSON nor capture 08. I cannot apply a patch I do not have, cannot verify sixteen formulae I cannot execute, and cannot confirm that the tree the captures were taken from is the tree the hashes describe.

This is the `OBS-CONV3-9` pattern at its most consequential: **a declared hash is not a transmitted artifact.** The report states criterion 15 was *"verified in a pristine clone"* — I do not doubt that the DA did so, but a DA's verification of its own patch is precisely what this role exists not to accept. **Correction ≠ approval, and neither does self-verification.**

Nothing about this determination questions the work. It questions the delivery.

---

## 2. WHAT I COULD VERIFY — AND IT IS PROMISING

### Transmission integrity of what did arrive

All seven transmitted PNGs match their report-declared hashes **exactly**, and all seven are mutually distinct. No dupes. On the evidence that arrived, the DA's hash discipline is intact — which makes the three omissions look like an attachment error, not a substantive one.

### ✅ M5 — the toolbar problem is solved well (capture 01)

This was the requirement I said I would look at first. The measured constraint was a flat flex row with 7 pills; 22 would overflow.

The delivered answer: **SMA 20 · SMA 50 · EMA 20 remain direct pills**, with five engine menus — `Trend · Momentum · Volatility · Levels · Statistics` — carrying the rest. Capture 01 shows the `Levels` menu open with `Pivots · Camarilla · Prev H/L · Session Lvls`, each tagged `overlay`.

**The three most-used indicators are reachable in exactly as many interactions as before**, which is the governing-reframe condition: a capability that becomes harder to reach after a phase is a defect. It did not. Active indicators also appear as dismissible chips below the toolbar (captures 03, 05, 07), so current state is visible without opening a menu.

### ✅ M6 — the pane budget refuses honestly (capture 07)

The other requirement I flagged. Measured risk: 5 panes × 110px + 360px price = 910px in a ~500px area.

Capture 07 shows the policy engaging:

> `STOCH1433: pane budget reached — at most 3 pane indicators concurrently; the indicator was NOT enabled`
> `pane budget: 3/3 (policy: price pane keeps a 280px minimum)`

**Explicit refusal, stated policy, stated numbers, and the indicator is confirmed not silently enabled.** This is exactly what the Build Order demanded — "a refusal must be explicit, never a silently dropped indicator." The chips row shows `RSI 14 · MACD · ATR 14` as the three occupants, so the refusal is legible in context.

### Deviations — six disclosed, and two are substantive

Deviation 5 is the one that matters most: **the pane-height policy failed its own rule on first capture** — three panes squeezed the price pane to 217px against the stated 280px minimum — and *the capture gate refused it*. The instrument the DA built in DATA-P01 cycle 3 caught a real violation of a requirement written in this Build Order. That is an evidence instrument doing its job against its own author.

Deviation 2 reports two performance defects found by **measuring S3 rather than by tests passing**: a quadratic `session_levels` recomputation (1,158 ms → 31 ms) and per-point ORM attribute re-reads (ichimoku 363 → 119 ms). Deviation 3 corrects HMA's full-definition requirement to `n + √n − 1` = 23 bars, which is the right reading of M3 and stricter than the obvious `n`.

Deviation 1 — extending the *compute* window to 2,880 bars for day/session levels while trimming output to the displayed window — is a legitimate and well-reasoned answer to a real problem, and it was disclosed rather than buried.

---

## 3. WHAT I CANNOT VERIFY — AND WILL NOT ASSERT

| Requirement | Status |
|---|---|
| M1 registry-only extension | **Unverifiable** — no patch |
| M2 sixteen formulae vs hand-computed values | **Unverifiable** — cannot execute |
| M3 `required_bars` full-definition | **Unverifiable** beyond the HMA claim in prose |
| M4 typed insufficiency | **Unverifiable** — capture 08 absent, no code |
| M7 time-axis sync after zoom | Capture 04 transmitted; **the JSON asserting `synced: true` is not** |
| M8 provenance inheritance | **Unverifiable** — no code |
| M9 no directional verdict language | **Unverifiable** — no guard source |
| R1–R7 | **Unverifiable** — no patch to inspect |
| Test transcripts, bundle delta `736.97 kB` | **Asserted only** |

**I verified all six CHART-P01 formulae by direct execution and found six exact matches. I will apply the same standard to these sixteen.** Supertrend's band-locking, CCI's mean-absolute-deviation constant, ADX's DX-averaging step, Ichimoku's 26-period displacement and HMA's `√n` rounding are exactly the conventions where a plausible-looking implementation can be quietly wrong. Prose declarations are not evidence.

---

## 4. 🔴 `CA-CHART2-1` — REQUIRED ARTIFACTS NOT TRANSMITTED

| Field | Content |
|---|---|
| **Finding ID** | `CA-CHART2-1` (return for re-submission — transmission) |
| **Requirement** | Build Order §8: upload patch · delivery report · capture verification JSON · PNGs. The artifact of record is the verified patch. |
| **Evidence** | `/home/user/uploads/` contains the report and 7 PNGs. `chart_p02.patch.txt` — absent. `CHART-P02_CAPTURE_VERIFICATION.json.txt` — absent. `CHART-P02_08_INSUFFICIENT_ON_1D.png` — absent. All three are declared with sha256 in the report. |
| **Failure** | The phase cannot be reviewed. This is the third recurrence of the declared-not-transmitted pattern (`OBS-CONV3-9`, `OBS-SURF3-1`). |
| **Required Correction** | Transmit `chart_p02.patch.txt`, `CHART-P02_CAPTURE_VERIFICATION.json.txt`, and `CHART-P02_08_INSUFFICIENT_ON_1D.png`. **Hashes must match those already declared** — `084b03c333c9c7cc…`, `7da21fadd4c5b2b5…`, `9622a0a56734d720…`. A hash mismatch would mean the shipped artifact is not the one the report describes and would escalate this finding. |
| **Do not** | Re-cut, re-capture or re-generate anything. The work is not in question; only its arrival. Re-running the captures would change hashes and destroy the reconciliation. |
| **Owner** | DA |

**Note on repeat occurrence:** `OBS-SURF3-1` remains open against the DA for exactly this — a capture declared but not transmitted. Two open instances of one pattern is a delivery-process problem rather than a lapse. **Recommended:** before upload, verify each hash in the report resolves to an attached file. That check is mechanical and would have caught all three.

---

## 5. STATUS

| Item | State |
|---|---|
| **CHART-P02** | **RETURN FOR RE-SUBMISSION** |
| `CA-CHART2-1` artifacts not transmitted | **OPEN — blocking** |
| M5 toolbar scaling | **Satisfied** on capture evidence |
| M6 pane budget refusal | **Satisfied** on capture evidence |
| M1–M4, M7–M9, R1–R7 | **Unverified** — pending artifacts |
| `OBS-SURF3-1` | **Open** — same pattern, DA |
| `OBS-CHART-1` orphan page · `OBS-DATA2-1` drift · `OBS-DATA-P01-WATCHLIST-CLIP` · `OBS-5` | Open |

**Fifteenth delivery: partially reconciled** — seven of eight captures match; the streak of fully reconciled deliveries ends here on transmission, not on integrity.

---

## 6. ASSESSMENT

The two requirements I singled out as most likely to be under-served — the toolbar and the pane budget — are the two I can see, and both are done properly. The grouped-menu design keeps the common indicators one click away while making twenty-three reachable, and the pane refusal states its policy in the product rather than hiding it. The disclosed deviations show an implementer measuring rather than assuming, and an evidence gate that caught its own author violating a stated minimum.

On what I can see, this looks like a strong phase. **I am returning it because I cannot see the substance**, and approving sixteen unexecuted formulae on a delivery report would be the precise failure this role exists to prevent.

Send the three files. Nothing else needs to change.

---

Gate **CLOSED**.
Production **NOT CERTIFIED**.
Return for re-submission ≠ rejection of the work. Not authorization for CHART-P03 or POLISH.

**We don't guess. We prove.**
