# =====================================================================
# AXIOM V2 - 0048 WORKING-DATABASE APPLICATION ACT (BAND BE-8)
# ITRGA SQLITE VERIFY ACT EVIDENCE PACK (V1)
# Pack ID: ITRGA-V2-0048-VERIFY-PACK-V1
# SUPERSESSION RECORD (VERIFY EDITION 3, 2026-09-05 supersedes VERIFY ed-2):
#   VERIFY ed-2 (37,706 B, MD5 D1E71697119887ACC1D934FCFC1F8091) RETIRED. Cause: twin of
#   the APPLY A6 defect in its B3 census block ($ExpectTriggers/$ExpectPerms/$ExpectCompver
#   vs declared $Expect*Total) - crashed field run 08:37Z after B0/B1/B2 PASSes. Field
#   adjudication + transcript-erosion finding in ITRGA-ISS-V2-0048-PACKS-006. ed-3 differs
#   ONLY in the three B3 identifier names and these header lines.
# SUPERSESSION RECORD (VERIFY EDITION 2, 2026-09-05 supersedes VERIFY ed-1):
#   VERIFY ed-1 (37,223 B, MD5 F30B63D52087D566D5FF13E736972018) RETIRED. Cause: the
#   shared transcript-template defect above (ITRGA-ISS-V2-0048-PACKS-005). One-line fix:
#   transcript now 0048-VERIFY-RUN-V1.txt. Every gate, pin, parser and contract byte
#   (incl. the 15-key apply-record contract) is unchanged from the operator-verified
#   ed-1 bytes; the pack remains a PURE READ on the database.
# Authority: ITRGA-ACC-V2-BE-8-INT-001; ITRGA-RULE-V2-BE8-HALT-0048-001;
#   pattern ITRGA-V2-0047-VERIFY-PACK-V5 ed-3 (all PGF lessons by
#   construction; independent re-proof: this pack trusts NOTHING it did
#   not recompute on this run - the apply-final-state record is
#   strict-parsed and cross-checked against this pack's embedded ACC
#   literals AND against a live recomputation of every census, file
#   hash, and gate).
#
# WHAT THIS PACK DOES (READ-ONLY on the database and the tree; writes
#   only its own transcript and the verify-final-state record in
#   operator-evidence\BE-8, plus throwaway helpers removed on exit):
#   - Requires the apply-final-state record (strict KEY=VALUE parse;
#     exact 15-key set; identity pin) - verify cannot precede apply.
#   - Refuses to start if 0048-VERIFY-FINAL-STATE.txt already exists
#     (completed-run law).
#   - Re-hashes the 20-file corpus and the six V1 files against pins.
#   - Re-proves the terminal state: chain head 20260904_0048 (single);
#     censuses 58 / 57 / 10 with exact members; compver PXS/PRG rows
#     equal to the embedded literals AND to a live on-box rolling-hash
#     recomputation; 8 paper tables present; compver delete-guard == 1;
#     six live guard probes with exact messages (transactional
#     insert-probe-rollback; nothing persists); full test suite
#     1026 passed / 0 failed; drift gate (non-zero exit, zero BE-8
#     tokens, inheritance witness).
#   - Never mutates the database (PRE == POST sha256 attested inside);
#     never runs any Git command; asks only for the database file path.
#
# BEFORE RUNNING: the application must still be STOPPED (start it only
#   after this pack PASSes).
# RUN MODE: as a file from the repository root, ONLY after
#   ITRGA_V2_0048_APPLY_PACK_V1.ps1 has PASSed:
#     powershell -NoProfile -ExecutionPolicy Bypass -File ".\ITRGA_V2_0048_VERIFY_PACK_V1.ps1"
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
$EvidenceDir   = Join-Path $RepoRoot "operator-evidence\BE-8"
$Transcript    = Join-Path $EvidenceDir "0048-VERIFY-RUN-V1.txt"
$ApplyRecPath  = Join-Path $EvidenceDir "0048-APPLY-FINAL-STATE.txt"
$VerifyRecPath = Join-Path $EvidenceDir "0048-VERIFY-FINAL-STATE.txt"
$AnchorPath    = Join-Path $EvidenceDir "0048-ANCHOR-axiom_dev.bak"
$PinsPath      = Join-Path $RepoRoot "ITRGA_V2_0048_BASELINE_PINS.txt"
$HelperProbe   = Join-Path $env:TEMP "be8_0048_guardprobe.py"
$HelperCensus  = Join-Path $env:TEMP "be8_0048_census.py"
$HelperRoll    = Join-Path $env:TEMP "be8_0048_rollhash.py"
$HelperPost    = Join-Path $env:TEMP "be8_0048_poststate.py"

