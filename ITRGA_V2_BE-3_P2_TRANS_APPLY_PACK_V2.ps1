# =====================================================================
# AXIOM V2 BE-3 P2 STATUS TRANSITION - ITRGA SQLITE APPLY ACT EVIDENCE PACK (V2)
# Pack ID: ITRGA-V2-BE-3-P2-TRANS-APPLY-PACK-V2
# Authority:
#   - AXIOM-V2-OD-BE-3-P2-005 (Operator decision - apply act re-scoped
#     to the SQLite working database)
#   - ITRGA-PLAN-V2-BE-3-P2-TRANS-APPLY-002 (boundary table, stop conditions)
#   - ITRGA-ASS-V2-BE-3-P2-TRANS-APPLY-SCOPE-001 (scope assessment, Option A)
#   - BO-V2-BE-3-P2-TRANS-001 section 6 (end state: contract_tested, history 2)
#   - ITRGA-DET-V2-BE-3-P2-TRANS-FINAL-001 (mechanism proven)
#   - Provenance anchor: accepted Revision-2 record (final migration hash
#     af77a63f903a43e2eb7b4426b67de7113791f37918bbfe7f465d8f1bab3cf8d4)
# Pattern: ITRGA-V2-BE-3-P2-TRANS-APPLY-PACK-V1 (defect-corrected
#   structure; PGF-001..007 lessons incorporated by construction).
#
# WHAT THIS PACK DOES:
#   Applies the PROVEN migration 20260829_0042 ONCE to the
#   APPLICATION'S WORKING SQLITE DATABASE FILE (the one the running app
#   uses: backend\.env AXIOM_DATABASE_URL =
#   sqlite+aiosqlite:///./axiom_dev.db) and proves the Build Order
#   section 6 end state on SQLite: contract_tested, verified,
#   persistence false, history 2, guards intact, authority unset,
#   alembic at head with the inherited V1 drift set only.
#
#   SQLite-specific design:
#   - No database server: NO psql, NO password prompt, NO server
#     credential of any kind. All SQL runs through the repo venv
#     python (sqlite3 module) against the file directly.
#   - FILE-LEVEL BACKUP of the working database file (plus any
#     -wal/-shm sidecars) to the operator-evidence directory BEFORE
#     any modification: the complete, credential-free rollback anchor.
#   - Exact-content history comparison runs IN PYTHON via chr(183)
#     for the middle dot: no encoding round-trip in the assertion.
#   - Spot-checks assert the EXACT SQLite guard messages
#     (separate UPDATE / DELETE triggers on SQLite).
#
#   - It does NOT create or delete any database file.
#   - It does NOT run the downgrade/refusal proof (proven on the gate
#     evidence database; running it here would corrupt the end state).
#   - It modifies ONLY the target file (the single apply) and writes
#     the transcript + backup file(s) in the evidence directory + a
#     throwaway helper in the OS temp directory (removed on exit).
#   - NO-OP BRANCH: if the target is already at 20260829_0042 with
#     contract_tested + history 2, the pack verifies that state
#     read-only and exits with verdict ALREADY APPLIED, having
#     changed nothing (no backup created in that branch).
#
# BEFORE RUNNING: STOP THE RUNNING APPLICATION (it holds a live
#   connection to the target database file). Restart it after the
#   pack completes. The target file is the SQLite file named by
#   backend\.env (AXIOM_DATABASE_URL = sqlite+aiosqlite:///./axiom_dev.db,
#   i.e. the file relative to the application's working directory -
#   typically C:\Users\victo\.vscode\AXIOM\axiom\backend\axiom_dev.db).
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
#     managed exclusively by this pack: UNSET (verified) -> SET (exact
#     string, single apply step) -> UNSET (recorded final act step).
#
# Save this file to the AXIOM repository root:
#   C:\Users\victo\.vscode\AXIOM\axiom\ITRGA_V2_BE-3_P2_TRANS_APPLY_PACK_V2.ps1
#
# Run from the AXIOM repository root, as a file (exactly one command):
#   powershell -NoProfile -ExecutionPolicy Bypass -File ".\ITRGA_V2_BE-3_P2_TRANS_APPLY_PACK_V2.ps1"
#
# Output (submit this one file to ITRGA):
#   C:\Users\victo\.vscode\AXIOM\axiom\operator-evidence\BE-3-P2-transition\BE-3-P2-TRANS-APPLY-EVIDENCE-V2.txt
# =====================================================================

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

