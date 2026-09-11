# ITRGA DETERMINATION — BO-F-05
## Lineage & Evidence Visualization (traceability across the terminal)

| Item | Value |
|------|-------|
| Review identity | ITRGA independent review of DA Delivery Report `DELIVERY_REPORT_F-05.txt` |
| Build Order | `BO-F-05` (Operator-authorized 2026-08-21) |
| Predecessors | F-04 CLOSED · Reconciliation §17/§37 · B-00 provenance protocol |
| Date | 2026-08-22 |
| Evidence standard | Level I (direct) / Level II (executed) / Level III (documentary) |

---

## 1. What I verified (Level I/II — reproduced in my custody)

| Check | Result |
|-------|--------|
| **CA-TRANSMIT-1** | **HONORED** — all 9 declared artifacts present, all 9 hashes match |
| Patch `f05.patch.txt` sha256 | `cae375af…` — **matches** |
| `git apply --check` + apply | **Clean** (exit 0) |
| Patch composition | 9 files (8 frontend + register), **zero backend** |
| D3 honesty fix | **Verified** — the pre-F-05 `"exp-001"` fabricated fallback is gone; every absent field renders `"not recorded"` |
| `LineageEvidencePanel` | **Persisted-only** — `source_artifact` node per real id, real `report_hash` only when persisted, per-field "provenance not recorded", 12-source render cap with disclosure, illustrative default chain never rendered for real artifacts |
| New F-05 tests | **10/10 passed** |
| **Full frontend suite** | **980 passed / 187 files, 0 failures** |
| Capture log | Real report hash + audit correlation; 12 "Source artifact" nodes + cap; `fabricatedChainAbsent: true`; `panelControls: 0`; honest "not recorded" |

## 2. Acceptance criteria vs. Build Order — line-by-line

| BO §8 requirement | Status |
|-------------------|--------|
| Lineage surfaced on intelligence/signals/alerts where present | ✓ (all three surfaces; audit correlation + source ids + hashes) |
| Read-only lineage/evidence view for a selected value | ✓ (`LineageEvidencePanel`, reusing `ArtifactLineageTree`) |
| Absent lineage renders "provenance not recorded" | ✓ (per-field; test-pinned) |
| No mutation/actuation (read-only) | ✓ (`panelControls: 0`; test-pinned) |
| Scope discipline (no over-labeling of presentation values) | ✓ (intelligence tab bar + counter badges carry zero lineage controls) |
| Register rows in patch | ✓ (pure-addition) |
| Full suite + typecheck green | ✓ |

**All acceptance criteria met.**

## 3. The pivotal properties — verified

1. **Traceability is now real, not aspirational.** An operator can open any intelligence report, advisory signal, or alert and see — from the *persisted* record — its hash, audit correlation, source artifacts, and creator. The Reconciliation §17/§37 question ("where did this come from, what supports it, what are its limitations?") is now answerable in the terminal.

2. **No fabrication, even where a prior unit had one.** The most significant finding in this delivery is D3: the pre-F-05 signal stream had a **fabricated `"exp-001"` fallback** for a missing experiment id. F-05 replaced it with honest `"not recorded"`. This is exactly the kind of small, silent fabrication the platform's honesty discipline exists to catch — and the DA both found and fixed it on their own, then disclosed it. That is the integrity culture working.

3. **The illustrative chain is never passed off as real.** The `ArtifactLineageTree`'s default "market → features → model → report" chain (with its placeholder hash) is deliberately *not* rendered for real artifacts — it would invent relationships the record doesn't assert. The lineage panel renders persisted-only nodes, with a 12-source cap + disclosure for real reports whose per-bar lineage runs to hundreds.

## 4. Observations (non-blocking)

- **OBS-F05-1 (Info):** the 12-source render cap truncates real reports with hundreds of per-bar source ids. Correctly disclosed on-screen and in the report; a future "expand all / paginate lineage" enhancement is optional, not a correctness gap.
- **Carried:** react-router MODERATE advisories (RR7 migration); file-sqlite business-write serialization (backend future unit).

## 5. Determination

| Field | Value |
|-------|-------|
| Determination | **APPROVED WITH OBSERVATIONS** |
| Basis | All acceptance criteria met; persisted-only lineage; the exp-001 fabrication removed; read-only/no-actuation; scope discipline; register-in-patch; 10/10 new + 980/187 full suite green |
| Observations | OBS-F05-1 (render cap — info) |
| Next authorization state | **F-05 CLOSED** — F-06 (accessibility, performance & navigation legibility) may be issued — the final frontend unit before X-01 Terminal Tier |
| What this is not | Not production certification; not gate-opening; not authorization beyond BO-F-05 |

## 6. Record

- Patch: `cae375af459c95002d84ef795c92f4e19f0709c94c8549c987db61121f69db35`
- 10/10 new tests · full suite 980/187 green · register-in-patch
- Lineage verified persisted-only; the exp-001 fabrication removed

> **We don't guess. We prove.** The terminal now shows where its numbers came from — and it stopped fabricating the one field it used to invent. Traceability is real, read-only, and honest. Approved.

**End of ITRGA Determination BO-F-05**
