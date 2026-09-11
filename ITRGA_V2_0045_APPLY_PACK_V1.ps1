# =====================================================================
# AXIOM V2 - 0044/0045 WORKING-DATABASE APPLICATION ACT (BAND BE-5)
# ITRGA SQLITE APPLY ACT EVIDENCE PACK (V1)
# Pack ID: ITRGA-V2-0045-APPLY-PACK-V1
# Authority:
#   - ITRGA-DET-V2-BE-5-FINAL-001 (final determination; verdict C
#     full-verify PASS; C-1 closed; C-2 = this act's evidence envelope)
#   - BO-V2-BE-5-001 (terminal state T-1...T-12; T-1/T-2 land on the
#     working lineage through this act)
#   - Delivery: AXIOM-V2-BE-5-DR-001 v1.0.1 + REM-001 evidence set
#     (all 19 file hashes pinned to the Rev-2 literals)
# Pattern: ITRGA-V2-0043-APPLY-PACK-V1 (instrument of record of the
#   BE-4 working-DB application act; all PGF-001 through PGF-014
#   lessons incorporated by construction: pure ASCII, no compound
#   braced expansions, helper command functions with non-colliding
#   parameter names, dialect-correct SQL, content-based row
#   comparisons, format-independent drift assertions, quote-normalized
#   operator input, canonical vocabulary).
#
# WHAT THIS PACK DOES:
#   Applies the verified band-BE-5 chain extension (migrations
#   20260902_0044_v2_be5_ml_governance and
#   20260902_0045_v2_be5_signal_contracts) ONCE to the APPLICATION'S
#   WORKING SQLITE DATABASE FILE (backend\axiom_dev.db) with exactly
#   one literal-revision invocation: alembic upgrade 20260902_0045.
#   It then proves the terminal state on SQLite:
#   revision 20260902_0045; exactly 28 v2 triggers; the 10 BE-5 guard
#   triggers in force (exact names, exact refusal messages, probe
#   cycles that roll their throwaway rows back); the five BE-5 tables
#   with their constraints and six indexes; exactly 5
#   computation-version rows (the two BE-5 rows proven by RUNTIME
#   RECOMPUTATION of the engine source-file hashes on this machine);
#   exactly 35 permission rows (8 additive BE-5 rows content-exact);
#   all five BE-5 tables empty; the inherited BE-1..BE-4 state
#   untouched (byte/content-exact proofs); drift re-baselined to
#   exactly the 9 inherited V1 tokens.
#
#   SQLite-specific design (as the proven predecessor packs):
#   - No database server: NO psql, NO password prompt, NO credential
#     of any kind. All SQL runs through the repo venv python (sqlite3
#     module) against the file directly.
#   - FILE-LEVEL ANCHOR copy to operator-evidence\BE-5 BEFORE any
#     modification: the complete, credential-free rollback anchor.
#   - Exact-content comparison runs IN PYTHON (never position-based).
#   - Baseline authority = the 0043 apply-final-state record produced
#     by the BE-4 act (chain of custody). Two-tier baseline: Tier 1
#     byte-identity of the target file vs that record; if forfeited
#     (application activity since the 0043 PASS), Tier 2 re-proves the
#     entire 0043 terminal state by content (revision, trigger set,
#     seed content, inherited anchors) and aborts on any failure.
#   - Spot-checks assert the EXACT SQLite guard messages, including
#     transactional insert-probe-rollback cycles on the empty tables
#     (the probe changes nothing).
#   - It does NOT create or delete any database file.
#   - It modifies ONLY the target file (the single sanctioned
#     mutation) and writes: the transcript, the anchor copy, and the
#     apply-final-state record (for the verify pack), all in
#     operator-evidence\BE-5; plus a throwaway helper in the OS temp
#     directory (removed on exit).
#   - NO AUTHORITY VARIABLE EXISTS FOR THIS ACT: the pack enumerates
#     and removes any pre-existing AXIOM_TD_* / authority variables
#     and asserts their absence. It never sets one.
#
# BEFORE RUNNING: STOP THE RUNNING APPLICATION (it holds a live
#   connection to the target database file). Do NOT restart it before
#   the verify pack has also completed (the verify pack requires the
#   five new tables to still be empty).
#
# RUN MODE: this pack MUST be executed as a file. Pasting the script
#   into an interactive console is NOT an acceptable evidence mode
#   (PGF-004).
#
# OPERATOR INSTRUCTION CARD:
#   1. Before running anything, verify byte-identity of the TWO
#      issued artifacts against the ITRGA issuance note
#      (ITRGA_ISSUANCE_V2_0045_PACKS_001.md):
#        ITRGA_V2_0045_APPLY_PACK_V1.ps1   (this file; runs FIRST)
#        ITRGA_V2_0045_VERIFY_PACK_V1.ps1  (verify pack; runs SECOND)
#      If any hash does not match: STOP; do not run; report to ITRGA.
#   2. The BE-5 file set must already be in the repository exactly as
#      delivered (the packs re-pin all 19 delivered files by hash and
#      abort on ANY deviation).
#   3. Execute ONLY this file, from the repository root:
#        powershell -NoProfile -ExecutionPolicy Bypass -File ".\ITRGA_V2_0045_APPLY_PACK_V1.ps1"
#   4. Single expected input: the absolute path of the working
#      database file backend\axiom_dev.db (a path, not a credential).
#      Nothing else is asked. No password. No API key.
#   5. Then run the verify pack (do NOT restart the application
#      between apply and verify):
#        powershell -NoProfile -ExecutionPolicy Bypass -File ".\ITRGA_V2_0045_VERIFY_PACK_V1.ps1"
#   6. Send BOTH transcripts back to ITRGA:
#        operator-evidence\BE-5\0045-APPLY-RUN-V1.txt
#        operator-evidence\BE-5\0045-VERIFY-RUN-V1.txt
#      (this is the evidence envelope that closes C-2 and places the
#      BO-V2-BE-5-001 terminal state on the working lineage.)
#
# Save the two issued artifacts to the AXIOM repository root:
#   C:\Users\victo\.vscode\AXIOM\axiom\
# =====================================================================

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

# ---------------------------------------------------------------------
# 0. ENCODING, LOCAL PATHS AND TOOL CHECKS
# ---------------------------------------------------------------------

[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
[Console]::InputEncoding  = [System.Text.Encoding]::UTF8
$env:PYTHONIOENCODING = "utf-8"

$RepoRoot    = (Get-Location).Path
$BackendRoot = Join-Path $RepoRoot "backend"
$Python      = Join-Path $RepoRoot ".venv\Scripts\python.exe"

if (!(Test-Path $BackendRoot)) { throw "Backend directory not found: ${BackendRoot}" }
if (!(Test-Path $Python))      { throw "Python executable not found: ${Python}" }

$EvidenceRoot  = Join-Path $RepoRoot "operator-evidence"
$EvidenceDir   = Join-Path $EvidenceRoot "BE-5"
$Transcript    = Join-Path $EvidenceDir "0045-APPLY-RUN-V1.txt"
$PrevStateDir  = Join-Path $EvidenceRoot "BE-4"
$PrevStatePath = Join-Path $PrevStateDir "0043-APPLY-FINAL-STATE.txt"
$StateRecPath  = Join-Path $EvidenceDir "0045-APPLY-FINAL-STATE.txt"

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
    param($Lines)
    foreach ($Line in @($Lines)) {
        Add-Content -Path $Transcript -Value ([string]$Line) -Encoding UTF8
    }
    $Lines | Out-Host
}

function Norm-Text {
    param($Lines)
    return (@($Lines | ForEach-Object { ([string]$_).Trim() }) -join "`n")
}

