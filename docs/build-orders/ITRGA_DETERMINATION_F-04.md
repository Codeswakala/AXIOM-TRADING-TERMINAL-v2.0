# ITRGA DETERMINATION — BO-F-04
## Alerts Center Completion (domain filtering + lineage/timestamp surfacing)

| Item | Value |
|------|-------|
| Review identity | ITRGA independent review of DA Delivery Report `DELIVERY_REPORT_F-04.md` |
| Build Order | `BO-F-04` (Operator-authorized 2026-08-21) |
| Predecessors | F-03 CLOSED · B-05 (emission) · SURF-P02 (existing alerts surface) |
| Date | 2026-08-21 |
| Evidence standard | Level I (direct) / Level II (executed) / Level III (documentary) |

---

## 1. What I verified (Level I/II — reproduced in my custody)

| Check | Result |
|-------|--------|
| **CA-TRANSMIT-1** | **HONORED** — all 11 declared artifacts present, all 11 hashes match |
| Patch `f04.patch.txt` sha256 | `920f8acf…` — **matches** |
| `git apply --check` + apply | **Clean** (exit 0) |
| Patch composition | 5 files (4 frontend + register), **zero backend** |
| `alertDomain(alert)` | **Data-origin-derived** — documented priority over persisted fields (`signal_id`→signal, `model_artifact_id`→risk, `market_series`/`market_class`→market, `system_component`→system, else→research neutral) — no invented categories |
| `formatAlertTimestamp` | Absolute UTC, honest raw-string fallback on invalid input |
| D3 churn (deep-links test) | **Genuine strengthening fix** — moved the two fixture assertions *inside* the `waitFor` (async race where assertions fired before provider population) — no assertion removed/weakened |
| New F-04 tests | **13/13 passed** |
| **Full frontend suite** | **970 passed / 186 files, 0 failures** |

## 2. Acceptance criteria vs. Build Order — line-by-line

| BO §8 requirement | Status |
|-------------------|--------|
| Five-domain filter present + functional | ✓ (ALL + 5 domains, role=tablist, filtered/total count) |
| Domain assignment data-origin-derived | ✓ (verified mapping in code) |
| Every alert card renders absolute UTC + provenance/lineage | ✓ (Created + Lineage lines) |
| Ack read-state-only preserved (no optimistic update) | ✓ (provider M2 untouched; capture confirms after-API) |
| Honest empty/error states | ✓ ("No alerts in the X domain." distinct from global empty) |
| Register rows in patch | ✓ (pure-addition) |
| Full suite + typecheck green | ✓ |

**All acceptance criteria met.**

## 3. The pivotal properties — verified

1. **The domain filter is honest derivation, not invention.** The `alertDomain` mapping reads only the alert's persisted fields in documented priority order, with "research" as the neutral bucket for unknown/null subjects. Nothing is guessed client-side.

2. **Timestamps and lineage are now visible.** Every card carries absolute-UTC `Created` and `Lineage: {source}` (honest "Lineage: none" fallback), so an operator can see *when* and *from where* each alert came — the accountability surface the roadmap required.

3. **The ack discipline held.** The provider's M2 behavior (render acknowledged state only after the API confirms — no optimistic update) is untouched, and the capture shows 4→3 unacked + one "Ack: yes" after the POST 200.

## 4. The OBS-F03-1 closure — this is significant

The D3 churn fixed the **exact test that failed in my F-03 environment** (`test_surf_p02_dock_alerts_deep_link_activates_the_alerts_tab`). I verified:

- The churn is a genuine async-race fix (assertions moved inside `waitFor`), not a weakened assertion.
- **My clone now runs the full suite green (970/186, 0 failures)** — the prior failure is resolved, and the "baseline divergence" I flagged was actually a *pre-existing timing flake* that the DA correctly diagnosed and fixed.

This closes OBS-F03-1's substance: the full-suite discrepancy was a race, not a custody divergence. My re-baseline recommendation (OBS-F03-2) becomes optional rather than required — though re-baselining to `7e4d993` would still make the count exact.

## 5. Observations (non-blocking)

- **OBS-F04-1 (Info):** the capture observed the B-AUDIT defensive path fire once (a ws-ticket audit row couldn't verify in 2 attempts + the durable marker couldn't persist, so the structured-log final record fired — **non-silent**, endpoint still 200). This is the residual OBS-B-AUDIT-1 materializing exactly as designed: file-sqlite business-write transaction merging remains, and the future serialization unit is still recommended. The mechanism held; nothing was silently lost.
- **Carried:** react-router MODERATE advisories (RR7 migration); file-sqlite serialization (backend future unit).

## 6. Determination

| Field | Value |
|-------|-------|
| Determination | **APPROVED WITH OBSERVATIONS** |
| Basis | All acceptance criteria met; data-origin domain mapping; timestamp/lineage surfacing; ack discipline preserved; D3 churn verified as a genuine race fix (full suite now green in my custody); register-in-patch honored |
| Observations | OBS-F04-1 (B-AUDIT residual materialized non-silently — future unit recommended) |
| Next authorization state | **F-04 CLOSED** — F-05 (lineage & evidence visualization) may be issued |
| What this is not | Not production certification; not gate-opening; not authorization beyond BO-F-04 |

## 7. Record

- Patch: `920f8acf36682398958ab86e6ebca47a856e6cdabdc230d90aca78e33462d895`
- 13/13 new tests · full suite 970/186 green (the OBS-F03-1 test now passes) · register-in-patch
- Domain filter + timestamp/lineage verified; ack read-state-only preserved

> **We don't guess. We prove.** The alerts center is now complete: five honest domains, visible timestamps and lineage, and a read-state-only ack that survives. And the DA's strengthening churn resolved the exact flake I'd flagged — my clone now runs the full suite green. Approved.

**End of ITRGA Determination BO-F-04**
