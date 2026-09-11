# =====================================================================
# AXIOM V2 BE-3 P2 STATUS TRANSITION - ITRGA POSTGRESQL GATE EVIDENCE PACK (V2)
# Pack ID: ITRGA-V2-BE-3-P2-TRANS-PG-GATE-PACK-V2
# Supersedes: ITRGA-V2-BE-3-P2-TRANS-PG-GATE-PACK-V1 (WITHDRAWN 2026-08-29 -
#   parse defect PGF-005; V1 never executed and produced no evidence)
# Authority:
#   - BO-V2-BE-3-P2-TRANS-001 (section 2.4 environment manifest, section 4 stop conditions)
#   - Plan AXIOM-V2-BE-3-P2-TRANS-PLAN-001 v1.1.0, Part 9 boundary table
#   - Runbook AXIOM-V2-BE-3-P2-TRANS-RUNBOOK-001 (re-issued, TRD-003 note)
#   - ITRGA-REV-V2-BE-3-P2-TRANS-DELIVERY-001 section 6.6 (gate clearance,
#     final migration hash af77a63f903a43e2eb7b4426b67de7113791f37918bbfe7f465d8f1bab3cf8d4)
# Pattern: ITRGA-V2-BE-3-P2-PG-FRESH-PACK-V3 (defect-corrected structure;
#   PGF-001..004 lessons incorporated by construction: no -Db parameter
#   alias, sentinel-armed failure-atomic gates, braced ${} variable
#   references, -File execution only).
#
# Corrections vs V1 (ITRGA-owned pack defect, recorded 2026-08-29):
#   PGF-005: line 231 of V1 contained an unbraced "$ExpectedRev:" inside a
#            double-quoted string. PowerShell parsed the colon as a
#            drive-qualified variable reference (InvalidVariableReference-
#            WithDrive) and the script FAILED AT PARSE. A parse failure
#            precedes all execution: V1 ran no command, created no database,
#            and wrote no transcript (zero side effects). Same defect class
#            as PGF-003; the full pack was re-audited - every in-string
#            variable reference is now braced ${} or a legitimate $env:
#            provider reference. Gate logic and boundary sequence unchanged.
#
# RUN MODE: this pack MUST be executed as a file.
#   Pasting the script into an interactive console is NOT an acceptable
#   evidence mode (PGF-004).
#
# Scope and credential law:
#   - No Twelve Data credential is read, set, or used.
#   - No provider network / contract test is performed.
#   - Single operator input: the PostgreSQL role password, entered once
#     through a masked prompt. It is never written to the transcript and
#     is removed from the environment on exit.
#   - The gate authority variable AXIOM_TD_TRANSITION_AUTHORITY_REF is
#     managed exclusively by this pack, per the runbook boundary table:
#     UNSET (steps 1-5) -> SET (step 6) -> NOT REQUIRED (step 7) ->
#     STILL SET (step 8) -> UNSET (step 9, recorded final gate step).
#
# Save this file to the AXIOM repository root:
#   C:\Users\victo\.vscode\AXIOM\axiom\ITRGA_V2_BE-3_P2_TRANS_POSTGRESQL_GATE_PACK_V2.ps1
#
# Run from the AXIOM repository root, as a file (exactly one command):
#   powershell -NoProfile -ExecutionPolicy Bypass -File ".\ITRGA_V2_BE-3_P2_TRANS_POSTGRESQL_GATE_PACK_V2.ps1"
#
# Output (submit this one file to ITRGA):
#   C:\Users\victo\.vscode\AXIOM\axiom\operator-evidence\BE-3-P2-transition\BE-3-P2-TRANS-GATE-EVIDENCE-V2.txt
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
$Transcript   = Join-Path $EvidenceDir "BE-3-P2-TRANS-GATE-EVIDENCE-V2.txt"

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
# 0A. SINGLE CONNECTION IDENTITY
# ---------------------------------------------------------------------
# Every psql and Alembic connection in this pack uses these values.
# The target database is created by this pack; no connection in this
# pack can point at a database this pack did not create.
# This is a NEW, dedicated database: a different name from the P2 gate's
# axiom_be3_p2_fresh, which is left in place and untouched.

$FreshDbName = "axiom_be3_p2_trans_fresh"
$DbUser      = "postgres"
$DbHost      = "localhost"
$DbPort      = "5432"