# ---------------------------------------------------------------------
# 0. ENCODING, LOCAL PATHS AND TOOL CHECKS
# ---------------------------------------------------------------------

# Force UTF-8 for the console / python / transcript round trip so the
# middle dot (U+00B7) inside the EVIDENCE_REF value round-trips
# un-mangled in the informational row printout. The authoritative
# exact-content check runs in Python via chr(183) and does not depend
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
$Transcript   = Join-Path $EvidenceDir "BE-3-P2-TRANS-APPLY-EVIDENCE-V2.txt"

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
    # Appends output to the transcript and shows it on the console
    # without polluting the caller's pipeline.
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

$AuthorityString    = "BO-V2-BE-3-P2-TRANS-001"
$FinalMigrationHash = "af77a63f903a43e2eb7b4426b67de7113791f37918bbfe7f465d8f1bab3cf8d4"

# Working-database file name from backend\.env (refused if mismatched).
$ExpectedLeafName = "axiom_dev.db"

# Populated by BOUNDARY 3; $null until then.
$MainBackupPath = $null
$MainBackupHash = $null

# ---------------------------------------------------------------------
# 0B. OPERATOR INPUT (ABSOLUTE PATH OF THE WORKING DATABASE FILE)
# ---------------------------------------------------------------------

Write-Host ""
Write-Host "STOP THE RUNNING APPLICATION BEFORE CONTINUING (it holds a live"
Write-Host "connection to the target database file). Restart it after this"
Write-Host "pack finishes."
Write-Host ""
Write-Host "This pack applies the proven transition migration 20260829_0042 ONCE to the"
Write-Host "application's SQLite WORKING DATABASE FILE and then proves the end state."
Write-Host ""
Write-Host "This pack prompts for NO credential of any kind (no password, no API key)."
Write-Host ""

$TargetDbPath = (Read-Host -Prompt "Absolute path to the application's working SQLite database file (for example C:\Users\victo\.vscode\AXIOM\axiom\backend\axiom_dev.db)").Trim()
if ([string]::IsNullOrEmpty($TargetDbPath)) {
    throw "No database file path entered. Aborting before any database modification."
}
if (!(Test-Path ${TargetDbPath})) {
    throw "STOP: file not found: ${TargetDbPath}. Aborting before any database modification."
}
$TargetItem = Get-Item ${TargetDbPath}
if ($TargetItem.PSIsContainer) {
    throw "STOP: path is a directory, not a file: ${TargetDbPath}. Aborting before any database modification."
}
if ($TargetItem.Length -eq 0) {
    throw "STOP: file is empty (0 bytes): ${TargetDbPath}. Aborting before any database modification."
}
$TargetDbPath = $TargetItem.FullName
$LeafName = Split-Path ${TargetDbPath} -Leaf
if ($LeafName.ToLower() -ne $ExpectedLeafName) {
    throw "STOP: file leaf name '${LeafName}' does not match the working database file name '${ExpectedLeafName}' from backend\.env. Aborting before any database modification."
}
$EvidenceRootFull = (Resolve-Path $EvidenceRoot).Path
if (${TargetDbPath.ToLower().StartsWith($EvidenceRootFull.ToLower())}) {
    throw "STOP: target file is inside the operator-evidence directory. Aborting before any database modification."
}

# ---------------------------------------------------------------------
# 0C. PYTHON HELPER (written to the OS temp directory, removed on exit)
# ---------------------------------------------------------------------

