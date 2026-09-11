# ITRGA-V2-0043-PACKS-001 — Issuance of the 0043 Apply and Verify Packs

Issuer: ITRGA (Independent Technical Review and Governance Agent, V2 governance chain)
Date of issuance: 2026-09-02 (Africa/Nairobi)
Act family: 0043 working-database application act (back-end work item BE-4; operator decision AXIOM-V2-OD-BE-4-009)
Plan under construction: ITRGA-PLAN-V2-0043-APPLY-001 (sections A0..A8 / B0..B10)
Scope assessment: ITRGA-ASS-V2-0043-APPLY-001
Build order: BO-V2-0043-APPLY-001 (terminal state T-1..T-11)
Operating rule of this issuance: NO act is executed before its battery is archived; each act stays gated. The Operator executes the packs on the operator console; the ITRGA verifies the returned transcripts against T-1..T-11 and renders the closure determination (ITRGA-DET-V2-0043-APPLY-001).

Standing operator constraints on record (ITRGA standing instructions, received 2026-09-02):
- The provided repo link is temporary storage only (bootstrap of a new DA/ITRGA; data recovery on operator-machine failure). ALL COMMITS strictly belong to the Operator; the ITRGA must never commit to it.
- Workspace budget: the sandbox persists a maximum of ~128 MB / 10,000 files; heavy transient test infrastructure must not persist.
- Development rights belong to the DA; the ITRGA operates strictly inside its mandated verification/governance scope as approved per act.

---

## 1. Issued artifacts (the ONLY sanctioned bytes)

The three artifacts below are issued as a set. Byte-identity is pinned here; the operator instruction card (section 4) requires these hashes to be verified BEFORE any execution.

| artifact | size (bytes) | SHA-256 | MD5 |
|---|---:|---|---|
| `ITRGA_V2_0043_APPLY_PACK_V1.ps1` | 68187 | 6e2b4c5dd96d83e489da9fe177ccd0011937d006380208c48438d3a286ce9021 | 8fc9336598238222c42f98402295b2a9 |
| `ITRGA_V2_0043_VERIFY_PACK_V1.ps1` | 61099 | 206a175f6868f90b8d4261ae8c3b8da8b36c71517ba8005f7a3c949dc5d034b4 | 8c225ab94a900a40d6b4cd34518c7b74 |
| `ITRGA_V2_0043_BASELINE_PINS.txt` | 543 | dc67bca8355ba0ff5a973ed290a001e8de148dd1b33f222d52c7d35c02735cb5 | a23c999838c2113c53d3035f8a39cad6 |

Placement (operator machine, repository root `C:\Users\victo\.vscode\AXIOM\axiom`): all three files at the repository root; the apply pack locates the pins file and the evidence directory relative to the root.

Supersession marks (explicit):
- `ITRGA_V2_0043_BASELINE_PINS.txt` pins the working database file `backend\axiom_dev.db` at its recorded in-force state (size 1310720; last write 2026-08-31 14:09:55 +03:00; SHA-256 0483f9fe12e3d71f514811571c64589d72c66ec47fb2a3a1f6e986715ca41006; revision 20260829_0042; 12 v2 triggers; journal delete; no sidecars). **Any change to that file before execution invalidates the pins**; the apply pack will abort at A1 in that event, by design.
- These are V1 bytes of the 0043 pack set. Any re-issue increments the version (V2, ...) and this record's hashes are then superseded; the newer issuance record names the superseding hashes.
- This issuance supersedes no prior 0043 pack set (none exists). It does not supersede the retired predecessor pack lineage (V1..V5 apply / V1..V3 verify), which remains RETIRED and must not be executed.

## 2. Pre-issuance static audits (all on the exact issued bytes)

- Pure ASCII: 0 non-ASCII bytes in either pack.
- PowerShell AST parse (PowerShell 7.4.6 `[System.Management.Automation.Language.Parser]::ParseFile`): 0 parse errors in each pack. Constructs compatible with Windows PowerShell 5.1 (no ternary, no null-coalescing, no `&&`/`||` chains).
- Braced-expansion span audit: every `${...}` span is a bare identifier (apply pack 186/186; verify pack 156/156; zero exceptions) — PGF-009 class discipline.
- Environment sweep discipline: the packs enumerate and remove `AXIOM_TD_*` / `*AUTHORITY_REF*` variables at start and in the finally block, and assert their absence (this act has no authority variable; BO T-10).

