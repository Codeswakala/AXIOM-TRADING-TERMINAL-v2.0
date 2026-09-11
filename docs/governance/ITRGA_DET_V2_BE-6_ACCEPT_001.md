# ITRGA FINAL ACCEPTANCE RECORD + BUILD-ORDER CLOSURE — V2 BE-6

- **RECORD_ID:** `ITRGA-DET-V2-BE-6-ACCEPT-001`
- **Date:** 2026-09-03
- **Authority:** the Operator's final acceptance authorization of 2026-09-03 ("proceed with acceptance authorization"), received after `ITRGA-DET-V2-BE-6-FINAL-001` (verdict C: full-verify PASS).
- **Chain:** `ITRGA-CN-V2-BE-6-001` → `ITRGA-REQ-V2-BE-6-PLAN-001` → `ITRGA-PRV-V2-BE-6-PLAN-001` (plan ACCEPTED) → **BO-V2-BE-6-001** → DR v1.0.0 intake (C-1) → DR v1.0.1 (C-1 closed) → determination C-PASS → **this record**.

## 1. Acceptance recorded

The Operator's authorization is recorded against the recommendation in the final determination §7. With it:

- `AXIOM-V2-BE-6-DR-001` **v1.0.1** stands as the delivery of record (Rev-2 evidence plane; annex Rev 1).
- **BO-V2-BE-6-001 is CLOSED.** Terminal state T-1…T-12 complete on the in-band evidence planes (DA-executed Level I; 911 passed / 0 failed; drift gates at both heads; P-7 recomputation executed by the ITRGA), with no objection to its reproduction on the working lineage when 0046 is applied as the separate sanctioned act.
- **Correction register:** C-1 CLOSED (both clusters). **C-2 (editorial, deferred-class) remains open** until its appointed transmission: the DA re-stamps the three stale cells of DR v1.0.1 (§2 T-9 "906/0" → floor 911 = 856 + 55 with itemization 17/7/14/17; §3 heading; T-8 cell audit enumeration) at the next evidence-channel package (0046-application sync or register-touch package, whichever first). The authoritative floor everywhere from this record onward: **911**.

## 2. Maturity grant

| Register row (`V2_CAPABILITY_MATURITY.md`) | Band | New state | Evidence | Date |
|---|---|---|---|---|
| `Portfolio Research` | BE-6 | **COMPLETE** | ITRGA-DET-V2-BE-6-FINAL-001 (verdict C full-verify) | 2026-09-03 |
| `Risk Research` | BE-6 | **COMPLETE** | same | 2026-09-03 |

The grant is the acceptance act's, not the DA's (DR §6 staged IMPLEMENTED only).

## 3. Evidence inventory (closing the band; full hashes; all byte-verified by ITRGA recomputation)

| Artifact | Revision | MD5 | SHA-256 |
|---|---|---|---|
| `V2_BE-6_SOURCE_TRANSCRIPT.md` (REM-001; 15/15 literal pins re-hashed exact) | Rev 2 | `5c4d0f4edaf254a91792d4e3b2fd5c67` | `8f134b229f2651a7228c2ab7a702952c404364b53ffb8ae297aca8102bd01bd4` |
| `V2_BE-6_API_TRANSCRIPT.txt` (Level I; 15/15 ASSERTs; §6 C-1 probes; drift PASS) | Rev 2 | `4b6a9067b38c439e7394fb4d1054d50c` | `4a2937fea487227ec4d242461692032ca421e77f16ca0a4762fd0cda60c94d77` |
| `V2_BE-6_TESTRUN_TRANSCRIPT.txt` (raw `-v`; 911/0) | Rev 2 | `6f7911c8ab118e9e15197e9a1fe35b90` | `8b875d046fab2e4c3d5f6671ef57c64a7c7c524efa249988ed2dcefc32add0ab` |
| `V2_BE-6_WORKED_SAMPLE_ANNEX.md` (P-7; **P-7 executed by the ITRGA — all values reproduced**) | Rev 1 | `6727334e26c77e08348442e18006938d` | `4c2bfe99f1074208f75889877200fb21649e7b2759a40698ff6b4eafdf98cf02` |

## 4. Registry synchronization package (**DA applies — register content is the DA's ownership per the Operator's standing correction**; ITRGA supplies exact content and verifies)