$HelperDir  = Join-Path $env:TEMP "axiom_itrga_apply_v2"
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

    if cmd in ("scalar", "integrity", "journalmode", "hashrow"):
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
            elif cmd == "hashrow":
                rows = con.execute(
                    "SELECT from_status, to_status, authority_ref, evidence_ref, operator_id "
                    "FROM v2_md_provider_status_history ORDER BY id"
                ).fetchall()
                if len(rows) != 2:
                    print("FAIL:history_count=" + str(len(rows)))
                    return
                row1 = rows[0]
                row2 = rows[1]
                exp2 = (
                    "architecture_candidate",
                    "contract_tested",
                    "BO-V2-BE-3-P2-TRANS-001",
                    "ITRGA-DET-V2-BE-3-P2-FINAL-001 " + chr(183)
                    + " run a246607c-f0c5-42e9-8f3b-a1e1bd75fa83",
                    None,
                )
                problems = []
                if not (row1[0] is None
                        and row1[1] == "architecture_candidate"
                        and row1[2] == "BO-V2-BE-3-P1-001"
                        and row1[4] is None):
                    problems.append("row1=" + repr(row1))
                if tuple(row2) != exp2:
                    problems.append("row2=" + repr(row2))
                if problems:
                    print("FAIL:" + " ".join(problems))
                else:
                    print("PASS:history_rows_exact")
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

