# ITRGA RULING — BE-8 0048 ACT HALT (AXIOM-V2-BE-8-0048-HALT-001)

- **Record:** ITRGA-RULE-V2-BE8-HALT-0048-001 · v1.0.0 · 2026-09-05 · **BLOCKING VERDICT: HALT LAWFUL — ACT VOID AT §3.3 — RE-TARGET AUTHORIZED, DISPOSITIONS RULED**
- **Reviews:** DA halt evidence set (ACT_HALT_RECORD §1–§6, CENSUS, DB_PINS, HALT_MANIFEST) against ITRGA-ACT-V2-BE-8-0048-001 and the chain's sealed records.

## 1 — Independent verification of the halt evidence (all performed, none trusted)

| Claim in the halt record | ITRGA verification | Result |
|---|---|---|
| Station census 20/20 pre-flight + post-halt re-census | Machine-parsed `V2_BE-8_0048_CENSUS.txt`: exactly 40 rows, every hash+size == ACT §2 pin table, all MATCH | **VERIFIED** |
| Anomaly measurements (80 tables, 0 triggers, no alembic_version, no changelog, paper tables pre-present, 1 auth row 2026-09-04T20:23:17Z) | Internally consistent; the auto-create signature (all 80 model tables, zero seeds, zero triggers) matches models-metadata creation exactly; paper tables pre-present is impossible on lawful 0047 lineage | **COHERENT** |
| Zero mutation across the act (pre == backup == post-halt == `b64b8400…cdc0`, 1,699,840 B) | DB_PINS internally consistent; backup exists outside apply path; identity retained pre/post | **VERIFIED** (self-pinned; strong) |
| Station file is NOT the working lineage | Sealed working-DB identity `27bda311…c776f` confirmed against **ITRGA's own records** (`ITRGA_CLO_V2_0047_BE7_ACT_001.md` §1; `0047-APPLY-RESUME-RUN-V1.txt` PRE==POST lines; `ITRGA_ISS_V2_0047_PACKS_007.md` B1/B2 pins). Station artifact `b64b8400…` = different artifact | **VERIFIED vs my own sealed files** |
| Evidence-set self-manifest (5,975 / 5,090 / 2,129 B; md5+sha256 declared) | Re-hashed the three uploaded files: 3/3 md5 OK, 3/3 sha256 OK, 3/3 sizes OK | **VERIFIED** |
| Backup retained; debris untouched pending ruling | Proper E-0046-DUP behavior — a suspect artifact is RULED on, never removed unilaterally | **DOCTRINE CONFORMANT** |

## 2 — Ruling

1. **The halt is the failure doctrine operating correctly, not a failure.** §3.2 proved the corpus act-ready (20/20); §3.3 refused a false target (a database with no alembic lineage, yet BE-8 tables present — upgrading it would have forged an evidence set against a fake lineage). The act is **VOID at §3.3**; §3.4–§3.8 never ran; no re-run is permitted except under this ruling's re-issue. The DA's full root-cause disclosure (its own debug-harness debris squatting on the config-default filename) is entered into the record with no penalty — disclosed debris, reported, untouched.
2. **(a) Re-target — RULED.** The 0048 application is re-issued **in console-pack form** against the true working lineage on the Operator console (the 0043/0045/0046/0047 household pattern), with a hard pre-mutation identity gate: DB sha256 must equal the sealed `27bda311…c776f` **and** `alembic current == 20260903_0047`. The Operator's authorization of record stands — same authorized act, corrected target mechanics; the Operator may suspend or revoke at will, but no new authorization is required. Pack family (STAGE/APPLY/VERIFY), PGF-022-validated gates, byte/MD5 identities of record to follow in `ITRGA-ISS-V2-0048-PACKS-001`. All carried pins: §2 corpus (20 files), §4 census values (57/58/10, 8 tables), compver PXS/PRG exact hashes, drift law (zero BE-8 tokens both heads, 9-token inherited class), suite 1,026/0, refuse-if-completed + pure-read-until-apply + failure-law-unchanged.
3. **(b) Debris — RULED: quarantine-rename by instruction (NO deletion).** DA executes on its station:
    - `backend/axiom_dev.db` -> `backend/axiom_dev.db.QUARANTINE-V2-BE8-20260905`
    - **Return evidence:** post-rename sha256 print == `b64b8400…cdc0` (byte-preservation proof) + directory listing showing the working filename ABSENT on the DA station + statement that `operator-evidence/BE-8/0048-ANCHOR-axiom_dev.bak` is retained, untouched.
    - Rationale: the debris is evidence of the root cause and a lawful tombstone; deletion can only happen under a later explicit order. Leaving it under the working filename is refused (it would re-squat the hazard).
4. **(c) Prevention — ADOPTED as a standing workspace rule, effective immediately** (to be registered as PGF-candidate at the next battery revision): *DA-side harnesses must always export an explicit `AXIOM_DATABASE_URL` (`:memory:` or a `/tmp` path) — never fall through to the config default.* The DA has committed to encoding this in its generators.
5. **Observation (non-blocking, no act this cycle):** the hazard amplifier is that the config-default path IS the working filename. Hardening the default (e.g., refuse-to-auto-create on it outside test mode) is a candidate for a future governed change — **expressly excluded from this act; no code edits under any act order.**

## 3 — Chain state after this ruling

- Working lineage: **untouched**, sealed 0047 state on the Operator console at `27bda311…c776f`.
- Delivered corpus: frozen, act-ready, 20/20 pinned — twice attested (pre-flight + post-halt) on the DA station.
- Act: VOID (first attempt). Re-targeted console-pack issuance follows (`ITRGA-ISS-V2-0048-PACKS-001`).
- Awaiting DA return: (i) quarantine-rename evidence per §2.3; (ii) acknowledgment of the §2.4 standing rule.
- After packs field-run PASS: ITRGA act review -> CLO/SEAL -> DA register sync (staged line incl. F-e verbatim).

**We don't guess. We prove.**
