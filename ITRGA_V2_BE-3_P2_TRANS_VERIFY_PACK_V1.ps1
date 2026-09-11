# =====================================================================
# AXIOM V2 BE-3 P2 STATUS TRANSITION - ITRGA READ-ONLY VERIFY PACK (V1)
# Pack ID: ITRGA-V2-BE-3-P2-TRANS-VERIFY-PACK-V1
# Authority:
#   - AXIOM-V2-OD-BE-3-P2-005 (Operator decision - apply act re-scoped
#     to the SQLite working database)
#   - ITRGA-PLAN-V2-BE-3-P2-TRANS-VERIFY-001 (boundary table, stop
#     conditions)
#   - BO-V2-BE-3-P2-TRANS-001 section 6 (end state: contract_tested,
#     history 2)
#   - ITRGA-ASS-V2-BE-3-P2-TRANS-APPLY-RUN-V5 (apply attempt V5 record:
#     migration applied ONCE; verdict FAIL at B7 on ITRGA finding
#     PGF-012)
#   - Provenance anchor: accepted Revision-2 record (final migration
#     hash af77a63f903a43e2eb7b4426b67de7113791f37918bbfe7f465d8f1bab3cf8d4)
# Chain: sixth instrument of the BE-3 P2 transition chain (V1 of the
#   verify act). Predecessors: apply packs V1 (PG; retired for target),
#   V2/V3 (SQLite; superseded, PGF-008/009), V4 (SQLite; superseded by
#   dry run, PGF-010), V5 (SQLite; EXECUTED 2026-08-31: migration
#   applied ONCE, end state substantively in force, verdict FAIL at B7
#   on ITRGA check defect PGF-012).
#   V6 delta vs apply pack V5 (minimal, all other logic identical):
#   - READ-ONLY: no alembic upgrade, no chain establishment, no
#     authority variable SET, no backup creation, no no-op branch.
#   - B2 requires the baseline to be EXACTLY 20260829_0042 (head).
#   - New B3: recovery-anchor check (the apply act's backup file:
#     exact recorded name, pre-state content, hash recorded).
#   - PGF-012 correction: the history exact-content check is
#     CONTENT-BASED, never position-based: the history id column is a
#     uuid4 TEXT primary key (accepted migration source), so
#     "ORDER BY id" is lexicographic and NOT insertion order. The
#     defective position-based check (hashrow) is REMOVED from the
#     helper.
#   - Strengthened B6: audit exact-content check (exactly the
#     start + complete rows with the exact details strings from the
#     accepted migration source; compared in Python via chr(183) for
#     the middle dot).
#   - B1 additionally asserts the four guard trigger names are
#     present.
#
# WHAT THIS PACK DOES:
#   Verifies, READ-ONLY, that the end state of the proven migration
#   20260829_0042 (applied ONCE by the apply act on 2026-08-31) is in
#   force on the APPLICATION'S WORKING SQLITE DATABASE FILE:
#   contract_tested, verified, persistence false, history 2 (exact
#   content), audit exactly start + complete (exact content), guards
#   intact (exact refusal messages), authority variable unset, alembic
#   at head with the inherited V1 drift set only.
#   - It changes NOTHING in the database (no row, schema, trigger, or
#     alembic_version change; all SQL runs read-only or is a guarded
#     refusal probe that the triggers abort).
#   - It writes ONLY the transcript. The throwaway helper in the OS
#     temp directory is removed on exit.
#   - It does NOT create or delete any database file. It does NOT run
#     the downgrade/refusal proof. It does NOT create a backup.
#
# BEFORE RUNNING: STOP THE RUNNING APPLICATION (it holds a live
#   connection to the target database file). Restart it after the
#   pack completes.
#
# RUN MODE: this pack MUST be executed as a file.
#   Pasting the script into an interactive console is NOT an acceptable
#   evidence mode (PGF-004).
#
# Scope and credential law:
#   - No Twelve Data credential is read, set, or used.
#   - No provider network / contract test is performed.
#   - Operator inputs: exactly ONE - the absolute path of the working
#     database file (plain; it is not a credential). No password.
#   - The authority variable AXIOM_TD_TRANSITION_AUTHORITY_REF is
#     verified UNSET (pack-managed; this act NEVER sets it).
#
# Save this file to the AXIOM repository root:
#   C:\Users\victo\.vscode\AXIOM\axiom\ITRGA_V2_BE-3_P2_TRANS_VERIFY_PACK_V1.ps1
#
# Run from the AXIOM repository root, as a file (exactly one command):
#   powershell -NoProfile -ExecutionPolicy Bypass -File ".\ITRGA_V2_BE-3_P2_TRANS_VERIFY_PACK_V1.ps1"
#
# Output (submit this one file to ITRGA):
#   C:\Users\victo\.vscode\AXIOM\axiom\operator-evidence\BE-3-P2-transition\BE-3-P2-TRANS-VERIFY-EVIDENCE-V1.txt
# =====================================================================

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

# ---------------------------------------------------------------------
# 0. ENCODING, LOCAL PATHS AND TOOL CHECKS
# ---------------------------------------------------------------------

# Force UTF-8 for the console / python / transcript round trip so the
# middle dot (U+00B7) inside the EVIDENCE_REF value round-trips
# un-mangled in the informational row printout. The authoritative
# exact-content checks run in Python via chr(183) and do not depend
# on the console. This pack's own source is pure ASCII.
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
[Console]::InputEncoding  = [System.Text.Encoding]::UTF8
$env:PYTHONIOENCODING = "utf-8"

