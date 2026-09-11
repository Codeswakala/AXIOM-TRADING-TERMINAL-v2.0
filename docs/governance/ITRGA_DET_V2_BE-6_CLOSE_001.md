# ITRGA Determination — BE-6 Working-Lineage Closure (0046 Application Act)

| Field | Value |
|---|---|
| Document Id | **ITRGA-DET-V2-BE-6-CLOSE-001** |
| Classification | Working-lineage closure record (band BE-6; working-DB half of BO-V2-BE-6-001) |
| Issued | 2026-09-03 (Africa/Nairobi +03:00) by the ITRGA |
| Subject act | 0046 working-DB application act (single sanctioned mutation: `alembic upgrade 20260903_0046` on the application's SQLite working database) |

---

## 1. Verdict

The **0046 working-database application act is COMPLETE and CLOSED.** The application act ran inside its sanction envelope, was proven at application time and independently re-proven at verification time, and the working lineage now stands at revision **`20260903_0046`**. The terminal state of BO-V2-BE-6-001 is on the working lineage. Band **BE-6 is fully closed**: the repository half closed at ITRGA-DET-V2-BE-6-ACCEPT-001; the working-database half closes by this record. The Operator's authorization to restart the application was issued upon receipt of the verify PASS (2026-09-03, verify run 22:29:08–22:29:27 +03:00).

## 2. Authority chain (closed)

`ITRGA-COMMISSION-V2-BE-6-001` → plan request `ITRGA-REQ-V2-BE-6-PLAN-001` → plan review/acceptance `ITRGA-PRV-V2-BE-6-PLAN-001` → build order **BO-V2-BE-6-001** → delivery-report intake `ITRGA-INT-V2-BE-6-DR-001` (C-1 PASS; 15/15 file-body re-hash) → final determination **ITRGA-DET-V2-BE-6-FINAL-001** (C full-verify PASS; §7.3 instrument contract) → acceptance **ITRGA-DET-V2-BE-6-ACCEPT-001** (repository half closed; sync completed) → scope assessment and commissioning **ITRGA-ASSESSMENT-V2-0046-APPLY-SCOPE-V1** (incl. pre-act disclosure N-1: anchor-as-is) → instrument issuance **ITRGA-ISSUANCE-V2-0046-PACKS-001** (with Addenda 1 and 2) → **this closure record**.

## 3. Terminal state of record (working lineage at `20260903_0046`)

Proven twice by independent instrument suites (apply A5–A7 at 18:45; verify B2–B9 at 22:29), with byte-identity between the two proven by gate B1:

- **Revision:** exactly `20260903_0046` (repository head; chain …0043 → 0044 → 0045 → 0046).
- **Triggers:** 32 v2 triggers, exact-named — 28 inherited intact + 4 BE-6 guards (`v2_portfolio_definition_immutable_update/delete`, `v2_portfolio_risk_report_immutable_update/delete`) with exact refusal messages proven live.
- **Tables:** `v2_portfolio_definition`, `v2_portfolio_risk_report` — pinned column name-sets, PK `id`, all seven named constraints in stored DDL, both uniqueness anchors proven **behaviorally**, both indexes exact-named; both tables **empty**.
- **Computation versions:** 6 rows — three BE-4 rows pinned by value (`fe9aab42…28dd35`, `69902503…0af3a8c`, `3887d6ca…912180`); mge/sge proven by runtime recomputation (`83e73e24…49dcff`, `dd1f308e…3fee439`); `portfolio_risk_engine = pre-1.0.0` (evidence_ref **BO-V2-BE-6-001**) equal to the runtime recomputation of the four pinned engine files **and** to the pinned anchor `5c6d8f08809680506694032a5580616d6e15c13ecfa7a59a1d4a0fd869cec90a` (identical recomputation on both runs).
- **Permissions:** 41 rows — 8 additive BE-5 rows (0045) + 6 additive BE-6 rows, all content-exact, no role+permission duplicates; forbidden-vocabulary posture per FINAL-001.
- **Inherited:** BE-1..BE-3 provider/history/audit anchors content-exact; all five BE-5 tables still empty.
- **Drift:** `alembic check` at the head — exactly the **9 inherited V1 tokens**, zero BE-6/V2 tokens (1 added table + 2 added indexes + 6 removed indexes; the same set at both the 0045 and 0046 closures).
- **Environment:** no authority variables (`AXIOM_TD_*`/`AUTHORITY_REF`) at any point; no credentials used or prompted.
- **File identity of record (terminal):** `backend\axiom_dev.db` = **1,490,944 bytes**, sha256 **`5bd60aff6ab2d7fb6889b60363653b1d5e95d4405f15c0a7220a649ed233e795`**, last write **2026-09-03 18:45:24 +03:00** — unchanged through the verify act (recorded per PGF-001: bytes are seed-time-dependent).

## 4. Custodial timeline of the act (all +03:00, 2026-09-03)

1. **00:44–09:44** (recorded anchors): the post-0045 restart's lawful bootstrap-admin row (disclosure N-1); DB pre-act image 1,445,888 B / `7ac43e5f…fce2`, last write 09:44:01.
2. **17:21:50** — first-issuance apply pack attempted; **halted at the A0b/A0c boundary on PGF-016** (instrument-production seam defect); **no database contact of any kind**. Custodial proof issued; pair revoked (Addendum 1).
3. **18:44:46 → 18:45:24** — the corrected apply pack ran **to a full PASS**: A1 baseline exact (`20260902_0045`, full Tier-2 re-proof), A2 anchor created+verified, A3 36 provenance pins exact, A4 the **single sanctioned mutation** (`alembic upgrade 20260903_0046`), A5–A7 complete post-state proof, A8 verdict PASS; state record written. Complete run transcript preserved by the Operator (50,515 B paste — the **witness of record**).
4. Between 18:46 and 21:31 — machine power loss; the verify pack was not run; **no process touched the database**.
5. **21:31:31–21:31:38** — duplicate apply run: startup hygiene deleted the PASS transcript and the PASS state record (**E-0046-DUP**); gate A1 then refused on `20260903_0046 (head)` — **replay protection held; zero mutation**; abort transcript (5,543 B) written.
6. **22:29:08–22:29:27** — verify instrument **V2** (evidence-continuity resumption): record absence asserted as the continuity marker; witnessed identity embedded; **B1 byte-binding to the live DB held exactly**; full independent content re-proof PASS. Verdict PASS; environment cleaned.
7. **22:3x** — operator disk/hash bundles received and matched for every artifact (§5).
8. This record closes the act.

## 5. Evidence register (all artifacts; hash-bound)

**Instruments of record (ITRGA-issued; repository root):**

| File | Bytes | MD5 | SHA-256 | Status |
|---|---|---|---|---|
| `ITRGA_V2_0046_APPLY_PACK_V1.ps1` | 102,350 | `fabac10eb1e67aa3fcac596269e73870` | `d9309bea66c6ea2a4469b1a847fa0fc7db8e9571a5b3e804cfb7d9daa9918225` | **EXECUTED — PASS** (18:44 run). **Do not run again** (replay-protected; duplicate-run startup hygiene erases markers — E-0046-DUP). |
| `ITRGA_V2_0046_VERIFY_PACK_V1.ps1` | 78,597 | `dea461ecbaf86f08acc96c26fb27ee1d` | `ca63701eb28da9eeef07e2300c570c25584f8cddc788fe8fd09df0b5cecdb868` | **SUPERSEDED — do not execute** (consumes the destroyed state record by design). |
| `ITRGA_V2_0046_VERIFY_PACK_V2.ps1` | 80,462 (1,465 lines) | `2c8409ef60cc1ceec8e00e12b75c57c1` | `b7fade3c2fc8652ec6b7b1d66a8272e9bb7e07e03f7915e089501706f35188a7` | **EXECUTED — PASS** (22:29 run); act-closing instrument. |

**Machine-side artifacts (operator-held; `operator-evidence\BE-6\`; keep in place — rollback and audit register):**

| Artifact | Bytes / last write | SHA-256 |
|---|---|---|
| `axiom_dev.db.pre-0046-20260903184515.bak` (recovery anchor; current-as-is pre-image per N-1, incl. bootstrap-admin row) | 1,445,888 B / 2026-09-03 09:44:01 AM | `7AC43E5F4495F17AD6057034075B14009D6B4D9D1D50E03347307E288DC7FCE2` |
| `0046-VERIFY-RUN-V2.txt` (verify transcript of record) | 31,387 B / 2026-09-03 10:29:27 PM | `2545F0F6FC616B965453161EF3721E691128D1B3D6C9AB15746F208EE4160A05` |
| `0046-APPLY-RUN-V1.txt` (21:31 duplicate-run abort transcript; E-0046-DUP record) | 5,543 B / 2026-09-03 9:31:38 PM | `33134B71C3E939F62CCB7C431BEAAC83A0265A5346AAB28C7D4F55E2901B329F` |
| `0046-APPLY-FINAL-STATE.txt` | **absent by design** — destroyed by E-0046-DUP; absence is the continuity marker asserted at verify gate B0e. Hand-recreation prohibited (Addendum 2, A2.2(d)). |

**ITRGA-held witnesses (console pastes received full-depth):** the 18:44 apply-PASS transcript paste (50,515 B); the 21:31 abort paste; the 17:21 PGF-016 halt paste; the V2 verify paste (33,586 B incl. hash-check prefix; the 31,387 B file above is its pack-written form); the disk-floor bundle; the artifact hash bundle (this section).

## 6. Events and lessons registered for the act

- **PGF-016** (corrected): instrument-production seam defect in the first-issuance pair (builder `keep_end` inversion; AST-invisible valid-token duplication). Corrected by direct exact-text repairs of the `.ps1` instruments; re-validated (seam inventory, duplicate/glue/whitespace/ASCII scans, AST PASS, helper byte-pairing); builder/simulator tooling closed per the standing rule (development belongs to the DA). Recorded in Addendum 1.
- **PGF-017** (provisional → **vacated**): apparent out-of-envelope advance; determination: the advance was the instrument's own sanctioned upgrade (18:44 run), unreported due to power loss. Recorded, with timeline proof, in Addendum 2.
- **E-0046-DUP** (instrument event): unconditional startup `Remove-Item` of transcript + state-record paths destroys a completed run's markers on re-invocation. Zero database impact; fully witnessed-around. Rule for all future instruments recorded in `ITRGA_PRACTICE_NOTE_V2_PACK_DISCIPLINE_001.md`, §5 postscript: **a completed-run marker at startup ⇒ STOP ("already applied — report to ITRGA"); never delete the marker.**
- **IO-0046-V2-1** (cosmetic, instrument feedback; no action): verify V2's B3 summary line retains the V1-era phrase "the apply act's record"; the bindings it verified were the witnessed pins (correctly echoed on the gate's own lines). Future practice: when an instrument's identity source changes (record → embedded witness), sweep every narrative PASS-line for the old source's name.
- **Console-paste artifacts:** operator pastes eat spaces at line wraps; the evidence of record is the pack-written transcript file (also enforced by pack design). Held witnesses are consistent with the files (§5).

## 7. Full-depth review declaration

Both run transcripts (apply 18:44; verify V2 22:29) and the abort transcript (21:31) were reviewed full-depth against the §7.3 instrument contract and the act checklist: single sanctioned mutation inside the envelope with anchor-before-mutation; fail-closed read gates (A1 refused a wrong baseline twice — once by defect-era design intent, once by replay protection; B1 byte-binding held); no credential prompts; no authority variables; exact pin bindings at every stage (instruments, 36 provenance files, migration `1e95ce49…`, anchor, terminal file); content re-proof strict (Tier-2) with Tier-1 recorded-only by disclosed policy; transactional probe hygiene (all throwaway rows rolled back; tables empty after probes); environment cleanup at every run end. All findings: PASS, complete, mutually consistent.

## 8. Register content for the DA (exact supply; DA office applies — not for operator-shell execution)

Annex entries below are the ITRGA office's exact text supply; the DA owns their incorporation into the registers.

**Annex A — for `V2_CURRENT_STATE.md` (working lineage):**

```
| Working lineage (application's SQLite dev database) | alembic revision 20260903_0046 (band BE-6 applied 2026-09-03 by sanctioned apply act; verified by ITRGA-V2-0046-VERIFY-PACK-V2 under the E-0046-DUP continuity ruling); terminal identity 1,490,944 B / sha256 5bd60aff6ab2d7fb6889b60363653b1d5e95d4405f15c0a7220a649ed233e795; closure ITRGA-DET-V2-BE-6-CLOSE-001 |
```

**Annex B — for the BO terminal-state register (BO-V2-BE-6-001):**

```
| Working-lineage half | COMPLETE (2026-09-03): apply act PASS (18:44–18:45 +03) witnessed; verify act PASS (22:29 +03); closure ITRGA-DET-V2-BE-6-CLOSE-001; band BE-6 fully closed |
```

**Annex C — for the provenance/incident register:**

```
PGF-016 (instrument-production seam defect; corrected in place; pair re-issued) — closed. PGF-017 (provisional out-of-envelope advance) — VACATED (the advance was the sanctioned 18:44 apply; power-loss reporting gap). E-0046-DUP (duplicate-run startup hygiene erases completed-run markers) — recorded; hygiene rule added to pack-discipline practice note §5. IO-0046-V2-1 (cosmetic PASS-line wording residue in verify V2 B3) — recorded; no action.
```

## 9. Closure

The 0046 application act is closed with the working lineage at `20260903_0046`. All instruments stand archived as-executed; the anchor and the two on-disk transcripts remain the rollback/audit register and must not be moved, renamed, edited, or deleted. The next act is the next build order.

— ITRGA, 2026-09-03