$ApplyTargetRevision = "20260904_0048"
$BaselineRevision    = "20260903_0047"
$SealedDbSha         = "27bda3112e53baf426604532da4d5f44ef0c4d089c0f002e08d0ab9b740c776f"
$ExpectFloorTriggers = 42
$ExpectFloorPerms    = 49
$ExpectFloorCompver  = 8
$ExpectTriggersTotal = 58
$ExpectPermsTotal    = 57
$ExpectCompverTotal  = 10
$SuiteFloor          = 1026
$AlembicPin          = "1.19.0"
$PytestPin           = "8.4.2"
$RpeHash             = "1499343d48b778af17065e8bf1eaabcffc116880fa6967ab442db1255992b178"
$RjeHash             = "8f107d174e081dc0a1527fea841b89dfb73744e3f16eba2d29c60521158c0598"
$PxsHash             = "c58a06a5402f30a3828012f91b4aeb564008a9bfa34685cc57558e1003d106c0"
$PrgHash             = "ed6434fa5ff00b937b71e1d76a8fef32bc019f134e56831ac9f74af525376b1b"
$FilePinsAfter = @(
    "app\v2\paper_trading\__init__.py|d0a090fe31cad5e36012b939987b9f3ae627f5d363ff34a3ee76d8f0b48c9911",
    "app\v2\paper_trading\contracts.py|c90e6e5828811a4699dabbb538183a55534306604020a11e96771cd79589b502",
    "app\v2\paper_trading\accounts.py|0e54f4c2c38d66a4d386d34574fc9625f9cc4d045fc92f814a1167e3a40b40ef",
    "app\v2\paper_trading\orders.py|af1ad32afc6953116a4b06289f3886dfd69442d6b2cbcd8f583b1bbdcfe87582",
    "app\v2\paper_trading\risk.py|ea4abf270da2cea46cc66a3bbff32ce1bdae70b9a4b4ddbb25e73bb082375717",
    "app\v2\paper_trading\simulator.py|4fb0d5586232f73ccbdff29c2a18d35b8d5670d8a4c9d5d4b9cc48c44162a804",
    "app\v2\paper_trading\ledger.py|7a901f8145b40aaaa80d3ef9c6c466be24ab55c7d290ede8887956dc86677138",
    "app\v2\paper_trading\reconciliation.py|74d7e70f89be1822d6ea2dce91920f471c7a0b5a43ea4b7c5d9524f48c044deb",
    "app\v2\paper_trading\api.py|1e4064e367cfd7340038388503dd90710c70a32cf386b568d0504097cc96b3be",
    "app\db\models\v2_paper_trading.py|61ccb99966106cdf85485dfdfc9fed276512501553af59c9a4e6ddb02d73b56c",
    "alembic\versions\20260904_0048_v2_be8_paper_trading.py|2cb83b3d102598523834b867aa780bb659df3366a8775c65cc0750740dc398c2",
    "tests\test_v2_be8_simulator.py|129c3d32f05945da5e55c33b6f020c3d4bebb8227d8baca07de3c47da2ae7f61",
    "tests\test_v2_be8_migration.py|bd3227587bd913d5bead7c8958ff3fb6bd18b077ca1b5975f0ae806e0ab019b1",
    "tests\test_v2_be8_orders.py|46c9cee65ca01033849f4b4176b3ae270673a25e9fa6151850533264920f1b01",
    "tests\test_v2_be8_boundaries.py|a42a19f803385fe6829e9623e97878935fbe89add3670f20a37282364e72a99e",
    "app\v2\mode\contract.py|3346e0eee27d6f13a2d6d02e2df06089879c563789a113cf0bf014223c040b59",
    "app\v2\rbac\permissions.py|064019ca495328e2f1c00e9735f6c97f3e786cadcccb52b673a353bed5c5a99b",
    "app\v2\api\router.py|530f91ec709b1d66c5c5cb7e339af5714d581f57169cb5b4566d0c9c45aafecd",
    "app\db\models\__init__.py|0b188cbf69fb984bb076648eba17c2408d42a5fb29462b6d4ff1ff853f1c6e68",
    "tests\test_v2_mode.py|19020e26a80ee7453abd34d88273d7e586c81b4bb075a9729a5016326e687ec4"
)

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
function Find-Python {
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
    if ($null -eq $Py) { throw "STOP: no python executable found." }
    return $Py
}
$PinKeyList = @(
    "PINS_FILE_ID","TARGET_REVISION","BASELINE_REVISION","DB_SHA256_SEALED",
    "V2_TRIGGERS_FLOOR","PERMISSIONS_FLOOR","COMPVER_FLOOR",
    "V2_TRIGGERS_AFTER","PERMISSIONS_AFTER","COMPVER_AFTER",
    "COMPVER_RPE_HASH","COMPVER_RJE_HASH","COMPVER_PXS_HASH","COMPVER_PRG_HASH",
    "SUITE_FLOOR","ALEMBIC_PIN","PYTEST_PIN")