$RepoRoot    = (Get-Location).Path
$BackendRoot = Join-Path $RepoRoot "backend"
$Python      = Join-Path $RepoRoot ".venv\Scripts\python.exe"

if (!(Test-Path $BackendRoot)) { throw "Backend directory not found: ${BackendRoot}" }
if (!(Test-Path $Python))      { throw "Python executable not found: ${Python}" }

$EvidenceRoot = Join-Path $RepoRoot "operator-evidence"
$EvidenceDir  = Join-Path $EvidenceRoot "BE-3-P2-transition"
$Transcript   = Join-Path $EvidenceDir "BE-3-P2-TRANS-VERIFY-EVIDENCE-V1.txt"

New-Item -ItemType Directory -Force -Path $EvidenceDir | Out-Null
Remove-Item -Force -ErrorAction SilentlyContinue $Transcript

function Write-Evidence {
    param([string]$Text)
    Add-Content -Path $Transcript -Value $Text -Encoding UTF8
    Write-Host $Text
}

function Write-Section {
    param([string]$Title)
    Write-Evidence ""
    Write-Evidence ("=" * 78)
    Write-Evidence $Title
    Write-Evidence ("=" * 78)
}

function Emit-Output {
    param($Lines)
    foreach ($Line in @($Lines)) {
        Add-Content -Path $Transcript -Value ([string]$Line) -Encoding UTF8
    }
    $Lines | Out-Host
}

function Norm-Text {
    # Trimmed-line join for exact string comparison (strips stray CR).
    param($Lines)
    return (@($Lines | ForEach-Object { ([string]$_).Trim() }) -join "`n")
}

# ---------------------------------------------------------------------
# 0A. CONSTANTS
# ---------------------------------------------------------------------

$FinalMigrationHash = "af77a63f903a43e2eb7b4426b67de7113791f37918bbfe7f465d8f1bab3cf8d4"

# Working-database file name from backend\.env (refused if mismatched).
$ExpectedLeafName = "axiom_dev.db"

# Recovery anchor recorded by the apply act (attempt V5, 2026-08-31):
# the apply transcript records this exact file name and its pre-0042
# content; its sha256 (6db478ee...) is recorded there and is
# cross-checked by ITRGA against this act's recorded hash.
$ExpectedBackupName = "axiom_dev.db.pre-0042-20260831140931.bak"

# ---------------------------------------------------------------------
# 0B. OPERATOR INPUT (ABSOLUTE PATH OF THE WORKING DATABASE FILE)
# ---------------------------------------------------------------------

Write-Host ""
Write-Host "STOP THE RUNNING APPLICATION BEFORE CONTINUING (it holds a live"
Write-Host "connection to the target database file). Restart it after this"
Write-Host "pack finishes."
Write-Host ""
Write-Host "This pack VERIFIES (read-only) the end state of the already-applied"
Write-Host "transition migration 20260829_0042 on the application's SQLite"
Write-Host "WORKING DATABASE FILE. It changes nothing in the database."
Write-Host ""
Write-Host "This pack prompts for NO credential of any kind (no password, no API key)."
Write-Host ""

$TargetDbPath = (Read-Host -Prompt "Absolute path to the application's working SQLite database file (quotes optional; for example C:\Users\victo\.vscode\AXIOM\axiom\backend\axiom_dev.db)").Trim()
# PGF-008: Read-Host returns raw input; a PowerShell path-quoting habit
# leaves literal quote characters around the path. Quotes are not part
# of a file path - strip one matching pair of surrounding quotes.
if ($TargetDbPath.Length -ge 2) {
    if (($TargetDbPath.StartsWith('"') -and $TargetDbPath.EndsWith('"')) -or
        ($TargetDbPath.StartsWith("'") -and $TargetDbPath.EndsWith("'"))) {
        $TargetDbPath = $TargetDbPath.Substring(1, $TargetDbPath.Length - 2).Trim()
        Write-Host "NOTE: surrounding quotes removed from the entered path (quotes are not part of a file path)."
    }
}
if ([string]::IsNullOrEmpty($TargetDbPath)) {
    throw "No database file path entered. Aborting before any database access."
}
if (!(Test-Path ${TargetDbPath})) {
    throw "STOP: file not found: ${TargetDbPath}. Aborting before any database access."
}
$TargetItem = Get-Item ${TargetDbPath}
if ($TargetItem.PSIsContainer) {
    throw "STOP: path is a directory, not a file: ${TargetDbPath}. Aborting before any database access."
}
if ($TargetItem.Length -eq 0) {
    throw "STOP: file is empty (0 bytes): ${TargetDbPath}. Aborting before any database access."
}
$TargetDbPath = $TargetItem.FullName
$LeafName = Split-Path ${TargetDbPath} -Leaf
if ($LeafName.ToLower() -ne $ExpectedLeafName) {
    throw "STOP: file leaf name '${LeafName}' does not match the working database file name '${ExpectedLeafName}' from backend\.env. Aborting before any database access."
}
$EvidenceRootFull = (Resolve-Path $EvidenceRoot).Path
# PGF-009: bare expression - a ${...} containing calls is a literal
# variable name in PowerShell (proven on Windows PowerShell 5.1).
if ($TargetDbPath.ToLower().StartsWith($EvidenceRootFull.ToLower())) {
    throw "STOP: target file is inside the operator-evidence directory. Aborting before any database access."
}

