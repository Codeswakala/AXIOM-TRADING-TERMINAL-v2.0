# =====================================================================
# AXIOM V2 BE-3 P2 STATUS TRANSITION - ITRGA APPLY ACT EVIDENCE PACK (V1)
# Pack ID: ITRGA-V2-BE-3-P2-TRANS-APPLY-PACK-V1
# Authority:
#   - AXIOM-V2-OD-BE-3-P2-004 (Operator decision - apply act authorized)
#   - ITRGA-PLAN-V2-BE-3-P2-TRANS-APPLY-001 (boundary table, stop conditions)
#   - ITRGA-DET-V2-BE-3-P2-TRANS-FINAL-001 section 7(a)
#   - BO-V2-BE-3-P2-TRANS-001 section 6 (end state: contract_tested, history 2)
#   - Provenance anchor: accepted Revision-2 record (final migration hash
#     af77a63f903a43e2eb7b4426b67de7113791f37918bbfe7f465d8f1bab3cf8d4)
# Pattern: ITRGA-V2-BE-3-P2-TRANS-PG-GATE-PACK-V3 (defect-corrected
#   structure; PGF-001..006 lessons incorporated by construction).
#
# WHAT THIS PACK DOES:
#   Applies the PROVEN migration 20260829_0042 ONCE to the
#   APPLICATION'S WORKING DATABASE (the one the running app uses) and
#   proves the Build Order section 6 end state: contract_tested,
#   verified, persistence false, history 2, guards intact, authority
#   unset, alembic at head with the inherited V1 drift set only.
#
#   - It does NOT create or drop any database.
#   - It does NOT run the downgrade/refusal proof (proven on the gate
#     evidence database; running it here would corrupt the end state).
#   - It REFUSES by name the known ITRGA evidence databases.
#   - NO-OP BRANCH: if the target is already at 20260829_0042 with
#     contract_tested + history 2, the pack verifies that state and
#     exits with verdict ALREADY APPLIED, having changed nothing.
#
# BEFORE RUNNING: STOP THE RUNNING APPLICATION (it holds a live
#   connection pool to the target database). Restart it after the pack
#   completes. Find the target database name in backend\.env
#   (the AXIOM_DATABASE_URL line).
#
# RUN MODE: this pack MUST be executed as a file.
#   Pasting the script into an interactive console is NOT an acceptable
#   evidence mode (PGF-004).
#
# Scope and credential law:
#   - No Twelve Data credential is read, set, or used.
#   - No provider network / contract test is performed.
#   - Operator inputs: (1) the target database name (plain - it is not a
#     credential), (2) the PostgreSQL role password once, through a
#     masked prompt. The password is never written to the transcript and
#     is removed from the environment on exit.
#   - The authority variable AXIOM_TD_TRANSITION_AUTHORITY_REF is
#     managed exclusively by this pack: UNSET (verified) -> SET (exact
#     string, single apply step) -> UNSET (recorded final act step).
#
# Save this file to the AXIOM repository root:
#   C:\Users\victo\.vscode\AXIOM\axiom\ITRGA_V2_BE-3_P2_TRANS_APPLY_PACK_V1.ps1
#
# Run from the AXIOM repository root, as a file (exactly one command):
#   powershell -NoProfile -ExecutionPolicy Bypass -File ".\ITRGA_V2_BE-3_P2_TRANS_APPLY_PACK_V1.ps1"
#
# Output (submit this one file to ITRGA):
#   C:\Users\victo\.vscode\AXIOM\axiom\operator-evidence\BE-3-P2-transition\BE-3-P2-TRANS-APPLY-EVIDENCE-V1.txt
# =====================================================================

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

# ---------------------------------------------------------------------
# 0. ENCODING, LOCAL PATHS AND TOOL CHECKS
# ---------------------------------------------------------------------

# Force UTF-8 for the console / psql / transcript round trip so the
# middle dot (U+00B7) inside the EVIDENCE_REF literal round-trips
# un-mangled. This pack's own source is pure ASCII.
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
[Console]::InputEncoding  = [System.Text.Encoding]::UTF8
$env:PGCLIENTENCODING = "UTF8"
$env:PYTHONIOENCODING = "utf-8"