## 3. Dry-run battery record (executed 2026-09-02, archived)

Battery root: `/home/user/battery-0043/` (archive at `/home/user/battery-0043/archive/`; controller and shim preserved as `harness.battery.py.txt`, `harness.alembic_check_shim.py.txt`).
Runtime: PowerShell 7.4.6; per-case copies of a faithful 0042-state replica of the working database; exact-issued pack bytes; pinned world-specific measurements written by the harness (never a pack edit).
Archive note (2026-09-02, workspace budget enforcement): heavy transient worlds (PS runtime, venvs, DB replicas) were purged post-run per the standing workspace-budget constraint; the archived evidence is the per-case console logs, pins, and full transcripts/state records, plus the harness sources. The battery was re-executed once after that purge from a re-constructed identical world (7/7 PASS) so the archived transcripts correspond to the final issued bytes.

Worlds:
- **W2 (recorded environment)**: real venv (backend `requirements.txt` + `alembic==1.19.0`, the recorded operator alembic version; SQLAlchemy 2.0.52). Replica built by running the real migration chain to `20260829_0042` and validated (revision; 12 triggers; provider `contract_tested|verified|0`; start+complete audit rows; no BE-4 tables).
- **W1 (run-1-format emulation)**: identical real venv, with `alembic check` answered by a shim that reprints the run-1-recorded output FORMAT faithfully (itemized `Detected ...` lines + `Target database is not up to date.`, exit non-zero). Provenance honesty: the run-1 venv's alembic version was never pinned in the record; no installable alembic 1.9.4-1.19.0 reproduces that combination (see the format map below). The shim exercises the pack's format-tolerance branch against the format ON RECORD; the recorded environment itself is proven in W2 with real tooling.
- **N1**: identical to W2, one byte of the database flipped after pinning.
- **N2**: identical to W2, one byte appended to the 0043 migration file (provenance violation).
- **N3**: identical to W2 with `20260831_0043` pre-applied by real alembic (operand already applied).
- **N4**: identical to W2 with the evidence directory made non-writable (anchor creation fails). Substitution note (on record): the anchor-integrity injection is not world-injectable without pack edits; the anchor Copy-Item failure exercises the same FAIL-CLOSED / no-mutation branch.
- **VERIFY**: the verify pack run against the W2 case after its PASS apply.

Battery matrix (expected vs actual; full transcripts archived):

| case | expectation (pac-man profile) | actual | result |
|---|---|---|---|
| W2-apply | PASS; all A1..A8 asserts; 6 guard-refusal proofs; head-satisfied verbose drift branch; revision 0043; 18 triggers; state record; one anchor | identical | **PASS** |
| W2-verify | PASS; B1..B11 asserts incl. B3 anchor triple-check; read-only enforcement re-stat | identical | **PASS** |
| W1-apply | PASS; itemized `not up to date` drift branch | identical | **PASS** |
| N1 | non-zero exit; FAIL verdict at the first violated A1 gate; no state record; no anchor; DB bytes unchanged | abort at A1.1 (`alembic current` fails: database disk image is malformed); bytes unchanged | **PASS** |
| N2 | non-zero exit; FAIL at A3 provenance hash mismatch; anchor exists (A2 precedes A3 by design); DB bytes unchanged; revision 0042 | identical | **PASS** |
| N3 | non-zero exit; FAIL at A1.1 revision gate (`expected exactly '20260829_0042'`); no state record; no anchor; DB unchanged at 0043 | identical | **PASS** |
| N4 | non-zero exit; FAIL at A2 anchor creation; no anchor created; DB unchanged | identical | **PASS** |

### Battery findings that changed the packs (defects found pre-flight — the battery's purpose)

- **V2-0043-BATTERY-F1 (verify pack, fixed):** B3's anchor revision probe read from the working database object (the shared `Get-PyScalar` idiom) rather than from the anchor file; on the true post-apply state that check always fails. Fixed by reading the revision from the anchor file itself; annotated in-pack; W2-verify PASS proves the fix.
- **V2-0043-BATTERY-F2 (both packs, fixed):** the drift-marker assertion required the literal `not up to date`. The real recorded alembic 1.19.0, on a head-satisfied database, instead prints `New upgrade operations detected: [...]` (exit 255) with itemized `Detected ...` lines on stderr — the earlier W2 attempt failed exactly on that false expectation. Both packs now accept either RECORDED marker form and extract drift names format-independently (itemized quoted/unquoted, plus `Table('<name>')` / `Index('<name>')` repr forms), retaining the PGF-014 summary fallback purely as defensive format tolerance.
- **Harness-level findings (controller only; not pack defects):** pwsh 7.x on Linux normalizes `.venv\Scripts\python.exe` separators for `Join-Path`/`Test-Path` (Windows behavior verified unchanged by inspection of the resolution idiom); a case-name mismatch left an N-case tamper unapplied; an evidence-directory permission poison required permission restoration before case rebuild. All fixed and re-proven.

