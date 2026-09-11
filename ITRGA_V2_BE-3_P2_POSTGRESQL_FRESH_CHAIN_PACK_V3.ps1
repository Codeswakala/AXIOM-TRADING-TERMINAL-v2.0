# =====================================================================
# AXIOM V2 BE-3 P2 - ITRGA POSTGRESQL FRESH-CHAIN EVIDENCE PACK (V3)
# Pack ID: ITRGA-V2-BE-3-P2-PG-FRESH-PACK-V3
# Authority: ITRGA-REV-V2-BE-3-P2-POSTGRESQL-003
# Supersedes: ITRGA-V2-BE-3-P2-PG-FRESH-PACK-V2 (withdrawn)
#
# Corrections vs V2 (all ITRGA-owned pack defects, see
# ITRGA-REV-V2-BE-3-P2-POSTGRESQL-003):
#   PGF-001: the psql helpers used a parameter named -Db, which
#            collides with the built-in "db" alias of the -Debug
#            common parameter; every psql call failed. Parameter is
#            now -TargetDb. A helper self-test (SELECT 1) runs
#            before any database modification.
#   PGF-002: the freshness gate was not failure-atomic and the
#            transcript recorded a PASS that never executed. The
#            whole run is now one try/catch/finally; gate variables
#            are armed with a sentinel; PASS is written only after
#            all three gate queries returned verified values.
#   PGF-003: unbraced "$DbHost:" in a double-quoted string is a
#            parse error; all such references now use ${} delimiters.
#
# RUN MODE: this pack MUST be executed as a file. Interactive
# line-by-line paste is not an acceptable evidence mode.
#
# Scope and credential law:
#   - No Twelve Data credential is read, set, or used.
#   - No provider network / contract test is performed.
#   - Single operator input: the PostgreSQL role password, entered
#     once through a masked prompt. It is never written to the
#     transcript and is removed from the environment on exit.
#
# Save this file to the AXIOM repository root:
#   C:\Users\victo\.vscode\AXIOM\axiom\ITRGA_V2_BE-3_P2_POSTGRESQL_FRESH_CHAIN_PACK_V3.ps1
#
# Run from the AXIOM repository root, as a file:
#   powershell -NoProfile -ExecutionPolicy Bypass -File ".\ITRGA_V2_BE-3_P2_POSTGRESQL_FRESH_CHAIN_PACK_V3.ps1"
#
# Output (submit this file to ITRGA):
#   C:\Users\victo\.vscode\AXIOM\axiom\operator-evidence\BE-3-P2-postgresql\BE-3-P2-POSTGRESQL-EVIDENCE-FRESH-V3.txt
# =====================================================================

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

# ---------------------------------------------------------------------
# 0. LOCAL PATHS AND TOOL CHECKS
# ---------------------------------------------------------------------

$RepoRoot    = (Get-Location).Path
$BackendRoot = Join-Path $RepoRoot "backend"
$Psql        = "C:\Program Files\PostgreSQL\18\bin\psql.exe"
$Python      = Join-Path $RepoRoot ".venv\Scripts\python.exe"

if (!(Test-Path $BackendRoot)) { throw "Backend directory not found: $BackendRoot" }
if (!(Test-Path $Psql))        { throw "psql.exe not found: $Psql" }
if (!(Test-Path $Python))      { throw "Python executable not found: $Python" }

$EvidenceRoot = Join-Path $RepoRoot "operator-evidence"
$EvidenceDir  = Join-Path $EvidenceRoot "BE-3-P2-postgresql"
$Transcript   = Join-Path $EvidenceDir "BE-3-P2-POSTGRESQL-EVIDENCE-FRESH-V3.txt"

New-Item -ItemType Directory -Force -Path $EvidenceDir | Out-Null
Remove-Item -Force -ErrorAction SilentlyContinue $Transcript

function Write-Evidence {
    param([string]$Text)
    Add-Content -Path $Transcript -Value $Text
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
        Add-Content -Path $Transcript -Value ([string]$Line)
    }
    $Lines | Out-Host
}

# ---------------------------------------------------------------------
# 0A. SINGLE CONNECTION IDENTITY
# ---------------------------------------------------------------------
# Every psql and Alembic connection in this pack uses these values.
# The target database is created by this pack; no connection in this
# pack can point at a database this pack did not create.