$RepoRoot    = (Get-Location).Path
$BackendRoot = Join-Path $RepoRoot "backend"
$Psql        = "C:\Program Files\PostgreSQL\18\bin\psql.exe"
$Python      = Join-Path $RepoRoot ".venv\Scripts\python.exe"

if (!(Test-Path $BackendRoot)) { throw "Backend directory not found: $BackendRoot" }
if (!(Test-Path $Psql))        { throw "psql.exe not found: $Psql" }
if (!(Test-Path $Python))      { throw "Python executable not found: $Python" }

$EvidenceRoot = Join-Path $RepoRoot "operator-evidence"
$EvidenceDir  = Join-Path $EvidenceRoot "BE-3-P2-transition"
$Transcript   = Join-Path $EvidenceDir "BE-3-P2-TRANS-APPLY-EVIDENCE-V1.txt"

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
# 0A. CONNECTION IDENTITY AND CONSTANTS
# ---------------------------------------------------------------------

$DbUser      = "postgres"
$DbHost      = "localhost"
$DbPort      = "5432"

$AuthorityString    = "BO-V2-BE-3-P2-TRANS-001"
$FinalMigrationHash = "af77a63f903a43e2eb7b4426b67de7113791f37918bbfe7f465d8f1bab3cf8d4"

# Known ITRGA evidence databases - this pack must never target them.
$KnownEvidenceDbs = @("axiom_be3_p2_fresh", "axiom_be3_p2_trans_fresh")

# ---------------------------------------------------------------------
# 0B. OPERATOR INPUTS (TARGET DATABASE NAME + MASKED PASSWORD)
# ---------------------------------------------------------------------

Write-Host ""
Write-Host "STOP THE RUNNING APPLICATION BEFORE CONTINUING (it holds a live connection pool"
Write-Host "to the target database). Restart it after this pack finishes."
Write-Host ""
Write-Host "This pack applies the proven transition migration 20260829_0042 ONCE to the"
Write-Host "APPLICATION'S WORKING DATABASE and then proves the end state."
Write-Host ""

$TargetDbName = (Read-Host -Prompt "PostgreSQL database name of the application's working database").Trim()
if ([string]::IsNullOrEmpty($TargetDbName)) {
    throw "No database name entered. Aborting before any database modification."
}
$TargetDbNameLower = $TargetDbName.ToLower()
foreach ($Known in $KnownEvidenceDbs) {
    if ($TargetDbNameLower -eq $Known) {
        throw "REFUSED: '$TargetDbName' is a known ITRGA evidence database. This pack applies only to the application's working database. Aborting before any database modification."
    }
}

Write-Host ""
Write-Host "Enter the PostgreSQL role password for the role shown next, once."
Write-Host "Input is masked, is never written to the transcript, and is removed from the environment when this pack finishes."
Write-Host ""

$SecurePassword = Read-Host -Prompt "PostgreSQL role password" -AsSecureString
$Bstr = [Runtime.InteropServices.Marshal]::SecureStringToBSTR($SecurePassword)
try {
    $DbPassword = [Runtime.InteropServices.Marshal]::PtrToStringBSTR($Bstr)
} finally {
    [Runtime.InteropServices.Marshal]::ZeroFreeBSTR($Bstr)
    Remove-Variable SecurePassword -ErrorAction SilentlyContinue
    Remove-Variable Bstr -ErrorAction SilentlyContinue
}

if ([string]::IsNullOrEmpty($DbPassword)) {
    throw "No database password entered. Aborting before any database modification."
}
$env:PGPASSWORD = $DbPassword

# ---------------------------------------------------------------------
# COMMAND HELPERS (parameter names avoid built-in common-parameter
# aliases; see PGF-001)
# ---------------------------------------------------------------------