# ---------------------------------------------------------------------
# 0C. PYTHON HELPER (written to the OS temp directory, removed on exit)
# ---------------------------------------------------------------------

$HelperDir  = Join-Path $env:TEMP "axiom_itrga_verify_v1"
$HelperPath = Join-Path $HelperDir "helper.py"
New-Item -ItemType Directory -Force -Path $HelperDir | Out-Null

$HelperSource = @'
import sqlite3
import sys


def ro_connect(db_path):
    uri = "file:" + db_path.replace("\\", "/") + "?mode=ro"
    return sqlite3.connect(uri, uri=True)


def main():
    cmd = sys.argv[1]
    db_path = sys.argv[2]

    if cmd == "selftest":
        con = ro_connect(db_path)
        try:
            value = con.execute("SELECT 1 AS helper_self_test").fetchone()[0]
            print(value)
        finally:
            con.close()
        return

    if cmd in ("scalar", "integrity", "journalmode", "verifyrows", "verifyaudit"):
        con = ro_connect(db_path)
        try:
            if cmd == "scalar":
                sql = sys.argv[3]
                rows = con.execute(sql).fetchall()
                for row in rows:
                    print("|".join("" if v is None else str(v) for v in row))
            elif cmd == "integrity":
                print(con.execute("PRAGMA integrity_check").fetchone()[0])
            elif cmd == "journalmode":
                print(con.execute("PRAGMA journal_mode").fetchone()[0])
            elif cmd == "verifyrows":
                # PGF-012 correction: the id column is a uuid4 TEXT
                # primary key (accepted migration source), so
                # "ORDER BY id" is lexicographic and NOT insertion
                # order. Rows are matched by CONTENT, never by
                # position.
                rows = con.execute(
                    "SELECT from_status, to_status, authority_ref, evidence_ref, operator_id "
                    "FROM v2_md_provider_status_history ORDER BY id"
                ).fetchall()
                if len(rows) != 2:
                    print("FAIL:history_count=" + str(len(rows)))
                    return
                tuples = [tuple(r) for r in rows]
                if tuples[0] == tuples[1]:
                    print("FAIL:duplicate_rows=" + repr(tuples))
                    return
                exp_genesis = (
                    None,
                    "architecture_candidate",
                    "BO-V2-BE-3-P1-001",
                    "AXIOM-V2-BE-3-DA-PLAN-001 v3.0.0 / ITRGA-DET-V2-BE-3-PLAN-001",
                    None,
                )
                exp_transition = (
                    "architecture_candidate",
                    "contract_tested",
                    "BO-V2-BE-3-P2-TRANS-001",
                    "ITRGA-DET-V2-BE-3-P2-FINAL-001 " + chr(183)
                    + " run a246607c-f0c5-42e9-8f3b-a1e1bd75fa83",
                    None,
                )
                if exp_genesis not in tuples or exp_transition not in tuples:
                    print("FAIL:rows=" + repr(tuples))
                    return
                print("PASS:history_rows_exact")
            elif cmd == "verifyaudit":
                # Exact start + complete rows from the accepted 0042
                # source (_in_transaction_audit). Non-deterministic
                # columns (id, correlation_id, created_at) are not
                # compared; action..details are compared exactly.
                rows = con.execute(
                    "SELECT action, actor_id, actor_type, domain, mode, classification, details "
                    "FROM v2_audit_event "
                    "WHERE action LIKE 'provider.status_transition%' "
                    "ORDER BY created_at"
                ).fetchall()
                if len(rows) != 2:
                    print("FAIL:audit_count=" + str(len(rows)))
                    return
                exp_start = (
                    "provider.status_transition.start",
                    "migration",
                    "operator",
                    "v2.marketdata",
                    "RESEARCH",
                    "internal",
                    '{"provider_id": "twelvedata", "from": "architecture_candidate", '
                    '"to": "contract_tested", "authority_ref": "BO-V2-BE-3-P2-TRANS-001", '
                    '"evidence_ref": "ITRGA-DET-V2-BE-3-P2-FINAL-001 ' + chr(183)
                    + ' run a246607c-f0c5-42e9-8f3b-a1e1bd75fa83"}',
                )
                exp_complete = (
                    "provider.status_transition.complete",
                    "migration",
                    "operator",
                    "v2.marketdata",
                    "RESEARCH",
                    "internal",
                    '{"history_count": 2, "post_status": "contract_tested", '
                    '"persistence_permitted": false}',
                )
                if tuple(rows[0]) != exp_start:
                    print("FAIL:audit_start=" + repr(rows[0]))
                    return
                if tuple(rows[1]) != exp_complete:
                    print("FAIL:audit_complete=" + repr(rows[1]))
                    return
                print("PASS:audit_rows_exact")
        finally:
            con.close()
        return

    if cmd == "tryrefuse":
        sql = sys.argv[3]
        con = sqlite3.connect(db_path)
        try:
            try:
                con.execute(sql)
                con.rollback()
                print("SUCCESS_UNEXPECTED")
            except sqlite3.Error as exc:
                print("REFUSED:" + str(exc))
        finally:
            con.close()
        return

    print("FAIL:unknown_command=" + cmd)
    sys.exit(2)


main()
'@

Set-Content -Path $HelperPath -Value $HelperSource -Encoding ASCII

# ---------------------------------------------------------------------
# COMMAND HELPERS (parameter names avoid built-in common-parameter
# aliases; see PGF-001)
# ---------------------------------------------------------------------

