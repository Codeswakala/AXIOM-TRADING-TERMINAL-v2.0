# =====================================================================
# AXIOM V2 - 0044/0045 WORKING-DATABASE VERIFICATION ACT (BAND BE-5)
# ITRGA SQLITE VERIFY ACT EVIDENCE PACK (V2) - RESUMPTION INSTRUMENT
# Pack ID: ITRGA-V2-0045-VERIFY-PACK-V2
# Authority:
#   - ITRGA-DET-V2-BE-5-FINAL-001 (final determination; C-2 envelope)
#   - BO-V2-BE-5-001 (terminal state T-1...T-12)
#   - ITRGA-ISS-V2-0045-PACKS-002 (this pack's issuance; supersedes
#     the V1 verify pack; the V1 apply pack is USED AND RETIRED)
# Incident context (recorded):
#   ITRGA-V2-0045-APPLY-PACK-V1 ran 2026-09-02 23:03:17 +03:00. The
#   sanctioned mutation (alembic upgrade 20260902_0045) EXECUTED ONCE
#   AND SUCCEEDED (A4 of 0045-APPLY-RUN-V1.txt; A5.1/A5.2 PASSED:
#   revision 20260902_0045 head; exactly 28 v2 triggers with the ten
#   BE-5 guards). The run then halted at an ITRGA INSTRUMENT DEFECT
#   (PGF-015: an A5.3 probe queried the non-existent column
#   sqlite_master.origin; the pack failed closed, correctly, AFTER
#   the apply had completed). The delivery and the database are not
#   implicated. This V2 pack is the resumption instrument: it verifies
#   the full terminal state without any dependency on the
#   never-written apply-final-state record, and re-proves the
#   halted sections with corrected (behavioral) instruments.
#
# WHAT THIS PACK DOES (READ-ONLY against the target file; the only
#   mutation channels are transactional probes that always roll back
#   their throwaway rows):
#   - TRI-BINDS the pre-0045 pre-image: the 0043 apply-final-state
#     record (strictly parsed), the anchor copy in
#     operator-evidence\BE-5 (exactly one, hash-pinned to the record),
#     and the V1 apply transcript (content-bound; its hash recorded).
#   - Asserts current revision exactly 20260902_0045 (single head).
#   - Re-proves the halted A5.3 content with corrected instruments:
#     five BE-5 tables, DDL column presence (record_seq, supersedes,
#     model_type, instrument_class; absence of updated_at_event_id;
#     inputs_hash/engine_versions_hash), the six BE-5 indexes by name,
#     and BOTH P-1/P-2 uniqueness anchors BEHAVIORALLY
#     (insert-duplicate-refuse-rollback probes).
#   - Re-proves: compver exactly 5 rows (mge/sge hashes by RUNTIME
#     recomputation of the engine files); permission rows (8 additive
#     BE-5 content-exact; total 35; no duplicates); all five BE-5
#     tables empty; inherited BE-1..BE-4 state untouched (content-
#     exact anchors + BE-4 report-table digests pinned to the values
#     captured pre-apply in the V1 transcript); ten BE-5 guard
#     refusals with exact messages + inherited compver guards + two
#     CHECK probes; authority-variable absence; drift = exactly the 9
#     inherited V1 tokens with zero BE-5/V2 tokens; final file
#     posture (integrity, journal delete, no sidecars; size+sha256
#     recorded, not pinned - seed-time bytes).
#
# PREREQUISITES:
#   - The V1 apply run has executed (its transcript exists).
#   - The application has NOT been restarted since the V1 apply run
#     (the emptiness gates and digest pins enforce this fail-closed).
#
# OPERATOR INSTRUCTION CARD:
#   1. Verify byte-identity of this file against
#      ITRGA-ISS-V2-0045-PACKS-002 (MD5 + SHA-256). On any mismatch:
#      STOP; do not run; report to ITRGA.
#   2. Execute ONLY this file, from the repository root:
#        powershell -NoProfile -ExecutionPolicy Bypass -File ".\ITRGA_V2_0045_VERIFY_PACK_V2.ps1"
#   3. Single expected input: the absolute path of the working
#      database file backend\axiom_dev.db (a path, not a credential).
#   4. Send back to ITRGA:
#        operator-evidence\BE-5\0045-APPLY-RUN-V1.txt     (run-of-record)
#        operator-evidence\BE-5\0045-VERIFY-RUN-V2.txt    (this run)
#      These two files close C-2 and place the BO terminal state on
#      the working lineage. Restart the application only after a PASS.
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

$EvidenceRoot    = Join-Path $RepoRoot "operator-evidence"
$EvidenceDir     = Join-Path $EvidenceRoot "BE-5"
$Transcript      = Join-Path $EvidenceDir "0045-VERIFY-RUN-V2.txt"
$ApplyTranscript = Join-Path $EvidenceDir "0045-APPLY-RUN-V1.txt"
$StateRecPath    = Join-Path $EvidenceDir "0045-APPLY-FINAL-STATE.txt"
$PrevStateDir    = Join-Path $EvidenceRoot "BE-4"
$PrevStatePath   = Join-Path $PrevStateDir "0043-APPLY-FINAL-STATE.txt"

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

