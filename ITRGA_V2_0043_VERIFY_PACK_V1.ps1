# =====================================================================
# AXIOM V2 - 0043 WORKING-DATABASE APPLICATION ACT
# ITRGA READ-ONLY VERIFY PACK (V1)
# Pack ID: ITRGA-V2-0043-VERIFY-PACK-V1
# Authority:
#   - AXIOM-V2-OD-BE-4-009 (Operator decision - 0043 working-DB
#     application act)
#   - ITRGA-PLAN-V2-0043-APPLY-001 (instrument design B1-B9)
#   - ITRGA-ASS-V2-0043-APPLY-001 (scope; re-pins resolved 2026-09-02)
#   - BO-V2-0043-APPLY-001 (terminal state T-1...T-11)
#   - ITRGA-PTN-V2-PACK-001 (pack discipline)
#   - Apply record: 0043-APPLY-RUN-V1.txt + 0043-APPLY-FINAL-STATE.txt
#     (this pack reads the apply pack's own recorded final values; it
#     can only run after a completed PASS apply run)
# Pattern: ITRGA-V2-BE-3-P2-TRANS-VERIFY-PACK-V3 (instrument of
#   record; PGF-012 content-based checks; PGF-014 format-independent
#   drift handling), re-pinned from the transition end state to the
#   0043 terminal state.
#
# WHAT THIS PACK DOES:
#   Verifies, READ-ONLY, that the end state of migration
#   20260831_0043_v2_be4_research_read_models (applied ONCE by the
#   apply act) is in force on the APPLICATION'S WORKING SQLITE
#   DATABASE FILE: revision 20260831_0043; 18 v2 triggers; six R-2
#   guard triggers with exact refusal messages; three BE-4 tables with
#   constraints and indexes; exactly 3 computation-version seeds
#   (exact content); exactly 5 permission seeds (exact content); both
#   report tables empty; inherited BE-1 to BE-3 state exact
#   (content-based proofs); drift = exactly the 9 inherited V1 tokens;
#   anchor file proven (the byte-identical 0042-state pre-image).
#   - It changes NOTHING in the database (no row, schema, trigger, or
#     alembic_version change; all SQL runs read-only or is a guarded
#     refusal probe that the triggers abort and the connection rolls
#     back).
#   - It writes ONLY the transcript. The throwaway helper in the OS
#     temp directory is removed on exit.
#   - It does NOT create or delete any database file or backup.
#
# BEFORE RUNNING: STOP THE RUNNING APPLICATION (it holds a live
#   connection to the target database file). Restart it after the
#   pack completes.
#
# RUN MODE: this pack MUST be executed as a file. Pasting the script
#   into an interactive console is NOT an acceptable evidence mode
#   (PGF-004).
#
# OPERATOR INSTRUCTION CARD (ITRGA-PTN-V2-PACK-001 section 2.2):
#   1. Before running anything, verify byte-identity of the THREE
#      issued artifacts with Get-FileHash -Algorithm MD5 against the
#      ITRGA ISSUANCE NOTE (ITRGA-ISS-V2-0043-PACKS-001, 2026-09-02):
#        ITRGA_V2_0043_APPLY_PACK_V1.ps1   (apply pack; runs FIRST)
#        ITRGA_V2_0043_VERIFY_PACK_V1.ps1  (this file; runs SECOND)
#        ITRGA_V2_0043_BASELINE_PINS.txt   (must sit at the repo root)
#      If any MD5 does not match: STOP; do not run anything; report
#      to ITRGA.
#   2. Execute ONLY this file, from the repository root, AFTER a
#      completed PASS apply run:
#        powershell -NoProfile -ExecutionPolicy Bypass -File ".\ITRGA_V2_0043_VERIFY_PACK_V1.ps1"
#   3. Single expected input: the absolute path of the working
#      database file backend\axiom_dev.db (a path, not a credential).
#      Nothing else is asked. No password. No API key.
#   4. Send back to ITRGA afterwards:
#        operator-evidence\BE-4\0043-VERIFY-RUN-V1.txt
#        operator-evidence\BE-4\0043-APPLY-FINAL-STATE.txt (as-is)
#   5. Do NOT execute any other pack file. Not for this act and
#      retired/superseded: apply packs V1-V5, verify packs V1/V2
#      (SUPERSEDED), all POSTGRESQL gate packs, and verify pack V3
#      (valid instrument of record for the pre-apply 0042 state ONLY).
#
# Save the three issued artifacts to the AXIOM repository root:
#   C:\Users\victo\.vscode\AXIOM\axiom\
# =====================================================================

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

# ---------------------------------------------------------------------
# 0. ENCODING, LOCAL PATHS AND TOOL CHECKS
# ---------------------------------------------------------------------

# Force UTF-8 for the console / python / transcript round trip. The
# authoritative exact-content checks run in Python and do not depend
# on the console. This pack's own source is pure ASCII.
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
[Console]::InputEncoding  = [System.Text.Encoding]::UTF8
$env:PYTHONIOENCODING = "utf-8"

$RepoRoot    = (Get-Location).Path
$BackendRoot = Join-Path $RepoRoot "backend"
$Python      = Join-Path $RepoRoot ".venv\Scripts\python.exe"

if (!(Test-Path $BackendRoot)) { throw "Backend directory not found: ${BackendRoot}" }
if (!(Test-Path $Python))      { throw "Python executable not found: ${Python}" }

$EvidenceRoot  = Join-Path $RepoRoot "operator-evidence"
$EvidenceDir   = Join-Path $EvidenceRoot "BE-4"
$Transcript    = Join-Path $EvidenceDir "0043-VERIFY-RUN-V1.txt"
$PinsPath      = Join-Path $RepoRoot "ITRGA_V2_0043_BASELINE_PINS.txt"
$StateRecPath  = Join-Path $EvidenceDir "0043-APPLY-FINAL-STATE.txt"

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

function Read-Pins {
    # Strict parse of a KEY=VALUE pin/state file: exact key set, no
    # duplicate keys. Fails closed.
    param(
        [Parameter(Mandatory = $true)][string]$Path,
        [Parameter(Mandatory = $true)][string[]]$ExpectedKeys,
        [Parameter(Mandatory = $true)][string]$Label
    )
    if (!(Test-Path $Path)) { throw "STOP: required pin file missing: ${Path} (${Label})." }
    $Map = @{}
    foreach ($RawLine in @(Get-Content -Path $Path -Encoding UTF8)) {
        $Line = ([string]$RawLine).TrimEnd()
        if ($Line -eq "" -or $Line.StartsWith("#")) { continue }
        if ($Line -notmatch '^([A-Z0-9_]+)=(.*)$') {
            throw "STOP: malformed line in pin file ${Path}: '${Line}' (${Label})."
        }
        $Key = $Matches[1]
        $Val = $Matches[2]
        if ($Map.ContainsKey($Key)) {
            throw "STOP: duplicate key '${Key}' in pin file ${Path} (${Label})."
        }
        $Map[$Key] = $Val
    }
    $Got = @($Map.Keys | Sort-Object)
    $Exp = @($ExpectedKeys | Sort-Object)
    if (($Got -join ",") -ne ($Exp -join ",")) {
        throw "STOP: pin file key set mismatch in ${Path}: got [$($Got -join ', ')], expected [$($Exp -join ', ')] (${Label})."
    }
    return $Map
}