function Check-Pins {
    $Pins = Read-Pins -Path $PinsPath -ExpectedKeys $PinKeyList -Label "baseline pins"
    if ($Pins["PINS_FILE_ID"] -ne "ITRGA-V2-0048-BASELINE-PINS-V1") { throw "STOP: pin file identity mismatch." }
    if ($Pins["TARGET_REVISION"] -ne $ApplyTargetRevision) { throw "STOP: TARGET_REVISION pin mismatch." }
    if ($Pins["BASELINE_REVISION"] -ne $BaselineRevision) { throw "STOP: BASELINE_REVISION pin mismatch." }
    if ($Pins["DB_SHA256_SEALED"] -ne $SealedDbSha) { throw "STOP: sealed working-lineage identity pin mismatch." }
    if ([int]$Pins["V2_TRIGGERS_FLOOR"] -ne $ExpectFloorTriggers) { throw "STOP: trigger floor pin mismatch." }
    if ([int]$Pins["PERMISSIONS_FLOOR"] -ne $ExpectFloorPerms) { throw "STOP: permission floor pin mismatch." }
    if ([int]$Pins["COMPVER_FLOOR"] -ne $ExpectFloorCompver) { throw "STOP: compver floor pin mismatch." }
    if ([int]$Pins["V2_TRIGGERS_AFTER"] -ne $ExpectTriggersTotal) { throw "STOP: trigger-total pin mismatch." }
    if ([int]$Pins["PERMISSIONS_AFTER"] -ne $ExpectPermsTotal) { throw "STOP: permission-total pin mismatch." }
    if ([int]$Pins["COMPVER_AFTER"] -ne $ExpectCompverTotal) { throw "STOP: compver-total pin mismatch." }
    if ($Pins["COMPVER_RPE_HASH"] -ne $RpeHash) { throw "STOP: RPE pin mismatch." }
    if ($Pins["COMPVER_RJE_HASH"] -ne $RjeHash) { throw "STOP: RJE pin mismatch." }
    if ($Pins["COMPVER_PXS_HASH"] -ne $PxsHash) { throw "STOP: PXS pin mismatch." }
    if ($Pins["COMPVER_PRG_HASH"] -ne $PrgHash) { throw "STOP: PRG pin mismatch." }
    if ([int]$Pins["SUITE_FLOOR"] -ne $SuiteFloor) { throw "STOP: suite-floor pin mismatch." }
    if ($Pins["ALEMBIC_PIN"] -ne $AlembicPin) { throw "STOP: alembic pin mismatch." }
    if ($Pins["PYTEST_PIN"] -ne $PytestPin) { throw "STOP: pytest pin mismatch." }
    return $Pins
}
function Write-Helpers {
    $ProbeB64 = @'
aW1wb3J0IHNxbGl0ZTMsIHN5cwojIElUUkdBIDAwNDggaW5zdHJ1bWVudCBoZWxwZXIgLSBndWFyZHB
yb2JlIDxkYj4gPGluc2VydF9zcWw+IDxwcm9iZV9zcWw+IDxleHBlY3RlZD4KIyBUcmFuc2FjdGlvbm
FsIHByb2JlOiBpbnNlcnQgdGhyb3dhd2F5IHJvdywgcnVuIHByb2JlLCByZXF1aXJlIEVYQUNUIG1lc
3NhZ2UsIHJvbGxiYWNrLgpkYiwgaW5zZXJ0X3NxbCwgcHJvYmVfc3FsLCBleHBlY3RlZCA9IHN5cy5h
cmd2WzFdLCBzeXMuYXJndlsyXSwgc3lzLmFyZ3ZbM10sIHN5cy5hcmd2WzRdCmNvbm4gPSBzcWxpdGU
zLmNvbm5lY3QoZGIpCnRyeToKICAgIGN1ciA9IGNvbm4uY3Vyc29yKCkKICAgIGN1ci5leGVjdXRlKG
luc2VydF9zcWwpCiAgICB0cnk6CiAgICAgICAgY3VyLmV4ZWN1dGUocHJvYmVfc3FsKQogICAgZXhjZ
XB0IHNxbGl0ZTMuRGF0YWJhc2VFcnJvciBhcyBleGM6CiAgICAgICAgZ290ID0gc3RyKGV4YykKICAg
ICAgICBjb25uLnJvbGxiYWNrKCkKICAgICAgICBpZiBnb3QgPT0gZXhwZWN0ZWQ6CiAgICAgICAgICA
gIHByaW50KCJQUk9CRS1FWEFDVC1NQVRDSCIpCiAgICAgICAgICAgIHN5cy5leGl0KDApCiAgICAgIC
AgcHJpbnQoIlBST0JFLU1FU1NBR0UtTUlTTUFUQ0ggOjoiICsgZ290KQogICAgICAgIHN5cy5leGl0K
DIpCiAgICBjb25uLnJvbGxiYWNrKCkKICAgIHByaW50KCJQUk9CRS1OT1QtUkVGVVNFRCIpCiAgICBz
eXMuZXhpdCgxKQpmaW5hbGx5OgogICAgY29ubi5jbG9zZSgpCg==
'@
    [IO.File]::WriteAllBytes($HelperProbe, (B64-Decode -B64Chunk $ProbeB64))
    $CensusB64 = @'
aW1wb3J0IHNxbGl0ZTMsIHN5cywganNvbgojIElUUkdBIDAwNDggaW5zdHJ1bWVudCBoZWxwZXIgLSB
jZW5zdXMgPGRiPgojIEVtaXRzIG9uZSBKU09OIGxpbmUgd2l0aCB0aGUgdGhyZWUgY2Vuc3VzIHRvdG
FscyBhbmQgdGhlIHBpY2tlZCBtZW1iZXJzLgpkYiA9IHN5cy5hcmd2WzFdCmNvbm4gPSBzcWxpdGUzL
mNvbm5lY3QoZGIpCnRyeToKICAgIGN1ciA9IGNvbm4uY3Vyc29yKCkKICAgIHRyaWdzID0gW3JbMF0g
Zm9yIHIgaW4gY3VyLmV4ZWN1dGUoIlNFTEVDVCBuYW1lIEZST00gc3FsaXRlX21hc3RlciBXSEVSRSB
0eXBlPSd0cmlnZ2VyJyBBTkQgbmFtZSBMSUtFICd2Ml8lJyBPUkRFUiBCWSBuYW1lIildCiAgICBwZX
JtcyA9IFt0dXBsZShyKSBmb3IgciBpbiBjdXIuZXhlY3V0ZSgiU0VMRUNUIHJvbGUsIHBlcm1pc3Npb
24sIHNhbCBGUk9NIHYyX3Blcm1pc3Npb24gT1JERVIgQlkgcm9sZSwgcGVybWlzc2lvbiIpXQogICAg
Y29tcCA9IFt0dXBsZShyKSBmb3IgciBpbiBjdXIuZXhlY3V0ZSgiU0VMRUNUIGNvbXBvbmVudCwgdmV
yc2lvbiwgc291cmNlX2hhc2ggRlJPTSB2Ml9jb21wdXRhdGlvbl92ZXJzaW9uIE9SREVSIEJZIGNvbX
BvbmVudCwgdmVyc2lvbiIpXQogICAgcHJpbnQoanNvbi5kdW1wcyh7InRyaWdnZXJzIjogdHJpZ3MsI
CJwZXJtaXNzaW9ucyI6IHBlcm1zLCAiY29tcHZlciI6IGNvbXB9KSkKZmluYWxseToKICAgIGNvbm4u
Y2xvc2UoKQo=
'@
    [IO.File]::WriteAllBytes($HelperCensus, (B64-Decode -B64Chunk $CensusB64))
    $RollB64 = @'
aW1wb3J0IGhhc2hsaWIsIHN5cwojIElUUkdBIDAwNDggaW5zdHJ1bWVudCBoZWxwZXIgLSByb2xsaGF
zaCA8YmFja2VuZF9yb290PiA8cHhzfHByZz4KIyBSZWNvbXB1dGVzIHRoZSBtaWdyYXRpb24ncyByb2
xsaW5nIGNvbnRlbnQgaGFzaCBmcm9tIGxpdmUgZmlsZXMuClNFVFMgPSB7CiAgICAicHhzIjogKCJhc
HAvdjIvcGFwZXJfdHJhZGluZy9zaW11bGF0b3IucHkiLCAiYXBwL3YyL3BhcGVyX3RyYWRpbmcvbGVk
Z2VyLnB5IiksCiAgICAicHJnIjogKCJhcHAvdjIvcGFwZXJfdHJhZGluZy9yaXNrLnB5IiwgImFwcC9
2Mi9wYXBlcl90cmFkaW5nL2NvbnRyYWN0cy5weSIpLAp9CnJvb3QsIG1vZGUgPSBzeXMuYXJndlsxXS
wgc3lzLmFyZ3ZbMl0KZGlnZXN0ID0gaGFzaGxpYi5zaGEyNTYoKQpmb3IgcmVsIGluIFNFVFNbbW9kZ
V06CiAgICBkaWdlc3QudXBkYXRlKHJlbC5lbmNvZGUoInV0Zi04IikpCiAgICBkaWdlc3QudXBkYXRl
KGIiXHgwMCIpCiAgICB3aXRoIG9wZW4ocm9vdC5yc3RyaXAoIi9cXCIpICsgIi8iICsgcmVsLCAicmI
iKSBhcyBmaDoKICAgICAgICBkaWdlc3QudXBkYXRlKGZoLnJlYWQoKSkKICAgIGRpZ2VzdC51cGRhdG
UoYiJceDAwIikKcHJpbnQoZGlnZXN0LmhleGRpZ2VzdCgpKQo=
'@
    [IO.File]::WriteAllBytes($HelperRoll, (B64-Decode -B64Chunk $RollB64))
    $PostB64 = @'
aW1wb3J0IHNxbGl0ZTMsIHN5cywganNvbgojIElUUkdBIDAwNDggaW5zdHJ1bWVudCBoZWxwZXIgLSB
wb3N0c3RhdGUgPGRiPgojIEVtaXRzIG9uZSBKU09OIGxpbmU6IHBhcGVyIHRhYmxlcywgYWxlbWJpY1
92ZXJzaW9uIHJvd3MsIGNvbXB2ZXIgZGVsZXRlLWd1YXJkIGNvdW50LgpkYiA9IHN5cy5hcmd2WzFdC
mNvbm4gPSBzcWxpdGUzLmNvbm5lY3QoZGIpCnRyeToKICAgIGN1ciA9IGNvbm4uY3Vyc29yKCkKICAg
IHRhYmxlcyA9IFtyWzBdIGZvciByIGluIGN1ci5leGVjdXRlKAogICAgICAgICJTRUxFQ1QgbmFtZSB
GUk9NIHNxbGl0ZV9tYXN0ZXIgV0hFUkUgdHlwZT0ndGFibGUnIEFORCBuYW1lIExJS0UgJ3YyX3BhcG
VyXyUnIE9SREVSIEJZIG5hbWUiKV0KICAgIHJldnMgPSBbclswXSBmb3IgciBpbiBjdXIuZXhlY3V0Z
SgiU0VMRUNUIHZlcnNpb25fbnVtIEZST00gYWxlbWJpY192ZXJzaW9uIE9SREVSIEJZIHZlcnNpb25f
bnVtIildCiAgICBndWFyZCA9IGN1ci5leGVjdXRlKCJTRUxFQ1QgQ09VTlQoKikgRlJPTSBzcWxpdGV
fbWFzdGVyIFdIRVJFIHR5cGU9J3RyaWdnZXInIEFORCBuYW1lPSd2Ml9jb21wdXRhdGlvbl92ZXJzaW
9uX2ltbXV0YWJsZV9kZWxldGUnIikuZmV0Y2hvbmUoKVswXQogICAgcHJpbnQoanNvbi5kdW1wcyh7I
nBhcGVyX3RhYmxlcyI6IHRhYmxlcywgImFsZW1iaWNfdmVyc2lvbiI6IHJldnMsICJjb21wdmVyX2Rl
bGV0ZV9ndWFyZCI6IGd1YXJkfSkpCmZpbmFsbHk6CiAgICBjb25uLmNsb3NlKCkK
'@
    [IO.File]::WriteAllBytes($HelperPost, (B64-Decode -B64Chunk $PostB64))
}
function Remove-Helpers {
    Remove-Item -Force -ErrorAction SilentlyContinue $HelperProbe
    Remove-Item -Force -ErrorAction SilentlyContinue $HelperCensus
    Remove-Item -Force -ErrorAction SilentlyContinue $HelperRoll
    Remove-Item -Force -ErrorAction SilentlyContinue $HelperPost
}
function Sweep-Authority {
    foreach ($Av in @(Get-ChildItem env: | Where-Object { $_.Name -like "AXIOM_TD_*" })) {
        Remove-Item ("env:" + $Av.Name) -ErrorAction SilentlyContinue
    }
    if (@(Get-ChildItem env: | Where-Object { $_.Name -like "AXIOM_TD_*" }).Count -gt 0) { throw "STOP: an AXIOM_TD_* authority variable persists." }
}

