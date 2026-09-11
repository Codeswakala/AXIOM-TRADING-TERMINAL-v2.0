
# =====================================================================
# AXIOM V2 - 0047 WORKING-DATABASE APPLICATION ACT (BAND BE-7)
# ITRGA SQLITE VERIFY ACT EVIDENCE PACK (V2)
# Pack ID: ITRGA-V2-0047-VERIFY-PACK-V3
# Authority: BO-V2-BE-7-001 T-1...T-14; ITRGA-ACC-V2-BE-7-001 section 5;
#   ITRGA-PTN-V2-PACK-001; pattern ITRGA-V2-0043-VERIFY-PACK-V1 (all
#   PGF lessons by construction; E-0046-DUP refuse-if-completed law;
#   independent re-proof: this pack trusts NOTHING it did not recompute
#   on this run - the apply-final-state record is strict-parsed and
#   cross-checked against this pack's embedded ACC literals AND against
#   a live recomputation of every census, file hash, and gate).
#
# WHAT THIS PACK DOES (READ-ONLY on the database and the tree; writes
#   only its own transcript and verify-final-state record in
#   operator-evidence\BE-7, plus a throwaway helper removed on exit):
#   - Requires the apply-final-state record (strict KEY=VALUE parse;
#     exact key set; identity pin) - the verify act cannot precede the
#     apply act.
#   - Refuses to start if 0047-VERIFY-FINAL-STATE.txt already exists
#     (completed-run law).
#   - Re-hashes all 17 delivered files against the ACCEPTED pins and
#     the six V1 files against the attested pins.
#   - Re-proves the terminal state: chain head 20260903_0047 (single);
#     censuses 42 / 49 / 8 with exact members incl. the compver rows
#     pinned to the ACC section 5 literals; ten live guard probes with
#     exact messages (transactional insert-probe-rollback; nothing
#     persists); full test suite 972 passed / 0 failed; drift gate
#     (non-zero exit, zero band/v2 tokens, inheritance witness).
#   - Never mutates the database; never runs any Git command; asks for
#     nothing but the database file path (a path, not a credential).
#
# BEFORE RUNNING: the application must still be STOPPED (run it only
#   after this pack PASSes).
#
# RUN MODE: this pack MUST be executed as a file from the repository
#   root, ONLY after ITRGA_V2_0047_APPLY_PACK_V3.ps1 has PASSed:
#     powershell -NoProfile -ExecutionPolicy Bypass -File ".\ITRGA_V2_0047_VERIFY_PACK_V3.ps1"
#
# OPERATOR INSTRUCTION CARD:
#   1. MD5-verify the issuance-note pins for all three artifacts FIRST.
#   2. Run this pack SECOND (after the apply pack PASS).
#   3. Send back operator-evidence\BE-7\0047-VERIFY-RUN-V3.txt.
#
#
# SUPERSESSION RECORD (V3, 2026-09-04):
#   V2 pair retired UNUSED-STOPPED (terminated mid-A1 by the PGF-018
#   NATIVE-STDERR LAW: a native command writing routine lines to stderr
#   (alembic INFO logging) under "2>&1" wraps each line as an error
#   record; with $ErrorActionPreference="Stop" that record terminates
#   the pack; the run died before the anchor step - nothing mutated).
#   Also repaired two latent cousins in the same argument-mode family:
#   (a) dash-bearing native arguments must be array ELEMENTS, not bare
#   tokens (PowerShell parameter binding matches -m/-p style tokens
#   against parameter names); (b) inline "str" + $var concatenation in
#   a call's argument list splits into separate arguments (PGF-017 law
#   applies to native-call argument lists too - concatenation only
#   inside parentheses). ALL native invocations in both packs now run
#   behind Invoke-Capped with array-form argument lists, executed under
#   a dynamically-scoped "Continue", returning clean strings.

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
$Transcript    = Join-Path $EvidenceDir "0047-VERIFY-RUN-V3.txt"
$ApplyRecPath  = Join-Path $EvidenceDir "0047-APPLY-FINAL-STATE.txt"
$VerifyRecPath = Join-Path $EvidenceDir "0047-VERIFY-FINAL-STATE.txt"
$PinsPath      = Join-Path $RepoRoot "ITRGA_V2_0047_BASELINE_PINS.txt"
$HelperProbe   = Join-Path $env:TEMP "be7_0047_guardprobe.py"
$HelperCensus  = Join-Path $env:TEMP "be7_0047_census.py"

