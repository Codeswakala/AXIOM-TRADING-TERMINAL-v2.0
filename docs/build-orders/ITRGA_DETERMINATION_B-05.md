# ITRGA DETERMINATION — BO-B-05
## Monitoring & Alerts Emission

| Item | Value |
|------|-------|
| Review identity | ITRGA independent review of DA Delivery Report `DELIVERY_REPORT_B-05.md` |
| Build Order | `BO-B-05` (Operator-authorized 2026-08-20) |
| Predecessors | B-00 → B-04 (all APPROVED WITH OBSERVATIONS) · Reconciliation Determination · predictive deferral |
| Date | 2026-08-20 |
| Evidence standard | Level I (direct) / Level II (executed) / Level III (documentary) |

---

## 1. What I verified (Level I/II — reproduced independently)

| Check | Result |
|-------|--------|
| **CA-TRANSMIT-1** | **HONORED** (second consecutive) — all 6 artifacts present, all 5 hashes match |
| Patch `b05.patch.txt` sha256 | `33abf5e6…` — **matches** |
| `git apply --check` + apply | **Clean** (exit 0) |
| 6 post-apply file SHAs | **All 6 match** |
| Emission module | Calls the four real `create_*_alert` services; **no actuation identifiers** (only `.order_by()` SQL + boundary prose) |
| D2 static-guard exemption | **Narrow, commented, justified** — the `/alerts/inference-health` endpoint *reports* health input, does not *perform* inference; the guard's intent still covers every other router |
| New B-05 tests (8) | **8/8 passed** (incl. ack-read-state-only + no-actuation-surface) |
| **Full backend suite** | **530 passed** — matches report (530 / 156.86s) |
| Emission log | check #1 → 3 alerts; check #2 → 0 (dedup); inference-health → full fields + 409 dedup; ack → read-state only, subject signal untouched |

## 2. Acceptance criteria vs. Build Order — line-by-line

| BO requirement | Status |
|-----------------|--------|
| Stale-data alert fires on genuine threshold breach, deduped | ✓ `test_b05_stale_feed_emits_deduped_alert` + `test_b05_fresh_feed_emits_no_alert` |
| Inference-health + drift + withheld wired, test-proven | ✓ all pinned; no new drift algorithm (honored) |
| Every alert carries severity/lineage/timestamp/condition-key | ✓ verified in emission log (all fields present) |
| ack mutates read-state only | ✓ test-pinned + log-verified (subject signal `withheld/STALE_INPUT` untouched) |
| Existing list/get/ack surface unchanged | ✓ GET /alerts returns the 4 emitted alerts |
| Full suite green | ✓ 530 passed |

**All acceptance criteria met.**

## 3. The pivotal properties — verified

1. **Alerts now actually fire.** The four `create_*_alert` methods that had zero callers are now wired to real conditions. The emission log shows 4 distinct alert types persisted and readable, with correct severity, lineage, subject keys, and timestamps.

2. **Dedup works.** Check #1 emitted 3; check #2 (same conditions) emitted 0; inference-health's second identical POST returned 409. No spam possible (bounded cooldown).

3. **Non-actuation holds.** The most important property: ack flipped the alert's read-state and left the underlying withheld signal (`withheld/STALE_INPUT`) byte-unchanged. Alerts inform; they never act. This is pinned by two dedicated tests and confirmed in the live probe.

## 4. Deviation D2 — reviewed and accepted (the one risk point)

D2 discloses that two pre-existing static inertness guards initially tripped on the new module, and that one test (`test_model_harness.py`) now exempts `monitoring_alerts.py` from its "no inference endpoint" scan. I examined this directly:

- The exemption is **narrow** (a single file), **commented** with the BO-B-05 rationale, and the guard's *intent* — "no live model/signal inference endpoint" — still covers every other router.
- The `/alerts/inference-health` endpoint genuinely **reports health degradation input** (schema-validated `degraded`/`down`) rather than performing inference. The semantic distinction is real and correct.
- The module was rewritten (`session.execute()` → `session.scalars()`) so the *other* guards still pass unchanged — no guard was weakened.

**Assessment: accepted.** The exemption is the correct, minimal, disclosed treatment of a genuine supersession, consistent with the B-04 D1 precedent (405→422) and the standing "churn must be stricter, not weaker" discipline.

## 5. The honest deferral note (verified, not papered over)

- `INFERENCE_HEALTH` and `SIGNAL_WITHHELD` fire from **explicit inputs and persisted withheld rows** — not from live model inference, because there is no promoted model (Operator's predictive deferral).
- The delivery discloses this plainly (§10), and it is the correct consequence of the deferral. Nothing is fabricated; the wiring is real and test-proven, awaiting a future model.

## 6. Observations (non-blocking)

- **OBS-B05-1 (Info):** emission remains on-request (the bounded `/alerts/check` + `/alerts/inference-health` paths), not a background actor — as the BO intended.
- **Carried:** PROJECT_STATE.md inventory staleness; W3-U03 semantic-narrowing record; fingerprint-determinism hardening.

## 7. Determination

| Field | Value |
|-------|-------|
| Determination | **APPROVED WITH OBSERVATIONS** |
| Basis | All acceptance criteria met; CA-TRANSMIT-1 honored; 6/6 SHAs; 8/8 new + 530/530 full suite; non-actuation + dedup proven |
| Observations | OBS-B05-1 (non-blocking) |
| Next authorization state | **B-05 CLOSED** — B-06 (Governed Assistant ask path) may be issued; F-04 (alerts center) is unblocked |
| What this is not | Not production certification; not gate-opening; not authorization beyond BO-B-05 |

## 8. Record

- Patch: `33abf5e610de48e18ed7bcbe406b7b4f6ee04de0d6c4ba3f69c5788a16787e6d`
- Post-apply: 6/6 file SHAs · 8/8 new · 530/530 full suite
- Emission verified: 4 alert types fire, dedup, read-state-only ack, no actuation

> **We don't guess. We prove.** The monitoring layer now actually emits its alerts, deduplicated, read-state-only, and non-actuating — and the evidence arrived complete for the second delivery running. Approved.

**End of ITRGA Determination BO-B-05**