Write-Section "0048 VERIFY PACK V1 - ITRGA-V2-0048-VERIFY-PACK-V1"
if (!(Test-Path $BackendRoot)) { throw ("STOP: backend directory not found: " + $BackendRoot + ". Run from the repository root.") }
if (!(Test-Path $PinsPath))    { throw ("STOP: baseline pin file missing at the repository root: " + $PinsPath) }
New-Item -ItemType Directory -Force -Path $EvidenceDir | Out-Null

# B0. ORDER, HYGIENE, AUTHORITY SWEEP, APPLY RECORD
if (Test-Path $VerifyRecPath) {
    throw ("STOP (E-0046-DUP law): a completed verify-final-state record already exists: " + $VerifyRecPath + " . Refusing to disturb it; report to ITRGA if you believe it is stale.")
}
Remove-Item -Force -ErrorAction SilentlyContinue $Transcript
Sweep-Authority
Write-Evidence ("UTC start: " + ([DateTime]::UtcNow.ToString("yyyy-MM-ddTHH:mm:ssZ")))
Write-Evidence "Independent re-proof of the 0048 apply act. PURE READ on the database; trusts nothing it did not recompute on this run."
$null = Check-Pins
Write-Helpers
if (!(Test-Path $ApplyRecPath)) { throw ("STOP: the apply-final-state record is missing: " + $ApplyRecPath + " . Verify cannot precede apply.") }
$RecLines = @(Get-Content -Path $ApplyRecPath -Encoding UTF8)
$Rec = @{}
foreach ($RawL in $RecLines) {
    $Ll = ([string]$RawL).TrimEnd()
    if ($Ll -eq "") { continue }
    if ($Ll -notmatch '^([A-Z0-9_]+)=(.*)$') { throw ("STOP: malformed apply record line: '" + $Ll + "'.") }
    if ($Rec.ContainsKey($Matches[1])) { throw "STOP: duplicate key in apply record." }
    $Rec[$Matches[1]] = $Matches[2]
}
$ExpRecKeys = @("ANCHOR_SHA256","COMPVER_PRG_HASH","COMPVER_PXS_HASH","COMPVER_RJE_HASH","COMPVER_RPE_HASH","COMPVER_TOTAL","DB_PATH","DB_SHA256_POST","PERMISSIONS_TOTAL","STATE_FILE_ID","SUITE_RESULT","TARGET_REVISION","TRANSCRIPT","TRIGGERS_TOTAL","UTC_COMPLETED")
$GotRecKeys = @($Rec.Keys | Sort-Object)
if (($GotRecKeys -join ",") -ne ($ExpRecKeys -join ",")) { throw ("STOP: apply record key set mismatch: [" + ($GotRecKeys -join ", ") + "].") }
if ($Rec["STATE_FILE_ID"] -ne "ITRGA-V2-0048-APPLY-FINAL-STATE-V1") { throw "STOP: apply record identity mismatch." }
if ($Rec["TARGET_REVISION"] -ne $ApplyTargetRevision) { throw "STOP: apply record revision mismatch." }
if ([int]$Rec["TRIGGERS_TOTAL"] -ne $ExpectTriggersTotal) { throw "STOP: record trigger total mismatch." }
if ([int]$Rec["PERMISSIONS_TOTAL"] -ne $ExpectPermsTotal) { throw "STOP: record permission total mismatch." }
if ([int]$Rec["COMPVER_TOTAL"] -ne $ExpectCompverTotal) { throw "STOP: record compver total mismatch." }
if ($Rec["COMPVER_RPE_HASH"] -ne $RpeHash) { throw "STOP: record RPE mismatch." }
if ($Rec["COMPVER_RJE_HASH"] -ne $RjeHash) { throw "STOP: record RJE mismatch." }
if ($Rec["COMPVER_PXS_HASH"] -ne $PxsHash) { throw "STOP: record PXS mismatch." }
if ($Rec["COMPVER_PRG_HASH"] -ne $PrgHash) { throw "STOP: record PRG mismatch." }
Write-Evidence "PASS: B0 - refuse-if-completed clear; apply record strict-parsed (15 keys) and cross-checked against embedded ACC literals."