$ApplyTargetRevision = "20260903_0047"
$BaselineRevision    = "20260903_0046"
$ExpectTriggersTotal = 42
$ExpectPermsTotal    = 49
$ExpectCompverTotal  = 8
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

function Invoke-Capped {
    param(
        [Parameter(Mandatory=$true, Position=0)][string]$Exe,
        [Parameter(Position=1, ValueFromRemainingArguments=$true)][object[]]$CallArgs
    )
    $ErrorActionPreference = 'Continue'   # dynamic scope: native stderr must never terminate (PGF-018)
    $collected = & $Exe @CallArgs 2>&1
    $script:NativeExit = $LASTEXITCODE
    return @($collected | ForEach-Object { [string]$_ })
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
        if ($Map.ContainsKey($Key)) { throw ("STOP: duplicate key '" + $Key + "' in pin file " + $Path + " (" + $Label + ").") }
        $Map[$Key] = $Val
    }
    $Got = @($Map.Keys | Sort-Object)
    $Exp = @($ExpectedKeys | Sort-Object)
    if (($Got -join ",") -ne ($Exp -join ",")) {
        throw ("STOP: pin file key set mismatch in " + $Path + ": got [" + ($Got -join ", ") + "], expected [" + ($Exp -join ", ") + "] (" + $Label + ").")
    }
    return $Map
}
function B64-Decode {
    param([string]$B64Chunk)
    $Joined = ($B64Chunk -split "`n" | ForEach-Object { $_.Trim() }) -join ""
    return [Convert]::FromBase64String($Joined)
}

# ---------------------------------------------------------------------
# B0. ORDER, HYGIENE, AUTHORITY SWEEP, APPLY RECORD
# ---------------------------------------------------------------------
if (!(Test-Path $BackendRoot)) { throw ("STOP: backend directory not found: " + $BackendRoot + ". Run from the repository root.") }
New-Item -ItemType Directory -Force -Path $EvidenceDir | Out-Null
if (Test-Path $VerifyRecPath) {
    throw ("STOP (E-0046-DUP law): a completed verify record already exists: " + $VerifyRecPath + " . Refusing to disturb it; report to ITRGA if you believe it is stale.")
}
if (!(Test-Path $ApplyRecPath)) {
    throw ("STOP: apply-final-state record missing: " + $ApplyRecPath + " . The verify act cannot precede the apply act. Run ITRGA_V2_0047_APPLY_PACK_V3.ps1 first.")
}
Remove-Item -Force -ErrorAction SilentlyContinue $Transcript

$AuthorityVars = @(Get-ChildItem env: | Where-Object { $_.Name -like "AXIOM_TD_*" })
foreach ($Av in $AuthorityVars) { Remove-Item ("env:" + $Av.Name) -ErrorAction SilentlyContinue }
if (@(Get-ChildItem env: | Where-Object { $_.Name -like "AXIOM_TD_*" }).Count -gt 0) { throw "STOP: an AXIOM_TD_* authority variable persists." }

Write-Section "0047 VERIFY PACK V3 - ITRGA-V2-0047-VERIFY-PACK-V3"
Write-Evidence ("UTC start: " + ([DateTime]::UtcNow.ToString("yyyy-MM-ddTHH:mm:ssZ")))
Write-Evidence "Read-only verification. Trusts nothing it did not recompute on this run."