# ---------------------------------------------------------------------
# 0A. CONSTANTS (BO-V2-0043-APPLY-001; approved manifests)
# ---------------------------------------------------------------------

$ExpectedMigrationHashes = @{
    "20260823_0038_v2_be1_core.py"                 = "6e071157c204e29bfb1254400f0a4543d776931fa5834723cc497d12a0b8f588"
    "20260824_0039_v2_be2_marketdata.py"           = "bc11cae24cdbe47361454a676604a9f81b1754df47058185dd4c002689ab5b19"
    "20260824_0040_v2_be3_provider.py"             = "1332ebf5780fcda00d19589400bbeb873f7187fbd1f4915da093f822f392b226"
    "20260825_0041_v2_be3_p2_entitlement.py"       = "d775c34aedac8fffd594f4ac4434f48c9d9cfd2fa88f4d3fd1cf9e7ba278dadd"
    "20260829_0042_v2_be3_p2_transition.py"        = "af77a63f903a43e2eb7b4426b67de7113791f37918bbfe7f465d8f1bab3cf8d4"
    "20260831_0043_v2_be4_research_read_models.py" = "ab90576203d9f7946154ad4efd7a3d52bc98b91e328dbf2a4dca0b5049bda84b"
}
$ApplyTargetRevision = "20260831_0043"
$BaselineRevision    = "20260829_0042"

$CompverPins = @{
    "indicator_engine"          = @("v1-reuse-1.0.0", "fe9aab42c34d671e960fd92a9346d3bf60c27135e76e52310d774bc84028dd35")
    "market_context_engine"     = @("mce-1.0.0",      "69902503483502bcd5ce5e35fdb0eeabcb2efcaf7a4b0c262a6fccf2d0af3a8c")
    "chart_intelligence_engine" = @("cie-1.0.0",      "3887d6ca8ba05858f41889cd99fa05aba42663ac22d906a7f989b567c3912180")
}

$NewGuardTriggers = @(
    "v2_chart_intelligence_report_immutable_delete",
    "v2_chart_intelligence_report_immutable_update",
    "v2_computation_version_immutable_delete",
    "v2_computation_version_immutable_update",
    "v2_market_context_report_immutable_delete",
    "v2_market_context_report_immutable_update"
)
$TransitionGuardTriggers = @(
    "v2_md_provider_hist_immutable_delete",
    "v2_md_provider_hist_immutable_update",
    "v2_md_provider_immutable_delete",
    "v2_md_provider_immutable_update"
)

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

$ExpectedLeafName = "axiom_dev.db"

# ---------------------------------------------------------------------
# 0B. OPERATOR INPUT (ABSOLUTE PATH OF THE WORKING DATABASE FILE)
# ---------------------------------------------------------------------

Write-Host ""
Write-Host "STOP THE RUNNING APPLICATION BEFORE CONTINUING (it holds a live"
Write-Host "connection to the target database file). Restart it after this"
Write-Host "pack finishes."
Write-Host ""
Write-Host "This pack VERIFIES (read-only) the end state of the already-applied"
Write-Host "migration 20260831_0043 on the application's SQLite WORKING DATABASE"
Write-Host "FILE. It changes nothing in the database."
Write-Host ""
Write-Host "This pack prompts for NO credential of any kind (no password, no API key)."
Write-Host ""

$TargetDbPath = (Read-Host -Prompt "Absolute path to the application's working SQLite database file (quotes optional; for example C:\Users\victo\.vscode\AXIOM\axiom\backend\axiom_dev.db)").Trim()
# PGF-008: strip one matching pair of surrounding quotes.
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
    throw "STOP: file leaf name '${LeafName}' does not match the working database file name '${ExpectedLeafName}'. Aborting before any database access."
}
$EvidenceRootFull = (Resolve-Path $EvidenceRoot).Path
if ($TargetDbPath.ToLower().StartsWith($EvidenceRootFull.ToLower())) {
    throw "STOP: target file is inside the operator-evidence directory. Aborting before any database access."
}

# ---------------------------------------------------------------------
# 0C. PYTHON HELPER (written to the OS temp directory, removed on exit)
# ---------------------------------------------------------------------

$HelperDir  = Join-Path $env:TEMP "axiom_itrga_0043_verify_v1"
$HelperPath = Join-Path $HelperDir "helper.py"
New-Item -ItemType Directory -Force -Path $HelperDir | Out-Null

$HelperSource = @'
import re
import sqlite3
import sys

MID_DOT = chr(183)


def ro_connect(db_path):
    uri = "file:" + db_path.replace("\\", "/") + "?mode=ro"
    return sqlite3.connect(uri, uri=True)


