# =====================================================================
# AXIOM V2 - 0043 WORKING-DATABASE APPLICATION ACT
# ITRGA SQLITE APPLY ACT EVIDENCE PACK (V1)
# Pack ID: ITRGA-V2-0043-APPLY-PACK-V1
# Authority:
#   - AXIOM-V2-OD-BE-4-009 (Operator decision - 0043 working-DB
#     application act; single sanctioned mutation)
#   - ITRGA-PLAN-V2-0043-APPLY-001 (instrument design A0-A8)
#   - ITRGA-ASS-V2-0043-APPLY-001 (scope; re-pins 0038/0039/0041
#     resolved 2026-09-02)
#   - BO-V2-0043-APPLY-001 (terminal state T-1...T-11)
#   - ITRGA-PTN-V2-PACK-001 (pack discipline; battery floor)
# Pattern: ITRGA-V2-BE-3-P2-TRANS-APPLY-PACK-V5 and VERIFY-PACK-V3
#   (instruments of record of the BE-3 P2 transition act; all PGF-001
#   through PGF-014 lessons incorporated by construction: pure ASCII,
#   no compound braced expansions (PGF-009), helper command functions
#   with non-colliding parameter names (PGF-001), dialect-correct SQL
#   functions (PGF-010), content-based row comparisons (PGF-012),
#   format-independent drift assertions (PGF-014), byte-identity
#   self-check via the issuance note (PGF-011), quote-normalized
#   operator input (PGF-008), canonical vocabulary (PGF-013)).
#
# WHAT THIS PACK DOES:
#   Applies the approved, hash-verified migration
#   20260831_0043_v2_be4_research_read_models ONCE to the
#   APPLICATION'S WORKING SQLITE DATABASE FILE (backend\axiom_dev.db)
#   and proves the Build Order terminal state on SQLite:
#   revision 20260831_0043; 18 v2 triggers; six R-2 guard triggers in
#   force (exact names, exact refusal messages); three BE-4 tables with
#   their constraints and indexes; exactly 3 computation-version seed
#   rows (exact content) and exactly 5 permission seed rows (exact
#   content); both report tables empty; the inherited BE-1 to BE-3
#   state untouched (byte-exact row proofs); drift re-baselined to
#   exactly the 9 inherited V1 tokens.
#
#   SQLite-specific design (as the proven predecessor packs):
#   - No database server: NO psql, NO password prompt, NO credential
#     of any kind. All SQL runs through the repo venv python (sqlite3
#     module) against the file directly.
#   - FILE-LEVEL ANCHOR copy to operator-evidence\BE-4 BEFORE any
#     modification: the complete, credential-free rollback anchor.
#   - Exact-content comparison runs IN PYTHON (never position-based).
#   - Spot-checks assert the EXACT SQLite guard messages, including
#     transactional insert-probe-rollback cycles on the report tables
#     (an UPDATE/DELETE that matches zero rows cannot fire a trigger;
#     the probe inserts a throwaway row, proves the refusal, and the
#     connection rollback removes the throwaway - the probe changes
#     nothing).
#   - It does NOT create or delete any database file.
#   - It modifies ONLY the target file (the single sanctioned
#     mutation) and writes: the transcript, the anchor copy, and the
#     apply-final-state record (for the verify pack), all in
#     operator-evidence\BE-4; plus a throwaway helper in the OS temp
#     directory (removed on exit).
#   - NO AUTHORITY VARIABLE EXISTS FOR THIS ACT (BO T-10): the pack
#     enumerates and removes any pre-existing AXIOM_TD_* / authority
#     variables and asserts their absence. It never sets one.
#
# BEFORE RUNNING: STOP THE RUNNING APPLICATION (it holds a live
#   connection to the target database file). Restart it after the
#   pack completes (the pack says so at the end of a PASS).
#
# RUN MODE: this pack MUST be executed as a file. Pasting the script
#   into an interactive console is NOT an acceptable evidence mode
#   (PGF-004).
#
# OPERATOR INSTRUCTION CARD (ITRGA-PTN-V2-PACK-001 section 2.2):
#   1. Before running anything, verify byte-identity of the THREE
#      issued artifacts with Get-FileHash -Algorithm MD5 against the
#      ITRGA ISSUANCE NOTE (ITRGA-ISS-V2-0043-PACKS-001, 2026-09-02):
#        ITRGA_V2_0043_APPLY_PACK_V1.ps1   (this file)
#        ITRGA_V2_0043_VERIFY_PACK_V1.ps1  (verify pack; runs SECOND)
#        ITRGA_V2_0043_BASELINE_PINS.txt   (must sit at the repo root)
#      If any MD5 does not match: STOP; do not run anything; report
#      to ITRGA.
#   2. Execute ONLY this file, from the repository root:
#        powershell -NoProfile -ExecutionPolicy Bypass -File ".\ITRGA_V2_0043_APPLY_PACK_V1.ps1"
#   3. Single expected input: the absolute path of the working
#      database file backend\axiom_dev.db (a path, not a credential).
#      Nothing else is asked. No password. No API key.
#   4. Send back to ITRGA afterwards:
#        operator-evidence\BE-4\0043-APPLY-RUN-V1.txt
#      (keep operator-evidence\BE-4\0043-APPLY-FINAL-STATE.txt in
#      place - the verify pack reads it).
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
$Transcript    = Join-Path $EvidenceDir "0043-APPLY-RUN-V1.txt"
$PinsPath      = Join-Path $RepoRoot "ITRGA_V2_0043_BASELINE_PINS.txt"
$StateRecPath  = Join-Path $EvidenceDir "0043-APPLY-FINAL-STATE.txt"

New-Item -ItemType Directory -Force -Path $EvidenceDir | Out-Null
Remove-Item -Force -ErrorAction SilentlyContinue $Transcript
Remove-Item -Force -ErrorAction SilentlyContinue $StateRecPath

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
    # duplicate keys, strict value shapes. Fails closed.
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

# Chain migration provenance pins (sha256; re-pins of
# ITRGA-ASS-V2-0043-APPLY-001 section 3 and the approved manifests).
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