function Invoke-Psql {
    param(
        [Parameter(Mandatory = $true)][string]$TargetDb,
        [Parameter(Mandatory = $true)][string]$Sql,
        [string]$Label
    )

    Write-Evidence ""
    Write-Evidence "PSQL against database: $TargetDb"
    Write-Evidence "SQL: $Sql"

    $prev = $ErrorActionPreference
    $ErrorActionPreference = "Continue"
    try {
        $Out  = & $Psql -X -v ON_ERROR_STOP=1 -U $DbUser -h $DbHost -p $DbPort -d $TargetDb -c $Sql 2>&1
        $Code = $LASTEXITCODE
    } finally {
        $ErrorActionPreference = $prev
    }

    Emit-Output $Out

    if ($Code -ne 0) { throw "psql failed (exit code $Code): $Label" }

    $Text = Norm-Text $Out
    if ($Text -eq "") { throw "psql returned no output (suspicious success): $Label" }

    return $Out
}

function Get-PsqlScalar {
    # Unaligned, tuples-only scalar read. The output contains no column
    # heading, so heading-based false positives are impossible.
    param(
        [Parameter(Mandatory = $true)][string]$TargetDb,
        [Parameter(Mandatory = $true)][string]$Sql
    )

    $prev = $ErrorActionPreference
    $ErrorActionPreference = "Continue"
    try {
        $Out  = & $Psql -X -t -A -v ON_ERROR_STOP=1 -U $DbUser -h $DbHost -p $DbPort -d $TargetDb -c $Sql
        $Code = $LASTEXITCODE
    } finally {
        $ErrorActionPreference = $prev
    }

    if ($Code -ne 0) { throw "scalar query failed (exit code $Code): $Sql" }
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
    if ($Code -ne 0) { throw "alembic $($AlembicArgs -join ' ') failed (exit code $Code): $Label" }
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
    if ($Text -notlike "*$ExpectedRev*") {
        throw "FAIL: alembic current does not show expected revision ${ExpectedRev}: $Label"
    }
}

function Invoke-ExpectedRefusal {
    param(
        [Parameter(Mandatory = $true)][string]$Label,
        [Parameter(Mandatory = $true)][string]$Sql,
        [string]$ExactMessage
    )

    Write-Evidence ""
    Write-Evidence "EXPECTED-REFUSAL: $Label"
    Write-Evidence "SQL: $Sql"

    $prev = $ErrorActionPreference
    $ErrorActionPreference = "Continue"
    try {
        $Out  = & $Psql -X -v ON_ERROR_STOP=1 -U $DbUser -h $DbHost -p $DbPort -d $TargetDbName -c $Sql 2>&1
        $Code = $LASTEXITCODE
    } finally {
        $ErrorActionPreference = $prev
    }

    Emit-Output $Out

    if ($Code -eq 0) { throw "FAIL: expected refusal unexpectedly succeeded: $Label" }

    $Text = Norm-Text $Out
    if ($ExactMessage) {
        if ($Text -notlike "*$ExactMessage*") {
            throw "FAIL: exact expected message was not observed: $Label"
        }
        Write-Evidence "PASS: exact refusal message observed."
    } else {
        if ($Text -notmatch "immutable") { throw "FAIL: expected immutability wording was not observed: $Label" }
        Write-Evidence "PASS: expected immutable refusal observed."
    }
}

# ---------------------------------------------------------------------
# SECTION 0 - RUN IDENTIFICATION
# ---------------------------------------------------------------------

Write-Section "0. RUN IDENTIFICATION"
Write-Evidence "Pack: ITRGA-V2-BE-3-P2-TRANS-APPLY-PACK-V1"
Write-Evidence "Operator decision: AXIOM-V2-OD-BE-3-P2-004 (apply act authorized)"
Write-Evidence "Plan: ITRGA-PLAN-V2-BE-3-P2-TRANS-APPLY-001"
Write-Evidence "Build order: BO-V2-BE-3-P2-TRANS-001 (section 6 end state)"
Write-Evidence "Final migration hash (apply target): $FinalMigrationHash"
Write-Evidence "Started: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss zzz')"
Write-Evidence "Repo root: $RepoRoot"
Write-Evidence "Target database (APPLICATION'S WORKING DATABASE - named by the Operator): $TargetDbName"
Write-Evidence "PostgreSQL client: $Psql"
Write-Evidence "Python (repo venv): $Python"
Write-Evidence "PostgreSQL role: ${DbUser}@${DbHost}:${DbPort}"
Write-Evidence "Provider credentials used: NONE"
Write-Evidence "This pack creates no database, runs no downgrade, and performs no refusal proof."