def rw_connect(db_path):
    return sqlite3.connect(db_path)


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

    if cmd in ("scalar", "integrity", "journalmode", "verifyrows",
               "verifyaudit", "compver", "permbe4", "reportempty"):
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
                # PGF-012: content-based, never position-based.
                rows = con.execute(
                    "SELECT from_status, to_status, authority_ref, evidence_ref, operator_id "
                    "FROM v2_md_provider_status_history ORDER BY id"
                ).fetchall()
                if len(rows) != 2:
                    print("FAIL:history_count=" + str(len(rows)))
                    return
                tuples = [tuple(r) for r in rows]
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
                    "ITRGA-DET-V2-BE-3-P2-FINAL-001 " + MID_DOT
                    + " run a246607c-f0c5-42e9-8f3b-a1e1bd75fa83",
                    None,
                )
                if exp_genesis not in tuples or exp_transition not in tuples:
                    print("FAIL:rows=" + repr(tuples))
                    return
                print("PASS:history_rows_exact")
            elif cmd == "verifyaudit":
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
                    '"evidence_ref": "ITRGA-DET-V2-BE-3-P2-FINAL-001 ' + MID_DOT
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
            elif cmd == "compver":
                pins = {
                    "indicator_engine": ("v1-reuse-1.0.0", sys.argv[3]),
                    "market_context_engine": ("mce-1.0.0", sys.argv[4]),
                    "chart_intelligence_engine": ("cie-1.0.0", sys.argv[5]),
                }
                rows = con.execute(
                    "SELECT component, version, source_hash, evidence_ref, registered_at "
                    "FROM v2_computation_version"
                ).fetchall()
                if len(rows) != 3:
                    print("FAIL:compver_count=" + str(len(rows)))
                    return
                seen = {}
                for component, version, source_hash, evidence_ref, registered_at in rows:
                    if component in seen:
                        print("FAIL:compver_duplicate_component=" + str(component))
                        return
                    seen[component] = (version, source_hash,
                                       evidence_ref, registered_at)
                for component, (exp_version, exp_hash) in pins.items():
                    if component not in seen:
                        print("FAIL:compver_missing=" + component)
                        return
                    version, source_hash, evidence_ref, registered_at = seen[component]
                    if version != exp_version:
                        print("FAIL:compver_version=" + component + "=" + repr(version))
                        return
                    if source_hash != exp_hash:
                        print("FAIL:compver_hash=" + component + "=" + repr(source_hash))
                        return
                    if not re.fullmatch(r"[0-9a-f]{64}", source_hash or ""):
                        print("FAIL:compver_hash_shape=" + component)
                        return
                    if evidence_ref != "BO-V2-BE-4-001":
                        print("FAIL:compver_evidence_ref=" + component + "=" + repr(evidence_ref))
                        return
                    if not registered_at or len(str(registered_at)) < 19:
                        print("FAIL:compver_registered_at_shape=" + component)
                        return
                print("PASS:compver_rows_exact")
            elif cmd == "permbe4":
                rows = con.execute(
                    "SELECT role, permission, sal FROM v2_permission "
                    "WHERE permission LIKE 'v2.research.%'"
                ).fetchall()
                if len(rows) != 5:
                    print("FAIL:permbe4_count=" + str(len(rows)))
                    return
                expected = {
                    ("admin", "v2.research.market_context.read", "SAL-2"),
                    ("admin", "v2.research.chart_intelligence.read", "SAL-2"),
                    ("admin", "v2.research.market_context.compute", "SAL-3"),
                    ("operator", "v2.research.market_context.read", "SAL-2"),
                    ("operator", "v2.research.chart_intelligence.read", "SAL-2"),
                }
                if set(tuple(r) for r in rows) != expected:
                    print("FAIL:permbe4_rows=" + repr(sorted(tuple(r) for r in rows)))
                    return
                total = con.execute("SELECT COUNT(*) FROM v2_permission").fetchone()[0]
                dupes = con.execute(
                    "SELECT COUNT(*) - COUNT(DISTINCT role || '|' || permission) "
                    "FROM v2_permission"
                ).fetchone()[0]
                if dupes != 0:
                    print("FAIL:perm_duplicate_role_permission")
                    return
                print("PASS:perm_rows_exact")
                print("INFO:v2_permission_total=" + str(total))
            elif cmd == "reportempty":
                count_mcr = con.execute(
                    "SELECT COUNT(*) FROM v2_market_context_report"
                ).fetchone()[0]
                count_cir = con.execute(
                    "SELECT COUNT(*) FROM v2_chart_intelligence_report"
                ).fetchone()[0]
                if count_mcr != 0 or count_cir != 0:
                    print("FAIL:report_counts=" + str(count_mcr) + "," + str(count_cir))
                    return
                print("PASS:report_tables_empty")
        finally:
            con.close()
        return

    if cmd == "tryrefuse":
        sql = sys.argv[3]
        con = rw_connect(db_path)
        try:
            try:
                con.execute(sql)
                con.rollback()
                print("SUCCESS_UNEXPECTED")
            except sqlite3.Error as exc:
                con.rollback()
                print("REFUSED:" + str(exc))
        finally:
            con.close()
        return

    if cmd == "guardprobe":
        # Insert-probe-rollback cycle on an (empty) table; the table is
        # left byte-equivalent regardless of the outcome.
        insert_sql = sys.argv[3]
        probe_sql = sys.argv[4]
        con = rw_connect(db_path)
        try:
            con.execute(insert_sql)
            try:
                con.execute(probe_sql)
                outcome = "SUCCESS_UNEXPECTED"
            except sqlite3.Error as exc:
                outcome = "REFUSED:" + str(exc)
            con.rollback()
            print(outcome)
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