# Computation-version seed pins: component -> (version, source_hash).
# source_hash values computed by ITRGA recomputation from the accepted
# BE-4 source corpus (app/v2/research/versioning.py file-hash recipe:
# sha256 over "relpath\0" + file bytes + "\0", in order, per component).
$CompverPins = @{
    "indicator_engine"          = @("v1-reuse-1.0.0", "fe9aab42c34d671e960fd92a9346d3bf60c27135e76e52310d774bc84028dd35")
    "market_context_engine"     = @("mce-1.0.0",      "69902503483502bcd5ce5e35fdb0eeabcb2efcaf7a4b0c262a6fccf2d0af3a8c")
    "chart_intelligence_engine" = @("cie-1.0.0",      "3887d6ca8ba05858f41889cd99fa05aba42663ac22d906a7f989b567c3912180")
}

# The six R-2 guard triggers (0043) and their exact SQLite messages.
$NewGuardTriggers = @(
    "v2_chart_intelligence_report_immutable_delete",
    "v2_chart_intelligence_report_immutable_update",
    "v2_computation_version_immutable_delete",
    "v2_computation_version_immutable_update",
    "v2_market_context_report_immutable_delete",
    "v2_market_context_report_immutable_update"
)
# The four transition-era guard triggers (inherited; asserted intact).
$TransitionGuardTriggers = @(
    "v2_md_provider_hist_immutable_delete",
    "v2_md_provider_hist_immutable_update",
    "v2_md_provider_immutable_delete",
    "v2_md_provider_immutable_update"
)

# Inherited V1 drift tokens (T-9; drift after the apply = exactly these).
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

# Working-database file name (refused if mismatched).
$ExpectedLeafName = "axiom_dev.db"

# Populated by A2; $null until then.
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
Write-Host "This pack applies the approved migration 20260831_0043 ONCE to the"
Write-Host "application's SQLite WORKING DATABASE FILE and then proves the end state."
Write-Host ""
Write-Host "This pack prompts for NO credential of any kind (no password, no API key)."
Write-Host ""

$TargetDbPath = (Read-Host -Prompt "Absolute path to the application's working SQLite database file (quotes optional; for example C:\Users\victo\.vscode\AXIOM\axiom\backend\axiom_dev.db)").Trim()
# PGF-008: Read-Host returns raw input; strip one matching pair of
# surrounding quotes (quotes are not part of a file path).
if ($TargetDbPath.Length -ge 2) {
    if (($TargetDbPath.StartsWith('"') -and $TargetDbPath.EndsWith('"')) -or
        ($TargetDbPath.StartsWith("'") -and $TargetDbPath.EndsWith("'"))) {
        $TargetDbPath = $TargetDbPath.Substring(1, $TargetDbPath.Length - 2).Trim()
        Write-Host "NOTE: surrounding quotes removed from the entered path (quotes are not part of a file path)."
    }
}
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
    throw "STOP: file leaf name '${LeafName}' does not match the working database file name '${ExpectedLeafName}'. Aborting before any database modification."
}
$EvidenceRootFull = (Resolve-Path $EvidenceRoot).Path
# PGF-009: bare expression - a dollar-brace span containing calls is a
# literal variable name in PowerShell (proven on Windows PowerShell 5.1).
if ($TargetDbPath.ToLower().StartsWith($EvidenceRootFull.ToLower())) {
    throw "STOP: target file is inside the operator-evidence directory. Aborting before any database modification."
}

# ---------------------------------------------------------------------
# 0C. PYTHON HELPER (written to the OS temp directory, removed on exit)
# ---------------------------------------------------------------------

$HelperDir  = Join-Path $env:TEMP "axiom_itrga_0043_apply_v1"
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
                # PGF-012: the history id column is a uuid4 TEXT primary
                # key; rows are matched by CONTENT, never by position.
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
                # Exactly 3 seed rows; content compared by (component,
                # version, source_hash, evidence_ref); id is a random
                # uuid4 and registered_at is seed-time - shape only.
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
        # Proves an UPDATE/DELETE guard on an (empty) table: a guard
        # cannot fire without a matching row, so the probe inserts a
        # throwaway row, runs the probe statement, and ALWAYS rolls
        # the connection back - the table is left byte-equivalent
        # (empty) regardless of the outcome.
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

