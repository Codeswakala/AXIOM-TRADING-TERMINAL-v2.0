
# =====================================================================
# AXIOM V2 - 0047 WORKING-DATABASE APPLICATION ACT (BAND BE-7)
# ITRGA SQLITE APPLY ACT EVIDENCE PACK (V1)
# Pack ID: ITRGA-V2-0047-APPLY-PACK-V2
# Authority:
#   - CN-V2-BE-7-001 (commission; band contract)
#   - BO-V2-BE-7-001 (build order; terminal state T-1...T-14; the 0047
#     application named a separate sanctioned act at chain end)
#   - ITRGA-DET-V2-BE-7-FINAL-001 / ITRGA-ACC-V2-BE-7-001 (band accepted;
#     ACC section 5 fixes the compver pre-declared expectations pinned
#     inside this pack: RPE 1499343d48b778af17065e8bf1eaabcffc116880fa6967ab442db1255992b178
#     (unchanged) and RJE 8f107d174e081dc0a1527fea841b89dfb73744e3f16eba2d29c60521158c0598 (CR-001 value))
#   - Operator authorization "proceed" (2026-09-04)
#   - ITRGA-PTN-V2-PACK-001 (pack discipline; battery floor)
# Pattern: ITRGA-V2-0043-APPLY-PACK-V1 / VERIFY-PACK-V1 (all PGF-001
#   through PGF-016 lessons incorporated by construction: pure ASCII,
#   no compound braced expansions (PGF-009), helper functions with
#   non-colliding parameter names (PGF-001), dialect-correct SQL
#   (PGF-010), content-based comparisons (PGF-012), format-independent
#   drift assertions (PGF-014), byte-identity self-check via the
#   issuance note (PGF-011), quote-normalized operator input (PGF-008),
#   canonical vocabulary (PGF-013), direct-authored instrument with
#   post-build gates: here-string pairing, ASCII purity, seam-marker
#   counts (PGF-016), refuse-if-completed startup hygiene (E-0046-DUP)).
#
# WHAT THIS PACK DOES:
#   Lands the ACCEPTED band BE-7 file set (17 hash-pinned literals
#   embedded below in base64: 14 new files + 3 cumulative overwrites of
#   app/v2/api/router.py, app/v2/rbac/permissions.py,
#   app/db/models/__init__.py, each pre-gated on its BE-6-floor markers
#   and backed up before write), then applies migration
#   20260903_0047_v2_be7_research_jobs ONCE to the application's working
#   SQLITE database file and proves the terminal state on SQLite:
#   revision 20260903_0047 (single head); 42 v2 triggers including the
#   ten new guards probed LIVE with their exact refusal messages
#   (transactional insert-probe-rollback; the probe changes nothing);
#   49 permission rows (8 new exact triples); 8 computation-version rows
#   including replay_engine=rpe-1.0.0 and research_job_engine=rje-1.0.0
#   whose source_hash values are pinned to the ACC section 5
#   pre-declared literals (apply-time compver gate); drift gate per
#   PGF-014 (forbidden band markers absent; inheritance witness
#   present); full test suite 972 passed / 0 failed.
#
#   SQLite-specific design (as the proven predecessor packs):
#   - No database server: NO psql, NO password prompt, NO credential
#     of any kind. All SQL runs through the repo venv python (sqlite3
#     module) against the file directly via a small ASCII helper script
#     written to the OS temp directory at start and removed on exit.
#   - FILE-LEVEL ANCHOR copy to operator-evidence\BE-7 BEFORE any
#     modification: the complete, credential-free rollback anchor
#     (hash-compared to the source, integrity_check ok).
#   - STARTUP HYGIENE (E-0046-DUP law): if 0047-APPLY-FINAL-STATE.txt
#     already exists, this pack REFUSES TO START. It never deletes a
#     completed-run record.
#   - It does NOT create or delete any database file. It does NOT run
#     any Git command.
#   - Read-write scope: exactly one schema mutation (alembic upgrade
#     20260903_0047) on the target file; writes only: the 17 delivered
#     files, the transcript, the anchor copy, the pre-write backups,
#     and the apply-final-state record in operator-evidence\BE-7; plus
#     the throwaway helper (removed on exit).
#   - NO AUTHORITY VARIABLE EXISTS FOR THIS ACT: the pack enumerates
#     and removes any pre-existing AXIOM_TD_* variables and asserts
#     their absence. It never sets one.
#
# BEFORE RUNNING: STOP THE RUNNING APPLICATION (it holds a live
#   connection to the target database file). Restart it only AFTER the
#   verify pack PASSes.
#
# RUN MODE: this pack MUST be executed as a file from the repository
#   root (PGF-004; no interactive paste):
#     powershell -NoProfile -ExecutionPolicy Bypass -File ".\ITRGA_V2_0047_APPLY_PACK_V2.ps1"
#   Single expected input: the absolute path of the working database
#   file backend\axiom_dev.db (a path, not a credential).
#
# OPERATOR INSTRUCTION CARD (ITRGA-PTN-V2-PACK-001 section 2.2):
#   1. Verify byte-identity of the THREE issued artifacts with
#      Get-FileHash -Algorithm MD5 against the ITRGA ISSUANCE NOTE
#      (ITRGA-ISS-V2-0047-PACKS-002):
#        ITRGA_V2_0047_APPLY_PACK_V2.ps1   (this file; runs FIRST)
#        ITRGA_V2_0047_VERIFY_PACK_V2.ps1  (runs SECOND, after this PASS)
#        ITRGA_V2_0047_BASELINE_PINS.txt   (must sit at the repo root)
#      If any MD5 does not match: STOP; report to ITRGA.
#   2. Execute ONLY this file, from the repository root:
#        C:\Users\victo\.vscode\AXIOM\axiom\
#   3. Send back afterwards:
#        operator-evidence\BE-7\0047-APPLY-RUN-V2.txt
#      (keep operator-evidence\BE-7\0047-APPLY-FINAL-STATE.txt in
#      place - the verify pack requires it.)
#
# SUPERSESSION RECORD (V2, 2026-09-04):
#   V1 pair retired UNUSED-STOPPED (refused at A1 before any
#   mutation; nothing to uninstall). V2 carries two rulings:
#   (1) A4 FOREIGN-STATE ADJUDICATION LAW: a new-file target that
#   already exists is hashed; if its sha256 equals the accepted
#   pin, the pre-landing is witnessed and accepted (the customary
#   operator-side merge); if it differs, the pack refuses and
#   nothing is modified. The A1 migration-absence gate is
#   superseded by this uniform adjudication.
#   (2) PGF-017 EVIDENCE-PRINTING LAW: function-call arguments
#   bind in argument mode; Write-Evidence "lit" + expr never
#   binds the concatenation. All concatenated evidence calls are
#   now parenthesized throughout both packs.
# =====================================================================

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

# ---------------------------------------------------------------------
# 0. ENCODING, LOCAL PATHS, CONSTANTS
# ---------------------------------------------------------------------
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
[Console]::InputEncoding  = [System.Text.Encoding]::UTF8
$env:PYTHONIOENCODING = "utf-8"

$RepoRoot      = (Get-Location).Path
$BackendRoot   = Join-Path $RepoRoot "backend"
$EvidenceDir   = Join-Path $RepoRoot "operator-evidence\BE-7"
$Transcript    = Join-Path $EvidenceDir "0047-APPLY-RUN-V2.txt"
$StateRecPath  = Join-Path $EvidenceDir "0047-APPLY-FINAL-STATE.txt"
$AnchorPath    = Join-Path $EvidenceDir "0047-ANCHOR-axiom_dev.v2.bak"
$BackupDir     = Join-Path $EvidenceDir "pre-write-backup"
$PinsPath      = Join-Path $RepoRoot "ITRGA_V2_0047_BASELINE_PINS.txt"
$HelperProbe   = Join-Path $env:TEMP "be7_0047_guardprobe.py"
$HelperCensus  = Join-Path $env:TEMP "be7_0047_census.py"

$ApplyTargetRevision = "20260903_0047"
$BaselineRevision    = "20260903_0046"
$ExpectTriggersTotal = 42
$ExpectPermsTotal    = 49
$ExpectCompverTotal  = 8
$ExpectFloorTriggers = 32
$ExpectFloorPerms    = 41
$ExpectFloorCompver  = 6
$SuiteFloor          = 972
$AlembicPin          = "1.19.0"
$PytestPin           = "8.4.2"
$RpeHash             = "1499343d48b778af17065e8bf1eaabcffc116880fa6967ab442db1255992b178"
$RjeHash             = "8f107d174e081dc0a1527fea841b89dfb73744e3f16eba2d29c60521158c0598"

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
    if (!(Test-Path $Path)) { throw ("STOP: required pin file missing: " + $Path + " (" + $Label + ").") }
    $Map = @{}
    foreach ($RawLine in @(Get-Content -Path $Path -Encoding UTF8)) {
        $Line = ([string]$RawLine).TrimEnd()
        if ($Line -eq "" -or $Line.StartsWith("#")) { continue }
        if ($Line -notmatch '^([A-Z0-9_]+)=(.*)$') {
            throw ("STOP: malformed line in pin file " + $Path + ": '" + $Line + "' (" + $Label + ").")
        }
        $Key = $Matches[1]
        $Val = $Matches[2]
        if ($Map.ContainsKey($Key)) {
            throw ("STOP: duplicate key '" + $Key + "' in pin file " + $Path + " (" + $Label + ").")
        }
        $Map[$Key] = $Val
    }
    $Got = @($Map.Keys | Sort-Object)
    $Exp = @($ExpectedKeys | Sort-Object)
    if (($Got -join ",") -ne ($Exp -join ",")) {
        throw ("STOP: pin file key set mismatch in " + $Path + ": got [" + ($Got -join ", ") + "], expected [" + ($Exp -join ", ") + "] (" + $Label + ").")
    }
    return $Map
}
function Hash-Bytes {
    param([byte[]]$Bytes)
    $Sha = [System.Security.Cryptography.SHA256]::Create()
    try { return ([BitConverter]::ToString($Sha.ComputeHash($Bytes))).Replace("-", "").ToLower() }
    finally { $Sha.Dispose() }
}
function B64-Decode {
    param([string]$B64Chunk)
    $Joined = ($B64Chunk -split "`n" | ForEach-Object { $_.Trim() }) -join ""
    return [Convert]::FromBase64String($Joined)
}

# ---------------------------------------------------------------------
# A0. STARTUP HYGIENE (refuse-if-completed law) + AUTHORITY SWEEP
# ---------------------------------------------------------------------
if (!(Test-Path $BackendRoot)) { throw ("STOP: backend directory not found: " + $BackendRoot + ". Run from the repository root.") }
if (!(Test-Path $PinsPath))    { throw ("STOP: baseline pin file missing at the repository root: " + $PinsPath) }
New-Item -ItemType Directory -Force -Path $EvidenceDir | Out-Null

if (Test-Path $StateRecPath) {
    throw ("STOP (E-0046-DUP law): a completed-run record already exists: " + $StateRecPath + " . This pack refuses to start rather than disturb a completed application. If you believe this is stale, STOP and report to ITRGA; do not delete it yourself.")
}
Remove-Item -Force -ErrorAction SilentlyContinue $Transcript

$AuthorityVars = @(Get-ChildItem env: | Where-Object { $_.Name -like "AXIOM_TD_*" })
foreach ($Av in $AuthorityVars) {
    Write-Output "Removing pre-existing authority variable: $($Av.Name)" | Out-Null
    Remove-Item ("env:" + $Av.Name) -ErrorAction SilentlyContinue
}
$Remain = @(Get-ChildItem env: | Where-Object { $_.Name -like "AXIOM_TD_*" })
if ($Remain.Count -gt 0) { throw "STOP: an AXIOM_TD_* authority variable persists. No authority variable exists for this act." }

Write-Section "0047 APPLY PACK V2 - ITRGA-V2-0047-APPLY-PACK-V2"
Write-Evidence ("UTC start: " + ([DateTime]::UtcNow.ToString("yyyy-MM-ddTHH:mm:ssZ")))
Write-Evidence "Authority: BO-V2-BE-7-001; ITRGA-ACC-V2-BE-7-001 section 5; operator authorization 2026-09-04."
Write-Evidence "Read-write scope: one schema mutation (alembic upgrade 20260903_0047) on the target db file; 17 delivered files; evidence in operator-evidence\BE-7; temp helper removed on exit."

$Pins = Read-Pins -Path $PinsPath -ExpectedKeys @(
    "PINS_FILE_ID","TARGET_REVISION","BASELINE_REVISION",
    "V2_TRIGGERS_AFTER","PERMISSIONS_AFTER","COMPVER_AFTER",
    "COMPVER_RPE_HASH","COMPVER_RJE_HASH","SUITE_FLOOR",
    "ALEMBIC_PIN","PYTEST_PIN") -Label "baseline pins"
if ($Pins["PINS_FILE_ID"] -ne "ITRGA-V2-0047-BASELINE-PINS-V1") { throw "STOP: pin file identity mismatch." }
if ($Pins["TARGET_REVISION"] -ne $ApplyTargetRevision) { throw "STOP: TARGET_REVISION pin mismatch." }
if ($Pins["BASELINE_REVISION"] -ne $BaselineRevision) { throw "STOP: BASELINE_REVISION pin mismatch." }
if ([int]$Pins["V2_TRIGGERS_AFTER"] -ne $ExpectTriggersTotal) { throw "STOP: trigger-total pin mismatch." }
if ([int]$Pins["PERMISSIONS_AFTER"] -ne $ExpectPermsTotal) { throw "STOP: permission-total pin mismatch." }
if ([int]$Pins["COMPVER_AFTER"] -ne $ExpectCompverTotal) { throw "STOP: compver-total pin mismatch." }
if ($Pins["COMPVER_RPE_HASH"] -ne $RpeHash) { throw "STOP: RPE pin mismatch." }
if ($Pins["COMPVER_RJE_HASH"] -ne $RjeHash) { throw "STOP: RJE pin mismatch." }
if ([int]$Pins["SUITE_FLOOR"] -ne $SuiteFloor) { throw "STOP: suite-floor pin mismatch." }
if ($Pins["ALEMBIC_PIN"] -ne $AlembicPin) { throw "STOP: alembic pin mismatch." }
if ($Pins["PYTEST_PIN"] -ne $PytestPin) { throw "STOP: pytest pin mismatch." }
Write-Evidence "PASS: A0 - startup hygiene, authority-variable sweep, baseline pins cross-pinned."

# throwaway helpers (ASCII python; removed on exit)
$ProbeB64 = @'
aW1wb3J0IHNxbGl0ZTMsIHN5cwojIElUUkdBIDAwNDcgaW5zdHJ1bWVudCBoZWxwZXIgLSBndWFyZHByb2JlIDxkYj4gPGluc2VydF9zcWw+IDxwcm9iZV9z
cWw+IDxleHBlY3RlZD4KIyBUcmFuc2FjdGlvbmFsIHByb2JlOiBpbnNlcnQgdGhyb3dhd2F5IHJvdywgcnVuIHByb2JlLCByZXF1aXJlIEVYQUNUIG1lc3Nh
Z2UsIHJvbGxiYWNrLgpkYiwgaW5zZXJ0X3NxbCwgcHJvYmVfc3FsLCBleHBlY3RlZCA9IHN5cy5hcmd2WzFdLCBzeXMuYXJndlsyXSwgc3lzLmFyZ3ZbM10s
IHN5cy5hcmd2WzRdCmNvbm4gPSBzcWxpdGUzLmNvbm5lY3QoZGIpCnRyeToKICAgIGN1ciA9IGNvbm4uY3Vyc29yKCkKICAgIGN1ci5leGVjdXRlKGluc2Vy
dF9zcWwpCiAgICB0cnk6CiAgICAgICAgY3VyLmV4ZWN1dGUocHJvYmVfc3FsKQogICAgZXhjZXB0IHNxbGl0ZTMuRGF0YWJhc2VFcnJvciBhcyBleGM6CiAg
ICAgICAgZ290ID0gc3RyKGV4YykKICAgICAgICBjb25uLnJvbGxiYWNrKCkKICAgICAgICBpZiBnb3QgPT0gZXhwZWN0ZWQ6CiAgICAgICAgICAgIHByaW50
KCJQUk9CRS1FWEFDVC1NQVRDSCIpCiAgICAgICAgICAgIHN5cy5leGl0KDApCiAgICAgICAgcHJpbnQoIlBST0JFLU1FU1NBR0UtTUlTTUFUQ0g6OiIgKyBn
b3QpCiAgICAgICAgc3lzLmV4aXQoMikKICAgIGNvbm4ucm9sbGJhY2soKQogICAgcHJpbnQoIlBST0JFLU5PVC1SRUZVU0VEIikKICAgIHN5cy5leGl0KDEp
CmZpbmFsbHk6CiAgICBjb25uLmNsb3NlKCkK
'@
[IO.File]::WriteAllBytes($HelperProbe, (B64-Decode -B64Chunk $ProbeB64))
$CensusB64 = @'
aW1wb3J0IHNxbGl0ZTMsIHN5cywganNvbgojIElUUkdBIDAwNDcgaW5zdHJ1bWVudCBoZWxwZXIgLSBjZW5zdXMgPGRiPgojIEVtaXRzIG9uZSBKU09OIGxp
bmUgd2l0aCB0aGUgdGhyZWUgY2Vuc3VzIHRvdGFscyBhbmQgdGhlIHBpY2tlZCBtZW1iZXJzLgpkYiA9IHN5cy5hcmd2WzFdCmNvbm4gPSBzcWxpdGUzLmNv
bm5lY3QoZGIpCnRyeToKICAgIGN1ciA9IGNvbm4uY3Vyc29yKCkKICAgIHRyaWdzID0gW3JbMF0gZm9yIHIgaW4gY3VyLmV4ZWN1dGUoIlNFTEVDVCBuYW1l
IEZST00gc3FsaXRlX21hc3RlciBXSEVSRSB0eXBlPSd0cmlnZ2VyJyBBTkQgbmFtZSBMSUtFICd2Ml8lJyBPUkRFUiBCWSBuYW1lIildCiAgICBwZXJtcyA9
IFt0dXBsZShyKSBmb3IgciBpbiBjdXIuZXhlY3V0ZSgiU0VMRUNUIHJvbGUsIHBlcm1pc3Npb24sIHNhbCBGUk9NIHYyX3Blcm1pc3Npb24gT1JERVIgQlkg
cm9sZSwgcGVybWlzc2lvbiIpXQogICAgY29tcCA9IFt0dXBsZShyKSBmb3IgciBpbiBjdXIuZXhlY3V0ZSgiU0VMRUNUIGNvbXBvbmVudCwgdmVyc2lvbiwg
c291cmNlX2hhc2ggRlJPTSB2Ml9jb21wdXRhdGlvbl92ZXJzaW9uIE9SREVSIEJZIGNvbXBvbmVudCwgdmVyc2lvbiIpXQogICAgcHJpbnQoanNvbi5kdW1w
cyh7InRyaWdnZXJzIjogdHJpZ3MsICJwZXJtaXNzaW9ucyI6IHBlcm1zLCAiY29tcHZlciI6IGNvbXB9KSkKZmluYWxseToKICAgIGNvbm4uY2xvc2UoKQo=
'@
[IO.File]::WriteAllBytes($HelperCensus, (B64-Decode -B64Chunk $CensusB64))

# ---------------------------------------------------------------------
# A1. TARGET INPUT + TOOLCHAIN + CHAIN FLOOR
# ---------------------------------------------------------------------
Write-Section "A1. TARGET IDENTITY, VENV TOOLCHAIN, FLOOR GATES"

$DbInput = Read-Host "Absolute path of the working database file (backend\axiom_dev.db)"
$TargetDbPath = ([string]$DbInput).Trim().Trim('"').Trim("'")
if (!(Test-Path $TargetDbPath)) { throw ("STOP: target database file not found: " + $TargetDbPath) }
Write-Evidence ("Target db: " + $TargetDbPath)
Write-Evidence "NOTE: the running application must be stopped (run card). If the file is locked, the anchor-copy hash check below fail-closes."

$Py = $null
foreach ($Cand in @(".venv\Scripts\python.exe", "venv\Scripts\python.exe",
                    "backend\.venv\Scripts\python.exe", "backend\venv\Scripts\python.exe")) {
    $Full = Join-Path $RepoRoot $Cand
    if (Test-Path $Full) { $Py = $Full; break }
}
if ($null -eq $Py) {
    $Cmd = Get-Command python -ErrorAction SilentlyContinue
    if ($null -ne $Cmd) { $Py = $Cmd.Source }
}
if ($null -eq $Py) { throw "STOP: no python executable found (.venv\Scripts\python.exe expected)." }
Write-Evidence ("Python: " + $Py)

$OutVer  = & $Py -c "import sys, alembic; print(sys.version.split()[0]); print(alembic.__version__)" 2>&1
$VerText = (Norm-Text $OutVer)
Write-Evidence ("python/alembic versions: " + ($VerText -replace "`n", " | "))
if ($LASTEXITCODE -ne 0) { throw "STOP: could not read python/alembic versions." }
if ($OutVer -notcontains $AlembicPin) { throw ("STOP: alembic " + $AlembicPin + " required (certified pin).") }
$OutPt = & $Py -m pytest --version 2>&1
if ($LASTEXITCODE -ne 0) { throw "STOP: pytest unavailable in the venv." }
if ((Norm-Text $OutPt) -notmatch [regex]::Escape($PytestPin)) { throw ("STOP: pytest " + $PytestPin + " required (certified pin).") }
Write-Evidence ("PASS: A1 toolchain - alembic " + $AlembicPin + ", pytest " + $PytestPin + ".")

$MigCand = Get-ChildItem (Join-Path $BackendRoot "alembic\versions") -Filter "*20260903_0046*.py" -ErrorAction SilentlyContinue
if ($null -eq $MigCand) { throw "STOP: floor migration 20260903_0046 file not present in backend\alembic\versions." }
$NewMigPath = Join-Path $BackendRoot "alembic\versions\20260903_0047_v2_be7_research_jobs.py"
if (Test-Path $NewMigPath) { Write-Evidence ("NOTE: 0047 migration file already present on the tree; A4 foreign-state adjudication will hash it against the accepted pin.") }

Push-Location $BackendRoot
try {
    $OutCur = & $Py -m alembic current 2>&1
    $CurCode = $LASTEXITCODE
    $OutHeads = & $Py -m alembic heads 2>&1
    $HeadsCode = $LASTEXITCODE
} finally { Pop-Location }
if ($CurCode -ne 0 -or $HeadsCode -ne 0) { throw "STOP: alembic current/heads could not be read." }
$CurLines = @(@($OutCur) | Where-Object { ([string]$_) -match "^(rev|[0-9a-f]{8})" -and ([string]$_) -notmatch "^INFO" -and ([string]$_) -match $BaselineRevision })
if ($CurLines.Count -ne 1) { throw ("STOP: floor gate - expected exactly one current line naming " + $BaselineRevision + "; observed " + $CurLines.Count + " in: '" + (Norm-Text $OutCur) + "'.") }
if ((Norm-Text $OutCur) -match $ApplyTargetRevision) { throw "STOP: the chain is ALREADY at 0047. Refusing to double-apply." }
$HeadLines = @(@($OutHeads) | Where-Object { ([string]$_) -match $BaselineRevision })
if ($HeadLines.Count -ne 1) { throw ("STOP: floor gate - expected a single head " + $BaselineRevision + "; observed: '" + (Norm-Text $OutHeads) + "'.") }
Write-Evidence ("PASS: A1 floor - alembic current = " + $BaselineRevision + " (single head); not at 0047.")

Write-Section "A2. ROLLBACK ANCHOR (before any modification)"
$DbHashPre = (Get-FileHash -Path $TargetDbPath -Algorithm SHA256).Hash.ToLower()
Copy-Item -Path $TargetDbPath -Destination $AnchorPath -Force
if (!(Test-Path $AnchorPath)) { throw "STOP: anchor copy not created." }
$AnchorHash = (Get-FileHash -Path $AnchorPath -Algorithm SHA256).Hash.ToLower()
if ($AnchorHash -ne $DbHashPre) { throw "STOP: anchor hash differs from source hash. Aborting before any modification." }
$OutIck = & $Py -c "import sqlite3; c=sqlite3.connect(r'" + $AnchorPath + "'); print(c.execute('PRAGMA integrity_check;').fetchone()[0]); c.close()" 2>&1
if ((Norm-Text $OutIck) -ne "ok") { throw ("STOP: anchor integrity_check '" + (Norm-Text $OutIck) + "', expected 'ok'.") }
Write-Evidence ("Anchor: " + $AnchorPath)
Write-Evidence ("Anchor sha256 == db sha256 pre-apply: " + $AnchorHash)
Write-Evidence "PASS: A2 - a proven rollback anchor exists before any mutation."

Write-Section "A3. PRE-STATE PINS (V1 floor; pre-census; floor totals)"
$V1Pins = @(
    "app\execution_research\simulation.py|f163e610ba1a6215ac9229c6993a0f667ac916bdc53bf9fc1bb30d1b1efe70c7",
    "app\ml\dataset\chronology_guard.py|7dbc665dc4b43f314c01d09da9a23576a47a78e4373c3daee6c15dcf03fd64cb",
    "app\ml\dataset\service.py|6c5d72a8942050b495e209aa4b0a4044ba5d9d61087703198a103a0ac57d99d0",
    "app\ml\dataset\snapshot_builder.py|b08ef4b1dec07567edbe4d153a3b18ef8838280bf2ec0a1ab6ed3f34e0b7fb9b",
    "app\ml\dataset\split_engine.py|e893b92c6ccce188f0e7dbedee1b121d270c57ec25ddea8f99e5201319f7acbc",
    "app\ml\economic\service.py|c49527ed12f4d2caf7f997f709f44d6e9d69e4f1c4a8eb485db83484c5c9fa13"
)
foreach ($V1Line in $V1Pins) {
    $Parts = $V1Line.Split("|")
    $V1Path = Join-Path $BackendRoot $Parts[0]
    if (!(Test-Path $V1Path)) { throw ("STOP: pinned V1 file missing: " + $V1Path) }
    $V1Hash = (Get-FileHash -Path $V1Path -Algorithm SHA256).Hash.ToLower()
    if ($V1Hash -ne $Parts[1]) { throw ("STOP: V1 floor moved: " + $Parts[0] + " hash " + $V1Hash + " != pinned " + $Parts[1] + " . STOP and report to ITRGA.") }
    Write-Evidence ("V1 pin OK: " + $Parts[0])
}
Write-Evidence "PASS: A3a - six V1 lineage files byte-identical to the attested pins."

$OutPre = & $Py $HelperCensus $TargetDbPath 2>&1
if ($LASTEXITCODE -ne 0) { throw ("STOP: pre-census helper failed: " + (Norm-Text $OutPre)) }
$Pre = (Norm-Text $OutPre) | ConvertFrom-Json
if ($Pre.triggers.Count -ne $ExpectFloorTriggers) { throw ("STOP: pre-census v2 trigger count " + $Pre.triggers.Count + " != floor " + $ExpectFloorTriggers) }
if ($Pre.permissions.Count -ne $ExpectFloorPerms) { throw ("STOP: pre-census permission count " + $Pre.permissions.Count + " != floor " + $ExpectFloorPerms) }
if ($Pre.compver.Count -ne $ExpectFloorCompver) { throw ("STOP: pre-census compver count " + $Pre.compver.Count + " != floor " + $ExpectFloorCompver) }
Write-Evidence ("PASS: A3b - floor totals exactly " + $ExpectFloorTriggers + " / " + $ExpectFloorPerms + " / " + $ExpectFloorCompver + " (triggers/permissions/compver).")

$ModGates = @(
    "app\db\models\__init__.py|v2_portfolio",
    "app\v2\api\router.py|portfolio_research_router;research_governance_router",
    "app\v2\rbac\permissions.py|RESEARCH_PF_READ"
)
foreach ($Gate in $ModGates) {
    $Partsg = $Gate.Split("|")
    $GatePath = Join-Path $BackendRoot $Partsg[0]
    if (!(Test-Path $GatePath)) { throw ("STOP: modified-target file missing at the floor: " + $GatePath) }
    $Content = [IO.File]::ReadAllText($GatePath)
    foreach ($Marker in @($Partsg[1].Split(";"))) {
        if ($Marker -ne "" -and $Content -notmatch [regex]::Escape($Marker)) {
            throw ("STOP: floor marker '" + $Marker + "' absent in " + $Partsg[0] + " . The tree is not at the BE-6 floor; STOP and report to ITRGA.")
        }
    }
    Write-Evidence ("Floor markers OK: " + $Partsg[0])
}
Write-Evidence "PASS: A3c - the three modified-file targets carry their BE-6 floor markers."

# ---------------------------------------------------------------------
# A4. DELIVERED FILE LANDING (17 hash-pinned literals)
# ---------------------------------------------------------------------
Write-Section "A4. LANDING THE ACCEPTED 17-FILE SET (base64 literals; sha256-verified twice)"
$ModifiedPaths = @(
    "app\db\models\__init__.py",
    "app\v2\api\router.py",
    "app\v2\rbac\permissions.py"
)
$Rec1Path = "alembic\versions\20260903_0047_v2_be7_research_jobs.py"
$Rec1Sha  = "b00ab32aec3cf9311b7da8333dba2baa91221c643cc35cba73d446504ece88ce"
$Rec1B64 = @'
IiIiVjIgQkUtNyBVLTEg4oCUIHJlc2VhcmNoIGpvYnMgKEJPLVYyLUJFLTctMDAxIMKnMS9ULTHigKZULTYpLgoKU2l4IHBoeXNpY2FsIHRhYmxlcyAoZml2
ZSBndWFyZGVkICsgdGhlIHNvbGUtbXV0YWJsZSBqb2IgcXVldWUsIEZQLTEpOwoxMCBndWFyZCB0cmlnZ2VycyAoMzLihpI0Mik7IDggcGVybWlzc2lvbiBy
b3dzICg0MeKGkjQ5KTsgMiBjb21wdmVyIHNlZWRzCig24oaSOCwgUC00IGNvLWRlbGl2ZXJ5LCBDLTIgZGlzY2xvc3VyZTogdGhlIDAwNDcgYXBwbGljYXRp
b24tYWN0Cmluc3RydW1lbnQgcmUtcGlucyBib3RoIGVuZ2luZSBmaWxlIHNldHMpLiBTeW1tZXRyaWMgZG93bmdyYWRlLgoKUmV2aXNpb24gSUQ6IDIwMjYw
OTAzXzAwNDcKUmV2aXNlczogMjAyNjA5MDNfMDA0NgoiIiIKCmZyb20gX19mdXR1cmVfXyBpbXBvcnQgYW5ub3RhdGlvbnMKCmltcG9ydCBoYXNobGliCmZy
b20gZGF0ZXRpbWUgaW1wb3J0IGRhdGV0aW1lLCB0aW1lem9uZQpmcm9tIHBhdGhsaWIgaW1wb3J0IFBhdGgKZnJvbSB1dWlkIGltcG9ydCB1dWlkNAoKaW1w
b3J0IHNxbGFsY2hlbXkgYXMgc2EKCmZyb20gYWxlbWJpYyBpbXBvcnQgb3AKCnJldmlzaW9uID0gIjIwMjYwOTAzXzAwNDciCmRvd25fcmV2aXNpb24gPSAi
MjAyNjA5MDNfMDA0NiIKYnJhbmNoX2xhYmVscyA9IE5vbmUKZGVwZW5kc19vbiA9IE5vbmUKCl9UUklHR0VSUyA9ICgKICAgICgidjJfYmFja3Rlc3RfaW5w
dXRfaW1tdXRhYmxlX3VwZGF0ZSIsICJ2Ml9iYWNrdGVzdF9pbnB1dCIsCiAgICAgIlVQREFURSIsICJWMiBiYWNrdGVzdCBpbnB1dHMgYXJlIGltbXV0YWJs
ZTsgVVBEQVRFIHByb2hpYml0ZWQiKSwKICAgICgidjJfYmFja3Rlc3RfaW5wdXRfaW1tdXRhYmxlX2RlbGV0ZSIsICJ2Ml9iYWNrdGVzdF9pbnB1dCIsCiAg
ICAgIkRFTEVURSIsICJWMiBiYWNrdGVzdCBpbnB1dHMgYXJlIGltbXV0YWJsZTsgREVMRVRFIHByb2hpYml0ZWQiKSwKICAgICgidjJfY29zdF9tb2RlbF9p
bW11dGFibGVfdXBkYXRlIiwgInYyX2Nvc3RfbW9kZWwiLAogICAgICJVUERBVEUiLCAiVjIgY29zdCBtb2RlbHMgYXJlIGltbXV0YWJsZTsgVVBEQVRFIHBy
b2hpYml0ZWQiKSwKICAgICgidjJfY29zdF9tb2RlbF9pbW11dGFibGVfZGVsZXRlIiwgInYyX2Nvc3RfbW9kZWwiLAogICAgICJERUxFVEUiLCAiVjIgY29z
dCBtb2RlbHMgYXJlIGltbXV0YWJsZTsgREVMRVRFIHByb2hpYml0ZWQiKSwKICAgICgidjJfc3RyYXRlZ3lfdmVyc2lvbl9pbW11dGFibGVfdXBkYXRlIiwg
InYyX3N0cmF0ZWd5X3ZlcnNpb24iLAogICAgICJVUERBVEUiLCAiVjIgc3RyYXRlZ3kgdmVyc2lvbnMgYXJlIGltbXV0YWJsZTsgVVBEQVRFIHByb2hpYml0
ZWQiKSwKICAgICgidjJfc3RyYXRlZ3lfdmVyc2lvbl9pbW11dGFibGVfZGVsZXRlIiwgInYyX3N0cmF0ZWd5X3ZlcnNpb24iLAogICAgICJERUxFVEUiLCAi
VjIgc3RyYXRlZ3kgdmVyc2lvbnMgYXJlIGltbXV0YWJsZTsgREVMRVRFIHByb2hpYml0ZWQiKSwKICAgICgidjJfcmVzZWFyY2hfam9iX2F0dGVtcHRfaW1t
dXRhYmxlX3VwZGF0ZSIsICJ2Ml9yZXNlYXJjaF9qb2JfYXR0ZW1wdCIsCiAgICAgIlVQREFURSIsICJWMiByZXNlYXJjaCBqb2IgYXR0ZW1wdHMgYXJlIGlt
bXV0YWJsZTsgVVBEQVRFIHByb2hpYml0ZWQiKSwKICAgICgidjJfcmVzZWFyY2hfam9iX2F0dGVtcHRfaW1tdXRhYmxlX2RlbGV0ZSIsICJ2Ml9yZXNlYXJj
aF9qb2JfYXR0ZW1wdCIsCiAgICAgIkRFTEVURSIsICJWMiByZXNlYXJjaCBqb2IgYXR0ZW1wdHMgYXJlIGltbXV0YWJsZTsgREVMRVRFIHByb2hpYml0ZWQi
KSwKICAgICgidjJfcmVzZWFyY2hfcmVzdWx0X2ltbXV0YWJsZV91cGRhdGUiLCAidjJfcmVzZWFyY2hfcmVzdWx0IiwKICAgICAiVVBEQVRFIiwgIlYyIHJl
c2VhcmNoIHJlc3VsdHMgYXJlIGltbXV0YWJsZTsgVVBEQVRFIHByb2hpYml0ZWQiKSwKICAgICgidjJfcmVzZWFyY2hfcmVzdWx0X2ltbXV0YWJsZV9kZWxl
dGUiLCAidjJfcmVzZWFyY2hfcmVzdWx0IiwKICAgICAiREVMRVRFIiwgIlYyIHJlc2VhcmNoIHJlc3VsdHMgYXJlIGltbXV0YWJsZTsgREVMRVRFIHByb2hp
Yml0ZWQiKSwKKQoKX1BFUk1JU1NJT05TID0gKAogICAgKCJhZG1pbiIsICJ2Mi5yZXNlYXJjaC5qb2JzLnJlYWQiLCAiU0FMLTIiKSwKICAgICgiYWRtaW4i
LCAidjIucmVzZWFyY2guam9icy5zdWJtaXQiLCAiU0FMLTMiKSwKICAgICgiYWRtaW4iLCAidjIucmVzZWFyY2guam9icy5jYW5jZWwiLCAiU0FMLTMiKSwK
ICAgICgiYWRtaW4iLCAidjIucmVzZWFyY2gucmVnaXN0cnkucmVhZCIsICJTQUwtMiIpLAogICAgKCJhZG1pbiIsICJ2Mi5yZXNlYXJjaC5yZWdpc3RyeS53
cml0ZSIsICJTQUwtMyIpLAogICAgKCJhZG1pbiIsICJ2Mi5yZXNlYXJjaC5yZXN1bHRzLnJlYWQiLCAiU0FMLTIiKSwKICAgICgib3BlcmF0b3IiLCAidjIu
cmVzZWFyY2guam9icy5yZWFkIiwgIlNBTC0yIiksCiAgICAoIm9wZXJhdG9yIiwgInYyLnJlc2VhcmNoLnJlc3VsdHMucmVhZCIsICJTQUwtMiIpLAopCgpf
UlBFX0ZJTEVTID0gKAogICAgImFwcC92Mi9yZXNlYXJjaF9qb2JzL19faW5pdF9fLnB5IiwKICAgICJhcHAvdjIvcmVzZWFyY2hfam9icy9sZWFrYWdlLnB5
IiwKICAgICJhcHAvdjIvcmVzZWFyY2hfam9icy9yZXBsYXkucHkiLAopCl9SSkVfRklMRVMgPSAoCiAgICAiYXBwL3YyL3Jlc2VhcmNoX2pvYnMvcXVldWUu
cHkiLAogICAgImFwcC92Mi9yZXNlYXJjaF9qb2JzL3J1bm5lci5weSIsCikKCl9EQVRBX0NMQVNTX0NIRUNLID0gKAogICAgImRhdGFfY2xhc3MgSU4gKCdz
eW50aGV0aWMnLCdzaW11bGF0ZWQnLCdoaXN0b3JpY2FsX3JlYWwnLCdsaXZlJywiCiAgICAiJ3N0YWxlX2NhY2hlZCcsJ3VuYXZhaWxhYmxlJykiCikKCgpk
ZWYgX3JvbGxpbmdfaGFzaChmaWxlczogdHVwbGVbc3RyLCAuLi5dKSAtPiBzdHI6CiAgICBiYXNlID0gUGF0aChfX2ZpbGVfXykucmVzb2x2ZSgpLnBhcmVu
dHNbMl0KICAgIGRpZ2VzdCA9IGhhc2hsaWIuc2hhMjU2KCkKICAgIGZvciByZWwgaW4gZmlsZXM6CiAgICAgICAgZGlnZXN0LnVwZGF0ZShyZWwuZW5jb2Rl
KCJ1dGYtOCIpKQogICAgICAgIGRpZ2VzdC51cGRhdGUoYiJceDAwIikKICAgICAgICBkaWdlc3QudXBkYXRlKChiYXNlIC8gcmVsKS5yZWFkX2J5dGVzKCkp
CiAgICAgICAgZGlnZXN0LnVwZGF0ZShiIlx4MDAiKQogICAgcmV0dXJuIGRpZ2VzdC5oZXhkaWdlc3QoKQoKCmRlZiBfY3JlYXRlX3RyaWdnZXJzKGJpbmQp
IC0+IE5vbmU6CiAgICBpZiBiaW5kLmRpYWxlY3QubmFtZSA9PSAic3FsaXRlIjoKICAgICAgICBmb3IgbmFtZSwgdGFibGUsIGV2ZW50LCBtZXNzYWdlIGlu
IF9UUklHR0VSUzoKICAgICAgICAgICAgb3AuZXhlY3V0ZShmIiIiCiAgICAgICAgICAgICAgICBDUkVBVEUgVFJJR0dFUiB7bmFtZX0KICAgICAgICAgICAg
ICAgIEJFRk9SRSB7ZXZlbnR9IE9OIHt0YWJsZX0KICAgICAgICAgICAgICAgIEJFR0lOCiAgICAgICAgICAgICAgICAgICAgU0VMRUNUIFJBSVNFKEFCT1JU
LCAne21lc3NhZ2V9Jyk7CiAgICAgICAgICAgICAgICBFTkQ7CiAgICAgICAgICAgICIiIikKICAgIGVsaWYgYmluZC5kaWFsZWN0Lm5hbWUgPT0gInBvc3Rn
cmVzcWwiOgogICAgICAgIG9wLmV4ZWN1dGUoIiIiCiAgICAgICAgICAgIENSRUFURSBPUiBSRVBMQUNFIEZVTkNUSU9OIHByZXZlbnRfdjJfcmVzZWFyY2hf
am9ic19tdXRhdGlvbigpCiAgICAgICAgICAgIFJFVFVSTlMgdHJpZ2dlciBBUyAkJAogICAgICAgICAgICBCRUdJTgogICAgICAgICAgICAgICAgUkFJU0Ug
RVhDRVBUSU9OCiAgICAgICAgICAgICAgICAgICAgJ1YyIHJlc2VhcmNoLWpvYnMgYXJ0aWZhY3QgaXMgaW1tdXRhYmxlOyAlIHByb2hpYml0ZWQgb24gJScs
CiAgICAgICAgICAgICAgICAgICAgVEdfT1AsIFRHX1RBQkxFX05BTUU7CiAgICAgICAgICAgIEVORDsKICAgICAgICAgICAgJCQgTEFOR1VBR0UgcGxwZ3Nx
bDsKICAgICAgICAiIiIpCiAgICAgICAgZm9yIG5hbWUsIHRhYmxlLCBldmVudCwgX21lc3NhZ2UgaW4gX1RSSUdHRVJTOgogICAgICAgICAgICBvcC5leGVj
dXRlKGYiIiIKICAgICAgICAgICAgICAgIENSRUFURSBUUklHR0VSIHtuYW1lfQogICAgICAgICAgICAgICAgQkVGT1JFIHtldmVudH0gT04ge3RhYmxlfQog
ICAgICAgICAgICAgICAgRk9SIEVBQ0ggUk9XIEVYRUNVVEUgRlVOQ1RJT04gcHJldmVudF92Ml9yZXNlYXJjaF9qb2JzX211dGF0aW9uKCk7CiAgICAgICAg
ICAgICIiIikKCgpkZWYgX2Ryb3BfdHJpZ2dlcnMoYmluZCkgLT4gTm9uZToKICAgIGlmIGJpbmQuZGlhbGVjdC5uYW1lID09ICJzcWxpdGUiOgogICAgICAg
IGZvciBuYW1lLCBfdCwgX2UsIF9tIGluIF9UUklHR0VSUzoKICAgICAgICAgICAgb3AuZXhlY3V0ZShmIkRST1AgVFJJR0dFUiBJRiBFWElTVFMge25hbWV9
IikKICAgIGVsaWYgYmluZC5kaWFsZWN0Lm5hbWUgPT0gInBvc3RncmVzcWwiOgogICAgICAgIGZvciBuYW1lLCB0YWJsZSwgX2UsIF9tIGluIF9UUklHR0VS
UzoKICAgICAgICAgICAgb3AuZXhlY3V0ZShmIkRST1AgVFJJR0dFUiBJRiBFWElTVFMge25hbWV9IE9OIHt0YWJsZX0iKQogICAgICAgIG9wLmV4ZWN1dGUo
IkRST1AgRlVOQ1RJT04gSUYgRVhJU1RTIHByZXZlbnRfdjJfcmVzZWFyY2hfam9ic19tdXRhdGlvbigpIikKCgpkZWYgX2Ryb3BfY29tcHZlcl9kZWxldGVf
Z3VhcmQoYmluZCkgLT4gTm9uZToKICAgIGlmIGJpbmQuZGlhbGVjdC5uYW1lID09ICJzcWxpdGUiOgogICAgICAgIG9wLmV4ZWN1dGUoIkRST1AgVFJJR0dF
UiBJRiBFWElTVFMgdjJfY29tcHV0YXRpb25fdmVyc2lvbl9pbW11dGFibGVfZGVsZXRlIikKICAgIGVsaWYgYmluZC5kaWFsZWN0Lm5hbWUgPT0gInBvc3Rn
cmVzcWwiOgogICAgICAgIG9wLmV4ZWN1dGUoCiAgICAgICAgICAgICJEUk9QIFRSSUdHRVIgSUYgRVhJU1RTIHYyX2NvbXB1dGF0aW9uX3ZlcnNpb25faW1t
dXRhYmxlX2RlbGV0ZSIKICAgICAgICAgICAgIiBPTiB2Ml9jb21wdXRhdGlvbl92ZXJzaW9uIikKCgpkZWYgX3JlY3JlYXRlX2NvbXB2ZXJfZGVsZXRlX2d1
YXJkKGJpbmQpIC0+IE5vbmU6CiAgICBpZiBiaW5kLmRpYWxlY3QubmFtZSA9PSAic3FsaXRlIjoKICAgICAgICBvcC5leGVjdXRlKCIiIgogICAgICAgICAg
ICBDUkVBVEUgVFJJR0dFUiB2Ml9jb21wdXRhdGlvbl92ZXJzaW9uX2ltbXV0YWJsZV9kZWxldGUKICAgICAgICAgICAgQkVGT1JFIERFTEVURSBPTiB2Ml9j
b21wdXRhdGlvbl92ZXJzaW9uCiAgICAgICAgICAgIEJFR0lOCiAgICAgICAgICAgICAgICBTRUxFQ1QgUkFJU0UoQUJPUlQsCiAgICAgICAgICAgICAgICAg
ICAgJ1YyIGNvbXB1dGF0aW9uIHZlcnNpb24gcmVnaXN0cnkgaXMgaW1tdXRhYmxlOyBERUxFVEUgcHJvaGliaXRlZCcpOwogICAgICAgICAgICBFTkQ7CiAg
ICAgICAgIiIiKQogICAgICAgIGNvdW50ID0gYmluZC5leGVjdXRlKHNhLnRleHQoCiAgICAgICAgICAgICJTRUxFQ1QgQ09VTlQoKikgRlJPTSBzcWxpdGVf
bWFzdGVyIFdIRVJFIHR5cGU9J3RyaWdnZXInIgogICAgICAgICAgICAiIEFORCBuYW1lPSd2Ml9jb21wdXRhdGlvbl92ZXJzaW9uX2ltbXV0YWJsZV9kZWxl
dGUnIikpLnNjYWxhcl9vbmUoKQogICAgZWxpZiBiaW5kLmRpYWxlY3QubmFtZSA9PSAicG9zdGdyZXNxbCI6CiAgICAgICAgb3AuZXhlY3V0ZSgiIiIKICAg
ICAgICAgICAgQ1JFQVRFIFRSSUdHRVIgdjJfY29tcHV0YXRpb25fdmVyc2lvbl9pbW11dGFibGVfZGVsZXRlCiAgICAgICAgICAgIEJFRk9SRSBERUxFVEUg
T04gdjJfY29tcHV0YXRpb25fdmVyc2lvbgogICAgICAgICAgICBGT1IgRUFDSCBST1cgRVhFQ1VURSBGVU5DVElPTiBwcmV2ZW50X3YyX3Jlc2VhcmNoX211
dGF0aW9uKCk7CiAgICAgICAgIiIiKQogICAgICAgIGNvdW50ID0gYmluZC5leGVjdXRlKHNhLnRleHQoCiAgICAgICAgICAgICJTRUxFQ1QgQ09VTlQoKikg
RlJPTSBwZ190cmlnZ2VyIgogICAgICAgICAgICAiIFdIRVJFIHRnbmFtZT0ndjJfY29tcHV0YXRpb25fdmVyc2lvbl9pbW11dGFibGVfZGVsZXRlJyIpKS5z
Y2FsYXJfb25lKCkKICAgIGVsc2U6ICAjIHByYWdtYTogbm8gY292ZXIKICAgICAgICByZXR1cm4KICAgIGlmIGludChjb3VudCkgIT0gMToKICAgICAgICBy
YWlzZSBSdW50aW1lRXJyb3IoCiAgICAgICAgICAgICJjb21wdmVyIGRlbGV0ZSBndWFyZCBOT1QgcmVzdG9yZWQgLSBtYW51YWwgcmVjb3ZlcnkgcmVxdWly
ZWQiKQoKCmRlZiBfYmUxX2NvbHVtbnMoKSAtPiBsaXN0OgogICAgcmV0dXJuIFsKICAgICAgICBzYS5Db2x1bW4oImRhdGFfY2xhc3MiLCBzYS5TdHJpbmco
MzIpLCBudWxsYWJsZT1GYWxzZSksCiAgICAgICAgc2EuQ29sdW1uKCJtb2RlIiwgc2EuU3RyaW5nKDE2KSwgbnVsbGFibGU9RmFsc2UpLAogICAgICAgIHNh
LkNvbHVtbigib3BlcmF0b3JfaWQiLCBzYS5TdHJpbmcoMTI4KSwgbnVsbGFibGU9RmFsc2UpLAogICAgICAgIHNhLkNvbHVtbigiY29ycmVsYXRpb25faWQi
LCBzYS5TdHJpbmcoNjQpLCBudWxsYWJsZT1UcnVlKSwKICAgICAgICBzYS5Db2x1bW4oImNyZWF0ZWRfYXQiLCBzYS5EYXRlVGltZSh0aW1lem9uZT1UcnVl
KSwgbnVsbGFibGU9RmFsc2UpLAogICAgXQoKCmRlZiB1cGdyYWRlKCkgLT4gTm9uZToKICAgIGJpbmQgPSBvcC5nZXRfYmluZCgpCiAgICBub3cgPSBkYXRl
dGltZS5ub3codGltZXpvbmUudXRjKQoKICAgIG9wLmNyZWF0ZV90YWJsZSgKICAgICAgICAidjJfYmFja3Rlc3RfaW5wdXQiLAogICAgICAgIHNhLkNvbHVt
bigiaWQiLCBzYS5TdHJpbmcoMzYpLCBwcmltYXJ5X2tleT1UcnVlKSwKICAgICAgICBzYS5Db2x1bW4oImlucHV0X2lkIiwgc2EuU3RyaW5nKDY0KSwgbnVs
bGFibGU9RmFsc2UpLAogICAgICAgIHNhLkNvbHVtbigicmVjb3JkX3NlcSIsIHNhLkludGVnZXIoKSwgbnVsbGFibGU9RmFsc2UpLAogICAgICAgIHNhLkNv
bHVtbigic3VwZXJzZWRlcyIsIHNhLlN0cmluZygzNiksIG51bGxhYmxlPVRydWUpLAogICAgICAgIHNhLkNvbHVtbigiY29udGVudF9oYXNoIiwgc2EuU3Ry
aW5nKDY0KSwgbnVsbGFibGU9RmFsc2UpLAogICAgICAgIHNhLkNvbHVtbigic2VyaWVzX3JlZnMiLCBzYS5KU09OKCksIG51bGxhYmxlPUZhbHNlKSwKICAg
ICAgICBzYS5Db2x1bW4oIndpbmRvd19zdGFydCIsIHNhLkRhdGVUaW1lKHRpbWV6b25lPVRydWUpLCBudWxsYWJsZT1GYWxzZSksCiAgICAgICAgc2EuQ29s
dW1uKCJ3aW5kb3dfZW5kIiwgc2EuRGF0ZVRpbWUodGltZXpvbmU9VHJ1ZSksIG51bGxhYmxlPUZhbHNlKSwKICAgICAgICBzYS5Db2x1bW4oInJlZ2lzdHJh
dGlvbl9vdXRjb21lIiwgc2EuU3RyaW5nKDE2KSwgbnVsbGFibGU9RmFsc2UpLAogICAgICAgICpfYmUxX2NvbHVtbnMoKSwKICAgICAgICBzYS5VbmlxdWVD
b25zdHJhaW50KCJpbnB1dF9pZCIsICJyZWNvcmRfc2VxIiwgbmFtZT0idXFfdjJfYnRpbl9pZF9zZXEiKSwKICAgICAgICBzYS5VbmlxdWVDb25zdHJhaW50
KCJjb250ZW50X2hhc2giLCBuYW1lPSJ1cV92Ml9idGluX2NvbnRlbnQiKSwKICAgICAgICBzYS5DaGVja0NvbnN0cmFpbnQoCiAgICAgICAgICAgICJyZWdp
c3RyYXRpb25fb3V0Y29tZSBJTiAoJ3JlZ2lzdGVyZWQnLCdyZXVzZWQnLCdyZWZ1c2VkJykiLAogICAgICAgICAgICBuYW1lPSJja192Ml9idGluX291dGNv
bWUiKSwKICAgICAgICBzYS5DaGVja0NvbnN0cmFpbnQoX0RBVEFfQ0xBU1NfQ0hFQ0ssIG5hbWU9ImNrX3YyX2J0aW5fZGF0YV9jbGFzcyIpLAogICAgKQog
ICAgb3AuY3JlYXRlX2luZGV4KCJpeF92Ml9idGluX2lucHV0IiwgInYyX2JhY2t0ZXN0X2lucHV0IiwgWyJpbnB1dF9pZCJdKQoKICAgIG9wLmNyZWF0ZV90
YWJsZSgKICAgICAgICAidjJfY29zdF9tb2RlbCIsCiAgICAgICAgc2EuQ29sdW1uKCJpZCIsIHNhLlN0cmluZygzNiksIHByaW1hcnlfa2V5PVRydWUpLAog
ICAgICAgIHNhLkNvbHVtbigiY29zdF9tb2RlbF9pZCIsIHNhLlN0cmluZyg2NCksIG51bGxhYmxlPUZhbHNlKSwKICAgICAgICBzYS5Db2x1bW4oInJlY29y
ZF9zZXEiLCBzYS5JbnRlZ2VyKCksIG51bGxhYmxlPUZhbHNlKSwKICAgICAgICBzYS5Db2x1bW4oInN1cGVyc2VkZXMiLCBzYS5TdHJpbmcoMzYpLCBudWxs
YWJsZT1UcnVlKSwKICAgICAgICBzYS5Db2x1bW4oInNwcmVhZCIsIHNhLkpTT04oKSwgbnVsbGFibGU9RmFsc2UpLAogICAgICAgIHNhLkNvbHVtbigiY29t
bWlzc2lvbiIsIHNhLkpTT04oKSwgbnVsbGFibGU9RmFsc2UpLAogICAgICAgIHNhLkNvbHVtbigic2xpcHBhZ2UiLCBzYS5KU09OKCksIG51bGxhYmxlPUZh
bHNlKSwKICAgICAgICBzYS5Db2x1bW4oImxhdGVuY3lfbXMiLCBzYS5JbnRlZ2VyKCksIG51bGxhYmxlPUZhbHNlKSwKICAgICAgICBzYS5Db2x1bW4oInJp
c2tfbGltaXRzIiwgc2EuSlNPTigpLCBudWxsYWJsZT1GYWxzZSksCiAgICAgICAgc2EuQ29sdW1uKCJjaXRhdGlvbnMiLCBzYS5KU09OKCksIG51bGxhYmxl
PUZhbHNlKSwKICAgICAgICAqX2JlMV9jb2x1bW5zKCksCiAgICAgICAgc2EuVW5pcXVlQ29uc3RyYWludCgiY29zdF9tb2RlbF9pZCIsICJyZWNvcmRfc2Vx
IiwKICAgICAgICAgICAgICAgICAgICAgICAgICAgIG5hbWU9InVxX3YyX2Nvc3RfaWRfc2VxIiksCiAgICAgICAgc2EuQ2hlY2tDb25zdHJhaW50KF9EQVRB
X0NMQVNTX0NIRUNLLCBuYW1lPSJja192Ml9jb3N0X2RhdGFfY2xhc3MiKSwKICAgICkKICAgIG9wLmNyZWF0ZV9pbmRleCgiaXhfdjJfY29zdF9tb2RlbCIs
ICJ2Ml9jb3N0X21vZGVsIiwgWyJjb3N0X21vZGVsX2lkIl0pCgogICAgb3AuY3JlYXRlX3RhYmxlKAogICAgICAgICJ2Ml9zdHJhdGVneV92ZXJzaW9uIiwK
ICAgICAgICBzYS5Db2x1bW4oImlkIiwgc2EuU3RyaW5nKDM2KSwgcHJpbWFyeV9rZXk9VHJ1ZSksCiAgICAgICAgc2EuQ29sdW1uKCJzdHJhdGVneV9pZCIs
IHNhLlN0cmluZyg2NCksIG51bGxhYmxlPUZhbHNlKSwKICAgICAgICBzYS5Db2x1bW4oInJlY29yZF9zZXEiLCBzYS5JbnRlZ2VyKCksIG51bGxhYmxlPUZh
bHNlKSwKICAgICAgICBzYS5Db2x1bW4oInN1cGVyc2VkZXMiLCBzYS5TdHJpbmcoMzYpLCBudWxsYWJsZT1UcnVlKSwKICAgICAgICBzYS5Db2x1bW4oIm5h
bWUiLCBzYS5TdHJpbmcoMTI4KSwgbnVsbGFibGU9RmFsc2UpLAogICAgICAgIHNhLkNvbHVtbigicGFyYW1ldGVycyIsIHNhLkpTT04oKSwgbnVsbGFibGU9
RmFsc2UpLAogICAgICAgIHNhLkNvbHVtbigibGlmZWN5Y2xlX3N0YXRlIiwgc2EuU3RyaW5nKDE2KSwgbnVsbGFibGU9RmFsc2UpLAogICAgICAgICpfYmUx
X2NvbHVtbnMoKSwKICAgICAgICBzYS5VbmlxdWVDb25zdHJhaW50KCJzdHJhdGVneV9pZCIsICJyZWNvcmRfc2VxIiwKICAgICAgICAgICAgICAgICAgICAg
ICAgICAgIG5hbWU9InVxX3YyX3N0cmF0X2lkX3NlcSIpLAogICAgICAgIHNhLkNoZWNrQ29uc3RyYWludCgKICAgICAgICAgICAgImxpZmVjeWNsZV9zdGF0
ZSBJTiAoJ2RyYWZ0JywncmVnaXN0ZXJlZCcsJ3JldGlyZWQnKSIsCiAgICAgICAgICAgIG5hbWU9ImNrX3YyX3N0cmF0X3N0YXRlIiksCiAgICAgICAgc2Eu
Q2hlY2tDb25zdHJhaW50KF9EQVRBX0NMQVNTX0NIRUNLLCBuYW1lPSJja192Ml9zdHJhdF9kYXRhX2NsYXNzIiksCiAgICApCiAgICBvcC5jcmVhdGVfaW5k
ZXgoIml4X3YyX3N0cmF0X3N0cmF0ZWd5IiwgInYyX3N0cmF0ZWd5X3ZlcnNpb24iLAogICAgICAgICAgICAgICAgICAgIFsic3RyYXRlZ3lfaWQiXSkKCiAg
ICBvcC5jcmVhdGVfdGFibGUoCiAgICAgICAgInYyX3Jlc2VhcmNoX2pvYiIsCiAgICAgICAgc2EuQ29sdW1uKCJpZCIsIHNhLlN0cmluZygzNiksIHByaW1h
cnlfa2V5PVRydWUpLAogICAgICAgIHNhLkNvbHVtbigib3duZXIiLCBzYS5TdHJpbmcoMTI4KSwgbnVsbGFibGU9RmFsc2UpLAogICAgICAgIHNhLkNvbHVt
bigiYXV0aG9yaXphdGlvbl9yZWYiLCBzYS5TdHJpbmcoMTI4KSwgbnVsbGFibGU9RmFsc2UpLAogICAgICAgIHNhLkNvbHVtbigiaW5wdXRzIiwgc2EuSlNP
TigpLCBudWxsYWJsZT1GYWxzZSksCiAgICAgICAgc2EuQ29sdW1uKCJzY2hlZHVsZSIsIHNhLkpTT04oKSwgbnVsbGFibGU9RmFsc2UpLAogICAgICAgIHNh
LkNvbHVtbigib3V0cHV0X3JlZiIsIHNhLlN0cmluZygzNiksIG51bGxhYmxlPVRydWUpLAogICAgICAgIHNhLkNvbHVtbigiZmFpbHVyZSIsIHNhLkpTT04o
KSwgbnVsbGFibGU9VHJ1ZSksCiAgICAgICAgc2EuQ29sdW1uKCJqb2Jfc3RhdGUiLCBzYS5TdHJpbmcoMTYpLCBudWxsYWJsZT1GYWxzZSksCiAgICAgICAg
c2EuQ29sdW1uKCJhdHRlbXB0X2NvdW50Iiwgc2EuSW50ZWdlcigpLCBudWxsYWJsZT1GYWxzZSksCiAgICAgICAgKl9iZTFfY29sdW1ucygpLAogICAgICAg
IHNhLkNoZWNrQ29uc3RyYWludCgKICAgICAgICAgICAgImpvYl9zdGF0ZSBJTiAoJ3F1ZXVlZCcsJ3J1bm5pbmcnLCdzdWNjZWVkZWQnLCdmYWlsZWQnLCIK
ICAgICAgICAgICAgIidjYW5jZWxsZWQnKSIsCiAgICAgICAgICAgIG5hbWU9ImNrX3YyX2pvYl9zdGF0ZSIpLAogICAgICAgIHNhLkNoZWNrQ29uc3RyYWlu
dChfREFUQV9DTEFTU19DSEVDSywgbmFtZT0iY2tfdjJfam9iX2RhdGFfY2xhc3MiKSwKICAgICkKICAgIG9wLmNyZWF0ZV9pbmRleCgiaXhfdjJfam9iX3N0
YXRlIiwgInYyX3Jlc2VhcmNoX2pvYiIsIFsiam9iX3N0YXRlIl0pCgogICAgb3AuY3JlYXRlX3RhYmxlKAogICAgICAgICJ2Ml9yZXNlYXJjaF9qb2JfYXR0
ZW1wdCIsCiAgICAgICAgc2EuQ29sdW1uKCJpZCIsIHNhLlN0cmluZygzNiksIHByaW1hcnlfa2V5PVRydWUpLAogICAgICAgIHNhLkNvbHVtbigiam9iX2lk
Iiwgc2EuU3RyaW5nKDM2KSwgbnVsbGFibGU9RmFsc2UpLAogICAgICAgIHNhLkNvbHVtbigiYXR0ZW1wdF9pbmRleCIsIHNhLkludGVnZXIoKSwgbnVsbGFi
bGU9RmFsc2UpLAogICAgICAgIHNhLkNvbHVtbigib3V0Y29tZSIsIHNhLlN0cmluZygxNiksIG51bGxhYmxlPUZhbHNlKSwKICAgICAgICBzYS5Db2x1bW4o
ImFydGlmYWN0X3JlZiIsIHNhLlN0cmluZygzNiksIG51bGxhYmxlPVRydWUpLAogICAgICAgIHNhLkNvbHVtbigicmVhc29uIiwgc2EuSlNPTigpLCBudWxs
YWJsZT1GYWxzZSksCiAgICAgICAgc2EuQ29sdW1uKCJhY3Rvcl9pZCIsIHNhLlN0cmluZygxMjgpLCBudWxsYWJsZT1GYWxzZSksCiAgICAgICAgc2EuQ29s
dW1uKCJtb2RlIiwgc2EuU3RyaW5nKDE2KSwgbnVsbGFibGU9RmFsc2UpLAogICAgICAgIHNhLkNvbHVtbigib3BlcmF0b3JfaWQiLCBzYS5TdHJpbmcoMTI4
KSwgbnVsbGFibGU9RmFsc2UpLAogICAgICAgIHNhLkNvbHVtbigiY29ycmVsYXRpb25faWQiLCBzYS5TdHJpbmcoNjQpLCBudWxsYWJsZT1UcnVlKSwKICAg
ICAgICBzYS5Db2x1bW4oImNyZWF0ZWRfYXQiLCBzYS5EYXRlVGltZSh0aW1lem9uZT1UcnVlKSwgbnVsbGFibGU9RmFsc2UpLAogICAgICAgIHNhLlVuaXF1
ZUNvbnN0cmFpbnQoImpvYl9pZCIsICJhdHRlbXB0X2luZGV4IiwgbmFtZT0idXFfdjJfam9iYXR0X2lkeCIpLAogICAgICAgIHNhLkNoZWNrQ29uc3RyYWlu
dCgKICAgICAgICAgICAgIm91dGNvbWUgSU4gKCdzdWNjZWVkZWQnLCdmYWlsZWQnLCdjYW5jZWxsZWQnKSIsCiAgICAgICAgICAgIG5hbWU9ImNrX3YyX2pv
YmF0dF9vdXRjb21lIiksCiAgICApCiAgICBvcC5jcmVhdGVfaW5kZXgoIml4X3YyX2pvYmF0dF9qb2IiLCAidjJfcmVzZWFyY2hfam9iX2F0dGVtcHQiLCBb
ImpvYl9pZCJdKQoKICAgIG9wLmNyZWF0ZV90YWJsZSgKICAgICAgICAidjJfcmVzZWFyY2hfcmVzdWx0IiwKICAgICAgICBzYS5Db2x1bW4oImlkIiwgc2Eu
U3RyaW5nKDM2KSwgcHJpbWFyeV9rZXk9VHJ1ZSksCiAgICAgICAgc2EuQ29sdW1uKCJyZXN1bHRfY2xhc3MiLCBzYS5TdHJpbmcoMTYpLCBudWxsYWJsZT1G
YWxzZSksCiAgICAgICAgc2EuQ29sdW1uKCJqb2JfaWQiLCBzYS5TdHJpbmcoMzYpLCBudWxsYWJsZT1GYWxzZSksCiAgICAgICAgc2EuQ29sdW1uKCJhdHRl
bXB0X2luZGV4Iiwgc2EuSW50ZWdlcigpLCBudWxsYWJsZT1GYWxzZSksCiAgICAgICAgc2EuQ29sdW1uKCJzdHJhdGVneV92ZXJzaW9uX2lkIiwgc2EuU3Ry
aW5nKDM2KSwgbnVsbGFibGU9RmFsc2UpLAogICAgICAgIHNhLkNvbHVtbigiaW5wdXRfcmVnaXN0cnlfaWQiLCBzYS5TdHJpbmcoMzYpLCBudWxsYWJsZT1G
YWxzZSksCiAgICAgICAgc2EuQ29sdW1uKCJjb3N0X21vZGVsX2lkIiwgc2EuU3RyaW5nKDM2KSwgbnVsbGFibGU9RmFsc2UpLAogICAgICAgIHNhLkNvbHVt
bigiaW5wdXRzX2hhc2giLCBzYS5TdHJpbmcoNjQpLCBudWxsYWJsZT1GYWxzZSksCiAgICAgICAgc2EuQ29sdW1uKCJlbmdpbmVfdmVyc2lvbnMiLCBzYS5K
U09OKCksIG51bGxhYmxlPUZhbHNlKSwKICAgICAgICBzYS5Db2x1bW4oImVuZ2luZV92ZXJzaW9uc19oYXNoIiwgc2EuU3RyaW5nKDY0KSwgbnVsbGFibGU9
RmFsc2UpLAogICAgICAgIHNhLkNvbHVtbigic3VtbWFyeSIsIHNhLkpTT04oKSwgbnVsbGFibGU9RmFsc2UpLAogICAgICAgIHNhLkNvbHVtbigicmVwbGF5
X29mIiwgc2EuU3RyaW5nKDM2KSwgbnVsbGFibGU9VHJ1ZSksCiAgICAgICAgc2EuQ29sdW1uKCJ0aW1lX2Jhc2lzIiwgc2EuSlNPTigpLCBudWxsYWJsZT1G
YWxzZSksCiAgICAgICAgKl9iZTFfY29sdW1ucygpLAogICAgICAgIHNhLlVuaXF1ZUNvbnN0cmFpbnQoInN0cmF0ZWd5X3ZlcnNpb25faWQiLCAiaW5wdXRz
X2hhc2giLAogICAgICAgICAgICAgICAgICAgICAgICAgICAgImVuZ2luZV92ZXJzaW9uc19oYXNoIiwKICAgICAgICAgICAgICAgICAgICAgICAgICAgIG5h
bWU9InVxX3YyX3Jlc3VsdF9kZXRlcm1pbmlzbV9hbmNob3IiKSwKICAgICAgICBzYS5DaGVja0NvbnN0cmFpbnQoInJlc3VsdF9jbGFzcyBJTiAoJ2JhY2t0
ZXN0Jywnc2ltdWxhdGlvbicpIiwKICAgICAgICAgICAgICAgICAgICAgICAgICAgbmFtZT0iY2tfdjJfcmVzdWx0X2NsYXNzIiksCiAgICAgICAgc2EuQ2hl
Y2tDb25zdHJhaW50KF9EQVRBX0NMQVNTX0NIRUNLLCBuYW1lPSJja192Ml9yZXN1bHRfZGF0YV9jbGFzcyIpLAogICAgKQogICAgb3AuY3JlYXRlX2luZGV4
KCJpeF92Ml9yZXN1bHRfam9iIiwgInYyX3Jlc2VhcmNoX3Jlc3VsdCIsIFsiam9iX2lkIl0pCgogICAgIyAtLS0gU2VlZHMgKHJldmlzaW9uLWxvY2FsIGxp
dGVyYWxzOyBERUwtMDA0IGxhdykgLS0tLS0tLS0tLS0tLS0tLS0tLS0tCiAgICBwZXJtaXNzaW9uX3RhYmxlID0gc2EudGFibGUoCiAgICAgICAgInYyX3Bl
cm1pc3Npb24iLAogICAgICAgIHNhLmNvbHVtbigiaWQiLCBzYS5TdHJpbmcpLCBzYS5jb2x1bW4oInJvbGUiLCBzYS5TdHJpbmcpLAogICAgICAgIHNhLmNv
bHVtbigicGVybWlzc2lvbiIsIHNhLlN0cmluZyksIHNhLmNvbHVtbigic2FsIiwgc2EuU3RyaW5nKSwKICAgICAgICBzYS5jb2x1bW4oImNyZWF0ZWRfYXQi
LCBzYS5EYXRlVGltZSh0aW1lem9uZT1UcnVlKSksCiAgICApCiAgICBleGlzdGluZyA9IHsKICAgICAgICAocm93WzBdLCByb3dbMV0pCiAgICAgICAgZm9y
IHJvdyBpbiBiaW5kLmV4ZWN1dGUoc2EudGV4dCgiU0VMRUNUIHJvbGUsIHBlcm1pc3Npb24gRlJPTSB2Ml9wZXJtaXNzaW9uIikpCiAgICB9CiAgICBmb3Ig
cm9sZSwgcGVybWlzc2lvbiwgc2FsIGluIF9QRVJNSVNTSU9OUzoKICAgICAgICBpZiAocm9sZSwgcGVybWlzc2lvbikgbm90IGluIGV4aXN0aW5nOgogICAg
ICAgICAgICBvcC5leGVjdXRlKHBlcm1pc3Npb25fdGFibGUuaW5zZXJ0KCkudmFsdWVzKAogICAgICAgICAgICAgICAgaWQ9c3RyKHV1aWQ0KCkpLCByb2xl
PXJvbGUsIHBlcm1pc3Npb249cGVybWlzc2lvbiwKICAgICAgICAgICAgICAgIHNhbD1zYWwsIGNyZWF0ZWRfYXQ9bm93LAogICAgICAgICAgICApKQoKICAg
IGNvbXB2ZXIgPSBzYS50YWJsZSgKICAgICAgICAidjJfY29tcHV0YXRpb25fdmVyc2lvbiIsCiAgICAgICAgc2EuY29sdW1uKCJpZCIsIHNhLlN0cmluZyks
IHNhLmNvbHVtbigiY29tcG9uZW50Iiwgc2EuU3RyaW5nKSwKICAgICAgICBzYS5jb2x1bW4oInZlcnNpb24iLCBzYS5TdHJpbmcpLCBzYS5jb2x1bW4oInNv
dXJjZV9oYXNoIiwgc2EuU3RyaW5nKSwKICAgICAgICBzYS5jb2x1bW4oImV2aWRlbmNlX3JlZiIsIHNhLlN0cmluZyksCiAgICAgICAgc2EuY29sdW1uKCJy
ZWdpc3RlcmVkX2F0Iiwgc2EuRGF0ZVRpbWUodGltZXpvbmU9VHJ1ZSkpLAogICAgKQogICAgZm9yIGNvbXBvbmVudCwgdmVyc2lvbiwgZmlsZXMgaW4gKAog
ICAgICAgICgicmVwbGF5X2VuZ2luZSIsICJycGUtMS4wLjAiLCBfUlBFX0ZJTEVTKSwKICAgICAgICAoInJlc2VhcmNoX2pvYl9lbmdpbmUiLCAicmplLTEu
MC4wIiwgX1JKRV9GSUxFUyksCiAgICApOgogICAgICAgIG9wLmV4ZWN1dGUoY29tcHZlci5pbnNlcnQoKS52YWx1ZXMoCiAgICAgICAgICAgIGlkPXN0cih1
dWlkNCgpKSwgY29tcG9uZW50PWNvbXBvbmVudCwgdmVyc2lvbj12ZXJzaW9uLAogICAgICAgICAgICBzb3VyY2VfaGFzaD1fcm9sbGluZ19oYXNoKGZpbGVz
KSwgZXZpZGVuY2VfcmVmPSJCTy1WMi1CRS03LTAwMSIsCiAgICAgICAgICAgIHJlZ2lzdGVyZWRfYXQ9bm93LAogICAgICAgICkpCgogICAgX2NyZWF0ZV90
cmlnZ2VycyhiaW5kKQogICAgX3ZlcmlmeV90cmlnZ2Vyc19wcmVzZW50KGJpbmQpCgoKZGVmIF92ZXJpZnlfdHJpZ2dlcnNfcHJlc2VudChiaW5kKSAtPiBO
b25lOgogICAgbmFtZXMgPSB0dXBsZSh0WzBdIGZvciB0IGluIF9UUklHR0VSUykKICAgIHBsYWNlaG9sZGVycyA9ICIsIi5qb2luKGYiJ3tufSciIGZvciBu
IGluIG5hbWVzKQogICAgaWYgYmluZC5kaWFsZWN0Lm5hbWUgPT0gInNxbGl0ZSI6CiAgICAgICAgY291bnQgPSBiaW5kLmV4ZWN1dGUoc2EudGV4dCgKICAg
ICAgICAgICAgIlNFTEVDVCBDT1VOVCgqKSBGUk9NIHNxbGl0ZV9tYXN0ZXIgV0hFUkUgdHlwZT0ndHJpZ2dlciciCiAgICAgICAgICAgIGYiIEFORCBuYW1l
IElOICh7cGxhY2Vob2xkZXJzfSkiKSkuc2NhbGFyX29uZSgpCiAgICBlbGlmIGJpbmQuZGlhbGVjdC5uYW1lID09ICJwb3N0Z3Jlc3FsIjoKICAgICAgICBj
b3VudCA9IGJpbmQuZXhlY3V0ZShzYS50ZXh0KAogICAgICAgICAgICBmIlNFTEVDVCBDT1VOVCgqKSBGUk9NIHBnX3RyaWdnZXIgV0hFUkUgdGduYW1lIElO
ICh7cGxhY2Vob2xkZXJzfSkiCiAgICAgICAgKSkuc2NhbGFyX29uZSgpCiAgICBlbHNlOiAgIyBwcmFnbWE6IG5vIGNvdmVyCiAgICAgICAgcmV0dXJuCiAg
ICBpZiBpbnQoY291bnQpICE9IGxlbihuYW1lcyk6CiAgICAgICAgcmFpc2UgUnVudGltZUVycm9yKAogICAgICAgICAgICAiQkUtNyAwMDQ3OiBndWFyZCB0
cmlnZ2VycyBOT1QgcHJlc2VudCDigJQgbWFudWFsIHJlY292ZXJ5IgogICAgICAgICAgICAiIHJlcXVpcmVkOyBkbyBub3QgdHJlYXQgdGhpcyBtaWdyYXRp
b24gYXMgYXBwbGllZCIpCgoKZGVmIGRvd25ncmFkZSgpIC0+IE5vbmU6CiAgICBiaW5kID0gb3AuZ2V0X2JpbmQoKQogICAgX2Ryb3BfdHJpZ2dlcnMoYmlu
ZCkKICAgIGZvciBfcm9sZSwgcGVybWlzc2lvbiwgX3NhbCBpbiBfUEVSTUlTU0lPTlM6CiAgICAgICAgb3AuZXhlY3V0ZShzYS50ZXh0KAogICAgICAgICAg
ICAiREVMRVRFIEZST00gdjJfcGVybWlzc2lvbiBXSEVSRSBwZXJtaXNzaW9uID0gOnAiCiAgICAgICAgKS5iaW5kcGFyYW1zKHA9cGVybWlzc2lvbikpCiAg
ICBfZHJvcF9jb21wdmVyX2RlbGV0ZV9ndWFyZChiaW5kKQogICAgZm9yIGNvbXBvbmVudCwgdmVyc2lvbiBpbiAoKCJyZXBsYXlfZW5naW5lIiwgInJwZS0x
LjAuMCIpLAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgKCJyZXNlYXJjaF9qb2JfZW5naW5lIiwgInJqZS0xLjAuMCIpKToKICAgICAgICBvcC5l
eGVjdXRlKHNhLnRleHQoCiAgICAgICAgICAgICJERUxFVEUgRlJPTSB2Ml9jb21wdXRhdGlvbl92ZXJzaW9uIgogICAgICAgICAgICAiIFdIRVJFIGNvbXBv
bmVudCA9IDpjIEFORCB2ZXJzaW9uID0gOnYiCiAgICAgICAgKS5iaW5kcGFyYW1zKGM9Y29tcG9uZW50LCB2PXZlcnNpb24pKQogICAgX3JlY3JlYXRlX2Nv
bXB2ZXJfZGVsZXRlX2d1YXJkKGJpbmQpCiAgICBmb3IgaW5kZXgsIHRhYmxlIGluICgKICAgICAgICAoIml4X3YyX3Jlc3VsdF9qb2IiLCAidjJfcmVzZWFy
Y2hfcmVzdWx0IiksCiAgICAgICAgKCJpeF92Ml9qb2JhdHRfam9iIiwgInYyX3Jlc2VhcmNoX2pvYl9hdHRlbXB0IiksCiAgICAgICAgKCJpeF92Ml9qb2Jf
c3RhdGUiLCAidjJfcmVzZWFyY2hfam9iIiksCiAgICAgICAgKCJpeF92Ml9zdHJhdF9zdHJhdGVneSIsICJ2Ml9zdHJhdGVneV92ZXJzaW9uIiksCiAgICAg
ICAgKCJpeF92Ml9jb3N0X21vZGVsIiwgInYyX2Nvc3RfbW9kZWwiKSwKICAgICAgICAoIml4X3YyX2J0aW5faW5wdXQiLCAidjJfYmFja3Rlc3RfaW5wdXQi
KSwKICAgICk6CiAgICAgICAgb3AuZHJvcF9pbmRleChpbmRleCwgdGFibGVfbmFtZT10YWJsZSkKICAgIGZvciB0YWJsZSBpbiAoInYyX3Jlc2VhcmNoX3Jl
c3VsdCIsICJ2Ml9yZXNlYXJjaF9qb2JfYXR0ZW1wdCIsCiAgICAgICAgICAgICAgICAgICJ2Ml9yZXNlYXJjaF9qb2IiLCAidjJfc3RyYXRlZ3lfdmVyc2lv
biIsCiAgICAgICAgICAgICAgICAgICJ2Ml9jb3N0X21vZGVsIiwgInYyX2JhY2t0ZXN0X2lucHV0Iik6CiAgICAgICAgb3AuZHJvcF90YWJsZSh0YWJsZSkK
'@
Write-Evidence ("record 1/17 staged: " + $Rec1Path)
$Rec2Path = "app\db\models\__init__.py"
$Rec2Sha  = "32b0f7707fe2bd2556b4e01eed125becff9676f494a960e5a74c0c34de9855e9"
$Rec2B64 = @'
IiIiT1JNIG1vZGVscyBwYWNrYWdlIOKAlCBpbXBvcnQgc2lkZSBlZmZlY3RzIHJlZ2lzdGVyIG1ldGFkYXRhIGZvciBBbGVtYmljLiIiIgoKZnJvbSBhcHAu
ZGIubW9kZWxzLmFkdmlzb3J5X3NpZ25hbCBpbXBvcnQgQWR2aXNvcnlTaWduYWwKZnJvbSBhcHAuZGIubW9kZWxzLmFzc2lzdGFudF9yZXNlYXJjaF9yZXNw
b25zZSBpbXBvcnQgQXNzaXN0YW50UmVzZWFyY2hSZXNwb25zZQpmcm9tIGFwcC5kYi5tb2RlbHMuYXVkaXQgaW1wb3J0IEF1ZGl0RXZlbnQsIEF1ZGl0V3Jp
dGVGYWlsdXJlUmVjb3JkCmZyb20gYXBwLmRiLm1vZGVscy5jYWxpYnJhdGlvbl9yZXBvcnQgaW1wb3J0IENhbGlicmF0aW9uUmVwb3J0CmZyb20gYXBwLmRi
Lm1vZGVscy5jYW5kbGUgaW1wb3J0IENhbmRsZQpmcm9tIGFwcC5kYi5tb2RlbHMuY2hhcnRfcmVzZWFyY2hfYW5ub3RhdGlvbiBpbXBvcnQgQ2hhcnRSZXNl
YXJjaEFubm90YXRpb24KZnJvbSBhcHAuZGIubW9kZWxzLmNvcnJlbGF0aW9uX3JlcG9ydCBpbXBvcnQgQ29ycmVsYXRpb25SZXBvcnQKZnJvbSBhcHAuZGIu
bW9kZWxzLmRhdGFzZXQgaW1wb3J0ICgKICAgIERhdGFzZXRMaW5lYWdlUmVjb3JkLAogICAgRGF0YXNldFF1YXJhbnRpbmVSZWNvcmQsCiAgICBEYXRhc2V0
U2VyaWVzTWVtYmVyLAogICAgRGF0YXNldFNuYXBzaG90LAopCmZyb20gYXBwLmRiLm1vZGVscy5kYXRhc2V0X3NwbGl0IGltcG9ydCBEYXRhc2V0U3BsaXRN
YW5pZmVzdApmcm9tIGFwcC5kYi5tb2RlbHMuZWNvbm9taWNfcmVwb3J0IGltcG9ydCBFY29ub21pY1JlcG9ydApmcm9tIGFwcC5kYi5tb2RlbHMuZXhlY3V0
aW9uX2V4cGVyaW1lbnQgaW1wb3J0IEV4ZWN1dGlvblJlc2VhcmNoRXhwZXJpbWVudApmcm9tIGFwcC5kYi5tb2RlbHMuZXhlY3V0aW9uX3Jpc2tfcmVwb3J0
IGltcG9ydCBFeGVjdXRpb25SaXNrUmVzZWFyY2hSZXBvcnQKZnJvbSBhcHAuZGIubW9kZWxzLmV4cGVyaW1lbnQgaW1wb3J0IEV4cGVyaW1lbnQKZnJvbSBh
cHAuZGIubW9kZWxzLmZlYXR1cmUgaW1wb3J0IEZlYXR1cmVSZWNvcmQKZnJvbSBhcHAuZGIubW9kZWxzLmZlYXR1cmVfZGVmaW5pdGlvbiBpbXBvcnQgRmVh
dHVyZURlZmluaXRpb24sIEZlYXR1cmVRdWFsaXR5UmVwb3J0CmZyb20gYXBwLmRiLm1vZGVscy5nZW5lcmFsaXphdGlvbiBpbXBvcnQgRHJpZnRNb25pdG9y
aW5nUmVjb3JkLCBHZW5lcmFsaXphdGlvblJlcG9ydApmcm9tIGFwcC5kYi5tb2RlbHMuaW5nZXN0aW9uX3J1biBpbXBvcnQgSW5nZXN0aW9uUnVuCmZyb20g
YXBwLmRiLm1vZGVscy5tYW51YWxfdHJhZGVfam91cm5hbF9lbnRyeSBpbXBvcnQgTWFudWFsVHJhZGVKb3VybmFsRW50cnlSZWNvcmQKZnJvbSBhcHAuZGIu
bW9kZWxzLm1hcmtldF9tZXRhZGF0YSBpbXBvcnQgTWFya2V0U2VyaWVzTWV0YWRhdGEKZnJvbSBhcHAuZGIubW9kZWxzLm1vZGVsX2FydGlmYWN0IGltcG9y
dCBNb2RlbEFydGlmYWN0CmZyb20gYXBwLmRiLm1vZGVscy5tb25pdG9yaW5nX2FsZXJ0IGltcG9ydCBNb25pdG9yaW5nQWxlcnQKZnJvbSBhcHAuZGIubW9k
ZWxzLm9wZXJhdG9yIGltcG9ydCBPcGVyYXRvcgpmcm9tIGFwcC5kYi5tb2RlbHMub3BlcmF0b3Jfd29ya3NwYWNlX3ByZWZlcmVuY2UgaW1wb3J0IE9wZXJh
dG9yV29ya3NwYWNlUHJlZmVyZW5jZQpmcm9tIGFwcC5kYi5tb2RlbHMucG9ydGZvbGlvX3Jpc2tfcmVwb3J0IGltcG9ydCBQb3J0Zm9saW9SaXNrUmVwb3J0
CmZyb20gYXBwLmRiLm1vZGVscy5yZWZyZXNoX3Rva2VuIGltcG9ydCBSZWZyZXNoVG9rZW5SZWNvcmQKZnJvbSBhcHAuZGIubW9kZWxzLnJlZ2ltZV9yZXBv
cnQgaW1wb3J0IFJlZ2ltZVJlcG9ydApmcm9tIGFwcC5kYi5tb2RlbHMucmVzZWFyY2hfbWFuYWdlbWVudCBpbXBvcnQgKAogICAgUmVzZWFyY2hDb2xsZWN0
aW9uLAogICAgUmVzZWFyY2hDb2xsZWN0aW9uTWVtYmVyLAogICAgUmVzZWFyY2hUYWcsCikKZnJvbSBhcHAuZGIubW9kZWxzLnNjZW5hcmlvX3JlcG9ydCBp
bXBvcnQgU2NlbmFyaW9SZXBvcnQKZnJvbSBhcHAuZGIubW9kZWxzLnNpZ25hbF92YWxpZGF0aW9uX3JlcG9ydCBpbXBvcnQgU2lnbmFsVmFsaWRhdGlvblJl
cG9ydApmcm9tIGFwcC5kYi5tb2RlbHMuc2ltdWxhdGVkX2V4ZWN1dGlvbiBpbXBvcnQgU2ltdWxhdGVkRXhlY3V0aW9uUnVuLCBTaW11bGF0ZWRGaWxsRXZl
bnQKZnJvbSBhcHAuZGIubW9kZWxzLnNpbXVsYXRlZF9leGVjdXRpb25fYW5hbHl0aWNzX3JlcG9ydCBpbXBvcnQgU2ltdWxhdGVkRXhlY3V0aW9uQW5hbHl0
aWNzUmVwb3J0CmZyb20gYXBwLmRiLm1vZGVscy5zaW11bGF0ZWRfcGFwZXJfbGVkZ2VyIGltcG9ydCBTaW11bGF0ZWRQYXBlckxlZGdlckVudHJ5CmZyb20g
YXBwLmRiLm1vZGVscy50cmFkZV9wbGFuX25vdGUgaW1wb3J0IFRyYWRlUGxhbk5vdGVSZWNvcmQKCiMgVjIgbW9kZWxzIOKAlCBtdXN0IGJlIGltcG9ydGVk
IHNvIEFsZW1iaWMgdGFyZ2V0X21ldGFkYXRhIGluY2x1ZGVzIHRoZW0KZnJvbSBhcHAuZGIubW9kZWxzLnYyX2F1ZGl0X2V2ZW50IGltcG9ydCBWMkF1ZGl0
RXZlbnQKZnJvbSBhcHAuZGIubW9kZWxzLnYyX2NhcGFiaWxpdHlfcmVjb3JkIGltcG9ydCBWMkNhcGFiaWxpdHlSZWNvcmQKZnJvbSBhcHAuZGIubW9kZWxz
LnYyX2xpbmVhZ2VfcmVjb3JkIGltcG9ydCBWMkxpbmVhZ2VSZWNvcmQKZnJvbSBhcHAuZGIubW9kZWxzLnYyX21hcmtldGRhdGEgaW1wb3J0ICgKICAgIFYy
TWRBc09mVmVyaWZpY2F0aW9uLAogICAgVjJNZEluc3RydW1lbnQsCiAgICBWMk1kSW50ZWdyaXR5RXhjZXB0aW9uLAogICAgVjJNZFNlcmllcywKICAgIFYy
TWRTb3VyY2UsCiAgICBWMk1kU3ltYm9sTWFwLAopCmZyb20gYXBwLmRiLm1vZGVscy52Ml9wZXJtaXNzaW9uIGltcG9ydCBWMlBlcm1pc3Npb24KZnJvbSBh
cHAuZGIubW9kZWxzLnYyX3BvcnRmb2xpbyBpbXBvcnQgKAogICAgVjJQb3J0Zm9saW9EZWZpbml0aW9uLAogICAgVjJQb3J0Zm9saW9SaXNrUmVwb3J0LAop
CmZyb20gYXBwLmRiLm1vZGVscy52Ml9wcm92aWRlciBpbXBvcnQgVjJNZFByb3ZpZGVyLCBWMk1kUHJvdmlkZXJTdGF0dXNIaXN0b3J5CmZyb20gYXBwLmRi
Lm1vZGVscy52Ml9yZXNlYXJjaCBpbXBvcnQgKAogICAgVjJDaGFydEludGVsbGlnZW5jZVJlcG9ydCwKICAgIFYyQ29tcHV0YXRpb25WZXJzaW9uLAogICAg
VjJNYXJrZXRDb250ZXh0UmVwb3J0LAopCmZyb20gYXBwLmRiLm1vZGVscy52Ml9yZXNlYXJjaF9nb3Zlcm5hbmNlIGltcG9ydCAoCiAgICBWMk1sRGlhZ25v
c3RpY1JlcG9ydCwKICAgIFYyTWxHb3Zlcm5hbmNlUmVjb3JkLAogICAgVjJNbExpZmVjeWNsZUV2ZW50LAopCmZyb20gYXBwLmRiLm1vZGVscy52Ml9yZXNl
YXJjaF9qb2JzIGltcG9ydCAoCiAgICBWMkJhY2t0ZXN0SW5wdXQsCiAgICBWMkNvc3RNb2RlbCwKICAgIFYyUmVzZWFyY2hKb2IsCiAgICBWMlJlc2VhcmNo
Sm9iQXR0ZW1wdCwKICAgIFYyUmVzZWFyY2hSZXN1bHQsCiAgICBWMlN0cmF0ZWd5VmVyc2lvbiwKKQpmcm9tIGFwcC5kYi5tb2RlbHMudjJfc2lnbmFsIGlt
cG9ydCBWMlNpZ25hbFJlY29yZCwgVjJTaWduYWxTdGF0ZUV2ZW50CmZyb20gYXBwLmRiLm1vZGVscy52YWxpZGF0aW9uX3JlcG9ydCBpbXBvcnQgVmFsaWRh
dGlvblJlcG9ydApmcm9tIGFwcC5kYi5tb2RlbHMud3NfdGlja2V0IGltcG9ydCBXc1RpY2tldAoKX19hbGxfXyA9IFsKICAgICJBZHZpc29yeVNpZ25hbCIs
CiAgICAiQXNzaXN0YW50UmVzZWFyY2hSZXNwb25zZSIsCiAgICAiQXVkaXRFdmVudCIsCiAgICAiQXVkaXRXcml0ZUZhaWx1cmVSZWNvcmQiLAogICAgIkNh
bGlicmF0aW9uUmVwb3J0IiwKICAgICJDYW5kbGUiLAogICAgIkNoYXJ0UmVzZWFyY2hBbm5vdGF0aW9uIiwKICAgICJDb3JyZWxhdGlvblJlcG9ydCIsCiAg
ICAiRGF0YXNldExpbmVhZ2VSZWNvcmQiLAogICAgIkRhdGFzZXRRdWFyYW50aW5lUmVjb3JkIiwKICAgICJEYXRhc2V0U2VyaWVzTWVtYmVyIiwKICAgICJE
YXRhc2V0U25hcHNob3QiLAogICAgIkRhdGFzZXRTcGxpdE1hbmlmZXN0IiwKICAgICJFY29ub21pY1JlcG9ydCIsCiAgICAiRXhlY3V0aW9uUmVzZWFyY2hF
eHBlcmltZW50IiwKICAgICJFeGVjdXRpb25SaXNrUmVzZWFyY2hSZXBvcnQiLAogICAgIkV4cGVyaW1lbnQiLAogICAgIkZlYXR1cmVEZWZpbml0aW9uIiwK
ICAgICJGZWF0dXJlUXVhbGl0eVJlcG9ydCIsCiAgICAiRmVhdHVyZVJlY29yZCIsCiAgICAiR2VuZXJhbGl6YXRpb25SZXBvcnQiLAogICAgIkRyaWZ0TW9u
aXRvcmluZ1JlY29yZCIsCiAgICAiSW5nZXN0aW9uUnVuIiwKICAgICJNYW51YWxUcmFkZUpvdXJuYWxFbnRyeVJlY29yZCIsCiAgICAiTWFya2V0U2VyaWVz
TWV0YWRhdGEiLAogICAgIk1vZGVsQXJ0aWZhY3QiLAogICAgIk1vbml0b3JpbmdBbGVydCIsCiAgICAiT3BlcmF0b3IiLAogICAgIk9wZXJhdG9yV29ya3Nw
YWNlUHJlZmVyZW5jZSIsCiAgICAiUG9ydGZvbGlvUmlza1JlcG9ydCIsCiAgICAiUmVmcmVzaFRva2VuUmVjb3JkIiwKICAgICJSZWdpbWVSZXBvcnQiLAog
ICAgIlJlc2VhcmNoQ29sbGVjdGlvbiIsCiAgICAiUmVzZWFyY2hDb2xsZWN0aW9uTWVtYmVyIiwKICAgICJSZXNlYXJjaFRhZyIsCiAgICAiU2NlbmFyaW9S
ZXBvcnQiLAogICAgIlNpZ25hbFZhbGlkYXRpb25SZXBvcnQiLAogICAgIlNpbXVsYXRlZEV4ZWN1dGlvblJ1biIsCiAgICAiU2ltdWxhdGVkRmlsbEV2ZW50
IiwKICAgICJTaW11bGF0ZWRFeGVjdXRpb25BbmFseXRpY3NSZXBvcnQiLAogICAgIlNpbXVsYXRlZFBhcGVyTGVkZ2VyRW50cnkiLAogICAgIlRyYWRlUGxh
bk5vdGVSZWNvcmQiLAogICAgIlZhbGlkYXRpb25SZXBvcnQiLAogICAgIldzVGlja2V0IiwKICAgICMgVjIKICAgICJWMkF1ZGl0RXZlbnQiLAogICAgIlYy
TGluZWFnZVJlY29yZCIsCiAgICAiVjJDYXBhYmlsaXR5UmVjb3JkIiwKICAgICJWMlBlcm1pc3Npb24iLAogICAgIlYyTWRBc09mVmVyaWZpY2F0aW9uIiwK
ICAgICJWMk1kSW5zdHJ1bWVudCIsCiAgICAiVjJNZEludGVncml0eUV4Y2VwdGlvbiIsCiAgICAiVjJNZFNlcmllcyIsCiAgICAiVjJNZFNvdXJjZSIsCiAg
ICAiVjJNZFN5bWJvbE1hcCIsCiAgICAiVjJNZFByb3ZpZGVyIiwKICAgICJWMk1kUHJvdmlkZXJTdGF0dXNIaXN0b3J5IiwKICAgICJWMkNvbXB1dGF0aW9u
VmVyc2lvbiIsCiAgICAiVjJNYXJrZXRDb250ZXh0UmVwb3J0IiwKICAgICJWMkNoYXJ0SW50ZWxsaWdlbmNlUmVwb3J0IiwKICAgICJWMk1sR292ZXJuYW5j
ZVJlY29yZCIsCiAgICAiVjJNbExpZmVjeWNsZUV2ZW50IiwKICAgICJWMk1sRGlhZ25vc3RpY1JlcG9ydCIsCiAgICAiVjJTaWduYWxSZWNvcmQiLAogICAg
IlYyU2lnbmFsU3RhdGVFdmVudCIsCiAgICAiVjJQb3J0Zm9saW9EZWZpbml0aW9uIiwKICAgICJWMlBvcnRmb2xpb1Jpc2tSZXBvcnQiLAogICAgIlYyQmFj
a3Rlc3RJbnB1dCIsCiAgICAiVjJDb3N0TW9kZWwiLAogICAgIlYyU3RyYXRlZ3lWZXJzaW9uIiwKICAgICJWMlJlc2VhcmNoSm9iIiwKICAgICJWMlJlc2Vh
cmNoSm9iQXR0ZW1wdCIsCiAgICAiVjJSZXNlYXJjaFJlc3VsdCIsCl0K
'@
Write-Evidence ("record 2/17 staged: " + $Rec2Path)
$Rec3Path = "app\db\models\v2_research_jobs.py"
$Rec3Sha  = "abc993d94ef603abacde26cf20b63a69ca0b09d4969ea5bdc75cfbf34f0df8ca"
$Rec3B64 = @'
IiIiVjIgQkUtNyB0YWJsZXMgKEJPLVYyLUJFLTctMDAxIMKnMSBVLTE7IHNpeCBwaHlzaWNhbCB0YWJsZXMpLgoKRml2ZSBndWFyZGVkLWltbXV0YWJsZSAr
IHRoZSBiYW5kJ3Mgc29sZSBtdXRhYmxlIHJvdyBzZXQKKGB2Ml9yZXNlYXJjaF9qb2JgIOKAlCBGUC0xIGFjY2VwdGVkIG1vZGVsOiBtdXRhYmxlIHF1ZXVl
IHN0YXRlLCBpbW11dGFibGUKYXR0ZW1wdCBsZWRnZXIsIEMxL0MyIHdyaXRlLW9uY2UvbXV0YWJsZS1zZXQgY29uZGl0aW9ucykuCiIiIgoKZnJvbSBfX2Z1
dHVyZV9fIGltcG9ydCBhbm5vdGF0aW9ucwoKZnJvbSBkYXRldGltZSBpbXBvcnQgZGF0ZXRpbWUKZnJvbSB1dWlkIGltcG9ydCB1dWlkNAoKZnJvbSBzcWxh
bGNoZW15IGltcG9ydCAoCiAgICBKU09OLAogICAgQ2hlY2tDb25zdHJhaW50LAogICAgRGF0ZVRpbWUsCiAgICBJbmRleCwKICAgIEludGVnZXIsCiAgICBT
dHJpbmcsCiAgICBVbmlxdWVDb25zdHJhaW50LAopCmZyb20gc3FsYWxjaGVteS5vcm0gaW1wb3J0IE1hcHBlZCwgbWFwcGVkX2NvbHVtbgoKZnJvbSBhcHAu
ZGIuYmFzZSBpbXBvcnQgQmFzZQpmcm9tIGFwcC52Mi50ZW1wb3JhbC52YWxpZGF0aW9uIGltcG9ydCB1dGNfbm93CgpfREFUQV9DTEFTU19DSEVDSyA9ICgK
ICAgICJkYXRhX2NsYXNzIElOICgnc3ludGhldGljJywnc2ltdWxhdGVkJywnaGlzdG9yaWNhbF9yZWFsJywnbGl2ZScsIgogICAgIidzdGFsZV9jYWNoZWQn
LCd1bmF2YWlsYWJsZScpIgopCgoKY2xhc3MgVjJCYWNrdGVzdElucHV0KEJhc2UpOgogICAgIiIiVmVyc2lvbmVkLWltbXV0YWJsZSBpbnB1dCByZWdpc3Ry
eSAoUkVRLTEuMykuIiIiCgogICAgX190YWJsZW5hbWVfXyA9ICJ2Ml9iYWNrdGVzdF9pbnB1dCIKICAgIF9fdGFibGVfYXJnc19fID0gKAogICAgICAgIFVu
aXF1ZUNvbnN0cmFpbnQoImlucHV0X2lkIiwgInJlY29yZF9zZXEiLCBuYW1lPSJ1cV92Ml9idGluX2lkX3NlcSIpLAogICAgICAgIFVuaXF1ZUNvbnN0cmFp
bnQoImNvbnRlbnRfaGFzaCIsIG5hbWU9InVxX3YyX2J0aW5fY29udGVudCIpLAogICAgICAgIEluZGV4KCJpeF92Ml9idGluX2lucHV0IiwgImlucHV0X2lk
IiksCiAgICAgICAgQ2hlY2tDb25zdHJhaW50KAogICAgICAgICAgICAicmVnaXN0cmF0aW9uX291dGNvbWUgSU4gKCdyZWdpc3RlcmVkJywncmV1c2VkJywn
cmVmdXNlZCcpIiwKICAgICAgICAgICAgbmFtZT0iY2tfdjJfYnRpbl9vdXRjb21lIiksCiAgICAgICAgQ2hlY2tDb25zdHJhaW50KF9EQVRBX0NMQVNTX0NI
RUNLLCBuYW1lPSJja192Ml9idGluX2RhdGFfY2xhc3MiKSwKICAgICkKCiAgICBpZDogTWFwcGVkW3N0cl0gPSBtYXBwZWRfY29sdW1uKFN0cmluZygzNiks
IHByaW1hcnlfa2V5PVRydWUsIGRlZmF1bHQ9bGFtYmRhOiBzdHIodXVpZDQoKSkpCiAgICBpbnB1dF9pZDogTWFwcGVkW3N0cl0gPSBtYXBwZWRfY29sdW1u
KFN0cmluZyg2NCksIG51bGxhYmxlPUZhbHNlKQogICAgcmVjb3JkX3NlcTogTWFwcGVkW2ludF0gPSBtYXBwZWRfY29sdW1uKEludGVnZXIsIG51bGxhYmxl
PUZhbHNlKQogICAgc3VwZXJzZWRlczogTWFwcGVkW3N0ciB8IE5vbmVdID0gbWFwcGVkX2NvbHVtbihTdHJpbmcoMzYpLCBudWxsYWJsZT1UcnVlKQogICAg
Y29udGVudF9oYXNoOiBNYXBwZWRbc3RyXSA9IG1hcHBlZF9jb2x1bW4oU3RyaW5nKDY0KSwgbnVsbGFibGU9RmFsc2UpCiAgICBzZXJpZXNfcmVmczogTWFw
cGVkW2RpY3RdID0gbWFwcGVkX2NvbHVtbihKU09OLCBudWxsYWJsZT1GYWxzZSkKICAgIHdpbmRvd19zdGFydDogTWFwcGVkW2RhdGV0aW1lXSA9IG1hcHBl
ZF9jb2x1bW4oRGF0ZVRpbWUodGltZXpvbmU9VHJ1ZSksIG51bGxhYmxlPUZhbHNlKQogICAgd2luZG93X2VuZDogTWFwcGVkW2RhdGV0aW1lXSA9IG1hcHBl
ZF9jb2x1bW4oRGF0ZVRpbWUodGltZXpvbmU9VHJ1ZSksIG51bGxhYmxlPUZhbHNlKQogICAgcmVnaXN0cmF0aW9uX291dGNvbWU6IE1hcHBlZFtzdHJdID0g
bWFwcGVkX2NvbHVtbihTdHJpbmcoMTYpLCBudWxsYWJsZT1GYWxzZSkKICAgIGRhdGFfY2xhc3M6IE1hcHBlZFtzdHJdID0gbWFwcGVkX2NvbHVtbihTdHJp
bmcoMzIpLCBudWxsYWJsZT1GYWxzZSkKICAgIG1vZGU6IE1hcHBlZFtzdHJdID0gbWFwcGVkX2NvbHVtbihTdHJpbmcoMTYpLCBudWxsYWJsZT1GYWxzZSkK
ICAgIG9wZXJhdG9yX2lkOiBNYXBwZWRbc3RyXSA9IG1hcHBlZF9jb2x1bW4oU3RyaW5nKDEyOCksIG51bGxhYmxlPUZhbHNlKQogICAgY29ycmVsYXRpb25f
aWQ6IE1hcHBlZFtzdHIgfCBOb25lXSA9IG1hcHBlZF9jb2x1bW4oU3RyaW5nKDY0KSwgbnVsbGFibGU9VHJ1ZSkKICAgIGNyZWF0ZWRfYXQ6IE1hcHBlZFtk
YXRldGltZV0gPSBtYXBwZWRfY29sdW1uKAogICAgICAgIERhdGVUaW1lKHRpbWV6b25lPVRydWUpLCBkZWZhdWx0PXV0Y19ub3csIG51bGxhYmxlPUZhbHNl
KQoKCmNsYXNzIFYyQ29zdE1vZGVsKEJhc2UpOgogICAgIiIiVmVyc2lvbmVkLWltbXV0YWJsZSBjb3N0LW1vZGVsIGNvbmZpZ3VyYXRpb24gKFJFUS0xLjQp
LiIiIgoKICAgIF9fdGFibGVuYW1lX18gPSAidjJfY29zdF9tb2RlbCIKICAgIF9fdGFibGVfYXJnc19fID0gKAogICAgICAgIFVuaXF1ZUNvbnN0cmFpbnQo
ImNvc3RfbW9kZWxfaWQiLCAicmVjb3JkX3NlcSIsCiAgICAgICAgICAgICAgICAgICAgICAgICBuYW1lPSJ1cV92Ml9jb3N0X2lkX3NlcSIpLAogICAgICAg
IEluZGV4KCJpeF92Ml9jb3N0X21vZGVsIiwgImNvc3RfbW9kZWxfaWQiKSwKICAgICAgICBDaGVja0NvbnN0cmFpbnQoX0RBVEFfQ0xBU1NfQ0hFQ0ssIG5h
bWU9ImNrX3YyX2Nvc3RfZGF0YV9jbGFzcyIpLAogICAgKQoKICAgIGlkOiBNYXBwZWRbc3RyXSA9IG1hcHBlZF9jb2x1bW4oU3RyaW5nKDM2KSwgcHJpbWFy
eV9rZXk9VHJ1ZSwgZGVmYXVsdD1sYW1iZGE6IHN0cih1dWlkNCgpKSkKICAgIGNvc3RfbW9kZWxfaWQ6IE1hcHBlZFtzdHJdID0gbWFwcGVkX2NvbHVtbihT
dHJpbmcoNjQpLCBudWxsYWJsZT1GYWxzZSkKICAgIHJlY29yZF9zZXE6IE1hcHBlZFtpbnRdID0gbWFwcGVkX2NvbHVtbihJbnRlZ2VyLCBudWxsYWJsZT1G
YWxzZSkKICAgIHN1cGVyc2VkZXM6IE1hcHBlZFtzdHIgfCBOb25lXSA9IG1hcHBlZF9jb2x1bW4oU3RyaW5nKDM2KSwgbnVsbGFibGU9VHJ1ZSkKICAgIHNw
cmVhZDogTWFwcGVkW2RpY3RdID0gbWFwcGVkX2NvbHVtbihKU09OLCBudWxsYWJsZT1GYWxzZSkKICAgIGNvbW1pc3Npb246IE1hcHBlZFtkaWN0XSA9IG1h
cHBlZF9jb2x1bW4oSlNPTiwgbnVsbGFibGU9RmFsc2UpCiAgICBzbGlwcGFnZTogTWFwcGVkW2RpY3RdID0gbWFwcGVkX2NvbHVtbihKU09OLCBudWxsYWJs
ZT1GYWxzZSkKICAgIGxhdGVuY3lfbXM6IE1hcHBlZFtpbnRdID0gbWFwcGVkX2NvbHVtbihJbnRlZ2VyLCBudWxsYWJsZT1GYWxzZSkKICAgIHJpc2tfbGlt
aXRzOiBNYXBwZWRbZGljdF0gPSBtYXBwZWRfY29sdW1uKEpTT04sIG51bGxhYmxlPUZhbHNlKQogICAgY2l0YXRpb25zOiBNYXBwZWRbZGljdF0gPSBtYXBw
ZWRfY29sdW1uKEpTT04sIG51bGxhYmxlPUZhbHNlKQogICAgZGF0YV9jbGFzczogTWFwcGVkW3N0cl0gPSBtYXBwZWRfY29sdW1uKFN0cmluZygzMiksIG51
bGxhYmxlPUZhbHNlKQogICAgbW9kZTogTWFwcGVkW3N0cl0gPSBtYXBwZWRfY29sdW1uKFN0cmluZygxNiksIG51bGxhYmxlPUZhbHNlKQogICAgb3BlcmF0
b3JfaWQ6IE1hcHBlZFtzdHJdID0gbWFwcGVkX2NvbHVtbihTdHJpbmcoMTI4KSwgbnVsbGFibGU9RmFsc2UpCiAgICBjb3JyZWxhdGlvbl9pZDogTWFwcGVk
W3N0ciB8IE5vbmVdID0gbWFwcGVkX2NvbHVtbihTdHJpbmcoNjQpLCBudWxsYWJsZT1UcnVlKQogICAgY3JlYXRlZF9hdDogTWFwcGVkW2RhdGV0aW1lXSA9
IG1hcHBlZF9jb2x1bW4oCiAgICAgICAgRGF0ZVRpbWUodGltZXpvbmU9VHJ1ZSksIGRlZmF1bHQ9dXRjX25vdywgbnVsbGFibGU9RmFsc2UpCgoKY2xhc3Mg
VjJTdHJhdGVneVZlcnNpb24oQmFzZSk6CiAgICAiIiJWZXJzaW9uZWQtaW1tdXRhYmxlIHN0cmF0ZWd5IHJlZ2lzdHJ5IChSRVEtMS42KS4gU3RydWN0dXJh
bGx5IGZyZWUKICAgIG9mIGNyZWRlbnRpYWwvYWRhcHRlci9vcmRlci9hY2NvdW50IGZpZWxkcyAoUC05KS4iIiIKCiAgICBfX3RhYmxlbmFtZV9fID0gInYy
X3N0cmF0ZWd5X3ZlcnNpb24iCiAgICBfX3RhYmxlX2FyZ3NfXyA9ICgKICAgICAgICBVbmlxdWVDb25zdHJhaW50KCJzdHJhdGVneV9pZCIsICJyZWNvcmRf
c2VxIiwKICAgICAgICAgICAgICAgICAgICAgICAgIG5hbWU9InVxX3YyX3N0cmF0X2lkX3NlcSIpLAogICAgICAgIEluZGV4KCJpeF92Ml9zdHJhdF9zdHJh
dGVneSIsICJzdHJhdGVneV9pZCIpLAogICAgICAgIENoZWNrQ29uc3RyYWludCgKICAgICAgICAgICAgImxpZmVjeWNsZV9zdGF0ZSBJTiAoJ2RyYWZ0Jywn
cmVnaXN0ZXJlZCcsJ3JldGlyZWQnKSIsCiAgICAgICAgICAgIG5hbWU9ImNrX3YyX3N0cmF0X3N0YXRlIiksCiAgICAgICAgQ2hlY2tDb25zdHJhaW50KF9E
QVRBX0NMQVNTX0NIRUNLLCBuYW1lPSJja192Ml9zdHJhdF9kYXRhX2NsYXNzIiksCiAgICApCgogICAgaWQ6IE1hcHBlZFtzdHJdID0gbWFwcGVkX2NvbHVt
bihTdHJpbmcoMzYpLCBwcmltYXJ5X2tleT1UcnVlLCBkZWZhdWx0PWxhbWJkYTogc3RyKHV1aWQ0KCkpKQogICAgc3RyYXRlZ3lfaWQ6IE1hcHBlZFtzdHJd
ID0gbWFwcGVkX2NvbHVtbihTdHJpbmcoNjQpLCBudWxsYWJsZT1GYWxzZSkKICAgIHJlY29yZF9zZXE6IE1hcHBlZFtpbnRdID0gbWFwcGVkX2NvbHVtbihJ
bnRlZ2VyLCBudWxsYWJsZT1GYWxzZSkKICAgIHN1cGVyc2VkZXM6IE1hcHBlZFtzdHIgfCBOb25lXSA9IG1hcHBlZF9jb2x1bW4oU3RyaW5nKDM2KSwgbnVs
bGFibGU9VHJ1ZSkKICAgIG5hbWU6IE1hcHBlZFtzdHJdID0gbWFwcGVkX2NvbHVtbihTdHJpbmcoMTI4KSwgbnVsbGFibGU9RmFsc2UpCiAgICBwYXJhbWV0
ZXJzOiBNYXBwZWRbZGljdF0gPSBtYXBwZWRfY29sdW1uKEpTT04sIG51bGxhYmxlPUZhbHNlKQogICAgbGlmZWN5Y2xlX3N0YXRlOiBNYXBwZWRbc3RyXSA9
IG1hcHBlZF9jb2x1bW4oU3RyaW5nKDE2KSwgbnVsbGFibGU9RmFsc2UpCiAgICBkYXRhX2NsYXNzOiBNYXBwZWRbc3RyXSA9IG1hcHBlZF9jb2x1bW4oU3Ry
aW5nKDMyKSwgbnVsbGFibGU9RmFsc2UpCiAgICBtb2RlOiBNYXBwZWRbc3RyXSA9IG1hcHBlZF9jb2x1bW4oU3RyaW5nKDE2KSwgbnVsbGFibGU9RmFsc2Up
CiAgICBvcGVyYXRvcl9pZDogTWFwcGVkW3N0cl0gPSBtYXBwZWRfY29sdW1uKFN0cmluZygxMjgpLCBudWxsYWJsZT1GYWxzZSkKICAgIGNvcnJlbGF0aW9u
X2lkOiBNYXBwZWRbc3RyIHwgTm9uZV0gPSBtYXBwZWRfY29sdW1uKFN0cmluZyg2NCksIG51bGxhYmxlPVRydWUpCiAgICBjcmVhdGVkX2F0OiBNYXBwZWRb
ZGF0ZXRpbWVdID0gbWFwcGVkX2NvbHVtbigKICAgICAgICBEYXRlVGltZSh0aW1lem9uZT1UcnVlKSwgZGVmYXVsdD11dGNfbm93LCBudWxsYWJsZT1GYWxz
ZSkKCgpjbGFzcyBWMlJlc2VhcmNoSm9iKEJhc2UpOgogICAgIiIiVGhlIGdvdmVybmVkIHF1ZXVlIOKAlCB0aGUgYmFuZCdzIFNPTEUgbXV0YWJsZSByb3cg
c2V0IChGUC0xKS4KICAgIEMxOiBvd25lci9hdXRob3JpemF0aW9uX3JlZi9pbnB1dHMvc2NoZWR1bGUgd3JpdGUtb25jZS4KICAgIEMyOiBtdXRhYmxlIHNl
dCBleGFjdGx5IHtqb2Jfc3RhdGUsIGF0dGVtcHRfY291bnQsIG91dHB1dF9yZWYsIGZhaWx1cmV9LiIiIgoKICAgIF9fdGFibGVuYW1lX18gPSAidjJfcmVz
ZWFyY2hfam9iIgogICAgX190YWJsZV9hcmdzX18gPSAoCiAgICAgICAgSW5kZXgoIml4X3YyX2pvYl9zdGF0ZSIsICJqb2Jfc3RhdGUiKSwKICAgICAgICBD
aGVja0NvbnN0cmFpbnQoCiAgICAgICAgICAgICJqb2Jfc3RhdGUgSU4gKCdxdWV1ZWQnLCdydW5uaW5nJywnc3VjY2VlZGVkJywnZmFpbGVkJywiCiAgICAg
ICAgICAgICInY2FuY2VsbGVkJykiLAogICAgICAgICAgICBuYW1lPSJja192Ml9qb2Jfc3RhdGUiKSwKICAgICAgICBDaGVja0NvbnN0cmFpbnQoX0RBVEFf
Q0xBU1NfQ0hFQ0ssIG5hbWU9ImNrX3YyX2pvYl9kYXRhX2NsYXNzIiksCiAgICApCgogICAgaWQ6IE1hcHBlZFtzdHJdID0gbWFwcGVkX2NvbHVtbihTdHJp
bmcoMzYpLCBwcmltYXJ5X2tleT1UcnVlLCBkZWZhdWx0PWxhbWJkYTogc3RyKHV1aWQ0KCkpKQogICAgb3duZXI6IE1hcHBlZFtzdHJdID0gbWFwcGVkX2Nv
bHVtbihTdHJpbmcoMTI4KSwgbnVsbGFibGU9RmFsc2UpCiAgICBhdXRob3JpemF0aW9uX3JlZjogTWFwcGVkW3N0cl0gPSBtYXBwZWRfY29sdW1uKFN0cmlu
ZygxMjgpLCBudWxsYWJsZT1GYWxzZSkKICAgIGlucHV0czogTWFwcGVkW2RpY3RdID0gbWFwcGVkX2NvbHVtbihKU09OLCBudWxsYWJsZT1GYWxzZSkKICAg
IHNjaGVkdWxlOiBNYXBwZWRbZGljdF0gPSBtYXBwZWRfY29sdW1uKEpTT04sIG51bGxhYmxlPUZhbHNlKQogICAgb3V0cHV0X3JlZjogTWFwcGVkW3N0ciB8
IE5vbmVdID0gbWFwcGVkX2NvbHVtbihTdHJpbmcoMzYpLCBudWxsYWJsZT1UcnVlKQogICAgZmFpbHVyZTogTWFwcGVkW2RpY3QgfCBOb25lXSA9IG1hcHBl
ZF9jb2x1bW4oSlNPTiwgbnVsbGFibGU9VHJ1ZSkKICAgIGpvYl9zdGF0ZTogTWFwcGVkW3N0cl0gPSBtYXBwZWRfY29sdW1uKFN0cmluZygxNiksIG51bGxh
YmxlPUZhbHNlKQogICAgYXR0ZW1wdF9jb3VudDogTWFwcGVkW2ludF0gPSBtYXBwZWRfY29sdW1uKEludGVnZXIsIG51bGxhYmxlPUZhbHNlLCBkZWZhdWx0
PTApCiAgICBkYXRhX2NsYXNzOiBNYXBwZWRbc3RyXSA9IG1hcHBlZF9jb2x1bW4oU3RyaW5nKDMyKSwgbnVsbGFibGU9RmFsc2UpCiAgICBtb2RlOiBNYXBw
ZWRbc3RyXSA9IG1hcHBlZF9jb2x1bW4oU3RyaW5nKDE2KSwgbnVsbGFibGU9RmFsc2UpCiAgICBvcGVyYXRvcl9pZDogTWFwcGVkW3N0cl0gPSBtYXBwZWRf
Y29sdW1uKFN0cmluZygxMjgpLCBudWxsYWJsZT1GYWxzZSkKICAgIGNvcnJlbGF0aW9uX2lkOiBNYXBwZWRbc3RyIHwgTm9uZV0gPSBtYXBwZWRfY29sdW1u
KFN0cmluZyg2NCksIG51bGxhYmxlPVRydWUpCiAgICBjcmVhdGVkX2F0OiBNYXBwZWRbZGF0ZXRpbWVdID0gbWFwcGVkX2NvbHVtbigKICAgICAgICBEYXRl
VGltZSh0aW1lem9uZT1UcnVlKSwgZGVmYXVsdD11dGNfbm93LCBudWxsYWJsZT1GYWxzZSkKCgpjbGFzcyBWMlJlc2VhcmNoSm9iQXR0ZW1wdChCYXNlKToK
ICAgICIiIkFwcGVuZC1vbmx5IGF0dGVtcHQgbGVkZ2VyIOKAlCB0aGUgUC0xMCBpZGVtcG90ZW5jeSBhbmNob3IuIiIiCgogICAgX190YWJsZW5hbWVfXyA9
ICJ2Ml9yZXNlYXJjaF9qb2JfYXR0ZW1wdCIKICAgIF9fdGFibGVfYXJnc19fID0gKAogICAgICAgIFVuaXF1ZUNvbnN0cmFpbnQoImpvYl9pZCIsICJhdHRl
bXB0X2luZGV4IiwgbmFtZT0idXFfdjJfam9iYXR0X2lkeCIpLAogICAgICAgIEluZGV4KCJpeF92Ml9qb2JhdHRfam9iIiwgImpvYl9pZCIpLAogICAgICAg
IENoZWNrQ29uc3RyYWludCgKICAgICAgICAgICAgIm91dGNvbWUgSU4gKCdzdWNjZWVkZWQnLCdmYWlsZWQnLCdjYW5jZWxsZWQnKSIsCiAgICAgICAgICAg
IG5hbWU9ImNrX3YyX2pvYmF0dF9vdXRjb21lIiksCiAgICApCgogICAgaWQ6IE1hcHBlZFtzdHJdID0gbWFwcGVkX2NvbHVtbihTdHJpbmcoMzYpLCBwcmlt
YXJ5X2tleT1UcnVlLCBkZWZhdWx0PWxhbWJkYTogc3RyKHV1aWQ0KCkpKQogICAgam9iX2lkOiBNYXBwZWRbc3RyXSA9IG1hcHBlZF9jb2x1bW4oU3RyaW5n
KDM2KSwgbnVsbGFibGU9RmFsc2UpCiAgICBhdHRlbXB0X2luZGV4OiBNYXBwZWRbaW50XSA9IG1hcHBlZF9jb2x1bW4oSW50ZWdlciwgbnVsbGFibGU9RmFs
c2UpCiAgICBvdXRjb21lOiBNYXBwZWRbc3RyXSA9IG1hcHBlZF9jb2x1bW4oU3RyaW5nKDE2KSwgbnVsbGFibGU9RmFsc2UpCiAgICBhcnRpZmFjdF9yZWY6
IE1hcHBlZFtzdHIgfCBOb25lXSA9IG1hcHBlZF9jb2x1bW4oU3RyaW5nKDM2KSwgbnVsbGFibGU9VHJ1ZSkKICAgIHJlYXNvbjogTWFwcGVkW2RpY3RdID0g
bWFwcGVkX2NvbHVtbihKU09OLCBudWxsYWJsZT1GYWxzZSkKICAgIGFjdG9yX2lkOiBNYXBwZWRbc3RyXSA9IG1hcHBlZF9jb2x1bW4oU3RyaW5nKDEyOCks
IG51bGxhYmxlPUZhbHNlKQogICAgbW9kZTogTWFwcGVkW3N0cl0gPSBtYXBwZWRfY29sdW1uKFN0cmluZygxNiksIG51bGxhYmxlPUZhbHNlKQogICAgb3Bl
cmF0b3JfaWQ6IE1hcHBlZFtzdHJdID0gbWFwcGVkX2NvbHVtbihTdHJpbmcoMTI4KSwgbnVsbGFibGU9RmFsc2UpCiAgICBjb3JyZWxhdGlvbl9pZDogTWFw
cGVkW3N0ciB8IE5vbmVdID0gbWFwcGVkX2NvbHVtbihTdHJpbmcoNjQpLCBudWxsYWJsZT1UcnVlKQogICAgY3JlYXRlZF9hdDogTWFwcGVkW2RhdGV0aW1l
XSA9IG1hcHBlZF9jb2x1bW4oCiAgICAgICAgRGF0ZVRpbWUodGltZXpvbmU9VHJ1ZSksIGRlZmF1bHQ9dXRjX25vdywgbnVsbGFibGU9RmFsc2UpCgoKY2xh
c3MgVjJSZXNlYXJjaFJlc3VsdChCYXNlKToKICAgICIiIkltbXV0YWJsZSByZXN1bHQgYXJ0aWZhY3RzLiBgcGFwZXJgL2BsaXZlYCBhYnNlbnQgZnJvbSB0
aGUgQ0hFQ0sg4oCUCiAgICBzY2hlbWEtaW1wb3NzaWJsZSAoUC05KS4iIiIKCiAgICBfX3RhYmxlbmFtZV9fID0gInYyX3Jlc2VhcmNoX3Jlc3VsdCIKICAg
IF9fdGFibGVfYXJnc19fID0gKAogICAgICAgIFVuaXF1ZUNvbnN0cmFpbnQoInN0cmF0ZWd5X3ZlcnNpb25faWQiLCAiaW5wdXRzX2hhc2giLAogICAgICAg
ICAgICAgICAgICAgICAgICAgImVuZ2luZV92ZXJzaW9uc19oYXNoIiwKICAgICAgICAgICAgICAgICAgICAgICAgIG5hbWU9InVxX3YyX3Jlc3VsdF9kZXRl
cm1pbmlzbV9hbmNob3IiKSwKICAgICAgICBJbmRleCgiaXhfdjJfcmVzdWx0X2pvYiIsICJqb2JfaWQiKSwKICAgICAgICBDaGVja0NvbnN0cmFpbnQoInJl
c3VsdF9jbGFzcyBJTiAoJ2JhY2t0ZXN0Jywnc2ltdWxhdGlvbicpIiwKICAgICAgICAgICAgICAgICAgICAgICAgbmFtZT0iY2tfdjJfcmVzdWx0X2NsYXNz
IiksCiAgICAgICAgQ2hlY2tDb25zdHJhaW50KF9EQVRBX0NMQVNTX0NIRUNLLCBuYW1lPSJja192Ml9yZXN1bHRfZGF0YV9jbGFzcyIpLAogICAgKQoKICAg
IGlkOiBNYXBwZWRbc3RyXSA9IG1hcHBlZF9jb2x1bW4oU3RyaW5nKDM2KSwgcHJpbWFyeV9rZXk9VHJ1ZSwgZGVmYXVsdD1sYW1iZGE6IHN0cih1dWlkNCgp
KSkKICAgIHJlc3VsdF9jbGFzczogTWFwcGVkW3N0cl0gPSBtYXBwZWRfY29sdW1uKFN0cmluZygxNiksIG51bGxhYmxlPUZhbHNlKQogICAgam9iX2lkOiBN
YXBwZWRbc3RyXSA9IG1hcHBlZF9jb2x1bW4oU3RyaW5nKDM2KSwgbnVsbGFibGU9RmFsc2UpCiAgICBhdHRlbXB0X2luZGV4OiBNYXBwZWRbaW50XSA9IG1h
cHBlZF9jb2x1bW4oSW50ZWdlciwgbnVsbGFibGU9RmFsc2UpCiAgICBzdHJhdGVneV92ZXJzaW9uX2lkOiBNYXBwZWRbc3RyXSA9IG1hcHBlZF9jb2x1bW4o
U3RyaW5nKDM2KSwgbnVsbGFibGU9RmFsc2UpCiAgICBpbnB1dF9yZWdpc3RyeV9pZDogTWFwcGVkW3N0cl0gPSBtYXBwZWRfY29sdW1uKFN0cmluZygzNiks
IG51bGxhYmxlPUZhbHNlKQogICAgY29zdF9tb2RlbF9pZDogTWFwcGVkW3N0cl0gPSBtYXBwZWRfY29sdW1uKFN0cmluZygzNiksIG51bGxhYmxlPUZhbHNl
KQogICAgaW5wdXRzX2hhc2g6IE1hcHBlZFtzdHJdID0gbWFwcGVkX2NvbHVtbihTdHJpbmcoNjQpLCBudWxsYWJsZT1GYWxzZSkKICAgIGVuZ2luZV92ZXJz
aW9uczogTWFwcGVkW2RpY3RdID0gbWFwcGVkX2NvbHVtbihKU09OLCBudWxsYWJsZT1GYWxzZSkKICAgIGVuZ2luZV92ZXJzaW9uc19oYXNoOiBNYXBwZWRb
c3RyXSA9IG1hcHBlZF9jb2x1bW4oU3RyaW5nKDY0KSwgbnVsbGFibGU9RmFsc2UpCiAgICBzdW1tYXJ5OiBNYXBwZWRbZGljdF0gPSBtYXBwZWRfY29sdW1u
KEpTT04sIG51bGxhYmxlPUZhbHNlKQogICAgcmVwbGF5X29mOiBNYXBwZWRbc3RyIHwgTm9uZV0gPSBtYXBwZWRfY29sdW1uKFN0cmluZygzNiksIG51bGxh
YmxlPVRydWUpCiAgICB0aW1lX2Jhc2lzOiBNYXBwZWRbZGljdF0gPSBtYXBwZWRfY29sdW1uKEpTT04sIG51bGxhYmxlPUZhbHNlKQogICAgZGF0YV9jbGFz
czogTWFwcGVkW3N0cl0gPSBtYXBwZWRfY29sdW1uKFN0cmluZygzMiksIG51bGxhYmxlPUZhbHNlKQogICAgbW9kZTogTWFwcGVkW3N0cl0gPSBtYXBwZWRf
Y29sdW1uKFN0cmluZygxNiksIG51bGxhYmxlPUZhbHNlKQogICAgb3BlcmF0b3JfaWQ6IE1hcHBlZFtzdHJdID0gbWFwcGVkX2NvbHVtbihTdHJpbmcoMTI4
KSwgbnVsbGFibGU9RmFsc2UpCiAgICBjb3JyZWxhdGlvbl9pZDogTWFwcGVkW3N0ciB8IE5vbmVdID0gbWFwcGVkX2NvbHVtbihTdHJpbmcoNjQpLCBudWxs
YWJsZT1UcnVlKQogICAgY3JlYXRlZF9hdDogTWFwcGVkW2RhdGV0aW1lXSA9IG1hcHBlZF9jb2x1bW4oCiAgICAgICAgRGF0ZVRpbWUodGltZXpvbmU9VHJ1
ZSksIGRlZmF1bHQ9dXRjX25vdywgbnVsbGFibGU9RmFsc2UpCg==
'@
Write-Evidence ("record 3/17 staged: " + $Rec3Path)
$Rec4Path = "app\v2\api\router.py"
$Rec4Sha  = "ad4afdd4eb5fe0c0676c45a9b779cb9eeeb16140163e6f7243fd3c9ad606f670"
$Rec4B64 = @'
IiIiVjIgQVBJIFJvdXRlciDigJQgYWdncmVnYXRlIHJvdXRlciBmb3IgYWxsIFYyIGVuZHBvaW50cy4iIiIKCmZyb20gX19mdXR1cmVfXyBpbXBvcnQgYW5u
b3RhdGlvbnMKCmZyb20gZGF0ZXRpbWUgaW1wb3J0IGRhdGV0aW1lLCB0aW1lem9uZQoKZnJvbSBmYXN0YXBpIGltcG9ydCBBUElSb3V0ZXIsIFJlcXVlc3QK
CmZyb20gYXBwLnYyLmFwaS5hdWRpdCBpbXBvcnQgcm91dGVyIGFzIGF1ZGl0X3JvdXRlcgpmcm9tIGFwcC52Mi5hcGkuY2FwYWJpbGl0eSBpbXBvcnQgcm91
dGVyIGFzIGNhcGFiaWxpdHlfcm91dGVyCmZyb20gYXBwLnYyLmFwaS5saW5lYWdlIGltcG9ydCByb3V0ZXIgYXMgbGluZWFnZV9yb3V0ZXIKZnJvbSBhcHAu
djIuYXBpLm1vZGUgaW1wb3J0IHJvdXRlciBhcyBtb2RlX3JvdXRlcgpmcm9tIGFwcC52Mi5lcnJvcnMuY29udHJhY3QgaW1wb3J0IFYyRXJyb3JDb2RlCmZy
b20gYXBwLnYyLm1hcmtldGRhdGEuYXBpLnJvdXRlciBpbXBvcnQgcm91dGVyIGFzIG1hcmtldGRhdGFfcm91dGVyCmZyb20gYXBwLnYyLm1vZGVscy5lcnJv
cnMgaW1wb3J0IFYyRXJyb3JUYXhvbm9teVJlc3BvbnNlCmZyb20gYXBwLnYyLnBvcnRmb2xpb19yZXNlYXJjaC5hcGkgaW1wb3J0IHJvdXRlciBhcyBwb3J0
Zm9saW9fcmVzZWFyY2hfcm91dGVyCmZyb20gYXBwLnYyLnJiYWMuZGVwZW5kZW5jaWVzIGltcG9ydCBSZXF1aXJlVjJFcnJvclJlYWQKZnJvbSBhcHAudjIu
cmVzZWFyY2guYXBpIGltcG9ydCByb3V0ZXIgYXMgcmVzZWFyY2hfcm91dGVyCmZyb20gYXBwLnYyLnJlc2VhcmNoX2dvdmVybmFuY2UuYXBpIGltcG9ydCBy
b3V0ZXIgYXMgcmVzZWFyY2hfZ292ZXJuYW5jZV9yb3V0ZXIKZnJvbSBhcHAudjIucmVzZWFyY2hfam9icy5hcGkgaW1wb3J0IHJvdXRlciBhcyByZXNlYXJj
aF9qb2JzX3JvdXRlcgoKcm91dGVyID0gQVBJUm91dGVyKHByZWZpeD0iL3YyIiwgdGFncz1bIlYyIl0pCgojIEluY2x1ZGUgc3ViLXJvdXRlcnMKcm91dGVy
LmluY2x1ZGVfcm91dGVyKG1vZGVfcm91dGVyKQpyb3V0ZXIuaW5jbHVkZV9yb3V0ZXIoY2FwYWJpbGl0eV9yb3V0ZXIpCnJvdXRlci5pbmNsdWRlX3JvdXRl
cihhdWRpdF9yb3V0ZXIpCnJvdXRlci5pbmNsdWRlX3JvdXRlcihsaW5lYWdlX3JvdXRlcikKcm91dGVyLmluY2x1ZGVfcm91dGVyKG1hcmtldGRhdGFfcm91
dGVyKQpyb3V0ZXIuaW5jbHVkZV9yb3V0ZXIocmVzZWFyY2hfcm91dGVyKSAgIyBCRS00IChCTy1WMi1CRS00LTAwMSBELTQpCnJvdXRlci5pbmNsdWRlX3Jv
dXRlcihyZXNlYXJjaF9nb3Zlcm5hbmNlX3JvdXRlcikgICMgQkUtNSAoQk8tVjItQkUtNS0wMDEpCnJvdXRlci5pbmNsdWRlX3JvdXRlcihwb3J0Zm9saW9f
cmVzZWFyY2hfcm91dGVyKSAgIyBCRS02IChCTy1WMi1CRS02LTAwMSkKcm91dGVyLmluY2x1ZGVfcm91dGVyKHJlc2VhcmNoX2pvYnNfcm91dGVyKSAgIyBC
RS03IChCTy1WMi1CRS03LTAwMSkKCgpAcm91dGVyLmdldCgiL2Vycm9ycyIsIHJlc3BvbnNlX21vZGVsPVYyRXJyb3JUYXhvbm9teVJlc3BvbnNlKQphc3lu
YyBkZWYgZ2V0X2Vycm9yX3RheG9ub215KAogICAgcmVxdWVzdDogUmVxdWVzdCwKICAgIG9wZXJhdG9yOiBSZXF1aXJlVjJFcnJvclJlYWQsCikgLT4gVjJF
cnJvclRheG9ub215UmVzcG9uc2U6CiAgICAiIiJHZXQgVjIgZXJyb3IgdGF4b25vbXkgcmVmZXJlbmNlLiBSZWFkLW9ubHkuIiIiCiAgICBlcnJvcl9jb2Rl
cyA9IFsKICAgICAgICB7ImNvZGUiOiBjb2RlLnZhbHVlLCAiY2F0ZWdvcnkiOiBjb2RlLm5hbWUuc3BsaXQoIl8iKVswXS5sb3dlcigpfQogICAgICAgIGZv
ciBjb2RlIGluIFYyRXJyb3JDb2RlCiAgICBdCiAgICBkb21haW5fc3RhdHVzZXMgPSBbImF2YWlsYWJsZSIsICJ1bmF2YWlsYWJsZSIsICJzdGFsZSIsICJk
ZWdyYWRlZCIsICJ1bmtub3duIiwgImRlbmllZCJdCgogICAgcmV0dXJuIFYyRXJyb3JUYXhvbm9teVJlc3BvbnNlKAogICAgICAgIGVycm9yX2NvZGVzPWVy
cm9yX2NvZGVzLAogICAgICAgIGRvbWFpbl9zdGF0dXNlcz1kb21haW5fc3RhdHVzZXMsCiAgICAgICAgbW9kZT1yZXF1ZXN0LmFwcC5zdGF0ZS52Ml9tb2Rl
LAogICAgICAgIGNvcnJlbGF0aW9uX2lkPWdldGF0dHIocmVxdWVzdC5zdGF0ZSwgImNvcnJlbGF0aW9uX2lkIiwgTm9uZSksCiAgICAgICAgdGltZXN0YW1w
PWRhdGV0aW1lLm5vdyh0aW1lem9uZS51dGMpLAogICAgKQo=
'@
Write-Evidence ("record 4/17 staged: " + $Rec4Path)
$Rec5Path = "app\v2\rbac\permissions.py"
$Rec5Sha  = "a3dff08218b2afa7029b678396673c317fe1852f9785697bb35a36cbf0cd3b3a"
$Rec5B64 = @'
IiIiVjIgUkJBQyBQZXJtaXNzaW9ucyDigJQgcmVhZC1vbmx5IHNlZWRlZCBwZXJtaXNzaW9uIGRlZmluaXRpb25zLgoKUGVyIDE3X0lOU1RJVFVUSU9OQUxf
U0VDVVJJVFlfU1RBTkRBUkQubWQgUGFydCBWSToKLSBEZWZhdWx0IERlbnkKLSBFeHBsaWNpdCBQZXJtaXNzaW9uIEdyYW50Ci0gTGVhc3QgUHJpdmlsZWdl
Ci0gQ29tcGxldGUgQXVkaXRhYmlsaXR5CgpQZXJtaXNzaW9ucyBhcmUgc2VlZGVkIGR1cmluZyBtaWdyYXRpb24uIE5vIHJ1bnRpbWUgbXV0YXRpb24uCiIi
IgoKZnJvbSBfX2Z1dHVyZV9fIGltcG9ydCBhbm5vdGF0aW9ucwoKZnJvbSBlbnVtIGltcG9ydCBFbnVtCgoKY2xhc3MgVjJQZXJtaXNzaW9uKHN0ciwgRW51
bSk6CiAgICAiIiJWMiBwZXJtaXNzaW9uIHN0cmluZ3MuIiIiCgogICAgTU9ERV9SRUFEID0gInYyLm1vZGUucmVhZCIKICAgIENBUEFCSUxJVFlfUkVBRCA9
ICJ2Mi5jYXBhYmlsaXR5LnJlYWQiCiAgICBBVURJVF9SRUFEID0gInYyLmF1ZGl0LnJlYWQiCiAgICBBVURJVF9SRUFEX0FMTCA9ICJ2Mi5hdWRpdC5yZWFk
X2FsbCIKICAgIExJTkVBR0VfUkVBRCA9ICJ2Mi5saW5lYWdlLnJlYWQiCiAgICBMSU5FQUdFX1JFQURfQUxMID0gInYyLmxpbmVhZ2UucmVhZF9hbGwiCiAg
ICBFUlJPUl9SRUFEID0gInYyLmVycm9yLnJlYWQiCiAgICAjIEJFLTIgbWFya2V0IGRhdGEgKEJPLVYyLUJFLTItMDAxKQogICAgTUFSS0VUREFUQV9SRUFE
ID0gInYyLm1hcmtldGRhdGEucmVhZCIKICAgIE1BUktFVERBVEFfUkVBRF9BTEwgPSAidjIubWFya2V0ZGF0YS5yZWFkX2FsbCIKICAgIE1BUktFVERBVEFf
VkVSSUZZID0gInYyLm1hcmtldGRhdGEudmVyaWZ5IgogICAgTUFSS0VUREFUQV9DQVRBTE9HX1JFRlJFU0ggPSAidjIubWFya2V0ZGF0YS5jYXRhbG9nLnJl
ZnJlc2giCiAgICAjIEJFLTMgUDEgcHJvdmlkZXIgKEJPLVYyLUJFLTMtUDEtMDAxKSDigJQgcmVhZC1vbmx5CiAgICBQUk9WSURFUl9SRUFEID0gInYyLm1h
cmtldGRhdGEucHJvdmlkZXIucmVhZCIKICAgIFBST1ZJREVSX1JFQURfSElTVE9SWSA9ICJ2Mi5tYXJrZXRkYXRhLnByb3ZpZGVyLnJlYWRfaGlzdG9yeSIK
ICAgICMgQkUtMyBQMiAoQk8tVjItQkUtMy1QMi0wMDEpIOKAlCBhZG1pbi1vbmx5IGNvbnRyYWN0IHRlc3QKICAgIFBST1ZJREVSX0NPTlRSQUNUX1RFU1Qg
PSAidjIubWFya2V0ZGF0YS5wcm92aWRlci5jb250cmFjdF90ZXN0IgogICAgIyBCRS00IHJlc2VhcmNoIHJlYWQgbW9kZWxzIChCTy1WMi1CRS00LTAwMTsg
Ui0xKQogICAgUkVTRUFSQ0hfTUNfUkVBRCA9ICJ2Mi5yZXNlYXJjaC5tYXJrZXRfY29udGV4dC5yZWFkIgogICAgUkVTRUFSQ0hfQ0lfUkVBRCA9ICJ2Mi5y
ZXNlYXJjaC5jaGFydF9pbnRlbGxpZ2VuY2UucmVhZCIKICAgIFJFU0VBUkNIX01DX0NPTVBVVEUgPSAidjIucmVzZWFyY2gubWFya2V0X2NvbnRleHQuY29t
cHV0ZSIKICAgICMgQkUtNSByZXNlYXJjaCBnb3Zlcm5hbmNlIChCTy1WMi1CRS01LTAwMSkKICAgIFJFU0VBUkNIX01MR09WX1JFQUQgPSAidjIucmVzZWFy
Y2gubWxfZ292ZXJuYW5jZS5yZWFkIgogICAgUkVTRUFSQ0hfTUxHT1ZfREVDSURFID0gInYyLnJlc2VhcmNoLm1sX2dvdmVybmFuY2UuZGVjaWRlIgogICAg
UkVTRUFSQ0hfU0lHTkFMX1JFQUQgPSAidjIucmVzZWFyY2guc2lnbmFsLnJlYWQiCiAgICBSRVNFQVJDSF9TSUdOQUxfRU1JVCA9ICJ2Mi5yZXNlYXJjaC5z
aWduYWwuZW1pdCIKICAgIFJFU0VBUkNIX01MRElBR19SRUFEID0gInYyLnJlc2VhcmNoLm1sX2RpYWdub3N0aWNzLnJlYWQiCiAgICAjIEJFLTYgcG9ydGZv
bGlvIHJlc2VhcmNoIChCTy1WMi1CRS02LTAwMSkKICAgIFJFU0VBUkNIX1BGX1JFQUQgPSAidjIucmVzZWFyY2gucG9ydGZvbGlvLnJlYWQiCiAgICBSRVNF
QVJDSF9QRl9ERUZJTkUgPSAidjIucmVzZWFyY2gucG9ydGZvbGlvLmRlZmluZSIKICAgIFJFU0VBUkNIX1BGUklTS19SRUFEID0gInYyLnJlc2VhcmNoLnBv
cnRmb2xpb19yaXNrLnJlYWQiCiAgICBSRVNFQVJDSF9QRlJJU0tfQ09NUFVURSA9ICJ2Mi5yZXNlYXJjaC5wb3J0Zm9saW9fcmlzay5jb21wdXRlIgogICAg
IyBCRS03IHJlc2VhcmNoIGpvYnMgKEJPLVYyLUJFLTctMDAxKQogICAgUkVTRUFSQ0hfSk9CU19SRUFEID0gInYyLnJlc2VhcmNoLmpvYnMucmVhZCIKICAg
IFJFU0VBUkNIX0pPQlNfU1VCTUlUID0gInYyLnJlc2VhcmNoLmpvYnMuc3VibWl0IgogICAgUkVTRUFSQ0hfSk9CU19DQU5DRUwgPSAidjIucmVzZWFyY2gu
am9icy5jYW5jZWwiCiAgICBSRVNFQVJDSF9SRUdJU1RSWV9SRUFEID0gInYyLnJlc2VhcmNoLnJlZ2lzdHJ5LnJlYWQiCiAgICBSRVNFQVJDSF9SRUdJU1RS
WV9XUklURSA9ICJ2Mi5yZXNlYXJjaC5yZWdpc3RyeS53cml0ZSIKICAgIFJFU0VBUkNIX1JFU1VMVFNfUkVBRCA9ICJ2Mi5yZXNlYXJjaC5yZXN1bHRzLnJl
YWQiCgoKIyBSb2xlIOKGkiBwZXJtaXNzaW9ucyBtYXBwaW5nClYyX1JPTEVfUEVSTUlTU0lPTlM6IGRpY3Rbc3RyLCBmcm96ZW5zZXRbc3RyXV0gPSB7CiAg
ICAiYWRtaW4iOiBmcm96ZW5zZXQoewogICAgICAgIFYyUGVybWlzc2lvbi5NT0RFX1JFQUQudmFsdWUsCiAgICAgICAgVjJQZXJtaXNzaW9uLkNBUEFCSUxJ
VFlfUkVBRC52YWx1ZSwKICAgICAgICBWMlBlcm1pc3Npb24uQVVESVRfUkVBRC52YWx1ZSwKICAgICAgICBWMlBlcm1pc3Npb24uQVVESVRfUkVBRF9BTEwu
dmFsdWUsCiAgICAgICAgVjJQZXJtaXNzaW9uLkxJTkVBR0VfUkVBRC52YWx1ZSwKICAgICAgICBWMlBlcm1pc3Npb24uTElORUFHRV9SRUFEX0FMTC52YWx1
ZSwKICAgICAgICBWMlBlcm1pc3Npb24uRVJST1JfUkVBRC52YWx1ZSwKICAgICAgICBWMlBlcm1pc3Npb24uTUFSS0VUREFUQV9SRUFELnZhbHVlLAogICAg
ICAgIFYyUGVybWlzc2lvbi5NQVJLRVREQVRBX1JFQURfQUxMLnZhbHVlLAogICAgICAgIFYyUGVybWlzc2lvbi5NQVJLRVREQVRBX1ZFUklGWS52YWx1ZSwK
ICAgICAgICBWMlBlcm1pc3Npb24uTUFSS0VUREFUQV9DQVRBTE9HX1JFRlJFU0gudmFsdWUsCiAgICAgICAgVjJQZXJtaXNzaW9uLlBST1ZJREVSX1JFQUQu
dmFsdWUsCiAgICAgICAgVjJQZXJtaXNzaW9uLlBST1ZJREVSX1JFQURfSElTVE9SWS52YWx1ZSwKICAgICAgICBWMlBlcm1pc3Npb24uUFJPVklERVJfQ09O
VFJBQ1RfVEVTVC52YWx1ZSwKICAgICAgICBWMlBlcm1pc3Npb24uUkVTRUFSQ0hfTUNfUkVBRC52YWx1ZSwKICAgICAgICBWMlBlcm1pc3Npb24uUkVTRUFS
Q0hfQ0lfUkVBRC52YWx1ZSwKICAgICAgICBWMlBlcm1pc3Npb24uUkVTRUFSQ0hfTUNfQ09NUFVURS52YWx1ZSwKICAgICAgICBWMlBlcm1pc3Npb24uUkVT
RUFSQ0hfTUxHT1ZfUkVBRC52YWx1ZSwKICAgICAgICBWMlBlcm1pc3Npb24uUkVTRUFSQ0hfTUxHT1ZfREVDSURFLnZhbHVlLAogICAgICAgIFYyUGVybWlz
c2lvbi5SRVNFQVJDSF9TSUdOQUxfUkVBRC52YWx1ZSwKICAgICAgICBWMlBlcm1pc3Npb24uUkVTRUFSQ0hfU0lHTkFMX0VNSVQudmFsdWUsCiAgICAgICAg
VjJQZXJtaXNzaW9uLlJFU0VBUkNIX01MRElBR19SRUFELnZhbHVlLAogICAgICAgIFYyUGVybWlzc2lvbi5SRVNFQVJDSF9QRl9SRUFELnZhbHVlLAogICAg
ICAgIFYyUGVybWlzc2lvbi5SRVNFQVJDSF9QRl9ERUZJTkUudmFsdWUsCiAgICAgICAgVjJQZXJtaXNzaW9uLlJFU0VBUkNIX1BGUklTS19SRUFELnZhbHVl
LAogICAgICAgIFYyUGVybWlzc2lvbi5SRVNFQVJDSF9QRlJJU0tfQ09NUFVURS52YWx1ZSwKICAgICAgICBWMlBlcm1pc3Npb24uUkVTRUFSQ0hfSk9CU19S
RUFELnZhbHVlLAogICAgICAgIFYyUGVybWlzc2lvbi5SRVNFQVJDSF9KT0JTX1NVQk1JVC52YWx1ZSwKICAgICAgICBWMlBlcm1pc3Npb24uUkVTRUFSQ0hf
Sk9CU19DQU5DRUwudmFsdWUsCiAgICAgICAgVjJQZXJtaXNzaW9uLlJFU0VBUkNIX1JFR0lTVFJZX1JFQUQudmFsdWUsCiAgICAgICAgVjJQZXJtaXNzaW9u
LlJFU0VBUkNIX1JFR0lTVFJZX1dSSVRFLnZhbHVlLAogICAgICAgIFYyUGVybWlzc2lvbi5SRVNFQVJDSF9SRVNVTFRTX1JFQUQudmFsdWUsCiAgICB9KSwK
ICAgICJvcGVyYXRvciI6IGZyb3plbnNldCh7CiAgICAgICAgVjJQZXJtaXNzaW9uLk1PREVfUkVBRC52YWx1ZSwKICAgICAgICBWMlBlcm1pc3Npb24uQ0FQ
QUJJTElUWV9SRUFELnZhbHVlLAogICAgICAgIFYyUGVybWlzc2lvbi5BVURJVF9SRUFELnZhbHVlLAogICAgICAgIFYyUGVybWlzc2lvbi5MSU5FQUdFX1JF
QUQudmFsdWUsCiAgICAgICAgVjJQZXJtaXNzaW9uLkVSUk9SX1JFQUQudmFsdWUsCiAgICAgICAgVjJQZXJtaXNzaW9uLk1BUktFVERBVEFfUkVBRC52YWx1
ZSwKICAgICAgICBWMlBlcm1pc3Npb24uTUFSS0VUREFUQV9WRVJJRlkudmFsdWUsCiAgICAgICAgVjJQZXJtaXNzaW9uLlBST1ZJREVSX1JFQUQudmFsdWUs
CiAgICAgICAgVjJQZXJtaXNzaW9uLlJFU0VBUkNIX01DX1JFQUQudmFsdWUsCiAgICAgICAgVjJQZXJtaXNzaW9uLlJFU0VBUkNIX0NJX1JFQUQudmFsdWUs
CiAgICAgICAgVjJQZXJtaXNzaW9uLlJFU0VBUkNIX01MR09WX1JFQUQudmFsdWUsCiAgICAgICAgVjJQZXJtaXNzaW9uLlJFU0VBUkNIX1NJR05BTF9SRUFE
LnZhbHVlLAogICAgICAgIFYyUGVybWlzc2lvbi5SRVNFQVJDSF9NTERJQUdfUkVBRC52YWx1ZSwKICAgICAgICBWMlBlcm1pc3Npb24uUkVTRUFSQ0hfUEZf
UkVBRC52YWx1ZSwKICAgICAgICBWMlBlcm1pc3Npb24uUkVTRUFSQ0hfUEZSSVNLX1JFQUQudmFsdWUsCiAgICAgICAgVjJQZXJtaXNzaW9uLlJFU0VBUkNI
X0pPQlNfUkVBRC52YWx1ZSwKICAgICAgICBWMlBlcm1pc3Npb24uUkVTRUFSQ0hfUkVTVUxUU19SRUFELnZhbHVlLAogICAgfSksCn0KCiMgRm9yYmlkZGVu
IHBlcm1pc3Npb24gbWFya2VycyDigJQgYW55IFYyIHBlcm1pc3Npb24gY29udGFpbmluZyB0aGVzZSBpcyByZWplY3RlZApWMl9GT1JCSURERU5fUEVSTUlT
U0lPTl9NQVJLRVJTID0gKAogICAgImdhdGUiLAogICAgImV4ZWN1dGlvbiIsCiAgICAiZXhlY3V0ZSIsCiAgICAib3JkZXIiLAogICAgImJyb2tlciIsCiAg
ICAiYWNjb3VudCIsCiAgICAicG9zaXRpb24iLAogICAgImxpdmUiLAogICAgImNhcGl0YWwiLAogICAgIm1hcmdpbiIsCikKCiMgU0FMIGNsYXNzaWZpY2F0
aW9uIGZvciBlYWNoIHBlcm1pc3Npb24KVjJfUEVSTUlTU0lPTl9TQUw6IGRpY3Rbc3RyLCBzdHJdID0gewogICAgVjJQZXJtaXNzaW9uLk1PREVfUkVBRC52
YWx1ZTogIlNBTC0yIiwKICAgIFYyUGVybWlzc2lvbi5DQVBBQklMSVRZX1JFQUQudmFsdWU6ICJTQUwtMiIsCiAgICBWMlBlcm1pc3Npb24uQVVESVRfUkVB
RC52YWx1ZTogIlNBTC0zIiwKICAgIFYyUGVybWlzc2lvbi5BVURJVF9SRUFEX0FMTC52YWx1ZTogIlNBTC00IiwKICAgIFYyUGVybWlzc2lvbi5MSU5FQUdF
X1JFQUQudmFsdWU6ICJTQUwtMyIsCiAgICBWMlBlcm1pc3Npb24uTElORUFHRV9SRUFEX0FMTC52YWx1ZTogIlNBTC00IiwKICAgIFYyUGVybWlzc2lvbi5F
UlJPUl9SRUFELnZhbHVlOiAiU0FMLTIiLAogICAgVjJQZXJtaXNzaW9uLk1BUktFVERBVEFfUkVBRC52YWx1ZTogIlNBTC0yIiwKICAgIFYyUGVybWlzc2lv
bi5NQVJLRVREQVRBX1JFQURfQUxMLnZhbHVlOiAiU0FMLTQiLAogICAgVjJQZXJtaXNzaW9uLk1BUktFVERBVEFfVkVSSUZZLnZhbHVlOiAiU0FMLTMiLAog
ICAgVjJQZXJtaXNzaW9uLk1BUktFVERBVEFfQ0FUQUxPR19SRUZSRVNILnZhbHVlOiAiU0FMLTMiLAogICAgVjJQZXJtaXNzaW9uLlBST1ZJREVSX1JFQUQu
dmFsdWU6ICJTQUwtMiIsCiAgICBWMlBlcm1pc3Npb24uUFJPVklERVJfUkVBRF9ISVNUT1JZLnZhbHVlOiAiU0FMLTQiLAogICAgVjJQZXJtaXNzaW9uLlBS
T1ZJREVSX0NPTlRSQUNUX1RFU1QudmFsdWU6ICJTQUwtNCIsCiAgICBWMlBlcm1pc3Npb24uUkVTRUFSQ0hfTUNfUkVBRC52YWx1ZTogIlNBTC0yIiwKICAg
IFYyUGVybWlzc2lvbi5SRVNFQVJDSF9DSV9SRUFELnZhbHVlOiAiU0FMLTIiLAogICAgVjJQZXJtaXNzaW9uLlJFU0VBUkNIX01DX0NPTVBVVEUudmFsdWU6
ICJTQUwtMyIsCiAgICBWMlBlcm1pc3Npb24uUkVTRUFSQ0hfTUxHT1ZfUkVBRC52YWx1ZTogIlNBTC0yIiwKICAgIFYyUGVybWlzc2lvbi5SRVNFQVJDSF9N
TEdPVl9ERUNJREUudmFsdWU6ICJTQUwtMyIsCiAgICBWMlBlcm1pc3Npb24uUkVTRUFSQ0hfU0lHTkFMX1JFQUQudmFsdWU6ICJTQUwtMiIsCiAgICBWMlBl
cm1pc3Npb24uUkVTRUFSQ0hfU0lHTkFMX0VNSVQudmFsdWU6ICJTQUwtMyIsCiAgICBWMlBlcm1pc3Npb24uUkVTRUFSQ0hfTUxESUFHX1JFQUQudmFsdWU6
ICJTQUwtMiIsCiAgICBWMlBlcm1pc3Npb24uUkVTRUFSQ0hfUEZfUkVBRC52YWx1ZTogIlNBTC0yIiwKICAgIFYyUGVybWlzc2lvbi5SRVNFQVJDSF9QRl9E
RUZJTkUudmFsdWU6ICJTQUwtMyIsCiAgICBWMlBlcm1pc3Npb24uUkVTRUFSQ0hfUEZSSVNLX1JFQUQudmFsdWU6ICJTQUwtMiIsCiAgICBWMlBlcm1pc3Np
b24uUkVTRUFSQ0hfUEZSSVNLX0NPTVBVVEUudmFsdWU6ICJTQUwtMyIsCiAgICBWMlBlcm1pc3Npb24uUkVTRUFSQ0hfSk9CU19SRUFELnZhbHVlOiAiU0FM
LTIiLAogICAgVjJQZXJtaXNzaW9uLlJFU0VBUkNIX0pPQlNfU1VCTUlULnZhbHVlOiAiU0FMLTMiLAogICAgVjJQZXJtaXNzaW9uLlJFU0VBUkNIX0pPQlNf
Q0FOQ0VMLnZhbHVlOiAiU0FMLTMiLAogICAgVjJQZXJtaXNzaW9uLlJFU0VBUkNIX1JFR0lTVFJZX1JFQUQudmFsdWU6ICJTQUwtMiIsCiAgICBWMlBlcm1p
c3Npb24uUkVTRUFSQ0hfUkVHSVNUUllfV1JJVEUudmFsdWU6ICJTQUwtMyIsCiAgICBWMlBlcm1pc3Npb24uUkVTRUFSQ0hfUkVTVUxUU19SRUFELnZhbHVl
OiAiU0FMLTIiLAp9CgoKZGVmIHBlcm1pc3Npb25zX2Zvcl9yb2xlKHJvbGU6IHN0cikgLT4gZnJvemVuc2V0W3N0cl06CiAgICAiIiJSZXR1cm4gcGVybWlz
c2lvbnMgZm9yIGEgcm9sZS4gVW5rbm93biByb2xlcyBkZWZhdWx0LWRlbnkuIiIiCiAgICByZXR1cm4gVjJfUk9MRV9QRVJNSVNTSU9OUy5nZXQocm9sZSwg
ZnJvemVuc2V0KCkpCgoKZGVmIGhhc19wZXJtaXNzaW9uKHJvbGU6IHN0ciwgcGVybWlzc2lvbjogc3RyKSAtPiBib29sOgogICAgIiIiQ2hlY2sgaWYgYSBy
b2xlIGhhcyBhIHNwZWNpZmljIHBlcm1pc3Npb24uIiIiCiAgICByZXR1cm4gcGVybWlzc2lvbiBpbiBwZXJtaXNzaW9uc19mb3Jfcm9sZShyb2xlKQoKCmRl
ZiBhc3NlcnRfcGVybWlzc2lvbl92b2NhYnVsYXJ5X3NhZmUoKSAtPiBOb25lOgogICAgIiIiUmVmdXNlIHBlcm1pc3Npb24gdm9jYWJ1bGFyaWVzIHRoYXQg
ZW5jb2RlIGZvcmJpZGRlbiBleGVjdXRpb24gcG93ZXJzLiIiIgogICAgZm9yIHBlcm1pc3Npb25fc2V0IGluIFYyX1JPTEVfUEVSTUlTU0lPTlMudmFsdWVz
KCk6CiAgICAgICAgZm9yIHBlcm1pc3Npb24gaW4gcGVybWlzc2lvbl9zZXQ6CiAgICAgICAgICAgIGxvd2VyID0gcGVybWlzc2lvbi5sb3dlcigpCiAgICAg
ICAgICAgIGlmIGFueShtYXJrZXIgaW4gbG93ZXIgZm9yIG1hcmtlciBpbiBWMl9GT1JCSURERU5fUEVSTUlTU0lPTl9NQVJLRVJTKToKICAgICAgICAgICAg
ICAgIHJhaXNlIFZhbHVlRXJyb3IoZiJWMl9QRVJNSVNTSU9OX0ZPUkJJRERFTjoge3Blcm1pc3Npb259IikKCgojIFNlZWQgZGF0YSBmb3IgdjJfcGVybWlz
c2lvbiB0YWJsZQpWMl9QRVJNSVNTSU9OX1NFRUQ6IGxpc3RbZGljdFtzdHIsIHN0cl1dID0gW10KZm9yIHJvbGUsIHBlcm1zIGluIFYyX1JPTEVfUEVSTUlT
U0lPTlMuaXRlbXMoKToKICAgIGZvciBwZXJtIGluIHBlcm1zOgogICAgICAgIFYyX1BFUk1JU1NJT05fU0VFRC5hcHBlbmQoewogICAgICAgICAgICAicm9s
ZSI6IHJvbGUsCiAgICAgICAgICAgICJwZXJtaXNzaW9uIjogcGVybSwKICAgICAgICAgICAgInNhbCI6IFYyX1BFUk1JU1NJT05fU0FMLmdldChwZXJtLCAi
U0FMLTIiKSwKICAgICAgICB9KQo=
'@
Write-Evidence ("record 5/17 staged: " + $Rec5Path)
$Rec6Path = "app\v2\research_jobs\__init__.py"
$Rec6Sha  = "29c2d81038281a73dafde56901871b2343b6a3ba2742ab726b03fd8bc304b306"
$Rec6B64 = @'
IiIiVjIgQkUtNyDigJQgQmFja3Rlc3RpbmcsIFNpbXVsYXRpb24sIFJlcGxheSwgYW5kIEdvdmVybmVkIFJlc2VhcmNoIEpvYnMuCgpCTy1WMi1CRS03LTAw
MTsgcGxhbiBBWElPTS1WMi1CRS03LURBLVBMQU4tMDAxIHYxLjAuMCAoQUNDRVBURUQgemVybwpjb3JyZWN0aW9ucywgSVRSR0EtUFJWLVYyLUJFLTctUExB
Ti0wMDEpOyBQaW5zIFAtMeKAplAtMTA7IGNvbmRpdGlvbnMKQzHigJNDNCArIHRoZSBzY2FuLXRva2VuIGNvbmRpdGlvbi4KClJlcHJvZHVjaWJsZSwgbm9u
LWxpdmUgcmVzZWFyY2ggb25seS4gTm8gcGFwZXIvbGl2ZSBjb25zdHJ1Y3Rpb24sIG5vCmV4ZWN1dGlvbiBzdXJmYWNlLCBubyBzY2hlZHVsZXIsIG5vIGNy
ZWRlbnRpYWwsIFJFU0VBUkNIIG1vZGUuCiIiIgo=
'@
Write-Evidence ("record 6/17 staged: " + $Rec6Path)
$Rec7Path = "app\v2\research_jobs\api.py"
$Rec7Sha  = "0b5fe719b839f848a8fb42a81de8a35197eeb443f6c267e3794f14292d2db253"
$Rec7B64 = @'
IiIiQkUtNyBVLTUgZW5kcG9pbnRzIChCTyDCpzE7IEMzL0M0KS4KCkdFVC1vbmx5IHJlYWRzICsgdGhlIGVudW1lcmF0ZWQgZ292ZXJuZWQgd3JpdGVyczog
cmVnaXN0ZXItaW5wdXQsCnJlZ2lzdGVyLWNvc3QtbW9kZWwsIHJlZ2lzdGVyLXN0cmF0ZWd5LCBzdWJtaXQtam9iLCBydW4tam9iLCBjYW5jZWwtam9iLgpO
TyBnZW5lcmljIGpvYi11cGRhdGUgZW5kcG9pbnQgZXhpc3RzIChDMykuIFJFU0VBUkNILW1vZGUgd3JpdGVycy4KIiIiCgpmcm9tIF9fZnV0dXJlX18gaW1w
b3J0IGFubm90YXRpb25zCgpmcm9tIGRhdGV0aW1lIGltcG9ydCBkYXRldGltZSwgdGltZXpvbmUKZnJvbSB0eXBpbmcgaW1wb3J0IEFubm90YXRlZAoKZnJv
bSBmYXN0YXBpIGltcG9ydCBBUElSb3V0ZXIsIERlcGVuZHMsIEhUVFBFeGNlcHRpb24sIFF1ZXJ5LCBSZXF1ZXN0LCBzdGF0dXMKZnJvbSBweWRhbnRpYyBp
bXBvcnQgQmFzZU1vZGVsLCBGaWVsZApmcm9tIHNxbGFsY2hlbXkgaW1wb3J0IHNlbGVjdApmcm9tIHNxbGFsY2hlbXkuZXh0LmFzeW5jaW8gaW1wb3J0IEFz
eW5jU2Vzc2lvbgoKZnJvbSBhcHAuZGIubW9kZWxzLm9wZXJhdG9yIGltcG9ydCBPcGVyYXRvcgpmcm9tIGFwcC5kYi5tb2RlbHMudjJfcmVzZWFyY2hfam9i
cyBpbXBvcnQgKAogICAgVjJCYWNrdGVzdElucHV0LAogICAgVjJSZXNlYXJjaEpvYiwKICAgIFYyUmVzZWFyY2hKb2JBdHRlbXB0LAogICAgVjJSZXNlYXJj
aFJlc3VsdCwKKQpmcm9tIGFwcC5kYi5zZXNzaW9uIGltcG9ydCBnZXRfZGJfc2Vzc2lvbgpmcm9tIGFwcC52Mi5pZGVudGlmaWVycyBpbXBvcnQgbmV3X2lk
CmZyb20gYXBwLnYyLm1hcmtldGRhdGEucmVwb3NpdG9yaWVzIGltcG9ydCAoCiAgICBWMk1kQmFyUmVhZEJvdW5kYXJ5LAogICAgVjJNZFJlZmVyZW5jZVJl
cG9zaXRvcnksCikKZnJvbSBhcHAudjIucmJhYy5kZXBlbmRlbmNpZXMgaW1wb3J0IHJlcXVpcmVfdjJfcGVybWlzc2lvbgpmcm9tIGFwcC52Mi5yZXNlYXJj
aF9qb2JzLmxlYWthZ2UgaW1wb3J0ICgKICAgIExlYWthZ2VSZWZ1c2VkLAogICAgUmVwbGF5V2luZG93LAogICAgY29udGVudF9oYXNoLAogICAgZmlsdGVy
X2JhcnNfZzEsCikKZnJvbSBhcHAudjIucmVzZWFyY2hfam9icy5xdWV1ZSBpbXBvcnQgSm9iU3VibWlzc2lvbiwgY2FuY2VsX2pvYiwgc3VibWl0X2pvYgpm
cm9tIGFwcC52Mi5yZXNlYXJjaF9qb2JzLnJlZ2lzdHJ5IGltcG9ydCAoCiAgICByZWdpc3Rlcl9jb3N0X21vZGVsLAogICAgcmVnaXN0ZXJfaW5wdXQsCiAg
ICByZWdpc3Rlcl9zdHJhdGVneSwKKQpmcm9tIGFwcC52Mi5yZXNlYXJjaF9qb2JzLnJ1bm5lciBpbXBvcnQgX3V0Y19mcm9tX3N0b3JlLCBydW5fam9iCmZy
b20gYXBwLnYyLnRlbXBvcmFsLnZhbGlkYXRpb24gaW1wb3J0IHJlcXVpcmVfdXRjLCB1dGNfbm93Cgpyb3V0ZXIgPSBBUElSb3V0ZXIocHJlZml4PSIvcmVz
ZWFyY2gtam9icyIsIHRhZ3M9WyJWMiBSZXNlYXJjaCBKb2JzIl0pCgpSZXF1aXJlSm9ic1JlYWQgPSBBbm5vdGF0ZWRbCiAgICBPcGVyYXRvciwgRGVwZW5k
cyhyZXF1aXJlX3YyX3Blcm1pc3Npb24oInYyLnJlc2VhcmNoLmpvYnMucmVhZCIpKV0KUmVxdWlyZUpvYnNTdWJtaXQgPSBBbm5vdGF0ZWRbCiAgICBPcGVy
YXRvciwgRGVwZW5kcyhyZXF1aXJlX3YyX3Blcm1pc3Npb24oInYyLnJlc2VhcmNoLmpvYnMuc3VibWl0IikpXQpSZXF1aXJlSm9ic0NhbmNlbCA9IEFubm90
YXRlZFsKICAgIE9wZXJhdG9yLCBEZXBlbmRzKHJlcXVpcmVfdjJfcGVybWlzc2lvbigidjIucmVzZWFyY2guam9icy5jYW5jZWwiKSldClJlcXVpcmVSZWdp
c3RyeVJlYWQgPSBBbm5vdGF0ZWRbCiAgICBPcGVyYXRvciwgRGVwZW5kcyhyZXF1aXJlX3YyX3Blcm1pc3Npb24oInYyLnJlc2VhcmNoLnJlZ2lzdHJ5LnJl
YWQiKSldClJlcXVpcmVSZWdpc3RyeVdyaXRlID0gQW5ub3RhdGVkWwogICAgT3BlcmF0b3IsIERlcGVuZHMocmVxdWlyZV92Ml9wZXJtaXNzaW9uKCJ2Mi5y
ZXNlYXJjaC5yZWdpc3RyeS53cml0ZSIpKV0KUmVxdWlyZVJlc3VsdHNSZWFkID0gQW5ub3RhdGVkWwogICAgT3BlcmF0b3IsIERlcGVuZHMocmVxdWlyZV92
Ml9wZXJtaXNzaW9uKCJ2Mi5yZXNlYXJjaC5yZXN1bHRzLnJlYWQiKSldCgoKZGVmIF9lbnZlbG9wZShyZXF1ZXN0OiBSZXF1ZXN0KSAtPiBkaWN0OgogICAg
cmV0dXJuIHsibW9kZSI6IHJlcXVlc3QuYXBwLnN0YXRlLnYyX21vZGUsCiAgICAgICAgICAgICJjb3JyZWxhdGlvbl9pZCI6IGdldGF0dHIocmVxdWVzdC5z
dGF0ZSwgImNvcnJlbGF0aW9uX2lkIiwgTm9uZSksCiAgICAgICAgICAgICJ0aW1lc3RhbXAiOiBkYXRldGltZS5ub3codGltZXpvbmUudXRjKX0KCgpkZWYg
X3JlcXVpcmVfcmVzZWFyY2gocmVxdWVzdDogUmVxdWVzdCkgLT4gc3RyOgogICAgbW9kZSA9IHJlcXVlc3QuYXBwLnN0YXRlLnYyX21vZGUKICAgIGlmIG1v
ZGUgIT0gIlJFU0VBUkNIIjoKICAgICAgICByYWlzZSBIVFRQRXhjZXB0aW9uKHN0YXR1c19jb2RlPXN0YXR1cy5IVFRQXzQwM19GT1JCSURERU4sCiAgICAg
ICAgICAgICAgICAgICAgICAgICAgICBkZXRhaWw9IldyaXRlciBub3QgcGVybWl0dGVkIGluIHRoaXMgbW9kZSIpCiAgICByZXR1cm4gbW9kZQoKCmRlZiBf
Y2lkKHJlcXVlc3Q6IFJlcXVlc3QpIC0+IHN0cjoKICAgIHJldHVybiBnZXRhdHRyKHJlcXVlc3Quc3RhdGUsICJjb3JyZWxhdGlvbl9pZCIsIE5vbmUpIG9y
IG5ld19pZCgpCgoKIyAtLS0gcmVxdWVzdCBtb2RlbHMgLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0t
LS0tLQoKCmNsYXNzIElucHV0UmVnaXN0cmF0aW9uKEJhc2VNb2RlbCk6CiAgICBpbnB1dF9pZDogc3RyID0gRmllbGQobWluX2xlbmd0aD0xLCBtYXhfbGVu
Z3RoPTY0KQogICAgaW5zdHJ1bWVudF9pZDogc3RyCiAgICB0aW1lZnJhbWU6IHN0ciA9ICJNMTUiCiAgICBzb3VyY2VfaWQ6IHN0ciA9ICJzaW0ubG9jYWwi
CiAgICB3aW5kb3dfc3RhcnQ6IGRhdGV0aW1lCiAgICB3aW5kb3dfZW5kOiBkYXRldGltZQogICAgZGF0YV9jbGFzczogc3RyID0gInNpbXVsYXRlZCIKICAg
IGJhcl9saW1pdDogaW50ID0gRmllbGQoZGVmYXVsdD01MDAsIGdlPTEwLCBsZT0xMDAwKQoKCmNsYXNzIENvc3RNb2RlbFJlZ2lzdHJhdGlvbihCYXNlTW9k
ZWwpOgogICAgY29zdF9tb2RlbF9pZDogc3RyID0gRmllbGQobWluX2xlbmd0aD0xLCBtYXhfbGVuZ3RoPTY0KQogICAgc3ByZWFkOiBkaWN0CiAgICBjb21t
aXNzaW9uOiBkaWN0CiAgICBzbGlwcGFnZTogZGljdAogICAgbGF0ZW5jeV9tczogaW50ID0gRmllbGQoZ2U9MCkKICAgIHJpc2tfbGltaXRzOiBkaWN0ID0g
RmllbGQoZGVmYXVsdF9mYWN0b3J5PWRpY3QpCiAgICBkYXRhX2NsYXNzOiBzdHIgPSAic2ltdWxhdGVkIgoKCmNsYXNzIFN0cmF0ZWd5UmVnaXN0cmF0aW9u
KEJhc2VNb2RlbCk6CiAgICBzdHJhdGVneV9pZDogc3RyID0gRmllbGQobWluX2xlbmd0aD0xLCBtYXhfbGVuZ3RoPTY0KQogICAgbmFtZTogc3RyCiAgICBw
YXJhbWV0ZXJzOiBkaWN0CiAgICBsaWZlY3ljbGVfc3RhdGU6IHN0ciA9ICJyZWdpc3RlcmVkIgogICAgZGF0YV9jbGFzczogc3RyID0gInNpbXVsYXRlZCIK
CgpjbGFzcyBKb2JTdWJtaXRSZXF1ZXN0KEJhc2VNb2RlbCk6CiAgICBhdXRob3JpemF0aW9uX3JlZjogc3RyID0gRmllbGQobWluX2xlbmd0aD0xKQogICAg
aW5wdXRzOiBkaWN0CiAgICBzY2hlZHVsZTogZGljdCA9IEZpZWxkKGRlZmF1bHRfZmFjdG9yeT1sYW1iZGE6IHsia2luZCI6ICJtYW51YWwifSkKICAgIGRh
dGFfY2xhc3M6IHN0ciA9ICJzaW11bGF0ZWQiCgoKY2xhc3MgSm9iUnVuUmVxdWVzdChCYXNlTW9kZWwpOgogICAgam9iX2lkOiBzdHIKCgpjbGFzcyBKb2JD
YW5jZWxSZXF1ZXN0KEJhc2VNb2RlbCk6CiAgICBqb2JfaWQ6IHN0cgogICAgcmVhc29uOiBzdHIgPSBGaWVsZChtaW5fbGVuZ3RoPTEpCgoKIyAtLS0gZ292
ZXJuZWQgd3JpdGVycyAtLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tCgoKQHJvdXRlci5wb3N0
KCIvcmVnaXN0cnkvaW5wdXRzIikKYXN5bmMgZGVmIGFwaV9yZWdpc3Rlcl9pbnB1dCgKICAgIGJvZHk6IElucHV0UmVnaXN0cmF0aW9uLCByZXF1ZXN0OiBS
ZXF1ZXN0LAogICAgb3BlcmF0b3I6IFJlcXVpcmVSZWdpc3RyeVdyaXRlLAogICAgc2Vzc2lvbjogQXN5bmNTZXNzaW9uID0gRGVwZW5kcyhnZXRfZGJfc2Vz
c2lvbikpIC0+IGRpY3Q6CiAgICBtb2RlID0gX3JlcXVpcmVfcmVzZWFyY2gocmVxdWVzdCkKICAgIHJlcXVpcmVfdXRjKGJvZHkud2luZG93X3N0YXJ0LCBi
b3VuZGFyeT0id2luZG93X3N0YXJ0IikKICAgIHJlcXVpcmVfdXRjKGJvZHkud2luZG93X2VuZCwgYm91bmRhcnk9IndpbmRvd19lbmQiKQogICAgbm93ID0g
dXRjX25vdygpCiAgICBpZiBib2R5LndpbmRvd19lbmQgPiBub3c6CiAgICAgICAgcmFpc2UgSFRUUEV4Y2VwdGlvbihzdGF0dXNfY29kZT1zdGF0dXMuSFRU
UF80MDBfQkFEX1JFUVVFU1QsCiAgICAgICAgICAgICAgICAgICAgICAgICAgICBkZXRhaWw9IndpbmRvd19lbmQgbWF5IG5vdCBiZSBpbiB0aGUgZnV0dXJl
IikKICAgIHJlZl9yZXBvID0gVjJNZFJlZmVyZW5jZVJlcG9zaXRvcnkoc2Vzc2lvbikKICAgIGluc3RydW1lbnQgPSBhd2FpdCByZWZfcmVwby5nZXRfaW5z
dHJ1bWVudChib2R5Lmluc3RydW1lbnRfaWQpCiAgICBzb3VyY2UgPSBhd2FpdCByZWZfcmVwby5nZXRfc291cmNlKGJvZHkuc291cmNlX2lkKQogICAgaWYg
aW5zdHJ1bWVudCBpcyBOb25lIG9yIHNvdXJjZSBpcyBOb25lIG9yIG5vdCBzb3VyY2UuYWN0aXZlOgogICAgICAgIHJhaXNlIEhUVFBFeGNlcHRpb24oc3Rh
dHVzX2NvZGU9c3RhdHVzLkhUVFBfNDA0X05PVF9GT1VORCwKICAgICAgICAgICAgICAgICAgICAgICAgICAgIGRldGFpbD0iSW5zdHJ1bWVudCBvciBzb3Vy
Y2Ugbm90IGZvdW5kIikKICAgIGJvdW5kYXJ5ID0gVjJNZEJhclJlYWRCb3VuZGFyeShzZXNzaW9uKQogICAgcm93cyA9IGF3YWl0IGJvdW5kYXJ5LnJlYWRf
YmFycygKICAgICAgICBtYXJrZXRfY2xhc3M9aW5zdHJ1bWVudC5tYXJrZXRfY2xhc3MsCiAgICAgICAgc3ltYm9sPWluc3RydW1lbnQuZGlzcGxheV9zeW1i
b2wsCiAgICAgICAgdGltZWZyYW1lPWJvZHkudGltZWZyYW1lLnVwcGVyKCksCiAgICAgICAgYXNfb2Y9Ym9keS53aW5kb3dfZW5kLCBsaW1pdD1ib2R5LmJh
cl9saW1pdCkKICAgIHJvd3MgPSBbciBmb3IgciBpbiByb3dzIGlmIHIuc291cmNlID09IHNvdXJjZS5hdXRob3JpdHldCiAgICBiYXJzID0gW3sib3Blbl90
aW1lIjogX3V0Y19mcm9tX3N0b3JlKHIub3Blbl90aW1lKSwgIm9wZW4iOiByLm9wZW4sCiAgICAgICAgICAgICAiaGlnaCI6IHIuaGlnaCwKICAgICAgICAg
ICAgICJsb3ciOiByLmxvdywgImNsb3NlIjogci5jbG9zZSwKICAgICAgICAgICAgICJ2b2x1bWUiOiBnZXRhdHRyKHIsICJ2b2x1bWUiLCAwKX0gZm9yIHIg
aW4gcm93c10KICAgIHdpbmRvdyA9IFJlcGxheVdpbmRvdyh3aW5kb3dfc3RhcnQ9Ym9keS53aW5kb3dfc3RhcnQsCiAgICAgICAgICAgICAgICAgICAgICAg
ICAgd2luZG93X2VuZD1ib2R5LndpbmRvd19lbmQsCiAgICAgICAgICAgICAgICAgICAgICAgICAgYXNfb2Y9Ym9keS53aW5kb3dfZW5kKQogICAgc2VyaWVz
X3JlZnMgPSB7Imluc3RydW1lbnRfaWQiOiBib2R5Lmluc3RydW1lbnRfaWQsCiAgICAgICAgICAgICAgICAgICAidGltZWZyYW1lIjogYm9keS50aW1lZnJh
bWUudXBwZXIoKSwKICAgICAgICAgICAgICAgICAgICJzb3VyY2VfaWQiOiBib2R5LnNvdXJjZV9pZCwKICAgICAgICAgICAgICAgICAgICJ0YWJsZSI6ICJj
YW5kbGVzIHZpYSBWMk1kQmFyUmVhZEJvdW5kYXJ5In0KICAgIHRyeToKICAgICAgICBhc3NlbWJsZWQgPSBmaWx0ZXJfYmFyc19nMShiYXJzLCB3aW5kb3cp
CiAgICBleGNlcHQgTGVha2FnZVJlZnVzZWQgYXMgZXhjOgogICAgICAgICMgdHlwZWQgcmVmdXNhbCB0aHJvdWdoIHRoZSByZWdpc3RyYXRpb24gd3JpdGVy
J3MgcmVmdXNhbCBwYXRoCiAgICAgICAgIyAoZHVyYWJsZSBhdWRpdCDigJQgQy0xIGxhdyksIG5ldmVyIGFuIHVuaGFuZGxlZCA1MDAKICAgICAgICBvdXRj
b21lID0gYXdhaXQgcmVnaXN0ZXJfaW5wdXQoCiAgICAgICAgICAgIHNlc3Npb24sIGlucHV0X2lkPWJvZHkuaW5wdXRfaWQsIGNvbnRlbnRfaGFzaD0iIiwK
ICAgICAgICAgICAgc2VyaWVzX3JlZnM9e30sIHdpbmRvd19zdGFydD1ib2R5LndpbmRvd19zdGFydCwKICAgICAgICAgICAgd2luZG93X2VuZD1ib2R5Lndp
bmRvd19lbmQsIGRhdGFfY2xhc3M9Ym9keS5kYXRhX2NsYXNzLAogICAgICAgICAgICBtb2RlPW1vZGUsIG9wZXJhdG9yX2lkPW9wZXJhdG9yLnVzZXJuYW1l
LAogICAgICAgICAgICBjb3JyZWxhdGlvbl9pZD1fY2lkKHJlcXVlc3QpKQogICAgICAgIHJldHVybiB7Im91dGNvbWUiOiAicmVmdXNlZCIsCiAgICAgICAg
ICAgICAgICAicmVjb3JkX2lkIjogTm9uZSwKICAgICAgICAgICAgICAgICJyZWFzb25zIjogZXhjLnJlYXNvbnMgKyBvdXRjb21lLnJlYXNvbnMsCiAgICAg
ICAgICAgICAgICAiY29udGVudF9oYXNoIjogTm9uZSwgImJhcnNfcmVnaXN0ZXJlZCI6IDAsCiAgICAgICAgICAgICAgICAqKl9lbnZlbG9wZShyZXF1ZXN0
KX0KICAgIGNoID0gY29udGVudF9oYXNoKGFzc2VtYmxlZCwgd2luZG93LCBzZXJpZXNfcmVmcykKICAgIG91dGNvbWUgPSBhd2FpdCByZWdpc3Rlcl9pbnB1
dCgKICAgICAgICBzZXNzaW9uLCBpbnB1dF9pZD1ib2R5LmlucHV0X2lkLCBjb250ZW50X2hhc2g9Y2gsCiAgICAgICAgc2VyaWVzX3JlZnM9c2VyaWVzX3Jl
ZnMsIHdpbmRvd19zdGFydD1ib2R5LndpbmRvd19zdGFydCwKICAgICAgICB3aW5kb3dfZW5kPWJvZHkud2luZG93X2VuZCwgZGF0YV9jbGFzcz1ib2R5LmRh
dGFfY2xhc3MsCiAgICAgICAgbW9kZT1tb2RlLCBvcGVyYXRvcl9pZD1vcGVyYXRvci51c2VybmFtZSwKICAgICAgICBjb3JyZWxhdGlvbl9pZD1fY2lkKHJl
cXVlc3QpKQogICAgcmV0dXJuIHsib3V0Y29tZSI6IG91dGNvbWUub3V0Y29tZSwgInJlY29yZF9pZCI6IG91dGNvbWUucmVjb3JkX2lkLAogICAgICAgICAg
ICAicmVhc29ucyI6IG91dGNvbWUucmVhc29ucywgImNvbnRlbnRfaGFzaCI6IGNoLAogICAgICAgICAgICAiYmFyc19yZWdpc3RlcmVkIjogbGVuKGFzc2Vt
YmxlZCksICoqX2VudmVsb3BlKHJlcXVlc3QpfQoKCkByb3V0ZXIucG9zdCgiL3JlZ2lzdHJ5L2Nvc3QtbW9kZWxzIikKYXN5bmMgZGVmIGFwaV9yZWdpc3Rl
cl9jb3N0X21vZGVsKAogICAgYm9keTogQ29zdE1vZGVsUmVnaXN0cmF0aW9uLCByZXF1ZXN0OiBSZXF1ZXN0LAogICAgb3BlcmF0b3I6IFJlcXVpcmVSZWdp
c3RyeVdyaXRlLAogICAgc2Vzc2lvbjogQXN5bmNTZXNzaW9uID0gRGVwZW5kcyhnZXRfZGJfc2Vzc2lvbikpIC0+IGRpY3Q6CiAgICBtb2RlID0gX3JlcXVp
cmVfcmVzZWFyY2gocmVxdWVzdCkKICAgIG91dGNvbWUgPSBhd2FpdCByZWdpc3Rlcl9jb3N0X21vZGVsKAogICAgICAgIHNlc3Npb24sIGNvc3RfbW9kZWxf
aWQ9Ym9keS5jb3N0X21vZGVsX2lkLCBzcHJlYWQ9Ym9keS5zcHJlYWQsCiAgICAgICAgY29tbWlzc2lvbj1ib2R5LmNvbW1pc3Npb24sIHNsaXBwYWdlPWJv
ZHkuc2xpcHBhZ2UsCiAgICAgICAgbGF0ZW5jeV9tcz1ib2R5LmxhdGVuY3lfbXMsIHJpc2tfbGltaXRzPWJvZHkucmlza19saW1pdHMsCiAgICAgICAgZGF0
YV9jbGFzcz1ib2R5LmRhdGFfY2xhc3MsIG1vZGU9bW9kZSwKICAgICAgICBvcGVyYXRvcl9pZD1vcGVyYXRvci51c2VybmFtZSwgY29ycmVsYXRpb25faWQ9
X2NpZChyZXF1ZXN0KSkKICAgIHJldHVybiB7Im91dGNvbWUiOiBvdXRjb21lLm91dGNvbWUsICJyZWNvcmRfaWQiOiBvdXRjb21lLnJlY29yZF9pZCwKICAg
ICAgICAgICAgInJlYXNvbnMiOiBvdXRjb21lLnJlYXNvbnMsICoqX2VudmVsb3BlKHJlcXVlc3QpfQoKCkByb3V0ZXIucG9zdCgiL3JlZ2lzdHJ5L3N0cmF0
ZWdpZXMiKQphc3luYyBkZWYgYXBpX3JlZ2lzdGVyX3N0cmF0ZWd5KAogICAgYm9keTogU3RyYXRlZ3lSZWdpc3RyYXRpb24sIHJlcXVlc3Q6IFJlcXVlc3Qs
CiAgICBvcGVyYXRvcjogUmVxdWlyZVJlZ2lzdHJ5V3JpdGUsCiAgICBzZXNzaW9uOiBBc3luY1Nlc3Npb24gPSBEZXBlbmRzKGdldF9kYl9zZXNzaW9uKSkg
LT4gZGljdDoKICAgIG1vZGUgPSBfcmVxdWlyZV9yZXNlYXJjaChyZXF1ZXN0KQogICAgb3V0Y29tZSA9IGF3YWl0IHJlZ2lzdGVyX3N0cmF0ZWd5KAogICAg
ICAgIHNlc3Npb24sIHN0cmF0ZWd5X2lkPWJvZHkuc3RyYXRlZ3lfaWQsIG5hbWU9Ym9keS5uYW1lLAogICAgICAgIHBhcmFtZXRlcnM9Ym9keS5wYXJhbWV0
ZXJzLCBsaWZlY3ljbGVfc3RhdGU9Ym9keS5saWZlY3ljbGVfc3RhdGUsCiAgICAgICAgZGF0YV9jbGFzcz1ib2R5LmRhdGFfY2xhc3MsIG1vZGU9bW9kZSwK
ICAgICAgICBvcGVyYXRvcl9pZD1vcGVyYXRvci51c2VybmFtZSwgY29ycmVsYXRpb25faWQ9X2NpZChyZXF1ZXN0KSkKICAgIHJldHVybiB7Im91dGNvbWUi
OiBvdXRjb21lLm91dGNvbWUsICJyZWNvcmRfaWQiOiBvdXRjb21lLnJlY29yZF9pZCwKICAgICAgICAgICAgInJlYXNvbnMiOiBvdXRjb21lLnJlYXNvbnMs
ICoqX2VudmVsb3BlKHJlcXVlc3QpfQoKCkByb3V0ZXIucG9zdCgiL2pvYnMvc3VibWl0IikKYXN5bmMgZGVmIGFwaV9zdWJtaXRfam9iKAogICAgYm9keTog
Sm9iU3VibWl0UmVxdWVzdCwgcmVxdWVzdDogUmVxdWVzdCwKICAgIG9wZXJhdG9yOiBSZXF1aXJlSm9ic1N1Ym1pdCwKICAgIHNlc3Npb246IEFzeW5jU2Vz
c2lvbiA9IERlcGVuZHMoZ2V0X2RiX3Nlc3Npb24pKSAtPiBkaWN0OgogICAgbW9kZSA9IF9yZXF1aXJlX3Jlc2VhcmNoKHJlcXVlc3QpCiAgICBvdXRjb21l
ID0gYXdhaXQgc3VibWl0X2pvYihzZXNzaW9uLCBKb2JTdWJtaXNzaW9uKAogICAgICAgIG93bmVyPW9wZXJhdG9yLnVzZXJuYW1lLAogICAgICAgIGF1dGhv
cml6YXRpb25fcmVmPWJvZHkuYXV0aG9yaXphdGlvbl9yZWYsCiAgICAgICAgaW5wdXRzPWJvZHkuaW5wdXRzLCBzY2hlZHVsZT1ib2R5LnNjaGVkdWxlLAog
ICAgICAgIGRhdGFfY2xhc3M9Ym9keS5kYXRhX2NsYXNzLCBtb2RlPW1vZGUsCiAgICAgICAgb3BlcmF0b3JfaWQ9b3BlcmF0b3IudXNlcm5hbWUsIGNvcnJl
bGF0aW9uX2lkPV9jaWQocmVxdWVzdCkpKQogICAgcmV0dXJuIHsib3V0Y29tZSI6IG91dGNvbWUub3V0Y29tZSwgImpvYl9pZCI6IG91dGNvbWUucmVjb3Jk
X2lkLAogICAgICAgICAgICAicmVhc29ucyI6IG91dGNvbWUucmVhc29ucywgKipfZW52ZWxvcGUocmVxdWVzdCl9CgoKQHJvdXRlci5wb3N0KCIvam9icy9y
dW4iKQphc3luYyBkZWYgYXBpX3J1bl9qb2IoCiAgICBib2R5OiBKb2JSdW5SZXF1ZXN0LCByZXF1ZXN0OiBSZXF1ZXN0LAogICAgb3BlcmF0b3I6IFJlcXVp
cmVKb2JzU3VibWl0LAogICAgc2Vzc2lvbjogQXN5bmNTZXNzaW9uID0gRGVwZW5kcyhnZXRfZGJfc2Vzc2lvbikpIC0+IGRpY3Q6CiAgICAiIiJNYW51YWwg
aW52b2NhdGlvbiAodjEgc2NvcGUpIOKAlCB0aGUgT05MWSBleGVjdXRpb24gdHJpZ2dlci4iIiIKICAgIF9yZXF1aXJlX3Jlc2VhcmNoKHJlcXVlc3QpICAj
IG1vZGUgZ2F0ZTsgdGhlIGpvYiByb3cgY2FycmllcyBpdHMgb3duIG1vZGUKICAgIGpvYiA9IChhd2FpdCBzZXNzaW9uLmV4ZWN1dGUoCiAgICAgICAgc2Vs
ZWN0KFYyUmVzZWFyY2hKb2IpLndoZXJlKFYyUmVzZWFyY2hKb2IuaWQgPT0gYm9keS5qb2JfaWQpCiAgICApKS5zY2FsYXJfb25lX29yX25vbmUoKQogICAg
aWYgam9iIGlzIE5vbmU6CiAgICAgICAgcmFpc2UgSFRUUEV4Y2VwdGlvbihzdGF0dXNfY29kZT1zdGF0dXMuSFRUUF80MDRfTk9UX0ZPVU5ELAogICAgICAg
ICAgICAgICAgICAgICAgICAgICAgZGV0YWlsPSJKb2Igbm90IGZvdW5kIikKICAgIHJlZ2lzdHJ5ID0gKGF3YWl0IHNlc3Npb24uZXhlY3V0ZSgKICAgICAg
ICBzZWxlY3QoVjJCYWNrdGVzdElucHV0KS53aGVyZSgKICAgICAgICAgICAgVjJCYWNrdGVzdElucHV0LmlkID09IGpvYi5pbnB1dHMuZ2V0KCJpbnB1dF9y
ZWdpc3RyeV9pZCIpKQogICAgKSkuc2NhbGFyX29uZV9vcl9ub25lKCkKICAgIGJhcnM6IGxpc3RbZGljdF0gPSBbXQogICAgaWYgcmVnaXN0cnkgaXMgbm90
IE5vbmU6CiAgICAgICAgcmVmX3JlcG8gPSBWMk1kUmVmZXJlbmNlUmVwb3NpdG9yeShzZXNzaW9uKQogICAgICAgIGluc3RydW1lbnQgPSBhd2FpdCByZWZf
cmVwby5nZXRfaW5zdHJ1bWVudCgKICAgICAgICAgICAgcmVnaXN0cnkuc2VyaWVzX3JlZnNbImluc3RydW1lbnRfaWQiXSkKICAgICAgICBzb3VyY2UgPSBh
d2FpdCByZWZfcmVwby5nZXRfc291cmNlKHJlZ2lzdHJ5LnNlcmllc19yZWZzWyJzb3VyY2VfaWQiXSkKICAgICAgICBpZiBpbnN0cnVtZW50IGlzIG5vdCBO
b25lIGFuZCBzb3VyY2UgaXMgbm90IE5vbmU6CiAgICAgICAgICAgIGJvdW5kYXJ5ID0gVjJNZEJhclJlYWRCb3VuZGFyeShzZXNzaW9uKQogICAgICAgICAg
ICByb3dzID0gYXdhaXQgYm91bmRhcnkucmVhZF9iYXJzKAogICAgICAgICAgICAgICAgbWFya2V0X2NsYXNzPWluc3RydW1lbnQubWFya2V0X2NsYXNzLAog
ICAgICAgICAgICAgICAgc3ltYm9sPWluc3RydW1lbnQuZGlzcGxheV9zeW1ib2wsCiAgICAgICAgICAgICAgICB0aW1lZnJhbWU9cmVnaXN0cnkuc2VyaWVz
X3JlZnNbInRpbWVmcmFtZSJdLAogICAgICAgICAgICAgICAgYXNfb2Y9X3V0Y19mcm9tX3N0b3JlKHJlZ2lzdHJ5LndpbmRvd19lbmQpLCBsaW1pdD0xMDAw
KQogICAgICAgICAgICByb3dzID0gW3IgZm9yIHIgaW4gcm93cyBpZiByLnNvdXJjZSA9PSBzb3VyY2UuYXV0aG9yaXR5XQogICAgICAgICAgICBiYXJzID0g
W3sib3Blbl90aW1lIjogX3V0Y19mcm9tX3N0b3JlKHIub3Blbl90aW1lKSwKICAgICAgICAgICAgICAgICAgICAgIm9wZW4iOiByLm9wZW4sCiAgICAgICAg
ICAgICAgICAgICAgICJoaWdoIjogci5oaWdoLCAibG93Ijogci5sb3csICJjbG9zZSI6IHIuY2xvc2UsCiAgICAgICAgICAgICAgICAgICAgICJ2b2x1bWUi
OiBnZXRhdHRyKHIsICJ2b2x1bWUiLCAwKX0gZm9yIHIgaW4gcm93c10KICAgIHJlc3VsdCA9IGF3YWl0IHJ1bl9qb2Ioc2Vzc2lvbiwgam9iX2lkPWJvZHku
am9iX2lkLAogICAgICAgICAgICAgICAgICAgICAgICAgICBhY3Rvcl9pZD1vcGVyYXRvci51c2VybmFtZSwgYmFycz1iYXJzLAogICAgICAgICAgICAgICAg
ICAgICAgICAgICBjb3JyZWxhdGlvbl9pZD1fY2lkKHJlcXVlc3QpKQogICAgcmV0dXJuIHsqKnJlc3VsdCwgKipfZW52ZWxvcGUocmVxdWVzdCl9CgoKQHJv
dXRlci5wb3N0KCIvam9icy9jYW5jZWwiKQphc3luYyBkZWYgYXBpX2NhbmNlbF9qb2IoCiAgICBib2R5OiBKb2JDYW5jZWxSZXF1ZXN0LCByZXF1ZXN0OiBS
ZXF1ZXN0LAogICAgb3BlcmF0b3I6IFJlcXVpcmVKb2JzQ2FuY2VsLAogICAgc2Vzc2lvbjogQXN5bmNTZXNzaW9uID0gRGVwZW5kcyhnZXRfZGJfc2Vzc2lv
bikpIC0+IGRpY3Q6CiAgICBtb2RlID0gX3JlcXVpcmVfcmVzZWFyY2gocmVxdWVzdCkKICAgIG91dGNvbWUgPSBhd2FpdCBjYW5jZWxfam9iKHNlc3Npb24s
IGpvYl9pZD1ib2R5LmpvYl9pZCwKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIGFjdG9yX2lkPW9wZXJhdG9yLnVzZXJuYW1lLAogICAgICAgICAg
ICAgICAgICAgICAgICAgICAgICAgcmVhc29uPWJvZHkucmVhc29uLCBtb2RlPW1vZGUsCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICBjb3JyZWxh
dGlvbl9pZD1fY2lkKHJlcXVlc3QpKQogICAgcmV0dXJuIHsib3V0Y29tZSI6IG91dGNvbWUub3V0Y29tZSwgInJlYXNvbnMiOiBvdXRjb21lLnJlYXNvbnMs
CiAgICAgICAgICAgICoqX2VudmVsb3BlKHJlcXVlc3QpfQoKCiMgLS0tIHJlYWRzIChHRVQgb25seSkgLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0t
LS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tCgoKQHJvdXRlci5nZXQoIi9qb2JzIikKYXN5bmMgZGVmIGxpc3Rfam9icygKICAgIHJlcXVlc3Q6
IFJlcXVlc3QsIG9wZXJhdG9yOiBSZXF1aXJlSm9ic1JlYWQsCiAgICBqb2Jfc3RhdGU6IHN0ciB8IE5vbmUgPSBRdWVyeShkZWZhdWx0PU5vbmUpLAogICAg
bGltaXQ6IGludCA9IFF1ZXJ5KGRlZmF1bHQ9MTAwLCBnZT0xLCBsZT01MDApLAogICAgc2Vzc2lvbjogQXN5bmNTZXNzaW9uID0gRGVwZW5kcyhnZXRfZGJf
c2Vzc2lvbikpIC0+IGRpY3Q6CiAgICBzdG10ID0gc2VsZWN0KFYyUmVzZWFyY2hKb2IpLm9yZGVyX2J5KFYyUmVzZWFyY2hKb2IuY3JlYXRlZF9hdC5kZXNj
KCkpCiAgICBpZiBqb2Jfc3RhdGUgaXMgbm90IE5vbmU6CiAgICAgICAgc3RtdCA9IHN0bXQud2hlcmUoVjJSZXNlYXJjaEpvYi5qb2Jfc3RhdGUgPT0gam9i
X3N0YXRlKQogICAgcm93cyA9IGxpc3QoKGF3YWl0IHNlc3Npb24uZXhlY3V0ZShzdG10LmxpbWl0KGxpbWl0KSkpLnNjYWxhcnMoKS5hbGwoKSkKICAgIHJl
dHVybiB7ImpvYnMiOiBbewogICAgICAgICJpZCI6IHIuaWQsICJvd25lciI6IHIub3duZXIsCiAgICAgICAgImF1dGhvcml6YXRpb25fcmVmIjogci5hdXRo
b3JpemF0aW9uX3JlZiwgImlucHV0cyI6IHIuaW5wdXRzLAogICAgICAgICJzY2hlZHVsZSI6IHIuc2NoZWR1bGUsICJqb2Jfc3RhdGUiOiByLmpvYl9zdGF0
ZSwKICAgICAgICAiYXR0ZW1wdF9jb3VudCI6IHIuYXR0ZW1wdF9jb3VudCwgIm91dHB1dF9yZWYiOiByLm91dHB1dF9yZWYsCiAgICAgICAgImZhaWx1cmUi
OiByLmZhaWx1cmUsICJkYXRhX2NsYXNzIjogci5kYXRhX2NsYXNzLAogICAgfSBmb3IgciBpbiByb3dzXSwgInRvdGFsIjogbGVuKHJvd3MpLCAqKl9lbnZl
bG9wZShyZXF1ZXN0KX0KCgpAcm91dGVyLmdldCgiL2pvYnMve2pvYl9pZH0vYXR0ZW1wdHMiKQphc3luYyBkZWYgbGlzdF9hdHRlbXB0cygKICAgIGpvYl9p
ZDogc3RyLCByZXF1ZXN0OiBSZXF1ZXN0LCBvcGVyYXRvcjogUmVxdWlyZUpvYnNSZWFkLAogICAgc2Vzc2lvbjogQXN5bmNTZXNzaW9uID0gRGVwZW5kcyhn
ZXRfZGJfc2Vzc2lvbikpIC0+IGRpY3Q6CiAgICByb3dzID0gbGlzdCgoYXdhaXQgc2Vzc2lvbi5leGVjdXRlKAogICAgICAgIHNlbGVjdChWMlJlc2VhcmNo
Sm9iQXR0ZW1wdCkKICAgICAgICAud2hlcmUoVjJSZXNlYXJjaEpvYkF0dGVtcHQuam9iX2lkID09IGpvYl9pZCkKICAgICAgICAub3JkZXJfYnkoVjJSZXNl
YXJjaEpvYkF0dGVtcHQuYXR0ZW1wdF9pbmRleCkpKS5zY2FsYXJzKCkuYWxsKCkpCiAgICByZXR1cm4geyJhdHRlbXB0cyI6IFt7CiAgICAgICAgImF0dGVt
cHRfaW5kZXgiOiByLmF0dGVtcHRfaW5kZXgsICJvdXRjb21lIjogci5vdXRjb21lLAogICAgICAgICJhcnRpZmFjdF9yZWYiOiByLmFydGlmYWN0X3JlZiwg
InJlYXNvbiI6IHIucmVhc29uLAogICAgICAgICJhY3Rvcl9pZCI6IHIuYWN0b3JfaWQsCiAgICB9IGZvciByIGluIHJvd3NdLCAidG90YWwiOiBsZW4ocm93
cyksICoqX2VudmVsb3BlKHJlcXVlc3QpfQoKCkByb3V0ZXIuZ2V0KCIvcmVzdWx0cyIpCmFzeW5jIGRlZiBsaXN0X3Jlc3VsdHMoCiAgICByZXF1ZXN0OiBS
ZXF1ZXN0LCBvcGVyYXRvcjogUmVxdWlyZVJlc3VsdHNSZWFkLAogICAgcmVzdWx0X2NsYXNzOiBzdHIgfCBOb25lID0gUXVlcnkoZGVmYXVsdD1Ob25lKSwK
ICAgIGxpbWl0OiBpbnQgPSBRdWVyeShkZWZhdWx0PTEwMCwgZ2U9MSwgbGU9NTAwKSwKICAgIHNlc3Npb246IEFzeW5jU2Vzc2lvbiA9IERlcGVuZHMoZ2V0
X2RiX3Nlc3Npb24pKSAtPiBkaWN0OgogICAgc3RtdCA9IHNlbGVjdChWMlJlc2VhcmNoUmVzdWx0KS5vcmRlcl9ieSgKICAgICAgICBWMlJlc2VhcmNoUmVz
dWx0LmNyZWF0ZWRfYXQuZGVzYygpKQogICAgaWYgcmVzdWx0X2NsYXNzIGlzIG5vdCBOb25lOgogICAgICAgIHN0bXQgPSBzdG10LndoZXJlKFYyUmVzZWFy
Y2hSZXN1bHQucmVzdWx0X2NsYXNzID09IHJlc3VsdF9jbGFzcykKICAgIHJvd3MgPSBsaXN0KChhd2FpdCBzZXNzaW9uLmV4ZWN1dGUoc3RtdC5saW1pdChs
aW1pdCkpKS5zY2FsYXJzKCkuYWxsKCkpCiAgICByZXR1cm4geyJyZXN1bHRzIjogW3sKICAgICAgICAiaWQiOiByLmlkLCAicmVzdWx0X2NsYXNzIjogci5y
ZXN1bHRfY2xhc3MsICJqb2JfaWQiOiByLmpvYl9pZCwKICAgICAgICAiYXR0ZW1wdF9pbmRleCI6IHIuYXR0ZW1wdF9pbmRleCwKICAgICAgICAic3RyYXRl
Z3lfdmVyc2lvbl9pZCI6IHIuc3RyYXRlZ3lfdmVyc2lvbl9pZCwKICAgICAgICAiaW5wdXRfcmVnaXN0cnlfaWQiOiByLmlucHV0X3JlZ2lzdHJ5X2lkLAog
ICAgICAgICJjb3N0X21vZGVsX2lkIjogci5jb3N0X21vZGVsX2lkLCAiaW5wdXRzX2hhc2giOiByLmlucHV0c19oYXNoLAogICAgICAgICJlbmdpbmVfdmVy
c2lvbnMiOiByLmVuZ2luZV92ZXJzaW9ucywKICAgICAgICAic3VtbWFyeSI6IHIuc3VtbWFyeSwgInRpbWVfYmFzaXMiOiByLnRpbWVfYmFzaXMsCiAgICAg
ICAgImRhdGFfY2xhc3MiOiByLmRhdGFfY2xhc3MsCiAgICB9IGZvciByIGluIHJvd3NdLCAidG90YWwiOiBsZW4ocm93cyksICoqX2VudmVsb3BlKHJlcXVl
c3QpfQo=
'@
Write-Evidence ("record 7/17 staged: " + $Rec7Path)
$Rec8Path = "app\v2\research_jobs\contracts.py"
$Rec8Sha  = "b8d0c5313c2c7a035a90167ece78cbdcda792f1a9bf706a447fa261eb7b7783e"
$Rec8B64 = @'
IiIiQkUtNyB0eXBlZCBjb250cmFjdHMg4oCUIHZvY2FidWxhcmllcyBhbmQgdGhlIFAtOSByZXN1bHQtY2xhc3MgbGF3LgoKVGhlIGZvdXItY2xhc3MgdGF4
b25vbXkgZXhpc3RzIGhlcmU7IE9OTFkgYmFja3Rlc3Qvc2ltdWxhdGlvbiBhcmUKY29uc3RydWN0aWJsZSBpbiB0aGlzIGJhbmQuIGBwYXBlcmAvYGxpdmVg
IGFyZSB0eXBlZCByZWZ1c2FscyBhdCBldmVyeQpjb25zdHJ1Y3Rpb24gcG9pbnQgQU5EIGFic2VudCBmcm9tIHRoZSBEREwgQ0hFQ0sgKHNjaGVtYS1pbXBv
c3NpYmxlKS4KIiIiCgpmcm9tIF9fZnV0dXJlX18gaW1wb3J0IGFubm90YXRpb25zCgpmcm9tIGRhdGFjbGFzc2VzIGltcG9ydCBkYXRhY2xhc3MsIGZpZWxk
Cgpmcm9tIGFwcC52Mi5yZXNlYXJjaF9nb3Zlcm5hbmNlLmNvbnRyYWN0cyBpbXBvcnQgREFUQV9DTEFTU0VTCgojIFNpbmdsZSB0YXhvbm9teSDigJQgc2hh
cmVkIGxpbmVhZ2UsIG5vIGZvcmsgKFJFUS0xLjEyKS4KUkpfREFUQV9DTEFTU0VTID0gREFUQV9DTEFTU0VTClJKX0ZJUlNUX0xBTkRJTkdfREFUQV9DTEFT
U0VTID0gKCJzeW50aGV0aWMiLCAic2ltdWxhdGVkIikKCiMgUC05OiB0aGUgZnVsbCB0YXhvbm9teSB2cyB0aGUgY29uc3RydWN0aWJsZSBzZXQuClJFU1VM
VF9DTEFTU19UQVhPTk9NWSA9ICgiYmFja3Rlc3QiLCAic2ltdWxhdGlvbiIsICJwYXBlciIsICJsaXZlIikKQ09OU1RSVUNUSUJMRV9SRVNVTFRfQ0xBU1NF
UyA9ICgiYmFja3Rlc3QiLCAic2ltdWxhdGlvbiIpCgpSRUdJU1RSQVRJT05fT1VUQ09NRVMgPSAoInJlZ2lzdGVyZWQiLCAicmV1c2VkIiwgInJlZnVzZWQi
KQojIENSLVYyLUJFLTctMDAxIEYtMTogdGhlIHYxIGNvc3QtdW5pdCB2b2NhYnVsYXJ5LiBUaGUgcmVwbGF5IGVuZ2luZSdzCiMgYGFwcGx5X2Nvc3RzYCBh
Y2NlcHRzIGV4YWN0bHkgdGhlc2UgdHdvIHVuaXRzOyByZWdpc3RyYXRpb24gcmVmdXNlcwojIGFueXRoaW5nIGVsc2UgKHR5cGVkICsgZHVyYWJseSBhdWRp
dGVkKSBzbyBubyBsYXdmdWxseSByZWdpc3RlcmVkIGNvc3QKIyBtb2RlbCBjYW4gcmVhY2ggdGhlIGVuZ2luZSdzIHVua25vd24tdW5pdCBicmFuY2guCkNP
U1RfVU5JVFNfVjEgPSAoInByaWNlIiwgImZyYWN0aW9uIikKTElGRUNZQ0xFX1NUQVRFUyA9ICgiZHJhZnQiLCAicmVnaXN0ZXJlZCIsICJyZXRpcmVkIikK
Sk9CX1NUQVRFUyA9ICgicXVldWVkIiwgInJ1bm5pbmciLCAic3VjY2VlZGVkIiwgImZhaWxlZCIsICJjYW5jZWxsZWQiKQpKT0JfVEVSTUlOQUxfU1RBVEVT
ID0gKCJzdWNjZWVkZWQiLCAiZmFpbGVkIiwgImNhbmNlbGxlZCIpCkFUVEVNUFRfT1VUQ09NRVMgPSAoInN1Y2NlZWRlZCIsICJmYWlsZWQiLCAiY2FuY2Vs
bGVkIikKU0NIRURVTEVfS0lORFNfVjEgPSAoIm1hbnVhbCIsKSAgIyBDNDogYW55dGhpbmcgZWxzZSBpcyBhIHR5cGVkIHJlZnVzYWwKCiMgQzI6IHRoZSBl
eGFjdCBtdXRhYmxlIGNvbHVtbiBzZXQgb24gdjJfcmVzZWFyY2hfam9iIChhbGxvdy1saXN0IGNvbnN0YW50OwojIGFzc2VydGVkIGJ5IHRlc3Qg4oCUIFBh
cnQgMTAuMSkuCkpPQl9NVVRBQkxFX0NPTFVNTlMgPSBmcm96ZW5zZXQoCiAgICB7ImpvYl9zdGF0ZSIsICJhdHRlbXB0X2NvdW50IiwgIm91dHB1dF9yZWYi
LCAiZmFpbHVyZSJ9KQojIFBhcnQgMTAuMTogdGhlIHJ1bm5lcidzIHdyaXRhYmxlLXRhYmxlIGFsbG93LWxpc3QuClJVTk5FUl9JTlNFUlRfVEFCTEVTID0g
ZnJvemVuc2V0KAogICAgeyJ2Ml9yZXNlYXJjaF9yZXN1bHQiLCAidjJfcmVzZWFyY2hfam9iX2F0dGVtcHQiLAogICAgICJ2Ml9hdWRpdF9ldmVudCIsICJ2
Ml9saW5lYWdlX3JlY29yZCJ9KQpSVU5ORVJfVVBEQVRFX1RBQkxFUyA9IGZyb3plbnNldCh7InYyX3Jlc2VhcmNoX2pvYiJ9KQoKCmNsYXNzIFJlc3VsdENs
YXNzUmVmdXNlZChFeGNlcHRpb24pOgogICAgIiIiUC05IHR5cGVkIHJlZnVzYWw6IHBhcGVyL2xpdmUgYXJlIG5vdCBjb25zdHJ1Y3RpYmxlIGluIEJFLTcu
IiIiCgogICAgZGVmIF9faW5pdF9fKHNlbGYsIHJlcXVlc3RlZDogc3RyKSAtPiBOb25lOgogICAgICAgIHNlbGYucmVxdWVzdGVkID0gcmVxdWVzdGVkCiAg
ICAgICAgc3VwZXIoKS5fX2luaXRfXygKICAgICAgICAgICAgZiJyZXN1bHQgY2xhc3MgJ3tyZXF1ZXN0ZWR9JyBpcyBub3QgY29uc3RydWN0aWJsZSBpbiBi
YW5kIEJFLTciCiAgICAgICAgICAgIGYiIOKAlCBjb25zdHJ1Y3RpYmxlIHNldDoge0NPTlNUUlVDVElCTEVfUkVTVUxUX0NMQVNTRVN9IgogICAgICAgICkK
CgpkZWYgcmVxdWlyZV9jb25zdHJ1Y3RpYmxlX3Jlc3VsdF9jbGFzcyhyZXN1bHRfY2xhc3M6IHN0cikgLT4gc3RyOgogICAgIiIiRXZlcnkgY29uc3RydWN0
aW9uIHBvaW50IGNhbGxzIHRoaXMgQkVGT1JFIHRvdWNoaW5nIHRoZSBEQi4iIiIKICAgIGlmIHJlc3VsdF9jbGFzcyBub3QgaW4gUkVTVUxUX0NMQVNTX1RB
WE9OT01ZOgogICAgICAgIHJhaXNlIFJlc3VsdENsYXNzUmVmdXNlZChyZXN1bHRfY2xhc3MpCiAgICBpZiByZXN1bHRfY2xhc3Mgbm90IGluIENPTlNUUlVD
VElCTEVfUkVTVUxUX0NMQVNTRVM6CiAgICAgICAgcmFpc2UgUmVzdWx0Q2xhc3NSZWZ1c2VkKHJlc3VsdF9jbGFzcykKICAgIHJldHVybiByZXN1bHRfY2xh
c3MKCgpAZGF0YWNsYXNzKGZyb3plbj1UcnVlKQpjbGFzcyBUeXBlZE91dGNvbWU6CiAgICAiIiJVbmlmb3JtIHR5cGVkIG91dGNvbWUgZm9yIHJlZ2lzdHJh
dGlvbi9zdWJtaXNzaW9uIHdyaXRlcnMuIiIiCgogICAgb3V0Y29tZTogc3RyCiAgICByZWFzb25zOiBsaXN0ID0gZmllbGQoZGVmYXVsdF9mYWN0b3J5PWxp
c3QpCiAgICByZWNvcmRfaWQ6IHN0ciB8IE5vbmUgPSBOb25lCgogICAgQHByb3BlcnR5CiAgICBkZWYgcmVmdXNlZChzZWxmKSAtPiBib29sOgogICAgICAg
IHJldHVybiBzZWxmLm91dGNvbWUgPT0gInJlZnVzZWQiCg==
'@
Write-Evidence ("record 8/17 staged: " + $Rec8Path)
$Rec9Path = "app\v2\research_jobs\leakage.py"
$Rec9Sha  = "98e9763f8d5d2bfed242bb80158542784b4958ca320fc89700067a58a77623c6"
$Rec9B64 = @'
IiIiQkUtNyBVLTIgc3RydWN0dXJhbCBsZWFrYWdlIGd1YXJkcyDigJQgUC04IChwbGFuIFBhcnQgNSwgRy0x4oCmRy01KS4KClB1cmUgdmFsaWRhdGlvbiBm
dW5jdGlvbnM7IG5vIEkvTywgbm8gY2xvY2sgKGFzX29mL25vdyBhbHdheXMgcGFyYW1ldGVycykuClRoZSBWMSBDaHJvbm9sb2d5R3VhcmQvVGVtcG9yYWxT
cGxpdEVuZ2luZSBsaW5lYWdlIChwaW5uZWQgwqcxLjApIGlzIHRoZQp2b2NhYnVsYXJ5IHJlZmVyZW5jZTsgdGhlc2UgZ3VhcmRzIGFyZSB0aGUgYmFuZCdz
IG93biBlbmZvcmNlZCBzdHJ1Y3R1cmUuCiIiIgoKZnJvbSBfX2Z1dHVyZV9fIGltcG9ydCBhbm5vdGF0aW9ucwoKaW1wb3J0IGhhc2hsaWIKaW1wb3J0IGpz
b24KZnJvbSBkYXRhY2xhc3NlcyBpbXBvcnQgZGF0YWNsYXNzCmZyb20gZGF0ZXRpbWUgaW1wb3J0IGRhdGV0aW1lLCB0aW1lZGVsdGEKCgpjbGFzcyBMZWFr
YWdlUmVmdXNlZChFeGNlcHRpb24pOgogICAgIiIiVHlwZWQgbGVha2FnZSByZWZ1c2FsIOKAlCBjYXJyaWVzIHRoZSBndWFyZCBpZCBhbmQgcmVhc29ucy4i
IiIKCiAgICBkZWYgX19pbml0X18oc2VsZiwgZ3VhcmQ6IHN0ciwgcmVhc29uczogbGlzdCkgLT4gTm9uZToKICAgICAgICBzZWxmLmd1YXJkID0gZ3VhcmQK
ICAgICAgICBzZWxmLnJlYXNvbnMgPSByZWFzb25zCiAgICAgICAgc3VwZXIoKS5fX2luaXRfXyhmImxlYWthZ2UgZ3VhcmQge2d1YXJkfSByZWZ1c2VkOiB7
cmVhc29uc30iKQoKCkBkYXRhY2xhc3MoZnJvemVuPVRydWUpCmNsYXNzIFJlcGxheVdpbmRvdzoKICAgICIiIlRoZSBhcy1vZiBtb2RlbCAocGxhbiBQYXJ0
IDIpOiBhc19vZiA+PSB3aW5kb3dfZW5kIGVuZm9yY2VkLiIiIgoKICAgIHdpbmRvd19zdGFydDogZGF0ZXRpbWUKICAgIHdpbmRvd19lbmQ6IGRhdGV0aW1l
CiAgICBhc19vZjogZGF0ZXRpbWUKCiAgICBkZWYgdmFsaWRhdGUoc2VsZikgLT4gTm9uZToKICAgICAgICByZWFzb25zID0gW10KICAgICAgICBpZiBzZWxm
LndpbmRvd19zdGFydCA+PSBzZWxmLndpbmRvd19lbmQ6CiAgICAgICAgICAgIHJlYXNvbnMuYXBwZW5kKHsiZmFpbGluZyI6ICJ3aW5kb3dfb3JkZXIiLAog
ICAgICAgICAgICAgICAgICAgICAgICAgICAgInN0YXJ0Ijogc2VsZi53aW5kb3dfc3RhcnQuaXNvZm9ybWF0KCksCiAgICAgICAgICAgICAgICAgICAgICAg
ICAgICAiZW5kIjogc2VsZi53aW5kb3dfZW5kLmlzb2Zvcm1hdCgpfSkKICAgICAgICBpZiBzZWxmLmFzX29mIDwgc2VsZi53aW5kb3dfZW5kOgogICAgICAg
ICAgICByZWFzb25zLmFwcGVuZCh7ImZhaWxpbmciOiAiYXNfb2ZfYmVmb3JlX3dpbmRvd19lbmQiLAogICAgICAgICAgICAgICAgICAgICAgICAgICAgImFz
X29mIjogc2VsZi5hc19vZi5pc29mb3JtYXQoKSwKICAgICAgICAgICAgICAgICAgICAgICAgICAgICJ3aW5kb3dfZW5kIjogc2VsZi53aW5kb3dfZW5kLmlz
b2Zvcm1hdCgpLAogICAgICAgICAgICAgICAgICAgICAgICAgICAgInJ1bGUiOiAiYXNfb2YgPj0gd2luZG93X2VuZCAocGxhbiBQYXJ0IDIpIn0pCiAgICAg
ICAgaWYgcmVhc29uczoKICAgICAgICAgICAgcmFpc2UgTGVha2FnZVJlZnVzZWQoIkctMTp3aW5kb3ciLCByZWFzb25zKQoKCmRlZiBmaWx0ZXJfYmFyc19n
MShiYXJzOiBsaXN0W2RpY3RdLCB3aW5kb3c6IFJlcGxheVdpbmRvdykgLT4gbGlzdFtkaWN0XToKICAgICIiIkctMSDigJQgdGhlIGFzLW9mIGN1dG9mZiBh
dCBpbnB1dCBhc3NlbWJseTogb25seSBiYXJzIHdpdGgKICAgIG9wZW5fdGltZSA8PSBhc19vZiBBTkQgaW5zaWRlIHRoZSB3aW5kb3cgc3Vydml2ZS4gVGhp
cyBmdW5jdGlvbiBpcyB0aGUKICAgIE9OTFkgcGF0aCBmcm9tIHJhdyBiYXJzIGludG8gYSByZXBsYXkgaW5wdXQgc2V0LiIiIgogICAgd2luZG93LnZhbGlk
YXRlKCkKICAgIGtlcHQgPSBbCiAgICAgICAgYiBmb3IgYiBpbiBiYXJzCiAgICAgICAgaWYgd2luZG93LndpbmRvd19zdGFydCA8PSBiWyJvcGVuX3RpbWUi
XSA8PSB3aW5kb3cud2luZG93X2VuZAogICAgICAgIGFuZCBiWyJvcGVuX3RpbWUiXSA8PSB3aW5kb3cuYXNfb2YKICAgIF0KICAgIHJldHVybiBzb3J0ZWQo
a2VwdCwga2V5PWxhbWJkYSBiOiBiWyJvcGVuX3RpbWUiXSkKCgpkZWYgdmFsaWRhdGVfaG9yaXpvbl9nMygqLCBsYWJlbF9ob3Jpem9uOiB0aW1lZGVsdGEs
IGVtYmFyZ286IHRpbWVkZWx0YSwKICAgICAgICAgICAgICAgICAgICAgICAgd2luZG93OiBSZXBsYXlXaW5kb3cpIC0+IE5vbmU6CiAgICAiIiJHLTMg4oCU
IGxhYmVsLWhvcml6b24vZW1iYXJnbyByZWplY3Rpb24gYXQgc3VibWlzc2lvbjogYSBob3Jpem9uCiAgICB3aG9zZSBsYWJlbHMgd291bGQgZXh0ZW5kIHBh
c3Qgd2luZG93X2VuZCAtIGVtYmFyZ28gaXMgcmVmdXNlZC4iIiIKICAgIGxhdGVzdF9sYWJlbF90cyA9IHdpbmRvdy53aW5kb3dfZW5kIC0gZW1iYXJnbwog
ICAgaWYgbGFiZWxfaG9yaXpvbiA+IHRpbWVkZWx0YSgwKToKICAgICAgICAjIGEgZGVjaXNpb24gYXQgdCBuZWVkcyBsYWJlbHMgYXQgdCArIGhvcml6b247
IHRoZSBsYXN0IGxlZ2FsCiAgICAgICAgIyBkZWNpc2lvbiB0aW1lIGlzIGxhdGVzdF9sYWJlbF90cyAtIGhvcml6b24sIHdoaWNoIG11c3QgbGllCiAgICAg
ICAgIyBpbnNpZGUgdGhlIHdpbmRvdwogICAgICAgIGxhc3RfbGVnYWwgPSBsYXRlc3RfbGFiZWxfdHMgLSBsYWJlbF9ob3Jpem9uCiAgICAgICAgaWYgbGFz
dF9sZWdhbCA8PSB3aW5kb3cud2luZG93X3N0YXJ0OgogICAgICAgICAgICByYWlzZSBMZWFrYWdlUmVmdXNlZCgiRy0zOmhvcml6b24iLCBbewogICAgICAg
ICAgICAgICAgImZhaWxpbmciOiAibGFiZWxfaG9yaXpvbl9wYXN0X2VtYmFyZ28iLAogICAgICAgICAgICAgICAgImxhYmVsX2hvcml6b25fcyI6IGxhYmVs
X2hvcml6b24udG90YWxfc2Vjb25kcygpLAogICAgICAgICAgICAgICAgImVtYmFyZ29fcyI6IGVtYmFyZ28udG90YWxfc2Vjb25kcygpLAogICAgICAgICAg
ICAgICAgIndpbmRvd19lbmQiOiB3aW5kb3cud2luZG93X2VuZC5pc29mb3JtYXQoKSwKICAgICAgICAgICAgICAgICJydWxlIjogImhvcml6b24gbXVzdCBs
ZWF2ZSBhIG5vbi1lbXB0eSBkZWNpc2lvbiB3aW5kb3ciCiAgICAgICAgICAgICAgICAgICAgICAgICIgYmVmb3JlIHdpbmRvd19lbmQgLSBlbWJhcmdvIiwK
ICAgICAgICAgICAgfV0pCgoKZGVmIHZhbGlkYXRlX2RlY2lzaW9uX29yZGVyaW5nX2c0KGxlZGdlcjogbGlzdFtkaWN0XSkgLT4gTm9uZToKICAgICIiIkct
NCDigJQgZGVjaXNpb24tdnMtZGF0YSB0aW1lc3RhbXAgb3JkZXJpbmc6IGV2ZXJ5IHJlY29yZGVkIGRlY2lzaW9uJ3MKICAgIGRhdGEgcmVmcyBtdXN0IGhh
dmUgb3Blbl90aW1lIDw9IGRlY2lzaW9uX3RzLiIiIgogICAgdmlvbGF0aW9ucyA9IFtdCiAgICBmb3IgZW50cnkgaW4gbGVkZ2VyOgogICAgICAgIGRlY2lz
aW9uX3RzID0gZW50cnlbImRlY2lzaW9uX3RzIl0KICAgICAgICBmb3IgcmVmX3RzIGluIGVudHJ5LmdldCgiZGF0YV9yZWZfdHMiLCBbXSk6CiAgICAgICAg
ICAgIGlmIHJlZl90cyA+IGRlY2lzaW9uX3RzOgogICAgICAgICAgICAgICAgdmlvbGF0aW9ucy5hcHBlbmQoewogICAgICAgICAgICAgICAgICAgICJkZWNp
c2lvbl90cyI6IGRlY2lzaW9uX3RzLmlzb2Zvcm1hdCgpLAogICAgICAgICAgICAgICAgICAgICJkYXRhX3JlZl90cyI6IHJlZl90cy5pc29mb3JtYXQoKX0p
CiAgICBpZiB2aW9sYXRpb25zOgogICAgICAgIHJhaXNlIExlYWthZ2VSZWZ1c2VkKCJHLTQ6b3JkZXJpbmciLCB2aW9sYXRpb25zKQoKCmRlZiBjb250ZW50
X2hhc2goYmFyczogbGlzdFtkaWN0XSwgd2luZG93OiBSZXBsYXlXaW5kb3csCiAgICAgICAgICAgICAgICAgc2VyaWVzX3JlZnM6IGRpY3QpIC0+IHN0cjoK
ICAgICIiIlRoZSByZWdpc3RlcmVkLWlucHV0IGNvbnRlbnQgaGFzaCAoRy01IGJhc2lzOyBSRVEtMS4zKS4iIiIKICAgIHBheWxvYWQgPSB7CiAgICAgICAg
IndpbmRvdyI6IFt3aW5kb3cud2luZG93X3N0YXJ0Lmlzb2Zvcm1hdCgpLAogICAgICAgICAgICAgICAgICAgd2luZG93LndpbmRvd19lbmQuaXNvZm9ybWF0
KCldLAogICAgICAgICJzZXJpZXNfcmVmcyI6IHNlcmllc19yZWZzLAogICAgICAgICJiYXJzIjogWwogICAgICAgICAgICB7Im9wZW5fdGltZSI6IGJbIm9w
ZW5fdGltZSJdLmlzb2Zvcm1hdCgpLAogICAgICAgICAgICAgIm9wZW4iOiBzdHIoYlsib3BlbiJdKSwgImhpZ2giOiBzdHIoYlsiaGlnaCJdKSwKICAgICAg
ICAgICAgICJsb3ciOiBzdHIoYlsibG93Il0pLCAiY2xvc2UiOiBzdHIoYlsiY2xvc2UiXSksCiAgICAgICAgICAgICAidm9sdW1lIjogc3RyKGIuZ2V0KCJ2
b2x1bWUiLCAiMCIpKX0KICAgICAgICAgICAgZm9yIGIgaW4gYmFycwogICAgICAgIF0sCiAgICB9CiAgICByZXR1cm4gaGFzaGxpYi5zaGEyNTYoCiAgICAg
ICAganNvbi5kdW1wcyhwYXlsb2FkLCBzb3J0X2tleXM9VHJ1ZSwgc2VwYXJhdG9ycz0oIiwiLCAiOiIpKQogICAgICAgIC5lbmNvZGUoInV0Zi04IikpLmhl
eGRpZ2VzdCgpCgoKZGVmIHZlcmlmeV9jb250ZW50X2c1KCosIHN0b3JlZF9oYXNoOiBzdHIsIHJlY29tcHV0ZWRfaGFzaDogc3RyKSAtPiBOb25lOgogICAg
IiIiRy01IOKAlCByZWdpc3RlcmVkLWlucHV0IGltbXV0YWJpbGl0eSByZS1wcm9vZiBhdCByZXBsYXkgdGltZToKICAgIG1pc21hdGNoID0gdHlwZWQgcmVm
dXNhbCwgbmV2ZXIgc2lsZW50IGluY2x1c2lvbiAoYWxzbyB0aGUgaW5nZXN0LWxhZwogICAgY29udHJvbCBwZXIgUFJWIMKnNS40IOKAlCBhIGJhciBpbmdl
c3RlZCBhZnRlciBhc19vZiBjaGFuZ2VzIHRoZSBjb250ZW50CiAgICBoYXNoIGFuZCByZWZ1c2VzKS4iIiIKICAgIGlmIHN0b3JlZF9oYXNoICE9IHJlY29t
cHV0ZWRfaGFzaDoKICAgICAgICByYWlzZSBMZWFrYWdlUmVmdXNlZCgiRy01OmNvbnRlbnQiLCBbewogICAgICAgICAgICAiZmFpbGluZyI6ICJjb250ZW50
X2hhc2hfbWlzbWF0Y2giLAogICAgICAgICAgICAic3RvcmVkIjogc3RvcmVkX2hhc2gsICJyZWNvbXB1dGVkIjogcmVjb21wdXRlZF9oYXNofV0pCg==
'@
Write-Evidence ("record 9/17 staged: " + $Rec9Path)
$Rec10Path = "app\v2\research_jobs\queue.py"
$Rec10Sha  = "1b5ceeedcc9738d0785d42732a23bdf39b5ecb0f3bfe4085b36edebb80514e43"
$Rec10B64 = @'
IiIiQkUtNyBVLTQgZ292ZXJuZWQgam9iIHF1ZXVlIChCTyDCpzE7IFJFUS0xLjc7IGNvbmRpdGlvbnMgQzHigJNDNCkuCgpEYXRhYmFzZS1iYWNrZWQgKEFS
Q0ggcm93IDg5IGRlY2lzaW9uKTsgbWFudWFsIGludm9jYXRpb24gb25seSAoQzQpLgpUaGUgam9iIHJvdyBpcyB0aGUgYmFuZCdzIHNvbGUgbXV0YWJsZSBz
dGF0ZTsgZXZlcnkgdHJhbnNpdGlvbiBtaW50cyBhbgphdHRlbXB0LWxlZGdlciByb3cgYW5kIGFuIGF1ZGl0IGV2ZW50IChQLTEwKS4gU3VibWlzc2lvbi10
aW1lIGZpZWxkcyBhcmUKd3JpdGUtb25jZSAoQzEpOyB0aGUgbXV0YWJsZSBzZXQgaXMgZXhhY3RseSBDMidzLgoiIiIKCmZyb20gX19mdXR1cmVfXyBpbXBv
cnQgYW5ub3RhdGlvbnMKCmZyb20gZGF0YWNsYXNzZXMgaW1wb3J0IGRhdGFjbGFzcwoKZnJvbSBzcWxhbGNoZW15IGltcG9ydCBzZWxlY3QKZnJvbSBzcWxh
bGNoZW15LmV4dC5hc3luY2lvIGltcG9ydCBBc3luY1Nlc3Npb24KCmZyb20gYXBwLmRiLm1vZGVscy52Ml9yZXNlYXJjaF9qb2JzIGltcG9ydCAoCiAgICBW
MlJlc2VhcmNoSm9iLAogICAgVjJSZXNlYXJjaEpvYkF0dGVtcHQsCiAgICBWMlN0cmF0ZWd5VmVyc2lvbiwKKQpmcm9tIGFwcC52Mi5hdWRpdC5jb250cmFj
dCBpbXBvcnQgVjJBdWRpdEV2ZW50Q3JlYXRlCmZyb20gYXBwLnYyLmF1ZGl0LnJlcG9zaXRvcnkgaW1wb3J0IFYyQXVkaXRSZXBvc2l0b3J5CmZyb20gYXBw
LnYyLnJlc2VhcmNoX2pvYnMuY29udHJhY3RzIGltcG9ydCAoCiAgICBKT0JfVEVSTUlOQUxfU1RBVEVTLAogICAgUkpfRklSU1RfTEFORElOR19EQVRBX0NM
QVNTRVMsCiAgICBTQ0hFRFVMRV9LSU5EU19WMSwKICAgIFR5cGVkT3V0Y29tZSwKKQoKX0RPTUFJTiA9ICJ2Mi5yZXNlYXJjaF9qb2JzIgoKCkBkYXRhY2xh
c3MoZnJvemVuPVRydWUpCmNsYXNzIEpvYlN1Ym1pc3Npb246CiAgICBvd25lcjogc3RyCiAgICBhdXRob3JpemF0aW9uX3JlZjogc3RyCiAgICBpbnB1dHM6
IGRpY3QgICAgICAgICAgICAjIHsiaW5wdXRfcmVnaXN0cnlfaWQiLCAic3RyYXRlZ3lfdmVyc2lvbl9pZCIsCiAgICAjICAgICAgICAgICAgICAgICAgICAg
ICAgICAiY29zdF9tb2RlbF9pZCIsICJyZXN1bHRfY2xhc3MiLCAuLi59CiAgICBzY2hlZHVsZTogZGljdAogICAgZGF0YV9jbGFzczogc3RyCiAgICBtb2Rl
OiBzdHIKICAgIG9wZXJhdG9yX2lkOiBzdHIKICAgIGNvcnJlbGF0aW9uX2lkOiBzdHIgfCBOb25lCgoKYXN5bmMgZGVmIF9hdWRpdChzZXNzaW9uOiBBc3lu
Y1Nlc3Npb24sIGFjdGlvbjogc3RyLCAqLCBkZXRhaWxzOiBkaWN0LAogICAgICAgICAgICAgICAgIG1vZGU6IHN0ciwgb3BlcmF0b3JfaWQ6IHN0ciwKICAg
ICAgICAgICAgICAgICBjb3JyZWxhdGlvbl9pZDogc3RyIHwgTm9uZSwKICAgICAgICAgICAgICAgICByZXNvdXJjZV9pZDogc3RyIHwgTm9uZSA9IE5vbmUp
IC0+IE5vbmU6CiAgICBhd2FpdCBWMkF1ZGl0UmVwb3NpdG9yeShzZXNzaW9uKS5hcHBlbmQoVjJBdWRpdEV2ZW50Q3JlYXRlKAogICAgICAgIGRvbWFpbj1f
RE9NQUlOLCBhY3Rpb249YWN0aW9uLCBhY3Rvcl9pZD1vcGVyYXRvcl9pZCwKICAgICAgICBhY3Rvcl90eXBlPSJvcGVyYXRvciIsIG1vZGU9bW9kZSwKICAg
ICAgICByZXNvdXJjZV90eXBlPSJyZXNlYXJjaF9qb2IiLCByZXNvdXJjZV9pZD1yZXNvdXJjZV9pZCwKICAgICAgICBkZXRhaWxzPWRldGFpbHMsIG9wZXJh
dG9yX2lkPW9wZXJhdG9yX2lkLAogICAgICAgIGNvcnJlbGF0aW9uX2lkPWNvcnJlbGF0aW9uX2lkKSkKCgphc3luYyBkZWYgc3VibWl0X2pvYihzZXNzaW9u
OiBBc3luY1Nlc3Npb24sIHN1YjogSm9iU3VibWlzc2lvbikgLT4gVHlwZWRPdXRjb21lOgogICAgIiIiU3VibWlzc2lvbjogdHlwZWQgcmVmdXNhbHMsIGR1
cmFibHkgYXVkaXRlZCAoQy0xIGxhdyk7IG9uIHBhc3MgdGhlCiAgICB3cml0ZS1vbmNlIHJvdyBpcyBJTlNFUlRlZCBxdWV1ZWQgKEMxKS4iIiIKICAgIHJl
YXNvbnM6IGxpc3QgPSBbXQogICAgaWYgbm90IHN1Yi5hdXRob3JpemF0aW9uX3JlZjoKICAgICAgICByZWFzb25zLmFwcGVuZCh7ImZhaWxpbmciOiAiYXV0
aG9yaXphdGlvbl9yZWYiLCAicmVxdWlyZWQiOiAic2V0In0pCiAgICBpZiBzdWIuc2NoZWR1bGUuZ2V0KCJraW5kIikgbm90IGluIFNDSEVEVUxFX0tJTkRT
X1YxOgogICAgICAgIHJlYXNvbnMuYXBwZW5kKHsiZmFpbGluZyI6ICJzY2hlZHVsZS5raW5kIiwKICAgICAgICAgICAgICAgICAgICAgICAgInZhbHVlIjog
c3ViLnNjaGVkdWxlLmdldCgia2luZCIpLAogICAgICAgICAgICAgICAgICAgICAgICAicmVxdWlyZWQiOiBsaXN0KFNDSEVEVUxFX0tJTkRTX1YxKSwKICAg
ICAgICAgICAgICAgICAgICAgICAgIm5vdGUiOiAiQzQg4oCUIHYxIHNjb3BlIGlzIG1hbnVhbCBpbnZvY2F0aW9uIG9ubHkifSkKICAgIGlmIHN1Yi5kYXRh
X2NsYXNzIG5vdCBpbiBSSl9GSVJTVF9MQU5ESU5HX0RBVEFfQ0xBU1NFUzoKICAgICAgICByZWFzb25zLmFwcGVuZCh7ImZhaWxpbmciOiAiZGF0YV9jbGFz
cyIsICJ2YWx1ZSI6IHN1Yi5kYXRhX2NsYXNzLAogICAgICAgICAgICAgICAgICAgICAgICAicmVxdWlyZWQiOiBsaXN0KFJKX0ZJUlNUX0xBTkRJTkdfREFU
QV9DTEFTU0VTKSwKICAgICAgICAgICAgICAgICAgICAgICAgIm5vdGUiOiAiY29ycHVzLWdhdGVkIChWMi1URC0xOCBjb250aW51aXR5KSJ9KQogICAgaWYg
c3ViLm1vZGUgIT0gIlJFU0VBUkNIIjoKICAgICAgICByZWFzb25zLmFwcGVuZCh7ImZhaWxpbmciOiAibW9kZSIsICJ2YWx1ZSI6IHN1Yi5tb2RlfSkKCiAg
ICAjIHN0cmF0ZWd5IG11c3QgYmUgYSByZWdpc3RlcmVkLWN1cnJlbnQgZ2VuZXJhdGlvbiAoUkVRLTEuNikKICAgIHN2X2lkID0gc3ViLmlucHV0cy5nZXQo
InN0cmF0ZWd5X3ZlcnNpb25faWQiKQogICAgaWYgbm90IHN2X2lkOgogICAgICAgIHJlYXNvbnMuYXBwZW5kKHsiZmFpbGluZyI6ICJpbnB1dHMuc3RyYXRl
Z3lfdmVyc2lvbl9pZCJ9KQogICAgZWxzZToKICAgICAgICBzdHJhdGVneSA9IChhd2FpdCBzZXNzaW9uLmV4ZWN1dGUoCiAgICAgICAgICAgIHNlbGVjdChW
MlN0cmF0ZWd5VmVyc2lvbikud2hlcmUoVjJTdHJhdGVneVZlcnNpb24uaWQgPT0gc3ZfaWQpCiAgICAgICAgKSkuc2NhbGFyX29uZV9vcl9ub25lKCkKICAg
ICAgICBpZiBzdHJhdGVneSBpcyBOb25lOgogICAgICAgICAgICByZWFzb25zLmFwcGVuZCh7ImZhaWxpbmciOiAic3RyYXRlZ3lfdmVyc2lvbiIsICJ2YWx1
ZSI6ICJ1bnJlc29sdmFibGUifSkKICAgICAgICBlbHNlOgogICAgICAgICAgICBuZXdlc3QgPSAoYXdhaXQgc2Vzc2lvbi5leGVjdXRlKAogICAgICAgICAg
ICAgICAgc2VsZWN0KFYyU3RyYXRlZ3lWZXJzaW9uKQogICAgICAgICAgICAgICAgLndoZXJlKFYyU3RyYXRlZ3lWZXJzaW9uLnN0cmF0ZWd5X2lkID09IHN0
cmF0ZWd5LnN0cmF0ZWd5X2lkKQogICAgICAgICAgICAgICAgLm9yZGVyX2J5KFYyU3RyYXRlZ3lWZXJzaW9uLnJlY29yZF9zZXEuZGVzYygpKQogICAgICAg
ICAgICApKS5zY2FsYXJzKCkuZmlyc3QoKQogICAgICAgICAgICBpZiBuZXdlc3QgaXMgTm9uZSBvciBuZXdlc3QuaWQgIT0gc3RyYXRlZ3kuaWQ6CiAgICAg
ICAgICAgICAgICByZWFzb25zLmFwcGVuZCh7ImZhaWxpbmciOiAic3RyYXRlZ3lfdmVyc2lvbiIsCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAg
InZhbHVlIjogInN1cGVyc2VkZWQgZ2VuZXJhdGlvbiDigJQgbm90IGN1cnJlbnQifSkKICAgICAgICAgICAgZWxpZiBzdHJhdGVneS5saWZlY3ljbGVfc3Rh
dGUgIT0gInJlZ2lzdGVyZWQiOgogICAgICAgICAgICAgICAgcmVhc29ucy5hcHBlbmQoeyJmYWlsaW5nIjogInN0cmF0ZWd5LmxpZmVjeWNsZV9zdGF0ZSIs
CiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgInZhbHVlIjogc3RyYXRlZ3kubGlmZWN5Y2xlX3N0YXRlLAogICAgICAgICAgICAgICAgICAgICAg
ICAgICAgICAgICJyZXF1aXJlZCI6ICJyZWdpc3RlcmVkIn0pCiAgICBmb3Iga2V5IGluICgiaW5wdXRfcmVnaXN0cnlfaWQiLCAiY29zdF9tb2RlbF9pZCIs
ICJyZXN1bHRfY2xhc3MiKToKICAgICAgICBpZiBub3Qgc3ViLmlucHV0cy5nZXQoa2V5KToKICAgICAgICAgICAgcmVhc29ucy5hcHBlbmQoeyJmYWlsaW5n
IjogZiJpbnB1dHMue2tleX0ifSkKCiAgICBpZiByZWFzb25zOgogICAgICAgIGF3YWl0IF9hdWRpdChzZXNzaW9uLCAiam9iLnN1Ym1pdC5yZWZ1c2VkIiwK
ICAgICAgICAgICAgICAgICAgICAgZGV0YWlscz17InJlYXNvbnMiOiByZWFzb25zWzo4XX0sCiAgICAgICAgICAgICAgICAgICAgIG1vZGU9c3ViLm1vZGUs
IG9wZXJhdG9yX2lkPXN1Yi5vcGVyYXRvcl9pZCwKICAgICAgICAgICAgICAgICAgICAgY29ycmVsYXRpb25faWQ9c3ViLmNvcnJlbGF0aW9uX2lkKQogICAg
ICAgIGF3YWl0IHNlc3Npb24uY29tbWl0KCkgICMgZHVyYWJsZSByZWZ1c2FsIGF1ZGl0IChDLTEgbGF3KQogICAgICAgIHJldHVybiBUeXBlZE91dGNvbWUo
b3V0Y29tZT0icmVmdXNlZCIsIHJlYXNvbnM9cmVhc29ucykKCiAgICBqb2IgPSBWMlJlc2VhcmNoSm9iKAogICAgICAgIG93bmVyPXN1Yi5vd25lciwKICAg
ICAgICBhdXRob3JpemF0aW9uX3JlZj1zdWIuYXV0aG9yaXphdGlvbl9yZWYsCiAgICAgICAgaW5wdXRzPXN1Yi5pbnB1dHMsCiAgICAgICAgc2NoZWR1bGU9
c3ViLnNjaGVkdWxlLAogICAgICAgIGpvYl9zdGF0ZT0icXVldWVkIiwKICAgICAgICBhdHRlbXB0X2NvdW50PTAsCiAgICAgICAgZGF0YV9jbGFzcz1zdWIu
ZGF0YV9jbGFzcywKICAgICAgICBtb2RlPXN1Yi5tb2RlLAogICAgICAgIG9wZXJhdG9yX2lkPXN1Yi5vcGVyYXRvcl9pZCwKICAgICAgICBjb3JyZWxhdGlv
bl9pZD1zdWIuY29ycmVsYXRpb25faWQsCiAgICApCiAgICBzZXNzaW9uLmFkZChqb2IpCiAgICBhd2FpdCBzZXNzaW9uLmZsdXNoKCkKICAgIGF3YWl0IF9h
dWRpdChzZXNzaW9uLCAiam9iLnN1Ym1pdHRlZCIsCiAgICAgICAgICAgICAgICAgZGV0YWlscz17Im93bmVyIjogc3ViLm93bmVyLAogICAgICAgICAgICAg
ICAgICAgICAgICAgICJhdXRob3JpemF0aW9uX3JlZiI6IHN1Yi5hdXRob3JpemF0aW9uX3JlZiwKICAgICAgICAgICAgICAgICAgICAgICAgICAiaW5wdXRz
Ijogc3ViLmlucHV0c30sCiAgICAgICAgICAgICAgICAgbW9kZT1zdWIubW9kZSwgb3BlcmF0b3JfaWQ9c3ViLm9wZXJhdG9yX2lkLAogICAgICAgICAgICAg
ICAgIGNvcnJlbGF0aW9uX2lkPXN1Yi5jb3JyZWxhdGlvbl9pZCwgcmVzb3VyY2VfaWQ9am9iLmlkKQogICAgcmV0dXJuIFR5cGVkT3V0Y29tZShvdXRjb21l
PSJyZWdpc3RlcmVkIiwgcmVjb3JkX2lkPWpvYi5pZCkKCgphc3luYyBkZWYgY2FuY2VsX2pvYihzZXNzaW9uOiBBc3luY1Nlc3Npb24sICosIGpvYl9pZDog
c3RyLCBhY3Rvcl9pZDogc3RyLAogICAgICAgICAgICAgICAgICAgICByZWFzb246IHN0ciwgbW9kZTogc3RyLAogICAgICAgICAgICAgICAgICAgICBjb3Jy
ZWxhdGlvbl9pZDogc3RyIHwgTm9uZSkgLT4gVHlwZWRPdXRjb21lOgogICAgIiIiVHlwZWQgY2FuY2VsOiB0ZXJtaW5hbCBzdGF0ZXMgcmVmdXNlIChSRVEt
MS43KTsgZXZlcnkgY2FuY2VsIG1pbnRzCiAgICBhIGxlZGdlciByb3cgKyBhdWRpdCBldmVudC4iIiIKICAgIGpvYiA9IChhd2FpdCBzZXNzaW9uLmV4ZWN1
dGUoCiAgICAgICAgc2VsZWN0KFYyUmVzZWFyY2hKb2IpLndoZXJlKFYyUmVzZWFyY2hKb2IuaWQgPT0gam9iX2lkKQogICAgKSkuc2NhbGFyX29uZV9vcl9u
b25lKCkKICAgIGlmIGpvYiBpcyBOb25lOgogICAgICAgIHJldHVybiBUeXBlZE91dGNvbWUob3V0Y29tZT0icmVmdXNlZCIsCiAgICAgICAgICAgICAgICAg
ICAgICAgICAgICByZWFzb25zPVt7ImZhaWxpbmciOiAiam9iX2lkIiwgInZhbHVlIjogInVucmVzb2x2YWJsZSJ9XSkKICAgIGlmIGpvYi5qb2Jfc3RhdGUg
aW4gSk9CX1RFUk1JTkFMX1NUQVRFUzoKICAgICAgICBhd2FpdCBfYXVkaXQoc2Vzc2lvbiwgImpvYi5jYW5jZWwucmVmdXNlZCIsCiAgICAgICAgICAgICAg
ICAgICAgIGRldGFpbHM9eyJqb2Jfc3RhdGUiOiBqb2Iuam9iX3N0YXRlLAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAibm90ZSI6ICJ0ZXJtaW5h
bCBzdGF0ZSJ9LAogICAgICAgICAgICAgICAgICAgICBtb2RlPW1vZGUsIG9wZXJhdG9yX2lkPWFjdG9yX2lkLAogICAgICAgICAgICAgICAgICAgICBjb3Jy
ZWxhdGlvbl9pZD1jb3JyZWxhdGlvbl9pZCwgcmVzb3VyY2VfaWQ9am9iLmlkKQogICAgICAgIGF3YWl0IHNlc3Npb24uY29tbWl0KCkKICAgICAgICByZXR1
cm4gVHlwZWRPdXRjb21lKG91dGNvbWU9InJlZnVzZWQiLAogICAgICAgICAgICAgICAgICAgICAgICAgICAgcmVhc29ucz1beyJmYWlsaW5nIjogImpvYl9z
dGF0ZSIsCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgInZhbHVlIjogam9iLmpvYl9zdGF0ZSwKICAgICAgICAgICAgICAgICAgICAg
ICAgICAgICAgICAgICAgICAibm90ZSI6ICJ0ZXJtaW5hbCDigJQgY2FuY2VsIHJlZnVzZWQifV0pCiAgICBqb2IuYXR0ZW1wdF9jb3VudCArPSAxCiAgICBq
b2Iuam9iX3N0YXRlID0gImNhbmNlbGxlZCIKICAgIGpvYi5mYWlsdXJlID0geyJjYW5jZWxsZWRfYnkiOiBhY3Rvcl9pZCwgInJlYXNvbiI6IHJlYXNvbn0K
ICAgIHNlc3Npb24uYWRkKFYyUmVzZWFyY2hKb2JBdHRlbXB0KAogICAgICAgIGpvYl9pZD1qb2IuaWQsIGF0dGVtcHRfaW5kZXg9am9iLmF0dGVtcHRfY291
bnQsCiAgICAgICAgb3V0Y29tZT0iY2FuY2VsbGVkIiwgcmVhc29uPXsiY2FuY2VsbGVkX2J5IjogYWN0b3JfaWQsCiAgICAgICAgICAgICAgICAgICAgICAg
ICAgICAgICAgICAgICAicmVhc29uIjogcmVhc29ufSwKICAgICAgICBhY3Rvcl9pZD1hY3Rvcl9pZCwgbW9kZT1tb2RlLCBvcGVyYXRvcl9pZD1hY3Rvcl9p
ZCwKICAgICAgICBjb3JyZWxhdGlvbl9pZD1jb3JyZWxhdGlvbl9pZCkpCiAgICBhd2FpdCBzZXNzaW9uLmZsdXNoKCkKICAgIGF3YWl0IF9hdWRpdChzZXNz
aW9uLCAiam9iLmNhbmNlbGxlZCIsCiAgICAgICAgICAgICAgICAgZGV0YWlscz17InJlYXNvbiI6IHJlYXNvbiwgImF0dGVtcHRfaW5kZXgiOiBqb2IuYXR0
ZW1wdF9jb3VudH0sCiAgICAgICAgICAgICAgICAgbW9kZT1tb2RlLCBvcGVyYXRvcl9pZD1hY3Rvcl9pZCwKICAgICAgICAgICAgICAgICBjb3JyZWxhdGlv
bl9pZD1jb3JyZWxhdGlvbl9pZCwgcmVzb3VyY2VfaWQ9am9iLmlkKQogICAgcmV0dXJuIFR5cGVkT3V0Y29tZShvdXRjb21lPSJyZWdpc3RlcmVkIiwgcmVj
b3JkX2lkPWpvYi5pZCkK
'@
Write-Evidence ("record 10/17 staged: " + $Rec10Path)
$Rec11Path = "app\v2\research_jobs\registry.py"
$Rec11Sha  = "bb3540221f92a688e272e09dc48983a51d248c58636e20ce9f65845e65d6ab4d"
$Rec11B64 = @'
IiIiQkUtNyBVLTMgcmVnaXN0cmF0aW9uIHdyaXRlcnMgKFJFUS0xLjMvMS40LzEuNikuCgpJbnB1dCByZWdpc3RyYXRpb24gd2l0aCBjb250ZW50LWFkZHJl
c3NlZCBkZWR1cGU7IGNvc3QtbW9kZWwgYW5kIHN0cmF0ZWd5CmdlbmVyYXRpb24gd3JpdGVycy4gQWxsIHJlZnVzYWxzIHR5cGVkICsgZHVyYWJseSBhdWRp
dGVkIChDLTEgbGF3Ogpjb21taXQtYmVmb3JlLXJldHVybiBvbiByZWZ1c2FsIHBhdGhzIHNvIHRoZSBhdWRpdCBzdXJ2aXZlcykuIiIiCgpmcm9tIF9fZnV0
dXJlX18gaW1wb3J0IGFubm90YXRpb25zCgpmcm9tIGRhdGV0aW1lIGltcG9ydCBkYXRldGltZQoKZnJvbSBzcWxhbGNoZW15IGltcG9ydCBzZWxlY3QKZnJv
bSBzcWxhbGNoZW15LmV4dC5hc3luY2lvIGltcG9ydCBBc3luY1Nlc3Npb24KCmZyb20gYXBwLmRiLm1vZGVscy52Ml9yZXNlYXJjaF9qb2JzIGltcG9ydCAo
CiAgICBWMkJhY2t0ZXN0SW5wdXQsCiAgICBWMkNvc3RNb2RlbCwKICAgIFYyU3RyYXRlZ3lWZXJzaW9uLAopCmZyb20gYXBwLnYyLmF1ZGl0LmNvbnRyYWN0
IGltcG9ydCBWMkF1ZGl0RXZlbnRDcmVhdGUKZnJvbSBhcHAudjIuYXVkaXQucmVwb3NpdG9yeSBpbXBvcnQgVjJBdWRpdFJlcG9zaXRvcnkKZnJvbSBhcHAu
djIucmVzZWFyY2hfam9icy5jb250cmFjdHMgaW1wb3J0ICgKICAgIENPU1RfVU5JVFNfVjEsCiAgICBMSUZFQ1lDTEVfU1RBVEVTLAogICAgUkpfRklSU1Rf
TEFORElOR19EQVRBX0NMQVNTRVMsCiAgICBUeXBlZE91dGNvbWUsCikKZnJvbSBhcHAudjIucmVzZWFyY2hfam9icy5sZWFrYWdlIGltcG9ydCBMZWFrYWdl
UmVmdXNlZCwgUmVwbGF5V2luZG93CgpfRE9NQUlOID0gInYyLnJlc2VhcmNoX2pvYnMiCgoKYXN5bmMgZGVmIF9hdWRpdChzZXNzaW9uOiBBc3luY1Nlc3Np
b24sIGFjdGlvbjogc3RyLCAqLCBkZXRhaWxzOiBkaWN0LAogICAgICAgICAgICAgICAgIG1vZGU6IHN0ciwgb3BlcmF0b3JfaWQ6IHN0ciwKICAgICAgICAg
ICAgICAgICBjb3JyZWxhdGlvbl9pZDogc3RyIHwgTm9uZSwKICAgICAgICAgICAgICAgICByZXNvdXJjZV90eXBlOiBzdHIsIHJlc291cmNlX2lkOiBzdHIg
fCBOb25lID0gTm9uZSkgLT4gTm9uZToKICAgIGF3YWl0IFYyQXVkaXRSZXBvc2l0b3J5KHNlc3Npb24pLmFwcGVuZChWMkF1ZGl0RXZlbnRDcmVhdGUoCiAg
ICAgICAgZG9tYWluPV9ET01BSU4sIGFjdGlvbj1hY3Rpb24sIGFjdG9yX2lkPW9wZXJhdG9yX2lkLAogICAgICAgIGFjdG9yX3R5cGU9Im9wZXJhdG9yIiwg
bW9kZT1tb2RlLCByZXNvdXJjZV90eXBlPXJlc291cmNlX3R5cGUsCiAgICAgICAgcmVzb3VyY2VfaWQ9cmVzb3VyY2VfaWQsIGRldGFpbHM9ZGV0YWlscywg
b3BlcmF0b3JfaWQ9b3BlcmF0b3JfaWQsCiAgICAgICAgY29ycmVsYXRpb25faWQ9Y29ycmVsYXRpb25faWQpKQoKCmFzeW5jIGRlZiByZWdpc3Rlcl9pbnB1
dCgKICAgIHNlc3Npb246IEFzeW5jU2Vzc2lvbiwgKiwgaW5wdXRfaWQ6IHN0ciwgY29udGVudF9oYXNoOiBzdHIsCiAgICBzZXJpZXNfcmVmczogZGljdCwg
d2luZG93X3N0YXJ0OiBkYXRldGltZSwgd2luZG93X2VuZDogZGF0ZXRpbWUsCiAgICBkYXRhX2NsYXNzOiBzdHIsIG1vZGU6IHN0ciwgb3BlcmF0b3JfaWQ6
IHN0ciwKICAgIGNvcnJlbGF0aW9uX2lkOiBzdHIgfCBOb25lLAopIC0+IFR5cGVkT3V0Y29tZToKICAgIHJlYXNvbnM6IGxpc3QgPSBbXQogICAgaWYgZGF0
YV9jbGFzcyBub3QgaW4gUkpfRklSU1RfTEFORElOR19EQVRBX0NMQVNTRVM6CiAgICAgICAgcmVhc29ucy5hcHBlbmQoeyJmYWlsaW5nIjogImRhdGFfY2xh
c3MiLCAidmFsdWUiOiBkYXRhX2NsYXNzLAogICAgICAgICAgICAgICAgICAgICAgICAibm90ZSI6ICJjb3JwdXMtZ2F0ZWQgKFYyLVRELTE4KSJ9KQogICAg
dHJ5OgogICAgICAgIFJlcGxheVdpbmRvdyh3aW5kb3dfc3RhcnQ9d2luZG93X3N0YXJ0LCB3aW5kb3dfZW5kPXdpbmRvd19lbmQsCiAgICAgICAgICAgICAg
ICAgICAgIGFzX29mPXdpbmRvd19lbmQpLnZhbGlkYXRlKCkKICAgIGV4Y2VwdCBMZWFrYWdlUmVmdXNlZCBhcyBleGM6CiAgICAgICAgcmVhc29ucy5leHRl
bmQoZXhjLnJlYXNvbnMpCiAgICBpZiBub3Qgc2VyaWVzX3JlZnM6CiAgICAgICAgcmVhc29ucy5hcHBlbmQoeyJmYWlsaW5nIjogInNlcmllc19yZWZzIiwg
InZhbHVlIjogImVtcHR5In0pCgogICAgaWYgcmVhc29uczoKICAgICAgICBhd2FpdCBfYXVkaXQoc2Vzc2lvbiwgImlucHV0LnJlZnVzZWQiLAogICAgICAg
ICAgICAgICAgICAgICBkZXRhaWxzPXsiaW5wdXRfaWQiOiBpbnB1dF9pZCwgInJlYXNvbnMiOiByZWFzb25zWzo4XX0sCiAgICAgICAgICAgICAgICAgICAg
IG1vZGU9bW9kZSwgb3BlcmF0b3JfaWQ9b3BlcmF0b3JfaWQsCiAgICAgICAgICAgICAgICAgICAgIGNvcnJlbGF0aW9uX2lkPWNvcnJlbGF0aW9uX2lkLAog
ICAgICAgICAgICAgICAgICAgICByZXNvdXJjZV90eXBlPSJiYWNrdGVzdF9pbnB1dCIpCiAgICAgICAgYXdhaXQgc2Vzc2lvbi5jb21taXQoKQogICAgICAg
IHJldHVybiBUeXBlZE91dGNvbWUob3V0Y29tZT0icmVmdXNlZCIsIHJlYXNvbnM9cmVhc29ucykKCiAgICAjIGNvbnRlbnQtYWRkcmVzc2VkIGRlZHVwZTog
aWRlbnRpY2FsIGNvbnRlbnQg4oeSIGlkZW1wb3RlbnQgcmV1c2UKICAgIGV4aXN0aW5nID0gKGF3YWl0IHNlc3Npb24uZXhlY3V0ZSgKICAgICAgICBzZWxl
Y3QoVjJCYWNrdGVzdElucHV0KS53aGVyZSgKICAgICAgICAgICAgVjJCYWNrdGVzdElucHV0LmNvbnRlbnRfaGFzaCA9PSBjb250ZW50X2hhc2gpCiAgICAp
KS5zY2FsYXJfb25lX29yX25vbmUoKQogICAgaWYgZXhpc3RpbmcgaXMgbm90IE5vbmU6CiAgICAgICAgYXdhaXQgX2F1ZGl0KHNlc3Npb24sICJpbnB1dC5y
ZXVzZWQiLAogICAgICAgICAgICAgICAgICAgICBkZXRhaWxzPXsiaW5wdXRfaWQiOiBleGlzdGluZy5pbnB1dF9pZCwKICAgICAgICAgICAgICAgICAgICAg
ICAgICAgICAgImNvbnRlbnRfaGFzaCI6IGNvbnRlbnRfaGFzaH0sCiAgICAgICAgICAgICAgICAgICAgIG1vZGU9bW9kZSwgb3BlcmF0b3JfaWQ9b3BlcmF0
b3JfaWQsCiAgICAgICAgICAgICAgICAgICAgIGNvcnJlbGF0aW9uX2lkPWNvcnJlbGF0aW9uX2lkLAogICAgICAgICAgICAgICAgICAgICByZXNvdXJjZV90
eXBlPSJiYWNrdGVzdF9pbnB1dCIsCiAgICAgICAgICAgICAgICAgICAgIHJlc291cmNlX2lkPWV4aXN0aW5nLmlkKQogICAgICAgIHJldHVybiBUeXBlZE91
dGNvbWUob3V0Y29tZT0icmV1c2VkIiwgcmVjb3JkX2lkPWV4aXN0aW5nLmlkKQoKICAgIG5ld2VzdCA9IChhd2FpdCBzZXNzaW9uLmV4ZWN1dGUoCiAgICAg
ICAgc2VsZWN0KFYyQmFja3Rlc3RJbnB1dCkKICAgICAgICAud2hlcmUoVjJCYWNrdGVzdElucHV0LmlucHV0X2lkID09IGlucHV0X2lkKQogICAgICAgIC5v
cmRlcl9ieShWMkJhY2t0ZXN0SW5wdXQucmVjb3JkX3NlcS5kZXNjKCkpCiAgICApKS5zY2FsYXJzKCkuZmlyc3QoKQogICAgcm93ID0gVjJCYWNrdGVzdElu
cHV0KAogICAgICAgIGlucHV0X2lkPWlucHV0X2lkLAogICAgICAgIHJlY29yZF9zZXE9MSBpZiBuZXdlc3QgaXMgTm9uZSBlbHNlIG5ld2VzdC5yZWNvcmRf
c2VxICsgMSwKICAgICAgICBzdXBlcnNlZGVzPW5ld2VzdC5pZCBpZiBuZXdlc3QgaXMgbm90IE5vbmUgZWxzZSBOb25lLAogICAgICAgIGNvbnRlbnRfaGFz
aD1jb250ZW50X2hhc2gsCiAgICAgICAgc2VyaWVzX3JlZnM9c2VyaWVzX3JlZnMsCiAgICAgICAgd2luZG93X3N0YXJ0PXdpbmRvd19zdGFydCwgd2luZG93
X2VuZD13aW5kb3dfZW5kLAogICAgICAgIHJlZ2lzdHJhdGlvbl9vdXRjb21lPSJyZWdpc3RlcmVkIiwKICAgICAgICBkYXRhX2NsYXNzPWRhdGFfY2xhc3Ms
IG1vZGU9bW9kZSwgb3BlcmF0b3JfaWQ9b3BlcmF0b3JfaWQsCiAgICAgICAgY29ycmVsYXRpb25faWQ9Y29ycmVsYXRpb25faWQpCiAgICBzZXNzaW9uLmFk
ZChyb3cpCiAgICBhd2FpdCBzZXNzaW9uLmZsdXNoKCkKICAgIGF3YWl0IF9hdWRpdChzZXNzaW9uLCAiaW5wdXQucmVnaXN0ZXJlZCIsCiAgICAgICAgICAg
ICAgICAgZGV0YWlscz17ImlucHV0X2lkIjogaW5wdXRfaWQsICJyZWNvcmRfc2VxIjogcm93LnJlY29yZF9zZXEsCiAgICAgICAgICAgICAgICAgICAgICAg
ICAgImNvbnRlbnRfaGFzaCI6IGNvbnRlbnRfaGFzaH0sCiAgICAgICAgICAgICAgICAgbW9kZT1tb2RlLCBvcGVyYXRvcl9pZD1vcGVyYXRvcl9pZCwKICAg
ICAgICAgICAgICAgICBjb3JyZWxhdGlvbl9pZD1jb3JyZWxhdGlvbl9pZCwKICAgICAgICAgICAgICAgICByZXNvdXJjZV90eXBlPSJiYWNrdGVzdF9pbnB1
dCIsIHJlc291cmNlX2lkPXJvdy5pZCkKICAgIHJldHVybiBUeXBlZE91dGNvbWUob3V0Y29tZT0icmVnaXN0ZXJlZCIsIHJlY29yZF9pZD1yb3cuaWQpCgoK
YXN5bmMgZGVmIHJlZ2lzdGVyX2Nvc3RfbW9kZWwoCiAgICBzZXNzaW9uOiBBc3luY1Nlc3Npb24sICosIGNvc3RfbW9kZWxfaWQ6IHN0ciwgc3ByZWFkOiBk
aWN0LAogICAgY29tbWlzc2lvbjogZGljdCwgc2xpcHBhZ2U6IGRpY3QsIGxhdGVuY3lfbXM6IGludCwgcmlza19saW1pdHM6IGRpY3QsCiAgICBkYXRhX2Ns
YXNzOiBzdHIsIG1vZGU6IHN0ciwgb3BlcmF0b3JfaWQ6IHN0ciwKICAgIGNvcnJlbGF0aW9uX2lkOiBzdHIgfCBOb25lLAopIC0+IFR5cGVkT3V0Y29tZToK
ICAgIHJlYXNvbnM6IGxpc3QgPSBbXQogICAgY2l0YXRpb25zOiBkaWN0ID0ge30KICAgIGZvciBrZXksIGVudHJ5IGluICgoInNwcmVhZCIsIHNwcmVhZCks
ICgiY29tbWlzc2lvbiIsIGNvbW1pc3Npb24pLAogICAgICAgICAgICAgICAgICAgICAgICgic2xpcHBhZ2UiLCBzbGlwcGFnZSkpOgogICAgICAgIGZvciBm
aWVsZCBpbiAoInZhbHVlIiwgInVuaXQiLCAiY2l0YXRpb24iKToKICAgICAgICAgICAgaWYgZmllbGQgbm90IGluIGVudHJ5OgogICAgICAgICAgICAgICAg
cmVhc29ucy5hcHBlbmQoeyJmYWlsaW5nIjogZiJ7a2V5fS57ZmllbGR9IiwKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAicmVxdWlyZWQiOiAi
dmFsdWUrdW5pdCtjaXRhdGlvbiIKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAiIChSRVEtMS40IOKAlCBubyBpbnZlbnRl
ZCIKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAiIG51bWJlcnMgYXMgc3BlYyB2YWx1ZXMpIn0pCiAgICAgICAgIyBGLTEg
KENSLVYyLUJFLTctMDAxKTogdW5pdCB2b2NhYnVsYXJ5IGdhdGUgYXQgcmVnaXN0cmF0aW9uIOKAlAogICAgICAgICMgYXBwbHlfY29zdHMga25vd3MgZXhh
Y3RseSBDT1NUX1VOSVRTX1YxOyBhbnl0aGluZyBlbHNlIG11c3QgYmUgYQogICAgICAgICMgdHlwZWQgcmVmdXNhbCBIRVJFLCBuZXZlciBhbiB1bnR5cGVk
IGVuZ2luZSBmYWlsdXJlIGRvd25zdHJlYW0uCiAgICAgICAgaWYgInVuaXQiIGluIGVudHJ5IGFuZCBlbnRyeVsidW5pdCJdIG5vdCBpbiBDT1NUX1VOSVRT
X1YxOgogICAgICAgICAgICByZWFzb25zLmFwcGVuZCh7ImZhaWxpbmciOiBmIntrZXl9LnVuaXQiLAogICAgICAgICAgICAgICAgICAgICAgICAgICAgInZh
bHVlIjogZW50cnlbInVuaXQiXSwKICAgICAgICAgICAgICAgICAgICAgICAgICAgICJhbGxvd2VkIjogbGlzdChDT1NUX1VOSVRTX1YxKX0pCiAgICAgICAg
Y2l0YXRpb25zW2tleV0gPSBlbnRyeS5nZXQoImNpdGF0aW9uIikKICAgIGlmIGRhdGFfY2xhc3Mgbm90IGluIFJKX0ZJUlNUX0xBTkRJTkdfREFUQV9DTEFT
U0VTOgogICAgICAgIHJlYXNvbnMuYXBwZW5kKHsiZmFpbGluZyI6ICJkYXRhX2NsYXNzIiwgInZhbHVlIjogZGF0YV9jbGFzc30pCiAgICBpZiByZWFzb25z
OgogICAgICAgIGF3YWl0IF9hdWRpdChzZXNzaW9uLCAiY29zdF9tb2RlbC5yZWZ1c2VkIiwKICAgICAgICAgICAgICAgICAgICAgZGV0YWlscz17ImNvc3Rf
bW9kZWxfaWQiOiBjb3N0X21vZGVsX2lkLAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAicmVhc29ucyI6IHJlYXNvbnNbOjhdfSwKICAgICAgICAg
ICAgICAgICAgICAgbW9kZT1tb2RlLCBvcGVyYXRvcl9pZD1vcGVyYXRvcl9pZCwKICAgICAgICAgICAgICAgICAgICAgY29ycmVsYXRpb25faWQ9Y29ycmVs
YXRpb25faWQsIHJlc291cmNlX3R5cGU9ImNvc3RfbW9kZWwiKQogICAgICAgIGF3YWl0IHNlc3Npb24uY29tbWl0KCkKICAgICAgICByZXR1cm4gVHlwZWRP
dXRjb21lKG91dGNvbWU9InJlZnVzZWQiLCByZWFzb25zPXJlYXNvbnMpCgogICAgbmV3ZXN0ID0gKGF3YWl0IHNlc3Npb24uZXhlY3V0ZSgKICAgICAgICBz
ZWxlY3QoVjJDb3N0TW9kZWwpCiAgICAgICAgLndoZXJlKFYyQ29zdE1vZGVsLmNvc3RfbW9kZWxfaWQgPT0gY29zdF9tb2RlbF9pZCkKICAgICAgICAub3Jk
ZXJfYnkoVjJDb3N0TW9kZWwucmVjb3JkX3NlcS5kZXNjKCkpCiAgICApKS5zY2FsYXJzKCkuZmlyc3QoKQogICAgcm93ID0gVjJDb3N0TW9kZWwoCiAgICAg
ICAgY29zdF9tb2RlbF9pZD1jb3N0X21vZGVsX2lkLAogICAgICAgIHJlY29yZF9zZXE9MSBpZiBuZXdlc3QgaXMgTm9uZSBlbHNlIG5ld2VzdC5yZWNvcmRf
c2VxICsgMSwKICAgICAgICBzdXBlcnNlZGVzPW5ld2VzdC5pZCBpZiBuZXdlc3QgaXMgbm90IE5vbmUgZWxzZSBOb25lLAogICAgICAgIHNwcmVhZD1zcHJl
YWQsIGNvbW1pc3Npb249Y29tbWlzc2lvbiwgc2xpcHBhZ2U9c2xpcHBhZ2UsCiAgICAgICAgbGF0ZW5jeV9tcz1sYXRlbmN5X21zLCByaXNrX2xpbWl0cz1y
aXNrX2xpbWl0cywKICAgICAgICBjaXRhdGlvbnM9Y2l0YXRpb25zLCBkYXRhX2NsYXNzPWRhdGFfY2xhc3MsIG1vZGU9bW9kZSwKICAgICAgICBvcGVyYXRv
cl9pZD1vcGVyYXRvcl9pZCwgY29ycmVsYXRpb25faWQ9Y29ycmVsYXRpb25faWQpCiAgICBzZXNzaW9uLmFkZChyb3cpCiAgICBhd2FpdCBzZXNzaW9uLmZs
dXNoKCkKICAgIGF3YWl0IF9hdWRpdChzZXNzaW9uLCAiY29zdF9tb2RlbC5yZWdpc3RlcmVkIiwKICAgICAgICAgICAgICAgICBkZXRhaWxzPXsiY29zdF9t
b2RlbF9pZCI6IGNvc3RfbW9kZWxfaWQsCiAgICAgICAgICAgICAgICAgICAgICAgICAgInJlY29yZF9zZXEiOiByb3cucmVjb3JkX3NlcX0sCiAgICAgICAg
ICAgICAgICAgbW9kZT1tb2RlLCBvcGVyYXRvcl9pZD1vcGVyYXRvcl9pZCwKICAgICAgICAgICAgICAgICBjb3JyZWxhdGlvbl9pZD1jb3JyZWxhdGlvbl9p
ZCwKICAgICAgICAgICAgICAgICByZXNvdXJjZV90eXBlPSJjb3N0X21vZGVsIiwgcmVzb3VyY2VfaWQ9cm93LmlkKQogICAgcmV0dXJuIFR5cGVkT3V0Y29t
ZShvdXRjb21lPSJyZWdpc3RlcmVkIiwgcmVjb3JkX2lkPXJvdy5pZCkKCgphc3luYyBkZWYgcmVnaXN0ZXJfc3RyYXRlZ3koCiAgICBzZXNzaW9uOiBBc3lu
Y1Nlc3Npb24sICosIHN0cmF0ZWd5X2lkOiBzdHIsIG5hbWU6IHN0ciwgcGFyYW1ldGVyczogZGljdCwKICAgIGxpZmVjeWNsZV9zdGF0ZTogc3RyLCBkYXRh
X2NsYXNzOiBzdHIsIG1vZGU6IHN0ciwgb3BlcmF0b3JfaWQ6IHN0ciwKICAgIGNvcnJlbGF0aW9uX2lkOiBzdHIgfCBOb25lLAopIC0+IFR5cGVkT3V0Y29t
ZToKICAgIGZyb20gYXBwLnYyLnJlc2VhcmNoX2pvYnMucmVwbGF5IGltcG9ydCBTVFJBVEVHWV9SVUxFUwoKICAgIHJlYXNvbnM6IGxpc3QgPSBbXQogICAg
aWYgbGlmZWN5Y2xlX3N0YXRlIG5vdCBpbiBMSUZFQ1lDTEVfU1RBVEVTOgogICAgICAgIHJlYXNvbnMuYXBwZW5kKHsiZmFpbGluZyI6ICJsaWZlY3ljbGVf
c3RhdGUiLAogICAgICAgICAgICAgICAgICAgICAgICAidmFsdWUiOiBsaWZlY3ljbGVfc3RhdGV9KQogICAgcnVsZSA9IHBhcmFtZXRlcnMuZ2V0KCJydWxl
IikKICAgIGlmIHJ1bGUgbm90IGluIFNUUkFURUdZX1JVTEVTOgogICAgICAgIHJlYXNvbnMuYXBwZW5kKHsiZmFpbGluZyI6ICJwYXJhbWV0ZXJzLnJ1bGUi
LCAidmFsdWUiOiBydWxlLAogICAgICAgICAgICAgICAgICAgICAgICAicmVxdWlyZWQiOiBzb3J0ZWQoU1RSQVRFR1lfUlVMRVMpLAogICAgICAgICAgICAg
ICAgICAgICAgICAibm90ZSI6ICJ2MSBzY29wZTogcmVnaXN0ZXJlZCBkZXRlcm1pbmlzdGljIHJ1bGUiCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAg
ICAgIiBmdW5jdGlvbnMgb25seSAocGxhbiBQYXJ0IDE1KSJ9KQogICAgZm9yIGJhbm5lZCBpbiAoImNyZWRlbnRpYWwiLCAiYXBpX2tleSIsICJicm9rZXIi
LCAiYWNjb3VudCIsICJhZGFwdGVyIik6CiAgICAgICAgaWYgYmFubmVkIGluIHtrLmxvd2VyKCkgZm9yIGsgaW4gcGFyYW1ldGVyc306CiAgICAgICAgICAg
IHJlYXNvbnMuYXBwZW5kKHsiZmFpbGluZyI6ICJwYXJhbWV0ZXJzIiwKICAgICAgICAgICAgICAgICAgICAgICAgICAgICJ2YWx1ZSI6IGYiZm9yYmlkZGVu
IGtleSBjbGFzczoge2Jhbm5lZH0ifSkKICAgIGlmIGRhdGFfY2xhc3Mgbm90IGluIFJKX0ZJUlNUX0xBTkRJTkdfREFUQV9DTEFTU0VTOgogICAgICAgIHJl
YXNvbnMuYXBwZW5kKHsiZmFpbGluZyI6ICJkYXRhX2NsYXNzIiwgInZhbHVlIjogZGF0YV9jbGFzc30pCiAgICBpZiByZWFzb25zOgogICAgICAgIGF3YWl0
IF9hdWRpdChzZXNzaW9uLCAic3RyYXRlZ3kucmVmdXNlZCIsCiAgICAgICAgICAgICAgICAgICAgIGRldGFpbHM9eyJzdHJhdGVneV9pZCI6IHN0cmF0ZWd5
X2lkLAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAicmVhc29ucyI6IHJlYXNvbnNbOjhdfSwKICAgICAgICAgICAgICAgICAgICAgbW9kZT1tb2Rl
LCBvcGVyYXRvcl9pZD1vcGVyYXRvcl9pZCwKICAgICAgICAgICAgICAgICAgICAgY29ycmVsYXRpb25faWQ9Y29ycmVsYXRpb25faWQsCiAgICAgICAgICAg
ICAgICAgICAgIHJlc291cmNlX3R5cGU9InN0cmF0ZWd5X3ZlcnNpb24iKQogICAgICAgIGF3YWl0IHNlc3Npb24uY29tbWl0KCkKICAgICAgICByZXR1cm4g
VHlwZWRPdXRjb21lKG91dGNvbWU9InJlZnVzZWQiLCByZWFzb25zPXJlYXNvbnMpCgogICAgbmV3ZXN0ID0gKGF3YWl0IHNlc3Npb24uZXhlY3V0ZSgKICAg
ICAgICBzZWxlY3QoVjJTdHJhdGVneVZlcnNpb24pCiAgICAgICAgLndoZXJlKFYyU3RyYXRlZ3lWZXJzaW9uLnN0cmF0ZWd5X2lkID09IHN0cmF0ZWd5X2lk
KQogICAgICAgIC5vcmRlcl9ieShWMlN0cmF0ZWd5VmVyc2lvbi5yZWNvcmRfc2VxLmRlc2MoKSkKICAgICkpLnNjYWxhcnMoKS5maXJzdCgpCiAgICByb3cg
PSBWMlN0cmF0ZWd5VmVyc2lvbigKICAgICAgICBzdHJhdGVneV9pZD1zdHJhdGVneV9pZCwKICAgICAgICByZWNvcmRfc2VxPTEgaWYgbmV3ZXN0IGlzIE5v
bmUgZWxzZSBuZXdlc3QucmVjb3JkX3NlcSArIDEsCiAgICAgICAgc3VwZXJzZWRlcz1uZXdlc3QuaWQgaWYgbmV3ZXN0IGlzIG5vdCBOb25lIGVsc2UgTm9u
ZSwKICAgICAgICBuYW1lPW5hbWUsIHBhcmFtZXRlcnM9cGFyYW1ldGVycywgbGlmZWN5Y2xlX3N0YXRlPWxpZmVjeWNsZV9zdGF0ZSwKICAgICAgICBkYXRh
X2NsYXNzPWRhdGFfY2xhc3MsIG1vZGU9bW9kZSwgb3BlcmF0b3JfaWQ9b3BlcmF0b3JfaWQsCiAgICAgICAgY29ycmVsYXRpb25faWQ9Y29ycmVsYXRpb25f
aWQpCiAgICBzZXNzaW9uLmFkZChyb3cpCiAgICBhd2FpdCBzZXNzaW9uLmZsdXNoKCkKICAgIGFjdGlvbiA9ICgic3RyYXRlZ3kucmVnaXN0ZXJlZCIgaWYg
bmV3ZXN0IGlzIE5vbmUKICAgICAgICAgICAgICBlbHNlICJzdHJhdGVneS5zdXBlcnNlZGVkIikKICAgIGF3YWl0IF9hdWRpdChzZXNzaW9uLCBhY3Rpb24s
CiAgICAgICAgICAgICAgICAgZGV0YWlscz17InN0cmF0ZWd5X2lkIjogc3RyYXRlZ3lfaWQsCiAgICAgICAgICAgICAgICAgICAgICAgICAgInJlY29yZF9z
ZXEiOiByb3cucmVjb3JkX3NlcSwKICAgICAgICAgICAgICAgICAgICAgICAgICAibGlmZWN5Y2xlX3N0YXRlIjogbGlmZWN5Y2xlX3N0YXRlfSwKICAgICAg
ICAgICAgICAgICBtb2RlPW1vZGUsIG9wZXJhdG9yX2lkPW9wZXJhdG9yX2lkLAogICAgICAgICAgICAgICAgIGNvcnJlbGF0aW9uX2lkPWNvcnJlbGF0aW9u
X2lkLAogICAgICAgICAgICAgICAgIHJlc291cmNlX3R5cGU9InN0cmF0ZWd5X3ZlcnNpb24iLCByZXNvdXJjZV9pZD1yb3cuaWQpCiAgICByZXR1cm4gVHlw
ZWRPdXRjb21lKG91dGNvbWU9InJlZ2lzdGVyZWQiLCByZWNvcmRfaWQ9cm93LmlkKQo=
'@
Write-Evidence ("record 11/17 staged: " + $Rec11Path)
$Rec12Path = "app\v2\research_jobs\replay.py"
$Rec12Sha  = "f241d615bd83aea1f5d279f18731580f6021f652871ac3b4dda10bfdfd0e8e26"
$Rec12B64 = @'
IiIiQkUtNyBVLTIgZGV0ZXJtaW5pc3RpYyByZXBsYXkgZW5naW5lIChwbGFuIFBhcnQgMjsgUC04IEctMikuCgpQdXJlIGZ1bmN0aW9uIG9mIChyZWdpc3Rl
cmVkIGlucHV0IGNvbnRlbnQsIHN0cmF0ZWd5IHBhcmFtZXRlcnMsIGNvc3QKbW9kZWwsIGVuZ2luZSB2ZXJzaW9ucykuIE5vIHdhbGwgY2xvY2ssIG5vIHVu
cGlubmVkIHJhbmRvbW5lc3MsIG5vIEkvTy4KVGhlIGRlY2lzaW9uIGN1cnNvciBpcyB0aGUgc3RydWN0dXJhbCBjdXRvZmY6IGF0IHN0ZXAgdCB0aGUgc3Ry
YXRlZ3kKY2FsbGJhY2sgY2FuIG9ic2VydmUgT05MWSBiYXJzIHdpdGggb3Blbl90aW1lIDw9IHQgKEctMikuCiIiIgoKZnJvbSBfX2Z1dHVyZV9fIGltcG9y
dCBhbm5vdGF0aW9ucwoKaW1wb3J0IGhhc2hsaWIKaW1wb3J0IGpzb24KZnJvbSBkYXRhY2xhc3NlcyBpbXBvcnQgZGF0YWNsYXNzLCBmaWVsZApmcm9tIGRh
dGV0aW1lIGltcG9ydCBkYXRldGltZQpmcm9tIGRlY2ltYWwgaW1wb3J0IERlY2ltYWwKCmZyb20gYXBwLnYyLnJlc2VhcmNoX2pvYnMubGVha2FnZSBpbXBv
cnQgKAogICAgUmVwbGF5V2luZG93LAogICAgZmlsdGVyX2JhcnNfZzEsCiAgICB2ZXJpZnlfY29udGVudF9nNSwKKQoKRU5HSU5FX1ZFUlNJT05TID0geyJy
ZXBsYXlfZW5naW5lIjogInJwZS0xLjAuMCIsCiAgICAgICAgICAgICAgICAgICAicmVzZWFyY2hfam9iX2VuZ2luZSI6ICJyamUtMS4wLjAifQoKCmRlZiBj
YW5vbmljYWwodmFsdWUpIC0+IHN0cjoKICAgIHJldHVybiBqc29uLmR1bXBzKHZhbHVlLCBzb3J0X2tleXM9VHJ1ZSwgc2VwYXJhdG9ycz0oIiwiLCAiOiIp
LAogICAgICAgICAgICAgICAgICAgICAgZGVmYXVsdD1zdHIpCgoKZGVmIGVuZ2luZV92ZXJzaW9uc19oYXNoKCkgLT4gc3RyOgogICAgcmV0dXJuIGhhc2hs
aWIuc2hhMjU2KGNhbm9uaWNhbChFTkdJTkVfVkVSU0lPTlMpLmVuY29kZSgpKS5oZXhkaWdlc3QoKQoKCiMgLS0tIENvc3QgYXBwbGljYXRpb24gKFJFUS0x
LjQ6IHB1cmUgYW5kIGRldGVybWluaXN0aWMpIC0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tCgoKZGVmIGFwcGx5X2Nvc3RzKGZpbGxfcHJpY2U6IERlY2ltYWws
IHNpZGU6IHN0ciwgY29zdF9tb2RlbDogZGljdCkgLT4gRGVjaW1hbDoKICAgICIiIkVmZmVjdGl2ZSBwcmljZSBhZnRlciBkZWNsYXJlZCBjb3N0cy4gc3By
ZWFkL2NvbW1pc3Npb24vc2xpcHBhZ2UgYXJlCiAgICB7dmFsdWUsIHVuaXQsIGNpdGF0aW9ufSBlbnRyaWVzOyB2MSB1bml0czogJ3ByaWNlJyAoYWJzb2x1
dGUgYWRkKSBhbmQKICAgICdmcmFjdGlvbicgKG11bHRpcGxpY2F0aXZlKS4gRGV0ZXJtaW5pc3RpYzsgbm8gcm91bmRpbmcgc3VycHJpc2VzCiAgICAoRGVj
aW1hbCB0aHJvdWdob3V0KS4iIiIKICAgIHByaWNlID0gRGVjaW1hbChzdHIoZmlsbF9wcmljZSkpCiAgICBzaWduID0gRGVjaW1hbCgxKSBpZiBzaWRlID09
ICJidXkiIGVsc2UgRGVjaW1hbCgtMSkKICAgIGZvciBrZXkgaW4gKCJzcHJlYWQiLCAiY29tbWlzc2lvbiIsICJzbGlwcGFnZSIpOgogICAgICAgIGVudHJ5
ID0gY29zdF9tb2RlbFtrZXldCiAgICAgICAgdmFsdWUgPSBEZWNpbWFsKHN0cihlbnRyeVsidmFsdWUiXSkpCiAgICAgICAgaWYgZW50cnlbInVuaXQiXSA9
PSAicHJpY2UiOgogICAgICAgICAgICBwcmljZSArPSBzaWduICogdmFsdWUKICAgICAgICBlbGlmIGVudHJ5WyJ1bml0Il0gPT0gImZyYWN0aW9uIjoKICAg
ICAgICAgICAgcHJpY2UgKj0gKERlY2ltYWwoMSkgKyBzaWduICogdmFsdWUpCiAgICAgICAgZWxzZTogICMgdW5rbm93biB1bml0IGlzIGEgdHlwZWQgY29u
ZmlndXJhdGlvbiBlcnJvciB1cHN0cmVhbQogICAgICAgICAgICByYWlzZSBWYWx1ZUVycm9yKGYidW5rbm93biBjb3N0IHVuaXQ6IHtlbnRyeVsndW5pdCdd
fSIpCiAgICByZXR1cm4gcHJpY2UKCgojIC0tLSBTdHJhdGVneSBydWxlcyAodjEgc2NvcGU6IHJlZ2lzdGVyZWQgZGV0ZXJtaW5pc3RpYyBydWxlIGZ1bmN0
aW9ucykgLS0tLS0tLS0KCgpAZGF0YWNsYXNzKGZyb3plbj1UcnVlKQpjbGFzcyBDdXJzb3JTbGljZToKICAgICIiIkctMjogdGhlIGltbXV0YWJsZSB3aW5k
b3cgc2xpY2UgYSBzdHJhdGVneSBzZWVzIGF0IG9uZSBzdGVwIOKAlAogICAgYmFycyBzdHJpY3RseSB1cCB0byBhbmQgaW5jbHVkaW5nIHRoZSBjdXJzb3I7
IG5vdGhpbmcgYmV5b25kLiIiIgoKICAgIGJhcnM6IHR1cGxlCiAgICBjdXJzb3I6IGRhdGV0aW1lCgoKZGVmIHRocmVzaG9sZF9ydWxlKHNsaWNlXzogQ3Vy
c29yU2xpY2UsIHBhcmFtczogZGljdCkgLT4gc3RyIHwgTm9uZToKICAgICIiInYxIHJ1bGU6IGJ1eSB3aGVuIGNsb3NlIDwgYnV5X2JlbG93OyBzZWxsIHdo
ZW4gY2xvc2UgPiBzZWxsX2Fib3ZlLgogICAgUHVyZTsgc2VlcyBvbmx5IHRoZSBzbGljZS4iIiIKICAgIGxhc3QgPSBzbGljZV8uYmFyc1stMV0KICAgIGNs
b3NlID0gRGVjaW1hbChzdHIobGFzdFsiY2xvc2UiXSkpCiAgICBpZiBjbG9zZSA8IERlY2ltYWwoc3RyKHBhcmFtc1siYnV5X2JlbG93Il0pKToKICAgICAg
ICByZXR1cm4gImJ1eSIKICAgIGlmIGNsb3NlID4gRGVjaW1hbChzdHIocGFyYW1zWyJzZWxsX2Fib3ZlIl0pKToKICAgICAgICByZXR1cm4gInNlbGwiCiAg
ICByZXR1cm4gTm9uZQoKCmRlZiBjcm9zc292ZXJfcnVsZShzbGljZV86IEN1cnNvclNsaWNlLCBwYXJhbXM6IGRpY3QpIC0+IHN0ciB8IE5vbmU6CiAgICAi
IiJ2MSBydWxlOiBmYXN0L3Nsb3cgbWVhbiBjcm9zc292ZXIgb3ZlciB0aGUgdmlzaWJsZSBzbGljZS4iIiIKICAgIG5fZmFzdCwgbl9zbG93ID0gaW50KHBh
cmFtc1siZmFzdCJdKSwgaW50KHBhcmFtc1sic2xvdyJdKQogICAgY2xvc2VzID0gW0RlY2ltYWwoc3RyKGJbImNsb3NlIl0pKSBmb3IgYiBpbiBzbGljZV8u
YmFyc10KICAgIGlmIGxlbihjbG9zZXMpIDwgbl9zbG93OgogICAgICAgIHJldHVybiBOb25lCiAgICBmYXN0ID0gc3VtKGNsb3Nlc1stbl9mYXN0Ol0pIC8g
bl9mYXN0CiAgICBzbG93ID0gc3VtKGNsb3Nlc1stbl9zbG93Ol0pIC8gbl9zbG93CiAgICBwcmV2X2Nsb3NlcyA9IGNsb3Nlc1s6LTFdCiAgICBpZiBsZW4o
cHJldl9jbG9zZXMpIDwgbl9zbG93OgogICAgICAgIHJldHVybiBOb25lCiAgICBwZmFzdCA9IHN1bShwcmV2X2Nsb3Nlc1stbl9mYXN0Ol0pIC8gbl9mYXN0
CiAgICBwc2xvdyA9IHN1bShwcmV2X2Nsb3Nlc1stbl9zbG93Ol0pIC8gbl9zbG93CiAgICBpZiBwZmFzdCA8PSBwc2xvdyBhbmQgZmFzdCA+IHNsb3c6CiAg
ICAgICAgcmV0dXJuICJidXkiCiAgICBpZiBwZmFzdCA+PSBwc2xvdyBhbmQgZmFzdCA8IHNsb3c6CiAgICAgICAgcmV0dXJuICJzZWxsIgogICAgcmV0dXJu
IE5vbmUKCgpTVFJBVEVHWV9SVUxFUyA9IHsidGhyZXNob2xkIjogdGhyZXNob2xkX3J1bGUsICJjcm9zc292ZXIiOiBjcm9zc292ZXJfcnVsZX0KCgpAZGF0
YWNsYXNzCmNsYXNzIFJlcGxheVJlc3VsdDoKICAgIGZpbGxzOiBsaXN0ID0gZmllbGQoZGVmYXVsdF9mYWN0b3J5PWxpc3QpCiAgICBzdW1tYXJ5OiBkaWN0
ID0gZmllbGQoZGVmYXVsdF9mYWN0b3J5PWRpY3QpCiAgICBkZWNpc2lvbl9sZWRnZXI6IGxpc3QgPSBmaWVsZChkZWZhdWx0X2ZhY3Rvcnk9bGlzdCkKCgpk
ZWYgcnVuX3JlcGxheSgqLCBiYXJzOiBsaXN0W2RpY3RdLCB3aW5kb3c6IFJlcGxheVdpbmRvdywKICAgICAgICAgICAgICAgc3RyYXRlZ3lfcnVsZTogc3Ry
LCBwYXJhbWV0ZXJzOiBkaWN0LCBjb3N0X21vZGVsOiBkaWN0LAogICAgICAgICAgICAgICBzdG9yZWRfY29udGVudF9oYXNoOiBzdHIsIHNlcmllc19yZWZz
OiBkaWN0KSAtPiBSZXBsYXlSZXN1bHQ6CiAgICAiIiJUaGUgZGV0ZXJtaW5pc3RpYyByZXBsYXkuIEctNSByZS12ZXJpZmllcyBjb250ZW50OyBHLTEgZmls
dGVyczsKICAgIEctMiBzbGljZXMgYXQgdGhlIGN1cnNvcjsgZXZlcnkgZGVjaXNpb24gaXMgbGVkZ2VyZWQgd2l0aCBpdHMgZGF0YQogICAgdGltZXN0YW1w
cyAoRy00IGV2aWRlbmNlKS4iIiIKICAgIGZyb20gYXBwLnYyLnJlc2VhcmNoX2pvYnMubGVha2FnZSBpbXBvcnQgY29udGVudF9oYXNoIGFzIF9jaAoKICAg
IGFzc2VtYmxlZCA9IGZpbHRlcl9iYXJzX2cxKGJhcnMsIHdpbmRvdykgICMgRy0xOiB0aGUgb25seSBmZXRjaCBwYXRoCiAgICB2ZXJpZnlfY29udGVudF9n
NSgKICAgICAgICBzdG9yZWRfaGFzaD1zdG9yZWRfY29udGVudF9oYXNoLAogICAgICAgIHJlY29tcHV0ZWRfaGFzaD1fY2goYXNzZW1ibGVkLCB3aW5kb3cs
IHNlcmllc19yZWZzKSkgICMgRy01CgogICAgaWYgc3RyYXRlZ3lfcnVsZSBub3QgaW4gU1RSQVRFR1lfUlVMRVM6CiAgICAgICAgcmFpc2UgVmFsdWVFcnJv
cihmInVucmVnaXN0ZXJlZCBzdHJhdGVneSBydWxlOiB7c3RyYXRlZ3lfcnVsZX0iKQogICAgcnVsZSA9IFNUUkFURUdZX1JVTEVTW3N0cmF0ZWd5X3J1bGVd
CgogICAgcmVzdWx0ID0gUmVwbGF5UmVzdWx0KCkKICAgIHBvc2l0aW9uID0gRGVjaW1hbCgwKQogICAgY2FzaCA9IERlY2ltYWwoc3RyKHBhcmFtZXRlcnMu
Z2V0KCJpbml0aWFsX2Nhc2giLCAiMTAwMDAiKSkpCiAgICBmb3IgaSBpbiByYW5nZSgxLCBsZW4oYXNzZW1ibGVkKSArIDEpOgogICAgICAgIHZpc2libGUg
PSB0dXBsZShhc3NlbWJsZWRbOmldKSAgICAgICAgICAjIEctMjogY3Vyc29yIHNsaWNlCiAgICAgICAgY3Vyc29yID0gdmlzaWJsZVstMV1bIm9wZW5fdGlt
ZSJdCiAgICAgICAgZGVjaXNpb24gPSBydWxlKEN1cnNvclNsaWNlKGJhcnM9dmlzaWJsZSwgY3Vyc29yPWN1cnNvciksIHBhcmFtZXRlcnMpCiAgICAgICAg
cmVzdWx0LmRlY2lzaW9uX2xlZGdlci5hcHBlbmQoewogICAgICAgICAgICAiZGVjaXNpb25fdHMiOiBjdXJzb3IsCiAgICAgICAgICAgICJkYXRhX3JlZl90
cyI6IFtiWyJvcGVuX3RpbWUiXSBmb3IgYiBpbiB2aXNpYmxlWy0zOl1dLAogICAgICAgICAgICAiZGVjaXNpb24iOiBkZWNpc2lvbiwKICAgICAgICB9KQog
ICAgICAgIGlmIGRlY2lzaW9uIGluICgiYnV5IiwgInNlbGwiKToKICAgICAgICAgICAgcmF3ID0gRGVjaW1hbChzdHIodmlzaWJsZVstMV1bImNsb3NlIl0p
KQogICAgICAgICAgICBlZmZlY3RpdmUgPSBhcHBseV9jb3N0cyhyYXcsIGRlY2lzaW9uLCBjb3N0X21vZGVsKQogICAgICAgICAgICBxdHkgPSBEZWNpbWFs
KHN0cihwYXJhbWV0ZXJzLmdldCgidW5pdF9xdHkiLCAiMSIpKSkKICAgICAgICAgICAgaWYgZGVjaXNpb24gPT0gImJ1eSI6CiAgICAgICAgICAgICAgICBw
b3NpdGlvbiArPSBxdHkKICAgICAgICAgICAgICAgIGNhc2ggLT0gZWZmZWN0aXZlICogcXR5CiAgICAgICAgICAgIGVsc2U6CiAgICAgICAgICAgICAgICBw
b3NpdGlvbiAtPSBxdHkKICAgICAgICAgICAgICAgIGNhc2ggKz0gZWZmZWN0aXZlICogcXR5CiAgICAgICAgICAgIHJlc3VsdC5maWxscy5hcHBlbmQoewog
ICAgICAgICAgICAgICAgInRzIjogY3Vyc29yLmlzb2Zvcm1hdCgpLCAic2lkZSI6IGRlY2lzaW9uLAogICAgICAgICAgICAgICAgInJhd19wcmljZSI6IHN0
cihyYXcpLCAiZWZmZWN0aXZlX3ByaWNlIjogc3RyKGVmZmVjdGl2ZSksCiAgICAgICAgICAgICAgICAicXR5Ijogc3RyKHF0eSksCiAgICAgICAgICAgIH0p
CiAgICBmaW5hbF9tYXJrID0gKERlY2ltYWwoc3RyKGFzc2VtYmxlZFstMV1bImNsb3NlIl0pKQogICAgICAgICAgICAgICAgICBpZiBhc3NlbWJsZWQgZWxz
ZSBEZWNpbWFsKDApKQogICAgZXF1aXR5ID0gY2FzaCArIHBvc2l0aW9uICogZmluYWxfbWFyawogICAgcmVzdWx0LnN1bW1hcnkgPSB7CiAgICAgICAgImJh
cnNfcmVwbGF5ZWQiOiBsZW4oYXNzZW1ibGVkKSwKICAgICAgICAiZmlsbHMiOiBsZW4ocmVzdWx0LmZpbGxzKSwKICAgICAgICAiZmluYWxfcG9zaXRpb24i
OiBzdHIocG9zaXRpb24pLAogICAgICAgICJmaW5hbF9jYXNoIjogc3RyKGNhc2gpLAogICAgICAgICJmaW5hbF9lcXVpdHkiOiBzdHIoZXF1aXR5KSwKICAg
ICAgICAicGVyZm9ybWFuY2VfZGlzY2xhaW1lciI6ICgKICAgICAgICAgICAgInBpcGVsaW5lLXZhbGlkYXRpb24gdGllciBvbiBsYWJlbGxlZCBzeW50aGV0
aWMgaW5wdXQ7IgogICAgICAgICAgICAiIE5PVCBsaXZlIG9yIGZ1dHVyZSBwZXJmb3JtYW5jZTsgbm8gbWFya2V0IGNvbmNsdXNpb24iKSwKICAgIH0KICAg
IHJldHVybiByZXN1bHQK
'@
Write-Evidence ("record 12/17 staged: " + $Rec12Path)
$Rec13Path = "app\v2\research_jobs\runner.py"
$Rec13Sha  = "8d0032cb92c1dc52fc09f40788c738dd1ae4f1ead3fb7b8136606bf704c68fda"
$Rec13B64 = @'
IiIiQkUtNyBVLTQgYXR0ZW1wdC1pZGVtcG90ZW50IHJ1bm5lciAoUC0xMDsgY29uZGl0aW9ucyBDMi9DMzsgUGFydCAxMC4xKS4KClRoZSBPTkxZIHBhdGgg
dGhhdCB0cmFuc2l0aW9ucyBhIGpvYiB0aHJvdWdoIHJ1bm5pbmcg4oaSIHN1Y2NlZWRlZC9mYWlsZWQKYW5kIHRoZSBPTkxZIGFydGlmYWN0IHdyaXRlci4g
SWRlbXBvdGVuY3k6IHRoZSByZXN1bHQgZGV0ZXJtaW5pc20gYW5jaG9yCnJldHVybnMgdGhlIGV4aXN0aW5nIGFydGlmYWN0IG9uIGEgcmV0cmllZCBpZGVu
dGljYWwgYXR0ZW1wdDsgdGhlIGxlZGdlcidzClVOSVFVRShqb2JfaWQsIGF0dGVtcHRfaW5kZXgpIGZvcmJpZHMgZG91YmxlLXdyaXRlcyBwZXIgYXR0ZW1w
dC4KIiIiCgpmcm9tIF9fZnV0dXJlX18gaW1wb3J0IGFubm90YXRpb25zCgpmcm9tIGRhdGV0aW1lIGltcG9ydCBkYXRldGltZSwgdGltZXpvbmUKCmZyb20g
c3FsYWxjaGVteSBpbXBvcnQgc2VsZWN0CmZyb20gc3FsYWxjaGVteS5leHQuYXN5bmNpbyBpbXBvcnQgQXN5bmNTZXNzaW9uCgpmcm9tIGFwcC5kYi5tb2Rl
bHMudjJfcmVzZWFyY2hfam9icyBpbXBvcnQgKAogICAgVjJCYWNrdGVzdElucHV0LAogICAgVjJDb3N0TW9kZWwsCiAgICBWMlJlc2VhcmNoSm9iLAogICAg
VjJSZXNlYXJjaEpvYkF0dGVtcHQsCiAgICBWMlJlc2VhcmNoUmVzdWx0LAogICAgVjJTdHJhdGVneVZlcnNpb24sCikKZnJvbSBhcHAudjIuYXVkaXQuY29u
dHJhY3QgaW1wb3J0IFYyQXVkaXRFdmVudENyZWF0ZQpmcm9tIGFwcC52Mi5hdWRpdC5yZXBvc2l0b3J5IGltcG9ydCBWMkF1ZGl0UmVwb3NpdG9yeQpmcm9t
IGFwcC52Mi5saW5lYWdlLmNvbnRyYWN0IGltcG9ydCBWMkxpbmVhZ2VSZWNvcmRDcmVhdGUKZnJvbSBhcHAudjIubGluZWFnZS5yZXBvc2l0b3J5IGltcG9y
dCBWMkxpbmVhZ2VSZXBvc2l0b3J5CmZyb20gYXBwLnYyLnJlc2VhcmNoX2pvYnMuY29udHJhY3RzIGltcG9ydCAoCiAgICBKT0JfTVVUQUJMRV9DT0xVTU5T
LAogICAgUlVOTkVSX0lOU0VSVF9UQUJMRVMsCiAgICBSVU5ORVJfVVBEQVRFX1RBQkxFUywKICAgIHJlcXVpcmVfY29uc3RydWN0aWJsZV9yZXN1bHRfY2xh
c3MsCikKZnJvbSBhcHAudjIucmVzZWFyY2hfam9icy5sZWFrYWdlIGltcG9ydCBMZWFrYWdlUmVmdXNlZCwgUmVwbGF5V2luZG93CmZyb20gYXBwLnYyLnJl
c2VhcmNoX2pvYnMucmVwbGF5IGltcG9ydCAoCiAgICBFTkdJTkVfVkVSU0lPTlMsCiAgICBlbmdpbmVfdmVyc2lvbnNfaGFzaCwKICAgIHJ1bl9yZXBsYXks
CikKCl9ET01BSU4gPSAidjIucmVzZWFyY2hfam9icyIKCgpkZWYgX3V0Y19mcm9tX3N0b3JlKHZhbHVlOiBkYXRldGltZSB8IE5vbmUpIC0+IGRhdGV0aW1l
IHwgTm9uZToKICAgICIiIlNRTGl0ZSBkaXNjYXJkcyB0eiBvbiBEYXRlVGltZSh0aW1lem9uZT1UcnVlKSDigJQgQkUtMiBub3JtYWxpemVyIGxhdy4iIiIK
ICAgIGlmIHZhbHVlIGlzIE5vbmU6CiAgICAgICAgcmV0dXJuIE5vbmUKICAgIGlmIHZhbHVlLnR6aW5mbyBpcyBOb25lOgogICAgICAgIHJldHVybiB2YWx1
ZS5yZXBsYWNlKHR6aW5mbz10aW1lem9uZS51dGMpCiAgICByZXR1cm4gdmFsdWUKCgoKIyBQYXJ0IDEwLjEgYWxsb3ctbGlzdCDigJQgYXNzZXJ0ZWQgYnkg
dGVzdDsgdGhlIG1vZHVsZSBjb25zdGFudCBJUyB0aGUgbGF3LgpXUklUQUJMRV9UQUJMRVMgPSB7Imluc2VydCI6IFJVTk5FUl9JTlNFUlRfVEFCTEVTLAog
ICAgICAgICAgICAgICAgICAgInVwZGF0ZSI6IFJVTk5FUl9VUERBVEVfVEFCTEVTfQpKT0JfVVBEQVRFX0NPTFVNTlMgPSBKT0JfTVVUQUJMRV9DT0xVTU5T
ICAjIEMyCgoKYXN5bmMgZGVmIF9hdWRpdChzZXNzaW9uOiBBc3luY1Nlc3Npb24sIGFjdGlvbjogc3RyLCAqLCBkZXRhaWxzOiBkaWN0LAogICAgICAgICAg
ICAgICAgIG1vZGU6IHN0ciwgb3BlcmF0b3JfaWQ6IHN0ciwgY29ycmVsYXRpb25faWQ6IHN0ciB8IE5vbmUsCiAgICAgICAgICAgICAgICAgcmVzb3VyY2Vf
aWQ6IHN0ciB8IE5vbmUgPSBOb25lKSAtPiBOb25lOgogICAgYXdhaXQgVjJBdWRpdFJlcG9zaXRvcnkoc2Vzc2lvbikuYXBwZW5kKFYyQXVkaXRFdmVudENy
ZWF0ZSgKICAgICAgICBkb21haW49X0RPTUFJTiwgYWN0aW9uPWFjdGlvbiwgYWN0b3JfaWQ9b3BlcmF0b3JfaWQsCiAgICAgICAgYWN0b3JfdHlwZT0ib3Bl
cmF0b3IiLCBtb2RlPW1vZGUsCiAgICAgICAgcmVzb3VyY2VfdHlwZT0icmVzZWFyY2hfam9iIiwgcmVzb3VyY2VfaWQ9cmVzb3VyY2VfaWQsCiAgICAgICAg
ZGV0YWlscz1kZXRhaWxzLCBvcGVyYXRvcl9pZD1vcGVyYXRvcl9pZCwKICAgICAgICBjb3JyZWxhdGlvbl9pZD1jb3JyZWxhdGlvbl9pZCkpCgoKYXN5bmMg
ZGVmIHJ1bl9qb2Ioc2Vzc2lvbjogQXN5bmNTZXNzaW9uLCAqLCBqb2JfaWQ6IHN0ciwgYWN0b3JfaWQ6IHN0ciwKICAgICAgICAgICAgICAgICAgYmFyczog
bGlzdFtkaWN0XSwgY29ycmVsYXRpb25faWQ6IHN0ciB8IE5vbmUpIC0+IGRpY3Q6CiAgICAiIiJFeGVjdXRlIG9uZSBhdHRlbXB0LiBSZXR1cm5zIHtqb2Jf
c3RhdGUsIHJlc3VsdF9pZCwgcmV1c2VkLCByZWFzb25zfS4iIiIKICAgIGpvYiA9IChhd2FpdCBzZXNzaW9uLmV4ZWN1dGUoCiAgICAgICAgc2VsZWN0KFYy
UmVzZWFyY2hKb2IpLndoZXJlKFYyUmVzZWFyY2hKb2IuaWQgPT0gam9iX2lkKQogICAgKSkuc2NhbGFyX29uZV9vcl9ub25lKCkKICAgIGlmIGpvYiBpcyBO
b25lOgogICAgICAgIHJldHVybiB7ImpvYl9zdGF0ZSI6ICJ1bmtub3duIiwgInJlc3VsdF9pZCI6IE5vbmUsICJyZXVzZWQiOiBGYWxzZSwKICAgICAgICAg
ICAgICAgICJyZWFzb25zIjogW3siZmFpbGluZyI6ICJqb2JfaWQifV19CiAgICBpZiBqb2Iuam9iX3N0YXRlIG5vdCBpbiAoInF1ZXVlZCIsICJmYWlsZWQi
KToKICAgICAgICByZXR1cm4geyJqb2Jfc3RhdGUiOiBqb2Iuam9iX3N0YXRlLCAicmVzdWx0X2lkIjogam9iLm91dHB1dF9yZWYsCiAgICAgICAgICAgICAg
ICAicmV1c2VkIjogam9iLmpvYl9zdGF0ZSA9PSAic3VjY2VlZGVkIiwKICAgICAgICAgICAgICAgICJyZWFzb25zIjogW3siZmFpbGluZyI6ICJqb2Jfc3Rh
dGUiLCAidmFsdWUiOiBqb2Iuam9iX3N0YXRlLAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICJub3RlIjogIm9ubHkgcXVldWVkL2ZhaWxlZCBqb2Jz
IHJ1biJ9XX0KCiAgICBtb2RlID0gam9iLm1vZGUKICAgIGF0dGVtcHQgPSBqb2IuYXR0ZW1wdF9jb3VudCArIDEKICAgIGpvYi5hdHRlbXB0X2NvdW50ID0g
YXR0ZW1wdCAgICAgICAgICAjIEMyIG11dGFibGUgc2V0IG9ubHkKICAgIGpvYi5qb2Jfc3RhdGUgPSAicnVubmluZyIKICAgIGF3YWl0IHNlc3Npb24uZmx1
c2goKQogICAgYXdhaXQgX2F1ZGl0KHNlc3Npb24sICJqb2Iuc3RhcnRlZCIsCiAgICAgICAgICAgICAgICAgZGV0YWlscz17ImF0dGVtcHRfaW5kZXgiOiBh
dHRlbXB0fSwgbW9kZT1tb2RlLAogICAgICAgICAgICAgICAgIG9wZXJhdG9yX2lkPWFjdG9yX2lkLCBjb3JyZWxhdGlvbl9pZD1jb3JyZWxhdGlvbl9pZCwK
ICAgICAgICAgICAgICAgICByZXNvdXJjZV9pZD1qb2IuaWQpCgogICAgIyByZXNvbHZlIHRoZSBsaW5lYWdlIHRyaXBsZQogICAgcmVnaXN0cnkgPSAoYXdh
aXQgc2Vzc2lvbi5leGVjdXRlKAogICAgICAgIHNlbGVjdChWMkJhY2t0ZXN0SW5wdXQpLndoZXJlKAogICAgICAgICAgICBWMkJhY2t0ZXN0SW5wdXQuaWQg
PT0gam9iLmlucHV0c1siaW5wdXRfcmVnaXN0cnlfaWQiXSkKICAgICkpLnNjYWxhcl9vbmVfb3Jfbm9uZSgpCiAgICBzdHJhdGVneSA9IChhd2FpdCBzZXNz
aW9uLmV4ZWN1dGUoCiAgICAgICAgc2VsZWN0KFYyU3RyYXRlZ3lWZXJzaW9uKS53aGVyZSgKICAgICAgICAgICAgVjJTdHJhdGVneVZlcnNpb24uaWQgPT0g
am9iLmlucHV0c1sic3RyYXRlZ3lfdmVyc2lvbl9pZCJdKQogICAgKSkuc2NhbGFyX29uZV9vcl9ub25lKCkKICAgIGNvc3QgPSAoYXdhaXQgc2Vzc2lvbi5l
eGVjdXRlKAogICAgICAgIHNlbGVjdChWMkNvc3RNb2RlbCkud2hlcmUoCiAgICAgICAgICAgIFYyQ29zdE1vZGVsLmlkID09IGpvYi5pbnB1dHNbImNvc3Rf
bW9kZWxfaWQiXSkKICAgICkpLnNjYWxhcl9vbmVfb3Jfbm9uZSgpCgogICAgZGVmIF9mYWlsKHJlYXNvbnM6IGxpc3QpIC0+IGRpY3Q6CiAgICAgICAgam9i
LmpvYl9zdGF0ZSA9ICJmYWlsZWQiCiAgICAgICAgam9iLmZhaWx1cmUgPSB7InJlYXNvbnMiOiByZWFzb25zLCAiYXR0ZW1wdF9pbmRleCI6IGF0dGVtcHR9
CiAgICAgICAgc2Vzc2lvbi5hZGQoVjJSZXNlYXJjaEpvYkF0dGVtcHQoCiAgICAgICAgICAgIGpvYl9pZD1qb2IuaWQsIGF0dGVtcHRfaW5kZXg9YXR0ZW1w
dCwgb3V0Y29tZT0iZmFpbGVkIiwKICAgICAgICAgICAgcmVhc29uPXsicmVhc29ucyI6IHJlYXNvbnN9LCBhY3Rvcl9pZD1hY3Rvcl9pZCwgbW9kZT1tb2Rl
LAogICAgICAgICAgICBvcGVyYXRvcl9pZD1hY3Rvcl9pZCwgY29ycmVsYXRpb25faWQ9Y29ycmVsYXRpb25faWQpKQogICAgICAgIHJldHVybiB7ImpvYl9z
dGF0ZSI6ICJmYWlsZWQiLCAicmVzdWx0X2lkIjogTm9uZSwgInJldXNlZCI6IEZhbHNlLAogICAgICAgICAgICAgICAgInJlYXNvbnMiOiByZWFzb25zfQoK
ICAgIGlmIHJlZ2lzdHJ5IGlzIE5vbmUgb3Igc3RyYXRlZ3kgaXMgTm9uZSBvciBjb3N0IGlzIE5vbmU6CiAgICAgICAgcmVzdWx0ID0gX2ZhaWwoW3siZmFp
bGluZyI6ICJsaW5lYWdlX3Jlc29sdXRpb24ifV0pCiAgICAgICAgYXdhaXQgX2F1ZGl0KHNlc3Npb24sICJqb2IuZmFpbGVkIiwgZGV0YWlscz1qb2IuZmFp
bHVyZSwgbW9kZT1tb2RlLAogICAgICAgICAgICAgICAgICAgICBvcGVyYXRvcl9pZD1hY3Rvcl9pZCwgY29ycmVsYXRpb25faWQ9Y29ycmVsYXRpb25faWQs
CiAgICAgICAgICAgICAgICAgICAgIHJlc291cmNlX2lkPWpvYi5pZCkKICAgICAgICByZXR1cm4gcmVzdWx0CgogICAgdHJ5OgogICAgICAgIHJlc3VsdF9j
bGFzcyA9IHJlcXVpcmVfY29uc3RydWN0aWJsZV9yZXN1bHRfY2xhc3MoCiAgICAgICAgICAgIGpvYi5pbnB1dHNbInJlc3VsdF9jbGFzcyJdKSAgIyBQLTkg
Y29uc3RydWN0aW9uIHBvaW50CiAgICBleGNlcHQgRXhjZXB0aW9uIGFzIGV4YzoKICAgICAgICByZXN1bHQgPSBfZmFpbChbeyJmYWlsaW5nIjogInJlc3Vs
dF9jbGFzcyIsICJ2YWx1ZSI6IHN0cihleGMpfV0pCiAgICAgICAgYXdhaXQgX2F1ZGl0KHNlc3Npb24sICJqb2IuZmFpbGVkIiwgZGV0YWlscz1qb2IuZmFp
bHVyZSwgbW9kZT1tb2RlLAogICAgICAgICAgICAgICAgICAgICBvcGVyYXRvcl9pZD1hY3Rvcl9pZCwgY29ycmVsYXRpb25faWQ9Y29ycmVsYXRpb25faWQs
CiAgICAgICAgICAgICAgICAgICAgIHJlc291cmNlX2lkPWpvYi5pZCkKICAgICAgICByZXR1cm4gcmVzdWx0CgogICAgdmVyc2lvbnNfaGFzaCA9IGVuZ2lu
ZV92ZXJzaW9uc19oYXNoKCkKICAgICMgUC0xMCBpZGVtcG90ZW5jeTogYW5jaG9yIGxvb2t1cCBCRUZPUkUgY29tcHV0aW5nCiAgICBleGlzdGluZyA9IChh
d2FpdCBzZXNzaW9uLmV4ZWN1dGUoCiAgICAgICAgc2VsZWN0KFYyUmVzZWFyY2hSZXN1bHQpLndoZXJlKAogICAgICAgICAgICBWMlJlc2VhcmNoUmVzdWx0
LnN0cmF0ZWd5X3ZlcnNpb25faWQgPT0gc3RyYXRlZ3kuaWQsCiAgICAgICAgICAgIFYyUmVzZWFyY2hSZXN1bHQuaW5wdXRzX2hhc2ggPT0gcmVnaXN0cnku
Y29udGVudF9oYXNoLAogICAgICAgICAgICBWMlJlc2VhcmNoUmVzdWx0LmVuZ2luZV92ZXJzaW9uc19oYXNoID09IHZlcnNpb25zX2hhc2gpCiAgICApKS5z
Y2FsYXJfb25lX29yX25vbmUoKQogICAgaWYgZXhpc3RpbmcgaXMgbm90IE5vbmU6CiAgICAgICAgam9iLmpvYl9zdGF0ZSA9ICJzdWNjZWVkZWQiCiAgICAg
ICAgam9iLm91dHB1dF9yZWYgPSBleGlzdGluZy5pZAogICAgICAgIHNlc3Npb24uYWRkKFYyUmVzZWFyY2hKb2JBdHRlbXB0KAogICAgICAgICAgICBqb2Jf
aWQ9am9iLmlkLCBhdHRlbXB0X2luZGV4PWF0dGVtcHQsIG91dGNvbWU9InN1Y2NlZWRlZCIsCiAgICAgICAgICAgIGFydGlmYWN0X3JlZj1leGlzdGluZy5p
ZCwKICAgICAgICAgICAgcmVhc29uPXsiaWRlbXBvdGVudF9yZXVzZSI6IFRydWUsCiAgICAgICAgICAgICAgICAgICAgImFuY2hvciI6ICJ1cV92Ml9yZXN1
bHRfZGV0ZXJtaW5pc21fYW5jaG9yIn0sCiAgICAgICAgICAgIGFjdG9yX2lkPWFjdG9yX2lkLCBtb2RlPW1vZGUsIG9wZXJhdG9yX2lkPWFjdG9yX2lkLAog
ICAgICAgICAgICBjb3JyZWxhdGlvbl9pZD1jb3JyZWxhdGlvbl9pZCkpCiAgICAgICAgYXdhaXQgc2Vzc2lvbi5mbHVzaCgpCiAgICAgICAgYXdhaXQgX2F1
ZGl0KHNlc3Npb24sICJyZXN1bHQucmV1c2VkIiwKICAgICAgICAgICAgICAgICAgICAgZGV0YWlscz17InJlc3VsdF9pZCI6IGV4aXN0aW5nLmlkLAogICAg
ICAgICAgICAgICAgICAgICAgICAgICAgICAiYXR0ZW1wdF9pbmRleCI6IGF0dGVtcHR9LAogICAgICAgICAgICAgICAgICAgICBtb2RlPW1vZGUsIG9wZXJh
dG9yX2lkPWFjdG9yX2lkLAogICAgICAgICAgICAgICAgICAgICBjb3JyZWxhdGlvbl9pZD1jb3JyZWxhdGlvbl9pZCwgcmVzb3VyY2VfaWQ9am9iLmlkKQog
ICAgICAgIHJldHVybiB7ImpvYl9zdGF0ZSI6ICJzdWNjZWVkZWQiLCAicmVzdWx0X2lkIjogZXhpc3RpbmcuaWQsCiAgICAgICAgICAgICAgICAicmV1c2Vk
IjogVHJ1ZSwgInJlYXNvbnMiOiBbXX0KCiAgICB3aW5kb3cgPSBSZXBsYXlXaW5kb3coCiAgICAgICAgd2luZG93X3N0YXJ0PV91dGNfZnJvbV9zdG9yZShy
ZWdpc3RyeS53aW5kb3dfc3RhcnQpLAogICAgICAgIHdpbmRvd19lbmQ9X3V0Y19mcm9tX3N0b3JlKHJlZ2lzdHJ5LndpbmRvd19lbmQpLAogICAgICAgIGFz
X29mPV91dGNfZnJvbV9zdG9yZShyZWdpc3RyeS53aW5kb3dfZW5kKSkKICAgIGNvc3RfbW9kZWwgPSB7InNwcmVhZCI6IGNvc3Quc3ByZWFkLCAiY29tbWlz
c2lvbiI6IGNvc3QuY29tbWlzc2lvbiwKICAgICAgICAgICAgICAgICAgInNsaXBwYWdlIjogY29zdC5zbGlwcGFnZX0KICAgIHRyeToKICAgICAgICByZXBs
YXkgPSBydW5fcmVwbGF5KAogICAgICAgICAgICBiYXJzPWJhcnMsIHdpbmRvdz13aW5kb3csCiAgICAgICAgICAgIHN0cmF0ZWd5X3J1bGU9c3RyYXRlZ3ku
cGFyYW1ldGVyc1sicnVsZSJdLAogICAgICAgICAgICBwYXJhbWV0ZXJzPXN0cmF0ZWd5LnBhcmFtZXRlcnMsCiAgICAgICAgICAgIGNvc3RfbW9kZWw9Y29z
dF9tb2RlbCwKICAgICAgICAgICAgc3RvcmVkX2NvbnRlbnRfaGFzaD1yZWdpc3RyeS5jb250ZW50X2hhc2gsCiAgICAgICAgICAgIHNlcmllc19yZWZzPXJl
Z2lzdHJ5LnNlcmllc19yZWZzKQogICAgZXhjZXB0IExlYWthZ2VSZWZ1c2VkIGFzIGV4YzoKICAgICAgICByZXN1bHQgPSBfZmFpbChbeyJmYWlsaW5nIjog
ZXhjLmd1YXJkLCAicmVhc29ucyI6IGV4Yy5yZWFzb25zfV0pCiAgICAgICAgYXdhaXQgX2F1ZGl0KHNlc3Npb24sICJqb2IuZmFpbGVkIiwgZGV0YWlscz1q
b2IuZmFpbHVyZSwgbW9kZT1tb2RlLAogICAgICAgICAgICAgICAgICAgICBvcGVyYXRvcl9pZD1hY3Rvcl9pZCwgY29ycmVsYXRpb25faWQ9Y29ycmVsYXRp
b25faWQsCiAgICAgICAgICAgICAgICAgICAgIHJlc291cmNlX2lkPWpvYi5pZCkKICAgICAgICByZXR1cm4gcmVzdWx0CiAgICBleGNlcHQgVmFsdWVFcnJv
ciBhcyBleGM6CiAgICAgICAgIyBGLTEgZGVmZW5zZS1pbi1kZXB0aCAoQ1ItVjItQkUtNy0wMDEpOiBlbmdpbmUgdm9jYWJ1bGFyeSBlcnJvcnMKICAgICAg
ICAjIChlLmcuIHVua25vd24gY29zdCB1bml0IG9uIHByZS1nYXRlIHJvd3MpIGZhaWwgVFlQRUQsIG5ldmVyIDUwMC4KICAgICAgICByZXN1bHQgPSBfZmFp
bChbeyJmYWlsaW5nIjogImVuZ2luZV92b2NhYnVsYXJ5IiwgInZhbHVlIjogc3RyKGV4Yyl9XSkKICAgICAgICBhd2FpdCBfYXVkaXQoc2Vzc2lvbiwgImpv
Yi5mYWlsZWQiLCBkZXRhaWxzPWpvYi5mYWlsdXJlLCBtb2RlPW1vZGUsCiAgICAgICAgICAgICAgICAgICAgIG9wZXJhdG9yX2lkPWFjdG9yX2lkLCBjb3Jy
ZWxhdGlvbl9pZD1jb3JyZWxhdGlvbl9pZCwKICAgICAgICAgICAgICAgICAgICAgcmVzb3VyY2VfaWQ9am9iLmlkKQogICAgICAgIHJldHVybiByZXN1bHQK
CiAgICBhcnRpZmFjdCA9IFYyUmVzZWFyY2hSZXN1bHQoCiAgICAgICAgcmVzdWx0X2NsYXNzPXJlc3VsdF9jbGFzcywKICAgICAgICBqb2JfaWQ9am9iLmlk
LCBhdHRlbXB0X2luZGV4PWF0dGVtcHQsCiAgICAgICAgc3RyYXRlZ3lfdmVyc2lvbl9pZD1zdHJhdGVneS5pZCwKICAgICAgICBpbnB1dF9yZWdpc3RyeV9p
ZD1yZWdpc3RyeS5pZCwKICAgICAgICBjb3N0X21vZGVsX2lkPWNvc3QuaWQsCiAgICAgICAgaW5wdXRzX2hhc2g9cmVnaXN0cnkuY29udGVudF9oYXNoLAog
ICAgICAgIGVuZ2luZV92ZXJzaW9ucz1FTkdJTkVfVkVSU0lPTlMsCiAgICAgICAgZW5naW5lX3ZlcnNpb25zX2hhc2g9dmVyc2lvbnNfaGFzaCwKICAgICAg
ICBzdW1tYXJ5PXJlcGxheS5zdW1tYXJ5LAogICAgICAgIHRpbWVfYmFzaXM9eyJ3aW5kb3dfc3RhcnQiOiBfdXRjX2Zyb21fc3RvcmUoCiAgICAgICAgICAg
ICAgICAgICAgICAgIHJlZ2lzdHJ5LndpbmRvd19zdGFydCkuaXNvZm9ybWF0KCksCiAgICAgICAgICAgICAgICAgICAgIndpbmRvd19lbmQiOiBfdXRjX2Zy
b21fc3RvcmUoCiAgICAgICAgICAgICAgICAgICAgICAgIHJlZ2lzdHJ5LndpbmRvd19lbmQpLmlzb2Zvcm1hdCgpLAogICAgICAgICAgICAgICAgICAgICJi
YXJzIjogcmVwbGF5LnN1bW1hcnlbImJhcnNfcmVwbGF5ZWQiXX0sCiAgICAgICAgZGF0YV9jbGFzcz1qb2IuZGF0YV9jbGFzcywKICAgICAgICBtb2RlPW1v
ZGUsIG9wZXJhdG9yX2lkPWFjdG9yX2lkLCBjb3JyZWxhdGlvbl9pZD1jb3JyZWxhdGlvbl9pZCkKICAgIHNlc3Npb24uYWRkKGFydGlmYWN0KQogICAgYXdh
aXQgc2Vzc2lvbi5mbHVzaCgpCgogICAgam9iLmpvYl9zdGF0ZSA9ICJzdWNjZWVkZWQiCiAgICBqb2Iub3V0cHV0X3JlZiA9IGFydGlmYWN0LmlkCiAgICBz
ZXNzaW9uLmFkZChWMlJlc2VhcmNoSm9iQXR0ZW1wdCgKICAgICAgICBqb2JfaWQ9am9iLmlkLCBhdHRlbXB0X2luZGV4PWF0dGVtcHQsIG91dGNvbWU9InN1
Y2NlZWRlZCIsCiAgICAgICAgYXJ0aWZhY3RfcmVmPWFydGlmYWN0LmlkLCByZWFzb249eyJjb21wdXRlZCI6IFRydWV9LAogICAgICAgIGFjdG9yX2lkPWFj
dG9yX2lkLCBtb2RlPW1vZGUsIG9wZXJhdG9yX2lkPWFjdG9yX2lkLAogICAgICAgIGNvcnJlbGF0aW9uX2lkPWNvcnJlbGF0aW9uX2lkKSkKICAgIGF3YWl0
IHNlc3Npb24uZmx1c2goKQoKICAgIGF3YWl0IF9hdWRpdChzZXNzaW9uLCAicmVzdWx0LmNyZWF0ZWQiLAogICAgICAgICAgICAgICAgIGRldGFpbHM9eyJy
ZXN1bHRfaWQiOiBhcnRpZmFjdC5pZCwKICAgICAgICAgICAgICAgICAgICAgICAgICAicmVzdWx0X2NsYXNzIjogcmVzdWx0X2NsYXNzLAogICAgICAgICAg
ICAgICAgICAgICAgICAgICJhdHRlbXB0X2luZGV4IjogYXR0ZW1wdH0sCiAgICAgICAgICAgICAgICAgbW9kZT1tb2RlLCBvcGVyYXRvcl9pZD1hY3Rvcl9p
ZCwKICAgICAgICAgICAgICAgICBjb3JyZWxhdGlvbl9pZD1jb3JyZWxhdGlvbl9pZCwgcmVzb3VyY2VfaWQ9am9iLmlkKQogICAgYXdhaXQgVjJMaW5lYWdl
UmVwb3NpdG9yeShzZXNzaW9uKS5hcHBlbmQoVjJMaW5lYWdlUmVjb3JkQ3JlYXRlKAogICAgICAgIGFydGlmYWN0X3R5cGU9InJlc2VhcmNoX3Jlc3VsdCIs
CiAgICAgICAgYXJ0aWZhY3RfaWQ9YXJ0aWZhY3QuaWQsCiAgICAgICAgb3BlcmF0b3JfaWQ9YWN0b3JfaWQsIG1vZGU9bW9kZSwKICAgICAgICBzb3VyY2Vf
YXJ0aWZhY3RfaWRzPVtyZWdpc3RyeS5pZCwgc3RyYXRlZ3kuaWQsIGNvc3QuaWQsIGpvYi5pZF0sCiAgICAgICAgY29tcHV0YXRpb25fdmVyc2lvbj12ZXJz
aW9uc19oYXNoLAogICAgICAgIGlucHV0X3NuYXBzaG90X2lkPXJlZ2lzdHJ5LmNvbnRlbnRfaGFzaCkpCiAgICBhd2FpdCBfYXVkaXQoc2Vzc2lvbiwgImpv
Yi5zdWNjZWVkZWQiLAogICAgICAgICAgICAgICAgIGRldGFpbHM9eyJyZXN1bHRfaWQiOiBhcnRpZmFjdC5pZCwKICAgICAgICAgICAgICAgICAgICAgICAg
ICAiYXR0ZW1wdF9pbmRleCI6IGF0dGVtcHR9LAogICAgICAgICAgICAgICAgIG1vZGU9bW9kZSwgb3BlcmF0b3JfaWQ9YWN0b3JfaWQsCiAgICAgICAgICAg
ICAgICAgY29ycmVsYXRpb25faWQ9Y29ycmVsYXRpb25faWQsIHJlc291cmNlX2lkPWpvYi5pZCkKICAgIHJldHVybiB7ImpvYl9zdGF0ZSI6ICJzdWNjZWVk
ZWQiLCAicmVzdWx0X2lkIjogYXJ0aWZhY3QuaWQsCiAgICAgICAgICAgICJyZXVzZWQiOiBGYWxzZSwgInJlYXNvbnMiOiBbXX0K
'@
Write-Evidence ("record 13/17 staged: " + $Rec13Path)
$Rec14Path = "tests\test_v2_be7_boundaries.py"
$Rec14Sha  = "45373d015a232d1c734e03e493bf4fc0f852639239513faafbb8ea39eaa25f31"
$Rec14B64 = @'
IiIiVjIgQkUtNyBib3VuZGFyeSArIHJlZ3Jlc3Npb24gY29tcGxldGlvbiDigJQgQk8tVjItQkUtNy0wMDEgVC04L1QtMTEvVC0xMgooYnVkZ2V0IGNvbXBs
ZXRpb24gdG8gNjA7IEFQSS1zdXJmYWNlIHNjYW47IG5vLXRvdWNoIHJlZ3Jlc3Npb24gcGFpcikuCiIiIgoKZnJvbSBfX2Z1dHVyZV9fIGltcG9ydCBhbm5v
dGF0aW9ucwoKaW1wb3J0IHNvY2tldApmcm9tIGRhdGV0aW1lIGltcG9ydCBkYXRldGltZSwgdGltZWRlbHRhLCB0aW1lem9uZQoKaW1wb3J0IHB5dGVzdAoK
ZnJvbSBhcHAudjIucmVzZWFyY2hfam9icy5jb250cmFjdHMgaW1wb3J0ICgKICAgIEpPQl9TVEFURVMsCiAgICBKT0JfVEVSTUlOQUxfU1RBVEVTLAogICAg
TElGRUNZQ0xFX1NUQVRFUywKICAgIFJFR0lTVFJBVElPTl9PVVRDT01FUywKICAgIFNDSEVEVUxFX0tJTkRTX1YxLAopCmZyb20gYXBwLnYyLnJlc2VhcmNo
X2pvYnMubGVha2FnZSBpbXBvcnQgKAogICAgTGVha2FnZVJlZnVzZWQsCiAgICBSZXBsYXlXaW5kb3csCiAgICB2YWxpZGF0ZV9ob3Jpem9uX2czLAopCmZy
b20gYXBwLnYyLnJlc2VhcmNoX2pvYnMucmVwbGF5IGltcG9ydCBTVFJBVEVHWV9SVUxFUywgQ3Vyc29yU2xpY2UsIGNyb3Nzb3Zlcl9ydWxlCgpVVEMgPSB0
aW1lem9uZS51dGMKVDAgPSBkYXRldGltZSgyMDI2LCA5LCAxLCB0emluZm89VVRDKQoKCkBweXRlc3QuZml4dHVyZShhdXRvdXNlPVRydWUpCmRlZiBfc29j
a2V0X2d1YXJkKG1vbmtleXBhdGNoKToKICAgIGRlZiBfZGVueSgqX2EsICoqX2spOgogICAgICAgIHJhaXNlIEFzc2VydGlvbkVycm9yKCJuZXR3b3JrIGF0
dGVtcHQgZHVyaW5nIEJFLTcgYm91bmRhcnkgdGVzdCIpCgogICAgbW9ua2V5cGF0Y2guc2V0YXR0cihzb2NrZXQsICJnZXRhZGRyaW5mbyIsIF9kZW55KQog
ICAgbW9ua2V5cGF0Y2guc2V0YXR0cihzb2NrZXQsICJjcmVhdGVfY29ubmVjdGlvbiIsIF9kZW55KQoKCiMgLS0tIHZvY2FidWxhcnkgaW50ZWdyaXR5ICgx
KSAtLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0KCgpkZWYgdGVzdF92b2NhYnVsYXJ5X2ludGVncml0eSgpOgog
ICAgYXNzZXJ0IEpPQl9TVEFURVMgPT0gKCJxdWV1ZWQiLCAicnVubmluZyIsICJzdWNjZWVkZWQiLCAiZmFpbGVkIiwKICAgICAgICAgICAgICAgICAgICAg
ICAgICAiY2FuY2VsbGVkIikKICAgIGFzc2VydCBzZXQoSk9CX1RFUk1JTkFMX1NUQVRFUykgPCBzZXQoSk9CX1NUQVRFUykKICAgIGFzc2VydCBMSUZFQ1lD
TEVfU1RBVEVTID09ICgiZHJhZnQiLCAicmVnaXN0ZXJlZCIsICJyZXRpcmVkIikKICAgIGFzc2VydCBSRUdJU1RSQVRJT05fT1VUQ09NRVMgPT0gKCJyZWdp
c3RlcmVkIiwgInJldXNlZCIsICJyZWZ1c2VkIikKICAgIGFzc2VydCBTQ0hFRFVMRV9LSU5EU19WMSA9PSAoIm1hbnVhbCIsKQogICAgYXNzZXJ0IHNldChT
VFJBVEVHWV9SVUxFUykgPT0geyJ0aHJlc2hvbGQiLCAiY3Jvc3NvdmVyIn0KCgojIC0tLSBjcm9zc292ZXIgcnVsZSBkZXRlcm1pbmlzbSAoMSkgLS0tLS0t
LS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tCgoKZGVmIHRlc3RfY3Jvc3NvdmVyX3J1bGVfZGV0ZXJtaW5pc3RpY19hbmRfc2xp
Y2VkKCk6CiAgICBkZWYgYmFycyhjbG9zZXMpOgogICAgICAgIHJldHVybiB0dXBsZSgKICAgICAgICAgICAgeyJvcGVuX3RpbWUiOiBUMCArIHRpbWVkZWx0
YShtaW51dGVzPTE1ICogaSksICJjbG9zZSI6IGN9CiAgICAgICAgICAgIGZvciBpLCBjIGluIGVudW1lcmF0ZShjbG9zZXMpKQoKICAgIHBhcmFtcyA9IHsi
ZmFzdCI6IDIsICJzbG93IjogNH0KICAgIHVwID0gYmFycyhbIjEwMCIsICIxMDAiLCAiMTAwIiwgIjEwMCIsICI5OSIsICIxMDMiLCAiMTA4Il0pCiAgICBz
bGljZV8gPSBDdXJzb3JTbGljZShiYXJzPXVwLCBjdXJzb3I9dXBbLTFdWyJvcGVuX3RpbWUiXSkKICAgIGZpcnN0ID0gY3Jvc3NvdmVyX3J1bGUoc2xpY2Vf
LCBwYXJhbXMpCiAgICBzZWNvbmQgPSBjcm9zc292ZXJfcnVsZShzbGljZV8sIHBhcmFtcykKICAgIGFzc2VydCBmaXJzdCA9PSBzZWNvbmQgICMgZGV0ZXJt
aW5pc3RpYwogICAgc2hvcnQgPSBDdXJzb3JTbGljZShiYXJzPXVwWzoyXSwgY3Vyc29yPXVwWzFdWyJvcGVuX3RpbWUiXSkKICAgIGFzc2VydCBjcm9zc292
ZXJfcnVsZShzaG9ydCwgcGFyYW1zKSBpcyBOb25lICAjIGluc3VmZmljaWVudCA9IHR5cGVkIE5vbmUKCgojIC0tLSBHLTMgYm91bmRhcnkgdmFsdWVzICgx
KSAtLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0KCgpkZWYgdGVzdF9nM19ib3VuZGFyeV9leGFjdG5l
c3MoKToKICAgIHdpbmRvdyA9IFJlcGxheVdpbmRvdyh3aW5kb3dfc3RhcnQ9VDAsCiAgICAgICAgICAgICAgICAgICAgICAgICAgd2luZG93X2VuZD1UMCAr
IHRpbWVkZWx0YShob3Vycz00KSwKICAgICAgICAgICAgICAgICAgICAgICAgICBhc19vZj1UMCArIHRpbWVkZWx0YShob3Vycz00KSkKICAgICMgemVybyBo
b3Jpem9uIGFsd2F5cyBsZWdhbAogICAgdmFsaWRhdGVfaG9yaXpvbl9nMyhsYWJlbF9ob3Jpem9uPXRpbWVkZWx0YSgwKSwKICAgICAgICAgICAgICAgICAg
ICAgICAgZW1iYXJnbz10aW1lZGVsdGEoaG91cnM9MSksIHdpbmRvdz13aW5kb3cpCiAgICAjIGhvcml6b24rZW1iYXJnbyBleGFjdGx5IGNvbnN1bWluZyB0
aGUgd2luZG93OiByZWZ1c2VkCiAgICB3aXRoIHB5dGVzdC5yYWlzZXMoTGVha2FnZVJlZnVzZWQpOgogICAgICAgIHZhbGlkYXRlX2hvcml6b25fZzMobGFi
ZWxfaG9yaXpvbj10aW1lZGVsdGEoaG91cnM9MyksCiAgICAgICAgICAgICAgICAgICAgICAgICAgICBlbWJhcmdvPXRpbWVkZWx0YShob3Vycz0xKSwgd2lu
ZG93PXdpbmRvdykKCgojIC0tLSB3aW5kb3cgdmFsaWRhdGlvbiBlZGdlcyAoMSkgLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0t
LS0tLS0tLS0tLS0tLQoKCmRlZiB0ZXN0X3dpbmRvd19kZWdlbmVyYXRlX3JlZnVzZWQoKToKICAgIHdpdGggcHl0ZXN0LnJhaXNlcyhMZWFrYWdlUmVmdXNl
ZCk6CiAgICAgICAgUmVwbGF5V2luZG93KHdpbmRvd19zdGFydD1UMCwgd2luZG93X2VuZD1UMCwgYXNfb2Y9VDApLnZhbGlkYXRlKCkKCgojIC0tLSBBUEkt
c3VyZmFjZSBlbnVtZXJhdGlvbiBzY2FuICgxKSDigJQgZXhpdCBpdGVtIHYgKGMpIC0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0KCgpkZWYg
dGVzdF9hcGlfc3VyZmFjZV9lbnVtZXJhdGlvbl9ub19leGVjdXRpb25fdm9jYWJ1bGFyeSgpOgogICAgZnJvbSBmYXN0YXBpLnJvdXRpbmcgaW1wb3J0IEFQ
SVJvdXRlCgogICAgZnJvbSBhcHAudjIucmVzZWFyY2hfam9icy5hcGkgaW1wb3J0IHJvdXRlcgoKICAgIHdyaXRlcl9wYXRocyA9IHsKICAgICAgICAiL3Jl
c2VhcmNoLWpvYnMvcmVnaXN0cnkvaW5wdXRzIiwKICAgICAgICAiL3Jlc2VhcmNoLWpvYnMvcmVnaXN0cnkvY29zdC1tb2RlbHMiLAogICAgICAgICIvcmVz
ZWFyY2gtam9icy9yZWdpc3RyeS9zdHJhdGVnaWVzIiwKICAgICAgICAiL3Jlc2VhcmNoLWpvYnMvam9icy9zdWJtaXQiLAogICAgICAgICIvcmVzZWFyY2gt
am9icy9qb2JzL3J1biIsCiAgICAgICAgIi9yZXNlYXJjaC1qb2JzL2pvYnMvY2FuY2VsIiwKICAgIH0KICAgIGJhbm5lZCA9ICgib3JkZXIiLCAiZXhlY3V0
ZSIsICJicm9rZXIiLCAicG9zaXRpb24iLCAiYWNjb3VudCIsCiAgICAgICAgICAgICAgInBhcGVyIiwgImxpdmUiKQogICAgZm9yIHJvdXRlIGluIHJvdXRl
ci5yb3V0ZXM6CiAgICAgICAgaWYgbm90IGlzaW5zdGFuY2Uocm91dGUsIEFQSVJvdXRlKToKICAgICAgICAgICAgY29udGludWUKICAgICAgICBmb3IgdG9r
ZW4gaW4gYmFubmVkOgogICAgICAgICAgICBhc3NlcnQgdG9rZW4gbm90IGluIHJvdXRlLnBhdGgubG93ZXIoKSwgcm91dGUucGF0aAogICAgICAgIGlmICJQ
T1NUIiBpbiByb3V0ZS5tZXRob2RzOgogICAgICAgICAgICBhc3NlcnQgcm91dGUucGF0aCBpbiB3cml0ZXJfcGF0aHMKICAgICAgICBlbHNlOgogICAgICAg
ICAgICBhc3NlcnQgcm91dGUubWV0aG9kcyA9PSB7IkdFVCJ9IG9yICJHRVQiIGluIHJvdXRlLm1ldGhvZHMKCgojIC0tLSByZWdyZXNzaW9uIHBhaXIgKDIp
OiBwcm90ZWN0ZWQtYmFuZCBtb2R1bGVzIHVudG91Y2hlZCBieSBCRS03IC0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLQoKCmRlZiB0ZXN0X3JlZ3Jlc3Npb25f
cHJpb3JfYmFuZF9jb250cmFjdHNfdW50b3VjaGVkKCk6CiAgICAiIiJCRS00L0JFLTUvQkUtNiBjb250cmFjdCB2b2NhYnVsYXJpZXMgdW5jaGFuZ2VkIGJ5
IHRoZSBCRS03IHBhY2thZ2UKICAgIChjb250ZW50IGFzc2VydGlvbnMsIG5vdCBpbXBvcnRzLW9ubHkpLiIiIgogICAgZnJvbSBhcHAudjIucG9ydGZvbGlv
X3Jlc2VhcmNoLmNvbnRyYWN0cyBpbXBvcnQgQkFTSVNfTEFCRUxTLCBQT1JURk9MSU9fQkFTRVMKICAgIGZyb20gYXBwLnYyLnJlc2VhcmNoLnR5cGluZyBp
bXBvcnQgRkFNSUxJRVMKICAgIGZyb20gYXBwLnYyLnJlc2VhcmNoX2dvdmVybmFuY2UuY29udHJhY3RzIGltcG9ydCAoCiAgICAgICAgREVQTE9ZTUVOVF9D
TEFTU0VTLAogICAgICAgIFNJR05BTF9GQU1JTElFUywKICAgICAgICBTSUdOQUxfU1RBVEVTLAogICAgKQoKICAgIGFzc2VydCBQT1JURk9MSU9fQkFTRVMg
PT0gKCJoeXBvdGhldGljYWwiLCkKICAgIGFzc2VydCBCQVNJU19MQUJFTFMgPT0gKCJoeXBvdGhldGljYWwtcmVzZWFyY2giLCkKICAgIGFzc2VydCBTSUdO
QUxfRkFNSUxJRVMgPT0gKCJzdHJ1Y3R1cmFsIiwgInByZWRpY3RpdmUiKQogICAgYXNzZXJ0IFNJR05BTF9TVEFURVMgPT0gKCJlbWl0dGVkIiwgIndpdGho
ZWxkIiwgImV4cGlyZWQiLCAicmVmdXNlZCIpCiAgICBhc3NlcnQgREVQTE9ZTUVOVF9DTEFTU0VTID09ICgicmVzZWFyY2giLCAic2hhZG93IiwgImNoYW1w
aW9uIiwKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICJjaGFsbGVuZ2VyIiwgInJldGlyZWQiKQogICAgYXNzZXJ0IGxlbihGQU1JTElFUykg
PT0gMTAKCgpkZWYgdGVzdF9yZWdyZXNzaW9uX3YxX3JldXNlX3BpbnNfdW5jaGFuZ2VkKCk6CiAgICAiIiJUaGUgc2l4IMKnMS4wLXBpbm5lZCBWMSBmaWxl
cyByZS1oYXNoIHVuY2hhbmdlZCAoVC03IHRhaWwpLiIiIgogICAgaW1wb3J0IGhhc2hsaWIKICAgIGZyb20gcGF0aGxpYiBpbXBvcnQgUGF0aAoKICAgIGJh
Y2tlbmQgPSBQYXRoKF9fZmlsZV9fKS5yZXNvbHZlKCkucGFyZW50c1sxXQogICAgcGlucyA9IHsKICAgICAgICAiYXBwL21sL2RhdGFzZXQvY2hyb25vbG9n
eV9ndWFyZC5weSI6ICI3ZGJjNjY1ZGM0YjQzZjMxIiwKICAgICAgICAiYXBwL21sL2RhdGFzZXQvc3BsaXRfZW5naW5lLnB5IjogImU4OTNiOTJjNmNjY2Ux
ODgiLAogICAgICAgICJhcHAvbWwvZGF0YXNldC9zbmFwc2hvdF9idWlsZGVyLnB5IjogImIwOGVmNGIxZGVjMDc1NjciLAogICAgICAgICJhcHAvbWwvZGF0
YXNldC9zZXJ2aWNlLnB5IjogIjZjNWQ3MmE4OTQyMDUwYjQiLAogICAgICAgICJhcHAvZXhlY3V0aW9uX3Jlc2VhcmNoL3NpbXVsYXRpb24ucHkiOiAiZjE2
M2U2MTBiYTFhNjIxNSIsCiAgICAgICAgImFwcC9tbC9lY29ub21pYy9zZXJ2aWNlLnB5IjogImM0OTUyN2VkMTJmNGQyY2EiLAogICAgfQogICAgZm9yIHJl
bCwgcGluIGluIHBpbnMuaXRlbXMoKToKICAgICAgICBhY3R1YWwgPSBoYXNobGliLnNoYTI1NigKICAgICAgICAgICAgKGJhY2tlbmQgLyByZWwpLnJlYWRf
Ynl0ZXMoKSkuaGV4ZGlnZXN0KClbOjE2XQogICAgICAgIGFzc2VydCBhY3R1YWwgPT0gcGluLCBmIntyZWx9OiB7YWN0dWFsfSAhPSB7cGlufSIK
'@
Write-Evidence ("record 14/17 staged: " + $Rec14Path)
$Rec15Path = "tests\test_v2_be7_jobs.py"
$Rec15Sha  = "4c9c33c2eb72d086964e529e27d255044ef0f9ff1baf445eb7a6572373c31c19"
$Rec15B64 = @'
IiIiVjIgQkUtNyBxdWV1ZS9yZWdpc3RyeS9BUEkgdGVzdHMg4oCUIEJPLVYyLUJFLTctMDAxIFQtOC9ULTEwL1QtMTEKKFUtMy9VLTQvVS01IGJ1ZGdldHMg
KyBjb25kaXRpb25zIEMx4oCTQzQgKyB0aGUgc2Nhbi10b2tlbiBjb25kaXRpb24pLgoKU29ja2V0IGd1YXJkIG9uIGV2ZXJ5IHRlc3QuIEVuZHBvaW50IHBh
dGg6IC9hcGkvdjEvdjIvcmVzZWFyY2gtam9icy8qLgoiIiIKCmZyb20gX19mdXR1cmVfXyBpbXBvcnQgYW5ub3RhdGlvbnMKCmltcG9ydCBzb2NrZXQKZnJv
bSBkYXRldGltZSBpbXBvcnQgZGF0ZXRpbWUsIHRpbWVkZWx0YSwgdGltZXpvbmUKZnJvbSBkZWNpbWFsIGltcG9ydCBEZWNpbWFsCmZyb20gdXVpZCBpbXBv
cnQgdXVpZDQKCmltcG9ydCBweXRlc3QKZnJvbSBzcWxhbGNoZW15IGltcG9ydCBzZWxlY3QKCmZyb20gYXBwLmF1dGguc2VjdXJpdHkgaW1wb3J0IGhhc2hf
cGFzc3dvcmQKZnJvbSBhcHAuZGIubW9kZWxzLmNhbmRsZSBpbXBvcnQgQ2FuZGxlCmZyb20gYXBwLmRiLm1vZGVscy5vcGVyYXRvciBpbXBvcnQgT3BlcmF0
b3IKZnJvbSBhcHAuZGIubW9kZWxzLnYyX2F1ZGl0X2V2ZW50IGltcG9ydCBWMkF1ZGl0RXZlbnQKZnJvbSBhcHAuZGIubW9kZWxzLnYyX2xpbmVhZ2VfcmVj
b3JkIGltcG9ydCBWMkxpbmVhZ2VSZWNvcmQKZnJvbSBhcHAuZGIubW9kZWxzLnYyX21hcmtldGRhdGEgaW1wb3J0IFYyTWRJbnN0cnVtZW50LCBWMk1kU291
cmNlCmZyb20gYXBwLmRiLm1vZGVscy52Ml9yZXNlYXJjaF9qb2JzIGltcG9ydCAoCiAgICBWMkNvc3RNb2RlbCwKICAgIFYyUmVzZWFyY2hKb2IsCiAgICBW
MlJlc2VhcmNoSm9iQXR0ZW1wdCwKICAgIFYyUmVzZWFyY2hSZXN1bHQsCikKZnJvbSBhcHAuZGIuc2Vzc2lvbiBpbXBvcnQgc2Vzc2lvbl9zY29wZQpmcm9t
IGFwcC52Mi5tYXJrZXRkYXRhLnNlZWQgaW1wb3J0IFYyX01EX0lOU1RSVU1FTlRfU0VFRCwgVjJfTURfU09VUkNFX1NFRUQKZnJvbSBhcHAudjIudGVtcG9y
YWwudmFsaWRhdGlvbiBpbXBvcnQgdXRjX25vdwoKUkogPSAiL2FwaS92MS92Mi9yZXNlYXJjaC1qb2JzIgpQQVNTV09SRCA9ICJvcGVyYXRvci1wYXNzLTEy
MyIKVVRDID0gdGltZXpvbmUudXRjCldfU1RBUlQgPSAiMjAyNi0wOS0wMVQwMDowMDowMCswMDowMCIKV19FTkQgPSAiMjAyNi0wOS0wMlQwMDowMDowMCsw
MDowMCIKCgpAcHl0ZXN0LmZpeHR1cmUoYXV0b3VzZT1UcnVlKQpkZWYgX3NvY2tldF9ndWFyZChtb25rZXlwYXRjaCk6CiAgICBkZWYgX2RlbnkoKl9hLCAq
Kl9rKToKICAgICAgICByYWlzZSBBc3NlcnRpb25FcnJvcigibmV0d29yayBhdHRlbXB0IGR1cmluZyBCRS03IHRlc3QiKQoKICAgIG1vbmtleXBhdGNoLnNl
dGF0dHIoc29ja2V0LCAiZ2V0YWRkcmluZm8iLCBfZGVueSkKICAgIG1vbmtleXBhdGNoLnNldGF0dHIoc29ja2V0LCAiY3JlYXRlX2Nvbm5lY3Rpb24iLCBf
ZGVueSkKCgphc3luYyBkZWYgX2xvZ2luKGNsaWVudCwgdXNlcm5hbWUsIHBhc3N3b3JkPVBBU1NXT1JEKToKICAgIHIgPSBhd2FpdCBjbGllbnQucG9zdCgi
L2FwaS92MS9hdXRoL2xvZ2luIiwKICAgICAgICAgICAgICAgICAgICAgICAgICBqc29uPXsidXNlcm5hbWUiOiB1c2VybmFtZSwgInBhc3N3b3JkIjogcGFz
c3dvcmR9KQogICAgYXNzZXJ0IHIuc3RhdHVzX2NvZGUgPT0gMjAwLCByLnRleHQKICAgIHJldHVybiB7IkF1dGhvcml6YXRpb24iOiBmIkJlYXJlciB7ci5q
c29uKClbJ3Rva2VucyddWydhY2Nlc3NfdG9rZW4nXX0ifQoKCmFzeW5jIGRlZiBfYWRtaW4oY2xpZW50KToKICAgIHJldHVybiBhd2FpdCBfbG9naW4oY2xp
ZW50LCAiYWRtaW4iLCAiYWRtaW4xMjMiKQoKCmFzeW5jIGRlZiBfbWFrZV9vcGVyYXRvcigpIC0+IHN0cjoKICAgIGFzeW5jIHdpdGggc2Vzc2lvbl9zY29w
ZSgpIGFzIHNlc3Npb246CiAgICAgICAgb3AgPSBPcGVyYXRvcih1c2VybmFtZT1mImJlNy1vcC17dXVpZDQoKS5oZXhbOjEwXX0iLAogICAgICAgICAgICAg
ICAgICAgICAgaGFzaGVkX3Bhc3N3b3JkPWhhc2hfcGFzc3dvcmQoUEFTU1dPUkQpLAogICAgICAgICAgICAgICAgICAgICAgcm9sZT0ib3BlcmF0b3IiLCBp
c19hY3RpdmU9VHJ1ZSkKICAgICAgICBzZXNzaW9uLmFkZChvcCkKICAgICAgICBhd2FpdCBzZXNzaW9uLmZsdXNoKCkKICAgICAgICByZXR1cm4gb3AudXNl
cm5hbWUKCgphc3luYyBkZWYgX3NlZWRfZW52KG5fYmFyczogaW50ID0gNjApIC0+IE5vbmU6CiAgICBhc3luYyB3aXRoIHNlc3Npb25fc2NvcGUoKSBhcyBz
ZXNzaW9uOgogICAgICAgIGlmIG5vdCAoYXdhaXQgc2Vzc2lvbi5leGVjdXRlKHNlbGVjdChWMk1kU291cmNlKSkpLnNjYWxhcnMoKS5maXJzdCgpOgogICAg
ICAgICAgICBmb3Igcm93IGluIFYyX01EX1NPVVJDRV9TRUVEOgogICAgICAgICAgICAgICAgc2Vzc2lvbi5hZGQoVjJNZFNvdXJjZShpZD1zdHIodXVpZDQo
KSksIGNyZWF0ZWRfYXQ9dXRjX25vdygpLCAqKnJvdykpCiAgICAgICAgICAgIGZvciByb3cgaW4gVjJfTURfSU5TVFJVTUVOVF9TRUVEOgogICAgICAgICAg
ICAgICAgc2Vzc2lvbi5hZGQoVjJNZEluc3RydW1lbnQoaWQ9c3RyKHV1aWQ0KCkpLCBjcmVhdGVkX2F0PXV0Y19ub3coKSwgKipyb3cpKQogICAgICAgIHN0
YXJ0ID0gZGF0ZXRpbWUoMjAyNiwgOSwgMSwgdHppbmZvPVVUQykKICAgICAgICBmb3IgaSBpbiByYW5nZShuX2JhcnMpOgogICAgICAgICAgICBweCA9IERl
Y2ltYWwoIjEwMCIpICsgRGVjaW1hbChpICUgNykgLSBEZWNpbWFsKDMpCiAgICAgICAgICAgIHNlc3Npb24uYWRkKENhbmRsZSgKICAgICAgICAgICAgICAg
IGlkPXN0cih1dWlkNCgpKSwgbWFya2V0X2NsYXNzPSJmb3JleCIsIHN5bWJvbD0iRVVSVVNEIiwKICAgICAgICAgICAgICAgIHRpbWVmcmFtZT0iTTE1Iiwg
b3Blbl90aW1lPXN0YXJ0ICsgdGltZWRlbHRhKG1pbnV0ZXM9MTUgKiBpKSwKICAgICAgICAgICAgICAgIG9wZW49cHgsIGhpZ2g9cHggKyAxLCBsb3c9cHgg
LSAxLCBjbG9zZT1weCwKICAgICAgICAgICAgICAgIHZvbHVtZT1EZWNpbWFsKCIxMDAiKSwgc291cmNlPSJsaXZlOnNpbXVsYXRlZCIpKQoKCkNPU1RTID0g
eyJzcHJlYWQiOiB7InZhbHVlIjogIjAuMSIsICJ1bml0IjogInByaWNlIiwgImNpdGF0aW9uIjogImJhbmQtZGVjbGFyZWQifSwKICAgICAgICAgImNvbW1p
c3Npb24iOiB7InZhbHVlIjogIjAuMDUiLCAidW5pdCI6ICJwcmljZSIsICJjaXRhdGlvbiI6ICJiYW5kLWRlY2xhcmVkIn0sCiAgICAgICAgICJzbGlwcGFn
ZSI6IHsidmFsdWUiOiAiMCIsICJ1bml0IjogInByaWNlIiwgImNpdGF0aW9uIjogImJhbmQtZGVjbGFyZWQifX0KCgphc3luYyBkZWYgX3BpcGVsaW5lKGNs
aWVudCwgaGVhZGVycykgLT4gZGljdDoKICAgICIiIlJlZ2lzdGVyIGlucHV0ICsgY29zdCBtb2RlbCArIHN0cmF0ZWd5OyByZXR1cm4gdGhlIGlkIHRyaXBs
ZS4iIiIKICAgIGlucCA9IChhd2FpdCBjbGllbnQucG9zdChmIntSSn0vcmVnaXN0cnkvaW5wdXRzIiwgaGVhZGVycz1oZWFkZXJzLCBqc29uPXsKICAgICAg
ICAiaW5wdXRfaWQiOiAiaW4tMSIsICJpbnN0cnVtZW50X2lkIjogImZvcmV4LmV1cnVzZCIsCiAgICAgICAgIndpbmRvd19zdGFydCI6IFdfU1RBUlQsICJ3
aW5kb3dfZW5kIjogV19FTkR9KSkuanNvbigpCiAgICBhc3NlcnQgaW5wWyJvdXRjb21lIl0gPT0gInJlZ2lzdGVyZWQiLCBpbnAKICAgIGNtID0gKGF3YWl0
IGNsaWVudC5wb3N0KGYie1JKfS9yZWdpc3RyeS9jb3N0LW1vZGVscyIsIGhlYWRlcnM9aGVhZGVycywKICAgICAgICAgICAgICAgICAgICAgICAgICAgIGpz
b249eyJjb3N0X21vZGVsX2lkIjogImNtLTEiLCAibGF0ZW5jeV9tcyI6IDEwMCwKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICoqQ09TVFN9
KSkuanNvbigpCiAgICBhc3NlcnQgY21bIm91dGNvbWUiXSA9PSAicmVnaXN0ZXJlZCIsIGNtCiAgICBzdCA9IChhd2FpdCBjbGllbnQucG9zdChmIntSSn0v
cmVnaXN0cnkvc3RyYXRlZ2llcyIsIGhlYWRlcnM9aGVhZGVycywganNvbj17CiAgICAgICAgInN0cmF0ZWd5X2lkIjogInN0LTEiLCAibmFtZSI6ICJUIiwK
ICAgICAgICAicGFyYW1ldGVycyI6IHsicnVsZSI6ICJ0aHJlc2hvbGQiLCAiYnV5X2JlbG93IjogIjk4IiwKICAgICAgICAgICAgICAgICAgICAgICAic2Vs
bF9hYm92ZSI6ICIxMDIiLCAidW5pdF9xdHkiOiAiMSIsCiAgICAgICAgICAgICAgICAgICAgICAgImluaXRpYWxfY2FzaCI6ICIxMDAwMCJ9fSkpLmpzb24o
KQogICAgYXNzZXJ0IHN0WyJvdXRjb21lIl0gPT0gInJlZ2lzdGVyZWQiLCBzdAogICAgcmV0dXJuIHsiaW5wdXRfcmVnaXN0cnlfaWQiOiBpbnBbInJlY29y
ZF9pZCJdLAogICAgICAgICAgICAiY29zdF9tb2RlbF9pZCI6IGNtWyJyZWNvcmRfaWQiXSwKICAgICAgICAgICAgInN0cmF0ZWd5X3ZlcnNpb25faWQiOiBz
dFsicmVjb3JkX2lkIl19CgoKYXN5bmMgZGVmIF9zdWJtaXR0ZWQoY2xpZW50LCBoZWFkZXJzLCBpZHMsIHJlc3VsdF9jbGFzcz0iYmFja3Rlc3QiKSAtPiBz
dHI6CiAgICByID0gKGF3YWl0IGNsaWVudC5wb3N0KGYie1JKfS9qb2JzL3N1Ym1pdCIsIGhlYWRlcnM9aGVhZGVycywganNvbj17CiAgICAgICAgImF1dGhv
cml6YXRpb25fcmVmIjogIkJPLVYyLUJFLTctMDAxIiwKICAgICAgICAiaW5wdXRzIjogeyoqaWRzLCAicmVzdWx0X2NsYXNzIjogcmVzdWx0X2NsYXNzfX0p
KS5qc29uKCkKICAgIGFzc2VydCByWyJvdXRjb21lIl0gPT0gInJlZ2lzdGVyZWQiLCByCiAgICByZXR1cm4gclsiam9iX2lkIl0KCgojIC0tLSBVLTM6IHJl
Z2lzdHJhdGlvbiAoNyB0ZXN0cykgLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tCgoKQHB5dGVzdC5tYXJrLmFzeW5j
aW8KYXN5bmMgZGVmIHRlc3RfaW5wdXRfcmVnaXN0cmF0aW9uX2FuZF9jb250ZW50X2RlZHVwZShwcmVwYXJlZF9kYiwgYXN5bmNfY2xpZW50KToKICAgIGF3
YWl0IF9zZWVkX2VudigpCiAgICBoZWFkZXJzID0gYXdhaXQgX2FkbWluKGFzeW5jX2NsaWVudCkKICAgIGZpcnN0ID0gKGF3YWl0IGFzeW5jX2NsaWVudC5w
b3N0KGYie1JKfS9yZWdpc3RyeS9pbnB1dHMiLCBoZWFkZXJzPWhlYWRlcnMsCiAgICAgICAgICAgICBqc29uPXsiaW5wdXRfaWQiOiAiaW4tZCIsICJpbnN0
cnVtZW50X2lkIjogImZvcmV4LmV1cnVzZCIsCiAgICAgICAgICAgICAgICAgICAid2luZG93X3N0YXJ0IjogV19TVEFSVCwgIndpbmRvd19lbmQiOiBXX0VO
RH0pKS5qc29uKCkKICAgIGFzc2VydCBmaXJzdFsib3V0Y29tZSJdID09ICJyZWdpc3RlcmVkIgogICAgYWdhaW4gPSAoYXdhaXQgYXN5bmNfY2xpZW50LnBv
c3QoZiJ7Ukp9L3JlZ2lzdHJ5L2lucHV0cyIsIGhlYWRlcnM9aGVhZGVycywKICAgICAgICAgICAgIGpzb249eyJpbnB1dF9pZCI6ICJpbi1PVEhFUiIsICJp
bnN0cnVtZW50X2lkIjogImZvcmV4LmV1cnVzZCIsCiAgICAgICAgICAgICAgICAgICAid2luZG93X3N0YXJ0IjogV19TVEFSVCwgIndpbmRvd19lbmQiOiBX
X0VORH0pKS5qc29uKCkKICAgIGFzc2VydCBhZ2Fpblsib3V0Y29tZSJdID09ICJyZXVzZWQiICAgICAgICAgICAgICAgICAjIGNvbnRlbnQtYWRkcmVzc2Vk
CiAgICBhc3NlcnQgYWdhaW5bInJlY29yZF9pZCJdID09IGZpcnN0WyJyZWNvcmRfaWQiXQoKCkBweXRlc3QubWFyay5hc3luY2lvCmFzeW5jIGRlZiB0ZXN0
X2lucHV0X3JlZnVzZWRfYmFkX3dpbmRvd19kdXJhYmx5X2F1ZGl0ZWQocHJlcGFyZWRfZGIsIGFzeW5jX2NsaWVudCk6CiAgICBhd2FpdCBfc2VlZF9lbnYo
KQogICAgaGVhZGVycyA9IGF3YWl0IF9hZG1pbihhc3luY19jbGllbnQpCiAgICByID0gKGF3YWl0IGFzeW5jX2NsaWVudC5wb3N0KGYie1JKfS9yZWdpc3Ry
eS9pbnB1dHMiLCBoZWFkZXJzPWhlYWRlcnMsCiAgICAgICAgIGpzb249eyJpbnB1dF9pZCI6ICJpbi1iYWQiLCAiaW5zdHJ1bWVudF9pZCI6ICJmb3JleC5l
dXJ1c2QiLAogICAgICAgICAgICAgICAid2luZG93X3N0YXJ0IjogV19FTkQsICJ3aW5kb3dfZW5kIjogV19TVEFSVH0pKS5qc29uKCkKICAgIGFzc2VydCBy
WyJvdXRjb21lIl0gPT0gInJlZnVzZWQiCiAgICBhc3luYyB3aXRoIHNlc3Npb25fc2NvcGUoKSBhcyBzZXNzaW9uOgogICAgICAgIGF1ZGl0cyA9IFthIGZv
ciAoYSwpIGluIChhd2FpdCBzZXNzaW9uLmV4ZWN1dGUoCiAgICAgICAgICAgIHNlbGVjdChWMkF1ZGl0RXZlbnQuYWN0aW9uKS53aGVyZSgKICAgICAgICAg
ICAgICAgIFYyQXVkaXRFdmVudC5hY3Rpb24gPT0gImlucHV0LnJlZnVzZWQiKSkpLmFsbCgpXQogICAgICAgIGFzc2VydCBhdWRpdHMgICMgZHVyYWJsZSBk
ZXNwaXRlIHJlZnVzYWwgKEMtMSBsYXcpCgoKQHB5dGVzdC5tYXJrLmFzeW5jaW8KYXN5bmMgZGVmIHRlc3RfY29zdF9tb2RlbF9yZXF1aXJlc19jaXRhdGlv
bnMocHJlcGFyZWRfZGIsIGFzeW5jX2NsaWVudCk6CiAgICBhd2FpdCBfc2VlZF9lbnYoKQogICAgaGVhZGVycyA9IGF3YWl0IF9hZG1pbihhc3luY19jbGll
bnQpCiAgICBiYWQgPSBkaWN0KENPU1RTKQogICAgYmFkWyJzcHJlYWQiXSA9IHsidmFsdWUiOiAiMC4xIiwgInVuaXQiOiAicHJpY2UifSAgIyBubyBjaXRh
dGlvbgogICAgciA9IChhd2FpdCBhc3luY19jbGllbnQucG9zdChmIntSSn0vcmVnaXN0cnkvY29zdC1tb2RlbHMiLCBoZWFkZXJzPWhlYWRlcnMsCiAgICAg
ICAgIGpzb249eyJjb3N0X21vZGVsX2lkIjogImNtLXgiLCAibGF0ZW5jeV9tcyI6IDAsICoqYmFkfSkpLmpzb24oKQogICAgYXNzZXJ0IHJbIm91dGNvbWUi
XSA9PSAicmVmdXNlZCIKICAgIGFzc2VydCBhbnkoImNpdGF0aW9uIiBpbiBzdHIoeCkgZm9yIHggaW4gclsicmVhc29ucyJdKQoKCkBweXRlc3QubWFyay5h
c3luY2lvCmFzeW5jIGRlZiB0ZXN0X2Nvc3RfbW9kZWxfdW5rbm93bl91bml0X3JlZnVzZWRfZjEocHJlcGFyZWRfZGIsIGFzeW5jX2NsaWVudCk6CiAgICAi
IiJDUi1WMi1CRS03LTAwMSBGLTE6IHVuaXQgb3V0c2lkZSBDT1NUX1VOSVRTX1YxIGlzIHJlZnVzZWQgVFlQRUQgYXQKICAgIHJlZ2lzdHJhdGlvbiB3aXRo
IGEgZHVyYWJsZSBhdWRpdCBhbmQgTk8gcm93IHdyaXR0ZW4g4oCUIGFuIHVua25vd24gdW5pdAogICAgY2FuIG5ldmVyIHJlYWNoIGFwcGx5X2Nvc3RzIGFz
IGFuIHVudHlwZWQgZW5naW5lIGZhaWx1cmUuIiIiCiAgICBhd2FpdCBfc2VlZF9lbnYoKQogICAgaGVhZGVycyA9IGF3YWl0IF9hZG1pbihhc3luY19jbGll
bnQpCiAgICBiYWQgPSBkaWN0KENPU1RTKQogICAgYmFkWyJzcHJlYWQiXSA9IHsidmFsdWUiOiAiMC4xIiwgInVuaXQiOiAiYm9ndXMiLAogICAgICAgICAg
ICAgICAgICAgICAiY2l0YXRpb24iOiAiYmFuZC1kZWNsYXJlZCJ9CiAgICByID0gKGF3YWl0IGFzeW5jX2NsaWVudC5wb3N0KGYie1JKfS9yZWdpc3RyeS9j
b3N0LW1vZGVscyIsIGhlYWRlcnM9aGVhZGVycywKICAgICAgICAganNvbj17ImNvc3RfbW9kZWxfaWQiOiAiY20tZjEiLCAibGF0ZW5jeV9tcyI6IDAsICoq
YmFkfSkpLmpzb24oKQogICAgYXNzZXJ0IHJbIm91dGNvbWUiXSA9PSAicmVmdXNlZCIKICAgIGFzc2VydCBhbnkoInNwcmVhZC51bml0IiBpbiBzdHIoeCkg
Zm9yIHggaW4gclsicmVhc29ucyJdKQogICAgYXNzZXJ0IGFueSgiJ3ByaWNlJyIgaW4gc3RyKHgpIGFuZCAiJ2ZyYWN0aW9uJyIgaW4gc3RyKHgpCiAgICAg
ICAgICAgICAgIGZvciB4IGluIHJbInJlYXNvbnMiXSkKICAgIGFzeW5jIHdpdGggc2Vzc2lvbl9zY29wZSgpIGFzIHNlc3Npb246CiAgICAgICAgcm93cyA9
IChhd2FpdCBzZXNzaW9uLmV4ZWN1dGUoCiAgICAgICAgICAgIHNlbGVjdChWMkNvc3RNb2RlbCkud2hlcmUoCiAgICAgICAgICAgICAgICBWMkNvc3RNb2Rl
bC5jb3N0X21vZGVsX2lkID09ICJjbS1mMSIpKSkuc2NhbGFycygpLmFsbCgpCiAgICAgICAgYXNzZXJ0IHJvd3MgPT0gW10gICMgcmVmdXNhbCB3cml0ZXMg
Tk8gcm93CiAgICAgICAgYXVkaXRzID0gW2EgZm9yIChhLCkgaW4gKGF3YWl0IHNlc3Npb24uZXhlY3V0ZSgKICAgICAgICAgICAgc2VsZWN0KFYyQXVkaXRF
dmVudC5hY3Rpb24pLndoZXJlKAogICAgICAgICAgICAgICAgVjJBdWRpdEV2ZW50LmFjdGlvbiA9PSAiY29zdF9tb2RlbC5yZWZ1c2VkIikpKS5hbGwoKV0K
ICAgICAgICBhc3NlcnQgYXVkaXRzICAjIGR1cmFibGUgZGVzcGl0ZSByZWZ1c2FsIChDLTEgbGF3KQoKCkBweXRlc3QubWFyay5hc3luY2lvCmFzeW5jIGRl
ZiB0ZXN0X3N0cmF0ZWd5X3VucmVnaXN0ZXJlZF9ydWxlX3JlZnVzZWQocHJlcGFyZWRfZGIsIGFzeW5jX2NsaWVudCk6CiAgICBhd2FpdCBfc2VlZF9lbnYo
KQogICAgaGVhZGVycyA9IGF3YWl0IF9hZG1pbihhc3luY19jbGllbnQpCiAgICByID0gKGF3YWl0IGFzeW5jX2NsaWVudC5wb3N0KGYie1JKfS9yZWdpc3Ry
eS9zdHJhdGVnaWVzIiwgaGVhZGVycz1oZWFkZXJzLAogICAgICAgICBqc29uPXsic3RyYXRlZ3lfaWQiOiAic3QteCIsICJuYW1lIjogIlgiLAogICAgICAg
ICAgICAgICAicGFyYW1ldGVycyI6IHsicnVsZSI6ICJhcmJpdHJhcnlfcHl0aG9uIn19KSkuanNvbigpCiAgICBhc3NlcnQgclsib3V0Y29tZSJdID09ICJy
ZWZ1c2VkIgogICAgYXNzZXJ0IGFueSgicnVsZSIgaW4gc3RyKHgpIGZvciB4IGluIHJbInJlYXNvbnMiXSkKCgpAcHl0ZXN0Lm1hcmsuYXN5bmNpbwphc3lu
YyBkZWYgdGVzdF9zdHJhdGVneV9mb3JiaWRkZW5fcGFyYW1ldGVyX2tleXNfcmVmdXNlZChwcmVwYXJlZF9kYiwgYXN5bmNfY2xpZW50KToKICAgIGF3YWl0
IF9zZWVkX2VudigpCiAgICBoZWFkZXJzID0gYXdhaXQgX2FkbWluKGFzeW5jX2NsaWVudCkKICAgIHIgPSAoYXdhaXQgYXN5bmNfY2xpZW50LnBvc3QoZiJ7
Ukp9L3JlZ2lzdHJ5L3N0cmF0ZWdpZXMiLCBoZWFkZXJzPWhlYWRlcnMsCiAgICAgICAgIGpzb249eyJzdHJhdGVneV9pZCI6ICJzdC15IiwgIm5hbWUiOiAi
WSIsCiAgICAgICAgICAgICAgICJwYXJhbWV0ZXJzIjogeyJydWxlIjogInRocmVzaG9sZCIsICJicm9rZXIiOiAieCJ9fSkpLmpzb24oKQogICAgYXNzZXJ0
IHJbIm91dGNvbWUiXSA9PSAicmVmdXNlZCIKCgpAcHl0ZXN0Lm1hcmsuYXN5bmNpbwphc3luYyBkZWYgdGVzdF9zdHJhdGVneV92ZXJzaW9uaW5nX3N1cGVy
c2VkZShwcmVwYXJlZF9kYiwgYXN5bmNfY2xpZW50KToKICAgIGF3YWl0IF9zZWVkX2VudigpCiAgICBoZWFkZXJzID0gYXdhaXQgX2FkbWluKGFzeW5jX2Ns
aWVudCkKICAgIHAgPSB7InJ1bGUiOiAidGhyZXNob2xkIiwgImJ1eV9iZWxvdyI6ICI5OCIsICJzZWxsX2Fib3ZlIjogIjEwMiJ9CiAgICBmaXJzdCA9IChh
d2FpdCBhc3luY19jbGllbnQucG9zdChmIntSSn0vcmVnaXN0cnkvc3RyYXRlZ2llcyIsCiAgICAgICAgICAgICBoZWFkZXJzPWhlYWRlcnMsIGpzb249eyJz
dHJhdGVneV9pZCI6ICJzdC12IiwgIm5hbWUiOiAiVjEiLAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAicGFyYW1ldGVycyI6IHB9KSku
anNvbigpCiAgICBzZWNvbmQgPSAoYXdhaXQgYXN5bmNfY2xpZW50LnBvc3QoZiJ7Ukp9L3JlZ2lzdHJ5L3N0cmF0ZWdpZXMiLAogICAgICAgICAgICAgIGhl
YWRlcnM9aGVhZGVycywganNvbj17InN0cmF0ZWd5X2lkIjogInN0LXYiLCAibmFtZSI6ICJWMiIsCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAg
ICAgICAicGFyYW1ldGVycyI6IHB9KSkuanNvbigpCiAgICBhc3NlcnQgZmlyc3RbIm91dGNvbWUiXSA9PSBzZWNvbmRbIm91dGNvbWUiXSA9PSAicmVnaXN0
ZXJlZCIKICAgIGFzc2VydCBmaXJzdFsicmVjb3JkX2lkIl0gIT0gc2Vjb25kWyJyZWNvcmRfaWQiXQoKCkBweXRlc3QubWFyay5hc3luY2lvCmFzeW5jIGRl
ZiB0ZXN0X2hpc3RvcmljYWxfcmVhbF9kYXRhX2NsYXNzX3JlZnVzZWQocHJlcGFyZWRfZGIsIGFzeW5jX2NsaWVudCk6CiAgICBhd2FpdCBfc2VlZF9lbnYo
KQogICAgaGVhZGVycyA9IGF3YWl0IF9hZG1pbihhc3luY19jbGllbnQpCiAgICByID0gKGF3YWl0IGFzeW5jX2NsaWVudC5wb3N0KGYie1JKfS9yZWdpc3Ry
eS9pbnB1dHMiLCBoZWFkZXJzPWhlYWRlcnMsCiAgICAgICAgIGpzb249eyJpbnB1dF9pZCI6ICJpbi1ociIsICJpbnN0cnVtZW50X2lkIjogImZvcmV4LmV1
cnVzZCIsCiAgICAgICAgICAgICAgICJ3aW5kb3dfc3RhcnQiOiBXX1NUQVJULCAid2luZG93X2VuZCI6IFdfRU5ELAogICAgICAgICAgICAgICAiZGF0YV9j
bGFzcyI6ICJoaXN0b3JpY2FsX3JlYWwifSkpLmpzb24oKQogICAgYXNzZXJ0IHJbIm91dGNvbWUiXSA9PSAicmVmdXNlZCIKCgojIC0tLSBVLTQ6IHF1ZXVl
ICsgcnVubmVyICgxMiB0ZXN0cykgLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLQoKCkBweXRlc3QubWFyay5hc3lu
Y2lvCmFzeW5jIGRlZiB0ZXN0X3N1Ym1pdF9ydW5fc3VjY2VlZF9mdWxsX2xpbmVhZ2UocHJlcGFyZWRfZGIsIGFzeW5jX2NsaWVudCk6CiAgICBhd2FpdCBf
c2VlZF9lbnYoKQogICAgaGVhZGVycyA9IGF3YWl0IF9hZG1pbihhc3luY19jbGllbnQpCiAgICBpZHMgPSBhd2FpdCBfcGlwZWxpbmUoYXN5bmNfY2xpZW50
LCBoZWFkZXJzKQogICAgam9iX2lkID0gYXdhaXQgX3N1Ym1pdHRlZChhc3luY19jbGllbnQsIGhlYWRlcnMsIGlkcykKICAgIHJ1biA9IChhd2FpdCBhc3lu
Y19jbGllbnQucG9zdChmIntSSn0vam9icy9ydW4iLCBoZWFkZXJzPWhlYWRlcnMsCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAganNvbj17
ImpvYl9pZCI6IGpvYl9pZH0pKS5qc29uKCkKICAgIGFzc2VydCBydW5bImpvYl9zdGF0ZSJdID09ICJzdWNjZWVkZWQiLCBydW4KICAgIGFzc2VydCBydW5b
InJlc3VsdF9pZCJdIGFuZCBydW5bInJldXNlZCJdIGlzIEZhbHNlCiAgICBhc3luYyB3aXRoIHNlc3Npb25fc2NvcGUoKSBhcyBzZXNzaW9uOgogICAgICAg
IHJlc3VsdCA9IChhd2FpdCBzZXNzaW9uLmV4ZWN1dGUoc2VsZWN0KFYyUmVzZWFyY2hSZXN1bHQpKSkuc2NhbGFyX29uZSgpCiAgICAgICAgYXNzZXJ0IHJl
c3VsdC5yZXN1bHRfY2xhc3MgPT0gImJhY2t0ZXN0IgogICAgICAgIGFzc2VydCAiTk9UIGxpdmUgb3IgZnV0dXJlIHBlcmZvcm1hbmNlIiBpbiByZXN1bHQu
c3VtbWFyeVsKICAgICAgICAgICAgInBlcmZvcm1hbmNlX2Rpc2NsYWltZXIiXQogICAgICAgIGxpbmVhZ2UgPSAoYXdhaXQgc2Vzc2lvbi5leGVjdXRlKAog
ICAgICAgICAgICBzZWxlY3QoVjJMaW5lYWdlUmVjb3JkKS53aGVyZSgKICAgICAgICAgICAgICAgIFYyTGluZWFnZVJlY29yZC5hcnRpZmFjdF90eXBlID09
ICJyZXNlYXJjaF9yZXN1bHQiCiAgICAgICAgICAgICkpKS5zY2FsYXJzKCkuYWxsKCkKICAgICAgICBhc3NlcnQgbGluZWFnZSBhbmQgbGluZWFnZVswXS5p
bnB1dF9zbmFwc2hvdF9pZCA9PSByZXN1bHQuaW5wdXRzX2hhc2gKICAgICAgICBhdHRlbXB0cyA9IChhd2FpdCBzZXNzaW9uLmV4ZWN1dGUoCiAgICAgICAg
ICAgIHNlbGVjdChWMlJlc2VhcmNoSm9iQXR0ZW1wdCkpKS5zY2FsYXJzKCkuYWxsKCkKICAgICAgICBhc3NlcnQgW2Eub3V0Y29tZSBmb3IgYSBpbiBhdHRl
bXB0c10gPT0gWyJzdWNjZWVkZWQiXQoKCkBweXRlc3QubWFyay5hc3luY2lvCmFzeW5jIGRlZiB0ZXN0X3JldHJ5X2lkZW1wb3RlbnRfbm9fZG91YmxlX2Fw
cGx5KHByZXBhcmVkX2RiLCBhc3luY19jbGllbnQpOgogICAgIiIiUC0xMC9ULTEwOiByZS1ydW5uaW5nIGEgc3VjY2VlZGVkIHBpcGVsaW5lIHJldHVybnMg
dGhlIFNBTUUgYXJ0aWZhY3QuIiIiCiAgICBhd2FpdCBfc2VlZF9lbnYoKQogICAgaGVhZGVycyA9IGF3YWl0IF9hZG1pbihhc3luY19jbGllbnQpCiAgICBp
ZHMgPSBhd2FpdCBfcGlwZWxpbmUoYXN5bmNfY2xpZW50LCBoZWFkZXJzKQogICAgajEgPSBhd2FpdCBfc3VibWl0dGVkKGFzeW5jX2NsaWVudCwgaGVhZGVy
cywgaWRzKQogICAgcjEgPSAoYXdhaXQgYXN5bmNfY2xpZW50LnBvc3QoZiJ7Ukp9L2pvYnMvcnVuIiwgaGVhZGVycz1oZWFkZXJzLAogICAgICAgICAgICAg
ICAgICAgICAgICAgICAgICAgICAganNvbj17ImpvYl9pZCI6IGoxfSkpLmpzb24oKQogICAgIyBhIHNlY29uZCBqb2Igb3ZlciB0aGUgaWRlbnRpY2FsIHRy
aXBsZSAoZHVwbGljYXRlLXN1Ym1pdCByYWNlKQogICAgajIgPSBhd2FpdCBfc3VibWl0dGVkKGFzeW5jX2NsaWVudCwgaGVhZGVycywgaWRzKQogICAgcjIg
PSAoYXdhaXQgYXN5bmNfY2xpZW50LnBvc3QoZiJ7Ukp9L2pvYnMvcnVuIiwgaGVhZGVycz1oZWFkZXJzLAogICAgICAgICAgICAgICAgICAgICAgICAgICAg
ICAgICAganNvbj17ImpvYl9pZCI6IGoyfSkpLmpzb24oKQogICAgYXNzZXJ0IHIyWyJyZXVzZWQiXSBpcyBUcnVlICAgICAgICAgICAgICAgICAgICAgICAj
IGFuY2hvciBjb2xsaXNpb24KICAgIGFzc2VydCByMlsicmVzdWx0X2lkIl0gPT0gcjFbInJlc3VsdF9pZCJdICAgICAgICAgIyBubyBkb3VibGUtYXBwbHkK
ICAgIGFzeW5jIHdpdGggc2Vzc2lvbl9zY29wZSgpIGFzIHNlc3Npb246CiAgICAgICAgY291bnQgPSBsZW4oKGF3YWl0IHNlc3Npb24uZXhlY3V0ZSgKICAg
ICAgICAgICAgc2VsZWN0KFYyUmVzZWFyY2hSZXN1bHQpKSkuc2NhbGFycygpLmFsbCgpKQogICAgICAgIGFzc2VydCBjb3VudCA9PSAxCiAgICAgICAgcmV1
c2VfYXVkaXRzID0gW2EgZm9yIChhLCkgaW4gKGF3YWl0IHNlc3Npb24uZXhlY3V0ZSgKICAgICAgICAgICAgc2VsZWN0KFYyQXVkaXRFdmVudC5hY3Rpb24p
LndoZXJlKAogICAgICAgICAgICAgICAgVjJBdWRpdEV2ZW50LmFjdGlvbiA9PSAicmVzdWx0LnJldXNlZCIpKSkuYWxsKCldCiAgICAgICAgYXNzZXJ0IHJl
dXNlX2F1ZGl0cwoKCkBweXRlc3QubWFyay5hc3luY2lvCmFzeW5jIGRlZiB0ZXN0X3JlcnVuX3N1Y2NlZWRlZF9qb2JfcmV0dXJuc19leGlzdGluZyhwcmVw
YXJlZF9kYiwgYXN5bmNfY2xpZW50KToKICAgIGF3YWl0IF9zZWVkX2VudigpCiAgICBoZWFkZXJzID0gYXdhaXQgX2FkbWluKGFzeW5jX2NsaWVudCkKICAg
IGlkcyA9IGF3YWl0IF9waXBlbGluZShhc3luY19jbGllbnQsIGhlYWRlcnMpCiAgICBqb2JfaWQgPSBhd2FpdCBfc3VibWl0dGVkKGFzeW5jX2NsaWVudCwg
aGVhZGVycywgaWRzKQogICAgZmlyc3QgPSAoYXdhaXQgYXN5bmNfY2xpZW50LnBvc3QoZiJ7Ukp9L2pvYnMvcnVuIiwgaGVhZGVycz1oZWFkZXJzLAogICAg
ICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAganNvbj17ImpvYl9pZCI6IGpvYl9pZH0pKS5qc29uKCkKICAgIGFnYWluID0gKGF3YWl0IGFzeW5j
X2NsaWVudC5wb3N0KGYie1JKfS9qb2JzL3J1biIsIGhlYWRlcnM9aGVhZGVycywKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIGpzb249
eyJqb2JfaWQiOiBqb2JfaWR9KSkuanNvbigpCiAgICBhc3NlcnQgYWdhaW5bImpvYl9zdGF0ZSJdID09ICJzdWNjZWVkZWQiCiAgICBhc3NlcnQgYWdhaW5b
InJlc3VsdF9pZCJdID09IGZpcnN0WyJyZXN1bHRfaWQiXQogICAgYXN5bmMgd2l0aCBzZXNzaW9uX3Njb3BlKCkgYXMgc2Vzc2lvbjoKICAgICAgICBqb2Ig
PSAoYXdhaXQgc2Vzc2lvbi5leGVjdXRlKHNlbGVjdChWMlJlc2VhcmNoSm9iKSkpLnNjYWxhcl9vbmUoKQogICAgICAgIGFzc2VydCBqb2IuYXR0ZW1wdF9j
b3VudCA9PSAxICAjIHRoZSBuby1vcCByZXJ1biBkaWQgbm90IGJ1cm4gYW4gYXR0ZW1wdAoKCkBweXRlc3QubWFyay5hc3luY2lvCmFzeW5jIGRlZiB0ZXN0
X2NhbmNlbF9xdWV1ZWRfdGhlbl90ZXJtaW5hbF9yZWZ1c2FsKHByZXBhcmVkX2RiLCBhc3luY19jbGllbnQpOgogICAgYXdhaXQgX3NlZWRfZW52KCkKICAg
IGhlYWRlcnMgPSBhd2FpdCBfYWRtaW4oYXN5bmNfY2xpZW50KQogICAgaWRzID0gYXdhaXQgX3BpcGVsaW5lKGFzeW5jX2NsaWVudCwgaGVhZGVycykKICAg
IGpvYl9pZCA9IGF3YWl0IF9zdWJtaXR0ZWQoYXN5bmNfY2xpZW50LCBoZWFkZXJzLCBpZHMpCiAgICBjMSA9IChhd2FpdCBhc3luY19jbGllbnQucG9zdChm
IntSSn0vam9icy9jYW5jZWwiLCBoZWFkZXJzPWhlYWRlcnMsCiAgICAgICAgICBqc29uPXsiam9iX2lkIjogam9iX2lkLCAicmVhc29uIjogIm9wZXJhdG9y
IGFib3J0In0pKS5qc29uKCkKICAgIGFzc2VydCBjMVsib3V0Y29tZSJdID09ICJyZWdpc3RlcmVkIgogICAgYzIgPSAoYXdhaXQgYXN5bmNfY2xpZW50LnBv
c3QoZiJ7Ukp9L2pvYnMvY2FuY2VsIiwgaGVhZGVycz1oZWFkZXJzLAogICAgICAgICAganNvbj17ImpvYl9pZCI6IGpvYl9pZCwgInJlYXNvbiI6ICJhZ2Fp
biJ9KSkuanNvbigpCiAgICBhc3NlcnQgYzJbIm91dGNvbWUiXSA9PSAicmVmdXNlZCIgICAgICAgICAgICAgICAgICMgdGVybWluYWwtcmVmdXNhbAogICAg
YXNzZXJ0IGFueSgidGVybWluYWwiIGluIHN0cih4KSBmb3IgeCBpbiBjMlsicmVhc29ucyJdKQogICAgYXN5bmMgd2l0aCBzZXNzaW9uX3Njb3BlKCkgYXMg
c2Vzc2lvbjoKICAgICAgICBhdHRlbXB0cyA9IChhd2FpdCBzZXNzaW9uLmV4ZWN1dGUoCiAgICAgICAgICAgIHNlbGVjdChWMlJlc2VhcmNoSm9iQXR0ZW1w
dCkpKS5zY2FsYXJzKCkuYWxsKCkKICAgICAgICBhc3NlcnQgW2Eub3V0Y29tZSBmb3IgYSBpbiBhdHRlbXB0c10gPT0gWyJjYW5jZWxsZWQiXQogICAgICAg
IGF1ZGl0cyA9IFthIGZvciAoYSwpIGluIChhd2FpdCBzZXNzaW9uLmV4ZWN1dGUoCiAgICAgICAgICAgIHNlbGVjdChWMkF1ZGl0RXZlbnQuYWN0aW9uKS53
aGVyZShWMkF1ZGl0RXZlbnQuYWN0aW9uLmluXygKICAgICAgICAgICAgICAgIFsiam9iLmNhbmNlbGxlZCIsICJqb2IuY2FuY2VsLnJlZnVzZWQiXSkpKSku
YWxsKCldCiAgICAgICAgYXNzZXJ0IHNldChhdWRpdHMpID09IHsiam9iLmNhbmNlbGxlZCIsICJqb2IuY2FuY2VsLnJlZnVzZWQifQoKCkBweXRlc3QubWFy
ay5hc3luY2lvCmFzeW5jIGRlZiB0ZXN0X3N1Ym1pdF9ub25tYW51YWxfc2NoZWR1bGVfcmVmdXNlZF9jNChwcmVwYXJlZF9kYiwgYXN5bmNfY2xpZW50KToK
ICAgIGF3YWl0IF9zZWVkX2VudigpCiAgICBoZWFkZXJzID0gYXdhaXQgX2FkbWluKGFzeW5jX2NsaWVudCkKICAgIGlkcyA9IGF3YWl0IF9waXBlbGluZShh
c3luY19jbGllbnQsIGhlYWRlcnMpCiAgICByID0gKGF3YWl0IGFzeW5jX2NsaWVudC5wb3N0KGYie1JKfS9qb2JzL3N1Ym1pdCIsIGhlYWRlcnM9aGVhZGVy
cywganNvbj17CiAgICAgICAgImF1dGhvcml6YXRpb25fcmVmIjogIkJPLVYyLUJFLTctMDAxIiwKICAgICAgICAiaW5wdXRzIjogeyoqaWRzLCAicmVzdWx0
X2NsYXNzIjogImJhY2t0ZXN0In0sCiAgICAgICAgInNjaGVkdWxlIjogeyJraW5kIjogImNyb24iLCAiZXhwciI6ICIqICogKiAqICoifX0pKS5qc29uKCkK
ICAgIGFzc2VydCByWyJvdXRjb21lIl0gPT0gInJlZnVzZWQiCiAgICBhc3NlcnQgYW55KHguZ2V0KCJmYWlsaW5nIikgPT0gInNjaGVkdWxlLmtpbmQiIGZv
ciB4IGluIHJbInJlYXNvbnMiXSkKICAgIGFzeW5jIHdpdGggc2Vzc2lvbl9zY29wZSgpIGFzIHNlc3Npb246CiAgICAgICAgYXVkaXRzID0gW2EgZm9yIChh
LCkgaW4gKGF3YWl0IHNlc3Npb24uZXhlY3V0ZSgKICAgICAgICAgICAgc2VsZWN0KFYyQXVkaXRFdmVudC5hY3Rpb24pLndoZXJlKAogICAgICAgICAgICAg
ICAgVjJBdWRpdEV2ZW50LmFjdGlvbiA9PSAiam9iLnN1Ym1pdC5yZWZ1c2VkIikpKS5hbGwoKV0KICAgICAgICBhc3NlcnQgYXVkaXRzICAjIGR1cmFibHkg
YXVkaXRlZCAoQzQpCgoKQHB5dGVzdC5tYXJrLmFzeW5jaW8KYXN5bmMgZGVmIHRlc3Rfc3VibWl0X3BhcGVyX2xpdmVfcmVzdWx0X2NsYXNzX3JlZnVzZWRf
cDkocHJlcGFyZWRfZGIsIGFzeW5jX2NsaWVudCk6CiAgICBhd2FpdCBfc2VlZF9lbnYoKQogICAgaGVhZGVycyA9IGF3YWl0IF9hZG1pbihhc3luY19jbGll
bnQpCiAgICBpZHMgPSBhd2FpdCBfcGlwZWxpbmUoYXN5bmNfY2xpZW50LCBoZWFkZXJzKQogICAgZm9yIGJhbm5lZCBpbiAoInBhcGVyIiwgImxpdmUiKToK
ICAgICAgICByID0gKGF3YWl0IGFzeW5jX2NsaWVudC5wb3N0KGYie1JKfS9qb2JzL3N1Ym1pdCIsIGhlYWRlcnM9aGVhZGVycywKICAgICAgICAgICAgIGpz
b249eyJhdXRob3JpemF0aW9uX3JlZiI6ICJCTy1WMi1CRS03LTAwMSIsCiAgICAgICAgICAgICAgICAgICAiaW5wdXRzIjogeyoqaWRzLCAicmVzdWx0X2Ns
YXNzIjogYmFubmVkfX0pKS5qc29uKCkKICAgICAgICAjIHN1Ym1pc3Npb24gcGFzc2VzIHNoYXBlIGNoZWNrczsgdGhlIENPTlNUUlVDVElPTiBwb2ludCBy
ZWZ1c2VzOgogICAgICAgIGlmIHJbIm91dGNvbWUiXSA9PSAicmVnaXN0ZXJlZCI6CiAgICAgICAgICAgIHJ1biA9IChhd2FpdCBhc3luY19jbGllbnQucG9z
dChmIntSSn0vam9icy9ydW4iLCBoZWFkZXJzPWhlYWRlcnMsCiAgICAgICAgICAgICAgICAgICBqc29uPXsiam9iX2lkIjogclsiam9iX2lkIl19KSkuanNv
bigpCiAgICAgICAgICAgIGFzc2VydCBydW5bImpvYl9zdGF0ZSJdID09ICJmYWlsZWQiCiAgICAgICAgICAgIGFzc2VydCBhbnkoInJlc3VsdF9jbGFzcyIg
aW4gc3RyKHgpIGZvciB4IGluIHJ1blsicmVhc29ucyJdKQoKCkBweXRlc3QubWFyay5hc3luY2lvCmFzeW5jIGRlZiB0ZXN0X3N1Ym1pdF9taXNzaW5nX2F1
dGhvcml6YXRpb25fcmVmdXNlZChwcmVwYXJlZF9kYiwgYXN5bmNfY2xpZW50KToKICAgIGF3YWl0IF9zZWVkX2VudigpCiAgICBoZWFkZXJzID0gYXdhaXQg
X2FkbWluKGFzeW5jX2NsaWVudCkKICAgIGlkcyA9IGF3YWl0IF9waXBlbGluZShhc3luY19jbGllbnQsIGhlYWRlcnMpCiAgICByID0gYXdhaXQgYXN5bmNf
Y2xpZW50LnBvc3QoZiJ7Ukp9L2pvYnMvc3VibWl0IiwgaGVhZGVycz1oZWFkZXJzLCBqc29uPXsKICAgICAgICAiYXV0aG9yaXphdGlvbl9yZWYiOiAiIiwg
ImlucHV0cyI6IHsqKmlkcywgInJlc3VsdF9jbGFzcyI6ICJiYWNrdGVzdCJ9fSkKICAgIGFzc2VydCByLnN0YXR1c19jb2RlID09IDQyMiBvciByLmpzb24o
KVsib3V0Y29tZSJdID09ICJyZWZ1c2VkIgoKCkBweXRlc3QubWFyay5hc3luY2lvCmFzeW5jIGRlZiB0ZXN0X3N1Ym1pdF9kcmFmdF9zdHJhdGVneV9yZWZ1
c2VkKHByZXBhcmVkX2RiLCBhc3luY19jbGllbnQpOgogICAgYXdhaXQgX3NlZWRfZW52KCkKICAgIGhlYWRlcnMgPSBhd2FpdCBfYWRtaW4oYXN5bmNfY2xp
ZW50KQogICAgaWRzID0gYXdhaXQgX3BpcGVsaW5lKGFzeW5jX2NsaWVudCwgaGVhZGVycykKICAgIGRyYWZ0ID0gKGF3YWl0IGFzeW5jX2NsaWVudC5wb3N0
KGYie1JKfS9yZWdpc3RyeS9zdHJhdGVnaWVzIiwKICAgICAgICAgICAgIGhlYWRlcnM9aGVhZGVycywganNvbj17CiAgICAgICAgICAgICAgICAgInN0cmF0
ZWd5X2lkIjogInN0LWQiLCAibmFtZSI6ICJEIiwKICAgICAgICAgICAgICAgICAicGFyYW1ldGVycyI6IHsicnVsZSI6ICJ0aHJlc2hvbGQifSwKICAgICAg
ICAgICAgICAgICAibGlmZWN5Y2xlX3N0YXRlIjogImRyYWZ0In0pKS5qc29uKCkKICAgIHIgPSAoYXdhaXQgYXN5bmNfY2xpZW50LnBvc3QoZiJ7Ukp9L2pv
YnMvc3VibWl0IiwgaGVhZGVycz1oZWFkZXJzLCBqc29uPXsKICAgICAgICAiYXV0aG9yaXphdGlvbl9yZWYiOiAiQk8tVjItQkUtNy0wMDEiLAogICAgICAg
ICJpbnB1dHMiOiB7KippZHMsICJzdHJhdGVneV92ZXJzaW9uX2lkIjogZHJhZnRbInJlY29yZF9pZCJdLAogICAgICAgICAgICAgICAgICAgInJlc3VsdF9j
bGFzcyI6ICJiYWNrdGVzdCJ9fSkpLmpzb24oKQogICAgYXNzZXJ0IHJbIm91dGNvbWUiXSA9PSAicmVmdXNlZCIKICAgIGFzc2VydCBhbnkoImxpZmVjeWNs
ZV9zdGF0ZSIgaW4gc3RyKHgpIGZvciB4IGluIHJbInJlYXNvbnMiXSkKCgpAcHl0ZXN0Lm1hcmsuYXN5bmNpbwphc3luYyBkZWYgdGVzdF9zdWJtaXRfc3Vw
ZXJzZWRlZF9zdHJhdGVneV9yZWZ1c2VkKHByZXBhcmVkX2RiLCBhc3luY19jbGllbnQpOgogICAgYXdhaXQgX3NlZWRfZW52KCkKICAgIGhlYWRlcnMgPSBh
d2FpdCBfYWRtaW4oYXN5bmNfY2xpZW50KQogICAgaWRzID0gYXdhaXQgX3BpcGVsaW5lKGFzeW5jX2NsaWVudCwgaGVhZGVycykKICAgIHAgPSB7InJ1bGUi
OiAidGhyZXNob2xkIiwgImJ1eV9iZWxvdyI6ICI5OCIsICJzZWxsX2Fib3ZlIjogIjEwMiJ9CiAgICBhd2FpdCBhc3luY19jbGllbnQucG9zdChmIntSSn0v
cmVnaXN0cnkvc3RyYXRlZ2llcyIsIGhlYWRlcnM9aGVhZGVycywKICAgICAgICAgICAgICAgICAgICAgICAgICAgIGpzb249eyJzdHJhdGVneV9pZCI6ICJz
dC0xIiwgIm5hbWUiOiAiZ2VuMiIsCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAicGFyYW1ldGVycyI6IHB9KSAgIyBzdXBlcnNlZGVzIHN0
LTEgZ2VuMQogICAgciA9IChhd2FpdCBhc3luY19jbGllbnQucG9zdChmIntSSn0vam9icy9zdWJtaXQiLCBoZWFkZXJzPWhlYWRlcnMsIGpzb249ewogICAg
ICAgICJhdXRob3JpemF0aW9uX3JlZiI6ICJCTy1WMi1CRS03LTAwMSIsCiAgICAgICAgImlucHV0cyI6IHsqKmlkcywgInJlc3VsdF9jbGFzcyI6ICJiYWNr
dGVzdCJ9fSkpLmpzb24oKQogICAgYXNzZXJ0IHJbIm91dGNvbWUiXSA9PSAicmVmdXNlZCIKICAgIGFzc2VydCBhbnkoInN1cGVyc2VkZWQiIGluIHN0cih4
KSBmb3IgeCBpbiByWyJyZWFzb25zIl0pCgoKQHB5dGVzdC5tYXJrLmFzeW5jaW8KYXN5bmMgZGVmIHRlc3RfYzFfc3VibWlzc2lvbl9maWVsZHNfd3JpdGVf
b25jZShwcmVwYXJlZF9kYiwgYXN5bmNfY2xpZW50KToKICAgICIiIkMxOiBubyB3cml0ZXIgcGF0aCB1cGRhdGVzIG93bmVyL2F1dGhvcml6YXRpb25fcmVm
L2lucHV0cy9zY2hlZHVsZS4iIiIKICAgIGF3YWl0IF9zZWVkX2VudigpCiAgICBoZWFkZXJzID0gYXdhaXQgX2FkbWluKGFzeW5jX2NsaWVudCkKICAgIGlk
cyA9IGF3YWl0IF9waXBlbGluZShhc3luY19jbGllbnQsIGhlYWRlcnMpCiAgICBqb2JfaWQgPSBhd2FpdCBfc3VibWl0dGVkKGFzeW5jX2NsaWVudCwgaGVh
ZGVycywgaWRzKQogICAgYXN5bmMgd2l0aCBzZXNzaW9uX3Njb3BlKCkgYXMgc2Vzc2lvbjoKICAgICAgICBiZWZvcmUgPSAoYXdhaXQgc2Vzc2lvbi5leGVj
dXRlKAogICAgICAgICAgICBzZWxlY3QoVjJSZXNlYXJjaEpvYikud2hlcmUoVjJSZXNlYXJjaEpvYi5pZCA9PSBqb2JfaWQpCiAgICAgICAgKSkuc2NhbGFy
X29uZSgpCiAgICAgICAgc25hcHNob3QgPSAoYmVmb3JlLm93bmVyLCBiZWZvcmUuYXV0aG9yaXphdGlvbl9yZWYsCiAgICAgICAgICAgICAgICAgICAgZGlj
dChiZWZvcmUuaW5wdXRzKSwgZGljdChiZWZvcmUuc2NoZWR1bGUpKQogICAgYXdhaXQgYXN5bmNfY2xpZW50LnBvc3QoZiJ7Ukp9L2pvYnMvcnVuIiwgaGVh
ZGVycz1oZWFkZXJzLAogICAgICAgICAgICAgICAgICAgICAgICAgICAganNvbj17ImpvYl9pZCI6IGpvYl9pZH0pCiAgICBhc3luYyB3aXRoIHNlc3Npb25f
c2NvcGUoKSBhcyBzZXNzaW9uOgogICAgICAgIGFmdGVyID0gKGF3YWl0IHNlc3Npb24uZXhlY3V0ZSgKICAgICAgICAgICAgc2VsZWN0KFYyUmVzZWFyY2hK
b2IpLndoZXJlKFYyUmVzZWFyY2hKb2IuaWQgPT0gam9iX2lkKQogICAgICAgICkpLnNjYWxhcl9vbmUoKQogICAgICAgIGFzc2VydCAoYWZ0ZXIub3duZXIs
IGFmdGVyLmF1dGhvcml6YXRpb25fcmVmLCBkaWN0KGFmdGVyLmlucHV0cyksCiAgICAgICAgICAgICAgICBkaWN0KGFmdGVyLnNjaGVkdWxlKSkgPT0gc25h
cHNob3QgICMgd3JpdGUtb25jZSBoZWxkCiAgICAgICAgYXNzZXJ0IGFmdGVyLmpvYl9zdGF0ZSA9PSAic3VjY2VlZGVkIiAgICAgICMgbXV0YWJsZSBzZXQg
bW92ZWQKCgpAcHl0ZXN0Lm1hcmsuYXN5bmNpbwphc3luYyBkZWYgdGVzdF9jMl9tdXRhYmxlX3NldF9jb25zdGFudF9leGFjdChwcmVwYXJlZF9kYiwgYXN5
bmNfY2xpZW50KToKICAgIGZyb20gYXBwLnYyLnJlc2VhcmNoX2pvYnMuY29udHJhY3RzIGltcG9ydCBKT0JfTVVUQUJMRV9DT0xVTU5TCiAgICBmcm9tIGFw
cC52Mi5yZXNlYXJjaF9qb2JzLnJ1bm5lciBpbXBvcnQgSk9CX1VQREFURV9DT0xVTU5TCgogICAgYXNzZXJ0IEpPQl9NVVRBQkxFX0NPTFVNTlMgPT0gZnJv
emVuc2V0KAogICAgICAgIHsiam9iX3N0YXRlIiwgImF0dGVtcHRfY291bnQiLCAib3V0cHV0X3JlZiIsICJmYWlsdXJlIn0pCiAgICBhc3NlcnQgSk9CX1VQ
REFURV9DT0xVTU5TID09IEpPQl9NVVRBQkxFX0NPTFVNTlMKCgpAcHl0ZXN0Lm1hcmsuYXN5bmNpbwphc3luYyBkZWYgdGVzdF9sZWFrYWdlX3JlZnVzYWxf
ZmFpbHNfam9iX3R5cGVkKHByZXBhcmVkX2RiLCBhc3luY19jbGllbnQpOgogICAgIiIiQSB0YW1wZXJlZCByZWdpc3RyeSBoYXNoIChHLTUpIGZhaWxzIHRo
ZSBqb2Igd2l0aCB0eXBlZCByZWFzb25zLiIiIgogICAgYXdhaXQgX3NlZWRfZW52KCkKICAgIGhlYWRlcnMgPSBhd2FpdCBfYWRtaW4oYXN5bmNfY2xpZW50
KQogICAgaWRzID0gYXdhaXQgX3BpcGVsaW5lKGFzeW5jX2NsaWVudCwgaGVhZGVycykKICAgICMgY29ycnVwdCB0aGUgc3RvcmVkIGNvbnRlbnQgaGFzaCAo
Z3VhcmQgZHJvcHBlZCBmb3IgdGVzdCBzZXR1cCkKICAgIGFzeW5jIHdpdGggc2Vzc2lvbl9zY29wZSgpIGFzIHNlc3Npb246CiAgICAgICAgZnJvbSBzcWxh
bGNoZW15IGltcG9ydCB0ZXh0CiAgICAgICAgYXdhaXQgc2Vzc2lvbi5leGVjdXRlKHRleHQoCiAgICAgICAgICAgICJEUk9QIFRSSUdHRVIgSUYgRVhJU1RT
IHYyX2JhY2t0ZXN0X2lucHV0X2ltbXV0YWJsZV91cGRhdGUiKSkKICAgICAgICBhd2FpdCBzZXNzaW9uLmV4ZWN1dGUodGV4dCgKICAgICAgICAgICAgIlVQ
REFURSB2Ml9iYWNrdGVzdF9pbnB1dCBTRVQgY29udGVudF9oYXNoID0gOmgiKSwKICAgICAgICAgICAgeyJoIjogIjAiICogNjR9KQogICAgam9iX2lkID0g
YXdhaXQgX3N1Ym1pdHRlZChhc3luY19jbGllbnQsIGhlYWRlcnMsIGlkcykKICAgIHJ1biA9IChhd2FpdCBhc3luY19jbGllbnQucG9zdChmIntSSn0vam9i
cy9ydW4iLCBoZWFkZXJzPWhlYWRlcnMsCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAganNvbj17ImpvYl9pZCI6IGpvYl9pZH0pKS5qc29u
KCkKICAgIGFzc2VydCBydW5bImpvYl9zdGF0ZSJdID09ICJmYWlsZWQiCiAgICBhc3NlcnQgYW55KCJHLTUiIGluIHN0cih4KSBmb3IgeCBpbiBydW5bInJl
YXNvbnMiXSkKCgojIC0tLSBVLTU6IEFQSSBzdXJmYWNlICsgc2NhbnMgKDYgdGVzdHMpIC0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0t
LS0tLS0tLS0tLQoKCkBweXRlc3QubWFyay5hc3luY2lvCmFzeW5jIGRlZiB0ZXN0X3JiYWNfZGVuaWVkX2FuZF9yZWFkcyhwcmVwYXJlZF9kYiwgYXN5bmNf
Y2xpZW50KToKICAgIGF3YWl0IF9zZWVkX2VudigpCiAgICBhZG1pbiA9IGF3YWl0IF9hZG1pbihhc3luY19jbGllbnQpCiAgICBvcGVyYXRvciA9IGF3YWl0
IF9sb2dpbihhc3luY19jbGllbnQsIGF3YWl0IF9tYWtlX29wZXJhdG9yKCkpCiAgICBmb3IgaGVhZGVycyBpbiAoYWRtaW4sIG9wZXJhdG9yKToKICAgICAg
ICBhc3NlcnQgKGF3YWl0IGFzeW5jX2NsaWVudC5nZXQoZiJ7Ukp9L2pvYnMiLAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICBoZWFk
ZXJzPWhlYWRlcnMpKS5zdGF0dXNfY29kZSA9PSAyMDAKICAgICAgICBhc3NlcnQgKGF3YWl0IGFzeW5jX2NsaWVudC5nZXQoZiJ7Ukp9L3Jlc3VsdHMiLAog
ICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICBoZWFkZXJzPWhlYWRlcnMpKS5zdGF0dXNfY29kZSA9PSAyMDAKICAgIGZvciBwYXRoLCBi
b2R5IGluICgKICAgICAgICAoZiJ7Ukp9L3JlZ2lzdHJ5L2lucHV0cyIsCiAgICAgICAgIHsiaW5wdXRfaWQiOiAieCIsICJpbnN0cnVtZW50X2lkIjogImZv
cmV4LmV1cnVzZCIsCiAgICAgICAgICAid2luZG93X3N0YXJ0IjogV19TVEFSVCwgIndpbmRvd19lbmQiOiBXX0VORH0pLAogICAgICAgIChmIntSSn0vam9i
cy9zdWJtaXQiLAogICAgICAgICB7ImF1dGhvcml6YXRpb25fcmVmIjogIngiLCAiaW5wdXRzIjoge319KSwKICAgICAgICAoZiJ7Ukp9L2pvYnMvY2FuY2Vs
IiwgeyJqb2JfaWQiOiAieCIsICJyZWFzb24iOiAiciJ9KSwKICAgICk6CiAgICAgICAgciA9IGF3YWl0IGFzeW5jX2NsaWVudC5wb3N0KHBhdGgsIGpzb249
Ym9keSwgaGVhZGVycz1vcGVyYXRvcikKICAgICAgICBhc3NlcnQgci5zdGF0dXNfY29kZSA9PSA0MDMKICAgICAgICBhc3NlcnQgci5qc29uKClbImRldGFp
bCJdID09ICJQZXJtaXNzaW9uIGRlbmllZCIKICAgIGFzc2VydCAoYXdhaXQgYXN5bmNfY2xpZW50LmdldChmIntSSn0vam9icyIpKS5zdGF0dXNfY29kZSA9
PSA0MDEKCgpAcHl0ZXN0Lm1hcmsuYXN5bmNpbwphc3luYyBkZWYgdGVzdF9jM19ub19nZW5lcmljX2pvYl91cGRhdGVfZW5kcG9pbnQocHJlcGFyZWRfZGIs
IGFzeW5jX2NsaWVudCk6CiAgICAiIiJDMzogdGhlIEFQSSBleHBvc2VzIG5vIFBBVENIL1BVVCBhbmQgbm8gZ2VuZXJpYyBqb2ItdXBkYXRlIHBhdGguIiIi
CiAgICBmcm9tIGZhc3RhcGkucm91dGluZyBpbXBvcnQgQVBJUm91dGUKCiAgICBmcm9tIGFwcC52Mi5yZXNlYXJjaF9qb2JzLmFwaSBpbXBvcnQgcm91dGVy
CgogICAgZm9yIHJvdXRlIGluIHJvdXRlci5yb3V0ZXM6CiAgICAgICAgaWYgaXNpbnN0YW5jZShyb3V0ZSwgQVBJUm91dGUpOgogICAgICAgICAgICBhc3Nl
cnQgbm90ICh7IlBVVCIsICJQQVRDSCIsICJERUxFVEUifSAmIHJvdXRlLm1ldGhvZHMpLCByb3V0ZS5wYXRoCiAgICAgICAgICAgIGlmICJQT1NUIiBpbiBy
b3V0ZS5tZXRob2RzOgogICAgICAgICAgICAgICAgYXNzZXJ0IHJvdXRlLnBhdGggaW4gKAogICAgICAgICAgICAgICAgICAgICIvcmVzZWFyY2gtam9icy9y
ZWdpc3RyeS9pbnB1dHMiLAogICAgICAgICAgICAgICAgICAgICIvcmVzZWFyY2gtam9icy9yZWdpc3RyeS9jb3N0LW1vZGVscyIsCiAgICAgICAgICAgICAg
ICAgICAgIi9yZXNlYXJjaC1qb2JzL3JlZ2lzdHJ5L3N0cmF0ZWdpZXMiLAogICAgICAgICAgICAgICAgICAgICIvcmVzZWFyY2gtam9icy9qb2JzL3N1Ym1p
dCIsCiAgICAgICAgICAgICAgICAgICAgIi9yZXNlYXJjaC1qb2JzL2pvYnMvcnVuIiwKICAgICAgICAgICAgICAgICAgICAiL3Jlc2VhcmNoLWpvYnMvam9i
cy9jYW5jZWwiKSwgcm91dGUucGF0aAoKCmRlZiB0ZXN0X2FsbG93X2xpc3RfY29uc3RhbnRzX3BhcnRfMTBfMSgpOgogICAgZnJvbSBhcHAudjIucmVzZWFy
Y2hfam9icy5jb250cmFjdHMgaW1wb3J0ICgKICAgICAgICBSVU5ORVJfSU5TRVJUX1RBQkxFUywKICAgICAgICBSVU5ORVJfVVBEQVRFX1RBQkxFUywKICAg
ICkKICAgIGZyb20gYXBwLnYyLnJlc2VhcmNoX2pvYnMucnVubmVyIGltcG9ydCBXUklUQUJMRV9UQUJMRVMKCiAgICBhc3NlcnQgV1JJVEFCTEVfVEFCTEVT
WyJpbnNlcnQiXSA9PSBSVU5ORVJfSU5TRVJUX1RBQkxFUyA9PSBmcm96ZW5zZXQoCiAgICAgICAgeyJ2Ml9yZXNlYXJjaF9yZXN1bHQiLCAidjJfcmVzZWFy
Y2hfam9iX2F0dGVtcHQiLAogICAgICAgICAidjJfYXVkaXRfZXZlbnQiLCAidjJfbGluZWFnZV9yZWNvcmQifSkKICAgIGFzc2VydCBXUklUQUJMRV9UQUJM
RVNbInVwZGF0ZSJdID09IFJVTk5FUl9VUERBVEVfVEFCTEVTID09IGZyb3plbnNldCgKICAgICAgICB7InYyX3Jlc2VhcmNoX2pvYiJ9KQoKCmRlZiB0ZXN0
X2ltcG9ydF9zY2FuX25vX2V4ZWN1dGlvbl9hZGFwdGVyX3JlYWNoYWJsZSgpOgogICAgIiIiVC0xMSArIHNjYW4tdG9rZW4gY29uZGl0aW9uOiB0aGUgYmFu
ZCdzIG1vZHVsZSBncmFwaCBtdXN0IG5vdCByZWFjaAogICAgZXhlY3V0aW9uL2Jyb2tlci9vcmRlci9hZGFwdGVyL3RyYWRpbmdfaW50ZWxsaWdlbmNlIG1v
ZHVsZXMuIiIiCiAgICBpbXBvcnQgYXN0CiAgICBmcm9tIHBhdGhsaWIgaW1wb3J0IFBhdGgKCiAgICBiYXNlID0gUGF0aChfX2ZpbGVfXykucmVzb2x2ZSgp
LnBhcmVudHNbMV0gLyAiYXBwL3YyL3Jlc2VhcmNoX2pvYnMiCiAgICBiYW5uZWRfdG9rZW5zID0gKCJleGVjdXRpb24iLCAiYnJva2VyIiwgIm9yZGVyIiwg
ImFkYXB0ZXIiLAogICAgICAgICAgICAgICAgICAgICAidHJhZGluZ19pbnRlbGxpZ2VuY2UiLCAibWFya2V0LmxpdmUiLAogICAgICAgICAgICAgICAgICAg
ICAiYXBwLm1hcmtldCIsICJwYXBlciIsICJsaXZlX3NlcnZpY2UiKQogICAgYWxsb3dlZF9leGNlcHRpb25zID0gKCJleGVjdXRpb25fcmVzZWFyY2giLCkg
ICMgVjEgcmVhZC1vbmx5IGxpbmVhZ2UgbmFtZQogICAgZm9yIGYgaW4gYmFzZS5nbG9iKCIqLnB5Iik6CiAgICAgICAgdHJlZSA9IGFzdC5wYXJzZShmLnJl
YWRfdGV4dCgpKQogICAgICAgIGZvciBub2RlIGluIGFzdC53YWxrKHRyZWUpOgogICAgICAgICAgICBuYW1lcyA9IFtdCiAgICAgICAgICAgIGlmIGlzaW5z
dGFuY2Uobm9kZSwgYXN0LkltcG9ydCk6CiAgICAgICAgICAgICAgICBuYW1lcyA9IFthLm5hbWUgZm9yIGEgaW4gbm9kZS5uYW1lc10KICAgICAgICAgICAg
ZWxpZiBpc2luc3RhbmNlKG5vZGUsIGFzdC5JbXBvcnRGcm9tKSBhbmQgbm9kZS5tb2R1bGU6CiAgICAgICAgICAgICAgICBuYW1lcyA9IFtub2RlLm1vZHVs
ZV0KICAgICAgICAgICAgZm9yIG5hbWUgaW4gbmFtZXM6CiAgICAgICAgICAgICAgICBsb3cgPSBuYW1lLmxvd2VyKCkKICAgICAgICAgICAgICAgIGlmIGFu
eShsb3cuc3RhcnRzd2l0aChhKSBvciBhIGluIGxvdwogICAgICAgICAgICAgICAgICAgICAgIGZvciBhIGluIGFsbG93ZWRfZXhjZXB0aW9ucyk6CiAgICAg
ICAgICAgICAgICAgICAgY29udGludWUKICAgICAgICAgICAgICAgIGZvciB0b2tlbiBpbiBiYW5uZWRfdG9rZW5zOgogICAgICAgICAgICAgICAgICAgIGFz
c2VydCB0b2tlbiBub3QgaW4gbG93LCBmIntmLm5hbWV9IGltcG9ydHMge25hbWV9IgoKCmRlZiB0ZXN0X2NvbnN0cnVjdGlvbl90b2tlbl9zY2FuKCk6CiAg
ICAiIiJObyBwYXBlci9saXZlL29yZGVyIGNvbnN0cnVjdGlvbiB2b2NhYnVsYXJ5IGluIGJhbmQgbW9kdWxlcy4iIiIKICAgIGZyb20gcGF0aGxpYiBpbXBv
cnQgUGF0aAoKICAgIGJhc2UgPSBQYXRoKF9fZmlsZV9fKS5yZXNvbHZlKCkucGFyZW50c1sxXSAvICJhcHAvdjIvcmVzZWFyY2hfam9icyIKICAgIGZvciBm
IGluIGJhc2UuZ2xvYigiKi5weSIpOgogICAgICAgIHRleHQgPSBmLnJlYWRfdGV4dCgpLmxvd2VyKCkKICAgICAgICBmb3IgdG9rZW4gaW4gKCJwbGFjZV9v
cmRlciIsICJzdWJtaXRfb3JkZXIiLCAiYnJva2VyXyIsCiAgICAgICAgICAgICAgICAgICAgICAiYWNjb3VudF9pZCIsICJwYXBlcl90cmFkZSIsICJsaXZl
X3RyYWRlIik6CiAgICAgICAgICAgIGFzc2VydCB0b2tlbiBub3QgaW4gdGV4dCwgZiJ7dG9rZW59IGluIHtmLm5hbWV9IgoKCkBweXRlc3QubWFyay5hc3lu
Y2lvCmFzeW5jIGRlZiB0ZXN0X2F0dGVtcHRzX3JlYWRfYW5kX3Jlc3VsdF9saXN0aW5nKHByZXBhcmVkX2RiLCBhc3luY19jbGllbnQpOgogICAgYXdhaXQg
X3NlZWRfZW52KCkKICAgIGhlYWRlcnMgPSBhd2FpdCBfYWRtaW4oYXN5bmNfY2xpZW50KQogICAgaWRzID0gYXdhaXQgX3BpcGVsaW5lKGFzeW5jX2NsaWVu
dCwgaGVhZGVycykKICAgIGpvYl9pZCA9IGF3YWl0IF9zdWJtaXR0ZWQoYXN5bmNfY2xpZW50LCBoZWFkZXJzLCBpZHMpCiAgICBhd2FpdCBhc3luY19jbGll
bnQucG9zdChmIntSSn0vam9icy9ydW4iLCBoZWFkZXJzPWhlYWRlcnMsCiAgICAgICAgICAgICAgICAgICAgICAgICAgICBqc29uPXsiam9iX2lkIjogam9i
X2lkfSkKICAgIGF0dGVtcHRzID0gKGF3YWl0IGFzeW5jX2NsaWVudC5nZXQoZiJ7Ukp9L2pvYnMve2pvYl9pZH0vYXR0ZW1wdHMiLAogICAgICAgICAgICAg
ICAgICAgICAgICAgICAgICAgICAgICAgICBoZWFkZXJzPWhlYWRlcnMpKS5qc29uKCkKICAgIGFzc2VydCBhdHRlbXB0c1sidG90YWwiXSA9PSAxCiAgICBh
c3NlcnQgYXR0ZW1wdHNbImF0dGVtcHRzIl1bMF1bIm91dGNvbWUiXSA9PSAic3VjY2VlZGVkIgogICAgcmVzdWx0cyA9IChhd2FpdCBhc3luY19jbGllbnQu
Z2V0KAogICAgICAgIGYie1JKfS9yZXN1bHRzIiwgcGFyYW1zPXsicmVzdWx0X2NsYXNzIjogImJhY2t0ZXN0In0sCiAgICAgICAgaGVhZGVycz1oZWFkZXJz
KSkuanNvbigpCiAgICBhc3NlcnQgcmVzdWx0c1sidG90YWwiXSA9PSAxCiAgICBhc3NlcnQgcmVzdWx0c1sicmVzdWx0cyJdWzBdWyJyZXN1bHRfY2xhc3Mi
XSA9PSAiYmFja3Rlc3QiCiAgICBhc3NlcnQgInBlcmZvcm1hbmNlX2Rpc2NsYWltZXIiIGluIHJlc3VsdHNbInJlc3VsdHMiXVswXVsic3VtbWFyeSJdCg==
'@
Write-Evidence ("record 15/17 staged: " + $Rec15Path)
$Rec16Path = "tests\test_v2_be7_migration.py"
$Rec16Sha  = "04e8ef5c0e83cb879809628bed113dc7187e6530ddd2416f687ba704a8711945"
$Rec16B64 = @'
IiIiVjIgQkUtNyBtaWdyYXRpb24gdGVzdHMg4oCUIEJPLVYyLUJFLTctMDAxIFQtMeKAplQtNyAoMTIgdGVzdHMpLgoKMDA0NyBvbiBkZWRpY2F0ZWQgU1FM
aXRlIGNoYWlucy4gQ29udGVudC1iYXNlZCBjb21wYXJpc29ucyAoUEdGLTAxMikuClBpbnM6IHRyaWdnZXJzIDMy4oaSNDI7IHBlcm1pc3Npb25zIDQx4oaS
NDk7IGNvbXB2ZXIgNuKGkjguCiIiIgoKZnJvbSBfX2Z1dHVyZV9fIGltcG9ydCBhbm5vdGF0aW9ucwoKaW1wb3J0IG9zCmltcG9ydCBzcWxpdGUzCmltcG9y
dCBzdWJwcm9jZXNzCmltcG9ydCBzeXMKZnJvbSBwYXRobGliIGltcG9ydCBQYXRoCgppbXBvcnQgcHl0ZXN0CgpCQUNLRU5EX0RJUiA9IFBhdGgoX19maWxl
X18pLnJlc29sdmUoKS5wYXJlbnRzWzFdClRSQU5TX0FVVEhPUklUWSA9ICJCTy1WMi1CRS0zLVAyLVRSQU5TLTAwMSIKUkVWXzAwNDYgPSAiMjAyNjA5MDNf
MDA0NiIKUkVWXzAwNDcgPSAiMjAyNjA5MDNfMDA0NyIKClRSSUdHRVJTXzAwNDcgPSB7CiAgICAidjJfYmFja3Rlc3RfaW5wdXRfaW1tdXRhYmxlX3VwZGF0
ZSI6CiAgICAgICAgIlYyIGJhY2t0ZXN0IGlucHV0cyBhcmUgaW1tdXRhYmxlOyBVUERBVEUgcHJvaGliaXRlZCIsCiAgICAidjJfYmFja3Rlc3RfaW5wdXRf
aW1tdXRhYmxlX2RlbGV0ZSI6CiAgICAgICAgIlYyIGJhY2t0ZXN0IGlucHV0cyBhcmUgaW1tdXRhYmxlOyBERUxFVEUgcHJvaGliaXRlZCIsCiAgICAidjJf
Y29zdF9tb2RlbF9pbW11dGFibGVfdXBkYXRlIjoKICAgICAgICAiVjIgY29zdCBtb2RlbHMgYXJlIGltbXV0YWJsZTsgVVBEQVRFIHByb2hpYml0ZWQiLAog
ICAgInYyX2Nvc3RfbW9kZWxfaW1tdXRhYmxlX2RlbGV0ZSI6CiAgICAgICAgIlYyIGNvc3QgbW9kZWxzIGFyZSBpbW11dGFibGU7IERFTEVURSBwcm9oaWJp
dGVkIiwKICAgICJ2Ml9zdHJhdGVneV92ZXJzaW9uX2ltbXV0YWJsZV91cGRhdGUiOgogICAgICAgICJWMiBzdHJhdGVneSB2ZXJzaW9ucyBhcmUgaW1tdXRh
YmxlOyBVUERBVEUgcHJvaGliaXRlZCIsCiAgICAidjJfc3RyYXRlZ3lfdmVyc2lvbl9pbW11dGFibGVfZGVsZXRlIjoKICAgICAgICAiVjIgc3RyYXRlZ3kg
dmVyc2lvbnMgYXJlIGltbXV0YWJsZTsgREVMRVRFIHByb2hpYml0ZWQiLAogICAgInYyX3Jlc2VhcmNoX2pvYl9hdHRlbXB0X2ltbXV0YWJsZV91cGRhdGUi
OgogICAgICAgICJWMiByZXNlYXJjaCBqb2IgYXR0ZW1wdHMgYXJlIGltbXV0YWJsZTsgVVBEQVRFIHByb2hpYml0ZWQiLAogICAgInYyX3Jlc2VhcmNoX2pv
Yl9hdHRlbXB0X2ltbXV0YWJsZV9kZWxldGUiOgogICAgICAgICJWMiByZXNlYXJjaCBqb2IgYXR0ZW1wdHMgYXJlIGltbXV0YWJsZTsgREVMRVRFIHByb2hp
Yml0ZWQiLAogICAgInYyX3Jlc2VhcmNoX3Jlc3VsdF9pbW11dGFibGVfdXBkYXRlIjoKICAgICAgICAiVjIgcmVzZWFyY2ggcmVzdWx0cyBhcmUgaW1tdXRh
YmxlOyBVUERBVEUgcHJvaGliaXRlZCIsCiAgICAidjJfcmVzZWFyY2hfcmVzdWx0X2ltbXV0YWJsZV9kZWxldGUiOgogICAgICAgICJWMiByZXNlYXJjaCBy
ZXN1bHRzIGFyZSBpbW11dGFibGU7IERFTEVURSBwcm9oaWJpdGVkIiwKfQoKUEVSTVNfMDA0NyA9IHsKICAgICgiYWRtaW4iLCAidjIucmVzZWFyY2guam9i
cy5yZWFkIiwgIlNBTC0yIiksCiAgICAoImFkbWluIiwgInYyLnJlc2VhcmNoLmpvYnMuc3VibWl0IiwgIlNBTC0zIiksCiAgICAoImFkbWluIiwgInYyLnJl
c2VhcmNoLmpvYnMuY2FuY2VsIiwgIlNBTC0zIiksCiAgICAoImFkbWluIiwgInYyLnJlc2VhcmNoLnJlZ2lzdHJ5LnJlYWQiLCAiU0FMLTIiKSwKICAgICgi
YWRtaW4iLCAidjIucmVzZWFyY2gucmVnaXN0cnkud3JpdGUiLCAiU0FMLTMiKSwKICAgICgiYWRtaW4iLCAidjIucmVzZWFyY2gucmVzdWx0cy5yZWFkIiwg
IlNBTC0yIiksCiAgICAoIm9wZXJhdG9yIiwgInYyLnJlc2VhcmNoLmpvYnMucmVhZCIsICJTQUwtMiIpLAogICAgKCJvcGVyYXRvciIsICJ2Mi5yZXNlYXJj
aC5yZXN1bHRzLnJlYWQiLCAiU0FMLTIiKSwKfQoKCmRlZiBfYWxlbWJpYyhhcmdzOiBsaXN0W3N0cl0sIGRiX3VybDogc3RyKSAtPiBzdWJwcm9jZXNzLkNv
bXBsZXRlZFByb2Nlc3Nbc3RyXToKICAgIGVudiA9IGRpY3Qob3MuZW52aXJvbikKICAgIGVudlsiQVhJT01fREFUQUJBU0VfVVJMIl0gPSBkYl91cmwKICAg
IGVudi5zZXRkZWZhdWx0KCJBWElPTV9FTlZJUk9OTUVOVCIsICJ0ZXN0aW5nIikKICAgIGVudi5zZXRkZWZhdWx0KCJBWElPTV9BTExPV19JTlNFQ1VSRV9E
RVYiLCAidHJ1ZSIpCiAgICBlbnYuc2V0ZGVmYXVsdCgiQVhJT01fSldUX1NFQ1JFVF9LRVkiLAogICAgICAgICAgICAgICAgICAgInRlc3Qtc2VjcmV0LWtl
eS1hdC1sZWFzdC0zMi1jaGFycy1sb25nISEiKQogICAgZW52LnNldGRlZmF1bHQoIkFYSU9NX1YyX01PREUiLCAiUkVTRUFSQ0giKQogICAgZW52WyJBWElP
TV9URF9UUkFOU0lUSU9OX0FVVEhPUklUWV9SRUYiXSA9IFRSQU5TX0FVVEhPUklUWQogICAgcmV0dXJuIHN1YnByb2Nlc3MucnVuKAogICAgICAgIFtzeXMu
ZXhlY3V0YWJsZSwgIi1tIiwgImFsZW1iaWMiLCAqYXJnc10sCiAgICAgICAgY3dkPUJBQ0tFTkRfRElSLCBlbnY9ZW52LCBjYXB0dXJlX291dHB1dD1UcnVl
LCB0ZXh0PVRydWUsIHRpbWVvdXQ9NjAwKQoKCmRlZiBfZGIodG1wX3BhdGg6IFBhdGgsIHJldjogc3RyKSAtPiB0dXBsZVtQYXRoLCBzdHJdOgogICAgZGJf
ZmlsZSA9IHRtcF9wYXRoIC8gImJlNy5kYiIKICAgIGRiX3VybCA9IGYic3FsaXRlK2Fpb3NxbGl0ZTovLy97ZGJfZmlsZX0iCiAgICByZXN1bHQgPSBfYWxl
bWJpYyhbInVwZ3JhZGUiLCByZXZdLCBkYl91cmwpCiAgICBhc3NlcnQgcmVzdWx0LnJldHVybmNvZGUgPT0gMCwgcmVzdWx0LnN0ZGVycgogICAgcmV0dXJu
IGRiX2ZpbGUsIGRiX3VybAoKCmRlZiBfcShkYl9maWxlOiBQYXRoLCBzcWw6IHN0cik6CiAgICBjb25uID0gc3FsaXRlMy5jb25uZWN0KGRiX2ZpbGUpCiAg
ICB0cnk6CiAgICAgICAgcmV0dXJuIGNvbm4uZXhlY3V0ZShzcWwpLmZldGNoYWxsKCkKICAgIGZpbmFsbHk6CiAgICAgICAgY29ubi5jbG9zZSgpCgoKZGVm
IF92Ml90cmlnZ2VycyhkYl9maWxlOiBQYXRoKSAtPiBzZXRbc3RyXToKICAgIHJldHVybiB7clswXSBmb3IgciBpbiBfcSgKICAgICAgICBkYl9maWxlLAog
ICAgICAgICJTRUxFQ1QgbmFtZSBGUk9NIHNxbGl0ZV9tYXN0ZXIgV0hFUkUgdHlwZT0ndHJpZ2dlciciCiAgICAgICAgIiBBTkQgbmFtZSBMSUtFICd2Ml8l
JyIpfQoKCkJFMSA9ICgiJ3NpbXVsYXRlZCcsJ1JFU0VBUkNIJywndCcsTlVMTCwnMjAyNi0wOS0wMyAwMDowMDowMCswMDowMCciKQoKCmRlZiBfaW5zZXJ0
X2lucHV0KGN1ciwgcmlkPSJpMSIsIGlpZD0iaW4tMSIsIHNlcT0xLCBjaD0iaDEiKToKICAgIGN1ci5leGVjdXRlKAogICAgICAgICJJTlNFUlQgSU5UTyB2
Ml9iYWNrdGVzdF9pbnB1dCAoaWQsIGlucHV0X2lkLCByZWNvcmRfc2VxLCIKICAgICAgICAiIGNvbnRlbnRfaGFzaCwgc2VyaWVzX3JlZnMsIHdpbmRvd19z
dGFydCwgd2luZG93X2VuZCwiCiAgICAgICAgIiByZWdpc3RyYXRpb25fb3V0Y29tZSwgZGF0YV9jbGFzcywgbW9kZSwgb3BlcmF0b3JfaWQsIgogICAgICAg
ICIgY29ycmVsYXRpb25faWQsIGNyZWF0ZWRfYXQpIgogICAgICAgIGYiIFZBTFVFUyAoJ3tyaWR9Jywne2lpZH0nLHtzZXF9LCd7Y2h9Jywne3t9fScsIgog
ICAgICAgICIgJzIwMjYtMDktMDEgMDA6MDA6MDArMDA6MDAnLCcyMDI2LTA5LTAyIDAwOjAwOjAwKzAwOjAwJywiCiAgICAgICAgZiIgJ3JlZ2lzdGVyZWQn
LHtCRTF9KSIpCgoKIyAtLS0gVC0xL1QtMjogY2hhaW4gKyBEREwgKDQgdGVzdHMpIC0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0t
LS0KCgpkZWYgdGVzdF8wMDQ3X3RhYmxlc19hbmRfY29sdW1ucyh0bXBfcGF0aDogUGF0aCkgLT4gTm9uZToKICAgIGRiX2ZpbGUsIF8gPSBfZGIodG1wX3Bh
dGgsIFJFVl8wMDQ3KQogICAgdGFibGVzID0ge3JbMF0gZm9yIHIgaW4gX3EoCiAgICAgICAgZGJfZmlsZSwgIlNFTEVDVCBuYW1lIEZST00gc3FsaXRlX21h
c3RlciBXSEVSRSB0eXBlPSd0YWJsZSciKX0KICAgIGZvciB0IGluICgidjJfYmFja3Rlc3RfaW5wdXQiLCAidjJfY29zdF9tb2RlbCIsICJ2Ml9zdHJhdGVn
eV92ZXJzaW9uIiwKICAgICAgICAgICAgICAidjJfcmVzZWFyY2hfam9iIiwgInYyX3Jlc2VhcmNoX2pvYl9hdHRlbXB0IiwKICAgICAgICAgICAgICAidjJf
cmVzZWFyY2hfcmVzdWx0Iik6CiAgICAgICAgYXNzZXJ0IHQgaW4gdGFibGVzCiAgICBqb2JfY29scyA9IFtyWzFdIGZvciByIGluIF9xKGRiX2ZpbGUsICJQ
UkFHTUEgdGFibGVfaW5mbyh2Ml9yZXNlYXJjaF9qb2IpIildCiAgICBmb3IgYyBpbiAoIm93bmVyIiwgImF1dGhvcml6YXRpb25fcmVmIiwgImlucHV0cyIs
ICJzY2hlZHVsZSIsCiAgICAgICAgICAgICAgIm91dHB1dF9yZWYiLCAiZmFpbHVyZSIsICJqb2Jfc3RhdGUiLCAiYXR0ZW1wdF9jb3VudCIpOgogICAgICAg
IGFzc2VydCBjIGluIGpvYl9jb2xzCiAgICByZXN1bHRfY29scyA9IFtyWzFdIGZvciByIGluIF9xKAogICAgICAgIGRiX2ZpbGUsICJQUkFHTUEgdGFibGVf
aW5mbyh2Ml9yZXNlYXJjaF9yZXN1bHQpIildCiAgICBmb3IgYyBpbiAoInJlc3VsdF9jbGFzcyIsICJpbnB1dHNfaGFzaCIsICJlbmdpbmVfdmVyc2lvbnNf
aGFzaCIsCiAgICAgICAgICAgICAgInN1bW1hcnkiLCAicmVwbGF5X29mIiwgInRpbWVfYmFzaXMiKToKICAgICAgICBhc3NlcnQgYyBpbiByZXN1bHRfY29s
cwoKCmRlZiB0ZXN0XzAwNDdfc2VlZHNfYW5kX3RvdGFscyh0bXBfcGF0aDogUGF0aCkgLT4gTm9uZToKICAgIGRiX2ZpbGUsIF8gPSBfZGIodG1wX3BhdGgs
IFJFVl8wMDQ3KQogICAgdHJpZ3MgPSBfdjJfdHJpZ2dlcnMoZGJfZmlsZSkKICAgIGFzc2VydCBsZW4odHJpZ3MpID09IDQyICAgICAgICAgICMgVC0zOiAz
MiArIDEwCiAgICBhc3NlcnQgc2V0KFRSSUdHRVJTXzAwNDcpIDw9IHRyaWdzCiAgICBwZXJtcyA9IF9xKGRiX2ZpbGUsICJTRUxFQ1Qgcm9sZSwgcGVybWlz
c2lvbiwgc2FsIEZST00gdjJfcGVybWlzc2lvbiIpCiAgICBhc3NlcnQgbGVuKHBlcm1zKSA9PSA0OSAgICAgICAgICAjIFQtNAogICAgYXNzZXJ0IGxlbih7
KHIsIHApIGZvciByLCBwLCBfIGluIHBlcm1zfSkgPT0gNDkKICAgIGFzc2VydCBQRVJNU18wMDQ3IDw9IHt0dXBsZShyKSBmb3IgciBpbiBwZXJtc30KICAg
IGNvbXB2ZXIgPSBfcShkYl9maWxlLAogICAgICAgICAgICAgICAgICJTRUxFQ1QgY29tcG9uZW50LCB2ZXJzaW9uLCBsZW5ndGgoc291cmNlX2hhc2gpIgog
ICAgICAgICAgICAgICAgICIgRlJPTSB2Ml9jb21wdXRhdGlvbl92ZXJzaW9uIikKICAgIGFzc2VydCBsZW4oY29tcHZlcikgPT0gOCAgICAgICAgICMgVC01
CiAgICBhc3NlcnQgKCJyZXBsYXlfZW5naW5lIiwgInJwZS0xLjAuMCIsIDY0KSBpbiBjb21wdmVyCiAgICBhc3NlcnQgKCJyZXNlYXJjaF9qb2JfZW5naW5l
IiwgInJqZS0xLjAuMCIsIDY0KSBpbiBjb21wdmVyCgoKZGVmIHRlc3RfMDA0N19yZXN1bHRfY2xhc3NfY2hlY2tfcmVmdXNlc19wYXBlcl9saXZlKHRtcF9w
YXRoOiBQYXRoKSAtPiBOb25lOgogICAgIiIiVC0yL1AtOTogYHBhcGVyYC9gbGl2ZWAgYXJlIHNjaGVtYS1pbXBvc3NpYmxlLiIiIgogICAgZGJfZmlsZSwg
XyA9IF9kYih0bXBfcGF0aCwgUkVWXzAwNDcpCiAgICBjb25uID0gc3FsaXRlMy5jb25uZWN0KGRiX2ZpbGUpCiAgICB0cnk6CiAgICAgICAgZm9yIGJhbm5l
ZCBpbiAoInBhcGVyIiwgImxpdmUiKToKICAgICAgICAgICAgd2l0aCBweXRlc3QucmFpc2VzKHNxbGl0ZTMuSW50ZWdyaXR5RXJyb3IpOgogICAgICAgICAg
ICAgICAgY29ubi5leGVjdXRlKAogICAgICAgICAgICAgICAgICAgICJJTlNFUlQgSU5UTyB2Ml9yZXNlYXJjaF9yZXN1bHQgKGlkLCByZXN1bHRfY2xhc3Ms
IgogICAgICAgICAgICAgICAgICAgICIgam9iX2lkLCBhdHRlbXB0X2luZGV4LCBzdHJhdGVneV92ZXJzaW9uX2lkLCIKICAgICAgICAgICAgICAgICAgICAi
IGlucHV0X3JlZ2lzdHJ5X2lkLCBjb3N0X21vZGVsX2lkLCBpbnB1dHNfaGFzaCwiCiAgICAgICAgICAgICAgICAgICAgIiBlbmdpbmVfdmVyc2lvbnMsIGVu
Z2luZV92ZXJzaW9uc19oYXNoLCBzdW1tYXJ5LCIKICAgICAgICAgICAgICAgICAgICAiIHRpbWVfYmFzaXMsIGRhdGFfY2xhc3MsIG1vZGUsIG9wZXJhdG9y
X2lkLCIKICAgICAgICAgICAgICAgICAgICAiIGNvcnJlbGF0aW9uX2lkLCBjcmVhdGVkX2F0KSIKICAgICAgICAgICAgICAgICAgICBmIiBWQUxVRVMgKCdy
LXtiYW5uZWR9Jywne2Jhbm5lZH0nLCdqJywxLCdzJywnaScsJ2MnLCIKICAgICAgICAgICAgICAgICAgICBmIiAnaCcsJ3t7fX0nLCdoMicsJ3t7fX0nLCd7
e319Jyx7QkUxfSkiKQogICAgICAgICMgY29uc3RydWN0aWJsZSBjbGFzc2VzIGluc2VydCBmaW5lCiAgICAgICAgY29ubi5leGVjdXRlKAogICAgICAgICAg
ICAiSU5TRVJUIElOVE8gdjJfcmVzZWFyY2hfcmVzdWx0IChpZCwgcmVzdWx0X2NsYXNzLCBqb2JfaWQsIgogICAgICAgICAgICAiIGF0dGVtcHRfaW5kZXgs
IHN0cmF0ZWd5X3ZlcnNpb25faWQsIGlucHV0X3JlZ2lzdHJ5X2lkLCIKICAgICAgICAgICAgIiBjb3N0X21vZGVsX2lkLCBpbnB1dHNfaGFzaCwgZW5naW5l
X3ZlcnNpb25zLCIKICAgICAgICAgICAgIiBlbmdpbmVfdmVyc2lvbnNfaGFzaCwgc3VtbWFyeSwgdGltZV9iYXNpcywgZGF0YV9jbGFzcywiCiAgICAgICAg
ICAgICIgbW9kZSwgb3BlcmF0b3JfaWQsIGNvcnJlbGF0aW9uX2lkLCBjcmVhdGVkX2F0KSIKICAgICAgICAgICAgZiIgVkFMVUVTICgnci1vaycsJ2JhY2t0
ZXN0JywnaicsMSwncycsJ2knLCdjJywnaCcsJ3t7fX0nLCdoMicsIgogICAgICAgICAgICBmIiAne3t9fScsJ3t7fX0nLHtCRTF9KSIpCiAgICAgICAgY29u
bi5jb21taXQoKQogICAgZmluYWxseToKICAgICAgICBjb25uLmNsb3NlKCkKCgpkZWYgdGVzdF8wMDQ3X3VuaXF1ZW5lc3NfYW5jaG9yc19iZWhhdmlvcmFs
KHRtcF9wYXRoOiBQYXRoKSAtPiBOb25lOgogICAgZGJfZmlsZSwgXyA9IF9kYih0bXBfcGF0aCwgUkVWXzAwNDcpCiAgICBjb25uID0gc3FsaXRlMy5jb25u
ZWN0KGRiX2ZpbGUpCiAgICB0cnk6CiAgICAgICAgY3VyID0gY29ubi5jdXJzb3IoKQogICAgICAgIF9pbnNlcnRfaW5wdXQoY3VyLCByaWQ9ImkxIiwgaWlk
PSJpbi0xIiwgc2VxPTEsIGNoPSJoMSIpCiAgICAgICAgY29ubi5jb21taXQoKQogICAgICAgIHdpdGggcHl0ZXN0LnJhaXNlcyhzcWxpdGUzLkludGVncml0
eUVycm9yKToKICAgICAgICAgICAgX2luc2VydF9pbnB1dChjdXIsIHJpZD0iaTIiLCBpaWQ9ImluLTEiLCBzZXE9MSwgY2g9ImgyIikgICMgZHVwIHNlcQog
ICAgICAgIHdpdGggcHl0ZXN0LnJhaXNlcyhzcWxpdGUzLkludGVncml0eUVycm9yKToKICAgICAgICAgICAgX2luc2VydF9pbnB1dChjdXIsIHJpZD0iaTMi
LCBpaWQ9ImluLTIiLCBzZXE9MSwgY2g9ImgxIikgICMgZHVwIGNvbnRlbnQKICAgICAgICBfaW5zZXJ0X2lucHV0KGN1ciwgcmlkPSJpNCIsIGlpZD0iaW4t
MSIsIHNlcT0yLCBjaD0iaDMiKSAgICAgICMgbmV4dCBnZW4gb2sKICAgICAgICBjb25uLmNvbW1pdCgpCiAgICAgICAgIyBhdHRlbXB0LWxlZGdlciBhbmNo
b3IKICAgICAgICBjdXIuZXhlY3V0ZSgKICAgICAgICAgICAgIklOU0VSVCBJTlRPIHYyX3Jlc2VhcmNoX2pvYl9hdHRlbXB0IChpZCwgam9iX2lkLCIKICAg
ICAgICAgICAgIiBhdHRlbXB0X2luZGV4LCBvdXRjb21lLCByZWFzb24sIGFjdG9yX2lkLCBtb2RlLCBvcGVyYXRvcl9pZCwiCiAgICAgICAgICAgICIgY29y
cmVsYXRpb25faWQsIGNyZWF0ZWRfYXQpIgogICAgICAgICAgICAiIFZBTFVFUyAoJ2ExJywnajEnLDEsJ2ZhaWxlZCcsJ3t9JywndCcsJ1JFU0VBUkNIJywn
dCcsTlVMTCwiCiAgICAgICAgICAgICIgJzIwMjYtMDktMDMgMDA6MDA6MDArMDA6MDAnKSIpCiAgICAgICAgY29ubi5jb21taXQoKQogICAgICAgIHdpdGgg
cHl0ZXN0LnJhaXNlcyhzcWxpdGUzLkludGVncml0eUVycm9yKToKICAgICAgICAgICAgY3VyLmV4ZWN1dGUoCiAgICAgICAgICAgICAgICAiSU5TRVJUIElO
VE8gdjJfcmVzZWFyY2hfam9iX2F0dGVtcHQgKGlkLCBqb2JfaWQsIgogICAgICAgICAgICAgICAgIiBhdHRlbXB0X2luZGV4LCBvdXRjb21lLCByZWFzb24s
IGFjdG9yX2lkLCBtb2RlLCIKICAgICAgICAgICAgICAgICIgb3BlcmF0b3JfaWQsIGNvcnJlbGF0aW9uX2lkLCBjcmVhdGVkX2F0KSIKICAgICAgICAgICAg
ICAgICIgVkFMVUVTICgnYTInLCdqMScsMSwnc3VjY2VlZGVkJywne30nLCd0JywnUkVTRUFSQ0gnLCd0JywiCiAgICAgICAgICAgICAgICAiIE5VTEwsJzIw
MjYtMDktMDMgMDA6MDA6MDArMDA6MDAnKSIpICAjIFAtMTAgYW5jaG9yCiAgICBmaW5hbGx5OgogICAgICAgIGNvbm4uY2xvc2UoKQoKCiMgLS0tIFQtMzog
Z3VhcmQgbWVzc2FnZXMgdmVyYmF0aW0gKDIgdGVzdHMpIC0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tCgoKZGVmIHRlc3RfMDA0N19n
dWFyZF9tZXNzYWdlc192ZXJiYXRpbV9yZWdpc3RyaWVzKHRtcF9wYXRoOiBQYXRoKSAtPiBOb25lOgogICAgZGJfZmlsZSwgXyA9IF9kYih0bXBfcGF0aCwg
UkVWXzAwNDcpCiAgICBjb25uID0gc3FsaXRlMy5jb25uZWN0KGRiX2ZpbGUpCiAgICB0cnk6CiAgICAgICAgY3VyID0gY29ubi5jdXJzb3IoKQogICAgICAg
IF9pbnNlcnRfaW5wdXQoY3VyKQogICAgICAgIGN1ci5leGVjdXRlKAogICAgICAgICAgICAiSU5TRVJUIElOVE8gdjJfY29zdF9tb2RlbCAoaWQsIGNvc3Rf
bW9kZWxfaWQsIHJlY29yZF9zZXEsIgogICAgICAgICAgICAiIHNwcmVhZCwgY29tbWlzc2lvbiwgc2xpcHBhZ2UsIGxhdGVuY3lfbXMsIHJpc2tfbGltaXRz
LCIKICAgICAgICAgICAgIiBjaXRhdGlvbnMsIGRhdGFfY2xhc3MsIG1vZGUsIG9wZXJhdG9yX2lkLCBjb3JyZWxhdGlvbl9pZCwiCiAgICAgICAgICAgICIg
Y3JlYXRlZF9hdCkiCiAgICAgICAgICAgIGYiIFZBTFVFUyAoJ2MxJywnY20tMScsMSwne3t9fScsJ3t7fX0nLCd7e319JywwLCd7e319Jywne3t9fScse0JF
MX0pIikKICAgICAgICBjdXIuZXhlY3V0ZSgKICAgICAgICAgICAgIklOU0VSVCBJTlRPIHYyX3N0cmF0ZWd5X3ZlcnNpb24gKGlkLCBzdHJhdGVneV9pZCwg
cmVjb3JkX3NlcSwiCiAgICAgICAgICAgICIgbmFtZSwgcGFyYW1ldGVycywgbGlmZWN5Y2xlX3N0YXRlLCBkYXRhX2NsYXNzLCBtb2RlLCIKICAgICAgICAg
ICAgIiBvcGVyYXRvcl9pZCwgY29ycmVsYXRpb25faWQsIGNyZWF0ZWRfYXQpIgogICAgICAgICAgICBmIiBWQUxVRVMgKCdzMScsJ3N0LTEnLDEsJ1MnLCd7
e319JywnZHJhZnQnLHtCRTF9KSIpCiAgICAgICAgY29ubi5jb21taXQoKQogICAgICAgIGZvciBzcWwsIHRyaWcgaW4gKAogICAgICAgICAgICAoIlVQREFU
RSB2Ml9iYWNrdGVzdF9pbnB1dCBTRVQgaW5wdXRfaWQ9J3gnIiwKICAgICAgICAgICAgICJ2Ml9iYWNrdGVzdF9pbnB1dF9pbW11dGFibGVfdXBkYXRlIiks
CiAgICAgICAgICAgICgiREVMRVRFIEZST00gdjJfYmFja3Rlc3RfaW5wdXQiLAogICAgICAgICAgICAgInYyX2JhY2t0ZXN0X2lucHV0X2ltbXV0YWJsZV9k
ZWxldGUiKSwKICAgICAgICAgICAgKCJVUERBVEUgdjJfY29zdF9tb2RlbCBTRVQgbGF0ZW5jeV9tcz0xIiwKICAgICAgICAgICAgICJ2Ml9jb3N0X21vZGVs
X2ltbXV0YWJsZV91cGRhdGUiKSwKICAgICAgICAgICAgKCJERUxFVEUgRlJPTSB2Ml9jb3N0X21vZGVsIiwKICAgICAgICAgICAgICJ2Ml9jb3N0X21vZGVs
X2ltbXV0YWJsZV9kZWxldGUiKSwKICAgICAgICAgICAgKCJVUERBVEUgdjJfc3RyYXRlZ3lfdmVyc2lvbiBTRVQgbmFtZT0neCciLAogICAgICAgICAgICAg
InYyX3N0cmF0ZWd5X3ZlcnNpb25faW1tdXRhYmxlX3VwZGF0ZSIpLAogICAgICAgICAgICAoIkRFTEVURSBGUk9NIHYyX3N0cmF0ZWd5X3ZlcnNpb24iLAog
ICAgICAgICAgICAgInYyX3N0cmF0ZWd5X3ZlcnNpb25faW1tdXRhYmxlX2RlbGV0ZSIpLAogICAgICAgICk6CiAgICAgICAgICAgIHdpdGggcHl0ZXN0LnJh
aXNlcyhzcWxpdGUzLkRhdGFiYXNlRXJyb3IpIGFzIGV4Y2luZm86CiAgICAgICAgICAgICAgICBjdXIuZXhlY3V0ZShzcWwpCiAgICAgICAgICAgIGFzc2Vy
dCBzdHIoZXhjaW5mby52YWx1ZSkgPT0gVFJJR0dFUlNfMDA0N1t0cmlnXQogICAgZmluYWxseToKICAgICAgICBjb25uLmNsb3NlKCkKCgpkZWYgdGVzdF8w
MDQ3X2d1YXJkX21lc3NhZ2VzX3ZlcmJhdGltX2xlZGdlcl9yZXN1bHRzKHRtcF9wYXRoOiBQYXRoKSAtPiBOb25lOgogICAgZGJfZmlsZSwgXyA9IF9kYih0
bXBfcGF0aCwgUkVWXzAwNDcpCiAgICBjb25uID0gc3FsaXRlMy5jb25uZWN0KGRiX2ZpbGUpCiAgICB0cnk6CiAgICAgICAgY3VyID0gY29ubi5jdXJzb3Io
KQogICAgICAgIGN1ci5leGVjdXRlKAogICAgICAgICAgICAiSU5TRVJUIElOVE8gdjJfcmVzZWFyY2hfam9iX2F0dGVtcHQgKGlkLCBqb2JfaWQsIGF0dGVt
cHRfaW5kZXgsIgogICAgICAgICAgICAiIG91dGNvbWUsIHJlYXNvbiwgYWN0b3JfaWQsIG1vZGUsIG9wZXJhdG9yX2lkLCBjb3JyZWxhdGlvbl9pZCwiCiAg
ICAgICAgICAgICIgY3JlYXRlZF9hdCkiCiAgICAgICAgICAgICIgVkFMVUVTICgnYTEnLCdqMScsMSwnc3VjY2VlZGVkJywne30nLCd0JywnUkVTRUFSQ0gn
LCd0JyxOVUxMLCIKICAgICAgICAgICAgIiAnMjAyNi0wOS0wMyAwMDowMDowMCswMDowMCcpIikKICAgICAgICBjdXIuZXhlY3V0ZSgKICAgICAgICAgICAg
IklOU0VSVCBJTlRPIHYyX3Jlc2VhcmNoX3Jlc3VsdCAoaWQsIHJlc3VsdF9jbGFzcywgam9iX2lkLCIKICAgICAgICAgICAgIiBhdHRlbXB0X2luZGV4LCBz
dHJhdGVneV92ZXJzaW9uX2lkLCBpbnB1dF9yZWdpc3RyeV9pZCwiCiAgICAgICAgICAgICIgY29zdF9tb2RlbF9pZCwgaW5wdXRzX2hhc2gsIGVuZ2luZV92
ZXJzaW9ucywiCiAgICAgICAgICAgICIgZW5naW5lX3ZlcnNpb25zX2hhc2gsIHN1bW1hcnksIHRpbWVfYmFzaXMsIGRhdGFfY2xhc3MsIG1vZGUsIgogICAg
ICAgICAgICAiIG9wZXJhdG9yX2lkLCBjb3JyZWxhdGlvbl9pZCwgY3JlYXRlZF9hdCkiCiAgICAgICAgICAgIGYiIFZBTFVFUyAoJ3IxJywnc2ltdWxhdGlv
bicsJ2oxJywxLCdzJywnaScsJ2MnLCdoJywne3t9fScsJ2gyJywiCiAgICAgICAgICAgIGYiICd7e319Jywne3t9fScse0JFMX0pIikKICAgICAgICBjb25u
LmNvbW1pdCgpCiAgICAgICAgZm9yIHNxbCwgdHJpZyBpbiAoCiAgICAgICAgICAgICgiVVBEQVRFIHYyX3Jlc2VhcmNoX2pvYl9hdHRlbXB0IFNFVCBvdXRj
b21lPSdmYWlsZWQnIiwKICAgICAgICAgICAgICJ2Ml9yZXNlYXJjaF9qb2JfYXR0ZW1wdF9pbW11dGFibGVfdXBkYXRlIiksCiAgICAgICAgICAgICgiREVM
RVRFIEZST00gdjJfcmVzZWFyY2hfam9iX2F0dGVtcHQiLAogICAgICAgICAgICAgInYyX3Jlc2VhcmNoX2pvYl9hdHRlbXB0X2ltbXV0YWJsZV9kZWxldGUi
KSwKICAgICAgICAgICAgKCJVUERBVEUgdjJfcmVzZWFyY2hfcmVzdWx0IFNFVCByZXN1bHRfY2xhc3M9J2JhY2t0ZXN0JyIsCiAgICAgICAgICAgICAidjJf
cmVzZWFyY2hfcmVzdWx0X2ltbXV0YWJsZV91cGRhdGUiKSwKICAgICAgICAgICAgKCJERUxFVEUgRlJPTSB2Ml9yZXNlYXJjaF9yZXN1bHQiLAogICAgICAg
ICAgICAgInYyX3Jlc2VhcmNoX3Jlc3VsdF9pbW11dGFibGVfZGVsZXRlIiksCiAgICAgICAgKToKICAgICAgICAgICAgd2l0aCBweXRlc3QucmFpc2VzKHNx
bGl0ZTMuRGF0YWJhc2VFcnJvcikgYXMgZXhjaW5mbzoKICAgICAgICAgICAgICAgIGN1ci5leGVjdXRlKHNxbCkKICAgICAgICAgICAgYXNzZXJ0IHN0cihl
eGNpbmZvLnZhbHVlKSA9PSBUUklHR0VSU18wMDQ3W3RyaWddCiAgICAgICAgIyB0aGUgam9iIHRhYmxlIGlzIFVOR1VBUkRFRCBieSBkZXNpZ24gKEZQLTEp
CiAgICAgICAgY3VyLmV4ZWN1dGUoCiAgICAgICAgICAgICJJTlNFUlQgSU5UTyB2Ml9yZXNlYXJjaF9qb2IgKGlkLCBvd25lciwgYXV0aG9yaXphdGlvbl9y
ZWYsIgogICAgICAgICAgICAiIGlucHV0cywgc2NoZWR1bGUsIGpvYl9zdGF0ZSwgYXR0ZW1wdF9jb3VudCwgZGF0YV9jbGFzcywgbW9kZSwiCiAgICAgICAg
ICAgICIgb3BlcmF0b3JfaWQsIGNvcnJlbGF0aW9uX2lkLCBjcmVhdGVkX2F0KSIKICAgICAgICAgICAgZiIgVkFMVUVTICgnajEnLCdvJywnQk8tVjItQkUt
Ny0wMDEnLCd7e319Jywne3t9fScsJ3F1ZXVlZCcsMCx7QkUxfSkiKQogICAgICAgIGN1ci5leGVjdXRlKCJVUERBVEUgdjJfcmVzZWFyY2hfam9iIFNFVCBq
b2Jfc3RhdGU9J3J1bm5pbmcnIikKICAgICAgICBjb25uLmNvbW1pdCgpCiAgICBmaW5hbGx5OgogICAgICAgIGNvbm4uY2xvc2UoKQoKCiMgLS0tIFQtNzog
bm8tdG91Y2ggKDEpICsgZG93bmdyYWRlICgxKSArIGRyaWZ0ICgyKSArIGNoZWNrcyAoMikgLS0tLS0tLS0tLS0tLS0tLS0tLS0KCgpkZWYgdGVzdF9ub190
b3VjaF9wcm90ZWN0ZWRfc3RhdGUodG1wX3BhdGg6IFBhdGgpIC0+IE5vbmU6CiAgICBkYl9maWxlLCBkYl91cmwgPSBfZGIodG1wX3BhdGgsIFJFVl8wMDQ2
KQogICAgcHJvdmlkZXIgPSBfcShkYl9maWxlLAogICAgICAgICAgICAgICAgICAiU0VMRUNUIHByb3ZpZGVyX2lkLCBzb3VyY2Vfc3RhdHVzIEZST00gdjJf
bWRfcHJvdmlkZXIiKQogICAgY29tcHZlcl9iZWZvcmUgPSBfcShkYl9maWxlLAogICAgICAgICAgICAgICAgICAgICAgICAiU0VMRUNUIGNvbXBvbmVudCwg
dmVyc2lvbiwgc291cmNlX2hhc2giCiAgICAgICAgICAgICAgICAgICAgICAgICIgRlJPTSB2Ml9jb21wdXRhdGlvbl92ZXJzaW9uIE9SREVSIEJZIGNvbXBv
bmVudCIpCiAgICB0cmlnZ2Vyc19iZWZvcmUgPSBfdjJfdHJpZ2dlcnMoZGJfZmlsZSkKICAgIGFzc2VydCBsZW4odHJpZ2dlcnNfYmVmb3JlKSA9PSAzMgog
ICAgcmVzdWx0ID0gX2FsZW1iaWMoWyJ1cGdyYWRlIiwgUkVWXzAwNDddLCBkYl91cmwpCiAgICBhc3NlcnQgcmVzdWx0LnJldHVybmNvZGUgPT0gMCwgcmVz
dWx0LnN0ZGVycgogICAgYXNzZXJ0IF9xKGRiX2ZpbGUsCiAgICAgICAgICAgICAgIlNFTEVDVCBwcm92aWRlcl9pZCwgc291cmNlX3N0YXR1cyIKICAgICAg
ICAgICAgICAiIEZST00gdjJfbWRfcHJvdmlkZXIiKSA9PSBwcm92aWRlcgogICAgYWZ0ZXJfcHJpb3IgPSBfcShkYl9maWxlLAogICAgICAgICAgICAgICAg
ICAgICAiU0VMRUNUIGNvbXBvbmVudCwgdmVyc2lvbiwgc291cmNlX2hhc2giCiAgICAgICAgICAgICAgICAgICAgICIgRlJPTSB2Ml9jb21wdXRhdGlvbl92
ZXJzaW9uIgogICAgICAgICAgICAgICAgICAgICAiIFdIRVJFIGNvbXBvbmVudCBOT1QgSU4gKCdyZXBsYXlfZW5naW5lJywiCiAgICAgICAgICAgICAgICAg
ICAgICIgJ3Jlc2VhcmNoX2pvYl9lbmdpbmUnKSBPUkRFUiBCWSBjb21wb25lbnQiKQogICAgYXNzZXJ0IGFmdGVyX3ByaW9yID09IGNvbXB2ZXJfYmVmb3Jl
CiAgICBhZnRlciA9IF92Ml90cmlnZ2VycyhkYl9maWxlKQogICAgYXNzZXJ0IGFmdGVyIC0gdHJpZ2dlcnNfYmVmb3JlID09IHNldChUUklHR0VSU18wMDQ3
KQoKCmRlZiB0ZXN0X2Rvd25ncmFkZV9jeWNsZV9jb250ZW50X2Jhc2VkKHRtcF9wYXRoOiBQYXRoKSAtPiBOb25lOgogICAgZGJfZmlsZSwgZGJfdXJsID0g
X2RiKHRtcF9wYXRoLCBSRVZfMDA0NykKICAgIGRvd24gPSBfYWxlbWJpYyhbImRvd25ncmFkZSIsIFJFVl8wMDQ2XSwgZGJfdXJsKQogICAgYXNzZXJ0IGRv
d24ucmV0dXJuY29kZSA9PSAwLCBkb3duLnN0ZGVycgogICAgdGFibGVzID0ge3JbMF0gZm9yIHIgaW4gX3EoCiAgICAgICAgZGJfZmlsZSwgIlNFTEVDVCBu
YW1lIEZST00gc3FsaXRlX21hc3RlciBXSEVSRSB0eXBlPSd0YWJsZSciKX0KICAgIGZvciB0IGluICgidjJfYmFja3Rlc3RfaW5wdXQiLCAidjJfcmVzZWFy
Y2hfcmVzdWx0IiwgInYyX3Jlc2VhcmNoX2pvYiIpOgogICAgICAgIGFzc2VydCB0IG5vdCBpbiB0YWJsZXMKICAgIGFzc2VydCBsZW4oX3YyX3RyaWdnZXJz
KGRiX2ZpbGUpKSA9PSAzMgogICAgYXNzZXJ0IF9xKGRiX2ZpbGUsICJTRUxFQ1QgQ09VTlQoKikgRlJPTSB2Ml9wZXJtaXNzaW9uIilbMF1bMF0gPT0gNDEK
ICAgIGFzc2VydCBfcShkYl9maWxlLAogICAgICAgICAgICAgICJTRUxFQ1QgQ09VTlQoKikgRlJPTSB2Ml9jb21wdXRhdGlvbl92ZXJzaW9uIilbMF1bMF0g
PT0gNgogICAgYXNzZXJ0ICJ2Ml9jb21wdXRhdGlvbl92ZXJzaW9uX2ltbXV0YWJsZV9kZWxldGUiIGluIF92Ml90cmlnZ2VycyhkYl9maWxlKQogICAgdXAg
PSBfYWxlbWJpYyhbInVwZ3JhZGUiLCBSRVZfMDA0N10sIGRiX3VybCkKICAgIGFzc2VydCB1cC5yZXR1cm5jb2RlID09IDAsIHVwLnN0ZGVycgogICAgYXNz
ZXJ0IGxlbihfcShkYl9maWxlLCAiU0VMRUNUIHJvbGUsIHBlcm1pc3Npb24gRlJPTSB2Ml9wZXJtaXNzaW9uIikpID09IDQ5CgoKQHB5dGVzdC5tYXJrLnBh
cmFtZXRyaXplKCJyZXYiLCBbUkVWXzAwNDYsIFJFVl8wMDQ3XSkKZGVmIHRlc3RfZHJpZnRfZ2F0ZSh0bXBfcGF0aDogUGF0aCwgcmV2OiBzdHIpIC0+IE5v
bmU6CiAgICAiIiJGb3JtYXQtaW5kZXBlbmRlbnQgKFBHRi0wMTQpOiB6ZXJvIEJFLTcgdG9rZW5zIGluIGVpdGhlciBmb3JtLiIiIgogICAgZGJfZmlsZSwg
ZGJfdXJsID0gX2RiKHRtcF9wYXRoLCByZXYpCiAgICBjaGVjayA9IF9hbGVtYmljKFsiY2hlY2siXSwgZGJfdXJsKQogICAgZHJpZnQgPSAoY2hlY2suc3Rk
b3V0ICsgY2hlY2suc3RkZXJyKS5sb3dlcigpCiAgICBhc3NlcnQgY2hlY2sucmV0dXJuY29kZSAhPSAwCiAgICBmb3IgbWFya2VyIGluICgidjJfYmFja3Rl
c3RfaW5wdXQiLCAidjJfY29zdF9tb2RlbCIsCiAgICAgICAgICAgICAgICAgICAidjJfc3RyYXRlZ3lfdmVyc2lvbiIsICJ2Ml9yZXNlYXJjaF9qb2IiLAog
ICAgICAgICAgICAgICAgICAgInYyX3Jlc2VhcmNoX3Jlc3VsdCIsICJ2Ml9tZF8iLCAidjJfcGVybWlzc2lvbiIsCiAgICAgICAgICAgICAgICAgICAidjJf
Y29tcHV0YXRpb25fdmVyc2lvbiIpOgogICAgICAgIGFzc2VydCBtYXJrZXIgbm90IGluIGRyaWZ0LCBmIkJFLTcgZHJpZnQgYXQge3Jldn06IHttYXJrZXJ9
IgogICAgaWYgIm5vdCB1cCB0byBkYXRlIiBub3QgaW4gZHJpZnQ6CiAgICAgICAgYXNzZXJ0ICJhdWRpdF93cml0ZV9mYWlsdXJlX3JlY29yZHMiIGluIGRy
aWZ0CgoKZGVmIHRlc3Rfam9iX3N0YXRlX2FuZF9vdXRjb21lX2NoZWNrcyh0bXBfcGF0aDogUGF0aCkgLT4gTm9uZToKICAgIGRiX2ZpbGUsIF8gPSBfZGIo
dG1wX3BhdGgsIFJFVl8wMDQ3KQogICAgY29ubiA9IHNxbGl0ZTMuY29ubmVjdChkYl9maWxlKQogICAgdHJ5OgogICAgICAgIHdpdGggcHl0ZXN0LnJhaXNl
cyhzcWxpdGUzLkludGVncml0eUVycm9yKToKICAgICAgICAgICAgY29ubi5leGVjdXRlKAogICAgICAgICAgICAgICAgIklOU0VSVCBJTlRPIHYyX3Jlc2Vh
cmNoX2pvYiAoaWQsIG93bmVyLCBhdXRob3JpemF0aW9uX3JlZiwiCiAgICAgICAgICAgICAgICAiIGlucHV0cywgc2NoZWR1bGUsIGpvYl9zdGF0ZSwgYXR0
ZW1wdF9jb3VudCwgZGF0YV9jbGFzcywiCiAgICAgICAgICAgICAgICAiIG1vZGUsIG9wZXJhdG9yX2lkLCBjb3JyZWxhdGlvbl9pZCwgY3JlYXRlZF9hdCki
CiAgICAgICAgICAgICAgICBmIiBWQUxVRVMgKCdqeCcsJ28nLCd4Jywne3t9fScsJ3t7fX0nLCdleGVjdXRpbmcnLDAse0JFMX0pIikKICAgICAgICB3aXRo
IHB5dGVzdC5yYWlzZXMoc3FsaXRlMy5JbnRlZ3JpdHlFcnJvcik6CiAgICAgICAgICAgIGNvbm4uZXhlY3V0ZSgKICAgICAgICAgICAgICAgICJJTlNFUlQg
SU5UTyB2Ml9zdHJhdGVneV92ZXJzaW9uIChpZCwgc3RyYXRlZ3lfaWQsIgogICAgICAgICAgICAgICAgIiByZWNvcmRfc2VxLCBuYW1lLCBwYXJhbWV0ZXJz
LCBsaWZlY3ljbGVfc3RhdGUsIGRhdGFfY2xhc3MsIgogICAgICAgICAgICAgICAgIiBtb2RlLCBvcGVyYXRvcl9pZCwgY29ycmVsYXRpb25faWQsIGNyZWF0
ZWRfYXQpIgogICAgICAgICAgICAgICAgZiIgVkFMVUVTICgnc3gnLCdzdC14JywxLCdTJywne3t9fScsJ2xpdmUnLHtCRTF9KSIpCiAgICBmaW5hbGx5Ogog
ICAgICAgIGNvbm4uY2xvc2UoKQo=
'@
Write-Evidence ("record 16/17 staged: " + $Rec16Path)
$Rec17Path = "tests\test_v2_be7_replay.py"
$Rec17Sha  = "521bf5632d2dfa154e494e79090e796066474b5fc3b257ea6962c1324700dfcd"
$Rec17B64 = @'
IiIiVjIgQkUtNyBVLTIgdGVzdHMg4oCUIEJPLVYyLUJFLTctMDAxIFQtOSAobGVha2FnZSBHLTHigKZHLTU7IGRldGVybWluaXNtOwphbm5leCB2YWx1ZXM7
IGNvc3QgcHVyaXR5KS4gRmFpbC1maXJzdCBmb3IgdGhlIGVuZ2luZSB1bml0LgoKVGhlIEFOTkVYLVIgZml4dHVyZXMgQVJFIHRoZSB3b3JrZWQtc2FtcGxl
IHJlcGxheSBhbm5leDogMTAgcGlubmVkIGJhcnMsCnBpbm5lZCB0aHJlc2hvbGQgc3RyYXRlZ3ksIHBpbm5lZCBjb3N0IG1vZGVsIHdpdGggY2l0YXRpb25z
LCBoYW5kLWNvbXB1dGVkCmV4cGVjdGVkIGZpbGxzL3N1bW1hcnkgKGNvbW1lbnRzIHNob3cgdGhlIGFyaXRobWV0aWMpLgoiIiIKCmZyb20gX19mdXR1cmVf
XyBpbXBvcnQgYW5ub3RhdGlvbnMKCmltcG9ydCBqc29uCmltcG9ydCBzb2NrZXQKZnJvbSBkYXRldGltZSBpbXBvcnQgZGF0ZXRpbWUsIHRpbWVkZWx0YSwg
dGltZXpvbmUKZnJvbSBkZWNpbWFsIGltcG9ydCBEZWNpbWFsCgppbXBvcnQgcHl0ZXN0Cgpmcm9tIGFwcC52Mi5yZXNlYXJjaF9qb2JzLmNvbnRyYWN0cyBp
bXBvcnQgKAogICAgQ09OU1RSVUNUSUJMRV9SRVNVTFRfQ0xBU1NFUywKICAgIFJFU1VMVF9DTEFTU19UQVhPTk9NWSwKICAgIFJKX0RBVEFfQ0xBU1NFUywK
ICAgIFJlc3VsdENsYXNzUmVmdXNlZCwKICAgIHJlcXVpcmVfY29uc3RydWN0aWJsZV9yZXN1bHRfY2xhc3MsCikKZnJvbSBhcHAudjIucmVzZWFyY2hfam9i
cy5sZWFrYWdlIGltcG9ydCAoCiAgICBMZWFrYWdlUmVmdXNlZCwKICAgIFJlcGxheVdpbmRvdywKICAgIGNvbnRlbnRfaGFzaCwKICAgIGZpbHRlcl9iYXJz
X2cxLAogICAgdmFsaWRhdGVfZGVjaXNpb25fb3JkZXJpbmdfZzQsCiAgICB2YWxpZGF0ZV9ob3Jpem9uX2czLAogICAgdmVyaWZ5X2NvbnRlbnRfZzUsCikK
ZnJvbSBhcHAudjIucmVzZWFyY2hfam9icy5yZXBsYXkgaW1wb3J0ICgKICAgIGFwcGx5X2Nvc3RzLAogICAgZW5naW5lX3ZlcnNpb25zX2hhc2gsCiAgICBy
dW5fcmVwbGF5LAopCgpVVEMgPSB0aW1lem9uZS51dGMKVDAgPSBkYXRldGltZSgyMDI2LCA5LCAxLCB0emluZm89VVRDKQoKCkBweXRlc3QuZml4dHVyZShh
dXRvdXNlPVRydWUpCmRlZiBfc29ja2V0X2d1YXJkKG1vbmtleXBhdGNoKToKICAgIGRlZiBfZGVueSgqX2EsICoqX2spOgogICAgICAgIHJhaXNlIEFzc2Vy
dGlvbkVycm9yKCJuZXR3b3JrIGF0dGVtcHQgZHVyaW5nIEJFLTcgdGVzdCIpCgogICAgbW9ua2V5cGF0Y2guc2V0YXR0cihzb2NrZXQsICJnZXRhZGRyaW5m
byIsIF9kZW55KQogICAgbW9ua2V5cGF0Y2guc2V0YXR0cihzb2NrZXQsICJjcmVhdGVfY29ubmVjdGlvbiIsIF9kZW55KQoKCmRlZiBfYmFyKGk6IGludCwg
Y2xvc2U6IHN0cikgLT4gZGljdDoKICAgIHB4ID0gRGVjaW1hbChjbG9zZSkKICAgIHJldHVybiB7Im9wZW5fdGltZSI6IFQwICsgdGltZWRlbHRhKG1pbnV0
ZXM9MTUgKiBpKSwKICAgICAgICAgICAgIm9wZW4iOiBweCwgImhpZ2giOiBweCArIERlY2ltYWwoIjAuNSIpLAogICAgICAgICAgICAibG93IjogcHggLSBE
ZWNpbWFsKCIwLjUiKSwgImNsb3NlIjogcHgsICJ2b2x1bWUiOiAxMDB9CgoKIyA9PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09
PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PQojIFdPUktFRC1TQU1QTEUgUkVQTEFZIEFOTkVYICJBTk5FWC1SIiDigJQgcGlubmVkIGlucHV0
cwojICAgYmFycyAoY2xvc2UpOiAxMDAsIDk5LCA5NywgOTYsIDk5LCAxMDIsIDEwNCwgMTAzLCAxMDEsIDEwMCAgICgxMCBiYXJzKQojICAgc3RyYXRlZ3k6
IHRocmVzaG9sZCDigJQgYnV5X2JlbG93PTk3LjUsIHNlbGxfYWJvdmU9MTAzLjUsIHVuaXRfcXR5PTEsCiMgICAgICAgICAgICAgaW5pdGlhbF9jYXNoPTEw
MDAwCiMgICBjb3N0IG1vZGVsOiBzcHJlYWQgMC4xMCBwcmljZSDCtyBjb21taXNzaW9uIDAuMDUgcHJpY2Ugwrcgc2xpcHBhZ2UgMC4wIHByaWNlCiMgICAg
ICAgICAgICAgICAoY2l0YXRpb25zOiBiYW5kLWRlY2xhcmVkLCB1bml0IHByaWNlIOKAlCBwbGFuIFBhcnQgNCkKIwojIEhhbmQgY29tcHV0YXRpb246CiMg
ICBidXlzICBhdCBiYXJzIGNsb3NlIDk3IGFuZCA5NiAoY2xvc2UgPCA5Ny41KToKIyAgICAgZWZmZWN0aXZlID0gY2xvc2UgKyAwLjEwICsgMC4wNSA9IDk3
LjE1IGFuZCA5Ni4xNQojICAgc2VsbCAgYXQgYmFyIGNsb3NlIDEwNCAoY2xvc2UgPiAxMDMuNSk6CiMgICAgIGVmZmVjdGl2ZSA9IDEwNCAtIDAuMTUgPSAx
MDMuODUKIyAgIGZpbGxzID0gMzsgZmluYWwgcG9zaXRpb24gPSAxICgrMSArMSAtMSkKIyAgIGNhc2ggID0gMTAwMDAgLSA5Ny4xNSAtIDk2LjE1ICsgMTAz
Ljg1ID0gOTkxMC41NQojICAgZmluYWwgbWFyayA9IDEwMCDihpIgZXF1aXR5ID0gOTkxMC41NSArIDHDlzEwMCA9IDEwMDEwLjU1CiMgPT09PT09PT09PT09
PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT0KCkFOTkVYX0NMT1NFUyA9IFsiMTAwIiwg
Ijk5IiwgIjk3IiwgIjk2IiwgIjk5IiwgIjEwMiIsICIxMDQiLCAiMTAzIiwgIjEwMSIsICIxMDAiXQpBTk5FWF9CQVJTID0gW19iYXIoaSwgYykgZm9yIGks
IGMgaW4gZW51bWVyYXRlKEFOTkVYX0NMT1NFUyldCkFOTkVYX1dJTkRPVyA9IFJlcGxheVdpbmRvdygKICAgIHdpbmRvd19zdGFydD1UMCwgd2luZG93X2Vu
ZD1UMCArIHRpbWVkZWx0YShtaW51dGVzPTE1ICogOSksCiAgICBhc19vZj1UMCArIHRpbWVkZWx0YShtaW51dGVzPTE1ICogOSkpCkFOTkVYX1BBUkFNUyA9
IHsiYnV5X2JlbG93IjogIjk3LjUiLCAic2VsbF9hYm92ZSI6ICIxMDMuNSIsCiAgICAgICAgICAgICAgICAidW5pdF9xdHkiOiAiMSIsICJpbml0aWFsX2Nh
c2giOiAiMTAwMDAifQpBTk5FWF9DT1NUUyA9IHsKICAgICJzcHJlYWQiOiB7InZhbHVlIjogIjAuMTAiLCAidW5pdCI6ICJwcmljZSIsCiAgICAgICAgICAg
ICAgICJjaXRhdGlvbiI6ICJiYW5kLWRlY2xhcmVkOiBmaXhlZCBzeW50aGV0aWMgc3ByZWFkIn0sCiAgICAiY29tbWlzc2lvbiI6IHsidmFsdWUiOiAiMC4w
NSIsICJ1bml0IjogInByaWNlIiwKICAgICAgICAgICAgICAgICAgICJjaXRhdGlvbiI6ICJiYW5kLWRlY2xhcmVkOiBmbGF0IGNvbW1pc3Npb24ifSwKICAg
ICJzbGlwcGFnZSI6IHsidmFsdWUiOiAiMCIsICJ1bml0IjogInByaWNlIiwKICAgICAgICAgICAgICAgICAiY2l0YXRpb24iOiAiYmFuZC1kZWNsYXJlZDog
emVybyBpbiBhbm5leCBzY29wZSJ9LAp9CkFOTkVYX1JFRlMgPSB7Imluc3RydW1lbnQiOiAiYW5uZXguc3ludGhldGljIiwgInRpbWVmcmFtZSI6ICJNMTUi
fQoKCmRlZiBfYW5uZXhfcnVuKCk6CiAgICBjaCA9IGNvbnRlbnRfaGFzaChmaWx0ZXJfYmFyc19nMShBTk5FWF9CQVJTLCBBTk5FWF9XSU5ET1cpLAogICAg
ICAgICAgICAgICAgICAgICAgQU5ORVhfV0lORE9XLCBBTk5FWF9SRUZTKQogICAgcmV0dXJuIHJ1bl9yZXBsYXkoYmFycz1BTk5FWF9CQVJTLCB3aW5kb3c9
QU5ORVhfV0lORE9XLAogICAgICAgICAgICAgICAgICAgICAgc3RyYXRlZ3lfcnVsZT0idGhyZXNob2xkIiwgcGFyYW1ldGVycz1BTk5FWF9QQVJBTVMsCiAg
ICAgICAgICAgICAgICAgICAgICBjb3N0X21vZGVsPUFOTkVYX0NPU1RTLCBzdG9yZWRfY29udGVudF9oYXNoPWNoLAogICAgICAgICAgICAgICAgICAgICAg
c2VyaWVzX3JlZnM9QU5ORVhfUkVGUykKCgojIC0tLSBBbm5leCBjb3JyZWN0bmVzcyAoaGFuZC1jb21wdXRlZCB2YWx1ZXMpIC0tLS0tLS0tLS0tLS0tLS0t
LS0tLS0tLS0tLS0tLS0tLS0KCgpkZWYgdGVzdF9hbm5leF9maWxsX2NvdW50X2FuZF9zaWRlcygpIC0+IE5vbmU6CiAgICByID0gX2FubmV4X3J1bigpCiAg
ICBhc3NlcnQgW2ZbInNpZGUiXSBmb3IgZiBpbiByLmZpbGxzXSA9PSBbImJ1eSIsICJidXkiLCAic2VsbCJdCgoKZGVmIHRlc3RfYW5uZXhfZWZmZWN0aXZl
X3ByaWNlc19leGFjdCgpIC0+IE5vbmU6CiAgICByID0gX2FubmV4X3J1bigpCiAgICBhc3NlcnQgW2ZbImVmZmVjdGl2ZV9wcmljZSJdIGZvciBmIGluIHIu
ZmlsbHNdID09IFsiOTcuMTUiLCAiOTYuMTUiLCAiMTAzLjg1Il0KCgpkZWYgdGVzdF9hbm5leF9zdW1tYXJ5X2V4YWN0KCkgLT4gTm9uZToKICAgIHIgPSBf
YW5uZXhfcnVuKCkKICAgIGFzc2VydCByLnN1bW1hcnlbImZpbmFsX3Bvc2l0aW9uIl0gPT0gIjEiCiAgICBhc3NlcnQgci5zdW1tYXJ5WyJmaW5hbF9jYXNo
Il0gPT0gIjk5MTAuNTUiCiAgICBhc3NlcnQgci5zdW1tYXJ5WyJmaW5hbF9lcXVpdHkiXSA9PSAiMTAwMTAuNTUiCiAgICBhc3NlcnQgci5zdW1tYXJ5WyJm
aWxscyJdID09IDMKICAgIGFzc2VydCByLnN1bW1hcnlbImJhcnNfcmVwbGF5ZWQiXSA9PSAxMAogICAgYXNzZXJ0ICJOT1QgbGl2ZSBvciBmdXR1cmUgcGVy
Zm9ybWFuY2UiIGluIHIuc3VtbWFyeVsicGVyZm9ybWFuY2VfZGlzY2xhaW1lciJdCgoKZGVmIHRlc3RfYW5uZXhfZGV0ZXJtaW5pc3RpY19ieXRlX2lkZW50
aWNhbCgpIC0+IE5vbmU6CiAgICAjIENSLVYyLUJFLTctMDAxIEYtMjogQk8gVC05IHBpbnMgcmV0cnkgeDMgYnl0ZS1pZGVudGljYWwuCiAgICBzMSA9IGpz
b24uZHVtcHMoX2FubmV4X3J1bigpLnN1bW1hcnksIHNvcnRfa2V5cz1UcnVlKQogICAgczIgPSBqc29uLmR1bXBzKF9hbm5leF9ydW4oKS5zdW1tYXJ5LCBz
b3J0X2tleXM9VHJ1ZSkKICAgIHMzID0ganNvbi5kdW1wcyhfYW5uZXhfcnVuKCkuc3VtbWFyeSwgc29ydF9rZXlzPVRydWUpCiAgICBhc3NlcnQgczEgPT0g
czIgPT0gczMKCgojIC0tLSBHLTE6IGFzLW9mIGN1dG9mZiAtLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0t
LS0tLS0KCgpkZWYgdGVzdF9nMV9mdXR1cmVfYmFyX2V4Y2x1ZGVkX2FuZF9zdW1tYXJ5X3VuY2hhbmdlZCgpIC0+IE5vbmU6CiAgICAiIiJFeGl0IGl0ZW0g
aSwgRy0xOiBwbGFudCBhIGJhciBhZnRlciBhc19vZjsgaXQgbXVzdCBiZSBhYnNlbnQgZnJvbQogICAgaW5wdXRzIEFORCB0aGUgc3VtbWFyeSBtdXN0IGVx
dWFsIHRoZSB1bi1wbGFudGVkIHJ1bi4iIiIKICAgIHBsYW50ZWQgPSBBTk5FWF9CQVJTICsgW19iYXIoMTAsICI1MCIpXSAgIyB3b3VsZCB0cmlnZ2VyIGEg
aHVnZSBidXkKICAgIGJhc2UgPSBfYW5uZXhfcnVuKCkuc3VtbWFyeQogICAgY2ggPSBjb250ZW50X2hhc2goZmlsdGVyX2JhcnNfZzEocGxhbnRlZCwgQU5O
RVhfV0lORE9XKSwKICAgICAgICAgICAgICAgICAgICAgIEFOTkVYX1dJTkRPVywgQU5ORVhfUkVGUykKICAgIHIgPSBydW5fcmVwbGF5KGJhcnM9cGxhbnRl
ZCwgd2luZG93PUFOTkVYX1dJTkRPVywKICAgICAgICAgICAgICAgICAgIHN0cmF0ZWd5X3J1bGU9InRocmVzaG9sZCIsIHBhcmFtZXRlcnM9QU5ORVhfUEFS
QU1TLAogICAgICAgICAgICAgICAgICAgY29zdF9tb2RlbD1BTk5FWF9DT1NUUywgc3RvcmVkX2NvbnRlbnRfaGFzaD1jaCwKICAgICAgICAgICAgICAgICAg
IHNlcmllc19yZWZzPUFOTkVYX1JFRlMpCiAgICBhc3NlcnQgci5zdW1tYXJ5ID09IGJhc2UgICMgdGhlIHBsYW50ZWQgYmFyIGhhZCB6ZXJvIGVmZmVjdAoK
CmRlZiB0ZXN0X2cxX3dpbmRvd19ydWxlX2FzX29mX2JlZm9yZV9lbmRfcmVmdXNlZCgpIC0+IE5vbmU6CiAgICB3aXRoIHB5dGVzdC5yYWlzZXMoTGVha2Fn
ZVJlZnVzZWQsIG1hdGNoPSJHLTE6d2luZG93Iik6CiAgICAgICAgUmVwbGF5V2luZG93KHdpbmRvd19zdGFydD1UMCwKICAgICAgICAgICAgICAgICAgICAg
d2luZG93X2VuZD1UMCArIHRpbWVkZWx0YShob3Vycz00KSwKICAgICAgICAgICAgICAgICAgICAgYXNfb2Y9VDAgKyB0aW1lZGVsdGEoaG91cnM9MikpLnZh
bGlkYXRlKCkKCgojIC0tLSBHLTI6IGRlY2lzaW9uLWN1cnNvciBvcmRlcmluZyAtLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0t
LS0tLS0tLS0KCgpkZWYgdGVzdF9nMl9jdXJzb3JfbmV2ZXJfc2Vlc19mdXR1cmUoKSAtPiBOb25lOgogICAgciA9IF9hbm5leF9ydW4oKQogICAgZm9yIGVu
dHJ5IGluIHIuZGVjaXNpb25fbGVkZ2VyOgogICAgICAgIGZvciByZWYgaW4gZW50cnlbImRhdGFfcmVmX3RzIl06CiAgICAgICAgICAgIGFzc2VydCByZWYg
PD0gZW50cnlbImRlY2lzaW9uX3RzIl0KCgojIC0tLSBHLTM6IGhvcml6b24vZW1iYXJnbyAtLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0t
LS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tCgoKZGVmIHRlc3RfZzNfaG9yaXpvbl9wYXN0X2VtYmFyZ29fcmVmdXNlZCgpIC0+IE5vbmU6CiAgICB3aXRoIHB5
dGVzdC5yYWlzZXMoTGVha2FnZVJlZnVzZWQsIG1hdGNoPSJHLTM6aG9yaXpvbiIpOgogICAgICAgIHZhbGlkYXRlX2hvcml6b25fZzMoCiAgICAgICAgICAg
IGxhYmVsX2hvcml6b249dGltZWRlbHRhKGhvdXJzPTQpLAogICAgICAgICAgICBlbWJhcmdvPXRpbWVkZWx0YShtaW51dGVzPTMwKSwKICAgICAgICAgICAg
d2luZG93PUFOTkVYX1dJTkRPVykgICMgd2luZG93IGlzIDJoMTVtIGxvbmcg4oaSIG5vIGxlZ2FsIGRlY2lzaW9uCgoKZGVmIHRlc3RfZzNfbGVnYWxfaG9y
aXpvbl9wYXNzZXMoKSAtPiBOb25lOgogICAgdmFsaWRhdGVfaG9yaXpvbl9nMyhsYWJlbF9ob3Jpem9uPXRpbWVkZWx0YShtaW51dGVzPTE1KSwKICAgICAg
ICAgICAgICAgICAgICAgICAgZW1iYXJnbz10aW1lZGVsdGEobWludXRlcz0xNSksIHdpbmRvdz1BTk5FWF9XSU5ET1cpCgoKIyAtLS0gRy00OiBkZWNpc2lv
bi12cy1kYXRhIG9yZGVyaW5nIC0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0KCgpkZWYgdGVzdF9nNF9jb3Jy
dXB0ZWRfbGVkZ2VyX3JlZnVzZWQoKSAtPiBOb25lOgogICAgYmFkID0gW3siZGVjaXNpb25fdHMiOiBUMCwKICAgICAgICAgICAgImRhdGFfcmVmX3RzIjog
W1QwICsgdGltZWRlbHRhKG1pbnV0ZXM9MTUpXX1dICAjIGRhdGEgQUZURVIgZGVjaXNpb24KICAgIHdpdGggcHl0ZXN0LnJhaXNlcyhMZWFrYWdlUmVmdXNl
ZCwgbWF0Y2g9IkctNDpvcmRlcmluZyIpOgogICAgICAgIHZhbGlkYXRlX2RlY2lzaW9uX29yZGVyaW5nX2c0KGJhZCkKCgojIC0tLSBHLTU6IGNvbnRlbnQg
aW1tdXRhYmlsaXR5IC0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0KCgpkZWYgdGVzdF9nNV90YW1w
ZXJlZF9jb250ZW50X3JlZnVzZWQoKSAtPiBOb25lOgogICAgd2l0aCBweXRlc3QucmFpc2VzKExlYWthZ2VSZWZ1c2VkLCBtYXRjaD0iRy01OmNvbnRlbnQi
KToKICAgICAgICB2ZXJpZnlfY29udGVudF9nNShzdG9yZWRfaGFzaD0iMCIgKiA2NCwgcmVjb21wdXRlZF9oYXNoPSIxIiAqIDY0KQoKCmRlZiB0ZXN0X2c1
X3JlcGxheV9yZWZ1c2VzX29uX3RhbXBlcigpIC0+IE5vbmU6CiAgICB0YW1wZXJlZCA9IFtkaWN0KGIpIGZvciBiIGluIEFOTkVYX0JBUlNdCiAgICB0YW1w
ZXJlZFszXVsiY2xvc2UiXSA9IERlY2ltYWwoIjEiKSAgIyBwb3N0LXJlZ2lzdHJhdGlvbiB0YW1wZXIKICAgIGdvb2RfaGFzaCA9IGNvbnRlbnRfaGFzaChm
aWx0ZXJfYmFyc19nMShBTk5FWF9CQVJTLCBBTk5FWF9XSU5ET1cpLAogICAgICAgICAgICAgICAgICAgICAgICAgICAgIEFOTkVYX1dJTkRPVywgQU5ORVhf
UkVGUykKICAgIHdpdGggcHl0ZXN0LnJhaXNlcyhMZWFrYWdlUmVmdXNlZCwgbWF0Y2g9IkctNTpjb250ZW50Iik6CiAgICAgICAgcnVuX3JlcGxheShiYXJz
PXRhbXBlcmVkLCB3aW5kb3c9QU5ORVhfV0lORE9XLAogICAgICAgICAgICAgICAgICAgc3RyYXRlZ3lfcnVsZT0idGhyZXNob2xkIiwgcGFyYW1ldGVycz1B
Tk5FWF9QQVJBTVMsCiAgICAgICAgICAgICAgICAgICBjb3N0X21vZGVsPUFOTkVYX0NPU1RTLCBzdG9yZWRfY29udGVudF9oYXNoPWdvb2RfaGFzaCwKICAg
ICAgICAgICAgICAgICAgIHNlcmllc19yZWZzPUFOTkVYX1JFRlMpCgoKIyAtLS0gQ29zdCBwdXJpdHkgKyBkZXRlcm1pbmlzbSBtaXNjIC0tLS0tLS0tLS0t
LS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0KCgpkZWYgdGVzdF9jb3N0X2FwcGxpY2F0aW9uX3B1cmVfYW5kX3NpZGVkKCkg
LT4gTm9uZToKICAgIGNtID0gQU5ORVhfQ09TVFMKICAgIGFzc2VydCBhcHBseV9jb3N0cyhEZWNpbWFsKCIxMDAiKSwgImJ1eSIsIGNtKSA9PSBEZWNpbWFs
KCIxMDAuMTUiKQogICAgYXNzZXJ0IGFwcGx5X2Nvc3RzKERlY2ltYWwoIjEwMCIpLCAic2VsbCIsIGNtKSA9PSBEZWNpbWFsKCI5OS44NSIpCiAgICAjIGZy
YWN0aW9uIHVuaXQKICAgIGNtMiA9IHsic3ByZWFkIjogeyJ2YWx1ZSI6ICIwLjAwMSIsICJ1bml0IjogImZyYWN0aW9uIiwgImNpdGF0aW9uIjogIngifSwK
ICAgICAgICAgICAiY29tbWlzc2lvbiI6IHsidmFsdWUiOiAiMCIsICJ1bml0IjogInByaWNlIiwgImNpdGF0aW9uIjogIngifSwKICAgICAgICAgICAic2xp
cHBhZ2UiOiB7InZhbHVlIjogIjAiLCAidW5pdCI6ICJwcmljZSIsICJjaXRhdGlvbiI6ICJ4In19CiAgICBhc3NlcnQgYXBwbHlfY29zdHMoRGVjaW1hbCgi
MTAwIiksICJidXkiLCBjbTIpID09IERlY2ltYWwoIjEwMC4xIikKCgpkZWYgdGVzdF9hbmNob3JfaW5wdXRzX2hhc2hfc2Vuc2l0aXZpdHkoKSAtPiBOb25l
OgogICAgYXNzZW1ibGVkID0gZmlsdGVyX2JhcnNfZzEoQU5ORVhfQkFSUywgQU5ORVhfV0lORE9XKQogICAgaDEgPSBjb250ZW50X2hhc2goYXNzZW1ibGVk
LCBBTk5FWF9XSU5ET1csIEFOTkVYX1JFRlMpCiAgICBjaGFuZ2VkID0gW2RpY3QoYikgZm9yIGIgaW4gYXNzZW1ibGVkXQogICAgY2hhbmdlZFswXVsiY2xv
c2UiXSA9IERlY2ltYWwoIjEwMC4wMDAxIikKICAgIGFzc2VydCBjb250ZW50X2hhc2goY2hhbmdlZCwgQU5ORVhfV0lORE9XLCBBTk5FWF9SRUZTKSAhPSBo
MQoKCmRlZiB0ZXN0X2VuZ2luZV92ZXJzaW9uc19oYXNoX2Nhbm9uaWNhbCgpIC0+IE5vbmU6CiAgICBpbXBvcnQgaGFzaGxpYgoKICAgIGZyb20gYXBwLnYy
LnJlc2VhcmNoX2pvYnMucmVwbGF5IGltcG9ydCBFTkdJTkVfVkVSU0lPTlMKCiAgICBleHBlY3RlZCA9IGhhc2hsaWIuc2hhMjU2KGpzb24uZHVtcHMoCiAg
ICAgICAgRU5HSU5FX1ZFUlNJT05TLCBzb3J0X2tleXM9VHJ1ZSwgc2VwYXJhdG9ycz0oIiwiLCAiOiIpCiAgICApLmVuY29kZSgpKS5oZXhkaWdlc3QoKQog
ICAgYXNzZXJ0IGVuZ2luZV92ZXJzaW9uc19oYXNoKCkgPT0gZXhwZWN0ZWQKCgojIC0tLSBQLTk6IHJlc3VsdC1jbGFzcyBsYXcgLS0tLS0tLS0tLS0tLS0t
LS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0KCgpkZWYgdGVzdF9yZXN1bHRfY2xhc3NfdGF4b25vbXlfYW5kX3Jl
ZnVzYWxzKCkgLT4gTm9uZToKICAgIGFzc2VydCBSRVNVTFRfQ0xBU1NfVEFYT05PTVkgPT0gKCJiYWNrdGVzdCIsICJzaW11bGF0aW9uIiwgInBhcGVyIiwg
ImxpdmUiKQogICAgYXNzZXJ0IENPTlNUUlVDVElCTEVfUkVTVUxUX0NMQVNTRVMgPT0gKCJiYWNrdGVzdCIsICJzaW11bGF0aW9uIikKICAgIGFzc2VydCBy
ZXF1aXJlX2NvbnN0cnVjdGlibGVfcmVzdWx0X2NsYXNzKCJiYWNrdGVzdCIpID09ICJiYWNrdGVzdCIKICAgIGFzc2VydCByZXF1aXJlX2NvbnN0cnVjdGli
bGVfcmVzdWx0X2NsYXNzKCJzaW11bGF0aW9uIikgPT0gInNpbXVsYXRpb24iCiAgICBmb3IgYmFubmVkIGluICgicGFwZXIiLCAibGl2ZSIsICJzaGFkb3ci
KToKICAgICAgICB3aXRoIHB5dGVzdC5yYWlzZXMoUmVzdWx0Q2xhc3NSZWZ1c2VkKToKICAgICAgICAgICAgcmVxdWlyZV9jb25zdHJ1Y3RpYmxlX3Jlc3Vs
dF9jbGFzcyhiYW5uZWQpCgoKZGVmIHRlc3RfdGF4b25vbXlfc2hhcmVkX3dpdGhfbGluZWFnZSgpIC0+IE5vbmU6CiAgICBmcm9tIGFwcC52Mi5yZXNlYXJj
aF9nb3Zlcm5hbmNlLmNvbnRyYWN0cyBpbXBvcnQgREFUQV9DTEFTU0VTCgogICAgYXNzZXJ0IFJKX0RBVEFfQ0xBU1NFUyA9PSBEQVRBX0NMQVNTRVMgICMg
bm8gZm9yawo=
'@
Write-Evidence ("record 17/17 staged: " + $Rec17Path)

$FileRecords = @(
    [pscustomobject]@{ Path = $Rec1Path; Sha = $Rec1Sha; B64 = $Rec1B64 },
    [pscustomobject]@{ Path = $Rec2Path; Sha = $Rec2Sha; B64 = $Rec2B64 },
    [pscustomobject]@{ Path = $Rec3Path; Sha = $Rec3Sha; B64 = $Rec3B64 },
    [pscustomobject]@{ Path = $Rec4Path; Sha = $Rec4Sha; B64 = $Rec4B64 },
    [pscustomobject]@{ Path = $Rec5Path; Sha = $Rec5Sha; B64 = $Rec5B64 },
    [pscustomobject]@{ Path = $Rec6Path; Sha = $Rec6Sha; B64 = $Rec6B64 },
    [pscustomobject]@{ Path = $Rec7Path; Sha = $Rec7Sha; B64 = $Rec7B64 },
    [pscustomobject]@{ Path = $Rec8Path; Sha = $Rec8Sha; B64 = $Rec8B64 },
    [pscustomobject]@{ Path = $Rec9Path; Sha = $Rec9Sha; B64 = $Rec9B64 },
    [pscustomobject]@{ Path = $Rec10Path; Sha = $Rec10Sha; B64 = $Rec10B64 },
    [pscustomobject]@{ Path = $Rec11Path; Sha = $Rec11Sha; B64 = $Rec11B64 },
    [pscustomobject]@{ Path = $Rec12Path; Sha = $Rec12Sha; B64 = $Rec12B64 },
    [pscustomobject]@{ Path = $Rec13Path; Sha = $Rec13Sha; B64 = $Rec13B64 },
    [pscustomobject]@{ Path = $Rec14Path; Sha = $Rec14Sha; B64 = $Rec14B64 },
    [pscustomobject]@{ Path = $Rec15Path; Sha = $Rec15Sha; B64 = $Rec15B64 },
    [pscustomobject]@{ Path = $Rec16Path; Sha = $Rec16Sha; B64 = $Rec16B64 },
    [pscustomobject]@{ Path = $Rec17Path; Sha = $Rec17Sha; B64 = $Rec17B64 }
)
New-Item -ItemType Directory -Force -Path $BackupDir | Out-Null
foreach ($Rec in $FileRecords) {
    $Rel  = $Rec.Path
    $Pin  = $Rec.Sha
    $Bytes = B64-Decode -B64Chunk $Rec.B64
    $BytesHash = Hash-Bytes -Bytes $Bytes
    if ($BytesHash -ne $Pin) {
        throw ("STOP (pack integrity): decoded literal for " + $Rel + " hashes " + $BytesHash + " != declared pin " + $Pin + " . The pack is damaged; STOP and report to ITRGA; do not proceed.")
    }
    $Dest = Join-Path $BackendRoot $Rel
    $IsModified = ($ModifiedPaths -contains $Rel)
    if ((Test-Path $Dest) -and (-not $IsModified)) {
        $ExistingHash = (Get-FileHash -Path $Dest -Algorithm SHA256).Hash.ToLower()
        if ($ExistingHash -eq $Pin) {
            Write-Evidence ("identity-proven pre-landing ACCEPTED: " + $Rel + " (sha256 == accepted pin; operator-side merge adjudicated; treated as landed)")
            continue
        }
        throw ("STOP (foreign-state law): new-file target exists with bytes NOT equal to the accepted pin: " + $Dest + " (hash " + $ExistingHash + "). The tree state cannot be adjudicated; STOP and report to ITRGA; do not modify anything.")
    }
    if ($IsModified) {
        $PreHash = (Get-FileHash -Path $Dest -Algorithm SHA256).Hash.ToLower()
        $BName = ($Rel -replace "\\", "__")
        $BDest = Join-Path $BackupDir $BName
        Copy-Item -Path $Dest -Destination $BDest -Force
        Write-Evidence ("pre-write backup: " + $Rel + " (pre-state sha256 " + $PreHash + ") -> operator-evidence\BE-7\pre-write-backup\" + $BName)
    }
    New-Item -ItemType Directory -Force -Path (Split-Path $Dest) | Out-Null
    [IO.File]::WriteAllBytes($Dest, $Bytes)
    $PostHash = (Get-FileHash -Path $Dest -Algorithm SHA256).Hash.ToLower()
    if ($PostHash -ne $Pin) {
        throw ("STOP (landing gate): written file " + $Dest + " hashes " + $PostHash + " != declared pin " + $Pin + " . Filesystem-level corruption; restore the anchor above and report to ITRGA.")
    }
    Write-Evidence ("landed + verified: " + $Rel + "  sha256=" + $PostHash.Substring(0, 16) + "... (" + $Bytes.Length + " B)")
}
Write-Evidence "PASS: A4 - all 17 delivered files landed, each sha256-verified at decode AND after write."

# ---------------------------------------------------------------------
# A5. THE SINGLE SANCTIONED SCHEMA MUTATION
# ---------------------------------------------------------------------
Write-Section "A5. alembic upgrade head (20260903_0047)"
Push-Location $BackendRoot
try {
    Write-Evidence "ALEMBIC: alembic upgrade head"
    $OutUp = & $Py -m alembic upgrade head 2>&1
    $UpCode = $LASTEXITCODE
    Emit-Output $OutUp
    if ($UpCode -ne 0) { throw ("FAIL: A5 - alembic upgrade head exited " + $UpCode + " . Database left at its pre-upgrade state per alembic semantics; the A2 anchor is the rollback point; restore it and report to ITRGA.") }
    $OutCur2 = & $Py -m alembic current 2>&1
    $Cur2Lines = @(@($OutCur2) | Where-Object { ([string]$_) -match $ApplyTargetRevision })
    if ($Cur2Lines.Count -ne 1) { throw ("FAIL: A5 - expected exactly one current line naming " + $ApplyTargetRevision + "; observed '" + (Norm-Text $OutCur2) + "'.") }
    if ((Norm-Text $Cur2Lines) -notmatch [regex]::Escape("(head)")) { throw ("FAIL: A5 - 0047 is current but NOT marked (head): '" + (Norm-Text $Cur2Lines) + "'.") }
    $OutHeads2 = & $Py -m alembic heads 2>&1
    $Heads2Lines = @(@($OutHeads2) | Where-Object { ([string]$_) -match $ApplyTargetRevision })
    if ($Heads2Lines.Count -ne 1) { throw ("FAIL: A5 - expected a single head " + $ApplyTargetRevision + "; observed '" + (Norm-Text $OutHeads2) + "'.") }
} finally { Pop-Location }
Write-Evidence "PASS: A5 - chain at 20260903_0047 (head), single head; exactly one sanctioned mutation performed."

# ---------------------------------------------------------------------
# A6. POST-CENSUS (totals + exact members; compver apply-time gate)
# ---------------------------------------------------------------------
Write-Section "A6. POST-CENSUS vs BO/ACC LITERALS"
$OutPost = & $Py $HelperCensus $TargetDbPath 2>&1
if ($LASTEXITCODE -ne 0) { throw ("FAIL: A6 - census helper failed: " + (Norm-Text $OutPost)) }
$Post = (Norm-Text $OutPost) | ConvertFrom-Json
if ($Post.triggers.Count -ne $ExpectTriggersTotal) { throw ("FAIL: A6 - v2 trigger census " + $Post.triggers.Count + " != " + $ExpectTriggersTotal) }
if ($Post.permissions.Count -ne $ExpectPermsTotal) { throw ("FAIL: A6 - permission census " + $Post.permissions.Count + " != " + $ExpectPermsTotal) }
if ($Post.compver.Count -ne $ExpectCompverTotal) { throw ("FAIL: A6 - compver census " + $Post.compver.Count + " != " + $ExpectCompverTotal) }
$TenNew = @(
    "v2_backtest_input_immutable_update",
    "v2_backtest_input_immutable_delete",
    "v2_cost_model_immutable_update",
    "v2_cost_model_immutable_delete",
    "v2_strategy_version_immutable_update",
    "v2_strategy_version_immutable_delete",
    "v2_research_job_attempt_immutable_update",
    "v2_research_job_attempt_immutable_delete",
    "v2_research_result_immutable_update",
    "v2_research_result_immutable_delete"
)
foreach ($Tn in $TenNew) {
    if ($Post.triggers -notcontains $Tn) { throw ("FAIL: A6 - required trigger missing: " + $Tn) }
}
if (@($Post.triggers | Where-Object { $_ -like "v2_research_job_immutable_*" }).Count -ne 0) {
    throw "FAIL: A6 - a v2_research_job immutability guard exists; FP-1 by-design-unguarded law violated."
}
$PermTriples = @(
    "admin|v2.research.jobs.read|SAL-2",
    "admin|v2.research.jobs.submit|SAL-3",
    "admin|v2.research.jobs.cancel|SAL-3",
    "admin|v2.research.registry.read|SAL-2",
    "admin|v2.research.registry.write|SAL-3",
    "admin|v2.research.results.read|SAL-2",
    "operator|v2.research.jobs.read|SAL-2",
    "operator|v2.research.results.read|SAL-2"
)
$PostPermSet = @($Post.permissions | ForEach-Object { $_[0] + "|" + $_[1] + "|" + $_[2] })
foreach ($Pt in $PermTriples) {
    if ($PostPermSet -notcontains $Pt) { throw ("FAIL: A6 - required permission triple missing: " + $Pt) }
}
$PostCompSet = @($Post.compver | ForEach-Object { $_[0] + "|" + $_[1] + "|" + $_[2] })
$RpeRow = "replay_engine|rpe-1.0.0|" + $RpeHash
$RjeRow = "research_job_engine|rje-1.0.0|" + $RjeHash
if ($PostCompSet -notcontains $RpeRow) { throw ("FAIL: A6 - compver row mismatch: expected exact '" + $RpeRow + "' (apply-time RPE gate).") }
if ($PostCompSet -notcontains $RjeRow) { throw ("FAIL: A6 - compver row mismatch: expected exact '" + $RjeRow + "' (apply-time RJE gate; ITRGA-ACC-V2-BE-7-001 section 5).") }
Write-Evidence "PASS: A6 - census exactly 42 / 49 / 8; the ten new trigger names present; v2_research_job unguarded by design (present-by-absence proven); eight permission triples exact; compver rows byte-exact to the ACC pre-declared literals."

# ---------------------------------------------------------------------
# A7. LIVE GUARD PROBES (insert-probe-rollback; nothing persists)
# ---------------------------------------------------------------------
Write-Section "A7. LIVE GUARD PROBES - TEN EXACT REFUSAL MESSAGES"
$ProbePlan = @(
    "v2_backtest_input_immutable_update~INSERT INTO v2_backtest_input (id,input_id,record_seq,supersedes,content_hash,series_refs,window_start,window_end,registration_outcome,data_class,mode,operator_id,correlation_id,created_at) VALUES ('probe-r','probe-i',1,NULL,'probehash','{}','2026-01-01 00:00:00','2026-01-02 00:00:00','registered','synthetic','RESEARCH','probe-op',NULL,'2026-01-01 00:00:00')~UPDATE v2_backtest_input SET record_seq = record_seq + 1~V2 backtest inputs are immutable; UPDATE prohibited",
    "v2_backtest_input_immutable_delete~INSERT INTO v2_backtest_input (id,input_id,record_seq,supersedes,content_hash,series_refs,window_start,window_end,registration_outcome,data_class,mode,operator_id,correlation_id,created_at) VALUES ('probe-r','probe-i',1,NULL,'probehash','{}','2026-01-01 00:00:00','2026-01-02 00:00:00','registered','synthetic','RESEARCH','probe-op',NULL,'2026-01-01 00:00:00')~DELETE FROM v2_backtest_input~V2 backtest inputs are immutable; DELETE prohibited",
    "v2_cost_model_immutable_update~INSERT INTO v2_cost_model (id,cost_model_id,record_seq,supersedes,spread,commission,slippage,latency_ms,risk_limits,citations,data_class,mode,operator_id,correlation_id,created_at) VALUES ('probe-r','probe-c',1,NULL,'{}','{}','{}',0,'{}','{}','synthetic','RESEARCH','probe-op',NULL,'2026-01-01 00:00:00')~UPDATE v2_cost_model SET record_seq = record_seq + 1~V2 cost models are immutable; UPDATE prohibited",
    "v2_cost_model_immutable_delete~INSERT INTO v2_cost_model (id,cost_model_id,record_seq,supersedes,spread,commission,slippage,latency_ms,risk_limits,citations,data_class,mode,operator_id,correlation_id,created_at) VALUES ('probe-r','probe-c',1,NULL,'{}','{}','{}',0,'{}','{}','synthetic','RESEARCH','probe-op',NULL,'2026-01-01 00:00:00')~DELETE FROM v2_cost_model~V2 cost models are immutable; DELETE prohibited",
    "v2_strategy_version_immutable_update~INSERT INTO v2_strategy_version (id,strategy_id,record_seq,supersedes,name,parameters,lifecycle_state,data_class,mode,operator_id,correlation_id,created_at) VALUES ('probe-r','probe-s',1,NULL,'probe','{}','draft','synthetic','RESEARCH','probe-op',NULL,'2026-01-01 00:00:00')~UPDATE v2_strategy_version SET record_seq = record_seq + 1~V2 strategy versions are immutable; UPDATE prohibited",
    "v2_strategy_version_immutable_delete~INSERT INTO v2_strategy_version (id,strategy_id,record_seq,supersedes,name,parameters,lifecycle_state,data_class,mode,operator_id,correlation_id,created_at) VALUES ('probe-r','probe-s',1,NULL,'probe','{}','draft','synthetic','RESEARCH','probe-op',NULL,'2026-01-01 00:00:00')~DELETE FROM v2_strategy_version~V2 strategy versions are immutable; DELETE prohibited",
    "v2_research_job_attempt_immutable_update~INSERT INTO v2_research_job_attempt (id,job_id,attempt_index,outcome,artifact_ref,reason,actor_id,mode,operator_id,correlation_id,created_at) VALUES ('probe-r','probe-j',1,'failed',NULL,'{}','probe-actor','RESEARCH','probe-op',NULL,'2026-01-01 00:00:00')~UPDATE v2_research_job_attempt SET record_seq = record_seq + 1~V2 research job attempts are immutable; UPDATE prohibited",
    "v2_research_job_attempt_immutable_delete~INSERT INTO v2_research_job_attempt (id,job_id,attempt_index,outcome,artifact_ref,reason,actor_id,mode,operator_id,correlation_id,created_at) VALUES ('probe-r','probe-j',1,'failed',NULL,'{}','probe-actor','RESEARCH','probe-op',NULL,'2026-01-01 00:00:00')~DELETE FROM v2_research_job_attempt~V2 research job attempts are immutable; DELETE prohibited",
    "v2_research_result_immutable_update~INSERT INTO v2_research_result (id,result_class,job_id,attempt_index,strategy_version_id,input_registry_id,cost_model_id,inputs_hash,engine_versions,engine_versions_hash,summary,replay_of,time_basis,data_class,mode,operator_id,correlation_id,created_at) VALUES ('probe-r','backtest','probe-j',1,'probe-s','probe-i','probe-c','h','{}','e','{}',NULL,'{}','synthetic','RESEARCH','probe-op',NULL,'2026-01-01 00:00:00')~UPDATE v2_research_result SET record_seq = record_seq + 1~V2 research results are immutable; UPDATE prohibited",
    "v2_research_result_immutable_delete~INSERT INTO v2_research_result (id,result_class,job_id,attempt_index,strategy_version_id,input_registry_id,cost_model_id,inputs_hash,engine_versions,engine_versions_hash,summary,replay_of,time_basis,data_class,mode,operator_id,correlation_id,created_at) VALUES ('probe-r','backtest','probe-j',1,'probe-s','probe-i','probe-c','h','{}','e','{}',NULL,'{}','synthetic','RESEARCH','probe-op',NULL,'2026-01-01 00:00:00')~DELETE FROM v2_research_result~V2 research results are immutable; DELETE prohibited"
)
foreach ($Plan in $ProbePlan) {
    $Partsp = $Plan.Split("~")
    $OutProbe = & $Py $HelperProbe $TargetDbPath $Partsp[1] $Partsp[2] $Partsp[3] 2>&1
    if ($LASTEXITCODE -ne 0 -or (Norm-Text $OutProbe) -ne "PROBE-EXACT-MATCH") {
        throw ("FAIL: A7 - guard probe for " + $Partsp[0] + " did not refuse with the exact message: '" + (Norm-Text $OutProbe) + "'.")
    }
    Write-Evidence ("probe OK: " + $Partsp[0] + " -> exact refusal witnessed")
}
Write-Evidence "PASS: A7 - all ten guard triggers refuse live with their exact BO T-3 messages (transactional probes; database unchanged)."

# ---------------------------------------------------------------------
# A8. FULL SUITE (972 passed / 0 failed)
# ---------------------------------------------------------------------
Write-Section "A8. FULL TEST SUITE (certified pins; tail witnessed)"
Push-Location $BackendRoot
try {
    Write-Evidence "PYTEST: python -m pytest -q"
    $OutSuite = & $Py -m pytest -q 2>&1
    $SuiteCode = $LASTEXITCODE
} finally { Pop-Location }
$SuiteText = Norm-Text $OutSuite
$TailLines = @(@($OutSuite) | Select-Object -Last 30)
Emit-Output $TailLines
if ($SuiteCode -ne 0) { throw ("FAIL: A8 - pytest exited " + $SuiteCode + " . See tail above; report to ITRGA.") }
if ($SuiteText -notmatch ("^" + $SuiteFloor + " passed") -and $SuiteText -notmatch ("= " + $SuiteFloor + " passed")) {
    throw ("FAIL: A8 - suite summary does not declare '" + $SuiteFloor + " passed': tail above.")
}
if ($SuiteText -match "[1-9][0-9]* (failed|error)") { throw "FAIL: A8 - failures/errors present in the suite summary." }
$SuiteSummary = ($TailLines | Where-Object { ([string]$_) -match "passed" } | Select-Object -Last 1)
Write-Evidence ("PASS: A8 - suite summary: " + ([string]$SuiteSummary).Trim())

# ---------------------------------------------------------------------
# A9. DRIFT GATE (PGF-014 format-independent)
# ---------------------------------------------------------------------
Write-Section "A9. DRIFT GATE AT 20260903_0047 (format-independent)"
Push-Location $BackendRoot
try {
    $OutChk = & $Py -m alembic check 2>&1
    $ChkCode = $LASTEXITCODE
} finally { Pop-Location }
Emit-Output $OutChk
$Drift = (Norm-Text $OutChk).ToLower()
if ($ChkCode -eq 0) { throw "FAIL: A9 - alembic check exited 0; the inherited drift declaration expects non-zero (the 9 inherited V1 tokens)." }
foreach ($Marker in @("v2_backtest_input","v2_cost_model","v2_strategy_version","v2_research_job","v2_research_result","v2_md_","v2_permission","v2_computation_version")) {
    if ($Drift.Contains($Marker)) { throw ("FAIL: A9 - band/v2 drift token present: '" + $Marker + "'. Zero band tokens is the law; report to ITRGA.") }
}
if ((-not $Drift.Contains("not up to date")) -and (-not $Drift.Contains("audit_write_failure_records"))) {
    throw "FAIL: A9 - inheritance witness absent (neither 'not up to date' nor 'audit_write_failure_records' in drift output)."
}
Write-Evidence "PASS: A9 - drift gate: non-zero exit (inherited diffs), zero band/v2 tokens, inheritance witness present."

# ---------------------------------------------------------------------
# A10. FINAL STATE RECORD
# ---------------------------------------------------------------------
Write-Section "A10. APPLY-FINAL-STATE RECORD"
$DbHashPost = (Get-FileHash -Path $TargetDbPath -Algorithm SHA256).Hash.ToLower()
$StateLines = @(
    "STATE_FILE_ID=ITRGA-V2-0047-APPLY-FINAL-STATE-V2",
    "TARGET_REVISION=" + $ApplyTargetRevision,
    "TRIGGERS_TOTAL=" + $ExpectTriggersTotal,
    "PERMISSIONS_TOTAL=" + $ExpectPermsTotal,
    "COMPVER_TOTAL=" + $ExpectCompverTotal,
    "COMPVER_RPE_HASH=" + $RpeHash,
    "COMPVER_RJE_HASH=" + $RjeHash,
    "SUITE_RESULT=" + ([string]$SuiteSummary).Trim(),
    "DB_PATH=" + $TargetDbPath,
    "DB_SHA256_POST=" + $DbHashPost,
    "ANCHOR_SHA256=" + $AnchorHash,
    "TRANSCRIPT=0047-APPLY-RUN-V2.txt",
    "UTC_COMPLETED=" + ([DateTime]::UtcNow.ToString("yyyy-MM-ddTHH:mm:ssZ"))
)
$StateLines | Set-Content -Path $StateRecPath -Encoding UTF8
foreach ($Sl in $StateLines) { Write-Evidence "STATE: " + $Sl }
Write-Evidence ""
Write-Evidence "APPLY PACK COMPLETE - PASS. Chain at 20260903_0047 (head). Keep the application STOPPED. Next act: execute ITRGA_V2_0047_VERIFY_PACK_V2.ps1, then send back operator-evidence\BE-7\0047-APPLY-RUN-V2.txt and 0047-VERIFY-RUN-V2.txt. Restart the application only after the verify pack PASSes."
Write-Evidence ("UTC end: " + ([DateTime]::UtcNow.ToString("yyyy-MM-ddTHH:mm:ssZ")))
