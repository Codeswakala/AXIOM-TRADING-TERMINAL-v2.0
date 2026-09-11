# ITRGA-DET-V2-0043-APPLY-001 — Closure Determination: 0043 Working-Database Application Act

Determiner: ITRGA (Independent Technical Review and Governance Agent, V2 governance chain; succession ITRGA-REA-V2-SUCCESSION-001)
Date of determination: 2026-09-02 (Africa/Nairobi)
Act closed: 0043 working-database application act (back-end work item BE-4; operator decision AXIOM-V2-OD-BE-4-009)
Issuance under test: ITRGA-V2-0043-PACKS-001 (`docs/governance/ITRGA_ISSUANCE_V2_0043_PACKS_001.md`)
Evidence: the Operator's console transcripts (apply run `0043-APPLY-RUN-V1.txt`, verify run `0043-VERIFY-RUN-V1.txt`, final-state record `0043-APPLY-FINAL-STATE.txt`, and the console text of both runs, received 2026-09-02; archive copy at `/home/user/operator-runs/ITRGA-V2-0043-OPERATOR-RUN-CONSOLE-20260902.md`)

## VERDICT: THE 0043 ACT IS CLOSED — VERIFIED COMPLETE AND IN FORCE

Both issued acts report their PASS verdicts on the operator console, and every terminal condition of the build order (BO-V2-0043-APPLY-001, T-1..T-11) is individually verified from the returned transcripts.

## 0. Channel integrity (verified first)

The operator's recorded hash verification precedes execution in the console transcript and matches the issuance table exactly:

| artifact | operator-observed SHA-256 | issued (pinned) SHA-256 | match |
|---|---|---|---|
| `ITRGA_V2_0043_APPLY_PACK_V1.ps1` | 6E2B4C5DD96D83E489DA9FE177CCD0011937D006380208C48438D3A286CE9021 | 6e2b4c5dd96d83e489da9fe177ccd0011937d006380208c48438d3a286ce9021 | YES |
| `ITRGA_V2_0043_VERIFY_PACK_V1.ps1` | 206A175F6868F90B8D4261AE8C3B8DA8B36C71517BA8005F7A3C949DC5D034B4 | 206a175f6868f90b8d4261ae8c3b8da8b36c71517ba8005f7a3c949dc5d034b4 | YES |
| `ITRGA_V2_0043_BASELINE_PINS.txt` | DC67BCA8355BA0FF5A973ED290A001E8DE148DD1B33F222D52C7D35C02735CB5 | dc67bca8355ba0ff5a973ed290a001e8de148dd1b33f222d52c7d35c02735cb5 | YES |

The executed bytes are certifiably the issued bytes.

## 1. Terminal-state verification table (T-1..T-11 vs the operator transcripts)

| condition | apply-pack evidence | verify-pack evidence | result |
|---|---|---|---|
| T-1 revision exactly 20260831_0043 | A5.1 PASS — `20260831_0043 (head)` after exactly one literal-revision `upgrade 20260831_0043` | B2 PASS — `20260831_0043 (head)` | VERIFIED |
| T-2 18 v2 triggers; six BE-4 guard names exact | A5.2 PASS — 18 names enumerated verbatim (12 inherited + 6 new guards) | B1 PASS — same 18-name set re-enumerated | VERIFIED |
| T-3 six R-2 guards in force, exact refusal messages; four transition guards intact | A6 PASS — six exact refusals (`V2 computation version registry is immutable; UPDATE prohibited` / `…DELETE prohibited`; `V2 market context reports are immutable; UPDATE/DELETE prohibited`; `V2 chart intelligence reports are immutable; UPDATE/DELETE prohibited`); throwaway probe rows rolled back | B7 PASS — all six re-probed with the same exact messages; transition guards intact | VERIFIED |
| T-4 three BE-4 tables with the two unique constraints and the three indexes | A5.3 PASS | re-proven by B4/B5 content checks against the same tables | VERIFIED |
| T-5 exactly 5 BE-4 permission rows (admin x3, operator x2; SAL-aligned), no duplicates | A5.5 PASS — `PASS:perm_rows_exact`, `INFO:v2_permission_total=27` | B5 PASS — identical | VERIFIED |
| T-6 exactly 3 computation-version rows; versions, source_hash pins, evidence_ref exact | A5.4 PASS — `PASS:compver_rows_exact` with the ITRGA-recomputed pins `fe9aab42…`, `699025034…`, `3887d6ca…` | B4 PASS — identical helper verdict | VERIFIED |
| T-7 both report tables empty | A5.6 PASS, re-asserted after guard probes in A6 | B5 PASS, re-asserted in B7 | VERIFIED |
| T-8 integrity ok; journal delete; no sidecars | A5.8 PASS — post-file size 1359872, mtime 2026-09-02 17:04:58 +03:00, sha256 `947684f2bf292b006a14dd3433c07d4faddf5424fcea73a4e7bcdec35682696a` | B1 PASS — target file byte-identical to the apply record (same size/mtime/sha256) | VERIFIED |
| T-9 drift re-baselined to exactly the 9 inherited V1 tokens | A7 PASS — real alembic 1.19.0 head-satisfied output: itemized `Detected …` lines + `New upgrade operations detected: […]`, exit non-zero; token set exactly the 9 inherited V1 tokens; no v2_*/ix_v2_ token | B9 PASS — identical result | VERIFIED |
| T-10 no authority variable for this act | A0d sweep: none present at start; absence asserted | B0d + B8 PASS | VERIFIED |
| T-11 anchor proven — byte-identical 0042 pre-image | A2 PASS — `axiom_dev.db.pre-0043-20260902170451.bak`, 1310720 B, sha256 `0483f9fe12e3d71f514811571c64589d72c66ec47fb2a3a1f6e986715ca41006`, integrity ok, created BEFORE the only mutation | B3 PASS — anchor revision read from the anchor itself = 20260829_0042; sha256 matches BOTH the apply record AND the ITRGA-pinned pre-image | VERIFIED |