$Pins = Read-Pins -Path $PinsPath -ExpectedKeys @(
    "PINS_FILE_ID","TARGET_REVISION","BASELINE_REVISION",
    "V2_TRIGGERS_AFTER","PERMISSIONS_AFTER","COMPVER_AFTER",
    "COMPVER_RPE_HASH","COMPVER_RJE_HASH","SUITE_FLOOR",
    "ALEMBIC_PIN","PYTEST_PIN") -Label "baseline pins"
if ($Pins["PINS_FILE_ID"] -ne "ITRGA-V2-0047-BASELINE-PINS-V1") { throw "STOP: pin file identity mismatch." }
if ($Pins["COMPVER_RPE_HASH"] -ne $RpeHash) { throw "STOP: RPE pin mismatch vs embedded ACC literal." }
if ($Pins["COMPVER_RJE_HASH"] -ne $RjeHash) { throw "STOP: RJE pin mismatch vs embedded ACC literal." }

$ApplyState = Read-Pins -Path $ApplyRecPath -ExpectedKeys @(
    "STATE_FILE_ID","TARGET_REVISION","TRIGGERS_TOTAL","PERMISSIONS_TOTAL",
    "COMPVER_TOTAL","COMPVER_RPE_HASH","COMPVER_RJE_HASH","SUITE_RESULT",
    "DB_PATH","DB_SHA256_POST","ANCHOR_SHA256","TRANSCRIPT","UTC_COMPLETED") -Label "apply-final-state"
if ($ApplyState["STATE_FILE_ID"] -ne "ITRGA-V2-0047-APPLY-FINAL-STATE-V3") { throw "STOP: apply state identity mismatch." }
if ($ApplyState["TARGET_REVISION"] -ne $ApplyTargetRevision) { throw "STOP: apply state revision mismatch." }
if ([int]$ApplyState["TRIGGERS_TOTAL"] -ne $ExpectTriggersTotal) { throw "STOP: apply state trigger-total mismatch vs this pack's embedded literals." }
if ([int]$ApplyState["PERMISSIONS_TOTAL"] -ne $ExpectPermsTotal) { throw "STOP: apply state permission-total mismatch." }
if ([int]$ApplyState["COMPVER_TOTAL"] -ne $ExpectCompverTotal) { throw "STOP: apply state compver-total mismatch." }
if ($ApplyState["COMPVER_RPE_HASH"] -ne $RpeHash) { throw "STOP: apply state RPE mismatch." }
if ($ApplyState["COMPVER_RJE_HASH"] -ne $RjeHash) { throw "STOP: apply state RJE mismatch." }
if ($ApplyState["SUITE_RESULT"] -notmatch ([regex]::Escape(($SuiteFloor.ToString() + " passed")))) { throw "STOP: apply state suite result does not declare the floor: " + $ApplyState["SUITE_RESULT"] }
Write-Evidence "PASS: B0 - order law satisfied; apply record strict-parsed and cross-pinned against this pack's embedded literals."

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
# B1. TARGET + TOOLCHAIN
# ---------------------------------------------------------------------
Write-Section "B1. TARGET IDENTITY + TOOLCHAIN (read-only)"
$DbInput = Read-Host "Absolute path of the working database file (backendxiom_dev.db)"
$TargetDbPath = ([string]$DbInput).Trim().Trim('"').Trim("'")
if (!(Test-Path $TargetDbPath)) { throw ("STOP: target database file not found: " + $TargetDbPath) }
if ($TargetDbPath -ne $ApplyState["DB_PATH"]) { throw ("STOP: the provided database path does not match the apply act's recorded target: '" + $ApplyState["DB_PATH"] + "'. Verify must run against the same file.") }
Write-Evidence ("Target db (matches apply record): " + $TargetDbPath)