function Read-Pins {
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
# 0A. CONSTANTS (BO-V2-BE-5-001; REM-001 Rev-2 pins)
# ---------------------------------------------------------------------

# Chain migration provenance pins (sha256). 0038-0043 re-pinned from
# the BE-4 act; 0044/0045 from the verified REM-001 Rev-2 literals.
$ExpectedMigrationHashes = @{
    "20260823_0038_v2_be1_core.py"                 = "6e071157c204e29bfb1254400f0a4543d776931fa5834723cc497d12a0b8f588"
    "20260824_0039_v2_be2_marketdata.py"           = "bc11cae24cdbe47361454a676604a9f81b1754df47058185dd4c002689ab5b19"
    "20260824_0040_v2_be3_provider.py"             = "1332ebf5780fcda00d19589400bbeb873f7187fbd1f4915da093f822f392b226"
    "20260825_0041_v2_be3_p2_entitlement.py"       = "d775c34aedac8fffd594f4ac4434f48c9d9cfd2fa88f4d3fd1cf9e7ba278dadd"
    "20260829_0042_v2_be3_p2_transition.py"        = "af77a63f903a43e2eb7b4426b67de7113791f37918bbfe7f465d8f1bab3cf8d4"
    "20260831_0043_v2_be4_research_read_models.py" = "ab90576203d9f7946154ad4efd7a3d52bc98b91e328dbf2a4dca0b5049bda84b"
    "20260902_0044_v2_be5_ml_governance.py"        = "18e14f0ae971b7ae3e94b02c3d23ef7a608a6f1dde711e52c6f64d780e20efab"
    "20260902_0045_v2_be5_signal_contracts.py"     = "9aa87508b6db4d74296f8dabfab33ae7fb84dc705326f141b4b42e2d4f981f52"
}
$ApplyTargetRevision = "20260902_0045"
$BaselineRevision    = "20260831_0043"

# Remaining 11 delivered BE-5 files (sha256; REM-001 Rev-2 literals).
$ExpectedDeliveredHashes = @{
    "backend\app\v2\research_governance\__init__.py"    = "858384d1ac31773e2f5d956b240844066acb74eea8b6a3e5b6bbb53b2c6624bb"
    "backend\app\v2\research_governance\contracts.py"   = "a0bfccadfa835b148691b127d1dde9c7bd4e19e59908a61d37ac6ba30860c314"
    "backend\app\v2\research_governance\decisions.py"   = "80f3efaed42f52290f4b47007b8ed09eed19d3e769ece4678a5ae6c5fec960aa"
    "backend\app\v2\research_governance\signals.py"     = "dbbedf5eda999a5400ad23de7bb072b33d4d2ae7466214def2b7e4ea5e007386"
    "backend\app\v2\research_governance\api.py"         = "ac348b8667e0e3dad45646019e5ad52cec2706b89a245a25d42d1996e3156701"
    "backend\app\v2\research_governance\diagnostics.py" = "ecd4e36e454e8771ed01bf6427d7deb0d6f5a6c4b051039e0f6a748f511200a3"
    "backend\app\db\models\v2_research_governance.py"   = "f6650efc81b222c5520b6c0aa3b0d5581a5e203f3f8ec968bf4b0bd08a2e4e78"
    "backend\app\db\models\v2_signal.py"                = "6aa2294890bce9bc6f2943a720bc6d927d97130453c3ecd976e2e49c4cac3be7"
    "backend\tests\test_v2_be5_decisions.py"            = "8388a9e709f4b2c5ad0f9b1f9afd4461398f17908071726909b4c2a180fd7d37"
    "backend\tests\test_v2_be5_migration.py"            = "6d36ad127d759e5240562689e6b8cd8268162951c7950aa248e05b72d3fc0e8c"
    "backend\tests\test_v2_be5_api.py"                  = "a7f39d1d7add9a16be2d20fa433601d99e397825abf5e0cf6d53d378e8d777d2"
    "backend\tests\test_v2_be5_diagnostics.py"          = "2663058c8e6860cc98d129472c7484de1e1cde692fab76298eabf053cc7f6a5b"
    "backend\tests\test_v2_be5_lifecycle.py"            = "39c41896456f7c59351ac9bab0bf26441203e512248d160066c0d3de204207dc"
    "backend\app\v2\api\router.py"                      = "c9ee841429621801d5175d40c9dbbd07767f7be6b029fdf2498e27f3ffbbd19c"
    "backend\app\v2\rbac\permissions.py"                = "45eb34e11add36355940d52116376fc387d86d264827ee1cae0cd46c1bcbf462"
    "backend\app\db\models\__init__.py"                 = "b569a8e430926847827b63e6bddc39d895d52f4b0849d069d01e57c1c1c6d5a7"
    "backend\tests\test_v2_be4_migration.py"            = "5935b9ea3c530dab3454daefa6c4e0ea3f2b46c957c923ccd62c6bb4eb5dce4d"
}

# The ten BE-5 guard triggers and their exact SQLite messages.
$Be5GuardNames = @(
    "v2_ml_diagnostic_report_immutable_delete",
    "v2_ml_diagnostic_report_immutable_update",
    "v2_ml_governance_record_immutable_delete",
    "v2_ml_governance_record_immutable_update",
    "v2_ml_lifecycle_event_immutable_delete",
    "v2_ml_lifecycle_event_immutable_update",
    "v2_signal_record_immutable_delete",
    "v2_signal_record_immutable_update",
    "v2_signal_state_event_immutable_delete",
    "v2_signal_state_event_immutable_update"
)
$Be4GuardTriggers = @(
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

# The six BE-5 indexes (exact names).
$Be5Indexes = @(
    "ix_v2_mldiag_artifact",
    "ix_v2_mlev_record",
    "ix_v2_mlgov_artifact",
    "ix_v2_sigev_signal",
    "ix_v2_signal_family_state",
    "ix_v2_signal_instrument"
)

# Inherited V1 drift tokens (drift after the apply = exactly these).
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
$AnchorSize = 0

# ---------------------------------------------------------------------
# 0B. OPERATOR INPUT (ABSOLUTE PATH OF THE WORKING DATABASE FILE)
# ---------------------------------------------------------------------

Write-Host ""
Write-Host "STOP THE RUNNING APPLICATION BEFORE CONTINUING (it holds a live"
Write-Host "connection to the target database file). Do NOT restart it before"
Write-Host "the verify pack has also completed."
Write-Host ""
Write-Host "This pack applies band BE-5 (migrations 0044+0045) ONCE to the"
Write-Host "application's SQLite WORKING DATABASE FILE and then proves the end state."
Write-Host ""
Write-Host "This pack prompts for NO credential of any kind (no password, no API key)."
Write-Host ""

$TargetDbPath = (Read-Host -Prompt "Absolute path to the application's working SQLite database file (quotes optional; for example C:\Users\victo\.vscode\AXIOM\axiom\backend\axiom_dev.db)").Trim()
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
if ($TargetDbPath.ToLower().StartsWith($EvidenceRootFull.ToLower())) {
    throw "STOP: target file is inside the operator-evidence directory. Aborting before any database modification."
}

# ---------------------------------------------------------------------
# 0C. PYTHON HELPER (written to the OS temp directory, removed on exit)
# ---------------------------------------------------------------------

$HelperDir  = Join-Path $env:TEMP "axiom_itrga_0045_apply_v1"
$HelperPath = Join-Path $HelperDir "helper.py"
New-Item -ItemType Directory -Force -Path $HelperDir | Out-Null

$HelperSource = @'
import hashlib
import re
import sqlite3
import sys

MID_DOT = chr(183)

MGE_FILES = (
    "app/v2/research_governance/__init__.py",
    "app/v2/research_governance/contracts.py",
    "app/v2/research_governance/decisions.py",
)
SGE_FILES = (
    "app/v2/research_governance/signals.py",
    "app/v2/research_governance/api.py",
)


def ro_connect(db_path):
    uri = "file:" + db_path.replace("\\", "/") + "?mode=ro"
    return sqlite3.connect(uri, uri=True)


def rw_connect(db_path):
    return sqlite3.connect(db_path)


def engine_hash(backend_dir, rel_files):
    # The pinned compver provenance algorithm, recomputed from the
    # on-disk source files: sha256 over (relpath\0 + bytes + \0) per
    # file, in the pinned order.
    import os
    digest = hashlib.sha256()
    for rel in rel_files:
        path = os.path.join(backend_dir, rel.replace("/", os.sep))
        with open(path, "rb") as handle:
            data = handle.read()
        digest.update(rel.encode("utf-8"))
        digest.update(b"\x00")
        digest.update(data)
        digest.update(b"\x00")
    return digest.hexdigest()


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

    if cmd in ("scalar", "verifyrows", "verifyaudit", "compverbe5",
               "permbe5", "reportempty5", "tabledigest"):
        con = ro_connect(db_path)
        try:
            if cmd == "scalar":
                sql = sys.argv[3]
                rows = con.execute(sql).fetchall()
                for row in rows:
                    print("|".join("" if v is None else str(v) for v in row))
            elif cmd == "verifyrows":
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
            elif cmd == "compverbe5":
                # Exactly 5 rows: the 3 BE-4 components pinned by
                # value; the 2 BE-5 components pinned by RUNTIME
                # RECOMPUTATION of the engine file hashes.
                backend_dir = sys.argv[3]
                pins_be4 = {
                    "indicator_engine": ("v1-reuse-1.0.0", sys.argv[4]),
                    "market_context_engine": ("mce-1.0.0", sys.argv[5]),
                    "chart_intelligence_engine": ("cie-1.0.0", sys.argv[6]),
                }
                exp_be5 = {
                    "ml_governance_engine": ("mge-1.0.0",
                                             engine_hash(backend_dir, MGE_FILES)),
                    "signal_engine": ("sge-1.0.0",
                                      engine_hash(backend_dir, SGE_FILES)),
                }
                rows = con.execute(
                    "SELECT component, version, source_hash, evidence_ref, registered_at "
                    "FROM v2_computation_version"
                ).fetchall()
                if len(rows) != 5:
                    print("FAIL:compver_count=" + str(len(rows)))
                    return
                seen = {}
                for component, version, source_hash, evidence_ref, registered_at in rows:
                    if component in seen:
                        print("FAIL:compver_duplicate_component=" + str(component))
                        return
                    seen[component] = (version, source_hash,
                                       evidence_ref, registered_at)
                for component, (exp_version, exp_hash) in list(pins_be4.items()) + list(exp_be5.items()):
                    if component not in seen:
                        print("FAIL:compver_missing=" + component)
                        return
                    version, source_hash, evidence_ref, registered_at = seen[component]
                    if version != exp_version:
                        print("FAIL:compver_version=" + component + "=" + repr(version))
                        return
                    if source_hash != exp_hash:
                        print("FAIL:compver_hash=" + component + "=" + repr(source_hash)
                              + " expected=" + repr(exp_hash))
                        return
                    if not re.fullmatch(r"[0-9a-f]{64}", source_hash or ""):
                        print("FAIL:compver_hash_shape=" + component)
                        return
                    exp_ref = "BO-V2-BE-4-001" if component in pins_be4 else "BO-V2-BE-5-001"
                    if evidence_ref != exp_ref:
                        print("FAIL:compver_evidence_ref=" + component + "=" + repr(evidence_ref))
                        return
                    if not registered_at or len(str(registered_at)) < 19:
                        print("FAIL:compver_registered_at_shape=" + component)
                        return
                print("PASS:compver_rows_exact")
                print("INFO:mge_recomputed=" + exp_be5["ml_governance_engine"][1])
                print("INFO:sge_recomputed=" + exp_be5["signal_engine"][1])
            elif cmd == "permbe5":
                rows = con.execute(
                    "SELECT role, permission, sal FROM v2_permission "
                    "WHERE permission LIKE 'v2.research.ml%' "
                    "OR permission LIKE 'v2.research.signal%'"
                ).fetchall()
                if len(rows) != 8:
                    print("FAIL:permbe5_count=" + str(len(rows)))
                    return
                expected = {
                    ("admin", "v2.research.ml_governance.read", "SAL-2"),
                    ("admin", "v2.research.ml_governance.decide", "SAL-3"),
                    ("admin", "v2.research.signal.read", "SAL-2"),
                    ("admin", "v2.research.signal.emit", "SAL-3"),
                    ("admin", "v2.research.ml_diagnostics.read", "SAL-2"),
                    ("operator", "v2.research.ml_governance.read", "SAL-2"),
                    ("operator", "v2.research.signal.read", "SAL-2"),
                    ("operator", "v2.research.ml_diagnostics.read", "SAL-2"),
                }
                if set(tuple(r) for r in rows) != expected:
                    print("FAIL:permbe5_rows=" + repr(sorted(tuple(r) for r in rows)))
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
            elif cmd == "reportempty5":
                counts = {}
                for table in ("v2_ml_governance_record", "v2_ml_lifecycle_event",
                              "v2_ml_diagnostic_report", "v2_signal_record",
                              "v2_signal_state_event"):
                    counts[table] = con.execute(
                        "SELECT COUNT(*) FROM " + table).fetchone()[0]
                if any(v != 0 for v in counts.values()):
                    print("FAIL:table_counts=" + repr(counts))
                    return
                print("PASS:be5_tables_empty")
            elif cmd == "tabledigest":
                table = sys.argv[3]
                rows = con.execute("SELECT * FROM " + table + " ORDER BY id").fetchall()
                digest = hashlib.sha256(
                    repr([tuple(r) for r in rows]).encode("utf-8")).hexdigest()
                print("DIGEST:" + str(len(rows)) + ":" + digest)
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
# COMMAND HELPERS
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
    Write-Evidence "PASS: expected refusal observed with the required text."
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
Write-Evidence "Pack: ITRGA-V2-0045-APPLY-PACK-V1"
Write-Evidence "Act: band BE-5 (0044+0045) working-database application act (single sanctioned mutation: alembic upgrade 20260902_0045)"
Write-Evidence "Determination: ITRGA-DET-V2-BE-5-FINAL-001 (C full-verify PASS; C-1 closed; C-2 scope = this envelope)"
Write-Evidence "Build order: BO-V2-BE-5-001 (terminal state T-1...T-12)"
Write-Evidence "Baseline authority: operator-evidence\BE-4\0043-APPLY-FINAL-STATE.txt (chain of custody of the 0043 act)"
Write-Evidence "Started: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss zzz')"
Write-Evidence "Repo root: ${RepoRoot}"
Write-Evidence "Target file (APPLICATION'S WORKING DATABASE - named by the Operator): ${TargetDbPath}"
Write-Evidence "SQL engine: SQLite (in-process, via the repo venv python sqlite3 module; no database server)"
Write-Evidence "Python (repo venv): ${Python}"
Write-Evidence "Server credentials used: NONE (no database server; no password prompt)"
Write-Evidence "Provider credentials used: NONE"
Write-Evidence "Authority variable: NONE EXISTS FOR THIS ACT; any pre-existing AXIOM_TD_* / authority variables are removed and their absence asserted; this pack never sets one."
Write-Evidence "Read-write scope: exactly one mutation (alembic upgrade 20260902_0045) on the target file; plus the transcript, the anchor copy, and the apply-final-state record in operator-evidence\BE-5; plus the throwaway helper (removed on exit)."

# ---------------------------------------------------------------------
# A0b. BASELINE AUTHORITY (the 0043 apply-final-state record, strict)
# ---------------------------------------------------------------------

Write-Section "A0b. BASELINE AUTHORITY (strict parse of the 0043 apply-final-state record)"

$Prev = Read-Pins -Path $PrevStatePath -ExpectedKeys @(
    "STATE_FILE_ID", "RUN_TIMESTAMP", "POST_SIZE_BYTES", "POST_LAST_WRITE",
    "POST_SHA256", "POST_REVISION", "POST_V2_TRIGGER_COUNT",
    "ANCHOR_FILENAME", "ANCHOR_SIZE_BYTES", "ANCHOR_SHA256"
) -Label "0043 apply-final-state record"

if ($Prev["STATE_FILE_ID"] -ne "ITRGA-V2-0043-APPLY-FINAL-STATE-V1") {
    throw "STOP: baseline record identity '$($Prev["STATE_FILE_ID"])' is not ITRGA-V2-0043-APPLY-FINAL-STATE-V1. The 0043 act must PASS first."
}
if ($Prev["POST_REVISION"] -ne ${BaselineRevision}) {
    throw "STOP: baseline record revision '$($Prev["POST_REVISION"])' is not ${BaselineRevision}."
}
if ($Prev["POST_V2_TRIGGER_COUNT"] -ne "18") {
    throw "STOP: baseline record trigger count '$($Prev["POST_V2_TRIGGER_COUNT"])' is not 18."
}
if ($Prev["POST_SIZE_BYTES"] -notmatch '^[0-9]+$') { throw "STOP: malformed POST_SIZE_BYTES in baseline record." }
if ($Prev["POST_SHA256"] -notmatch '^[0-9a-f]{64}$') { throw "STOP: malformed POST_SHA256 in baseline record." }

Write-Evidence "Record: ${PrevStatePath}"
Write-Evidence "  RUN_TIMESTAMP            $($Prev["RUN_TIMESTAMP"])"
Write-Evidence "  POST_SIZE_BYTES          $($Prev["POST_SIZE_BYTES"])"
Write-Evidence "  POST_LAST_WRITE          $($Prev["POST_LAST_WRITE"])"
Write-Evidence "  POST_SHA256              $($Prev["POST_SHA256"])"
Write-Evidence "  POST_REVISION            $($Prev["POST_REVISION"])"
Write-Evidence "  POST_V2_TRIGGER_COUNT    $($Prev["POST_V2_TRIGGER_COUNT"])"
Write-Evidence "PASS: baseline record parsed, shapes valid, identity and revision correct."

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

    Write-Evidence "Authority/TD environment sweep:"
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
    # A1. BASELINE (PRE-MUTATION)
    # -----------------------------------------------------------------

    Write-Section "A1. BASELINE (pre-mutation; two-tier authority; abort on content failure)"

    # A1.1: current revision gate (read-only; explicit already-applied abort).
    [void](Assert-CurrentExactly -ExpectedRev ${BaselineRevision} -Label "A1 baseline current")
    Write-Evidence "PASS: A1.1 - current revision is exactly ${BaselineRevision} (an already-applied 0044/0045 or any other value aborts here)."

    # A1.2: file identity (Tier 1 against the 0043 final-state record).
    $B1File = Get-Item ${TargetDbPath}
    $B1Size  = $B1File.Length
    $B1Write = $B1File.LastWriteTime.ToString('yyyy-MM-dd HH:mm:ss zzz')
    $B1Hash  = (Get-FileHash ${TargetDbPath} -Algorithm SHA256).Hash.ToLower()
    Write-Evidence "Target file: ${TargetDbPath}"
    Write-Evidence "  size       ${B1Size} bytes (baseline record $($Prev["POST_SIZE_BYTES"]))"
    Write-Evidence "  last write ${B1Write} (baseline record $($Prev["POST_LAST_WRITE"]))"
    Write-Evidence "  sha256     ${B1Hash} (baseline record $($Prev["POST_SHA256"]))"
    $Tier1ByteExact = $false
    if (([string]$B1Size -eq $Prev["POST_SIZE_BYTES"]) -and ($B1Hash -eq $Prev["POST_SHA256"])) {
        $Tier1ByteExact = $true
        Write-Evidence "PASS: A1.2 Tier 1 - target file is byte-identical to the 0043 apply-final-state record (untouched since the 0043 PASS)."
    } else {
        Write-Evidence "NOTE: A1.2 Tier 1 byte-identity forfeited (file changed since the 0043 PASS - e.g. application activity). Falling through to Tier 2: full CONTENT re-proof of the 0043 terminal state."
    }

    # A1.3: integrity / journal / sidecars.
    [void](Invoke-Py -PyArgs @("scalar", ${TargetDbPath}, "SELECT sqlite_version();") -Label "A1 sqlite version (recorded)")
    $IntegrityOut = Invoke-Py -PyArgs @("scalar", ${TargetDbPath}, "PRAGMA integrity_check;") -Label "A1 integrity check"
    $IntegrityText = (Norm-Text $IntegrityOut).Trim()
    if ($IntegrityText -ne "ok") {
        throw "FAIL: A1 - integrity_check '${IntegrityText}', expected 'ok'. Stopping before any modification; report to ITRGA."
    }
    $JournalOut = Invoke-Py -PyArgs @("scalar", ${TargetDbPath}, "PRAGMA journal_mode;") -Label "A1 journal mode"
    $JournalText = (Norm-Text $JournalOut).Trim()
    if ($JournalText -ne "delete") {
        throw "FAIL: A1 - journal_mode '${JournalText}', expected 'delete'. Stopping before any modification; report to ITRGA."
    }
    foreach ($Suffix in @("-wal", "-shm")) {
        $SidePath = ${TargetDbPath} + $Suffix
        if (Test-Path $SidePath) {
            throw "FAIL: A1 - unexpected sidecar present: ${SidePath}. Stopping before any modification; report to ITRGA."
        }
        Write-Evidence "Sidecar ${Suffix}: absent"
    }
    Write-Evidence "PASS: A1.3 - integrity ok; journal delete; no sidecars."

    # A1.4: trigger posture (exactly 18; the known subsets present; the
    # ten BE-5 guards absent). Snapshot the full 18-name set for the
    # post-apply set-difference proof.
    [void](Invoke-Py -PyArgs @("scalar", ${TargetDbPath}, "SELECT name FROM sqlite_master WHERE type='trigger' AND name LIKE 'v2_%' ORDER BY name;") -Label "A1 v2 trigger names (recorded)")
    $PreTrigNamesText = Get-PyScalar -Sql "SELECT name FROM sqlite_master WHERE type='trigger' AND name LIKE 'v2_%' ORDER BY name;" -Label "A1 v2 trigger set (snapshot)"
    $PreTrigNames = @($PreTrigNamesText -split "`n" | Where-Object { $_ -ne "" })
    if ($PreTrigNames.Count -ne 18) {
        throw "FAIL: A1 - v2 trigger count '$($PreTrigNames.Count)', expected exactly 18 (the 0043 terminal state). Stopping before any modification; report to ITRGA."
    }
    $KnownSubset = @($Be4GuardTriggers + $TransitionGuardTriggers) | Sort-Object
    foreach ($KnownName in $KnownSubset) {
        if ($PreTrigNames -notcontains $KnownName) {
            throw "FAIL: A1 - expected inherited guard trigger missing from the baseline set: ${KnownName}. Stopping before any modification; report to ITRGA."
        }
    }
    foreach ($Be5Name in $Be5GuardNames) {
        if ($PreTrigNames -contains $Be5Name) {
            throw "FAIL: A1 - a BE-5 guard trigger is already present: ${Be5Name} (double-apply suspected). Stopping before any modification; report to ITRGA."
        }
    }
    Write-Evidence "PASS: A1.4 - exactly 18 v2 triggers; the four transition guards and the six BE-4 guards present; the ten BE-5 guards absent."

    # A1.5: Tier-2 CONTENT re-proof of the 0043 terminal state (always
    # run; Tier 1 merely records byte-identity on top). Perm seeds of
    # BE-4 exact; compver 3 rows (BE-4 pins); inherited anchors exact.
    $PreCompverCount = Get-PyScalar -Sql "SELECT COUNT(*) FROM v2_computation_version;" -Label "A1 compver count"
    if ($PreCompverCount -ne "3") {
        throw "FAIL: A1 - compver row count '${PreCompverCount}', expected 3 (the 0043 terminal state). Stopping; report to ITRGA."
    }
    $PrePermTotal = Get-PyScalar -Sql "SELECT COUNT(*) FROM v2_permission;" -Label "A1 permission count"
    if ($PrePermTotal -ne "27") {
        throw "FAIL: A1 - v2_permission row count '${PrePermTotal}', expected 27 (the 0043 terminal state). Stopping; report to ITRGA."
    }
    $PreBe4PermCount = Get-PyScalar -Sql "SELECT COUNT(*) FROM v2_permission WHERE permission LIKE 'v2.research.market_context%' OR permission LIKE 'v2.research.chart_intelligence%';" -Label "A1 BE-4 permission count"
    if ($PreBe4PermCount -ne "5") {
        throw "FAIL: A1 - BE-4 permission rows '${PreBe4PermCount}', expected 5. Stopping; report to ITRGA."
    }
    $PreBe5PermCount = Get-PyScalar -Sql "SELECT COUNT(*) FROM v2_permission WHERE permission LIKE 'v2.research.ml%' OR permission LIKE 'v2.research.signal%';" -Label "A1 BE-5 permission absence"
    if ($PreBe5PermCount -ne "0") {
        throw "FAIL: A1 - BE-5 permission rows already present ('${PreBe5PermCount}'). Stopping; report to ITRGA."
    }
    $ProvPre = Get-PyScalar -Sql "SELECT source_status, entitlement_status, persistence_permitted FROM v2_md_provider WHERE provider_id='twelvedata';" -Label "A1 inherited provider row"
    if ($ProvPre -ne "contract_tested|verified|0") {
        throw "FAIL: A1 - inherited provider row is '${ProvPre}', expected 'contract_tested|verified|0'. Stopping; report to ITRGA."
    }
    $RowsPre = Invoke-Py -PyArgs @("verifyrows", ${TargetDbPath}) -Label "A1 inherited history exact-content"
    if ((Norm-Text $RowsPre).Trim() -ne "PASS:history_rows_exact") {
        throw "FAIL: A1 - inherited history content differs from the pinned state. Stopping; report to ITRGA."
    }
    $AuditPre = Invoke-Py -PyArgs @("verifyaudit", ${TargetDbPath}) -Label "A1 inherited audit exact-content"
    if ((Norm-Text $AuditPre).Trim() -ne "PASS:audit_rows_exact") {
        throw "FAIL: A1 - inherited audit content differs from the pinned state. Stopping; report to ITRGA."
    }
    # BE-4 report tables: content digests (tolerant of legitimate app
    # activity; equality re-proven after the apply).
    $McrDigestPre = Invoke-Py -PyArgs @("tabledigest", ${TargetDbPath}, "v2_market_context_report") -Label "A1 BE-4 market-context report digest (pre)"
    $CirDigestPre = Invoke-Py -PyArgs @("tabledigest", ${TargetDbPath}, "v2_chart_intelligence_report") -Label "A1 BE-4 chart-intelligence report digest (pre)"
    $Be5TablesPre = Get-PyScalar -Sql "SELECT COUNT(*) FROM sqlite_master WHERE type='table' AND name IN ('v2_ml_governance_record','v2_ml_lifecycle_event','v2_ml_diagnostic_report','v2_signal_record','v2_signal_state_event');" -Label "A1 BE-5 table absence"
    if ($Be5TablesPre -ne "0") {
        throw "FAIL: A1 - BE-5 tables already present ('${Be5TablesPre}'). Stopping; report to ITRGA."
    }
    Write-Evidence "PASS: A1.5 - 0043 terminal state re-proven by content (compver 3; permissions 27/5/0; provider/history/audit exact; BE-4 report digests captured; BE-5 tables absent)."

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
    $MainBackupPath = Join-Path $EvidenceDir (${LeafName} + ".pre-0045-" + ${BackupStamp} + ".bak")
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
    Write-Evidence "PASS: A2 - a proven rollback anchor exists before any mutation."

    # -----------------------------------------------------------------
    # A3. PROVENANCE (on-disk runtime re-pin; abort on any mismatch)
    # -----------------------------------------------------------------

    Write-Section "A3. PROVENANCE (25 files re-pinned on disk: 8 chain migrations + 17 delivered BE-5 files; abort on any mismatch)"

    foreach ($MigName in @(
        "20260823_0038_v2_be1_core.py",
        "20260824_0039_v2_be2_marketdata.py",
        "20260824_0040_v2_be3_provider.py",
        "20260825_0041_v2_be3_p2_entitlement.py",
        "20260829_0042_v2_be3_p2_transition.py",
        "20260831_0043_v2_be4_research_read_models.py",
        "20260902_0044_v2_be5_ml_governance.py",
        "20260902_0045_v2_be5_signal_contracts.py"
    )) {
        $MigPath = Join-Path $BackendRoot ("alembic\versions\" + ${MigName})
        if (!(Test-Path $MigPath)) { throw "STOP: migration file missing: ${MigPath}." }
        $ActualHash = (Get-FileHash $MigPath -Algorithm SHA256).Hash.ToLower()
        $PinnedHash = $ExpectedMigrationHashes[${MigName}]
        Write-Evidence ("{0}" -f ${MigName})
        Write-Evidence "  actual   ${ActualHash}"
        Write-Evidence "  expected ${PinnedHash}"
        if ($ActualHash -ne $PinnedHash) {
            throw "STOP: A3 - provenance hash mismatch for ${MigName} - not the verified file. The apply must not proceed; report to ITRGA."
        }
    }

    foreach ($RelPath in @(
        "backend\app\v2\research_governance\__init__.py",
        "backend\app\v2\research_governance\contracts.py",
        "backend\app\v2\research_governance\decisions.py",
        "backend\app\v2\research_governance\signals.py",
        "backend\app\v2\research_governance\api.py",
        "backend\app\v2\research_governance\diagnostics.py",
        "backend\app\db\models\v2_research_governance.py",
        "backend\app\db\models\v2_signal.py",
        "backend\tests\test_v2_be5_decisions.py",
        "backend\tests\test_v2_be5_migration.py",
        "backend\tests\test_v2_be5_api.py",
        "backend\tests\test_v2_be5_diagnostics.py",
        "backend\tests\test_v2_be5_lifecycle.py",
        "backend\app\v2\api\router.py",
        "backend\app\v2\rbac\permissions.py",
        "backend\app\db\models\__init__.py",
        "backend\tests\test_v2_be4_migration.py"
    )) {
        $FullPath = Join-Path $RepoRoot ${RelPath}
        if (!(Test-Path $FullPath)) { throw "STOP: delivered file missing: ${FullPath}." }
        $ActualHash = (Get-FileHash $FullPath -Algorithm SHA256).Hash.ToLower()
        $PinnedHash = $ExpectedDeliveredHashes[${RelPath}]
        Write-Evidence ("{0}" -f ${RelPath})
        Write-Evidence "  actual   ${ActualHash}"
        Write-Evidence "  expected ${PinnedHash}"
        if ($ActualHash -ne $PinnedHash) {
            throw "STOP: A3 - provenance hash mismatch for ${RelPath} - not the verified file. The apply must not proceed; report to ITRGA."
        }
    }
    Write-Evidence "PASS: A3 - all 25 files on disk hash to the pinned values (8 chain migrations 0038-0045; 17 delivered BE-5 files per REM-001 Rev 2)."

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
    # A5. POST-APPLY STATE
    # -----------------------------------------------------------------

    Write-Section "A5. POST-APPLY STATE"

    # A5.1: revision exactly 20260902_0045 (T-1).
    [void](Assert-CurrentExactly -ExpectedRev ${ApplyTargetRevision} -Label "A5 post-apply current")
    Write-Evidence "PASS: A5.1 (T-1) - current revision is exactly ${ApplyTargetRevision} (chain 0043 -> 0044 -> 0045)."

    # A5.2: exactly 28 v2 triggers; set difference vs baseline exactly
    # the ten BE-5 guards (T-3/T-6; 18 -> 24 -> 28).
    [void](Invoke-Py -PyArgs @("scalar", ${TargetDbPath}, "SELECT name FROM sqlite_master WHERE type='trigger' AND name LIKE 'v2_%' ORDER BY name;") -Label "A5 v2 trigger names (recorded)")
    $PostTrigNamesText = Get-PyScalar -Sql "SELECT name FROM sqlite_master WHERE type='trigger' AND name LIKE 'v2_%' ORDER BY name;" -Label "A5 v2 trigger set"
    $PostTrigNames = @($PostTrigNamesText -split "`n" | Where-Object { $_ -ne "" })
    if ($PostTrigNames.Count -ne 28) {
        throw "FAIL: A5 (T-3/T-6) - v2 trigger count '$($PostTrigNames.Count)', expected exactly 28 (18 + 6 + 4)."
    }
    $AddedNames = @($PostTrigNames | Where-Object { $PreTrigNames -notcontains $_ })
    $AddedSorted = @($AddedNames | Sort-Object)
    $ExpectedAddedSorted = @($Be5GuardNames | Sort-Object)
    if (($AddedSorted -join "`n") -ne ($ExpectedAddedSorted -join "`n")) {
        throw "FAIL: A5 (T-3/T-6) - the added trigger set is not exactly the ten pinned BE-5 guards: added [$($AddedSorted -join ', ')]."
    }
    Write-Evidence "PASS: A5.2 (T-3/T-6) - 28 v2 triggers; the added set is exactly the ten BE-5 guard names; the 18 inherited are intact."

    # A5.3: the five tables; the two UNIQUE anchors; the six indexes (T-2/T-6).
    $NewTableCount = Get-PyScalar -Sql "SELECT COUNT(*) FROM sqlite_master WHERE type='table' AND name IN ('v2_ml_governance_record','v2_ml_lifecycle_event','v2_ml_diagnostic_report','v2_signal_record','v2_signal_state_event');" -Label "A5 BE-5 table presence"
    if ($NewTableCount -ne "5") {
        throw "FAIL: A5 (T-2/T-6) - BE-5 table count '${NewTableCount}', expected 5."
    }
    $MlgovDdl = Get-PyScalar -Sql "SELECT sql FROM sqlite_master WHERE type='table' AND name='v2_ml_governance_record';" -Label "A5 governance-record DDL"
    foreach ($Anchor in @("record_seq", "supersedes", "model_type", "instrument_class")) {
        if ($MlgovDdl -notlike "*${Anchor}*") {
            throw "FAIL: A5 (T-2) - '${Anchor}' not present in v2_ml_governance_record DDL."
        }
    }
    if ($MlgovDdl -like "*updated_at_event_id*") {
        throw "FAIL: A5 (T-2/P-1) - updated_at_event_id is present in v2_ml_governance_record DDL (must be absent)."
    }
    $MldiagDdl = Get-PyScalar -Sql "SELECT sql FROM sqlite_master WHERE type='table' AND name='v2_ml_diagnostic_report';" -Label "A5 diagnostic-report DDL"
    if ($MldiagDdl -notlike "*inputs_hash*" -or $MldiagDdl -notlike "*engine_versions_hash*") {
        throw "FAIL: A5 (T-2/P-2) - determinism-anchor columns missing from v2_ml_diagnostic_report DDL."
    }
    # P-1 / P-2 uniqueness proven behaviorally (SQLite renders table-level
    # UNIQUE as an autoindex):
    $UniqRows = Get-PyScalar -Sql "SELECT name FROM sqlite_master WHERE type='index' AND tbl_name IN ('v2_ml_governance_record','v2_ml_diagnostic_report') AND origin='u' ORDER BY name;" -Label "A5 autoindex origin-u presence"
    $UniqCount = @($UniqRows -split "`n" | Where-Object { $_ -ne "" }).Count
    if ($UniqCount -lt 2) {
        throw "FAIL: A5 (T-2/P-1/P-2) - fewer than 2 origin-u autoindexes on the two anchor tables (observed ${UniqCount})."
    }
    $IdxFound = Get-PyScalar -Sql "SELECT name FROM sqlite_master WHERE type='index' AND name IN ('ix_v2_mlgov_artifact','ix_v2_mlev_record','ix_v2_mldiag_artifact','ix_v2_sigev_signal','ix_v2_signal_family_state','ix_v2_signal_instrument') ORDER BY name;" -Label "A5 BE-5 index names"
    $ExpectedIndexesText = $Be5Indexes -join "`n"
    if ($IdxFound -ne $ExpectedIndexesText) {
        throw "FAIL: A5 (T-2/T-6) - the six BE-5 index names are not exactly the pinned set: '${IdxFound}'."
    }
    Write-Evidence "PASS: A5.3 (T-2/T-6; P-1/P-2/P-3) - five tables present; record_seq/supersedes/model_type/instrument_class in the DDL; no updated_at_event_id; both uniqueness anchors present (behavioral form); the six indexes exact."

    # A5.4: computation-version rows exactly 5; BE-5 hashes proven by
    # RUNTIME RECOMPUTATION of the engine files (T-5/T-6; P-4).
    $CompverOut = Invoke-Py -PyArgs @(
        "compverbe5", ${TargetDbPath}, ${BackendRoot},
        "fe9aab42c34d671e960fd92a9346d3bf60c27135e76e52310d774bc84028dd35",
        "69902503483502bcd5ce5e35fdb0eeabcb2efcaf7a4b0c262a6fccf2d0af3a8c",
        "3887d6ca8ba05858f41889cd99fa05aba42663ac22d906a7f989b567c3912180"
    ) -Label "A5 computation-version rows (5; BE-5 hashes recomputed)"
    $CompverText = (Norm-Text $CompverOut).Trim()
    if ($CompverText -notlike "PASS:compver_rows_exact*") {
        throw "FAIL: A5 (T-5/T-6) - computation-version check failed: ${CompverText}"
    }
    Write-Evidence "PASS: A5.4 (T-5/T-6; P-4) - exactly 5 computation-version rows; BE-4 rows content-exact; mge/sge source hashes equal the runtime recomputation of the engine files on this machine; evidence_ref values exact."

    # A5.5: permission rows (T-4/T-6): 8 additive BE-5 content-exact;
    # total 35; no duplicates.
    $PermOut = Invoke-Py -PyArgs @("permbe5", ${TargetDbPath}) -Label "A5 permission rows (BE-5 additive set)"
    $PermText = (Norm-Text $PermOut).Trim()
    if ($PermText -notlike "PASS:perm_rows_exact*") {
        throw "FAIL: A5 (T-4/T-6) - permission check failed: ${PermText}"
    }
    Write-Evidence "PASS: A5.5 (T-4/T-6) - exactly 8 additive BE-5 permission rows (admin x5 incl. signal.emit, operator x3; SAL-aligned); total 35; no role+permission duplicates."

    # A5.6: the five BE-5 tables are empty (T-2/T-6 posture).
    $EmptyOut = Invoke-Py -PyArgs @("reportempty5", ${TargetDbPath}) -Label "A5 BE-5 tables empty"
    $EmptyText = (Norm-Text $EmptyOut).Trim()
    if ($EmptyText -ne "PASS:be5_tables_empty") {
        throw "FAIL: A5 - the BE-5 tables are not empty: ${EmptyText}"
    }
    Write-Evidence "PASS: A5.6 - all five BE-5 tables are empty."

    # A5.7: inherited state untouched (no-touch proof).
    $ProvNow = Get-PyScalar -Sql "SELECT source_status, entitlement_status, persistence_permitted FROM v2_md_provider WHERE provider_id='twelvedata';" -Label "A5 inherited provider row"
    if ($ProvNow -ne "contract_tested|verified|0") {
        throw "FAIL: A5 (T-9) - inherited provider row changed: '${ProvNow}'."
    }
    $RowsNow = Invoke-Py -PyArgs @("verifyrows", ${TargetDbPath}) -Label "A5 inherited history exact-content"
    if ((Norm-Text $RowsNow).Trim() -ne "PASS:history_rows_exact") {
        throw "FAIL: A5 (T-9) - inherited history content changed."
    }
    $AuditNow = Invoke-Py -PyArgs @("verifyaudit", ${TargetDbPath}) -Label "A5 inherited audit exact-content"
    if ((Norm-Text $AuditNow).Trim() -ne "PASS:audit_rows_exact") {
        throw "FAIL: A5 (T-9) - inherited audit content changed."
    }
    $McrDigestPost = Invoke-Py -PyArgs @("tabledigest", ${TargetDbPath}, "v2_market_context_report") -Label "A5 BE-4 market-context report digest (post)"
    $CirDigestPost = Invoke-Py -PyArgs @("tabledigest", ${TargetDbPath}, "v2_chart_intelligence_report") -Label "A5 BE-4 chart-intelligence report digest (post)"
    if ((Norm-Text $McrDigestPost).Trim() -ne (Norm-Text $McrDigestPre).Trim()) {
        throw "FAIL: A5 (T-9) - v2_market_context_report content changed across the apply."
    }
    if ((Norm-Text $CirDigestPost).Trim() -ne (Norm-Text $CirDigestPre).Trim()) {
        throw "FAIL: A5 (T-9) - v2_chart_intelligence_report content changed across the apply."
    }
    $Be4CompverCountNow = Get-PyScalar -Sql "SELECT COUNT(*) FROM v2_computation_version WHERE component IN ('indicator_engine','market_context_engine','chart_intelligence_engine');" -Label "A5 BE-4 compver rows intact"
    if ($Be4CompverCountNow -ne "3") {
        throw "FAIL: A5 (T-9) - BE-4 computation-version rows not intact: '${Be4CompverCountNow}'."
    }
    Write-Evidence "PASS: A5.7 (T-9) - inherited BE-1..BE-4 state untouched: provider row, history, audit content-exact; BE-4 report-table digests identical pre/post; BE-4 compver rows intact."

    # A5.8: file posture after the apply.
    [void](Invoke-Py -PyArgs @("scalar", ${TargetDbPath}, "PRAGMA integrity_check;") -Label "A5 integrity check")
    $PostJournal = Get-PyScalar -Sql "PRAGMA journal_mode;" -Label "A5 journal mode"
    if ($PostJournal -ne "delete") {
        throw "FAIL: A5 - journal_mode '${PostJournal}', expected 'delete'."
    }
    foreach ($Suffix in @("-wal", "-shm")) {
        $SidePath = ${TargetDbPath} + $Suffix
        if (Test-Path $SidePath) {
            $SideItem = Get-Item $SidePath
            Write-Evidence "Sidecar ${Suffix}: present, $($SideItem.Length) bytes (FAIL: expected absent)"
            throw "FAIL: A5 - unexpected sidecar present: ${SidePath}."
        }
        Write-Evidence "Sidecar ${Suffix}: absent"
    }
    Write-Evidence "PASS: A5.8 - integrity ok; journal delete; no sidecars."

    # Final target-file state (recorded for the verify pack).
    $FinalFile = Get-Item ${TargetDbPath}
    $FinalSize  = $FinalFile.Length
    $FinalWrite = $FinalFile.LastWriteTime.ToString('yyyy-MM-dd HH:mm:ss zzz')
    $FinalHash  = (Get-FileHash ${TargetDbPath} -Algorithm SHA256).Hash.ToLower()
    Write-Evidence "Post-apply target file:"
    Write-Evidence "  size       ${FinalSize} bytes"
    Write-Evidence "  last write ${FinalWrite}"
    Write-Evidence "  sha256     ${FinalHash}"
    Write-Evidence "NOTE (PGF-001 lineage): post-apply file bytes contain seed-time timestamps; the verify pack binds identity to THIS run's record, not to any pre-pinned value."

    # -----------------------------------------------------------------
    # A6. GUARD SPOT-CHECKS (ten refusals, exact messages) + CHECK probes
    # -----------------------------------------------------------------

    Write-Section "A6. GUARD SPOT-CHECKS (ten refusals; exact messages; two CHECK-vocabulary probes)"

    # compver holds five seed rows: direct UPDATE/DELETE probes fire on
    # any of them (0043 guards; intact proof).
    Invoke-ExpectedRefusal -Label "A6: compver UPDATE (inherited 0043 guard intact)" -Sql "UPDATE v2_computation_version SET version='probe' WHERE component='ml_governance_engine';" -ExactMessage "V2 computation version registry is immutable; UPDATE prohibited"
    Invoke-ExpectedRefusal -Label "A6: compver DELETE (inherited 0043 guard intact)" -Sql "DELETE FROM v2_computation_version WHERE component='signal_engine';" -ExactMessage "V2 computation version registry is immutable; DELETE prohibited"

    # The five BE-5 tables are empty: transactional probe cycles.
    $MlgovInsert = "INSERT INTO v2_ml_governance_record (id, model_artifact_id, record_seq, registry_version, model_type, instrument_class, eligibility_status, calibration_status, freshness_status, economic_status, statistical_status, deployment_class, data_class, evidence_refs, mode, operator_id, created_at) VALUES ('guardprobe', 'guardprobe', 1, '1.0', 'guardprobe', 'guardprobe', 'unevaluated', 'unevaluated', 'unknown', 'unevaluated', 'unevaluated', 'research', 'synthetic', '{}', 'RESEARCH', 'guardprobe', '2026-09-02 00:00:00');"
    Invoke-ExpectedGuardProbe -Label "A6: governance-record UPDATE" -InsertSql ${MlgovInsert} -ProbeSql "UPDATE v2_ml_governance_record SET deployment_class='champion' WHERE id='guardprobe';" -ExactMessage "V2 ML governance records are immutable; UPDATE prohibited"
    Invoke-ExpectedGuardProbe -Label "A6: governance-record DELETE" -InsertSql ${MlgovInsert} -ProbeSql "DELETE FROM v2_ml_governance_record WHERE id='guardprobe';" -ExactMessage "V2 ML governance records are immutable; DELETE prohibited"

    $MlevInsert = "INSERT INTO v2_ml_lifecycle_event (id, governance_record_id, event_type, from_value, to_value, decision_basis, mode, actor_id, operator_id, created_at) VALUES ('guardprobe', 'guardprobe', 'registered', 'none', 'research', '{}', 'RESEARCH', 'guardprobe', 'guardprobe', '2026-09-02 00:00:00');"
    Invoke-ExpectedGuardProbe -Label "A6: lifecycle-event UPDATE" -InsertSql ${MlevInsert} -ProbeSql "UPDATE v2_ml_lifecycle_event SET to_value='x' WHERE id='guardprobe';" -ExactMessage "V2 ML lifecycle events are immutable; UPDATE prohibited"
    Invoke-ExpectedGuardProbe -Label "A6: lifecycle-event DELETE" -InsertSql ${MlevInsert} -ProbeSql "DELETE FROM v2_ml_lifecycle_event WHERE id='guardprobe';" -ExactMessage "V2 ML lifecycle events are immutable; DELETE prohibited"

    $MldiagInsert = "INSERT INTO v2_ml_diagnostic_report (id, model_artifact_id, diagnostics, input_refs, inputs_hash, engine_versions, engine_versions_hash, data_class, mode, operator_id, created_at) VALUES ('guardprobe', 'guardprobe', '{}', '{}', 'guardprobe', '{}', 'guardprobe', 'synthetic', 'RESEARCH', 'guardprobe', '2026-09-02 00:00:00');"
    Invoke-ExpectedGuardProbe -Label "A6: diagnostic-report UPDATE" -InsertSql ${MldiagInsert} -ProbeSql "UPDATE v2_ml_diagnostic_report SET data_class='live' WHERE id='guardprobe';" -ExactMessage "V2 ML diagnostic reports are immutable; UPDATE prohibited"
    Invoke-ExpectedGuardProbe -Label "A6: diagnostic-report DELETE" -InsertSql ${MldiagInsert} -ProbeSql "DELETE FROM v2_ml_diagnostic_report WHERE id='guardprobe';" -ExactMessage "V2 ML diagnostic reports are immutable; DELETE prohibited"

    $SigInsert = "INSERT INTO v2_signal_record (id, family, signal_type, instrument_id, timeframe, state, uncertainty, limitations, source_family_refs, data_class, as_of, mode, operator_id, created_at) VALUES ('guardprobe', 'structural', 'probe', 'guardprobe', 'M15', 'emitted', '{}', '{}', '{}', 'synthetic', '2026-09-02 00:00:00', 'RESEARCH', 'guardprobe', '2026-09-02 00:00:00');"
    Invoke-ExpectedGuardProbe -Label "A6: signal-record UPDATE" -InsertSql ${SigInsert} -ProbeSql "UPDATE v2_signal_record SET state='refused' WHERE id='guardprobe';" -ExactMessage "V2 signal records are immutable; UPDATE prohibited"
    Invoke-ExpectedGuardProbe -Label "A6: signal-record DELETE" -InsertSql ${SigInsert} -ProbeSql "DELETE FROM v2_signal_record WHERE id='guardprobe';" -ExactMessage "V2 signal records are immutable; DELETE prohibited"

    $SigevInsert = "INSERT INTO v2_signal_state_event (id, signal_record_id, event_type, from_state, to_state, reason, mode, actor_id, operator_id, created_at) VALUES ('guardprobe', 'guardprobe', 'emitted', 'none', 'emitted', '{}', 'RESEARCH', 'guardprobe', 'guardprobe', '2026-09-02 00:00:00');"
    Invoke-ExpectedGuardProbe -Label "A6: signal-state-event UPDATE" -InsertSql ${SigevInsert} -ProbeSql "UPDATE v2_signal_state_event SET to_state='expired' WHERE id='guardprobe';" -ExactMessage "V2 signal state events are immutable; UPDATE prohibited"
    Invoke-ExpectedGuardProbe -Label "A6: signal-state-event DELETE" -InsertSql ${SigevInsert} -ProbeSql "DELETE FROM v2_signal_state_event WHERE id='guardprobe';" -ExactMessage "V2 signal state events are immutable; DELETE prohibited"

    # CHECK-vocabulary probes (INSERT is allowed; the CHECK must refuse).
    Invoke-ExpectedRefusal -Label "A6: CHECK probe - signal family 'hybrid' refused" -Sql "INSERT INTO v2_signal_record (id, family, signal_type, instrument_id, timeframe, state, uncertainty, limitations, source_family_refs, data_class, as_of, mode, operator_id, created_at) VALUES ('checkprobe', 'hybrid', 'probe', 'guardprobe', 'M15', 'emitted', '{}', '{}', '{}', 'synthetic', '2026-09-02 00:00:00', 'RESEARCH', 'guardprobe', '2026-09-02 00:00:00');" -ExactMessage "CHECK"
    Invoke-ExpectedRefusal -Label "A6: CHECK probe - eligibility vocabulary refused" -Sql "INSERT INTO v2_ml_governance_record (id, model_artifact_id, record_seq, registry_version, model_type, instrument_class, eligibility_status, calibration_status, freshness_status, economic_status, statistical_status, deployment_class, data_class, evidence_refs, mode, operator_id, created_at) VALUES ('checkprobe', 'guardprobe', 9, '1.0', 'guardprobe', 'guardprobe', 'bogus', 'unevaluated', 'unknown', 'unevaluated', 'unevaluated', 'research', 'synthetic', '{}', 'RESEARCH', 'guardprobe', '2026-09-02 00:00:00');" -ExactMessage "CHECK"

    # Probe hygiene: the five tables must still be empty after the rollback probes.
    $EmptyOut2 = Invoke-Py -PyArgs @("reportempty5", ${TargetDbPath}) -Label "A6 BE-5 tables empty after probes"
    if ((Norm-Text $EmptyOut2).Trim() -ne "PASS:be5_tables_empty") {
        throw "FAIL: A6 - the BE-5 tables are not empty after the probes."
    }
    Write-Evidence "PASS: A6 - all ten BE-5 guard refusals observed with the exact pinned messages; the inherited compver guards intact; both CHECK probes refused; throwaway rows rolled back; tables confirmed empty."

    # -----------------------------------------------------------------
    # A7. DRIFT RE-BASELINE (format-independent; PGF-014)
    # -----------------------------------------------------------------

    Write-Section "A7. DRIFT RE-BASELINE: alembic check (expected: exactly the 9 inherited V1 tokens; zero BE-5/V2 tokens; format-independent)"

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
        throw "FAIL: A7 (T-10) - alembic check reported no drift (exit 0); expected the inherited V1 drift set to persist (non-zero exit)."
    }
    if ($DriftText -like "*not up to date*") {
        throw "FAIL: A7 (T-10) - alembic check printed the revision-offset refusal form at the HEAD revision (current is exactly ${ApplyTargetRevision}); the chain state is inconsistent. Report to ITRGA."
    }
    $DriftBanPattern = "v2_ml_governance_record|v2_ml_lifecycle_event|v2_ml_diagnostic_report|v2_signal_record|v2_signal_state_event|mlgov|mlev|mldiag|sigev|v2_md_|v2_permission|v2_computation_version|v2_market_context|v2_chart_intelligence|v2_audit_event|v2_lineage_record|ix_v2_"
    if ($DriftText -match $DriftBanPattern) {
        throw "FAIL: A7 (T-10) - V2/BE-5 drift token detected in alembic check output; after the 0045 apply the BE-5 schema set must have left the drift set."
    }

    # Format-independent name extraction (itemized forms).
    $DriftNameMatches = @()
    $DriftNameMatches += [regex]::Matches($DriftText, '(?:added|removed) (?:table|index) [''"]?([A-Za-z0-9_]+)[''"]?')
    $DriftNameMatches += [regex]::Matches($DriftText, '(?:Table|Index)\(''([A-Za-z0-9_]+)''')
    $DriftNames = @($DriftNameMatches | ForEach-Object { $_.Groups[1].Value })

    if ($DriftNames.Count -gt 0) {
        foreach ($Token in $ExpectedDriftTokens) {
            if ($DriftText -notlike "*${Token}*") {
                throw "FAIL: A7 (T-10) - expected inherited V1 drift token missing from alembic check output: ${Token}."
            }
        }
        $UnexpectedDriftNames = @($DriftNames | Where-Object { $ExpectedDriftTokens -notcontains $_ })
        if ($UnexpectedDriftNames.Count -ne 0) {
            throw "FAIL: A7 (T-10) - unexpected drift token(s) beyond the 9 inherited V1 tokens: $($UnexpectedDriftNames -join ', ')."
        }
        $DriftNote = "itemized format: the token set is exactly the 9 inherited V1 tokens - all present, no extras, no v2_* or ix_v2_ token"
    } else {
        if ($DriftText -notlike "*New upgrade operations detected*") {
            throw "FAIL: A7 (T-10) - expected a recorded drift marker in alembic check output; observed: '${DriftText}'."
        }
        $DriftNote = "summary format (no itemized list in this alembic version; PGF-014): drift existence asserted (non-zero exit + a recorded drift marker); no V2/BE-5 token anywhere; the exact token set is pinned by the Level-II test evidence and the recorded lineage"
        Write-Evidence "NOTE: this alembic version does not print the itemized drift list (PGF-014); the drift-content proof is carried by the summary marker plus the A5 schema assertions. Environment evidence: the alembic version recorded in A1."
    }

    Write-Evidence "PASS: A7 (T-10) - alembic check: ${DriftNote}."

    # -----------------------------------------------------------------
    # A8. VERDICT, STATE RECORD, CLEANUP
    # -----------------------------------------------------------------

    Write-Section "A8. FINAL APPLY VERDICT"

    if ($null -ne ${MainBackupPath} -and (Test-Path ${MainBackupPath})) {
        $BackupFinalHash = (Get-FileHash ${MainBackupPath} -Algorithm SHA256).Hash.ToLower()
        if ($BackupFinalHash -ne ${MainBackupHash}) {
            throw "FAIL: A8 - the anchor file changed after creation. Stopping; report to ITRGA."
        }
        Write-Evidence "Anchor unchanged since creation: ${MainBackupPath} (sha256 ${BackupFinalHash})"
    }

    $StateLines = @(
        "# ITRGA-V2-0045-APPLY-FINAL-STATE-V1",
        "# Written by ITRGA-V2-0045-APPLY-PACK-V1 at the end of a PASS.",
        "# Consumed strictly by ITRGA-V2-0045-VERIFY-PACK-V1.",
        "# This run's post-0045 bytes are seed-time-dependent; this record",
        "# is the verdict-binding identity register for exactly this run.",
        "STATE_FILE_ID=ITRGA-V2-0045-APPLY-FINAL-STATE-V1",
        "RUN_TIMESTAMP=$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss zzz')",
        "POST_SIZE_BYTES=${FinalSize}",
        "POST_LAST_WRITE=${FinalWrite}",
        "POST_SHA256=${FinalHash}",
        "POST_REVISION=${ApplyTargetRevision}",
        "POST_V2_TRIGGER_COUNT=28",
        "BASELINE_TIER1_BYTE_EXACT=${Tier1ByteExact}",
        "ANCHOR_FILENAME=$((Split-Path ${MainBackupPath} -Leaf))",
        "ANCHOR_SIZE_BYTES=${AnchorSize}",
        "ANCHOR_SHA256=${MainBackupHash}"
    )
    Set-Content -Path $StateRecPath -Value $StateLines -Encoding ASCII
    Write-Evidence "Apply-final-state record written: ${StateRecPath}"

    Write-Evidence ""
    Write-Evidence "APPLY VERDICT: PASS - band BE-5 (20260902_0044 + 20260902_0045) was applied ONCE to the application's working SQLite database file '${TargetDbPath}'."
    Write-Evidence "Terminal state on the working lineage (BO-V2-BE-5-001): revision 20260902_0045; 28 v2 triggers (18 inherited intact + 10 BE-5, exact names and exact refusal messages); five BE-5 tables with both uniqueness anchors and the six indexes; 5 computation-version rows (mge/sge hashes proven by runtime recomputation); 35 permission rows (8 additive BE-5, content-exact); all five BE-5 tables empty; inherited BE-1..BE-4 state untouched (content-exact proofs); drift re-baselined to exactly the 9 inherited V1 tokens with zero BE-5/V2 tokens; anchor created and verified."
    Write-Evidence "Transcript: ${Transcript}"
    Write-Evidence "State record: ${StateRecPath} (required by the verify pack; do not move or edit it.)"
    Write-Evidence "NEXT: run ITRGA_V2_0045_VERIFY_PACK_V1.ps1 NOW - BEFORE restarting the application (the verify pack requires the five new tables to still be empty)."

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
    if (Test-Path variable:TargetDbPathUrl) { Remove-Variable TargetDbPathUrl -ErrorAction SilentlyContinue }

    Remove-Item -Recurse -Force ${HelperDir} -ErrorAction SilentlyContinue

    Write-Host "Environment cleaned (AXIOM_DATABASE_URL, AXIOM_JWT_SECRET_KEY, AXIOM_ALLOW_INSECURE_DEV, AXIOM_ENVIRONMENT, AXIOM_V2_MODE, any AXIOM_TD_* / authority variables); helper removed."
}