1. **`V2_CURRENT_STATE.md`** (root): add the Completed-Bands BE-6 entry and update the Active Band row to *"NONE — BE-6 ACCEPTED, CLOSED, AND SYNCHRONIZED"* with the chain citation (CN-001 → REQ → PLAN PRV → BO-001 → DR v1.0.1 → FINAL-001 C-PASS → this record); floor line: **test baseline going forward: 911** (module itemization 17/7/14/17); bands closed BE-0…BE-6; forward register: BE-7 (Backtesting, Simulation, Replay, and Governed Research Jobs) per roadmap order, each next act requiring its own Operator authorization. **Note:** the DA's BE-5-era Next-Actions curation observation (duplicate numbering; stale 0043-era items incl. "ITRGA migration in progress") remains routed for the same touch.
2. **`V2_CAPABILITY_MATURITY.md`**: the two BE-6 rows → COMPLETE with the evidence/date of §2.
3. **Risk register +2:** *hypothetical-mistaken-for-account-state* — mitigated structurally (single-value `basis`/`basis_label` CHECKs probed; labels on every response; forbidden-vocabulary guard); *metric-overtrust* — mitigated by the mandatory uncertainty/limitations contract per metric and the both-VaR-methods-separated rule. Both: BE-6, Mitigated.
4. **Tech-debt register +2:** *long-only v1 allocations scope* (short/leveraged = future band); *grouping-not-regression factor scope* (regression factors = future band). Both: deferred by design, disclosed in output limitations.
5. Re-serialize per the 30.x convention at the last edit.

## 5. File placement (verify on placement)

Place the four artifacts under `docs\evidence\` preserving the DR §5 filenames; then verify hashes (expected values in §3 — `Get-FileHash -Algorithm SHA256`, compare case-insensitively). Any mismatch: stop, do not place, report. (If, as in BE-5, the DA has already placed them: run the same verification — it is the placement act either way.)

## 6. Forward register (nothing else owed in BE-6)

- **The 0046 working-DB application is the next separate sanctioned act** — commissioned only by your authorization. Its instrument contract is fixed in the determination §7.3 (REM-Rev-2 literals as the recompute source; `pre-1.0.0` compver hash re-pinned exactly; behavioral probes; census pins 32/41/6; drift itemized; tri-binding; simulated validation first).
- **C-2** re-stamp at the next evidence transmission (§1).
- BE-7 stands in the roadmap queue; commissioning conversations only on Operator authorization.

**INSCRIBED as `ITRGA-DET-V2-BE-6-ACCEPT-001`. Band BE-6: accepted, closed, synchronized-ready pending the DA's register touch. We don't guess. We prove.**

---

### ADDENDUM (2026-09-03) — placement act

Operator executed the placement verification on his machine; all four artifacts found at `docs\evidence\` (DA-placed) and their `Get-FileHash` results **byte-matched the §3 pins** (SOURCE `8F134B22…01BD4` · API `4A2937FE…94D77` · TESTRUN `8B875D04…2ADD0AB` · ANNEX `4C2BFE99…8CF02`). **File placement act: PASS, complete.** The DA-side register sync (§4) is issued via relay with exact insert/replace text; post-sync review runs on the Operator's read-only verification output.

### ADDENDUM 2 (2026-09-03) — post-sync review: **CLOSED**

The DA applied the §4 package; Operator verification returned and reviewed in full. All six items verified byte-level: **(1)** `V2_CURRENT_STATE.md` — header serialized by the DA (36.0.0 / 2026-09-03, his 30.x-series ownership), Completed-Bands BE-6 entry byte-verbatim against the issued insert (chain citations through ACCEPT-001; "**test baseline going forward: 911**"), Active Band row replaced as issued (bands closed BE-0…BE-6; C-2 and 0046 as sole open registers), **Next Actions curated** — the carried BE-5-era item is done (duplicates merged, the three stale 0043-era items incl. "ITRGA migration in progress" removed; residue items 1–2 added verbatim; standing posture incl. OBS-9 retained). **(2)** Capability rows 55/56 COMPLETE with the §2 citation, verbatim. **(3)** Risk V2-R-35/36 present, verbatim. **(4)** Debt V2-TD-22/23 present, verbatim. **(5)** Placement PASS (Addendum 1). **(6)** Floor **911** carried everywhere. **BAND BE-6 IS AT REST IN FULL.** Open-by-design registers only: C-2 (editorial re-stamp, at the next evidence transmission) and the 0046 working-DB application (separate sanctioned act, awaiting Operator commission).
