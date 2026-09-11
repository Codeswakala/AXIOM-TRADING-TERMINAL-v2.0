<#
.SYNOPSIS
  Operator-run Level-I evidence runner for TD-AXIOM-GIT-PROVENANCE-REMEDIATION.

.DESCRIPTION
  Executes ITRGA Amendment 4's validated sequence: intake hash snapshot,
  index-only evidence/database removal, conflict and value controls, full
  worktree baseline commit/tag, runtime-only hook rejection, provenance
  verification, and regression capture. It never rewrites history or changes
  Gate/certification/production posture.
#>

[CmdletBinding()]
param(
    [string]$TargetRoot = ""
)

if ([string]::IsNullOrWhiteSpace($TargetRoot)) {
    $scriptDirectory = Split-Path -Parent $MyInvocation.MyCommand.Path
    $TargetRoot = Split-Path -Parent $scriptDirectory
}

$ErrorActionPreference = "Stop"
$repoRoot = (Resolve-Path -LiteralPath $TargetRoot).Path
$evidenceRoot = Join-Path $repoRoot "docs\evidence"
$intakeManifest = Join-Path $repoRoot "docs\governance\TD-PROVENANCE_INTAKE_MANIFEST.csv"
$operatorResults = Join-Path $evidenceRoot "TD-AXIOM-GIT-PROVENANCE_OPERATOR_RESULTS.txt"
$utf8NoBom = New-Object System.Text.UTF8Encoding($false)
$logLines = New-Object System.Collections.Generic.List[string]

function Write-Utf8NoBom {
    param(
        [Parameter(Mandatory = $true)][string]$Path,
        [Parameter(Mandatory = $true)][AllowEmptyCollection()][AllowEmptyString()][string[]]$Lines
    )
    $parent = Split-Path -Parent $Path
    if (-not (Test-Path -LiteralPath $parent)) { New-Item -ItemType Directory -Path $parent -Force | Out-Null }
    [System.IO.File]::WriteAllText($Path, ($Lines -join [Environment]::NewLine), $utf8NoBom)
}

function Write-Log {
    param([Parameter(Mandatory = $true)][AllowEmptyString()][string]$Message)
    Write-Host $Message
    [void]$logLines.Add($Message)
}

function Write-Artifact {
    param([Parameter(Mandatory = $true)][string]$Path, [AllowEmptyString()][string]$Text)
    $lines = if ($null -eq $Text) { @() } else { @($Text -split "`r?`n") }
    Write-Utf8NoBom -Path $Path -Lines $lines
}

function Invoke-NativeEvidence {
    param(
        [Parameter(Mandatory = $true)][string]$Gate,
        [Parameter(Mandatory = $true)][string]$Executable,
        [string[]]$Arguments = @(),
        [Parameter(Mandatory = $true)][string]$Artifact,
        [Parameter(Mandatory = $false)][bool]$ExpectSuccess = $true
    )

    Write-Log "=== $Gate ==="
    Write-Log "COMMAND: $Executable $($Arguments -join ' ')"
    $priorErrorAction = $ErrorActionPreference
    try {
        # Git may emit line-ending warnings on stderr with an otherwise successful
        # exit code. Capture stderr as evidence without promoting it to a PowerShell
        # terminating NativeCommandError.
        $ErrorActionPreference = "Continue"
        $output = & $Executable @Arguments 2>&1 | Out-String
        $code = $LASTEXITCODE
    }
    finally {
        $ErrorActionPreference = $priorErrorAction
    }
    Write-Artifact -Path $Artifact -Text $output
    if ($output.Trim()) {
        ($output -split "`r?`n" | Select-Object -Last 80) | ForEach-Object { Write-Log $_ }
    }
    Write-Log "${Gate}_EXIT_CODE: $code"
    if ($ExpectSuccess -and $code -ne 0) { throw "${Gate}_FAILED:$code" }
    if (-not $ExpectSuccess -and $code -eq 0) { throw "${Gate}_UNEXPECTED_SUCCESS" }
    return $code
}