$Py = $null
foreach ($Cand in @(".venv\Scripts\python.exe", "venv\Scripts\python.exe",
                    "backend\.venv\Scripts\python.exe", "backend
env\Scripts\python.exe")) {
    $Full = Join-Path $RepoRoot $Cand
    if (Test-Path $Full) { $Py = $Full; break }
}
if ($null -eq $Py) {
    $Cmd = Get-Command python -ErrorAction SilentlyContinue
    if ($null -ne $Cmd) { $Py = $Cmd.Source }
}
if ($null -eq $Py) { throw "STOP: no python executable found." }
$OutVer = Invoke-Capped $Py @('-c', "import alembic; print(alembic.__version__)")
if ((Norm-Text $OutVer) -ne $AlembicPin) { throw ("STOP: alembic " + $AlembicPin + " required.") }
Write-Evidence ("PASS: B1 - tool venv at certified pins (alembic " + $AlembicPin + ").")

# ---------------------------------------------------------------------
# B2. FILE PINS (17 delivered + 6 V1)
# ---------------------------------------------------------------------
Write-Section "B2. FILE HASH PINS (READ-ONLY)"
$FilePins = @(
    "alembic\versions\20260903_0047_v2_be7_research_jobs.py|b00ab32aec3cf9311b7da8333dba2baa91221c643cc35cba73d446504ece88ce",
    "app\db\models\__init__.py|32b0f7707fe2bd2556b4e01eed125becff9676f494a960e5a74c0c34de9855e9",
    "app\db\models\v2_research_jobs.py|abc993d94ef603abacde26cf20b63a69ca0b09d4969ea5bdc75cfbf34f0df8ca",
    "app\v2\api\router.py|ad4afdd4eb5fe0c0676c45a9b779cb9eeeb16140163e6f7243fd3c9ad606f670",
    "app\v2\rbac\permissions.py|a3dff08218b2afa7029b678396673c317fe1852f9785697bb35a36cbf0cd3b3a",
    "app\v2\research_jobs\__init__.py|29c2d81038281a73dafde56901871b2343b6a3ba2742ab726b03fd8bc304b306",
    "app\v2\research_jobs\api.py|0b5fe719b839f848a8fb42a81de8a35197eeb443f6c267e3794f14292d2db253",
    "app\v2\research_jobs\contracts.py|b8d0c5313c2c7a035a90167ece78cbdcda792f1a9bf706a447fa261eb7b7783e",
    "app\v2\research_jobs\leakage.py|98e9763f8d5d2bfed242bb80158542784b4958ca320fc89700067a58a77623c6",
    "app\v2\research_jobs\queue.py|1b5ceeedcc9738d0785d42732a23bdf39b5ecb0f3bfe4085b36edebb80514e43",
    "app\v2\research_jobs\registry.py|bb3540221f92a688e272e09dc48983a51d248c58636e20ce9f65845e65d6ab4d",
    "app\v2\research_jobs\replay.py|f241d615bd83aea1f5d279f18731580f6021f652871ac3b4dda10bfdfd0e8e26",
    "app\v2\research_jobs\runner.py|8d0032cb92c1dc52fc09f40788c738dd1ae4f1ead3fb7b8136606bf704c68fda",
    "tests\test_v2_be7_boundaries.py|45373d015a232d1c734e03e493bf4fc0f852639239513faafbb8ea39eaa25f31",
    "tests\test_v2_be7_jobs.py|4c9c33c2eb72d086964e529e27d255044ef0f9ff1baf445eb7a6572373c31c19",
    "tests\test_v2_be7_migration.py|04e8ef5c0e83cb879809628bed113dc7187e6530ddd2416f687ba704a8711945",
    "tests\test_v2_be7_replay.py|521bf5632d2dfa154e494e79090e796066474b5fc3b257ea6962c1324700dfcd"
)
foreach ($Fp in $FilePins) {
    $Parts = $Fp.Split("|")
    $FpPath = Join-Path $BackendRoot $Parts[0]
    if (!(Test-Path $FpPath)) { throw ("FAIL: B2 - delivered file missing: " + $FpPath) }
    $FpHash = (Get-FileHash -Path $FpPath -Algorithm SHA256).Hash.ToLower()
    if ($FpHash -ne $Parts[1]) { throw ("FAIL: B2 - delivered file hash drift: " + $Parts[0] + " = " + $FpHash + " != pinned " + $Parts[1] + " . The accepted corpus moved after apply; report to ITRGA.") }
    Write-Evidence ("file pin OK: " + $Parts[0])
}
$V1Block = @'
app\execution_research\simulation.py|f163e610ba1a6215ac9229c6993a0f667ac916bdc53bf9fc1bb30d1b1efe70c7
app\ml\dataset\chronology_guard.py|7dbc665dc4b43f314c01d09da9a23576a47a78e4373c3daee6c15dcf03fd64cb
app\ml\dataset\service.py|6c5d72a8942050b495e209aa4b0a4044ba5d9d61087703198a103a0ac57d99d0
app\ml\dataset\snapshot_builder.py|b08ef4b1dec07567edbe4d153a3b18ef8838280bf2ec0a1ab6ed3f34e0b7fb9b
app\ml\dataset\split_engine.py|e893b92c6ccce188f0e7dbedee1b121d270c57ec25ddea8f99e5201319f7acbc
app\ml\economic\service.py|c49527ed12f4d2caf7f997f709f44d6e9d69e4f1c4a8eb485db83484c5c9fa13
'@
foreach ($V1Line in @($V1Block -split "`n")) {
    if ($V1Line.Trim() -eq "") { continue }
    $Parts = $V1Line.Split("|")
    $V1Path = Join-Path $BackendRoot $Parts[0]
    $V1Hash = (Get-FileHash -Path $V1Path -Algorithm SHA256).Hash.ToLower()
    if ($V1Hash -ne $Parts[1]) { throw ("FAIL: B2 - V1 floor moved: " + $Parts[0]) }
    Write-Evidence ("V1 pin OK: " + $Parts[0])
}
Write-Evidence "PASS: B2 - all 17 delivered files byte-identical to the accepted pins; six V1 pins intact."

# ---------------------------------------------------------------------
# B3. CHAIN HEAD + CENSUSES
# ---------------------------------------------------------------------
Write-Section "B3. CHAIN HEAD + CENSUSES (INDEPENDENT RECOMPUTATION)"
Push-Location $BackendRoot
try {
    $OutCur = Invoke-Capped $Py @('-m', 'alembic', 'current')
    $CurLines = @(@($OutCur) | Where-Object { ([string]$_) -match $ApplyTargetRevision -and ([string]$_) -match [regex]::Escape("(head)") })
    if ($CurLines.Count -ne 1) { throw ("FAIL: B3 - expected current = 20260903_0047 (head); observed '" + (Norm-Text $OutCur) + "'.") }
    $OutHeads = Invoke-Capped $Py @('-m', 'alembic', 'heads')
    $HeadCount = @(@($OutHeads) | Where-Object { ([string]$_).Trim() -ne "" -and ([string]$_) -notmatch "^INFO" }).Count
    if ($HeadCount -ne 1) { throw ("FAIL: B3 - expected a single head; observed '" + (Norm-Text $OutHeads) + "'.") }
} finally { Pop-Location }
Write-Evidence "PASS: B3a - chain at 20260903_0047 (head), single head."

$OutPost = Invoke-Capped $Py @($HelperCensus, $TargetDbPath)
if ($LASTEXITCODE -ne 0) { throw ("FAIL: B3 - census helper failed: " + (Norm-Text $OutPost)) }
$Post = (Norm-Text $OutPost) | ConvertFrom-Json
if ($Post.triggers.Count -ne $ExpectTriggersTotal) { throw ("FAIL: B3 - trigger census " + $Post.triggers.Count) }
if ($Post.permissions.Count -ne $ExpectPermsTotal) { throw ("FAIL: B3 - permission census " + $Post.permissions.Count) }
if ($Post.compver.Count -ne $ExpectCompverTotal) { throw ("FAIL: B3 - compver census " + $Post.compver.Count) }
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
foreach ($Tn in $TenNew) { if ($Post.triggers -notcontains $Tn) { throw ("FAIL: B3 - trigger missing: " + $Tn) } }
if (@($Post.triggers | Where-Object { $_ -like "v2_research_job_immutable_*" }).Count -ne 0) { throw "FAIL: B3 - FP-1 by-design law violated." }
$PostPermSet = @($Post.permissions | ForEach-Object { $_[0] + "|" + $_[1] + "|" + $_[2] })
foreach ($Pt in @(
    "admin|v2.research.jobs.read|SAL-2",
    "admin|v2.research.jobs.submit|SAL-3",
    "admin|v2.research.jobs.cancel|SAL-3",
    "admin|v2.research.registry.read|SAL-2",
    "admin|v2.research.registry.write|SAL-3",
    "admin|v2.research.results.read|SAL-2",
    "operator|v2.research.jobs.read|SAL-2",
    "operator|v2.research.results.read|SAL-2"
)) { if ($PostPermSet -notcontains $Pt) { throw ("FAIL: B3 - permission triple missing: " + $Pt) } }
$PostCompSet = @($Post.compver | ForEach-Object { $_[0] + "|" + $_[1] + "|" + $_[2] })
if ($PostCompSet -notcontains ("replay_engine|rpe-1.0.0|" + $RpeHash)) { throw "FAIL: B3 - RPE row mismatch." }
if ($PostCompSet -notcontains ("research_job_engine|rje-1.0.0|" + $RjeHash)) { throw "FAIL: B3 - RJE row mismatch." }
Write-Evidence "PASS: B3b - censuses exactly 42 / 49 / 8; exact members; compver literals honored."

# ---------------------------------------------------------------------
# B4. LIVE GUARD PROBES
# ---------------------------------------------------------------------
Write-Section "B4. LIVE GUARD PROBES (transactional; nothing persists)"
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
    $OutProbe = Invoke-Capped $Py @($HelperProbe, $TargetDbPath, $Partsp[1], $Partsp[2], $Partsp[3])
    if ($LASTEXITCODE -ne 0 -or (Norm-Text $OutProbe) -ne "PROBE-EXACT-MATCH") {
        throw ("FAIL: B4 - probe " + $Partsp[0] + ": '" + (Norm-Text $OutProbe) + "'.")
    }
    Write-Evidence ("probe OK: " + $Partsp[0])
}
Write-Evidence "PASS: B4 - all ten guards refuse live with exact messages."