# B1. TARGET + TOOLCHAIN + RECORD-CHAINED PATH + DB IDENTITY
Write-Section "B1. TARGET IDENTITY (record-chained) + TOOLCHAIN"
$DbInput = Read-Host "Absolute path of the working database file (backend\axiom_dev.db)"
$TargetDbPath = ([string]$DbInput).Trim().Trim('"').Trim("'")
if (!(Test-Path $TargetDbPath)) { throw ("STOP: target database file not found: " + $TargetDbPath) }
if ($Rec["DB_PATH"] -ne $TargetDbPath) { throw ("STOP: typed target " + $TargetDbPath + " != recorded mutated target " + $Rec["DB_PATH"] + " . STOP and report to ITRGA.") }
$Py = Find-Python
$OutVer = Invoke-Capped $Py @('-c', "import alembic; print(alembic.__version__)")
if ((Norm-Text $OutVer) -ne $AlembicPin) { throw ("STOP: alembic " + $AlembicPin + " required.") }
$DbShaVerifyPre = (Get-FileHash -Path $TargetDbPath -Algorithm SHA256).Hash.ToLower()
Write-Evidence ("DB sha256 at verify start: " + $DbShaVerifyPre)
if ($DbShaVerifyPre -ne $Rec["DB_SHA256_POST"]) { throw ("STOP: database identity drifted since the apply act: " + $DbShaVerifyPre + " != recorded " + $Rec["DB_SHA256_POST"] + " . STOP and report to ITRGA.") }
$DbFs = (Get-Item $TargetDbPath).FullName -replace "\\", "/"
$env:AXIOM_DATABASE_URL = ("sqlite+aiosqlite:///" + $DbFs)
Write-Evidence ("AXIOM_DATABASE_URL pinned explicit (standing rule): " + $env:AXIOM_DATABASE_URL)
Push-Location $BackendRoot
try {
    $OutCur = Invoke-Capped $Py @('-m', 'alembic', 'current')
    $CurLines = @(@($OutCur) | Where-Object { ([string]$_) -match $ApplyTargetRevision -and ([string]$_) -match [regex]::Escape("(head)") })
    if ($CurLines.Count -ne 1) { throw ("FAIL: B1 - expected current = " + $ApplyTargetRevision + " (head); observed '" + (Norm-Text $OutCur) + "'.") }
    $OutHeads = Invoke-Capped $Py @('-m', 'alembic', 'heads')
    $HeadLines = @(@($OutHeads) | Where-Object { ([string]$_).Trim() -ne "" -and ([string]$_) -notmatch "^INFO" })
    if ($HeadLines.Count -ne 1 -or (@($HeadLines | Where-Object { ([string]$_) -match $ApplyTargetRevision }).Count -ne 1)) { throw ("FAIL: B1 - single head " + $ApplyTargetRevision + " not observed.") }
} finally { Pop-Location }
Write-Evidence "PASS: B1 - target equals the recorded mutated database at the recorded identity; chain at 20260904_0048 (head), single head."

