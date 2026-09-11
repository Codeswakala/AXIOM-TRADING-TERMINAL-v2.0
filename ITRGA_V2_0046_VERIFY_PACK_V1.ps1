# =====================================================================
# AXIOM V2 - 0046 WORKING-DATABASE VERIFICATION ACT (BAND BE-6)
# ITRGA SQLITE VERIFY ACT EVIDENCE PACK (V1)
# Pack ID: ITRGA-V2-0046-VERIFY-PACK-V1
# Authority:
#   - ITRGA-DET-V2-BE-6-FINAL-001 (final determination; C full-verify
#     PASS; instrument contract for the application act in section 7.3)
#   - ITRGA-DET-V2-BE-6-ACCEPT-001 (acceptance; BO-V2-BE-6-001 closed)
#   - BO-V2-BE-6-001 (terminal state; working-lineage half via this
#     apply+verify envelope)
#   - ITRGA-ASSESSMENT-V2-0046-APPLY-SCOPE-V1 (scope assessment,
#     instrument contract and commissioning record, incl. the pre-act
#     disclosure)
#   - ITRGA-V2-0046-APPLY-PACK-V1 (produces the state record and the
#     anchor this pack consumes; the verify act CANNOT precede the
#     apply act)
# Pattern: ITRGA-V2-0045-VERIFY-PACK-V1 -> ITRGA-V2-0043-VERIFY-PACK-V1
#   (instruments of record of the two preceding working-DB verification
#   acts; PGF-001 through PGF-015 incorporated by construction: pure
#   ASCII, helper command functions with non-colliding parameter names,
#   dialect-correct SQL, content-based comparisons, format-independent
#   drift assertions, name-set/PRAGMA-only index introspection with
#   uniqueness proven BEHAVIORALLY - sqlite_master has no 'origin'
#   column (PGF-015)).
#
# WHAT THIS PACK DOES (READ-ONLY against the target file; the only
#   mutation channels are the transactional probes, which always roll
#   their throwaway rows back):
#   - Binds the target file to the 0046 apply act byte-for-byte
#     (apply-final-state record consumed strictly; abort unless the
#     record is the 0046 PASS-state and the bytes match exactly).
#   - Independently re-proves the full terminal state: revision
#     exactly 20260903_0046; exactly 32 v2 triggers (28 inherited + 4
#     BE-6, exact names); the four BE-6 guard refusals with exact
#     messages plus the inherited compver guards on the new seed row;
#     both uniqueness anchors proven BEHAVIORALLY; three CHECK-vocabulary
#     probes refused; the two BE-6 tables with the pinned column
#     name-sets, all seven named constraints and both indexes; 6
#     computation-version rows (BE-4 pinned; mge/sge and
#     portfolio_risk_engine proven by RUNTIME RECOMPUTATION of the
#     engine files, the BE-6 recomputation asserted equal to the pinned
#     anchor); 41 permission rows (6 additive BE-6 rows content-exact,
#     no duplicates); both BE-6 tables empty and all five BE-5 tables
#     still empty; inherited BE-1..BE-3 anchors content-exact; drift
#     exactly the 9 inherited V1 tokens with zero BE-6/V2 tokens; no
#     authority variable present.
#   - Re-verifies the recovery anchor (file hash equal to the record;
#     the anchor is the CURRENT-AS-IS pre-image per pre-act disclosure
#     N-1: it lawfully includes the restart-era bootstrap-admin row).
#
# PREREQUISITES:
#   - The apply pack completed with verdict PASS (state record
#     present in operator-evidence\BE-6).
#   - The application has NOT been restarted since the apply (the
#     state-record byte-binding enforces this; the
#     both-BE-6-tables-empty proof additionally assumes it).
#
# OPERATOR INSTRUCTION CARD:
#   1. Run ITRGA_V2_0046_APPLY_PACK_V1.ps1 FIRST (its PASS is the
#      precondition; this pack reads its state record).
#   2. Execute ONLY this file, from the repository root:
#        powershell -NoProfile -ExecutionPolicy Bypass -File ".\ITRGA_V2_0046_VERIFY_PACK_V1.ps1"
#   3. Single expected input: the absolute path of the working
#      database file backend\axiom_dev.db (a path, not a credential).
#   4. Send BOTH transcripts back to ITRGA:
#        operator-evidence\BE-6\0046-APPLY-RUN-V1.txt
#        operator-evidence\BE-6\0046-VERIFY-RUN-V1.txt
#      These two files close the 0046 application act and place the
#      BO-V2-BE-6-001 terminal state on the working lineage. Restart
#      the application only after this pack completes with PASS.
#
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
$EvidenceDir   = Join-Path $EvidenceRoot "BE-6"
$Transcript    = Join-Path $EvidenceDir "0046-VERIFY-RUN-V1.txt"
$StateRecPath  = Join-Path $EvidenceDir "0046-APPLY-FINAL-STATE.txt"

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
    param($Lines)
    return (@($Lines | ForEach-Object { ([string]$_).Trim() }) -join "`n")
}