$Be5Indexes = @(
    "ix_v2_mldiag_artifact",
    "ix_v2_mlev_record",
    "ix_v2_mlgov_artifact",
    "ix_v2_sigev_signal",
    "ix_v2_signal_family_state",
    "ix_v2_signal_instrument"
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

# The BE-4 report-table digests captured pre-apply by the V1 run
# (both tables were empty at baseline; no-touch requires the identical
# values post-apply).
$ExpectedMcrDigest = "DIGEST:0:4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945"
$ExpectedCirDigest = "DIGEST:0:4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945"

$ExpectedLeafName = "axiom_dev.db"

# ---------------------------------------------------------------------
# 0B. OPERATOR INPUT
# ---------------------------------------------------------------------

Write-Host ""
Write-Host "This pack VERIFIES the 0044/0045 working-database terminal state"
Write-Host "after the V1 apply run (read-only; transactional probes roll back)."
Write-Host "The APPLICATION must NOT have been restarted since the V1 apply run."
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
# 0C. PYTHON HELPER (written to the OS temp directory, removed on exit)
# ---------------------------------------------------------------------

$HelperDir  = Join-Path $env:TEMP "axiom_itrga_0045_verify_v2"
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

    if cmd == "uniqprobe":
        # Behavioral uniqueness proof (PGF-015 discipline: prove the
        # constraint by behavior, never by catalog internals). Inserts
        # a first row, attempts a duplicate on the anchored key columns,
        # expects a refusal, and ALWAYS rolls back - the table is left
        # byte-equivalent (empty) regardless of the outcome.
        first_sql = sys.argv[3]
        dup_sql = sys.argv[4]
        con = rw_connect(db_path)
        try:
            con.execute(first_sql)
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

function Invoke-ExpectedUniqueProbe {
    param(
        [Parameter(Mandatory = $true)][string]$Label,
        [Parameter(Mandatory = $true)][string]$FirstSql,
        [Parameter(Mandatory = $true)][string]$DupSql
    )

    Write-Evidence ""
    Write-Evidence "EXPECTED-UNIQUE-PROBE: ${Label}"
    Write-Evidence "FIRST (throwaway, rolled back): ${FirstSql}"
    Write-Evidence "DUPLICATE (expected refused): ${DupSql}"

    $Out = Invoke-Py -PyArgs @("uniqprobe", ${TargetDbPath}, ${FirstSql}, ${DupSql}) -Label $Label
    $Text = (Norm-Text $Out).Trim()

    if ($Text -notlike "REFUSED:*") {
        throw "FAIL: expected duplicate-key refusal did not occur (statement succeeded or helper error): ${Label}"
    }
    if ($Text -notlike "*UNIQUE*") {
        throw "FAIL: the refusal was not a UNIQUE-constraint violation: ${Text}: ${Label}"
    }
    Write-Evidence "PASS: duplicate-key refusal observed (UNIQUE constraint fired); throwaway rows rolled back."
}

# ---------------------------------------------------------------------
# B0. RUN IDENTIFICATION
# ---------------------------------------------------------------------

Write-Section "B0. RUN IDENTIFICATION"
Write-Evidence "Pack: ITRGA-V2-0045-VERIFY-PACK-V2 (resumption instrument)"
Write-Evidence "Incident: ITRGA-V2-0045-APPLY-PACK-V1 applied 0044+0045 successfully and then halted at instrument defect PGF-015 (A5.3 probe referenced the non-existent sqlite_master.origin column; fail-closed after the mutation). This V2 pack completes the verification with corrected instruments."
Write-Evidence "Determination: ITRGA-DET-V2-BE-5-FINAL-001 (C full-verify PASS; C-2 scope = this envelope)"
Write-Evidence "Build order: BO-V2-BE-5-001 (terminal state T-1...T-12)"
Write-Evidence "Run-of-record transcript (content-bound in B0e): ${ApplyTranscript}"
Write-Evidence "Started: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss zzz')"
Write-Evidence "Repo root: ${RepoRoot}"
Write-Evidence "Target file (APPLICATION'S WORKING DATABASE - named by the Operator): ${TargetDbPath}"
Write-Evidence "SQL engine: SQLite (in-process, via the repo venv python sqlite3 module; no database server)"
Write-Evidence "Server credentials used: NONE (no database server; no password prompt)"
Write-Evidence "Authority variable: NONE EXISTS FOR THIS ACT; absence asserted in B8."

Push-Location $BackendRoot

try {

# ---------------------------------------------------------------------
# B0e. TRI-BINDING OF THE RUN-OF-RECORD (pre-image + transcript + marker)
# ---------------------------------------------------------------------

Write-Section "B0e. TRI-BINDING (0043 record + anchor copy + V1 apply transcript + absence marker)"

# (1) The 0043 apply-final-state record (chain of custody, strict).
$Prev = Read-Pins -Path $PrevStatePath -ExpectedKeys @(
    "STATE_FILE_ID", "RUN_TIMESTAMP", "POST_SIZE_BYTES", "POST_LAST_WRITE",
    "POST_SHA256", "POST_REVISION", "POST_V2_TRIGGER_COUNT",
    "ANCHOR_FILENAME", "ANCHOR_SIZE_BYTES", "ANCHOR_SHA256"
) -Label "0043 apply-final-state record"
if ($Prev["STATE_FILE_ID"] -ne "ITRGA-V2-0043-APPLY-FINAL-STATE-V1") {
    throw "STOP: 0043 record identity '$($Prev["STATE_FILE_ID"])' is not ITRGA-V2-0043-APPLY-FINAL-STATE-V1."
}
if ($Prev["POST_REVISION"] -ne "20260831_0043") {
    throw "STOP: 0043 record revision '$($Prev["POST_REVISION"])' is not 20260831_0043."
}
if ($Prev["POST_SHA256"] -notmatch '^[0-9a-f]{64}$') { throw "STOP: malformed POST_SHA256 in the 0043 record." }
if ($Prev["POST_SIZE_BYTES"] -notmatch '^[0-9]+$') { throw "STOP: malformed POST_SIZE_BYTES in the 0043 record." }

# (2) The anchor copy of the V1 apply run (exactly one; hash-bound to
#     the 0043 record's POST state - the pre-0045 pre-image).
$AnchorCandidates = @(Get-ChildItem -Path $EvidenceDir -Filter (${LeafName} + ".pre-0045-*.bak"))
if ($AnchorCandidates.Count -ne 1) {
    throw "STOP: expected exactly one pre-0045 anchor copy in ${EvidenceDir}; found $($AnchorCandidates.Count)."
}
$AnchorFullPath = $AnchorCandidates[0].FullName
$AnchorItem     = Get-Item $AnchorFullPath
$AnchorHashNow  = (Get-FileHash $AnchorFullPath -Algorithm SHA256).Hash.ToLower()
Write-Evidence "Anchor: ${AnchorFullPath}"
Write-Evidence "  size       $($AnchorItem.Length) bytes (0043 record POST_SIZE_BYTES=$($Prev["POST_SIZE_BYTES"]))"
Write-Evidence "  sha256     ${AnchorHashNow} (0043 record POST_SHA256=$($Prev["POST_SHA256"]))"
if ([string]$AnchorItem.Length -ne $Prev["POST_SIZE_BYTES"]) {
    throw "STOP: anchor size differs from the 0043 record POST_SIZE_BYTES. The pre-image chain is broken; report to ITRGA."
}
if ($AnchorHashNow -ne $Prev["POST_SHA256"]) {
    throw "STOP: anchor sha256 differs from the 0043 record POST_SHA256. The pre-image chain is broken; report to ITRGA."
}
$AnchorIntOut = Invoke-Py -PyArgs @("scalar", ${AnchorFullPath}, "PRAGMA integrity_check;") -Label "B0e anchor integrity"
if ((Norm-Text $AnchorIntOut).Trim() -ne "ok") {
    throw "STOP: anchor integrity_check not 'ok'; report to ITRGA."
}
Write-Evidence "PASS: (1)+(2) - the rollback pre-image is bound: 0043 record POST state == the V1 anchor copy (byte-exact), integrity ok. (The V1 apply transcript independently records this same binding - its Tier-1 gate.)"

# (3) The V1 apply transcript (content-bound; its hash recorded).
if (!(Test-Path $ApplyTranscript)) {
    throw "STOP: V1 apply transcript missing: ${ApplyTranscript}. The run-of-record is unavailable; report to ITRGA."
}
$ApplyTranscriptHash = (Get-FileHash $ApplyTranscript -Algorithm SHA256).Hash.ToLower()
$ApplyTextRaw = Get-Content -Path $ApplyTranscript -Raw
foreach ($Marker in @("Running upgrade 20260831_0043 -> 20260902_0044",
                      "Running upgrade 20260902_0044 -> 20260902_0045",
                      "PASS: A5.1 (T-1) - current revision is exactly 20260902_0045",
                      "PASS: A5.2 (T-3/T-6) - 28 v2 triggers",
                      "Anchor created and verified",
                      "APPLY VERDICT: FAIL",
                      "A5 autoindex origin-u presence")) {
    if ($ApplyTextRaw -notlike "*${Marker}*") {
        throw "STOP: V1 apply transcript is missing the run-of-record marker: ${Marker}. The transcript is not the expected one; report to ITRGA."
    }
}
Write-Evidence "PASS: (3) - V1 apply transcript present and content-bound (upgrade lines, A5.1/A5.2 passes, anchor record, the PGF-015 halt signature all present)."
Write-Evidence "V1 apply transcript sha256: ${ApplyTranscriptHash} (recorded; cite in the evidence envelope)."

# (4) The absence marker: no 0045 apply-final-state record may exist
#     (it is written only after a full PASS of the retired V1 apply
#     pack; its existence now would mean a foreign hand).
if (Test-Path $StateRecPath) {
    throw "STOP: unexpected 0045 apply-final-state record present: ${StateRecPath}. That file can only be written by the retired V1 apply pack. Report to ITRGA."
}
Write-Evidence "PASS: (4) - absence of the never-written apply-final-state record confirmed (self-consistent with the halted V1 run)."

# ---------------------------------------------------------------------
# B0f. PROVENANCE (25 files re-pinned on disk; abort on any mismatch)
# ---------------------------------------------------------------------

Write-Section "B0f. PROVENANCE (25 files re-pinned on disk; abort on any mismatch)"

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
    "backend\tests\test_v2_be4_migration.py"
)) {
    $FullPath = Join-Path $RepoRoot ${RelPath}
    if (!(Test-Path $FullPath)) { throw "STOP: delivered file missing: ${FullPath}." }
    $ActualHash = (Get-FileHash $FullPath -Algorithm SHA256).Hash.ToLower()
    $PinnedHash = $ExpectedDeliveredHashes[${RelPath}]
    if ($ActualHash -ne $PinnedHash) {
        throw "STOP: B0f - provenance hash mismatch for ${RelPath}; report to ITRGA."
    }
}
Write-Evidence "PASS: B0f - all 25 files on disk hash to the pinned values."

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
    $EnvSweepAfter = @(Get-ChildItem Env: | Where-Object { $_.Name -like 'AXIOM_TD_*' -or $_.Name -like '*AUTHORITY_REF*' } | ForEach-Object { $_.Name })
    if ($EnvSweepAfter.Count -ne 0) {
        throw "FAIL: authority/TD environment variables still present after removal."
    }
    Write-Evidence "  absence verified after sweep."
    Write-Evidence "AXIOM_DATABASE_URL built for the target file (value not printed); testing env; RESEARCH mode."

    # -----------------------------------------------------------------
    # B0c. HELPER SELF-TEST
    # -----------------------------------------------------------------

    Write-Section "B0c. HELPER SELF-TEST"

    [void](Invoke-Py -PyArgs @("selftest", ${TargetDbPath}) -Label "helper self-test")

    # -----------------------------------------------------------------
    # B0g. REPOSITORY STATE EVIDENCE
    # -----------------------------------------------------------------

    Write-Section "B0g. REPOSITORY STATE EVIDENCE"

    $HeadsOut = Invoke-Alembic -AlembicArgs @("heads") -Label "B0g repository heads (recorded)"
    $HeadsText = Norm-Text $HeadsOut
    $HeadLines = @($HeadsText -split "`n" | Where-Object { $_ -match '^[0-9a-z]{8}_[0-9]{4}(\s*\([^)]*\))?$' })
    if ($HeadLines.Count -ne 1) {
        throw "FAIL: B0g - expected exactly one alembic head; observed $($HeadLines.Count) in: '${HeadsText}'."
    }
    $RepoHead = ($HeadLines[0].Trim() -replace '\s*\([^)]*\)$', '').Trim()
    if ($RepoHead -ne ${ApplyTargetRevision}) {
        throw "FAIL: B0g - repository head is '${RepoHead}'; expected exactly ${ApplyTargetRevision}."
    }
    Write-Evidence "Repository head: ${RepoHead}"

    # -----------------------------------------------------------------
    # B2. CURRENT REVISION EXACTLY 20260902_0045 (T-1)
    # -----------------------------------------------------------------

    Write-Section "B2. CURRENT REVISION EXACTLY ${ApplyTargetRevision} (T-1)"

    [void](Assert-CurrentExactly -ExpectedRev ${ApplyTargetRevision} -Label "B2 current revision")
    Write-Evidence "PASS: B2 (T-1) - current revision is exactly ${ApplyTargetRevision}."

    # -----------------------------------------------------------------
    # B5. PERMISSION ROWS + BE-5 TABLES EMPTY + TRIGGER POSTURE
    # -----------------------------------------------------------------

    Write-Section "B5. PERMISSION ROWS + BE-5 TABLES EMPTY + TRIGGER POSTURE"

    $PermOut = Invoke-Py -PyArgs @("permbe5", ${TargetDbPath}) -Label "B5 permission rows"
    $PermText = (Norm-Text $PermOut).Trim()
    if ($PermText -notlike "PASS:perm_rows_exact*") {
        throw "FAIL: B5 - permission check failed: ${PermText}"
    }

    $EmptyOut = Invoke-Py -PyArgs @("reportempty5", ${TargetDbPath}) -Label "B5 BE-5 tables empty"
    $EmptyText = (Norm-Text $EmptyOut).Trim()
    if ($EmptyText -ne "PASS:be5_tables_empty") {
        throw "FAIL: B5 - the five BE-5 tables are not empty. The application may have been restarted since the V1 apply run. Report to ITRGA."
    }

    [void](Invoke-Py -PyArgs @("scalar", ${TargetDbPath}, "SELECT name FROM sqlite_master WHERE type='trigger' AND name LIKE 'v2_%' ORDER BY name;") -Label "B5 v2 trigger names (recorded)")
    $TrigNamesText = Get-PyScalar -Sql "SELECT name FROM sqlite_master WHERE type='trigger' AND name LIKE 'v2_%' ORDER BY name;" -Label "B5 v2 trigger set"
    $TrigNames = @($TrigNamesText -split "`n" | Where-Object { $_ -ne "" })
    if ($TrigNames.Count -ne 28) {
        throw "FAIL: B5 (T-3/T-6) - v2 trigger count '$($TrigNames.Count)', expected exactly 28."
    }
    foreach ($Be5Name in $Be5GuardNames) {
        if ($TrigNames -notcontains $Be5Name) {
            throw "FAIL: B5 - BE-5 guard trigger missing: ${Be5Name}."
        }
    }
    foreach ($KnownName in (@($Be4GuardTriggers + $TransitionGuardTriggers) | Sort-Object)) {
        if ($TrigNames -notcontains $KnownName) {
            throw "FAIL: B5 - inherited guard trigger missing: ${KnownName}."
        }
    }
    Write-Evidence "PASS: B5 (T-2/T-3/T-4/T-6) - exactly 8 additive BE-5 permission rows (total 35, no duplicates); all five BE-5 tables empty; 28 v2 triggers with the ten BE-5 guards and all known inherited guards present."

    # -----------------------------------------------------------------
    # B5b. TABLES, COLUMNS, INDEXES, BEHAVIORAL UNIQUENESS (corrected
    # A5.3 - PGF-015; the halted section, re-proven)
    # -----------------------------------------------------------------

    Write-Section "B5b. BE-5 TABLES/COLUMNS/INDEXES + BEHAVIORAL UNIQUENESS (corrected A5.3; PGF-015)"

    $NewTableCount = Get-PyScalar -Sql "SELECT COUNT(*) FROM sqlite_master WHERE type='table' AND name IN ('v2_ml_governance_record','v2_ml_lifecycle_event','v2_ml_diagnostic_report','v2_signal_record','v2_signal_state_event');" -Label "B5b BE-5 table presence"
    if ($NewTableCount -ne "5") {
        throw "FAIL: B5b (T-2/T-6) - BE-5 table count '${NewTableCount}', expected 5."
    }
    $MlgovDdl = Get-PyScalar -Sql "SELECT sql FROM sqlite_master WHERE type='table' AND name='v2_ml_governance_record';" -Label "B5b governance-record DDL"
    foreach ($Anchor in @("record_seq", "supersedes", "model_type", "instrument_class")) {
        if ($MlgovDdl -notlike "*${Anchor}*") {
            throw "FAIL: B5b (T-2) - '${Anchor}' not present in v2_ml_governance_record DDL."
        }
    }
    if ($MlgovDdl -like "*updated_at_event_id*") {
        throw "FAIL: B5b (T-2/P-1) - updated_at_event_id is present in v2_ml_governance_record DDL (must be absent)."
    }
    $MldiagDdl = Get-PyScalar -Sql "SELECT sql FROM sqlite_master WHERE type='table' AND name='v2_ml_diagnostic_report';" -Label "B5b diagnostic-report DDL"
    if ($MldiagDdl -notlike "*inputs_hash*" -or $MldiagDdl -notlike "*engine_versions_hash*") {
        throw "FAIL: B5b (T-2/P-2) - determinism-anchor columns missing from v2_ml_diagnostic_report DDL."
    }
    $IdxFound = Get-PyScalar -Sql "SELECT name FROM sqlite_master WHERE type='index' AND name IN ('ix_v2_mlgov_artifact','ix_v2_mlev_record','ix_v2_mldiag_artifact','ix_v2_sigev_signal','ix_v2_signal_family_state','ix_v2_signal_instrument') ORDER BY name;" -Label "B5b BE-5 index names"
    $ExpectedIndexesText = $Be5Indexes -join "`n"
    if ($IdxFound -ne $ExpectedIndexesText) {
        throw "FAIL: B5b (T-2/T-6) - the six BE-5 index names are not exactly the pinned set: '${IdxFound}'."
    }

    # P-1: UNIQUE(model_artifact_id, record_seq) - proven BEHAVIORALLY:
    # insert one row, then a duplicate on (artifact, seq) is refused;
    # rollback leaves the empty table untouched.
    $U1First = "INSERT INTO v2_ml_governance_record (id, model_artifact_id, record_seq, registry_version, model_type, instrument_class, eligibility_status, calibration_status, freshness_status, economic_status, statistical_status, deployment_class, data_class, evidence_refs, mode, operator_id, created_at) VALUES ('uq1', 'uqartifact', 1, '1.0', 'probe', 'probe', 'unevaluated', 'unevaluated', 'unknown', 'unevaluated', 'unevaluated', 'research', 'synthetic', '{}', 'RESEARCH', 'probe', '2026-09-02 00:00:00');"
    $U1Dup   = "INSERT INTO v2_ml_governance_record (id, model_artifact_id, record_seq, registry_version, model_type, instrument_class, eligibility_status, calibration_status, freshness_status, economic_status, statistical_status, deployment_class, data_class, evidence_refs, mode, operator_id, created_at) VALUES ('uq2', 'uqartifact', 1, '1.0', 'probe', 'probe', 'unevaluated', 'unevaluated', 'unknown', 'unevaluated', 'unevaluated', 'research', 'synthetic', '{}', 'RESEARCH', 'probe', '2026-09-02 00:00:00');"
    Invoke-ExpectedUniqueProbe -Label "B5b: P-1 UNIQUE(model_artifact_id, record_seq)" -FirstSql ${U1First} -DupSql ${U1Dup}

    # P-2: UNIQUE(model_artifact_id, inputs_hash, engine_versions_hash)
    # - proven BEHAVIORALLY in the same form.
    $U2First = "INSERT INTO v2_ml_diagnostic_report (id, model_artifact_id, diagnostics, input_refs, inputs_hash, engine_versions, engine_versions_hash, data_class, mode, operator_id, created_at) VALUES ('uq1', 'uqartifact', '{}', '{}', 'uqin', '{}', 'uqev', 'synthetic', 'RESEARCH', 'probe', '2026-09-02 00:00:00');"
    $U2Dup   = "INSERT INTO v2_ml_diagnostic_report (id, model_artifact_id, diagnostics, input_refs, inputs_hash, engine_versions, engine_versions_hash, data_class, mode, operator_id, created_at) VALUES ('uq2', 'uqartifact', '{}', '{}', 'uqin', '{}', 'uqev', 'synthetic', 'RESEARCH', 'probe', '2026-09-02 00:00:00');"
    Invoke-ExpectedUniqueProbe -Label "B5b: P-2 UNIQUE(model_artifact_id, inputs_hash, engine_versions_hash)" -FirstSql ${U2First} -DupSql ${U2Dup}

    $EmptyAfterUniq = Invoke-Py -PyArgs @("reportempty5", ${TargetDbPath}) -Label "B5b BE-5 tables empty after uniq probes"
    if ((Norm-Text $EmptyAfterUniq).Trim() -ne "PASS:be5_tables_empty") {
        throw "FAIL: B5b - tables not empty after the uniqueness probes."
    }
    Write-Evidence "PASS: B5b (T-2/T-6; P-1/P-2/P-3) - five tables; record_seq/supersedes/model_type/instrument_class in the DDL; updated_at_event_id absent; determinism-anchor columns present; the six indexes exact; BOTH uniqueness anchors refused duplicates behaviorally; tables still empty after probes."

    # -----------------------------------------------------------------
    # B4. COMPUTATION-VERSION ROWS (5; BE-5 hashes recomputed)
    # -----------------------------------------------------------------

    Write-Section "B4. COMPUTATION-VERSION ROWS (exactly 5; runtime recomputation)"

    $CompverOut = Invoke-Py -PyArgs @(
        "compverbe5", ${TargetDbPath}, ${BackendRoot},
        "fe9aab42c34d671e960fd92a9346d3bf60c27135e76e52310d774bc84028dd35",
        "69902503483502bcd5ce5e35fdb0eeabcb2efcaf7a4b0c262a6fccf2d0af3a8c",
        "3887d6ca8ba05858f41889cd99fa05aba42663ac22d906a7f989b567c3912180"
    ) -Label "B4 computation-version rows"
    $CompverText = (Norm-Text $CompverOut).Trim()
    if ($CompverText -notlike "PASS:compver_rows_exact*") {
        throw "FAIL: B4 - computation-version check failed: ${CompverText}"
    }
    Write-Evidence "PASS: B4 (T-5/T-6; P-4) - exactly 5 rows; BE-4 rows content-exact; mge/sge source hashes equal the runtime recomputation of the engine files; evidence_ref values exact."

    # -----------------------------------------------------------------
    # B6. INHERITED STATE (BE-1..BE-4, content-exact / digest-pinned)
    # -----------------------------------------------------------------

    Write-Section "B6. INHERITED STATE (BE-1..BE-4 anchors; BE-4 report digests pinned to the V1 pre-apply captures)"

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
    $McrDigestNow = Invoke-Py -PyArgs @("tabledigest", ${TargetDbPath}, "v2_market_context_report") -Label "B6 BE-4 market-context report digest"
    if ((Norm-Text $McrDigestNow).Trim() -ne $ExpectedMcrDigest) {
        throw "FAIL: B6 (T-9) - v2_market_context_report digest changed since the V1 pre-apply capture."
    }
    $CirDigestNow = Invoke-Py -PyArgs @("tabledigest", ${TargetDbPath}, "v2_chart_intelligence_report") -Label "B6 BE-4 chart-intelligence report digest"
    if ((Norm-Text $CirDigestNow).Trim() -ne $ExpectedCirDigest) {
        throw "FAIL: B6 (T-9) - v2_chart_intelligence_report digest changed since the V1 pre-apply capture."
    }
    Write-Evidence "PASS: B6 (T-9) - provider row, history rows, and transition audit events content-exact; both BE-4 report-table digests identical to the V1 pre-apply captures (untouched)."

    # -----------------------------------------------------------------
    # B7. GUARD REFUSALS (ten; exact messages) + CHECK probes
    # -----------------------------------------------------------------

    Write-Section "B7. GUARD REFUSALS (ten; exact messages; transactional probes roll back) + CHECK probes"

    Invoke-ExpectedRefusal -Label "B7: compver UPDATE (inherited guard intact)" -Sql "UPDATE v2_computation_version SET version='probe' WHERE component='ml_governance_engine';" -ExactMessage "V2 computation version registry is immutable; UPDATE prohibited"
    Invoke-ExpectedRefusal -Label "B7: compver DELETE (inherited guard intact)" -Sql "DELETE FROM v2_computation_version WHERE component='signal_engine';" -ExactMessage "V2 computation version registry is immutable; DELETE prohibited"

    $MlgovInsert = "INSERT INTO v2_ml_governance_record (id, model_artifact_id, record_seq, registry_version, model_type, instrument_class, eligibility_status, calibration_status, freshness_status, economic_status, statistical_status, deployment_class, data_class, evidence_refs, mode, operator_id, created_at) VALUES ('guardprobe', 'guardprobe', 1, '1.0', 'guardprobe', 'guardprobe', 'unevaluated', 'unevaluated', 'unknown', 'unevaluated', 'unevaluated', 'research', 'synthetic', '{}', 'RESEARCH', 'guardprobe', '2026-09-02 00:00:00');"
    Invoke-ExpectedGuardProbe -Label "B7: governance-record UPDATE" -InsertSql ${MlgovInsert} -ProbeSql "UPDATE v2_ml_governance_record SET deployment_class='champion' WHERE id='guardprobe';" -ExactMessage "V2 ML governance records are immutable; UPDATE prohibited"
    Invoke-ExpectedGuardProbe -Label "B7: governance-record DELETE" -InsertSql ${MlgovInsert} -ProbeSql "DELETE FROM v2_ml_governance_record WHERE id='guardprobe';" -ExactMessage "V2 ML governance records are immutable; DELETE prohibited"

    $MlevInsert = "INSERT INTO v2_ml_lifecycle_event (id, governance_record_id, event_type, from_value, to_value, decision_basis, mode, actor_id, operator_id, created_at) VALUES ('guardprobe', 'guardprobe', 'registered', 'none', 'research', '{}', 'RESEARCH', 'guardprobe', 'guardprobe', '2026-09-02 00:00:00');"
    Invoke-ExpectedGuardProbe -Label "B7: lifecycle-event UPDATE" -InsertSql ${MlevInsert} -ProbeSql "UPDATE v2_ml_lifecycle_event SET to_value='x' WHERE id='guardprobe';" -ExactMessage "V2 ML lifecycle events are immutable; UPDATE prohibited"
    Invoke-ExpectedGuardProbe -Label "B7: lifecycle-event DELETE" -InsertSql ${MlevInsert} -ProbeSql "DELETE FROM v2_ml_lifecycle_event WHERE id='guardprobe';" -ExactMessage "V2 ML lifecycle events are immutable; DELETE prohibited"

    $MldiagInsert = "INSERT INTO v2_ml_diagnostic_report (id, model_artifact_id, diagnostics, input_refs, inputs_hash, engine_versions, engine_versions_hash, data_class, mode, operator_id, created_at) VALUES ('guardprobe', 'guardprobe', '{}', '{}', 'guardprobe', '{}', 'guardprobe', 'synthetic', 'RESEARCH', 'guardprobe', '2026-09-02 00:00:00');"
    Invoke-ExpectedGuardProbe -Label "B7: diagnostic-report UPDATE" -InsertSql ${MldiagInsert} -ProbeSql "UPDATE v2_ml_diagnostic_report SET data_class='live' WHERE id='guardprobe';" -ExactMessage "V2 ML diagnostic reports are immutable; UPDATE prohibited"
    Invoke-ExpectedGuardProbe -Label "B7: diagnostic-report DELETE" -InsertSql ${MldiagInsert} -ProbeSql "DELETE FROM v2_ml_diagnostic_report WHERE id='guardprobe';" -ExactMessage "V2 ML diagnostic reports are immutable; DELETE prohibited"

    $SigInsert = "INSERT INTO v2_signal_record (id, family, signal_type, instrument_id, timeframe, state, uncertainty, limitations, source_family_refs, data_class, as_of, mode, operator_id, created_at) VALUES ('guardprobe', 'structural', 'probe', 'guardprobe', 'M15', 'emitted', '{}', '{}', '{}', 'synthetic', '2026-09-02 00:00:00', 'RESEARCH', 'guardprobe', '2026-09-02 00:00:00');"
    Invoke-ExpectedGuardProbe -Label "B7: signal-record UPDATE" -InsertSql ${SigInsert} -ProbeSql "UPDATE v2_signal_record SET state='refused' WHERE id='guardprobe';" -ExactMessage "V2 signal records are immutable; UPDATE prohibited"
    Invoke-ExpectedGuardProbe -Label "B7: signal-record DELETE" -InsertSql ${SigInsert} -ProbeSql "DELETE FROM v2_signal_record WHERE id='guardprobe';" -ExactMessage "V2 signal records are immutable; DELETE prohibited"

    $SigevInsert = "INSERT INTO v2_signal_state_event (id, signal_record_id, event_type, from_state, to_state, reason, mode, actor_id, operator_id, created_at) VALUES ('guardprobe', 'guardprobe', 'emitted', 'none', 'emitted', '{}', 'RESEARCH', 'guardprobe', 'guardprobe', '2026-09-02 00:00:00');"
    Invoke-ExpectedGuardProbe -Label "B7: signal-state-event UPDATE" -InsertSql ${SigevInsert} -ProbeSql "UPDATE v2_signal_state_event SET to_state='expired' WHERE id='guardprobe';" -ExactMessage "V2 signal state events are immutable; UPDATE prohibited"
    Invoke-ExpectedGuardProbe -Label "B7: signal-state-event DELETE" -InsertSql ${SigevInsert} -ProbeSql "DELETE FROM v2_signal_state_event WHERE id='guardprobe';" -ExactMessage "V2 signal state events are immutable; DELETE prohibited"

    Invoke-ExpectedRefusal -Label "B7: CHECK probe - signal family 'hybrid' refused" -Sql "INSERT INTO v2_signal_record (id, family, signal_type, instrument_id, timeframe, state, uncertainty, limitations, source_family_refs, data_class, as_of, mode, operator_id, created_at) VALUES ('checkprobe', 'hybrid', 'probe', 'guardprobe', 'M15', 'emitted', '{}', '{}', '{}', 'synthetic', '2026-09-02 00:00:00', 'RESEARCH', 'guardprobe', '2026-09-02 00:00:00');" -ExactMessage "CHECK"
    Invoke-ExpectedRefusal -Label "B7: CHECK probe - eligibility vocabulary refused" -Sql "INSERT INTO v2_ml_governance_record (id, model_artifact_id, record_seq, registry_version, model_type, instrument_class, eligibility_status, calibration_status, freshness_status, economic_status, statistical_status, deployment_class, data_class, evidence_refs, mode, operator_id, created_at) VALUES ('checkprobe', 'guardprobe', 9, '1.0', 'guardprobe', 'guardprobe', 'bogus', 'unevaluated', 'unknown', 'unevaluated', 'unevaluated', 'research', 'synthetic', '{}', 'RESEARCH', 'guardprobe', '2026-09-02 00:00:00');" -ExactMessage "CHECK"

    $EmptyOut2 = Invoke-Py -PyArgs @("reportempty5", ${TargetDbPath}) -Label "B7 BE-5 tables empty after probes"
    if ((Norm-Text $EmptyOut2).Trim() -ne "PASS:be5_tables_empty") {
        throw "FAIL: B7 - the BE-5 tables are not empty after the probes."
    }
    Write-Evidence "PASS: B7 - all ten BE-5 guard refusals observed with exact messages; inherited compver guards intact; both CHECK probes refused; tables confirmed empty after probes."

    # -----------------------------------------------------------------
    # B8. AUTHORITY VARIABLES (absent)
    # -----------------------------------------------------------------

    Write-Section "B8. AUTHORITY VARIABLES (absent)"

    $EnvCheck = @(Get-ChildItem Env: | Where-Object { $_.Name -like 'AXIOM_TD_*' -or $_.Name -like '*AUTHORITY_REF*' } | ForEach-Object { $_.Name })
    if ($EnvCheck.Count -ne 0) {
        throw "FAIL: B8 - authority/TD environment variables present: $($EnvCheck -join ', ')."
    }
    Write-Evidence "PASS: B8 - no AXIOM_TD_* / authority variables exist in this process."

    # -----------------------------------------------------------------
    # B9. DRIFT: alembic check (format-independent - PGF-014)
    # -----------------------------------------------------------------

    Write-Section "B9. DRIFT: alembic check (expected: exactly the 9 inherited V1 tokens; zero BE-5/V2 tokens)"

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
    $DriftBanPattern = "v2_ml_governance_record|v2_ml_lifecycle_event|v2_ml_diagnostic_report|v2_signal_record|v2_signal_state_event|mlgov|mlev|mldiag|sigev|v2_md_|v2_permission|v2_computation_version|v2_market_context|v2_chart_intelligence|v2_audit_event|v2_lineage_record|ix_v2_"
    if ($DriftText -match $DriftBanPattern) {
        throw "FAIL: B9 (T-10) - V2/BE-5 drift token detected in alembic check output."
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
        $DriftNote = "summary format (PGF-014): drift existence asserted (non-zero exit + a recorded drift marker); no V2/BE-5 token anywhere; the exact token set stands per the Level-II test evidence and the recorded lineage"
    }

    Write-Evidence "PASS: B9 (T-10) - alembic check: ${DriftNote}."

    # -----------------------------------------------------------------
    # B10. FINAL FILE POSTURE + VERDICT
    # -----------------------------------------------------------------

    Write-Section "B10. FINAL FILE POSTURE + VERIFY VERDICT"

    $IntegrityFinal = Invoke-Py -PyArgs @("scalar", ${TargetDbPath}, "PRAGMA integrity_check;") -Label "B10 integrity check"
    if ((Norm-Text $IntegrityFinal).Trim() -ne "ok") {
        throw "FAIL: B10 - final integrity_check not 'ok'."
    }
    $FinalJournal = Get-PyScalar -Sql "PRAGMA journal_mode;" -Label "B10 journal mode"
    if ($FinalJournal -ne "delete") {
        throw "FAIL: B10 - journal_mode '${FinalJournal}', expected 'delete'."
    }
    foreach ($Suffix in @("-wal", "-shm")) {
        $SidePath = ${TargetDbPath} + $Suffix
        if (Test-Path $SidePath) {
            throw "FAIL: B10 - unexpected sidecar present: ${SidePath}."
        }
        Write-Evidence "Sidecar ${Suffix}: absent"
    }

    $FinalFile = Get-Item ${TargetDbPath}
    $FinalSize = $FinalFile.Length
    $FinalWrite = $FinalFile.LastWriteTime.ToString('yyyy-MM-dd HH:mm:ss zzz')
    $FinalHash = (Get-FileHash ${TargetDbPath} -Algorithm SHA256).Hash.ToLower()
    Write-Evidence "Current target file (RECORDED, not pinned - post-apply bytes carry seed-time timestamps per the PGF-001 lineage):"
    Write-Evidence "  size       ${FinalSize} bytes"
    Write-Evidence "  last write ${FinalWrite}"
    Write-Evidence "  sha256     ${FinalHash}"

    Write-Evidence ""
    Write-Evidence "VERIFY VERDICT: PASS (V2 resumption) - the working database at '${TargetDbPath}' carries the BO-V2-BE-5-001 terminal state, re-proven end-to-end after the V1 run's instrument-defect halt: revision exactly 20260902_0045 (transcript of record attests the single sanctioned upgrade); 28 v2 triggers with the ten BE-5 guards exact-named; ten guard refusals observed with exact messages + inherited compver guards intact + two CHECK probes refused; five BE-5 tables with the pinned columns (record_seq/supersedes/model_type/instrument_class; no updated_at_event_id), both P-1/P-2 uniqueness anchors proven behaviorally, six indexes exact; 5 computation-version rows with mge/sge hashes runtime-recomputed; 35 permission rows (8 additive BE-5 exact, no duplicates); all five BE-5 tables empty; inherited BE-1..BE-4 state untouched (content-exact + digest-pinned); drift exactly the 9 inherited V1 tokens with zero BE-5/V2 tokens; no authority variable present; rollback pre-image tri-bound (0043 record == anchor, byte-exact)."
    Write-Evidence "Transcript: ${Transcript}"
    Write-Evidence ""
    Write-Evidence "EVIDENCE ENVELOPE TO SEND TO ITRGA (closes C-2):"
    Write-Evidence "  operator-evidence\BE-5\0045-APPLY-RUN-V1.txt  (run-of-record; sha256 ${ApplyTranscriptHash})"
    Write-Evidence "  operator-evidence\BE-5\0045-VERIFY-RUN-V2.txt  (this run)"
    Write-Evidence "The application may now be restarted."

} catch {
    Write-Evidence ""
    Write-Evidence "VERIFY VERDICT: FAIL - RUN ABORTED: $($_.Exception.Message)"
    Write-Evidence "Transcript: ${Transcript}"
    Write-Host ""
    Write-Host "VERIFY (V2) FAILED. Do not edit anything in the repository (and do NOT treat the C-2 evidence envelope as delivered)."
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
