# ITRGA DETERMINATION — SURF-P02

**Reviewing body:** Independent Technical Review & Governance Authority
**Subject:** Alerts — left-rail badge, ALERTS dock, read-state acknowledge · closes `TD-061`
**Date:** 2026-08-17
**Base:** `34f4c62` + item3 + item5 + item6 + item4 Rev B + SURF-P01 + OBS-SURF1-2
**Verification:** `/tmp/p2` — pristine clone → full chain → SURF-P02 applied

| Artifact | sha256 | Size |
|---|---|---|
| `surf_p02.patch.txt` | `e039c74bc9993640` | 1,600 lines · 15 files |
| `DELIVERY_REPORT_SURF-P02.md` | `590c5f634fe101b5` | 179 lines |
| `SURF-P02_CAPTURE_VERIFICATION.json.txt` | `bce446a77e488080` | 104 lines |
| 6 PNGs | all reconcile | 1920×1080 |

---

## 1. DETERMINATION

# APPROVED
# `TD-061` — CLOSED

Every mandatory requirement, standing requirement and acceptance criterion is met. **No observations are raised.**

This is the first unqualified APPROVED of the programme. It earns that on four counts: the acknowledge write is correctly constrained and evidenced end-to-end; the T-1 guard solves a problem I had not anticipated; the orphan panel was extended rather than duplicated; and every capture hash reconciles with a machine record that measures the right property.

**Transport:** `e039c74bc9993640…` matches exactly; `git apply --check` exit 0; full seven-element base chain declared. **Seventh consecutive hash-reconciled delivery.**

---

## 2. THE ACKNOWLEDGE WRITE — CORRECTLY CONSTRAINED

This was the phase's governing risk: a write path in a surfacing programme.

### M1 — Read-state vocabulary ✓

Controls are `Acknowledge`, `View detail`, `Refresh alerts`. A search for `resolve`, `dismiss`, `clear`, `fix`, `handle`, `action` across the alerts UI returns **one hit** — the word `remediate` inside the preserved disclaimer sentence, which is the opposite of an actuation affordance.

No operator can infer from this UI that acknowledging changed the underlying condition.

### M2 — No optimistic update ✓

```ts
// M2: render the acknowledged state only after the API confirms.
const updated = await acknowledgeMonitoringAlert(alertId);
setAlerts((current) => current.map((a) => (a.alert_id === alertId ? updated : a)));
...
catch (err) { setAckError(...); return false; }
```

The **server's returned record** replaces local state — not a locally-mutated copy. Failure sets `ackError` and returns `false`, leaving the alert unacknowledged. Separate `acknowledgingId` and `ackError` state keeps the ack failure distinct from the load failure.

### M3 — Acknowledged alerts remain visible ✓

`AlertsProvider` filters only to *count* unread (`alerts.filter(a => !a.acknowledged).length`). No display filter, no default hiding. Capture 03b confirms it: the acknowledged alert stays in the list with `Ack: yes` and its `Acknowledge` button removed.

### M4 — Frontend T-1 guard ✓ — **and it solved a problem I did not foresee**

I required forbidden terms including `retrain` and `remediate`. **Those words legitimately appear in the module** — in the constitutional disclaimer *"Read-only alerts inform the operator; they do not retrain, remediate, or act."*

A naive implementation of my requirement would have failed against correct code, and the likely "fix" would have been to delete or reword the disclaimer — **weakening a constitutional honesty surface to satisfy a guard meant to protect it.**

The DA resolved it precisely:

```python
assert "Read-only alerts inform the operator; they do not retrain, remediate, or act." in text
disclaimer = "read-only alerts inform the operator; they do not retrain, remediate, or act."
residue = text.lower().replace(disclaimer, "")
forbidden = ("place_order", "submit order", "go live", "connect broker", "broker_account",
             "resolve_alert", "auto_action", "execute", "retrain", "remediate")
assert all(item not in residue for item in forbidden)
```

The sentence is asserted **present** as a non-vacuity anchor, then excised before the absence check. The guard is strictly stronger than what I specified: it now enforces both that the disclaimer exists verbatim **and** that those terms appear nowhere else.

**This is the correct handling of a defective requirement — satisfy the intent, and say so.** The docstring explains the reasoning in full.

---

## 3. REMAINING REQUIREMENTS