function Assert-AlembicCurrent {
    # Runs `alembic current` and requires the expected revision token.
    param(
        [Parameter(Mandatory = $true)][string]$ExpectedRev,
        [string]$Label
    )

    $Out = Invoke-Alembic -AlembicArgs @("current") -Label $Label
    $Text = Norm-Text $Out
    if ($Text -notlike "*${ExpectedRev}*") {
        throw "FAIL: alembic current does not show expected revision ${ExpectedRev}: ${Label}"
    }
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
Write-Evidence "Pack: ITRGA-V2-BE-3-P2-TRANS-APPLY-PACK-V2"
Write-Evidence "Operator decision: AXIOM-V2-OD-BE-3-P2-005 (apply act re-scoped to the SQLite working database)"
Write-Evidence "Plan: ITRGA-PLAN-V2-BE-3-P2-TRANS-APPLY-002"
Write-Evidence "Scope assessment: ITRGA-ASS-V2-BE-3-P2-TRANS-APPLY-SCOPE-001 (Option A)"
Write-Evidence "Build order: BO-V2-BE-3-P2-TRANS-001 (section 6 end state)"
Write-Evidence "Final migration hash (apply target): ${FinalMigrationHash}"
Write-Evidence "Started: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss zzz')"
Write-Evidence "Repo root: ${RepoRoot}"
Write-Evidence "Target file (APPLICATION'S WORKING DATABASE - named by the Operator): ${TargetDbPath}"
Write-Evidence "SQL engine: SQLite (in-process, via the repo venv python sqlite3 module; no database server)"
Write-Evidence "Python (repo venv): ${Python}"
Write-Evidence "Server credentials used: NONE (no database server; no password prompt)"
Write-Evidence "Provider credentials used: NONE"
Write-Evidence "This pack creates no database file, runs no downgrade, and performs no refusal proof."

Push-Location $BackendRoot

try {

    # -----------------------------------------------------------------
    # SECTION 1 - HELPER SELF-TEST (READ-ONLY; BEFORE ANY MODIFICATION)
    # -----------------------------------------------------------------

    Write-Section "1. HELPER SELF-TEST"

    [void](Invoke-Py -PyArgs @("selftest", ${TargetDbPath}) -Label "helper self-test")

    # -----------------------------------------------------------------
    # SECTION 2 - RUN ENVIRONMENT (NO PROVIDER CREDENTIALS)
    # -----------------------------------------------------------------

    Write-Section "2. RUN ENVIRONMENT (NO PROVIDER CREDENTIALS)"

    $TargetDbPathUrl = ${TargetDbPath.Replace("\", "/")}
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
        throw "FAIL: AXIOM_TD_TRANSITION_AUTHORITY_REF still present before the apply step; expected UNSET."
    }

    Write-Evidence "AXIOM_DATABASE_URL: built by this pack (sqlite+aiosqlite scheme) for the target file (value not printed)."
    Write-Evidence "AXIOM_ENVIRONMENT=testing, AXIOM_ALLOW_INSECURE_DEV=true, AXIOM_JWT_SECRET_KEY set (value not printed)."
    Write-Evidence "AXIOM_V2_MODE=RESEARCH (plan item 9)."
    Write-Evidence "AXIOM_TD_API_KEY / AXIOM_TD_API_KEY_FILE / AXIOM_TD_CONTRACT_TEST_ENABLED / AXIOM_TD_P2_AUTHORITY_REF: removed from environment."
    Write-Evidence "AXIOM_TD_TRANSITION_AUTHORITY_REF: UNSET (verified; pack-managed)."

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
        throw "STOP: provenance hash mismatch - the migration on disk is not the ITRGA-accepted Revision-2 file. The apply must not proceed; report to ITRGA."
    }
    Write-Evidence "PASS: provenance - the migration on disk hashes to the ITRGA-accepted value."

    # -----------------------------------------------------------------
    # BOUNDARY 1 - TARGET IDENTITY (READ-ONLY)
    # -----------------------------------------------------------------

    Write-Section "BOUNDARY 1: TARGET IDENTITY (read-only)"

    $B1File = Get-Item ${TargetDbPath}
    Write-Evidence "Target file: ${TargetDbPath}"
    Write-Evidence "  size       ${B1File.Length} bytes"
    Write-Evidence "  last write ${B1File.LastWriteTime.ToString('yyyy-MM-dd HH:mm:ss zzz')}"
    $B1FileHash = (Get-FileHash ${TargetDbPath} -Algorithm SHA256).Hash.ToLower()
    Write-Evidence "  sha256     ${B1FileHash}"

    [void](Invoke-Py -PyArgs @("scalar", ${TargetDbPath}, "SELECT version();") -Label "B1 sqlite version")

    $IntegrityOut = Invoke-Py -PyArgs @("scalar", ${TargetDbPath}, "PRAGMA integrity_check;") -Label "B1 integrity check"
    $IntegrityText = (Norm-Text $IntegrityOut).Trim()
    if ($IntegrityText -ne "ok") {
        throw "FAIL: B1 - integrity_check '${IntegrityText}', expected 'ok'. Stopping before any modification; report to ITRGA."
    }
    Write-Evidence "PASS: B1 - integrity_check ok."

    [void](Invoke-Py -PyArgs @("scalar", ${TargetDbPath}, "PRAGMA journal_mode;") -Label "B1 journal mode")

    foreach ($Suffix in @("-wal", "-shm")) {
        $SidePath = ${TargetDbPath} + $Suffix
        if (Test-Path $SidePath) {
            $SideItem = Get-Item $SidePath
            Write-Evidence "Sidecar ${Suffix}: present, ${SideItem.Length} bytes"
        } else {
            Write-Evidence "Sidecar ${Suffix}: absent"
        }
    }

    [void](Invoke-Py -PyArgs @("scalar", ${TargetDbPath}, "SELECT COUNT(*) FROM sqlite_master WHERE type='trigger' AND name LIKE 'v2_%';") -Label "B1 v2 trigger count (informational)")

    # -----------------------------------------------------------------
    # BOUNDARY 2 - BASELINE STATE (alembic current) + NO-OP BRANCH
    # -----------------------------------------------------------------

    Write-Section "BOUNDARY 2: BASELINE STATE (alembic current)"

    $BaseOut = Invoke-Alembic -AlembicArgs @("current") -Label "baseline current"
    $BaseText = Norm-Text $BaseOut

    if ($BaseText -like "*20260829_0042*") {
        Write-Evidence "NOTE: target is already at 20260829_0042 - no-op branch: verifying whether the transition already exists (read-only; nothing changed)."
        $AlreadyState = Get-PyScalar -Sql "SELECT source_status, entitlement_status, persistence_permitted FROM v2_md_provider WHERE provider_id='twelvedata';" -Label "no-op state"
        $AlreadyHist = Get-PyScalar -Sql "SELECT COUNT(*) FROM v2_md_provider_status_history;" -Label "no-op history count"
        if ($AlreadyState -eq "contract_tested|verified|0" -and $AlreadyHist -eq "2") {
            Write-Evidence ""
            Write-Evidence "APPLY VERDICT: ALREADY APPLIED - the transition already exists on this database (contract_tested | verified | persistence_permitted=0 (false), history 2)."
            Write-Evidence "Nothing was applied by this pack; no backup was created. The OD-005 objective is satisfied by the existing state."
            return
        }
        throw "FAIL: target is at 20260829_0042 but its state ('${AlreadyState}', history ${AlreadyHist}) does not match an applied transition. Stopping; report to ITRGA."
    }

    # -----------------------------------------------------------------
    # BOUNDARY 3 - FILE-LEVEL BACKUP (FIRST SIDE EFFECT)
    # -----------------------------------------------------------------

    Write-Section "BOUNDARY 3: FILE-LEVEL BACKUP (first side effect; target: the evidence directory)"

    $BackupStamp = Get-Date -Format "yyyyMMddHHmmss"
    $MainBackupPath = Join-Path $EvidenceDir (${LeafName} + ".pre-0042-" + ${BackupStamp} + ".bak")
    Copy-Item ${TargetDbPath} ${MainBackupPath} -Force
    $MainBackupHash = (Get-FileHash ${MainBackupPath} -Algorithm SHA256).Hash.ToLower()
    if ($MainBackupHash -ne $B1FileHash) {
        throw "FAIL: B3 - backup hash differs from the original file hash. Aborting before any database modification; report to ITRGA."
    }
    Write-Evidence "Backup created: ${MainBackupPath}"
    Write-Evidence "  original sha256 ${B1FileHash}"
    Write-Evidence "  backup   sha256 ${MainBackupHash} (verified equal)"

    foreach ($Suffix in @("-wal", "-shm")) {
        $SidePath = ${TargetDbPath} + $Suffix
        if (Test-Path $SidePath) {
            $SideBackupPath = Join-Path $EvidenceDir (${LeafName} + $Suffix + ".pre-0042-" + ${BackupStamp} + ".bak")
            Copy-Item $SidePath ${SideBackupPath} -Force
            $SideBackupHash = (Get-FileHash ${SideBackupPath} -Algorithm SHA256).Hash.ToLower()
            $SideOrigHash   = (Get-FileHash $SidePath -Algorithm SHA256).Hash.ToLower()
            if ($SideBackupHash -ne $SideOrigHash) {
                throw "FAIL: B3 - sidecar backup hash differs from the original sidecar hash. Aborting before any database modification; report to ITRGA."
            }
            Write-Evidence "Sidecar backup created: ${SideBackupPath} (hash verified equal)"
        }
    }

    # -----------------------------------------------------------------
    # BOUNDARY 4 - ESTABLISH CHAIN TO 20260825_0041
    # -----------------------------------------------------------------

    Write-Section "BOUNDARY 4: ESTABLISH CHAIN TO 20260825_0041 (each upgrade is a no-op if already at or past it)"

    [void](Invoke-Alembic -AlembicArgs @("upgrade", "20260717_0037") -Label "chain 0037")
    [void](Invoke-Alembic -AlembicArgs @("upgrade", "20260823_0038") -Label "chain 0038")
    [void](Invoke-Alembic -AlembicArgs @("upgrade", "20260824_0039") -Label "chain 0039")
    [void](Invoke-Alembic -AlembicArgs @("upgrade", "20260824_0040") -Label "chain 0040")
    [void](Invoke-Alembic -AlembicArgs @("upgrade", "20260825_0041") -Label "chain 0041")
    Assert-AlembicCurrent -ExpectedRev "20260825_0041" -Label "B4 current after chain"

    # -----------------------------------------------------------------
    # BOUNDARY 5 - PRE-STATE
    # -----------------------------------------------------------------

    Write-Section "BOUNDARY 5: PRE-STATE"

    [void](Invoke-Py -PyArgs @("scalar", ${TargetDbPath}, "SELECT entitlement_status, source_status, persistence_permitted FROM v2_md_provider WHERE provider_id='twelvedata';") -Label "B5 pre-state provider row")
    $PreState = Get-PyScalar -Sql "SELECT entitlement_status, source_status, persistence_permitted FROM v2_md_provider WHERE provider_id='twelvedata';" -Label "B5 pre-state"
    if ($PreState -ne "verified|architecture_candidate|0") {
        throw "FAIL: B5 - pre-state '${PreState}', expected 'verified|architecture_candidate|0'. Stopping before the apply step; report to ITRGA."
    }
    $PreHist = Get-PyScalar -Sql "SELECT COUNT(*) FROM v2_md_provider_status_history;" -Label "B5 history count"
    if ($PreHist -ne "1") {
        throw "FAIL: B5 - pre-state history count '${PreHist}', expected 1 (genesis). Stopping before the apply step; report to ITRGA."
    }
    $PreAudit = Get-PyScalar -Sql "SELECT COUNT(*) FROM v2_audit_event;" -Label "B5 audit count"
    if ($PreAudit -ne "0") {
        throw "FAIL: B5 - pre-state audit count '${PreAudit}', expected 0 (clean registry; any prior row - including a prior 0042 refusal - is a deviation). Stopping before the apply step; report to ITRGA."
    }
    Write-Evidence "PASS: B5 - pre-state verified|architecture_candidate|0 (SQLite boolean rendering); history count 1; audit count 0."

    # -----------------------------------------------------------------
    # BOUNDARY 6 - THE APPLY (authority SET to the exact BO string)
    # -----------------------------------------------------------------

    Write-Section "BOUNDARY 6 [var SET = ${AuthorityString}]: alembic upgrade 20260829_0042"

    $env:AXIOM_TD_TRANSITION_AUTHORITY_REF = ${AuthorityString}
    if ($env:AXIOM_TD_TRANSITION_AUTHORITY_REF -ne ${AuthorityString}) {
        throw "FAIL: authority variable did not take the exact BO string."
    }
    Write-Evidence "AXIOM_TD_TRANSITION_AUTHORITY_REF = SET to exact string ${AuthorityString} (plan step 6)."

    [void](Invoke-Alembic -AlembicArgs @("upgrade", "20260829_0042") -Label "the apply")
    Assert-AlembicCurrent -ExpectedRev "20260829_0042" -Label "B6 current (head)"

    # -----------------------------------------------------------------
    # BOUNDARY 7 - POST-STATE (Build Order section 6 end state)
    # -----------------------------------------------------------------

    Write-Section "BOUNDARY 7: POST-STATE (end state)"

    [void](Invoke-Py -PyArgs @("scalar", ${TargetDbPath}, "SELECT source_status, entitlement_status, persistence_permitted FROM v2_md_provider WHERE provider_id='twelvedata';") -Label "B7 post-state provider row")
    $PostState = Get-PyScalar -Sql "SELECT source_status, entitlement_status, persistence_permitted FROM v2_md_provider WHERE provider_id='twelvedata';" -Label "B7 post-state"
    if ($PostState -ne "contract_tested|verified|0") {
        throw "FAIL: B7 - post-state '${PostState}', expected 'contract_tested|verified|0'."
    }

    [void](Invoke-Py -PyArgs @("scalar", ${TargetDbPath}, "SELECT from_status, to_status, authority_ref, evidence_ref, operator_id FROM v2_md_provider_status_history ORDER BY id;") -Label "B7 history rows (ordered by id)")
    $PostHistCount = Get-PyScalar -Sql "SELECT COUNT(*) FROM v2_md_provider_status_history;" -Label "B7 history count"
    if ($PostHistCount -ne "2") {
        throw "FAIL: B7 - history count '${PostHistCount}', expected 2."
    }
    $RowOut = Invoke-Py -PyArgs @("hashrow", ${TargetDbPath}) -Label "B7 history exact-content"
    $RowText = (Norm-Text $RowOut).Trim()
    if ($RowText -ne "PASS:history_rows_exact") {
        throw "FAIL: B7 - history exact-content check failed: ${RowText}"
    }
    Write-Evidence "PASS: B7 - history is exactly 2 rows; genesis + transition rows match the approved content (evidence_ref compared in Python via chr(183) for the middle dot)."

    [void](Invoke-Py -PyArgs @("scalar", ${TargetDbPath}, "SELECT action FROM v2_audit_event WHERE action LIKE 'provider.status_transition%' ORDER BY created_at;") -Label "B7 status-transition audit actions (ordered)")
    $PostAudit = Get-PyScalar -Sql "SELECT action FROM v2_audit_event WHERE action LIKE 'provider.status_transition%' ORDER BY created_at;" -Label "B7 audit sequence"
    if ($PostAudit -ne "provider.status_transition.start`nprovider.status_transition.complete") {
        throw "FAIL: B7 - audit action sequence '${PostAudit}', expected start then complete."
    }
    Write-Evidence "PASS: B7 - audit sequence is exactly start, complete."

    # -----------------------------------------------------------------
    # BOUNDARY 8 - IMMUTABILITY SPOT-CHECKS (EXACT SQLITE MESSAGES)
    # -----------------------------------------------------------------

    Write-Section "BOUNDARY 8: IMMUTABILITY SPOT-CHECKS (exact SQLite guard messages)"

    $ProviderUpdateMessage = "V2 provider registry is immutable in P1; UPDATE prohibited"
    $ProviderDeleteMessage = "V2 provider registry is immutable in P1; DELETE prohibited"
    $HistoryUpdateMessage  = "V2 provider status history is immutable; UPDATE prohibited"
    $HistoryDeleteMessage  = "V2 provider status history is immutable; DELETE prohibited"

    Invoke-ExpectedRefusal -Label "B8 spot-check: provider source_status UPDATE to 'integrated'" -Sql "UPDATE v2_md_provider SET source_status='integrated' WHERE provider_id='twelvedata';" -ExactMessage ${ProviderUpdateMessage}
    Invoke-ExpectedRefusal -Label "B8 spot-check: provider persistence_permitted UPDATE" -Sql "UPDATE v2_md_provider SET persistence_permitted=1 WHERE provider_id='twelvedata';" -ExactMessage ${ProviderUpdateMessage}
    Invoke-ExpectedRefusal -Label "B8 spot-check: provider registry DELETE" -Sql "DELETE FROM v2_md_provider WHERE provider_id='twelvedata';" -ExactMessage ${ProviderDeleteMessage}
    Invoke-ExpectedRefusal -Label "B8 spot-check: history UPDATE" -Sql "UPDATE v2_md_provider_status_history SET to_status='integrated';" -ExactMessage ${HistoryUpdateMessage}
    Invoke-ExpectedRefusal -Label "B8 spot-check: history DELETE" -Sql "DELETE FROM v2_md_provider_status_history;" -ExactMessage ${HistoryDeleteMessage}
    Write-Evidence "PASS: B8 - all five spot-checks refused with the exact SQLite guard messages; registry and history unchanged."

    # -----------------------------------------------------------------
    # BOUNDARY 9 - AUTHORITY VARIABLE UNSET (RECORDED FINAL ACT STEP)
    # -----------------------------------------------------------------

    Write-Section "BOUNDARY 9 [UNSET]: authority variable unset (recorded final act step)"

    Remove-Item Env:\AXIOM_TD_TRANSITION_AUTHORITY_REF -ErrorAction SilentlyContinue
    if ($null -ne $env:AXIOM_TD_TRANSITION_AUTHORITY_REF) {
        throw "FAIL: AXIOM_TD_TRANSITION_AUTHORITY_REF still present after the UNSET step."
    }
    Write-Evidence "AXIOM_TD_TRANSITION_AUTHORITY_REF = UNSET (verified; recorded final act step)."

    # -----------------------------------------------------------------
    # BOUNDARY 10 - ALEMBIC CHECK AT HEAD (INHERITED V1 DRIFT SET ONLY)
    # -----------------------------------------------------------------

    Write-Section "BOUNDARY 10: alembic check at head (expected: inherited V1 drift set ONLY)"

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
            throw "FAIL: B10 - expected inherited V1 drift token missing from alembic check output: ${Token}"
        }
    }
    if ($DriftText -match "v2_md_provider|v2_permission|contract_test") {
        throw "FAIL: B10 - V2/P2/transition drift token detected in alembic check output."
    }
    if ($DriftCode -eq 0) {
        throw "FAIL: B10 - alembic check reported no drift; expected the inherited V1 drift set (non-zero exit)."
    }
    Write-Evidence "PASS: B10 - alembic check at head 20260829_0042 shows the inherited V1 drift set ONLY (all 9 expected tokens present, no V2/P2/transition drift, non-zero exit as expected)."

    # -----------------------------------------------------------------
    # SECTION 11 - FINAL APPLY VERDICT
    # -----------------------------------------------------------------

    Write-Section "11. FINAL APPLY VERDICT"
    Write-Evidence "APPLY VERDICT: PASS - the proven migration 20260829_0042 was applied ONCE to the application's working SQLite database file '${TargetDbPath}'."
    Write-Evidence "Terminal state (BO-V2-BE-3-P2-TRANS-001 section 6): source_status=contract_tested, entitlement_status=verified, persistence_permitted=0 (false; SQLite boolean rendering), history=2 (genesis + transition), guards intact, authority variable UNSET, alembic at head 20260829_0042."
    Write-Evidence "Provenance: migration on disk = ${FinalMigrationHash}."

    $FinalFile = Get-Item ${TargetDbPath}
    Write-Evidence "Final target file: ${TargetDbPath}"
    Write-Evidence "  size  ${FinalFile.Length} bytes; last write ${FinalFile.LastWriteTime.ToString('yyyy-MM-dd HH:mm:ss zzz')}"
    $FinalHash = (Get-FileHash ${TargetDbPath} -Algorithm SHA256).Hash.ToLower()
    Write-Evidence "  sha256 ${FinalHash}"
    foreach ($Suffix in @("-wal", "-shm")) {
        $SidePath = ${TargetDbPath} + $Suffix
        if (Test-Path $SidePath) {
            $SideItem = Get-Item $SidePath
            Write-Evidence "  sidecar ${Suffix}: present, ${SideItem.Length} bytes"
        } else {
            Write-Evidence "  sidecar ${Suffix}: absent"
        }
    }

    if ($null -ne ${MainBackupPath} -and (Test-Path ${MainBackupPath})) {
        $BackupFinalHash = (Get-FileHash ${MainBackupPath} -Algorithm SHA256).Hash.ToLower()
        if ($BackupFinalHash -ne ${MainBackupHash}) {
            throw "FAIL: 11 - the backup file changed after creation. Stopping; report to ITRGA."
        }
        Write-Evidence "Backup file unchanged since creation: ${MainBackupPath} (sha256 ${BackupFinalHash})"
    }

    Write-Evidence "Transcript: ${Transcript}"
    Write-Evidence "Disposal: this pack created no database file; it modified only the target file (the single apply) and wrote the transcript plus the backup file(s). Restart the application when ready."

} catch {
    Write-Evidence ""
    Write-Evidence "APPLY VERDICT: FAIL - RUN ABORTED: $($_.Exception.Message)"
    Write-Evidence "Transcript: ${Transcript}"
    if ($null -ne ${MainBackupPath} -and (Test-Path ${MainBackupPath})) {
        Write-Evidence "Backup (unchanged anchor for any ITRGA-directed recovery): ${MainBackupPath}"
    }
    Write-Host ""
    Write-Host "APPLY FAILED. Do not edit anything in the repository and do not re-run without ITRGA instruction."
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