function Invoke-Py {
    param(
        [Parameter(Mandatory = $true)][string[]]$PyArgs,
        [string]$Label
    )

    Write-Evidence ""
    Write-Evidence "PYTHON-HELPER: helper.py $($PyArgs -join ' ')"

    $prev = $ErrorActionPreference
    $ErrorActionPreference = "Continue"
    try {
        $Out  = & $Python ${HelperPath} @PyArgs 2>&1
        $Code = $LASTEXITCODE
    } finally {
        $ErrorActionPreference = $prev
    }

    Emit-Output $Out

    if ($Code -ne 0) { throw "helper failed (exit code ${Code}): ${Label}" }
    return $Out
}

function Get-PyScalar {
    # Silent scalar read (no transcript line); the companion Invoke-Py
    # call prints the same statement for the record.
    param(
        [Parameter(Mandatory = $true)][string]$Sql,
        [string]$Label
    )

    $prev = $ErrorActionPreference
    $ErrorActionPreference = "Continue"
    try {
        $Out  = & $Python ${HelperPath} "scalar" ${TargetDbPath} ${Sql} 2>&1
        $Code = $LASTEXITCODE
    } finally {
        $ErrorActionPreference = $prev
    }

    if ($Code -ne 0) { throw "scalar query failed (exit code ${Code}): ${Label}" }
    return (Norm-Text $Out)
}

function Invoke-Alembic {
    param(
        [Parameter(Mandatory = $true)][string[]]$AlembicArgs,
        [string]$Label
    )

    Write-Evidence ""
    Write-Evidence "ALEMBIC: alembic $($AlembicArgs -join ' ')"

    $prev = $ErrorActionPreference
    $ErrorActionPreference = "Continue"
    try {
        $Out  = & $Python -m alembic @AlembicArgs 2>&1
        $Code = $LASTEXITCODE
    } finally {
        $ErrorActionPreference = $prev
    }

    Emit-Output $Out
    if ($Code -ne 0) { throw "alembic $($AlembicArgs -join ' ') failed (exit code ${Code}): ${Label}" }
    return $Out
}

function Invoke-ExpectedRefusal {
    param(
        [Parameter(Mandatory = $true)][string]$Label,
        [Parameter(Mandatory = $true)][string]$Sql,
        [string]$ExactMessage
    )

    Write-Evidence ""
    Write-Evidence "EXPECTED-REFUSAL: ${Label}"
    Write-Evidence "SQL: ${Sql}"

    $Out = Invoke-Py -PyArgs @("tryrefuse", ${TargetDbPath}, ${Sql}) -Label $Label
    $Text = (Norm-Text $Out).Trim()

    if ($Text -notlike "REFUSED:*") {
        throw "FAIL: expected refusal did not occur (statement succeeded or helper error): ${Label}"
    }
    if ($Text -notlike "*${ExactMessage}*") {
        throw "FAIL: exact expected message was not observed: ${Label}"
    }
    Write-Evidence "PASS: exact refusal message observed."
}

# ---------------------------------------------------------------------
# SECTION 0 - RUN IDENTIFICATION
# ---------------------------------------------------------------------

Write-Section "0. RUN IDENTIFICATION"
Write-Evidence "Pack: ITRGA-V2-BE-3-P2-TRANS-VERIFY-PACK-V1"
Write-Evidence "Pack note: V1 of the verify act (sixth instrument of the transition chain) - READ-ONLY verification of the applied end state; PGF-012-corrected content-based history check; all other logic per the verified apply pack V5"
Write-Evidence "Operator decision: AXIOM-V2-OD-BE-3-P2-005 (apply act re-scoped to the SQLite working database)"
Write-Evidence "Apply act record: BE-3-P2-TRANS-APPLY-EVIDENCE-V5.txt (migration 20260829_0042 applied ONCE; verdict FAIL at B7 on ITRGA finding PGF-012)"
Write-Evidence "Plan: ITRGA-PLAN-V2-BE-3-P2-TRANS-VERIFY-001"
Write-Evidence "Build order: BO-V2-BE-3-P2-TRANS-001 (section 6 end state)"
Write-Evidence "Final migration hash (applied; re-anchored here): ${FinalMigrationHash}"
Write-Evidence "Started: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss zzz')"
Write-Evidence "Repo root: ${RepoRoot}"
Write-Evidence "Target file (APPLICATION'S WORKING DATABASE - named by the Operator): ${TargetDbPath}"
Write-Evidence "SQL engine: SQLite (in-process, via the repo venv python sqlite3 module; no database server)"
Write-Evidence "Python (repo venv): ${Python}"
Write-Evidence "Server credentials used: NONE (no database server; no password prompt)"
Write-Evidence "Provider credentials used: NONE"
Write-Evidence "This pack is READ-ONLY with respect to the database: no alembic upgrade, no row/schema/trigger/alembic_version change, no authority variable set, no backup created. It writes only the transcript."

Push-Location $BackendRoot