$AuthorityString    = "BO-V2-BE-3-P2-TRANS-001"
$FinalMigrationHash = "af77a63f903a43e2eb7b4426b67de7113791f37918bbfe7f465d8f1bab3cf8d4"

# ---------------------------------------------------------------------
# 0B. SINGLE MASKED PASSWORD INPUT
# ---------------------------------------------------------------------

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
        $Out  = & $Psql -X -v ON_ERROR_STOP=1 -U $DbUser -h $DbHost -p $DbPort -d $FreshDbName -c $Sql 2>&1
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

function Invoke-ExpectedRefusalUpgrade {
    # Runbook step 8: with the authority variable STILL SET, the
    # re-upgrade must be refused by P-5 (history count 3, expected 1)
    # with a non-zero exit and the exact refusal text.
    param([string]$Label)

    Write-Evidence ""
    Write-Evidence "ALEMBIC (expected refusal): alembic upgrade 20260829_0042"

    $prev = $ErrorActionPreference
    $ErrorActionPreference = "Continue"
    try {
        $Out  = & $Python -m alembic upgrade 20260829_0042 2>&1
        $Code = $LASTEXITCODE
    } finally {
        $ErrorActionPreference = $prev
    }

    Emit-Output $Out

    if ($Code -eq 0) { throw "FAIL: expected P-5 refusal, but the re-upgrade succeeded: $Label" }

    $Text = Norm-Text $Out
    if ($Text -notlike "*precondition P-5:history_count failed*") {
        throw "FAIL: expected P-5 refusal text was not observed: $Label"
    }
    Write-Evidence "PASS: expected P-5:history_count refusal observed (non-zero exit)."
}

function Assert-FreshDatabase {
    # Failure-atomic freshness gate. Gate values are armed with a
    # sentinel; if any query fails to assign a real value, the gate
    # throws. PASS is written only after all three values are verified.
    param(
        [Parameter(Mandatory = $true)][string]$TargetDbName
    )

    $Sentinel = "__GATE_NOT_RUN__"

    $DbActual   = $Sentinel
    $AlembicReg = $Sentinel
    $PubTables  = $Sentinel

    try {
        $DbActual   = Get-PsqlScalar -TargetDb $TargetDbName -Sql "SELECT current_database();"
        $AlembicReg = Get-PsqlScalar -TargetDb $TargetDbName -Sql "SELECT COALESCE(to_regclass('public.alembic_version')::text, '')"
        $PubTables  = Get-PsqlScalar -TargetDb $TargetDbName -Sql "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'public'"
    } catch {
        throw "STOP: freshness gate query failed. No Alembic command will run. Fresh-chain evidence is invalid. Detail: $($_.Exception.Message)"
    }

    if ($DbActual -eq $Sentinel -or $AlembicReg -eq $Sentinel -or $PubTables -eq $Sentinel) {
        throw "STOP: freshness gate incomplete - one or more gate queries did not return a value. No Alembic command will run. Fresh-chain evidence is invalid."
    }

    Write-Evidence "GATE-1 current_database() = '$DbActual' (expected '$TargetDbName')"
    Write-Evidence "GATE-2 public.alembic_version = '$AlembicReg' (expected empty)"
    Write-Evidence "GATE-3 public table count = '$PubTables' (expected 0)"

    if ($DbActual -ne $TargetDbName) {
        throw "STOP: freshness gate GATE-1 failed - connected to '$DbActual', expected '$TargetDbName'. No Alembic command will run. Fresh-chain evidence is invalid."
    }
    if ($AlembicReg -ne "") {
        throw "STOP: freshness gate GATE-2 failed - preexisting public.alembic_version '$AlembicReg' detected. No Alembic command will run. Fresh-chain evidence is invalid."
    }
    if ($PubTables -ne "0") {
        throw "STOP: freshness gate GATE-3 failed - public schema contains $PubTables table(s). No Alembic command will run. Fresh-chain evidence is invalid."
    }

    Write-Evidence "PASS: freshness gate - '$TargetDbName' is the database created by this pack and it is empty."
}