# B2. FILE PINS (20 corpus + 6 V1)
Write-Section "B2. FILE HASH PINS (READ-ONLY)"
$FilePins = @(
    "app\v2\paper_trading\__init__.py|d0a090fe31cad5e36012b939987b9f3ae627f5d363ff34a3ee76d8f0b48c9911",
    "app\v2\paper_trading\contracts.py|c90e6e5828811a4699dabbb538183a55534306604020a11e96771cd79589b502",
    "app\v2\paper_trading\accounts.py|0e54f4c2c38d66a4d386d34574fc9625f9cc4d045fc92f814a1167e3a40b40ef",
    "app\v2\paper_trading\orders.py|af1ad32afc6953116a4b06289f3886dfd69442d6b2cbcd8f583b1bbdcfe87582",
    "app\v2\paper_trading\risk.py|ea4abf270da2cea46cc66a3bbff32ce1bdae70b9a4b4ddbb25e73bb082375717",
    "app\v2\paper_trading\simulator.py|4fb0d5586232f73ccbdff29c2a18d35b8d5670d8a4c9d5d4b9cc48c44162a804",
    "app\v2\paper_trading\ledger.py|7a901f8145b40aaaa80d3ef9c6c466be24ab55c7d290ede8887956dc86677138",
    "app\v2\paper_trading\reconciliation.py|74d7e70f89be1822d6ea2dce91920f471c7a0b5a43ea4b7c5d9524f48c044deb",
    "app\v2\paper_trading\api.py|1e4064e367cfd7340038388503dd90710c70a32cf386b568d0504097cc96b3be",
    "app\db\models\v2_paper_trading.py|61ccb99966106cdf85485dfdfc9fed276512501553af59c9a4e6ddb02d73b56c",
    "alembic\versions\20260904_0048_v2_be8_paper_trading.py|2cb83b3d102598523834b867aa780bb659df3366a8775c65cc0750740dc398c2",
    "tests\test_v2_be8_simulator.py|129c3d32f05945da5e55c33b6f020c3d4bebb8227d8baca07de3c47da2ae7f61",
    "tests\test_v2_be8_migration.py|bd3227587bd913d5bead7c8958ff3fb6bd18b077ca1b5975f0ae806e0ab019b1",
    "tests\test_v2_be8_orders.py|46c9cee65ca01033849f4b4176b3ae270673a25e9fa6151850533264920f1b01",
    "tests\test_v2_be8_boundaries.py|a42a19f803385fe6829e9623e97878935fbe89add3670f20a37282364e72a99e",
    "app\v2\mode\contract.py|3346e0eee27d6f13a2d6d02e2df06089879c563789a113cf0bf014223c040b59",
    "app\v2\rbac\permissions.py|064019ca495328e2f1c00e9735f6c97f3e786cadcccb52b673a353bed5c5a99b",
    "app\v2\api\router.py|530f91ec709b1d66c5c5cb7e339af5714d581f57169cb5b4566d0c9c45aafecd",
    "app\db\models\__init__.py|0b188cbf69fb984bb076648eba17c2408d42a5fb29462b6d4ff1ff853f1c6e68",
    "tests\test_v2_mode.py|19020e26a80ee7453abd34d88273d7e586c81b4bb075a9729a5016326e687ec4"
)
foreach ($Fp in $FilePins) {
    $Parts = $Fp.Split("|")
    $FpPath = Join-Path $BackendRoot $Parts[0]
    if (!(Test-Path $FpPath)) { throw ("FAIL: delivered file missing: " + $FpPath) }
    $FpHash = (Get-FileHash -Path $FpPath -Algorithm SHA256).Hash.ToLower()
    if ($FpHash -ne $Parts[1]) { throw ("FAIL: delivered file hash drift: " + $Parts[0] + " = " + $FpHash + " != pinned " + $Parts[1] + " . The accepted corpus moved; report to ITRGA.") }
    Write-Evidence ("file pin OK: " + $Parts[0])
}
Write-Evidence "PASS: B2a - all 20 corpus files byte-identical to the ACC-pinned set."

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
Write-Evidence "PASS: B2b - six V1 lineage files byte-identical to the attested pins."

# B3. CHAIN + CENSUSES + COMPVER TRIPLE (independent recomputation)
Write-Section "B3. CENSUSES + COMPVER TRIPLE (INDEPENDENT RECOMPUTATION)"
$OutC = Invoke-Capped $Py @($HelperCensus, $TargetDbPath)
if ($LASTEXITCODE -ne 0) { throw ("STOP: census helper failed: " + (Norm-Text $OutC)) }
$Post = (Norm-Text $OutC) | ConvertFrom-Json
if ($Post.triggers.Count -ne $ExpectTriggersTotal) { throw ("STOP: trigger census " + $Post.triggers.Count) }
if ($Post.permissions.Count -ne $ExpectPermsTotal) { throw ("STOP: permission census " + $Post.permissions.Count) }
if ($Post.compver.Count -ne $ExpectCompverTotal) { throw ("STOP: compver census " + $Post.compver.Count) }
$PaperTrig = @(
    "v2_paper_account_immutable_update",
    "v2_paper_account_immutable_delete",
    "v2_paper_order_intent_immutable_update",
    "v2_paper_order_intent_immutable_delete",
    "v2_paper_risk_decision_immutable_update",
    "v2_paper_risk_decision_immutable_delete",
    "v2_paper_order_event_immutable_update",
    "v2_paper_order_event_immutable_delete",
    "v2_paper_fill_immutable_update",
    "v2_paper_fill_immutable_delete",
    "v2_paper_position_snapshot_immutable_update",
    "v2_paper_position_snapshot_immutable_delete",
    "v2_paper_balance_snapshot_immutable_update",
    "v2_paper_balance_snapshot_immutable_delete",
    "v2_paper_reconciliation_immutable_update",
    "v2_paper_reconciliation_immutable_delete"
)
foreach ($Tn in $PaperTrig) { if ($Post.triggers -notcontains $Tn) { throw ("FAIL: paper guard trigger missing: " + $Tn) } }
$PermSet = @($Post.permissions | ForEach-Object { $_[0] + "|" + $_[1] + "|" + $_[2] })
foreach ($Pt in @(
    "admin|v2.paper.accounts.read|SAL-2",
    "admin|v2.paper.accounts.manage|SAL-3",
    "admin|v2.paper.orders.read|SAL-2",
    "admin|v2.paper.orders.place|SAL-3",
    "admin|v2.paper.orders.cancel|SAL-3",
    "admin|v2.paper.orders.confirm|SAL-3",
    "admin|v2.paper.fills.read|SAL-2",
    "admin|v2.paper.risk.read|SAL-2"
)) { if ($PermSet -notcontains $Pt) { throw ("FAIL: permission triple missing: " + $Pt) } }
$CompSet = @($Post.compver | ForEach-Object { $_[0] + "|" + $_[1] + "|" + $_[2] })
if ($CompSet -notcontains ("replay_engine|rpe-1.0.0|" + $RpeHash)) { throw "FAIL: RPE row moved." }
if ($CompSet -notcontains ("research_job_engine|rje-1.0.0|" + $RjeHash)) { throw "FAIL: RJE row moved." }
if ($CompSet -notcontains ("paper_execution_simulator|pxs-1.0.0|" + $PxsHash)) { throw "FAIL: PXS compver row mismatch vs pinned literal." }
if ($CompSet -notcontains ("paper_risk_gateway|prg-1.0.0|" + $PrgHash)) { throw "FAIL: PRG compver row mismatch vs pinned literal." }
$OutPs = Invoke-Capped $Py @($HelperPost, $TargetDbPath)
if ($LASTEXITCODE -ne 0) { throw ("FAIL: poststate helper failed: " + (Norm-Text $OutPs)) }
$Pst = (Norm-Text $OutPs) | ConvertFrom-Json
if ($Pst.paper_tables.Count -ne 8) { throw ("FAIL: paper-table census " + $Pst.paper_tables.Count) }
if ($Pst.alembic_version.Count -ne 1 -or $Pst.alembic_version[0] -ne $ApplyTargetRevision) { throw "FAIL: alembic_version row not exactly 20260904_0048." }
if ([int]$Pst.compver_delete_guard -ne 1) { throw "FAIL: compver delete-guard not present exactly once." }
$OutPxs = Invoke-Capped $Py @($HelperRoll, $BackendRoot, "pxs")
if ($LASTEXITCODE -ne 0 -or (Norm-Text $OutPxs) -ne $PxsHash) { throw "FAIL: PXS rollhash recomputation mismatch." }
$OutPrg = Invoke-Capped $Py @($HelperRoll, $BackendRoot, "prg")
if ($LASTEXITCODE -ne 0 -or (Norm-Text $OutPrg) -ne $PrgHash) { throw "FAIL: PRG rollhash recomputation mismatch." }
Write-Evidence "PASS: B3 - censuses exactly 58 / 57 / 10; exact members; compver triple agreement (DB row == literal == live rollhash); RPE/RJE byte-carried."

