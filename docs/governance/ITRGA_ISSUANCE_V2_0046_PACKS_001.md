# ITRGA ISSUANCE — V2 / 0046 WORKING-DATABASE APPLICATION ACT (BAND BE-6)

**Document ID:** ITRGA-ISSUANCE-V2-0046-PACKS-001
**Date:** 2026-09-03
**Authority:** ITRGA-DET-V2-BE-6-FINAL-001 (§7.3 instrument contract) · ITRGA-DET-V2-BE-6-ACCEPT-001 · BO-V2-BE-6-001 · ITRGA-ASSESSMENT-V2-0046-APPLY-SCOPE-V1 (commissioning record; pre-act disclosure herein re-affirmed)
**Status:** ISSUED for execution by the Operator on the operator machine (Windows, PowerShell 5.1, VS Code tree `C:\Users\victo\.vscode\AXIOM\axiom`)

---

## 1. The two instruments (byte-exact identity)

Save BOTH files to the **repository root** (`C:\Users\victo\.vscode\AXIOM\axiom\`). Do not rename, re-save, or edit them.

| # | File | Pack ID | Bytes | MD5 | SHA-256 |
|---|------|---------|-------|-----|---------|
| 1 | `ITRGA_V2_0046_APPLY_PACK_V1.ps1` | ITRGA-V2-0046-APPLY-PACK-V1 | 103,259 | `5b615f3b894f7a2fab2a7e2f5b935556` | `2a85bc4bcc9c984d3254cba6838a85abacf2d4a90813ea3ab5a4451561af50bd` |
| 2 | `ITRGA_V2_0046_VERIFY_PACK_V1.ps1` | ITRGA-V2-0046-VERIFY-PACK-V1 | 79,441 | `8f7a8d5b27ffa6cb02d37ac78eec3e81` | `01dbc36da0d2e8801e2a0d4509ea9a36621951099bd36bf152228c122e7e6d2c` |

**Byte-identity check (run before anything else; from the repository root):**

```powershell
Get-FileHash .\ITRGA_V2_0046_APPLY_PACK_V1.ps1 -Algorithm SHA256
Get-FileHash .\ITRGA_V2_0046_VERIFY_PACK_V1.ps1 -Algorithm SHA256
```

The two printed hashes (case-insensitive) must equal the SHA-256 values above. **If either does not match: STOP. Do not run either pack. Report the mismatch to ITRGA.**

## 2. Instrument provenance and validation record (ITRGA-side)

Both packs are surgical adaptations of the proven instruments of record (`ITRGA_V2_0045_APPLY_PACK_V1.ps1` and `ITRGA_V2_0045_VERIFY_PACK_V1.ps1`), carrying all PGF-001…PGF-015 lessons by construction. Before issuance I validated, on this sandbox:

1. **AST parse** — both packs parse with zero errors (PowerShell 7.4.6 parser; 5.1-grammar-safe constructs only; pure ASCII; LF endings, same as the proven packs).
2. **Every-SQL-string simulation (PGF-015 law)** — against a fabricated database carrying the verbatim-pinned 0046 migration literals (exact table DDL with all seven named constraints, the four exact guard triggers and messages, the exact six permission seeds, the exact compver seed, the recorded rollback-safe probe shapes):
   - pre-state gates: 28-name trigger census; compver 5 rows incl. mge/sge runtime recomputation; permbe5 octet + total 35; provider pin; history/audit exact pins **proven tolerant of the restart-era bootstrap-admin audit row**; record-only digests captured;
   - post-state gates: 32-name census (added set exactly the 4 BE-6 guards; compver DELETE guard re-created); PRAGMA column name-sets 14/17 order-exact with PK `id`; all 7 named constraints in stored DDL; 2 indexes exact; autoindex census ≥ 2 per table; compver 6 rows with the BE-6 anchor **runtime-recomputed and asserted equal to the pinned anchor `5c6d8f08…9cec90a`** (the mismatch path was negative-tested and refuses correctly); permissions total 41 with the 6 additive rows content-exact; no-touch digests equal across the mutation;
   - probes: 4 BE-6 guard refusals with the **exact pinned messages**; both uniqueness anchors refused duplicate inserts **behaviorally** (`UNIQUE constraint failed` on exactly the pinned columns); all 3 CHECK probes refused by the named constraints (`ck_v2_pfdef_basis`, `ck_v2_pfrisk_status`, `ck_v2_pfrisk_basis_label`); inherited compver UPDATE/DELETE refusals intact on the new seed row; probe hygiene (rollback) confirmed — both BE-6 tables and all five BE-5 tables empty afterwards.
3. **Helper byte-identity** — the python helper embedded in the verify pack is byte-identical to the one in the apply pack (same binary; single sim covers both).
4. **Joint contract check** — the apply pack writes exactly the 14-key state record the verify pack strictly consumes; pin maps and guard-message literals are identical across the two packs; the verify pack binds the target file byte-for-byte to the apply act's recorded PASS state.

## 3. Scope law (reprise — nothing beyond this is sanctioned)

One chain step on the working lineage: `20260902_0045 → 20260903_0046`, executed **once**, via the single literal invocation `alembic upgrade 20260903_0046` (never `head`). The packs: stop on any deviation (fail-closed), re-pin all **36 provenance files** by hash before and after (9 chain migrations `0038…0046` + 27 delivered files; the four paths shared by both bands are pinned to the BE-6 Rev-2 literals), sweep and forbid any `AXIOM_TD_*` / authority variable, and write only: the two transcripts, one anchor copy, one apply-final-state record, all under `operator-evidence\BE-6`, plus a throwaway helper in the OS temp directory (removed on exit). No database file is created or deleted by the packs.

## 4. Preconditions (mandatory)

1. The application is **STOPPED** before the apply pack starts and **stays stopped until the verify pack has printed its PASS verdict** (it holds a live connection to `backend\axiom_dev.db`).
2. The BE-6 file set is placed in the repository tree exactly as delivered (the packs re-pin it and abort on any deviation).
3. The repo venv (`.venv`) with alembic is intact (the pack records the alembic version as environment evidence).
4. Only the working database file `backend\axiom_dev.db` is targeted; the packs refuse any other leaf name and any path inside `operator-evidence`.

## 5. Run card (operator; execution as files, never console-paste)

```powershell
# Step 1 — APPLY (from the repository root; PowerShell 5.1 console is correct)
powershell -NoProfile -ExecutionPolicy Bypass -File ".\ITRGA_V2_0046_APPLY_PACK_V1.ps1"
```

- Single expected input: the absolute path of the working database file, e.g. `C:\Users\victo\.vscode\AXIOM\axiom\backend\axiom_dev.db` (a path, not a credential — nothing else is asked; no password, no API key).
- Expected end: `APPLY VERDICT: PASS …` and the instruction `NEXT: run ITRGA_V2_0046_VERIFY_PACK_V1.ps1 NOW`.

```powershell
# Step 2 — VERIFY (immediately after; application still stopped)
powershell -NoProfile -ExecutionPolicy Bypass -File ".\ITRGA_V2_0046_VERIFY_PACK_V1.ps1"
```

- Same single input (the absolute database path).
- Expected end: `VERIFY VERDICT: PASS …` and `The application may now be restarted.`

**Fail-closed rule:** if either pack aborts with a `FAIL`/`STOP` verdict, change nothing in the repository and do not attempt a repair; send the transcript to ITRGA. The pack itself is the only sanctioned mutation channel, and it refuses to proceed outside the exact contract.

## 6. Send-back (closes the application act)

After the verify PASS, send ITRGA these two files (they are the complete evidence envelope):

```
operator-evidence\BE-6\0046-APPLY-RUN-V1.txt
operator-evidence\BE-6\0046-VERIFY-RUN-V1.txt
```

Keep `operator-evidence\BE-6\0046-APPLY-FINAL-STATE.txt` and the anchor copy (`axiom_dev.db.pre-0046-*.bak`) in place — they are the rollback register of record. Do not move, rename, or edit them.

## 7. Disclosure reprise (N-1, from the commissioning record)

The apply anchor is deliberately **current-as-is**: the post-0045 application restart lawfully wrote a bootstrap-admin row, so the recorded 0045-era file hash is **recorded only, not gated**. Strictness is carried instead by the Tier-2 content re-proof inside the packs (revision, exact trigger census, compver/permission content pins incl. runtime recomputation, provider/history/audit anchors) and by the byte-exact binding between the apply act's PASS record and the verify act. Rollback restores exactly the pre-act image that ran on the machine. This was disclosed pre-act and is embodied in the instruments, not an improvisation.

## 8. After the PASS envelope arrives

ITRGA reviews both transcripts full-depth against the instrument contract and the 11-law checklist; on verification it records the working lineage at `20260903_0046` (band BE-6 working-DB half complete) and issues the closure record. Register edits remain the DA's office; ITRGA supplies exact content only.

---
*End of issuance note — ITRGA-ISSUANCE-V2-0046-PACKS-001*