function Assert-SourceProvenance {
    # The gate must run against the ITRGA-accepted Revision-2 files.
    # All five manifest files are hashed and required to match exactly
    # before any boundary step runs (stop condition: any runtime source
    # change; the runbook gate runs "against the final migration hash").
    $Manifest = @(
        @("alembic\versions\20260829_0042_v2_be3_p2_transition.py", "af77a63f903a43e2eb7b4426b67de7113791f37918bbfe7f465d8f1bab3cf8d4"),
        @("tests\test_v2_p2_transition.py", "f6c886df3b8495dc9b24f737aecc0d00badf1af137811c59b4315c2a1989b31f"),
        @("tests\test_v2_integration.py", "f75190ae4f75b093a9fb1cd97d84d41dc309da8eb93b90ec6c6a9d318d2347ad"),
        @("tests\test_v2_marketdata_integration.py", "9c3efcba95073a3212d9fa8ce151468b8d155dccc24410d22fddffbcf3135fcf"),
        @("tests\test_v2_p2_contract_test.py", "324a585a72cb4098370e6887295583ac3ecb37270a131761cd62feed8c67ce38")
    )

    foreach ($Entry in $Manifest) {
        $RelPath  = $Entry[0]
        $Expected = $Entry[1]
        $Full = Join-Path $BackendRoot $RelPath
        if (!(Test-Path $Full)) { throw "STOP: provenance file missing: $Full" }
        $Actual = (Get-FileHash $Full -Algorithm SHA256).Hash.ToLower()
        Write-Evidence "$RelPath"
        Write-Evidence "  actual   $Actual"
        Write-Evidence "  expected $Expected"
        if ($Actual -ne $Expected) {
            throw "STOP: provenance hash mismatch for $RelPath. The gate must not proceed; report to ITRGA."
        }
    }
    Write-Evidence "PASS: source provenance - all five Revision-2 manifest files hash to the ITRGA-accepted values (final migration hash $FinalMigrationHash)."
}

# ---------------------------------------------------------------------
# SECTION 0 - RUN IDENTIFICATION
# ---------------------------------------------------------------------

Write-Section "0. RUN IDENTIFICATION"
Write-Evidence "Pack: ITRGA-V2-BE-3-P2-TRANS-PG-GATE-PACK-V2"
Write-Evidence "Supersedes: ITRGA-V2-BE-3-P2-TRANS-PG-GATE-PACK-V1 (withdrawn - parse defect PGF-005, never executed)"
Write-Evidence "Runbook: AXIOM-V2-BE-3-P2-TRANS-RUNBOOK-001 (re-issued)"
Write-Evidence "Build order: BO-V2-BE-3-P2-TRANS-001"
Write-Evidence "Plan: AXIOM-V2-BE-3-P2-TRANS-PLAN-001 v1.1.0 (Part 9 boundary table)"
Write-Evidence "Gate clearance: ITRGA-REV-V2-BE-3-P2-TRANS-DELIVERY-001 section 6.6"
Write-Evidence "Final migration hash (gate target): $FinalMigrationHash"
Write-Evidence "Started: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss zzz')"
Write-Evidence "Repo root: $RepoRoot"
Write-Evidence "Target database (created by this pack): $FreshDbName"
Write-Evidence "PostgreSQL client: $Psql"
Write-Evidence "Python (repo venv): $Python"
Write-Evidence "PostgreSQL role: ${DbUser}@${DbHost}:${DbPort}"
Write-Evidence "Provider credentials used: NONE"

Push-Location $BackendRoot