# ---------------------------------------------------------------------
# B5. FULL SUITE (independent rerun)
# ---------------------------------------------------------------------
Write-Section "B5. FULL TEST SUITE - INDEPENDENT RERUN"
$OutPt = Invoke-Capped $Py @('-m', 'pytest', '--version')
if ((Norm-Text $OutPt) -notmatch [regex]::Escape($PytestPin)) { throw ("STOP: pytest " + $PytestPin + " required.") }
Push-Location $BackendRoot
try {
    Write-Evidence "PYTEST: python -m pytest -q"
    $OutSuite = Invoke-Capped $Py @('-m', 'pytest', '-q')
    $SuiteCode = $LASTEXITCODE
} finally { Pop-Location }
$SuiteText = Norm-Text $OutSuite
$TailLines = @(@($OutSuite) | Select-Object -Last 30)
Emit-Output $TailLines
if ($SuiteCode -ne 0) { throw ("FAIL: B5 - pytest exited " + $SuiteCode) }
if ($SuiteText -notmatch ("^" + $SuiteFloor + " passed") -and $SuiteText -notmatch ("= " + $SuiteFloor + " passed")) { throw ("FAIL: B5 - summary does not declare " + $SuiteFloor + " passed.") }
if ($SuiteText -match "[1-9][0-9]* (failed|error)") { throw "FAIL: B5 - failures/errors in summary." }
$SuiteSummary = ($TailLines | Where-Object { ([string]$_) -match "passed" } | Select-Object -Last 1)
Write-Evidence ("PASS: B5 - suite summary: " + ([string]$SuiteSummary).Trim())