# B4. LIVE GUARD PROBES
Write-Section "LIVE GUARD PROBES (transactional; nothing persists)"
$ProbePlan = @(
    "v2_paper_account_immutable_update~INSERT INTO v2_paper_account (id,account_id,record_seq,supersedes,name,base_currency,initial_balance,margin_params,lifecycle_state,confirmation_ref,data_class,mode,operator_id,correlation_id,created_at) VALUES ('probe-r','probe-a',1,NULL,'probe','USD','0','{}','active','probe-ref','synthetic','PAPER','probe-op',NULL,'2026-01-01 00:00:00')~UPDATE v2_paper_account SET name = 'x'~V2 paper accounts are immutable; UPDATE prohibited",
    "v2_paper_account_immutable_delete~INSERT INTO v2_paper_account (id,account_id,record_seq,supersedes,name,base_currency,initial_balance,margin_params,lifecycle_state,confirmation_ref,data_class,mode,operator_id,correlation_id,created_at) VALUES ('probe-r','probe-a',1,NULL,'probe','USD','0','{}','active','probe-ref','synthetic','PAPER','probe-op',NULL,'2026-01-01 00:00:00')~DELETE FROM v2_paper_account~V2 paper accounts are immutable; DELETE prohibited",
    "v2_paper_order_intent_immutable_update~INSERT INTO v2_paper_order_intent (id,intent_id,account_id,instrument_id,side,order_type,quantity,limit_price,time_in_force,idempotency_key,snapshot_ref,time_basis,confirmation_ref,actor_id,data_class,mode,operator_id,correlation_id,created_at) VALUES ('probe-r','probe-i','probe-a','instrument.probe','buy','market','1',NULL,'replay_window','probe-key','probe-snap','{}',NULL,'probe-actor','synthetic','PAPER','probe-op',NULL,'2026-01-01 00:00:00')~UPDATE v2_paper_order_intent SET quantity = '2'~V2 paper order intents are immutable; UPDATE prohibited",
    "v2_paper_order_intent_immutable_delete~INSERT INTO v2_paper_order_intent (id,intent_id,account_id,instrument_id,side,order_type,quantity,limit_price,time_in_force,idempotency_key,snapshot_ref,time_basis,confirmation_ref,actor_id,data_class,mode,operator_id,correlation_id,created_at) VALUES ('probe-r','probe-i','probe-a','instrument.probe','buy','market','1',NULL,'replay_window','probe-key','probe-snap','{}',NULL,'probe-actor','synthetic','PAPER','probe-op',NULL,'2026-01-01 00:00:00')~DELETE FROM v2_paper_order_intent~V2 paper order intents are immutable; DELETE prohibited",
    "v2_paper_risk_decision_immutable_update~INSERT INTO v2_paper_risk_decision (id,intent_id,decision,evaluated_limits,reasons,risk_config_version,decided_at_basis,confirmation_ref,data_class,mode,operator_id,correlation_id,created_at) VALUES ('probe-r','probe-i','pass','{}','{}','prc-probe','{}',NULL,'synthetic','PAPER','probe-op',NULL,'2026-01-01 00:00:00')~UPDATE v2_paper_risk_decision SET reasons = '[]'~V2 paper risk decisions are immutable; UPDATE prohibited",
    "v2_paper_risk_decision_immutable_delete~INSERT INTO v2_paper_risk_decision (id,intent_id,decision,evaluated_limits,reasons,risk_config_version,decided_at_basis,confirmation_ref,data_class,mode,operator_id,correlation_id,created_at) VALUES ('probe-r','probe-i','pass','{}','{}','prc-probe','{}',NULL,'synthetic','PAPER','probe-op',NULL,'2026-01-01 00:00:00')~DELETE FROM v2_paper_risk_decision~V2 paper risk decisions are immutable; DELETE prohibited"
)
foreach ($Plan in $ProbePlan) {
    $Partsp = $Plan.Split("~")
    $OutProbe = Invoke-Capped $Py @($HelperProbe, $TargetDbPath, $Partsp[1], $Partsp[2], $Partsp[3])
    if ($LASTEXITCODE -ne 0 -or (Norm-Text $OutProbe) -ne "PROBE-EXACT-MATCH") {
        throw ("FAIL: guard probe " + $Partsp[0] + ": '" + (Norm-Text $OutProbe) + "'.")
    }
    Write-Evidence ("probe OK: " + $Partsp[0])
}
Write-Evidence "PASS: B4 - six paper guards refuse live with exact messages."