function Read-Pins {
    param(
        [Parameter(Mandatory = $true)][string]$Path,
        [Parameter(Mandatory = $true)][string[]]$ExpectedKeys,
        [Parameter(Mandatory = $true)][string]$Label
    )
    if (!(Test-Path $Path)) { throw "STOP: required pin file missing: ${Path} (${Label}). The verify act cannot precede the apply act." }
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
# 0A. CONSTANTS (identical pins to the apply pack)
# ---------------------------------------------------------------------

$ExpectedMigrationHashes = @{
    "20260823_0038_v2_be1_core.py"                 = "6e071157c204e29bfb1254400f0a4543d776931fa5834723cc497d12a0b8f588"
    "20260824_0039_v2_be2_marketdata.py"           = "bc11cae24cdbe47361454a676604a9f81b1754df47058185dd4c002689ab5b19"
    "20260824_0040_v2_be3_provider.py"             = "1332ebf5780fcda00d19589400bbeb873f7187fbd1f4915da093f822f392b226"
    "20260825_0041_v2_be3_p2_entitlement.py"       = "d775c34aedac8fffd594f4ac4434f48c9d9cfd2fa88f4d3fd1cf9e7ba278dadd"
    "20260829_0042_v2_be3_p2_transition.py"        = "af77a63f903a43e2eb7b4426b67de7113791f37918bbfe7f465d8f1bab3cf8d4"
    "20260831_0043_v2_be4_research_read_models.py" = "ab90576203d9f7946154ad4efd7a3d52bc98b91e328dbf2a4dca0b5049bda84b"
    "20260902_0044_v2_be5_ml_governance.py"        = "18e14f0ae971b7ae3e94b02c3d23ef7a608a6f1dde711e52c6f64d780e20efab"
    "20260902_0045_v2_be5_signal_contracts.py"     = "9aa87508b6db4d74296f8dabfab33ae7fb84dc705326f141b4b42e2d4f981f52"
    "20260903_0046_v2_be6_portfolio_research.py"   = "1e95ce499ec73bb5b8b0a628cfa01f1f26642c3cfcc080806cacce2532156962"
}
$ApplyTargetRevision = "20260903_0046"

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
    "backend\tests\test_v2_be5_api.py"                  = "a7f39d1d7add9a16be2d20fa433601d99e397825abf5e0cf6d53d378e8d777d2"
    "backend\tests\test_v2_be5_diagnostics.py"          = "2663058c8e6860cc98d129472c7484de1e1cde692fab76298eabf053cc7f6a5b"
    "backend\tests\test_v2_be5_lifecycle.py"            = "39c41896456f7c59351ac9bab0bf26441203e512248d160066c0d3de204207dc"
    "backend\tests\test_v2_be4_migration.py"            = "5935b9ea3c530dab3454daefa6c4e0ea3f2b46c957c923ccd62c6bb4eb5dce4d"
    "backend\app\v2\portfolio_research\__init__.py"     = "a8241065ce6c4963c861137df3e43d5ba3468c66f6206013f4e7a252b31747a3"
    "backend\app\v2\portfolio_research\contracts.py"    = "bc1f3c25ef72b3203a1bf33f670e5bbead825c09dc02482c5a432a148125f036"
    "backend\app\v2\portfolio_research\metrics.py"      = "5409c7da2f578a1e8756ecc779beabe55ffc4cfa2509c46f19fb664d12ce2d78"
    "backend\app\v2\portfolio_research\scenarios.py"    = "e032224e90d389f9e73f3009f21359d37c2566c6ad53783d8775ef8333ba4e66"
    "backend\app\v2\portfolio_research\api.py"          = "7f8a12ac05e04cc3fedaa7a04319b0c3af25a31eb115d722b968e345d78815eb"
    "backend\app\db\models\v2_portfolio.py"             = "89ead20a39008df516806332e76e0c7394b5e94ce746bf49d0d760876ca35e4b"
    "backend\tests\test_v2_be6_metrics.py"               = "c8716bdd23b4901d07525eaef5fbfdf8cc98c4ceece0573dcfb5132af0f3fa8d"
    "backend\tests\test_v2_be6_migration.py"             = "5f082ae956a074b9bca56a1b3368f5e1ab6c2c2db457551df2ac0219ba81462c"
    "backend\tests\test_v2_be6_api.py"                   = "c983989b21dd38369f1a93dd82a7b0bf60686aa8ee4c79bb1b32fde81f6923db"
    "backend\tests\test_v2_be6_annex.py"                 = "352d9924cbd62f022c7b3ded351b9e35e5364d650b4568036e6082d0e4c1cfae"
    "backend\app\v2\api\router.py"                      = "8eae85bcf9c7d0ceb273f0ff942076a523f8165c66ba35e831277fd944a64a3d"
    "backend\app\v2\rbac\permissions.py"                = "2400e6e78339422086723495a6e3621aca5c1162e8cb5fefad00e91a9c02a097"
    "backend\app\db\models\__init__.py"                 = "3465a5b0633da8165dac6b08aff2907472f780f573523c5ed1e84c451955b1ff"
    "backend\tests\test_v2_be5_migration.py"             = "1eb4ade1b11b71b4ba8f000bc588cb13c6db589d0181297df844a4b97cf30f6e"
}

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
$Be6GuardNames = @(
    "v2_portfolio_definition_immutable_delete",
    "v2_portfolio_definition_immutable_update",
    "v2_portfolio_risk_report_immutable_delete",
    "v2_portfolio_risk_report_immutable_update"
)
$Be6UpdateMsgDef  = "V2 portfolio definitions are immutable; UPDATE prohibited"
$Be6DeleteMsgDef  = "V2 portfolio definitions are immutable; DELETE prohibited"
$Be6UpdateMsgRep  = "V2 portfolio risk reports are immutable; UPDATE prohibited"
$Be6DeleteMsgRep  = "V2 portfolio risk reports are immutable; DELETE prohibited"