Push-Location $BackendRoot

try {

    # -----------------------------------------------------------------
    # SECTION 1 - HELPER SELF-TEST (BEFORE ANY DATABASE MODIFICATION)
    # -----------------------------------------------------------------

    Write-Section "1. HELPER SELF-TEST"

    [void](Invoke-Psql -TargetDb "postgres" -Sql "SELECT 1 AS helper_self_test;" -Label "psql helper self-test")

    # -----------------------------------------------------------------
    # SECTION 2 - RUN ENVIRONMENT (NO PROVIDER CREDENTIALS)
    # -----------------------------------------------------------------

    Write-Section "2. RUN ENVIRONMENT (NO PROVIDER CREDENTIALS)"

    $DbPasswordEscaped = [System.Uri]::EscapeDataString($DbPassword)
    $env:AXIOM_DATABASE_URL       = "postgresql+asyncpg://${DbUser}:${DbPasswordEscaped}@${DbHost}:${DbPort}/${TargetDbName}"
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

    Write-Evidence "AXIOM_DATABASE_URL: built by this pack for database '$TargetDbName' (value not printed)."
    Write-Evidence "AXIOM_ENVIRONMENT=testing, AXIOM_ALLOW_INSECURE_DEV=true, AXIOM_JWT_SECRET_KEY set (value not printed)."
    Write-Evidence "AXIOM_V2_MODE=RESEARCH (plan item 9)."
    Write-Evidence "AXIOM_TD_API_KEY / AXIOM_TD_API_KEY_FILE / AXIOM_TD_CONTRACT_TEST_ENABLED / AXIOM_TD_P2_AUTHORITY_REF: removed from environment."
    Write-Evidence "AXIOM_TD_TRANSITION_AUTHORITY_REF: UNSET (verified; pack-managed)."

    # -----------------------------------------------------------------
    # SECTION 3 - SOURCE PROVENANCE (FINAL MIGRATION HASH)
    # -----------------------------------------------------------------

    Write-Section "3. SOURCE PROVENANCE (FINAL MIGRATION HASH)"

    $MigrationPath = Join-Path $BackendRoot "alembic\versions\20260829_0042_v2_be3_p2_transition.py"
    if (!(Test-Path $MigrationPath)) { throw "STOP: migration file missing: $MigrationPath" }
    $MigrationHash = (Get-FileHash $MigrationPath -Algorithm SHA256).Hash.ToLower()
    Write-Evidence "alembic\versions\20260829_0042_v2_be3_p2_transition.py"
    Write-Evidence "  actual   $MigrationHash"
    Write-Evidence "  expected $FinalMigrationHash"
    if ($MigrationHash -ne $FinalMigrationHash) {
        throw "STOP: provenance hash mismatch - the migration on disk is not the ITRGA-accepted Revision-2 file. The apply must not proceed; report to ITRGA."
    }
    Write-Evidence "PASS: provenance - the migration on disk hashes to the ITRGA-accepted value."

    # -----------------------------------------------------------------
    # BOUNDARY 1 - TARGET IDENTITY
    # -----------------------------------------------------------------

    Write-Section "BOUNDARY 1: TARGET IDENTITY"

    [void](Invoke-Psql -TargetDb $TargetDbName -Label "identity" -Sql "SELECT current_database(), current_user, version();")

    # -----------------------------------------------------------------
    # BOUNDARY 2 - BASELINE STATE (alembic current) + NO-OP BRANCH
    # -----------------------------------------------------------------

    Write-Section "BOUNDARY 2: BASELINE STATE (alembic current)"

    $BaseOut = Invoke-Alembic -AlembicArgs @("current") -Label "baseline current"
    $BaseText = Norm-Text $BaseOut

    if ($BaseText -like "*20260829_0042*") {
        Write-Evidence "NOTE: target is already at 20260829_0042 - no-op branch: verifying whether the transition already exists."
        $AlreadyState = Get-PsqlScalar -TargetDb $TargetDbName -Sql "SELECT source_status, entitlement_status, persistence_permitted FROM v2_md_provider WHERE provider_id='twelvedata';"
        $AlreadyHist = Get-PsqlScalar -TargetDb $TargetDbName -Sql "SELECT COUNT(*) FROM v2_md_provider_status_history;"
        if ($AlreadyState -eq "contract_tested|verified|f" -and $AlreadyHist -eq "2") {
            Write-Evidence ""
            Write-Evidence "APPLY VERDICT: ALREADY APPLIED - the transition already exists on this database (contract_tested | verified | f, history 2)."
            Write-Evidence "Nothing was applied by this pack. The OD-004 objective is satisfied by the existing state."
            return
        }
        throw "FAIL: target is at 20260829_0042 but its state ('$AlreadyState', history $AlreadyHist) does not match an applied transition. Stopping; report to ITRGA."
    }

    # -----------------------------------------------------------------
    # BOUNDARY 3 - ESTABLISH CHAIN TO 20260825_0041
    # -----------------------------------------------------------------

    Write-Section "BOUNDARY 3: ESTABLISH CHAIN TO 20260825_0041 (each upgrade is a no-op if already at or past it)"

    [void](Invoke-Alembic -AlembicArgs @("upgrade", "20260717_0037") -Label "chain 0037")
    [void](Invoke-Alembic -AlembicArgs @("upgrade", "20260823_0038") -Label "chain 0038")
    [void](Invoke-Alembic -AlembicArgs @("upgrade", "20260824_0039") -Label "chain 0039")
    [void](Invoke-Alembic -AlembicArgs @("upgrade", "20260824_0040") -Label "chain 0040")
    [void](Invoke-Alembic -AlembicArgs @("upgrade", "20260825_0041") -Label "chain 0041")
    Assert-AlembicCurrent -ExpectedRev "20260825_0041" -Label "B3 current after chain"

    # -----------------------------------------------------------------
    # BOUNDARY 4 - PRE-STATE
    # -----------------------------------------------------------------

    Write-Section "BOUNDARY 4: PRE-STATE"

    [void](Invoke-Psql -TargetDb $TargetDbName -Label "B4 pre-state provider row" -Sql "SELECT entitlement_status, source_status, persistence_permitted FROM v2_md_provider WHERE provider_id='twelvedata';")
    $PreState = Get-PsqlScalar -TargetDb $TargetDbName -Sql "SELECT entitlement_status, source_status, persistence_permitted FROM v2_md_provider WHERE provider_id='twelvedata';"
    if ($PreState -ne "verified|architecture_candidate|f") {
        throw "FAIL: B4 - pre-state '$PreState', expected 'verified|architecture_candidate|f'. Stopping before the apply step; report to ITRGA."
    }
    $PreHist = Get-PsqlScalar -TargetDb $TargetDbName -Sql "SELECT COUNT(*) FROM v2_md_provider_status_history;"
    if ($PreHist -ne "1") {
        throw "FAIL: B4 - pre-state history count '$PreHist', expected 1 (genesis). Stopping before the apply step; report to ITRGA."
    }
    Write-Evidence "PASS: B4 - pre-state verified|architecture_candidate|f; history count 1."

    # -----------------------------------------------------------------
    # BOUNDARY 5 - THE APPLY (authority SET to the exact BO string)
    # -----------------------------------------------------------------

    Write-Section "BOUNDARY 5 [var SET = $AuthorityString]: alembic upgrade 20260829_0042"

    $env:AXIOM_TD_TRANSITION_AUTHORITY_REF = $AuthorityString
    if ($env:AXIOM_TD_TRANSITION_AUTHORITY_REF -ne $AuthorityString) {
        throw "FAIL: authority variable did not take the exact BO string."
    }
    Write-Evidence "AXIOM_TD_TRANSITION_AUTHORITY_REF = SET to exact string $AuthorityString (plan step 6)."

    [void](Invoke-Alembic -AlembicArgs @("upgrade", "20260829_0042") -Label "the apply")
    Assert-AlembicCurrent -ExpectedRev "20260829_0042" -Label "B5 current (head)"

    # -----------------------------------------------------------------
    # BOUNDARY 6 - POST-STATE (Build Order section 6 end state)
    # -----------------------------------------------------------------

    Write-Section "BOUNDARY 6: POST-STATE (end state)"

    [void](Invoke-Psql -TargetDb $TargetDbName -Label "B6 post-state provider row" -Sql "SELECT source_status, entitlement_status, persistence_permitted FROM v2_md_provider WHERE provider_id='twelvedata';")
    $PostState = Get-PsqlScalar -TargetDb $TargetDbName -Sql "SELECT source_status, entitlement_status, persistence_permitted FROM v2_md_provider WHERE provider_id='twelvedata';"
    if ($PostState -ne "contract_tested|verified|f") {
        throw "FAIL: B6 - post-state '$PostState', expected 'contract_tested|verified|f'."
    }

    [void](Invoke-Psql -TargetDb $TargetDbName -Label "B6 history rows (ordered)" -Sql "SELECT from_status, to_status, authority_ref, evidence_ref FROM v2_md_provider_status_history ORDER BY created_at;")
    $PostHistCount = Get-PsqlScalar -TargetDb $TargetDbName -Sql "SELECT COUNT(*) FROM v2_md_provider_status_history;"
    if ($PostHistCount -ne "2") { throw "FAIL: B6 - history count '$PostHistCount', expected 2." }
    $PostRow1 = Get-PsqlScalar -TargetDb $TargetDbName -Sql "SELECT (from_status IS NULL AND to_status='architecture_candidate' AND authority_ref='BO-V2-BE-3-P1-001') FROM v2_md_provider_status_history ORDER BY created_at LIMIT 1 OFFSET 0;"
    if ($PostRow1 -ne "t") { throw "FAIL: B6 - genesis row content mismatch (expected NULL -> architecture_candidate under BO-V2-BE-3-P1-001)." }
    $PostRow2 = Get-PsqlScalar -TargetDb $TargetDbName -Sql "SELECT (from_status='architecture_candidate' AND to_status='contract_tested' AND authority_ref='$AuthorityString' AND evidence_ref='ITRGA-DET-V2-BE-3-P2-FINAL-001 '||chr(183)||' run a246607c-f0c5-42e9-8f3b-a1e1bd75fa83' AND operator_id IS NULL) FROM v2_md_provider_status_history ORDER BY created_at LIMIT 1 OFFSET 1;"
    if ($PostRow2 -ne "t") { throw "FAIL: B6 - transition row content mismatch (from_status/to_status/authority_ref/evidence_ref/operator_id)." }
    Write-Evidence "PASS: B6 - history is exactly 2 rows; genesis + transition rows match the approved content (evidence_ref compared inside the database via chr(183) for the middle dot)."

    [void](Invoke-Psql -TargetDb $TargetDbName -Label "B6 status-transition audit actions (ordered)" -Sql "SELECT action FROM v2_audit_event WHERE action LIKE 'provider.status_transition%' ORDER BY created_at;")
    $PostAudit = Get-PsqlScalar -TargetDb $TargetDbName -Sql "SELECT action FROM v2_audit_event WHERE action LIKE 'provider.status_transition%' ORDER BY created_at;"
    if ($PostAudit -ne "provider.status_transition.start`nprovider.status_transition.complete") {
        throw "FAIL: B6 - audit action sequence '$PostAudit', expected start then complete."
    }
    Write-Evidence "PASS: B6 - audit sequence is exactly start, complete."

    # -----------------------------------------------------------------
    # BOUNDARY 7 - IMMUTABILITY SPOT-CHECKS
    # -----------------------------------------------------------------

    Write-Section "BOUNDARY 7: IMMUTABILITY SPOT-CHECKS"

    $ProviderExactMessage = "V2 provider registry is immutable in P1; UPDATE/DELETE prohibited"
    Invoke-ExpectedRefusal -Label "B7 spot-check: provider source_status UPDATE to 'integrated'" -Sql "UPDATE v2_md_provider SET source_status='integrated' WHERE provider_id='twelvedata';" -ExactMessage $ProviderExactMessage
    Invoke-ExpectedRefusal -Label "B7 spot-check: provider persistence_permitted UPDATE" -Sql "UPDATE v2_md_provider SET persistence_permitted=true WHERE provider_id='twelvedata';" -ExactMessage $ProviderExactMessage
    Invoke-ExpectedRefusal -Label "B7 spot-check: provider registry DELETE" -Sql "DELETE FROM v2_md_provider WHERE provider_id='twelvedata';" -ExactMessage $ProviderExactMessage
    Invoke-ExpectedRefusal -Label "B7 spot-check: history UPDATE" -Sql "UPDATE v2_md_provider_status_history SET to_status='integrated';"
    Invoke-ExpectedRefusal -Label "B7 spot-check: history DELETE" -Sql "DELETE FROM v2_md_provider_status_history;"

    # -----------------------------------------------------------------
    # BOUNDARY 8 - AUTHORITY VARIABLE UNSET (RECORDED FINAL ACT STEP)
    # -----------------------------------------------------------------

    Write-Section "BOUNDARY 8 [UNSET]: authority variable unset (recorded final act step)"

    Remove-Item Env:\AXIOM_TD_TRANSITION_AUTHORITY_REF -ErrorAction SilentlyContinue
    if ($null -ne $env:AXIOM_TD_TRANSITION_AUTHORITY_REF) {
        throw "FAIL: AXIOM_TD_TRANSITION_AUTHORITY_REF still present after the UNSET step."
    }
    Write-Evidence "AXIOM_TD_TRANSITION_AUTHORITY_REF = UNSET (verified; recorded final act step)."

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
        if ($DriftText -notlike "*$Token*") {
            throw "FAIL: B9 - expected inherited V1 drift token missing from alembic check output: $Token"
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
    # SECTION 10 - FINAL APPLY VERDICT
    # -----------------------------------------------------------------

    Write-Section "10. FINAL APPLY VERDICT"
    Write-Evidence "APPLY VERDICT: PASS - the proven migration 20260829_0042 was applied ONCE to the application's working database '$TargetDbName'."
    Write-Evidence "Terminal state (BO-V2-BE-3-P2-TRANS-001 section 6): source_status=contract_tested, entitlement_status=verified, persistence_permitted=false, history=2 (genesis + transition), guards intact, authority variable UNSET, alembic at head 20260829_0042."
    Write-Evidence "Provenance: migration on disk = $FinalMigrationHash."
    Write-Evidence "Transcript: $Transcript"
    Write-Evidence "Disposal: this pack created no database; the target is the application's working database. Restart the application when ready."

} catch {
    Write-Evidence ""
    Write-Evidence "APPLY VERDICT: FAIL - RUN ABORTED: $($_.Exception.Message)"
    Write-Evidence "Transcript: $Transcript"
    Write-Host ""
    Write-Host "APPLY FAILED. Do not edit anything in the repository and do not re-run without ITRGA instruction."
    Write-Host "Send the transcript file to ITRGA:"
    Write-Host "  $Transcript"
    throw
} finally {
    Pop-Location

    Remove-Item Env:\PGPASSWORD -ErrorAction SilentlyContinue
    Remove-Item Env:\AXIOM_DATABASE_URL -ErrorAction SilentlyContinue
    Remove-Item Env:\AXIOM_JWT_SECRET_KEY -ErrorAction SilentlyContinue
    Remove-Item Env:\AXIOM_ALLOW_INSECURE_DEV -ErrorAction SilentlyContinue
    Remove-Item Env:\AXIOM_ENVIRONMENT -ErrorAction SilentlyContinue
    Remove-Item Env:\AXIOM_V2_MODE -ErrorAction SilentlyContinue
    Remove-Item Env:\AXIOM_TD_TRANSITION_AUTHORITY_REF -ErrorAction SilentlyContinue
    Remove-Variable DbPassword -ErrorAction SilentlyContinue
    Remove-Variable DbPasswordEscaped -ErrorAction SilentlyContinue

    Write-Host "Environment cleaned (PGPASSWORD, AXIOM_DATABASE_URL, AXIOM_JWT_SECRET_KEY, AXIOM_ALLOW_INSECURE_DEV, AXIOM_ENVIRONMENT, AXIOM_V2_MODE, AXIOM_TD_TRANSITION_AUTHORITY_REF)."
}