function Get-ProvenanceSnapshot {
    param([Parameter(Mandatory = $true)][string]$Root)
    $roots = @("backend", "frontend", "docs", "scripts")
    $rows = New-Object System.Collections.Generic.List[object]
    foreach ($relativeRoot in $roots) {
        $absoluteRoot = Join-Path $Root $relativeRoot
        if (-not (Test-Path -LiteralPath $absoluteRoot)) { continue }
        Get-ChildItem -LiteralPath $absoluteRoot -Recurse -File -Force | ForEach-Object {
            $relative = $_.FullName.Substring($Root.Length).TrimStart('\', '/').Replace('\', '/')
            if ($relative -notmatch '(^|/)(node_modules|\.venv|dist|__pycache__|\.git)(/|$)') {
                $hash = (Get-FileHash -LiteralPath $_.FullName -Algorithm SHA256).Hash.ToLowerInvariant()
                [void]$rows.Add([PSCustomObject]@{ Path = $relative; SHA256 = $hash })
            }
        }
    }
    return @($rows | Sort-Object Path)
}

function Write-IntakeManifest {
    param([Parameter(Mandatory = $true)][object[]]$Rows, [Parameter(Mandatory = $true)][string]$Path)
    $csv = @($Rows | ConvertTo-Csv -NoTypeInformation)
    Write-Utf8NoBom -Path $Path -Lines $csv
}

function Get-WorkingRedactionCount {
    param([Parameter(Mandatory = $true)][string]$Root, [Parameter(Mandatory = $true)][string]$Artifact)
    $output = & python (Join-Path $Root "scripts\git_provenance_guard.py") --mode redaction-candidates 2>&1 | Out-String
    $code = $LASTEXITCODE
    Write-Artifact -Path $Artifact -Text $output
    if ($code -ne 0) { throw "REDACTION_CANDIDATE_SCAN_FAILED:$code" }
    return $output
}

function Test-ForbiddenPath {
    param([Parameter(Mandatory = $true)][string]$Path)
    $normalized = $Path.Replace('\', '/')
    if ($normalized -like "backend/app/*") { return $true }
    if ($normalized -like "frontend/src/*") { return $true }
    if ($normalized -like "backend/tests/*") { return $true }
    if ($normalized -match '(^|/)tests?/.*' -or $normalized -match '\.(test|spec)\.[^/]+$') { return $true }
    if ($normalized -like "backend/alembic/*" -or $normalized -like "*/migrations/*") { return $true }
    if ($normalized -like "backend/app/db/models/*" -or $normalized -like "*/schema/*") { return $true }
    if ($normalized -like "backend/app/api/routes/*") { return $true }
    $name = [System.IO.Path]::GetFileName($normalized).ToLowerInvariant()
    if ($name -in @("package.json", "package-lock.json", "pyproject.toml", "requirements.txt", "requirements-dev.txt", "pnpm-lock.yaml", "yarn.lock")) { return $true }
    return $false
}

Set-Location $repoRoot
$intakeStarted = Get-Date
$intakeRows = Get-ProvenanceSnapshot -Root $repoRoot
Write-IntakeManifest -Rows $intakeRows -Path $intakeManifest

try {
    Write-Log "TD_AXIOM_GIT_PROVENANCE_STARTED: $($intakeStarted.ToString('o'))"
    Write-Log "TD_AXIOM_GIT_PROVENANCE_REPO_ROOT: $repoRoot"
    Write-Log "TD_AXIOM_GIT_PROVENANCE_AUTHORITY: ITRGA_AMENDMENT_4_TD-AXIOM-GIT-PROVENANCE_FINAL.md"
    Write-Log "INTAKE_MANIFEST_FILE_COUNT: $($intakeRows.Count)"
    Write-Log "INTAKE_MANIFEST_CAPTURED_AT: $($intakeStarted.ToString('o'))"
    Write-Log "INTAKE_MANIFEST_PATH: $intakeManifest"
    Write-Log "GOVERNANCE_GATE: CLOSED"
    Write-Log "PRODUCTION: NOT_CERTIFIED"

    $head = (& git rev-parse HEAD).Trim()
    $commitCount = (& git rev-list --count HEAD).Trim()
    Write-Log "INITIAL_HEAD: $head"
    Write-Log "INITIAL_COMMIT_COUNT: $commitCount"
    if ($head -ne "22c735a01f33cd4c5886b8bab1944dac19604127" -or $commitCount -ne "1") {
        throw "INITIAL_HISTORY_PRECONDITION_FAILED"
    }
    $guardPath = Join-Path $repoRoot "scripts\git_provenance_guard.py"
    $guardVersion = "td-provenance-guard-v2-strict-conflict-ascii"
    if (-not (Test-Path -LiteralPath $guardPath) -or (Get-Content -LiteralPath $guardPath -Raw) -notmatch [regex]::Escape($guardVersion)) {
        throw "STALE_GIT_PROVENANCE_GUARD__EXPECTED_$guardVersion"
    }
    Write-Log "GUARD_IMPLEMENTATION_VERSION_EXPECTED: $guardVersion"

    # Step 1: consolidated P-1 ignore rules.
    $ignorePath = Join-Path $repoRoot ".gitignore"
    $requiredIgnore = @("docs/evidence/**", "**/OPERATOR_RESULTS*.md", "**/*_RAW_*.json", "*.db")
    $ignoreText = Get-Content -LiteralPath $ignorePath -Raw
    foreach ($rule in $requiredIgnore) {
        if ($ignoreText -notmatch [regex]::Escape($rule)) {
            [System.IO.File]::AppendAllText($ignorePath, [Environment]::NewLine + $rule + [Environment]::NewLine, $utf8NoBom)
            $ignoreText = Get-Content -LiteralPath $ignorePath -Raw
        }
    }
    $ignoreArtifact = Join-Path $evidenceRoot "TD-AXIOM-GIT-PROVENANCE_01_GITIGNORE_DIFF.txt"
    Invoke-NativeEvidence -Gate "GITIGNORE_DIFF" -Executable "git" -Arguments @("diff", "--", ".gitignore") -Artifact $ignoreArtifact | Out-Null

    # Step 2: authorized index-only removal. Never delete local evidence/database files.
    $evidencePaths = @(& git ls-files -- docs/evidence)
    $dbPaths = @(& git ls-files | Where-Object { $_ -match '\.db($|\.)' })
    # A prior halted invocation may already have completed the authorized
    # index-only D-3 removal. Preserve that evidence/count on an idempotent rerun.
    $alreadyDeindexedEvidence = @(& git diff --cached --name-only --diff-filter=D -- docs/evidence)
    $alreadyDeindexedDb = @(& git diff --cached --name-only --diff-filter=D | Where-Object { $_ -match '\.db($|\.)' })
    $deindexedCount = @($evidencePaths + $dbPaths + $alreadyDeindexedEvidence + $alreadyDeindexedDb | Sort-Object -Unique).Count
    $sampleEvidence = ($evidencePaths + $alreadyDeindexedEvidence | Sort-Object -Unique | Select-Object -First 1)
    $sampleDb = ($dbPaths + $alreadyDeindexedDb | Sort-Object -Unique | Select-Object -First 1)
    $deindexArtifact = Join-Path $evidenceRoot "TD-AXIOM-GIT-PROVENANCE_02_DEINDEX.txt"
    $deindexLines = New-Object System.Collections.Generic.List[string]
    [void]$deindexLines.Add("EVIDENCE_PATH_COUNT_BEFORE_DEINDEX: $($evidencePaths.Count)")
    [void]$deindexLines.Add("DATABASE_BACKUP_PATH_COUNT_BEFORE_DEINDEX: $($dbPaths.Count)")
    [void]$deindexLines.Add("RESUMED_STAGED_EVIDENCE_DEINDEX_COUNT: $($alreadyDeindexedEvidence.Count)")
    [void]$deindexLines.Add("RESUMED_STAGED_DATABASE_DEINDEX_COUNT: $($alreadyDeindexedDb.Count)")
    if ($evidencePaths.Count -gt 0) {
        $output = & git rm -r --cached --ignore-unmatch -- docs/evidence 2>&1 | Out-String
        [void]$deindexLines.Add("=== GIT_RM_EVIDENCE ===")
        [void]$deindexLines.Add($output)
        if ($LASTEXITCODE -ne 0) { throw "DEINDEX_EVIDENCE_FAILED:$LASTEXITCODE" }
    }
    foreach ($dbPath in $dbPaths) {
        $output = & git rm --cached --ignore-unmatch -- $dbPath 2>&1 | Out-String
        [void]$deindexLines.Add("=== GIT_RM_DATABASE_BACKUP ===")
        [void]$deindexLines.Add($output)
        if ($LASTEXITCODE -ne 0) { throw "DEINDEX_DATABASE_BACKUP_FAILED:$LASTEXITCODE" }
    }
    [void]$deindexLines.Add("DEINDEXED_PATH_COUNT: $deindexedCount")
    [void]$deindexLines.Add("LOCAL_EVIDENCE_SAMPLE_INTACT: $([bool]($sampleEvidence -and (Test-Path -LiteralPath (Join-Path $repoRoot $sampleEvidence))))")
    [void]$deindexLines.Add("LOCAL_DATABASE_SAMPLE_INTACT: $([bool]($sampleDb -and (Test-Path -LiteralPath (Join-Path $repoRoot $sampleDb))))")
    Write-Utf8NoBom -Path $deindexArtifact -Lines @($deindexLines)
    @($deindexLines | Select-Object -Last 30) | ForEach-Object { Write-Log $_ }

    # Steps 3-5: conflict/diff guards and transparent redaction candidate counts.
    $redactionBeforeArtifact = Join-Path $evidenceRoot "TD-AXIOM-GIT-PROVENANCE_04_REDACTION_BEFORE_DEINDEX.txt"
    # The pre-deindex candidate scan is preserved from the prepared corpus; after scan is authoritative for staged records.
    Write-Log "REDACTION_CANDIDATES_BEFORE_DEINDEX: prepared prior to D-3; see P-3 manifest (37 files / 71 A / 1 B / 0 C)"
    Write-Artifact -Path $redactionBeforeArtifact -Text "REDACTION_CANDIDATES_BEFORE_DEINDEX: prepared prior to D-3; P-3 manifest totals 37 files / 71 Class A / 1 Class B / 0 Class C."
    $redactionAfterArtifact = Join-Path $evidenceRoot "TD-AXIOM-GIT-PROVENANCE_04_REDACTION_AFTER_DEINDEX.txt"
    $redactionAfter = Get-WorkingRedactionCount -Root $repoRoot -Artifact $redactionAfterArtifact
    ($redactionAfter -split "`r?`n") | ForEach-Object { if ($_){ Write-Log $_ } }
    Write-Log "REDACTION_CANDIDATES_AFTER_DEINDEX: $((($redactionAfter | Select-String -Pattern 'REDACTION_CANDIDATE_FILE_COUNT:').Line -replace '.*: ', ''))"

    $conflictArtifact = Join-Path $evidenceRoot "TD-AXIOM-GIT-PROVENANCE_03_CONFLICT_SCAN.txt"
    $candidatePaths = @(& git ls-files) + @(& git ls-files --others --exclude-standard)
    $conflicts = New-Object System.Collections.Generic.List[string]
    foreach ($relative in ($candidatePaths | Sort-Object -Unique)) {
        $absolute = Join-Path $repoRoot $relative
        if (-not (Test-Path -LiteralPath $absolute -PathType Leaf)) { continue }
        try {
            # Match only standard Git conflict syntax. Do not treat a test-run
            # banner such as "======== 74 passed ========" as a conflict marker.
            $matches = Select-String -LiteralPath $absolute -Pattern '^(<<<<<<< .+|=======$|>>>>>>> .+)$' -AllMatches -ErrorAction Stop
            foreach ($match in $matches) { [void]$conflicts.Add("$relative`:$($match.LineNumber)") }
        } catch { }
    }
    if ($conflicts.Count -gt 0) {
        Write-Utf8NoBom -Path $conflictArtifact -Lines @($conflicts)
        $conflicts | ForEach-Object { Write-Log "CONFLICT_MARKER_PATH: $_" }
        throw "CONFLICT_MARKERS_FOUND:$($conflicts.Count)"
    }
    Write-Utf8NoBom -Path $conflictArtifact -Lines @("CONFLICT_MARKER_SCAN_CLEAN")
    Write-Log "CONFLICT_MARKER_SCAN_CLEAN"
    Invoke-NativeEvidence -Gate "GIT_DIFF_CHECK" -Executable "git" -Arguments @("diff", "--check") -Artifact (Join-Path $evidenceRoot "TD-AXIOM-GIT-PROVENANCE_03_DIFF_CHECK.txt") | Out-Null

    # Steps 6-8: full staging, approved D-2 manifest, and real counter reconciliation.
    $manifestPath = Join-Path $repoRoot "docs\governance\TD-AXIOM-GIT-PROVENANCE_D2_EXCEPTION_MANIFEST.md"
    if (-not (Test-Path -LiteralPath $manifestPath)) { throw "D2_EXCEPTION_MANIFEST_MISSING" }
    Write-Log "D2_EXCEPTION_MANIFEST_PRESENT: True"
    # Amendment 2 withdrew this provisional D-5 exception record. A prior
    # interrupted attempt may have staged it as an untracked addition; remove
    # both the working copy and any index entry before the complete stage.
    $obsoleteD5Record = "docs/build-orders/TD-AXIOM-GIT-PROVENANCE_P3_DOCUMENTED_SCAN_EXCEPTIONS.md"
    $obsoleteD5Absolute = Join-Path $repoRoot $obsoleteD5Record
    if (Test-Path -LiteralPath $obsoleteD5Absolute) {
        Remove-Item -LiteralPath $obsoleteD5Absolute -Force
        Write-Log "WITHDRAWN_D5_RECORD_REMOVED_FROM_WORKTREE: True"
    }
    & git reset -- $obsoleteD5Record 2>&1 | Out-Null
    Write-Log "WITHDRAWN_D5_RECORD_REMOVED_FROM_INDEX: True"
    Invoke-NativeEvidence -Gate "GIT_ADD_ALL" -Executable "git" -Arguments @("add", "-A") -Artifact (Join-Path $evidenceRoot "TD-AXIOM-GIT-PROVENANCE_07_GIT_ADD.txt") | Out-Null
    Invoke-NativeEvidence -Gate "GIT_STATUS_PRE_COMMIT" -Executable "git" -Arguments @("status", "--short") -Artifact (Join-Path $evidenceRoot "TD-AXIOM-GIT-PROVENANCE_07_GIT_STATUS_PRE_COMMIT.txt") | Out-Null
    Invoke-NativeEvidence -Gate "STAGED_DIFF_STAT" -Executable "git" -Arguments @("diff", "--cached", "--stat") -Artifact (Join-Path $evidenceRoot "TD-AXIOM-GIT-PROVENANCE_07_STAGED_DIFF_STAT.txt") | Out-Null
    Invoke-NativeEvidence -Gate "STAGED_VALUE_SCAN" -Executable "python" -Arguments @("scripts/git_provenance_guard.py", "--mode", "evidence") -Artifact (Join-Path $evidenceRoot "TD-AXIOM-GIT-PROVENANCE_08_STAGED_VALUE_SCAN.txt") | Out-Null

    # Step 11 hook is installed before the clean baseline commit so the clean commit proves it.
    Invoke-NativeEvidence -Gate "HOOK_PATH_CONFIG" -Executable "git" -Arguments @("config", "core.hooksPath", ".githooks") -Artifact (Join-Path $evidenceRoot "TD-AXIOM-GIT-PROVENANCE_11_HOOK_CONFIG.txt") | Out-Null
    $demoScratch = Join-Path $repoRoot ".td-provenance-hook-demo.tmp"
    $demo = 'PASS' + 'WORD = "' + [guid]::NewGuid().ToString('N').Substring(0,12) + '"'
    [System.IO.File]::WriteAllText($demoScratch, $demo, $utf8NoBom)
    Invoke-NativeEvidence -Gate "HOOK_DEMO_STAGE" -Executable "git" -Arguments @("add", "--", ".td-provenance-hook-demo.tmp") -Artifact (Join-Path $evidenceRoot "TD-AXIOM-GIT-PROVENANCE_11_HOOK_DEMO_STAGE.txt") | Out-Null
    Invoke-NativeEvidence -Gate "HOOK_DEMO_REJECTION" -Executable "git" -Arguments @("commit", "-m", "TD provenance hook demonstration - must reject") -Artifact (Join-Path $evidenceRoot "TD-AXIOM-GIT-PROVENANCE_11_HOOK_DEMO_REJECTION.txt") -ExpectSuccess $false | Out-Null
    Invoke-NativeEvidence -Gate "HOOK_DEMO_UNSTAGE" -Executable "git" -Arguments @("reset", "--", ".td-provenance-hook-demo.tmp") -Artifact (Join-Path $evidenceRoot "TD-AXIOM-GIT-PROVENANCE_11_HOOK_DEMO_UNSTAGE.txt") | Out-Null
    Remove-Item -LiteralPath $demoScratch -Force -ErrorAction Stop
    Write-Log "D5_DEMO_SCRATCH_DELETED: $(-not (Test-Path -LiteralPath $demoScratch))"
    Invoke-NativeEvidence -Gate "HOOK_CLEAN_GUARD" -Executable "python" -Arguments @("scripts/git_provenance_guard.py", "--mode", "pre-commit") -Artifact (Join-Path $evidenceRoot "TD-AXIOM-GIT-PROVENANCE_11_HOOK_CLEAN_GUARD.txt") | Out-Null

    # Steps 9-10: the one anchored baseline commit and one honest baseline tag.
    $userName = (@(& git config user.name) -join "")
    $userEmail = (@(& git config user.email) -join "")
    if ([string]::IsNullOrWhiteSpace($userName) -or [string]::IsNullOrWhiteSpace($userEmail)) { throw "GIT_IDENTITY_MISSING" }
    $message = "AXIOM v0.62.0 - governance baseline`nAlembic head 20260717_0037 / backend 414 / frontend 61f/276t`nWaves 0-7 CLOSED / UI-001 through UI-007 COMPLETE / Gate CLOSED / Production NOT CERTIFIED`nEstablishes the first anchored baseline (TD-AXIOM-GIT-PROVENANCE)."
    Invoke-NativeEvidence -Gate "BASELINE_COMMIT" -Executable "git" -Arguments @("commit", "-m", $message) -Artifact (Join-Path $evidenceRoot "TD-AXIOM-GIT-PROVENANCE_09_BASELINE_COMMIT.txt") | Out-Null
    $baselineSha = (& git rev-parse HEAD).Trim()
    Write-Log "BASELINE_COMMIT_SHA: $baselineSha"
    $tagMessage = "AXIOM v0.62.0 - first anchored governance baseline.`nAlembic 20260717_0037 / backend 414 / frontend 61f/276t`nWaves 0-7 CLOSED / UI-001 through UI-007 COMPLETE / Gate CLOSED / Production NOT CERTIFIED`nNOTE: no per-phase commit history existed before this baseline. This tag marks the state at UI-007 completion, not the historical completion point of any earlier phase.`nPer-phase tagging begins with the next ITRGA-approved unit."
    Invoke-NativeEvidence -Gate "BASELINE_TAG" -Executable "git" -Arguments @("tag", "-a", "AXIOM_v0.62.0_BASELINE", $baselineSha, "-m", $tagMessage) -Artifact (Join-Path $evidenceRoot "TD-AXIOM-GIT-PROVENANCE_10_BASELINE_TAG.txt") | Out-Null
    Invoke-NativeEvidence -Gate "BASELINE_TAG_VERIFY" -Executable "git" -Arguments @("rev-parse", "--verify", "AXIOM_v0.62.0_BASELINE") -Artifact (Join-Path $evidenceRoot "TD-AXIOM-GIT-PROVENANCE_10_TAG_VERIFY.txt") | Out-Null
    Invoke-NativeEvidence -Gate "TAG_ANNOTATIONS" -Executable "git" -Arguments @("tag", "-n99") -Artifact (Join-Path $evidenceRoot "TD-AXIOM-GIT-PROVENANCE_10_TAG_ANNOTATIONS.txt") | Out-Null
    Invoke-NativeEvidence -Gate "GIT_LOG" -Executable "git" -Arguments @("log", "--oneline", "-3") -Artifact (Join-Path $evidenceRoot "TD-AXIOM-GIT-PROVENANCE_10_GIT_LOG.txt") | Out-Null

    # Step 12: now tag and HEAD identify the same baseline tree.
    $phaseDiffArtifact = Join-Path $evidenceRoot "TD-AXIOM-GIT-PROVENANCE_12_BASELINE_PHASE_DIFF.txt"
    $phaseDiff = & git diff --stat AXIOM_v0.62.0_BASELINE..HEAD 2>&1 | Out-String
    $phaseDiffExit = $LASTEXITCODE
    Write-Artifact -Path $phaseDiffArtifact -Text $phaseDiff
    Write-Log "BASELINE_PHASE_DIFF_EXIT_CODE: $phaseDiffExit"
    if ($phaseDiffExit -ne 0) { throw "BASELINE_PHASE_DIFF_FAILED:$phaseDiffExit" }
    if ($phaseDiff.Trim()) { throw "BASELINE_PHASE_DIFF_NOT_EMPTY" }
    Write-Log "BASELINE_PHASE_DIFF_EMPTY: True"

    # Step 14: content-based proof that this unit changed no forbidden path after the intake snapshot.
    $before = @{}
    Import-Csv -LiteralPath $intakeManifest | ForEach-Object { $before[$_.Path] = $_.SHA256 }
    $afterRows = Get-ProvenanceSnapshot -Root $repoRoot
    $after = @{}
    $afterRows | ForEach-Object { $after[$_.Path] = $_.SHA256 }
    $changedPaths = @($before.Keys + $after.Keys | Sort-Object -Unique | Where-Object { $before[$_] -ne $after[$_] })
    $forbidden = @($changedPaths | Where-Object { Test-ForbiddenPath -Path $_ })
    $permitted = @($changedPaths | Where-Object { -not (Test-ForbiddenPath -Path $_) })
    $intakeCompareArtifact = Join-Path $evidenceRoot "TD-AXIOM-GIT-PROVENANCE_14_INTAKE_COMPARE.txt"
    $compareLines = @(
        "PROVENANCE_UNIT_FORBIDDEN_PATH_MODIFICATIONS: $($forbidden.Count)",
        "PROVENANCE_UNIT_PERMITTED_PATH_MODIFICATIONS: $($permitted.Count)",
        "=== FORBIDDEN PATHS ==="
    ) + $forbidden + @("=== PERMITTED PATHS ===") + $permitted
    Write-Utf8NoBom -Path $intakeCompareArtifact -Lines $compareLines
    $compareLines | ForEach-Object { Write-Log $_ }
    if ($forbidden.Count -ne 0) { throw "PROVENANCE_FORBIDDEN_PATH_MODIFICATIONS_FOUND" }

    $showArtifact = Join-Path $evidenceRoot "TD-AXIOM-GIT-PROVENANCE_14_BASELINE_SHOW_STAT.txt"
    $showStat = & git show --stat --oneline $baselineSha 2>&1 | Out-String
    $showExit = $LASTEXITCODE
    Write-Artifact -Path $showArtifact -Text $showStat
    if ($showExit -ne 0) { throw "BASELINE_SHOW_STAT_FAILED:$showExit" }
    ($showStat -split "`r?`n" | Select-Object -Last 1) | ForEach-Object { Write-Log "BASELINE_SHOW_STAT_TOTAL: $_" }
    Write-Log "BASELINE_SHOW_STAT_DISCLOSURE: baseline files are pre-existing approved v0.62.0 state being anchored for the first time; no provenance-unit forbidden edit is proven by the intake manifest."

    # Step 13a records were staged in the baseline with a tag anchor, never self-closed.
    foreach ($record in @(
        "docs/governance/REPOSITORY_PROVENANCE_PROTOCOL.md",
        "docs/governance/TECHNICAL_DEBT_REGISTER.md",
        "docs/governance/GOVERNANCE_AMENDMENTS.md",
        "PROJECT_STATE.md",
        "CHANGELOG.md"
    )) {
        $recordText = & git show "$baselineSha`:$record" 2>&1 | Out-String
        if ($LASTEXITCODE -ne 0) { throw "BASELINE_RECORD_MISSING:$record" }
        Write-Log "BASELINE_RECORD_PRESENT: $record"
    }
    Write-Log "TD_AXIOM_GIT_PROVENANCE_STATUS: REMEDIATION_SUBMITTED_AWAITING_ITRGA_DETERMINATION"

    # Step 15: unchanged full regression / schema / networked CI evidence.
    Push-Location (Join-Path $repoRoot "frontend")
    try {
        Invoke-NativeEvidence -Gate "FRONTEND_VITEST" -Executable "npm" -Arguments @("test", "--", "--reporter=verbose") -Artifact (Join-Path $evidenceRoot "TD-AXIOM-GIT-PROVENANCE_15_FRONTEND_VITEST.txt") | Out-Null
        Invoke-NativeEvidence -Gate "FRONTEND_TSC" -Executable "npx" -Arguments @("tsc", "-b", "--pretty", "false") -Artifact (Join-Path $evidenceRoot "TD-AXIOM-GIT-PROVENANCE_15_FRONTEND_TSC.txt") | Out-Null
        Invoke-NativeEvidence -Gate "FRONTEND_BUILD" -Executable "npm" -Arguments @("run", "build") -Artifact (Join-Path $evidenceRoot "TD-AXIOM-GIT-PROVENANCE_15_FRONTEND_BUILD.txt") | Out-Null
    } finally { Pop-Location }
    Push-Location (Join-Path $repoRoot "backend")
    try {
        Invoke-NativeEvidence -Gate "BACKEND_RUFF" -Executable "python" -Arguments @("-m", "ruff", "check", ".") -Artifact (Join-Path $evidenceRoot "TD-AXIOM-GIT-PROVENANCE_15_BACKEND_RUFF.txt") | Out-Null
        Invoke-NativeEvidence -Gate "BACKEND_PYTEST" -Executable "python" -Arguments @("-m", "pytest", "-q") -Artifact (Join-Path $evidenceRoot "TD-AXIOM-GIT-PROVENANCE_15_BACKEND_PYTEST.txt") | Out-Null
        Invoke-NativeEvidence -Gate "ALEMBIC_CURRENT" -Executable "python" -Arguments @("-m", "alembic", "current") -Artifact (Join-Path $evidenceRoot "TD-AXIOM-GIT-PROVENANCE_15_ALEMBIC_CURRENT.txt") | Out-Null
    } finally { Pop-Location }
    Invoke-NativeEvidence -Gate "LOCAL_CI" -Executable "bash" -Arguments @((Join-Path $repoRoot "scripts\local_ci.sh")) -Artifact (Join-Path $evidenceRoot "TD-AXIOM-GIT-PROVENANCE_15_LOCAL_CI.txt") | Out-Null

    Write-Log "TD_AXIOM_GIT_PROVENANCE_COMPLETED_AWAITING_ITRGA_REVIEW"
    $global:LASTEXITCODE = 0
}
catch {
    Write-Log "TD_AXIOM_GIT_PROVENANCE_COMPLETED_WITH_FINDINGS"
    Write-Log "TD_AXIOM_GIT_PROVENANCE_ERROR: $($_.Exception.Message)"
    $global:LASTEXITCODE = 1
}
finally {
    Write-Log "TD_AXIOM_GIT_PROVENANCE_FINISHED: $((Get-Date).ToString('o'))"
    Write-Utf8NoBom -Path $operatorResults -Lines @($logLines)
}

exit $global:LASTEXITCODE