$FreshDbName = "axiom_be3_p2_fresh"
$DbUser      = "postgres"
$DbHost      = "localhost"
$DbPort      = "5432"

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
# COMMAND HELPERS
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

    $Text = (@($Out) -join "`n")
    if ($Text.Trim() -eq "") { throw "psql returned no output (suspicious success): $Label" }

    return $Out
}

function Get-PsqlScalar {
    # Unaligned, tuples-only scalar read. The output contains no
    # column heading, so heading-based false positives are impossible.
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

    if ($Code -ne 0) { throw "Freshness-gate scalar query failed (exit code $Code): $Sql" }
    return (@($Out) -join "`n").Trim()
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
}

function Invoke-ExpectedRefusal {
    param(
        [string]$Label,
        [string]$Sql
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
    if ((@($Out) -join "`n") -notmatch "immutable") { throw "FAIL: expected immutability wording was not observed: $Label" }
    Write-Evidence "PASS: expected immutable refusal observed."
}

function Assert-FreshDatabase {
    # Failure-atomic freshness gate. Gate values are armed with a
    # sentinel; if any query fails to assign a real value, the gate
    # throws. PASS is written only after all three values are
    # verified to pass. This function is the ONLY place where the
    # freshness PASS line can be produced.
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

# ---------------------------------------------------------------------
# SECTION 0 - RUN IDENTIFICATION
# ---------------------------------------------------------------------

Write-Section "0. RUN IDENTIFICATION"
Write-Evidence "Pack: ITRGA-V2-BE-3-P2-PG-FRESH-PACK-V3"
Write-Evidence "Supersedes: ITRGA-V2-BE-3-P2-PG-FRESH-PACK-V2 (withdrawn per ITRGA-REV-V2-BE-3-P2-POSTGRESQL-003)"
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

    $DropOut = Invoke-Psql -TargetDb "postgres" -Label "drop previous fresh database" -Sql "DROP DATABASE IF EXISTS $FreshDbName WITH (FORCE);"

    # Acceptable outcomes: the database existed and was dropped
    # ("DROP DATABASE"), or it did not exist and was skipped
    # ("does not exist, skipping" NOTICE). Anything else is a failure.
    $DropText = (@($DropOut) -join "`n")
    if ($DropText -notmatch "DROP DATABASE" -and $DropText -notmatch "does not exist, skipping") {
        throw "FAIL: no DROP confirmation observed (expected 'DROP DATABASE' or 'does not exist, skipping'). Creation evidence is invalid; aborting before any gate or migration."
    }

    $CreateOut = Invoke-Psql -TargetDb "postgres" -Label "create fresh database" -Sql "CREATE DATABASE $FreshDbName;"

    if ((@($CreateOut) -join "`n") -notmatch "CREATE DATABASE") {
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

    # No provider credential may be present for this PostgreSQL evidence run.
    Remove-Item Env:\AXIOM_TD_API_KEY -ErrorAction SilentlyContinue
    Remove-Item Env:\AXIOM_TD_API_KEY_FILE -ErrorAction SilentlyContinue
    Remove-Item Env:\AXIOM_TD_CONTRACT_TEST_ENABLED -ErrorAction SilentlyContinue
    Remove-Item Env:\AXIOM_TD_P2_AUTHORITY_REF -ErrorAction SilentlyContinue

    Write-Evidence "AXIOM_DATABASE_URL: built by this pack for database '$FreshDbName' (value not printed)."
    Write-Evidence "AXIOM_ENVIRONMENT=testing, AXIOM_ALLOW_INSECURE_DEV=true, AXIOM_JWT_SECRET_KEY set (value not printed)."
    Write-Evidence "AXIOM_TD_API_KEY / AXIOM_TD_API_KEY_FILE / AXIOM_TD_CONTRACT_TEST_ENABLED / AXIOM_TD_P2_AUTHORITY_REF: removed from environment."

    # -----------------------------------------------------------------
    # SECTION 6 - CORRECTED SOURCE HASHES
    # -----------------------------------------------------------------

    Write-Section "6. CORRECTED SOURCE HASHES"

    $Files = @(
        "app\v2\marketdata\providers\contract_test.py",
        "app\v2\marketdata\api\contract_test.py",
        "alembic\versions\20260823_0038_v2_be1_core.py",
        "alembic\versions\20260825_0041_v2_be3_p2_entitlement.py",
        "tests\test_v2_p2_contract_test.py",
        "tests\test_v2_provider_integration.py"
    )

    foreach ($File in $Files) {
        $Path = Join-Path $BackendRoot $File
        if (!(Test-Path $Path)) { throw "Required source file missing: $Path" }
        Write-Evidence ""
        Write-Evidence $File
        Write-Evidence ((Get-FileHash $Path -Algorithm SHA256).Hash)
    }

    # -----------------------------------------------------------------
    # SECTION 7 - UPGRADE TO BE-1 REVISION 20260823_0038
    # -----------------------------------------------------------------

    Write-Section "7. UPGRADE TO BE-1 REVISION 20260823_0038"

    Invoke-Alembic -AlembicArgs @("upgrade", "20260823_0038") -Label "BE-1 upgrade"
    Invoke-Alembic -AlembicArgs @("current") -Label "BE-1 current"

    Write-Section "8. BE-1 P2-PERMISSION ABSENCE"

    [void](Invoke-Psql -TargetDb $FreshDbName -Label "BE-1 permission absence" -Sql "SELECT role, permission, sal FROM v2_permission WHERE permission='v2.marketdata.provider.contract_test';")

    # -----------------------------------------------------------------
    # SECTION 9 - UPGRADE TO APPROVED P1 REVISION
    # -----------------------------------------------------------------

    Write-Section "9. UPGRADE TO P1 REVISION 20260824_0040"

    Invoke-Alembic -AlembicArgs @("upgrade", "20260824_0040") -Label "P1 upgrade"
    Invoke-Alembic -AlembicArgs @("current") -Label "P1 current"

    Write-Section "10. P1 STATE - P2 PERMISSION MUST REMAIN ABSENT"

    [void](Invoke-Psql -TargetDb $FreshDbName -Label "P1 state" -Sql "SELECT provider_id, source_status, entitlement_status, persistence_permitted FROM v2_md_provider WHERE provider_id='twelvedata'; SELECT role, permission, sal FROM v2_permission WHERE permission='v2.marketdata.provider.contract_test';")

    # -----------------------------------------------------------------
    # SECTION 11 - UPGRADE TO P2
    # -----------------------------------------------------------------

    Write-Section "11. UPGRADE TO P2 REVISION 20260825_0041"

    Invoke-Alembic -AlembicArgs @("upgrade", "20260825_0041") -Label "P2 upgrade"
    Invoke-Alembic -AlembicArgs @("current") -Label "P2 current"

    Write-Section "12. P2 PROVIDER STATE AND ADMIN/SAL-4 PERMISSION"

    [void](Invoke-Psql -TargetDb $FreshDbName -Label "P2 state and permission" -Sql "SELECT provider_id, source_status, entitlement_status, persistence_permitted, entitlement->>'plan' AS plan, entitlement->>'evidence_ref' AS evidence_ref FROM v2_md_provider WHERE provider_id='twelvedata'; SELECT role, permission, sal FROM v2_permission WHERE permission='v2.marketdata.provider.contract_test'; SELECT COUNT(*) AS provider_history_rows FROM v2_md_provider_status_history WHERE provider_id='twelvedata';")

    Write-Section "13. POSTGRESQL REGISTRY TRIGGER AND FUNCTION"

    [void](Invoke-Psql -TargetDb $FreshDbName -Label "trigger and function" -Sql "SELECT c.relname AS table_name, t.tgname AS trigger_name, pg_get_triggerdef(t.oid) AS trigger_definition FROM pg_trigger t JOIN pg_class c ON c.oid=t.tgrelid JOIN pg_namespace n ON n.oid=c.relnamespace WHERE NOT t.tgisinternal AND n.nspname='public' AND c.relname='v2_md_provider' ORDER BY t.tgname; SELECT p.proname AS function_name, pg_get_functiondef(p.oid) AS function_definition FROM pg_proc p JOIN pg_namespace n ON n.oid=p.pronamespace WHERE n.nspname='public' AND p.proname='prevent_v2_md_provider_mutation';")

    Write-Section "14. POST-P2 PROVIDER-REGISTRY IMMUTABILITY"

    Invoke-ExpectedRefusal -Label "Provider entitlement_status UPDATE" -Sql "UPDATE v2_md_provider SET entitlement_status='expired' WHERE provider_id='twelvedata';"
    Invoke-ExpectedRefusal -Label "Provider registry DELETE" -Sql "DELETE FROM v2_md_provider WHERE provider_id='twelvedata';"

    # -----------------------------------------------------------------
    # SECTION 15 - ALEMBIC DRIFT CHECK
    # -----------------------------------------------------------------

    Write-Section "15. ALEMBIC DRIFT CHECK"

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

    $DriftText = (@($DriftOut) -join "`n")

    if ($DriftText -match "v2_md_provider|v2_permission|contract_test") {
        throw "FAIL: V2/P2 Alembic drift token detected."
    }

    if ($DriftCode -eq 0) {
        Write-Evidence "PASS: alembic check reports no drift."
    }
    else {
        Write-Evidence "NOTICE: alembic check is non-zero; transcript must show inherited V1 drift only."
    }

    # -----------------------------------------------------------------
    # SECTION 16 - DOWNGRADE TO P1 AND VERIFY FULL RESTORATION
    # -----------------------------------------------------------------

    Write-Section "16. DOWNGRADE TO 20260824_0040"

    Invoke-Alembic -AlembicArgs @("downgrade", "20260824_0040") -Label "downgrade"
    Invoke-Alembic -AlembicArgs @("current") -Label "current after downgrade"

    Write-Section "17. P1 RESTORATION AFTER P2 DOWNGRADE"

    [void](Invoke-Psql -TargetDb $FreshDbName -Label "P1 restoration" -Sql "SELECT provider_id, source_status, entitlement_status, persistence_permitted, entitlement IS NULL AS entitlement_is_null FROM v2_md_provider WHERE provider_id='twelvedata'; SELECT role, permission, sal FROM v2_permission WHERE permission='v2.marketdata.provider.contract_test';")

    Write-Section "18. P1 REGISTRY IMMUTABILITY AFTER P2 DOWNGRADE"

    Invoke-ExpectedRefusal -Label "Post-downgrade provider entitlement_status UPDATE" -Sql "UPDATE v2_md_provider SET entitlement_status='verified' WHERE provider_id='twelvedata';"
    Invoke-ExpectedRefusal -Label "Post-downgrade provider registry DELETE" -Sql "DELETE FROM v2_md_provider WHERE provider_id='twelvedata';"

    # -----------------------------------------------------------------
    # SECTION 19 - FINAL RE-UPGRADE
    # -----------------------------------------------------------------

    Write-Section "19. RE-UPGRADE TO P2 HEAD"

    Invoke-Alembic -AlembicArgs @("upgrade", "head") -Label "re-upgrade"
    Invoke-Alembic -AlembicArgs @("current") -Label "final current"

    Write-Section "20. FINAL P2 STATE AFTER RE-UPGRADE"

    [void](Invoke-Psql -TargetDb $FreshDbName -Label "final P2 state" -Sql "SELECT provider_id, source_status, entitlement_status, persistence_permitted, entitlement->>'plan' AS plan, entitlement->>'evidence_ref' AS evidence_ref FROM v2_md_provider WHERE provider_id='twelvedata'; SELECT role, permission, sal FROM v2_permission WHERE permission='v2.marketdata.provider.contract_test'; SELECT COUNT(*) AS provider_history_rows FROM v2_md_provider_status_history WHERE provider_id='twelvedata';")

    Write-Evidence ""
    Write-Evidence "FINAL RESULT: BE-3 P2 PostgreSQL fresh-chain evidence completed."
    Write-Evidence "Transcript: $Transcript"
    Write-Evidence "Disposal: database '$FreshDbName' is left in place for ITRGA inspection; the next run of this pack drops and recreates it."

} catch {
    Write-Evidence ""
    Write-Evidence "RUN ABORTED: $($_.Exception.Message)"
    throw
} finally {
    Pop-Location

    Remove-Item Env:\PGPASSWORD -ErrorAction SilentlyContinue
    Remove-Item Env:\AXIOM_DATABASE_URL -ErrorAction SilentlyContinue
    Remove-Item Env:\AXIOM_JWT_SECRET_KEY -ErrorAction SilentlyContinue
    Remove-Item Env:\AXIOM_ALLOW_INSECURE_DEV -ErrorAction SilentlyContinue
    Remove-Item Env:\AXIOM_ENVIRONMENT -ErrorAction SilentlyContinue
    Remove-Variable DbPassword -ErrorAction SilentlyContinue
    Remove-Variable DbPasswordEscaped -ErrorAction SilentlyContinue

    Write-Host ""
    Write-Host "Environment cleaned (PGPASSWORD, AXIOM_DATABASE_URL, AXIOM_JWT_SECRET_KEY, AXIOM_ALLOW_INSECURE_DEV, AXIOM_ENVIRONMENT)."
    Write-Host "Transcript: $Transcript"
}