| Req | Result |
|---|---|
| **S1** rail badge + dock | `UnifiedModuleRail` badge; ALERTS tab in the right dock |
| **S2** genuine unread count | `unreadCount: number \| null` — **`null` while loading or on error**; badge renders only when `!== null && > 0`. Never a fabricated `0`. |
| **S3** acknowledge action | `acknowledgeMonitoringAlert` client fn + wired control |
| **S4** severity styling | All three `Literal` values — capture 02 records `["info","warning","critical"]` |
| **S5** `GET /alerts/{alert_id}` | Surfaced via `View detail` |
| **S6** `limit = 5` truncation | **Removed** — default raised 5 → 200 |
| **S7** testids | Present across regions |
| **R1** disclaimer preserved | Verbatim, and now guard-enforced |
| **R8** no new orphan | **Extended in place** — stated precisely as *extended*, not *relocated* |
| **R9** `TD-061` | `**Closed** SURF-P02: left-rail unread badge, terminal ALERTS right-dock tab, read-state-only acknowledge, severity styling, alert detail record` |

**S2 deserves emphasis.** Returning `null` rather than `0` when the count is unknown is the `OBS-CONV2-1` discipline applied to a trivial-looking number. A `0` badge during a failed load would be a fabricated value — small, plausible, and wrong.

### Execution evidence

```
Test Files  168 passed (168)
     Tests  803 passed (803)      ← +18
tsc exit: 0
pytest      417 passed            ← +1 (the M4 guard)
build       index-B1ixir5U.js 704.00 kB │ gzip 189.41 kB
```

**1,220 tests green.** Bundle 697.62 → 704.00 kB (+6.38 kB), disclosed under `OBS-5`.

---

## 4. CAPTURES — ALL SIX RECONCILE

Raw PNGs, as requested after the gallery upload failures. Every declared hash matches the transmitted bytes.

**The acknowledge before/after pair is the strongest evidence in this delivery:**

```
03a BEFORE  ebf0d8b9  badge "2" · 2 ack buttons · hitTestOwnsPointer: true
03b AFTER   343eaaed  badge "1" · 1 ack button  · itemAckState "…: yes…"
```

Badge 2 → 1, ack buttons 2 → 1, the acknowledged alert still listed with `Ack: yes`. That is M1, M2, M3 and S2 demonstrated in a single state transition — and the interaction trace confirms the click landed on the intended control in a real browser.

Capture 01 records `ariaLabel: "System Alerts (2 Unread)"` — the count is exposed to assistive technology, not colour-only.
Capture 04 records `emptyText: "No monitoring alerts returned."` with `badgeAbsentWhenZero: true`.
Capture 05 shows `Failed to fetch` inside the dock while the terminal continues rendering (R3).

**Note:** 03a and 02 share hash `ebf0d8b9` — expected, as the pre-acknowledge state is the populated dock. Not a duplicate-submission defect.

---

## 5. PROGRAMME POSITION

| Phase | State |
|---|---|
| CONV P01–P03 | COMPLETE |
| SURF-P01 Execution Research | APPROVED WITH OBSERVATIONS — no open findings |
| **SURF-P02 Alerts** | **APPROVED** · `TD-061` CLOSED |
| SURF-P03 Governance & platform | **Not authorized** |

**Open findings across the programme:** `OBS-5` (bundle 704 kB → POLISH-P01) · `OBS-CONV2-5` (seeded evidence fixtures) · `F-BRAND-1` (GA-173, Operator).

**Artifacts of record** (`/home/user/uploads/`), applying clean in order:

```
item3.patch.txt            b7b4c4f74f3016cb
item5.patch.txt            4c03910c76fdcbf2
item6.patch.txt            f65da5c3ce8433ec
item4.patch (1).txt        a516c2c144c1f2f6
surf_p01.patch.txt         62c4d021e5b6f0a0
surf_p01_obs1-2.patch.txt  69964afec17b9c0f
surf_p02.patch.txt         e039c74bc9993640
```

**Next:** SURF-P03 — audit trail, RBAC, scope records, API catalogue, route inventory, plugin contracts, workspace preferences. Note that CONV item 5 already surfaced the governance overlay (Audit Explorer, Evidence Viewer, platform posture); SURF-P03 scoping must establish what remains genuinely unsurfaced rather than re-home what exists. I will inventory before issuing the Build Order.

---

Gate **CLOSED**.
Production **NOT CERTIFIED**.
This determination approves **SURF-P02** and closes `TD-061`. It is not authorization for SURF-P03, DATA, CHART or POLISH.

**We don't guess. We prove.**
