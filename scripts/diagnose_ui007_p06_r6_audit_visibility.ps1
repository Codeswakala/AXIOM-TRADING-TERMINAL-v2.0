<#
.SYNOPSIS
  Historical read-only visibility diagnostic. Superseded for disposition by the ITRGA window-insufficiency ruling.

.NOTES
  Read-only diagnostic: one psql SELECT and existing GET endpoints only.
  It creates no audit event and modifies no source or database row.
#>

[CmdletBinding()]
param(
    [string]$TargetRoot = "",
    [string]$BaseUrl = "http://127.0.0.1:8000",
    [string]$Username = "admin",
    [string]$Password = "admin123",
    [string]$RefusedAuditId = "055e3295-b485-4e84-9771-04c2318bf0b0"
)

if ([string]::IsNullOrWhiteSpace($TargetRoot)) {
    $scriptDirectory = Split-Path -Parent $MyInvocation.MyCommand.Path
    $TargetRoot = Split-Path -Parent $scriptDirectory
}

$ErrorActionPreference = "Stop"
$repoRoot = (Resolve-Path -LiteralPath $TargetRoot).Path
$evidenceRoot = Join-Path $repoRoot "docs\evidence"
$transcript = Join-Path $evidenceRoot "UI-007-P06_R6_VISIBILITY_DIAGNOSTIC.txt"
$loginArtifact = Join-Path $evidenceRoot "UI-007-P06_R6_VISIBILITY_LOGIN.json"
$loginBody = Join-Path $evidenceRoot "UI-007-P06_R6_VISIBILITY_LOGIN_BODY.json"
$apiSecurity = Join-Path $evidenceRoot "UI-007-P06_R6_VISIBILITY_SECURITY_API.json"
$apiStats = Join-Path $evidenceRoot "UI-007-P06_R6_VISIBILITY_STATS_API.json"

Remove-Item -LiteralPath $transcript, $loginArtifact, $loginBody, $apiSecurity, $apiStats -Force -ErrorAction SilentlyContinue
Start-Transcript -Path $transcript -Force | Out-Null
try {
    Write-Host "UI007_P06_R6_VISIBILITY_STARTED:" (Get-Date -Format o)
    Write-Host "UI007_P06_R6_VISIBILITY_REPO_ROOT:" $repoRoot
    Write-Host "UI007_P06_R6_VISIBILITY_AUDIT_ID:" $RefusedAuditId

    Write-Host "=== PSQL EXISTING-ROW CHECK ==="
    & psql -h localhost -U axiom -d axiom -c "SELECT id, category, action, actor, resource_type, resource_id, details->>'reason_code' AS reason_code, created_at FROM audit_events WHERE id = '$RefusedAuditId';"
    $psqlExit = $LASTEXITCODE
    Write-Host "UI007_P06_R6_VISIBILITY_PSQL_EXIT_CODE:" $psqlExit
    if ($psqlExit -ne 0) { throw "UI007_P06_R6_VISIBILITY_PSQL_FAILED" }

    $payload = @{ username = $Username; password = $Password } | ConvertTo-Json -Compress
    $utf8NoBom = New-Object System.Text.UTF8Encoding($false)
    [System.IO.File]::WriteAllText($loginBody, $payload, $utf8NoBom)
    try {
        $loginStatus = (& curl.exe -sS -X POST "$BaseUrl/api/v1/auth/login" -H "Content-Type: application/json" --data-binary "@$loginBody" -o $loginArtifact -w "%{http_code}").Trim()
        Write-Host "UI007_P06_R6_VISIBILITY_LOGIN_HTTP_STATUS:" $loginStatus
        if ($loginStatus -ne "200") {
            Get-Content -LiteralPath $loginArtifact
            throw "UI007_P06_R6_VISIBILITY_LOGIN_FAILED:$loginStatus"
        }
        $token = [string]((Get-Content -LiteralPath $loginArtifact -Raw | ConvertFrom-Json).tokens.access_token)
        if ([string]::IsNullOrWhiteSpace($token)) { throw "UI007_P06_R6_VISIBILITY_TOKEN_MISSING" }
        Write-Host "UI007_P06_R6_VISIBILITY_TOKEN_PRESENT: True"
    }
    finally {
        Remove-Item -LiteralPath $loginBody, $loginArtifact -Force -ErrorAction SilentlyContinue
    }

    $auth = "Authorization: Bearer $token"
    $securityStatus = (& curl.exe -sS -H $auth "$BaseUrl/api/v1/persistence/audit-events?category=SECURITY&limit=200" -o $apiSecurity -w "%{http_code}").Trim()
    Write-Host "UI007_P06_R6_VISIBILITY_SECURITY_API_HTTP_STATUS:" $securityStatus
    if ($securityStatus -ne "200") {
        Get-Content -LiteralPath $apiSecurity
        throw "UI007_P06_R6_VISIBILITY_SECURITY_API_FAILED:$securityStatus"
    }

    $statsStatus = (& curl.exe -sS -H $auth "$BaseUrl/api/v1/persistence/stats" -o $apiStats -w "%{http_code}").Trim()
    Write-Host "UI007_P06_R6_VISIBILITY_STATS_API_HTTP_STATUS:" $statsStatus
    if ($statsStatus -ne "200") {
        Get-Content -LiteralPath $apiStats
        throw "UI007_P06_R6_VISIBILITY_STATS_API_FAILED:$statsStatus"
    }

    # Force enumeration before counting/matching. A prior run reported 1 for a raw
    # 200-record JSON array, creating OBS-P06-3 evidence-harness undercount risk.
    $securityPayload = Get-Content -LiteralPath $apiSecurity -Raw | ConvertFrom-Json
    $securityRows = @($securityPayload | ForEach-Object { $_ })
    $stats = Get-Content -LiteralPath $apiStats -Raw | ConvertFrom-Json
    $apiMatch = $securityRows | Where-Object { $_.id -eq $RefusedAuditId }
    $reasonMatches = $securityRows | Where-Object { $_.details.reason_code -eq "PLUGIN_CONTRACT_IMPORT_REFUSED" }

    Write-Host "UI007_P06_R6_VISIBILITY_SECURITY_ROW_COUNT:" @($securityRows | ForEach-Object { $_ }).Count
    Write-Host "UI007_P06_R6_VISIBILITY_API_ID_PRESENT:" ([bool]$apiMatch)
    Write-Host "UI007_P06_R6_VISIBILITY_API_REASON_MATCH_COUNT:" @($reasonMatches | ForEach-Object { $_ }).Count
    Write-Host "UI007_P06_R6_VISIBILITY_API_DATABASE_BACKEND:" $stats.backend
    Write-Host "UI007_P06_R6_VISIBILITY_API_AUDIT_COUNT:" $stats.audit_count

    if ($apiMatch) {
        Write-Host "=== API MATCHING ROW ==="
        $apiMatch | ConvertTo-Json -Depth 8
        Write-Host "UI007_P06_R6_VISIBILITY_DIAGNOSIS: API_ROW_PRESENT__CHECK_BROWSER_CACHE_OR_CLIENT_ASSEMBLY"
    }
    else {
        Write-Host "UI007_P06_R6_VISIBILITY_DIAGNOSIS: PSQL_ROW_PRESENT_BUT_API_SECURITY_WINDOW_MISSING__REFER_TO_ITRGA_WINDOW_INSUFFICIENCY_RULING"
    }

    Write-Host "UI007_P06_R6_VISIBILITY_COMPLETED"
    $global:LASTEXITCODE = 0
}
finally {
    Stop-Transcript | Out-Null
}