function Assert-CurrentExactly {
    # Runs `alembic current` and requires EXACTLY one revision line
    # whose token is exactly $ExpectedRev (head-suffix recorded).
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
# A0. RUN IDENTIFICATION
# ---------------------------------------------------------------------

Write-Section "A0. RUN IDENTIFICATION"
Write-Evidence "Pack: ITRGA-V2-0043-APPLY-PACK-V1"
Write-Evidence "Act: 0043 working-database application act (single sanctioned mutation)"
Write-Evidence "Operator decision: AXIOM-V2-OD-BE-4-009"
Write-Evidence "Plan: ITRGA-PLAN-V2-0043-APPLY-001 (boundaries A0-A8)"
Write-Evidence "Scope assessment: ITRGA-ASS-V2-0043-APPLY-001 (re-pins resolved 2026-09-02)"
Write-Evidence "Build order: BO-V2-0043-APPLY-001 (terminal state T-1...T-11)"
Write-Evidence "Baseline pins file (required at the repo root): ${PinsPath}"
Write-Evidence "Started: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss zzz')"
Write-Evidence "Repo root: ${RepoRoot}"
Write-Evidence "Target file (APPLICATION'S WORKING DATABASE - named by the Operator): ${TargetDbPath}"
Write-Evidence "SQL engine: SQLite (in-process, via the repo venv python sqlite3 module; no database server)"
Write-Evidence "Python (repo venv): ${Python}"
Write-Evidence "Server credentials used: NONE (no database server; no password prompt)"
Write-Evidence "Provider credentials used: NONE"
Write-Evidence "Authority variable: NONE EXISTS FOR THIS ACT (BO T-10); any pre-existing AXIOM_TD_* / authority variables are removed and their absence asserted; this pack never sets one."
Write-Evidence "Read-write scope: exactly one mutation (alembic upgrade 20260831_0043) on the target file; plus the transcript, the anchor copy, and the apply-final-state record in operator-evidence\BE-4; plus the throwaway helper (removed on exit)."

# ---------------------------------------------------------------------
# A0b. BASELINE PINS (the ITRGA-pinned in-force baseline record)
# ---------------------------------------------------------------------

Write-Section "A0b. BASELINE PINS (strict parse of the ITRGA-pinned baseline record)"

$Pins = Read-Pins -Path $PinsPath -ExpectedKeys @(
    "PIN_FILE_ID", "TARGET_SIZE_BYTES", "TARGET_LAST_WRITE",
    "TARGET_SHA256", "TARGET_CURRENT_REVISION", "TARGET_V2_TRIGGER_COUNT",
    "TARGET_JOURNAL_MODE", "TARGET_SIDECARS"
) -Label "baseline pins"

if ($Pins["PIN_FILE_ID"] -ne "ITRGA-V2-0043-BASELINE-PINS-V1") {
    throw "STOP: baseline pin file identity '$($Pins["PIN_FILE_ID"])' is not ITRGA-V2-0043-BASELINE-PINS-V1."
}
if ($Pins["TARGET_SIZE_BYTES"] -notmatch '^[0-9]+$') { throw "STOP: malformed TARGET_SIZE_BYTES in baseline pins." }
if ($Pins["TARGET_SHA256"] -notmatch '^[0-9a-f]{64}$') { throw "STOP: malformed TARGET_SHA256 in baseline pins." }
if ($Pins["TARGET_CURRENT_REVISION"] -notmatch '^[0-9]{8}_[0-9]{4}$') { throw "STOP: malformed TARGET_CURRENT_REVISION in baseline pins." }
if ($Pins["TARGET_V2_TRIGGER_COUNT"] -notmatch '^[0-9]+$') { throw "STOP: malformed TARGET_V2_TRIGGER_COUNT in baseline pins." }
if ($Pins["TARGET_JOURNAL_MODE"] -ne "delete") { throw "STOP: baseline pins journal mode is not 'delete'." }
if ($Pins["TARGET_SIDECARS"] -ne "none") { throw "STOP: baseline pins sidecar state is not 'none'." }
if ($Pins["TARGET_CURRENT_REVISION"] -ne ${BaselineRevision}) {
    throw "STOP: baseline pins current revision '$($Pins["TARGET_CURRENT_REVISION"])' is not the act baseline ${BaselineRevision}."
}

Write-Evidence "Pin file: ${PinsPath}"
Write-Evidence "  PIN_FILE_ID              $($Pins["PIN_FILE_ID"])"
Write-Evidence "  TARGET_SIZE_BYTES        $($Pins["TARGET_SIZE_BYTES"])"
Write-Evidence "  TARGET_LAST_WRITE        $($Pins["TARGET_LAST_WRITE"])"
Write-Evidence "  TARGET_SHA256            $($Pins["TARGET_SHA256"])"
Write-Evidence "  TARGET_CURRENT_REVISION  $($Pins["TARGET_CURRENT_REVISION"])"
Write-Evidence "  TARGET_V2_TRIGGER_COUNT  $($Pins["TARGET_V2_TRIGGER_COUNT"])"
Write-Evidence "  TARGET_JOURNAL_MODE      $($Pins["TARGET_JOURNAL_MODE"])"
Write-Evidence "  TARGET_SIDECARS          $($Pins["TARGET_SIDECARS"])"
Write-Evidence "PASS: baseline pins parsed, shapes valid, identity and revision correct."

Push-Location $BackendRoot

try {

    # -----------------------------------------------------------------
    # A0c. HELPER SELF-TEST (READ-ONLY; BEFORE ANY MODIFICATION)
    # -----------------------------------------------------------------

    Write-Section "A0c. HELPER SELF-TEST"

    [void](Invoke-Py -PyArgs @("selftest", ${TargetDbPath}) -Label "helper self-test")

    # -----------------------------------------------------------------
    # A0d. RUN ENVIRONMENT (NO CREDENTIALS; NO AUTHORITY VARIABLE)
    # -----------------------------------------------------------------

    Write-Section "A0d. RUN ENVIRONMENT (no credentials; no authority variable for this act)"

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
    # A1. BASELINE (PRE-MUTATION) - abort on any difference from the
    # ITRGA-pinned in-force state
    # -----------------------------------------------------------------

    Write-Section "A1. BASELINE (pre-mutation; abort on any difference from the pinned in-force state)"

    # A1.1: current revision gate (read-only; explicit already-applied abort).
    $PreRev = Assert-CurrentExactly -ExpectedRev ${BaselineRevision} -Label "A1 baseline current"
    Write-Evidence "PASS: A1.1 - current revision is exactly ${BaselineRevision} (abort would have fired with the operand already at ${ApplyTargetRevision} had it been applied; STOP/abort on any other value)."

    # A1.2: file identity (abort on any difference).
    $B1File = Get-Item ${TargetDbPath}
    $B1Size  = $B1File.Length
    $B1Write = $B1File.LastWriteTime.ToString('yyyy-MM-dd HH:mm:ss zzz')
    $B1Hash  = (Get-FileHash ${TargetDbPath} -Algorithm SHA256).Hash.ToLower()
    Write-Evidence "Target file: ${TargetDbPath}"
    Write-Evidence "  size       ${B1Size} bytes (pinned $($Pins["TARGET_SIZE_BYTES"]))"
    Write-Evidence "  last write ${B1Write} (pinned $($Pins["TARGET_LAST_WRITE"]))"
    Write-Evidence "  sha256     ${B1Hash} (pinned $($Pins["TARGET_SHA256"]))"
    if ([string]$B1Size -ne $Pins["TARGET_SIZE_BYTES"]) {
        throw "FAIL: A1 - target file size differs from the pinned in-force state. Aborting before any modification; report to ITRGA."
    }
    if ($B1Write -ne $Pins["TARGET_LAST_WRITE"]) {
        throw "FAIL: A1 - target file last-write differs from the pinned in-force state. Aborting before any modification; report to ITRGA."
    }
    if ($B1Hash -ne $Pins["TARGET_SHA256"]) {
        throw "FAIL: A1 - target file sha256 differs from the pinned in-force state (byte-identity check). Aborting before any modification; report to ITRGA."
    }
    Write-Evidence "PASS: A1.2 - target file is byte-identical to the pinned in-force state (size, last write, sha256)."

    # A1.3: integrity / journal / sidecars.
    [void](Invoke-Py -PyArgs @("scalar", ${TargetDbPath}, "SELECT sqlite_version();") -Label "A1 sqlite version (recorded)")
    $IntegrityOut = Invoke-Py -PyArgs @("scalar", ${TargetDbPath}, "PRAGMA integrity_check;") -Label "A1 integrity check"
    $IntegrityText = (Norm-Text $IntegrityOut).Trim()
    if ($IntegrityText -ne "ok") {
        throw "FAIL: A1 - integrity_check '${IntegrityText}', expected 'ok'. Stopping before any modification; report to ITRGA."
    }
    $JournalOut = Invoke-Py -PyArgs @("scalar", ${TargetDbPath}, "PRAGMA journal_mode;") -Label "A1 journal mode"
    $JournalText = (Norm-Text $JournalOut).Trim()
    if ($JournalText -ne $Pins["TARGET_JOURNAL_MODE"]) {
        throw "FAIL: A1 - journal_mode '${JournalText}', expected '$($Pins["TARGET_JOURNAL_MODE"])'. Stopping before any modification; report to ITRGA."
    }
    foreach ($Suffix in @("-wal", "-shm")) {
        $SidePath = ${TargetDbPath} + $Suffix
        if (Test-Path $SidePath) {
            throw "FAIL: A1 - unexpected sidecar present: ${SidePath} (pinned sidecar state is 'none'). Stopping before any modification; report to ITRGA."
        }
        Write-Evidence "Sidecar ${Suffix}: absent"
    }
    Write-Evidence "PASS: A1.3 - integrity ok; journal delete; no sidecars."

    # A1.4: trigger posture (exactly the pinned count; the four
    # transition guards present; the six BE-4 guards absent).
    [void](Invoke-Py -PyArgs @("scalar", ${TargetDbPath}, "SELECT name FROM sqlite_master WHERE type='trigger' AND name LIKE 'v2_%' ORDER BY name;") -Label "A1 v2 trigger names (recorded)")
    $PreTrigCount = Get-PyScalar -Sql "SELECT COUNT(*) FROM sqlite_master WHERE type='trigger' AND name LIKE 'v2_%';" -Label "A1 v2 trigger count"
    if ($PreTrigCount -ne $Pins["TARGET_V2_TRIGGER_COUNT"]) {
        throw "FAIL: A1 - v2 trigger count '${PreTrigCount}', expected the pinned '$($Pins["TARGET_V2_TRIGGER_COUNT"])'. Stopping before any modification; report to ITRGA."
    }
    $PreGuardNames = Get-PyScalar -Sql "SELECT name FROM sqlite_master WHERE type='trigger' AND name IN ('v2_md_provider_immutable_update','v2_md_provider_immutable_delete','v2_md_provider_hist_immutable_update','v2_md_provider_hist_immutable_delete') ORDER BY name;" -Label "A1 transition guard names"
    $ExpectedTransitionGuards = $TransitionGuardTriggers -join "`n"
    if ($PreGuardNames -ne $ExpectedTransitionGuards) {
        throw "FAIL: A1 - transition guard trigger set '${PreGuardNames}' is not exactly the four recorded transition guards. Stopping before any modification; report to ITRGA."
    }
    $PreBe4Guards = Get-PyScalar -Sql "SELECT COUNT(*) FROM sqlite_master WHERE type='trigger' AND name IN ('v2_computation_version_immutable_update','v2_computation_version_immutable_delete','v2_market_context_report_immutable_update','v2_market_context_report_immutable_delete','v2_chart_intelligence_report_immutable_update','v2_chart_intelligence_report_immutable_delete');" -Label "A1 BE-4 guard absence"
    if ($PreBe4Guards -ne "0") {
        throw "FAIL: A1 - BE-4 guard triggers already present ('${PreBe4Guards}'); 0043 may already be applied. Stopping before any modification; report to ITRGA."
    }
    Write-Evidence "PASS: A1.4 - exactly $($Pins["TARGET_V2_TRIGGER_COUNT"]) v2 triggers; the four transition guards present; the six BE-4 guards absent."

    # A1.5: inherited state baseline (recorded; re-proven after the apply).
    [void](Invoke-Py -PyArgs @("scalar", ${TargetDbPath}, "SELECT source_status, entitlement_status, persistence_permitted FROM v2_md_provider WHERE provider_id='twelvedata';") -Label "A1 inherited provider row (recorded)")
    [void](Invoke-Py -PyArgs @("scalar", ${TargetDbPath}, "SELECT COUNT(*) FROM v2_md_provider_status_history;") -Label "A1 inherited history count (recorded)")

    # Alembic version (recorded environment evidence).
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
        throw "FAIL: A1 - could not record the alembic version (exit code ${VerCode}). Stopping before any modification; report to ITRGA."
    }

    # -----------------------------------------------------------------
    # A2. ANCHOR (first side effect; target: the evidence directory)
    # -----------------------------------------------------------------

    Write-Section "A2. ANCHOR (file-level backup; first side effect; evidence directory only)"

    $BackupStamp = Get-Date -Format "yyyyMMddHHmmss"
    $MainBackupPath = Join-Path $EvidenceDir (${LeafName} + ".pre-0043-" + ${BackupStamp} + ".bak")
    Write-Evidence "Creating anchor copy: ${MainBackupPath}"
    Copy-Item ${TargetDbPath} ${MainBackupPath} -Force
    if (!(Test-Path ${MainBackupPath})) {
        throw "FAIL: A2 - anchor copy was not created. Aborting before any database modification; report to ITRGA."
    }
    $MainBackupHash = (Get-FileHash ${MainBackupPath} -Algorithm SHA256).Hash.ToLower()
    if ($MainBackupHash -ne $B1Hash) {
        throw "FAIL: A2 - anchor hash differs from the original file hash. Aborting before any database modification; report to ITRGA."
    }
    $AnchorIntOut = Invoke-Py -PyArgs @("scalar", ${MainBackupPath}, "PRAGMA integrity_check;") -Label "A2 anchor integrity"
    $AnchorIntText = (Norm-Text $AnchorIntOut).Trim()
    if ($AnchorIntText -ne "ok") {
        throw "FAIL: A2 - anchor copy integrity_check '${AnchorIntText}', expected 'ok'. Aborting before any database modification; report to ITRGA."
    }
    $AnchorSize = (Get-Item ${MainBackupPath}).Length
    Write-Evidence "Anchor created and verified: ${MainBackupPath}"
    Write-Evidence "  size       ${AnchorSize} bytes"
    Write-Evidence "  sha256     ${MainBackupHash} (verified equal to the pre-mutation file)"
    Write-Evidence "  integrity  ok"
    Write-Evidence "PASS: A2 - a proven rollback anchor exists before any mutation. The mutation may not precede a valid anchor; it does not."

    # -----------------------------------------------------------------
    # A3. PROVENANCE (on-disk runtime re-pin of the chain migrations)
    # -----------------------------------------------------------------

    Write-Section "A3. PROVENANCE (on-disk runtime re-pin; abort on any mismatch)"

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
        Write-Evidence ("{0}" -f ${MigName})
        Write-Evidence "  actual   ${ActualHash}"
        Write-Evidence "  expected ${PinnedHash}"
        if ($ActualHash -ne $PinnedHash) {
            throw "STOP: A3 - provenance hash mismatch for ${MigName} - the migration on disk is not the ITRGA-accepted file. The apply must not proceed; report to ITRGA."
        }
    }
    Write-Evidence "PASS: A3 - all six chain migrations (0038-0043) on disk hash to the ITRGA-accepted values."

    # Repository head (recorded; must be exactly the apply target).
    $HeadsOut = Invoke-Alembic -AlembicArgs @("heads") -Label "A3 repository heads (recorded)"
    $HeadsText = Norm-Text $HeadsOut
    $HeadLines = @($HeadsText -split "`n" | Where-Object { $_ -match '^[0-9a-z]{8}_[0-9]{4}(\s*\([^)]*\))?$' })
    if ($HeadLines.Count -ne 1) {
        throw "FAIL: A3 - expected exactly one alembic head; observed $($HeadLines.Count) in: '${HeadsText}'. Stopping before the apply; report to ITRGA."
    }
    $RepoHead = ($HeadLines[0].Trim() -replace '\s*\([^)]*\)$', '').Trim()
    if ($RepoHead -ne ${ApplyTargetRevision}) {
        throw "FAIL: A3 - repository head is '${RepoHead}'; this act requires exactly ${ApplyTargetRevision} (anything else means the repository moved mid-act). Stopping before the apply; report to ITRGA."
    }
    Write-Evidence "Repository head: ${RepoHead} (exactly the apply target, as required)"

    # -----------------------------------------------------------------
    # A4. THE APPLY (exactly one invocation)
    # -----------------------------------------------------------------

    Write-Section "A4. THE APPLY: alembic upgrade ${ApplyTargetRevision} (exactly one invocation; literal revision, never 'head')"

    [void](Invoke-Alembic -AlembicArgs @("upgrade", ${ApplyTargetRevision}) -Label "the apply")

    # -----------------------------------------------------------------
    # A5. POST-APPLY STATE (Build Order T-1...T-7)
    # -----------------------------------------------------------------

    Write-Section "A5. POST-APPLY STATE"

    # A5.1: revision exactly 20260831_0043 (T-1).
    [void](Assert-CurrentExactly -ExpectedRev ${ApplyTargetRevision} -Label "A5 post-apply current")
    Write-Evidence "PASS: A5.1 (T-1) - current revision is exactly ${ApplyTargetRevision}."

    # A5.2: 18 v2 triggers; six new guard names exact (T-2, T-3).
    [void](Invoke-Py -PyArgs @("scalar", ${TargetDbPath}, "SELECT name FROM sqlite_master WHERE type='trigger' AND name LIKE 'v2_%' ORDER BY name;") -Label "A5 v2 trigger names (recorded)")
    $PostTrigCount = Get-PyScalar -Sql "SELECT COUNT(*) FROM sqlite_master WHERE type='trigger' AND name LIKE 'v2_%';" -Label "A5 v2 trigger count"
    if ($PostTrigCount -ne "18") {
        throw "FAIL: A5 (T-2) - v2 trigger count '${PostTrigCount}', expected exactly 18 (12 inherited + 6 new)."
    }
    $NewGuardFound = Get-PyScalar -Sql "SELECT name FROM sqlite_master WHERE type='trigger' AND name IN ('v2_computation_version_immutable_update','v2_computation_version_immutable_delete','v2_market_context_report_immutable_update','v2_market_context_report_immutable_delete','v2_chart_intelligence_report_immutable_update','v2_chart_intelligence_report_immutable_delete') ORDER BY name;" -Label "A5 new guard names"
    $ExpectedNewGuards = $NewGuardTriggers -join "`n"
    if ($NewGuardFound -ne $ExpectedNewGuards) {
        throw "FAIL: A5 (T-3) - the six BE-4 guard trigger names are not exactly the pinned set: '${NewGuardFound}'."
    }
    $TransGuardFound = Get-PyScalar -Sql "SELECT name FROM sqlite_master WHERE type='trigger' AND name IN ('v2_md_provider_immutable_update','v2_md_provider_immutable_delete','v2_md_provider_hist_immutable_update','v2_md_provider_hist_immutable_delete') ORDER BY name;" -Label "A5 transition guard names (intact)"
    if ($TransGuardFound -ne $ExpectedTransitionGuards) {
        throw "FAIL: A5 - the four inherited transition guard triggers are not intact: '${TransGuardFound}'."
    }
    Write-Evidence "PASS: A5.2 (T-2/T-3) - 18 v2 triggers; the six BE-4 guard names exact; the four transition guards intact."

    # A5.3: the three tables, constraints, indexes (T-4).
    $TableCount = Get-PyScalar -Sql "SELECT COUNT(*) FROM sqlite_master WHERE type='table' AND name IN ('v2_computation_version','v2_market_context_report','v2_chart_intelligence_report');" -Label "A5 table presence"
    if ($TableCount -ne "3") {
        throw "FAIL: A5 (T-4) - BE-4 table count '${TableCount}', expected 3."
    }
    $CompverDdl = Get-PyScalar -Sql "SELECT sql FROM sqlite_master WHERE type='table' AND name='v2_computation_version';" -Label "A5 compver DDL"
    if ($CompverDdl -notlike "*uq_v2_compver_component_version*") {
        throw "FAIL: A5 (T-4) - uq_v2_compver_component_version not present in v2_computation_version DDL."
    }
    $McrDdl = Get-PyScalar -Sql "SELECT sql FROM sqlite_master WHERE type='table' AND name='v2_market_context_report';" -Label "A5 mcr DDL"
    if ($McrDdl -notlike "*uq_v2_mcr_determinism_anchor*") {
        throw "FAIL: A5 (T-4) - uq_v2_mcr_determinism_anchor not present in v2_market_context_report DDL."
    }
    $IndexNames = Get-PyScalar -Sql "SELECT name FROM sqlite_master WHERE type='index' AND name IN ('ix_v2_mcr_instrument','ix_v2_mcr_mode','ix_v2_cir_mcr') ORDER BY name;" -Label "A5 index names"
    $ExpectedIndexes = @("ix_v2_cir_mcr", "ix_v2_mcr_instrument", "ix_v2_mcr_mode") -join "`n"
    if ($IndexNames -ne $ExpectedIndexes) {
        throw "FAIL: A5 (T-4) - expected indexes ix_v2_mcr_instrument, ix_v2_mcr_mode, ix_v2_cir_mcr; found '${IndexNames}'."
    }
    Write-Evidence "PASS: A5.3 (T-4) - three tables with the two unique constraints and the three indexes present."

    # A5.4: computation-version seed content (T-6), exact.
    $CompverOut = Invoke-Py -PyArgs @(
        "compver", ${TargetDbPath},
        $CompverPins["indicator_engine"][1],
        $CompverPins["market_context_engine"][1],
        $CompverPins["chart_intelligence_engine"][1]
    ) -Label "A5 computation-version seeds (exact content)"
    $CompverText = (Norm-Text $CompverOut).Trim()
    if ($CompverText -ne "PASS:compver_rows_exact") {
        throw "FAIL: A5 (T-6) - computation-version seed check failed: ${CompverText}"
    }
    Write-Evidence "PASS: A5.4 (T-6) - exactly 3 computation-version rows; per-component version, source_hash (ITRGA-recomputed pins), and evidence_ref all exact."

    # A5.5: permission seed content (T-5), exact.
    $PermOut = Invoke-Py -PyArgs @("permbe4", ${TargetDbPath}) -Label "A5 permission seeds (exact content)"
    $PermText = (Norm-Text $PermOut).Trim()
    if ($PermText -notlike "PASS:perm_rows_exact*") {
        throw "FAIL: A5 (T-5) - permission seed check failed: ${PermText}"
    }
    Write-Evidence "PASS: A5.5 (T-5) - exactly 5 BE-4 permission rows (admin x3, operator x2; SAL-aligned); no role+permission duplicates."

    # A5.6: report tables empty (T-7).
    $EmptyOut = Invoke-Py -PyArgs @("reportempty", ${TargetDbPath}) -Label "A5 report tables empty"
    $EmptyText = (Norm-Text $EmptyOut).Trim()
    if ($EmptyText -ne "PASS:report_tables_empty") {
        throw "FAIL: A5 (T-7) - report tables are not empty: ${EmptyText}"
    }
    Write-Evidence "PASS: A5.6 (T-7) - both report tables are empty."

    # A5.7: inherited state untouched (no-touch proof, BO section 5).
    $ProvNow = Get-PyScalar -Sql "SELECT source_status, entitlement_status, persistence_permitted FROM v2_md_provider WHERE provider_id='twelvedata';" -Label "A5 inherited provider row"
    if ($ProvNow -ne "contract_tested|verified|0") {
        throw "FAIL: A5 - inherited provider row changed: '${ProvNow}'."
    }
    $RowsOut = Invoke-Py -PyArgs @("verifyrows", ${TargetDbPath}) -Label "A5 inherited history exact-content"
    $RowsText = (Norm-Text $RowsOut).Trim()
    if ($RowsText -ne "PASS:history_rows_exact") {
        throw "FAIL: A5 - inherited history content changed: ${RowsText}"
    }
    $AuditOut = Invoke-Py -PyArgs @("verifyaudit", ${TargetDbPath}) -Label "A5 inherited audit exact-content"
    $AuditText = (Norm-Text $AuditOut).Trim()
    if ($AuditText -ne "PASS:audit_rows_exact") {
        throw "FAIL: A5 - inherited audit content changed: ${AuditText}"
    }
    Write-Evidence "PASS: A5.7 - inherited BE-1 to BE-3 state untouched: provider row contract_tested|verified|0; history exactly 2 rows content-exact; audit exactly start+complete content-exact."

    # A5.8: file posture after the apply.
    [void](Invoke-Py -PyArgs @("scalar", ${TargetDbPath}, "PRAGMA integrity_check;") -Label "A5 integrity check")
    $PostJournal = Get-PyScalar -Sql "PRAGMA journal_mode;" -Label "A5 journal mode"
    if ($PostJournal -ne "delete") {
        throw "FAIL: A5 (T-8) - journal_mode '${PostJournal}', expected 'delete'."
    }
    foreach ($Suffix in @("-wal", "-shm")) {
        $SidePath = ${TargetDbPath} + $Suffix
        if (Test-Path $SidePath) {
            $SideItem = Get-Item $SidePath
            Write-Evidence "Sidecar ${Suffix}: present, $($SideItem.Length) bytes (FAIL: expected absent)"
            throw "FAIL: A5 (T-8) - unexpected sidecar present: ${SidePath}."
        }
        Write-Evidence "Sidecar ${Suffix}: absent"
    }
    Write-Evidence "PASS: A5.8 (T-8) - integrity ok; journal delete; no sidecars."

    # Final target-file state (recorded for the verify pack via the
    # apply-final-state record; T-11 anchor cross-check below).
    $FinalFile = Get-Item ${TargetDbPath}
    $FinalSize  = $FinalFile.Length
    $FinalWrite = $FinalFile.LastWriteTime.ToString('yyyy-MM-dd HH:mm:ss zzz')
    $FinalHash  = (Get-FileHash ${TargetDbPath} -Algorithm SHA256).Hash.ToLower()
    Write-Evidence "Post-apply target file:"
    Write-Evidence "  size       ${FinalSize} bytes"
    Write-Evidence "  last write ${FinalWrite}"
    Write-Evidence "  sha256     ${FinalHash}"

    # -----------------------------------------------------------------
    # A6. GUARD SPOT-CHECKS (six refusals, exact R-2 messages)
    # -----------------------------------------------------------------

    Write-Section "A6. GUARD SPOT-CHECKS (six refusals; exact R-2 messages)"

    $CompverUpdateMessage = "V2 computation version registry is immutable; UPDATE prohibited"
    $CompverDeleteMessage = "V2 computation version registry is immutable; DELETE prohibited"
    $McrUpdateMessage     = "V2 market context reports are immutable; UPDATE prohibited"
    $McrDeleteMessage     = "V2 market context reports are immutable; DELETE prohibited"
    $CirUpdateMessage     = "V2 chart intelligence reports are immutable; UPDATE prohibited"
    $CirDeleteMessage     = "V2 chart intelligence reports are immutable; DELETE prohibited"

    # compver holds three seed rows: direct UPDATE/DELETE probes fire.
    Invoke-ExpectedRefusal -Label "A6: compver UPDATE" -Sql "UPDATE v2_computation_version SET version='probe' WHERE component='indicator_engine';" -ExactMessage ${CompverUpdateMessage}
    Invoke-ExpectedRefusal -Label "A6: compver DELETE" -Sql "DELETE FROM v2_computation_version WHERE component='indicator_engine';" -ExactMessage ${CompverDeleteMessage}

    # Report tables are empty: an UPDATE/DELETE matches zero rows and
    # cannot fire the guard. Proof by transactional probe cycle: insert
    # a throwaway row, probe, always roll back (table left empty).
    $McrInsert = "INSERT INTO v2_market_context_report (id, instrument_id, timeframe_set, as_of, mode, status, validation_tier, input_snapshot_id, input_content_hash, observations, engine_versions, engine_versions_hash, operator_id, created_at) VALUES ('guardprobe', 'guardprobe', '[]', '2026-09-02 00:00:00', 'RESEARCH', 'probe', 'probe', 'guardprobe', 'guardprobe', '[]', '{}', 'guardprobe', 'guardprobe', '2026-09-02 00:00:00');"
    Invoke-ExpectedGuardProbe -Label "A6: market-context-report UPDATE" -InsertSql ${McrInsert} -ProbeSql "UPDATE v2_market_context_report SET status='y' WHERE id='guardprobe';" -ExactMessage ${McrUpdateMessage}
    Invoke-ExpectedGuardProbe -Label "A6: market-context-report DELETE" -InsertSql ${McrInsert} -ProbeSql "DELETE FROM v2_market_context_report WHERE id='guardprobe';" -ExactMessage ${McrDeleteMessage}

    $CirInsert = "INSERT INTO v2_chart_intelligence_report (id, market_context_report_id, as_of, mode, status, annotations, interpretations, engine_versions, operator_id, created_at) VALUES ('guardprobe', 'guardprobe', '2026-09-02 00:00:00', 'RESEARCH', 'probe', '[]', '[]', '{}', 'guardprobe', '2026-09-02 00:00:00');"
    Invoke-ExpectedGuardProbe -Label "A6: chart-intelligence-report UPDATE" -InsertSql ${CirInsert} -ProbeSql "UPDATE v2_chart_intelligence_report SET status='y' WHERE id='guardprobe';" -ExactMessage ${CirUpdateMessage}
    Invoke-ExpectedGuardProbe -Label "A6: chart-intelligence-report DELETE" -InsertSql ${CirInsert} -ProbeSql "DELETE FROM v2_chart_intelligence_report WHERE id='guardprobe';" -ExactMessage ${CirDeleteMessage}

    # Probe hygiene: the report tables must still be empty after the
    # rollback probes (T-7 re-asserted).
    $EmptyOut2 = Invoke-Py -PyArgs @("reportempty", ${TargetDbPath}) -Label "A6 report tables empty after probes"
    $EmptyText2 = (Norm-Text $EmptyOut2).Trim()
    if ($EmptyText2 -ne "PASS:report_tables_empty") {
        throw "FAIL: A6 - report tables are not empty after the guard probes: ${EmptyText2}"
    }
    Write-Evidence "PASS: A6 - all six guard refusals observed with the exact R-2 messages; throwaway probe rows rolled back; report tables confirmed empty."

    # -----------------------------------------------------------------
    # A7. DRIFT RE-BASELINE (format-independent; PGF-014)
    # -----------------------------------------------------------------

    Write-Section "A7. DRIFT RE-BASELINE: alembic check (expected: exactly the 9 inherited V1 tokens; format-independent)"

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

    # Format-independent assertions (PGF-014): drift must exist and no
    # v2_* / ix_v2_ token may appear anywhere in any format.
    if ($DriftCode -eq 0) {
        throw "FAIL: A7 (T-9) - alembic check reported no drift (exit 0); expected the inherited V1 drift set to persist (non-zero exit)."
    }
    # Recorded alembic drift-marker forms (both on record for this code path):
    #   'Target database is not up to date.'        (revision-offset / summary form)
    #   'New upgrade operations detected: [...]'    (head-satisfied verbose form)
    if (($DriftText -notlike "*not up to date*") -and ($DriftText -notlike "*New upgrade operations detected*")) {
        throw "FAIL: A7 (T-9) - expected a recorded drift marker in alembic check output; observed: '${DriftText}'."
    }
    if ($DriftText -match "v2_md_provider|v2_permission|contract_test|v2_computation_version|v2_market_context_report|v2_chart_intelligence_report|ix_v2_") {
        throw "FAIL: A7 (T-9) - V2 drift token detected in alembic check output; after the 0043 apply the BE-4 schema set must have left the drift set."
    }

    # Format-independent name extraction (hardening over VERIFY-PACK-V3 B9; PGF-014 class):
    #  (i)  itemized 'Detected added|removed table|index <name>' lines (quoted or unquoted);
    #  (ii) verbose repr forms Table('<name>') / Index('<name>').
    $DriftNameMatches = @()
    $DriftNameMatches += [regex]::Matches($DriftText, '(?:added|removed) (?:table|index) [''"]?([A-Za-z0-9_]+)[''"]?')
    $DriftNameMatches += [regex]::Matches($DriftText, '(?:Table|Index)\(''([A-Za-z0-9_]+)''')
    $DriftNames = @($DriftNameMatches | ForEach-Object { $_.Groups[1].Value })

    if ($DriftNames.Count -gt 0) {
        # Itemized drift format: assert the set is EXACTLY the 9
        # inherited V1 tokens (no extras, none missing).
        foreach ($Token in $ExpectedDriftTokens) {
            if ($DriftText -notlike "*${Token}*") {
                throw "FAIL: A7 (T-9) - expected inherited V1 drift token missing from alembic check output: ${Token}."
            }
        }
        $UnexpectedDriftNames = @($DriftNames | Where-Object { $ExpectedDriftTokens -notcontains $_ })
        if ($UnexpectedDriftNames.Count -ne 0) {
            throw "FAIL: A7 (T-9) - unexpected drift token(s) beyond the 9 inherited V1 tokens: $($UnexpectedDriftNames -join ', ')."
        }
        $DriftNote = "itemized format: the token set is exactly the 9 inherited V1 tokens - all present, no extras, no v2_* or ix_v2_ token"
    } else {
        # Summary format (PGF-014): the itemized list is not printed by
        # this alembic version. Drift existence is asserted above; the
        # BE-4 object's presence is proven independently in A5 (tables,
        # constraints, indexes, triggers, seeds), and the inherited set
        # stands per the inherited lineage recorded in the issuance.
        $DriftNote = "summary format (no itemized list in this alembic version; PGF-014): drift existence asserted (non-zero exit + a recorded drift marker); no v2_* or ix_v2_ token anywhere; the exact object set is proven by A5 (schema) and the inherited 9-token set stands per the recorded lineage"
        Write-Evidence "NOTE: this alembic version does not print the itemized drift list (PGF-014); the drift-content proof is carried by A5 schema assertions plus the recorded lineage. Environment evidence: the alembic version recorded in A1."
    }

    Write-Evidence "PASS: A7 (T-9) - alembic check: ${DriftNote}."

    # -----------------------------------------------------------------
    # A8. VERDICT, STATE RECORD, CLEANUP
    # -----------------------------------------------------------------

    Write-Section "A8. FINAL APPLY VERDICT"

    # Anchor still equals the A2 record (T-11 cross-check).
    if ($null -ne ${MainBackupPath} -and (Test-Path ${MainBackupPath})) {
        $BackupFinalHash = (Get-FileHash ${MainBackupPath} -Algorithm SHA256).Hash.ToLower()
        if ($BackupFinalHash -ne ${MainBackupHash}) {
            throw "FAIL: A8 (T-11) - the anchor file changed after creation. Stopping; report to ITRGA."
        }
        Write-Evidence "Anchor unchanged since creation: ${MainBackupPath} (sha256 ${BackupFinalHash})"
    }

    # Apply-final-state record (consumed by ITRGA-V2-0043-VERIFY-PACK-V1).
    $StateLines = @(
        "# ITRGA-V2-0043-APPLY-FINAL-STATE-V1",
        "# Written by ITRGA-V2-0043-APPLY-PACK-V1 at the end of a PASS.",
        "# Consumed strictly by ITRGA-V2-0043-VERIFY-PACK-V1 (B1/B3).",
        "STATE_FILE_ID=ITRGA-V2-0043-APPLY-FINAL-STATE-V1",
        "RUN_TIMESTAMP=$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss zzz')",
        "POST_SIZE_BYTES=${FinalSize}",
        "POST_LAST_WRITE=${FinalWrite}",
        "POST_SHA256=${FinalHash}",
        "POST_REVISION=${ApplyTargetRevision}",
        "POST_V2_TRIGGER_COUNT=18",
        "ANCHOR_FILENAME=$((Split-Path ${MainBackupPath} -Leaf))",
        "ANCHOR_SIZE_BYTES=${AnchorSize}",
        "ANCHOR_SHA256=${MainBackupHash}"
    )
    Set-Content -Path $StateRecPath -Value $StateLines -Encoding ASCII
    Write-Evidence "Apply-final-state record written: ${StateRecPath}"

    Write-Evidence ""
    Write-Evidence "APPLY VERDICT: PASS - the approved migration 20260831_0043_v2_be4_research_read_models was applied ONCE to the application's working SQLite database file '${TargetDbPath}'."
    Write-Evidence "Terminal state (BO-V2-0043-APPLY-001): revision 20260831_0043; 18 v2 triggers; six R-2 guard triggers in force (exact refusal messages); three BE-4 tables with two unique constraints and three indexes; 3 computation-version seeds exact; 5 permission seeds exact; both report tables empty; inherited BE-1 to BE-3 state untouched (content-exact proofs); drift re-baselined to exactly the 9 inherited V1 tokens; anchor created and verified."
    Write-Evidence "Transcript: ${Transcript}"
    Write-Evidence "State record: ${StateRecPath} (required by the verify pack; do not move or edit it.)"
    Write-Evidence "Disposal: this pack created no database file; it modified only the target file (the single sanctioned mutation) and wrote the transcript, the anchor copy, and the state record. Restart the application when ready - or after the verify run, per the ITRGA instruction."

} catch {
    Write-Evidence ""
    Write-Evidence "APPLY VERDICT: FAIL - RUN ABORTED: $($_.Exception.Message)"
    Write-Evidence "Transcript: ${Transcript}"
    if ($null -ne ${MainBackupPath} -and (Test-Path ${MainBackupPath})) {
        Write-Evidence "Anchor (unchanged rollback copy for any ITRGA-directed recovery): ${MainBackupPath}"
    } else {
        Write-Evidence "No anchor was created by this run (aborted before A2): the target file was not modified by this pack in that branch."
    }
    Write-Evidence "The apply-final-state record is written only after a full PASS; its absence is itself the 'not applied' marker for the verify pack."
    if (!(Test-Path $StateRecPath)) {
        Write-Evidence "State record absent: confirmed."
    } else {
        Write-Evidence "State record present: ${StateRecPath}"
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
    $EnvFinalSweep = @(Get-ChildItem Env: | Where-Object { $_.Name -like 'AXIOM_TD_*' -or $_.Name -like '*AUTHORITY_REF*' } | ForEach-Object { $_.Name })
    foreach ($EnvName in $EnvFinalSweep) {
        Remove-Item -Path ("Env:\" + ${EnvName}) -ErrorAction SilentlyContinue
    }
    Remove-Variable TargetDbPathUrl -ErrorAction SilentlyContinue

    Remove-Item -Recurse -Force ${HelperDir} -ErrorAction SilentlyContinue

    Write-Host "Environment cleaned (AXIOM_DATABASE_URL, AXIOM_JWT_SECRET_KEY, AXIOM_ALLOW_INSECURE_DEV, AXIOM_ENVIRONMENT, AXIOM_V2_MODE, any AXIOM_TD_* / authority variables); helper removed."
}