# The full prior 28-name trigger census (verified on the working
# database by the 0045-VERIFY-RUN-V2 transcript; pinned verbatim).
$ExpectedPreTrig28 = @(
    "v2_audit_immutable_delete",
    "v2_audit_immutable_update",
    "v2_chart_intelligence_report_immutable_delete",
    "v2_chart_intelligence_report_immutable_update",
    "v2_computation_version_immutable_delete",
    "v2_computation_version_immutable_update",
    "v2_lineage_immutable_delete",
    "v2_lineage_immutable_update",
    "v2_market_context_report_immutable_delete",
    "v2_market_context_report_immutable_update",
    "v2_md_integrity_immutable_delete",
    "v2_md_integrity_immutable_update",
    "v2_md_provider_hist_immutable_delete",
    "v2_md_provider_hist_immutable_update",
    "v2_md_provider_immutable_delete",
    "v2_md_provider_immutable_update",
    "v2_md_verification_immutable_delete",
    "v2_md_verification_immutable_update",
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

# The two BE-6 indexes (exact names).
$Be6Indexes = @(
    "ix_v2_pfdef_portfolio",
    "ix_v2_pfrisk_def"
)

# The pinned BE-6 engine-anchor (sha256 rolling digest over the four
# engine files, relpath+NUL+bytes+NUL in the pinned order; recomputed
# from the REM-Rev-2 literals and asserted equal at runtime).
$Be6EngineAnchor = "5c6d8f08809680506694032a5580616d6e15c13ecfa7a59a1d4a0fd869cec90a"

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
# 0B. OPERATOR INPUT
# ---------------------------------------------------------------------

Write-Host ""
Write-Host "This pack VERIFIES the 0046 working-database state (band BE-6)"
Write-Host "(read-only; transactional probes roll their probe rows back)."
Write-Host "The apply pack must have completed with PASS first."
Write-Host "This pack prompts for NO credential of any kind."
Write-Host ""

$TargetDbPath = (Read-Host -Prompt "Absolute path to the application's working SQLite database file (quotes optional; for example C:\Users\victo\.vscode\AXIOM\axiom\backend\axiom_dev.db)").Trim()
if ($TargetDbPath.Length -ge 2) {
    if (($TargetDbPath.StartsWith('"') -and $TargetDbPath.EndsWith('"')) -or
        ($TargetDbPath.StartsWith("'") -and $TargetDbPath.EndsWith("'"))) {
        $TargetDbPath = $TargetDbPath.Substring(1, $TargetDbPath.Length - 2).Trim()
        Write-Host "NOTE: surrounding quotes removed from the entered path (quotes are not part of a file path)."
    }
}
if ([string]::IsNullOrEmpty($TargetDbPath)) { throw "No database file path entered. Aborting." }
if (!(Test-Path ${TargetDbPath})) { throw "STOP: file not found: ${TargetDbPath}. Aborting." }
$TargetItem = Get-Item ${TargetDbPath}
if ($TargetItem.PSIsContainer) { throw "STOP: path is a directory, not a file: ${TargetDbPath}. Aborting." }
if ($TargetItem.Length -eq 0) { throw "STOP: file is empty (0 bytes): ${TargetDbPath}. Aborting." }
$TargetDbPath = $TargetItem.FullName
$LeafName = Split-Path ${TargetDbPath} -Leaf
if ($LeafName.ToLower() -ne $ExpectedLeafName) {
    throw "STOP: file leaf name '${LeafName}' does not match the working database file name '${ExpectedLeafName}'. Aborting."
}
$EvidenceRootFull = (Resolve-Path $EvidenceRoot).Path
if ($TargetDbPath.ToLower().StartsWith($EvidenceRootFull.ToLower())) {
    throw "STOP: target file is inside the operator-evidence directory. Aborting."
}

# ---------------------------------------------------------------------
# 0C. PYTHON HELPER (identical content to the apply pack)
# ---------------------------------------------------------------------

$HelperDir  = Join-Path $env:TEMP "axiom_itrga_0046_verify_v1"
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
BE6_FILES = (
    "app/v2/portfolio_research/__init__.py",
    "app/v2/portfolio_research/contracts.py",
    "app/v2/portfolio_research/metrics.py",
    "app/v2/portfolio_research/scenarios.py",
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
               "permbe5", "reportempty5", "compverbe6", "permbe6",
               "reportempty2", "tabledigest"):
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
            elif cmd == "compverbe6":
                # Exactly 6 rows: the 3 BE-4 components pinned by value;
                # the 2 BE-5 components and the BE-6 component pinned by
                # RUNTIME RECOMPUTATION of the engine file hashes. The
                # BE-6 recomputation is asserted equal to the pinned
                # anchor literal passed as argv[7] before the row check.
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
                be6_anchor_arg = sys.argv[7]
                be6_recomputed = engine_hash(backend_dir, BE6_FILES)
                if be6_recomputed != be6_anchor_arg:
                    print("FAIL:be6_anchor_mismatch recomputed=" + be6_recomputed
                          + " pinned=" + be6_anchor_arg)
                    return
                exp_be6 = {
                    "portfolio_risk_engine": ("pre-1.0.0", be6_recomputed),
                }
                rows = con.execute(
                    "SELECT component, version, source_hash, evidence_ref, registered_at "
                    "FROM v2_computation_version"
                ).fetchall()
                if len(rows) != 6:
                    print("FAIL:compver6_count=" + str(len(rows)))
                    return
                seen = {}
                for component, version, source_hash, evidence_ref, registered_at in rows:
                    if component in seen:
                        print("FAIL:compver6_duplicate_component=" + str(component))
                        return
                    seen[component] = (version, source_hash,
                                       evidence_ref, registered_at)
                exp_map = {}
                for src_map in (pins_be4, exp_be5, exp_be6):
                    exp_map.update(src_map)
                for component, (exp_version, exp_hash) in exp_map.items():
                    if component not in seen:
                        print("FAIL:compver6_missing=" + component)
                        return
                    version, source_hash, evidence_ref, registered_at = seen[component]
                    if version != exp_version:
                        print("FAIL:compver6_version=" + component + "=" + repr(version))
                        return
                    if source_hash != exp_hash:
                        print("FAIL:compver6_hash=" + component + "=" + repr(source_hash)
                              + " expected=" + repr(exp_hash))
                        return
                    if not re.fullmatch(r"[0-9a-f]{64}", source_hash or ""):
                        print("FAIL:compver6_hash_shape=" + component)
                        return
                    if component in pins_be4:
                        exp_ref = "BO-V2-BE-4-001"
                    elif component in exp_be5:
                        exp_ref = "BO-V2-BE-5-001"
                    else:
                        exp_ref = "BO-V2-BE-6-001"
                    if evidence_ref != exp_ref:
                        print("FAIL:compver6_evidence_ref=" + component + "=" + repr(evidence_ref))
                        return
                    if not registered_at or len(str(registered_at)) < 19:
                        print("FAIL:compver6_registered_at_shape=" + component)
                        return
                print("PASS:compver6_rows_exact")
                print("INFO:mge_recomputed=" + exp_be5["ml_governance_engine"][1])
                print("INFO:sge_recomputed=" + exp_be5["signal_engine"][1])
                print("INFO:pre_recomputed=" + be6_recomputed)
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
            elif cmd == "permbe6":
                rows = con.execute(
                    "SELECT role, permission, sal FROM v2_permission "
                    "WHERE permission LIKE 'v2.research.portfolio%'"
                ).fetchall()
                if len(rows) != 6:
                    print("FAIL:permbe6_count=" + str(len(rows)))
                    return
                expected = {
                    ("admin", "v2.research.portfolio.read", "SAL-2"),
                    ("admin", "v2.research.portfolio.define", "SAL-3"),
                    ("admin", "v2.research.portfolio_risk.read", "SAL-2"),
                    ("admin", "v2.research.portfolio_risk.compute", "SAL-3"),
                    ("operator", "v2.research.portfolio.read", "SAL-2"),
                    ("operator", "v2.research.portfolio_risk.read", "SAL-2"),
                }
                if set(tuple(r) for r in rows) != expected:
                    print("FAIL:permbe6_rows=" + repr(sorted(tuple(r) for r in rows)))
                    return
                total = con.execute("SELECT COUNT(*) FROM v2_permission").fetchone()[0]
                if total != 41:
                    print("FAIL:permbe6_total=" + str(total))
                    return
                dupes = con.execute(
                    "SELECT COUNT(*) - COUNT(DISTINCT role || '|' || permission) "
                    "FROM v2_permission"
                ).fetchone()[0]
                if dupes != 0:
                    print("FAIL:perm_duplicate_role_permission")
                    return
                print("PASS:perm6_rows_exact")
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
            elif cmd == "reportempty2":
                counts = {}
                for table in ("v2_portfolio_definition", "v2_portfolio_risk_report"):
                    counts[table] = con.execute(
                        "SELECT COUNT(*) FROM " + table).fetchone()[0]
                if any(v != 0 for v in counts.values()):
                    print("FAIL:table_counts=" + repr(counts))
                    return
                print("PASS:be6_tables_empty")
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

    if cmd == "uniqbe6":
        flavor = sys.argv[3]
        if flavor == "pfdef":
            base_sql = ("INSERT INTO v2_portfolio_definition (id, portfolio_id, "
                        "record_seq, name, basis, allocations, base_currency, "
                        "data_class, assumptions, mode, operator_id, created_at) "
                        "VALUES ('uniqprobe-a', 'uniqprobe', 1, 'uniqprobe', "
                        "'hypothetical', '{}', 'EUR', 'synthetic', '{}', "
                        "'RESEARCH', 'uniqprobe', '2026-09-03 00:00:00');")
            dup_sql = ("INSERT INTO v2_portfolio_definition (id, portfolio_id, "
                       "record_seq, name, basis, allocations, base_currency, "
                       "data_class, assumptions, mode, operator_id, created_at) "
                       "VALUES ('uniqprobe-b', 'uniqprobe', 1, 'uniqprobe', "
                       "'hypothetical', '{}', 'EUR', 'synthetic', '{}', "
                       "'RESEARCH', 'uniqprobe', '2026-09-03 00:00:00');")
        elif flavor == "pfrisk":
            base_sql = ("INSERT INTO v2_portfolio_risk_report (id, "
                        "portfolio_definition_id, as_of, time_basis, input_refs, "
                        "inputs_hash, metrics, scenarios, status, basis_label, "
                        "data_class, engine_versions, engine_versions_hash, mode, "
                        "operator_id, created_at) "
                        "VALUES ('uniqprobe-a', 'uniqprobe', '2026-09-03 00:00:00', "
                        "'{}', '[]', 'uniqprobe-in', '{}', '[]', 'available', "
                        "'hypothetical-research', 'synthetic', '{}', 'uniqprobe-eng', "
                        "'RESEARCH', 'uniqprobe', '2026-09-03 00:00:00');")
            dup_sql = ("INSERT INTO v2_portfolio_risk_report (id, "
                       "portfolio_definition_id, as_of, time_basis, input_refs, "
                       "inputs_hash, metrics, scenarios, status, basis_label, "
                       "data_class, engine_versions, engine_versions_hash, mode, "
                       "operator_id, created_at) "
                       "VALUES ('uniqprobe-b', 'uniqprobe', '2026-09-03 00:00:00', "
                       "'{}', '[]', 'uniqprobe-in', '{}', '[]', 'available', "
                       "'hypothetical-research', 'synthetic', '{}', 'uniqprobe-eng', "
                       "'RESEARCH', 'uniqprobe', '2026-09-03 00:00:00');")
        else:
            print("FAIL:unknown_flavor=" + flavor)
            sys.exit(2)
        con = rw_connect(db_path)
        try:
            con.execute(base_sql)
            try:
                con.execute(dup_sql)
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
    if ($RevToken -ne $ExpectedRev) {
        throw "FAIL: ${Label} - current revision is '${RevLine}'; expected exactly '${ExpectedRev}'."
    }
    Write-Evidence "Current revision: ${RevToken}"
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

function Invoke-ExpectedUniqProbe {
    param(
        [Parameter(Mandatory = $true)][string]$Label,
        [Parameter(Mandatory = $true)][string]$Flavor
    )

    Write-Evidence ""
    Write-Evidence "EXPECTED-UNIQUENESS-PROBE: ${Label}"

    $Out = Invoke-Py -PyArgs @("uniqbe6", ${TargetDbPath}, ${Flavor}) -Label $Label
    $Text = (Norm-Text $Out).Trim()

    if ($Text -notlike "REFUSED:*") {
        throw "FAIL: expected uniqueness refusal did not occur (duplicate insert succeeded or helper error): ${Label}"
    }
    if ($Text -notlike "*UNIQUE constraint failed*") {
        throw "FAIL: the refusal was not a UNIQUE-constraint refusal: ${Label} (observed '${Text}')"
    }
    Write-Evidence "PASS: duplicate insert refused by the uniqueness anchor (behavioral proof); throwaway rows rolled back."
}

# ---------------------------------------------------------------------
# B0. RUN IDENTIFICATION
# ---------------------------------------------------------------------

Write-Section "B0. RUN IDENTIFICATION"
Write-Evidence "Pack: ITRGA-V2-0046-VERIFY-PACK-V1"
Write-Evidence "Act: band BE-6 (0046) working-database verification act (read-only; transactional probes roll back)"
Write-Evidence "Determination: ITRGA-DET-V2-BE-6-FINAL-001 (C full-verify PASS) + ITRGA-DET-V2-BE-6-ACCEPT-001"
Write-Evidence "Build order: BO-V2-BE-6-001 (terminal state; working-lineage half via this envelope)"
Write-Evidence "Scope/commissioning: ITRGA-ASSESSMENT-V2-0046-APPLY-SCOPE-V1 (incl. pre-act disclosure N-1)"
Write-Evidence "State record (strictly consumed): ${StateRecPath}"
Write-Evidence "Started: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss zzz')"
Write-Evidence "Repo root: ${RepoRoot}"
Write-Evidence "Target file (APPLICATION'S WORKING DATABASE - named by the Operator): ${TargetDbPath}"
Write-Evidence "SQL engine: SQLite (in-process, via the repo venv python sqlite3 module; no database server)"
Write-Evidence "Server credentials used: NONE (no database server; no password prompt)"
Write-Evidence "Authority variable: NONE EXISTS FOR THIS ACT; absence asserted in B8."

Push-Location $BackendRoot

try {

    # -----------------------------------------------------------------
    # B0c. HELPER SELF-TEST
    # -----------------------------------------------------------------

    Write-Section "B0c. HELPER SELF-TEST"

    [void](Invoke-Py -PyArgs @("selftest", ${TargetDbPath}) -Label "helper self-test")

    # -----------------------------------------------------------------
    # B0d. RUN ENVIRONMENT
    # -----------------------------------------------------------------

    Write-Section "B0d. RUN ENVIRONMENT (no credentials; no authority variable)"

    $TargetDbPathUrl = $TargetDbPath.Replace("\", "/")
    $env:AXIOM_DATABASE_URL       = "sqlite+aiosqlite:///" + ${TargetDbPathUrl}
    $env:AXIOM_ENVIRONMENT        = "testing"
    $env:AXIOM_ALLOW_INSECURE_DEV = "true"
    $env:AXIOM_JWT_SECRET_KEY     = "operator-local-test-secret-at-least-32-characters"
    $env:AXIOM_V2_MODE            = "RESEARCH"

    $EnvSweepNames = @(Get-ChildItem Env: | Where-Object { $_.Name -like 'AXIOM_TD_*' -or $_.Name -like '*AUTHORITY_REF*' } | ForEach-Object { $_.Name })
    if ($EnvSweepNames.Count -eq 0) {
        Write-Evidence "Authority/TD variables: none present at act start (recorded)."
    } else {
        foreach ($EnvName in $EnvSweepNames) {
            Remove-Item -Path ("Env:\" + ${EnvName}) -ErrorAction SilentlyContinue
            Write-Evidence ("  removed pre-existing variable: " + ${EnvName} + " (value never printed)")
        }
    }
    Write-Evidence "AXIOM_DATABASE_URL built for the target file (value not printed); testing env; RESEARCH mode."

    # -----------------------------------------------------------------
    # B0e. APPLY-FINAL-STATE RECORD (strict; gate of this act)
    # -----------------------------------------------------------------

    Write-Section "B0e. APPLY-FINAL-STATE RECORD (strict parse; the verify act cannot precede the apply act)"

    $State = Read-Pins -Path $StateRecPath -ExpectedKeys @(
        "STATE_FILE_ID", "RUN_TIMESTAMP", "POST_SIZE_BYTES", "POST_LAST_WRITE",
        "POST_SHA256", "POST_REVISION", "POST_V2_TRIGGER_COUNT",
        "POST_COMPVER_COUNT", "POST_PERMISSION_COUNT",
        "BASELINE_TIER1_BYTE_EXACT", "BASELINE_POLICY",
        "ANCHOR_FILENAME", "ANCHOR_SIZE_BYTES", "ANCHOR_SHA256"
    ) -Label "0046 apply-final-state record"

    if ($State["STATE_FILE_ID"] -ne "ITRGA-V2-0046-APPLY-FINAL-STATE-V1") {
        throw "STOP: state record identity '$($State["STATE_FILE_ID"])' is not ITRGA-V2-0046-APPLY-FINAL-STATE-V1."
    }
    if ($State["POST_REVISION"] -ne ${ApplyTargetRevision}) {
        throw "STOP: state record revision '$($State["POST_REVISION"])' is not ${ApplyTargetRevision}."
    }
    if ($State["POST_V2_TRIGGER_COUNT"] -ne "32") {
        throw "STOP: state record trigger count '$($State["POST_V2_TRIGGER_COUNT"])' is not 32."
    }
    if ($State["POST_COMPVER_COUNT"] -ne "6") {
        throw "STOP: state record computation-version count '$($State["POST_COMPVER_COUNT"])' is not 6."
    }
    if ($State["POST_PERMISSION_COUNT"] -ne "41") {
        throw "STOP: state record permission count '$($State["POST_PERMISSION_COUNT"])' is not 41."
    }
    if ($State["POST_SIZE_BYTES"] -notmatch '^[0-9]+$') { throw "STOP: malformed POST_SIZE_BYTES in state record." }
    if ($State["POST_SHA256"] -notmatch '^[0-9a-f]{64}$') { throw "STOP: malformed POST_SHA256 in state record." }
    if ($State["ANCHOR_SHA256"] -notmatch '^[0-9a-f]{64}$') { throw "STOP: malformed ANCHOR_SHA256 in state record." }
    if ($State["ANCHOR_SIZE_BYTES"] -notmatch '^[0-9]+$') { throw "STOP: malformed ANCHOR_SIZE_BYTES in state record." }
    if ($State["BASELINE_TIER1_BYTE_EXACT"] -notmatch '^(True|False)$') { throw "STOP: malformed BASELINE_TIER1_BYTE_EXACT in state record." }
    if ($State["BASELINE_POLICY"] -ne "anchor-as-is (pre-act disclosure N-1)") {
        throw "STOP: state record BASELINE_POLICY '$($State["BASELINE_POLICY"])' is not the disclosed anchor-as-is policy."
    }

    Write-Evidence "Record: ${StateRecPath}"
    Write-Evidence "  RUN_TIMESTAMP                $($State["RUN_TIMESTAMP"])"
    Write-Evidence "  POST_SIZE_BYTES              $($State["POST_SIZE_BYTES"])"
    Write-Evidence "  POST_LAST_WRITE              $($State["POST_LAST_WRITE"])"
    Write-Evidence "  POST_SHA256                  $($State["POST_SHA256"])"
    Write-Evidence "  POST_REVISION                $($State["POST_REVISION"])"
    Write-Evidence "  POST_V2_TRIGGER_COUNT        $($State["POST_V2_TRIGGER_COUNT"])"
    Write-Evidence "  POST_COMPVER_COUNT           $($State["POST_COMPVER_COUNT"])"
    Write-Evidence "  POST_PERMISSION_COUNT        $($State["POST_PERMISSION_COUNT"])"
    Write-Evidence "  BASELINE_TIER1_BYTE_EXACT    $($State["BASELINE_TIER1_BYTE_EXACT"])  (policy-recorded; anchor-as-is per pre-act disclosure N-1)"
    Write-Evidence "  BASELINE_POLICY              $($State["BASELINE_POLICY"])"
    Write-Evidence "PASS: state record parsed; this run's verdict-binding post-0046 identity is known."

    # -----------------------------------------------------------------
    # B0f. PROVENANCE (36 files re-pinned on disk: 9 chain migrations + 27 delivered files)
    # -----------------------------------------------------------------

    Write-Section "B0f. PROVENANCE (36 files re-pinned on disk: 9 chain migrations + 27 delivered files; abort on any mismatch)"

    foreach ($MigName in @(
        "20260823_0038_v2_be1_core.py",
        "20260824_0039_v2_be2_marketdata.py",
        "20260824_0040_v2_be3_provider.py",
        "20260825_0041_v2_be3_p2_entitlement.py",
        "20260829_0042_v2_be3_p2_transition.py",
        "20260831_0043_v2_be4_research_read_models.py",
        "20260902_0044_v2_be5_ml_governance.py",
        "20260902_0045_v2_be5_signal_contracts.py",
        "20260903_0046_v2_be6_portfolio_research.py"
    )) {
        $MigPath = Join-Path $BackendRoot ("alembic\versions\" + ${MigName})
        if (!(Test-Path $MigPath)) { throw "STOP: migration file missing: ${MigPath}." }
        $ActualHash = (Get-FileHash $MigPath -Algorithm SHA256).Hash.ToLower()
        $PinnedHash = $ExpectedMigrationHashes[${MigName}]
        if ($ActualHash -ne $PinnedHash) {
            throw "STOP: B0f - provenance hash mismatch for ${MigName}; report to ITRGA."
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
        "backend\tests\test_v2_be4_migration.py",
        "backend\app\v2\portfolio_research\__init__.py",
        "backend\app\v2\portfolio_research\contracts.py",
        "backend\app\v2\portfolio_research\metrics.py",
        "backend\app\v2\portfolio_research\scenarios.py",
        "backend\app\v2\portfolio_research\api.py",
        "backend\app\db\models\v2_portfolio.py",
        "backend\tests\test_v2_be6_metrics.py",
        "backend\tests\test_v2_be6_migration.py",
        "backend\tests\test_v2_be6_api.py",
        "backend\tests\test_v2_be6_annex.py"
    )) {
        $FullPath = Join-Path $RepoRoot ${RelPath}
        if (!(Test-Path $FullPath)) { throw "STOP: delivered file missing: ${FullPath}." }
        $ActualHash = (Get-FileHash $FullPath -Algorithm SHA256).Hash.ToLower()
        $PinnedHash = $ExpectedDeliveredHashes[${RelPath}]
        if ($ActualHash -ne $PinnedHash) {
            throw "STOP: B0f - provenance hash mismatch for ${RelPath}; report to ITRGA."
        }
    }
    Write-Evidence "PASS: B0f - all 36 files on disk hash to the pinned values (9 chain migrations 0038-0046; 27 delivered BE-5/BE-6 files; the four shared paths pinned to the BE-6 Rev-2 literals)."

    # Repository head (recorded).
    $HeadsOut = Invoke-Alembic -AlembicArgs @("heads") -Label "B0f repository heads (recorded)"
    $HeadsText = Norm-Text $HeadsOut
    $HeadLines = @($HeadsText -split "`n" | Where-Object { $_ -match '^[0-9a-z]{8}_[0-9]{4}(\s*\([^)]*\))?$' })
    if ($HeadLines.Count -ne 1) {
        throw "FAIL: B0f - expected exactly one alembic head; observed $($HeadLines.Count) in: '${HeadsText}'."
    }
    $RepoHead = ($HeadLines[0].Trim() -replace '\s*\([^)]*\)$', '').Trim()
    if ($RepoHead -ne ${ApplyTargetRevision}) {
        throw "FAIL: B0f - repository head is '${RepoHead}'; expected exactly ${ApplyTargetRevision}."
    }
    Write-Evidence "Repository head: ${RepoHead}"

    # -----------------------------------------------------------------
    # B1. TARGET IDENTITY vs THE APPLY-FINAL-STATE RECORD (byte-exact)
    # -----------------------------------------------------------------

    Write-Section "B1. TARGET IDENTITY vs THE APPLY-FINAL-STATE RECORD (byte-exact binding)"

    $V1File = Get-Item ${TargetDbPath}
    $V1Size = $V1File.Length
    $V1Hash = (Get-FileHash ${TargetDbPath} -Algorithm SHA256).Hash.ToLower()
    Write-Evidence "  size       ${V1Size} bytes (record $($State["POST_SIZE_BYTES"]))"
    Write-Evidence "  sha256     ${V1Hash} (record $($State["POST_SHA256"]))"
    if ([string]$V1Size -ne $State["POST_SIZE_BYTES"]) {
        throw "FAIL: B1 - target file size differs from the apply-final-state record. The application may have been restarted between apply and verify (or the file changed). Report to ITRGA."
    }
    if ($V1Hash -ne $State["POST_SHA256"]) {
        throw "FAIL: B1 - target file sha256 differs from the apply-final-state record. The application may have been restarted between apply and verify (or the file changed). Report to ITRGA."
    }
    Write-Evidence "PASS: B1 - target file is byte-identical to the apply-final-state record (the state under verification is exactly the state the apply act produced)."

    # -----------------------------------------------------------------
    # B2. CURRENT REVISION EXACTLY 20260903_0046 (T-1)
    # -----------------------------------------------------------------

    Write-Section "B2. CURRENT REVISION EXACTLY ${ApplyTargetRevision} (T-1)"

    [void](Assert-CurrentExactly -ExpectedRev ${ApplyTargetRevision} -Label "B2 current revision")
    Write-Evidence "PASS: B2 (T-1) - current revision is exactly ${ApplyTargetRevision}."

    # -----------------------------------------------------------------
    # B3. RECOVERY ANCHOR (the apply act's pre-image copy)
    # -----------------------------------------------------------------

    Write-Section "B3. RECOVERY ANCHOR (the apply act's pre-image copy; re-verified)"

    $AnchorFullPath = Join-Path $EvidenceDir $State["ANCHOR_FILENAME"]
    if (!(Test-Path $AnchorFullPath)) { throw "FAIL: B3 - anchor file missing: ${AnchorFullPath}." }
    $AnchorItem = Get-Item $AnchorFullPath
    $AnchorHashNow = (Get-FileHash $AnchorFullPath -Algorithm SHA256).Hash.ToLower()
    Write-Evidence "Anchor: ${AnchorFullPath}"
    Write-Evidence "  size       $($AnchorItem.Length) bytes (record $($State["ANCHOR_SIZE_BYTES"]))"
    Write-Evidence "  sha256     ${AnchorHashNow} (record $($State["ANCHOR_SHA256"]))"
    if ([string]$AnchorItem.Length -ne $State["ANCHOR_SIZE_BYTES"]) {
        throw "FAIL: B3 - anchor size differs from the record."
    }
    if ($AnchorHashNow -ne $State["ANCHOR_SHA256"]) {
        throw "FAIL: B3 - anchor sha256 differs from the record."
    }
    $AnchorIntOut = Invoke-Py -PyArgs @("scalar", ${AnchorFullPath}, "PRAGMA integrity_check;") -Label "B3 anchor integrity"
    $AnchorIntText = (Norm-Text $AnchorIntOut).Trim()
    if ($AnchorIntText -ne "ok") {
        throw "FAIL: B3 - anchor integrity_check '${AnchorIntText}', expected 'ok'."
    }
    Write-Evidence "PASS: B3 - the recovery anchor (pre-0046 pre-image; current-as-is per pre-act disclosure N-1, incl. the restart-era bootstrap-admin row) exists and is byte-identical to the apply act's record; integrity ok."

    Write-Section "B4. COMPUTATION-VERSION ROWS (exactly 6; runtime recomputation incl. the BE-6 anchor)"

    $CompverOut = Invoke-Py -PyArgs @(
        "compverbe6", ${TargetDbPath}, ${BackendRoot},
        "fe9aab42c34d671e960fd92a9346d3bf60c27135e76e52310d774bc84028dd35",
        "69902503483502bcd5ce5e35fdb0eeabcb2efcaf7a4b0c262a6fccf2d0af3a8c",
        "3887d6ca8ba05858f41889cd99fa05aba42663ac22d906a7f989b567c3912180",
        ${Be6EngineAnchor}
    ) -Label "B4 computation-version rows"
    $CompverText = (Norm-Text $CompverOut).Trim()
    if ($CompverText -notlike "PASS:compver6_rows_exact*") {
        throw "FAIL: B4 - computation-version check failed: ${CompverText}"
    }
    if ($CompverText -notlike "*INFO:pre_recomputed=${Be6EngineAnchor}*") {
        throw "FAIL: B4 (P-4) - the runtime-recomputed BE-6 engine anchor does not equal the pinned anchor."
    }
    Write-Evidence "PASS: B4 (T-5/T-6; P-4) - exactly 6 rows; BE-4 rows content-exact; mge/sge source hashes equal the runtime recomputation; the portfolio_risk_engine row (pre-1.0.0, evidence_ref BO-V2-BE-6-001) equals the runtime recomputation of the four pinned files AND the pinned anchor."

    Write-Section "B5. PERMISSION ROWS + BE-6 TABLES EMPTY (+ BE-5 STILL EMPTY) + TRIGGER POSTURE"

    $PermOut = Invoke-Py -PyArgs @("permbe6", ${TargetDbPath}) -Label "B5 permission rows"
    $PermText = (Norm-Text $PermOut).Trim()
    if ($PermText -notlike "PASS:perm6_rows_exact*") {
        throw "FAIL: B5 - permission check failed: ${PermText}"
    }
    if ($PermText -notlike "*INFO:v2_permission_total=41*") {
        throw "FAIL: B5 (T-4/T-6) - permission total is not exactly 41."
    }

    $EmptyOut2 = Invoke-Py -PyArgs @("reportempty2", ${TargetDbPath}) -Label "B5 BE-6 tables empty"
    $EmptyText2 = (Norm-Text $EmptyOut2).Trim()
    if ($EmptyText2 -ne "PASS:be6_tables_empty") {
        throw "FAIL: B5 - the two BE-6 tables are not empty. The application may have been restarted between apply and verify. Report to ITRGA."
    }
    $EmptyOut5 = Invoke-Py -PyArgs @("reportempty5", ${TargetDbPath}) -Label "B5 BE-5 tables still empty"
    $EmptyText5 = (Norm-Text $EmptyOut5).Trim()
    if ($EmptyText5 -ne "PASS:be5_tables_empty") {
        throw "FAIL: B5 - the five BE-5 tables are not empty. Report to ITRGA."
    }

    [void](Invoke-Py -PyArgs @("scalar", ${TargetDbPath}, "SELECT name FROM sqlite_master WHERE type='trigger' AND name LIKE 'v2_%' ORDER BY name;") -Label "B5 v2 trigger names (recorded)")
    $TrigNamesText = Get-PyScalar -Sql "SELECT name FROM sqlite_master WHERE type='trigger' AND name LIKE 'v2_%' ORDER BY name;" -Label "B5 v2 trigger set"
    $TrigNames = @($TrigNamesText -split "`n" | Where-Object { $_ -ne "" })
    if ($TrigNames.Count -ne 32) {
        throw "FAIL: B5 (T-3/T-6) - v2 trigger count '$($TrigNames.Count)', expected exactly 32."
    }
    $Expected32Sorted = @(($ExpectedPreTrig28 + $Be6GuardNames) | Sort-Object)
    $TrigSorted = @($TrigNames | Sort-Object)
    if (($TrigSorted -join "`n") -ne ($Expected32Sorted -join "`n")) {
        throw "FAIL: B5 (T-3/T-6) - the v2 trigger name set is not exactly the pinned 32-name census (28 inherited + 4 BE-6)."
    }
    Write-Evidence "PASS: B5 (T-2/T-3/T-4/T-6) - exactly 6 additive BE-6 permission rows (total 41, no duplicates); both BE-6 tables empty and all five BE-5 tables still empty; 32 v2 triggers exact-named (28 inherited intact + 4 BE-6)."

    # BE-6 schema census (PRAGMA/name-set; PGF-015): columns, PKs, named
    # constraints in the stored DDL, the two indexes, autoindex census.
    $PfdefCols = Get-PyScalar -Sql "SELECT name FROM pragma_table_info('v2_portfolio_definition') ORDER BY cid;" -Label "B5 pfdef columns"
    $ExpectedPfdefCols = @("id","portfolio_id","record_seq","supersedes","name","basis","allocations","base_currency","data_class","assumptions","mode","operator_id","correlation_id","created_at") -join "`n"
    if ($PfdefCols -ne $ExpectedPfdefCols) {
        throw "FAIL: B5 (T-2) - v2_portfolio_definition column set/order mismatch."
    }
    $PfriskCols = Get-PyScalar -Sql "SELECT name FROM pragma_table_info('v2_portfolio_risk_report') ORDER BY cid;" -Label "B5 pfrisk columns"
    $ExpectedPfriskCols = @("id","portfolio_definition_id","as_of","time_basis","input_refs","inputs_hash","metrics","scenarios","status","basis_label","data_class","engine_versions","engine_versions_hash","mode","operator_id","correlation_id","created_at") -join "`n"
    if ($PfriskCols -ne $ExpectedPfriskCols) {
        throw "FAIL: B5 (T-2) - v2_portfolio_risk_report column set/order mismatch."
    }
    $PfdefPk = Get-PyScalar -Sql "SELECT name FROM pragma_table_info('v2_portfolio_definition') WHERE pk > 0;" -Label "B5 pfdef pk"
    if ($PfdefPk -ne "id") { throw "FAIL: B5 (T-2) - pfdef primary key is not 'id'." }
    $PfriskPk = Get-PyScalar -Sql "SELECT name FROM pragma_table_info('v2_portfolio_risk_report') WHERE pk > 0;" -Label "B5 pfrisk pk"
    if ($PfriskPk -ne "id") { throw "FAIL: B5 (T-2) - pfrisk primary key is not 'id'." }
    $PfdefDdl = Get-PyScalar -Sql "SELECT sql FROM sqlite_master WHERE type='table' AND name='v2_portfolio_definition';" -Label "B5 pfdef DDL"
    foreach ($Anchor in @("uq_v2_pfdef_id_seq", "ck_v2_pfdef_basis", "ck_v2_pfdef_data_class")) {
        if ($PfdefDdl -notlike "*${Anchor}*") { throw "FAIL: B5 (T-2) - '${Anchor}' missing from v2_portfolio_definition DDL." }
    }
    $PfriskDdl = Get-PyScalar -Sql "SELECT sql FROM sqlite_master WHERE type='table' AND name='v2_portfolio_risk_report';" -Label "B5 pfrisk DDL"
    foreach ($Anchor in @("uq_v2_pfrisk_determinism_anchor", "ck_v2_pfrisk_status", "ck_v2_pfrisk_basis_label", "ck_v2_pfrisk_data_class")) {
        if ($PfriskDdl -notlike "*${Anchor}*") { throw "FAIL: B5 (T-2) - '${Anchor}' missing from v2_portfolio_risk_report DDL." }
    }
    $Be6IdxFound = Get-PyScalar -Sql "SELECT name FROM sqlite_master WHERE type='index' AND name IN ('ix_v2_pfdef_portfolio','ix_v2_pfrisk_def') ORDER BY name;" -Label "B5 BE-6 index names"
    if ($Be6IdxFound -ne ($Be6Indexes -join "`n")) {
        throw "FAIL: B5 (T-2/T-6) - the two BE-6 index names are not exactly the pinned set."
    }
    $PfdefAuto = Get-PyScalar -Sql "SELECT COUNT(*) FROM sqlite_master WHERE type='index' AND tbl_name='v2_portfolio_definition' AND name LIKE 'sqlite_autoindex%';" -Label "B5 pfdef autoindex census"
    if ([int]$PfdefAuto -lt 2) { throw "FAIL: B5 (T-2) - fewer than 2 autoindexes on v2_portfolio_definition." }
    $PfriskAuto = Get-PyScalar -Sql "SELECT COUNT(*) FROM sqlite_master WHERE type='index' AND tbl_name='v2_portfolio_risk_report' AND name LIKE 'sqlite_autoindex%';" -Label "B5 pfrisk autoindex census"
    if ([int]$PfriskAuto -lt 2) { throw "FAIL: B5 (T-2) - fewer than 2 autoindexes on v2_portfolio_risk_report." }
    Write-Evidence "PASS: B5 (T-2) - both BE-6 tables carry the pinned column name-sets with PK 'id'; all seven named constraints present in the stored DDL; both BE-6 indexes exact-named; autoindex census consistent with the PK + uniqueness anchors (behavioral proof in B7)."

    # -----------------------------------------------------------------
    # B6. INHERITED STATE UNTOUCHED (BE-1..BE-3 anchors, content-exact)
    # -----------------------------------------------------------------

    Write-Section "B6. INHERITED STATE (BE-1..BE-3 anchors, content-exact)"

    $ProvNow = Get-PyScalar -Sql "SELECT source_status, entitlement_status, persistence_permitted FROM v2_md_provider WHERE provider_id='twelvedata';" -Label "B6 provider row"
    if ($ProvNow -ne "contract_tested|verified|0") {
        throw "FAIL: B6 - inherited provider row is '${ProvNow}', expected 'contract_tested|verified|0'."
    }
    $RowsNow = Invoke-Py -PyArgs @("verifyrows", ${TargetDbPath}) -Label "B6 history exact-content"
    if ((Norm-Text $RowsNow).Trim() -ne "PASS:history_rows_exact") {
        throw "FAIL: B6 - inherited history content differs from the pinned state."
    }
    $AuditNow = Invoke-Py -PyArgs @("verifyaudit", ${TargetDbPath}) -Label "B6 audit exact-content"
    if ((Norm-Text $AuditNow).Trim() -ne "PASS:audit_rows_exact") {
        throw "FAIL: B6 - inherited audit content differs from the pinned state."
    }
    Write-Evidence "PASS: B6 (T-9) - provider row, history rows, and transition audit events content-exact."

    Write-Section "B7. GUARD REFUSALS (four BE-6, exact messages; inherited compver guards intact on the new seed row; two behavioral uniqueness proofs; three CHECK probes)"

    Invoke-ExpectedRefusal -Label "B7: compver UPDATE on the BE-6 seed row (inherited guard intact)" -Sql "UPDATE v2_computation_version SET version='probe' WHERE component='portfolio_risk_engine';" -ExactMessage "V2 computation version registry is immutable; UPDATE prohibited"
    Invoke-ExpectedRefusal -Label "B7: compver DELETE on the BE-6 seed row (drop/re-created guard intact)" -Sql "DELETE FROM v2_computation_version WHERE component='portfolio_risk_engine';" -ExactMessage "V2 computation version registry is immutable; DELETE prohibited"

    $PfdefInsert = "INSERT INTO v2_portfolio_definition (id, portfolio_id, record_seq, name, basis, allocations, base_currency, data_class, assumptions, mode, operator_id, created_at) VALUES ('guardprobe', 'guardprobe', 1, 'guardprobe', 'hypothetical', '{}', 'EUR', 'synthetic', '{}', 'RESEARCH', 'guardprobe', '2026-09-03 00:00:00');"
    Invoke-ExpectedGuardProbe -Label "B7: portfolio-definition UPDATE" -InsertSql ${PfdefInsert} -ProbeSql "UPDATE v2_portfolio_definition SET name='probe' WHERE id='guardprobe';" -ExactMessage ${Be6UpdateMsgDef}
    Invoke-ExpectedGuardProbe -Label "B7: portfolio-definition DELETE" -InsertSql ${PfdefInsert} -ProbeSql "DELETE FROM v2_portfolio_definition WHERE id='guardprobe';" -ExactMessage ${Be6DeleteMsgDef}

    $PfriskInsert = "INSERT INTO v2_portfolio_risk_report (id, portfolio_definition_id, as_of, time_basis, input_refs, inputs_hash, metrics, scenarios, status, basis_label, data_class, engine_versions, engine_versions_hash, mode, operator_id, created_at) VALUES ('guardprobe', 'guardprobe', '2026-09-03 00:00:00', '{}', '[]', 'guardprobe-in', '{}', '[]', 'available', 'hypothetical-research', 'synthetic', '{}', 'guardprobe-eng', 'RESEARCH', 'guardprobe', '2026-09-03 00:00:00');"
    Invoke-ExpectedGuardProbe -Label "B7: portfolio-risk-report UPDATE" -InsertSql ${PfriskInsert} -ProbeSql "UPDATE v2_portfolio_risk_report SET status='stale' WHERE id='guardprobe';" -ExactMessage ${Be6UpdateMsgRep}
    Invoke-ExpectedGuardProbe -Label "B7: portfolio-risk-report DELETE" -InsertSql ${PfriskInsert} -ProbeSql "DELETE FROM v2_portfolio_risk_report WHERE id='guardprobe';" -ExactMessage ${Be6DeleteMsgRep}

    Invoke-ExpectedUniqProbe -Label "B7: uq_v2_pfdef_id_seq (portfolio_id, record_seq)" -Flavor "pfdef"
    Invoke-ExpectedUniqProbe -Label "B7: uq_v2_pfrisk_determinism_anchor (portfolio_definition_id, inputs_hash, engine_versions_hash)" -Flavor "pfrisk"

    Invoke-ExpectedRefusal -Label "B7: CHECK probe - basis 'real' refused (ck_v2_pfdef_basis)" -Sql "INSERT INTO v2_portfolio_definition (id, portfolio_id, record_seq, name, basis, allocations, base_currency, data_class, assumptions, mode, operator_id, created_at) VALUES ('checkprobe', 'checkprobe', 7, 'checkprobe', 'real', '{}', 'EUR', 'synthetic', '{}', 'RESEARCH', 'checkprobe', '2026-09-03 00:00:00');" -ExactMessage "CHECK"
    Invoke-ExpectedRefusal -Label "B7: CHECK probe - status 'bogus' refused (ck_v2_pfrisk_status)" -Sql "INSERT INTO v2_portfolio_risk_report (id, portfolio_definition_id, as_of, time_basis, input_refs, inputs_hash, metrics, scenarios, status, basis_label, data_class, engine_versions, engine_versions_hash, mode, operator_id, created_at) VALUES ('checkprobe', 'checkprobe', '2026-09-03 00:00:00', '{}', '[]', 'checkprobe-in', '{}', '[]', 'bogus', 'hypothetical-research', 'synthetic', '{}', 'checkprobe-eng', 'RESEARCH', 'checkprobe', '2026-09-03 00:00:00');" -ExactMessage "CHECK"
    Invoke-ExpectedRefusal -Label "B7: CHECK probe - basis_label 'account-state' refused (ck_v2_pfrisk_basis_label)" -Sql "INSERT INTO v2_portfolio_risk_report (id, portfolio_definition_id, as_of, time_basis, input_refs, inputs_hash, metrics, scenarios, status, basis_label, data_class, engine_versions, engine_versions_hash, mode, operator_id, created_at) VALUES ('checkprobe', 'checkprobe', '2026-09-03 00:00:00', '{}', '[]', 'checkprobe-in2', '{}', '[]', 'available', 'account-state', 'synthetic', '{}', 'checkprobe-eng2', 'RESEARCH', 'checkprobe', '2026-09-03 00:00:00');" -ExactMessage "CHECK"

    $EmptyAfter2 = Invoke-Py -PyArgs @("reportempty2", ${TargetDbPath}) -Label "B7 BE-6 tables empty after probes"
    if ((Norm-Text $EmptyAfter2).Trim() -ne "PASS:be6_tables_empty") {
        throw "FAIL: B7 - the BE-6 tables are not empty after the probes."
    }
    $EmptyAfter5 = Invoke-Py -PyArgs @("reportempty5", ${TargetDbPath}) -Label "B7 BE-5 tables still empty after probes"
    if ((Norm-Text $EmptyAfter5).Trim() -ne "PASS:be5_tables_empty") {
        throw "FAIL: B7 - the BE-5 tables are not empty after the probes."
    }
    Write-Evidence "PASS: B7 - all four BE-6 guard refusals observed with the exact pinned messages; the inherited compver guards intact on the new seed row; both uniqueness anchors proven behaviorally; all three CHECK probes refused; throwaway rows rolled back; tables confirmed empty."

    # -----------------------------------------------------------------
    # B8. AUTHORITY VARIABLES (absent)
    # -----------------------------------------------------------------

    Write-Section "B8. AUTHORITY VARIABLES (absent)"

    $EnvCheck = @(Get-ChildItem Env: | Where-Object { $_.Name -like 'AXIOM_TD_*' -or $_.Name -like '*AUTHORITY_REF*' } | ForEach-Object { $_.Name })
    if ($EnvCheck.Count -ne 0) {
        throw "FAIL: B8 - authority/TD environment variables present: $($EnvCheck -join ', ')."
    }
    Write-Evidence "PASS: B8 - no AXIOM_TD_* / authority variables exist in this process (neither set nor observed)."

    # -----------------------------------------------------------------
    # B9. DRIFT: alembic check (format-independent - PGF-014)
    # -----------------------------------------------------------------

    Write-Section "B9. DRIFT: alembic check (expected: exactly the 9 inherited V1 tokens; zero BE-6/V2 tokens)"

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
        throw "FAIL: B9 (T-10) - alembic check reported no drift (exit 0); expected the inherited V1 drift set to persist (non-zero exit)."
    }
    if ($DriftText -like "*not up to date*") {
        throw "FAIL: B9 (T-10) - alembic check printed the revision-offset refusal form at the HEAD revision; the chain state is inconsistent. Report to ITRGA."
    }
    $DriftBanPattern = "v2_portfolio_definition|v2_portfolio_risk_report|pfdef|pfrisk|v2_ml_governance_record|v2_ml_lifecycle_event|v2_ml_diagnostic_report|v2_signal_record|v2_signal_state_event|mlgov|mlev|mldiag|sigev|v2_md_|v2_permission|v2_computation_version|v2_market_context|v2_chart_intelligence|v2_audit_event|v2_lineage_record|ix_v2_"
    if ($DriftText -match $DriftBanPattern) {
        throw "FAIL: B9 (T-10) - V2/BE-6 drift token detected in alembic check output."
    }

    $DriftNameMatches = @()
    $DriftNameMatches += [regex]::Matches($DriftText, '(?:added|removed) (?:table|index) [''"]?([A-Za-z0-9_]+)[''"]?')
    $DriftNameMatches += [regex]::Matches($DriftText, '(?:Table|Index)\(''([A-Za-z0-9_]+)''')
    $DriftNames = @($DriftNameMatches | ForEach-Object { $_.Groups[1].Value })

    if ($DriftNames.Count -gt 0) {
        foreach ($Token in $ExpectedDriftTokens) {
            if ($DriftText -notlike "*${Token}*") {
                throw "FAIL: B9 (T-10) - expected inherited V1 drift token missing from alembic check output: ${Token}."
            }
        }
        $UnexpectedDriftNames = @($DriftNames | Where-Object { $ExpectedDriftTokens -notcontains $_ })
        if ($UnexpectedDriftNames.Count -ne 0) {
            throw "FAIL: B9 (T-10) - unexpected drift token(s) beyond the 9 inherited V1 tokens: $($UnexpectedDriftNames -join ', ')."
        }
        $DriftNote = "itemized format: the token set is exactly the 9 inherited V1 tokens - all present, no extras, no v2_* or ix_v2_ token"
    } else {
        if ($DriftText -notlike "*New upgrade operations detected*") {
            throw "FAIL: B9 (T-10) - expected a recorded drift marker in alembic check output; observed: '${DriftText}'."
        }
        $DriftNote = "summary format (PGF-014): drift existence asserted (non-zero exit + a recorded drift marker); no V2/BE-5/BE-6 token anywhere; the exact token set stands per the Level-II test evidence and the recorded lineage"
    }

    Write-Evidence "PASS: B9 (T-10) - alembic check: ${DriftNote}."

    # -----------------------------------------------------------------
    # B10. FINAL VERIFY VERDICT
    # -----------------------------------------------------------------

    Write-Section "B10. FINAL VERIFY VERDICT"

    $IntegrityFinal = Invoke-Py -PyArgs @("scalar", ${TargetDbPath}, "PRAGMA integrity_check;") -Label "B10 integrity check"
    if ((Norm-Text $IntegrityFinal).Trim() -ne "ok") {
        throw "FAIL: B10 - final integrity_check not 'ok'."
    }

    Write-Evidence ""
    Write-Evidence "VERIFY VERDICT: PASS - the working database in '${TargetDbPath}' is byte-identical to the PASS-state recorded by the apply act and independently re-proves the BO-V2-BE-6-001 terminal state on the working lineage: revision exactly 20260903_0046 (transcript of record attests the single sanctioned upgrade); 32 v2 triggers exact-named (28 inherited intact + 4 BE-6 guards exact-messaged); both BE-6 tables with the pinned column name-sets, PK 'id', all seven named constraints in the stored DDL, both uniqueness anchors PROVEN BEHAVIORALLY and both indexes exact-named; 6 computation-version rows (BE-4 pinned by value; mge/sge and portfolio_risk_engine runtime-recomputed, the BE-6 recomputation equal to the pinned anchor); 41 permission rows (6 additive BE-6 exact, no duplicates); both BE-6 tables empty and all five BE-5 tables still empty; inherited BE-1..BE-3 anchors content-exact; drift exactly the 9 inherited V1 tokens with zero BE-6/V2 tokens; no authority variable present; recovery anchor (current-as-is, pre-act disclosure N-1) verified byte-exact against the apply record."
    Write-Evidence "Transcript: ${Transcript}"
    Write-Evidence ""
    Write-Evidence "EVIDENCE ENVELOPE TO SEND TO ITRGA (closes the 0046 application act):"
    Write-Evidence "  operator-evidence\BE-6\0046-APPLY-RUN-V1.txt"
    Write-Evidence "  operator-evidence\BE-6\0046-VERIFY-RUN-V1.txt"
    Write-Evidence "The application may now be restarted."

} catch {
    Write-Evidence ""
    Write-Evidence "VERIFY VERDICT: FAIL - RUN ABORTED: $($_.Exception.Message)"
    Write-Evidence "Transcript: ${Transcript}"
    Write-Host ""
    Write-Host "VERIFY FAILED. Do not edit anything in the repository (and do NOT treat the C-2 evidence envelope as delivered)."
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

    Write-Host "Environment cleaned; helper removed."
}