try {

    # -----------------------------------------------------------------
    # SECTION 1 - HELPER SELF-TEST (READ-ONLY)
    # -----------------------------------------------------------------

    Write-Section "1. HELPER SELF-TEST"

    [void](Invoke-Py -PyArgs @("selftest", ${TargetDbPath}) -Label "helper self-test")

    # -----------------------------------------------------------------
    # SECTION 2 - RUN ENVIRONMENT (NO PROVIDER CREDENTIALS)
    # -----------------------------------------------------------------

    Write-Section "2. RUN ENVIRONMENT (NO PROVIDER CREDENTIALS; AUTHORITY VARIABLE NEVER SET BY THIS ACT)"

    $TargetDbPathUrl = $TargetDbPath.Replace("\", "/")
    $env:AXIOM_DATABASE_URL       = "sqlite+aiosqlite:///" + ${TargetDbPathUrl}
    $env:AXIOM_ENVIRONMENT        = "testing"
    $env:AXIOM_ALLOW_INSECURE_DEV = "true"
    $env:AXIOM_JWT_SECRET_KEY     = "operator-local-test-secret-at-least-32-characters"
    $env:AXIOM_V2_MODE            = "RESEARCH"

    Remove-Item Env:\AXIOM_TD_API_KEY -ErrorAction SilentlyContinue
    Remove-Item Env:\AXIOM_TD_API_KEY_FILE -ErrorAction SilentlyContinue
    Remove-Item Env:\AXIOM_TD_CONTRACT_TEST_ENABLED -ErrorAction SilentlyContinue
    Remove-Item Env:\AXIOM_TD_P2_AUTHORITY_REF -ErrorAction SilentlyContinue
    Remove-Item Env:\AXIOM_TD_TRANSITION_AUTHORITY_REF -ErrorAction SilentlyContinue

    if ($null -ne $env:AXIOM_TD_TRANSITION_AUTHORITY_REF) {
        throw "FAIL: AXIOM_TD_TRANSITION_AUTHORITY_REF still present at act start; expected UNSET."
    }

    Write-Evidence "AXIOM_DATABASE_URL: built by this pack (sqlite+aiosqlite scheme) for the target file (value not printed)."
    Write-Evidence "AXIOM_ENVIRONMENT=testing, AXIOM_ALLOW_INSECURE_DEV=true, AXIOM_JWT_SECRET_KEY set (value not printed)."
    Write-Evidence "AXIOM_V2_MODE=RESEARCH (plan item 9)."
    Write-Evidence "AXIOM_TD_API_KEY / AXIOM_TD_API_KEY_FILE / AXIOM_TD_CONTRACT_TEST_ENABLED / AXIOM_TD_P2_AUTHORITY_REF: removed from environment."
    Write-Evidence "AXIOM_TD_TRANSITION_AUTHORITY_REF: UNSET (verified; pack-managed; this act never sets it)."

    # -----------------------------------------------------------------
    # SECTION 3 - SOURCE PROVENANCE (FINAL MIGRATION HASH)
    # -----------------------------------------------------------------

    Write-Section "3. SOURCE PROVENANCE (FINAL MIGRATION HASH)"

    $MigrationPath = Join-Path $BackendRoot "alembic\versions\20260829_0042_v2_be3_p2_transition.py"
    if (!(Test-Path $MigrationPath)) { throw "STOP: migration file missing: ${MigrationPath}" }
    $MigrationHash = (Get-FileHash $MigrationPath -Algorithm SHA256).Hash.ToLower()
    Write-Evidence "alembic\versions\20260829_0042_v2_be3_p2_transition.py"
    Write-Evidence "  actual   ${MigrationHash}"
    Write-Evidence "  expected ${FinalMigrationHash}"
    if ($MigrationHash -ne $FinalMigrationHash) {
        throw "STOP: provenance hash mismatch - the migration on disk is not the ITRGA-accepted Revision-2 file. Stopping; report to ITRGA."
    }
    Write-Evidence "PASS: provenance - the migration on disk hashes to the ITRGA-accepted value."

    # -----------------------------------------------------------------
    # BOUNDARY 1 - TARGET IDENTITY (READ-ONLY)
    # -----------------------------------------------------------------

    Write-Section "BOUNDARY 1: TARGET IDENTITY (read-only)"

    $B1File = Get-Item ${TargetDbPath}
    Write-Evidence "Target file: ${TargetDbPath}"
    Write-Evidence "  size       $($B1File.Length) bytes"
    Write-Evidence "  last write $($B1File.LastWriteTime.ToString('yyyy-MM-dd HH:mm:ss zzz'))"
    $B1FileHash = (Get-FileHash ${TargetDbPath} -Algorithm SHA256).Hash.ToLower()
    Write-Evidence "  sha256     ${B1FileHash}"

    [void](Invoke-Py -PyArgs @("scalar", ${TargetDbPath}, "SELECT sqlite_version();") -Label "B1 sqlite version")

    $IntegrityOut = Invoke-Py -PyArgs @("scalar", ${TargetDbPath}, "PRAGMA integrity_check;") -Label "B1 integrity check"
    $IntegrityText = (Norm-Text $IntegrityOut).Trim()
    if ($IntegrityText -ne "ok") {
        throw "FAIL: B1 - integrity_check '${IntegrityText}', expected 'ok'. Stopping; report to ITRGA."
    }
    Write-Evidence "PASS: B1 - integrity_check ok."

    [void](Invoke-Py -PyArgs @("scalar", ${TargetDbPath}, "PRAGMA journal_mode;") -Label "B1 journal mode")

    foreach ($Suffix in @("-wal", "-shm")) {
        $SidePath = ${TargetDbPath} + $Suffix
        if (Test-Path $SidePath) {
            $SideItem = Get-Item $SidePath
            Write-Evidence "Sidecar ${Suffix}: present, $($SideItem.Length) bytes"
        } else {
            Write-Evidence "Sidecar ${Suffix}: absent"
        }
    }

    [void](Invoke-Py -PyArgs @("scalar", ${TargetDbPath}, "SELECT COUNT(*) FROM sqlite_master WHERE type='trigger' AND name LIKE 'v2_%';") -Label "B1 v2 trigger count (informational)")

    $GuardNames = Get-PyScalar -Sql "SELECT name FROM sqlite_master WHERE type='trigger' AND name IN ('v2_md_provider_immutable_update','v2_md_provider_immutable_delete','v2_md_provider_hist_immutable_update','v2_md_provider_hist_immutable_delete') ORDER BY name;" -Label "B1 guard trigger names"
    $ExpectedGuards = "v2_md_provider_hist_immutable_delete`nv2_md_provider_hist_immutable_update`nv2_md_provider_immutable_delete`nv2_md_provider_immutable_update"
    if ($GuardNames -ne $ExpectedGuards) {
        throw "FAIL: B1 - guard trigger names '${GuardNames}'; expected exactly the four recorded guard triggers. Stopping; report to ITRGA."
    }
    Write-Evidence "PASS: B1 - the four guard triggers are present (provider update/delete, history update/delete)."

    # -----------------------------------------------------------------
    # BOUNDARY 2 - BASELINE (MUST BE EXACTLY 20260829_0042 HEAD)
    # -----------------------------------------------------------------

    Write-Section "BOUNDARY 2: BASELINE (alembic current must be 20260829_0042 head)"

    $BaseOut = Invoke-Alembic -AlembicArgs @("current") -Label "baseline current"
    $BaseText = Norm-Text $BaseOut
    if ($BaseText -notlike "*20260829_0042 (head)*") {
        throw "FAIL: B2 - alembic current is '${BaseText}'; expected exactly '20260829_0042 (head)'. Stopping; report to ITRGA."
    }
    Write-Evidence "PASS: B2 - alembic at head 20260829_0042, as the apply act record requires."

    # -----------------------------------------------------------------
    # BOUNDARY 3 - RECOVERY ANCHOR (APPLY ACT BACKUP FILE)
    # -----------------------------------------------------------------

    Write-Section "BOUNDARY 3: RECOVERY ANCHOR (the apply act's backup file)"

    $BackupPath = Join-Path $EvidenceDir ${ExpectedBackupName}
    if (!(Test-Path $BackupPath)) {
        throw "FAIL: B3 - the apply act's backup file is missing: ${BackupPath}. The recovery anchor must be reported to ITRGA; stopping."
    }
    $BackupItem = Get-Item $BackupPath
    Write-Evidence "Backup anchor: ${BackupPath}"
    Write-Evidence "  size       $($BackupItem.Length) bytes"
    $BackupHash = (Get-FileHash $BackupPath -Algorithm SHA256).Hash.ToLower()
    Write-Evidence "  sha256     ${BackupHash}"
    Write-Evidence "  (the apply act record states this file's sha256 as 6db478ee7464a004d1188fa242ce40e2d397abb75ea027792063e74fb8620895; ITRGA cross-checks the two records. The backup was taken at the pre-modification baseline, so its table set is revision-dependent and is NOT queried here.)"

    $AnchorOut = Invoke-Py -PyArgs @("scalar", ${BackupPath}, "PRAGMA integrity_check;") -Label "B3 anchor integrity"
    $AnchorIntText = (Norm-Text $AnchorOut).Trim()
    if ($AnchorIntText -ne "ok") {
        throw "FAIL: B3 - backup anchor integrity_check '${AnchorIntText}', expected 'ok'. Stopping; report to ITRGA."
    }
    Write-Evidence "PASS: B3 - the recovery anchor is present and is a valid SQLite database (integrity ok); its sha256 is recorded for ITRGA's cross-check against the apply act record."

    # -----------------------------------------------------------------
    # BOUNDARY 4 - END STATE: PROVIDER ROW
    # -----------------------------------------------------------------

    Write-Section "BOUNDARY 4: END STATE - PROVIDER ROW"

    [void](Invoke-Py -PyArgs @("scalar", ${TargetDbPath}, "SELECT source_status, entitlement_status, persistence_permitted FROM v2_md_provider WHERE provider_id='twelvedata';") -Label "B4 provider row")
    $EndState = Get-PyScalar -Sql "SELECT source_status, entitlement_status, persistence_permitted FROM v2_md_provider WHERE provider_id='twelvedata';" -Label "B4 end state"
    if ($EndState -ne "contract_tested|verified|0") {
        throw "FAIL: B4 - end state '${EndState}', expected 'contract_tested|verified|0'. Stopping; report to ITRGA."
    }
    Write-Evidence "PASS: B4 - provider row is contract_tested|verified|0 (persistence false; SQLite boolean rendering)."

    # -----------------------------------------------------------------
    # BOUNDARY 5 - END STATE: HISTORY (CONTENT-BASED EXACT, PGF-012)
    # -----------------------------------------------------------------

    Write-Section "BOUNDARY 5: END STATE - HISTORY (exactly 2 rows; exact content; order-independent per PGF-012)"

    [void](Invoke-Py -PyArgs @("scalar", ${TargetDbPath}, "SELECT from_status, to_status, authority_ref, evidence_ref, operator_id FROM v2_md_provider_status_history ORDER BY id;") -Label "B5 history rows (ordered by id; id is a uuid4 - this order is lexicographic, NOT insertion order; informational only)")
    $HistCount = Get-PyScalar -Sql "SELECT COUNT(*) FROM v2_md_provider_status_history;" -Label "B5 history count"
    if ($HistCount -ne "2") {
        throw "FAIL: B5 - history count '${HistCount}', expected 2. Stopping; report to ITRGA."
    }
    $RowOut = Invoke-Py -PyArgs @("verifyrows", ${TargetDbPath}) -Label "B5 history exact-content (content-based; PGF-012)"
    $RowText = (Norm-Text $RowOut).Trim()
    if ($RowText -ne "PASS:history_rows_exact") {
        throw "FAIL: B5 - history exact-content check failed: ${RowText}"
    }
    Write-Evidence "PASS: B5 - history is exactly 2 rows; the genesis row and the transition row each match the approved content exactly (evidence_ref compared in Python via chr(183) for the middle dot; rows matched by content, never by position - PGF-012)."

    # -----------------------------------------------------------------
    # BOUNDARY 6 - END STATE: AUDIT (EXACT START + COMPLETE)
    # -----------------------------------------------------------------

    Write-Section "BOUNDARY 6: END STATE - AUDIT (exactly start + complete; exact details)"

    [void](Invoke-Py -PyArgs @("scalar", ${TargetDbPath}, "SELECT action FROM v2_audit_event WHERE action LIKE 'provider.status_transition%' ORDER BY created_at;") -Label "B6 status-transition audit actions (ordered)")
    $AuditOut = Invoke-Py -PyArgs @("verifyaudit", ${TargetDbPath}) -Label "B6 audit exact-content"
    $AuditText = (Norm-Text $AuditOut).Trim()
    if ($AuditText -ne "PASS:audit_rows_exact") {
        throw "FAIL: B6 - audit exact-content check failed: ${AuditText}"
    }
    Write-Evidence "PASS: B6 - the audit holds exactly the start row and the complete row with the exact details strings from the accepted migration source (details compared in Python via chr(183) for the middle dot)."

    # -----------------------------------------------------------------
    # BOUNDARY 7 - IMMUTABILITY SPOT-CHECKS (EXACT SQLITE MESSAGES)
    # -----------------------------------------------------------------

    Write-Section "BOUNDARY 7: IMMUTABILITY SPOT-CHECKS (exact SQLite guard messages)"

    $ProviderUpdateMessage = "V2 provider registry is immutable in P1; UPDATE prohibited"
    $ProviderDeleteMessage = "V2 provider registry is immutable in P1; DELETE prohibited"
    $HistoryUpdateMessage  = "V2 provider status history is immutable; UPDATE prohibited"
    $HistoryDeleteMessage  = "V2 provider status history is immutable; DELETE prohibited"

    Invoke-ExpectedRefusal -Label "B7 spot-check: provider source_status UPDATE to 'integrated'" -Sql "UPDATE v2_md_provider SET source_status='integrated' WHERE provider_id='twelvedata';" -ExactMessage ${ProviderUpdateMessage}
    Invoke-ExpectedRefusal -Label "B7 spot-check: provider persistence_permitted UPDATE" -Sql "UPDATE v2_md_provider SET persistence_permitted=1 WHERE provider_id='twelvedata';" -ExactMessage ${ProviderUpdateMessage}
    Invoke-ExpectedRefusal -Label "B7 spot-check: provider registry DELETE" -Sql "DELETE FROM v2_md_provider WHERE provider_id='twelvedata';" -ExactMessage ${ProviderDeleteMessage}
    Invoke-ExpectedRefusal -Label "B7 spot-check: history UPDATE" -Sql "UPDATE v2_md_provider_status_history SET to_status='integrated';" -ExactMessage ${HistoryUpdateMessage}
    Invoke-ExpectedRefusal -Label "B7 spot-check: history DELETE" -Sql "DELETE FROM v2_md_provider_status_history;" -ExactMessage ${HistoryDeleteMessage}
    Write-Evidence "PASS: B7 - all five spot-checks refused with the exact SQLite guard messages; registry and history unchanged."

    # -----------------------------------------------------------------
    # BOUNDARY 8 - AUTHORITY VARIABLE (UNSET; NEVER SET BY THIS ACT)
    # -----------------------------------------------------------------

    Write-Section "BOUNDARY 8: authority variable UNSET (recorded final act step)"

    Remove-Item Env:\AXIOM_TD_TRANSITION_AUTHORITY_REF -ErrorAction SilentlyContinue
    if ($null -ne $env:AXIOM_TD_TRANSITION_AUTHORITY_REF) {
        throw "FAIL: AXIOM_TD_TRANSITION_AUTHORITY_REF still present at act end; expected UNSET."
    }
    Write-Evidence "AXIOM_TD_TRANSITION_AUTHORITY_REF = UNSET (verified; this act never set it; recorded final act step)."

    # -----------------------------------------------------------------
    # BOUNDARY 9 - ALEMBIC CHECK AT HEAD (INHERITED V1 DRIFT SET ONLY)
    # -----------------------------------------------------------------

    Write-Section "BOUNDARY 9: alembic check at head (expected: inherited V1 drift set ONLY)"

    Write-Evidence ""
    Write-Evidence "ALEMBIC: alembic check"

    $prev = $ErrorActionPreference
    $ErrorActionPreference = "Continue"
    try {
        $DriftOut  = & $Python -m alembic check 2>&1
        $DriftCode = $LASTEXITCODE
    } finally {
        $ErrorActionPreference = $prev
    }

    Emit-Output $DriftOut

    $DriftText = Norm-Text $DriftOut

    $ExpectedDriftTokens = @(
        "audit_write_failure_records",
        "ix_audit_write_failures_category_action",
        "ix_audit_write_failures_created",
        "ix_advisory_signals_expires_at",
        "ix_advisory_signals_freshness_status",
        "ix_ingestion_runs_symbol_started",
        "ix_model_artifacts_advisory_status",
        "ix_model_artifacts_artifact_hash",
        "ix_model_artifacts_experiment_id"
    )
    foreach ($Token in $ExpectedDriftTokens) {
        if ($DriftText -notlike "*${Token}*") {
            throw "FAIL: B9 - expected inherited V1 drift token missing from alembic check output: ${Token}"
        }
    }
    if ($DriftText -match "v2_md_provider|v2_permission|contract_test") {
        throw "FAIL: B9 - V2/P2/transition drift token detected in alembic check output."
    }
    if ($DriftCode -eq 0) {
        throw "FAIL: B9 - alembic check reported no drift; expected the inherited V1 drift set (non-zero exit)."
    }
    Write-Evidence "PASS: B9 - alembic check at head 20260829_0042 shows the inherited V1 drift set ONLY (all 9 expected tokens present, no V2/P2/transition drift, non-zero exit as expected)."

    # -----------------------------------------------------------------
    # SECTION 10 - FINAL VERIFY VERDICT
    # -----------------------------------------------------------------

    Write-Section "10. FINAL VERIFY VERDICT"
    Write-Evidence "VERIFY VERDICT: PASS - the end state of the proven migration 20260829_0042 is verified IN FORCE on the application's working SQLite database file '${TargetDbPath}' (applied ONCE per the apply act record; this verification act changed nothing in the database)."
    Write-Evidence "Terminal state (BO-V2-BE-3-P2-TRANS-001 section 6): source_status=contract_tested, entitlement_status=verified, persistence_permitted=0 (false; SQLite boolean rendering), history=2 (genesis + transition, exact content), audit exactly start+complete (exact details), guards intact (exact refusal messages), authority variable UNSET, alembic at head 20260829_0042, drift = inherited V1 set only."
    Write-Evidence "Provenance: migration on disk = ${FinalMigrationHash}."

    $FinalFile = Get-Item ${TargetDbPath}
    Write-Evidence "Final target file: ${TargetDbPath}"
    Write-Evidence "  size  $($FinalFile.Length) bytes; last write $($FinalFile.LastWriteTime.ToString('yyyy-MM-dd HH:mm:ss zzz'))"
    $FinalHash = (Get-FileHash ${TargetDbPath} -Algorithm SHA256).Hash.ToLower()
    Write-Evidence "  sha256 ${FinalHash}"
    Write-Evidence "  (this act is read-only: if the sha256 differs from the apply act's post-apply state, the file changed outside the act - report to ITRGA.)"
    foreach ($Suffix in @("-wal", "-shm")) {
        $SidePath = ${TargetDbPath} + $Suffix
        if (Test-Path $SidePath) {
            $SideItem = Get-Item $SidePath
            Write-Evidence "  sidecar ${Suffix}: present, $($SideItem.Length) bytes"
        } else {
            Write-Evidence "  sidecar ${Suffix}: absent"
        }
    }

    Write-Evidence "Transcript: ${Transcript}"
    Write-Evidence "Disposal: this pack created no file other than the transcript; the throwaway helper was removed on exit; the database is unchanged. Restart the application when ready."

} catch {
    Write-Evidence ""
    Write-Evidence "VERIFY VERDICT: FAIL - RUN ABORTED: $($_.Exception.Message)"
    Write-Evidence "Transcript: ${Transcript}"
    Write-Evidence "This act is READ-ONLY: the database state is unchanged by this act; the apply act's state stands as the apply record shows."
    $BackupPathLate = Join-Path $EvidenceDir ${ExpectedBackupName}
    if (Test-Path $BackupPathLate) {
        Write-Evidence "Recovery anchor (apply act backup; unchanged): ${BackupPathLate}"
    }
    Write-Host ""
    Write-Host "VERIFY FAILED. Do not edit anything in the repository and do not re-run without ITRGA instruction."
    Write-Host "Send the transcript file to ITRGA:"
    Write-Host "  ${Transcript}"
    throw
} finally {
    Pop-Location

    Remove-Item Env:\AXIOM_DATABASE_URL -ErrorAction SilentlyContinue
    Remove-Item Env:\AXIOM_JWT_SECRET_KEY -ErrorAction SilentlyContinue
    Remove-Item Env:\AXIOM_ALLOW_INSECURE_DEV -ErrorAction SilentlyContinue
    Remove-Item Env:\AXIOM_ENVIRONMENT -ErrorAction SilentlyContinue
    Remove-Item Env:\AXIOM_V2_MODE -ErrorAction SilentlyContinue
    Remove-Item Env:\AXIOM_TD_TRANSITION_AUTHORITY_REF -ErrorAction SilentlyContinue
    Remove-Variable TargetDbPathUrl -ErrorAction SilentlyContinue

    Remove-Item -Recurse -Force ${HelperDir} -ErrorAction SilentlyContinue

    Write-Host "Environment cleaned (AXIOM_DATABASE_URL, AXIOM_JWT_SECRET_KEY, AXIOM_ALLOW_INSECURE_DEV, AXIOM_ENVIRONMENT, AXIOM_V2_MODE, AXIOM_TD_TRANSITION_AUTHORITY_REF); helper removed."
}