# B5. FULL SUITE - INDEPENDENT RERUN
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
if ($SuiteCode -ne 0) { throw ("FAIL: pytest exited " + $SuiteCode) }
# PGF-022: per-line anchored containment; pytest -q prints the BARE summary form
# (no '=' bars); '^' on the joined string anchors to the whole string start,
# so the summary must be matched line-by-line. Counterfeit prefix counts
# ("21026 passed") cannot satisfy the anchor: '2' is outside [ =].
$SuiteFloorHits = @($SuiteText -split "`n" | Where-Object { $_ -match ("^[ =]*" + $SuiteFloor + " passed[ ,]") })
if ($SuiteFloorHits.Count -eq 0) { throw ("FAIL: summary does not declare " + $SuiteFloor + " passed.") }
if ($SuiteText -match "[1-9][0-9]* (failed|error)") { throw "FAIL: failures/errors in summary." }
$SuiteSummary = ($TailLines | Where-Object { ([string]$_) -match "passed" } | Select-Object -Last 1)
Write-Evidence ("PASS: B5 - suite summary: " + ([string]$SuiteSummary).Trim())

# B6. DRIFT GATE (PGF-014)
Write-Section "B6. DRIFT GATE (PGF-014)"
Push-Location $BackendRoot
try {
    $OutChk = Invoke-Capped $Py @('-m', 'alembic', 'check')
    $ChkCode = $LASTEXITCODE
} finally { Pop-Location }
Emit-Output $OutChk
$Drift = (Norm-Text $OutChk).ToLower()
if ($ChkCode -eq 0) { throw "FAIL: zero-exit check contradicts the inherited drift declaration." }
foreach ($Marker in @(
    "v2_paper_account",
    "v2_paper_order_intent",
    "v2_paper_risk_decision",
    "v2_paper_order_event",
    "v2_paper_fill",
    "v2_paper_position_snapshot",
    "v2_paper_balance_snapshot",
    "v2_paper_reconciliation"
)) {
    if ($Drift.Contains($Marker)) { throw ("FAIL: BE-8 drift token in alembic check output: " + $Marker) }
}
if ((-not $Drift.Contains("not up to date")) -and (-not $Drift.Contains("audit_write_failure_records"))) {
    throw "FAIL: inheritance witness absent."
}
Write-Evidence "PASS: B6 - drift gate: non-zero exit, zero BE-8 tokens, inheritance witness present."

# B7. VERIFY-FINAL-STATE RECORD + ANCHOR + PURE-READ LAW
Write-Section "B7. VERIFY-FINAL-STATE RECORD"
$DbShaVerifyPost = (Get-FileHash -Path $TargetDbPath -Algorithm SHA256).Hash.ToLower()
if ($DbShaVerifyPost -ne $DbShaVerifyPre) { throw ("STOP (pure-read law): the database bytes moved under a verify run: " + $DbShaVerifyPre + " -> " + $DbShaVerifyPost + " . Report to ITRGA immediately.") }
if (!(Test-Path $AnchorPath)) { throw ("STOP: the apply anchor is missing: " + $AnchorPath + " . Evidence chain incomplete; report to ITRGA.") }
$AnchorHash = (Get-FileHash -Path $AnchorPath -Algorithm SHA256).Hash.ToLower()
if ($AnchorHash -ne $Rec["ANCHOR_SHA256"]) { throw "STOP: anchor identity drifted since the apply act." }
Write-Evidence ("Anchor sha256 (recomputed, matches the apply record): " + $AnchorHash)
$VLines = @(
    "STATE_FILE_ID=ITRGA-V2-0048-VERIFY-FINAL-STATE-V1",
    ("TARGET_REVISION=" + $ApplyTargetRevision),
    ("TRIGGERS_TOTAL=" + $ExpectTriggersTotal),
    ("PERMISSIONS_TOTAL=" + $ExpectPermsTotal),
    ("COMPVER_TOTAL=" + $ExpectCompverTotal),
    ("COMPVER_PXS_HASH=" + $PxsHash),
    ("COMPVER_PRG_HASH=" + $PrgHash),
    ("SUITE_RESULT=" + ([string]$SuiteSummary).Trim()),
    ("DB_PATH=" + $TargetDbPath),
    ("DB_SHA256_VERIFIED=" + $DbShaVerifyPost),
    ("ANCHOR_SHA256=" + $AnchorHash),
    "APPLY_RECORD=0048-APPLY-FINAL-STATE.txt",
    "RESULT=VERIFIED-COMPLETE-0048",
    "TRANSCRIPT=0048-VERIFY-RUN-V1.txt",
    ("UTC_COMPLETED=" + ([DateTime]::UtcNow.ToString("yyyy-MM-ddTHH:mm:ssZ")))
)
$VLines | Set-Content -Path $VerifyRecPath -Encoding UTF8
foreach ($Vl in $VLines) { Write-Evidence ("STATE: " + $Vl) }
Write-Evidence ""
Write-Evidence "VERIFY PACK COMPLETE - PASS. 0048 is VERIFIED-COMPLETE on the operator environment; the application may now be started. Send back operator-evidence\BE-8\0048-VERIFY-RUN-V1.txt (with 0048-APPLY-RUN-V1.txt)."
Write-Evidence ("UTC end: " + ([DateTime]::UtcNow.ToString("yyyy-MM-ddTHH:mm:ssZ")))

Remove-Helpers