### Empirical `alembic check` format map (probed 2026-09-02; informs the format expectations above)

- DB revision != script head (e.g. 0042 vs head 0043): `ERROR ... Target database is not up to date.` + `FAILED: Target database is not up to date.`, exit 255, no drift detail — observed identically on alembic 1.9.4, 1.10.4, 1.11.1, 1.12.1, 1.13.3, 1.14.0, 1.15.2, 1.16.1, 1.17.1, 1.19.0.
- DB at head with model drift (the post-apply case; 9 ops observed): verbose stdout `FAILED: New upgrade operations detected: [<op reprs>]`; stderr itemized `Detected added table '<name>'` / `Detected added index '<name>' on ...` / `Detected removed index '<name>' on '<table>'` lines; exit 255.
- Source basis: `command.py` raises `AutogenerateDiffsDetected(f"New upgrade operations detected: {diffs}")`; `autogenerate/api.py` raises `CommandError("Target database is not up to date.")` when the DB revision set differs from the heads set (revision-offset refusal).
- The recorded run-1 transcript combination (itemized list + `not up to date`) is not reproduced by any installable version probed; W1 emulation stands as the faithful-format proxy for that recorded world.

### N1 severity note (recorded)

The working database file has no freelist pages and no slack (page size 4096; 320 pages; freelist 0). Any byte flip is structural: `alembic current` itself fails, so the pack aborts at A1.1 rather than at the A1.2 byte-identity gate. The invariant proven is the one the plan requires — abort BEFORE any mutation, FAIL verdict, no state record, database bytes unchanged. The sha gate remains reachable in principle for content-semantic deviations (the A1 gate ordering is recorded and unchanged).

## 4. Operator instruction card (verbatim)

1. Copy the three issued artifacts to the repository root (alongside the packs' predecessors location). Verify byte-identity BEFORE any execution:
   `Get-FileHash -Algorithm SHA256 <file>` and `Get-FileHash -Algorithm MD5 <file>` against the table in section 1. Any mismatch: STOP and report; do not proceed.
2. Confirm the working application is stopped (it holds a live connection to the database file).
3. Run `ITRGA_V2_0043_APPLY_PACK_V1.ps1` in an elevated-independent Windows PowerShell 5.1 console from the repository root. Its only prompt is the absolute path of the working database file (`C:\Users\victo\.vscode\AXIOM\axiom\backend\axiom_dev.db`).
   - Expected: `APPLY VERDICT: PASS` and a final-state record `operator-evidence\BE-4\0043-APPLY-FINAL-STATE.txt`.
   - On `APPLY VERDICT: FAIL`: do NOT re-run; do NOT edit anything; send the transcript `operator-evidence\BE-4\0043-APPLY-RUN-V1.txt` to the ITRGA.
4. Only if the apply act reports PASS, run `ITRGA_V2_0043_VERIFY_PACK_V1.ps1` the same way (read-only; same single prompt).
   - Expected: `VERIFY VERDICT: PASS`.
   - On `VERIFY VERDICT: FAIL`: do NOT re-run; send `operator-evidence\BE-4\0043-VERIFY-RUN-V1.txt` to the ITRGA.
5. Return to the ITRGA: both transcripts, the final-state record, and the console text (or screenshot pages) of both runs.
6. The packs prompt for NO credential of any kind. If a prompt for any credential occurs, the bytes are not the issued bytes: STOP and verify section 1.

## 5. Open tails (tracked)

- The run-1 venv alembic version is unpinnable (see format map); the battery records the emulated-world caveat. Requires no action; recorded for lineage accuracy.
- The battery environment is Linux pwsh 7.4.6; the operator console is Windows PowerShell 5.1. Pack constructs are 5.1-clean (static audits section 2); any residual console-difference behavior will surface as an explicit pack FAIL with transcript — never as silent divergence, by fail-closed design.

— ITRGA (succession ITRGA-REA-V2-SUCCESSION-001). Artifact of record; changes by re-issue only.