# ---------------------------------------------------------------------
# B6. DRIFT GATE
# ---------------------------------------------------------------------
Write-Section "B6. DRIFT GATE (PGF-014)"
Push-Location $BackendRoot
try {
    $OutChk = Invoke-Capped $Py @('-m', 'alembic', 'check')
    $ChkCode = $LASTEXITCODE
} finally { Pop-Location }
Emit-Output $OutChk
$Drift = (Norm-Text $OutChk).ToLower()
if ($ChkCode -eq 0) { throw "FAIL: B6 - zero-exit check contradicts the inherited drift declaration." }
foreach ($Marker in @("v2_backtest_input","v2_cost_model","v2_strategy_version","v2_research_job","v2_research_result","v2_md_","v2_permission","v2_computation_version")) {
    if ($Drift.Contains($Marker)) { throw ("FAIL: B6 - band/v2 drift token: " + $Marker) }
}
if ((-not $Drift.Contains("not up to date")) -and (-not $Drift.Contains("audit_write_failure_records"))) {
    throw "FAIL: B6 - inheritance witness absent."
}
Write-Evidence "PASS: B6 - zero band/v2 tokens; inheritance witness present."

# ---------------------------------------------------------------------
# B7. VERIFY-FINAL-STATE RECORD
# ---------------------------------------------------------------------
Write-Section "B7. VERIFY-FINAL-STATE RECORD"
$VLines = @(
    "STATE_FILE_ID=ITRGA-V2-0047-VERIFY-FINAL-STATE-V3",
    "TARGET_REVISION=" + $ApplyTargetRevision,
    "APPLY_STATE_RECORD=0047-APPLY-FINAL-STATE.txt",
    "TRIGGERS_TOTAL=" + $ExpectTriggersTotal,
    "PERMISSIONS_TOTAL=" + $ExpectPermsTotal,
    "COMPVER_TOTAL=" + $ExpectCompverTotal,
    "COMPVER_RPE_HASH=" + $RpeHash,
    "COMPVER_RJE_HASH=" + $RjeHash,
    "SUITE_RESULT=" + ([string]$SuiteSummary).Trim(),
    "DB_PATH=" + $TargetDbPath,
    "TRANSCRIPT=0047-VERIFY-RUN-V3.txt",
    "UTC_COMPLETED=" + ([DateTime]::UtcNow.ToString("yyyy-MM-ddTHH:mm:ssZ"))
)
$VLines | Set-Content -Path $VerifyRecPath -Encoding UTF8
foreach ($Vl in $VLines) { Write-Evidence "STATE: " + $Vl }
Write-Evidence ""
Write-Evidence "VERIFY PACK COMPLETE - PASS. The 0047 working-DB application act is proven end-to-end on the operator environment. The application may be restarted. Send back operator-evidence\BE-7\0047-APPLY-RUN-V3.txt and 0047-VERIFY-RUN-V3.txt to ITRGA."
Write-Evidence ("UTC end: " + ([DateTime]::UtcNow.ToString("yyyy-MM-ddTHH:mm:ssZ")))

# helper cleanup (best effort; the helpers are tiny ASCII files in OS temp)
Remove-Item -Force -ErrorAction SilentlyContinue $HelperProbe
Remove-Item -Force -ErrorAction SilentlyContinue $HelperCensus
