<#
.SYNOPSIS
  Fast, non-approval UI-007-P05 preflight for development feedback.

.NOTES
  This script intentionally does NOT run the full frontend suite, backend
  suite, Alembic, browser evidence, raw API capture, or networked local CI.
  It cannot replace scripts/run_ui007_p05_evidence.ps1 for ITRGA submission.
#>

[CmdletBinding()]
param(
    [string]$TargetRoot = ""
)

if ([string]::IsNullOrWhiteSpace($TargetRoot)) {
    # $PSScriptRoot is not reliably populated while Windows PowerShell binds
    # parameter defaults under -File. Resolve it after param binding instead.
    $scriptDirectory = Split-Path -Parent $MyInvocation.MyCommand.Path
    $TargetRoot = Split-Path -Parent $scriptDirectory
}

$ErrorActionPreference = "Continue"
$repoRoot = (Resolve-Path -LiteralPath $TargetRoot).Path
$frontend = Join-Path $repoRoot "frontend"
$checks = New-Object System.Collections.ArrayList

function Add-PreflightResult {
    param([string]$Name, [int]$ExitCode)
    [void]$checks.Add([PSCustomObject]@{ Check = $Name; ExitCode = $ExitCode })
    Write-Host "$Name`_EXIT_CODE:" $ExitCode
}

function Invoke-PreflightNative {
    param([string]$Name, [string]$WorkingDirectory, [string]$Command)
    $exitCode = 9001
    $stdout = Join-Path ([System.IO.Path]::GetTempPath()) "axiom-p05-$Name.stdout.txt"
    $stderr = Join-Path ([System.IO.Path]::GetTempPath()) "axiom-p05-$Name.stderr.txt"
    Remove-Item -LiteralPath $stdout, $stderr -Force -ErrorAction SilentlyContinue
    try {
        $process = Start-Process -FilePath "cmd.exe" `
            -ArgumentList @("/d", "/s", "/c", $Command) `
            -WorkingDirectory $WorkingDirectory `
            -RedirectStandardOutput $stdout `
            -RedirectStandardError $stderr `
            -Wait -PassThru -NoNewWindow
        $exitCode = $process.ExitCode
    }
    catch {
        $exitCode = 9001
    }
    finally {
        Remove-Item -LiteralPath $stdout, $stderr -Force -ErrorAction SilentlyContinue
    }
    Add-PreflightResult -Name $Name -ExitCode $exitCode
}

Write-Host "UI007_P05_FAST_PREFLIGHT_STARTED:" (Get-Date -Format o)
Write-Host "UI007_P05_FAST_PREFLIGHT_REPO_ROOT:" $repoRoot

Invoke-PreflightNative -Name "UI007_P05_FAST_NAMED_VITEST" -WorkingDirectory $frontend -Command "npm test -- --reporter=dot PlatformOperationsPosture.test.tsx"
Invoke-PreflightNative -Name "UI007_P05_FAST_TYPESCRIPT" -WorkingDirectory $frontend -Command "npx tsc -b --pretty false"
Invoke-PreflightNative -Name "UI007_P05_FAST_AUDIT_HIGH" -WorkingDirectory $frontend -Command "npm audit --audit-level=high"

$page = Join-Path $repoRoot "frontend\src\pages\GovernanceEvidencePage.tsx"
$patterns = @(
    'open_gate|allow_execution|gate.*toggle|toggle.*gate|certify|mark_ready|approve_production|waive|risk_accept',
    'restart|redeploy|drain|flush|reset_metrics|clear_cache|rerun_migration|trigger_health',
    'inferSignal|runInference|authoritativeRecompute|emitSignal|generateSignal|generateScenario|inferRelationship|recompute|recalculat|deriveConfidence|reclassif|openai|gpt|external_llm|llm_summary|ai_summary',
    'production\.ready|all systems go|fully operational|production_ready'
)

foreach ($pattern in $patterns) {
    $hits = Select-String -Path $page -Pattern $pattern -CaseSensitive:$false
    if ($hits) {
        $hits
        Add-PreflightResult -Name "UI007_P05_FAST_SOURCE_GUARD" -ExitCode 1
        break
    }
}
if ($checks | Where-Object { $_.Check -eq "UI007_P05_FAST_SOURCE_GUARD" }) {
    # Result already recorded.
}
else {
    Write-Host "UI007_P05_FAST_SOURCE_GUARD_CLEAN"
    Add-PreflightResult -Name "UI007_P05_FAST_SOURCE_GUARD" -ExitCode 0
}

Write-Host "=== UI-007-P05 FAST PREFLIGHT SUMMARY ==="
$checks | Format-Table -AutoSize | Out-String | Write-Host
if ($checks | Where-Object { $_.ExitCode -ne 0 }) {
    $global:LASTEXITCODE = 1
    Write-Host "UI007_P05_FAST_PREFLIGHT_WITH_FINDINGS"
}
else {
    $global:LASTEXITCODE = 0
    Write-Host "UI007_P05_FAST_PREFLIGHT_PASSED"
}
Write-Host "UI007_P05_FAST_PREFLIGHT_FINISHED:" (Get-Date -Format o)