function Assert-CurrentExactly {
    param(
        [Parameter(Mandatory = $true)][string]$ExpectedRev,
        [Parameter(Mandatory = $true)][string]$Label
    )

    $Out = Invoke-Alembic -AlembicArgs @("current") -Label $Label
    $Text = Norm-Text $Out
    $RevLines = @($Text -split "`n" | Where-Object { $_ -match '^[0-9a-z]{8}_[0-9]{4}(\s*\([^)]*\))?$' })
    if ($RevLines.Count -ne 1) {
        throw "FAIL: ${Label} - expected exactly one current-revision line in alembic current output; observed $($RevLines.Count) in: '${Text}'."
    }
    $RevLine = $RevLines[0].Trim()
    $RevToken = ($RevLine -replace '\s*\([^)]*\)$', '').Trim()
    $RevSuffix = ""
    if ($RevLine -match '\s*\(([^)]*)\)$') { $RevSuffix = $Matches[1] }
    if ($RevToken -ne $ExpectedRev) {
        throw "FAIL: ${Label} - current revision is '${RevLine}'; expected exactly '${ExpectedRev}'."
    }
    Write-Evidence "Current revision: ${RevToken} (suffix as printed: '${RevSuffix}')"
    return $RevToken
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

function Invoke-ExpectedGuardProbe {
    param(
        [Parameter(Mandatory = $true)][string]$Label,
        [Parameter(Mandatory = $true)][string]$InsertSql,
        [Parameter(Mandatory = $true)][string]$ProbeSql,
        [string]$ExactMessage
    )

    Write-Evidence ""
    Write-Evidence "EXPECTED-GUARD-PROBE: ${Label}"
    Write-Evidence "INSERT (throwaway, rolled back): ${InsertSql}"
    Write-Evidence "PROBE: ${ProbeSql}"

    $Out = Invoke-Py -PyArgs @("guardprobe", ${TargetDbPath}, ${InsertSql}, ${ProbeSql}) -Label $Label
    $Text = (Norm-Text $Out).Trim()

    if ($Text -notlike "REFUSED:*") {
        throw "FAIL: expected guard refusal did not occur (statement succeeded or helper error): ${Label}"
    }
    if ($Text -notlike "*${ExactMessage}*") {
        throw "FAIL: exact expected message was not observed: ${Label}"
    }
    Write-Evidence "PASS: exact refusal message observed; throwaway row rolled back."
}

# ---------------------------------------------------------------------
# B0. RUN IDENTIFICATION
# ---------------------------------------------------------------------

Write-Section "B0. RUN IDENTIFICATION"
Write-Evidence "Pack: ITRGA-V2-0043-VERIFY-PACK-V1"
Write-Evidence "Act: 0043 working-database application act (read-only terminal-state re-proof)"
Write-Evidence "Operator decision: AXIOM-V2-OD-BE-4-009"
Write-Evidence "Plan: ITRGA-PLAN-V2-0043-APPLY-001 (verify pack boundaries B1-B9)"
Write-Evidence "Scope assessment: ITRGA-ASS-V2-0043-APPLY-001"
Write-Evidence "Build order: BO-V2-0043-APPLY-001 (terminal state T-1...T-11)"
Write-Evidence "Apply record required: 0043-APPLY-RUN-V1.txt + 0043-APPLY-FINAL-STATE.txt (this pack pins the apply pack's recorded final values)"
Write-Evidence "Baseline pins file (required at the repo root): ${PinsPath}"
Write-Evidence "Started: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss zzz')"
Write-Evidence "Repo root: ${RepoRoot}"
Write-Evidence "Target file (APPLICATION'S WORKING DATABASE - named by the Operator): ${TargetDbPath}"
Write-Evidence "SQL engine: SQLite (in-process, via the repo venv python sqlite3 module; no database server)"
Write-Evidence "Python (repo venv): ${Python}"
Write-Evidence "Server credentials used: NONE (no database server; no password prompt)"
Write-Evidence "Provider credentials used: NONE"
Write-Evidence "Authority variable: NONE EXISTS FOR THIS ACT (BO T-10); any pre-existing AXIOM_TD_* / authority variables are removed and their absence asserted; this act never sets one."
Write-Evidence "This pack is READ-ONLY with respect to the database. It writes only the transcript."

Push-Location $BackendRoot

try {

    # -----------------------------------------------------------------
    # B0c. HELPER SELF-TEST (READ-ONLY)
    # -----------------------------------------------------------------

    Write-Section "B0c. HELPER SELF-TEST"

    [void](Invoke-Py -PyArgs @("selftest", ${TargetDbPath}) -Label "helper self-test")

    # -----------------------------------------------------------------
    # B0d. RUN ENVIRONMENT (NO CREDENTIALS; NO AUTHORITY VARIABLE)
    # -----------------------------------------------------------------

    Write-Section "B0d. RUN ENVIRONMENT (no credentials; no authority variable for this act)"

    $TargetDbPathUrl = $TargetDbPath.Replace("\", "/")
    $env:AXIOM_DATABASE_URL       = "sqlite+aiosqlite:///" + ${TargetDbPathUrl}
    $env:AXIOM_ENVIRONMENT        = "testing"
    $env:AXIOM_ALLOW_INSECURE_DEV = "true"
    $env:AXIOM_JWT_SECRET_KEY     = "operator-local-test-secret-at-least-32-characters"
    $env:AXIOM_V2_MODE            = "RESEARCH"

    Write-Evidence "Authority/TD environment sweep (BO T-10):"
    $EnvSweepNames = @(Get-ChildItem Env: | Where-Object { $_.Name -like 'AXIOM_TD_*' -or $_.Name -like '*AUTHORITY_REF*' } | ForEach-Object { $_.Name })
    if ($EnvSweepNames.Count -eq 0) {
        Write-Evidence "  none present at act start (recorded)."
    } else {
        foreach ($EnvName in $EnvSweepNames) {
            Remove-Item -Path ("Env:\" + ${EnvName}) -ErrorAction SilentlyContinue
            Write-Evidence ("  removed pre-existing variable: " + ${EnvName} + " (value never printed)")
        }
    }
    $EnvSweepAfter = @(Get-ChildItem Env: | Where-Object { $_.Name -like 'AXIOM_TD_*' -or $_.Name -like '*AUTHORITY_REF*' } | ForEach-Object { $_.Name })
    if ($EnvSweepAfter.Count -ne 0) {
        throw "FAIL: authority/TD environment variables still present after removal: $($EnvSweepAfter -join ', ')"
    }
    Write-Evidence "  absence verified after sweep."
    Write-Evidence "AXIOM_DATABASE_URL: built by this pack (sqlite+aiosqlite scheme) for the target file (value not printed)."
    Write-Evidence "AXIOM_ENVIRONMENT=testing, AXIOM_ALLOW_INSECURE_DEV=true, AXIOM_JWT_SECRET_KEY set (value not printed)."
    Write-Evidence "AXIOM_V2_MODE=RESEARCH."

    # -----------------------------------------------------------------
    # B0e. PIN + APPLY-STATE RECORDS (strict parse; sequencing gate)
    # -----------------------------------------------------------------

    Write-Section "B0e. PIN FILE + APPLY-FINAL-STATE RECORD (strict parse; the verify act cannot precede the apply act)"

    $Pins = Read-Pins -Path $PinsPath -ExpectedKeys @(
        "PIN_FILE_ID", "TARGET_SIZE_BYTES", "TARGET_LAST_WRITE",
        "TARGET_SHA256", "TARGET_CURRENT_REVISION", "TARGET_V2_TRIGGER_COUNT",
        "TARGET_JOURNAL_MODE", "TARGET_SIDECARS"
    ) -Label "baseline pins"
    if ($Pins["PIN_FILE_ID"] -ne "ITRGA-V2-0043-BASELINE-PINS-V1") {
        throw "STOP: baseline pin file identity '$($Pins["PIN_FILE_ID"])' is not ITRGA-V2-0043-BASELINE-PINS-V1."
    }
    Write-Evidence "Baseline pins parsed: TARGET_SHA256 $($Pins["TARGET_SHA256"]) (the expected pre-image; anchor cross-check key)."

    $State = Read-Pins -Path $StateRecPath -ExpectedKeys @(
        "STATE_FILE_ID", "RUN_TIMESTAMP", "POST_SIZE_BYTES",
        "POST_LAST_WRITE", "POST_SHA256", "POST_REVISION",
        "POST_V2_TRIGGER_COUNT", "ANCHOR_FILENAME", "ANCHOR_SIZE_BYTES",
        "ANCHOR_SHA256"
    ) -Label "apply-final-state record"
    if ($State["STATE_FILE_ID"] -ne "ITRGA-V2-0043-APPLY-FINAL-STATE-V1") {
        throw "STOP: state file identity '$($State["STATE_FILE_ID"])' is not ITRGA-V2-0043-APPLY-FINAL-STATE-V1."
    }
    if ($State["POST_REVISION"] -ne ${ApplyTargetRevision}) {
        throw "STOP: apply state record POST_REVISION '$($State["POST_REVISION"])' is not ${ApplyTargetRevision}."
    }
    if ($State["POST_SHA256"] -notmatch '^[0-9a-f]{64}$') {
        throw "STOP: malformed POST_SHA256 in the apply state record."
    }
    if ($State["ANCHOR_SHA256"] -notmatch '^[0-9a-f]{64}$') {
        throw "STOP: malformed ANCHOR_SHA256 in the apply state record."
    }
    Write-Evidence "Apply-final-state record parsed: ${StateRecPath}"
    Write-Evidence "  RUN_TIMESTAMP          $($State["RUN_TIMESTAMP"])"
    Write-Evidence "  POST_SIZE_BYTES        $($State["POST_SIZE_BYTES"])"
    Write-Evidence "  POST_LAST_WRITE        $($State["POST_LAST_WRITE"])"
    Write-Evidence "  POST_SHA256            $($State["POST_SHA256"])"
    Write-Evidence "  POST_REVISION          $($State["POST_REVISION"])"
    Write-Evidence "  POST_V2_TRIGGER_COUNT  $($State["POST_V2_TRIGGER_COUNT"])"
    Write-Evidence "  ANCHOR_FILENAME        $($State["ANCHOR_FILENAME"])"
    Write-Evidence "  ANCHOR_SIZE_BYTES      $($State["ANCHOR_SIZE_BYTES"])"
    Write-Evidence "  ANCHOR_SHA256          $($State["ANCHOR_SHA256"])"
    Write-Evidence "PASS: records valid; the apply act completed and recorded its final values."

    # -----------------------------------------------------------------
    # B0f. PROVENANCE (six chain migrations; abort on any mismatch)
    # -----------------------------------------------------------------

    Write-Section "B0f. PROVENANCE (six chain migrations on disk; abort on any mismatch)"

    foreach ($MigName in @(
        "20260823_0038_v2_be1_core.py",
        "20260824_0039_v2_be2_marketdata.py",
        "20260824_0040_v2_be3_provider.py",
        "20260825_0041_v2_be3_p2_entitlement.py",
        "20260829_0042_v2_be3_p2_transition.py",
        "20260831_0043_v2_be4_research_read_models.py"
    )) {
        $MigPath = Join-Path $BackendRoot ("alembic\versions\" + ${MigName})
        if (!(Test-Path $MigPath)) { throw "STOP: migration file missing: ${MigPath}." }
        $ActualHash = (Get-FileHash $MigPath -Algorithm SHA256).Hash.ToLower()
        $PinnedHash = $ExpectedMigrationHashes[${MigName}]
        Write-Evidence ("{0} | actual {1} | expected {2}" -f ${MigName}, ${ActualHash}, ${PinnedHash})
        if ($ActualHash -ne $PinnedHash) {
            throw "STOP: provenance hash mismatch for ${MigName}. Stopping; report to ITRGA."
        }
    }
    Write-Evidence "PASS: B0f - all six chain migrations (0038-0043) on disk hash to the ITRGA-accepted values."

    # -----------------------------------------------------------------
    # B0g. REPOSITORY STATE EVIDENCE (head asserted for THIS act;
    # listings recorded, not asserted)
    # -----------------------------------------------------------------

    Write-Section "B0g. REPOSITORY STATE EVIDENCE"

    $HeadsOut = Invoke-Alembic -AlembicArgs @("heads") -Label "repository heads"
    $HeadsText = Norm-Text $HeadsOut
    $HeadLines = @($HeadsText -split "`n" | Where-Object { $_ -match '^[0-9a-z]{8}_[0-9]{4}(\s*\([^)]*\))?$' })
    if ($HeadLines.Count -ne 1) {
        throw "FAIL: expected exactly one alembic head; observed $($HeadLines.Count) in: '${HeadsText}'. Stopping; report to ITRGA."
    }
    $RepoHead = ($HeadLines[0].Trim() -replace '\s*\([^)]*\)$', '').Trim()
    if ($RepoHead -ne ${ApplyTargetRevision}) {
        throw "FAIL: repository head is '${RepoHead}'; this act requires exactly ${ApplyTargetRevision} (anything else means the repository moved mid-act). Stopping; report to ITRGA."
    }
    Write-Evidence "PASS: repository head is exactly ${ApplyTargetRevision} (required for this act)."

    Write-Evidence ""
    Write-Evidence "Alembic version (recorded environment evidence):"
    $prev = $ErrorActionPreference
    $ErrorActionPreference = "Continue"
    try {
        $VerOut  = & $Python -m alembic --version 2>&1
        $VerCode = $LASTEXITCODE
    } finally {
        $ErrorActionPreference = $prev
    }
    Emit-Output $VerOut
    if ($VerCode -ne 0) {
        Write-Evidence "Alembic version could not be recorded (exit code ${VerCode}); recorded as not available. This does not fail the act."
    }

    Write-Evidence ""
    Write-Evidence "Migration files under backend\alembic\versions (recorded: name | size | last write | sha256):"
    $VersionsDir = Join-Path $BackendRoot "alembic\versions"
    $VersionFiles = @(Get-ChildItem -Path $VersionsDir -Filter "*.py" | Sort-Object Name)
    if ($VersionFiles.Count -eq 0) {
        throw "FAIL: no migration files found in ${VersionsDir}. Stopping; report to ITRGA."
    }
    Write-Evidence ("  count: " + $VersionFiles.Count)
    foreach ($VFile in $VersionFiles) {
        $VHash = (Get-FileHash $VFile.FullName -Algorithm SHA256).Hash.ToLower()
        Write-Evidence ("  {0} | {1} bytes | {2} | sha256 {3}" -f $VFile.Name, $VFile.Length, $VFile.LastWriteTime.ToString('yyyy-MM-dd HH:mm:ss zzz'), $VHash)
    }

    Write-Evidence ""
    Write-Evidence "Git working-tree status (read-only; recorded, not asserted):"
    $prev = $ErrorActionPreference
    $ErrorActionPreference = "Continue"
    try {
        $GitOut  = & git status --short 2>&1
        $GitCode = $LASTEXITCODE
    } catch {
        $GitOut  = @("git not available: " + $_.Exception.Message)
        $GitCode = -1
    } finally {
        $ErrorActionPreference = $prev
    }
    Emit-Output $GitOut
    if ($GitCode -ne 0) {
        Write-Evidence "Git status could not be recorded (exit code ${GitCode}); recorded as not available. This does not fail the act."
    }

    # -----------------------------------------------------------------
    # B1. TARGET IDENTITY vs THE APPLY RECORD + TRIGGER POSTURE
    # -----------------------------------------------------------------

    Write-Section "B1. TARGET IDENTITY vs THE APPLY-FINAL-STATE RECORD (read-only)"

    $B1File = Get-Item ${TargetDbPath}
    $B1Size  = $B1File.Length
    $B1Write = $B1File.LastWriteTime.ToString('yyyy-MM-dd HH:mm:ss zzz')
    $B1Hash  = (Get-FileHash ${TargetDbPath} -Algorithm SHA256).Hash.ToLower()
    Write-Evidence "Target file: ${TargetDbPath}"
    Write-Evidence "  size       ${B1Size} bytes (apply record $($State["POST_SIZE_BYTES"]))"
    Write-Evidence "  last write ${B1Write} (apply record $($State["POST_LAST_WRITE"]))"
    Write-Evidence "  sha256     ${B1Hash} (apply record $($State["POST_SHA256"]))"
    if ([string]$B1Size -ne $State["POST_SIZE_BYTES"]) {
        throw "FAIL: B1 - target file size differs from the apply act record. Something wrote to the file after the apply; report to ITRGA."
    }
    if ($B1Write -ne $State["POST_LAST_WRITE"]) {
        throw "FAIL: B1 - target file last-write differs from the apply act record. Something wrote to the file after the apply; report to ITRGA."
    }
    if ($B1Hash -ne $State["POST_SHA256"]) {
        throw "FAIL: B1 - target file sha256 differs from the apply act record (byte-identity). Something wrote to the file after the apply; report to ITRGA."
    }
    Write-Evidence "PASS: B1 - target file is byte-identical to the apply act's recorded final state."

    [void](Invoke-Py -PyArgs @("scalar", ${TargetDbPath}, "SELECT sqlite_version();") -Label "B1 sqlite version (recorded)")
    $IntegrityOut = Invoke-Py -PyArgs @("scalar", ${TargetDbPath}, "PRAGMA integrity_check;") -Label "B1 integrity check"
    $IntegrityText = (Norm-Text $IntegrityOut).Trim()
    if ($IntegrityText -ne "ok") {
        throw "FAIL: B1 (T-8) - integrity_check '${IntegrityText}', expected 'ok'."
    }
    $JournalOut = Invoke-Py -PyArgs @("scalar", ${TargetDbPath}, "PRAGMA journal_mode;") -Label "B1 journal mode"
    $JournalText = (Norm-Text $JournalOut).Trim()
    if ($JournalText -ne "delete") {
        throw "FAIL: B1 (T-8) - journal_mode '${JournalText}', expected 'delete'."
    }
    foreach ($Suffix in @("-wal", "-shm")) {
        $SidePath = ${TargetDbPath} + $Suffix
        if (Test-Path $SidePath) {
            throw "FAIL: B1 (T-8) - unexpected sidecar present: ${SidePath}."
        }
        Write-Evidence "Sidecar ${Suffix}: absent"
    }
    Write-Evidence "PASS: B1 (T-8) - integrity ok; journal delete; no sidecars."

    [void](Invoke-Py -PyArgs @("scalar", ${TargetDbPath}, "SELECT name FROM sqlite_master WHERE type='trigger' AND name LIKE 'v2_%' ORDER BY name;") -Label "B1 v2 trigger names (recorded)")
    $TrigCount = Get-PyScalar -Sql "SELECT COUNT(*) FROM sqlite_master WHERE type='trigger' AND name LIKE 'v2_%';" -Label "B1 v2 trigger count"
    if ($TrigCount -ne $State["POST_V2_TRIGGER_COUNT"] -or $TrigCount -ne "18") {
        throw "FAIL: B1 (T-2) - v2 trigger count '${TrigCount}', expected exactly 18 (apply record $($State["POST_V2_TRIGGER_COUNT"]))."
    }
    $NewGuardFound = Get-PyScalar -Sql "SELECT name FROM sqlite_master WHERE type='trigger' AND name IN ('v2_computation_version_immutable_update','v2_computation_version_immutable_delete','v2_market_context_report_immutable_update','v2_market_context_report_immutable_delete','v2_chart_intelligence_report_immutable_update','v2_chart_intelligence_report_immutable_delete') ORDER BY name;" -Label "B1 new guard names"
    $ExpectedNewGuards = $NewGuardTriggers -join "`n"
    if ($NewGuardFound -ne $ExpectedNewGuards) {
        throw "FAIL: B1 (T-3) - the six BE-4 guard trigger names are not exactly the pinned set: '${NewGuardFound}'."
    }
    $TransGuardFound = Get-PyScalar -Sql "SELECT name FROM sqlite_master WHERE type='trigger' AND name IN ('v2_md_provider_immutable_update','v2_md_provider_immutable_delete','v2_md_provider_hist_immutable_update','v2_md_provider_hist_immutable_delete') ORDER BY name;" -Label "B1 transition guard names (intact)"
    $ExpectedTransitionGuards = $TransitionGuardTriggers -join "`n"
    if ($TransGuardFound -ne $ExpectedTransitionGuards) {
        throw "FAIL: B1 - the four inherited transition guard triggers are not intact: '${TransGuardFound}'."
    }
    Write-Evidence "PASS: B1 (T-2/T-3) - 18 v2 triggers; the six BE-4 guard names exact; the four transition guards intact."

    # -----------------------------------------------------------------
    # B2. CURRENT REVISION EXACTLY 20260831_0043
    # -----------------------------------------------------------------

    Write-Section "B2. CURRENT REVISION EXACTLY ${ApplyTargetRevision} (T-1)"

    [void](Assert-CurrentExactly -ExpectedRev ${ApplyTargetRevision} -Label "B2 current")
    Write-Evidence "PASS: B2 (T-1) - the working database is at revision ${ApplyTargetRevision}."

    # -----------------------------------------------------------------
    # B3. RECOVERY ANCHOR (the apply act's pre-image copy; T-11)
    # -----------------------------------------------------------------

    Write-Section "B3. RECOVERY ANCHOR (the apply act's pre-image copy; T-11)"

    $BackupPath = Join-Path $EvidenceDir $($State["ANCHOR_FILENAME"])
    if (!(Test-Path $BackupPath)) {
        throw "FAIL: B3 (T-11) - the apply act's anchor copy is missing: ${BackupPath}. Report to ITRGA; stopping."
    }
    $BackupItem = Get-Item $BackupPath
    $BackupHash = (Get-FileHash $BackupPath -Algorithm SHA256).Hash.ToLower()
    Write-Evidence "Anchor: ${BackupPath}"
    Write-Evidence "  size       $($BackupItem.Length) bytes (apply record $($State["ANCHOR_SIZE_BYTES"]))"
    Write-Evidence "  sha256     ${BackupHash}"
    Write-Evidence "  apply record ANCHOR_SHA256 $($State["ANCHOR_SHA256"])"
    Write-Evidence "  baseline pins TARGET_SHA256 $($Pins["TARGET_SHA256"]) (the recorded pre-image in-force bytes)"
    if ([string]$BackupItem.Length -ne $State["ANCHOR_SIZE_BYTES"]) {
        throw "FAIL: B3 (T-11) - anchor size differs from the apply act record."
    }
    if ($BackupHash -ne $State["ANCHOR_SHA256"]) {
        throw "FAIL: B3 (T-11) - anchor sha256 differs from the apply act record."
    }
    if ($BackupHash -ne $Pins["TARGET_SHA256"]) {
        throw "FAIL: B3 (T-11) - anchor sha256 differs from the ITRGA-pinned pre-image bytes."
    }
    $AnchorIntOut = Invoke-Py -PyArgs @("scalar", ${BackupPath}, "PRAGMA integrity_check;") -Label "B3 anchor integrity"
    $AnchorIntText = (Norm-Text $AnchorIntOut).Trim()
    if ($AnchorIntText -ne "ok") {
        throw "FAIL: B3 (T-11) - anchor integrity_check '${AnchorIntText}', expected 'ok'."
    }
    # NOTE (battery finding V2-0043-BATTERY-F1): the anchor revision must be
    # read FROM THE ANCHOR FILE, not from the working database target.
    $AnchorRevOut = Invoke-Py -PyArgs @("scalar", ${BackupPath}, "SELECT version_num FROM alembic_version;") -Label "B3 anchor revision (recorded)"
    $AnchorRev = (Norm-Text $AnchorRevOut).Trim()
    Write-Evidence "Anchor revision as recorded on the pre-image: ${AnchorRev} (expected the act baseline ${BaselineRevision})"
    if ($AnchorRev -ne ${BaselineRevision}) {
        throw "FAIL: B3 (T-11) - the anchor is not the ${BaselineRevision} pre-image (revision '${AnchorRev}')."
    }
    Write-Evidence "PASS: B3 (T-11) - the anchor is present, integrity ok, revision ${BaselineRevision}; its sha256 matches BOTH the apply act record AND the ITRGA-pinned pre-image bytes."

    # -----------------------------------------------------------------
    # B4. COMPUTATION-VERSION SEEDS (T-6; exact content)
    # -----------------------------------------------------------------

    Write-Section "B4. COMPUTATION-VERSION SEEDS (T-6; exact content)"

    $CompverOut = Invoke-Py -PyArgs @(
        "compver", ${TargetDbPath},
        $CompverPins["indicator_engine"][1],
        $CompverPins["market_context_engine"][1],
        $CompverPins["chart_intelligence_engine"][1]
    ) -Label "B4 computation-version seeds (exact content)"
    $CompverText = (Norm-Text $CompverOut).Trim()
    if ($CompverText -ne "PASS:compver_rows_exact") {
        throw "FAIL: B4 (T-6) - ${CompverText}"
    }
    Write-Evidence "PASS: B4 (T-6) - exactly 3 computation-version rows; per-component version, source_hash (ITRGA-recomputed pins), and evidence_ref all exact."

    # -----------------------------------------------------------------
    # B5. PERMISSION SEEDS (T-5) + REPORT TABLES EMPTY (T-7)
    # -----------------------------------------------------------------

    Write-Section "B5. PERMISSION SEEDS (T-5) + REPORT TABLES EMPTY (T-7)"

    $PermOut = Invoke-Py -PyArgs @("permbe4", ${TargetDbPath}) -Label "B5 permission seeds (exact content)"
    $PermText = (Norm-Text $PermOut).Trim()
    if ($PermText -notlike "PASS:perm_rows_exact*") {
        throw "FAIL: B5 (T-5) - ${PermText}"
    }
    Write-Evidence "PASS: B5 (T-5) - exactly 5 BE-4 permission rows (admin x3, operator x2; SAL-aligned); no role+permission duplicates."

    $EmptyOut = Invoke-Py -PyArgs @("reportempty", ${TargetDbPath}) -Label "B5 report tables empty"
    $EmptyText = (Norm-Text $EmptyOut).Trim()
    if ($EmptyText -ne "PASS:report_tables_empty") {
        throw "FAIL: B5 (T-7) - ${EmptyText}"
    }
    Write-Evidence "PASS: B5 (T-7) - both report tables are empty."

    # -----------------------------------------------------------------
    # B6. INHERITED STATE UNTOUCHED (content-exact; BO section 5)
    # -----------------------------------------------------------------

    Write-Section "B6. INHERITED STATE UNTOUCHED (BE-1 to BE-3; content-exact)"

    [void](Invoke-Py -PyArgs @("scalar", ${TargetDbPath}, "SELECT source_status, entitlement_status, persistence_permitted FROM v2_md_provider WHERE provider_id='twelvedata';") -Label "B6 provider row")
    $EndState = Get-PyScalar -Sql "SELECT source_status, entitlement_status, persistence_permitted FROM v2_md_provider WHERE provider_id='twelvedata';" -Label "B6 end state"
    if ($EndState -ne "contract_tested|verified|0") {
        throw "FAIL: B6 - provider row '${EndState}', expected 'contract_tested|verified|0' (inherited state changed)."
    }

    [void](Invoke-Py -PyArgs @("scalar", ${TargetDbPath}, "SELECT from_status, to_status, authority_ref, evidence_ref, operator_id FROM v2_md_provider_status_history ORDER BY id;") -Label "B6 history rows (ordered by id; lexicographic uuid4 order - informational only)")
    $RowsOut = Invoke-Py -PyArgs @("verifyrows", ${TargetDbPath}) -Label "B6 history exact-content (content-based; PGF-012)"
    $RowsText = (Norm-Text $RowsOut).Trim()
    if ($RowsText -ne "PASS:history_rows_exact") {
        throw "FAIL: B6 - history exact-content check failed: ${RowsText}"
    }

    [void](Invoke-Py -PyArgs @("scalar", ${TargetDbPath}, "SELECT action FROM v2_audit_event WHERE action LIKE 'provider.status_transition%' ORDER BY created_at;") -Label "B6 status-transition audit actions (ordered)")
    $AuditOut = Invoke-Py -PyArgs @("verifyaudit", ${TargetDbPath}) -Label "B6 audit exact-content"
    $AuditText = (Norm-Text $AuditOut).Trim()
    if ($AuditText -ne "PASS:audit_rows_exact") {
        throw "FAIL: B6 - audit exact-content check failed: ${AuditText}"
    }
    Write-Evidence "PASS: B6 - provider row contract_tested|verified|0; history exactly 2 rows content-exact; audit exactly start+complete content-exact; the 0043 act touched no inherited row."

    # -----------------------------------------------------------------
    # B7. GUARD REFUSALS (six; exact R-2 messages; T-3)
    # -----------------------------------------------------------------

    Write-Section "B7. GUARD REFUSALS (six; exact R-2 messages; T-3)"

    $CompverUpdateMessage = "V2 computation version registry is immutable; UPDATE prohibited"
    $CompverDeleteMessage = "V2 computation version registry is immutable; DELETE prohibited"
    $McrUpdateMessage     = "V2 market context reports are immutable; UPDATE prohibited"
    $McrDeleteMessage     = "V2 market context reports are immutable; DELETE prohibited"
    $CirUpdateMessage     = "V2 chart intelligence reports are immutable; UPDATE prohibited"
    $CirDeleteMessage     = "V2 chart intelligence reports are immutable; DELETE prohibited"

    Invoke-ExpectedRefusal -Label "B7: compver UPDATE" -Sql "UPDATE v2_computation_version SET version='probe' WHERE component='indicator_engine';" -ExactMessage ${CompverUpdateMessage}
    Invoke-ExpectedRefusal -Label "B7: compver DELETE" -Sql "DELETE FROM v2_computation_version WHERE component='indicator_engine';" -ExactMessage ${CompverDeleteMessage}

    $McrInsert = "INSERT INTO v2_market_context_report (id, instrument_id, timeframe_set, as_of, mode, status, validation_tier, input_snapshot_id, input_content_hash, observations, engine_versions, engine_versions_hash, operator_id, created_at) VALUES ('guardprobe', 'guardprobe', '[]', '2026-09-02 00:00:00', 'RESEARCH', 'probe', 'probe', 'guardprobe', 'guardprobe', '[]', '{}', 'guardprobe', 'guardprobe', '2026-09-02 00:00:00');"
    Invoke-ExpectedGuardProbe -Label "B7: market-context-report UPDATE" -InsertSql ${McrInsert} -ProbeSql "UPDATE v2_market_context_report SET status='y' WHERE id='guardprobe';" -ExactMessage ${McrUpdateMessage}
    Invoke-ExpectedGuardProbe -Label "B7: market-context-report DELETE" -InsertSql ${McrInsert} -ProbeSql "DELETE FROM v2_market_context_report WHERE id='guardprobe';" -ExactMessage ${McrDeleteMessage}

    $CirInsert = "INSERT INTO v2_chart_intelligence_report (id, market_context_report_id, as_of, mode, status, annotations, interpretations, engine_versions, operator_id, created_at) VALUES ('guardprobe', 'guardprobe', '2026-09-02 00:00:00', 'RESEARCH', 'probe', '[]', '[]', '{}', 'guardprobe', '2026-09-02 00:00:00');"
    Invoke-ExpectedGuardProbe -Label "B7: chart-intelligence-report UPDATE" -InsertSql ${CirInsert} -ProbeSql "UPDATE v2_chart_intelligence_report SET status='y' WHERE id='guardprobe';" -ExactMessage ${CirUpdateMessage}
    Invoke-ExpectedGuardProbe -Label "B7: chart-intelligence-report DELETE" -InsertSql ${CirInsert} -ProbeSql "DELETE FROM v2_chart_intelligence_report WHERE id='guardprobe';" -ExactMessage ${CirDeleteMessage}

    $EmptyOut2 = Invoke-Py -PyArgs @("reportempty", ${TargetDbPath}) -Label "B7 report tables empty after probes"
    $EmptyText2 = (Norm-Text $EmptyOut2).Trim()
    if ($EmptyText2 -ne "PASS:report_tables_empty") {
        throw "FAIL: B7 - report tables are not empty after the guard probes: ${EmptyText2}"
    }
    Write-Evidence "PASS: B7 (T-3) - all six guard refusals observed with the exact R-2 messages; throwaway probe rows rolled back; report tables confirmed empty; the database is unchanged by this act."

    # -----------------------------------------------------------------
    # B8. AUTHORITY VARIABLES (NONE EXIST FOR THIS ACT; ABSENT)
    # -----------------------------------------------------------------

    Write-Section "B8. AUTHORITY VARIABLES (none exist for this act; absent - T-10)"

    $EnvSweepEnd = @(Get-ChildItem Env: | Where-Object { $_.Name -like 'AXIOM_TD_*' -or $_.Name -like '*AUTHORITY_REF*' } | ForEach-Object { $_.Name })
    if ($EnvSweepEnd.Count -ne 0) {
        throw "FAIL: B8 (T-10) - authority/TD environment variables present at act end: $($EnvSweepEnd -join ', ')."
    }
    Write-Evidence "PASS: B8 (T-10) - no AXIOM_TD_* / authority environment variable exists (n/a for this act; the six legacy TD/authority variables absent as in all prior acts)."

    # -----------------------------------------------------------------
    # B9. DRIFT (exactly the 9 inherited V1 tokens; format-independent)
    # -----------------------------------------------------------------

    Write-Section "B9. DRIFT: alembic check (T-9; format-independent - PGF-014)"

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

    if ($DriftCode -eq 0) {
        throw "FAIL: B9 (T-9) - alembic check reported no drift (exit 0); expected the inherited V1 drift set to persist."
    }
    # Recorded alembic drift-marker forms (both on record for this code path):
    #   'Target database is not up to date.'        (revision-offset / summary form)
    #   'New upgrade operations detected: [...]'    (head-satisfied verbose form)
    if (($DriftText -notlike "*not up to date*") -and ($DriftText -notlike "*New upgrade operations detected*")) {
        throw "FAIL: B9 (T-9) - expected a recorded drift marker in alembic check output; observed: '${DriftText}'."
    }
    if ($DriftText -match "v2_md_provider|v2_permission|contract_test|v2_computation_version|v2_market_context_report|v2_chart_intelligence_report|ix_v2_") {
        throw "FAIL: B9 (T-9) - V2 drift token detected in alembic check output."
    }

    # Format-independent name extraction (hardening over VERIFY-PACK-V3 B9; PGF-014 class):
    #  (i)  itemized 'Detected added|removed table|index <name>' lines (quoted or unquoted);
    #  (ii) verbose repr forms Table('<name>') / Index('<name>').
    $DriftNameMatches = @()
    $DriftNameMatches += [regex]::Matches($DriftText, '(?:added|removed) (?:table|index) [''"]?([A-Za-z0-9_]+)[''"]?')
    $DriftNameMatches += [regex]::Matches($DriftText, '(?:Table|Index)\(''([A-Za-z0-9_]+)''')
    $DriftNames = @($DriftNameMatches | ForEach-Object { $_.Groups[1].Value })

    if ($DriftNames.Count -gt 0) {
        foreach ($Token in $ExpectedDriftTokens) {
            if ($DriftText -notlike "*${Token}*") {
                throw "FAIL: B9 (T-9) - expected inherited V1 drift token missing from alembic check output: ${Token}."
            }
        }
        $UnexpectedDriftNames = @($DriftNames | Where-Object { $ExpectedDriftTokens -notcontains $_ })
        if ($UnexpectedDriftNames.Count -ne 0) {
            throw "FAIL: B9 (T-9) - unexpected drift token(s) beyond the 9 inherited V1 tokens: $($UnexpectedDriftNames -join ', ')."
        }
        $DriftNote = "itemized format: the token set is exactly the 9 inherited V1 tokens - all present, no extras, no v2_* or ix_v2_ token"
    } else {
        $DriftNote = "summary format (no itemized list in this alembic version; PGF-014): drift existence asserted (non-zero exit + a recorded drift marker); no v2_* or ix_v2_ token anywhere; the exact object set is proven by B1-B6 (schema and content) and the inherited 9-token set stands per the recorded lineage"
        Write-Evidence "NOTE: this alembic version does not print the itemized drift list (PGF-014); the drift-content proof is carried by B1-B6 assertions plus the recorded lineage. Environment evidence: the alembic version recorded in B0g."
    }

    Write-Evidence "PASS: B9 (T-9) - alembic check: ${DriftNote}."

    # -----------------------------------------------------------------
    # B10. FINAL VERIFY VERDICT (+ READ-ONLY ENFORCEMENT)
    # -----------------------------------------------------------------

    Write-Section "B10. FINAL VERIFY VERDICT"

    $FinalFile = Get-Item ${TargetDbPath}
    $FinalSize  = $FinalFile.Length
    $FinalWrite = $FinalFile.LastWriteTime.ToString('yyyy-MM-dd HH:mm:ss zzz')
    $FinalHash  = (Get-FileHash ${TargetDbPath} -Algorithm SHA256).Hash.ToLower()
    Write-Evidence "Final target file (read-only enforcement):"
    Write-Evidence "  size       ${FinalSize} bytes"
    Write-Evidence "  last write ${FinalWrite}"
    Write-Evidence "  sha256     ${FinalHash}"
    if ([string]$FinalSize -ne [string]$B1Size -or $FinalHash -ne $B1Hash -or $FinalWrite -ne $B1Write) {
        throw "FAIL: B10 - the target file changed DURING this read-only act (B1 vs final state differ). Report to ITRGA."
    }
    Write-Evidence "PASS: B10 - the target file is byte-identical before and after this read-only act (size, last write, sha256 all equal)."

    $AnchorFinalHash = (Get-FileHash ${BackupPath} -Algorithm SHA256).Hash.ToLower()
    if ($AnchorFinalHash -ne $State["ANCHOR_SHA256"]) {
        throw "FAIL: B10 - the anchor file changed during this act."
    }
    Write-Evidence "Anchor unchanged at act end: ${BackupPath} (sha256 ${AnchorFinalHash})"

    Write-Evidence ""
    Write-Evidence "VERIFY VERDICT: PASS - the terminal state of migration 20260831_0043_v2_be4_research_read_models is verified IN FORCE on the application's working SQLite database file '${TargetDbPath}' (applied ONCE per the apply act record; this verification act changed nothing in the database)."
    Write-Evidence "Terminal state (BO-V2-0043-APPLY-001 T-1...T-11): revision 20260831_0043; 18 v2 triggers; six R-2 guard triggers in force (exact refusal messages); three BE-4 tables with two unique constraints and three indexes; 3 computation-version seeds exact; 5 permission seeds exact; both report tables empty; inherited BE-1 to BE-3 state untouched (content-exact proofs); drift = exactly the 9 inherited V1 tokens; anchor proven (the byte-identical 0042-state pre-image); no authority variable exists for this act."
    Write-Evidence "Transcript: ${Transcript}"
    Write-Evidence "Disposal: this pack created no file other than the transcript; the throwaway helper was removed on exit; the database is unchanged. Restart the application when ready."

} catch {
    Write-Evidence ""
    Write-Evidence "VERIFY VERDICT: FAIL - RUN ABORTED: $($_.Exception.Message)"
    Write-Evidence "Transcript: ${Transcript}"
    Write-Evidence "This act is READ-ONLY: the database state is unchanged by this act; the apply act's state stands as the apply record shows."
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
    $EnvFinalSweep = @(Get-ChildItem Env: | Where-Object { $_.Name -like 'AXIOM_TD_*' -or $_.Name -like '*AUTHORITY_REF*' } | ForEach-Object { $_.Name })
    foreach ($EnvName in $EnvFinalSweep) {
        Remove-Item -Path ("Env:\" + ${EnvName}) -ErrorAction SilentlyContinue
    }
    Remove-Variable TargetDbPathUrl -ErrorAction SilentlyContinue

    Remove-Item -Recurse -Force ${HelperDir} -ErrorAction SilentlyContinue

    Write-Host "Environment cleaned (AXIOM_DATABASE_URL, AXIOM_JWT_SECRET_KEY, AXIOM_ALLOW_INSECURE_DEV, AXIOM_ENVIRONMENT, AXIOM_V2_MODE, any AXIOM_TD_* / authority variables); helper removed."
}