Cross-cutting proofs additionally present in the transcripts:
- Baseline gate: A1 confirmed the working file byte-identical to the ITRGA-pinned in-force state (1310720 B; 2026-08-31 14:09:55 +03:00; `0483f9fe…`; revision 20260829_0042; 12 triggers; journal delete; no sidecars) — the apply proceeded only on a verified baseline.
- Provenance: A3/B0f re-pinned all six chain migrations (0038..0043) on disk to the ITRGA-accepted hashes (0043: `ab90576203d9f7946154ad4efd7a3d52bc98b91e328dbf2a4dca0b5049bda84b`).
- Single mutation: one literal `alembic upgrade 20260831_0043` invocation; nothing else in the protocol writes to the database.
- Read-only enforcement: B10 — target byte-identical before/after the verify act (size, last write, sha256 all equal).
- Environment hygiene: `AXIOM_*` sets and removals evidenced; helper self-tests passed; helper removed on exit (both packs).

## 2. Battery-record correlation (the pre-flight battery was predictive, not decorative)

- **F2 (drift-marker breadth) proved decisive in production:** the operator's own `alembic check` (real 1.19.0, head satisfied) printed exactly `New upgrade operations detected: […]` with itemized `Detected …` lines — the form the battery empirically established. The pre-battery assertion (literal `not up to date` only) would have failed this exact output; the fixed dual-marker + format-independent extraction asserted it correctly in A7/B9.
- **F1 (B3 anchor-revision read) proved decisive:** the anchor revision was correctly read from the anchor file (20260829_0042) rather than from the working database; the triple-check (state record + pinned pre-image + anchor content) stands.
- The recorded PASS shapes match the W2 world battery transcripts section-for-section (drift token set, guard-refusal strings, `v2_permission_total=27`, compver pins, anchor/profile values), and the negative-case fail-closed proofs (N1..N4) stand untriggered — i.e., no abort branch fired in production, as expected on a conforming machine.

## 3. Recorded notes (no action required)

- Cosmetic console rendering: Windows PowerShell 5.1 decorates native stderr (alembic INFO lines) as `NativeCommandError` blocks; the transcripts show these decorations around expected INFO output only. Behavior-by-design in the packs (native stderr is captured and asserted as data, never trusted implicitly); no effect on any gate.
- SQLite 3.50.4 / alembic 1.19.0 / provider end state `contract_tested|verified|0` recorded as environment evidence.
- 43 migration files enumerated with hashes in B0g (recorded, not asserted).

## 4. Dispositions

- The working database `backend\axiom_dev.db` is now at revision 20260831_0043 and is the in-force terminal state. The application may be restarted.
- The recovery anchor `operator-evidence\BE-4\axiom_dev.db.pre-0043-20260902170451.bak` (the 0042 pre-image, sha256 `0483f9fe…`) is RETAINED as the only sanctioned rollback pre-image for this act. Its restoration is itself a future gated act; it is not to be restored casually.
- The transcripts, final-state record, pins file, and this determination are the act's permanent record.
- The issued packs (V1) are now CONSUMED/SINGLE-USE; any re-run is a new act requiring new ITRGA issuance (the state they were built against no longer holds: the baseline is 0043, not 0042 — by design the packs would refuse at A1).

Determination rendered under the V2 governance chain. Artifact of record; changes by superseding determination only.

— ITRGA