try {

    # -----------------------------------------------------------------
    # SECTION 1 - HELPER SELF-TEST (BEFORE ANY DATABASE MODIFICATION)
    # -----------------------------------------------------------------

    Write-Section "1. HELPER SELF-TEST"

    [void](Invoke-Psql -TargetDb "postgres" -Sql "SELECT 1 AS helper_self_test;" -Label "psql helper self-test")

    # -----------------------------------------------------------------
    # SECTION 2 - CREATE GENUINELY FRESH DATABASE
    # -----------------------------------------------------------------

    Write-Section "2. CREATE GENUINELY FRESH DATABASE"

    $DropOut = Invoke-Psql -TargetDb "postgres" -Label "drop previous transition gate database" -Sql "DROP DATABASE IF EXISTS $FreshDbName WITH (FORCE);"

    # Acceptable outcomes: the database existed and was dropped
    # ("DROP DATABASE"), or it did not exist and was skipped
    # ("does not exist, skipping" NOTICE). Anything else is a failure.
    $DropText = Norm-Text $DropOut
    if ($DropText -notmatch "DROP DATABASE" -and $DropText -notmatch "does not exist, skipping") {
        throw "FAIL: no DROP confirmation observed (expected 'DROP DATABASE' or 'does not exist, skipping'). Creation evidence is invalid; aborting before any gate or migration."
    }

    $CreateOut = Invoke-Psql -TargetDb "postgres" -Label "create fresh database" -Sql "CREATE DATABASE $FreshDbName;"

    if ((Norm-Text $CreateOut) -notmatch "CREATE DATABASE") {
        throw "FAIL: 'CREATE DATABASE' confirmation line not observed. Creation evidence is invalid; aborting before any gate or migration."
    }

    # -----------------------------------------------------------------
    # SECTION 3 - HARD FRESHNESS GATE (PRE-ALEMBIC)
    # -----------------------------------------------------------------

    Write-Section "3. HARD FRESHNESS GATE (PRE-ALEMBIC)"
    Write-Evidence "Method: unaligned scalar reads (psql -t -A); compared values contain no column heading. Gate is failure-atomic (sentinel-armed)."

    Assert-FreshDatabase -TargetDbName $FreshDbName

    # -----------------------------------------------------------------
    # SECTION 4 - DATABASE IDENTITY
    # -----------------------------------------------------------------

    Write-Section "4. DATABASE IDENTITY"

    [void](Invoke-Psql -TargetDb $FreshDbName -Label "identity" -Sql "SELECT current_database(), current_user, version();")

    # -----------------------------------------------------------------
    # SECTION 5 - RUN ENVIRONMENT (NO PROVIDER CREDENTIALS)
    # -----------------------------------------------------------------

    Write-Section "5. RUN ENVIRONMENT (NO PROVIDER CREDENTIALS)"

    $DbPasswordEscaped = [System.Uri]::EscapeDataString($DbPassword)
    $env:AXIOM_DATABASE_URL       = "postgresql+asyncpg://${DbUser}:${DbPasswordEscaped}@${DbHost}:${DbPort}/${FreshDbName}"
    $env:AXIOM_ENVIRONMENT        = "testing"
    $env:AXIOM_ALLOW_INSECURE_DEV = "true"
    $env:AXIOM_JWT_SECRET_KEY     = "operator-local-test-secret-at-least-32-characters"
    $env:AXIOM_V2_MODE            = "RESEARCH"

    # No provider credential, and no leftover authority, may be present
    # for this gate run. The authority variable is pack-managed below,
    # per the runbook boundary table.
    Remove-Item Env:\AXIOM_TD_API_KEY -ErrorAction SilentlyContinue
    Remove-Item Env:\AXIOM_TD_API_KEY_FILE -ErrorAction SilentlyContinue
    Remove-Item Env:\AXIOM_TD_CONTRACT_TEST_ENABLED -ErrorAction SilentlyContinue
    Remove-Item Env:\AXIOM_TD_P2_AUTHORITY_REF -ErrorAction SilentlyContinue
    Remove-Item Env:\AXIOM_TD_TRANSITION_AUTHORITY_REF -ErrorAction SilentlyContinue

    if ($null -ne $env:AXIOM_TD_TRANSITION_AUTHORITY_REF) {
        throw "FAIL: AXIOM_TD_TRANSITION_AUTHORITY_REF still present before step 1; expected UNSET."
    }

    Write-Evidence "AXIOM_DATABASE_URL: built by this pack for database '$FreshDbName' (value not printed)."
    Write-Evidence "AXIOM_ENVIRONMENT=testing, AXIOM_ALLOW_INSECURE_DEV=true, AXIOM_JWT_SECRET_KEY set (value not printed)."
    Write-Evidence "AXIOM_V2_MODE=RESEARCH (runbook environment manifest)."
    Write-Evidence "AXIOM_TD_API_KEY / AXIOM_TD_API_KEY_FILE / AXIOM_TD_CONTRACT_TEST_ENABLED / AXIOM_TD_P2_AUTHORITY_REF: removed from environment."
    Write-Evidence "AXIOM_TD_TRANSITION_AUTHORITY_REF: UNSET (verified; pack-managed per the boundary table)."

    # -----------------------------------------------------------------
    # SECTION 6 - SOURCE PROVENANCE (REVISION-2 MANIFEST)
    # -----------------------------------------------------------------

    Write-Section "6. SOURCE PROVENANCE (REVISION-2 MANIFEST)"

    Assert-SourceProvenance

    # -----------------------------------------------------------------
    # BOUNDARY 1 [var UNSET] - upgrade 20260717_0037
    # -----------------------------------------------------------------

    Write-Section "BOUNDARY 1 [var UNSET]: alembic upgrade 20260717_0037"

    [void](Invoke-Alembic -AlembicArgs @("upgrade", "20260717_0037") -Label "V1-head upgrade")
    Assert-AlembicCurrent -ExpectedRev "20260717_0037" -Label "B1 current"

    # -----------------------------------------------------------------
    # BOUNDARY 2 [var UNSET] - upgrade 20260823_0038
    # -----------------------------------------------------------------

    Write-Section "BOUNDARY 2 [var UNSET]: alembic upgrade 20260823_0038"

    [void](Invoke-Alembic -AlembicArgs @("upgrade", "20260823_0038") -Label "BE-1 upgrade")
    Assert-AlembicCurrent -ExpectedRev "20260823_0038" -Label "B2 current"

    # -----------------------------------------------------------------
    # BOUNDARY 3 [var UNSET] - upgrade 20260824_0039
    # -----------------------------------------------------------------

    Write-Section "BOUNDARY 3 [var UNSET]: alembic upgrade 20260824_0039"

    [void](Invoke-Alembic -AlembicArgs @("upgrade", "20260824_0039") -Label "BE-2 upgrade")
    Assert-AlembicCurrent -ExpectedRev "20260824_0039" -Label "B3 current"

    # -----------------------------------------------------------------
    # BOUNDARY 4 [var UNSET] - upgrade 20260824_0040 + permission absence
    # -----------------------------------------------------------------

    Write-Section "BOUNDARY 4 [var UNSET]: alembic upgrade 20260824_0040"

    [void](Invoke-Alembic -AlembicArgs @("upgrade", "20260824_0040") -Label "P1 upgrade")
    Assert-AlembicCurrent -ExpectedRev "20260824_0040" -Label "B4 current"

    [void](Invoke-Psql -TargetDb $FreshDbName -Label "B4 contract-test permission rows (expect none)" -Sql "SELECT role, permission, sal FROM v2_permission WHERE permission='v2.marketdata.provider.contract_test';")
    $B4Count = Get-PsqlScalar -TargetDb $FreshDbName -Sql "SELECT COUNT(*) FROM v2_permission WHERE permission='v2.marketdata.provider.contract_test';"
    if ($B4Count -ne "0") { throw "FAIL: B4 - contract-test permission present at P1 (count $B4Count, expected 0)." }
    Write-Evidence "PASS: B4 - contract-test permission absent at 20260824_0040 (count 0)."

    # -----------------------------------------------------------------
    # BOUNDARY 5 [var UNSET] - upgrade 20260825_0041 + pre-transition state
    # -----------------------------------------------------------------

    Write-Section "BOUNDARY 5 [var UNSET]: alembic upgrade 20260825_0041"

    [void](Invoke-Alembic -AlembicArgs @("upgrade", "20260825_0041") -Label "P2 upgrade")
    Assert-AlembicCurrent -ExpectedRev "20260825_0041" -Label "B5 current"

    [void](Invoke-Psql -TargetDb $FreshDbName -Label "B5 pre-transition provider state" -Sql "SELECT entitlement_status, source_status, persistence_permitted FROM v2_md_provider WHERE provider_id='twelvedata';")
    $B5State = Get-PsqlScalar -TargetDb $FreshDbName -Sql "SELECT entitlement_status, source_status, persistence_permitted FROM v2_md_provider WHERE provider_id='twelvedata';"
    if ($B5State -ne "verified|architecture_candidate|f") { throw "FAIL: B5 - pre-transition state '$B5State', expected 'verified|architecture_candidate|f'." }
    $B5Hist = Get-PsqlScalar -TargetDb $FreshDbName -Sql "SELECT COUNT(*) FROM v2_md_provider_status_history;"
    if ($B5Hist -ne "1") { throw "FAIL: B5 - history count '$B5Hist', expected 1." }
    Write-Evidence "PASS: B5 - pre-transition state verified|architecture_candidate|f; history count 1."

    # -----------------------------------------------------------------
    # BOUNDARY 6 [var SET] - upgrade 20260829_0042 + post-transition state
    # -----------------------------------------------------------------

    Write-Section "BOUNDARY 6 [var SET = $AuthorityString]: alembic upgrade 20260829_0042"

    $env:AXIOM_TD_TRANSITION_AUTHORITY_REF = $AuthorityString
    if ($env:AXIOM_TD_TRANSITION_AUTHORITY_REF -ne $AuthorityString) {
        throw "FAIL: authority variable did not take the exact BO string."
    }
    Write-Evidence "AXIOM_TD_TRANSITION_AUTHORITY_REF = SET to exact string $AuthorityString (runbook step 6)."

    [void](Invoke-Alembic -AlembicArgs @("upgrade", "20260829_0042") -Label "transition upgrade")
    Assert-AlembicCurrent -ExpectedRev "20260829_0042" -Label "B6 current (head)"

    [void](Invoke-Psql -TargetDb $FreshDbName -Label "B6 post-transition provider state" -Sql "SELECT source_status, entitlement_status, persistence_permitted FROM v2_md_provider WHERE provider_id='twelvedata';")
    $B6State = Get-PsqlScalar -TargetDb $FreshDbName -Sql "SELECT source_status, entitlement_status, persistence_permitted FROM v2_md_provider WHERE provider_id='twelvedata';"
    if ($B6State -ne "contract_tested|verified|f") { throw "FAIL: B6 - post-transition state '$B6State', expected 'contract_tested|verified|f'." }

    [void](Invoke-Psql -TargetDb $FreshDbName -Label "B6 history rows (ordered)" -Sql "SELECT from_status, to_status, authority_ref, evidence_ref FROM v2_md_provider_status_history ORDER BY created_at;")
    $B6HistCount = Get-PsqlScalar -TargetDb $FreshDbName -Sql "SELECT COUNT(*) FROM v2_md_provider_status_history;"
    if ($B6HistCount -ne "2") { throw "FAIL: B6 - history count '$B6HistCount', expected 2." }
    $B6Row1 = Get-PsqlScalar -TargetDb $FreshDbName -Sql "SELECT (from_status IS NULL AND to_status='architecture_candidate' AND authority_ref='BO-V2-BE-3-P1-001') FROM v2_md_provider_status_history ORDER BY created_at LIMIT 1 OFFSET 0;"
    if ($B6Row1 -ne "t") { throw "FAIL: B6 - genesis row content mismatch (expected NULL -> architecture_candidate under BO-V2-BE-3-P1-001)." }
    $B6Row2 = Get-PsqlScalar -TargetDb $FreshDbName -Sql "SELECT (from_status='architecture_candidate' AND to_status='contract_tested' AND authority_ref='$AuthorityString' AND evidence_ref='ITRGA-DET-V2-BE-3-P2-FINAL-001 '||chr(183)||' run a246607c-f0c5-42e9-8f3b-a1e1bd75fa83' AND operator_id IS NULL) FROM v2_md_provider_status_history ORDER BY created_at LIMIT 1 OFFSET 1;"
    if ($B6Row2 -ne "t") { throw "FAIL: B6 - transition row content mismatch (from_status/to_status/authority_ref/evidence_ref/operator_id)." }
    Write-Evidence "PASS: B6 - history is exactly 2 rows; genesis + transition rows match the approved content (evidence_ref compared inside the database via chr(183) for the middle dot)."

    [void](Invoke-Psql -TargetDb $FreshDbName -Label "B6 status-transition audit actions (ordered)" -Sql "SELECT action FROM v2_audit_event WHERE action LIKE 'provider.status_transition%' ORDER BY created_at;")
    $B6Audit = Get-PsqlScalar -TargetDb $FreshDbName -Sql "SELECT action FROM v2_audit_event WHERE action LIKE 'provider.status_transition%' ORDER BY created_at;"
    if ($B6Audit -ne "provider.status_transition.start`nprovider.status_transition.complete") {
        throw "FAIL: B6 - audit action sequence '$B6Audit', expected start then complete."
    }
    Write-Evidence "PASS: B6 - audit sequence is exactly start, complete."

    # Immutability spot-checks (runbook step 6).
    $ProviderExactMessage = "V2 provider registry is immutable in P1; UPDATE/DELETE prohibited"
    Invoke-ExpectedRefusal -Label "B6 spot-check: provider source_status UPDATE to 'integrated'" -Sql "UPDATE v2_md_provider SET source_status='integrated' WHERE provider_id='twelvedata';" -ExactMessage $ProviderExactMessage
    Invoke-ExpectedRefusal -Label "B6 spot-check: provider persistence_permitted UPDATE" -Sql "UPDATE v2_md_provider SET persistence_permitted=true WHERE provider_id='twelvedata';" -ExactMessage $ProviderExactMessage
    Invoke-ExpectedRefusal -Label "B6 spot-check: provider registry DELETE" -Sql "DELETE FROM v2_md_provider WHERE provider_id='twelvedata';" -ExactMessage $ProviderExactMessage
    Invoke-ExpectedRefusal -Label "B6 spot-check: history UPDATE" -Sql "UPDATE v2_md_provider_status_history SET to_status='integrated';"
    Invoke-ExpectedRefusal -Label "B6 spot-check: history DELETE" -Sql "DELETE FROM v2_md_provider_status_history;"
    Write-Evidence "DEVIATION NOTE (TRD-003, ITRGA-accepted; runbook step 6): the plan Part 9 other-provider fixture spot check is deliberately omitted from the gate - a fixture row would be permanently undeletable under the table-level DELETE trigger and would pollute the evidence database; coverage is by the test module (test_post_transition_immutability seeds 'otherprov') and the trigger's table-level scope (ITRGA-REV-V2-BE-3-P2-TRANS-DELIVERY-001 section 3)."

    # -----------------------------------------------------------------
    # BOUNDARY 7 [var NOT REQUIRED] - downgrade 20260825_0041
    # -----------------------------------------------------------------

    Write-Section "BOUNDARY 7 [var NOT REQUIRED]: alembic downgrade 20260825_0041"
    Write-Evidence "AXIOM_TD_TRANSITION_AUTHORITY_REF = NOT REQUIRED for the downgrade (still SET from step 6; harmless)."

    [void](Invoke-Alembic -AlembicArgs @("downgrade", "20260825_0041") -Label "transition downgrade")
    Assert-AlembicCurrent -ExpectedRev "20260825_0041" -Label "B7 current after downgrade"

    $B7Status = Get-PsqlScalar -TargetDb $FreshDbName -Sql "SELECT source_status FROM v2_md_provider WHERE provider_id='twelvedata';"
    if ($B7Status -ne "architecture_candidate") { throw "FAIL: B7 - source_status '$B7Status' after downgrade, expected architecture_candidate." }
    $B7Hist = Get-PsqlScalar -TargetDb $FreshDbName -Sql "SELECT COUNT(*) FROM v2_md_provider_status_history;"
    if ($B7Hist -ne "3") { throw "FAIL: B7 - history count '$B7Hist' after downgrade, expected 3 (reversal append, never deletion)." }
    [void](Invoke-Psql -TargetDb $FreshDbName -Label "B7 history rows after downgrade (3 rows)" -Sql "SELECT from_status, to_status, authority_ref FROM v2_md_provider_status_history ORDER BY created_at;")
    $B7Downgraded = Get-PsqlScalar -TargetDb $FreshDbName -Sql "SELECT COUNT(*) FROM v2_audit_event WHERE action='provider.status_transition.downgraded';"
    if ($B7Downgraded -ne "1") { throw "FAIL: B7 - downgraded audit count '$B7Downgraded', expected 1." }
    Write-Evidence "PASS: B7 - status restored, history 3 (reversal append), downgraded audit present."

    Invoke-ExpectedRefusal -Label "B7 re-proof: provider source_status UPDATE" -Sql "UPDATE v2_md_provider SET source_status='integrated' WHERE provider_id='twelvedata';" -ExactMessage $ProviderExactMessage

    # -----------------------------------------------------------------
    # BOUNDARY 8 [var STILL SET] - re-upgrade must be refused by P-5
    # -----------------------------------------------------------------

    Write-Section "BOUNDARY 8 [var STILL SET]: alembic upgrade 20260829_0042 (expected P-5 refusal)"
    Write-Evidence "AXIOM_TD_TRANSITION_AUTHORITY_REF = STILL SET (so P-1 passes and P-5 is the proven refusal)."

    Invoke-ExpectedRefusalUpgrade -Label "B8 re-upgrade"

    [void](Invoke-Psql -TargetDb $FreshDbName -Label "B8 durable refusal audit (latest refused row)" -Sql "SELECT details FROM v2_audit_event WHERE action='provider.status_transition.refused' ORDER BY created_at DESC LIMIT 1;")
    $B8Details = Get-PsqlScalar -TargetDb $FreshDbName -Sql "SELECT details FROM v2_audit_event WHERE action='provider.status_transition.refused' ORDER BY created_at DESC LIMIT 1;"
    if ($B8Details -notlike "*P-5:history_count*") { throw "FAIL: B8 - durable refusal audit details '$B8Details' do not show P-5:history_count." }
    $B8Hist = Get-PsqlScalar -TargetDb $FreshDbName -Sql "SELECT COUNT(*) FROM v2_md_provider_status_history;"
    if ($B8Hist -ne "3") { throw "FAIL: B8 - refused re-upgrade mutated history (count '$B8Hist', expected 3 - zero side effects)." }
    $B8Status = Get-PsqlScalar -TargetDb $FreshDbName -Sql "SELECT source_status FROM v2_md_provider WHERE provider_id='twelvedata';"
    if ($B8Status -ne "architecture_candidate") { throw "FAIL: B8 - refused re-upgrade mutated status ('$B8Status')." }
    Write-Evidence "PASS: B8 - P-5 refusal with durable audit row and zero side effects."

    # -----------------------------------------------------------------
    # BOUNDARY 9 [UNSET] - final recorded gate step
    # -----------------------------------------------------------------

    Write-Section "BOUNDARY 9 [UNSET]: authority variable unset (final recorded gate step)"

    Remove-Item Env:\AXIOM_TD_TRANSITION_AUTHORITY_REF -ErrorAction SilentlyContinue
    if ($null -ne $env:AXIOM_TD_TRANSITION_AUTHORITY_REF) {
        throw "FAIL: AXIOM_TD_TRANSITION_AUTHORITY_REF still present after the UNSET step."
    }
    Write-Evidence "AXIOM_TD_TRANSITION_AUTHORITY_REF = UNSET (verified; recorded final gate step)."

    # -----------------------------------------------------------------
    # BOUNDARY 10 - alembic check: inherited V1 drift set ONLY
    # -----------------------------------------------------------------

    Write-Section "BOUNDARY 10: alembic check (expected: inherited V1 drift set ONLY)"

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
            throw "FAIL: B10 - expected inherited V1 drift token missing from alembic check output: $Token"
        }
    }
    if ($DriftText -match "v2_md_provider|v2_permission|contract_test") {
        throw "FAIL: B10 - V2/P2/transition drift token detected in alembic check output."
    }
    if ($DriftCode -eq 0) {
        throw "FAIL: B10 - alembic check reported no drift; expected the inherited V1 drift set (non-zero exit)."
    }
    Write-Evidence "PASS: B10 - alembic check shows the inherited V1 drift set ONLY (all 9 expected tokens present, no V2/P2/transition drift, non-zero exit as expected)."

    # -----------------------------------------------------------------
    # SECTION 11 - FINAL GATE VERDICT
    # -----------------------------------------------------------------

    Write-Section "11. FINAL GATE VERDICT"
    Write-Evidence "GATE VERDICT: PASS - all ten boundary steps executed and verified (runbook AXIOM-V2-BE-3-P2-TRANS-RUNBOOK-001)."
    Write-Evidence "Final migration hash used: $FinalMigrationHash"
    Write-Evidence "Transcript: $Transcript"
    Write-Evidence "Disposal: database '$FreshDbName' is left in place for ITRGA inspection; a re-run of this pack drops and recreates it."

} catch {
    Write-Evidence ""
    Write-Evidence "GATE VERDICT: FAIL - RUN ABORTED: $($_.Exception.Message)"
    Write-Evidence "Transcript: $Transcript"
    Write-Host ""
    Write-Host "GATE FAILED. Do not edit anything in the repository. Send the transcript file to ITRGA:"
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
