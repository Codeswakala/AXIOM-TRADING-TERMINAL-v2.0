# =====================================================================
# AXIOM V2 - 0048 WORKING-DATABASE APPLICATION ACT (BAND BE-8)
# ITRGA SQLITE APPLY ACT EVIDENCE PACK (V1)
# Pack ID: ITRGA-V2-0048-APPLY-PACK-V1
# Authority: BO-V2-BE-8-001 T-1...T-18; ITRGA-ACC-V2-BE-8-INT-001
#   (INT ACCEPTED + DRIFT GATE); ITRGA-ACT-V2-BE-8-0048-001 (original
#   order, station-targeted) -> AXIOM-V2-BE-8-0048-HALT-001 (act VOID
#   at 3.3, halt LAWFUL) -> ITRGA-RULE-V2-BE8-HALT-0048-001 section 2
#   (re-target RULED to this console-pack form) ; operator
#   authorization 2026-09-05 stands for the same act.
# Pattern: ITRGA-V2-0047-APPLY-PACK-V4 / RESUME V1 ed-2/VERIFY V5 ed-3
#   (all PGF lessons by construction; E-0046-DUP refuse-if-completed
#   law; independent re-proof: this pack trusts NOTHING it did not
#   recompute on this run).
#
# Re-target notes (R1):
#   - The first (station-targeted) act attempt halted correctly at its
#     own 3.3 identity gate: the DA-station file was never the working
#     lineage (no alembic lineage; paper tables pre-present by
#     models-metadata auto-create; identity b64b8400... != sealed
#     27bda311...). The gates worked. This pack re-issues the SAME act
#     against the sealed console lineage with a HARD pre-mutation
#     identity gate: DB sha256 must equal the sealed
#     27bda311...c776f AND alembic current must equal 20260903_0047.
#   - Rerun safety: if a run dies AFTER the one sanctioned mutation
#     but before the final-state record exists, a rerun correctly
#     refuses at the identity gate (DB no longer sealed); STOP and
#     report to ITRGA - a RESUME pack follows the 0047 precedent.
#   - Debris rule on console (E-0046-DUP): the backend directory must
#     hold EXACTLY ONE axiom_dev.db* entry - the database itself.
#
# WHAT THIS PACK DOES:
#   - Read-write scope: ONE schema mutation (alembic upgrade
#     20260903_0047 -> 20260904_0048) on the target db file; lands the
#     20-file accepted corpus (15 new + 5 amended, hash-pinned base64
#     literals, adjudicated); writes only its transcript, apply
#     final-state record, the rollback anchor, and throwaway helpers
#     removed on exit.
#   - BEFORE RUNNING: MD5-verify the issuance pins FIRST; the
#     application must be STOPPED; run from the repository root:
#       powershell -NoProfile -ExecutionPolicy Bypass -File ".\ITRGA_V2_0048_APPLY_PACK_V1.ps1"
#   - OPERATOR INSTRUCTION CARD:
#       1. MD5-verify ITRGA_V2_0048_APPLY_PACK_V1.ps1 and
#          ITRGA_V2_0048_BASELINE_PINS.txt against ITRGA-ISS-V2-0048-PACKS-001.
#       2. Run this pack; send back operator-evidence\BE-8\0048-APPLY-RUN-V1.txt.
#       3. On PASS, run ITRGA_V2_0048_VERIFY_PACK_V1.ps1; keep the
#          application STOPPED until VERIFY PASSes.
# =====================================================================
# SUPERSESSION RECORDS (EDITION 3, 2026-09-05 supersedes ed-2):
#   Ed-1 STOPped lawfully at the A1 DUP sweep (3 axiom_dev.db* entries);
#   ed-2 carried the ISS-002 heritage-pin adjudication. Ed-2 then STOPped
#   lawfully at the A1 chain-shape gate: the 0048 migration file proved
#   PRE-LANDED at pinned bytes with current == 20260903_0047 and a single
#   script head 20260904_0048 (the customary operator-side merge). Ed-3
#   carries the ISS-003 uniform FOREIGN-STATE ADJUDICATION at A1 (0047 V2
#   law): classic and witnessed-pre-landing chain shapes both lawful at
#   pinned bytes; every other shape refuses. No mutation ever occurred.
#
# SUPERSESSION RECORD (EDITION 2, 2026-09-05):
#   Ed-1 field run STOPped lawfully at the A1 console sweep (3 axiom_dev.db*
#   entries). Field enumeration identified all three entries: sealed lineage
#   (27bda311...c776f), V1 git-custody relic (561b2758...), HALT-0048 debris
#   tombstone (b64b8400...). ITRGA-ISS-V2-0048-PACKS-002 section ruling:
#   heritage artifacts exempted by name+sha256 pin; any UNPINNED sibling still
#   refuses. Ed-1 STOPped pre-mutation (nothing to unwind); ed-1 bytes retired.
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
$Transcript    = Join-Path $EvidenceDir "0048-%PACK%-RUN-V1.txt"
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

Write-Section "0048 APPLY PACK V1 - ITRGA-V2-0048-APPLY-PACK-V1"
if (!(Test-Path $BackendRoot)) { throw ("STOP: backend directory not found: " + $BackendRoot + ". Run from the repository root.") }
if (!(Test-Path $PinsPath))    { throw ("STOP: baseline pin file missing at the repository root: " + $PinsPath) }
New-Item -ItemType Directory -Force -Path $EvidenceDir | Out-Null

# A0. STARTUP HYGIENE (refuse-if-completed law) + AUTHORITY SWEEP
if (Test-Path $ApplyRecPath) {
    throw ("STOP (E-0046-DUP law): a completed apply-final-state record already exists: " + $ApplyRecPath + " . Refusing to disturb it; report to ITRGA if you believe it is stale.")
}
Remove-Item -Force -ErrorAction SilentlyContinue $Transcript
Sweep-Authority
Write-Evidence ("UTC start: " + ([DateTime]::UtcNow.ToString("yyyy-MM-ddTHH:mm:ssZ")))
Write-Evidence "Authority: BO-V2-BE-8-001; ITRGA-ACC-V2-BE-8-INT-001; ITRGA-RULE-V2-BE8-HALT-0048-001 (re-target to console lineage); operator authorization 2026-09-05."
Write-Evidence "Read-write scope: ONE schema mutation (alembic upgrade head) on the target db; 20-file corpus landing; evidence in operator-evidence\BE-8; temp helpers removed on exit."
$null = Check-Pins
Write-Helpers
Write-Evidence "PASS: A0 - startup hygiene, authority sweep, baseline pins cross-pinned, helpers staged."

# A1. TARGET, IDENTITY GATE, TOOLCHAIN, CHAIN FLOOR
Write-Section "A1. TARGET IDENTITY (SEALED-LINEAGE GATE) + TOOLCHAIN + FLOOR"
$DbInput = Read-Host "Absolute path of the working database file (backend\axiom_dev.db)"
$TargetDbPath = ([string]$DbInput).Trim().Trim('"').Trim("'")
if (!(Test-Path $TargetDbPath)) { throw ("STOP: target database file not found: " + $TargetDbPath) }
Write-Evidence ("Target db: " + $TargetDbPath)
# E-0046-DUP console sweep (EDITION 2 adjudication, ITRGA-ISS-V2-0048-PACKS-002):
# law = exactly one axiom_dev.db target candidate + ZERO UNPINNED siblings
# in the backend root. The two pinned heritage artifacts below were ruled on
# field enumeration 2026-09-05: V1 git-custody relic (QRET ruling: untouched)
# and the HALT-0048 debris tombstone (RULING: preserved, never deleted).
$DupSweep = @(Get-ChildItem $BackendRoot -Filter "axiom_dev.db*" -ErrorAction SilentlyContinue)
$Exempt = @{
    "axiom_dev.db.backup" = "561b275800ab2b677d7c643e65fe2de2b18cee2e9b4840036a2fc2aebc5e4a98"
    "axiom_dev.db.QUARANTINE-V2-BE8-20260905" = "b64b8400d08c97d9c30f130489a78aade8c33675014652368368205240a1cdc0"
}
foreach ($Eit in $DupSweep) {
    if ($Eit.Name -eq "axiom_dev.db") { continue }
    $Eh = (Get-FileHash -Path $Eit.FullName -Algorithm SHA256).Hash.ToLower()
    if ($Exempt.ContainsKey($Eit.Name) -and $Exempt[$Eit.Name] -eq $Eh) {
        Write-Evidence ("DUP-sweep exempted pinned heritage: " + $Eit.Name + " (" + $Eh.Substring(0, 12) + "...)")
        continue
    }
    if ($Exempt.ContainsKey($Eit.Name)) { throw ("STOP (E-0046-DUP): pinned heritage artifact drifted from its known bytes: " + $Eit.Name + " sha " + $Eh + " . STOP and report to ITRGA.") }
    throw ("STOP (E-0046-DUP console sweep): unpinned axiom_dev.db* sibling in the backend root: " + $Eit.Name + " sha " + $Eh + " . Resolve with ITRGA first.")
}
$DbCount = @($DupSweep | Where-Object { $_.Name -eq "axiom_dev.db" }).Count
if ($DbCount -ne 1) { throw ("STOP: exactly one axiom_dev.db target candidate is lawful; found " + $DbCount + ".") }
$Py = Find-Python
$OutVer = Invoke-Capped $Py @('-c', "import alembic; print(alembic.__version__)")
if ((Norm-Text $OutVer) -ne $AlembicPin) { throw ("STOP: alembic " + $AlembicPin + " required.") }
$DbShaPre = (Get-FileHash -Path $TargetDbPath -Algorithm SHA256).Hash.ToLower()
Write-Evidence ("DB sha256 PRE: " + $DbShaPre)
if ($DbShaPre -ne $SealedDbSha) { throw ("STOP (sealed-lineage identity gate, ITRGA-RULE-V2-BE8-HALT-0048-001): the target is NOT the sealed 0047 working lineage: got " + $DbShaPre + " , expected " + $SealedDbSha + " . No mutation can follow. class act.target.not_working_lineage; report to ITRGA.") }
Push-Location $BackendRoot
try {
    $OutCur = Invoke-Capped $Py @('-m', 'alembic', 'current')
    $CurLines = @(@($OutCur) | Where-Object { ([string]$_) -match $BaselineRevision -and ([string]$_) -notmatch "^INFO" })
    if ($CurLines.Count -ne 1) { throw ("STOP: expected current = " + $BaselineRevision + "; observed '" + (Norm-Text $OutCur) + "'.") }
    $CurHasHeadTag = @($CurLines | Where-Object { ([string]$_) -match [regex]::Escape("(head)") }).Count -eq 1
    $OutHeads = Invoke-Capped $Py @('-m', 'alembic', 'heads')
    $HeadLines = @(@($OutHeads) | Where-Object { ([string]$_).Trim() -ne "" -and ([string]$_) -notmatch "^INFO" })
    if ($HeadLines.Count -ne 1) { throw ("STOP: expected a single head; observed '" + (Norm-Text $OutHeads) + "'.") }
    $HeadIsBaseline = @($HeadLines | Where-Object { ([string]$_) -match $BaselineRevision }).Count -eq 1
    $HeadIsTarget = @($HeadLines | Where-Object { ([string]$_) -match $ApplyTargetRevision }).Count -eq 1
    if ($HeadIsBaseline) {
        if (-not $CurHasHeadTag) { throw ("STOP: classic chain shape requires the (head) tag on current; observed bare - inconsistent with a single baseline head; report to ITRGA.") }
        Write-Evidence "chain shape: classic (script head == baseline; 0048 not pre-landed)"
    } elseif ($HeadIsTarget) {
        # EDITION 3 FOREIGN-STATE ADJUDICATION (ITRGA-ISS-V2-0048-PACKS-003):
        # single script head == the 0048 target => the migration file pre-landed;
        # it is witnessed-accepted ONLY at its pinned bytes (the 0047 V2 law).
        if ($CurHasHeadTag) { throw "STOP: current carries (head) while the script head is the 0048 target - inconsistent chain state; report to ITRGA." }
        $MigPath = Join-Path $BackendRoot "alembic\versions\20260904_0048_v2_be8_paper_trading.py"
        if (!(Test-Path $MigPath)) { throw ("STOP: 0048 head advertised but the migration file is missing at " + $MigPath) }
        $MigHash = (Get-FileHash -Path $MigPath -Algorithm SHA256).Hash.ToLower()
        if ($MigHash -ne "2cb83b3d102598523834b867aa780bb659df3366a8775c65cc0750740dc398c2") { throw ("STOP: pre-landed 0048 migration file at foreign bytes: " + $MigHash + " . Refuse (uniform adjudication law); report to ITRGA.") }
        Write-Evidence "chain shape: witnessed pre-landing (current == 20260903_0047; single head 20260904_0048; pre-landed migration == pinned bytes)"
    } else {
        throw ("STOP: the single script head is neither the baseline nor the 0048 target: '" + (Norm-Text $OutHeads) + "'.")
    }
} finally { Pop-Location }
$DbFs = (Get-Item $TargetDbPath).FullName -replace "\\", "/"
$env:AXIOM_DATABASE_URL = ("sqlite+aiosqlite:///" + $DbFs)
Write-Evidence ("AXIOM_DATABASE_URL pinned explicit (standing rule): " + $env:AXIOM_DATABASE_URL)
Write-Evidence "PASS: A1 - sealed lineage proven (sha + current==20260903_0047 (head), single head); toolchain pinned; console DUP sweep clean."

# A2. ROLLBACK ANCHOR (before any modification)
Write-Section "A2. ROLLBACK ANCHOR (before any modification)"
Copy-Item -Path $TargetDbPath -Destination $AnchorPath -Force
if (!(Test-Path $AnchorPath)) { throw "STOP: anchor copy not created." }
$AnchorHash = (Get-FileHash -Path $AnchorPath -Algorithm SHA256).Hash.ToLower()
if ($AnchorHash -ne $DbShaPre) { throw "STOP: anchor hash differs from source hash. Aborting before any modification." }
$OutIck = Invoke-Capped $Py @('-c', ("import sqlite3; c=sqlite3.connect(r'" + $AnchorPath + "'); print(c.execute('PRAGMA integrity_check;').fetchone()[0]); c.close()"))
if ((Norm-Text $OutIck) -ne "ok") { throw ("STOP: anchor integrity_check '" + (Norm-Text $OutIck) + "', expected 'ok'.") }
Write-Evidence ("Anchor: " + $AnchorPath)
Write-Evidence ("Anchor sha256 == db sha256 pre-apply: " + $AnchorHash)
Write-Evidence "PASS: A2 - a proven rollback anchor exists before any mutation."

# A3. PRE-STATE PINS + PRE-DRIFT GATE
Write-Section "A3. PRE-STATE PINS (V1 floor; floor census; modified targets) + PRE-DRIFT"
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

$OutC = Invoke-Capped $Py @($HelperCensus, $TargetDbPath)
if ($LASTEXITCODE -ne 0) { throw ("STOP: census helper failed: " + (Norm-Text $OutC)) }
$Pre = (Norm-Text $OutC) | ConvertFrom-Json
if ($Pre.triggers.Count -ne $ExpectFloorTriggers) { throw ("STOP: trigger census " + $Pre.triggers.Count) }
if ($Pre.permissions.Count -ne $ExpectFloorPerms) { throw ("STOP: permission census " + $Pre.permissions.Count) }
if ($Pre.compver.Count -ne $ExpectFloorCompver) { throw ("STOP: compver census " + $Pre.compver.Count) }
Write-Evidence "PASS: A3b - floor totals exactly 42 / 49 / 8 (triggers/permissions/compver)."
$PreStates = @(
    "app\v2\api\router.py|ad4afdd4eb5fe0c0676c45a9b779cb9eeeb16140163e6f7243fd3c9ad606f670",
    "app\v2\rbac\permissions.py|a3dff08218b2afa7029b678396673c317fe1852f9785697bb35a36cbf0cd3b3a",
    "app\db\models\__init__.py|32b0f7707fe2bd2556b4e01eed125becff9676f494a960e5a74c0c34de9855e9"
)
foreach ($Ps in $PreStates) {
    $Parts = $Ps.Split("|")
    $PsPath = Join-Path $BackendRoot $Parts[0]
    if (!(Test-Path $PsPath)) { throw ("STOP: modified-target missing at the floor: " + $PsPath) }
    $PsHash = (Get-FileHash -Path $PsPath -Algorithm SHA256).Hash.ToLower()
    if ($PsHash -ne $Parts[1]) {
        $PinnedAfter = @($FilePinsAfter | Where-Object { $_.StartsWith($Parts[0] + "|") })
        if ($PinnedAfter.Count -eq 1 -and $PsHash -eq $PinnedAfter[0].Split("|")[1]) { Write-Evidence ("already at post-state (pre-landed): " + $Parts[0]); continue }
        throw ("STOP: modified-target at unpinned state: " + $Parts[0] + " sha " + $PsHash + " . Expected 0047 floor " + $Parts[1] + " . STOP and report to ITRGA.")
    }
    Write-Evidence ("floor pre-hash OK: " + $Parts[0])
}
Write-Evidence "PASS: A3c - the three hash-pinned modified targets sit at their 0047-floor bytes (or already pre-landed)."
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
Write-Evidence "PASS: A3d - PRE-drift gate at 20260903_0047: non-zero exit, zero BE-8 tokens, inheritance witness present."


# ---------------------------------------------------------------------
# A4. DELIVERED FILE LANDING (20 hash-pinned literals)
# ---------------------------------------------------------------------
Write-Section "A4. LANDING THE ACCEPTED 20-FILE SET (base64 literals; adjudicated; verified twice)"
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

# file: app\v2\paper_trading\__init__.py  (pin d0a090fe31ca...)
$Fapp_v2_paper_trading__init__py = @'
IiIiQVhJT00gVjIgQkUtOCDigJQgcGFwZXIgdHJhZGluZywgcGFwZXIgYWNjb3VudCwgcmlzayBnYXR
ld2F5LgoKU2VhbGVkIHBhcmFsbGVsIGRvbWFpbiAoZGVzaWduIEFYSU9NLVYyLUJFLTgtREVTSUdOLT
AwMSB2MS4xLjAgQUNDRVBURUQ7CkJPLVYyLUJFLTgtMDAxKS4gTm8gYWRhcHRlciBpbnRlcmZhY2UgZ
Xhpc3RzIGluIHRoaXMgcGFja2FnZSBCWSBERVNJR04KKE4yIHN0cnVjdHVyYWwgaXNvbGF0aW9uKTsg
emVybyBjcmVkZW50aWFscyAoTjEpOyBmaWxscyBhcmUKc2NoZW1hLWxvY2tlZCAncGFwZXJfc2ltdWx
hdGVkJyAoTjQpLgoiIiIK
'@
$LandPath = Join-Path $BackendRoot "app\v2\paper_trading\__init__.py"
New-Item -ItemType Directory -Force -Path (Split-Path $LandPath) | Out-Null
if (Test-Path $LandPath) {
    $Cur = (Get-FileHash -Path $LandPath -Algorithm SHA256).Hash.ToLower()
    if ($Cur -eq "d0a090fe31cad5e36012b939987b9f3ae627f5d363ff34a3ee76d8f0b48c9911") { Write-Evidence ("pre-landing witnessed (already pinned bytes): app\v2\paper_trading\__init__.py") }
    else { throw ("STOP (A4 FOREIGN-STATE ADJUDICATION LAW): new-file target exists with foreign bytes: " + $LandPath + " sha " + $Cur + " . Nothing modified for this file; report to ITRGA.") }
} else {
    [IO.File]::WriteAllBytes($LandPath, (B64-Decode -B64Chunk $Fapp_v2_paper_trading__init__py))
    $Cur = (Get-FileHash -Path $LandPath -Algorithm SHA256).Hash.ToLower()
    if ($Cur -ne "d0a090fe31cad5e36012b939987b9f3ae627f5d363ff34a3ee76d8f0b48c9911") { throw ("FAIL: post-write hash drift on " + $LandPath) }
    Write-Evidence ("landed + verified: app\v2\paper_trading\__init__.py")
}

# file: app\v2\paper_trading\contracts.py  (pin c90e6e582881...)
$Fapp_v2_paper_trading_contracts_py = @'
IiIiQkUtOCB0eXBlZCBjb250cmFjdHMg4oCUIHZvY2FidWxhcmllcywgc2VhbGVkIHJlZ2lzdHJ5LCB
0eXBlZCBzZWFtLgoKRGVzaWduIEFYSU9NLVYyLUJFLTgtREVTSUdOLTAwMSB2MS4xLjAgKEFDQ0VQVE
VEKSBTMS9TMi9TNjsgQk8tVjItQkUtOC0wMDEKVC0yL1QtNC9ULTkuIFRoZSBOMiBpc29sYXRpb24gb
WVjaGFuaXNtIGxpdmVzIGhlcmU6IEVYRUNVVElPTl9CQUNLRU5EUyBpcyBhCmZyb3plbiBzaW5nbGUt
ZW50cnkgbGl0ZXJhbCAobm8gcmVnaXN0cmF0aW9uIGZ1bmN0aW9uLCBubyBwbHVnaW4gcGF0aCwgbm8
KY29uZmlnIGZpbGUg4oCUIGFkZGluZyBhIGtleSByZXF1aXJlcyBlZGl0aW5nIHRoaXMgbGl0ZXJhbC
wgY2F1Z2h0IGJ5IHRoZQpzb3VyY2UgbWFuaWZlc3QgYW5kIHRoZSBpbXBvcnQgc2NhbikuIE5vIGFkY
XB0ZXIgaW50ZXJmYWNlL0FCQyBleGlzdHMKYW55d2hlcmUgaW4gdGhpcyBiYW5kIEJZIERFU0lHTiAo
YW4gYWJzdHJhY3Rpb24gd2l0aCBvbmUgcGFwZXIKaW1wbGVtZW50YXRpb24gaXMgdGhlIHN1YnN0aXR
1dGlvbiBzdXJmYWNlIE4yIGZvcmJpZHMpLgoiIiIKCmZyb20gX19mdXR1cmVfXyBpbXBvcnQgYW5ub3
RhdGlvbnMKCmZyb20gZGF0YWNsYXNzZXMgaW1wb3J0IGRhdGFjbGFzcwpmcm9tIGRlY2ltYWwgaW1wb
3J0IERlY2ltYWwKZnJvbSB0eXBlcyBpbXBvcnQgTWFwcGluZ1Byb3h5VHlwZQpmcm9tIHR5cGluZyBp
bXBvcnQgRmluYWwKCiMgLS0tIE4yOiB0aGUgc2VhbGVkIHJvdXRpbmcgcmVnaXN0cnkgKFM2LjEpIC0
tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tCkVYRUNVVElPTl9CQUNLRU5EUzogRmluYW
wgPSBNYXBwaW5nUHJveHlUeXBlKAogICAgeyJwYXBlciI6ICJhcHAudjIucGFwZXJfdHJhZGluZy5za
W11bGF0b3IifSkKCiMgLS0tIE9yZGVyIGxpZmVjeWNsZSB2b2NhYnVsYXJ5IChTMi4xOyBjbG9zZWQp
IC0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLQpPUkRFUl9TVEFURVMgPSAoCiAgICAiZHJ
hZnQiLCAidmFsaWRhdGVkIiwgInJlamVjdGVkIiwKICAgICJyaXNrX3Bhc3NlZCIsICJyaXNrX2Jsb2
NrZWQiLCAicmlza19ob2xkIiwKICAgICJleGVjdXRpbmciLCAiZmlsbGVkIiwgInBhcnRpYWxseV9ma
WxsZWQiLAogICAgInNldHRsZWQiLCAiY2FuY2VsbGVkIiwgImV4cGlyZWQiLCAicXVhcmFudGluZWRf
dW5rbm93biIsCikKVEVSTUlOQUxfU1RBVEVTID0gKCJzZXR0bGVkIiwgInJlamVjdGVkIiwgInJpc2t
fYmxvY2tlZCIsICJjYW5jZWxsZWQiLAogICAgICAgICAgICAgICAgICAgImV4cGlyZWQiLCAicXVhcm
FudGluZWRfdW5rbm93biIpCgojIFMyLjIgZXhoYXVzdGl2ZSBsZWdhbCB0cmFuc2l0aW9ucyDigJQgY
WJzZW5jZSBpcyBhIHR5cGVkIHJlZnVzYWwuCkxFR0FMX1RSQU5TSVRJT05TID0gKAogICAgKCJkcmFm
dCIsICJ2YWxpZGF0ZWQiKSwgKCJkcmFmdCIsICJyZWplY3RlZCIpLCAoImRyYWZ0IiwgImNhbmNlbGx
lZCIpLAogICAgKCJ2YWxpZGF0ZWQiLCAicmlza19wYXNzZWQiKSwgKCJ2YWxpZGF0ZWQiLCAicmlza1
9ibG9ja2VkIiksCiAgICAoInZhbGlkYXRlZCIsICJyaXNrX2hvbGQiKSwgKCJ2YWxpZGF0ZWQiLCAiY
2FuY2VsbGVkIiksCiAgICAoInJpc2tfaG9sZCIsICJyaXNrX3Bhc3NlZCIpLCAoInJpc2tfaG9sZCIs
ICJjYW5jZWxsZWQiKSwKICAgICgicmlza19wYXNzZWQiLCAiZXhlY3V0aW5nIiksCiAgICAoImV4ZWN
1dGluZyIsICJmaWxsZWQiKSwgKCJleGVjdXRpbmciLCAicGFydGlhbGx5X2ZpbGxlZCIpLAogICAgKC
JleGVjdXRpbmciLCAiZXhwaXJlZCIpLCAoImV4ZWN1dGluZyIsICJxdWFyYW50aW5lZF91bmtub3duI
iksCiAgICAoImZpbGxlZCIsICJzZXR0bGVkIiksICgicGFydGlhbGx5X2ZpbGxlZCIsICJzZXR0bGVk
IiksCikKCiMgUzIuNi9DLTFjIGNsb3NlZCBldmVudC1jbGFzcyB2b2NhYnVsYXJ5LgpFVkVOVF9DTEF
TU0VTID0gKAogICAgIm9yZGVyLmRyYWZ0ZWQiLCAib3JkZXIudmFsaWRhdGVkIiwgIm9yZGVyLnJlam
VjdGVkIiwKICAgICJyaXNrLnBhc3NlZCIsICJyaXNrLmJsb2NrZWQiLCAiaG9sZC5pc3N1ZWQiLAogI
CAgImhvbGQuY29uZmlybWVkIiwgImhvbGQuY2FuY2VsbGVkIiwKICAgICJvcmRlci5jYW5jZWxsZWQi
LCAiZXhlY3V0aW9uLnN0YXJ0ZWQiLAogICAgImV4ZWN1dGlvbi5maWxsZWQiLCAiZXhlY3V0aW9uLnB
hcnRpYWxseV9maWxsZWQiLAogICAgImV4ZWN1dGlvbi5leHBpcmVkIiwgIm9yZGVyLnNldHRsZWQiLA
ogICAgIm9yZGVyLnJlY292ZXJlZCIsICJvcmRlci5xdWFyYW50aW5lZCIsCikKCiMgUzMgZGVjaXNpb
24gdm9jYWJ1bGFyeS4KUklTS19ERUNJU0lPTlMgPSAoInBhc3MiLCAiYmxvY2siLCAiaG9sZCIpCgoj
IE40OiB0aGUgc2luZ2xlLXZhbHVlIGZpbGwtY2xhc3MgbGF3IOKAlCB0aGUgc2NoZW1hIENIRUNLIGF
kbWl0cyBleGFjdGx5IHRoaXMuCkZJTExfQ0xBU1NFUyA9ICgicGFwZXJfc2ltdWxhdGVkIiwpCgojIF
M3LjIvQy0xYiBjb25maXJtYXRpb24gcmVmdXNhbCBjbGFzc2VzICh0eXBlZDsgZWFjaCBkdXJhYmx5I
GF1ZGl0ZWQpLgpDT05GSVJNQVRJT05fUkVGVVNBTFMgPSAoCiAgICAicGFwZXIuY29uZmlybWF0aW9u
LmFscmVhZHlfY29uc3VtZWQiLAogICAgInBhcGVyLmNvbmZpcm1hdGlvbi5yZWZfbWlzbWF0Y2giLAo
gICAgInBhcGVyLmNvbmZpcm1hdGlvbi5jYW5jZWxsZWQiLAogICAgInBhcGVyLmNvbmZpcm1hdGlvbi
5ub3RfY29uZmlybWFibGUiLAopCgpBQ0NPVU5UX1NUQVRFUyA9ICgiYWN0aXZlIiwgImZyb3plbiIsI
CJjbG9zZWQiKQpBQ0NPVU5UX0FDVElPTlMgPSAoImNyZWF0ZSIsICJmcmVlemUiLCAiY2xvc2UiKQpJ
TlRFTlRfU0lERVMgPSAoImJ1eSIsICJzZWxsIikKSU5URU5UX1RZUEVTID0gKCJtYXJrZXQiLCAibGl
taXQiKQpUSU1FX0lOX0ZPUkNFX1YxID0gKCJyZXBsYXlfd2luZG93IiwpCkJBU0VfQ1VSUkVOQ0lFU1
9WMSA9ICgiVVNEIiwpCgojIENvc3QtdW5pdCB2b2NhYnVsYXJ5IOKAlCBDUi1WMi1CRS03LTAwMSBsa
W5lYWdlLCBzYW1lIGxhdy4KQ09TVF9VTklUU19WMSA9ICgicHJpY2UiLCAiZnJhY3Rpb24iKQoKIyBT
MyB2MSByaXNrIGNvbmZpZ3VyYXRpb24gKEEtMTogREEgZGVmYXVsdHMsIE9wZXJhdG9yIHJlc2V0cyB
hdCB3aWxsIHZpYSBhCiMgZnV0dXJlIGdvdmVybmVkIGFjdDsgdmVyc2lvbiBwaW5uZWQgb24gZXZlcn
kgZGVjaXNpb24gcm93KS4KUklTS19DT05GSUdfVkVSU0lPTl9WMSA9ICJwcmMtMSIKUklTS19DT05GS
UdfVjE6IEZpbmFsID0gTWFwcGluZ1Byb3h5VHlwZSh7CiAgICAibWF4X29yZGVyX3F1YW50aXR5Ijog
RGVjaW1hbCgiMTAwMDAiKSwKICAgICJtYXhfb3JkZXJfbm90aW9uYWwiOiBEZWNpbWFsKCIxMDAwMDA
iKSwKICAgICJob2xkX2JhbmRfbG93ZXJfZnJhY3Rpb24iOiBEZWNpbWFsKCIwLjgwIiksCiAgICAibW
F4X2NvbmNlbnRyYXRpb25fZnJhY3Rpb24iOiBEZWNpbWFsKCIwLjI1IiksCiAgICAibWFyZ2luX3Jhd
GVfZGVmYXVsdCI6IERlY2ltYWwoIjAuNSIpLAogICAgIm1heF9pbnRlbnRzX3Blcl9zZXNzaW9uIjog
MTAwLAp9KQoKIyBUaGUgbWFuZGF0b3J5IHVuY29uZGl0aW9uYWwgZGlzY2xhaW1lciAoTjQgc3VyZmF
jZSBsYXcpLgpQQVBFUl9ESVNDTEFJTUVSID0gKAogICAgInBhcGVyLXNpbXVsYXRlZCBleGVjdXRpb2
4gb24gZ292ZXJuZWQgcmVwbGF5YWJsZSBzbmFwc2hvdHM7ICIKICAgICJuZXZlciBicm9rZXItY29uZ
mlybWVkOyBubyBsaXZlIG9yIGZ1dHVyZSBwZXJmb3JtYW5jZSBjbGFpbSIKKQoKX0RPTUFJTiA9ICJ2
Mi5wYXBlcl90cmFkaW5nIgoKCkBkYXRhY2xhc3MoZnJvemVuPVRydWUpCmNsYXNzIFBhcGVyT3JkZXJ
JbnRlbnQ6CiAgICAiIiJUaGUgT05MWSB0eXBlIHRoZSBzaW11bGF0b3Igc2VhbSBhY2NlcHRzIChTNi
4xIHR5cGVkIHNlYW0pLgoKICAgIENvbnN0cnVjdGVkIGV4Y2x1c2l2ZWx5IGJ5IHRoZSBydW4gd3Jpd
GVyIGFmdGVyIHRoZSBTMi42IGRlcml2ZWQgcnVsZQogICAgKGBtYXlfZXhlY3V0ZWApIHBhc3Nlcy4g
RnJvemVuOiBubyBmaWVsZCBpcyBhc3NpZ25hYmxlIHBvc3QtY29uc3RydWN0aW9uLgogICAgIiIiCgo
gICAgaW50ZW50X2lkOiBzdHIKICAgIGFjY291bnRfaWQ6IHN0cgogICAgaW5zdHJ1bWVudF9pZDogc3
RyCiAgICBzaWRlOiBzdHIKICAgIG9yZGVyX3R5cGU6IHN0cgogICAgcXVhbnRpdHk6IERlY2ltYWwKI
CAgIGxpbWl0X3ByaWNlOiBEZWNpbWFsIHwgTm9uZQogICAgc25hcHNob3RfcmVmOiBzdHIKICAgIHdp
bmRvd19zdGFydDogc3RyCiAgICB3aW5kb3dfZW5kOiBzdHIKICAgIGNvc3RfbW9kZWw6IGRpY3QKCgp
AZGF0YWNsYXNzKGZyb3plbj1UcnVlKQpjbGFzcyBQYXBlck91dGNvbWU6CiAgICAiIiJVbmlmb3JtIH
R5cGVkIG91dGNvbWUgZm9yIHBhcGVyIHdyaXRlcnMuIiIiCgogICAgb3V0Y29tZTogc3RyCiAgICByZ
WFzb25zOiBsaXN0CiAgICByZWNvcmRfaWQ6IHN0ciB8IE5vbmUgPSBOb25lCiAgICBjb25maXJtYXRp
b25fcmVmOiBzdHIgfCBOb25lID0gTm9uZQoKICAgIEBwcm9wZXJ0eQogICAgZGVmIHJlZnVzZWQoc2V
sZikgLT4gYm9vbDoKICAgICAgICByZXR1cm4gc2VsZi5vdXRjb21lID09ICJyZWZ1c2VkIgoKCmNsYX
NzIFBhcGVyUmVmdXNlZChFeGNlcHRpb24pOgogICAgIiIiVHlwZWQgcmVmdXNhbCBpbiB0aGUgcGFwZ
XIgZG9tYWluOyBjbGFzcyArIHJlYXNvbnMgYWx3YXlzIGNhcnJpZWQuIiIiCgogICAgZGVmIF9faW5p
dF9fKHNlbGYsIHJlZnVzYWxfY2xhc3M6IHN0ciwgcmVhc29uczogbGlzdCkgLT4gTm9uZToKICAgICA
gICBzZWxmLnJlZnVzYWxfY2xhc3MgPSByZWZ1c2FsX2NsYXNzCiAgICAgICAgc2VsZi5yZWFzb25zID
0gcmVhc29ucwogICAgICAgIHN1cGVyKCkuX19pbml0X18oZiJ7cmVmdXNhbF9jbGFzc306IHtyZWFzb
25zfSIpCg==
'@
$LandPath = Join-Path $BackendRoot "app\v2\paper_trading\contracts.py"
New-Item -ItemType Directory -Force -Path (Split-Path $LandPath) | Out-Null
if (Test-Path $LandPath) {
    $Cur = (Get-FileHash -Path $LandPath -Algorithm SHA256).Hash.ToLower()
    if ($Cur -eq "c90e6e5828811a4699dabbb538183a55534306604020a11e96771cd79589b502") { Write-Evidence ("pre-landing witnessed (already pinned bytes): app\v2\paper_trading\contracts.py") }
    else { throw ("STOP (A4 FOREIGN-STATE ADJUDICATION LAW): new-file target exists with foreign bytes: " + $LandPath + " sha " + $Cur + " . Nothing modified for this file; report to ITRGA.") }
} else {
    [IO.File]::WriteAllBytes($LandPath, (B64-Decode -B64Chunk $Fapp_v2_paper_trading_contracts_py))
    $Cur = (Get-FileHash -Path $LandPath -Algorithm SHA256).Hash.ToLower()
    if ($Cur -ne "c90e6e5828811a4699dabbb538183a55534306604020a11e96771cd79589b502") { throw ("FAIL: post-write hash drift on " + $LandPath) }
    Write-Evidence ("landed + verified: app\v2\paper_trading\contracts.py")
}

# file: app\v2\paper_trading\accounts.py  (pin 0e54f4c2c38d...)
$Fapp_v2_paper_trading_accounts_py = @'
IiIiQkUtOCBwYXBlciBhY2NvdW50IHdyaXRlcnMgKGRlc2lnbiBTMS9TNy4yOyBCTyBULTUpLgoKVmV
yc2lvbmVkLWltbXV0YWJsZSBhY2NvdW50cyAocmVjb3JkX3NlcSArIHN1cGVyc2VkZXM7IGN1cnJlbm
N5IG9mIHRoZQpncmVhdGVzdCByZWNvcmRfc2VxKS4gQWNjb3VudCBsaWZlY3ljbGUgYWN0cyBhcmUgY
29uZmlybWF0aW9uLWdhdGVkCihTNy4yKTogdGhlIGNyZWF0ZS9mcmVlemUvY2xvc2UgcHJpbWFyeSBh
Y3QgcmV0dXJucyBwZW5kaW5nX2NvbmZpcm1hdGlvbgp3aXRoIGEgc2luZ2xlLXVzZSByZWY7IHRoZSB
jb25maXJtIGFjdCBleGVjdXRlcyB0aGUgd3JpdGUuIENvbnN1bXB0aW9uIGlzCmxlZGdlci1kZXJpdm
VkIG92ZXIgdGhlIGF1ZGl0IHRyYWlsIG9mIHRoaXMgbW9kdWxlJ3Mgb3duIHBlbmRpbmcgcmVnaXN0c
nkKdGFibGUtZnJlZSBkZXNpZ246IHRoZSBwZW5kaW5nIHJlZiBpcyBoZWxkIGluIHRoZSBhdWRpdCBl
dmVudCBhbmQKcmUtZGVyaXZlZCDigJQgdjEga2VlcHMgaXQgc2ltcGxlcjogdGhlIHByaW1hcnkgYWN
0IHN0b3JlcyBOT1RISU5HIGFuZApyZXR1cm5zIHRoZSByZWY7IHRoZSBjb25maXJtIGFjdCBjYXJyaW
VzIHRoZSBmdWxsIHBheWxvYWQgKyByZWYgYW5kIHRoZQp3cml0ZXIgdmVyaWZpZXMgdGhlIHJlZiB3Y
XMgbWludGVkIGZvciBleGFjdGx5IHRoYXQgcGF5bG9hZCAoSE1BQy1mcmVlCmRldGVybWluaXN0aWMg
ZGlnZXN0IOKAlCBubyBzZWNyZXQsIE4xKS4KIiIiCgpmcm9tIF9fZnV0dXJlX18gaW1wb3J0IGFubm9
0YXRpb25zCgppbXBvcnQgaGFzaGxpYgppbXBvcnQganNvbgoKZnJvbSBzcWxhbGNoZW15IGltcG9ydC
BzZWxlY3QKZnJvbSBzcWxhbGNoZW15LmV4dC5hc3luY2lvIGltcG9ydCBBc3luY1Nlc3Npb24KCmZyb
20gYXBwLmRiLm1vZGVscy52Ml9wYXBlcl90cmFkaW5nIGltcG9ydCBWMlBhcGVyQWNjb3VudApmcm9t
IGFwcC52Mi5wYXBlcl90cmFkaW5nLmNvbnRyYWN0cyBpbXBvcnQgKAogICAgQUNDT1VOVF9TVEFURVM
sCiAgICBCQVNFX0NVUlJFTkNJRVNfVjEsCiAgICBQYXBlck91dGNvbWUsCikKZnJvbSBhcHAudjIucG
FwZXJfdHJhZGluZy5vcmRlcnMgaW1wb3J0IGF1ZGl0CgoKZGVmIF9jYW5vbmljYWwob2JqKSAtPiBzd
HI6CiAgICByZXR1cm4ganNvbi5kdW1wcyhvYmosIHNvcnRfa2V5cz1UcnVlLCBzZXBhcmF0b3JzPSgi
LCIsICI6IiksIGRlZmF1bHQ9c3RyKQoKCmRlZiBtaW50X2NvbmZpcm1hdGlvbl9yZWYocGF5bG9hZDo
gZGljdCkgLT4gc3RyOgogICAgIiIiRGV0ZXJtaW5pc3RpYyBzaW5nbGUtdXNlIHJlZiBib3VuZCB0by
B0aGUgZXhhY3QgcGF5bG9hZCAobm8gc2VjcmV0KS4iIiIKICAgIHJldHVybiAicGNvbmYtIiArIGhhc
2hsaWIuc2hhMjU2KAogICAgICAgIF9jYW5vbmljYWwocGF5bG9hZCkuZW5jb2RlKCkpLmhleGRpZ2Vz
dCgpWzozMl0KCgphc3luYyBkZWYgcmVxdWVzdF9hY2NvdW50X2FjdGlvbigKICAgIHNlc3Npb246IEF
zeW5jU2Vzc2lvbiwgKiwgYWN0aW9uOiBzdHIsIHBheWxvYWQ6IGRpY3QsIG1vZGU6IHN0ciwKICAgIG
9wZXJhdG9yX2lkOiBzdHIsIGNvcnJlbGF0aW9uX2lkOiBzdHIgfCBOb25lLAopIC0+IFBhcGVyT3V0Y
29tZToKICAgICIiIlByaW1hcnkgYWN0OiB2YWxpZGF0ZXMgYW5kIHJldHVybnMgcGVuZGluZ19jb25m
aXJtYXRpb24gKyByZWYuIiIiCiAgICByZWFzb25zOiBsaXN0ID0gW10KICAgIGlmIGFjdGlvbiA9PSA
iY3JlYXRlIjoKICAgICAgICBpZiBwYXlsb2FkLmdldCgiYmFzZV9jdXJyZW5jeSIpIG5vdCBpbiBCQV
NFX0NVUlJFTkNJRVNfVjE6CiAgICAgICAgICAgIHJlYXNvbnMuYXBwZW5kKHsiZmFpbGluZyI6ICJiY
XNlX2N1cnJlbmN5IiwKICAgICAgICAgICAgICAgICAgICAgICAgICAgICJhbGxvd2VkIjogbGlzdChC
QVNFX0NVUlJFTkNJRVNfVjEpfSkKICAgICAgICB0cnk6CiAgICAgICAgICAgIGlmIGZsb2F0KHBheWx
vYWQuZ2V0KCJpbml0aWFsX2JhbGFuY2UiLCAiMCIpKSA8PSAwOgogICAgICAgICAgICAgICAgcmVhc2
9ucy5hcHBlbmQoeyJmYWlsaW5nIjogImluaXRpYWxfYmFsYW5jZSIsCiAgICAgICAgICAgICAgICAgI
CAgICAgICAgICAgICAgIm5vdGUiOiAibXVzdCBiZSBwb3NpdGl2ZSJ9KQogICAgICAgIGV4Y2VwdCAo
VHlwZUVycm9yLCBWYWx1ZUVycm9yKToKICAgICAgICAgICAgcmVhc29ucy5hcHBlbmQoeyJmYWlsaW5
nIjogImluaXRpYWxfYmFsYW5jZSIsCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAibm90ZSI6IC
Jub3QgYSBkZWNpbWFsIn0pCiAgICBpZiByZWFzb25zOgogICAgICAgIGF3YWl0IGF1ZGl0KHNlc3Npb
24sICJwYXBlci5hY2NvdW50LnJlcXVlc3RfcmVmdXNlZCIsCiAgICAgICAgICAgICAgICAgICAgZGV0
YWlscz17ImFjdGlvbiI6IGFjdGlvbiwgInJlYXNvbnMiOiByZWFzb25zfSwKICAgICAgICAgICAgICA
gICAgICBtb2RlPW1vZGUsIG9wZXJhdG9yX2lkPW9wZXJhdG9yX2lkLAogICAgICAgICAgICAgICAgIC
AgIGNvcnJlbGF0aW9uX2lkPWNvcnJlbGF0aW9uX2lkLAogICAgICAgICAgICAgICAgICAgIHJlc291c
mNlX3R5cGU9InBhcGVyX2FjY291bnQiKQogICAgICAgIGF3YWl0IHNlc3Npb24uY29tbWl0KCkKICAg
ICAgICByZXR1cm4gUGFwZXJPdXRjb21lKG91dGNvbWU9InJlZnVzZWQiLCByZWFzb25zPXJlYXNvbnM
pCiAgICByZWYgPSBtaW50X2NvbmZpcm1hdGlvbl9yZWYoeyJhY3Rpb24iOiBhY3Rpb24sICoqcGF5bG
9hZH0pCiAgICBhd2FpdCBhdWRpdChzZXNzaW9uLCAicGFwZXIuYWNjb3VudC5jb25maXJtYXRpb25fc
mVxdWVzdGVkIiwKICAgICAgICAgICAgICAgIGRldGFpbHM9eyJhY3Rpb24iOiBhY3Rpb24sICJjb25m
aXJtYXRpb25fcmVmIjogcmVmfSwKICAgICAgICAgICAgICAgIG1vZGU9bW9kZSwgb3BlcmF0b3JfaWQ
9b3BlcmF0b3JfaWQsCiAgICAgICAgICAgICAgICBjb3JyZWxhdGlvbl9pZD1jb3JyZWxhdGlvbl9pZC
wKICAgICAgICAgICAgICAgIHJlc291cmNlX3R5cGU9InBhcGVyX2FjY291bnQiKQogICAgcmV0dXJuI
FBhcGVyT3V0Y29tZShvdXRjb21lPSJwZW5kaW5nX2NvbmZpcm1hdGlvbiIsIHJlYXNvbnM9W10sCiAg
ICAgICAgICAgICAgICAgICAgICAgIGNvbmZpcm1hdGlvbl9yZWY9cmVmKQoKCmFzeW5jIGRlZiBjb25
maXJtX2FjY291bnRfYWN0aW9uKAogICAgc2Vzc2lvbjogQXN5bmNTZXNzaW9uLCAqLCBhY3Rpb246IH
N0ciwgcGF5bG9hZDogZGljdCwKICAgIGNvbmZpcm1hdGlvbl9yZWY6IHN0ciwgYWN0b3JfaWQ6IHN0c
iwgbW9kZTogc3RyLCBvcGVyYXRvcl9pZDogc3RyLAogICAgY29ycmVsYXRpb25faWQ6IHN0ciB8IE5v
bmUsIGRhdGFfY2xhc3M6IHN0ciwKKSAtPiBQYXBlck91dGNvbWU6CiAgICAiIiJDb25maXJtIGFjdDo
gdmVyaWZpZXMgdGhlIHJlZiBiaW5kcyB0aGUgZXhhY3QgcGF5bG9hZCwgdGhlbiB3cml0ZXMuIiIiCi
AgICBleHBlY3RlZCA9IG1pbnRfY29uZmlybWF0aW9uX3JlZih7ImFjdGlvbiI6IGFjdGlvbiwgKipwY
Xlsb2FkfSkKICAgIGlmIGNvbmZpcm1hdGlvbl9yZWYgIT0gZXhwZWN0ZWQ6CiAgICAgICAgYXdhaXQg
YXVkaXQoc2Vzc2lvbiwgInBhcGVyLmFjY291bnQuY29uZmlybV9yZWZ1c2VkIiwKICAgICAgICAgICA
gICAgICAgICBkZXRhaWxzPXsicmVmdXNhbF9jbGFzcyI6CiAgICAgICAgICAgICAgICAgICAgICAgIC
AgICAgInBhcGVyLmNvbmZpcm1hdGlvbi5yZWZfbWlzbWF0Y2giLAogICAgICAgICAgICAgICAgICAgI
CAgICAgICAgICJhY3Rpb24iOiBhY3Rpb259LAogICAgICAgICAgICAgICAgICAgIG1vZGU9bW9kZSwg
b3BlcmF0b3JfaWQ9b3BlcmF0b3JfaWQsCiAgICAgICAgICAgICAgICAgICAgY29ycmVsYXRpb25faWQ
9Y29ycmVsYXRpb25faWQsCiAgICAgICAgICAgICAgICAgICAgcmVzb3VyY2VfdHlwZT0icGFwZXJfYW
Njb3VudCIpCiAgICAgICAgYXdhaXQgc2Vzc2lvbi5jb21taXQoKQogICAgICAgIHJldHVybiBQYXBlc
k91dGNvbWUob3V0Y29tZT0icmVmdXNlZCIsIHJlYXNvbnM9WwogICAgICAgICAgICB7ImZhaWxpbmci
OiAicGFwZXIuY29uZmlybWF0aW9uLnJlZl9taXNtYXRjaCJ9XSkKCiAgICBhY2NvdW50X2lkID0gcGF
5bG9hZFsiYWNjb3VudF9pZCJdCiAgICBuZXdlc3QgPSAoYXdhaXQgc2Vzc2lvbi5leGVjdXRlKAogIC
AgICAgIHNlbGVjdChWMlBhcGVyQWNjb3VudCkKICAgICAgICAud2hlcmUoVjJQYXBlckFjY291bnQuY
WNjb3VudF9pZCA9PSBhY2NvdW50X2lkKQogICAgICAgIC5vcmRlcl9ieShWMlBhcGVyQWNjb3VudC5y
ZWNvcmRfc2VxLmRlc2MoKSkKICAgICkpLnNjYWxhcnMoKS5maXJzdCgpCgogICAgaWYgYWN0aW9uID0
9ICJjcmVhdGUiOgogICAgICAgIGlmIG5ld2VzdCBpcyBub3QgTm9uZToKICAgICAgICAgICAgYXdhaX
QgYXVkaXQoc2Vzc2lvbiwgInBhcGVyLmFjY291bnQuY29uZmlybV9yZWZ1c2VkIiwKICAgICAgICAgI
CAgICAgICAgICAgICAgZGV0YWlscz17InJlZnVzYWxfY2xhc3MiOgogICAgICAgICAgICAgICAgICAg
ICAgICAgICAgICAgICAicGFwZXIuY29uZmlybWF0aW9uLmFscmVhZHlfY29uc3VtZWQiLAogICAgICA
gICAgICAgICAgICAgICAgICAgICAgICAgICAibm90ZSI6ICJhY2NvdW50IGV4aXN0cyJ9LAogICAgIC
AgICAgICAgICAgICAgICAgICBtb2RlPW1vZGUsIG9wZXJhdG9yX2lkPW9wZXJhdG9yX2lkLAogICAgI
CAgICAgICAgICAgICAgICAgICBjb3JyZWxhdGlvbl9pZD1jb3JyZWxhdGlvbl9pZCwKICAgICAgICAg
ICAgICAgICAgICAgICAgcmVzb3VyY2VfdHlwZT0icGFwZXJfYWNjb3VudCIpCiAgICAgICAgICAgIGF
3YWl0IHNlc3Npb24uY29tbWl0KCkKICAgICAgICAgICAgcmV0dXJuIFBhcGVyT3V0Y29tZShvdXRjb2
1lPSJyZWZ1c2VkIiwgcmVhc29ucz1bCiAgICAgICAgICAgICAgICB7ImZhaWxpbmciOiAicGFwZXIuY
29uZmlybWF0aW9uLmFscmVhZHlfY29uc3VtZWQiLAogICAgICAgICAgICAgICAgICJub3RlIjogImFj
Y291bnQgYWxyZWFkeSBleGlzdHMgKHNpbmdsZS11c2UgcmVmIGNvbnN1bWVkKSJ9XSkKICAgICAgICB
yb3cgPSBWMlBhcGVyQWNjb3VudCgKICAgICAgICAgICAgYWNjb3VudF9pZD1hY2NvdW50X2lkLCByZW
NvcmRfc2VxPTEsIHN1cGVyc2VkZXM9Tm9uZSwKICAgICAgICAgICAgbmFtZT1wYXlsb2FkWyJuYW1lI
l0sIGJhc2VfY3VycmVuY3k9cGF5bG9hZFsiYmFzZV9jdXJyZW5jeSJdLAogICAgICAgICAgICBpbml0
aWFsX2JhbGFuY2U9c3RyKHBheWxvYWRbImluaXRpYWxfYmFsYW5jZSJdKSwKICAgICAgICAgICAgbWF
yZ2luX3BhcmFtcz1wYXlsb2FkLmdldCgibWFyZ2luX3BhcmFtcyIsIHt9KSwKICAgICAgICAgICAgbG
lmZWN5Y2xlX3N0YXRlPSJhY3RpdmUiLCBjb25maXJtYXRpb25fcmVmPWNvbmZpcm1hdGlvbl9yZWYsC
iAgICAgICAgICAgIGRhdGFfY2xhc3M9ZGF0YV9jbGFzcywgbW9kZT1tb2RlLCBvcGVyYXRvcl9pZD1v
cGVyYXRvcl9pZCwKICAgICAgICAgICAgY29ycmVsYXRpb25faWQ9Y29ycmVsYXRpb25faWQpCiAgICA
gICAgc2Vzc2lvbi5hZGQocm93KQogICAgICAgIGF3YWl0IHNlc3Npb24uZmx1c2goKQogICAgICAgIG
F3YWl0IGF1ZGl0KHNlc3Npb24sICJwYXBlci5hY2NvdW50LmNyZWF0ZWQiLAogICAgICAgICAgICAgI
CAgICAgIGRldGFpbHM9eyJhY2NvdW50X2lkIjogYWNjb3VudF9pZCwKICAgICAgICAgICAgICAgICAg
ICAgICAgICAgICAiY29uZmlybWF0aW9uX3JlZiI6IGNvbmZpcm1hdGlvbl9yZWZ9LAogICAgICAgICA
gICAgICAgICAgIG1vZGU9bW9kZSwgb3BlcmF0b3JfaWQ9b3BlcmF0b3JfaWQsCiAgICAgICAgICAgIC
AgICAgICAgY29ycmVsYXRpb25faWQ9Y29ycmVsYXRpb25faWQsCiAgICAgICAgICAgICAgICAgICAgc
mVzb3VyY2VfdHlwZT0icGFwZXJfYWNjb3VudCIsIHJlc291cmNlX2lkPXJvdy5pZCkKICAgICAgICBy
ZXR1cm4gUGFwZXJPdXRjb21lKG91dGNvbWU9ImFwcGxpZWQiLCByZWFzb25zPVtdLCByZWNvcmRfaWQ
9cm93LmlkKQoKICAgICMgZnJlZXplIC8gY2xvc2U6IHN1cGVyc2VkZSB3aXRoIHRoZSBuZXcgbGlmZW
N5Y2xlIHN0YXRlLgogICAgdGFyZ2V0X3N0YXRlID0geyJmcmVlemUiOiAiZnJvemVuIiwgImNsb3NlI
jogImNsb3NlZCJ9LmdldChhY3Rpb24pCiAgICBpZiB0YXJnZXRfc3RhdGUgaXMgTm9uZSBvciB0YXJn
ZXRfc3RhdGUgbm90IGluIEFDQ09VTlRfU1RBVEVTOgogICAgICAgIGF3YWl0IHNlc3Npb24uY29tbWl
0KCkKICAgICAgICByZXR1cm4gUGFwZXJPdXRjb21lKG91dGNvbWU9InJlZnVzZWQiLCByZWFzb25zPV
sKICAgICAgICAgICAgeyJmYWlsaW5nIjogImFjdGlvbiIsICJ2YWx1ZSI6IGFjdGlvbn1dKQogICAga
WYgbmV3ZXN0IGlzIE5vbmU6CiAgICAgICAgYXdhaXQgc2Vzc2lvbi5jb21taXQoKQogICAgICAgIHJl
dHVybiBQYXBlck91dGNvbWUob3V0Y29tZT0icmVmdXNlZCIsIHJlYXNvbnM9WwogICAgICAgICAgICB
7ImZhaWxpbmciOiAiYWNjb3VudF9pZCIsICJub3RlIjogInVua25vd24gYWNjb3VudCJ9XSkKICAgIH
JvdyA9IFYyUGFwZXJBY2NvdW50KAogICAgICAgIGFjY291bnRfaWQ9YWNjb3VudF9pZCwgcmVjb3JkX
3NlcT1uZXdlc3QucmVjb3JkX3NlcSArIDEsCiAgICAgICAgc3VwZXJzZWRlcz1uZXdlc3QuaWQsIG5h
bWU9bmV3ZXN0Lm5hbWUsCiAgICAgICAgYmFzZV9jdXJyZW5jeT1uZXdlc3QuYmFzZV9jdXJyZW5jeSw
KICAgICAgICBpbml0aWFsX2JhbGFuY2U9bmV3ZXN0LmluaXRpYWxfYmFsYW5jZSwKICAgICAgICBtYX
JnaW5fcGFyYW1zPW5ld2VzdC5tYXJnaW5fcGFyYW1zLAogICAgICAgIGxpZmVjeWNsZV9zdGF0ZT10Y
XJnZXRfc3RhdGUsIGNvbmZpcm1hdGlvbl9yZWY9Y29uZmlybWF0aW9uX3JlZiwKICAgICAgICBkYXRh
X2NsYXNzPWRhdGFfY2xhc3MsIG1vZGU9bW9kZSwgb3BlcmF0b3JfaWQ9b3BlcmF0b3JfaWQsCiAgICA
gICAgY29ycmVsYXRpb25faWQ9Y29ycmVsYXRpb25faWQpCiAgICBzZXNzaW9uLmFkZChyb3cpCiAgIC
Bhd2FpdCBzZXNzaW9uLmZsdXNoKCkKICAgIGF3YWl0IGF1ZGl0KHNlc3Npb24sIGYicGFwZXIuYWNjb
3VudC57YWN0aW9ufWQiLAogICAgICAgICAgICAgICAgZGV0YWlscz17ImFjY291bnRfaWQiOiBhY2Nv
dW50X2lkLAogICAgICAgICAgICAgICAgICAgICAgICAgImNvbmZpcm1hdGlvbl9yZWYiOiBjb25maXJ
tYXRpb25fcmVmfSwKICAgICAgICAgICAgICAgIG1vZGU9bW9kZSwgb3BlcmF0b3JfaWQ9b3BlcmF0b3
JfaWQsCiAgICAgICAgICAgICAgICBjb3JyZWxhdGlvbl9pZD1jb3JyZWxhdGlvbl9pZCwKICAgICAgI
CAgICAgICAgIHJlc291cmNlX3R5cGU9InBhcGVyX2FjY291bnQiLCByZXNvdXJjZV9pZD1yb3cuaWQp
CiAgICByZXR1cm4gUGFwZXJPdXRjb21lKG91dGNvbWU9ImFwcGxpZWQiLCByZWFzb25zPVtdLCByZWN
vcmRfaWQ9cm93LmlkKQoKCmFzeW5jIGRlZiBjdXJyZW50X2FjY291bnQoc2Vzc2lvbjogQXN5bmNTZX
NzaW9uLAogICAgICAgICAgICAgICAgICAgICAgICAgIGFjY291bnRfaWQ6IHN0cikgLT4gVjJQYXBlc
kFjY291bnQgfCBOb25lOgogICAgIiIiQ3VycmVuY3kgbGF3OiBncmVhdGVzdCByZWNvcmRfc2VxIGlz
IHRoZSBjdXJyZW50IGdlbmVyYXRpb24uIiIiCiAgICByZXR1cm4gKGF3YWl0IHNlc3Npb24uZXhlY3V
0ZSgKICAgICAgICBzZWxlY3QoVjJQYXBlckFjY291bnQpCiAgICAgICAgLndoZXJlKFYyUGFwZXJBY2
NvdW50LmFjY291bnRfaWQgPT0gYWNjb3VudF9pZCkKICAgICAgICAub3JkZXJfYnkoVjJQYXBlckFjY
291bnQucmVjb3JkX3NlcS5kZXNjKCkpCiAgICApKS5zY2FsYXJzKCkuZmlyc3QoKQo=
'@
$LandPath = Join-Path $BackendRoot "app\v2\paper_trading\accounts.py"
New-Item -ItemType Directory -Force -Path (Split-Path $LandPath) | Out-Null
if (Test-Path $LandPath) {
    $Cur = (Get-FileHash -Path $LandPath -Algorithm SHA256).Hash.ToLower()
    if ($Cur -eq "0e54f4c2c38d66a4d386d34574fc9625f9cc4d045fc92f814a1167e3a40b40ef") { Write-Evidence ("pre-landing witnessed (already pinned bytes): app\v2\paper_trading\accounts.py") }
    else { throw ("STOP (A4 FOREIGN-STATE ADJUDICATION LAW): new-file target exists with foreign bytes: " + $LandPath + " sha " + $Cur + " . Nothing modified for this file; report to ITRGA.") }
} else {
    [IO.File]::WriteAllBytes($LandPath, (B64-Decode -B64Chunk $Fapp_v2_paper_trading_accounts_py))
    $Cur = (Get-FileHash -Path $LandPath -Algorithm SHA256).Hash.ToLower()
    if ($Cur -ne "0e54f4c2c38d66a4d386d34574fc9625f9cc4d045fc92f814a1167e3a40b40ef") { throw ("FAIL: post-write hash drift on " + $LandPath) }
    Write-Evidence ("landed + verified: app\v2\paper_trading\accounts.py")
}

# file: app\v2\paper_trading\orders.py  (pin af1ad32afc69...)
$Fapp_v2_paper_trading_orders_py = @'
IiIiQkUtOCBvcmRlciBsaWZlY3ljbGUgd3JpdGVycyAoZGVzaWduIFMyOyBCTyBULTUvVC03L1QtOC9
ULTkpLgoKWmVyby1VUERBVEUgcmVnaW1lOiBzdGF0ZSBsaXZlcyBPTkxZIGluIHRoZSBhcHBlbmQtb2
5seSBldmVudCBsZWRnZXI7CmN1cnJlbnQgc3RhdGUgPSB0b19zdGF0ZSBvZiBtYXggZXZlbnRfaW5kZ
XggKFMyLjMgZGVyaXZhdGlvbiBsYXcpLgpUaGUgUzIuNi9DLTFhIGRlcml2ZWQgcnVsZSBgbWF5X2V4
ZWN1dGVgIGlzIG93bmVkIEhFUkUsIG9uY2UsIGFuZApjb25zdW1lZCBieSB0aGUgcnVuIHdyaXRlciB
hbmQgYnkgdGVzdHMg4oCUIG5vIGR1cGxpY2F0ZWQgbG9naWMuCiIiIgoKZnJvbSBfX2Z1dHVyZV9fIG
ltcG9ydCBhbm5vdGF0aW9ucwoKZnJvbSBzcWxhbGNoZW15IGltcG9ydCBzZWxlY3QKZnJvbSBzcWxhb
GNoZW15LmV4dC5hc3luY2lvIGltcG9ydCBBc3luY1Nlc3Npb24KCmZyb20gYXBwLmRiLm1vZGVscy52
Ml9wYXBlcl90cmFkaW5nIGltcG9ydCAoCiAgICBWMlBhcGVyT3JkZXJFdmVudCwKICAgIFYyUGFwZXJ
PcmRlckludGVudCwKICAgIFYyUGFwZXJSaXNrRGVjaXNpb24sCikKZnJvbSBhcHAudjIuYXVkaXQuY2
9udHJhY3QgaW1wb3J0IFYyQXVkaXRFdmVudENyZWF0ZQpmcm9tIGFwcC52Mi5hdWRpdC5yZXBvc2l0b
3J5IGltcG9ydCBWMkF1ZGl0UmVwb3NpdG9yeQpmcm9tIGFwcC52Mi5wYXBlcl90cmFkaW5nLmNvbnRy
YWN0cyBpbXBvcnQgKAogICAgTEVHQUxfVFJBTlNJVElPTlMsCiAgICBURVJNSU5BTF9TVEFURVMsCiA
gICBQYXBlck91dGNvbWUsCikKCl9ET01BSU4gPSAidjIucGFwZXJfdHJhZGluZyIKCgphc3luYyBkZW
YgYXVkaXQoc2Vzc2lvbjogQXN5bmNTZXNzaW9uLCBhY3Rpb246IHN0ciwgKiwgZGV0YWlsczogZGljd
CwKICAgICAgICAgICAgICAgIG1vZGU6IHN0ciwgb3BlcmF0b3JfaWQ6IHN0ciwgY29ycmVsYXRpb25f
aWQ6IHN0ciB8IE5vbmUsCiAgICAgICAgICAgICAgICByZXNvdXJjZV90eXBlOiBzdHIgPSAicGFwZXJ
fb3JkZXIiLAogICAgICAgICAgICAgICAgcmVzb3VyY2VfaWQ6IHN0ciB8IE5vbmUgPSBOb25lKSAtPi
BOb25lOgogICAgYXdhaXQgVjJBdWRpdFJlcG9zaXRvcnkoc2Vzc2lvbikuYXBwZW5kKFYyQXVkaXRFd
mVudENyZWF0ZSgKICAgICAgICBkb21haW49X0RPTUFJTiwgYWN0aW9uPWFjdGlvbiwgYWN0b3JfaWQ9
b3BlcmF0b3JfaWQsCiAgICAgICAgYWN0b3JfdHlwZT0ib3BlcmF0b3IiLCBtb2RlPW1vZGUsIHJlc29
1cmNlX3R5cGU9cmVzb3VyY2VfdHlwZSwKICAgICAgICByZXNvdXJjZV9pZD1yZXNvdXJjZV9pZCwgZG
V0YWlscz1kZXRhaWxzLCBvcGVyYXRvcl9pZD1vcGVyYXRvcl9pZCwKICAgICAgICBjb3JyZWxhdGlvb
l9pZD1jb3JyZWxhdGlvbl9pZCkpCgoKYXN5bmMgZGVmIGN1cnJlbnRfc3RhdGUoc2Vzc2lvbjogQXN5
bmNTZXNzaW9uLCBpbnRlbnRfcm93X2lkOiBzdHIpIC0+IHN0cjoKICAgICIiIlMyLjM6IHRoZSB0b19
zdGF0ZSBvZiB0aGUgbWF4IGV2ZW50X2luZGV4IOKAlCBhIHF1ZXJ5LCBub3QgYSBjb2x1bW4uIiIiCi
AgICBsYXRlc3QgPSAoYXdhaXQgc2Vzc2lvbi5leGVjdXRlKAogICAgICAgIHNlbGVjdChWMlBhcGVyT
3JkZXJFdmVudCkKICAgICAgICAud2hlcmUoVjJQYXBlck9yZGVyRXZlbnQuaW50ZW50X2lkID09IGlu
dGVudF9yb3dfaWQpCiAgICAgICAgLm9yZGVyX2J5KFYyUGFwZXJPcmRlckV2ZW50LmV2ZW50X2luZGV
4LmRlc2MoKSkKICAgICkpLnNjYWxhcnMoKS5maXJzdCgpCiAgICByZXR1cm4gbGF0ZXN0LnRvX3N0YX
RlIGlmIGxhdGVzdCBpcyBub3QgTm9uZSBlbHNlICJkcmFmdCIKCgphc3luYyBkZWYgYXBwZW5kX2V2Z
W50KHNlc3Npb246IEFzeW5jU2Vzc2lvbiwgKiwgaW50ZW50X3Jvd19pZDogc3RyLAogICAgICAgICAg
ICAgICAgICAgICAgIGZyb21fc3RhdGU6IHN0ciwgdG9fc3RhdGU6IHN0ciwgZXZlbnRfY2xhc3M6IHN
0ciwKICAgICAgICAgICAgICAgICAgICAgICBkZXRhaWxzOiBkaWN0LCBhY3Rvcl9pZDogc3RyLCBtb2
RlOiBzdHIsCiAgICAgICAgICAgICAgICAgICAgICAgb3BlcmF0b3JfaWQ6IHN0ciwgY29ycmVsYXRpb
25faWQ6IHN0ciB8IE5vbmUsCiAgICAgICAgICAgICAgICAgICAgICAgZGF0YV9jbGFzczogc3RyKSAt
PiBQYXBlck91dGNvbWU6CiAgICAiIiJUaGUgT05MWSBzdGF0ZS1hZHZhbmNpbmcgd3JpdGVyLiBSZWZ
1c2VzIGlsbGVnYWwgdHJhbnNpdGlvbnMgdHlwZWQuIiIiCiAgICBpZiAoZnJvbV9zdGF0ZSwgdG9fc3
RhdGUpIG5vdCBpbiBMRUdBTF9UUkFOU0lUSU9OUzoKICAgICAgICBhd2FpdCBhdWRpdChzZXNzaW9uL
CAicGFwZXIub3JkZXIudHJhbnNpdGlvbl9yZWZ1c2VkIiwKICAgICAgICAgICAgICAgICAgICBkZXRh
aWxzPXsiZnJvbSI6IGZyb21fc3RhdGUsICJ0byI6IHRvX3N0YXRlLAogICAgICAgICAgICAgICAgICA
gICAgICAgICAgICJub3RlIjogImFic2VudCBmcm9tIExFR0FMX1RSQU5TSVRJT05TIn0sCiAgICAgIC
AgICAgICAgICAgICAgbW9kZT1tb2RlLCBvcGVyYXRvcl9pZD1vcGVyYXRvcl9pZCwKICAgICAgICAgI
CAgICAgICAgICBjb3JyZWxhdGlvbl9pZD1jb3JyZWxhdGlvbl9pZCwKICAgICAgICAgICAgICAgICAg
ICByZXNvdXJjZV9pZD1pbnRlbnRfcm93X2lkKQogICAgICAgIGF3YWl0IHNlc3Npb24uY29tbWl0KCk
gICMgQy0xIGR1cmFibGUtcmVmdXNhbCBsYXcKICAgICAgICByZXR1cm4gUGFwZXJPdXRjb21lKG91dG
NvbWU9InJlZnVzZWQiLCByZWFzb25zPVsKICAgICAgICAgICAgeyJmYWlsaW5nIjogInRyYW5zaXRpb
24iLCAiZnJvbSI6IGZyb21fc3RhdGUsICJ0byI6IHRvX3N0YXRlfV0pCiAgICBvYnNlcnZlZCA9IGF3
YWl0IGN1cnJlbnRfc3RhdGUoc2Vzc2lvbiwgaW50ZW50X3Jvd19pZCkKICAgIGlmIG9ic2VydmVkICE
9IGZyb21fc3RhdGU6CiAgICAgICAgYXdhaXQgYXVkaXQoc2Vzc2lvbiwgInBhcGVyLm9yZGVyLnRyYW
5zaXRpb25fcmVmdXNlZCIsCiAgICAgICAgICAgICAgICAgICAgZGV0YWlscz17ImV4cGVjdGVkX2Zyb
20iOiBmcm9tX3N0YXRlLAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICJvYnNlcnZlZCI6IG9i
c2VydmVkLCAidG8iOiB0b19zdGF0ZX0sCiAgICAgICAgICAgICAgICAgICAgbW9kZT1tb2RlLCBvcGV
yYXRvcl9pZD1vcGVyYXRvcl9pZCwKICAgICAgICAgICAgICAgICAgICBjb3JyZWxhdGlvbl9pZD1jb3
JyZWxhdGlvbl9pZCwKICAgICAgICAgICAgICAgICAgICByZXNvdXJjZV9pZD1pbnRlbnRfcm93X2lkK
QogICAgICAgIGF3YWl0IHNlc3Npb24uY29tbWl0KCkKICAgICAgICByZXR1cm4gUGFwZXJPdXRjb21l
KG91dGNvbWU9InJlZnVzZWQiLCByZWFzb25zPVsKICAgICAgICAgICAgeyJmYWlsaW5nIjogImN1cnJ
lbnRfc3RhdGUiLCAib2JzZXJ2ZWQiOiBvYnNlcnZlZCwKICAgICAgICAgICAgICJleHBlY3RlZCI6IG
Zyb21fc3RhdGV9XSkKICAgIGxhdGVzdCA9IChhd2FpdCBzZXNzaW9uLmV4ZWN1dGUoCiAgICAgICAgc
2VsZWN0KFYyUGFwZXJPcmRlckV2ZW50KQogICAgICAgIC53aGVyZShWMlBhcGVyT3JkZXJFdmVudC5p
bnRlbnRfaWQgPT0gaW50ZW50X3Jvd19pZCkKICAgICAgICAub3JkZXJfYnkoVjJQYXBlck9yZGVyRXZ
lbnQuZXZlbnRfaW5kZXguZGVzYygpKQogICAgKSkuc2NhbGFycygpLmZpcnN0KCkKICAgIG5leHRfaW
5kZXggPSAwIGlmIGxhdGVzdCBpcyBOb25lIGVsc2UgbGF0ZXN0LmV2ZW50X2luZGV4ICsgMQogICAgc
m93ID0gVjJQYXBlck9yZGVyRXZlbnQoCiAgICAgICAgaW50ZW50X2lkPWludGVudF9yb3dfaWQsIGV2
ZW50X2luZGV4PW5leHRfaW5kZXgsCiAgICAgICAgZnJvbV9zdGF0ZT1mcm9tX3N0YXRlLCB0b19zdGF
0ZT10b19zdGF0ZSwgZXZlbnRfY2xhc3M9ZXZlbnRfY2xhc3MsCiAgICAgICAgZGV0YWlscz1kZXRhaW
xzLCBhY3Rvcl9pZD1hY3Rvcl9pZCwgZGF0YV9jbGFzcz1kYXRhX2NsYXNzLAogICAgICAgIG1vZGU9b
W9kZSwgb3BlcmF0b3JfaWQ9b3BlcmF0b3JfaWQsIGNvcnJlbGF0aW9uX2lkPWNvcnJlbGF0aW9uX2lk
KQogICAgc2Vzc2lvbi5hZGQocm93KQogICAgYXdhaXQgc2Vzc2lvbi5mbHVzaCgpCiAgICByZXR1cm4
gUGFwZXJPdXRjb21lKG91dGNvbWU9ImFwcGxpZWQiLCByZWFzb25zPVtdLCByZWNvcmRfaWQ9cm93Lm
lkKQoKCmFzeW5jIGRlZiBtYXlfZXhlY3V0ZShzZXNzaW9uOiBBc3luY1Nlc3Npb24sIGludGVudF9yb
3dfaWQ6IHN0cikgLT4gdHVwbGVbYm9vbCwgbGlzdF06CiAgICAiIiJUSEUgc2luZ2xlIGRlcml2ZWQg
ZXhlY3V0aW5nLXByZWNvbmRpdGlvbiBydWxlIChTMi42L0MtMWEpLCBvd25lZCBvbmNlLgoKICAgIFR
ydWUgaWZmOiBkZWNpc2lvbj0ncGFzcycsIE9SIChkZWNpc2lvbj0naG9sZCcgQU5EIGEgaG9sZC5jb2
5maXJtZWQKICAgIGV2ZW50IGNpdGluZyB0aGUgZGVjaXNpb24ncyBleGFjdCBjb25maXJtYXRpb25fc
mVmIGV4aXN0cyBBTkQgbm8KICAgIGhvbGQuY2FuY2VsbGVkIGV2ZW50IGV4aXN0cykuIEFsbCBvdGhl
ciBjYXNlczogKEZhbHNlLCByZWFzb25zKS4KICAgICIiIgogICAgZGVjaXNpb24gPSAoYXdhaXQgc2V
zc2lvbi5leGVjdXRlKAogICAgICAgIHNlbGVjdChWMlBhcGVyUmlza0RlY2lzaW9uKQogICAgICAgIC
53aGVyZShWMlBhcGVyUmlza0RlY2lzaW9uLmludGVudF9pZCA9PSBpbnRlbnRfcm93X2lkKQogICAgK
Skuc2NhbGFyX29uZV9vcl9ub25lKCkKICAgIGlmIGRlY2lzaW9uIGlzIE5vbmU6CiAgICAgICAgcmV0
dXJuIEZhbHNlLCBbeyJmYWlsaW5nIjogInJpc2tfZGVjaXNpb24iLCAibm90ZSI6ICJhYnNlbnQifV0
KICAgIGlmIGRlY2lzaW9uLmRlY2lzaW9uID09ICJwYXNzIjoKICAgICAgICByZXR1cm4gVHJ1ZSwgW1
0KICAgIGlmIGRlY2lzaW9uLmRlY2lzaW9uID09ICJibG9jayI6CiAgICAgICAgcmV0dXJuIEZhbHNlL
CBbeyJmYWlsaW5nIjogInJpc2tfZGVjaXNpb24iLCAidmFsdWUiOiAiYmxvY2siLAogICAgICAgICAg
ICAgICAgICAgICAgICAibm90ZSI6ICJ0ZXJtaW5hbDsgbm8gY29uZmlybWF0aW9uIHBhdGggKEMtMWQ
pIn1dCiAgICAjIGRlY2lzaW9uID09ICdob2xkJwogICAgZXZlbnRzID0gbGlzdCgoYXdhaXQgc2Vzc2
lvbi5leGVjdXRlKAogICAgICAgIHNlbGVjdChWMlBhcGVyT3JkZXJFdmVudCkKICAgICAgICAud2hlc
mUoVjJQYXBlck9yZGVyRXZlbnQuaW50ZW50X2lkID09IGludGVudF9yb3dfaWQpCiAgICApKS5zY2Fs
YXJzKCkuYWxsKCkpCiAgICBjYW5jZWxsZWQgPSBhbnkoZS5ldmVudF9jbGFzcyA9PSAiaG9sZC5jYW5
jZWxsZWQiIGZvciBlIGluIGV2ZW50cykKICAgIGlmIGNhbmNlbGxlZDoKICAgICAgICByZXR1cm4gRm
Fsc2UsIFt7ImZhaWxpbmciOiAiaG9sZCIsICJub3RlIjogImNhbmNlbGxlZCJ9XQogICAgY29uZmlyb
WVkID0gYW55KAogICAgICAgIGUuZXZlbnRfY2xhc3MgPT0gImhvbGQuY29uZmlybWVkIgogICAgICAg
IGFuZCBlLmRldGFpbHMuZ2V0KCJjb25maXJtYXRpb25fcmVmIikgPT0gZGVjaXNpb24uY29uZmlybWF
0aW9uX3JlZgogICAgICAgIGZvciBlIGluIGV2ZW50cykKICAgIGlmIGNvbmZpcm1lZDoKICAgICAgIC
ByZXR1cm4gVHJ1ZSwgW10KICAgIHJldHVybiBGYWxzZSwgW3siZmFpbGluZyI6ICJob2xkIiwgIm5vd
GUiOiAidW5yZXNvbHZlZCJ9XQoKCmFzeW5jIGRlZiBjb25maXJtYXRpb25fc3RhdHVzKHNlc3Npb246
IEFzeW5jU2Vzc2lvbiwKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgaW50ZW50X3Jvd19pZDo
gc3RyKSAtPiB0dXBsZVtzdHIsIHN0ciB8IE5vbmVdOgogICAgIiIiQy0xYiBjb25zdW1wdGlvbiBkZX
JpdmF0aW9uOiAoJ25vbmUnfCdvcGVuJ3wnY29uZmlybWVkJ3wnY2FuY2VsbGVkJywKICAgIHRoZSBta
W50ZWQgcmVmIG9yIE5vbmUpLiBMZWRnZXItZGVyaXZlZDsgbm8gbXV0YWJsZSBtYXJrZXIgZXhpc3Rz
LiIiIgogICAgZGVjaXNpb24gPSAoYXdhaXQgc2Vzc2lvbi5leGVjdXRlKAogICAgICAgIHNlbGVjdCh
WMlBhcGVyUmlza0RlY2lzaW9uKQogICAgICAgIC53aGVyZShWMlBhcGVyUmlza0RlY2lzaW9uLmludG
VudF9pZCA9PSBpbnRlbnRfcm93X2lkKQogICAgKSkuc2NhbGFyX29uZV9vcl9ub25lKCkKICAgIGlmI
GRlY2lzaW9uIGlzIE5vbmUgb3IgZGVjaXNpb24uZGVjaXNpb24gIT0gImhvbGQiOgogICAgICAgIHJl
dHVybiAibm9uZSIsIE5vbmUKICAgIGV2ZW50cyA9IGxpc3QoKGF3YWl0IHNlc3Npb24uZXhlY3V0ZSg
KICAgICAgICBzZWxlY3QoVjJQYXBlck9yZGVyRXZlbnQpCiAgICAgICAgLndoZXJlKFYyUGFwZXJPcm
RlckV2ZW50LmludGVudF9pZCA9PSBpbnRlbnRfcm93X2lkKQogICAgKSkuc2NhbGFycygpLmFsbCgpK
QogICAgZm9yIGUgaW4gZXZlbnRzOgogICAgICAgIGlmIGUuZXZlbnRfY2xhc3MgPT0gImhvbGQuY2Fu
Y2VsbGVkIjoKICAgICAgICAgICAgcmV0dXJuICJjYW5jZWxsZWQiLCBkZWNpc2lvbi5jb25maXJtYXR
pb25fcmVmCiAgICBmb3IgZSBpbiBldmVudHM6CiAgICAgICAgaWYgKGUuZXZlbnRfY2xhc3MgPT0gIm
hvbGQuY29uZmlybWVkIgogICAgICAgICAgICAgICAgYW5kIGUuZGV0YWlscy5nZXQoImNvbmZpcm1hd
Glvbl9yZWYiKQogICAgICAgICAgICAgICAgPT0gZGVjaXNpb24uY29uZmlybWF0aW9uX3JlZik6CiAg
ICAgICAgICAgIHJldHVybiAiY29uZmlybWVkIiwgZGVjaXNpb24uY29uZmlybWF0aW9uX3JlZgogICA
gcmV0dXJuICJvcGVuIiwgZGVjaXNpb24uY29uZmlybWF0aW9uX3JlZgoKCmFzeW5jIGRlZiBjb25maX
JtX2hvbGQoc2Vzc2lvbjogQXN5bmNTZXNzaW9uLCAqLCBpbnRlbnRfcm93X2lkOiBzdHIsCiAgICAgI
CAgICAgICAgICAgICAgICAgc3VwcGxpZWRfcmVmOiBzdHIsIHJlc29sdmVfdG86IHN0ciwgYWN0b3Jf
aWQ6IHN0ciwKICAgICAgICAgICAgICAgICAgICAgICBtb2RlOiBzdHIsIG9wZXJhdG9yX2lkOiBzdHI
sCiAgICAgICAgICAgICAgICAgICAgICAgY29ycmVsYXRpb25faWQ6IHN0ciB8IE5vbmUsCiAgICAgIC
AgICAgICAgICAgICAgICAgZGF0YV9jbGFzczogc3RyKSAtPiBQYXBlck91dGNvbWU6CiAgICAiIiJUa
GUgQy0xYiBjb25maXJtL2NhbmNlbCB3cml0ZXIgd2l0aCB0aGUgZm91ciB0eXBlZCByZWZ1c2FsIGNs
YXNzZXMuCgogICAgcmVzb2x2ZV90bzogJ2NvbmZpcm0nIC0+IHJpc2tfaG9sZCAtPiByaXNrX3Bhc3N
lZCAoaG9sZC5jb25maXJtZWQpOwogICAgJ2NhbmNlbCcgLT4gcmlza19ob2xkIC0+IGNhbmNlbGxlZC
AoaG9sZC5jYW5jZWxsZWQpLgogICAgIiIiCiAgICBhc3luYyBkZWYgX3JlZnVzZShyZWZ1c2FsX2NsY
XNzOiBzdHIsIGV4dHJhOiBkaWN0KSAtPiBQYXBlck91dGNvbWU6CiAgICAgICAgYXdhaXQgYXVkaXQo
c2Vzc2lvbiwgInBhcGVyLm9yZGVyLmNvbmZpcm1fcmVmdXNlZCIsCiAgICAgICAgICAgICAgICAgICA
gZGV0YWlscz17InJlZnVzYWxfY2xhc3MiOiByZWZ1c2FsX2NsYXNzLCAqKmV4dHJhfSwKICAgICAgIC
AgICAgICAgICAgICBtb2RlPW1vZGUsIG9wZXJhdG9yX2lkPW9wZXJhdG9yX2lkLAogICAgICAgICAgI
CAgICAgICAgIGNvcnJlbGF0aW9uX2lkPWNvcnJlbGF0aW9uX2lkLAogICAgICAgICAgICAgICAgICAg
IHJlc291cmNlX2lkPWludGVudF9yb3dfaWQpCiAgICAgICAgYXdhaXQgc2Vzc2lvbi5jb21taXQoKSA
gIyBkdXJhYmxlIGRlc3BpdGUgcmVmdXNhbAogICAgICAgIHJldHVybiBQYXBlck91dGNvbWUob3V0Y2
9tZT0icmVmdXNlZCIsIHJlYXNvbnM9WwogICAgICAgICAgICB7ImZhaWxpbmciOiByZWZ1c2FsX2NsY
XNzLCAqKmV4dHJhfV0pCgogICAgZGVjaXNpb24gPSAoYXdhaXQgc2Vzc2lvbi5leGVjdXRlKAogICAg
ICAgIHNlbGVjdChWMlBhcGVyUmlza0RlY2lzaW9uKQogICAgICAgIC53aGVyZShWMlBhcGVyUmlza0R
lY2lzaW9uLmludGVudF9pZCA9PSBpbnRlbnRfcm93X2lkKQogICAgKSkuc2NhbGFyX29uZV9vcl9ub2
5lKCkKICAgIGlmIGRlY2lzaW9uIGlzIE5vbmUgb3IgZGVjaXNpb24uZGVjaXNpb24gIT0gImhvbGQiO
gogICAgICAgIHJldHVybiBhd2FpdCBfcmVmdXNlKCJwYXBlci5jb25maXJtYXRpb24ubm90X2NvbmZp
cm1hYmxlIiwgewogICAgICAgICAgICAiZGVjaXNpb24iOiBkZWNpc2lvbi5kZWNpc2lvbiBpZiBkZWN
pc2lvbiBlbHNlIE5vbmV9KQogICAgc3RhdHVzLCBtaW50ZWRfcmVmID0gYXdhaXQgY29uZmlybWF0aW
9uX3N0YXR1cyhzZXNzaW9uLCBpbnRlbnRfcm93X2lkKQogICAgaWYgc3RhdHVzID09ICJjYW5jZWxsZ
WQiOgogICAgICAgIHJldHVybiBhd2FpdCBfcmVmdXNlKCJwYXBlci5jb25maXJtYXRpb24uY2FuY2Vs
bGVkIiwge30pCiAgICBpZiBzdGF0dXMgPT0gImNvbmZpcm1lZCI6CiAgICAgICAgcmV0dXJuIGF3YWl
0IF9yZWZ1c2UoInBhcGVyLmNvbmZpcm1hdGlvbi5hbHJlYWR5X2NvbnN1bWVkIiwge30pCiAgICBpZi
BzdXBwbGllZF9yZWYgIT0gbWludGVkX3JlZjoKICAgICAgICByZXR1cm4gYXdhaXQgX3JlZnVzZSgic
GFwZXIuY29uZmlybWF0aW9uLnJlZl9taXNtYXRjaCIsIHt9KQoKICAgIGlmIHJlc29sdmVfdG8gPT0g
ImNvbmZpcm0iOgogICAgICAgIG91dGNvbWUgPSBhd2FpdCBhcHBlbmRfZXZlbnQoCiAgICAgICAgICA
gIHNlc3Npb24sIGludGVudF9yb3dfaWQ9aW50ZW50X3Jvd19pZCwKICAgICAgICAgICAgZnJvbV9zdG
F0ZT0icmlza19ob2xkIiwgdG9fc3RhdGU9InJpc2tfcGFzc2VkIiwKICAgICAgICAgICAgZXZlbnRfY
2xhc3M9ImhvbGQuY29uZmlybWVkIiwKICAgICAgICAgICAgZGV0YWlscz17ImNvbmZpcm1hdGlvbl9y
ZWYiOiBtaW50ZWRfcmVmLAogICAgICAgICAgICAgICAgICAgICAiY29uZmlybWVkX2J5IjogYWN0b3J
faWR9LAogICAgICAgICAgICBhY3Rvcl9pZD1hY3Rvcl9pZCwgbW9kZT1tb2RlLCBvcGVyYXRvcl9pZD
1vcGVyYXRvcl9pZCwKICAgICAgICAgICAgY29ycmVsYXRpb25faWQ9Y29ycmVsYXRpb25faWQsIGRhd
GFfY2xhc3M9ZGF0YV9jbGFzcykKICAgICAgICBhY3Rpb24gPSAicGFwZXIub3JkZXIuaG9sZF9jb25m
aXJtZWQiCiAgICBlbHNlOgogICAgICAgIG91dGNvbWUgPSBhd2FpdCBhcHBlbmRfZXZlbnQoCiAgICA
gICAgICAgIHNlc3Npb24sIGludGVudF9yb3dfaWQ9aW50ZW50X3Jvd19pZCwKICAgICAgICAgICAgZn
JvbV9zdGF0ZT0icmlza19ob2xkIiwgdG9fc3RhdGU9ImNhbmNlbGxlZCIsCiAgICAgICAgICAgIGV2Z
W50X2NsYXNzPSJob2xkLmNhbmNlbGxlZCIsCiAgICAgICAgICAgIGRldGFpbHM9eyJjb25maXJtYXRp
b25fcmVmIjogbWludGVkX3JlZiwKICAgICAgICAgICAgICAgICAgICAgImNhbmNlbGxlZF9ieSI6IGF
jdG9yX2lkfSwKICAgICAgICAgICAgYWN0b3JfaWQ9YWN0b3JfaWQsIG1vZGU9bW9kZSwgb3BlcmF0b3
JfaWQ9b3BlcmF0b3JfaWQsCiAgICAgICAgICAgIGNvcnJlbGF0aW9uX2lkPWNvcnJlbGF0aW9uX2lkL
CBkYXRhX2NsYXNzPWRhdGFfY2xhc3MpCiAgICAgICAgYWN0aW9uID0gInBhcGVyLm9yZGVyLmhvbGRf
Y2FuY2VsbGVkIgogICAgaWYgb3V0Y29tZS5yZWZ1c2VkOgogICAgICAgIHJldHVybiBvdXRjb21lCiA
gICBhd2FpdCBhdWRpdChzZXNzaW9uLCBhY3Rpb24sCiAgICAgICAgICAgICAgICBkZXRhaWxzPXsiY2
9uZmlybWF0aW9uX3JlZiI6IG1pbnRlZF9yZWZ9LAogICAgICAgICAgICAgICAgbW9kZT1tb2RlLCBvc
GVyYXRvcl9pZD1vcGVyYXRvcl9pZCwKICAgICAgICAgICAgICAgIGNvcnJlbGF0aW9uX2lkPWNvcnJl
bGF0aW9uX2lkLCByZXNvdXJjZV9pZD1pbnRlbnRfcm93X2lkKQogICAgcmV0dXJuIG91dGNvbWUKCgp
hc3luYyBkZWYgY2FuY2VsX29yZGVyKHNlc3Npb246IEFzeW5jU2Vzc2lvbiwgKiwgaW50ZW50X3Jvd1
9pZDogc3RyLAogICAgICAgICAgICAgICAgICAgICAgIGFjdG9yX2lkOiBzdHIsIG1vZGU6IHN0ciwgb
3BlcmF0b3JfaWQ6IHN0ciwKICAgICAgICAgICAgICAgICAgICAgICBjb3JyZWxhdGlvbl9pZDogc3Ry
IHwgTm9uZSwKICAgICAgICAgICAgICAgICAgICAgICBkYXRhX2NsYXNzOiBzdHIpIC0+IFBhcGVyT3V
0Y29tZToKICAgICIiIlByZS1leGVjdXRpb24gY2FuY2VsIG9ubHk7IHRlcm1pbmFsL2V4ZWN1dGluZy
A9IHR5cGVkIHJlZnVzYWwuIiIiCiAgICBzdGF0ZSA9IGF3YWl0IGN1cnJlbnRfc3RhdGUoc2Vzc2lvb
iwgaW50ZW50X3Jvd19pZCkKICAgIGlmIHN0YXRlIGluIFRFUk1JTkFMX1NUQVRFUyBvciBzdGF0ZSBp
biAoImV4ZWN1dGluZyIsICJmaWxsZWQiLAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICA
gICAgICAgICAgICAicGFydGlhbGx5X2ZpbGxlZCIsCiAgICAgICAgICAgICAgICAgICAgICAgICAgIC
AgICAgICAgICAgICAgICAgICJyaXNrX3Bhc3NlZCIpOgogICAgICAgIGF3YWl0IGF1ZGl0KHNlc3Npb
24sICJwYXBlci5vcmRlci5jYW5jZWxfcmVmdXNlZCIsCiAgICAgICAgICAgICAgICAgICAgZGV0YWls
cz17InN0YXRlIjogc3RhdGV9LCBtb2RlPW1vZGUsCiAgICAgICAgICAgICAgICAgICAgb3BlcmF0b3J
faWQ9b3BlcmF0b3JfaWQsIGNvcnJlbGF0aW9uX2lkPWNvcnJlbGF0aW9uX2lkLAogICAgICAgICAgIC
AgICAgICAgIHJlc291cmNlX2lkPWludGVudF9yb3dfaWQpCiAgICAgICAgYXdhaXQgc2Vzc2lvbi5jb
21taXQoKQogICAgICAgIHJldHVybiBQYXBlck91dGNvbWUob3V0Y29tZT0icmVmdXNlZCIsIHJlYXNv
bnM9WwogICAgICAgICAgICB7ImZhaWxpbmciOiAic3RhdGUiLCAidmFsdWUiOiBzdGF0ZSwKICAgICA
gICAgICAgICJub3RlIjogImNhbmNlbCBpcyBwcmUtcmlzay9wcmUtZXhlY3V0aW9uIG9ubHkifV0pCi
AgICBpZiBzdGF0ZSA9PSAicmlza19ob2xkIjoKICAgICAgICAjIGhvbGQtY2FuY2VsIGdvZXMgdGhyb
3VnaCB0aGUgQy0xIG1lY2hhbmlzbSwgbm90IHRoaXMgd3JpdGVyLgogICAgICAgIGF3YWl0IGF1ZGl0
KHNlc3Npb24sICJwYXBlci5vcmRlci5jYW5jZWxfcmVmdXNlZCIsCiAgICAgICAgICAgICAgICAgICA
gZGV0YWlscz17InN0YXRlIjogc3RhdGUsCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIm5vdG
UiOiAicmVzb2x2ZSBob2xkcyB2aWEgdGhlIGNvbmZpcm1hdGlvbiBhY3QifSwKICAgICAgICAgICAgI
CAgICAgICBtb2RlPW1vZGUsIG9wZXJhdG9yX2lkPW9wZXJhdG9yX2lkLAogICAgICAgICAgICAgICAg
ICAgIGNvcnJlbGF0aW9uX2lkPWNvcnJlbGF0aW9uX2lkLCByZXNvdXJjZV9pZD1pbnRlbnRfcm93X2l
kKQogICAgICAgIGF3YWl0IHNlc3Npb24uY29tbWl0KCkKICAgICAgICByZXR1cm4gUGFwZXJPdXRjb2
1lKG91dGNvbWU9InJlZnVzZWQiLCByZWFzb25zPVsKICAgICAgICAgICAgeyJmYWlsaW5nIjogInN0Y
XRlIiwgInZhbHVlIjogc3RhdGUsCiAgICAgICAgICAgICAibm90ZSI6ICJob2xkIHJlc29sdXRpb24g
dXNlcyB0aGUgY29uZmlybWF0aW9uIG1lY2hhbmlzbSJ9XSkKICAgIG91dGNvbWUgPSBhd2FpdCBhcHB
lbmRfZXZlbnQoCiAgICAgICAgc2Vzc2lvbiwgaW50ZW50X3Jvd19pZD1pbnRlbnRfcm93X2lkLCBmcm
9tX3N0YXRlPXN0YXRlLAogICAgICAgIHRvX3N0YXRlPSJjYW5jZWxsZWQiLCBldmVudF9jbGFzcz0ib
3JkZXIuY2FuY2VsbGVkIiwKICAgICAgICBkZXRhaWxzPXsiY2FuY2VsbGVkX2J5IjogYWN0b3JfaWR9
LCBhY3Rvcl9pZD1hY3Rvcl9pZCwgbW9kZT1tb2RlLAogICAgICAgIG9wZXJhdG9yX2lkPW9wZXJhdG9
yX2lkLCBjb3JyZWxhdGlvbl9pZD1jb3JyZWxhdGlvbl9pZCwKICAgICAgICBkYXRhX2NsYXNzPWRhdG
FfY2xhc3MpCiAgICBpZiBub3Qgb3V0Y29tZS5yZWZ1c2VkOgogICAgICAgIGF3YWl0IGF1ZGl0KHNlc
3Npb24sICJwYXBlci5vcmRlci5jYW5jZWxsZWQiLCBkZXRhaWxzPXt9LAogICAgICAgICAgICAgICAg
ICAgIG1vZGU9bW9kZSwgb3BlcmF0b3JfaWQ9b3BlcmF0b3JfaWQsCiAgICAgICAgICAgICAgICAgICA
gY29ycmVsYXRpb25faWQ9Y29ycmVsYXRpb25faWQsIHJlc291cmNlX2lkPWludGVudF9yb3dfaWQpCi
AgICByZXR1cm4gb3V0Y29tZQoKCmFzeW5jIGRlZiBnZXRfaW50ZW50KHNlc3Npb246IEFzeW5jU2Vzc
2lvbiwKICAgICAgICAgICAgICAgICAgICAgaW50ZW50X3Jvd19pZDogc3RyKSAtPiBWMlBhcGVyT3Jk
ZXJJbnRlbnQgfCBOb25lOgogICAgcmV0dXJuIChhd2FpdCBzZXNzaW9uLmV4ZWN1dGUoCiAgICAgICA
gc2VsZWN0KFYyUGFwZXJPcmRlckludGVudCkKICAgICAgICAud2hlcmUoVjJQYXBlck9yZGVySW50ZW
50LmlkID09IGludGVudF9yb3dfaWQpCiAgICApKS5zY2FsYXJfb25lX29yX25vbmUoKQo=
'@
$LandPath = Join-Path $BackendRoot "app\v2\paper_trading\orders.py"
New-Item -ItemType Directory -Force -Path (Split-Path $LandPath) | Out-Null
if (Test-Path $LandPath) {
    $Cur = (Get-FileHash -Path $LandPath -Algorithm SHA256).Hash.ToLower()
    if ($Cur -eq "af1ad32afc6953116a4b06289f3886dfd69442d6b2cbcd8f583b1bbdcfe87582") { Write-Evidence ("pre-landing witnessed (already pinned bytes): app\v2\paper_trading\orders.py") }
    else { throw ("STOP (A4 FOREIGN-STATE ADJUDICATION LAW): new-file target exists with foreign bytes: " + $LandPath + " sha " + $Cur + " . Nothing modified for this file; report to ITRGA.") }
} else {
    [IO.File]::WriteAllBytes($LandPath, (B64-Decode -B64Chunk $Fapp_v2_paper_trading_orders_py))
    $Cur = (Get-FileHash -Path $LandPath -Algorithm SHA256).Hash.ToLower()
    if ($Cur -ne "af1ad32afc6953116a4b06289f3886dfd69442d6b2cbcd8f583b1bbdcfe87582") { throw ("FAIL: post-write hash drift on " + $LandPath) }
    Write-Evidence ("landed + verified: app\v2\paper_trading\orders.py")
}

# file: app\v2\paper_trading\risk.py  (pin ea4abf270da2...)
$Fapp_v2_paper_trading_risk_py = @'
IiIiQkUtOCBwcmUtdHJhZGUgcmlzayBnYXRld2F5IChkZXNpZ24gUzM7IEJPIFQtOC9ULTkpLgoKRGV
mYXVsdC1kZW55OiBhbiBpbnRlbnQgd2l0aCBubyBkZWNpc2lvbiByb3cgY2Fubm90IHJlYWNoIGBleG
VjdXRpbmdgCihvcmRlcnMucHkgZW5mb3JjZXMgdGhlIFMyLjYgZGVyaXZlZCBydWxlKS4gRXhhY3Rse
S1vbmNlIGV2YWx1YXRpb24gaXMgYQpTQ0hFTUEgZmFjdCAodXEoaW50ZW50X2lkKSBvbiB2Ml9wYXBl
cl9yaXNrX2RlY2lzaW9uKS4gRXZlcnkgbGltaXQgaXMKbWVhc3VyZWQgYW5kIHJlY29yZGVkOiB7b2J
zZXJ2ZWQsIHRocmVzaG9sZCwgdmVyZGljdH0gcGVyIGxpbWl0IOKAlCBuZXZlcgphc3NlcnRlZC4gVG
hlIG1hcmdpbiBlbmdpbmUgKGxlZGdlci5weSkgY29tcHV0ZXM7IE9OTFkgdGhpcyBnYXRld2F5CmRlY
2lkZXMgKFE1IHNpbmdsZS1kZWNpc2lvbi1hdXRob3JpdHkgbGF3KS4KIiIiCgpmcm9tIF9fZnV0dXJl
X18gaW1wb3J0IGFubm90YXRpb25zCgpmcm9tIGRlY2ltYWwgaW1wb3J0IERlY2ltYWwKCmZyb20gYXB
wLnYyLnBhcGVyX3RyYWRpbmcuY29udHJhY3RzIGltcG9ydCAoCiAgICBSSVNLX0NPTkZJR19WMSwKIC
AgIFJJU0tfQ09ORklHX1ZFUlNJT05fVjEsCikKClNJTVVMQVRPUl9WRVJTSU9OID0gInB4cy0xLjAuM
CIKR0FURVdBWV9WRVJTSU9OID0gInByZy0xLjAuMCIKCgpkZWYgZXZhbHVhdGVfaW50ZW50KAogICAg
KiwKICAgIHF1YW50aXR5OiBEZWNpbWFsLAogICAgcmVmZXJlbmNlX3ByaWNlOiBEZWNpbWFsLAogICA
gYWNjb3VudF9zdGF0ZTogc3RyLAogICAgaW5zdHJ1bWVudF9rbm93bjogYm9vbCwKICAgIG1hcmdpbl
9hdmFpbGFibGU6IERlY2ltYWwsCiAgICBtYXJnaW5fcmVxdWlyZWQ6IERlY2ltYWwsCiAgICBjb25jZ
W50cmF0aW9uX2ZyYWN0aW9uOiBEZWNpbWFsLAogICAgc2Vzc2lvbl9pbnRlbnRfY291bnQ6IGludCwK
KSAtPiB0dXBsZVtzdHIsIGRpY3QsIGxpc3RdOgogICAgIiIiUHVyZSBkZWNpc2lvbiBmdW5jdGlvbi4
gUmV0dXJucyAoZGVjaXNpb24sIGV2YWx1YXRlZF9saW1pdHMsIHJlYXNvbnMpLgoKICAgIGRlY2lzaW
9uOiAncGFzcycgfCAnYmxvY2snIHwgJ2hvbGQnIChTMyBzZW1hbnRpY3M6IGJsb2NrIHRlcm1pbmFsI
HdpdGgKICAgIG5vIGNvbmZpcm1hdGlvbiBwYXRoOyBob2xkIHdoZW4gYSBsaW1pdCBpcyBpbnNpZGUg
aXRzIGRlY2xhcmVkCiAgICBjb25maXJtYXRpb24gYmFuZDsgcGFzcyBvdGhlcndpc2UpLgogICAgIiI
iCiAgICBjZmcgPSBSSVNLX0NPTkZJR19WMQogICAgbm90aW9uYWwgPSBxdWFudGl0eSAqIHJlZmVyZW
5jZV9wcmljZQogICAgbGltaXRzOiBkaWN0ID0ge30KICAgIHJlYXNvbnM6IGxpc3QgPSBbXQogICAga
G9sZF9yZWFzb25zOiBsaXN0ID0gW10KCiAgICBkZWYgX2NoZWNrKG5hbWU6IHN0ciwgb2JzZXJ2ZWQs
IHRocmVzaG9sZCwgb2s6IGJvb2wpIC0+IE5vbmU6CiAgICAgICAgbGltaXRzW25hbWVdID0geyJvYnN
lcnZlZCI6IHN0cihvYnNlcnZlZCksICJ0aHJlc2hvbGQiOiBzdHIodGhyZXNob2xkKSwKICAgICAgIC
AgICAgICAgICAgICAgICAgInZlcmRpY3QiOiAicGFzcyIgaWYgb2sgZWxzZSAiZmFpbCJ9CiAgICAgI
CAgaWYgbm90IG9rOgogICAgICAgICAgICByZWFzb25zLmFwcGVuZCh7ImZhaWxpbmciOiBuYW1lLCAi
b2JzZXJ2ZWQiOiBzdHIob2JzZXJ2ZWQpLAogICAgICAgICAgICAgICAgICAgICAgICAgICAgInRocmV
zaG9sZCI6IHN0cih0aHJlc2hvbGQpfSkKCiAgICBfY2hlY2soIm1heF9vcmRlcl9xdWFudGl0eSIsIH
F1YW50aXR5LCBjZmdbIm1heF9vcmRlcl9xdWFudGl0eSJdLAogICAgICAgICAgIHF1YW50aXR5IDw9I
GNmZ1sibWF4X29yZGVyX3F1YW50aXR5Il0pCiAgICBfY2hlY2soIm1heF9vcmRlcl9ub3Rpb25hbCIs
IG5vdGlvbmFsLCBjZmdbIm1heF9vcmRlcl9ub3Rpb25hbCJdLAogICAgICAgICAgIG5vdGlvbmFsIDw
9IGNmZ1sibWF4X29yZGVyX25vdGlvbmFsIl0pCiAgICBfY2hlY2soImluc3RydW1lbnRfYWxsb3dlZC
IsIGluc3RydW1lbnRfa25vd24sIFRydWUsIGluc3RydW1lbnRfa25vd24pCiAgICBfY2hlY2soImFjY
291bnRfYWN0aXZlIiwgYWNjb3VudF9zdGF0ZSwgImFjdGl2ZSIsCiAgICAgICAgICAgYWNjb3VudF9z
dGF0ZSA9PSAiYWN0aXZlIikKICAgIF9jaGVjaygic3VmZmljaWVudF9tYXJnaW4iLCBtYXJnaW5fcmV
xdWlyZWQsIG1hcmdpbl9hdmFpbGFibGUsCiAgICAgICAgICAgbWFyZ2luX3JlcXVpcmVkIDw9IG1hcm
dpbl9hdmFpbGFibGUpCiAgICBfY2hlY2soImNvbmNlbnRyYXRpb24iLCBjb25jZW50cmF0aW9uX2ZyY
WN0aW9uLAogICAgICAgICAgIGNmZ1sibWF4X2NvbmNlbnRyYXRpb25fZnJhY3Rpb24iXSwKICAgICAg
ICAgICBjb25jZW50cmF0aW9uX2ZyYWN0aW9uIDw9IGNmZ1sibWF4X2NvbmNlbnRyYXRpb25fZnJhY3R
pb24iXSkKICAgIF9jaGVjaygic2Vzc2lvbl9yYXRlIiwgc2Vzc2lvbl9pbnRlbnRfY291bnQsCiAgIC
AgICAgICAgY2ZnWyJtYXhfaW50ZW50c19wZXJfc2Vzc2lvbiJdLAogICAgICAgICAgIHNlc3Npb25fa
W50ZW50X2NvdW50IDwgY2ZnWyJtYXhfaW50ZW50c19wZXJfc2Vzc2lvbiJdKQoKICAgIGlmIHJlYXNv
bnM6CiAgICAgICAgcmV0dXJuICJibG9jayIsIGxpbWl0cywgcmVhc29ucwoKICAgICMgSG9sZCBiYW5
kOiBub3Rpb25hbCB3aXRoaW4gW2JhbmRfbG93ZXIgKiBtYXgsIG1heF0gKFMzKS4KICAgIGJhbmRfZm
xvb3IgPSBjZmdbIm1heF9vcmRlcl9ub3Rpb25hbCJdICogY2ZnWyJob2xkX2JhbmRfbG93ZXJfZnJhY
3Rpb24iXQogICAgaWYgbm90aW9uYWwgPj0gYmFuZF9mbG9vcjoKICAgICAgICBob2xkX3JlYXNvbnMu
YXBwZW5kKHsKICAgICAgICAgICAgImhvbGRpbmciOiAibWF4X29yZGVyX25vdGlvbmFsX2JhbmQiLAo
gICAgICAgICAgICAib2JzZXJ2ZWQiOiBzdHIobm90aW9uYWwpLAogICAgICAgICAgICAiYmFuZCI6IF
tzdHIoYmFuZF9mbG9vciksIHN0cihjZmdbIm1heF9vcmRlcl9ub3Rpb25hbCJdKV0sCiAgICAgICAgI
CAgICJub3RlIjogImNvbmZpcm1hdGlvbiBiYW5kIC0gaHVtYW4gY29uZmlybWF0aW9uIHJlcXVpcmVk
IChTNy4yKSIsCiAgICAgICAgfSkKICAgICAgICBsaW1pdHNbIm1heF9vcmRlcl9ub3Rpb25hbF9iYW5
kIl0gPSB7CiAgICAgICAgICAgICJvYnNlcnZlZCI6IHN0cihub3Rpb25hbCksCiAgICAgICAgICAgIC
J0aHJlc2hvbGQiOiBzdHIoYmFuZF9mbG9vciksICJ2ZXJkaWN0IjogImhvbGQifQogICAgICAgIHJld
HVybiAiaG9sZCIsIGxpbWl0cywgaG9sZF9yZWFzb25zCgogICAgcmV0dXJuICJwYXNzIiwgbGltaXRz
LCBbXQoKCmRlZiBjb25maWdfdmVyc2lvbigpIC0+IHN0cjoKICAgICIiIlRoZSB2ZXJzaW9uIHBpbm5
lZCBvbiBldmVyeSBkZWNpc2lvbiByb3cgKFMzIGdvdmVybmFuY2UpLiIiIgogICAgcmV0dXJuIFJJU0
tfQ09ORklHX1ZFUlNJT05fVjEK
'@
$LandPath = Join-Path $BackendRoot "app\v2\paper_trading\risk.py"
New-Item -ItemType Directory -Force -Path (Split-Path $LandPath) | Out-Null
if (Test-Path $LandPath) {
    $Cur = (Get-FileHash -Path $LandPath -Algorithm SHA256).Hash.ToLower()
    if ($Cur -eq "ea4abf270da2cea46cc66a3bbff32ce1bdae70b9a4b4ddbb25e73bb082375717") { Write-Evidence ("pre-landing witnessed (already pinned bytes): app\v2\paper_trading\risk.py") }
    else { throw ("STOP (A4 FOREIGN-STATE ADJUDICATION LAW): new-file target exists with foreign bytes: " + $LandPath + " sha " + $Cur + " . Nothing modified for this file; report to ITRGA.") }
} else {
    [IO.File]::WriteAllBytes($LandPath, (B64-Decode -B64Chunk $Fapp_v2_paper_trading_risk_py))
    $Cur = (Get-FileHash -Path $LandPath -Algorithm SHA256).Hash.ToLower()
    if ($Cur -ne "ea4abf270da2cea46cc66a3bbff32ce1bdae70b9a4b4ddbb25e73bb082375717") { throw ("FAIL: post-write hash drift on " + $LandPath) }
    Write-Evidence ("landed + verified: app\v2\paper_trading\risk.py")
}

# file: app\v2\paper_trading\simulator.py  (pin 4fb0d5586232...)
$Fapp_v2_paper_trading_simulator_py = @'
IiIiQkUtOCBwYXBlciBleGVjdXRpb24gc2ltdWxhdG9yIChkZXNpZ24gUzQ7IEJPIFQtNC9ULTYvVC0
xMCkuCgpEZXRlcm1pbmlzdGljIHNpbmdsZS1wYXNzIG92ZXIgYSBwaW5uZWQgc25hcHNob3QncyBiYX
JzOiBtYXJrZXQgb3JkZXJzCmZpbGwgYXQgdGhlIGZpcnN0IGJhciBjbG9zZTsgbGltaXQgb3JkZXJzI
HdoZW4gdG91Y2hlZCAobG93IDw9IGxpbWl0IGZvcgpidXlzLCBoaWdoID49IGxpbWl0IGZvciBzZWxs
cyk7IHBhcnRpYWwgZmlsbHMgd2hlbiBkZWNsYXJlZCBiYXIgbGlxdWlkaXR5CmlzIGJlbG93IHJlbWF
pbmluZyBxdWFudGl0eS4gQ29zdHMgdmlhIHRoZSBDUi1WMi1CRS03LTAwMSB1bml0IHZvY2FidWxhcn
kKKCdwcmljZScvJ2ZyYWN0aW9uJyk7IERlY2ltYWwgdGhyb3VnaG91dCAoUzUgbW9uZXkgbGF3KS4gV
GhlIHNlYW0gYWNjZXB0cwpPTkxZIFBhcGVyT3JkZXJJbnRlbnQgKFM2LjEpIOKAlCBubyBkaWN0LXNo
YXBlZCBvcmRlciBjYW4gY3Jvc3MuIFNuYXBzaG90CmNvbnRlbnQgaXMgcmUtdmVyaWZpZWQgYmVmb3J
lIGV4ZWN1dGlvbiAoRy01IGxpbmVhZ2U7IG1pc21hdGNoID0gdHlwZWQKcmVmdXNhbCwgbmV2ZXIgc2
lsZW50KS4KClJlcGxheSBjb250cmFjdCAoUzQuMyk6IChpbnRlbnQgKyBzbmFwc2hvdCBjb250ZW50I
Ghhc2ggKyBjb3N0IG1vZGVsICsKc2ltdWxhdG9yIHZlcnNpb24pIC0+IGJ5dGUtaWRlbnRpY2FsIGZp
bGxzLCB4My1hdHRlc3RlZCBpbiB0ZXN0cy4KIiIiCgpmcm9tIF9fZnV0dXJlX18gaW1wb3J0IGFubm9
0YXRpb25zCgppbXBvcnQgaGFzaGxpYgppbXBvcnQganNvbgpmcm9tIGRlY2ltYWwgaW1wb3J0IERlY2
ltYWwKCmZyb20gYXBwLnYyLnBhcGVyX3RyYWRpbmcuY29udHJhY3RzIGltcG9ydCAoCiAgICBDT1NUX
1VOSVRTX1YxLAogICAgUEFQRVJfRElTQ0xBSU1FUiwKICAgIFBhcGVyT3JkZXJJbnRlbnQsCiAgICBQ
YXBlclJlZnVzZWQsCikKClNJTVVMQVRPUl9WRVJTSU9OID0gInB4cy0xLjAuMCIKRU5HSU5FX1ZFUlN
JT05TID0geyJwYXBlcl9leGVjdXRpb25fc2ltdWxhdG9yIjogU0lNVUxBVE9SX1ZFUlNJT04sCiAgIC
AgICAgICAgICAgICAgICAicGFwZXJfcmlza19nYXRld2F5IjogInByZy0xLjAuMCJ9CgoKZGVmIGNhb
m9uaWNhbChvYmopIC0+IHN0cjoKICAgIHJldHVybiBqc29uLmR1bXBzKG9iaiwgc29ydF9rZXlzPVRy
dWUsIHNlcGFyYXRvcnM9KCIsIiwgIjoiKSwKICAgICAgICAgICAgICAgICAgICAgIGRlZmF1bHQ9c3R
yKQoKCmRlZiBlbmdpbmVfdmVyc2lvbnNfaGFzaCgpIC0+IHN0cjoKICAgIHJldHVybiBoYXNobGliLn
NoYTI1NihjYW5vbmljYWwoRU5HSU5FX1ZFUlNJT05TKS5lbmNvZGUoKSkuaGV4ZGlnZXN0KCkKCgpkZ
WYgc25hcHNob3RfY29udGVudF9oYXNoKGJhcnM6IGxpc3RbZGljdF0sIHNuYXBzaG90X3JlZjogc3Ry
KSAtPiBzdHI6CiAgICAiIiJDb250ZW50IGhhc2ggb3ZlciB0aGUgYmFyIHNldCArIHJlZiAoUzQuMSB
yZS12ZXJpZmljYXRpb24gbGF3KS4iIiIKICAgIHBheWxvYWQgPSBjYW5vbmljYWwoeyJzbmFwc2hvdF
9yZWYiOiBzbmFwc2hvdF9yZWYsICJiYXJzIjogYmFyc30pCiAgICByZXR1cm4gaGFzaGxpYi5zaGEyN
TYocGF5bG9hZC5lbmNvZGUoKSkuaGV4ZGlnZXN0KCkKCgpkZWYgYXBwbHlfY29zdHMoZmlsbF9wcmlj
ZTogRGVjaW1hbCwgc2lkZTogc3RyLCBjb3N0X21vZGVsOiBkaWN0KSAtPiBEZWNpbWFsOgogICAgIiI
iRWZmZWN0aXZlIHByaWNlIGFmdGVyIGRlY2xhcmVkIGNvc3RzIChDUi1WMi1CRS03LTAwMSB2b2NhYn
VsYXJ5KS4iIiIKICAgIHByaWNlID0gRGVjaW1hbChzdHIoZmlsbF9wcmljZSkpCiAgICBzaWduID0gR
GVjaW1hbCgxKSBpZiBzaWRlID09ICJidXkiIGVsc2UgRGVjaW1hbCgtMSkKICAgIGZvciBrZXkgaW4g
KCJzcHJlYWQiLCAiY29tbWlzc2lvbiIsICJzbGlwcGFnZSIpOgogICAgICAgIGVudHJ5ID0gY29zdF9
tb2RlbFtrZXldCiAgICAgICAgaWYgZW50cnlbInVuaXQiXSBub3QgaW4gQ09TVF9VTklUU19WMToKIC
AgICAgICAgICAgcmFpc2UgUGFwZXJSZWZ1c2VkKCJwYXBlci5jb3N0X3VuaXQudW5rbm93biIsIFsKI
CAgICAgICAgICAgICAgIHsiZmFpbGluZyI6IGYie2tleX0udW5pdCIsICJ2YWx1ZSI6IGVudHJ5WyJ1
bml0Il0sCiAgICAgICAgICAgICAgICAgImFsbG93ZWQiOiBsaXN0KENPU1RfVU5JVFNfVjEpfV0pCiA
gICAgICAgdmFsdWUgPSBEZWNpbWFsKHN0cihlbnRyeVsidmFsdWUiXSkpCiAgICAgICAgaWYgZW50cn
lbInVuaXQiXSA9PSAicHJpY2UiOgogICAgICAgICAgICBwcmljZSArPSBzaWduICogdmFsdWUKICAgI
CAgICBlbHNlOgogICAgICAgICAgICBwcmljZSAqPSAoRGVjaW1hbCgxKSArIHNpZ24gKiB2YWx1ZSkK
ICAgIHJldHVybiBwcmljZQoKCmRlZiBydW5fc2ltdWxhdGlvbigKICAgIGludGVudDogUGFwZXJPcmR
lckludGVudCwKICAgIGJhcnM6IGxpc3RbZGljdF0sCiAgICAqLAogICAgc3RvcmVkX2NvbnRlbnRfaG
FzaDogc3RyLAopIC0+IGRpY3Q6CiAgICAiIiJFeGVjdXRlIHRoZSBpbnRlbnQgZGV0ZXJtaW5pc3RpY
2FsbHkuIFR5cGVkIHNlYW06IFBhcGVyT3JkZXJJbnRlbnQgb25seS4KCiAgICBSZXR1cm5zIHtmaWxs
cywgb3V0Y29tZSwgZGlzY2xhaW1lciwgZW5naW5lX3ZlcnNpb25zLAogICAgZW5naW5lX3ZlcnNpb25
zX2hhc2gsIGJhcnNfcmVwbGF5ZWR9LiBvdXRjb21lOiAnZmlsbGVkJyB8CiAgICAncGFydGlhbGx5X2
ZpbGxlZCcgfCAnZXhwaXJlZCcuCiAgICAiIiIKICAgIGlmIG5vdCBpc2luc3RhbmNlKGludGVudCwgU
GFwZXJPcmRlckludGVudCk6ICAjIFM2LjEgdHlwZWQgc2VhbQogICAgICAgIHJhaXNlIFBhcGVyUmVm
dXNlZCgicGFwZXIuc2VhbS51bnR5cGVkIiwgWwogICAgICAgICAgICB7ImZhaWxpbmciOiAiaW50ZW5
0IiwgIm5vdGUiOgogICAgICAgICAgICAgInNpbXVsYXRvciBzZWFtIGFjY2VwdHMgUGFwZXJPcmRlck
ludGVudCBvbmx5In1dKQoKICAgIG9ic2VydmVkID0gc25hcHNob3RfY29udGVudF9oYXNoKGJhcnMsI
GludGVudC5zbmFwc2hvdF9yZWYpCiAgICBpZiBvYnNlcnZlZCAhPSBzdG9yZWRfY29udGVudF9oYXNo
OgogICAgICAgIHJhaXNlIFBhcGVyUmVmdXNlZCgicGFwZXIuc25hcHNob3QuY29udGVudF9taXNtYXR
jaCIsIFsKICAgICAgICAgICAgeyJmYWlsaW5nIjogInNuYXBzaG90X2NvbnRlbnRfaGFzaCIsCiAgIC
AgICAgICAgICAic3RvcmVkIjogc3RvcmVkX2NvbnRlbnRfaGFzaCwgIm9ic2VydmVkIjogb2JzZXJ2Z
WQsCiAgICAgICAgICAgICAibm90ZSI6ICJHLTUgbGluZWFnZSBsYXc6IHJlZnVzYWwsIG5ldmVyIHNp
bGVudCBpbmNsdXNpb24ifV0pCgogICAgcmVtYWluaW5nID0gRGVjaW1hbChzdHIoaW50ZW50LnF1YW5
0aXR5KSkKICAgIGZpbGxzOiBsaXN0W2RpY3RdID0gW10KICAgIGZpbGxfaW5kZXggPSAwCiAgICBmb3
IgYmFyIGluIGJhcnM6CiAgICAgICAgaWYgcmVtYWluaW5nIDw9IDA6CiAgICAgICAgICAgIGJyZWFrC
iAgICAgICAgY2xvc2UgPSBEZWNpbWFsKHN0cihiYXJbImNsb3NlIl0pKQogICAgICAgIGxvdyA9IERl
Y2ltYWwoc3RyKGJhclsibG93Il0pKQogICAgICAgIGhpZ2ggPSBEZWNpbWFsKHN0cihiYXJbImhpZ2g
iXSkpCiAgICAgICAgbGlxdWlkaXR5ID0gRGVjaW1hbChzdHIoYmFyLmdldCgibGlxdWlkaXR5Iiwgcm
VtYWluaW5nKSkpCgogICAgICAgIGlmIGludGVudC5vcmRlcl90eXBlID09ICJtYXJrZXQiOgogICAgI
CAgICAgICByYXcgPSBjbG9zZQogICAgICAgIGVsc2U6CiAgICAgICAgICAgIGxpbWl0ID0gRGVjaW1h
bChzdHIoaW50ZW50LmxpbWl0X3ByaWNlKSkKICAgICAgICAgICAgaWYgaW50ZW50LnNpZGUgPT0gImJ
1eSIgYW5kIGxvdyA8PSBsaW1pdDoKICAgICAgICAgICAgICAgIHJhdyA9IGxpbWl0CiAgICAgICAgIC
AgIGVsaWYgaW50ZW50LnNpZGUgPT0gInNlbGwiIGFuZCBoaWdoID49IGxpbWl0OgogICAgICAgICAgI
CAgICAgcmF3ID0gbGltaXQKICAgICAgICAgICAgZWxzZToKICAgICAgICAgICAgICAgIGNvbnRpbnVl
CgogICAgICAgIHF0eSA9IG1pbihyZW1haW5pbmcsIGxpcXVpZGl0eSkgaWYgbGlxdWlkaXR5ID4gMCB
lbHNlIHJlbWFpbmluZwogICAgICAgIGlmIHF0eSA8PSAwOgogICAgICAgICAgICBjb250aW51ZQogIC
AgICAgIGVmZmVjdGl2ZSA9IGFwcGx5X2Nvc3RzKHJhdywgaW50ZW50LnNpZGUsIGludGVudC5jb3N0X
21vZGVsKQogICAgICAgIGZpbGxzLmFwcGVuZCh7CiAgICAgICAgICAgICJmaWxsX2luZGV4IjogZmls
bF9pbmRleCwKICAgICAgICAgICAgInF1YW50aXR5Ijogc3RyKHF0eSksCiAgICAgICAgICAgICJyYXd
fcHJpY2UiOiBzdHIocmF3KSwKICAgICAgICAgICAgImVmZmVjdGl2ZV9wcmljZSI6IHN0cihlZmZlY3
RpdmUpLAogICAgICAgICAgICAiZmlsbF9jbGFzcyI6ICJwYXBlcl9zaW11bGF0ZWQiLCAgIyBONCDig
JQgdGhlIG9ubHkgdmFsdWUKICAgICAgICAgICAgInNpbXVsYXRvcl92ZXJzaW9uIjogU0lNVUxBVE9S
X1ZFUlNJT04sCiAgICAgICAgICAgICJiYXJfb3Blbl90aW1lIjogc3RyKGJhclsib3Blbl90aW1lIl0
pLAogICAgICAgIH0pCiAgICAgICAgcmVtYWluaW5nIC09IHF0eQogICAgICAgIGZpbGxfaW5kZXggKz
0gMQoKICAgIGlmIG5vdCBmaWxsczoKICAgICAgICBvdXRjb21lID0gImV4cGlyZWQiCiAgICBlbGlmI
HJlbWFpbmluZyA+IDA6CiAgICAgICAgb3V0Y29tZSA9ICJwYXJ0aWFsbHlfZmlsbGVkIgogICAgZWxz
ZToKICAgICAgICBvdXRjb21lID0gImZpbGxlZCIKCiAgICByZXR1cm4gewogICAgICAgICJmaWxscyI
6IGZpbGxzLAogICAgICAgICJvdXRjb21lIjogb3V0Y29tZSwKICAgICAgICAidW5maWxsZWRfcXVhbn
RpdHkiOiBzdHIocmVtYWluaW5nKSwKICAgICAgICAiYmFyc19yZXBsYXllZCI6IGxlbihiYXJzKSwKI
CAgICAgICAiZGlzY2xhaW1lciI6IFBBUEVSX0RJU0NMQUlNRVIsCiAgICAgICAgImVuZ2luZV92ZXJz
aW9ucyI6IGRpY3QoRU5HSU5FX1ZFUlNJT05TKSwKICAgICAgICAiZW5naW5lX3ZlcnNpb25zX2hhc2g
iOiBlbmdpbmVfdmVyc2lvbnNfaGFzaCgpLAogICAgfQo=
'@
$LandPath = Join-Path $BackendRoot "app\v2\paper_trading\simulator.py"
New-Item -ItemType Directory -Force -Path (Split-Path $LandPath) | Out-Null
if (Test-Path $LandPath) {
    $Cur = (Get-FileHash -Path $LandPath -Algorithm SHA256).Hash.ToLower()
    if ($Cur -eq "4fb0d5586232f73ccbdff29c2a18d35b8d5670d8a4c9d5d4b9cc48c44162a804") { Write-Evidence ("pre-landing witnessed (already pinned bytes): app\v2\paper_trading\simulator.py") }
    else { throw ("STOP (A4 FOREIGN-STATE ADJUDICATION LAW): new-file target exists with foreign bytes: " + $LandPath + " sha " + $Cur + " . Nothing modified for this file; report to ITRGA.") }
} else {
    [IO.File]::WriteAllBytes($LandPath, (B64-Decode -B64Chunk $Fapp_v2_paper_trading_simulator_py))
    $Cur = (Get-FileHash -Path $LandPath -Algorithm SHA256).Hash.ToLower()
    if ($Cur -ne "4fb0d5586232f73ccbdff29c2a18d35b8d5670d8a4c9d5d4b9cc48c44162a804") { throw ("FAIL: post-write hash drift on " + $LandPath) }
    Write-Evidence ("landed + verified: app\v2\paper_trading\simulator.py")
}

# file: app\v2\paper_trading\ledger.py  (pin 7a901f8145b4...)
$Fapp_v2_paper_trading_ledger_py = @'
IiIiQkUtOCBwb3NpdGlvbnMvYmFsYW5jZXMvbWFyZ2luL1AmTCBlbmdpbmUgKGRlc2lnbiBTNTsgQk8
gVC0xMS9ULTEyKS4KClB1cmUgZGVyaXZhdGlvbiBvdmVyIHRoZSBpbW11dGFibGUgZmlsbCBsZWRnZX
I6IHBvc2l0aW9ucyA9IHNpZ25lZCBmaWxsCnN1bXM7IGNhc2ggPSBpbml0aWFsIC0gYnV5cyArIHNlb
GxzOyBlcXVpdHkgPSBjYXNoICsgcG9zaXRpb24geCBtYXJrCihtYXJrID0gbGFzdCBjbG9zZSBPRiBU
SEUgUElOTkVEIFNOQVBTSE9UIOKAlCBuZXZlciBhIGxpdmUgcmVhZCk7IHJlYWxpemVkClAmTCBhdmV
yYWdlLWNvc3QgKEEtMyk7IG1hcmdpbiBlbmdpbmUgQ09NUFVURVMgT05MWSDigJQgdGhlIHJpc2sgZ2
F0ZXdheQpkZWNpZGVzIChRNSkuIERlY2ltYWwgZW5kLXRvLWVuZDsgVEVYVC1kZWNpbWFsIHN0b3JhZ
2U7IHJvdW5kaW5nIGF0CnByZXNlbnRhdGlvbiBvbmx5IChTNSBtb25leSBsYXcpLiBSZWNvbmNpbGlh
dGlvbiA9IGdlbmVzaXMgcmVjb21wdXRlICsKY29udGVudCBjb21wYXJpc29uIChQR0YtMDEyKTsgZGl
zY3JlcGFudCBpcyBhIHR5cGVkIGFsYXJtLCBuZXZlcgphdXRvLWNvcnJlY3RlZC4KIiIiCgpmcm9tIF
9fZnV0dXJlX18gaW1wb3J0IGFubm90YXRpb25zCgppbXBvcnQgaGFzaGxpYgppbXBvcnQganNvbgpmc
m9tIGRlY2ltYWwgaW1wb3J0IERlY2ltYWwKCmZyb20gYXBwLnYyLnBhcGVyX3RyYWRpbmcuY29udHJh
Y3RzIGltcG9ydCBSSVNLX0NPTkZJR19WMQoKCmRlZiBfY2Fub25pY2FsKG9iaikgLT4gc3RyOgogICA
gcmV0dXJuIGpzb24uZHVtcHMob2JqLCBzb3J0X2tleXM9VHJ1ZSwgc2VwYXJhdG9ycz0oIiwiLCAiOi
IpLCBkZWZhdWx0PXN0cikKCgpkZWYgZGVyaXZhdGlvbl9oYXNoKHBheWxvYWQ6IGRpY3QpIC0+IHN0c
joKICAgIHJldHVybiBoYXNobGliLnNoYTI1NihfY2Fub25pY2FsKHBheWxvYWQpLmVuY29kZSgpKS5o
ZXhkaWdlc3QoKQoKCmRlZiBkZXJpdmVfcG9zaXRpb25zKGZpbGxzOiBsaXN0W2RpY3RdKSAtPiBkaWN
0W3N0ciwgRGVjaW1hbF06CiAgICAiIiJpbnN0cnVtZW50IC0+IHNpZ25lZCBxdWFudGl0eSAoYnV5IC
ssIHNlbGwgLSkuIiIiCiAgICBwb3NpdGlvbnM6IGRpY3Rbc3RyLCBEZWNpbWFsXSA9IHt9CiAgICBmb
3IgZiBpbiBmaWxsczoKICAgICAgICBxdHkgPSBEZWNpbWFsKHN0cihmWyJxdWFudGl0eSJdKSkKICAg
ICAgICBzaWduZWQgPSBxdHkgaWYgZlsic2lkZSJdID09ICJidXkiIGVsc2UgLXF0eQogICAgICAgIGt
leSA9IGZbImluc3RydW1lbnRfaWQiXQogICAgICAgIHBvc2l0aW9uc1trZXldID0gcG9zaXRpb25zLm
dldChrZXksIERlY2ltYWwoMCkpICsgc2lnbmVkCiAgICByZXR1cm4ge2s6IHYgZm9yIGssIHYgaW4gc
G9zaXRpb25zLml0ZW1zKCkgaWYgdiAhPSAwfQoKCmRlZiBkZXJpdmVfY2FzaChpbml0aWFsX2JhbGFu
Y2U6IERlY2ltYWwsIGZpbGxzOiBsaXN0W2RpY3RdKSAtPiBEZWNpbWFsOgogICAgY2FzaCA9IERlY2l
tYWwoc3RyKGluaXRpYWxfYmFsYW5jZSkpCiAgICBmb3IgZiBpbiBmaWxsczoKICAgICAgICBxdHkgPS
BEZWNpbWFsKHN0cihmWyJxdWFudGl0eSJdKSkKICAgICAgICBweCA9IERlY2ltYWwoc3RyKGZbImVmZ
mVjdGl2ZV9wcmljZSJdKSkKICAgICAgICBpZiBmWyJzaWRlIl0gPT0gImJ1eSI6CiAgICAgICAgICAg
IGNhc2ggLT0gcXR5ICogcHgKICAgICAgICBlbHNlOgogICAgICAgICAgICBjYXNoICs9IHF0eSAqIHB
4CiAgICByZXR1cm4gY2FzaAoKCmRlZiBkZXJpdmVfcmVhbGl6ZWRfcG5sKGZpbGxzOiBsaXN0W2RpY3
RdKSAtPiBEZWNpbWFsOgogICAgIiIiQXZlcmFnZS1jb3N0IHJlYWxpemVkIFAmTCAoQS0zKSwgcGVyI
Gluc3RydW1lbnQsIGNocm9ub2xvZ2ljYWwuIiIiCiAgICByZWFsaXplZCA9IERlY2ltYWwoMCkKICAg
IGJvb2s6IGRpY3Rbc3RyLCBkaWN0XSA9IHt9CiAgICBmb3IgZiBpbiBmaWxsczoKICAgICAgICBrZXk
gPSBmWyJpbnN0cnVtZW50X2lkIl0KICAgICAgICBxdHkgPSBEZWNpbWFsKHN0cihmWyJxdWFudGl0eS
JdKSkKICAgICAgICBweCA9IERlY2ltYWwoc3RyKGZbImVmZmVjdGl2ZV9wcmljZSJdKSkKICAgICAgI
CBlbnRyeSA9IGJvb2suc2V0ZGVmYXVsdChrZXksIHsicXR5IjogRGVjaW1hbCgwKSwgImNvc3QiOiBE
ZWNpbWFsKDApfSkKICAgICAgICBwb3MsIGNvc3QgPSBlbnRyeVsicXR5Il0sIGVudHJ5WyJjb3N0Il0
KICAgICAgICBzaWduZWQgPSBxdHkgaWYgZlsic2lkZSJdID09ICJidXkiIGVsc2UgLXF0eQogICAgIC
AgIGlmIHBvcyA9PSAwIG9yIChwb3MgPiAwKSA9PSAoc2lnbmVkID4gMCk6CiAgICAgICAgICAgIGVud
HJ5WyJxdHkiXSA9IHBvcyArIHNpZ25lZAogICAgICAgICAgICBlbnRyeVsiY29zdCJdID0gY29zdCAr
IHNpZ25lZCAqIHB4CiAgICAgICAgZWxzZToKICAgICAgICAgICAgY2xvc2luZyA9IG1pbihhYnMoc2l
nbmVkKSwgYWJzKHBvcykpCiAgICAgICAgICAgIGF2ZyA9IGNvc3QgLyBwb3MgaWYgcG9zICE9IDAgZW
xzZSBEZWNpbWFsKDApCiAgICAgICAgICAgIGRpcmVjdGlvbiA9IERlY2ltYWwoMSkgaWYgcG9zID4gM
CBlbHNlIERlY2ltYWwoLTEpCiAgICAgICAgICAgIHJlYWxpemVkICs9IGNsb3NpbmcgKiAocHggLSBh
dmcpICogZGlyZWN0aW9uCiAgICAgICAgICAgIGVudHJ5WyJxdHkiXSA9IHBvcyArIHNpZ25lZAogICA
gICAgICAgICBlbnRyeVsiY29zdCJdID0gYXZnICogZW50cnlbInF0eSJdCiAgICByZXR1cm4gcmVhbG
l6ZWQKCgpkZWYgbWFyZ2luX3VzZWQocG9zaXRpb25zOiBkaWN0W3N0ciwgRGVjaW1hbF0sIG1hcmtzO
iBkaWN0W3N0ciwgRGVjaW1hbF0sCiAgICAgICAgICAgICAgICBtYXJnaW5fcGFyYW1zOiBkaWN0KSAt
PiBEZWNpbWFsOgogICAgIiIiQ29tcHV0ZXMgT05MWSAoUTUpOiBzdW0gfHBvc2l0aW9uIG5vdGlvbmF
sfCB4IG1hcmdpbl9yYXRlLiIiIgogICAgcmF0ZSA9IERlY2ltYWwoc3RyKG1hcmdpbl9wYXJhbXMuZ2
V0KAogICAgICAgICJtYXJnaW5fcmF0ZSIsIFJJU0tfQ09ORklHX1YxWyJtYXJnaW5fcmF0ZV9kZWZhd
Wx0Il0pKSkKICAgIHRvdGFsID0gRGVjaW1hbCgwKQogICAgZm9yIGluc3RydW1lbnQsIHF0eSBpbiBw
b3NpdGlvbnMuaXRlbXMoKToKICAgICAgICBtYXJrID0gbWFya3MuZ2V0KGluc3RydW1lbnQsIERlY2l
tYWwoMCkpCiAgICAgICAgdG90YWwgKz0gYWJzKHF0eSAqIG1hcmspICogcmF0ZQogICAgcmV0dXJuIH
RvdGFsCgoKZGVmIGRlcml2ZV9iYWxhbmNlKCosIGluaXRpYWxfYmFsYW5jZTogRGVjaW1hbCwgZmlsb
HM6IGxpc3RbZGljdF0sCiAgICAgICAgICAgICAgICAgICBtYXJrczogZGljdFtzdHIsIERlY2ltYWxd
LCBtYXJnaW5fcGFyYW1zOiBkaWN0KSAtPiBkaWN0OgogICAgcG9zaXRpb25zID0gZGVyaXZlX3Bvc2l
0aW9ucyhmaWxscykKICAgIGNhc2ggPSBkZXJpdmVfY2FzaChpbml0aWFsX2JhbGFuY2UsIGZpbGxzKQ
ogICAgdW5yZWFsaXplZCA9IERlY2ltYWwoMCkKICAgIGVxdWl0eSA9IGNhc2gKICAgIGJvb2tfY29zd
DogZGljdFtzdHIsIERlY2ltYWxdID0ge30KICAgIGZvciBmIGluIGZpbGxzOgogICAgICAgIGtleSA9
IGZbImluc3RydW1lbnRfaWQiXQogICAgICAgIHF0eSA9IERlY2ltYWwoc3RyKGZbInF1YW50aXR5Il0
pKQogICAgICAgIHB4ID0gRGVjaW1hbChzdHIoZlsiZWZmZWN0aXZlX3ByaWNlIl0pKQogICAgICAgIH
NpZ25lZCA9IHF0eSBpZiBmWyJzaWRlIl0gPT0gImJ1eSIgZWxzZSAtcXR5CiAgICAgICAgYm9va19jb
3N0W2tleV0gPSBib29rX2Nvc3QuZ2V0KGtleSwgRGVjaW1hbCgwKSkgKyBzaWduZWQgKiBweAogICAg
Zm9yIGluc3RydW1lbnQsIHF0eSBpbiBwb3NpdGlvbnMuaXRlbXMoKToKICAgICAgICBtYXJrID0gbWF
ya3MuZ2V0KGluc3RydW1lbnQsIERlY2ltYWwoMCkpCiAgICAgICAgZXF1aXR5ICs9IHF0eSAqIG1hcm
sKICAgICAgICBhdmcgPSAoYm9va19jb3N0LmdldChpbnN0cnVtZW50LCBEZWNpbWFsKDApKSAvIHF0e
SkgaWYgcXR5IGVsc2UgRGVjaW1hbCgwKQogICAgICAgIHVucmVhbGl6ZWQgKz0gcXR5ICogKG1hcmsg
LSBhdmcpCiAgICB1c2VkID0gbWFyZ2luX3VzZWQocG9zaXRpb25zLCBtYXJrcywgbWFyZ2luX3BhcmF
tcykKICAgIHJldHVybiB7CiAgICAgICAgInBvc2l0aW9ucyI6IHtrOiBzdHIodikgZm9yIGssIHYgaW
4gcG9zaXRpb25zLml0ZW1zKCl9LAogICAgICAgICJjYXNoIjogc3RyKGNhc2gpLAogICAgICAgICJlc
XVpdHkiOiBzdHIoZXF1aXR5KSwKICAgICAgICAibWFyZ2luX3VzZWQiOiBzdHIodXNlZCksCiAgICAg
ICAgIm1hcmdpbl9hdmFpbGFibGUiOiBzdHIoZXF1aXR5IC0gdXNlZCksCiAgICAgICAgInVucmVhbGl
6ZWRfcG5sIjogc3RyKHVucmVhbGl6ZWQpLAogICAgICAgICJyZWFsaXplZF9wbmwiOiBzdHIoZGVyaX
ZlX3JlYWxpemVkX3BubChmaWxscykpLAogICAgfQoKCmRlZiByZWNvbmNpbGUoKiwgc25hcHNob3Q6I
GRpY3QsIHJlY29tcHV0ZWQ6IGRpY3QpIC0+IHR1cGxlW3N0ciwgbGlzdF06CiAgICAiIiJHZW5lc2lz
IHJlY29tcHV0ZSB2cyBzdG9yZWQgc25hcHNob3Q7IGNvbnRlbnQgY29tcGFyaXNvbiAoUEdGLTAxMik
uCgogICAgUmV0dXJucyAob3V0Y29tZSwgZGlzY3JlcGFuY2llcykuIE5ldmVyIG11dGF0ZXMgYW55dG
hpbmcuCiAgICAiIiIKICAgIGRpc2NyZXBhbmNpZXM6IGxpc3QgPSBbXQogICAgZm9yIGZpZWxkIGluI
CgiY2FzaCIsICJlcXVpdHkiLCAibWFyZ2luX3VzZWQiLCAibWFyZ2luX2F2YWlsYWJsZSIsCiAgICAg
ICAgICAgICAgICAgICJ1bnJlYWxpemVkX3BubCIsICJyZWFsaXplZF9wbmwiKToKICAgICAgICBpZiB
EZWNpbWFsKHN0cihzbmFwc2hvdFtmaWVsZF0pKSAhPSBEZWNpbWFsKHN0cihyZWNvbXB1dGVkW2ZpZW
xkXSkpOgogICAgICAgICAgICBkaXNjcmVwYW5jaWVzLmFwcGVuZCh7CiAgICAgICAgICAgICAgICAiZ
mllbGQiOiBmaWVsZCwgInN0b3JlZCI6IHN0cihzbmFwc2hvdFtmaWVsZF0pLAogICAgICAgICAgICAg
ICAgInJlY29tcHV0ZWQiOiBzdHIocmVjb21wdXRlZFtmaWVsZF0pfSkKICAgIGlmIHNuYXBzaG90Lmd
ldCgicG9zaXRpb25zIikgIT0gcmVjb21wdXRlZC5nZXQoInBvc2l0aW9ucyIpOgogICAgICAgIGRpc2
NyZXBhbmNpZXMuYXBwZW5kKHsKICAgICAgICAgICAgImZpZWxkIjogInBvc2l0aW9ucyIsICJzdG9yZ
WQiOiBzbmFwc2hvdC5nZXQoInBvc2l0aW9ucyIpLAogICAgICAgICAgICAicmVjb21wdXRlZCI6IHJl
Y29tcHV0ZWQuZ2V0KCJwb3NpdGlvbnMiKX0pCiAgICByZXR1cm4gKCJjb25zaXN0ZW50IiBpZiBub3Q
gZGlzY3JlcGFuY2llcyBlbHNlICJkaXNjcmVwYW50IiwKICAgICAgICAgICAgZGlzY3JlcGFuY2llcy
kKCgpkZWYgcHJlc2VudGF0aW9uX3JvdW5kKHZhbHVlOiBEZWNpbWFsKSAtPiBzdHI6CiAgICAiIiJSb
3VuZGluZyBhdCBwcmVzZW50YXRpb24gT05MWSAoaGFsZi1ldmVuLCAyIGRwKSDigJQgUzUgbW9uZXkg
bGF3LiIiIgogICAgcmV0dXJuIHN0cih2YWx1ZS5xdWFudGl6ZShEZWNpbWFsKCIwLjAxIikpKQo=
'@
$LandPath = Join-Path $BackendRoot "app\v2\paper_trading\ledger.py"
New-Item -ItemType Directory -Force -Path (Split-Path $LandPath) | Out-Null
if (Test-Path $LandPath) {
    $Cur = (Get-FileHash -Path $LandPath -Algorithm SHA256).Hash.ToLower()
    if ($Cur -eq "7a901f8145b40aaaa80d3ef9c6c466be24ab55c7d290ede8887956dc86677138") { Write-Evidence ("pre-landing witnessed (already pinned bytes): app\v2\paper_trading\ledger.py") }
    else { throw ("STOP (A4 FOREIGN-STATE ADJUDICATION LAW): new-file target exists with foreign bytes: " + $LandPath + " sha " + $Cur + " . Nothing modified for this file; report to ITRGA.") }
} else {
    [IO.File]::WriteAllBytes($LandPath, (B64-Decode -B64Chunk $Fapp_v2_paper_trading_ledger_py))
    $Cur = (Get-FileHash -Path $LandPath -Algorithm SHA256).Hash.ToLower()
    if ($Cur -ne "7a901f8145b40aaaa80d3ef9c6c466be24ab55c7d290ede8887956dc86677138") { throw ("FAIL: post-write hash drift on " + $LandPath) }
    Write-Evidence ("landed + verified: app\v2\paper_trading\ledger.py")
}

# file: app\v2\paper_trading\reconciliation.py  (pin 74d7e70f89be...)
$Fapp_v2_paper_trading_reconciliation_py = @'
IiIiQkUtOCByZWNvbmNpbGlhdGlvbiB3cml0ZXIgKGRlc2lnbiBTNS9TMS4xIHJvdyA4OyBCTyBULTE
yKS4KCkdlbmVzaXMgcmVjb21wdXRlIG92ZXIgdGhlIGZ1bGwgZmlsbCBsZWRnZXIgdnMgdGhlIGxhdG
VzdCBzdG9yZWQgYmFsYW5jZQpzbmFwc2hvdDsgY29udGVudCBjb21wYXJpc29uIChQR0YtMDEyKTsgb
3V0Y29tZSByb3cgaW1tdXRhYmxlOyBkaXNjcmVwYW50CmlzIGEgdHlwZWQgYWxhcm0gc3VyZmFjZSDi
gJQgTkVWRVIgYXV0by1jb3JyZWN0ZWQuCiIiIgoKZnJvbSBfX2Z1dHVyZV9fIGltcG9ydCBhbm5vdGF
0aW9ucwoKZnJvbSBkZWNpbWFsIGltcG9ydCBEZWNpbWFsCgpmcm9tIHNxbGFsY2hlbXkgaW1wb3J0IH
NlbGVjdApmcm9tIHNxbGFsY2hlbXkuZXh0LmFzeW5jaW8gaW1wb3J0IEFzeW5jU2Vzc2lvbgoKZnJvb
SBhcHAuZGIubW9kZWxzLnYyX3BhcGVyX3RyYWRpbmcgaW1wb3J0ICgKICAgIFYyUGFwZXJCYWxhbmNl
U25hcHNob3QsCiAgICBWMlBhcGVyRmlsbCwKICAgIFYyUGFwZXJPcmRlckludGVudCwKICAgIFYyUGF
wZXJSZWNvbmNpbGlhdGlvbiwKKQpmcm9tIGFwcC52Mi5wYXBlcl90cmFkaW5nLmNvbnRyYWN0cyBpbX
BvcnQgUGFwZXJPdXRjb21lCmZyb20gYXBwLnYyLnBhcGVyX3RyYWRpbmcubGVkZ2VyIGltcG9ydCBkZ
XJpdmF0aW9uX2hhc2gsIGRlcml2ZV9iYWxhbmNlLCByZWNvbmNpbGUKZnJvbSBhcHAudjIucGFwZXJf
dHJhZGluZy5vcmRlcnMgaW1wb3J0IGF1ZGl0CgoKYXN5bmMgZGVmIGNvbGxlY3RfYWNjb3VudF9maWx
scyhzZXNzaW9uOiBBc3luY1Nlc3Npb24sCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgYW
Njb3VudF9yb3dfaWQ6IHN0cikgLT4gbGlzdFtkaWN0XToKICAgICIiIkFsbCBmaWxscyBmb3IgdGhlI
GFjY291bnQsIGNocm9ub2xvZ2ljYWwsIHdpdGggc2lkZS9pbnN0cnVtZW50LiIiIgogICAgaW50ZW50
cyA9IHsKICAgICAgICByb3cuaWQ6IHJvdwogICAgICAgIGZvciByb3cgaW4gKGF3YWl0IHNlc3Npb24
uZXhlY3V0ZSgKICAgICAgICAgICAgc2VsZWN0KFYyUGFwZXJPcmRlckludGVudCkKICAgICAgICAgIC
AgLndoZXJlKFYyUGFwZXJPcmRlckludGVudC5hY2NvdW50X2lkID09IGFjY291bnRfcm93X2lkKQogI
CAgICAgICkpLnNjYWxhcnMoKS5hbGwoKQogICAgfQogICAgaWYgbm90IGludGVudHM6CiAgICAgICAg
cmV0dXJuIFtdCiAgICBmaWxscyA9IGxpc3QoKGF3YWl0IHNlc3Npb24uZXhlY3V0ZSgKICAgICAgICB
zZWxlY3QoVjJQYXBlckZpbGwpCiAgICAgICAgLndoZXJlKFYyUGFwZXJGaWxsLmludGVudF9pZC5pbl
8obGlzdChpbnRlbnRzKSkpCiAgICAgICAgLm9yZGVyX2J5KFYyUGFwZXJGaWxsLmNyZWF0ZWRfYXQsI
FYyUGFwZXJGaWxsLmZpbGxfaW5kZXgpCiAgICApKS5zY2FsYXJzKCkuYWxsKCkpCiAgICBvdXQgPSBb
XQogICAgZm9yIGYgaW4gZmlsbHM6CiAgICAgICAgaW50ZW50ID0gaW50ZW50c1tmLmludGVudF9pZF0
KICAgICAgICBvdXQuYXBwZW5kKHsKICAgICAgICAgICAgImluc3RydW1lbnRfaWQiOiBpbnRlbnQuaW
5zdHJ1bWVudF9pZCwgInNpZGUiOiBpbnRlbnQuc2lkZSwKICAgICAgICAgICAgInF1YW50aXR5IjogZ
i5xdWFudGl0eSwgImVmZmVjdGl2ZV9wcmljZSI6IGYuZWZmZWN0aXZlX3ByaWNlfSkKICAgIHJldHVy
biBvdXQKCgphc3luYyBkZWYgcnVuX3JlY29uY2lsaWF0aW9uKAogICAgc2Vzc2lvbjogQXN5bmNTZXN
zaW9uLCAqLCBhY2NvdW50X3Jvd19pZDogc3RyLAogICAgaW5pdGlhbF9iYWxhbmNlOiBEZWNpbWFsLC
BtYXJrczogZGljdCwgbWFyZ2luX3BhcmFtczogZGljdCwKICAgIG1vZGU6IHN0ciwgb3BlcmF0b3Jfa
WQ6IHN0ciwgY29ycmVsYXRpb25faWQ6IHN0ciB8IE5vbmUsCiAgICBkYXRhX2NsYXNzOiBzdHIsCikg
LT4gUGFwZXJPdXRjb21lOgogICAgZmlsbHMgPSBhd2FpdCBjb2xsZWN0X2FjY291bnRfZmlsbHMoc2V
zc2lvbiwgYWNjb3VudF9yb3dfaWQpCiAgICByZWNvbXB1dGVkID0gZGVyaXZlX2JhbGFuY2UoCiAgIC
AgICAgaW5pdGlhbF9iYWxhbmNlPWluaXRpYWxfYmFsYW5jZSwgZmlsbHM9ZmlsbHMsCiAgICAgICAgb
WFya3M9e2s6IERlY2ltYWwoc3RyKHYpKSBmb3IgaywgdiBpbiBtYXJrcy5pdGVtcygpfSwKICAgICAg
ICBtYXJnaW5fcGFyYW1zPW1hcmdpbl9wYXJhbXMpCiAgICBsYXRlc3QgPSAoYXdhaXQgc2Vzc2lvbi5
leGVjdXRlKAogICAgICAgIHNlbGVjdChWMlBhcGVyQmFsYW5jZVNuYXBzaG90KQogICAgICAgIC53aG
VyZShWMlBhcGVyQmFsYW5jZVNuYXBzaG90LmFjY291bnRfaWQgPT0gYWNjb3VudF9yb3dfaWQpCiAgI
CAgICAgLm9yZGVyX2J5KFYyUGFwZXJCYWxhbmNlU25hcHNob3QuY3JlYXRlZF9hdC5kZXNjKCkpCiAg
ICApKS5zY2FsYXJzKCkuZmlyc3QoKQogICAgaWYgbGF0ZXN0IGlzIE5vbmU6CiAgICAgICAgb3V0Y29
tZSwgZGlzY3JlcGFuY2llcyA9ICJjb25zaXN0ZW50IiwgW10KICAgIGVsc2U6CiAgICAgICAgc3Rvcm
VkID0gewogICAgICAgICAgICAicG9zaXRpb25zIjogbGF0ZXN0LmFzX29mX2Jhc2lzLmdldCgicG9za
XRpb25zIiwKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgcmVj
b21wdXRlZFsicG9zaXRpb25zIl0pLAogICAgICAgICAgICAiY2FzaCI6IGxhdGVzdC5jYXNoLCAiZXF
1aXR5IjogbGF0ZXN0LmVxdWl0eSwKICAgICAgICAgICAgIm1hcmdpbl91c2VkIjogbGF0ZXN0Lm1hcm
dpbl91c2VkLAogICAgICAgICAgICAibWFyZ2luX2F2YWlsYWJsZSI6IGxhdGVzdC5tYXJnaW5fYXZha
WxhYmxlLAogICAgICAgICAgICAidW5yZWFsaXplZF9wbmwiOiBsYXRlc3QudW5yZWFsaXplZF9wbmws
CiAgICAgICAgICAgICJyZWFsaXplZF9wbmwiOiBsYXRlc3QucmVhbGl6ZWRfcG5sLAogICAgICAgIH0
KICAgICAgICBzdG9yZWRbInBvc2l0aW9ucyJdID0gcmVjb21wdXRlZFsicG9zaXRpb25zIl0gaWYgbm
90IGlzaW5zdGFuY2UoCiAgICAgICAgICAgIHN0b3JlZFsicG9zaXRpb25zIl0sIGRpY3QpIGVsc2Ugc
3RvcmVkWyJwb3NpdGlvbnMiXQogICAgICAgIG91dGNvbWUsIGRpc2NyZXBhbmNpZXMgPSByZWNvbmNp
bGUoc25hcHNob3Q9c3RvcmVkLAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICA
gICAgcmVjb21wdXRlZD1yZWNvbXB1dGVkKQogICAgcm93ID0gVjJQYXBlclJlY29uY2lsaWF0aW9uKA
ogICAgICAgIGFjY291bnRfaWQ9YWNjb3VudF9yb3dfaWQsCiAgICAgICAgcnVuX2Jhc2lzPXsiZmlsb
HMiOiBsZW4oZmlsbHMpLCAibWFya3MiOiB7CiAgICAgICAgICAgIGs6IHN0cih2KSBmb3IgaywgdiBp
biBtYXJrcy5pdGVtcygpfX0sCiAgICAgICAgb3V0Y29tZT1vdXRjb21lLCBkaXNjcmVwYW5jaWVzPXs
iaXRlbXMiOiBkaXNjcmVwYW5jaWVzfSwKICAgICAgICBpbnB1dHNfaGFzaD1kZXJpdmF0aW9uX2hhc2
goeyJmaWxscyI6IGZpbGxzLCAibWFya3MiOiB7CiAgICAgICAgICAgIGs6IHN0cih2KSBmb3Igaywgd
iBpbiBtYXJrcy5pdGVtcygpfX0pLAogICAgICAgIGRhdGFfY2xhc3M9ZGF0YV9jbGFzcywgbW9kZT1t
b2RlLCBvcGVyYXRvcl9pZD1vcGVyYXRvcl9pZCwKICAgICAgICBjb3JyZWxhdGlvbl9pZD1jb3JyZWx
hdGlvbl9pZCkKICAgIHNlc3Npb24uYWRkKHJvdykKICAgIGF3YWl0IHNlc3Npb24uZmx1c2goKQogIC
AgYXdhaXQgYXVkaXQoc2Vzc2lvbiwgInBhcGVyLnJlY29uY2lsaWF0aW9uLmNvbXBsZXRlZCIsCiAgI
CAgICAgICAgICAgICBkZXRhaWxzPXsib3V0Y29tZSI6IG91dGNvbWUsCiAgICAgICAgICAgICAgICAg
ICAgICAgICAiZGlzY3JlcGFuY3lfY291bnQiOiBsZW4oZGlzY3JlcGFuY2llcyl9LAogICAgICAgICA
gICAgICAgbW9kZT1tb2RlLCBvcGVyYXRvcl9pZD1vcGVyYXRvcl9pZCwKICAgICAgICAgICAgICAgIG
NvcnJlbGF0aW9uX2lkPWNvcnJlbGF0aW9uX2lkLAogICAgICAgICAgICAgICAgcmVzb3VyY2VfdHlwZ
T0icGFwZXJfcmVjb25jaWxpYXRpb24iLCByZXNvdXJjZV9pZD1yb3cuaWQpCiAgICByZXR1cm4gUGFw
ZXJPdXRjb21lKG91dGNvbWU9b3V0Y29tZSwgcmVhc29ucz1kaXNjcmVwYW5jaWVzLAogICAgICAgICA
gICAgICAgICAgICAgICByZWNvcmRfaWQ9cm93LmlkKQo=
'@
$LandPath = Join-Path $BackendRoot "app\v2\paper_trading\reconciliation.py"
New-Item -ItemType Directory -Force -Path (Split-Path $LandPath) | Out-Null
if (Test-Path $LandPath) {
    $Cur = (Get-FileHash -Path $LandPath -Algorithm SHA256).Hash.ToLower()
    if ($Cur -eq "74d7e70f89be1822d6ea2dce91920f471c7a0b5a43ea4b7c5d9524f48c044deb") { Write-Evidence ("pre-landing witnessed (already pinned bytes): app\v2\paper_trading\reconciliation.py") }
    else { throw ("STOP (A4 FOREIGN-STATE ADJUDICATION LAW): new-file target exists with foreign bytes: " + $LandPath + " sha " + $Cur + " . Nothing modified for this file; report to ITRGA.") }
} else {
    [IO.File]::WriteAllBytes($LandPath, (B64-Decode -B64Chunk $Fapp_v2_paper_trading_reconciliation_py))
    $Cur = (Get-FileHash -Path $LandPath -Algorithm SHA256).Hash.ToLower()
    if ($Cur -ne "74d7e70f89be1822d6ea2dce91920f471c7a0b5a43ea4b7c5d9524f48c044deb") { throw ("FAIL: post-write hash drift on " + $LandPath) }
    Write-Evidence ("landed + verified: app\v2\paper_trading\reconciliation.py")
}

# file: app\v2\paper_trading\api.py  (pin 1e4064e367cf...)
$Fapp_v2_paper_trading_api_py = @'
IiIiQkUtOCBlbmRwb2ludHMgKEJPIEQtMS9ELTM7IGRlc2lnbiBTOTsgQzMgbGF3OiBQT1NULW9ubHk
gd3JpdGVycykuCgpHb3Zlcm5lZCB3cml0ZXJzOiBhY2NvdW50cywgYWNjb3VudHMvY29uZmlybSwgb3
JkZXJzLCBvcmRlcnMvY29uZmlybSwKb3JkZXJzL2NhbmNlbCwgb3JkZXJzL3tpZH0vcnVuLiBSZWFkc
zogYWNjb3VudHMsIG9yZGVycywgb3JkZXJzL3tpZH0vZXZlbnRzLApmaWxscywgcG9zaXRpb25zLCBi
YWxhbmNlcywgcmlzay1kZWNpc2lvbnMsIHJlY29uY2lsaWF0aW9ucy4KUEFQRVItbW9kZSB3cml0ZXJ
zIChELTIgbGF3OyB0eXBlZCByZWZ1c2FsIG90aGVyd2lzZSkuIEJFLTEgZW52ZWxvcGUgb24KZXZlcn
kgcmVzcG9uc2U7IHVuY29uZGl0aW9uYWwgcGFwZXItc2ltdWxhdGVkIGRpc2NsYWltZXIgKE40KS4KI
iIiCgpmcm9tIF9fZnV0dXJlX18gaW1wb3J0IGFubm90YXRpb25zCgpmcm9tIGRhdGV0aW1lIGltcG9y
dCBkYXRldGltZSwgdGltZXpvbmUKZnJvbSBkZWNpbWFsIGltcG9ydCBEZWNpbWFsLCBJbnZhbGlkT3B
lcmF0aW9uCmZyb20gdHlwaW5nIGltcG9ydCBBbm5vdGF0ZWQKCmZyb20gZmFzdGFwaSBpbXBvcnQgQV
BJUm91dGVyLCBEZXBlbmRzLCBIVFRQRXhjZXB0aW9uLCBRdWVyeSwgUmVxdWVzdCwgc3RhdHVzCmZyb
20gcHlkYW50aWMgaW1wb3J0IEJhc2VNb2RlbCwgRmllbGQKZnJvbSBzcWxhbGNoZW15IGltcG9ydCBz
ZWxlY3QKZnJvbSBzcWxhbGNoZW15LmV4dC5hc3luY2lvIGltcG9ydCBBc3luY1Nlc3Npb24KCmZyb20
gYXBwLmRiLm1vZGVscy5vcGVyYXRvciBpbXBvcnQgT3BlcmF0b3IKZnJvbSBhcHAuZGIubW9kZWxzLn
YyX3BhcGVyX3RyYWRpbmcgaW1wb3J0ICgKICAgIFYyUGFwZXJCYWxhbmNlU25hcHNob3QsCiAgICBWM
lBhcGVyRmlsbCwKICAgIFYyUGFwZXJPcmRlckV2ZW50LAogICAgVjJQYXBlck9yZGVySW50ZW50LAog
ICAgVjJQYXBlclBvc2l0aW9uU25hcHNob3QsCiAgICBWMlBhcGVyUmVjb25jaWxpYXRpb24sCiAgICB
WMlBhcGVyUmlza0RlY2lzaW9uLAopCmZyb20gYXBwLmRiLnNlc3Npb24gaW1wb3J0IGdldF9kYl9zZX
NzaW9uCmZyb20gYXBwLnYyLmlkZW50aWZpZXJzIGltcG9ydCBuZXdfaWQKZnJvbSBhcHAudjIucGFwZ
XJfdHJhZGluZy5hY2NvdW50cyBpbXBvcnQgKAogICAgY29uZmlybV9hY2NvdW50X2FjdGlvbiwKICAg
IGN1cnJlbnRfYWNjb3VudCwKICAgIHJlcXVlc3RfYWNjb3VudF9hY3Rpb24sCikKZnJvbSBhcHAudjI
ucGFwZXJfdHJhZGluZy5jb250cmFjdHMgaW1wb3J0ICgKICAgIElOVEVOVF9TSURFUywKICAgIElOVE
VOVF9UWVBFUywKICAgIFBBUEVSX0RJU0NMQUlNRVIsCiAgICBQYXBlck9yZGVySW50ZW50LAogICAgU
GFwZXJSZWZ1c2VkLAopCmZyb20gYXBwLnYyLnBhcGVyX3RyYWRpbmcubGVkZ2VyIGltcG9ydCBkZXJp
dmF0aW9uX2hhc2gsIGRlcml2ZV9iYWxhbmNlCmZyb20gYXBwLnYyLnBhcGVyX3RyYWRpbmcub3JkZXJ
zIGltcG9ydCAoCiAgICBhcHBlbmRfZXZlbnQsCiAgICBhdWRpdCwKICAgIGNhbmNlbF9vcmRlciwKIC
AgIGNvbmZpcm1faG9sZCwKICAgIGN1cnJlbnRfc3RhdGUsCiAgICBnZXRfaW50ZW50LAogICAgbWF5X
2V4ZWN1dGUsCikKZnJvbSBhcHAudjIucGFwZXJfdHJhZGluZy5yZWNvbmNpbGlhdGlvbiBpbXBvcnQg
KAogICAgY29sbGVjdF9hY2NvdW50X2ZpbGxzLAogICAgcnVuX3JlY29uY2lsaWF0aW9uLAopCmZyb20
gYXBwLnYyLnBhcGVyX3RyYWRpbmcucmlzayBpbXBvcnQgY29uZmlnX3ZlcnNpb24sIGV2YWx1YXRlX2
ludGVudApmcm9tIGFwcC52Mi5wYXBlcl90cmFkaW5nLnNpbXVsYXRvciBpbXBvcnQgKAogICAgRU5HS
U5FX1ZFUlNJT05TLAogICAgU0lNVUxBVE9SX1ZFUlNJT04sCiAgICBlbmdpbmVfdmVyc2lvbnNfaGFz
aCwKICAgIHJ1bl9zaW11bGF0aW9uLAogICAgc25hcHNob3RfY29udGVudF9oYXNoLAopCmZyb20gYXB
wLnYyLnJiYWMuZGVwZW5kZW5jaWVzIGltcG9ydCByZXF1aXJlX3YyX3Blcm1pc3Npb24KCnJvdXRlci
A9IEFQSVJvdXRlcihwcmVmaXg9Ii9wYXBlciIsIHRhZ3M9WyJWMiBQYXBlciBUcmFkaW5nIl0pCgpSZ
XF1aXJlQWNjb3VudHNSZWFkID0gQW5ub3RhdGVkWwogICAgT3BlcmF0b3IsIERlcGVuZHMocmVxdWly
ZV92Ml9wZXJtaXNzaW9uKCJ2Mi5wYXBlci5hY2NvdW50cy5yZWFkIikpXQpSZXF1aXJlQWNjb3VudHN
NYW5hZ2UgPSBBbm5vdGF0ZWRbCiAgICBPcGVyYXRvciwgRGVwZW5kcyhyZXF1aXJlX3YyX3Blcm1pc3
Npb24oInYyLnBhcGVyLmFjY291bnRzLm1hbmFnZSIpKV0KUmVxdWlyZU9yZGVyc1JlYWQgPSBBbm5vd
GF0ZWRbCiAgICBPcGVyYXRvciwgRGVwZW5kcyhyZXF1aXJlX3YyX3Blcm1pc3Npb24oInYyLnBhcGVy
Lm9yZGVycy5yZWFkIikpXQpSZXF1aXJlT3JkZXJzUGxhY2UgPSBBbm5vdGF0ZWRbCiAgICBPcGVyYXR
vciwgRGVwZW5kcyhyZXF1aXJlX3YyX3Blcm1pc3Npb24oInYyLnBhcGVyLm9yZGVycy5wbGFjZSIpKV
0KUmVxdWlyZU9yZGVyc0NhbmNlbCA9IEFubm90YXRlZFsKICAgIE9wZXJhdG9yLCBEZXBlbmRzKHJlc
XVpcmVfdjJfcGVybWlzc2lvbigidjIucGFwZXIub3JkZXJzLmNhbmNlbCIpKV0KUmVxdWlyZU9yZGVy
c0NvbmZpcm0gPSBBbm5vdGF0ZWRbCiAgICBPcGVyYXRvciwgRGVwZW5kcyhyZXF1aXJlX3YyX3Blcm1
pc3Npb24oInYyLnBhcGVyLm9yZGVycy5jb25maXJtIikpXQpSZXF1aXJlRmlsbHNSZWFkID0gQW5ub3
RhdGVkWwogICAgT3BlcmF0b3IsIERlcGVuZHMocmVxdWlyZV92Ml9wZXJtaXNzaW9uKCJ2Mi5wYXBlc
i5maWxscy5yZWFkIikpXQpSZXF1aXJlUmlza1JlYWQgPSBBbm5vdGF0ZWRbCiAgICBPcGVyYXRvciwg
RGVwZW5kcyhyZXF1aXJlX3YyX3Blcm1pc3Npb24oInYyLnBhcGVyLnJpc2sucmVhZCIpKV0KCl9EQVR
BX0NMQVNTID0gInNpbXVsYXRlZCIKCgpkZWYgX2VudmVsb3BlKHJlcXVlc3Q6IFJlcXVlc3QpIC0+IG
RpY3Q6CiAgICByZXR1cm4geyJtb2RlIjogcmVxdWVzdC5hcHAuc3RhdGUudjJfbW9kZSwKICAgICAgI
CAgICAgImNvcnJlbGF0aW9uX2lkIjogZ2V0YXR0cihyZXF1ZXN0LnN0YXRlLCAiY29ycmVsYXRpb25f
aWQiLCBOb25lKSwKICAgICAgICAgICAgInRpbWVzdGFtcCI6IGRhdGV0aW1lLm5vdyh0aW1lem9uZS5
1dGMpLAogICAgICAgICAgICAiZGlzY2xhaW1lciI6IFBBUEVSX0RJU0NMQUlNRVJ9CgoKZGVmIF9yZX
F1aXJlX3BhcGVyKHJlcXVlc3Q6IFJlcXVlc3QpIC0+IHN0cjoKICAgICIiIkQtMiBsYXc6IHBhcGVyI
HdyaXRlcnMgZGVtYW5kIG1vZGUgPT0gUEFQRVIsIHR5cGVkIHJlZnVzYWwgZWxzZS4iIiIKICAgIG1v
ZGUgPSByZXF1ZXN0LmFwcC5zdGF0ZS52Ml9tb2RlCiAgICBpZiBtb2RlICE9ICJQQVBFUiI6CiAgICA
gICAgcmFpc2UgSFRUUEV4Y2VwdGlvbigKICAgICAgICAgICAgc3RhdHVzX2NvZGU9c3RhdHVzLkhUVF
BfNDAzX0ZPUkJJRERFTiwKICAgICAgICAgICAgZGV0YWlsPSJQYXBlciB3cml0ZXIgbm90IHBlcm1pd
HRlZCBpbiB0aGlzIG1vZGUiKQogICAgcmV0dXJuIG1vZGUKCgpkZWYgX2NpZChyZXF1ZXN0OiBSZXF1
ZXN0KSAtPiBzdHI6CiAgICByZXR1cm4gZ2V0YXR0cihyZXF1ZXN0LnN0YXRlLCAiY29ycmVsYXRpb25
faWQiLCBOb25lKSBvciBuZXdfaWQoKQoKCiMgLS0tIHJlcXVlc3QgbW9kZWxzIC0tLS0tLS0tLS0tLS
0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tCgoKY2xhc3MgQWNjb
3VudFJlcXVlc3QoQmFzZU1vZGVsKToKICAgIGFjdGlvbjogc3RyID0gRmllbGQocGF0dGVybj0iXihj
cmVhdGV8ZnJlZXplfGNsb3NlKSQiKQogICAgYWNjb3VudF9pZDogc3RyID0gRmllbGQobWluX2xlbmd
0aD0xLCBtYXhfbGVuZ3RoPTY0KQogICAgbmFtZTogc3RyID0gIiIKICAgIGJhc2VfY3VycmVuY3k6IH
N0ciA9ICJVU0QiCiAgICBpbml0aWFsX2JhbGFuY2U6IHN0ciA9ICIwIgogICAgbWFyZ2luX3BhcmFtc
zogZGljdCA9IEZpZWxkKGRlZmF1bHRfZmFjdG9yeT1kaWN0KQoKCmNsYXNzIEFjY291bnRDb25maXJt
KEFjY291bnRSZXF1ZXN0KToKICAgIGNvbmZpcm1hdGlvbl9yZWY6IHN0cgoKCmNsYXNzIE9yZGVyUmV
xdWVzdChCYXNlTW9kZWwpOgogICAgYWNjb3VudF9pZDogc3RyCiAgICBpbnN0cnVtZW50X2lkOiBzdH
IKICAgIHNpZGU6IHN0cgogICAgb3JkZXJfdHlwZTogc3RyID0gIm1hcmtldCIKICAgIHF1YW50aXR5O
iBzdHIKICAgIGxpbWl0X3ByaWNlOiBzdHIgfCBOb25lID0gTm9uZQogICAgaWRlbXBvdGVuY3lfa2V5
OiBzdHIgPSBGaWVsZChtaW5fbGVuZ3RoPTEsIG1heF9sZW5ndGg9NjQpCiAgICBzbmFwc2hvdF9yZWY
6IHN0ciA9IEZpZWxkKG1pbl9sZW5ndGg9MSwgbWF4X2xlbmd0aD02NCkKICAgIGJhcnM6IGxpc3RbZG
ljdF0gPSBGaWVsZChkZWZhdWx0X2ZhY3Rvcnk9bGlzdCkKICAgIHdpbmRvd19zdGFydDogc3RyID0gI
iIKICAgIHdpbmRvd19lbmQ6IHN0ciA9ICIiCgoKY2xhc3MgT3JkZXJDb25maXJtKEJhc2VNb2RlbCk6
CiAgICBvcmRlcl9pZDogc3RyCiAgICBjb25maXJtYXRpb25fcmVmOiBzdHIKICAgIHJlc29sdmVfdG8
6IHN0ciA9IEZpZWxkKHBhdHRlcm49Il4oY29uZmlybXxjYW5jZWwpJCIpCgoKY2xhc3MgT3JkZXJDYW
5jZWwoQmFzZU1vZGVsKToKICAgIG9yZGVyX2lkOiBzdHIKCgpjbGFzcyBPcmRlclJ1bihCYXNlTW9kZ
WwpOgogICAgYmFyczogbGlzdFtkaWN0XSA9IEZpZWxkKGRlZmF1bHRfZmFjdG9yeT1saXN0KQogICAg
Y29zdF9tb2RlbDogZGljdCB8IE5vbmUgPSBOb25lCgoKIyAtLS0gd3JpdGVycyAoUE9TVCBvbmx5OyB
DMykgLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLQoKCk
Byb3V0ZXIucG9zdCgiL2FjY291bnRzIikKYXN5bmMgZGVmIGFwaV9hY2NvdW50X3JlcXVlc3QoCiAgI
CBib2R5OiBBY2NvdW50UmVxdWVzdCwgcmVxdWVzdDogUmVxdWVzdCwgb3BlcmF0b3I6IFJlcXVpcmVB
Y2NvdW50c01hbmFnZSwKICAgIHNlc3Npb246IEFubm90YXRlZFtBc3luY1Nlc3Npb24sIERlcGVuZHM
oZ2V0X2RiX3Nlc3Npb24pXSwKKToKICAgIG1vZGUgPSBfcmVxdWlyZV9wYXBlcihyZXF1ZXN0KQogIC
AgcmVzdWx0ID0gYXdhaXQgcmVxdWVzdF9hY2NvdW50X2FjdGlvbigKICAgICAgICBzZXNzaW9uLCBhY
3Rpb249Ym9keS5hY3Rpb24sCiAgICAgICAgcGF5bG9hZD1ib2R5Lm1vZGVsX2R1bXAoZXhjbHVkZT17
ImFjdGlvbiJ9KSwKICAgICAgICBtb2RlPW1vZGUsIG9wZXJhdG9yX2lkPW9wZXJhdG9yLnVzZXJuYW1
lLAogICAgICAgIGNvcnJlbGF0aW9uX2lkPV9jaWQocmVxdWVzdCkpCiAgICBpZiBub3QgcmVzdWx0Ln
JlZnVzZWQ6CiAgICAgICAgYXdhaXQgc2Vzc2lvbi5jb21taXQoKQogICAgcmV0dXJuIHsib3V0Y29tZ
SI6IHJlc3VsdC5vdXRjb21lLCAicmVhc29ucyI6IHJlc3VsdC5yZWFzb25zLAogICAgICAgICAgICAi
Y29uZmlybWF0aW9uX3JlZiI6IHJlc3VsdC5jb25maXJtYXRpb25fcmVmLAogICAgICAgICAgICAqKl9
lbnZlbG9wZShyZXF1ZXN0KX0KCgpAcm91dGVyLnBvc3QoIi9hY2NvdW50cy9jb25maXJtIikKYXN5bm
MgZGVmIGFwaV9hY2NvdW50X2NvbmZpcm0oCiAgICBib2R5OiBBY2NvdW50Q29uZmlybSwgcmVxdWVzd
DogUmVxdWVzdCwgb3BlcmF0b3I6IFJlcXVpcmVBY2NvdW50c01hbmFnZSwKICAgIHNlc3Npb246IEFu
bm90YXRlZFtBc3luY1Nlc3Npb24sIERlcGVuZHMoZ2V0X2RiX3Nlc3Npb24pXSwKKToKICAgIG1vZGU
gPSBfcmVxdWlyZV9wYXBlcihyZXF1ZXN0KQogICAgcmVzdWx0ID0gYXdhaXQgY29uZmlybV9hY2NvdW
50X2FjdGlvbigKICAgICAgICBzZXNzaW9uLCBhY3Rpb249Ym9keS5hY3Rpb24sCiAgICAgICAgcGF5b
G9hZD1ib2R5Lm1vZGVsX2R1bXAoZXhjbHVkZT17ImFjdGlvbiIsICJjb25maXJtYXRpb25fcmVmIn0p
LAogICAgICAgIGNvbmZpcm1hdGlvbl9yZWY9Ym9keS5jb25maXJtYXRpb25fcmVmLAogICAgICAgIGF
jdG9yX2lkPW9wZXJhdG9yLnVzZXJuYW1lLCBtb2RlPW1vZGUsCiAgICAgICAgb3BlcmF0b3JfaWQ9b3
BlcmF0b3IudXNlcm5hbWUsIGNvcnJlbGF0aW9uX2lkPV9jaWQocmVxdWVzdCksCiAgICAgICAgZGF0Y
V9jbGFzcz1fREFUQV9DTEFTUykKICAgIGlmIG5vdCByZXN1bHQucmVmdXNlZDoKICAgICAgICBhd2Fp
dCBzZXNzaW9uLmNvbW1pdCgpCiAgICByZXR1cm4geyJvdXRjb21lIjogcmVzdWx0Lm91dGNvbWUsICJ
yZWFzb25zIjogcmVzdWx0LnJlYXNvbnMsCiAgICAgICAgICAgICJyZWNvcmRfaWQiOiByZXN1bHQucm
Vjb3JkX2lkLCAqKl9lbnZlbG9wZShyZXF1ZXN0KX0KCgpAcm91dGVyLnBvc3QoIi9vcmRlcnMiKQphc
3luYyBkZWYgYXBpX3BsYWNlX29yZGVyKAogICAgYm9keTogT3JkZXJSZXF1ZXN0LCByZXF1ZXN0OiBS
ZXF1ZXN0LCBvcGVyYXRvcjogUmVxdWlyZU9yZGVyc1BsYWNlLAogICAgc2Vzc2lvbjogQW5ub3RhdGV
kW0FzeW5jU2Vzc2lvbiwgRGVwZW5kcyhnZXRfZGJfc2Vzc2lvbildLAopOgogICAgIiIiSW50ZW50IC
sgdmFsaWRhdGlvbiArIHJpc2sgZGVjaXNpb24gaW4gb25lIGdvdmVybmVkIGFjdCAoUzIgZHJhZnQgL
T4KICAgIHZhbGlkYXRlZCAtPiByaXNrXyopLiBOMzogZXZlcnkgZmllbGQgb2YgdGhlIGxhdyBvbiB0
aGUgcm93LiIiIgogICAgbW9kZSA9IF9yZXF1aXJlX3BhcGVyKHJlcXVlc3QpCiAgICBjaWQgPSBfY2l
kKHJlcXVlc3QpCgogICAgcmVhc29uczogbGlzdCA9IFtdCiAgICBhY2NvdW50ID0gYXdhaXQgY3Vycm
VudF9hY2NvdW50KHNlc3Npb24sIGJvZHkuYWNjb3VudF9pZCkKICAgIGFjY291bnRfcm93X2lkID0gY
WNjb3VudC5pZCBpZiBhY2NvdW50IGlzIG5vdCBOb25lIGVsc2UgTm9uZQogICAgaWYgYWNjb3VudCBp
cyBOb25lOgogICAgICAgIHJlYXNvbnMuYXBwZW5kKHsiZmFpbGluZyI6ICJhY2NvdW50X2lkIiwgIm5
vdGUiOiAidW5rbm93biBhY2NvdW50In0pCgogICAgIyBJZGVtcG90ZW5jeSAoUzgpOiBzYW1lIChhY2
NvdW50LCBrZXkpIHJldHVybnMgdGhlIGV4aXN0aW5nIGludGVudC4KICAgICMgUm93cyBwaW4gdGhlI
GFjY291bnQgUk9XIGlkIOKAlCBkZWR1cGUgb24gaXQsIG5vdCB0aGUgbG9naWNhbCBpZC4KICAgIGlm
IGFjY291bnRfcm93X2lkIGlzIG5vdCBOb25lOgogICAgICAgIGV4aXN0aW5nID0gKGF3YWl0IHNlc3N
pb24uZXhlY3V0ZSgKICAgICAgICAgICAgc2VsZWN0KFYyUGFwZXJPcmRlckludGVudCkud2hlcmUoCi
AgICAgICAgICAgICAgICBWMlBhcGVyT3JkZXJJbnRlbnQuYWNjb3VudF9pZCA9PSBhY2NvdW50X3Jvd
19pZCwKICAgICAgICAgICAgICAgIFYyUGFwZXJPcmRlckludGVudC5pZGVtcG90ZW5jeV9rZXkgPT0g
Ym9keS5pZGVtcG90ZW5jeV9rZXkpCiAgICAgICAgKSkuc2NhbGFyX29uZV9vcl9ub25lKCkKICAgICA
gICBpZiBleGlzdGluZyBpcyBub3QgTm9uZToKICAgICAgICAgICAgYXdhaXQgYXVkaXQoc2Vzc2lvbi
wgInBhcGVyLm9yZGVyLnJldXNlZCIsCiAgICAgICAgICAgICAgICAgICAgICAgIGRldGFpbHM9eyJpZ
GVtcG90ZW5jeV9rZXkiOiBib2R5LmlkZW1wb3RlbmN5X2tleX0sCiAgICAgICAgICAgICAgICAgICAg
ICAgIG1vZGU9bW9kZSwgb3BlcmF0b3JfaWQ9b3BlcmF0b3IudXNlcm5hbWUsCiAgICAgICAgICAgICA
gICAgICAgICAgIGNvcnJlbGF0aW9uX2lkPWNpZCwgcmVzb3VyY2VfaWQ9ZXhpc3RpbmcuaWQpCiAgIC
AgICAgICAgIGF3YWl0IHNlc3Npb24uY29tbWl0KCkKICAgICAgICAgICAgc3RhdGUgPSBhd2FpdCBjd
XJyZW50X3N0YXRlKHNlc3Npb24sIGV4aXN0aW5nLmlkKQogICAgICAgICAgICByZXR1cm4geyJvdXRj
b21lIjogInJldXNlZCIsICJvcmRlcl9pZCI6IGV4aXN0aW5nLmlkLAogICAgICAgICAgICAgICAgICA
gICJzdGF0ZSI6IHN0YXRlLCAicmVhc29ucyI6IFtdLCAqKl9lbnZlbG9wZShyZXF1ZXN0KX0KICAgIG
lmIGJvZHkuc2lkZSBub3QgaW4gSU5URU5UX1NJREVTOgogICAgICAgIHJlYXNvbnMuYXBwZW5kKHsiZ
mFpbGluZyI6ICJzaWRlIiwgImFsbG93ZWQiOiBsaXN0KElOVEVOVF9TSURFUyl9KQogICAgaWYgYm9k
eS5vcmRlcl90eXBlIG5vdCBpbiBJTlRFTlRfVFlQRVM6CiAgICAgICAgcmVhc29ucy5hcHBlbmQoeyJ
mYWlsaW5nIjogIm9yZGVyX3R5cGUiLAogICAgICAgICAgICAgICAgICAgICAgICAiYWxsb3dlZCI6IG
xpc3QoSU5URU5UX1RZUEVTKX0pCiAgICBpZiAoYm9keS5vcmRlcl90eXBlID09ICJsaW1pdCIpICE9I
Chib2R5LmxpbWl0X3ByaWNlIGlzIG5vdCBOb25lKToKICAgICAgICByZWFzb25zLmFwcGVuZCh7ImZh
aWxpbmciOiAibGltaXRfcHJpY2UiLAogICAgICAgICAgICAgICAgICAgICAgICAibm90ZSI6ICJwcmV
zZW50IGlmZiBvcmRlcl90eXBlPWxpbWl0In0pCiAgICB0cnk6CiAgICAgICAgcXVhbnRpdHkgPSBEZW
NpbWFsKGJvZHkucXVhbnRpdHkpCiAgICAgICAgaWYgcXVhbnRpdHkgPD0gMDoKICAgICAgICAgICAgc
mVhc29ucy5hcHBlbmQoeyJmYWlsaW5nIjogInF1YW50aXR5IiwgIm5vdGUiOiAibXVzdCBiZSA+IDAi
fSkKICAgIGV4Y2VwdCBJbnZhbGlkT3BlcmF0aW9uOgogICAgICAgIHF1YW50aXR5ID0gRGVjaW1hbCg
wKQogICAgICAgIHJlYXNvbnMuYXBwZW5kKHsiZmFpbGluZyI6ICJxdWFudGl0eSIsICJub3RlIjogIm
5vdCBhIGRlY2ltYWwifSkKICAgIGlmIG5vdCBib2R5LmJhcnM6CiAgICAgICAgcmVhc29ucy5hcHBlb
mQoeyJmYWlsaW5nIjogImJhcnMiLAogICAgICAgICAgICAgICAgICAgICAgICAibm90ZSI6ICJnb3Zl
cm5lZCBzbmFwc2hvdCBiYXJzIHJlcXVpcmVkIChRNCkifSkKCiAgICBpZiByZWFzb25zOgogICAgICA
gIGF3YWl0IGF1ZGl0KHNlc3Npb24sICJwYXBlci5vcmRlci5yZWplY3RlZCIsCiAgICAgICAgICAgIC
AgICAgICAgZGV0YWlscz17InJlYXNvbnMiOiByZWFzb25zWzo4XX0sIG1vZGU9bW9kZSwKICAgICAgI
CAgICAgICAgICAgICBvcGVyYXRvcl9pZD1vcGVyYXRvci51c2VybmFtZSwgY29ycmVsYXRpb25faWQ9
Y2lkKQogICAgICAgIGF3YWl0IHNlc3Npb24uY29tbWl0KCkKICAgICAgICByZXR1cm4geyJvdXRjb21
lIjogInJlamVjdGVkIiwgIm9yZGVyX2lkIjogTm9uZSwKICAgICAgICAgICAgICAgICJyZWFzb25zIj
ogcmVhc29ucywgKipfZW52ZWxvcGUocmVxdWVzdCl9CgogICAgY29udGVudCA9IHNuYXBzaG90X2Nvb
nRlbnRfaGFzaChib2R5LmJhcnMsIGJvZHkuc25hcHNob3RfcmVmKQogICAgaW50ZW50ID0gVjJQYXBl
ck9yZGVySW50ZW50KAogICAgICAgIGludGVudF9pZD1uZXdfaWQoKSwgYWNjb3VudF9pZD1hY2NvdW5
0X3Jvd19pZCwKICAgICAgICBpbnN0cnVtZW50X2lkPWJvZHkuaW5zdHJ1bWVudF9pZCwgc2lkZT1ib2
R5LnNpZGUsCiAgICAgICAgb3JkZXJfdHlwZT1ib2R5Lm9yZGVyX3R5cGUsIHF1YW50aXR5PXN0cihxd
WFudGl0eSksCiAgICAgICAgbGltaXRfcHJpY2U9Ym9keS5saW1pdF9wcmljZSwgdGltZV9pbl9mb3Jj
ZT0icmVwbGF5X3dpbmRvdyIsCiAgICAgICAgaWRlbXBvdGVuY3lfa2V5PWJvZHkuaWRlbXBvdGVuY3l
fa2V5LAogICAgICAgIHNuYXBzaG90X3JlZj1ib2R5LnNuYXBzaG90X3JlZiwKICAgICAgICB0aW1lX2
Jhc2lzPXsid2luZG93X3N0YXJ0IjogYm9keS53aW5kb3dfc3RhcnQsCiAgICAgICAgICAgICAgICAgI
CAgIndpbmRvd19lbmQiOiBib2R5LndpbmRvd19lbmQsCiAgICAgICAgICAgICAgICAgICAgInNuYXBz
aG90X2NvbnRlbnRfaGFzaCI6IGNvbnRlbnR9LAogICAgICAgIGNvbmZpcm1hdGlvbl9yZWY9Tm9uZSw
gYWN0b3JfaWQ9b3BlcmF0b3IudXNlcm5hbWUsCiAgICAgICAgZGF0YV9jbGFzcz1fREFUQV9DTEFTUy
wgbW9kZT1tb2RlLAogICAgICAgIG9wZXJhdG9yX2lkPW9wZXJhdG9yLnVzZXJuYW1lLCBjb3JyZWxhd
Glvbl9pZD1jaWQpCiAgICBzZXNzaW9uLmFkZChpbnRlbnQpCiAgICBhd2FpdCBzZXNzaW9uLmZsdXNo
KCkKCiAgICBldiA9IGF3YWl0IGFwcGVuZF9ldmVudCgKICAgICAgICBzZXNzaW9uLCBpbnRlbnRfcm9
3X2lkPWludGVudC5pZCwgZnJvbV9zdGF0ZT0iZHJhZnQiLAogICAgICAgIHRvX3N0YXRlPSJ2YWxpZG
F0ZWQiLCBldmVudF9jbGFzcz0ib3JkZXIudmFsaWRhdGVkIiwKICAgICAgICBkZXRhaWxzPXt9LCBhY
3Rvcl9pZD1vcGVyYXRvci51c2VybmFtZSwgbW9kZT1tb2RlLAogICAgICAgIG9wZXJhdG9yX2lkPW9w
ZXJhdG9yLnVzZXJuYW1lLCBjb3JyZWxhdGlvbl9pZD1jaWQsCiAgICAgICAgZGF0YV9jbGFzcz1fREF
UQV9DTEFTUykKICAgIGFzc2VydCBub3QgZXYucmVmdXNlZAoKICAgICMgUmlzayBnYXRld2F5IOKAlC
BleGFjdGx5IG9uY2UgKFMzL1M4KS4KICAgIHJlZmVyZW5jZV9wcmljZSA9IERlY2ltYWwoc3RyKGJvZ
HkuYmFyc1swXVsiY2xvc2UiXSkpCiAgICBmaWxsc19zb19mYXIgPSBhd2FpdCBjb2xsZWN0X2FjY291
bnRfZmlsbHMoc2Vzc2lvbiwgYWNjb3VudF9yb3dfaWQpCiAgICBiYWxhbmNlID0gZGVyaXZlX2JhbGF
uY2UoCiAgICAgICAgaW5pdGlhbF9iYWxhbmNlPURlY2ltYWwoYWNjb3VudC5pbml0aWFsX2JhbGFuY2
UpLAogICAgICAgIGZpbGxzPWZpbGxzX3NvX2ZhciwKICAgICAgICBtYXJrcz17Ym9keS5pbnN0cnVtZ
W50X2lkOiByZWZlcmVuY2VfcHJpY2V9LAogICAgICAgIG1hcmdpbl9wYXJhbXM9YWNjb3VudC5tYXJn
aW5fcGFyYW1zKQogICAgbm90aW9uYWwgPSBxdWFudGl0eSAqIHJlZmVyZW5jZV9wcmljZQogICAgZXF
1aXR5ID0gRGVjaW1hbChiYWxhbmNlWyJlcXVpdHkiXSkKICAgIGNvbmNlbnRyYXRpb24gPSAobm90aW
9uYWwgLyBlcXVpdHkpIGlmIGVxdWl0eSA+IDAgZWxzZSBEZWNpbWFsKDEpCiAgICBzZXNzaW9uX2Nvd
W50ID0gbGVuKChhd2FpdCBzZXNzaW9uLmV4ZWN1dGUoCiAgICAgICAgc2VsZWN0KFYyUGFwZXJPcmRl
ckludGVudC5pZCkud2hlcmUoCiAgICAgICAgICAgIFYyUGFwZXJPcmRlckludGVudC5hY2NvdW50X2l
kID09IGFjY291bnRfcm93X2lkKQogICAgKSkuYWxsKCkpCiAgICBkZWNpc2lvbiwgbGltaXRzLCBkZW
Npc2lvbl9yZWFzb25zID0gZXZhbHVhdGVfaW50ZW50KAogICAgICAgIHF1YW50aXR5PXF1YW50aXR5L
CByZWZlcmVuY2VfcHJpY2U9cmVmZXJlbmNlX3ByaWNlLAogICAgICAgIGFjY291bnRfc3RhdGU9YWNj
b3VudC5saWZlY3ljbGVfc3RhdGUsIGluc3RydW1lbnRfa25vd249VHJ1ZSwKICAgICAgICBtYXJnaW5
fYXZhaWxhYmxlPURlY2ltYWwoYmFsYW5jZVsibWFyZ2luX2F2YWlsYWJsZSJdKSwKICAgICAgICBtYX
JnaW5fcmVxdWlyZWQ9bm90aW9uYWwgKiBEZWNpbWFsKHN0cihhY2NvdW50Lm1hcmdpbl9wYXJhbXMuZ
2V0KAogICAgICAgICAgICAibWFyZ2luX3JhdGUiLCAiMC41IikpKSwKICAgICAgICBjb25jZW50cmF0
aW9uX2ZyYWN0aW9uPWNvbmNlbnRyYXRpb24sCiAgICAgICAgc2Vzc2lvbl9pbnRlbnRfY291bnQ9c2V
zc2lvbl9jb3VudCAtIDEpCgogICAgY29uZmlybWF0aW9uX3JlZiA9IG5ld19pZCgpIGlmIGRlY2lzaW
9uID09ICJob2xkIiBlbHNlIE5vbmUKICAgIHNlc3Npb24uYWRkKFYyUGFwZXJSaXNrRGVjaXNpb24oC
iAgICAgICAgaW50ZW50X2lkPWludGVudC5pZCwgZGVjaXNpb249ZGVjaXNpb24sCiAgICAgICAgZXZh
bHVhdGVkX2xpbWl0cz1saW1pdHMsIHJlYXNvbnM9eyJpdGVtcyI6IGRlY2lzaW9uX3JlYXNvbnN9LAo
gICAgICAgIHJpc2tfY29uZmlnX3ZlcnNpb249Y29uZmlnX3ZlcnNpb24oKSwKICAgICAgICBkZWNpZG
VkX2F0X2Jhc2lzPXsicmVmZXJlbmNlX3ByaWNlIjogc3RyKHJlZmVyZW5jZV9wcmljZSl9LAogICAgI
CAgIGNvbmZpcm1hdGlvbl9yZWY9Y29uZmlybWF0aW9uX3JlZiwgZGF0YV9jbGFzcz1fREFUQV9DTEFT
UywKICAgICAgICBtb2RlPW1vZGUsIG9wZXJhdG9yX2lkPW9wZXJhdG9yLnVzZXJuYW1lLCBjb3JyZWx
hdGlvbl9pZD1jaWQpKQogICAgYXdhaXQgc2Vzc2lvbi5mbHVzaCgpCgogICAgaWYgZGVjaXNpb24gPT
0gInBhc3MiOgogICAgICAgIGV2ID0gYXdhaXQgYXBwZW5kX2V2ZW50KAogICAgICAgICAgICBzZXNza
W9uLCBpbnRlbnRfcm93X2lkPWludGVudC5pZCwgZnJvbV9zdGF0ZT0idmFsaWRhdGVkIiwKICAgICAg
ICAgICAgdG9fc3RhdGU9InJpc2tfcGFzc2VkIiwgZXZlbnRfY2xhc3M9InJpc2sucGFzc2VkIiwKICA
gICAgICAgICAgZGV0YWlscz17ImxpbWl0cyI6IGxpbWl0c30sIGFjdG9yX2lkPW9wZXJhdG9yLnVzZX
JuYW1lLAogICAgICAgICAgICBtb2RlPW1vZGUsIG9wZXJhdG9yX2lkPW9wZXJhdG9yLnVzZXJuYW1lL
CBjb3JyZWxhdGlvbl9pZD1jaWQsCiAgICAgICAgICAgIGRhdGFfY2xhc3M9X0RBVEFfQ0xBU1MpCiAg
ICAgICAgYXdhaXQgYXVkaXQoc2Vzc2lvbiwgInBhcGVyLnJpc2sucGFzc2VkIiwgZGV0YWlscz17fSw
KICAgICAgICAgICAgICAgICAgICBtb2RlPW1vZGUsIG9wZXJhdG9yX2lkPW9wZXJhdG9yLnVzZXJuYW
1lLAogICAgICAgICAgICAgICAgICAgIGNvcnJlbGF0aW9uX2lkPWNpZCwgcmVzb3VyY2VfaWQ9aW50Z
W50LmlkKQogICAgZWxpZiBkZWNpc2lvbiA9PSAiYmxvY2siOgogICAgICAgIGV2ID0gYXdhaXQgYXBw
ZW5kX2V2ZW50KAogICAgICAgICAgICBzZXNzaW9uLCBpbnRlbnRfcm93X2lkPWludGVudC5pZCwgZnJ
vbV9zdGF0ZT0idmFsaWRhdGVkIiwKICAgICAgICAgICAgdG9fc3RhdGU9InJpc2tfYmxvY2tlZCIsIG
V2ZW50X2NsYXNzPSJyaXNrLmJsb2NrZWQiLAogICAgICAgICAgICBkZXRhaWxzPXsicmVhc29ucyI6I
GRlY2lzaW9uX3JlYXNvbnN9LAogICAgICAgICAgICBhY3Rvcl9pZD1vcGVyYXRvci51c2VybmFtZSwg
bW9kZT1tb2RlLAogICAgICAgICAgICBvcGVyYXRvcl9pZD1vcGVyYXRvci51c2VybmFtZSwgY29ycmV
sYXRpb25faWQ9Y2lkLAogICAgICAgICAgICBkYXRhX2NsYXNzPV9EQVRBX0NMQVNTKQogICAgICAgIG
F3YWl0IGF1ZGl0KHNlc3Npb24sICJwYXBlci5yaXNrLmJsb2NrZWQiLAogICAgICAgICAgICAgICAgI
CAgIGRldGFpbHM9eyJyZWFzb25zIjogZGVjaXNpb25fcmVhc29uc30sIG1vZGU9bW9kZSwKICAgICAg
ICAgICAgICAgICAgICBvcGVyYXRvcl9pZD1vcGVyYXRvci51c2VybmFtZSwgY29ycmVsYXRpb25faWQ
9Y2lkLAogICAgICAgICAgICAgICAgICAgIHJlc291cmNlX2lkPWludGVudC5pZCkKICAgIGVsc2U6Ci
AgICAgICAgZXYgPSBhd2FpdCBhcHBlbmRfZXZlbnQoCiAgICAgICAgICAgIHNlc3Npb24sIGludGVud
F9yb3dfaWQ9aW50ZW50LmlkLCBmcm9tX3N0YXRlPSJ2YWxpZGF0ZWQiLAogICAgICAgICAgICB0b19z
dGF0ZT0icmlza19ob2xkIiwgZXZlbnRfY2xhc3M9ImhvbGQuaXNzdWVkIiwKICAgICAgICAgICAgZGV
0YWlscz17ImNvbmZpcm1hdGlvbl9yZWYiOiBjb25maXJtYXRpb25fcmVmLAogICAgICAgICAgICAgIC
AgICAgICAicmVhc29ucyI6IGRlY2lzaW9uX3JlYXNvbnN9LAogICAgICAgICAgICBhY3Rvcl9pZD1vc
GVyYXRvci51c2VybmFtZSwgbW9kZT1tb2RlLAogICAgICAgICAgICBvcGVyYXRvcl9pZD1vcGVyYXRv
ci51c2VybmFtZSwgY29ycmVsYXRpb25faWQ9Y2lkLAogICAgICAgICAgICBkYXRhX2NsYXNzPV9EQVR
BX0NMQVNTKQogICAgICAgIGF3YWl0IGF1ZGl0KHNlc3Npb24sICJwYXBlci5yaXNrLmhvbGRfaXNzdW
VkIiwKICAgICAgICAgICAgICAgICAgICBkZXRhaWxzPXsiY29uZmlybWF0aW9uX3JlZiI6IGNvbmZpc
m1hdGlvbl9yZWZ9LAogICAgICAgICAgICAgICAgICAgIG1vZGU9bW9kZSwgb3BlcmF0b3JfaWQ9b3Bl
cmF0b3IudXNlcm5hbWUsCiAgICAgICAgICAgICAgICAgICAgY29ycmVsYXRpb25faWQ9Y2lkLCByZXN
vdXJjZV9pZD1pbnRlbnQuaWQpCiAgICBhc3NlcnQgbm90IGV2LnJlZnVzZWQKICAgIGF3YWl0IHNlc3
Npb24uY29tbWl0KCkKICAgIHN0YXRlID0gYXdhaXQgY3VycmVudF9zdGF0ZShzZXNzaW9uLCBpbnRlb
nQuaWQpCiAgICByZXR1cm4geyJvdXRjb21lIjogInJlZ2lzdGVyZWQiLCAib3JkZXJfaWQiOiBpbnRl
bnQuaWQsCiAgICAgICAgICAgICJzdGF0ZSI6IHN0YXRlLCAiZGVjaXNpb24iOiBkZWNpc2lvbiwKICA
gICAgICAgICAgImNvbmZpcm1hdGlvbl9yZWYiOiBjb25maXJtYXRpb25fcmVmLAogICAgICAgICAgIC
AicmVhc29ucyI6IGRlY2lzaW9uX3JlYXNvbnMsICoqX2VudmVsb3BlKHJlcXVlc3QpfQoKCkByb3V0Z
XIucG9zdCgiL29yZGVycy9jb25maXJtIikKYXN5bmMgZGVmIGFwaV9jb25maXJtX29yZGVyKAogICAg
Ym9keTogT3JkZXJDb25maXJtLCByZXF1ZXN0OiBSZXF1ZXN0LCBvcGVyYXRvcjogUmVxdWlyZU9yZGV
yc0NvbmZpcm0sCiAgICBzZXNzaW9uOiBBbm5vdGF0ZWRbQXN5bmNTZXNzaW9uLCBEZXBlbmRzKGdldF
9kYl9zZXNzaW9uKV0sCik6CiAgICBtb2RlID0gX3JlcXVpcmVfcGFwZXIocmVxdWVzdCkKICAgIHJlc
3VsdCA9IGF3YWl0IGNvbmZpcm1faG9sZCgKICAgICAgICBzZXNzaW9uLCBpbnRlbnRfcm93X2lkPWJv
ZHkub3JkZXJfaWQsCiAgICAgICAgc3VwcGxpZWRfcmVmPWJvZHkuY29uZmlybWF0aW9uX3JlZiwgcmV
zb2x2ZV90bz1ib2R5LnJlc29sdmVfdG8sCiAgICAgICAgYWN0b3JfaWQ9b3BlcmF0b3IudXNlcm5hbW
UsIG1vZGU9bW9kZSwKICAgICAgICBvcGVyYXRvcl9pZD1vcGVyYXRvci51c2VybmFtZSwgY29ycmVsY
XRpb25faWQ9X2NpZChyZXF1ZXN0KSwKICAgICAgICBkYXRhX2NsYXNzPV9EQVRBX0NMQVNTKQogICAg
aWYgbm90IHJlc3VsdC5yZWZ1c2VkOgogICAgICAgIGF3YWl0IHNlc3Npb24uY29tbWl0KCkKICAgIHN
0YXRlID0gYXdhaXQgY3VycmVudF9zdGF0ZShzZXNzaW9uLCBib2R5Lm9yZGVyX2lkKQogICAgcmV0dX
JuIHsib3V0Y29tZSI6IHJlc3VsdC5vdXRjb21lLCAic3RhdGUiOiBzdGF0ZSwKICAgICAgICAgICAgI
nJlYXNvbnMiOiByZXN1bHQucmVhc29ucywgKipfZW52ZWxvcGUocmVxdWVzdCl9CgoKQHJvdXRlci5w
b3N0KCIvb3JkZXJzL2NhbmNlbCIpCmFzeW5jIGRlZiBhcGlfY2FuY2VsX29yZGVyKAogICAgYm9keTo
gT3JkZXJDYW5jZWwsIHJlcXVlc3Q6IFJlcXVlc3QsIG9wZXJhdG9yOiBSZXF1aXJlT3JkZXJzQ2FuY2
VsLAogICAgc2Vzc2lvbjogQW5ub3RhdGVkW0FzeW5jU2Vzc2lvbiwgRGVwZW5kcyhnZXRfZGJfc2Vzc
2lvbildLAopOgogICAgbW9kZSA9IF9yZXF1aXJlX3BhcGVyKHJlcXVlc3QpCiAgICByZXN1bHQgPSBh
d2FpdCBjYW5jZWxfb3JkZXIoCiAgICAgICAgc2Vzc2lvbiwgaW50ZW50X3Jvd19pZD1ib2R5Lm9yZGV
yX2lkLCBhY3Rvcl9pZD1vcGVyYXRvci51c2VybmFtZSwKICAgICAgICBtb2RlPW1vZGUsIG9wZXJhdG
9yX2lkPW9wZXJhdG9yLnVzZXJuYW1lLAogICAgICAgIGNvcnJlbGF0aW9uX2lkPV9jaWQocmVxdWVzd
CksIGRhdGFfY2xhc3M9X0RBVEFfQ0xBU1MpCiAgICBpZiBub3QgcmVzdWx0LnJlZnVzZWQ6CiAgICAg
ICAgYXdhaXQgc2Vzc2lvbi5jb21taXQoKQogICAgc3RhdGUgPSBhd2FpdCBjdXJyZW50X3N0YXRlKHN
lc3Npb24sIGJvZHkub3JkZXJfaWQpCiAgICByZXR1cm4geyJvdXRjb21lIjogcmVzdWx0Lm91dGNvbW
UsICJzdGF0ZSI6IHN0YXRlLAogICAgICAgICAgICAicmVhc29ucyI6IHJlc3VsdC5yZWFzb25zLCAqK
l9lbnZlbG9wZShyZXF1ZXN0KX0KCgpAcm91dGVyLnBvc3QoIi9vcmRlcnMve29yZGVyX2lkfS9ydW4i
KQphc3luYyBkZWYgYXBpX3J1bl9vcmRlcigKICAgIG9yZGVyX2lkOiBzdHIsIGJvZHk6IE9yZGVyUnV
uLCByZXF1ZXN0OiBSZXF1ZXN0LAogICAgb3BlcmF0b3I6IFJlcXVpcmVPcmRlcnNQbGFjZSwKICAgIH
Nlc3Npb246IEFubm90YXRlZFtBc3luY1Nlc3Npb24sIERlcGVuZHMoZ2V0X2RiX3Nlc3Npb24pXSwKK
ToKICAgICIiIkdvdmVybmVkIHNpbXVsYXRvciBpbnZvY2F0aW9uIChtYW51YWwsIFEzKS4gRW5mb3Jj
ZXMgbWF5X2V4ZWN1dGUuIiIiCiAgICBtb2RlID0gX3JlcXVpcmVfcGFwZXIocmVxdWVzdCkKICAgIGN
pZCA9IF9jaWQocmVxdWVzdCkKICAgIGludGVudCA9IGF3YWl0IGdldF9pbnRlbnQoc2Vzc2lvbiwgb3
JkZXJfaWQpCiAgICBpZiBpbnRlbnQgaXMgTm9uZToKICAgICAgICByYWlzZSBIVFRQRXhjZXB0aW9uK
HN0YXR1c19jb2RlPTQwNCwgZGV0YWlsPSJVbmtub3duIG9yZGVyIikKCiAgICBhbGxvd2VkLCByZWFz
b25zID0gYXdhaXQgbWF5X2V4ZWN1dGUoc2Vzc2lvbiwgb3JkZXJfaWQpCiAgICBpZiBub3QgYWxsb3d
lZDoKICAgICAgICBhd2FpdCBhdWRpdChzZXNzaW9uLCAicGFwZXIub3JkZXIucnVuX3JlZnVzZWQiLA
ogICAgICAgICAgICAgICAgICAgIGRldGFpbHM9eyJyZWFzb25zIjogcmVhc29uc30sIG1vZGU9bW9kZ
SwKICAgICAgICAgICAgICAgICAgICBvcGVyYXRvcl9pZD1vcGVyYXRvci51c2VybmFtZSwgY29ycmVs
YXRpb25faWQ9Y2lkLAogICAgICAgICAgICAgICAgICAgIHJlc291cmNlX2lkPW9yZGVyX2lkKQogICA
gICAgIGF3YWl0IHNlc3Npb24uY29tbWl0KCkKICAgICAgICByZXR1cm4geyJvdXRjb21lIjogInJlZn
VzZWQiLCAic3RhdGUiOiBhd2FpdCBjdXJyZW50X3N0YXRlKAogICAgICAgICAgICBzZXNzaW9uLCBvc
mRlcl9pZCksICJyZWFzb25zIjogcmVhc29ucywgKipfZW52ZWxvcGUocmVxdWVzdCl9CgogICAgc3Rh
dGUgPSBhd2FpdCBjdXJyZW50X3N0YXRlKHNlc3Npb24sIG9yZGVyX2lkKQogICAgaWYgc3RhdGUgIT0
gInJpc2tfcGFzc2VkIjoKICAgICAgICBhd2FpdCBhdWRpdChzZXNzaW9uLCAicGFwZXIub3JkZXIucn
VuX3JlZnVzZWQiLAogICAgICAgICAgICAgICAgICAgIGRldGFpbHM9eyJzdGF0ZSI6IHN0YXRlfSwgb
W9kZT1tb2RlLAogICAgICAgICAgICAgICAgICAgIG9wZXJhdG9yX2lkPW9wZXJhdG9yLnVzZXJuYW1l
LCBjb3JyZWxhdGlvbl9pZD1jaWQsCiAgICAgICAgICAgICAgICAgICAgcmVzb3VyY2VfaWQ9b3JkZXJ
faWQpCiAgICAgICAgYXdhaXQgc2Vzc2lvbi5jb21taXQoKQogICAgICAgIHJldHVybiB7Im91dGNvbW
UiOiAicmVmdXNlZCIsICJzdGF0ZSI6IHN0YXRlLAogICAgICAgICAgICAgICAgInJlYXNvbnMiOiBbe
yJmYWlsaW5nIjogInN0YXRlIiwgInZhbHVlIjogc3RhdGV9XSwKICAgICAgICAgICAgICAgICoqX2Vu
dmVsb3BlKHJlcXVlc3QpfQoKICAgICMgSWRlbXBvdGVudCByZS1ydW46IGV4aXN0aW5nIGZpbGxzID0
+IGNvbnZlcmdlLCBubyByZS1leGVjdXRpb24gKFM4KS4KICAgIGV4aXN0aW5nX2ZpbGxzID0gbGlzdC
goYXdhaXQgc2Vzc2lvbi5leGVjdXRlKAogICAgICAgIHNlbGVjdChWMlBhcGVyRmlsbCkud2hlcmUoV
jJQYXBlckZpbGwuaW50ZW50X2lkID09IG9yZGVyX2lkKQogICAgKSkuc2NhbGFycygpLmFsbCgpKQog
ICAgaWYgZXhpc3RpbmdfZmlsbHM6CiAgICAgICAgYXdhaXQgYXVkaXQoc2Vzc2lvbiwgInBhcGVyLm9
yZGVyLnJ1bl9yZXVzZWQiLAogICAgICAgICAgICAgICAgICAgIGRldGFpbHM9eyJmaWxsX2NvdW50Ij
ogbGVuKGV4aXN0aW5nX2ZpbGxzKX0sIG1vZGU9bW9kZSwKICAgICAgICAgICAgICAgICAgICBvcGVyY
XRvcl9pZD1vcGVyYXRvci51c2VybmFtZSwgY29ycmVsYXRpb25faWQ9Y2lkLAogICAgICAgICAgICAg
ICAgICAgIHJlc291cmNlX2lkPW9yZGVyX2lkKQogICAgICAgIGF3YWl0IHNlc3Npb24uY29tbWl0KCk
KICAgICAgICByZXR1cm4geyJvdXRjb21lIjogInJldXNlZCIsICJzdGF0ZSI6IHN0YXRlLAogICAgIC
AgICAgICAgICAgImZpbGxfY291bnQiOiBsZW4oZXhpc3RpbmdfZmlsbHMpLCAicmVhc29ucyI6IFtdL
AogICAgICAgICAgICAgICAgKipfZW52ZWxvcGUocmVxdWVzdCl9CgogICAgZXYgPSBhd2FpdCBhcHBl
bmRfZXZlbnQoCiAgICAgICAgc2Vzc2lvbiwgaW50ZW50X3Jvd19pZD1vcmRlcl9pZCwgZnJvbV9zdGF
0ZT0icmlza19wYXNzZWQiLAogICAgICAgIHRvX3N0YXRlPSJleGVjdXRpbmciLCBldmVudF9jbGFzcz
0iZXhlY3V0aW9uLnN0YXJ0ZWQiLCBkZXRhaWxzPXt9LAogICAgICAgIGFjdG9yX2lkPW9wZXJhdG9yL
nVzZXJuYW1lLCBtb2RlPW1vZGUsCiAgICAgICAgb3BlcmF0b3JfaWQ9b3BlcmF0b3IudXNlcm5hbWUs
IGNvcnJlbGF0aW9uX2lkPWNpZCwKICAgICAgICBkYXRhX2NsYXNzPV9EQVRBX0NMQVNTKQogICAgYXN
zZXJ0IG5vdCBldi5yZWZ1c2VkCgogICAgdHlwZWQgPSBQYXBlck9yZGVySW50ZW50KAogICAgICAgIG
ludGVudF9pZD1pbnRlbnQuaW50ZW50X2lkLCBhY2NvdW50X2lkPWludGVudC5hY2NvdW50X2lkLAogI
CAgICAgIGluc3RydW1lbnRfaWQ9aW50ZW50Lmluc3RydW1lbnRfaWQsIHNpZGU9aW50ZW50LnNpZGUs
CiAgICAgICAgb3JkZXJfdHlwZT1pbnRlbnQub3JkZXJfdHlwZSwgcXVhbnRpdHk9RGVjaW1hbChpbnR
lbnQucXVhbnRpdHkpLAogICAgICAgIGxpbWl0X3ByaWNlPShEZWNpbWFsKGludGVudC5saW1pdF9wcm
ljZSkKICAgICAgICAgICAgICAgICAgICAgaWYgaW50ZW50LmxpbWl0X3ByaWNlIGlzIG5vdCBOb25lI
GVsc2UgTm9uZSksCiAgICAgICAgc25hcHNob3RfcmVmPWludGVudC5zbmFwc2hvdF9yZWYsCiAgICAg
ICAgd2luZG93X3N0YXJ0PXN0cihpbnRlbnQudGltZV9iYXNpcy5nZXQoIndpbmRvd19zdGFydCIpKSw
KICAgICAgICB3aW5kb3dfZW5kPXN0cihpbnRlbnQudGltZV9iYXNpcy5nZXQoIndpbmRvd19lbmQiKS
ksCiAgICAgICAgY29zdF9tb2RlbD1ib2R5LmNvc3RfbW9kZWwgb3IgewogICAgICAgICAgICAic3ByZ
WFkIjogeyJ2YWx1ZSI6ICIwIiwgInVuaXQiOiAicHJpY2UiLCAiY2l0YXRpb24iOiAibm9uZSJ9LAog
ICAgICAgICAgICAiY29tbWlzc2lvbiI6IHsidmFsdWUiOiAiMCIsICJ1bml0IjogInByaWNlIiwKICA
gICAgICAgICAgICAgICAgICAgICAgICAgImNpdGF0aW9uIjogIm5vbmUifSwKICAgICAgICAgICAgIn
NsaXBwYWdlIjogeyJ2YWx1ZSI6ICIwIiwgInVuaXQiOiAicHJpY2UiLCAiY2l0YXRpb24iOiAibm9uZ
SJ9LAogICAgICAgIH0pCiAgICB0cnk6CiAgICAgICAgcmVzdWx0ID0gcnVuX3NpbXVsYXRpb24oCiAg
ICAgICAgICAgIHR5cGVkLCBib2R5LmJhcnMsCiAgICAgICAgICAgIHN0b3JlZF9jb250ZW50X2hhc2g
9aW50ZW50LnRpbWVfYmFzaXNbInNuYXBzaG90X2NvbnRlbnRfaGFzaCJdKQogICAgZXhjZXB0IFBhcG
VyUmVmdXNlZCBhcyBleGM6CiAgICAgICAgZXYgPSBhd2FpdCBhcHBlbmRfZXZlbnQoCiAgICAgICAgI
CAgIHNlc3Npb24sIGludGVudF9yb3dfaWQ9b3JkZXJfaWQsIGZyb21fc3RhdGU9ImV4ZWN1dGluZyIs
CiAgICAgICAgICAgIHRvX3N0YXRlPSJxdWFyYW50aW5lZF91bmtub3duIiwgZXZlbnRfY2xhc3M9Im9
yZGVyLnF1YXJhbnRpbmVkIiwKICAgICAgICAgICAgZGV0YWlscz17InJlZnVzYWxfY2xhc3MiOiBleG
MucmVmdXNhbF9jbGFzcywKICAgICAgICAgICAgICAgICAgICAgInJlYXNvbnMiOiBleGMucmVhc29uc
30sCiAgICAgICAgICAgIGFjdG9yX2lkPW9wZXJhdG9yLnVzZXJuYW1lLCBtb2RlPW1vZGUsCiAgICAg
ICAgICAgIG9wZXJhdG9yX2lkPW9wZXJhdG9yLnVzZXJuYW1lLCBjb3JyZWxhdGlvbl9pZD1jaWQsCiA
gICAgICAgICAgIGRhdGFfY2xhc3M9X0RBVEFfQ0xBU1MpCiAgICAgICAgYXdhaXQgYXVkaXQoc2Vzc2
lvbiwgInBhcGVyLm9yZGVyLnF1YXJhbnRpbmVkIiwKICAgICAgICAgICAgICAgICAgICBkZXRhaWxzP
XsicmVmdXNhbF9jbGFzcyI6IGV4Yy5yZWZ1c2FsX2NsYXNzfSwKICAgICAgICAgICAgICAgICAgICBt
b2RlPW1vZGUsIG9wZXJhdG9yX2lkPW9wZXJhdG9yLnVzZXJuYW1lLAogICAgICAgICAgICAgICAgICA
gIGNvcnJlbGF0aW9uX2lkPWNpZCwgcmVzb3VyY2VfaWQ9b3JkZXJfaWQpCiAgICAgICAgYXdhaXQgc2
Vzc2lvbi5jb21taXQoKQogICAgICAgIHJldHVybiB7Im91dGNvbWUiOiAicXVhcmFudGluZWQiLCAic
3RhdGUiOiAicXVhcmFudGluZWRfdW5rbm93biIsCiAgICAgICAgICAgICAgICAicmVhc29ucyI6IGV4
Yy5yZWFzb25zLCAqKl9lbnZlbG9wZShyZXF1ZXN0KX0KCiAgICBmb3IgZiBpbiByZXN1bHRbImZpbGx
zIl06CiAgICAgICAgc2Vzc2lvbi5hZGQoVjJQYXBlckZpbGwoCiAgICAgICAgICAgIGZpbGxfaWQ9bm
V3X2lkKCksIGludGVudF9pZD1vcmRlcl9pZCwKICAgICAgICAgICAgZmlsbF9pbmRleD1mWyJmaWxsX
2luZGV4Il0sIHF1YW50aXR5PWZbInF1YW50aXR5Il0sCiAgICAgICAgICAgIHJhd19wcmljZT1mWyJy
YXdfcHJpY2UiXSwgZWZmZWN0aXZlX3ByaWNlPWZbImVmZmVjdGl2ZV9wcmljZSJdLAogICAgICAgICA
gICBjb3N0X21vZGVsX3JlZj10eXBlZC5jb3N0X21vZGVsLCBmaWxsX2NsYXNzPWZbImZpbGxfY2xhc3
MiXSwKICAgICAgICAgICAgc2ltdWxhdG9yX3ZlcnNpb249U0lNVUxBVE9SX1ZFUlNJT04sCiAgICAgI
CAgICAgIHNuYXBzaG90X3JlZj1pbnRlbnQuc25hcHNob3RfcmVmLAogICAgICAgICAgICB0aW1lX2Jh
c2lzPWludGVudC50aW1lX2Jhc2lzLCBkYXRhX2NsYXNzPV9EQVRBX0NMQVNTLAogICAgICAgICAgICB
tb2RlPW1vZGUsIG9wZXJhdG9yX2lkPW9wZXJhdG9yLnVzZXJuYW1lLCBjb3JyZWxhdGlvbl9pZD1jaW
QpKQogICAgYXdhaXQgc2Vzc2lvbi5mbHVzaCgpCgogICAgb3V0Y29tZV9zdGF0ZSA9IHsiZmlsbGVkI
jogImZpbGxlZCIsCiAgICAgICAgICAgICAgICAgICAgICJwYXJ0aWFsbHlfZmlsbGVkIjogInBhcnRp
YWxseV9maWxsZWQiLAogICAgICAgICAgICAgICAgICAgICAiZXhwaXJlZCI6ICJleHBpcmVkIn1bcmV
zdWx0WyJvdXRjb21lIl1dCiAgICBldmVudF9jbGFzcyA9IHsiZmlsbGVkIjogImV4ZWN1dGlvbi5maW
xsZWQiLAogICAgICAgICAgICAgICAgICAgInBhcnRpYWxseV9maWxsZWQiOiAiZXhlY3V0aW9uLnBhc
nRpYWxseV9maWxsZWQiLAogICAgICAgICAgICAgICAgICAgImV4cGlyZWQiOiAiZXhlY3V0aW9uLmV4
cGlyZWQifVtyZXN1bHRbIm91dGNvbWUiXV0KICAgIGV2ID0gYXdhaXQgYXBwZW5kX2V2ZW50KAogICA
gICAgIHNlc3Npb24sIGludGVudF9yb3dfaWQ9b3JkZXJfaWQsIGZyb21fc3RhdGU9ImV4ZWN1dGluZy
IsCiAgICAgICAgdG9fc3RhdGU9b3V0Y29tZV9zdGF0ZSwgZXZlbnRfY2xhc3M9ZXZlbnRfY2xhc3MsC
iAgICAgICAgZGV0YWlscz17ImZpbGxfY291bnQiOiBsZW4ocmVzdWx0WyJmaWxscyJdKSwKICAgICAg
ICAgICAgICAgICAidW5maWxsZWRfcXVhbnRpdHkiOiByZXN1bHRbInVuZmlsbGVkX3F1YW50aXR5Il1
9LAogICAgICAgIGFjdG9yX2lkPW9wZXJhdG9yLnVzZXJuYW1lLCBtb2RlPW1vZGUsCiAgICAgICAgb3
BlcmF0b3JfaWQ9b3BlcmF0b3IudXNlcm5hbWUsIGNvcnJlbGF0aW9uX2lkPWNpZCwKICAgICAgICBkY
XRhX2NsYXNzPV9EQVRBX0NMQVNTKQogICAgYXNzZXJ0IG5vdCBldi5yZWZ1c2VkCgogICAgaWYgb3V0
Y29tZV9zdGF0ZSBpbiAoImZpbGxlZCIsICJwYXJ0aWFsbHlfZmlsbGVkIik6CiAgICAgICAgZXYgPSB
hd2FpdCBhcHBlbmRfZXZlbnQoCiAgICAgICAgICAgIHNlc3Npb24sIGludGVudF9yb3dfaWQ9b3JkZX
JfaWQsIGZyb21fc3RhdGU9b3V0Y29tZV9zdGF0ZSwKICAgICAgICAgICAgdG9fc3RhdGU9InNldHRsZ
WQiLCBldmVudF9jbGFzcz0ib3JkZXIuc2V0dGxlZCIsCiAgICAgICAgICAgIGRldGFpbHM9eyJ2b2lk
ZWRfcmVtYWluZGVyIjogcmVzdWx0WyJ1bmZpbGxlZF9xdWFudGl0eSJdfSwKICAgICAgICAgICAgYWN
0b3JfaWQ9b3BlcmF0b3IudXNlcm5hbWUsIG1vZGU9bW9kZSwKICAgICAgICAgICAgb3BlcmF0b3JfaW
Q9b3BlcmF0b3IudXNlcm5hbWUsIGNvcnJlbGF0aW9uX2lkPWNpZCwKICAgICAgICAgICAgZGF0YV9jb
GFzcz1fREFUQV9DTEFTUykKICAgICAgICBhc3NlcnQgbm90IGV2LnJlZnVzZWQKCiAgICAgICAgIyBE
ZXJpdmVkIGFydGlmYWN0cyAoUzUpOiBwb3NpdGlvbnMgKyBiYWxhbmNlcyB3aXRoIGFuY2hvcnMuCiA
gICAgICAgZnJvbSBhcHAuZGIubW9kZWxzLnYyX3BhcGVyX3RyYWRpbmcgaW1wb3J0IFYyUGFwZXJBY2
NvdW50CiAgICAgICAgYWNjdCA9IChhd2FpdCBzZXNzaW9uLmV4ZWN1dGUoCiAgICAgICAgICAgIHNlb
GVjdChWMlBhcGVyQWNjb3VudCkKICAgICAgICAgICAgLndoZXJlKFYyUGFwZXJBY2NvdW50LmlkID09
IGludGVudC5hY2NvdW50X2lkKQogICAgICAgICkpLnNjYWxhcl9vbmUoKQogICAgICAgIGZpbGxzX2F
sbCA9IGF3YWl0IGNvbGxlY3RfYWNjb3VudF9maWxscyhzZXNzaW9uLCBhY2N0LmlkKQogICAgICAgIG
1hcmtzID0ge2ludGVudC5pbnN0cnVtZW50X2lkOgogICAgICAgICAgICAgICAgIERlY2ltYWwoc3RyK
GJvZHkuYmFyc1stMV1bImNsb3NlIl0pKSBpZiBib2R5LmJhcnMKICAgICAgICAgICAgICAgICBlbHNl
IERlY2ltYWwoMCl9CiAgICAgICAgYmFsYW5jZSA9IGRlcml2ZV9iYWxhbmNlKAogICAgICAgICAgICB
pbml0aWFsX2JhbGFuY2U9RGVjaW1hbChhY2N0LmluaXRpYWxfYmFsYW5jZSksCiAgICAgICAgICAgIG
ZpbGxzPWZpbGxzX2FsbCwgbWFya3M9bWFya3MsCiAgICAgICAgICAgIG1hcmdpbl9wYXJhbXM9YWNjd
C5tYXJnaW5fcGFyYW1zKQogICAgICAgIGRfaGFzaCA9IGRlcml2YXRpb25faGFzaCh7ImZpbGxzIjog
ZmlsbHNfYWxsLCAibWFya3MiOiB7CiAgICAgICAgICAgIGs6IHN0cih2KSBmb3IgaywgdiBpbiBtYXJ
rcy5pdGVtcygpfX0pCiAgICAgICAgZXZfaGFzaCA9IGVuZ2luZV92ZXJzaW9uc19oYXNoKCkKICAgIC
AgICBzZXNzaW9uLmFkZChWMlBhcGVyUG9zaXRpb25TbmFwc2hvdCgKICAgICAgICAgICAgYWNjb3Vud
F9pZD1hY2N0LmlkLAogICAgICAgICAgICBhc19vZl9iYXNpcz17IndpbmRvd19lbmQiOiBzdHIoCiAg
ICAgICAgICAgICAgICBpbnRlbnQudGltZV9iYXNpcy5nZXQoIndpbmRvd19lbmQiKSl9LAogICAgICA
gICAgICBwb3NpdGlvbnM9YmFsYW5jZVsicG9zaXRpb25zIl0sCiAgICAgICAgICAgIGRlcml2YXRpb2
5faW5wdXRzX2hhc2g9ZF9oYXNoLCBlbmdpbmVfdmVyc2lvbnNfaGFzaD1ldl9oYXNoLAogICAgICAgI
CAgICBkYXRhX2NsYXNzPV9EQVRBX0NMQVNTLCBtb2RlPW1vZGUsCiAgICAgICAgICAgIG9wZXJhdG9y
X2lkPW9wZXJhdG9yLnVzZXJuYW1lLCBjb3JyZWxhdGlvbl9pZD1jaWQpKQogICAgICAgIHNlc3Npb24
uYWRkKFYyUGFwZXJCYWxhbmNlU25hcHNob3QoCiAgICAgICAgICAgIGFjY291bnRfaWQ9YWNjdC5pZC
wKICAgICAgICAgICAgYXNfb2ZfYmFzaXM9eyJ3aW5kb3dfZW5kIjogc3RyKAogICAgICAgICAgICAgI
CAgaW50ZW50LnRpbWVfYmFzaXMuZ2V0KCJ3aW5kb3dfZW5kIikpLAogICAgICAgICAgICAgICAgInBv
c2l0aW9ucyI6IGJhbGFuY2VbInBvc2l0aW9ucyJdfSwKICAgICAgICAgICAgY2FzaD1iYWxhbmNlWyJ
jYXNoIl0sIGVxdWl0eT1iYWxhbmNlWyJlcXVpdHkiXSwKICAgICAgICAgICAgbWFyZ2luX3VzZWQ9Ym
FsYW5jZVsibWFyZ2luX3VzZWQiXSwKICAgICAgICAgICAgbWFyZ2luX2F2YWlsYWJsZT1iYWxhbmNlW
yJtYXJnaW5fYXZhaWxhYmxlIl0sCiAgICAgICAgICAgIHVucmVhbGl6ZWRfcG5sPWJhbGFuY2VbInVu
cmVhbGl6ZWRfcG5sIl0sCiAgICAgICAgICAgIHJlYWxpemVkX3BubD1iYWxhbmNlWyJyZWFsaXplZF9
wbmwiXSwKICAgICAgICAgICAgZGVyaXZhdGlvbl9pbnB1dHNfaGFzaD1kX2hhc2gsIGVuZ2luZV92ZX
JzaW9uc19oYXNoPWV2X2hhc2gsCiAgICAgICAgICAgIGRhdGFfY2xhc3M9X0RBVEFfQ0xBU1MsIG1vZ
GU9bW9kZSwKICAgICAgICAgICAgb3BlcmF0b3JfaWQ9b3BlcmF0b3IudXNlcm5hbWUsIGNvcnJlbGF0
aW9uX2lkPWNpZCkpCiAgICAgICAgYXdhaXQgc2Vzc2lvbi5mbHVzaCgpCiAgICAgICAgYXdhaXQgcnV
uX3JlY29uY2lsaWF0aW9uKAogICAgICAgICAgICBzZXNzaW9uLCBhY2NvdW50X3Jvd19pZD1hY2N0Lm
lkLAogICAgICAgICAgICBpbml0aWFsX2JhbGFuY2U9RGVjaW1hbChhY2N0LmluaXRpYWxfYmFsYW5jZ
SksCiAgICAgICAgICAgIG1hcmtzPW1hcmtzLCBtYXJnaW5fcGFyYW1zPWFjY3QubWFyZ2luX3BhcmFt
cywKICAgICAgICAgICAgbW9kZT1tb2RlLCBvcGVyYXRvcl9pZD1vcGVyYXRvci51c2VybmFtZSwgY29
ycmVsYXRpb25faWQ9Y2lkLAogICAgICAgICAgICBkYXRhX2NsYXNzPV9EQVRBX0NMQVNTKQoKICAgIG
F3YWl0IGF1ZGl0KHNlc3Npb24sICJwYXBlci5vcmRlci5leGVjdXRlZCIsCiAgICAgICAgICAgICAgI
CBkZXRhaWxzPXsib3V0Y29tZSI6IHJlc3VsdFsib3V0Y29tZSJdLAogICAgICAgICAgICAgICAgICAg
ICAgICAgImZpbGxfY291bnQiOiBsZW4ocmVzdWx0WyJmaWxscyJdKX0sCiAgICAgICAgICAgICAgICB
tb2RlPW1vZGUsIG9wZXJhdG9yX2lkPW9wZXJhdG9yLnVzZXJuYW1lLAogICAgICAgICAgICAgICAgY2
9ycmVsYXRpb25faWQ9Y2lkLCByZXNvdXJjZV9pZD1vcmRlcl9pZCkKICAgIGF3YWl0IHNlc3Npb24uY
29tbWl0KCkKICAgIHJldHVybiB7Im91dGNvbWUiOiByZXN1bHRbIm91dGNvbWUiXSwKICAgICAgICAg
ICAgInN0YXRlIjogYXdhaXQgY3VycmVudF9zdGF0ZShzZXNzaW9uLCBvcmRlcl9pZCksCiAgICAgICA
gICAgICJmaWxscyI6IHJlc3VsdFsiZmlsbHMiXSwKICAgICAgICAgICAgImVuZ2luZV92ZXJzaW9ucy
I6IEVOR0lORV9WRVJTSU9OUywKICAgICAgICAgICAgInJlYXNvbnMiOiBbXSwgKipfZW52ZWxvcGUoc
mVxdWVzdCl9CgoKIyAtLS0gcmVhZHMgLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0t
LS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLQoKCkByb3V0ZXIuZ2V0KCIvYWNjb3VudHM
iKQphc3luYyBkZWYgYXBpX2xpc3RfYWNjb3VudHMoCiAgICByZXF1ZXN0OiBSZXF1ZXN0LCBvcGVyYX
RvcjogUmVxdWlyZUFjY291bnRzUmVhZCwKICAgIHNlc3Npb246IEFubm90YXRlZFtBc3luY1Nlc3Npb
24sIERlcGVuZHMoZ2V0X2RiX3Nlc3Npb24pXSwKICAgIGxpbWl0OiBpbnQgPSBRdWVyeShkZWZhdWx0
PTEwMCwgZ2U9MSwgbGU9NTAwKSwKKToKICAgIGZyb20gYXBwLmRiLm1vZGVscy52Ml9wYXBlcl90cmF
kaW5nIGltcG9ydCBWMlBhcGVyQWNjb3VudAogICAgcm93cyA9IGxpc3QoKGF3YWl0IHNlc3Npb24uZX
hlY3V0ZSgKICAgICAgICBzZWxlY3QoVjJQYXBlckFjY291bnQpLm9yZGVyX2J5KFYyUGFwZXJBY2Nvd
W50LmNyZWF0ZWRfYXQuZGVzYygpKQogICAgICAgIC5saW1pdChsaW1pdCkpKS5zY2FsYXJzKCkuYWxs
KCkpCiAgICByZXR1cm4geyJhY2NvdW50cyI6IFsKICAgICAgICB7ImlkIjogci5pZCwgImFjY291bnR
faWQiOiByLmFjY291bnRfaWQsICJyZWNvcmRfc2VxIjogci5yZWNvcmRfc2VxLAogICAgICAgICAibm
FtZSI6IHIubmFtZSwgImxpZmVjeWNsZV9zdGF0ZSI6IHIubGlmZWN5Y2xlX3N0YXRlLAogICAgICAgI
CAiYmFzZV9jdXJyZW5jeSI6IHIuYmFzZV9jdXJyZW5jeSwKICAgICAgICAgImluaXRpYWxfYmFsYW5j
ZSI6IHIuaW5pdGlhbF9iYWxhbmNlfSBmb3IgciBpbiByb3dzXSwKICAgICAgICAqKl9lbnZlbG9wZSh
yZXF1ZXN0KX0KCgpAcm91dGVyLmdldCgiL29yZGVycyIpCmFzeW5jIGRlZiBhcGlfbGlzdF9vcmRlcn
MoCiAgICByZXF1ZXN0OiBSZXF1ZXN0LCBvcGVyYXRvcjogUmVxdWlyZU9yZGVyc1JlYWQsCiAgICBzZ
XNzaW9uOiBBbm5vdGF0ZWRbQXN5bmNTZXNzaW9uLCBEZXBlbmRzKGdldF9kYl9zZXNzaW9uKV0sCiAg
ICBsaW1pdDogaW50ID0gUXVlcnkoZGVmYXVsdD0xMDAsIGdlPTEsIGxlPTUwMCksCik6CiAgICByb3d
zID0gbGlzdCgoYXdhaXQgc2Vzc2lvbi5leGVjdXRlKAogICAgICAgIHNlbGVjdChWMlBhcGVyT3JkZX
JJbnRlbnQpCiAgICAgICAgLm9yZGVyX2J5KFYyUGFwZXJPcmRlckludGVudC5jcmVhdGVkX2F0LmRlc
2MoKSkKICAgICAgICAubGltaXQobGltaXQpKSkuc2NhbGFycygpLmFsbCgpKQogICAgb3V0ID0gW10K
ICAgIGZvciByIGluIHJvd3M6CiAgICAgICAgb3V0LmFwcGVuZCh7ImlkIjogci5pZCwgImludGVudF9
pZCI6IHIuaW50ZW50X2lkLAogICAgICAgICAgICAgICAgICAgICJhY2NvdW50X2lkIjogci5hY2NvdW
50X2lkLCAic2lkZSI6IHIuc2lkZSwKICAgICAgICAgICAgICAgICAgICAib3JkZXJfdHlwZSI6IHIub
3JkZXJfdHlwZSwgInF1YW50aXR5Ijogci5xdWFudGl0eSwKICAgICAgICAgICAgICAgICAgICAic3Rh
dGUiOiBhd2FpdCBjdXJyZW50X3N0YXRlKHNlc3Npb24sIHIuaWQpfSkKICAgIHJldHVybiB7Im9yZGV
ycyI6IG91dCwgKipfZW52ZWxvcGUocmVxdWVzdCl9CgoKQHJvdXRlci5nZXQoIi9vcmRlcnMve29yZG
VyX2lkfS9ldmVudHMiKQphc3luYyBkZWYgYXBpX29yZGVyX2V2ZW50cygKICAgIG9yZGVyX2lkOiBzd
HIsIHJlcXVlc3Q6IFJlcXVlc3QsIG9wZXJhdG9yOiBSZXF1aXJlT3JkZXJzUmVhZCwKICAgIHNlc3Np
b246IEFubm90YXRlZFtBc3luY1Nlc3Npb24sIERlcGVuZHMoZ2V0X2RiX3Nlc3Npb24pXSwKKToKICA
gIHJvd3MgPSBsaXN0KChhd2FpdCBzZXNzaW9uLmV4ZWN1dGUoCiAgICAgICAgc2VsZWN0KFYyUGFwZX
JPcmRlckV2ZW50KQogICAgICAgIC53aGVyZShWMlBhcGVyT3JkZXJFdmVudC5pbnRlbnRfaWQgPT0gb
3JkZXJfaWQpCiAgICAgICAgLm9yZGVyX2J5KFYyUGFwZXJPcmRlckV2ZW50LmV2ZW50X2luZGV4KSkp
LnNjYWxhcnMoKS5hbGwoKSkKICAgIHJldHVybiB7ImV2ZW50cyI6IFsKICAgICAgICB7ImV2ZW50X2l
uZGV4Ijogci5ldmVudF9pbmRleCwgImZyb21fc3RhdGUiOiByLmZyb21fc3RhdGUsCiAgICAgICAgIC
J0b19zdGF0ZSI6IHIudG9fc3RhdGUsICJldmVudF9jbGFzcyI6IHIuZXZlbnRfY2xhc3MsCiAgICAgI
CAgICJkZXRhaWxzIjogci5kZXRhaWxzfSBmb3IgciBpbiByb3dzXSwgKipfZW52ZWxvcGUocmVxdWVz
dCl9CgoKQHJvdXRlci5nZXQoIi9maWxscyIpCmFzeW5jIGRlZiBhcGlfbGlzdF9maWxscygKICAgIHJ
lcXVlc3Q6IFJlcXVlc3QsIG9wZXJhdG9yOiBSZXF1aXJlRmlsbHNSZWFkLAogICAgc2Vzc2lvbjogQW
5ub3RhdGVkW0FzeW5jU2Vzc2lvbiwgRGVwZW5kcyhnZXRfZGJfc2Vzc2lvbildLAogICAgbGltaXQ6I
GludCA9IFF1ZXJ5KGRlZmF1bHQ9MTAwLCBnZT0xLCBsZT01MDApLAopOgogICAgcm93cyA9IGxpc3Qo
KGF3YWl0IHNlc3Npb24uZXhlY3V0ZSgKICAgICAgICBzZWxlY3QoVjJQYXBlckZpbGwpLm9yZGVyX2J
5KFYyUGFwZXJGaWxsLmNyZWF0ZWRfYXQuZGVzYygpKQogICAgICAgIC5saW1pdChsaW1pdCkpKS5zY2
FsYXJzKCkuYWxsKCkpCiAgICByZXR1cm4geyJmaWxscyI6IFsKICAgICAgICB7ImlkIjogci5pZCwgI
mludGVudF9pZCI6IHIuaW50ZW50X2lkLCAiZmlsbF9pbmRleCI6IHIuZmlsbF9pbmRleCwKICAgICAg
ICAgInF1YW50aXR5Ijogci5xdWFudGl0eSwgInJhd19wcmljZSI6IHIucmF3X3ByaWNlLAogICAgICA
gICAiZWZmZWN0aXZlX3ByaWNlIjogci5lZmZlY3RpdmVfcHJpY2UsCiAgICAgICAgICJmaWxsX2NsYX
NzIjogci5maWxsX2NsYXNzLAogICAgICAgICAic2ltdWxhdG9yX3ZlcnNpb24iOiByLnNpbXVsYXRvc
l92ZXJzaW9ufSBmb3IgciBpbiByb3dzXSwKICAgICAgICAqKl9lbnZlbG9wZShyZXF1ZXN0KX0KCgpA
cm91dGVyLmdldCgiL3Bvc2l0aW9ucyIpCmFzeW5jIGRlZiBhcGlfbGlzdF9wb3NpdGlvbnMoCiAgICB
yZXF1ZXN0OiBSZXF1ZXN0LCBvcGVyYXRvcjogUmVxdWlyZUFjY291bnRzUmVhZCwKICAgIHNlc3Npb2
46IEFubm90YXRlZFtBc3luY1Nlc3Npb24sIERlcGVuZHMoZ2V0X2RiX3Nlc3Npb24pXSwKICAgIGxpb
Wl0OiBpbnQgPSBRdWVyeShkZWZhdWx0PTEwMCwgZ2U9MSwgbGU9NTAwKSwKKToKICAgIHJvd3MgPSBs
aXN0KChhd2FpdCBzZXNzaW9uLmV4ZWN1dGUoCiAgICAgICAgc2VsZWN0KFYyUGFwZXJQb3NpdGlvblN
uYXBzaG90KQogICAgICAgIC5vcmRlcl9ieShWMlBhcGVyUG9zaXRpb25TbmFwc2hvdC5jcmVhdGVkX2
F0LmRlc2MoKSkKICAgICAgICAubGltaXQobGltaXQpKSkuc2NhbGFycygpLmFsbCgpKQogICAgcmV0d
XJuIHsicG9zaXRpb25zIjogWwogICAgICAgIHsiaWQiOiByLmlkLCAiYWNjb3VudF9pZCI6IHIuYWNj
b3VudF9pZCwKICAgICAgICAgInBvc2l0aW9ucyI6IHIucG9zaXRpb25zLCAiYXNfb2ZfYmFzaXMiOiB
yLmFzX29mX2Jhc2lzfQogICAgICAgIGZvciByIGluIHJvd3NdLCAqKl9lbnZlbG9wZShyZXF1ZXN0KX
0KCgpAcm91dGVyLmdldCgiL2JhbGFuY2VzIikKYXN5bmMgZGVmIGFwaV9saXN0X2JhbGFuY2VzKAogI
CAgcmVxdWVzdDogUmVxdWVzdCwgb3BlcmF0b3I6IFJlcXVpcmVBY2NvdW50c1JlYWQsCiAgICBzZXNz
aW9uOiBBbm5vdGF0ZWRbQXN5bmNTZXNzaW9uLCBEZXBlbmRzKGdldF9kYl9zZXNzaW9uKV0sCiAgICB
saW1pdDogaW50ID0gUXVlcnkoZGVmYXVsdD0xMDAsIGdlPTEsIGxlPTUwMCksCik6CiAgICByb3dzID
0gbGlzdCgoYXdhaXQgc2Vzc2lvbi5leGVjdXRlKAogICAgICAgIHNlbGVjdChWMlBhcGVyQmFsYW5jZ
VNuYXBzaG90KQogICAgICAgIC5vcmRlcl9ieShWMlBhcGVyQmFsYW5jZVNuYXBzaG90LmNyZWF0ZWRf
YXQuZGVzYygpKQogICAgICAgIC5saW1pdChsaW1pdCkpKS5zY2FsYXJzKCkuYWxsKCkpCiAgICByZXR
1cm4geyJiYWxhbmNlcyI6IFsKICAgICAgICB7ImlkIjogci5pZCwgImFjY291bnRfaWQiOiByLmFjY2
91bnRfaWQsICJjYXNoIjogci5jYXNoLAogICAgICAgICAiZXF1aXR5Ijogci5lcXVpdHksICJtYXJna
W5fdXNlZCI6IHIubWFyZ2luX3VzZWQsCiAgICAgICAgICJtYXJnaW5fYXZhaWxhYmxlIjogci5tYXJn
aW5fYXZhaWxhYmxlLAogICAgICAgICAidW5yZWFsaXplZF9wbmwiOiByLnVucmVhbGl6ZWRfcG5sLAo
gICAgICAgICAicmVhbGl6ZWRfcG5sIjogci5yZWFsaXplZF9wbmx9IGZvciByIGluIHJvd3NdLAogIC
AgICAgICoqX2VudmVsb3BlKHJlcXVlc3QpfQoKCkByb3V0ZXIuZ2V0KCIvcmlzay1kZWNpc2lvbnMiK
Qphc3luYyBkZWYgYXBpX2xpc3Rfcmlza19kZWNpc2lvbnMoCiAgICByZXF1ZXN0OiBSZXF1ZXN0LCBv
cGVyYXRvcjogUmVxdWlyZVJpc2tSZWFkLAogICAgc2Vzc2lvbjogQW5ub3RhdGVkW0FzeW5jU2Vzc2l
vbiwgRGVwZW5kcyhnZXRfZGJfc2Vzc2lvbildLAogICAgbGltaXQ6IGludCA9IFF1ZXJ5KGRlZmF1bH
Q9MTAwLCBnZT0xLCBsZT01MDApLAopOgogICAgcm93cyA9IGxpc3QoKGF3YWl0IHNlc3Npb24uZXhlY
3V0ZSgKICAgICAgICBzZWxlY3QoVjJQYXBlclJpc2tEZWNpc2lvbikKICAgICAgICAub3JkZXJfYnko
VjJQYXBlclJpc2tEZWNpc2lvbi5jcmVhdGVkX2F0LmRlc2MoKSkKICAgICAgICAubGltaXQobGltaXQ
pKSkuc2NhbGFycygpLmFsbCgpKQogICAgcmV0dXJuIHsicmlza19kZWNpc2lvbnMiOiBbCiAgICAgIC
AgeyJpZCI6IHIuaWQsICJpbnRlbnRfaWQiOiByLmludGVudF9pZCwgImRlY2lzaW9uIjogci5kZWNpc
2lvbiwKICAgICAgICAgImV2YWx1YXRlZF9saW1pdHMiOiByLmV2YWx1YXRlZF9saW1pdHMsCiAgICAg
ICAgICJyaXNrX2NvbmZpZ192ZXJzaW9uIjogci5yaXNrX2NvbmZpZ192ZXJzaW9ufSBmb3IgciBpbiB
yb3dzXSwKICAgICAgICAqKl9lbnZlbG9wZShyZXF1ZXN0KX0KCgpAcm91dGVyLmdldCgiL3JlY29uY2
lsaWF0aW9ucyIpCmFzeW5jIGRlZiBhcGlfbGlzdF9yZWNvbmNpbGlhdGlvbnMoCiAgICByZXF1ZXN0O
iBSZXF1ZXN0LCBvcGVyYXRvcjogUmVxdWlyZUFjY291bnRzUmVhZCwKICAgIHNlc3Npb246IEFubm90
YXRlZFtBc3luY1Nlc3Npb24sIERlcGVuZHMoZ2V0X2RiX3Nlc3Npb24pXSwKICAgIGxpbWl0OiBpbnQ
gPSBRdWVyeShkZWZhdWx0PTEwMCwgZ2U9MSwgbGU9NTAwKSwKKToKICAgIHJvd3MgPSBsaXN0KChhd2
FpdCBzZXNzaW9uLmV4ZWN1dGUoCiAgICAgICAgc2VsZWN0KFYyUGFwZXJSZWNvbmNpbGlhdGlvbikKI
CAgICAgICAub3JkZXJfYnkoVjJQYXBlclJlY29uY2lsaWF0aW9uLmNyZWF0ZWRfYXQuZGVzYygpKQog
ICAgICAgIC5saW1pdChsaW1pdCkpKS5zY2FsYXJzKCkuYWxsKCkpCiAgICByZXR1cm4geyJyZWNvbmN
pbGlhdGlvbnMiOiBbCiAgICAgICAgeyJpZCI6IHIuaWQsICJhY2NvdW50X2lkIjogci5hY2NvdW50X2
lkLCAib3V0Y29tZSI6IHIub3V0Y29tZSwKICAgICAgICAgImRpc2NyZXBhbmNpZXMiOiByLmRpc2NyZ
XBhbmNpZXN9IGZvciByIGluIHJvd3NdLAogICAgICAgICoqX2VudmVsb3BlKHJlcXVlc3QpfQo=
'@
$LandPath = Join-Path $BackendRoot "app\v2\paper_trading\api.py"
New-Item -ItemType Directory -Force -Path (Split-Path $LandPath) | Out-Null
if (Test-Path $LandPath) {
    $Cur = (Get-FileHash -Path $LandPath -Algorithm SHA256).Hash.ToLower()
    if ($Cur -eq "1e4064e367cfd7340038388503dd90710c70a32cf386b568d0504097cc96b3be") { Write-Evidence ("pre-landing witnessed (already pinned bytes): app\v2\paper_trading\api.py") }
    else { throw ("STOP (A4 FOREIGN-STATE ADJUDICATION LAW): new-file target exists with foreign bytes: " + $LandPath + " sha " + $Cur + " . Nothing modified for this file; report to ITRGA.") }
} else {
    [IO.File]::WriteAllBytes($LandPath, (B64-Decode -B64Chunk $Fapp_v2_paper_trading_api_py))
    $Cur = (Get-FileHash -Path $LandPath -Algorithm SHA256).Hash.ToLower()
    if ($Cur -ne "1e4064e367cfd7340038388503dd90710c70a32cf386b568d0504097cc96b3be") { throw ("FAIL: post-write hash drift on " + $LandPath) }
    Write-Evidence ("landed + verified: app\v2\paper_trading\api.py")
}

# file: app\db\models\v2_paper_trading.py  (pin 61ccb9996610...)
$Fapp_db_models_v2_paper_trading_py = @'
IiIiVjIgQkUtOCB0YWJsZXMgKEJPLVYyLUJFLTgtMDAxIEQtMjsgZGVzaWduIFMxLjEg4oCUIGVpZ2h
0IHRhYmxlcykuCgpaZXJvLVVQREFURSByZWdpbWUgKGRlc2lnbiBTMS4yKTogZXZlcnkgdGFibGUgZ3
VhcmRlZCBVUERBVEUrREVMRVRFOyBvcmRlcgpzdGF0ZSBsaXZlcyBpbiB0aGUgYXBwZW5kLW9ubHkgZ
XZlbnQgbGVkZ2VyOyBjdXJyZW50IHN0YXRlIGlzIGRlcml2ZWQKKG1heCBldmVudF9pbmRleCkuIE40
OiBmaWxsX2NsYXNzIENIRUNLIGFkbWl0cyBleGFjdGx5ICdwYXBlcl9zaW11bGF0ZWQnLgoiIiIKCmZ
yb20gX19mdXR1cmVfXyBpbXBvcnQgYW5ub3RhdGlvbnMKCmZyb20gZGF0ZXRpbWUgaW1wb3J0IGRhdG
V0aW1lCmZyb20gdXVpZCBpbXBvcnQgdXVpZDQKCmZyb20gc3FsYWxjaGVteSBpbXBvcnQgKAogICAgS
lNPTiwKICAgIENoZWNrQ29uc3RyYWludCwKICAgIERhdGVUaW1lLAogICAgSW5kZXgsCiAgICBJbnRl
Z2VyLAogICAgU3RyaW5nLAogICAgVW5pcXVlQ29uc3RyYWludCwKKQpmcm9tIHNxbGFsY2hlbXkub3J
tIGltcG9ydCBNYXBwZWQsIG1hcHBlZF9jb2x1bW4KCmZyb20gYXBwLmRiLmJhc2UgaW1wb3J0IEJhc2
UKZnJvbSBhcHAudjIudGVtcG9yYWwudmFsaWRhdGlvbiBpbXBvcnQgdXRjX25vdwoKX0RBVEFfQ0xBU
1NfQ0hFQ0sgPSAoCiAgICAiZGF0YV9jbGFzcyBJTiAoJ3N5bnRoZXRpYycsJ3NpbXVsYXRlZCcsJ2hp
c3RvcmljYWxfcmVhbCcsJ2xpdmUnLCIKICAgICInc3RhbGVfY2FjaGVkJywndW5hdmFpbGFibGUnKSI
KKQoKCmNsYXNzIFYyUGFwZXJBY2NvdW50KEJhc2UpOgogICAgIiIiVmVyc2lvbmVkLWltbXV0YWJsZS
BwYXBlciBhY2NvdW50IChTMS4xIHJvdyAxKS4iIiIKCiAgICBfX3RhYmxlbmFtZV9fID0gInYyX3Bhc
GVyX2FjY291bnQiCiAgICBfX3RhYmxlX2FyZ3NfXyA9ICgKICAgICAgICBVbmlxdWVDb25zdHJhaW50
KCJhY2NvdW50X2lkIiwgInJlY29yZF9zZXEiLCBuYW1lPSJ1cV92Ml9wYWNjdF9pZF9zZXEiKSwKICA
gICAgICBJbmRleCgiaXhfdjJfcGFjY3RfYWNjb3VudCIsICJhY2NvdW50X2lkIiksCiAgICAgICAgQ2
hlY2tDb25zdHJhaW50KCJiYXNlX2N1cnJlbmN5IElOICgnVVNEJykiLCBuYW1lPSJja192Ml9wYWNjd
F9jY3kiKSwKICAgICAgICBDaGVja0NvbnN0cmFpbnQoCiAgICAgICAgICAgICJsaWZlY3ljbGVfc3Rh
dGUgSU4gKCdhY3RpdmUnLCdmcm96ZW4nLCdjbG9zZWQnKSIsCiAgICAgICAgICAgIG5hbWU9ImNrX3Y
yX3BhY2N0X3N0YXRlIiksCiAgICAgICAgQ2hlY2tDb25zdHJhaW50KF9EQVRBX0NMQVNTX0NIRUNLLC
BuYW1lPSJja192Ml9wYWNjdF9kYXRhX2NsYXNzIiksCiAgICApCgogICAgaWQ6IE1hcHBlZFtzdHJdI
D0gbWFwcGVkX2NvbHVtbihTdHJpbmcoMzYpLCBwcmltYXJ5X2tleT1UcnVlLCBkZWZhdWx0PWxhbWJk
YTogc3RyKHV1aWQ0KCkpKQogICAgYWNjb3VudF9pZDogTWFwcGVkW3N0cl0gPSBtYXBwZWRfY29sdW1
uKFN0cmluZyg2NCksIG51bGxhYmxlPUZhbHNlKQogICAgcmVjb3JkX3NlcTogTWFwcGVkW2ludF0gPS
BtYXBwZWRfY29sdW1uKEludGVnZXIsIG51bGxhYmxlPUZhbHNlKQogICAgc3VwZXJzZWRlczogTWFwc
GVkW3N0ciB8IE5vbmVdID0gbWFwcGVkX2NvbHVtbihTdHJpbmcoMzYpLCBudWxsYWJsZT1UcnVlKQog
ICAgbmFtZTogTWFwcGVkW3N0cl0gPSBtYXBwZWRfY29sdW1uKFN0cmluZygxMjgpLCBudWxsYWJsZT1
GYWxzZSkKICAgIGJhc2VfY3VycmVuY3k6IE1hcHBlZFtzdHJdID0gbWFwcGVkX2NvbHVtbihTdHJpbm
coOCksIG51bGxhYmxlPUZhbHNlKQogICAgaW5pdGlhbF9iYWxhbmNlOiBNYXBwZWRbc3RyXSA9IG1hc
HBlZF9jb2x1bW4oU3RyaW5nKDY0KSwgbnVsbGFibGU9RmFsc2UpCiAgICBtYXJnaW5fcGFyYW1zOiBN
YXBwZWRbZGljdF0gPSBtYXBwZWRfY29sdW1uKEpTT04sIG51bGxhYmxlPUZhbHNlKQogICAgbGlmZWN
5Y2xlX3N0YXRlOiBNYXBwZWRbc3RyXSA9IG1hcHBlZF9jb2x1bW4oU3RyaW5nKDE2KSwgbnVsbGFibG
U9RmFsc2UpCiAgICBjb25maXJtYXRpb25fcmVmOiBNYXBwZWRbc3RyXSA9IG1hcHBlZF9jb2x1bW4oU
3RyaW5nKDY0KSwgbnVsbGFibGU9RmFsc2UpCiAgICBkYXRhX2NsYXNzOiBNYXBwZWRbc3RyXSA9IG1h
cHBlZF9jb2x1bW4oU3RyaW5nKDMyKSwgbnVsbGFibGU9RmFsc2UpCiAgICBtb2RlOiBNYXBwZWRbc3R
yXSA9IG1hcHBlZF9jb2x1bW4oU3RyaW5nKDE2KSwgbnVsbGFibGU9RmFsc2UpCiAgICBvcGVyYXRvcl
9pZDogTWFwcGVkW3N0cl0gPSBtYXBwZWRfY29sdW1uKFN0cmluZygxMjgpLCBudWxsYWJsZT1GYWxzZ
SkKICAgIGNvcnJlbGF0aW9uX2lkOiBNYXBwZWRbc3RyIHwgTm9uZV0gPSBtYXBwZWRfY29sdW1uKFN0
cmluZyg2NCksIG51bGxhYmxlPVRydWUpCiAgICBjcmVhdGVkX2F0OiBNYXBwZWRbZGF0ZXRpbWVdID0
gbWFwcGVkX2NvbHVtbigKICAgICAgICBEYXRlVGltZSh0aW1lem9uZT1UcnVlKSwgZGVmYXVsdD11dG
Nfbm93LCBudWxsYWJsZT1GYWxzZSkKCgpjbGFzcyBWMlBhcGVyT3JkZXJJbnRlbnQoQmFzZSk6CiAgI
CAiIiJXcml0ZS1vbmNlIG9yZGVyIGludGVudCAoUzEuMSByb3cgMjsgTjMgYW5jaG9yKS4iIiIKCiAg
ICBfX3RhYmxlbmFtZV9fID0gInYyX3BhcGVyX29yZGVyX2ludGVudCIKICAgIF9fdGFibGVfYXJnc19
fID0gKAogICAgICAgIFVuaXF1ZUNvbnN0cmFpbnQoImFjY291bnRfaWQiLCAiaWRlbXBvdGVuY3lfa2
V5IiwKICAgICAgICAgICAgICAgICAgICAgICAgIG5hbWU9InVxX3YyX3BpbnRlbnRfaWRlbSIpLAogI
CAgICAgIEluZGV4KCJpeF92Ml9waW50ZW50X2FjY291bnQiLCAiYWNjb3VudF9pZCIpLAogICAgICAg
IENoZWNrQ29uc3RyYWludCgic2lkZSBJTiAoJ2J1eScsJ3NlbGwnKSIsIG5hbWU9ImNrX3YyX3BpbnR
lbnRfc2lkZSIpLAogICAgICAgIENoZWNrQ29uc3RyYWludCgib3JkZXJfdHlwZSBJTiAoJ21hcmtldC
csJ2xpbWl0JykiLAogICAgICAgICAgICAgICAgICAgICAgICBuYW1lPSJja192Ml9waW50ZW50X3R5c
GUiKSwKICAgICAgICBDaGVja0NvbnN0cmFpbnQoInRpbWVfaW5fZm9yY2UgSU4gKCdyZXBsYXlfd2lu
ZG93JykiLAogICAgICAgICAgICAgICAgICAgICAgICBuYW1lPSJja192Ml9waW50ZW50X3RpZiIpLAo
gICAgICAgIENoZWNrQ29uc3RyYWludCgKICAgICAgICAgICAgIihvcmRlcl90eXBlID0gJ2xpbWl0Jy
kgPSAobGltaXRfcHJpY2UgSVMgTk9UIE5VTEwpIiwKICAgICAgICAgICAgbmFtZT0iY2tfdjJfcGlud
GVudF9saW1pdF9pZmYiKSwKICAgICAgICBDaGVja0NvbnN0cmFpbnQoIkNBU1QocXVhbnRpdHkgQVMg
UkVBTCkgPiAwIiwKICAgICAgICAgICAgICAgICAgICAgICAgbmFtZT0iY2tfdjJfcGludGVudF9xdHk
iKSwKICAgICAgICBDaGVja0NvbnN0cmFpbnQoX0RBVEFfQ0xBU1NfQ0hFQ0ssIG5hbWU9ImNrX3YyX3
BpbnRlbnRfZGF0YV9jbGFzcyIpLAogICAgKQoKICAgIGlkOiBNYXBwZWRbc3RyXSA9IG1hcHBlZF9jb
2x1bW4oU3RyaW5nKDM2KSwgcHJpbWFyeV9rZXk9VHJ1ZSwgZGVmYXVsdD1sYW1iZGE6IHN0cih1dWlk
NCgpKSkKICAgIGludGVudF9pZDogTWFwcGVkW3N0cl0gPSBtYXBwZWRfY29sdW1uKFN0cmluZyg2NCk
sIG51bGxhYmxlPUZhbHNlLCB1bmlxdWU9VHJ1ZSkKICAgIGFjY291bnRfaWQ6IE1hcHBlZFtzdHJdID
0gbWFwcGVkX2NvbHVtbihTdHJpbmcoMzYpLCBudWxsYWJsZT1GYWxzZSkKICAgIGluc3RydW1lbnRfa
WQ6IE1hcHBlZFtzdHJdID0gbWFwcGVkX2NvbHVtbihTdHJpbmcoNjQpLCBudWxsYWJsZT1GYWxzZSkK
ICAgIHNpZGU6IE1hcHBlZFtzdHJdID0gbWFwcGVkX2NvbHVtbihTdHJpbmcoOCksIG51bGxhYmxlPUZ
hbHNlKQogICAgb3JkZXJfdHlwZTogTWFwcGVkW3N0cl0gPSBtYXBwZWRfY29sdW1uKFN0cmluZygxNi
ksIG51bGxhYmxlPUZhbHNlKQogICAgcXVhbnRpdHk6IE1hcHBlZFtzdHJdID0gbWFwcGVkX2NvbHVtb
ihTdHJpbmcoNjQpLCBudWxsYWJsZT1GYWxzZSkKICAgIGxpbWl0X3ByaWNlOiBNYXBwZWRbc3RyIHwg
Tm9uZV0gPSBtYXBwZWRfY29sdW1uKFN0cmluZyg2NCksIG51bGxhYmxlPVRydWUpCiAgICB0aW1lX2l
uX2ZvcmNlOiBNYXBwZWRbc3RyXSA9IG1hcHBlZF9jb2x1bW4oU3RyaW5nKDE2KSwgbnVsbGFibGU9Rm
Fsc2UpCiAgICBpZGVtcG90ZW5jeV9rZXk6IE1hcHBlZFtzdHJdID0gbWFwcGVkX2NvbHVtbihTdHJpb
mcoNjQpLCBudWxsYWJsZT1GYWxzZSkKICAgIHNuYXBzaG90X3JlZjogTWFwcGVkW3N0cl0gPSBtYXBw
ZWRfY29sdW1uKFN0cmluZyg2NCksIG51bGxhYmxlPUZhbHNlKQogICAgdGltZV9iYXNpczogTWFwcGV
kW2RpY3RdID0gbWFwcGVkX2NvbHVtbihKU09OLCBudWxsYWJsZT1GYWxzZSkKICAgIGNvbmZpcm1hdG
lvbl9yZWY6IE1hcHBlZFtzdHIgfCBOb25lXSA9IG1hcHBlZF9jb2x1bW4oU3RyaW5nKDY0KSwgbnVsb
GFibGU9VHJ1ZSkKICAgIGFjdG9yX2lkOiBNYXBwZWRbc3RyXSA9IG1hcHBlZF9jb2x1bW4oU3RyaW5n
KDEyOCksIG51bGxhYmxlPUZhbHNlKQogICAgZGF0YV9jbGFzczogTWFwcGVkW3N0cl0gPSBtYXBwZWR
fY29sdW1uKFN0cmluZygzMiksIG51bGxhYmxlPUZhbHNlKQogICAgbW9kZTogTWFwcGVkW3N0cl0gPS
BtYXBwZWRfY29sdW1uKFN0cmluZygxNiksIG51bGxhYmxlPUZhbHNlKQogICAgb3BlcmF0b3JfaWQ6I
E1hcHBlZFtzdHJdID0gbWFwcGVkX2NvbHVtbihTdHJpbmcoMTI4KSwgbnVsbGFibGU9RmFsc2UpCiAg
ICBjb3JyZWxhdGlvbl9pZDogTWFwcGVkW3N0ciB8IE5vbmVdID0gbWFwcGVkX2NvbHVtbihTdHJpbmc
oNjQpLCBudWxsYWJsZT1UcnVlKQogICAgY3JlYXRlZF9hdDogTWFwcGVkW2RhdGV0aW1lXSA9IG1hcH
BlZF9jb2x1bW4oCiAgICAgICAgRGF0ZVRpbWUodGltZXpvbmU9VHJ1ZSksIGRlZmF1bHQ9dXRjX25vd
ywgbnVsbGFibGU9RmFsc2UpCgoKY2xhc3MgVjJQYXBlclJpc2tEZWNpc2lvbihCYXNlKToKICAgICIi
IkltbXV0YWJsZSByaXNrIGRlY2lzaW9uIOKAlCBleGFjdGx5IG9uZSBwZXIgaW50ZW50IChTMS4xIHJ
vdyAzOyBTOCkuIiIiCgogICAgX190YWJsZW5hbWVfXyA9ICJ2Ml9wYXBlcl9yaXNrX2RlY2lzaW9uIg
ogICAgX190YWJsZV9hcmdzX18gPSAoCiAgICAgICAgVW5pcXVlQ29uc3RyYWludCgiaW50ZW50X2lkI
iwgbmFtZT0idXFfdjJfcHJpc2tfaW50ZW50IiksCiAgICAgICAgQ2hlY2tDb25zdHJhaW50KCJkZWNp
c2lvbiBJTiAoJ3Bhc3MnLCdibG9jaycsJ2hvbGQnKSIsCiAgICAgICAgICAgICAgICAgICAgICAgIG5
hbWU9ImNrX3YyX3ByaXNrX2RlY2lzaW9uIiksCiAgICAgICAgIyBDLTFiOiByZWYgTk9UIE5VTEwgaW
ZmIGhvbGQg4oCUIGJvdGggZGlyZWN0aW9ucy4KICAgICAgICBDaGVja0NvbnN0cmFpbnQoCiAgICAgI
CAgICAgICIoZGVjaXNpb24gPSAnaG9sZCcpID0gKGNvbmZpcm1hdGlvbl9yZWYgSVMgTk9UIE5VTEwp
IiwKICAgICAgICAgICAgbmFtZT0iY2tfdjJfcHJpc2tfcmVmX2lmZiIpLAogICAgICAgIENoZWNrQ29
uc3RyYWludChfREFUQV9DTEFTU19DSEVDSywgbmFtZT0iY2tfdjJfcHJpc2tfZGF0YV9jbGFzcyIpLA
ogICAgKQoKICAgIGlkOiBNYXBwZWRbc3RyXSA9IG1hcHBlZF9jb2x1bW4oU3RyaW5nKDM2KSwgcHJpb
WFyeV9rZXk9VHJ1ZSwgZGVmYXVsdD1sYW1iZGE6IHN0cih1dWlkNCgpKSkKICAgIGludGVudF9pZDog
TWFwcGVkW3N0cl0gPSBtYXBwZWRfY29sdW1uKFN0cmluZygzNiksIG51bGxhYmxlPUZhbHNlKQogICA
gZGVjaXNpb246IE1hcHBlZFtzdHJdID0gbWFwcGVkX2NvbHVtbihTdHJpbmcoOCksIG51bGxhYmxlPU
ZhbHNlKQogICAgZXZhbHVhdGVkX2xpbWl0czogTWFwcGVkW2RpY3RdID0gbWFwcGVkX2NvbHVtbihKU
09OLCBudWxsYWJsZT1GYWxzZSkKICAgIHJlYXNvbnM6IE1hcHBlZFtkaWN0XSA9IG1hcHBlZF9jb2x1
bW4oSlNPTiwgbnVsbGFibGU9RmFsc2UpCiAgICByaXNrX2NvbmZpZ192ZXJzaW9uOiBNYXBwZWRbc3R
yXSA9IG1hcHBlZF9jb2x1bW4oU3RyaW5nKDMyKSwgbnVsbGFibGU9RmFsc2UpCiAgICBkZWNpZGVkX2
F0X2Jhc2lzOiBNYXBwZWRbZGljdF0gPSBtYXBwZWRfY29sdW1uKEpTT04sIG51bGxhYmxlPUZhbHNlK
QogICAgY29uZmlybWF0aW9uX3JlZjogTWFwcGVkW3N0ciB8IE5vbmVdID0gbWFwcGVkX2NvbHVtbihT
dHJpbmcoNjQpLCBudWxsYWJsZT1UcnVlKQogICAgZGF0YV9jbGFzczogTWFwcGVkW3N0cl0gPSBtYXB
wZWRfY29sdW1uKFN0cmluZygzMiksIG51bGxhYmxlPUZhbHNlKQogICAgbW9kZTogTWFwcGVkW3N0cl
0gPSBtYXBwZWRfY29sdW1uKFN0cmluZygxNiksIG51bGxhYmxlPUZhbHNlKQogICAgb3BlcmF0b3Jfa
WQ6IE1hcHBlZFtzdHJdID0gbWFwcGVkX2NvbHVtbihTdHJpbmcoMTI4KSwgbnVsbGFibGU9RmFsc2Up
CiAgICBjb3JyZWxhdGlvbl9pZDogTWFwcGVkW3N0ciB8IE5vbmVdID0gbWFwcGVkX2NvbHVtbihTdHJ
pbmcoNjQpLCBudWxsYWJsZT1UcnVlKQogICAgY3JlYXRlZF9hdDogTWFwcGVkW2RhdGV0aW1lXSA9IG
1hcHBlZF9jb2x1bW4oCiAgICAgICAgRGF0ZVRpbWUodGltZXpvbmU9VHJ1ZSksIGRlZmF1bHQ9dXRjX
25vdywgbnVsbGFibGU9RmFsc2UpCgoKY2xhc3MgVjJQYXBlck9yZGVyRXZlbnQoQmFzZSk6CiAgICAi
IiJBcHBlbmQtb25seSBvcmRlciBldmVudCBsZWRnZXIgKFMxLjEgcm93IDQ7IFMyLjMgZGVyaXZhdGl
vbiBsYXcpLiIiIgoKICAgIF9fdGFibGVuYW1lX18gPSAidjJfcGFwZXJfb3JkZXJfZXZlbnQiCiAgIC
BfX3RhYmxlX2FyZ3NfXyA9ICgKICAgICAgICBVbmlxdWVDb25zdHJhaW50KCJpbnRlbnRfaWQiLCAiZ
XZlbnRfaW5kZXgiLCBuYW1lPSJ1cV92Ml9wZXZlbnRfaWR4IiksCiAgICAgICAgSW5kZXgoIml4X3Yy
X3BldmVudF9pbnRlbnQiLCAiaW50ZW50X2lkIiksCiAgICAgICAgQ2hlY2tDb25zdHJhaW50KF9EQVR
BX0NMQVNTX0NIRUNLLCBuYW1lPSJja192Ml9wZXZlbnRfZGF0YV9jbGFzcyIpLAogICAgKQoKICAgIG
lkOiBNYXBwZWRbc3RyXSA9IG1hcHBlZF9jb2x1bW4oU3RyaW5nKDM2KSwgcHJpbWFyeV9rZXk9VHJ1Z
SwgZGVmYXVsdD1sYW1iZGE6IHN0cih1dWlkNCgpKSkKICAgIGludGVudF9pZDogTWFwcGVkW3N0cl0g
PSBtYXBwZWRfY29sdW1uKFN0cmluZygzNiksIG51bGxhYmxlPUZhbHNlKQogICAgZXZlbnRfaW5kZXg
6IE1hcHBlZFtpbnRdID0gbWFwcGVkX2NvbHVtbihJbnRlZ2VyLCBudWxsYWJsZT1GYWxzZSkKICAgIG
Zyb21fc3RhdGU6IE1hcHBlZFtzdHJdID0gbWFwcGVkX2NvbHVtbihTdHJpbmcoMjQpLCBudWxsYWJsZ
T1GYWxzZSkKICAgIHRvX3N0YXRlOiBNYXBwZWRbc3RyXSA9IG1hcHBlZF9jb2x1bW4oU3RyaW5nKDI0
KSwgbnVsbGFibGU9RmFsc2UpCiAgICBldmVudF9jbGFzczogTWFwcGVkW3N0cl0gPSBtYXBwZWRfY29
sdW1uKFN0cmluZyg0OCksIG51bGxhYmxlPUZhbHNlKQogICAgZGV0YWlsczogTWFwcGVkW2RpY3RdID
0gbWFwcGVkX2NvbHVtbihKU09OLCBudWxsYWJsZT1GYWxzZSkKICAgIGFjdG9yX2lkOiBNYXBwZWRbc
3RyXSA9IG1hcHBlZF9jb2x1bW4oU3RyaW5nKDEyOCksIG51bGxhYmxlPUZhbHNlKQogICAgZGF0YV9j
bGFzczogTWFwcGVkW3N0cl0gPSBtYXBwZWRfY29sdW1uKFN0cmluZygzMiksIG51bGxhYmxlPUZhbHN
lKQogICAgbW9kZTogTWFwcGVkW3N0cl0gPSBtYXBwZWRfY29sdW1uKFN0cmluZygxNiksIG51bGxhYm
xlPUZhbHNlKQogICAgb3BlcmF0b3JfaWQ6IE1hcHBlZFtzdHJdID0gbWFwcGVkX2NvbHVtbihTdHJpb
mcoMTI4KSwgbnVsbGFibGU9RmFsc2UpCiAgICBjb3JyZWxhdGlvbl9pZDogTWFwcGVkW3N0ciB8IE5v
bmVdID0gbWFwcGVkX2NvbHVtbihTdHJpbmcoNjQpLCBudWxsYWJsZT1UcnVlKQogICAgY3JlYXRlZF9
hdDogTWFwcGVkW2RhdGV0aW1lXSA9IG1hcHBlZF9jb2x1bW4oCiAgICAgICAgRGF0ZVRpbWUodGltZX
pvbmU9VHJ1ZSksIGRlZmF1bHQ9dXRjX25vdywgbnVsbGFibGU9RmFsc2UpCgoKY2xhc3MgVjJQYXBlc
kZpbGwoQmFzZSk6CiAgICAiIiJJbW11dGFibGUgZmlsbCDigJQgTjQ6IGZpbGxfY2xhc3Mgc2luZ2xl
LXZhbHVlIENIRUNLIChTMS4xIHJvdyA1KS4iIiIKCiAgICBfX3RhYmxlbmFtZV9fID0gInYyX3BhcGV
yX2ZpbGwiCiAgICBfX3RhYmxlX2FyZ3NfXyA9ICgKICAgICAgICBVbmlxdWVDb25zdHJhaW50KCJpbn
RlbnRfaWQiLCAiZmlsbF9pbmRleCIsIG5hbWU9InVxX3YyX3BmaWxsX2lkeCIpLAogICAgICAgIEluZ
GV4KCJpeF92Ml9wZmlsbF9pbnRlbnQiLCAiaW50ZW50X2lkIiksCiAgICAgICAgQ2hlY2tDb25zdHJh
aW50KCJmaWxsX2NsYXNzIElOICgncGFwZXJfc2ltdWxhdGVkJykiLAogICAgICAgICAgICAgICAgICA
gICAgICBuYW1lPSJja192Ml9wZmlsbF9jbGFzcyIpLAogICAgICAgIENoZWNrQ29uc3RyYWludChfRE
FUQV9DTEFTU19DSEVDSywgbmFtZT0iY2tfdjJfcGZpbGxfZGF0YV9jbGFzcyIpLAogICAgKQoKICAgI
GlkOiBNYXBwZWRbc3RyXSA9IG1hcHBlZF9jb2x1bW4oU3RyaW5nKDM2KSwgcHJpbWFyeV9rZXk9VHJ1
ZSwgZGVmYXVsdD1sYW1iZGE6IHN0cih1dWlkNCgpKSkKICAgIGZpbGxfaWQ6IE1hcHBlZFtzdHJdID0
gbWFwcGVkX2NvbHVtbihTdHJpbmcoNjQpLCBudWxsYWJsZT1GYWxzZSwgdW5pcXVlPVRydWUpCiAgIC
BpbnRlbnRfaWQ6IE1hcHBlZFtzdHJdID0gbWFwcGVkX2NvbHVtbihTdHJpbmcoMzYpLCBudWxsYWJsZ
T1GYWxzZSkKICAgIGZpbGxfaW5kZXg6IE1hcHBlZFtpbnRdID0gbWFwcGVkX2NvbHVtbihJbnRlZ2Vy
LCBudWxsYWJsZT1GYWxzZSkKICAgIHF1YW50aXR5OiBNYXBwZWRbc3RyXSA9IG1hcHBlZF9jb2x1bW4
oU3RyaW5nKDY0KSwgbnVsbGFibGU9RmFsc2UpCiAgICByYXdfcHJpY2U6IE1hcHBlZFtzdHJdID0gbW
FwcGVkX2NvbHVtbihTdHJpbmcoNjQpLCBudWxsYWJsZT1GYWxzZSkKICAgIGVmZmVjdGl2ZV9wcmljZ
TogTWFwcGVkW3N0cl0gPSBtYXBwZWRfY29sdW1uKFN0cmluZyg2NCksIG51bGxhYmxlPUZhbHNlKQog
ICAgY29zdF9tb2RlbF9yZWY6IE1hcHBlZFtkaWN0XSA9IG1hcHBlZF9jb2x1bW4oSlNPTiwgbnVsbGF
ibGU9RmFsc2UpCiAgICBmaWxsX2NsYXNzOiBNYXBwZWRbc3RyXSA9IG1hcHBlZF9jb2x1bW4oU3RyaW
5nKDI0KSwgbnVsbGFibGU9RmFsc2UpCiAgICBzaW11bGF0b3JfdmVyc2lvbjogTWFwcGVkW3N0cl0gP
SBtYXBwZWRfY29sdW1uKFN0cmluZygzMiksIG51bGxhYmxlPUZhbHNlKQogICAgc25hcHNob3RfcmVm
OiBNYXBwZWRbc3RyXSA9IG1hcHBlZF9jb2x1bW4oU3RyaW5nKDY0KSwgbnVsbGFibGU9RmFsc2UpCiA
gICB0aW1lX2Jhc2lzOiBNYXBwZWRbZGljdF0gPSBtYXBwZWRfY29sdW1uKEpTT04sIG51bGxhYmxlPU
ZhbHNlKQogICAgZGF0YV9jbGFzczogTWFwcGVkW3N0cl0gPSBtYXBwZWRfY29sdW1uKFN0cmluZygzM
iksIG51bGxhYmxlPUZhbHNlKQogICAgbW9kZTogTWFwcGVkW3N0cl0gPSBtYXBwZWRfY29sdW1uKFN0
cmluZygxNiksIG51bGxhYmxlPUZhbHNlKQogICAgb3BlcmF0b3JfaWQ6IE1hcHBlZFtzdHJdID0gbWF
wcGVkX2NvbHVtbihTdHJpbmcoMTI4KSwgbnVsbGFibGU9RmFsc2UpCiAgICBjb3JyZWxhdGlvbl9pZD
ogTWFwcGVkW3N0ciB8IE5vbmVdID0gbWFwcGVkX2NvbHVtbihTdHJpbmcoNjQpLCBudWxsYWJsZT1Uc
nVlKQogICAgY3JlYXRlZF9hdDogTWFwcGVkW2RhdGV0aW1lXSA9IG1hcHBlZF9jb2x1bW4oCiAgICAg
ICAgRGF0ZVRpbWUodGltZXpvbmU9VHJ1ZSksIGRlZmF1bHQ9dXRjX25vdywgbnVsbGFibGU9RmFsc2U
pCgoKY2xhc3MgVjJQYXBlclBvc2l0aW9uU25hcHNob3QoQmFzZSk6CiAgICAiIiJJbW11dGFibGUgZG
VyaXZlZCBwb3NpdGlvbnMgYXJ0aWZhY3QgKFMxLjEgcm93IDY7IGFuY2hvciBsYXcpLiIiIgoKICAgI
F9fdGFibGVuYW1lX18gPSAidjJfcGFwZXJfcG9zaXRpb25fc25hcHNob3QiCiAgICBfX3RhYmxlX2Fy
Z3NfXyA9ICgKICAgICAgICBVbmlxdWVDb25zdHJhaW50KCJhY2NvdW50X2lkIiwgImRlcml2YXRpb25
faW5wdXRzX2hhc2giLAogICAgICAgICAgICAgICAgICAgICAgICAgImVuZ2luZV92ZXJzaW9uc19oYX
NoIiwKICAgICAgICAgICAgICAgICAgICAgICAgIG5hbWU9InVxX3YyX3Bwb3NfYW5jaG9yIiksCiAgI
CAgICAgSW5kZXgoIml4X3YyX3Bwb3NfYWNjb3VudCIsICJhY2NvdW50X2lkIiksCiAgICAgICAgQ2hl
Y2tDb25zdHJhaW50KF9EQVRBX0NMQVNTX0NIRUNLLCBuYW1lPSJja192Ml9wcG9zX2RhdGFfY2xhc3M
iKSwKICAgICkKCiAgICBpZDogTWFwcGVkW3N0cl0gPSBtYXBwZWRfY29sdW1uKFN0cmluZygzNiksIH
ByaW1hcnlfa2V5PVRydWUsIGRlZmF1bHQ9bGFtYmRhOiBzdHIodXVpZDQoKSkpCiAgICBhY2NvdW50X
2lkOiBNYXBwZWRbc3RyXSA9IG1hcHBlZF9jb2x1bW4oU3RyaW5nKDM2KSwgbnVsbGFibGU9RmFsc2Up
CiAgICBhc19vZl9iYXNpczogTWFwcGVkW2RpY3RdID0gbWFwcGVkX2NvbHVtbihKU09OLCBudWxsYWJ
sZT1GYWxzZSkKICAgIHBvc2l0aW9uczogTWFwcGVkW2RpY3RdID0gbWFwcGVkX2NvbHVtbihKU09OLC
BudWxsYWJsZT1GYWxzZSkKICAgIGRlcml2YXRpb25faW5wdXRzX2hhc2g6IE1hcHBlZFtzdHJdID0gb
WFwcGVkX2NvbHVtbihTdHJpbmcoNjQpLCBudWxsYWJsZT1GYWxzZSkKICAgIGVuZ2luZV92ZXJzaW9u
c19oYXNoOiBNYXBwZWRbc3RyXSA9IG1hcHBlZF9jb2x1bW4oU3RyaW5nKDY0KSwgbnVsbGFibGU9RmF
sc2UpCiAgICBkYXRhX2NsYXNzOiBNYXBwZWRbc3RyXSA9IG1hcHBlZF9jb2x1bW4oU3RyaW5nKDMyKS
wgbnVsbGFibGU9RmFsc2UpCiAgICBtb2RlOiBNYXBwZWRbc3RyXSA9IG1hcHBlZF9jb2x1bW4oU3Rya
W5nKDE2KSwgbnVsbGFibGU9RmFsc2UpCiAgICBvcGVyYXRvcl9pZDogTWFwcGVkW3N0cl0gPSBtYXBw
ZWRfY29sdW1uKFN0cmluZygxMjgpLCBudWxsYWJsZT1GYWxzZSkKICAgIGNvcnJlbGF0aW9uX2lkOiB
NYXBwZWRbc3RyIHwgTm9uZV0gPSBtYXBwZWRfY29sdW1uKFN0cmluZyg2NCksIG51bGxhYmxlPVRydW
UpCiAgICBjcmVhdGVkX2F0OiBNYXBwZWRbZGF0ZXRpbWVdID0gbWFwcGVkX2NvbHVtbigKICAgICAgI
CBEYXRlVGltZSh0aW1lem9uZT1UcnVlKSwgZGVmYXVsdD11dGNfbm93LCBudWxsYWJsZT1GYWxzZSkK
CgpjbGFzcyBWMlBhcGVyQmFsYW5jZVNuYXBzaG90KEJhc2UpOgogICAgIiIiSW1tdXRhYmxlIGRlcml
2ZWQgYmFsYW5jZXMgYXJ0aWZhY3QgKFMxLjEgcm93IDc7IGFuY2hvciBsYXcpLiIiIgoKICAgIF9fdG
FibGVuYW1lX18gPSAidjJfcGFwZXJfYmFsYW5jZV9zbmFwc2hvdCIKICAgIF9fdGFibGVfYXJnc19fI
D0gKAogICAgICAgIFVuaXF1ZUNvbnN0cmFpbnQoImFjY291bnRfaWQiLCAiZGVyaXZhdGlvbl9pbnB1
dHNfaGFzaCIsCiAgICAgICAgICAgICAgICAgICAgICAgICAiZW5naW5lX3ZlcnNpb25zX2hhc2giLAo
gICAgICAgICAgICAgICAgICAgICAgICAgbmFtZT0idXFfdjJfcGJhbF9hbmNob3IiKSwKICAgICAgIC
BJbmRleCgiaXhfdjJfcGJhbF9hY2NvdW50IiwgImFjY291bnRfaWQiKSwKICAgICAgICBDaGVja0Nvb
nN0cmFpbnQoX0RBVEFfQ0xBU1NfQ0hFQ0ssIG5hbWU9ImNrX3YyX3BiYWxfZGF0YV9jbGFzcyIpLAog
ICAgKQoKICAgIGlkOiBNYXBwZWRbc3RyXSA9IG1hcHBlZF9jb2x1bW4oU3RyaW5nKDM2KSwgcHJpbWF
yeV9rZXk9VHJ1ZSwgZGVmYXVsdD1sYW1iZGE6IHN0cih1dWlkNCgpKSkKICAgIGFjY291bnRfaWQ6IE
1hcHBlZFtzdHJdID0gbWFwcGVkX2NvbHVtbihTdHJpbmcoMzYpLCBudWxsYWJsZT1GYWxzZSkKICAgI
GFzX29mX2Jhc2lzOiBNYXBwZWRbZGljdF0gPSBtYXBwZWRfY29sdW1uKEpTT04sIG51bGxhYmxlPUZh
bHNlKQogICAgY2FzaDogTWFwcGVkW3N0cl0gPSBtYXBwZWRfY29sdW1uKFN0cmluZyg2NCksIG51bGx
hYmxlPUZhbHNlKQogICAgZXF1aXR5OiBNYXBwZWRbc3RyXSA9IG1hcHBlZF9jb2x1bW4oU3RyaW5nKD
Y0KSwgbnVsbGFibGU9RmFsc2UpCiAgICBtYXJnaW5fdXNlZDogTWFwcGVkW3N0cl0gPSBtYXBwZWRfY
29sdW1uKFN0cmluZyg2NCksIG51bGxhYmxlPUZhbHNlKQogICAgbWFyZ2luX2F2YWlsYWJsZTogTWFw
cGVkW3N0cl0gPSBtYXBwZWRfY29sdW1uKFN0cmluZyg2NCksIG51bGxhYmxlPUZhbHNlKQogICAgdW5
yZWFsaXplZF9wbmw6IE1hcHBlZFtzdHJdID0gbWFwcGVkX2NvbHVtbihTdHJpbmcoNjQpLCBudWxsYW
JsZT1GYWxzZSkKICAgIHJlYWxpemVkX3BubDogTWFwcGVkW3N0cl0gPSBtYXBwZWRfY29sdW1uKFN0c
mluZyg2NCksIG51bGxhYmxlPUZhbHNlKQogICAgZGVyaXZhdGlvbl9pbnB1dHNfaGFzaDogTWFwcGVk
W3N0cl0gPSBtYXBwZWRfY29sdW1uKFN0cmluZyg2NCksIG51bGxhYmxlPUZhbHNlKQogICAgZW5naW5
lX3ZlcnNpb25zX2hhc2g6IE1hcHBlZFtzdHJdID0gbWFwcGVkX2NvbHVtbihTdHJpbmcoNjQpLCBudW
xsYWJsZT1GYWxzZSkKICAgIGRhdGFfY2xhc3M6IE1hcHBlZFtzdHJdID0gbWFwcGVkX2NvbHVtbihTd
HJpbmcoMzIpLCBudWxsYWJsZT1GYWxzZSkKICAgIG1vZGU6IE1hcHBlZFtzdHJdID0gbWFwcGVkX2Nv
bHVtbihTdHJpbmcoMTYpLCBudWxsYWJsZT1GYWxzZSkKICAgIG9wZXJhdG9yX2lkOiBNYXBwZWRbc3R
yXSA9IG1hcHBlZF9jb2x1bW4oU3RyaW5nKDEyOCksIG51bGxhYmxlPUZhbHNlKQogICAgY29ycmVsYX
Rpb25faWQ6IE1hcHBlZFtzdHIgfCBOb25lXSA9IG1hcHBlZF9jb2x1bW4oU3RyaW5nKDY0KSwgbnVsb
GFibGU9VHJ1ZSkKICAgIGNyZWF0ZWRfYXQ6IE1hcHBlZFtkYXRldGltZV0gPSBtYXBwZWRfY29sdW1u
KAogICAgICAgIERhdGVUaW1lKHRpbWV6b25lPVRydWUpLCBkZWZhdWx0PXV0Y19ub3csIG51bGxhYmx
lPUZhbHNlKQoKCmNsYXNzIFYyUGFwZXJSZWNvbmNpbGlhdGlvbihCYXNlKToKICAgICIiIkltbXV0YW
JsZSByZWNvbmNpbGlhdGlvbiByZWNvcmQgKFMxLjEgcm93IDg7IFM1IGdlbmVzaXMgcmVjb21wdXRlK
S4iIiIKCiAgICBfX3RhYmxlbmFtZV9fID0gInYyX3BhcGVyX3JlY29uY2lsaWF0aW9uIgogICAgX190
YWJsZV9hcmdzX18gPSAoCiAgICAgICAgSW5kZXgoIml4X3YyX3ByZWNvbl9hY2NvdW50IiwgImFjY29
1bnRfaWQiKSwKICAgICAgICBDaGVja0NvbnN0cmFpbnQoIm91dGNvbWUgSU4gKCdjb25zaXN0ZW50Jy
wnZGlzY3JlcGFudCcpIiwKICAgICAgICAgICAgICAgICAgICAgICAgbmFtZT0iY2tfdjJfcHJlY29uX
291dGNvbWUiKSwKICAgICAgICBDaGVja0NvbnN0cmFpbnQoX0RBVEFfQ0xBU1NfQ0hFQ0ssIG5hbWU9
ImNrX3YyX3ByZWNvbl9kYXRhX2NsYXNzIiksCiAgICApCgogICAgaWQ6IE1hcHBlZFtzdHJdID0gbWF
wcGVkX2NvbHVtbihTdHJpbmcoMzYpLCBwcmltYXJ5X2tleT1UcnVlLCBkZWZhdWx0PWxhbWJkYTogc3
RyKHV1aWQ0KCkpKQogICAgYWNjb3VudF9pZDogTWFwcGVkW3N0cl0gPSBtYXBwZWRfY29sdW1uKFN0c
mluZygzNiksIG51bGxhYmxlPUZhbHNlKQogICAgcnVuX2Jhc2lzOiBNYXBwZWRbZGljdF0gPSBtYXBw
ZWRfY29sdW1uKEpTT04sIG51bGxhYmxlPUZhbHNlKQogICAgb3V0Y29tZTogTWFwcGVkW3N0cl0gPSB
tYXBwZWRfY29sdW1uKFN0cmluZygxNiksIG51bGxhYmxlPUZhbHNlKQogICAgZGlzY3JlcGFuY2llcz
ogTWFwcGVkW2RpY3RdID0gbWFwcGVkX2NvbHVtbihKU09OLCBudWxsYWJsZT1GYWxzZSkKICAgIGluc
HV0c19oYXNoOiBNYXBwZWRbc3RyXSA9IG1hcHBlZF9jb2x1bW4oU3RyaW5nKDY0KSwgbnVsbGFibGU9
RmFsc2UpCiAgICBkYXRhX2NsYXNzOiBNYXBwZWRbc3RyXSA9IG1hcHBlZF9jb2x1bW4oU3RyaW5nKDM
yKSwgbnVsbGFibGU9RmFsc2UpCiAgICBtb2RlOiBNYXBwZWRbc3RyXSA9IG1hcHBlZF9jb2x1bW4oU3
RyaW5nKDE2KSwgbnVsbGFibGU9RmFsc2UpCiAgICBvcGVyYXRvcl9pZDogTWFwcGVkW3N0cl0gPSBtY
XBwZWRfY29sdW1uKFN0cmluZygxMjgpLCBudWxsYWJsZT1GYWxzZSkKICAgIGNvcnJlbGF0aW9uX2lk
OiBNYXBwZWRbc3RyIHwgTm9uZV0gPSBtYXBwZWRfY29sdW1uKFN0cmluZyg2NCksIG51bGxhYmxlPVR
ydWUpCiAgICBjcmVhdGVkX2F0OiBNYXBwZWRbZGF0ZXRpbWVdID0gbWFwcGVkX2NvbHVtbigKICAgIC
AgICBEYXRlVGltZSh0aW1lem9uZT1UcnVlKSwgZGVmYXVsdD11dGNfbm93LCBudWxsYWJsZT1GYWxzZ
SkK
'@
$LandPath = Join-Path $BackendRoot "app\db\models\v2_paper_trading.py"
New-Item -ItemType Directory -Force -Path (Split-Path $LandPath) | Out-Null
if (Test-Path $LandPath) {
    $Cur = (Get-FileHash -Path $LandPath -Algorithm SHA256).Hash.ToLower()
    if ($Cur -eq "61ccb99966106cdf85485dfdfc9fed276512501553af59c9a4e6ddb02d73b56c") { Write-Evidence ("pre-landing witnessed (already pinned bytes): app\db\models\v2_paper_trading.py") }
    else { throw ("STOP (A4 FOREIGN-STATE ADJUDICATION LAW): new-file target exists with foreign bytes: " + $LandPath + " sha " + $Cur + " . Nothing modified for this file; report to ITRGA.") }
} else {
    [IO.File]::WriteAllBytes($LandPath, (B64-Decode -B64Chunk $Fapp_db_models_v2_paper_trading_py))
    $Cur = (Get-FileHash -Path $LandPath -Algorithm SHA256).Hash.ToLower()
    if ($Cur -ne "61ccb99966106cdf85485dfdfc9fed276512501553af59c9a4e6ddb02d73b56c") { throw ("FAIL: post-write hash drift on " + $LandPath) }
    Write-Evidence ("landed + verified: app\db\models\v2_paper_trading.py")
}

# file: alembic\versions\20260904_0048_v2_be8_paper_trading.py  (pin 2cb83b3d1025...)
$Falembic_versions_20260904_0048_v2_be8_paper_trading_py = @'
IiIiVjIgQkUtOCDigJQgcGFwZXIgdHJhZGluZyAoQk8tVjItQkUtOC0wMDEgRC00OyBkZXNpZ24gUzE
vUzEwKS4KCkVpZ2h0IHRhYmxlcywgQUxMIGd1YXJkZWQgKHplcm8tVVBEQVRFIHJlZ2ltZSk6IDE2IH
RyaWdnZXJzICg0Mi0+NTgpOwo4IHBlcm1pc3Npb24gcm93cyAoNDktPjU3OyBELTEgc2NvcGVkLWV4Z
W1wdGlvbiB2b2NhYnVsYXJ5KTsgMiBjb21wdmVyCnNlZWRzICg4LT4xMDogcGFwZXJfZXhlY3V0aW9u
X3NpbXVsYXRvcj1weHMtMS4wLjAgb3ZlciB7c2ltdWxhdG9yLApsZWRnZXJ9LnB5LCBwYXBlcl9yaXN
rX2dhdGV3YXk9cHJnLTEuMC4wIG92ZXIge3Jpc2ssY29udHJhY3RzfS5weSDigJQKcm9sbGluZy1oYX
NoIHJlY2lwZSBpZGVudGljYWwgdG8gMDA0NzsgUlBFL1JKRSB1bnRvdWNoZWQsIGFwcGVuZC1vbmx5C
mxhdykuIFN5bW1ldHJpYyBjb250ZW50LWJhc2VkIGRvd25ncmFkZS4KClJldmlzaW9uIElEOiAyMDI2
MDkwNF8wMDQ4ClJldmlzZXM6IDIwMjYwOTAzXzAwNDcKIiIiCgpmcm9tIF9fZnV0dXJlX18gaW1wb3J
0IGFubm90YXRpb25zCgppbXBvcnQgaGFzaGxpYgpmcm9tIGRhdGV0aW1lIGltcG9ydCBkYXRldGltZS
wgdGltZXpvbmUKZnJvbSBwYXRobGliIGltcG9ydCBQYXRoCmZyb20gdXVpZCBpbXBvcnQgdXVpZDQKC
mltcG9ydCBzcWxhbGNoZW15IGFzIHNhCgpmcm9tIGFsZW1iaWMgaW1wb3J0IG9wCgpyZXZpc2lvbiA9
ICIyMDI2MDkwNF8wMDQ4Igpkb3duX3JldmlzaW9uID0gIjIwMjYwOTAzXzAwNDciCmJyYW5jaF9sYWJ
lbHMgPSBOb25lCmRlcGVuZHNfb24gPSBOb25lCgpfVFJJR0dFUlMgPSAoCiAgICAoInYyX3BhcGVyX2
FjY291bnRfaW1tdXRhYmxlX3VwZGF0ZSIsICJ2Ml9wYXBlcl9hY2NvdW50IiwKICAgICAiVVBEQVRFI
iwgIlYyIHBhcGVyIGFjY291bnRzIGFyZSBpbW11dGFibGU7IFVQREFURSBwcm9oaWJpdGVkIiksCiAg
ICAoInYyX3BhcGVyX2FjY291bnRfaW1tdXRhYmxlX2RlbGV0ZSIsICJ2Ml9wYXBlcl9hY2NvdW50Iiw
KICAgICAiREVMRVRFIiwgIlYyIHBhcGVyIGFjY291bnRzIGFyZSBpbW11dGFibGU7IERFTEVURSBwcm
9oaWJpdGVkIiksCiAgICAoInYyX3BhcGVyX29yZGVyX2ludGVudF9pbW11dGFibGVfdXBkYXRlIiwgI
nYyX3BhcGVyX29yZGVyX2ludGVudCIsCiAgICAgIlVQREFURSIsICJWMiBwYXBlciBvcmRlciBpbnRl
bnRzIGFyZSBpbW11dGFibGU7IFVQREFURSBwcm9oaWJpdGVkIiksCiAgICAoInYyX3BhcGVyX29yZGV
yX2ludGVudF9pbW11dGFibGVfZGVsZXRlIiwgInYyX3BhcGVyX29yZGVyX2ludGVudCIsCiAgICAgIk
RFTEVURSIsICJWMiBwYXBlciBvcmRlciBpbnRlbnRzIGFyZSBpbW11dGFibGU7IERFTEVURSBwcm9oa
WJpdGVkIiksCiAgICAoInYyX3BhcGVyX3Jpc2tfZGVjaXNpb25faW1tdXRhYmxlX3VwZGF0ZSIsICJ2
Ml9wYXBlcl9yaXNrX2RlY2lzaW9uIiwKICAgICAiVVBEQVRFIiwgIlYyIHBhcGVyIHJpc2sgZGVjaXN
pb25zIGFyZSBpbW11dGFibGU7IFVQREFURSBwcm9oaWJpdGVkIiksCiAgICAoInYyX3BhcGVyX3Jpc2
tfZGVjaXNpb25faW1tdXRhYmxlX2RlbGV0ZSIsICJ2Ml9wYXBlcl9yaXNrX2RlY2lzaW9uIiwKICAgI
CAiREVMRVRFIiwgIlYyIHBhcGVyIHJpc2sgZGVjaXNpb25zIGFyZSBpbW11dGFibGU7IERFTEVURSBw
cm9oaWJpdGVkIiksCiAgICAoInYyX3BhcGVyX29yZGVyX2V2ZW50X2ltbXV0YWJsZV91cGRhdGUiLCA
idjJfcGFwZXJfb3JkZXJfZXZlbnQiLAogICAgICJVUERBVEUiLCAiVjIgcGFwZXIgb3JkZXIgZXZlbn
RzIGFyZSBpbW11dGFibGU7IFVQREFURSBwcm9oaWJpdGVkIiksCiAgICAoInYyX3BhcGVyX29yZGVyX
2V2ZW50X2ltbXV0YWJsZV9kZWxldGUiLCAidjJfcGFwZXJfb3JkZXJfZXZlbnQiLAogICAgICJERUxF
VEUiLCAiVjIgcGFwZXIgb3JkZXIgZXZlbnRzIGFyZSBpbW11dGFibGU7IERFTEVURSBwcm9oaWJpdGV
kIiksCiAgICAoInYyX3BhcGVyX2ZpbGxfaW1tdXRhYmxlX3VwZGF0ZSIsICJ2Ml9wYXBlcl9maWxsIi
wKICAgICAiVVBEQVRFIiwgIlYyIHBhcGVyIGZpbGxzIGFyZSBpbW11dGFibGU7IFVQREFURSBwcm9oa
WJpdGVkIiksCiAgICAoInYyX3BhcGVyX2ZpbGxfaW1tdXRhYmxlX2RlbGV0ZSIsICJ2Ml9wYXBlcl9m
aWxsIiwKICAgICAiREVMRVRFIiwgIlYyIHBhcGVyIGZpbGxzIGFyZSBpbW11dGFibGU7IERFTEVURSB
wcm9oaWJpdGVkIiksCiAgICAoInYyX3BhcGVyX3Bvc2l0aW9uX3NuYXBzaG90X2ltbXV0YWJsZV91cG
RhdGUiLAogICAgICJ2Ml9wYXBlcl9wb3NpdGlvbl9zbmFwc2hvdCIsCiAgICAgIlVQREFURSIsICJWM
iBwYXBlciBwb3NpdGlvbiBzbmFwc2hvdHMgYXJlIGltbXV0YWJsZTsgVVBEQVRFIHByb2hpYml0ZWQi
KSwKICAgICgidjJfcGFwZXJfcG9zaXRpb25fc25hcHNob3RfaW1tdXRhYmxlX2RlbGV0ZSIsCiAgICA
gInYyX3BhcGVyX3Bvc2l0aW9uX3NuYXBzaG90IiwKICAgICAiREVMRVRFIiwgIlYyIHBhcGVyIHBvc2
l0aW9uIHNuYXBzaG90cyBhcmUgaW1tdXRhYmxlOyBERUxFVEUgcHJvaGliaXRlZCIpLAogICAgKCJ2M
l9wYXBlcl9iYWxhbmNlX3NuYXBzaG90X2ltbXV0YWJsZV91cGRhdGUiLAogICAgICJ2Ml9wYXBlcl9i
YWxhbmNlX3NuYXBzaG90IiwKICAgICAiVVBEQVRFIiwgIlYyIHBhcGVyIGJhbGFuY2Ugc25hcHNob3R
zIGFyZSBpbW11dGFibGU7IFVQREFURSBwcm9oaWJpdGVkIiksCiAgICAoInYyX3BhcGVyX2JhbGFuY2
Vfc25hcHNob3RfaW1tdXRhYmxlX2RlbGV0ZSIsCiAgICAgInYyX3BhcGVyX2JhbGFuY2Vfc25hcHNob
3QiLAogICAgICJERUxFVEUiLCAiVjIgcGFwZXIgYmFsYW5jZSBzbmFwc2hvdHMgYXJlIGltbXV0YWJs
ZTsgREVMRVRFIHByb2hpYml0ZWQiKSwKICAgICgidjJfcGFwZXJfcmVjb25jaWxpYXRpb25faW1tdXR
hYmxlX3VwZGF0ZSIsICJ2Ml9wYXBlcl9yZWNvbmNpbGlhdGlvbiIsCiAgICAgIlVQREFURSIsICJWMi
BwYXBlciByZWNvbmNpbGlhdGlvbnMgYXJlIGltbXV0YWJsZTsgVVBEQVRFIHByb2hpYml0ZWQiKSwKI
CAgICgidjJfcGFwZXJfcmVjb25jaWxpYXRpb25faW1tdXRhYmxlX2RlbGV0ZSIsICJ2Ml9wYXBlcl9y
ZWNvbmNpbGlhdGlvbiIsCiAgICAgIkRFTEVURSIsICJWMiBwYXBlciByZWNvbmNpbGlhdGlvbnMgYXJ
lIGltbXV0YWJsZTsgREVMRVRFIHByb2hpYml0ZWQiKSwKKQoKX1BFUk1JU1NJT05TID0gKAogICAgKC
JhZG1pbiIsICJ2Mi5wYXBlci5hY2NvdW50cy5yZWFkIiwgIlNBTC0yIiksCiAgICAoImFkbWluIiwgI
nYyLnBhcGVyLmFjY291bnRzLm1hbmFnZSIsICJTQUwtMyIpLAogICAgKCJhZG1pbiIsICJ2Mi5wYXBl
ci5vcmRlcnMucmVhZCIsICJTQUwtMiIpLAogICAgKCJhZG1pbiIsICJ2Mi5wYXBlci5vcmRlcnMucGx
hY2UiLCAiU0FMLTMiKSwKICAgICgiYWRtaW4iLCAidjIucGFwZXIub3JkZXJzLmNhbmNlbCIsICJTQU
wtMyIpLAogICAgKCJhZG1pbiIsICJ2Mi5wYXBlci5vcmRlcnMuY29uZmlybSIsICJTQUwtMyIpLAogI
CAgKCJhZG1pbiIsICJ2Mi5wYXBlci5maWxscy5yZWFkIiwgIlNBTC0yIiksCiAgICAoImFkbWluIiwg
InYyLnBhcGVyLnJpc2sucmVhZCIsICJTQUwtMiIpLAopCgpfUFhTX0ZJTEVTID0gKAogICAgImFwcC9
2Mi9wYXBlcl90cmFkaW5nL3NpbXVsYXRvci5weSIsCiAgICAiYXBwL3YyL3BhcGVyX3RyYWRpbmcvbG
VkZ2VyLnB5IiwKKQpfUFJHX0ZJTEVTID0gKAogICAgImFwcC92Mi9wYXBlcl90cmFkaW5nL3Jpc2suc
HkiLAogICAgImFwcC92Mi9wYXBlcl90cmFkaW5nL2NvbnRyYWN0cy5weSIsCikKCl9EQVRBX0NMQVNT
X0NIRUNLID0gKAogICAgImRhdGFfY2xhc3MgSU4gKCdzeW50aGV0aWMnLCdzaW11bGF0ZWQnLCdoaXN
0b3JpY2FsX3JlYWwnLCdsaXZlJywiCiAgICAiJ3N0YWxlX2NhY2hlZCcsJ3VuYXZhaWxhYmxlJykiCi
kKCgpkZWYgX3JvbGxpbmdfaGFzaChmaWxlczogdHVwbGVbc3RyLCAuLi5dKSAtPiBzdHI6CiAgICBiY
XNlID0gUGF0aChfX2ZpbGVfXykucmVzb2x2ZSgpLnBhcmVudHNbMl0KICAgIGRpZ2VzdCA9IGhhc2hs
aWIuc2hhMjU2KCkKICAgIGZvciByZWwgaW4gZmlsZXM6CiAgICAgICAgZGlnZXN0LnVwZGF0ZShyZWw
uZW5jb2RlKCJ1dGYtOCIpKQogICAgICAgIGRpZ2VzdC51cGRhdGUoYiJceDAwIikKICAgICAgICBkaW
dlc3QudXBkYXRlKChiYXNlIC8gcmVsKS5yZWFkX2J5dGVzKCkpCiAgICAgICAgZGlnZXN0LnVwZGF0Z
ShiIlx4MDAiKQogICAgcmV0dXJuIGRpZ2VzdC5oZXhkaWdlc3QoKQoKCmRlZiBfY3JlYXRlX3RyaWdn
ZXJzKGJpbmQpIC0+IE5vbmU6CiAgICBpZiBiaW5kLmRpYWxlY3QubmFtZSA9PSAic3FsaXRlIjoKICA
gICAgICBmb3IgbmFtZSwgdGFibGUsIGV2ZW50LCBtZXNzYWdlIGluIF9UUklHR0VSUzoKICAgICAgIC
AgICAgb3AuZXhlY3V0ZShmIiIiCiAgICAgICAgICAgICAgICBDUkVBVEUgVFJJR0dFUiB7bmFtZX0KI
CAgICAgICAgICAgICAgIEJFRk9SRSB7ZXZlbnR9IE9OIHt0YWJsZX0KICAgICAgICAgICAgICAgIEJF
R0lOCiAgICAgICAgICAgICAgICAgICAgU0VMRUNUIFJBSVNFKEFCT1JULCAne21lc3NhZ2V9Jyk7CiA
gICAgICAgICAgICAgICBFTkQ7CiAgICAgICAgICAgICIiIikKICAgIGVsaWYgYmluZC5kaWFsZWN0Lm
5hbWUgPT0gInBvc3RncmVzcWwiOgogICAgICAgIG9wLmV4ZWN1dGUoIiIiCiAgICAgICAgICAgIENSR
UFURSBPUiBSRVBMQUNFIEZVTkNUSU9OIHByZXZlbnRfdjJfcGFwZXJfdHJhZGluZ19tdXRhdGlvbigp
CiAgICAgICAgICAgIFJFVFVSTlMgdHJpZ2dlciBBUyAkJAogICAgICAgICAgICBCRUdJTgogICAgICA
gICAgICAgICAgUkFJU0UgRVhDRVBUSU9OCiAgICAgICAgICAgICAgICAgICAgJ1YyIHBhcGVyLXRyYW
RpbmcgYXJ0aWZhY3QgaXMgaW1tdXRhYmxlOyAlIHByb2hpYml0ZWQgb24gJScsCiAgICAgICAgICAgI
CAgICAgICAgVEdfT1AsIFRHX1RBQkxFX05BTUU7CiAgICAgICAgICAgIEVORDsKICAgICAgICAgICAg
JCQgTEFOR1VBR0UgcGxwZ3NxbDsKICAgICAgICAiIiIpCiAgICAgICAgZm9yIG5hbWUsIHRhYmxlLCB
ldmVudCwgX21lc3NhZ2UgaW4gX1RSSUdHRVJTOgogICAgICAgICAgICBvcC5leGVjdXRlKGYiIiIKIC
AgICAgICAgICAgICAgIENSRUFURSBUUklHR0VSIHtuYW1lfQogICAgICAgICAgICAgICAgQkVGT1JFI
HtldmVudH0gT04ge3RhYmxlfQogICAgICAgICAgICAgICAgRk9SIEVBQ0ggUk9XIEVYRUNVVEUgRlVO
Q1RJT04gcHJldmVudF92Ml9wYXBlcl90cmFkaW5nX211dGF0aW9uKCk7CiAgICAgICAgICAgICIiIik
KCgpkZWYgX2Ryb3BfdHJpZ2dlcnMoYmluZCkgLT4gTm9uZToKICAgIGlmIGJpbmQuZGlhbGVjdC5uYW
1lID09ICJzcWxpdGUiOgogICAgICAgIGZvciBuYW1lLCBfdCwgX2UsIF9tIGluIF9UUklHR0VSUzoKI
CAgICAgICAgICAgb3AuZXhlY3V0ZShmIkRST1AgVFJJR0dFUiBJRiBFWElTVFMge25hbWV9IikKICAg
IGVsaWYgYmluZC5kaWFsZWN0Lm5hbWUgPT0gInBvc3RncmVzcWwiOgogICAgICAgIGZvciBuYW1lLCB
0YWJsZSwgX2UsIF9tIGluIF9UUklHR0VSUzoKICAgICAgICAgICAgb3AuZXhlY3V0ZShmIkRST1AgVF
JJR0dFUiBJRiBFWElTVFMge25hbWV9IE9OIHt0YWJsZX0iKQogICAgICAgIG9wLmV4ZWN1dGUoCiAgI
CAgICAgICAgICJEUk9QIEZVTkNUSU9OIElGIEVYSVNUUyBwcmV2ZW50X3YyX3BhcGVyX3RyYWRpbmdf
bXV0YXRpb24oKSIpCgoKZGVmIF9kcm9wX2NvbXB2ZXJfZGVsZXRlX2d1YXJkKGJpbmQpIC0+IE5vbmU
6CiAgICBpZiBiaW5kLmRpYWxlY3QubmFtZSA9PSAic3FsaXRlIjoKICAgICAgICBvcC5leGVjdXRlKA
ogICAgICAgICAgICAiRFJPUCBUUklHR0VSIElGIEVYSVNUUyB2Ml9jb21wdXRhdGlvbl92ZXJzaW9uX
2ltbXV0YWJsZV9kZWxldGUiKQogICAgZWxpZiBiaW5kLmRpYWxlY3QubmFtZSA9PSAicG9zdGdyZXNx
bCI6CiAgICAgICAgb3AuZXhlY3V0ZSgKICAgICAgICAgICAgIkRST1AgVFJJR0dFUiBJRiBFWElTVFM
gdjJfY29tcHV0YXRpb25fdmVyc2lvbl9pbW11dGFibGVfZGVsZXRlIgogICAgICAgICAgICAiIE9OIH
YyX2NvbXB1dGF0aW9uX3ZlcnNpb24iKQoKCmRlZiBfcmVjcmVhdGVfY29tcHZlcl9kZWxldGVfZ3Vhc
mQoYmluZCkgLT4gTm9uZToKICAgIGlmIGJpbmQuZGlhbGVjdC5uYW1lID09ICJzcWxpdGUiOgogICAg
ICAgIG9wLmV4ZWN1dGUoIiIiCiAgICAgICAgICAgIENSRUFURSBUUklHR0VSIHYyX2NvbXB1dGF0aW9
uX3ZlcnNpb25faW1tdXRhYmxlX2RlbGV0ZQogICAgICAgICAgICBCRUZPUkUgREVMRVRFIE9OIHYyX2
NvbXB1dGF0aW9uX3ZlcnNpb24KICAgICAgICAgICAgQkVHSU4KICAgICAgICAgICAgICAgIFNFTEVDV
CBSQUlTRShBQk9SVCwKICAgICAgICAgICAgICAgICAgICAnVjIgY29tcHV0YXRpb24gdmVyc2lvbiBy
ZWdpc3RyeSBpcyBpbW11dGFibGU7IERFTEVURSBwcm9oaWJpdGVkJyk7CiAgICAgICAgICAgIEVORDs
KICAgICAgICAiIiIpCiAgICAgICAgY291bnQgPSBiaW5kLmV4ZWN1dGUoc2EudGV4dCgKICAgICAgIC
AgICAgIlNFTEVDVCBDT1VOVCgqKSBGUk9NIHNxbGl0ZV9tYXN0ZXIgV0hFUkUgdHlwZT0ndHJpZ2dlc
iciCiAgICAgICAgICAgICIgQU5EIG5hbWU9J3YyX2NvbXB1dGF0aW9uX3ZlcnNpb25faW1tdXRhYmxl
X2RlbGV0ZSciKSkuc2NhbGFyX29uZSgpCiAgICBlbGlmIGJpbmQuZGlhbGVjdC5uYW1lID09ICJwb3N
0Z3Jlc3FsIjoKICAgICAgICBvcC5leGVjdXRlKCIiIgogICAgICAgICAgICBDUkVBVEUgVFJJR0dFUi
B2Ml9jb21wdXRhdGlvbl92ZXJzaW9uX2ltbXV0YWJsZV9kZWxldGUKICAgICAgICAgICAgQkVGT1JFI
ERFTEVURSBPTiB2Ml9jb21wdXRhdGlvbl92ZXJzaW9uCiAgICAgICAgICAgIEZPUiBFQUNIIFJPVyBF
WEVDVVRFIEZVTkNUSU9OIHByZXZlbnRfdjJfcmVzZWFyY2hfbXV0YXRpb24oKTsKICAgICAgICAiIiI
pCiAgICAgICAgY291bnQgPSBiaW5kLmV4ZWN1dGUoc2EudGV4dCgKICAgICAgICAgICAgIlNFTEVDVC
BDT1VOVCgqKSBGUk9NIHBnX3RyaWdnZXIiCiAgICAgICAgICAgICIgV0hFUkUgdGduYW1lPSd2Ml9jb
21wdXRhdGlvbl92ZXJzaW9uX2ltbXV0YWJsZV9kZWxldGUnIikpLnNjYWxhcl9vbmUoKQogICAgZWxz
ZTogICMgcHJhZ21hOiBubyBjb3ZlcgogICAgICAgIHJldHVybgogICAgaWYgaW50KGNvdW50KSAhPSA
xOgogICAgICAgIHJhaXNlIFJ1bnRpbWVFcnJvcigKICAgICAgICAgICAgImNvbXB2ZXIgZGVsZXRlIG
d1YXJkIE5PVCByZXN0b3JlZCAtIG1hbnVhbCByZWNvdmVyeSByZXF1aXJlZCIpCgoKZGVmIF9iZTFfY
29sdW1ucygpIC0+IGxpc3Q6CiAgICByZXR1cm4gWwogICAgICAgIHNhLkNvbHVtbigiZGF0YV9jbGFz
cyIsIHNhLlN0cmluZygzMiksIG51bGxhYmxlPUZhbHNlKSwKICAgICAgICBzYS5Db2x1bW4oIm1vZGU
iLCBzYS5TdHJpbmcoMTYpLCBudWxsYWJsZT1GYWxzZSksCiAgICAgICAgc2EuQ29sdW1uKCJvcGVyYX
Rvcl9pZCIsIHNhLlN0cmluZygxMjgpLCBudWxsYWJsZT1GYWxzZSksCiAgICAgICAgc2EuQ29sdW1uK
CJjb3JyZWxhdGlvbl9pZCIsIHNhLlN0cmluZyg2NCksIG51bGxhYmxlPVRydWUpLAogICAgICAgIHNh
LkNvbHVtbigiY3JlYXRlZF9hdCIsIHNhLkRhdGVUaW1lKHRpbWV6b25lPVRydWUpLCBudWxsYWJsZT1
GYWxzZSksCiAgICBdCgoKZGVmIHVwZ3JhZGUoKSAtPiBOb25lOgogICAgYmluZCA9IG9wLmdldF9iaW
5kKCkKICAgIG5vdyA9IGRhdGV0aW1lLm5vdyh0aW1lem9uZS51dGMpCgogICAgb3AuY3JlYXRlX3RhY
mxlKAogICAgICAgICJ2Ml9wYXBlcl9hY2NvdW50IiwKICAgICAgICBzYS5Db2x1bW4oImlkIiwgc2Eu
U3RyaW5nKDM2KSwgcHJpbWFyeV9rZXk9VHJ1ZSksCiAgICAgICAgc2EuQ29sdW1uKCJhY2NvdW50X2l
kIiwgc2EuU3RyaW5nKDY0KSwgbnVsbGFibGU9RmFsc2UpLAogICAgICAgIHNhLkNvbHVtbigicmVjb3
JkX3NlcSIsIHNhLkludGVnZXIoKSwgbnVsbGFibGU9RmFsc2UpLAogICAgICAgIHNhLkNvbHVtbigic
3VwZXJzZWRlcyIsIHNhLlN0cmluZygzNiksIG51bGxhYmxlPVRydWUpLAogICAgICAgIHNhLkNvbHVt
bigibmFtZSIsIHNhLlN0cmluZygxMjgpLCBudWxsYWJsZT1GYWxzZSksCiAgICAgICAgc2EuQ29sdW1
uKCJiYXNlX2N1cnJlbmN5Iiwgc2EuU3RyaW5nKDgpLCBudWxsYWJsZT1GYWxzZSksCiAgICAgICAgc2
EuQ29sdW1uKCJpbml0aWFsX2JhbGFuY2UiLCBzYS5TdHJpbmcoNjQpLCBudWxsYWJsZT1GYWxzZSksC
iAgICAgICAgc2EuQ29sdW1uKCJtYXJnaW5fcGFyYW1zIiwgc2EuSlNPTigpLCBudWxsYWJsZT1GYWxz
ZSksCiAgICAgICAgc2EuQ29sdW1uKCJsaWZlY3ljbGVfc3RhdGUiLCBzYS5TdHJpbmcoMTYpLCBudWx
sYWJsZT1GYWxzZSksCiAgICAgICAgc2EuQ29sdW1uKCJjb25maXJtYXRpb25fcmVmIiwgc2EuU3RyaW
5nKDY0KSwgbnVsbGFibGU9RmFsc2UpLAogICAgICAgICpfYmUxX2NvbHVtbnMoKSwKICAgICAgICBzY
S5VbmlxdWVDb25zdHJhaW50KCJhY2NvdW50X2lkIiwgInJlY29yZF9zZXEiLAogICAgICAgICAgICAg
ICAgICAgICAgICAgICAgbmFtZT0idXFfdjJfcGFjY3RfaWRfc2VxIiksCiAgICAgICAgc2EuQ2hlY2t
Db25zdHJhaW50KCJiYXNlX2N1cnJlbmN5IElOICgnVVNEJykiLAogICAgICAgICAgICAgICAgICAgIC
AgICAgICBuYW1lPSJja192Ml9wYWNjdF9jY3kiKSwKICAgICAgICBzYS5DaGVja0NvbnN0cmFpbnQoC
iAgICAgICAgICAgICJsaWZlY3ljbGVfc3RhdGUgSU4gKCdhY3RpdmUnLCdmcm96ZW4nLCdjbG9zZWQn
KSIsCiAgICAgICAgICAgIG5hbWU9ImNrX3YyX3BhY2N0X3N0YXRlIiksCiAgICAgICAgc2EuQ2hlY2t
Db25zdHJhaW50KF9EQVRBX0NMQVNTX0NIRUNLLCBuYW1lPSJja192Ml9wYWNjdF9kYXRhX2NsYXNzIi
ksCiAgICApCiAgICBvcC5jcmVhdGVfaW5kZXgoIml4X3YyX3BhY2N0X2FjY291bnQiLCAidjJfcGFwZ
XJfYWNjb3VudCIsCiAgICAgICAgICAgICAgICAgICAgWyJhY2NvdW50X2lkIl0pCgogICAgb3AuY3Jl
YXRlX3RhYmxlKAogICAgICAgICJ2Ml9wYXBlcl9vcmRlcl9pbnRlbnQiLAogICAgICAgIHNhLkNvbHV
tbigiaWQiLCBzYS5TdHJpbmcoMzYpLCBwcmltYXJ5X2tleT1UcnVlKSwKICAgICAgICBzYS5Db2x1bW
4oImludGVudF9pZCIsIHNhLlN0cmluZyg2NCksIG51bGxhYmxlPUZhbHNlLCB1bmlxdWU9VHJ1ZSksC
iAgICAgICAgc2EuQ29sdW1uKCJhY2NvdW50X2lkIiwgc2EuU3RyaW5nKDM2KSwgbnVsbGFibGU9RmFs
c2UpLAogICAgICAgIHNhLkNvbHVtbigiaW5zdHJ1bWVudF9pZCIsIHNhLlN0cmluZyg2NCksIG51bGx
hYmxlPUZhbHNlKSwKICAgICAgICBzYS5Db2x1bW4oInNpZGUiLCBzYS5TdHJpbmcoOCksIG51bGxhYm
xlPUZhbHNlKSwKICAgICAgICBzYS5Db2x1bW4oIm9yZGVyX3R5cGUiLCBzYS5TdHJpbmcoMTYpLCBud
WxsYWJsZT1GYWxzZSksCiAgICAgICAgc2EuQ29sdW1uKCJxdWFudGl0eSIsIHNhLlN0cmluZyg2NCks
IG51bGxhYmxlPUZhbHNlKSwKICAgICAgICBzYS5Db2x1bW4oImxpbWl0X3ByaWNlIiwgc2EuU3RyaW5
nKDY0KSwgbnVsbGFibGU9VHJ1ZSksCiAgICAgICAgc2EuQ29sdW1uKCJ0aW1lX2luX2ZvcmNlIiwgc2
EuU3RyaW5nKDE2KSwgbnVsbGFibGU9RmFsc2UpLAogICAgICAgIHNhLkNvbHVtbigiaWRlbXBvdGVuY
3lfa2V5Iiwgc2EuU3RyaW5nKDY0KSwgbnVsbGFibGU9RmFsc2UpLAogICAgICAgIHNhLkNvbHVtbigi
c25hcHNob3RfcmVmIiwgc2EuU3RyaW5nKDY0KSwgbnVsbGFibGU9RmFsc2UpLAogICAgICAgIHNhLkN
vbHVtbigidGltZV9iYXNpcyIsIHNhLkpTT04oKSwgbnVsbGFibGU9RmFsc2UpLAogICAgICAgIHNhLk
NvbHVtbigiY29uZmlybWF0aW9uX3JlZiIsIHNhLlN0cmluZyg2NCksIG51bGxhYmxlPVRydWUpLAogI
CAgICAgIHNhLkNvbHVtbigiYWN0b3JfaWQiLCBzYS5TdHJpbmcoMTI4KSwgbnVsbGFibGU9RmFsc2Up
LAogICAgICAgICpfYmUxX2NvbHVtbnMoKSwKICAgICAgICBzYS5VbmlxdWVDb25zdHJhaW50KCJhY2N
vdW50X2lkIiwgImlkZW1wb3RlbmN5X2tleSIsCiAgICAgICAgICAgICAgICAgICAgICAgICAgICBuYW
1lPSJ1cV92Ml9waW50ZW50X2lkZW0iKSwKICAgICAgICBzYS5DaGVja0NvbnN0cmFpbnQoInNpZGUgS
U4gKCdidXknLCdzZWxsJykiLAogICAgICAgICAgICAgICAgICAgICAgICAgICBuYW1lPSJja192Ml9w
aW50ZW50X3NpZGUiKSwKICAgICAgICBzYS5DaGVja0NvbnN0cmFpbnQoIm9yZGVyX3R5cGUgSU4gKCd
tYXJrZXQnLCdsaW1pdCcpIiwKICAgICAgICAgICAgICAgICAgICAgICAgICAgbmFtZT0iY2tfdjJfcG
ludGVudF90eXBlIiksCiAgICAgICAgc2EuQ2hlY2tDb25zdHJhaW50KCJ0aW1lX2luX2ZvcmNlIElOI
CgncmVwbGF5X3dpbmRvdycpIiwKICAgICAgICAgICAgICAgICAgICAgICAgICAgbmFtZT0iY2tfdjJf
cGludGVudF90aWYiKSwKICAgICAgICBzYS5DaGVja0NvbnN0cmFpbnQoCiAgICAgICAgICAgICIob3J
kZXJfdHlwZSA9ICdsaW1pdCcpID0gKGxpbWl0X3ByaWNlIElTIE5PVCBOVUxMKSIsCiAgICAgICAgIC
AgIG5hbWU9ImNrX3YyX3BpbnRlbnRfbGltaXRfaWZmIiksCiAgICAgICAgc2EuQ2hlY2tDb25zdHJha
W50KCJDQVNUKHF1YW50aXR5IEFTIFJFQUwpID4gMCIsCiAgICAgICAgICAgICAgICAgICAgICAgICAg
IG5hbWU9ImNrX3YyX3BpbnRlbnRfcXR5IiksCiAgICAgICAgc2EuQ2hlY2tDb25zdHJhaW50KF9EQVR
BX0NMQVNTX0NIRUNLLAogICAgICAgICAgICAgICAgICAgICAgICAgICBuYW1lPSJja192Ml9waW50ZW
50X2RhdGFfY2xhc3MiKSwKICAgICkKICAgIG9wLmNyZWF0ZV9pbmRleCgiaXhfdjJfcGludGVudF9hY
2NvdW50IiwgInYyX3BhcGVyX29yZGVyX2ludGVudCIsCiAgICAgICAgICAgICAgICAgICAgWyJhY2Nv
dW50X2lkIl0pCgogICAgb3AuY3JlYXRlX3RhYmxlKAogICAgICAgICJ2Ml9wYXBlcl9yaXNrX2RlY2l
zaW9uIiwKICAgICAgICBzYS5Db2x1bW4oImlkIiwgc2EuU3RyaW5nKDM2KSwgcHJpbWFyeV9rZXk9VH
J1ZSksCiAgICAgICAgc2EuQ29sdW1uKCJpbnRlbnRfaWQiLCBzYS5TdHJpbmcoMzYpLCBudWxsYWJsZ
T1GYWxzZSksCiAgICAgICAgc2EuQ29sdW1uKCJkZWNpc2lvbiIsIHNhLlN0cmluZyg4KSwgbnVsbGFi
bGU9RmFsc2UpLAogICAgICAgIHNhLkNvbHVtbigiZXZhbHVhdGVkX2xpbWl0cyIsIHNhLkpTT04oKSw
gbnVsbGFibGU9RmFsc2UpLAogICAgICAgIHNhLkNvbHVtbigicmVhc29ucyIsIHNhLkpTT04oKSwgbn
VsbGFibGU9RmFsc2UpLAogICAgICAgIHNhLkNvbHVtbigicmlza19jb25maWdfdmVyc2lvbiIsIHNhL
lN0cmluZygzMiksIG51bGxhYmxlPUZhbHNlKSwKICAgICAgICBzYS5Db2x1bW4oImRlY2lkZWRfYXRf
YmFzaXMiLCBzYS5KU09OKCksIG51bGxhYmxlPUZhbHNlKSwKICAgICAgICBzYS5Db2x1bW4oImNvbmZ
pcm1hdGlvbl9yZWYiLCBzYS5TdHJpbmcoNjQpLCBudWxsYWJsZT1UcnVlKSwKICAgICAgICAqX2JlMV
9jb2x1bW5zKCksCiAgICAgICAgc2EuVW5pcXVlQ29uc3RyYWludCgiaW50ZW50X2lkIiwgbmFtZT0id
XFfdjJfcHJpc2tfaW50ZW50IiksCiAgICAgICAgc2EuQ2hlY2tDb25zdHJhaW50KCJkZWNpc2lvbiBJ
TiAoJ3Bhc3MnLCdibG9jaycsJ2hvbGQnKSIsCiAgICAgICAgICAgICAgICAgICAgICAgICAgIG5hbWU
9ImNrX3YyX3ByaXNrX2RlY2lzaW9uIiksCiAgICAgICAgc2EuQ2hlY2tDb25zdHJhaW50KAogICAgIC
AgICAgICAiKGRlY2lzaW9uID0gJ2hvbGQnKSA9IChjb25maXJtYXRpb25fcmVmIElTIE5PVCBOVUxMK
SIsCiAgICAgICAgICAgIG5hbWU9ImNrX3YyX3ByaXNrX3JlZl9pZmYiKSwKICAgICAgICBzYS5DaGVj
a0NvbnN0cmFpbnQoX0RBVEFfQ0xBU1NfQ0hFQ0ssIG5hbWU9ImNrX3YyX3ByaXNrX2RhdGFfY2xhc3M
iKSwKICAgICkKCiAgICBvcC5jcmVhdGVfdGFibGUoCiAgICAgICAgInYyX3BhcGVyX29yZGVyX2V2ZW
50IiwKICAgICAgICBzYS5Db2x1bW4oImlkIiwgc2EuU3RyaW5nKDM2KSwgcHJpbWFyeV9rZXk9VHJ1Z
SksCiAgICAgICAgc2EuQ29sdW1uKCJpbnRlbnRfaWQiLCBzYS5TdHJpbmcoMzYpLCBudWxsYWJsZT1G
YWxzZSksCiAgICAgICAgc2EuQ29sdW1uKCJldmVudF9pbmRleCIsIHNhLkludGVnZXIoKSwgbnVsbGF
ibGU9RmFsc2UpLAogICAgICAgIHNhLkNvbHVtbigiZnJvbV9zdGF0ZSIsIHNhLlN0cmluZygyNCksIG
51bGxhYmxlPUZhbHNlKSwKICAgICAgICBzYS5Db2x1bW4oInRvX3N0YXRlIiwgc2EuU3RyaW5nKDI0K
SwgbnVsbGFibGU9RmFsc2UpLAogICAgICAgIHNhLkNvbHVtbigiZXZlbnRfY2xhc3MiLCBzYS5TdHJp
bmcoNDgpLCBudWxsYWJsZT1GYWxzZSksCiAgICAgICAgc2EuQ29sdW1uKCJkZXRhaWxzIiwgc2EuSlN
PTigpLCBudWxsYWJsZT1GYWxzZSksCiAgICAgICAgc2EuQ29sdW1uKCJhY3Rvcl9pZCIsIHNhLlN0cm
luZygxMjgpLCBudWxsYWJsZT1GYWxzZSksCiAgICAgICAgKl9iZTFfY29sdW1ucygpLAogICAgICAgI
HNhLlVuaXF1ZUNvbnN0cmFpbnQoImludGVudF9pZCIsICJldmVudF9pbmRleCIsCiAgICAgICAgICAg
ICAgICAgICAgICAgICAgICBuYW1lPSJ1cV92Ml9wZXZlbnRfaWR4IiksCiAgICAgICAgc2EuQ2hlY2t
Db25zdHJhaW50KF9EQVRBX0NMQVNTX0NIRUNLLCBuYW1lPSJja192Ml9wZXZlbnRfZGF0YV9jbGFzcy
IpLAogICAgKQogICAgb3AuY3JlYXRlX2luZGV4KCJpeF92Ml9wZXZlbnRfaW50ZW50IiwgInYyX3Bhc
GVyX29yZGVyX2V2ZW50IiwKICAgICAgICAgICAgICAgICAgICBbImludGVudF9pZCJdKQoKICAgIG9w
LmNyZWF0ZV90YWJsZSgKICAgICAgICAidjJfcGFwZXJfZmlsbCIsCiAgICAgICAgc2EuQ29sdW1uKCJ
pZCIsIHNhLlN0cmluZygzNiksIHByaW1hcnlfa2V5PVRydWUpLAogICAgICAgIHNhLkNvbHVtbigiZm
lsbF9pZCIsIHNhLlN0cmluZyg2NCksIG51bGxhYmxlPUZhbHNlLCB1bmlxdWU9VHJ1ZSksCiAgICAgI
CAgc2EuQ29sdW1uKCJpbnRlbnRfaWQiLCBzYS5TdHJpbmcoMzYpLCBudWxsYWJsZT1GYWxzZSksCiAg
ICAgICAgc2EuQ29sdW1uKCJmaWxsX2luZGV4Iiwgc2EuSW50ZWdlcigpLCBudWxsYWJsZT1GYWxzZSk
sCiAgICAgICAgc2EuQ29sdW1uKCJxdWFudGl0eSIsIHNhLlN0cmluZyg2NCksIG51bGxhYmxlPUZhbH
NlKSwKICAgICAgICBzYS5Db2x1bW4oInJhd19wcmljZSIsIHNhLlN0cmluZyg2NCksIG51bGxhYmxlP
UZhbHNlKSwKICAgICAgICBzYS5Db2x1bW4oImVmZmVjdGl2ZV9wcmljZSIsIHNhLlN0cmluZyg2NCks
IG51bGxhYmxlPUZhbHNlKSwKICAgICAgICBzYS5Db2x1bW4oImNvc3RfbW9kZWxfcmVmIiwgc2EuSlN
PTigpLCBudWxsYWJsZT1GYWxzZSksCiAgICAgICAgc2EuQ29sdW1uKCJmaWxsX2NsYXNzIiwgc2EuU3
RyaW5nKDI0KSwgbnVsbGFibGU9RmFsc2UpLAogICAgICAgIHNhLkNvbHVtbigic2ltdWxhdG9yX3Zlc
nNpb24iLCBzYS5TdHJpbmcoMzIpLCBudWxsYWJsZT1GYWxzZSksCiAgICAgICAgc2EuQ29sdW1uKCJz
bmFwc2hvdF9yZWYiLCBzYS5TdHJpbmcoNjQpLCBudWxsYWJsZT1GYWxzZSksCiAgICAgICAgc2EuQ29
sdW1uKCJ0aW1lX2Jhc2lzIiwgc2EuSlNPTigpLCBudWxsYWJsZT1GYWxzZSksCiAgICAgICAgKl9iZT
FfY29sdW1ucygpLAogICAgICAgIHNhLlVuaXF1ZUNvbnN0cmFpbnQoImludGVudF9pZCIsICJmaWxsX
2luZGV4IiwKICAgICAgICAgICAgICAgICAgICAgICAgICAgIG5hbWU9InVxX3YyX3BmaWxsX2lkeCIp
LAogICAgICAgIHNhLkNoZWNrQ29uc3RyYWludCgiZmlsbF9jbGFzcyBJTiAoJ3BhcGVyX3NpbXVsYXR
lZCcpIiwKICAgICAgICAgICAgICAgICAgICAgICAgICAgbmFtZT0iY2tfdjJfcGZpbGxfY2xhc3MiKS
wKICAgICAgICBzYS5DaGVja0NvbnN0cmFpbnQoX0RBVEFfQ0xBU1NfQ0hFQ0ssIG5hbWU9ImNrX3YyX
3BmaWxsX2RhdGFfY2xhc3MiKSwKICAgICkKICAgIG9wLmNyZWF0ZV9pbmRleCgiaXhfdjJfcGZpbGxf
aW50ZW50IiwgInYyX3BhcGVyX2ZpbGwiLCBbImludGVudF9pZCJdKQoKICAgIG9wLmNyZWF0ZV90YWJ
sZSgKICAgICAgICAidjJfcGFwZXJfcG9zaXRpb25fc25hcHNob3QiLAogICAgICAgIHNhLkNvbHVtbi
giaWQiLCBzYS5TdHJpbmcoMzYpLCBwcmltYXJ5X2tleT1UcnVlKSwKICAgICAgICBzYS5Db2x1bW4oI
mFjY291bnRfaWQiLCBzYS5TdHJpbmcoMzYpLCBudWxsYWJsZT1GYWxzZSksCiAgICAgICAgc2EuQ29s
dW1uKCJhc19vZl9iYXNpcyIsIHNhLkpTT04oKSwgbnVsbGFibGU9RmFsc2UpLAogICAgICAgIHNhLkN
vbHVtbigicG9zaXRpb25zIiwgc2EuSlNPTigpLCBudWxsYWJsZT1GYWxzZSksCiAgICAgICAgc2EuQ2
9sdW1uKCJkZXJpdmF0aW9uX2lucHV0c19oYXNoIiwgc2EuU3RyaW5nKDY0KSwgbnVsbGFibGU9RmFsc
2UpLAogICAgICAgIHNhLkNvbHVtbigiZW5naW5lX3ZlcnNpb25zX2hhc2giLCBzYS5TdHJpbmcoNjQp
LCBudWxsYWJsZT1GYWxzZSksCiAgICAgICAgKl9iZTFfY29sdW1ucygpLAogICAgICAgIHNhLlVuaXF
1ZUNvbnN0cmFpbnQoImFjY291bnRfaWQiLCAiZGVyaXZhdGlvbl9pbnB1dHNfaGFzaCIsCiAgICAgIC
AgICAgICAgICAgICAgICAgICAgICAiZW5naW5lX3ZlcnNpb25zX2hhc2giLAogICAgICAgICAgICAgI
CAgICAgICAgICAgICAgbmFtZT0idXFfdjJfcHBvc19hbmNob3IiKSwKICAgICAgICBzYS5DaGVja0Nv
bnN0cmFpbnQoX0RBVEFfQ0xBU1NfQ0hFQ0ssIG5hbWU9ImNrX3YyX3Bwb3NfZGF0YV9jbGFzcyIpLAo
gICAgKQogICAgb3AuY3JlYXRlX2luZGV4KCJpeF92Ml9wcG9zX2FjY291bnQiLCAidjJfcGFwZXJfcG
9zaXRpb25fc25hcHNob3QiLAogICAgICAgICAgICAgICAgICAgIFsiYWNjb3VudF9pZCJdKQoKICAgI
G9wLmNyZWF0ZV90YWJsZSgKICAgICAgICAidjJfcGFwZXJfYmFsYW5jZV9zbmFwc2hvdCIsCiAgICAg
ICAgc2EuQ29sdW1uKCJpZCIsIHNhLlN0cmluZygzNiksIHByaW1hcnlfa2V5PVRydWUpLAogICAgICA
gIHNhLkNvbHVtbigiYWNjb3VudF9pZCIsIHNhLlN0cmluZygzNiksIG51bGxhYmxlPUZhbHNlKSwKIC
AgICAgICBzYS5Db2x1bW4oImFzX29mX2Jhc2lzIiwgc2EuSlNPTigpLCBudWxsYWJsZT1GYWxzZSksC
iAgICAgICAgc2EuQ29sdW1uKCJjYXNoIiwgc2EuU3RyaW5nKDY0KSwgbnVsbGFibGU9RmFsc2UpLAog
ICAgICAgIHNhLkNvbHVtbigiZXF1aXR5Iiwgc2EuU3RyaW5nKDY0KSwgbnVsbGFibGU9RmFsc2UpLAo
gICAgICAgIHNhLkNvbHVtbigibWFyZ2luX3VzZWQiLCBzYS5TdHJpbmcoNjQpLCBudWxsYWJsZT1GYW
xzZSksCiAgICAgICAgc2EuQ29sdW1uKCJtYXJnaW5fYXZhaWxhYmxlIiwgc2EuU3RyaW5nKDY0KSwgb
nVsbGFibGU9RmFsc2UpLAogICAgICAgIHNhLkNvbHVtbigidW5yZWFsaXplZF9wbmwiLCBzYS5TdHJp
bmcoNjQpLCBudWxsYWJsZT1GYWxzZSksCiAgICAgICAgc2EuQ29sdW1uKCJyZWFsaXplZF9wbmwiLCB
zYS5TdHJpbmcoNjQpLCBudWxsYWJsZT1GYWxzZSksCiAgICAgICAgc2EuQ29sdW1uKCJkZXJpdmF0aW
9uX2lucHV0c19oYXNoIiwgc2EuU3RyaW5nKDY0KSwgbnVsbGFibGU9RmFsc2UpLAogICAgICAgIHNhL
kNvbHVtbigiZW5naW5lX3ZlcnNpb25zX2hhc2giLCBzYS5TdHJpbmcoNjQpLCBudWxsYWJsZT1GYWxz
ZSksCiAgICAgICAgKl9iZTFfY29sdW1ucygpLAogICAgICAgIHNhLlVuaXF1ZUNvbnN0cmFpbnQoImF
jY291bnRfaWQiLCAiZGVyaXZhdGlvbl9pbnB1dHNfaGFzaCIsCiAgICAgICAgICAgICAgICAgICAgIC
AgICAgICAiZW5naW5lX3ZlcnNpb25zX2hhc2giLAogICAgICAgICAgICAgICAgICAgICAgICAgICAgb
mFtZT0idXFfdjJfcGJhbF9hbmNob3IiKSwKICAgICAgICBzYS5DaGVja0NvbnN0cmFpbnQoX0RBVEFf
Q0xBU1NfQ0hFQ0ssIG5hbWU9ImNrX3YyX3BiYWxfZGF0YV9jbGFzcyIpLAogICAgKQogICAgb3AuY3J
lYXRlX2luZGV4KCJpeF92Ml9wYmFsX2FjY291bnQiLCAidjJfcGFwZXJfYmFsYW5jZV9zbmFwc2hvdC
IsCiAgICAgICAgICAgICAgICAgICAgWyJhY2NvdW50X2lkIl0pCgogICAgb3AuY3JlYXRlX3RhYmxlK
AogICAgICAgICJ2Ml9wYXBlcl9yZWNvbmNpbGlhdGlvbiIsCiAgICAgICAgc2EuQ29sdW1uKCJpZCIs
IHNhLlN0cmluZygzNiksIHByaW1hcnlfa2V5PVRydWUpLAogICAgICAgIHNhLkNvbHVtbigiYWNjb3V
udF9pZCIsIHNhLlN0cmluZygzNiksIG51bGxhYmxlPUZhbHNlKSwKICAgICAgICBzYS5Db2x1bW4oIn
J1bl9iYXNpcyIsIHNhLkpTT04oKSwgbnVsbGFibGU9RmFsc2UpLAogICAgICAgIHNhLkNvbHVtbigib
3V0Y29tZSIsIHNhLlN0cmluZygxNiksIG51bGxhYmxlPUZhbHNlKSwKICAgICAgICBzYS5Db2x1bW4o
ImRpc2NyZXBhbmNpZXMiLCBzYS5KU09OKCksIG51bGxhYmxlPUZhbHNlKSwKICAgICAgICBzYS5Db2x
1bW4oImlucHV0c19oYXNoIiwgc2EuU3RyaW5nKDY0KSwgbnVsbGFibGU9RmFsc2UpLAogICAgICAgIC
pfYmUxX2NvbHVtbnMoKSwKICAgICAgICBzYS5DaGVja0NvbnN0cmFpbnQoIm91dGNvbWUgSU4gKCdjb
25zaXN0ZW50JywnZGlzY3JlcGFudCcpIiwKICAgICAgICAgICAgICAgICAgICAgICAgICAgbmFtZT0i
Y2tfdjJfcHJlY29uX291dGNvbWUiKSwKICAgICAgICBzYS5DaGVja0NvbnN0cmFpbnQoX0RBVEFfQ0x
BU1NfQ0hFQ0ssCiAgICAgICAgICAgICAgICAgICAgICAgICAgIG5hbWU9ImNrX3YyX3ByZWNvbl9kYX
RhX2NsYXNzIiksCiAgICApCiAgICBvcC5jcmVhdGVfaW5kZXgoIml4X3YyX3ByZWNvbl9hY2NvdW50I
iwgInYyX3BhcGVyX3JlY29uY2lsaWF0aW9uIiwKICAgICAgICAgICAgICAgICAgICBbImFjY291bnRf
aWQiXSkKCiAgICAjIC0tLSBTZWVkcyAocmV2aXNpb24tbG9jYWwgbGl0ZXJhbHM7IERFTC0wMDQgbGF
3KSAtLS0tLS0tLS0tLS0tLS0tLS0tLS0KICAgIHBlcm1pc3Npb25fdGFibGUgPSBzYS50YWJsZSgKIC
AgICAgICAidjJfcGVybWlzc2lvbiIsCiAgICAgICAgc2EuY29sdW1uKCJpZCIsIHNhLlN0cmluZyksI
HNhLmNvbHVtbigicm9sZSIsIHNhLlN0cmluZyksCiAgICAgICAgc2EuY29sdW1uKCJwZXJtaXNzaW9u
Iiwgc2EuU3RyaW5nKSwgc2EuY29sdW1uKCJzYWwiLCBzYS5TdHJpbmcpLAogICAgICAgIHNhLmNvbHV
tbigiY3JlYXRlZF9hdCIsIHNhLkRhdGVUaW1lKHRpbWV6b25lPVRydWUpKSwKICAgICkKICAgIGV4aX
N0aW5nID0gewogICAgICAgIChyb3dbMF0sIHJvd1sxXSkKICAgICAgICBmb3Igcm93IGluIGJpbmQuZ
XhlY3V0ZSgKICAgICAgICAgICAgc2EudGV4dCgiU0VMRUNUIHJvbGUsIHBlcm1pc3Npb24gRlJPTSB2
Ml9wZXJtaXNzaW9uIikpCiAgICB9CiAgICBmb3Igcm9sZSwgcGVybWlzc2lvbiwgc2FsIGluIF9QRVJ
NSVNTSU9OUzoKICAgICAgICBpZiAocm9sZSwgcGVybWlzc2lvbikgbm90IGluIGV4aXN0aW5nOgogIC
AgICAgICAgICBvcC5leGVjdXRlKHBlcm1pc3Npb25fdGFibGUuaW5zZXJ0KCkudmFsdWVzKAogICAgI
CAgICAgICAgICAgaWQ9c3RyKHV1aWQ0KCkpLCByb2xlPXJvbGUsIHBlcm1pc3Npb249cGVybWlzc2lv
biwKICAgICAgICAgICAgICAgIHNhbD1zYWwsIGNyZWF0ZWRfYXQ9bm93LAogICAgICAgICAgICApKQo
KICAgIGNvbXB2ZXIgPSBzYS50YWJsZSgKICAgICAgICAidjJfY29tcHV0YXRpb25fdmVyc2lvbiIsCi
AgICAgICAgc2EuY29sdW1uKCJpZCIsIHNhLlN0cmluZyksIHNhLmNvbHVtbigiY29tcG9uZW50Iiwgc
2EuU3RyaW5nKSwKICAgICAgICBzYS5jb2x1bW4oInZlcnNpb24iLCBzYS5TdHJpbmcpLCBzYS5jb2x1
bW4oInNvdXJjZV9oYXNoIiwgc2EuU3RyaW5nKSwKICAgICAgICBzYS5jb2x1bW4oImV2aWRlbmNlX3J
lZiIsIHNhLlN0cmluZyksCiAgICAgICAgc2EuY29sdW1uKCJyZWdpc3RlcmVkX2F0Iiwgc2EuRGF0ZV
RpbWUodGltZXpvbmU9VHJ1ZSkpLAogICAgKQogICAgZm9yIGNvbXBvbmVudCwgdmVyc2lvbiwgZmlsZ
XMgaW4gKAogICAgICAgICgicGFwZXJfZXhlY3V0aW9uX3NpbXVsYXRvciIsICJweHMtMS4wLjAiLCBf
UFhTX0ZJTEVTKSwKICAgICAgICAoInBhcGVyX3Jpc2tfZ2F0ZXdheSIsICJwcmctMS4wLjAiLCBfUFJ
HX0ZJTEVTKSwKICAgICk6CiAgICAgICAgb3AuZXhlY3V0ZShjb21wdmVyLmluc2VydCgpLnZhbHVlcy
gKICAgICAgICAgICAgaWQ9c3RyKHV1aWQ0KCkpLCBjb21wb25lbnQ9Y29tcG9uZW50LCB2ZXJzaW9uP
XZlcnNpb24sCiAgICAgICAgICAgIHNvdXJjZV9oYXNoPV9yb2xsaW5nX2hhc2goZmlsZXMpLCBldmlk
ZW5jZV9yZWY9IkJPLVYyLUJFLTgtMDAxIiwKICAgICAgICAgICAgcmVnaXN0ZXJlZF9hdD1ub3csCiA
gICAgICAgKSkKCiAgICBfY3JlYXRlX3RyaWdnZXJzKGJpbmQpCiAgICBfdmVyaWZ5X3RyaWdnZXJzX3
ByZXNlbnQoYmluZCkKCgpkZWYgX3ZlcmlmeV90cmlnZ2Vyc19wcmVzZW50KGJpbmQpIC0+IE5vbmU6C
iAgICBuYW1lcyA9IHR1cGxlKHRbMF0gZm9yIHQgaW4gX1RSSUdHRVJTKQogICAgcGxhY2Vob2xkZXJz
ID0gIiwiLmpvaW4oZiIne259JyIgZm9yIG4gaW4gbmFtZXMpCiAgICBpZiBiaW5kLmRpYWxlY3QubmF
tZSA9PSAic3FsaXRlIjoKICAgICAgICBjb3VudCA9IGJpbmQuZXhlY3V0ZShzYS50ZXh0KAogICAgIC
AgICAgICAiU0VMRUNUIENPVU5UKCopIEZST00gc3FsaXRlX21hc3RlciBXSEVSRSB0eXBlPSd0cmlnZ
2VyJyIKICAgICAgICAgICAgZiIgQU5EIG5hbWUgSU4gKHtwbGFjZWhvbGRlcnN9KSIpKS5zY2FsYXJf
b25lKCkKICAgIGVsaWYgYmluZC5kaWFsZWN0Lm5hbWUgPT0gInBvc3RncmVzcWwiOgogICAgICAgIGN
vdW50ID0gYmluZC5leGVjdXRlKHNhLnRleHQoCiAgICAgICAgICAgIGYiU0VMRUNUIENPVU5UKCopIE
ZST00gcGdfdHJpZ2dlciBXSEVSRSB0Z25hbWUgSU4gKHtwbGFjZWhvbGRlcnN9KSIKICAgICAgICApK
S5zY2FsYXJfb25lKCkKICAgIGVsc2U6ICAjIHByYWdtYTogbm8gY292ZXIKICAgICAgICByZXR1cm4K
ICAgIGlmIGludChjb3VudCkgIT0gbGVuKG5hbWVzKToKICAgICAgICByYWlzZSBSdW50aW1lRXJyb3I
oCiAgICAgICAgICAgICJCRS04IDAwNDg6IGd1YXJkIHRyaWdnZXJzIE5PVCBwcmVzZW50IC0gbWFudW
FsIHJlY292ZXJ5IgogICAgICAgICAgICAiIHJlcXVpcmVkOyBkbyBub3QgdHJlYXQgdGhpcyBtaWdyY
XRpb24gYXMgYXBwbGllZCIpCgoKZGVmIGRvd25ncmFkZSgpIC0+IE5vbmU6CiAgICBiaW5kID0gb3Au
Z2V0X2JpbmQoKQogICAgX2Ryb3BfdHJpZ2dlcnMoYmluZCkKICAgIGZvciBfcm9sZSwgcGVybWlzc2l
vbiwgX3NhbCBpbiBfUEVSTUlTU0lPTlM6CiAgICAgICAgb3AuZXhlY3V0ZShzYS50ZXh0KAogICAgIC
AgICAgICAiREVMRVRFIEZST00gdjJfcGVybWlzc2lvbiBXSEVSRSBwZXJtaXNzaW9uID0gOnAiCiAgI
CAgICAgKS5iaW5kcGFyYW1zKHA9cGVybWlzc2lvbikpCiAgICBfZHJvcF9jb21wdmVyX2RlbGV0ZV9n
dWFyZChiaW5kKQogICAgZm9yIGNvbXBvbmVudCwgdmVyc2lvbiBpbiAoCiAgICAgICAgICAgICgicGF
wZXJfZXhlY3V0aW9uX3NpbXVsYXRvciIsICJweHMtMS4wLjAiKSwKICAgICAgICAgICAgKCJwYXBlcl
9yaXNrX2dhdGV3YXkiLCAicHJnLTEuMC4wIikpOgogICAgICAgIG9wLmV4ZWN1dGUoc2EudGV4dCgKI
CAgICAgICAgICAgIkRFTEVURSBGUk9NIHYyX2NvbXB1dGF0aW9uX3ZlcnNpb24iCiAgICAgICAgICAg
ICIgV0hFUkUgY29tcG9uZW50ID0gOmMgQU5EIHZlcnNpb24gPSA6diIKICAgICAgICApLmJpbmRwYXJ
hbXMoYz1jb21wb25lbnQsIHY9dmVyc2lvbikpCiAgICBfcmVjcmVhdGVfY29tcHZlcl9kZWxldGVfZ3
VhcmQoYmluZCkKICAgIGZvciBpbmRleCwgdGFibGUgaW4gKAogICAgICAgICgiaXhfdjJfcHJlY29uX
2FjY291bnQiLCAidjJfcGFwZXJfcmVjb25jaWxpYXRpb24iKSwKICAgICAgICAoIml4X3YyX3BiYWxf
YWNjb3VudCIsICJ2Ml9wYXBlcl9iYWxhbmNlX3NuYXBzaG90IiksCiAgICAgICAgKCJpeF92Ml9wcG9
zX2FjY291bnQiLCAidjJfcGFwZXJfcG9zaXRpb25fc25hcHNob3QiKSwKICAgICAgICAoIml4X3YyX3
BmaWxsX2ludGVudCIsICJ2Ml9wYXBlcl9maWxsIiksCiAgICAgICAgKCJpeF92Ml9wZXZlbnRfaW50Z
W50IiwgInYyX3BhcGVyX29yZGVyX2V2ZW50IiksCiAgICAgICAgKCJpeF92Ml9waW50ZW50X2FjY291
bnQiLCAidjJfcGFwZXJfb3JkZXJfaW50ZW50IiksCiAgICAgICAgKCJpeF92Ml9wYWNjdF9hY2NvdW5
0IiwgInYyX3BhcGVyX2FjY291bnQiKSwKICAgICk6CiAgICAgICAgb3AuZHJvcF9pbmRleChpbmRleC
wgdGFibGVfbmFtZT10YWJsZSkKICAgIGZvciB0YWJsZSBpbiAoInYyX3BhcGVyX3JlY29uY2lsaWF0a
W9uIiwgInYyX3BhcGVyX2JhbGFuY2Vfc25hcHNob3QiLAogICAgICAgICAgICAgICAgICAidjJfcGFw
ZXJfcG9zaXRpb25fc25hcHNob3QiLCAidjJfcGFwZXJfZmlsbCIsCiAgICAgICAgICAgICAgICAgICJ
2Ml9wYXBlcl9vcmRlcl9ldmVudCIsICJ2Ml9wYXBlcl9yaXNrX2RlY2lzaW9uIiwKICAgICAgICAgIC
AgICAgICAgInYyX3BhcGVyX29yZGVyX2ludGVudCIsICJ2Ml9wYXBlcl9hY2NvdW50Iik6CiAgICAgI
CAgb3AuZHJvcF90YWJsZSh0YWJsZSkK
'@
$LandPath = Join-Path $BackendRoot "alembic\versions\20260904_0048_v2_be8_paper_trading.py"
New-Item -ItemType Directory -Force -Path (Split-Path $LandPath) | Out-Null
if (Test-Path $LandPath) {
    $Cur = (Get-FileHash -Path $LandPath -Algorithm SHA256).Hash.ToLower()
    if ($Cur -eq "2cb83b3d102598523834b867aa780bb659df3366a8775c65cc0750740dc398c2") { Write-Evidence ("pre-landing witnessed (already pinned bytes): alembic\versions\20260904_0048_v2_be8_paper_trading.py") }
    else { throw ("STOP (A4 FOREIGN-STATE ADJUDICATION LAW): new-file target exists with foreign bytes: " + $LandPath + " sha " + $Cur + " . Nothing modified for this file; report to ITRGA.") }
} else {
    [IO.File]::WriteAllBytes($LandPath, (B64-Decode -B64Chunk $Falembic_versions_20260904_0048_v2_be8_paper_trading_py))
    $Cur = (Get-FileHash -Path $LandPath -Algorithm SHA256).Hash.ToLower()
    if ($Cur -ne "2cb83b3d102598523834b867aa780bb659df3366a8775c65cc0750740dc398c2") { throw ("FAIL: post-write hash drift on " + $LandPath) }
    Write-Evidence ("landed + verified: alembic\versions\20260904_0048_v2_be8_paper_trading.py")
}

# file: tests\test_v2_be8_simulator.py  (pin 129c3d32f059...)
$Ftests_test_v2_be8_simulator_py = @'
IiIiVjIgQkUtOCBzaW11bGF0b3IgKyBsZWRnZXIgZW5naW5lIHRlc3RzIOKAlCBCTy1WMi1CRS04LTA
wMSBULTYvVC0xMC9ULTExLgoKQU5ORVgtUCBoYW5kLWNvbXB1dGVkIHZhbHVlcyAoZG9jcy9ldmlkZW
5jZS9WMl9CRS04X0FOTkVYX1BfV09SS0VEX1NBTVBMRS5tZCkKYXNzZXJ0ZWQgYWdhaW5zdCBpbmRlc
GVuZGVudCB0ZXN0LWxvY2FsIGxpdGVyYWxzOyBkZXRlcm1pbmlzbSB4MzsgY29zdApwdXJpdHk7IHR5
cGVkIHNlYW07IGNvbnRlbnQgcmUtdmVyaWZpY2F0aW9uOyBtb25leSBsYXcuClNvY2tldCBndWFyZCB
vbiBldmVyeSB0ZXN0LgoiIiIKCmZyb20gX19mdXR1cmVfXyBpbXBvcnQgYW5ub3RhdGlvbnMKCmltcG
9ydCBqc29uCmltcG9ydCBzb2NrZXQKZnJvbSBkZWNpbWFsIGltcG9ydCBEZWNpbWFsCgppbXBvcnQgc
Hl0ZXN0Cgpmcm9tIGFwcC52Mi5wYXBlcl90cmFkaW5nLmNvbnRyYWN0cyBpbXBvcnQgKAogICAgQ09T
VF9VTklUU19WMSwKICAgIEZJTExfQ0xBU1NFUywKICAgIFBBUEVSX0RJU0NMQUlNRVIsCiAgICBQYXB
lck9yZGVySW50ZW50LAogICAgUGFwZXJSZWZ1c2VkLAopCmZyb20gYXBwLnYyLnBhcGVyX3RyYWRpbm
cubGVkZ2VyIGltcG9ydCAoCiAgICBkZXJpdmVfYmFsYW5jZSwKICAgIGRlcml2ZV9jYXNoLAogICAgZ
GVyaXZlX3Bvc2l0aW9ucywKICAgIGRlcml2ZV9yZWFsaXplZF9wbmwsCiAgICBwcmVzZW50YXRpb25f
cm91bmQsCiAgICByZWNvbmNpbGUsCikKZnJvbSBhcHAudjIucGFwZXJfdHJhZGluZy5zaW11bGF0b3I
gaW1wb3J0ICgKICAgIFNJTVVMQVRPUl9WRVJTSU9OLAogICAgYXBwbHlfY29zdHMsCiAgICBydW5fc2
ltdWxhdGlvbiwKICAgIHNuYXBzaG90X2NvbnRlbnRfaGFzaCwKKQoKCkBweXRlc3QuZml4dHVyZShhd
XRvdXNlPVRydWUpCmRlZiBfc29ja2V0X2d1YXJkKG1vbmtleXBhdGNoKToKICAgIGRlZiBfZGVueSgq
X2EsICoqX2spOgogICAgICAgIHJhaXNlIEFzc2VydGlvbkVycm9yKCJuZXR3b3JrIGF0dGVtcHQgZHV
yaW5nIEJFLTggdGVzdCIpCgogICAgbW9ua2V5cGF0Y2guc2V0YXR0cihzb2NrZXQsICJnZXRhZGRyaW
5mbyIsIF9kZW55KQogICAgbW9ua2V5cGF0Y2guc2V0YXR0cihzb2NrZXQsICJjcmVhdGVfY29ubmVjd
GlvbiIsIF9kZW55KQoKCiMgLS0tIEFOTkVYLVAgcGlucyAoaW5kZXBlbmRlbnQgbGl0ZXJhbHM7IHRo
ZSBkb2MgaXMgdGhlIGxhdykgLS0tLS0tLS0tLS0tLS0tLS0tLS0KCkFOTkVYX0NMT1NFUyA9IFsiMTA
wIiwgIjk5IiwgIjk3IiwgIjk2IiwgIjk5IiwgIjEwMiIsICIxMDQiLCAiMTAzIiwgIjEwMSIsCiAgIC
AgICAgICAgICAgICAiMTAwIl0KQU5ORVhfQ09TVFMgPSB7CiAgICAic3ByZWFkIjogeyJ2YWx1ZSI6I
CIwLjEwIiwgInVuaXQiOiAicHJpY2UiLCAiY2l0YXRpb24iOiAiYmFuZC1kZWNsYXJlZCJ9LAogICAg
ImNvbW1pc3Npb24iOiB7InZhbHVlIjogIjAuMDUiLCAidW5pdCI6ICJwcmljZSIsCiAgICAgICAgICA
gICAgICAgICAiY2l0YXRpb24iOiAiYmFuZC1kZWNsYXJlZCJ9LAogICAgInNsaXBwYWdlIjogeyJ2YW
x1ZSI6ICIwIiwgInVuaXQiOiAicHJpY2UiLCAiY2l0YXRpb24iOiAiYmFuZC1kZWNsYXJlZCJ9LAp9C
goKZGVmIF9iYXJzKGxpcXVpZGl0eTogc3RyID0gIjIiKSAtPiBsaXN0W2RpY3RdOgogICAgb3V0ID0g
W10KICAgIGZvciBpLCBjbG9zZSBpbiBlbnVtZXJhdGUoQU5ORVhfQ0xPU0VTKToKICAgICAgICBjID0
gRGVjaW1hbChjbG9zZSkKICAgICAgICBvdXQuYXBwZW5kKHsib3Blbl90aW1lIjogZiIyMDI2LTA5LT
AxVHtpOjAyZH06MDA6MDArMDA6MDAiLAogICAgICAgICAgICAgICAgICAgICJvcGVuIjogc3RyKGMpL
CAiaGlnaCI6IHN0cihjICsgMSksICJsb3ciOiBzdHIoYyAtIDEpLAogICAgICAgICAgICAgICAgICAg
ICJjbG9zZSI6IHN0cihjKSwgImxpcXVpZGl0eSI6IGxpcXVpZGl0eX0pCiAgICByZXR1cm4gb3V0Cgo
KZGVmIF9pbnRlbnQob3JkZXJfdHlwZTogc3RyID0gImxpbWl0IiwgcXVhbnRpdHk6IHN0ciA9ICI1Ii
wKICAgICAgICAgICAgbGltaXRfcHJpY2U6IHN0ciB8IE5vbmUgPSAiOTcuNSIpIC0+IFBhcGVyT3JkZ
XJJbnRlbnQ6CiAgICByZXR1cm4gUGFwZXJPcmRlckludGVudCgKICAgICAgICBpbnRlbnRfaWQ9ImFu
bmV4LXAiLCBhY2NvdW50X2lkPSJhY2N0LTEiLAogICAgICAgIGluc3RydW1lbnRfaWQ9ImZvcmV4LmV
1cnVzZCIsIHNpZGU9ImJ1eSIsIG9yZGVyX3R5cGU9b3JkZXJfdHlwZSwKICAgICAgICBxdWFudGl0eT
1EZWNpbWFsKHF1YW50aXR5KSwKICAgICAgICBsaW1pdF9wcmljZT1EZWNpbWFsKGxpbWl0X3ByaWNlK
SBpZiBsaW1pdF9wcmljZSBlbHNlIE5vbmUsCiAgICAgICAgc25hcHNob3RfcmVmPSJzbmFwLWFubmV4
LXAiLCB3aW5kb3dfc3RhcnQ9IjIwMjYtMDktMDFUMDA6MDA6MDArMDA6MDAiLAogICAgICAgIHdpbmR
vd19lbmQ9IjIwMjYtMDktMDFUMTA6MDA6MDArMDA6MDAiLCBjb3N0X21vZGVsPUFOTkVYX0NPU1RTKQ
oKCmRlZiBfcnVuKGludGVudDogUGFwZXJPcmRlckludGVudCwgYmFyczogbGlzdFtkaWN0XSkgLT4gZ
GljdDoKICAgIHJldHVybiBydW5fc2ltdWxhdGlvbigKICAgICAgICBpbnRlbnQsIGJhcnMsCiAgICAg
ICAgc3RvcmVkX2NvbnRlbnRfaGFzaD1zbmFwc2hvdF9jb250ZW50X2hhc2goYmFycywgaW50ZW50LnN
uYXBzaG90X3JlZikpCgoKIyAtLS0gQU5ORVgtUCBDYXNlIEE6IGxpbWl0IGJ1eSBwYXJ0aWFsIC0tLS
0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLQoKCmRlZiB0ZXN0X2FubmV4X3BfY
2FzZV9hX2ZpbGxfY291bnRfYW5kX3ByaWNlcygpOgogICAgcmVzdWx0ID0gX3J1bihfaW50ZW50KCks
IF9iYXJzKCkpCiAgICBhc3NlcnQgbGVuKHJlc3VsdFsiZmlsbHMiXSkgPT0gMgogICAgZm9yIGYgaW4
gcmVzdWx0WyJmaWxscyJdOgogICAgICAgIGFzc2VydCBmWyJxdWFudGl0eSJdID09ICIyIgogICAgIC
AgIGFzc2VydCBmWyJyYXdfcHJpY2UiXSA9PSAiOTcuNSIKICAgICAgICBhc3NlcnQgZlsiZWZmZWN0a
XZlX3ByaWNlIl0gPT0gIjk3LjY1IiAgIyA5Ny41ICsgMC4xMCArIDAuMDUKCgpkZWYgdGVzdF9hbm5l
eF9wX2Nhc2VfYV9wYXJ0aWFsX2FuZF9yZW1haW5kZXIoKToKICAgIHJlc3VsdCA9IF9ydW4oX2ludGV
udCgpLCBfYmFycygpKQogICAgYXNzZXJ0IHJlc3VsdFsib3V0Y29tZSJdID09ICJwYXJ0aWFsbHlfZm
lsbGVkIgogICAgYXNzZXJ0IERlY2ltYWwocmVzdWx0WyJ1bmZpbGxlZF9xdWFudGl0eSJdKSA9PSBEZ
WNpbWFsKCIxIikKCgpkZWYgdGVzdF9hbm5leF9wX2Nhc2VfYl9tYXJrZXRfZmlyc3RfY2xvc2UoKToK
ICAgIHJlc3VsdCA9IF9ydW4oX2ludGVudChvcmRlcl90eXBlPSJtYXJrZXQiLCBxdWFudGl0eT0iMSI
sCiAgICAgICAgICAgICAgICAgICAgICAgICAgbGltaXRfcHJpY2U9Tm9uZSksIF9iYXJzKCkpCiAgIC
Bhc3NlcnQgcmVzdWx0WyJvdXRjb21lIl0gPT0gImZpbGxlZCIKICAgIGFzc2VydCBsZW4ocmVzdWx0W
yJmaWxscyJdKSA9PSAxCiAgICBhc3NlcnQgcmVzdWx0WyJmaWxscyJdWzBdWyJyYXdfcHJpY2UiXSA9
PSAiMTAwIgogICAgYXNzZXJ0IHJlc3VsdFsiZmlsbHMiXVswXVsiZWZmZWN0aXZlX3ByaWNlIl0gPT0
gIjEwMC4xNSIKCgpkZWYgdGVzdF9hbm5leF9wX2xlZGdlcl9kZXJpdmF0aW9uX2V4YWN0KCk6CiAgIC
AiIiJBTk5FWC1QIMKnMiBhY2NvdW50IG51bWJlcnM6IGNhc2ggOTYwOS40MCwgZXF1aXR5IDEwMDA5L
jQwLAogICAgdW5yZWFsaXplZCA5LjQwLCBtYXJnaW4gMjAwLzk4MDkuNDAg4oCUIGFsbCBoYW5kLWNv
bXB1dGVkLiIiIgogICAgcmVzdWx0ID0gX3J1bihfaW50ZW50KCksIF9iYXJzKCkpCiAgICBmaWxscyA
9IFt7Imluc3RydW1lbnRfaWQiOiAiZm9yZXguZXVydXNkIiwgInNpZGUiOiAiYnV5IiwKICAgICAgIC
AgICAgICAicXVhbnRpdHkiOiBmWyJxdWFudGl0eSJdLAogICAgICAgICAgICAgICJlZmZlY3RpdmVfc
HJpY2UiOiBmWyJlZmZlY3RpdmVfcHJpY2UiXX0KICAgICAgICAgICAgIGZvciBmIGluIHJlc3VsdFsi
ZmlsbHMiXV0KICAgIGJhbGFuY2UgPSBkZXJpdmVfYmFsYW5jZSgKICAgICAgICBpbml0aWFsX2JhbGF
uY2U9RGVjaW1hbCgiMTAwMDAiKSwgZmlsbHM9ZmlsbHMsCiAgICAgICAgbWFya3M9eyJmb3JleC5ldX
J1c2QiOiBEZWNpbWFsKCIxMDAiKX0sCiAgICAgICAgbWFyZ2luX3BhcmFtcz17Im1hcmdpbl9yYXRlI
jogIjAuNSJ9KQogICAgYXNzZXJ0IERlY2ltYWwoYmFsYW5jZVsiY2FzaCJdKSA9PSBEZWNpbWFsKCI5
NjA5LjQwIikKICAgIGFzc2VydCBEZWNpbWFsKGJhbGFuY2VbImVxdWl0eSJdKSA9PSBEZWNpbWFsKCI
xMDAwOS40MCIpCiAgICBhc3NlcnQgRGVjaW1hbChiYWxhbmNlWyJ1bnJlYWxpemVkX3BubCJdKSA9PS
BEZWNpbWFsKCI5LjQwIikKICAgIGFzc2VydCBEZWNpbWFsKGJhbGFuY2VbInJlYWxpemVkX3BubCJdK
SA9PSBEZWNpbWFsKCIwIikKICAgIGFzc2VydCBEZWNpbWFsKGJhbGFuY2VbIm1hcmdpbl91c2VkIl0p
ID09IERlY2ltYWwoIjIwMCIpCiAgICBhc3NlcnQgRGVjaW1hbChiYWxhbmNlWyJtYXJnaW5fYXZhaWx
hYmxlIl0pID09IERlY2ltYWwoIjk4MDkuNDAiKQogICAgYXNzZXJ0IGJhbGFuY2VbInBvc2l0aW9ucy
JdID09IHsiZm9yZXguZXVydXNkIjogIjQifQoKCmRlZiB0ZXN0X2RldGVybWluaXN0aWNfeDNfYnl0Z
V9pZGVudGljYWwoKToKICAgICIiIlQtMTA6IHJlcGxheSBjb250cmFjdCB4MyAodGhlIDAwNDctZXJh
IEYtMiBsZXNzb24sIGRlc2lnbmVkIGluKS4iIiIKICAgIHMxID0ganNvbi5kdW1wcyhfcnVuKF9pbnR
lbnQoKSwgX2JhcnMoKSlbImZpbGxzIl0sIHNvcnRfa2V5cz1UcnVlKQogICAgczIgPSBqc29uLmR1bX
BzKF9ydW4oX2ludGVudCgpLCBfYmFycygpKVsiZmlsbHMiXSwgc29ydF9rZXlzPVRydWUpCiAgICBzM
yA9IGpzb24uZHVtcHMoX3J1bihfaW50ZW50KCksIF9iYXJzKCkpWyJmaWxscyJdLCBzb3J0X2tleXM9
VHJ1ZSkKICAgIGFzc2VydCBzMSA9PSBzMiA9PSBzMwoKCmRlZiB0ZXN0X2ZpbGxfY2xhc3Nfc2luZ2x
lX3ZhbHVlX29uX2V2ZXJ5X2ZpbGwoKToKICAgIHJlc3VsdCA9IF9ydW4oX2ludGVudCgpLCBfYmFycy
gpKQogICAgYXNzZXJ0IEZJTExfQ0xBU1NFUyA9PSAoInBhcGVyX3NpbXVsYXRlZCIsKQogICAgZm9yI
GYgaW4gcmVzdWx0WyJmaWxscyJdOgogICAgICAgIGFzc2VydCBmWyJmaWxsX2NsYXNzIl0gPT0gInBh
cGVyX3NpbXVsYXRlZCIKICAgIGFzc2VydCByZXN1bHRbImRpc2NsYWltZXIiXSA9PSBQQVBFUl9ESVN
DTEFJTUVSCgoKZGVmIHRlc3Rfc25hcHNob3RfY29udGVudF9taXNtYXRjaF90eXBlZF9yZWZ1c2FsKC
k6CiAgICAiIiJTNC4xL0ctNSBsYXc6IHRhbXBlciA9PiB0eXBlZCByZWZ1c2FsLCBuZXZlciBzaWxlb
nQgaW5jbHVzaW9uLiIiIgogICAgYmFycyA9IF9iYXJzKCkKICAgIGdvb2RfaGFzaCA9IHNuYXBzaG90
X2NvbnRlbnRfaGFzaChiYXJzLCAic25hcC1hbm5leC1wIikKICAgIGJhcnNbM11bImNsb3NlIl0gPSA
iNTAiICAjIHRhbXBlciBhZnRlciBoYXNoaW5nCiAgICB3aXRoIHB5dGVzdC5yYWlzZXMoUGFwZXJSZW
Z1c2VkKSBhcyBleGM6CiAgICAgICAgcnVuX3NpbXVsYXRpb24oX2ludGVudCgpLCBiYXJzLCBzdG9yZ
WRfY29udGVudF9oYXNoPWdvb2RfaGFzaCkKICAgIGFzc2VydCBleGMudmFsdWUucmVmdXNhbF9jbGFz
cyA9PSAicGFwZXIuc25hcHNob3QuY29udGVudF9taXNtYXRjaCIKCgpkZWYgdGVzdF91bnR5cGVkX3N
lYW1fcmVmdXNlZCgpOgogICAgIiIiUzYuMTogdGhlIHNlYW0gYWNjZXB0cyBQYXBlck9yZGVySW50ZW
50IE9OTFkuIiIiCiAgICB3aXRoIHB5dGVzdC5yYWlzZXMoUGFwZXJSZWZ1c2VkKSBhcyBleGM6CiAgI
CAgICAgcnVuX3NpbXVsYXRpb24oeyJzaWRlIjogImJ1eSJ9LCBfYmFycygpLCBzdG9yZWRfY29udGVu
dF9oYXNoPSJ4IikKICAgIGFzc2VydCBleGMudmFsdWUucmVmdXNhbF9jbGFzcyA9PSAicGFwZXIuc2V
hbS51bnR5cGVkIgoKCmRlZiB0ZXN0X2Nvc3RfYXBwbGljYXRpb25fcHVyZV9hbmRfc2lkZWQoKToKIC
AgIGJ1eSA9IGFwcGx5X2Nvc3RzKERlY2ltYWwoIjEwMCIpLCAiYnV5IiwgQU5ORVhfQ09TVFMpCiAgI
CBzZWxsID0gYXBwbHlfY29zdHMoRGVjaW1hbCgiMTAwIiksICJzZWxsIiwgQU5ORVhfQ09TVFMpCiAg
ICBhc3NlcnQgYnV5ID09IERlY2ltYWwoIjEwMC4xNSIpCiAgICBhc3NlcnQgc2VsbCA9PSBEZWNpbWF
sKCI5OS44NSIpCgoKZGVmIHRlc3RfY29zdF91bmtub3duX3VuaXRfdHlwZWQoKToKICAgICIiIkNSLV
YyLUJFLTctMDAxIHZvY2FidWxhcnkgbGF3IGNhcnJpZWQ6IHVua25vd24gdW5pdCByZWZ1c2VkIHR5c
GVkLiIiIgogICAgYmFkID0gZGljdChBTk5FWF9DT1NUUykKICAgIGJhZFsic3ByZWFkIl0gPSB7InZh
bHVlIjogIjAuMSIsICJ1bml0IjogImJvZ3VzIiwgImNpdGF0aW9uIjogIngifQogICAgd2l0aCBweXR
lc3QucmFpc2VzKFBhcGVyUmVmdXNlZCkgYXMgZXhjOgogICAgICAgIGFwcGx5X2Nvc3RzKERlY2ltYW
woIjEwMCIpLCAiYnV5IiwgYmFkKQogICAgYXNzZXJ0IGV4Yy52YWx1ZS5yZWZ1c2FsX2NsYXNzID09I
CJwYXBlci5jb3N0X3VuaXQudW5rbm93biIKICAgIGFzc2VydCBDT1NUX1VOSVRTX1YxID09ICgicHJp
Y2UiLCAiZnJhY3Rpb24iKQoKCmRlZiB0ZXN0X2V4cGlyZWRfd2hlbl9uZXZlcl90b3VjaGVkKCk6CiA
gICByZXN1bHQgPSBfcnVuKF9pbnRlbnQobGltaXRfcHJpY2U9IjUwIiksIF9iYXJzKCkpCiAgICBhc3
NlcnQgcmVzdWx0WyJvdXRjb21lIl0gPT0gImV4cGlyZWQiCiAgICBhc3NlcnQgcmVzdWx0WyJmaWxsc
yJdID09IFtdCgoKZGVmIHRlc3RfcmVhbGl6ZWRfcG5sX2F2ZXJhZ2VfY29zdCgpOgogICAgIiIiUzUv
QS0zOiBidXkgMiBAIDEwMCwgc2VsbCAxIEAgMTEwID0+IHJlYWxpemVkICsxMC4iIiIKICAgIGZpbGx
zID0gWwogICAgICAgIHsiaW5zdHJ1bWVudF9pZCI6ICJ4IiwgInNpZGUiOiAiYnV5IiwgInF1YW50aX
R5IjogIjIiLAogICAgICAgICAiZWZmZWN0aXZlX3ByaWNlIjogIjEwMCJ9LAogICAgICAgIHsiaW5zd
HJ1bWVudF9pZCI6ICJ4IiwgInNpZGUiOiAic2VsbCIsICJxdWFudGl0eSI6ICIxIiwKICAgICAgICAg
ImVmZmVjdGl2ZV9wcmljZSI6ICIxMTAifSwKICAgIF0KICAgIGFzc2VydCBkZXJpdmVfcmVhbGl6ZWR
fcG5sKGZpbGxzKSA9PSBEZWNpbWFsKCIxMCIpCiAgICBhc3NlcnQgZGVyaXZlX3Bvc2l0aW9ucyhmaW
xscykgPT0geyJ4IjogRGVjaW1hbCgiMSIpfQogICAgYXNzZXJ0IGRlcml2ZV9jYXNoKERlY2ltYWwoI
jEwMDAiKSwgZmlsbHMpID09IERlY2ltYWwoIjkxMCIpCgoKZGVmIHRlc3RfcmVjb25jaWxlX2NvbnRl
bnRfYmFzZWRfYW5kX2FsYXJtKCk6CiAgICAiIiJULTEyOiBQR0YtMDEyIGNvbnRlbnQgY29tcGFyaXN
vbjsgZGlzY3JlcGFudCB0eXBlZCwgbm90IGNvcnJlY3RlZC4iIiIKICAgIGJhbGFuY2UgPSB7InBvc2
l0aW9ucyI6IHsieCI6ICIxIn0sICJjYXNoIjogIjkxMCIsICJlcXVpdHkiOiAiMTAxMCIsCiAgICAgI
CAgICAgICAgICJtYXJnaW5fdXNlZCI6ICI1MCIsICJtYXJnaW5fYXZhaWxhYmxlIjogIjk2MCIsCiAg
ICAgICAgICAgICAgICJ1bnJlYWxpemVkX3BubCI6ICIwIiwgInJlYWxpemVkX3BubCI6ICIxMCJ9CiA
gICBvaywgaXRlbXMgPSByZWNvbmNpbGUoc25hcHNob3Q9YmFsYW5jZSwgcmVjb21wdXRlZD1kaWN0KG
JhbGFuY2UpKQogICAgYXNzZXJ0IChvaywgaXRlbXMpID09ICgiY29uc2lzdGVudCIsIFtdKQogICAgd
GFtcGVyZWQgPSBkaWN0KGJhbGFuY2UpCiAgICB0YW1wZXJlZFsiY2FzaCJdID0gIjk5OSIKICAgIG91
dGNvbWUsIGRpc2NyZXBhbmNpZXMgPSByZWNvbmNpbGUoc25hcHNob3Q9dGFtcGVyZWQsCiAgICAgICA
gICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIHJlY29tcHV0ZWQ9YmFsYW5jZSkKICAgIGFzc2
VydCBvdXRjb21lID09ICJkaXNjcmVwYW50IgogICAgYXNzZXJ0IGRpc2NyZXBhbmNpZXNbMF1bImZpZ
WxkIl0gPT0gImNhc2giCgoKZGVmIHRlc3RfbW9uZXlfbGF3X2RlY2ltYWxfYW5kX3ByZXNlbnRhdGlv
bl9yb3VuZGluZygpOgogICAgIiIiVC0xMTogVEVYVC1kZWNpbWFsIGludGVybmFsIHByZWNpc2lvbjs
gcm91bmRpbmcgcHJlc2VudGF0aW9uLW9ubHkuIiIiCiAgICB2ID0gRGVjaW1hbCgiOTYwOS40MDAwMD
AwIikKICAgIGFzc2VydCBwcmVzZW50YXRpb25fcm91bmQodikgPT0gIjk2MDkuNDAiCiAgICBhc3Nlc
nQgcHJlc2VudGF0aW9uX3JvdW5kKERlY2ltYWwoIjAuMTI1IikpID09ICIwLjEyIiAgIyBoYWxmLWV2
ZW4KICAgIGFzc2VydCBzdHIoRGVjaW1hbCgiOTcuNSIpICsgRGVjaW1hbCgiMC4xNSIpKSA9PSAiOTc
uNjUiICAjIG5vIGZsb2F0IGRyaWZ0CgoKZGVmIHRlc3Rfc2ltdWxhdG9yX3ZlcnNpb25fcGlubmVkKC
k6CiAgICBhc3NlcnQgU0lNVUxBVE9SX1ZFUlNJT04gPT0gInB4cy0xLjAuMCIKICAgIHJlc3VsdCA9I
F9ydW4oX2ludGVudChvcmRlcl90eXBlPSJtYXJrZXQiLCBxdWFudGl0eT0iMSIsCiAgICAgICAgICAg
ICAgICAgICAgICAgICAgbGltaXRfcHJpY2U9Tm9uZSksIF9iYXJzKCkpCiAgICBhc3NlcnQgcmVzdWx
0WyJlbmdpbmVfdmVyc2lvbnMiXVsicGFwZXJfZXhlY3V0aW9uX3NpbXVsYXRvciJdID09ICJweHMtMS
4wLjAiCiAgICBhc3NlcnQgcmVzdWx0WyJlbmdpbmVfdmVyc2lvbnMiXVsicGFwZXJfcmlza19nYXRld
2F5Il0gPT0gInByZy0xLjAuMCIKICAgIGFzc2VydCBsZW4ocmVzdWx0WyJlbmdpbmVfdmVyc2lvbnNf
aGFzaCJdKSA9PSA2NAo=
'@
$LandPath = Join-Path $BackendRoot "tests\test_v2_be8_simulator.py"
New-Item -ItemType Directory -Force -Path (Split-Path $LandPath) | Out-Null
if (Test-Path $LandPath) {
    $Cur = (Get-FileHash -Path $LandPath -Algorithm SHA256).Hash.ToLower()
    if ($Cur -eq "129c3d32f05945da5e55c33b6f020c3d4bebb8227d8baca07de3c47da2ae7f61") { Write-Evidence ("pre-landing witnessed (already pinned bytes): tests\test_v2_be8_simulator.py") }
    else { throw ("STOP (A4 FOREIGN-STATE ADJUDICATION LAW): new-file target exists with foreign bytes: " + $LandPath + " sha " + $Cur + " . Nothing modified for this file; report to ITRGA.") }
} else {
    [IO.File]::WriteAllBytes($LandPath, (B64-Decode -B64Chunk $Ftests_test_v2_be8_simulator_py))
    $Cur = (Get-FileHash -Path $LandPath -Algorithm SHA256).Hash.ToLower()
    if ($Cur -ne "129c3d32f05945da5e55c33b6f020c3d4bebb8227d8baca07de3c47da2ae7f61") { throw ("FAIL: post-write hash drift on " + $LandPath) }
    Write-Evidence ("landed + verified: tests\test_v2_be8_simulator.py")
}

# file: tests\test_v2_be8_migration.py  (pin bd3227587bd9...)
$Ftests_test_v2_be8_migration_py = @'
IiIiVjIgQkUtOCBtaWdyYXRpb24gdGVzdHMg4oCUIEJPLVYyLUJFLTgtMDAxIFQtNy9ULTEzL1QtMTQ
vVC0xNS4KCjAwNDggb24gZGVkaWNhdGVkIFNRTGl0ZSBjaGFpbnMuIENvbnRlbnQtYmFzZWQgY29tcG
FyaXNvbnMgKFBHRi0wMTIpLgpQaW5zOiB0cmlnZ2VycyA0Mi0+NTg7IHBlcm1pc3Npb25zIDQ5LT41N
zsgY29tcHZlciA4LT4xMC4KIiIiCgpmcm9tIF9fZnV0dXJlX18gaW1wb3J0IGFubm90YXRpb25zCgpp
bXBvcnQgb3MKaW1wb3J0IHNxbGl0ZTMKaW1wb3J0IHN1YnByb2Nlc3MKaW1wb3J0IHN5cwpmcm9tIHB
hdGhsaWIgaW1wb3J0IFBhdGgKCmltcG9ydCBweXRlc3QKCkJBQ0tFTkRfRElSID0gUGF0aChfX2ZpbG
VfXykucmVzb2x2ZSgpLnBhcmVudHNbMV0KVFJBTlNfQVVUSE9SSVRZID0gIkJPLVYyLUJFLTMtUDItV
FJBTlMtMDAxIgpSRVZfMDA0NyA9ICIyMDI2MDkwM18wMDQ3IgpSRVZfMDA0OCA9ICIyMDI2MDkwNF8w
MDQ4IgoKVFJJR0dFUlNfMDA0OCA9IHsKICAgICJ2Ml9wYXBlcl9hY2NvdW50X2ltbXV0YWJsZV91cGR
hdGUiOgogICAgICAgICJWMiBwYXBlciBhY2NvdW50cyBhcmUgaW1tdXRhYmxlOyBVUERBVEUgcHJvaG
liaXRlZCIsCiAgICAidjJfcGFwZXJfYWNjb3VudF9pbW11dGFibGVfZGVsZXRlIjoKICAgICAgICAiV
jIgcGFwZXIgYWNjb3VudHMgYXJlIGltbXV0YWJsZTsgREVMRVRFIHByb2hpYml0ZWQiLAogICAgInYy
X3BhcGVyX29yZGVyX2ludGVudF9pbW11dGFibGVfdXBkYXRlIjoKICAgICAgICAiVjIgcGFwZXIgb3J
kZXIgaW50ZW50cyBhcmUgaW1tdXRhYmxlOyBVUERBVEUgcHJvaGliaXRlZCIsCiAgICAidjJfcGFwZX
Jfb3JkZXJfaW50ZW50X2ltbXV0YWJsZV9kZWxldGUiOgogICAgICAgICJWMiBwYXBlciBvcmRlciBpb
nRlbnRzIGFyZSBpbW11dGFibGU7IERFTEVURSBwcm9oaWJpdGVkIiwKICAgICJ2Ml9wYXBlcl9yaXNr
X2RlY2lzaW9uX2ltbXV0YWJsZV91cGRhdGUiOgogICAgICAgICJWMiBwYXBlciByaXNrIGRlY2lzaW9
ucyBhcmUgaW1tdXRhYmxlOyBVUERBVEUgcHJvaGliaXRlZCIsCiAgICAidjJfcGFwZXJfcmlza19kZW
Npc2lvbl9pbW11dGFibGVfZGVsZXRlIjoKICAgICAgICAiVjIgcGFwZXIgcmlzayBkZWNpc2lvbnMgY
XJlIGltbXV0YWJsZTsgREVMRVRFIHByb2hpYml0ZWQiLAogICAgInYyX3BhcGVyX29yZGVyX2V2ZW50
X2ltbXV0YWJsZV91cGRhdGUiOgogICAgICAgICJWMiBwYXBlciBvcmRlciBldmVudHMgYXJlIGltbXV
0YWJsZTsgVVBEQVRFIHByb2hpYml0ZWQiLAogICAgInYyX3BhcGVyX29yZGVyX2V2ZW50X2ltbXV0YW
JsZV9kZWxldGUiOgogICAgICAgICJWMiBwYXBlciBvcmRlciBldmVudHMgYXJlIGltbXV0YWJsZTsgR
EVMRVRFIHByb2hpYml0ZWQiLAogICAgInYyX3BhcGVyX2ZpbGxfaW1tdXRhYmxlX3VwZGF0ZSI6CiAg
ICAgICAgIlYyIHBhcGVyIGZpbGxzIGFyZSBpbW11dGFibGU7IFVQREFURSBwcm9oaWJpdGVkIiwKICA
gICJ2Ml9wYXBlcl9maWxsX2ltbXV0YWJsZV9kZWxldGUiOgogICAgICAgICJWMiBwYXBlciBmaWxscy
BhcmUgaW1tdXRhYmxlOyBERUxFVEUgcHJvaGliaXRlZCIsCiAgICAidjJfcGFwZXJfcG9zaXRpb25fc
25hcHNob3RfaW1tdXRhYmxlX3VwZGF0ZSI6CiAgICAgICAgIlYyIHBhcGVyIHBvc2l0aW9uIHNuYXBz
aG90cyBhcmUgaW1tdXRhYmxlOyBVUERBVEUgcHJvaGliaXRlZCIsCiAgICAidjJfcGFwZXJfcG9zaXR
pb25fc25hcHNob3RfaW1tdXRhYmxlX2RlbGV0ZSI6CiAgICAgICAgIlYyIHBhcGVyIHBvc2l0aW9uIH
NuYXBzaG90cyBhcmUgaW1tdXRhYmxlOyBERUxFVEUgcHJvaGliaXRlZCIsCiAgICAidjJfcGFwZXJfY
mFsYW5jZV9zbmFwc2hvdF9pbW11dGFibGVfdXBkYXRlIjoKICAgICAgICAiVjIgcGFwZXIgYmFsYW5j
ZSBzbmFwc2hvdHMgYXJlIGltbXV0YWJsZTsgVVBEQVRFIHByb2hpYml0ZWQiLAogICAgInYyX3BhcGV
yX2JhbGFuY2Vfc25hcHNob3RfaW1tdXRhYmxlX2RlbGV0ZSI6CiAgICAgICAgIlYyIHBhcGVyIGJhbG
FuY2Ugc25hcHNob3RzIGFyZSBpbW11dGFibGU7IERFTEVURSBwcm9oaWJpdGVkIiwKICAgICJ2Ml9wY
XBlcl9yZWNvbmNpbGlhdGlvbl9pbW11dGFibGVfdXBkYXRlIjoKICAgICAgICAiVjIgcGFwZXIgcmVj
b25jaWxpYXRpb25zIGFyZSBpbW11dGFibGU7IFVQREFURSBwcm9oaWJpdGVkIiwKICAgICJ2Ml9wYXB
lcl9yZWNvbmNpbGlhdGlvbl9pbW11dGFibGVfZGVsZXRlIjoKICAgICAgICAiVjIgcGFwZXIgcmVjb2
5jaWxpYXRpb25zIGFyZSBpbW11dGFibGU7IERFTEVURSBwcm9oaWJpdGVkIiwKfQoKUEVSTVNfMDA0O
CA9IHsKICAgICgiYWRtaW4iLCAidjIucGFwZXIuYWNjb3VudHMucmVhZCIsICJTQUwtMiIpLAogICAg
KCJhZG1pbiIsICJ2Mi5wYXBlci5hY2NvdW50cy5tYW5hZ2UiLCAiU0FMLTMiKSwKICAgICgiYWRtaW4
iLCAidjIucGFwZXIub3JkZXJzLnJlYWQiLCAiU0FMLTIiKSwKICAgICgiYWRtaW4iLCAidjIucGFwZX
Iub3JkZXJzLnBsYWNlIiwgIlNBTC0zIiksCiAgICAoImFkbWluIiwgInYyLnBhcGVyLm9yZGVycy5jY
W5jZWwiLCAiU0FMLTMiKSwKICAgICgiYWRtaW4iLCAidjIucGFwZXIub3JkZXJzLmNvbmZpcm0iLCAi
U0FMLTMiKSwKICAgICgiYWRtaW4iLCAidjIucGFwZXIuZmlsbHMucmVhZCIsICJTQUwtMiIpLAogICA
gKCJhZG1pbiIsICJ2Mi5wYXBlci5yaXNrLnJlYWQiLCAiU0FMLTIiKSwKfQoKUEFQRVJfVEFCTEVTID
0gKAogICAgInYyX3BhcGVyX2FjY291bnQiLCAidjJfcGFwZXJfb3JkZXJfaW50ZW50IiwgInYyX3Bhc
GVyX3Jpc2tfZGVjaXNpb24iLAogICAgInYyX3BhcGVyX29yZGVyX2V2ZW50IiwgInYyX3BhcGVyX2Zp
bGwiLCAidjJfcGFwZXJfcG9zaXRpb25fc25hcHNob3QiLAogICAgInYyX3BhcGVyX2JhbGFuY2Vfc25
hcHNob3QiLCAidjJfcGFwZXJfcmVjb25jaWxpYXRpb24iLAopCgpCRTEgPSAiJ3NpbXVsYXRlZCcsJ1
BBUEVSJywndCcsTlVMTCwnMjAyNi0wOS0wNCAwMDowMDowMCswMDowMCciCgoKZGVmIF9hbGVtYmljK
GFyZ3M6IGxpc3Rbc3RyXSwgZGJfdXJsOiBzdHIpIC0+IHN1YnByb2Nlc3MuQ29tcGxldGVkUHJvY2Vz
c1tzdHJdOgogICAgZW52ID0gZGljdChvcy5lbnZpcm9uKQogICAgZW52WyJBWElPTV9EQVRBQkFTRV9
VUkwiXSA9IGRiX3VybAogICAgZW52LnNldGRlZmF1bHQoIkFYSU9NX0VOVklST05NRU5UIiwgInRlc3
RpbmciKQogICAgZW52LnNldGRlZmF1bHQoIkFYSU9NX0FMTE9XX0lOU0VDVVJFX0RFViIsICJ0cnVlI
ikKICAgIGVudi5zZXRkZWZhdWx0KCJBWElPTV9KV1RfU0VDUkVUX0tFWSIsCiAgICAgICAgICAgICAg
ICAgICAidGVzdC1zZWNyZXQta2V5LWF0LWxlYXN0LTMyLWNoYXJzLWxvbmchISIpCiAgICBlbnZbIkF
YSU9NX1YyX01PREUiXSA9ICJSRVNFQVJDSCIgICMgMDA0MiBnYXRlIHByZWNvbmRpdGlvbiAoUC03KQ
ogICAgZW52WyJBWElPTV9URF9UUkFOU0lUSU9OX0FVVEhPUklUWV9SRUYiXSA9IFRSQU5TX0FVVEhPU
klUWQogICAgcmV0dXJuIHN1YnByb2Nlc3MucnVuKAogICAgICAgIFtzeXMuZXhlY3V0YWJsZSwgIi1t
IiwgImFsZW1iaWMiLCAqYXJnc10sCiAgICAgICAgY3dkPUJBQ0tFTkRfRElSLCBlbnY9ZW52LCBjYXB
0dXJlX291dHB1dD1UcnVlLCB0ZXh0PVRydWUsIHRpbWVvdXQ9NjAwKQoKCmRlZiBfZGIodG1wX3BhdG
g6IFBhdGgsIHJldjogc3RyKSAtPiB0dXBsZVtQYXRoLCBzdHJdOgogICAgZGJfZmlsZSA9IHRtcF9wY
XRoIC8gImJlOC5kYiIKICAgIGRiX3VybCA9IGYic3FsaXRlK2Fpb3NxbGl0ZTovLy97ZGJfZmlsZX0i
CiAgICByZXN1bHQgPSBfYWxlbWJpYyhbInVwZ3JhZGUiLCByZXZdLCBkYl91cmwpCiAgICBhc3NlcnQ
gcmVzdWx0LnJldHVybmNvZGUgPT0gMCwgcmVzdWx0LnN0ZGVycgogICAgcmV0dXJuIGRiX2ZpbGUsIG
RiX3VybAoKCmRlZiBfcShkYl9maWxlOiBQYXRoLCBzcWw6IHN0cik6CiAgICBjb25uID0gc3FsaXRlM
y5jb25uZWN0KGRiX2ZpbGUpCiAgICB0cnk6CiAgICAgICAgcmV0dXJuIGNvbm4uZXhlY3V0ZShzcWwp
LmZldGNoYWxsKCkKICAgIGZpbmFsbHk6CiAgICAgICAgY29ubi5jbG9zZSgpCgoKZGVmIF92Ml90cml
nZ2VycyhkYl9maWxlOiBQYXRoKSAtPiBzZXRbc3RyXToKICAgIHJldHVybiB7clswXSBmb3IgciBpbi
BfcSgKICAgICAgICBkYl9maWxlLAogICAgICAgICJTRUxFQ1QgbmFtZSBGUk9NIHNxbGl0ZV9tYXN0Z
XIgV0hFUkUgdHlwZT0ndHJpZ2dlciciCiAgICAgICAgIiBBTkQgbmFtZSBMSUtFICd2Ml8lJyIpfQoK
CiMgLS0tIFQtMTM6IGNoYWluICsgY2Vuc3VzZXMgLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0
tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0KCgpkZWYgdGVzdF8wMDQ4X3RhYmxlc19hbmRfY29sdW1ucy
h0bXBfcGF0aDogUGF0aCkgLT4gTm9uZToKICAgIGRiX2ZpbGUsIF8gPSBfZGIodG1wX3BhdGgsIFJFV
l8wMDQ4KQogICAgdGFibGVzID0ge3JbMF0gZm9yIHIgaW4gX3EoCiAgICAgICAgZGJfZmlsZSwgIlNF
TEVDVCBuYW1lIEZST00gc3FsaXRlX21hc3RlciBXSEVSRSB0eXBlPSd0YWJsZSciKX0KICAgIGZvciB
0IGluIFBBUEVSX1RBQkxFUzoKICAgICAgICBhc3NlcnQgdCBpbiB0YWJsZXMKICAgIGludGVudF9jb2
xzID0gW3JbMV0gZm9yIHIgaW4gX3EoCiAgICAgICAgZGJfZmlsZSwgIlBSQUdNQSB0YWJsZV9pbmZvK
HYyX3BhcGVyX29yZGVyX2ludGVudCkiKV0KICAgICMgTjM6IGV2ZXJ5IG9yZGVyIGNhcnJpZXMgdGhl
IGZ1bGwgbGF3LgogICAgZm9yIGMgaW4gKCJtb2RlIiwgImFjdG9yX2lkIiwgImFjY291bnRfaWQiLCA
iY29ycmVsYXRpb25faWQiLAogICAgICAgICAgICAgICJpZGVtcG90ZW5jeV9rZXkiLCAic25hcHNob3
RfcmVmIiwgInRpbWVfYmFzaXMiKToKICAgICAgICBhc3NlcnQgYyBpbiBpbnRlbnRfY29scwogICAgZ
GVjaXNpb25fY29scyA9IFtyWzFdIGZvciByIGluIF9xKAogICAgICAgIGRiX2ZpbGUsICJQUkFHTUEg
dGFibGVfaW5mbyh2Ml9wYXBlcl9yaXNrX2RlY2lzaW9uKSIpXQogICAgZm9yIGMgaW4gKCJkZWNpc2l
vbiIsICJldmFsdWF0ZWRfbGltaXRzIiwgInJpc2tfY29uZmlnX3ZlcnNpb24iLAogICAgICAgICAgIC
AgICJjb25maXJtYXRpb25fcmVmIik6CiAgICAgICAgYXNzZXJ0IGMgaW4gZGVjaXNpb25fY29scwoKC
mRlZiB0ZXN0XzAwNDhfc2VlZHNfYW5kX3RvdGFscyh0bXBfcGF0aDogUGF0aCkgLT4gTm9uZToKICAg
IGRiX2ZpbGUsIF8gPSBfZGIodG1wX3BhdGgsIFJFVl8wMDQ4KQogICAgdHJpZ3MgPSBfdjJfdHJpZ2d
lcnMoZGJfZmlsZSkKICAgIGFzc2VydCBsZW4odHJpZ3MpID09IDU4ICAgICAgICAgICMgVC0xMzogND
IgKyAxNgogICAgYXNzZXJ0IHNldChUUklHR0VSU18wMDQ4KSA8PSB0cmlncwogICAgcGVybXMgPSBfc
ShkYl9maWxlLCAiU0VMRUNUIHJvbGUsIHBlcm1pc3Npb24sIHNhbCBGUk9NIHYyX3Blcm1pc3Npb24i
KQogICAgYXNzZXJ0IGxlbihwZXJtcykgPT0gNTcgICAgICAgICAgIyBULTEzOiA0OSArIDgKICAgIGF
zc2VydCBsZW4oeyhyLCBwKSBmb3IgciwgcCwgXyBpbiBwZXJtc30pID09IDU3CiAgICBhc3NlcnQgUE
VSTVNfMDA0OCA8PSB7dHVwbGUocikgZm9yIHIgaW4gcGVybXN9CiAgICBjb21wdmVyID0gX3EoZGJfZ
mlsZSwKICAgICAgICAgICAgICAgICAiU0VMRUNUIGNvbXBvbmVudCwgdmVyc2lvbiwgbGVuZ3RoKHNv
dXJjZV9oYXNoKSIKICAgICAgICAgICAgICAgICAiIEZST00gdjJfY29tcHV0YXRpb25fdmVyc2lvbiI
pCiAgICBhc3NlcnQgbGVuKGNvbXB2ZXIpID09IDEwICAgICAgICAjIFQtMTM6IDggKyAyCiAgICBhc3
NlcnQgKCJwYXBlcl9leGVjdXRpb25fc2ltdWxhdG9yIiwgInB4cy0xLjAuMCIsIDY0KSBpbiBjb21wd
mVyCiAgICBhc3NlcnQgKCJwYXBlcl9yaXNrX2dhdGV3YXkiLCAicHJnLTEuMC4wIiwgNjQpIGluIGNv
bXB2ZXIKICAgICMgUlBFL1JKRSB1bmNoYW5nZWQgbWVtYmVycyAoYXBwZW5kLW9ubHkgbGF3KQogICA
gYXNzZXJ0ICgicmVwbGF5X2VuZ2luZSIsICJycGUtMS4wLjAiLCA2NCkgaW4gY29tcHZlcgogICAgYX
NzZXJ0ICgicmVzZWFyY2hfam9iX2VuZ2luZSIsICJyamUtMS4wLjAiLCA2NCkgaW4gY29tcHZlcgoKC
mRlZiB0ZXN0XzAwNDhfZmlsbF9jbGFzc19zY2hlbWFfaW1wb3NzaWJsZSh0bXBfcGF0aDogUGF0aCkg
LT4gTm9uZToKICAgICIiIlQtNi9ONDogYW55IGZpbGxfY2xhc3Mgb3RoZXIgdGhhbiBwYXBlcl9zaW1
1bGF0ZWQgcmVmdXNlZCBhdCBEQi4iIiIKICAgIGRiX2ZpbGUsIF8gPSBfZGIodG1wX3BhdGgsIFJFVl
8wMDQ4KQogICAgY29ubiA9IHNxbGl0ZTMuY29ubmVjdChkYl9maWxlKQogICAgdHJ5OgogICAgICAgI
GZvciBiYW5uZWQgaW4gKCJicm9rZXJfY29uZmlybWVkIiwgImxpdmUiLCAicGFwZXIiLCAiY29uZmly
bWVkIik6CiAgICAgICAgICAgIHdpdGggcHl0ZXN0LnJhaXNlcyhzcWxpdGUzLkludGVncml0eUVycm9
yKToKICAgICAgICAgICAgICAgIGNvbm4uZXhlY3V0ZSgKICAgICAgICAgICAgICAgICAgICAiSU5TRV
JUIElOVE8gdjJfcGFwZXJfZmlsbCAoaWQsIGZpbGxfaWQsIGludGVudF9pZCwiCiAgICAgICAgICAgI
CAgICAgICAgIiBmaWxsX2luZGV4LCBxdWFudGl0eSwgcmF3X3ByaWNlLCBlZmZlY3RpdmVfcHJpY2Us
IgogICAgICAgICAgICAgICAgICAgICIgY29zdF9tb2RlbF9yZWYsIGZpbGxfY2xhc3MsIHNpbXVsYXR
vcl92ZXJzaW9uLCIKICAgICAgICAgICAgICAgICAgICAiIHNuYXBzaG90X3JlZiwgdGltZV9iYXNpcy
wgZGF0YV9jbGFzcywgbW9kZSwiCiAgICAgICAgICAgICAgICAgICAgIiBvcGVyYXRvcl9pZCwgY29yc
mVsYXRpb25faWQsIGNyZWF0ZWRfYXQpIgogICAgICAgICAgICAgICAgICAgIGYiIFZBTFVFUyAoJ2Yt
e2Jhbm5lZH0nLCdmaWQte2Jhbm5lZH0nLCdpJywwLCcxJywnMTAwJywiCiAgICAgICAgICAgICAgICA
gICAgZiIgJzEwMCcsJ3t7fX0nLCd7YmFubmVkfScsJ3B4cy0xLjAuMCcsJ3MnLCd7e319Jyx7QkUxfS
kiKQogICAgICAgIGNvbm4uZXhlY3V0ZSgKICAgICAgICAgICAgIklOU0VSVCBJTlRPIHYyX3BhcGVyX
2ZpbGwgKGlkLCBmaWxsX2lkLCBpbnRlbnRfaWQsIGZpbGxfaW5kZXgsIgogICAgICAgICAgICAiIHF1
YW50aXR5LCByYXdfcHJpY2UsIGVmZmVjdGl2ZV9wcmljZSwgY29zdF9tb2RlbF9yZWYsIgogICAgICA
gICAgICAiIGZpbGxfY2xhc3MsIHNpbXVsYXRvcl92ZXJzaW9uLCBzbmFwc2hvdF9yZWYsIHRpbWVfYm
FzaXMsIgogICAgICAgICAgICAiIGRhdGFfY2xhc3MsIG1vZGUsIG9wZXJhdG9yX2lkLCBjb3JyZWxhd
Glvbl9pZCwgY3JlYXRlZF9hdCkiCiAgICAgICAgICAgIGYiIFZBTFVFUyAoJ2Ytb2snLCdmaWQtb2sn
LCdpJywwLCcxJywnMTAwJywnMTAwJywne3t9fScsIgogICAgICAgICAgICBmIiAncGFwZXJfc2ltdWx
hdGVkJywncHhzLTEuMC4wJywncycsJ3t7fX0nLHtCRTF9KSIpCiAgICAgICAgY29ubi5jb21taXQoKQ
ogICAgZmluYWxseToKICAgICAgICBjb25uLmNsb3NlKCkKCgpkZWYgdGVzdF8wMDQ4X2d1YXJkX21lc
3NhZ2VzX3ZlcmJhdGltKHRtcF9wYXRoOiBQYXRoKSAtPiBOb25lOgogICAgIiIiVC03OiBhbGwgMTYg
Z3VhcmQgbWVzc2FnZXMgYnl0ZS1leGFjdCB2cyBpbmRlcGVuZGVudCBsaXRlcmFscy4iIiIKICAgIGR
iX2ZpbGUsIF8gPSBfZGIodG1wX3BhdGgsIFJFVl8wMDQ4KQogICAgY29ubiA9IHNxbGl0ZTMuY29ubm
VjdChkYl9maWxlKQogICAgdHJ5OgogICAgICAgIGN1ciA9IGNvbm4uY3Vyc29yKCkKICAgICAgICBjd
XIuZXhlY3V0ZSgKICAgICAgICAgICAgIklOU0VSVCBJTlRPIHYyX3BhcGVyX2FjY291bnQgKGlkLCBh
Y2NvdW50X2lkLCByZWNvcmRfc2VxLCIKICAgICAgICAgICAgIiBuYW1lLCBiYXNlX2N1cnJlbmN5LCB
pbml0aWFsX2JhbGFuY2UsIG1hcmdpbl9wYXJhbXMsIgogICAgICAgICAgICAiIGxpZmVjeWNsZV9zdG
F0ZSwgY29uZmlybWF0aW9uX3JlZiwgZGF0YV9jbGFzcywgbW9kZSwiCiAgICAgICAgICAgICIgb3Blc
mF0b3JfaWQsIGNvcnJlbGF0aW9uX2lkLCBjcmVhdGVkX2F0KSIKICAgICAgICAgICAgZiIgVkFMVUVT
ICgnYTEnLCdhY2N0LTEnLDEsJ0EnLCdVU0QnLCcxMDAwMCcsJ3t7fX0nLCdhY3RpdmUnLCIKICAgICA
gICAgICAgZiIgJ3JlZi0xJyx7QkUxfSkiKQogICAgICAgIGN1ci5leGVjdXRlKAogICAgICAgICAgIC
AiSU5TRVJUIElOVE8gdjJfcGFwZXJfb3JkZXJfaW50ZW50IChpZCwgaW50ZW50X2lkLCBhY2NvdW50X
2lkLCIKICAgICAgICAgICAgIiBpbnN0cnVtZW50X2lkLCBzaWRlLCBvcmRlcl90eXBlLCBxdWFudGl0
eSwgbGltaXRfcHJpY2UsIgogICAgICAgICAgICAiIHRpbWVfaW5fZm9yY2UsIGlkZW1wb3RlbmN5X2t
leSwgc25hcHNob3RfcmVmLCB0aW1lX2Jhc2lzLCIKICAgICAgICAgICAgIiBjb25maXJtYXRpb25fcm
VmLCBhY3Rvcl9pZCwgZGF0YV9jbGFzcywgbW9kZSwgb3BlcmF0b3JfaWQsIgogICAgICAgICAgICAiI
GNvcnJlbGF0aW9uX2lkLCBjcmVhdGVkX2F0KSIKICAgICAgICAgICAgZiIgVkFMVUVTICgnaTEnLCdp
bnQtMScsJ2ExJywneCcsJ2J1eScsJ21hcmtldCcsJzEnLE5VTEwsIgogICAgICAgICAgICBmIiAncmV
wbGF5X3dpbmRvdycsJ2sxJywnczEnLCd7e319JyxOVUxMLCd0Jyx7QkUxfSkiKQogICAgICAgIGN1ci
5leGVjdXRlKAogICAgICAgICAgICAiSU5TRVJUIElOVE8gdjJfcGFwZXJfcmlza19kZWNpc2lvbiAoa
WQsIGludGVudF9pZCwgZGVjaXNpb24sIgogICAgICAgICAgICAiIGV2YWx1YXRlZF9saW1pdHMsIHJl
YXNvbnMsIHJpc2tfY29uZmlnX3ZlcnNpb24sIgogICAgICAgICAgICAiIGRlY2lkZWRfYXRfYmFzaXM
sIGNvbmZpcm1hdGlvbl9yZWYsIGRhdGFfY2xhc3MsIG1vZGUsIgogICAgICAgICAgICAiIG9wZXJhdG
9yX2lkLCBjb3JyZWxhdGlvbl9pZCwgY3JlYXRlZF9hdCkiCiAgICAgICAgICAgIGYiIFZBTFVFUyAoJ
2QxJywnaTEnLCdwYXNzJywne3t9fScsJ3t7fX0nLCdwcmMtMScsJ3t7fX0nLE5VTEwse0JFMX0pIikK
ICAgICAgICBjdXIuZXhlY3V0ZSgKICAgICAgICAgICAgIklOU0VSVCBJTlRPIHYyX3BhcGVyX29yZGV
yX2V2ZW50IChpZCwgaW50ZW50X2lkLCBldmVudF9pbmRleCwiCiAgICAgICAgICAgICIgZnJvbV9zdG
F0ZSwgdG9fc3RhdGUsIGV2ZW50X2NsYXNzLCBkZXRhaWxzLCBhY3Rvcl9pZCwiCiAgICAgICAgICAgI
CIgZGF0YV9jbGFzcywgbW9kZSwgb3BlcmF0b3JfaWQsIGNvcnJlbGF0aW9uX2lkLCBjcmVhdGVkX2F0
KSIKICAgICAgICAgICAgZiIgVkFMVUVTICgnZTEnLCdpMScsMCwnZHJhZnQnLCd2YWxpZGF0ZWQnLCd
vcmRlci52YWxpZGF0ZWQnLCIKICAgICAgICAgICAgZiIgJ3t7fX0nLCd0Jyx7QkUxfSkiKQogICAgIC
AgIGN1ci5leGVjdXRlKAogICAgICAgICAgICAiSU5TRVJUIElOVE8gdjJfcGFwZXJfZmlsbCAoaWQsI
GZpbGxfaWQsIGludGVudF9pZCwgZmlsbF9pbmRleCwiCiAgICAgICAgICAgICIgcXVhbnRpdHksIHJh
d19wcmljZSwgZWZmZWN0aXZlX3ByaWNlLCBjb3N0X21vZGVsX3JlZiwiCiAgICAgICAgICAgICIgZml
sbF9jbGFzcywgc2ltdWxhdG9yX3ZlcnNpb24sIHNuYXBzaG90X3JlZiwgdGltZV9iYXNpcywiCiAgIC
AgICAgICAgICIgZGF0YV9jbGFzcywgbW9kZSwgb3BlcmF0b3JfaWQsIGNvcnJlbGF0aW9uX2lkLCBjc
mVhdGVkX2F0KSIKICAgICAgICAgICAgZiIgVkFMVUVTICgnZjEnLCdmaWQtMScsJ2kxJywwLCcxJywn
MTAwJywnMTAwJywne3t9fScsIgogICAgICAgICAgICBmIiAncGFwZXJfc2ltdWxhdGVkJywncHhzLTE
uMC4wJywncycsJ3t7fX0nLHtCRTF9KSIpCiAgICAgICAgY3VyLmV4ZWN1dGUoCiAgICAgICAgICAgIC
JJTlNFUlQgSU5UTyB2Ml9wYXBlcl9wb3NpdGlvbl9zbmFwc2hvdCAoaWQsIGFjY291bnRfaWQsIgogI
CAgICAgICAgICAiIGFzX29mX2Jhc2lzLCBwb3NpdGlvbnMsIGRlcml2YXRpb25faW5wdXRzX2hhc2gs
IgogICAgICAgICAgICAiIGVuZ2luZV92ZXJzaW9uc19oYXNoLCBkYXRhX2NsYXNzLCBtb2RlLCBvcGV
yYXRvcl9pZCwiCiAgICAgICAgICAgICIgY29ycmVsYXRpb25faWQsIGNyZWF0ZWRfYXQpIgogICAgIC
AgICAgICBmIiBWQUxVRVMgKCdwMScsJ2ExJywne3t9fScsJ3t7fX0nLCdoMScsJ2gyJyx7QkUxfSkiK
QogICAgICAgIGN1ci5leGVjdXRlKAogICAgICAgICAgICAiSU5TRVJUIElOVE8gdjJfcGFwZXJfYmFs
YW5jZV9zbmFwc2hvdCAoaWQsIGFjY291bnRfaWQsIgogICAgICAgICAgICAiIGFzX29mX2Jhc2lzLCB
jYXNoLCBlcXVpdHksIG1hcmdpbl91c2VkLCBtYXJnaW5fYXZhaWxhYmxlLCIKICAgICAgICAgICAgIi
B1bnJlYWxpemVkX3BubCwgcmVhbGl6ZWRfcG5sLCBkZXJpdmF0aW9uX2lucHV0c19oYXNoLCIKICAgI
CAgICAgICAgIiBlbmdpbmVfdmVyc2lvbnNfaGFzaCwgZGF0YV9jbGFzcywgbW9kZSwgb3BlcmF0b3Jf
aWQsIgogICAgICAgICAgICAiIGNvcnJlbGF0aW9uX2lkLCBjcmVhdGVkX2F0KSIKICAgICAgICAgICA
gZiIgVkFMVUVTICgnYjEnLCdhMScsJ3t7fX0nLCcxJywnMScsJzAnLCcxJywnMCcsJzAnLCdoMScsJ2
gyJyx7QkUxfSkiKQogICAgICAgIGN1ci5leGVjdXRlKAogICAgICAgICAgICAiSU5TRVJUIElOVE8gd
jJfcGFwZXJfcmVjb25jaWxpYXRpb24gKGlkLCBhY2NvdW50X2lkLCBydW5fYmFzaXMsIgogICAgICAg
ICAgICAiIG91dGNvbWUsIGRpc2NyZXBhbmNpZXMsIGlucHV0c19oYXNoLCBkYXRhX2NsYXNzLCBtb2R
lLCIKICAgICAgICAgICAgIiBvcGVyYXRvcl9pZCwgY29ycmVsYXRpb25faWQsIGNyZWF0ZWRfYXQpIg
ogICAgICAgICAgICBmIiBWQUxVRVMgKCdyMScsJ2ExJywne3t9fScsJ2NvbnNpc3RlbnQnLCd7e319J
ywnaDEnLHtCRTF9KSIpCiAgICAgICAgY29ubi5jb21taXQoKQoKICAgICAgICBwcm9iZXMgPSAoCiAg
ICAgICAgICAgICgidjJfcGFwZXJfYWNjb3VudCIsICJhMSIpLAogICAgICAgICAgICAoInYyX3BhcGV
yX29yZGVyX2ludGVudCIsICJpMSIpLAogICAgICAgICAgICAoInYyX3BhcGVyX3Jpc2tfZGVjaXNpb2
4iLCAiZDEiKSwKICAgICAgICAgICAgKCJ2Ml9wYXBlcl9vcmRlcl9ldmVudCIsICJlMSIpLAogICAgI
CAgICAgICAoInYyX3BhcGVyX2ZpbGwiLCAiZjEiKSwKICAgICAgICAgICAgKCJ2Ml9wYXBlcl9wb3Np
dGlvbl9zbmFwc2hvdCIsICJwMSIpLAogICAgICAgICAgICAoInYyX3BhcGVyX2JhbGFuY2Vfc25hcHN
ob3QiLCAiYjEiKSwKICAgICAgICAgICAgKCJ2Ml9wYXBlcl9yZWNvbmNpbGlhdGlvbiIsICJyMSIpLA
ogICAgICAgICkKICAgICAgICBmb3IgdGFibGUsIHJpZCBpbiBwcm9iZXM6CiAgICAgICAgICAgIHVwX
21zZyA9IFRSSUdHRVJTXzAwNDhbZiJ7dGFibGV9X2ltbXV0YWJsZV91cGRhdGUiXQogICAgICAgICAg
ICBkZWxfbXNnID0gVFJJR0dFUlNfMDA0OFtmInt0YWJsZX1faW1tdXRhYmxlX2RlbGV0ZSJdCiAgICA
gICAgICAgIHdpdGggcHl0ZXN0LnJhaXNlcyhzcWxpdGUzLkludGVncml0eUVycm9yKSBhcyBlX3VwOg
ogICAgICAgICAgICAgICAgY3VyLmV4ZWN1dGUoCiAgICAgICAgICAgICAgICAgICAgZiJVUERBVEUge
3RhYmxlfSBTRVQgb3BlcmF0b3JfaWQ9J3gnIFdIRVJFIGlkPSd7cmlkfSciKQogICAgICAgICAgICBh
c3NlcnQgdXBfbXNnIGluIHN0cihlX3VwLnZhbHVlKQogICAgICAgICAgICB3aXRoIHB5dGVzdC5yYWl
zZXMoc3FsaXRlMy5JbnRlZ3JpdHlFcnJvcikgYXMgZV9kZWw6CiAgICAgICAgICAgICAgICBjdXIuZX
hlY3V0ZShmIkRFTEVURSBGUk9NIHt0YWJsZX0gV0hFUkUgaWQ9J3tyaWR9JyIpCiAgICAgICAgICAgI
GFzc2VydCBkZWxfbXNnIGluIHN0cihlX2RlbC52YWx1ZSkKICAgIGZpbmFsbHk6CiAgICAgICAgY29u
bi5jbG9zZSgpCgoKZGVmIHRlc3RfMDA0OF9iZWhhdmlvcmFsX3VuaXF1ZW5lc3NfYW5jaG9ycyh0bXB
fcGF0aDogUGF0aCkgLT4gTm9uZToKICAgICIiIlQtOCBhbmNob3JzIGF0IERCOiBpZGVtcG90ZW5jeS
wgZGVjaXNpb24gdXEsIGV2ZW50IHVxLCBmaWxsIHVxLiIiIgogICAgZGJfZmlsZSwgXyA9IF9kYih0b
XBfcGF0aCwgUkVWXzAwNDgpCiAgICBjb25uID0gc3FsaXRlMy5jb25uZWN0KGRiX2ZpbGUpCiAgICB0
cnk6CiAgICAgICAgY3VyID0gY29ubi5jdXJzb3IoKQoKICAgICAgICBkZWYgX2ludGVudChyaWQsIGl
pZCwga2V5KToKICAgICAgICAgICAgY3VyLmV4ZWN1dGUoCiAgICAgICAgICAgICAgICAiSU5TRVJUIE
lOVE8gdjJfcGFwZXJfb3JkZXJfaW50ZW50IChpZCwgaW50ZW50X2lkLCIKICAgICAgICAgICAgICAgI
CIgYWNjb3VudF9pZCwgaW5zdHJ1bWVudF9pZCwgc2lkZSwgb3JkZXJfdHlwZSwgcXVhbnRpdHksIgog
ICAgICAgICAgICAgICAgIiBsaW1pdF9wcmljZSwgdGltZV9pbl9mb3JjZSwgaWRlbXBvdGVuY3lfa2V
5LCBzbmFwc2hvdF9yZWYsIgogICAgICAgICAgICAgICAgIiB0aW1lX2Jhc2lzLCBjb25maXJtYXRpb2
5fcmVmLCBhY3Rvcl9pZCwgZGF0YV9jbGFzcywgbW9kZSwiCiAgICAgICAgICAgICAgICAiIG9wZXJhd
G9yX2lkLCBjb3JyZWxhdGlvbl9pZCwgY3JlYXRlZF9hdCkiCiAgICAgICAgICAgICAgICBmIiBWQUxV
RVMgKCd7cmlkfScsJ3tpaWR9JywnYTEnLCd4JywnYnV5JywnbWFya2V0JywnMScsTlVMTCwiCiAgICA
gICAgICAgICAgICBmIiAncmVwbGF5X3dpbmRvdycsJ3trZXl9JywnczEnLCd7e319JyxOVUxMLCd0Jy
x7QkUxfSkiKQoKICAgICAgICBfaW50ZW50KCJpMSIsICJpbnQtMSIsICJrMSIpCiAgICAgICAgY29ub
i5jb21taXQoKQogICAgICAgIHdpdGggcHl0ZXN0LnJhaXNlcyhzcWxpdGUzLkludGVncml0eUVycm9y
KToKICAgICAgICAgICAgX2ludGVudCgiaTIiLCAiaW50LTIiLCAiazEiKSAgIyBzYW1lIChhY2NvdW5
0LCBrZXkpCiAgICAgICAgX2ludGVudCgiaTMiLCAiaW50LTMiLCAiazIiKQogICAgICAgIGNvbm4uY2
9tbWl0KCkKCiAgICAgICAgY3VyLmV4ZWN1dGUoCiAgICAgICAgICAgICJJTlNFUlQgSU5UTyB2Ml9wY
XBlcl9yaXNrX2RlY2lzaW9uIChpZCwgaW50ZW50X2lkLCBkZWNpc2lvbiwiCiAgICAgICAgICAgICIg
ZXZhbHVhdGVkX2xpbWl0cywgcmVhc29ucywgcmlza19jb25maWdfdmVyc2lvbiwiCiAgICAgICAgICA
gICIgZGVjaWRlZF9hdF9iYXNpcywgY29uZmlybWF0aW9uX3JlZiwgZGF0YV9jbGFzcywgbW9kZSwiCi
AgICAgICAgICAgICIgb3BlcmF0b3JfaWQsIGNvcnJlbGF0aW9uX2lkLCBjcmVhdGVkX2F0KSIKICAgI
CAgICAgICAgZiIgVkFMVUVTICgnZDEnLCdpMScsJ3Bhc3MnLCd7e319Jywne3t9fScsJ3ByYy0xJywn
e3t9fScsTlVMTCx7QkUxfSkiKQogICAgICAgIGNvbm4uY29tbWl0KCkKICAgICAgICB3aXRoIHB5dGV
zdC5yYWlzZXMoc3FsaXRlMy5JbnRlZ3JpdHlFcnJvcik6CiAgICAgICAgICAgIGN1ci5leGVjdXRlKC
AgIyBzZWNvbmQgZGVjaXNpb24gZm9yIGkxIOKAlCBzY2hlbWEtcmVmdXNlZCAoVC04KQogICAgICAgI
CAgICAgICAgIklOU0VSVCBJTlRPIHYyX3BhcGVyX3Jpc2tfZGVjaXNpb24gKGlkLCBpbnRlbnRfaWQs
IgogICAgICAgICAgICAgICAgIiBkZWNpc2lvbiwgZXZhbHVhdGVkX2xpbWl0cywgcmVhc29ucywgcml
za19jb25maWdfdmVyc2lvbiwiCiAgICAgICAgICAgICAgICAiIGRlY2lkZWRfYXRfYmFzaXMsIGNvbm
Zpcm1hdGlvbl9yZWYsIGRhdGFfY2xhc3MsIG1vZGUsIgogICAgICAgICAgICAgICAgIiBvcGVyYXRvc
l9pZCwgY29ycmVsYXRpb25faWQsIGNyZWF0ZWRfYXQpIgogICAgICAgICAgICAgICAgZiIgVkFMVUVT
ICgnZDInLCdpMScsJ2Jsb2NrJywne3t9fScsJ3t7fX0nLCdwcmMtMScsJ3t7fX0nLCIKICAgICAgICA
gICAgICAgIGYiIE5VTEwse0JFMX0pIikKICAgICAgICAjIEMtMWIgaWZmLUNIRUNLIGJvdGggZGlyZW
N0aW9ucwogICAgICAgIHdpdGggcHl0ZXN0LnJhaXNlcyhzcWxpdGUzLkludGVncml0eUVycm9yKToKI
CAgICAgICAgICAgY3VyLmV4ZWN1dGUoICAjIGhvbGQgV0lUSE9VVCByZWYKICAgICAgICAgICAgICAg
ICJJTlNFUlQgSU5UTyB2Ml9wYXBlcl9yaXNrX2RlY2lzaW9uIChpZCwgaW50ZW50X2lkLCIKICAgICA
gICAgICAgICAgICIgZGVjaXNpb24sIGV2YWx1YXRlZF9saW1pdHMsIHJlYXNvbnMsIHJpc2tfY29uZm
lnX3ZlcnNpb24sIgogICAgICAgICAgICAgICAgIiBkZWNpZGVkX2F0X2Jhc2lzLCBjb25maXJtYXRpb
25fcmVmLCBkYXRhX2NsYXNzLCBtb2RlLCIKICAgICAgICAgICAgICAgICIgb3BlcmF0b3JfaWQsIGNv
cnJlbGF0aW9uX2lkLCBjcmVhdGVkX2F0KSIKICAgICAgICAgICAgICAgIGYiIFZBTFVFUyAoJ2QzJyw
naTMnLCdob2xkJywne3t9fScsJ3t7fX0nLCdwcmMtMScsJ3t7fX0nLCIKICAgICAgICAgICAgICAgIG
YiIE5VTEwse0JFMX0pIikKICAgICAgICB3aXRoIHB5dGVzdC5yYWlzZXMoc3FsaXRlMy5JbnRlZ3Jpd
HlFcnJvcik6CiAgICAgICAgICAgIGN1ci5leGVjdXRlKCAgIyBwYXNzIFdJVEggcmVmCiAgICAgICAg
ICAgICAgICAiSU5TRVJUIElOVE8gdjJfcGFwZXJfcmlza19kZWNpc2lvbiAoaWQsIGludGVudF9pZCw
iCiAgICAgICAgICAgICAgICAiIGRlY2lzaW9uLCBldmFsdWF0ZWRfbGltaXRzLCByZWFzb25zLCByaX
NrX2NvbmZpZ192ZXJzaW9uLCIKICAgICAgICAgICAgICAgICIgZGVjaWRlZF9hdF9iYXNpcywgY29uZ
mlybWF0aW9uX3JlZiwgZGF0YV9jbGFzcywgbW9kZSwiCiAgICAgICAgICAgICAgICAiIG9wZXJhdG9y
X2lkLCBjb3JyZWxhdGlvbl9pZCwgY3JlYXRlZF9hdCkiCiAgICAgICAgICAgICAgICBmIiBWQUxVRVM
gKCdkNCcsJ2kzJywncGFzcycsJ3t7fX0nLCd7e319JywncHJjLTEnLCd7e319JywiCiAgICAgICAgIC
AgICAgICBmIiAncmVmLXgnLHtCRTF9KSIpCgogICAgICAgICMgZXZlbnQtbGVkZ2VyIHVxIChhcHBlb
mQtb25seSBkb3VibGUtYXBwZW5kIHJlZnVzYWwpCiAgICAgICAgY3VyLmV4ZWN1dGUoCiAgICAgICAg
ICAgICJJTlNFUlQgSU5UTyB2Ml9wYXBlcl9vcmRlcl9ldmVudCAoaWQsIGludGVudF9pZCwgZXZlbnR
faW5kZXgsIgogICAgICAgICAgICAiIGZyb21fc3RhdGUsIHRvX3N0YXRlLCBldmVudF9jbGFzcywgZG
V0YWlscywgYWN0b3JfaWQsIgogICAgICAgICAgICAiIGRhdGFfY2xhc3MsIG1vZGUsIG9wZXJhdG9yX
2lkLCBjb3JyZWxhdGlvbl9pZCwgY3JlYXRlZF9hdCkiCiAgICAgICAgICAgIGYiIFZBTFVFUyAoJ2Ux
JywnaTEnLDAsJ2RyYWZ0JywndmFsaWRhdGVkJywnb3JkZXIudmFsaWRhdGVkJywiCiAgICAgICAgICA
gIGYiICd7e319JywndCcse0JFMX0pIikKICAgICAgICBjb25uLmNvbW1pdCgpCiAgICAgICAgd2l0aC
BweXRlc3QucmFpc2VzKHNxbGl0ZTMuSW50ZWdyaXR5RXJyb3IpOgogICAgICAgICAgICBjdXIuZXhlY
3V0ZSgKICAgICAgICAgICAgICAgICJJTlNFUlQgSU5UTyB2Ml9wYXBlcl9vcmRlcl9ldmVudCAoaWQs
IGludGVudF9pZCwiCiAgICAgICAgICAgICAgICAiIGV2ZW50X2luZGV4LCBmcm9tX3N0YXRlLCB0b19
zdGF0ZSwgZXZlbnRfY2xhc3MsIGRldGFpbHMsIgogICAgICAgICAgICAgICAgIiBhY3Rvcl9pZCwgZG
F0YV9jbGFzcywgbW9kZSwgb3BlcmF0b3JfaWQsIGNvcnJlbGF0aW9uX2lkLCIKICAgICAgICAgICAgI
CAgICIgY3JlYXRlZF9hdCkiCiAgICAgICAgICAgICAgICBmIiBWQUxVRVMgKCdlMicsJ2kxJywwLCdk
cmFmdCcsJ3JlamVjdGVkJywnb3JkZXIucmVqZWN0ZWQnLCIKICAgICAgICAgICAgICAgIGYiICd7e31
9JywndCcse0JFMX0pIikKICAgICAgICAjIGZpbGwgYW5jaG9yCiAgICAgICAgY3VyLmV4ZWN1dGUoCi
AgICAgICAgICAgICJJTlNFUlQgSU5UTyB2Ml9wYXBlcl9maWxsIChpZCwgZmlsbF9pZCwgaW50ZW50X
2lkLCBmaWxsX2luZGV4LCIKICAgICAgICAgICAgIiBxdWFudGl0eSwgcmF3X3ByaWNlLCBlZmZlY3Rp
dmVfcHJpY2UsIGNvc3RfbW9kZWxfcmVmLCIKICAgICAgICAgICAgIiBmaWxsX2NsYXNzLCBzaW11bGF
0b3JfdmVyc2lvbiwgc25hcHNob3RfcmVmLCB0aW1lX2Jhc2lzLCIKICAgICAgICAgICAgIiBkYXRhX2
NsYXNzLCBtb2RlLCBvcGVyYXRvcl9pZCwgY29ycmVsYXRpb25faWQsIGNyZWF0ZWRfYXQpIgogICAgI
CAgICAgICBmIiBWQUxVRVMgKCdmMScsJ2ZpZC0xJywnaTEnLDAsJzEnLCcxMDAnLCcxMDAnLCd7e319
JywiCiAgICAgICAgICAgIGYiICdwYXBlcl9zaW11bGF0ZWQnLCdweHMtMS4wLjAnLCdzJywne3t9fSc
se0JFMX0pIikKICAgICAgICBjb25uLmNvbW1pdCgpCiAgICAgICAgd2l0aCBweXRlc3QucmFpc2VzKH
NxbGl0ZTMuSW50ZWdyaXR5RXJyb3IpOgogICAgICAgICAgICBjdXIuZXhlY3V0ZSgKICAgICAgICAgI
CAgICAgICJJTlNFUlQgSU5UTyB2Ml9wYXBlcl9maWxsIChpZCwgZmlsbF9pZCwgaW50ZW50X2lkLCIK
ICAgICAgICAgICAgICAgICIgZmlsbF9pbmRleCwgcXVhbnRpdHksIHJhd19wcmljZSwgZWZmZWN0aXZ
lX3ByaWNlLCIKICAgICAgICAgICAgICAgICIgY29zdF9tb2RlbF9yZWYsIGZpbGxfY2xhc3MsIHNpbX
VsYXRvcl92ZXJzaW9uLCIKICAgICAgICAgICAgICAgICIgc25hcHNob3RfcmVmLCB0aW1lX2Jhc2lzL
CBkYXRhX2NsYXNzLCBtb2RlLCBvcGVyYXRvcl9pZCwiCiAgICAgICAgICAgICAgICAiIGNvcnJlbGF0
aW9uX2lkLCBjcmVhdGVkX2F0KSIKICAgICAgICAgICAgICAgIGYiIFZBTFVFUyAoJ2YyJywnZmlkLTI
nLCdpMScsMCwnMScsJzEwMCcsJzEwMCcsJ3t7fX0nLCIKICAgICAgICAgICAgICAgIGYiICdwYXBlcl
9zaW11bGF0ZWQnLCdweHMtMS4wLjAnLCdzJywne3t9fScse0JFMX0pIikKICAgIGZpbmFsbHk6CiAgI
CAgICAgY29ubi5jbG9zZSgpCgoKZGVmIHRlc3RfMDA0OF9ub190b3VjaF9wcm90ZWN0ZWRfc3RhdGUo
dG1wX3BhdGg6IFBhdGgpIC0+IE5vbmU6CiAgICAiIiJULTE1OiAwMDQ3LWNoYWluIGNvbnRlbnQgYnl
0ZS1pZGVudGljYWwgYWNyb3NzIDAwNDg7IHRyaWdnZXIgZGVsdGEKICAgIGlzIGV4YWN0bHkgdGhlID
E2IG5ldyBuYW1lcyAoY29udGVudC1iYXNlZCwgUEdGLTAxMikuIiIiCiAgICBkYl9maWxlLCBkYl91c
mwgPSBfZGIodG1wX3BhdGgsIFJFVl8wMDQ3KQogICAgcHJlX3Blcm1zID0gc29ydGVkKF9xKGRiX2Zp
bGUsCiAgICAgICAgICAgICAgICAgICAgICAgICAgIlNFTEVDVCByb2xlLCBwZXJtaXNzaW9uLCBzYWw
gRlJPTSB2Ml9wZXJtaXNzaW9uIikpCiAgICBwcmVfY29tcCA9IHNvcnRlZChfcShkYl9maWxlLAogIC
AgICAgICAgICAgICAgICAgICAgICAgIlNFTEVDVCBjb21wb25lbnQsIHZlcnNpb24sIHNvdXJjZV9oY
XNoIgogICAgICAgICAgICAgICAgICAgICAgICAgIiBGUk9NIHYyX2NvbXB1dGF0aW9uX3ZlcnNpb24i
KSkKICAgIHByZV90cmlncyA9IF92Ml90cmlnZ2VycyhkYl9maWxlKQogICAgcmVzdWx0ID0gX2FsZW1
iaWMoWyJ1cGdyYWRlIiwgUkVWXzAwNDhdLCBkYl91cmwpCiAgICBhc3NlcnQgcmVzdWx0LnJldHVybm
NvZGUgPT0gMCwgcmVzdWx0LnN0ZGVycgogICAgcG9zdF9wZXJtcyA9IHNvcnRlZChfcShkYl9maWxlL
AogICAgICAgICAgICAgICAgICAgICAgICAgICAiU0VMRUNUIHJvbGUsIHBlcm1pc3Npb24sIHNhbCBG
Uk9NIHYyX3Blcm1pc3Npb24iKSkKICAgIHBvc3RfY29tcCA9IHNvcnRlZChfcShkYl9maWxlLAogICA
gICAgICAgICAgICAgICAgICAgICAgICJTRUxFQ1QgY29tcG9uZW50LCB2ZXJzaW9uLCBzb3VyY2VfaG
FzaCIKICAgICAgICAgICAgICAgICAgICAgICAgICAiIEZST00gdjJfY29tcHV0YXRpb25fdmVyc2lvb
iIpKQogICAgcG9zdF90cmlncyA9IF92Ml90cmlnZ2VycyhkYl9maWxlKQogICAgYXNzZXJ0IFtwIGZv
ciBwIGluIHBvc3RfcGVybXMKICAgICAgICAgICAgaWYgbm90IHBbMV0uc3RhcnRzd2l0aCgidjIucGF
wZXIuIildID09IHByZV9wZXJtcwogICAgYXNzZXJ0IFtjIGZvciBjIGluIHBvc3RfY29tcAogICAgIC
AgICAgICBpZiBub3QgY1swXS5zdGFydHN3aXRoKCJwYXBlcl8iKV0gPT0gcHJlX2NvbXAKICAgIGFzc
2VydCBwb3N0X3RyaWdzIC0gcHJlX3RyaWdzID09IHNldChUUklHR0VSU18wMDQ4KQoKCmRlZiB0ZXN0
XzAwNDhfZG93bmdyYWRlX2N5Y2xlX2NvbnRlbnRfYmFzZWQodG1wX3BhdGg6IFBhdGgpIC0+IE5vbmU
6CiAgICAiIiJULTE1OiBzeW1tZXRyaWMgdGVhcmRvd247IGNvbnRlbnQgZXF1YWwgdG8gdGhlIHByZS
0wMDQ4IHN0YXRlLiIiIgogICAgZGJfZmlsZSwgZGJfdXJsID0gX2RiKHRtcF9wYXRoLCBSRVZfMDA0N
ykKICAgIHByZV9wZXJtcyA9IHNvcnRlZChfcShkYl9maWxlLAogICAgICAgICAgICAgICAgICAgICAg
ICAgICJTRUxFQ1Qgcm9sZSwgcGVybWlzc2lvbiwgc2FsIEZST00gdjJfcGVybWlzc2lvbiIpKQogICA
gcHJlX2NvbXAgPSBzb3J0ZWQoX3EoZGJfZmlsZSwKICAgICAgICAgICAgICAgICAgICAgICAgICJTRU
xFQ1QgY29tcG9uZW50LCB2ZXJzaW9uIEZST00iCiAgICAgICAgICAgICAgICAgICAgICAgICAiIHYyX
2NvbXB1dGF0aW9uX3ZlcnNpb24iKSkKICAgIHJlc3VsdCA9IF9hbGVtYmljKFsidXBncmFkZSIsIFJF
Vl8wMDQ4XSwgZGJfdXJsKQogICAgYXNzZXJ0IHJlc3VsdC5yZXR1cm5jb2RlID09IDAsIHJlc3VsdC5
zdGRlcnIKICAgIHJlc3VsdCA9IF9hbGVtYmljKFsiZG93bmdyYWRlIiwgUkVWXzAwNDddLCBkYl91cm
wpCiAgICBhc3NlcnQgcmVzdWx0LnJldHVybmNvZGUgPT0gMCwgcmVzdWx0LnN0ZGVycgogICAgdGFib
GVzID0ge3JbMF0gZm9yIHIgaW4gX3EoCiAgICAgICAgZGJfZmlsZSwgIlNFTEVDVCBuYW1lIEZST00g
c3FsaXRlX21hc3RlciBXSEVSRSB0eXBlPSd0YWJsZSciKX0KICAgIGZvciB0IGluIFBBUEVSX1RBQkx
FUzoKICAgICAgICBhc3NlcnQgdCBub3QgaW4gdGFibGVzCiAgICBhc3NlcnQgc29ydGVkKF9xKGRiX2
ZpbGUsCiAgICAgICAgICAgICAgICAgICAgICJTRUxFQ1Qgcm9sZSwgcGVybWlzc2lvbiwgc2FsIEZST
00gdjJfcGVybWlzc2lvbiIpKSBcCiAgICAgICAgPT0gcHJlX3Blcm1zCiAgICBhc3NlcnQgc29ydGVk
KF9xKGRiX2ZpbGUsCiAgICAgICAgICAgICAgICAgICAgICJTRUxFQ1QgY29tcG9uZW50LCB2ZXJzaW9
uIEZST00iCiAgICAgICAgICAgICAgICAgICAgICIgdjJfY29tcHV0YXRpb25fdmVyc2lvbiIpKSA9PS
BwcmVfY29tcAogICAgYXNzZXJ0IGxlbihfdjJfdHJpZ2dlcnMoZGJfZmlsZSkpID09IDQyCiAgICAjI
GNvbXB2ZXIgZGVsZXRlLWd1YXJkIHJlc3RvcmVkCiAgICBndWFyZCA9IF9xKGRiX2ZpbGUsCiAgICAg
ICAgICAgICAgICJTRUxFQ1QgQ09VTlQoKikgRlJPTSBzcWxpdGVfbWFzdGVyIFdIRVJFIHR5cGU9J3R
yaWdnZXInIgogICAgICAgICAgICAgICAiIEFORCBuYW1lPSd2Ml9jb21wdXRhdGlvbl92ZXJzaW9uX2
ltbXV0YWJsZV9kZWxldGUnIikKICAgIGFzc2VydCBndWFyZFswXVswXSA9PSAxCgoKQHB5dGVzdC5tY
XJrLnBhcmFtZXRyaXplKCJyZXYiLCBbUkVWXzAwNDcsIFJFVl8wMDQ4XSkKZGVmIHRlc3RfZHJpZnRf
Z2F0ZV8wMDQ4KHRtcF9wYXRoOiBQYXRoLCByZXY6IHN0cikgLT4gTm9uZToKICAgICIiIlQtMTQ6IGZ
vcm1hdC1pbmRlcGVuZGVudCAoUEdGLTAxNCk7IHplcm8gQkUtOCB0b2tlbnMgZWl0aGVyIGZvcm07Ci
AgICBhdCBoZWFkIHRoZSBkcmlmdCBpcyBleGFjdGx5IHRoZSA5IGluaGVyaXRlZCBWMSB0b2tlbnMuI
iIiCiAgICBkYl9maWxlLCBkYl91cmwgPSBfZGIodG1wX3BhdGgsIHJldikKICAgIGNoZWNrID0gX2Fs
ZW1iaWMoWyJjaGVjayJdLCBkYl91cmwpCiAgICBkcmlmdCA9IChjaGVjay5zdGRvdXQgKyBjaGVjay5
zdGRlcnIpLmxvd2VyKCkKICAgIGFzc2VydCBjaGVjay5yZXR1cm5jb2RlICE9IDAKICAgIGZvciBtYX
JrZXIgaW4gKCJ2Ml9wYXBlcl9hY2NvdW50IiwgInYyX3BhcGVyX29yZGVyX2ludGVudCIsCiAgICAgI
CAgICAgICAgICAgICAidjJfcGFwZXJfcmlza19kZWNpc2lvbiIsICJ2Ml9wYXBlcl9vcmRlcl9ldmVu
dCIsCiAgICAgICAgICAgICAgICAgICAidjJfcGFwZXJfZmlsbCIsICJ2Ml9wYXBlcl9wb3NpdGlvbl9
zbmFwc2hvdCIsCiAgICAgICAgICAgICAgICAgICAidjJfcGFwZXJfYmFsYW5jZV9zbmFwc2hvdCIsIC
J2Ml9wYXBlcl9yZWNvbmNpbGlhdGlvbiIpOgogICAgICAgIGFzc2VydCBtYXJrZXIgbm90IGluIGRya
WZ0LCBmIkJFLTggZHJpZnQgYXQge3Jldn06IHttYXJrZXJ9IgogICAgaWYgIm5vdCB1cCB0byBkYXRl
IiBub3QgaW4gZHJpZnQ6CiAgICAgICAgYXNzZXJ0ICJhdWRpdF93cml0ZV9mYWlsdXJlX3JlY29yZHM
iIGluIGRyaWZ0CgoKZGVmIHRlc3RfMDA0OF9zdGF0ZV9jaGVja3ModG1wX3BhdGg6IFBhdGgpIC0+IE
5vbmU6CiAgICAiIiJDbG9zZWQgQ0hFQ0sgdm9jYWJ1bGFyaWVzOiBhY2NvdW50IHN0YXRlLCBkZWNpc
2lvbiwgb3V0Y29tZSwgdGlmLiIiIgogICAgZGJfZmlsZSwgXyA9IF9kYih0bXBfcGF0aCwgUkVWXzAw
NDgpCiAgICBjb25uID0gc3FsaXRlMy5jb25uZWN0KGRiX2ZpbGUpCiAgICB0cnk6CiAgICAgICAgd2l
0aCBweXRlc3QucmFpc2VzKHNxbGl0ZTMuSW50ZWdyaXR5RXJyb3IpOgogICAgICAgICAgICBjb25uLm
V4ZWN1dGUoCiAgICAgICAgICAgICAgICAiSU5TRVJUIElOVE8gdjJfcGFwZXJfYWNjb3VudCAoaWQsI
GFjY291bnRfaWQsIHJlY29yZF9zZXEsIgogICAgICAgICAgICAgICAgIiBuYW1lLCBiYXNlX2N1cnJl
bmN5LCBpbml0aWFsX2JhbGFuY2UsIG1hcmdpbl9wYXJhbXMsIgogICAgICAgICAgICAgICAgIiBsaWZ
lY3ljbGVfc3RhdGUsIGNvbmZpcm1hdGlvbl9yZWYsIGRhdGFfY2xhc3MsIG1vZGUsIgogICAgICAgIC
AgICAgICAgIiBvcGVyYXRvcl9pZCwgY29ycmVsYXRpb25faWQsIGNyZWF0ZWRfYXQpIgogICAgICAgI
CAgICAgICAgZiIgVkFMVUVTICgnYS14JywnYWNjdC14JywxLCdBJywnVVNEJywnMScsJ3t7fX0nLCdv
cGVuJywiCiAgICAgICAgICAgICAgICBmIiAncicse0JFMX0pIikKICAgICAgICB3aXRoIHB5dGVzdC5
yYWlzZXMoc3FsaXRlMy5JbnRlZ3JpdHlFcnJvcik6CiAgICAgICAgICAgIGNvbm4uZXhlY3V0ZSggIC
Mgbm9uLVVTRCByZWZ1c2VkICh2MSBjdXJyZW5jeSBsYXcpCiAgICAgICAgICAgICAgICAiSU5TRVJUI
ElOVE8gdjJfcGFwZXJfYWNjb3VudCAoaWQsIGFjY291bnRfaWQsIHJlY29yZF9zZXEsIgogICAgICAg
ICAgICAgICAgIiBuYW1lLCBiYXNlX2N1cnJlbmN5LCBpbml0aWFsX2JhbGFuY2UsIG1hcmdpbl9wYXJ
hbXMsIgogICAgICAgICAgICAgICAgIiBsaWZlY3ljbGVfc3RhdGUsIGNvbmZpcm1hdGlvbl9yZWYsIG
RhdGFfY2xhc3MsIG1vZGUsIgogICAgICAgICAgICAgICAgIiBvcGVyYXRvcl9pZCwgY29ycmVsYXRpb
25faWQsIGNyZWF0ZWRfYXQpIgogICAgICAgICAgICAgICAgZiIgVkFMVUVTICgnYS15JywnYWNjdC15
JywxLCdBJywnRVVSJywnMScsJ3t7fX0nLCdhY3RpdmUnLCIKICAgICAgICAgICAgICAgIGYiICdyJyx
7QkUxfSkiKQogICAgICAgIHdpdGggcHl0ZXN0LnJhaXNlcyhzcWxpdGUzLkludGVncml0eUVycm9yKT
oKICAgICAgICAgICAgY29ubi5leGVjdXRlKCAgIyBsaW1pdF9wcmljZSBpZmYgbGltaXQgdHlwZQogI
CAgICAgICAgICAgICAgIklOU0VSVCBJTlRPIHYyX3BhcGVyX29yZGVyX2ludGVudCAoaWQsIGludGVu
dF9pZCwiCiAgICAgICAgICAgICAgICAiIGFjY291bnRfaWQsIGluc3RydW1lbnRfaWQsIHNpZGUsIG9
yZGVyX3R5cGUsIHF1YW50aXR5LCIKICAgICAgICAgICAgICAgICIgbGltaXRfcHJpY2UsIHRpbWVfaW
5fZm9yY2UsIGlkZW1wb3RlbmN5X2tleSwiCiAgICAgICAgICAgICAgICAiIHNuYXBzaG90X3JlZiwgd
GltZV9iYXNpcywgY29uZmlybWF0aW9uX3JlZiwgYWN0b3JfaWQsIgogICAgICAgICAgICAgICAgIiBk
YXRhX2NsYXNzLCBtb2RlLCBvcGVyYXRvcl9pZCwgY29ycmVsYXRpb25faWQsIgogICAgICAgICAgICA
gICAgIiBjcmVhdGVkX2F0KSIKICAgICAgICAgICAgICAgIGYiIFZBTFVFUyAoJ2kteCcsJ2ludC14Jy
wnYTEnLCd4JywnYnV5JywnbWFya2V0JywnMScsJzk5JywiCiAgICAgICAgICAgICAgICBmIiAncmVwb
GF5X3dpbmRvdycsJ2t4JywncycsJ3t7fX0nLE5VTEwsJ3QnLHtCRTF9KSIpCiAgICAgICAgd2l0aCBw
eXRlc3QucmFpc2VzKHNxbGl0ZTMuSW50ZWdyaXR5RXJyb3IpOgogICAgICAgICAgICBjb25uLmV4ZWN
1dGUoICAjIHJlY29uY2lsaWF0aW9uIG91dGNvbWUgY2xvc2VkIHNldAogICAgICAgICAgICAgICAgIk
lOU0VSVCBJTlRPIHYyX3BhcGVyX3JlY29uY2lsaWF0aW9uIChpZCwgYWNjb3VudF9pZCwiCiAgICAgI
CAgICAgICAgICAiIHJ1bl9iYXNpcywgb3V0Y29tZSwgZGlzY3JlcGFuY2llcywgaW5wdXRzX2hhc2gs
IgogICAgICAgICAgICAgICAgIiBkYXRhX2NsYXNzLCBtb2RlLCBvcGVyYXRvcl9pZCwgY29ycmVsYXR
pb25faWQsIgogICAgICAgICAgICAgICAgIiBjcmVhdGVkX2F0KSIKICAgICAgICAgICAgICAgIGYiIF
ZBTFVFUyAoJ3IteCcsJ2ExJywne3t9fScsJ21heWJlJywne3t9fScsJ2gnLHtCRTF9KSIpCiAgICBma
W5hbGx5OgogICAgICAgIGNvbm4uY2xvc2UoKQo=
'@
$LandPath = Join-Path $BackendRoot "tests\test_v2_be8_migration.py"
New-Item -ItemType Directory -Force -Path (Split-Path $LandPath) | Out-Null
if (Test-Path $LandPath) {
    $Cur = (Get-FileHash -Path $LandPath -Algorithm SHA256).Hash.ToLower()
    if ($Cur -eq "bd3227587bd913d5bead7c8958ff3fb6bd18b077ca1b5975f0ae806e0ab019b1") { Write-Evidence ("pre-landing witnessed (already pinned bytes): tests\test_v2_be8_migration.py") }
    else { throw ("STOP (A4 FOREIGN-STATE ADJUDICATION LAW): new-file target exists with foreign bytes: " + $LandPath + " sha " + $Cur + " . Nothing modified for this file; report to ITRGA.") }
} else {
    [IO.File]::WriteAllBytes($LandPath, (B64-Decode -B64Chunk $Ftests_test_v2_be8_migration_py))
    $Cur = (Get-FileHash -Path $LandPath -Algorithm SHA256).Hash.ToLower()
    if ($Cur -ne "bd3227587bd913d5bead7c8958ff3fb6bd18b077ca1b5975f0ae806e0ab019b1") { throw ("FAIL: post-write hash drift on " + $LandPath) }
    Write-Evidence ("landed + verified: tests\test_v2_be8_migration.py")
}

# file: tests\test_v2_be8_orders.py  (pin 46c9cee65ca0...)
$Ftests_test_v2_be8_orders_py = @'
IiIiVjIgQkUtOCBvcmRlciBsaWZlY3ljbGUgKyBBUEkgdGVzdHMg4oCUIEJPLVYyLUJFLTgtMDAxIFQ
tMi9ULTUvVC04L1QtOS9ULTE2LgoKRTEgZW5kLXRvLWVuZCBsaWZlY3ljbGU7IHRoZSBTMi42L0MtMS
Bob2xkIHNlYW0gKGFsbCBmb3VyIHJlZnVzYWwgY2xhc3NlcworIEMtMWQgYm90aCBhcm1zKTsgaWRlb
XBvdGVuY3kgKEUyKTsgZmFpbHVyZSB0YXhvbm9teSAoRTMpOyBSQkFDICsgbW9kZQpnYXRlLiBQQVBF
Ui1tb2RlIGFwcCAoRC0yKS4gU29ja2V0IGd1YXJkIG9uIGV2ZXJ5IHRlc3QuCiIiIgoKZnJvbSBfX2Z
1dHVyZV9fIGltcG9ydCBhbm5vdGF0aW9ucwoKaW1wb3J0IHNvY2tldApmcm9tIGRlY2ltYWwgaW1wb3
J0IERlY2ltYWwKZnJvbSB1dWlkIGltcG9ydCB1dWlkNAoKaW1wb3J0IHB5dGVzdAppbXBvcnQgcHl0Z
XN0X2FzeW5jaW8KZnJvbSBodHRweCBpbXBvcnQgQVNHSVRyYW5zcG9ydCwgQXN5bmNDbGllbnQKZnJv
bSBzcWxhbGNoZW15IGltcG9ydCBzZWxlY3QKCmZyb20gYXBwLmF1dGguc2VjdXJpdHkgaW1wb3J0IGh
hc2hfcGFzc3dvcmQKZnJvbSBhcHAuZGIubW9kZWxzLm9wZXJhdG9yIGltcG9ydCBPcGVyYXRvcgpmcm
9tIGFwcC5kYi5tb2RlbHMudjJfYXVkaXRfZXZlbnQgaW1wb3J0IFYyQXVkaXRFdmVudApmcm9tIGFwc
C5kYi5tb2RlbHMudjJfcGFwZXJfdHJhZGluZyBpbXBvcnQgKAogICAgVjJQYXBlckZpbGwsCiAgICBW
MlBhcGVyT3JkZXJFdmVudCwKICAgIFYyUGFwZXJSaXNrRGVjaXNpb24sCikKZnJvbSBhcHAuZGIuc2V
zc2lvbiBpbXBvcnQgc2Vzc2lvbl9zY29wZQoKUFQgPSAiL2FwaS92MS92Mi9wYXBlciIKUEFTU1dPUk
QgPSAib3BlcmF0b3ItcGFzcy0xMjMiCkFOTkVYX0NPU1RTID0gewogICAgInNwcmVhZCI6IHsidmFsd
WUiOiAiMC4xMCIsICJ1bml0IjogInByaWNlIiwgImNpdGF0aW9uIjogImJhbmQtZGVjbGFyZWQifSwK
ICAgICJjb21taXNzaW9uIjogeyJ2YWx1ZSI6ICIwLjA1IiwgInVuaXQiOiAicHJpY2UiLAogICAgICA
gICAgICAgICAgICAgImNpdGF0aW9uIjogImJhbmQtZGVjbGFyZWQifSwKICAgICJzbGlwcGFnZSI6IH
sidmFsdWUiOiAiMCIsICJ1bml0IjogInByaWNlIiwgImNpdGF0aW9uIjogImJhbmQtZGVjbGFyZWQif
SwKfQoKCkBweXRlc3QuZml4dHVyZShhdXRvdXNlPVRydWUpCmRlZiBfc29ja2V0X2d1YXJkKG1vbmtl
eXBhdGNoKToKICAgIGRlZiBfZGVueSgqX2EsICoqX2spOgogICAgICAgIHJhaXNlIEFzc2VydGlvbkV
ycm9yKCJuZXR3b3JrIGF0dGVtcHQgZHVyaW5nIEJFLTggdGVzdCIpCgogICAgbW9ua2V5cGF0Y2guc2
V0YXR0cihzb2NrZXQsICJnZXRhZGRyaW5mbyIsIF9kZW55KQogICAgbW9ua2V5cGF0Y2guc2V0YXR0c
ihzb2NrZXQsICJjcmVhdGVfY29ubmVjdGlvbiIsIF9kZW55KQoKCkBweXRlc3RfYXN5bmNpby5maXh0
dXJlCmFzeW5jIGRlZiBwYXBlcl9jbGllbnQocHJlcGFyZWRfZGIsIG1vbmtleXBhdGNoKToKICAgICI
iIkFwcCBpbiBQQVBFUiBtb2RlIChELTIgbGF3KSDigJQgdGhlIGJhbmQncyB3cml0ZXIgbW9kZS4iIi
IKICAgIG1vbmtleXBhdGNoLnNldGVudigiQVhJT01fVjJfTU9ERSIsICJQQVBFUiIpCiAgICBmcm9tI
GFwcC5jb3JlLmNvbmZpZyBpbXBvcnQgY2xlYXJfc2V0dGluZ3NfY2FjaGUKICAgIGZyb20gYXBwLm1h
aW4gaW1wb3J0IGNyZWF0ZV9hcHAKCiAgICBjbGVhcl9zZXR0aW5nc19jYWNoZSgpCiAgICBhcHBsaWN
hdGlvbiA9IGNyZWF0ZV9hcHAoKQogICAgdHJhbnNwb3J0ID0gQVNHSVRyYW5zcG9ydChhcHA9YXBwbG
ljYXRpb24pCiAgICBhc3luYyB3aXRoIEFzeW5jQ2xpZW50KHRyYW5zcG9ydD10cmFuc3BvcnQsIGJhc
2VfdXJsPSJodHRwOi8vdGVzdCIpIGFzIGFjOgogICAgICAgIGFzeW5jIHdpdGggYXBwbGljYXRpb24u
cm91dGVyLmxpZmVzcGFuX2NvbnRleHQoYXBwbGljYXRpb24pOgogICAgICAgICAgICB5aWVsZCBhYwo
KCkBweXRlc3RfYXN5bmNpby5maXh0dXJlCmFzeW5jIGRlZiByZXNlYXJjaF9jbGllbnQocHJlcGFyZW
RfZGIsIG1vbmtleXBhdGNoKToKICAgICIiIkFwcCBpbiBSRVNFQVJDSCBtb2RlIOKAlCBuZWdhdGl2Z
S1tb2RlIGFybSAoVC0yKS4iIiIKICAgIG1vbmtleXBhdGNoLnNldGVudigiQVhJT01fVjJfTU9ERSIs
ICJSRVNFQVJDSCIpCiAgICBmcm9tIGFwcC5jb3JlLmNvbmZpZyBpbXBvcnQgY2xlYXJfc2V0dGluZ3N
fY2FjaGUKICAgIGZyb20gYXBwLm1haW4gaW1wb3J0IGNyZWF0ZV9hcHAKCiAgICBjbGVhcl9zZXR0aW
5nc19jYWNoZSgpCiAgICBhcHBsaWNhdGlvbiA9IGNyZWF0ZV9hcHAoKQogICAgdHJhbnNwb3J0ID0gQ
VNHSVRyYW5zcG9ydChhcHA9YXBwbGljYXRpb24pCiAgICBhc3luYyB3aXRoIEFzeW5jQ2xpZW50KHRy
YW5zcG9ydD10cmFuc3BvcnQsIGJhc2VfdXJsPSJodHRwOi8vdGVzdCIpIGFzIGFjOgogICAgICAgIGF
zeW5jIHdpdGggYXBwbGljYXRpb24ucm91dGVyLmxpZmVzcGFuX2NvbnRleHQoYXBwbGljYXRpb24pOg
ogICAgICAgICAgICB5aWVsZCBhYwoKCmFzeW5jIGRlZiBfbG9naW4oY2xpZW50LCB1c2VybmFtZSwgc
GFzc3dvcmQ9UEFTU1dPUkQpOgogICAgciA9IGF3YWl0IGNsaWVudC5wb3N0KCIvYXBpL3YxL2F1dGgv
bG9naW4iLAogICAgICAgICAgICAgICAgICAgICAgICAgIGpzb249eyJ1c2VybmFtZSI6IHVzZXJuYW1
lLCAicGFzc3dvcmQiOiBwYXNzd29yZH0pCiAgICBhc3NlcnQgci5zdGF0dXNfY29kZSA9PSAyMDAsIH
IudGV4dAogICAgcmV0dXJuIHsiQXV0aG9yaXphdGlvbiI6IGYiQmVhcmVyIHtyLmpzb24oKVsndG9rZ
W5zJ11bJ2FjY2Vzc190b2tlbiddfSJ9CgoKYXN5bmMgZGVmIF9hZG1pbihjbGllbnQpOgogICAgcmV0
dXJuIGF3YWl0IF9sb2dpbihjbGllbnQsICJhZG1pbiIsICJhZG1pbjEyMyIpCgoKYXN5bmMgZGVmIF9
vcGVyYXRvcl9oZWFkZXJzKGNsaWVudCk6CiAgICBhc3luYyB3aXRoIHNlc3Npb25fc2NvcGUoKSBhcy
BzZXNzaW9uOgogICAgICAgIG9wID0gT3BlcmF0b3IodXNlcm5hbWU9ZiJiZTgtb3Ate3V1aWQ0KCkua
GV4WzoxMF19IiwKICAgICAgICAgICAgICAgICAgICAgIGhhc2hlZF9wYXNzd29yZD1oYXNoX3Bhc3N3
b3JkKFBBU1NXT1JEKSwKICAgICAgICAgICAgICAgICAgICAgIHJvbGU9Im9wZXJhdG9yIiwgaXNfYWN
0aXZlPVRydWUpCiAgICAgICAgc2Vzc2lvbi5hZGQob3ApCiAgICAgICAgYXdhaXQgc2Vzc2lvbi5mbH
VzaCgpCiAgICAgICAgdXNlcm5hbWUgPSBvcC51c2VybmFtZQogICAgcmV0dXJuIGF3YWl0IF9sb2dpb
ihjbGllbnQsIHVzZXJuYW1lKQoKCmRlZiBfYmFycyhjbG9zZXM9Tm9uZSwgbGlxdWlkaXR5PSIyIik6
CiAgICBjbG9zZXMgPSBjbG9zZXMgb3IgWyIxMDAiLCAiOTkiLCAiOTciLCAiOTYiLCAiOTkiLCAiMTA
yIiwgIjEwNCIsICIxMDMiLAogICAgICAgICAgICAgICAgICAgICAgICAiMTAxIiwgIjEwMCJdCiAgIC
BvdXQgPSBbXQogICAgZm9yIGksIGNsb3NlIGluIGVudW1lcmF0ZShjbG9zZXMpOgogICAgICAgIGMgP
SBEZWNpbWFsKGNsb3NlKQogICAgICAgIG91dC5hcHBlbmQoeyJvcGVuX3RpbWUiOiBmIjIwMjYtMDkt
MDFUe2k6MDJkfTowMDowMCswMDowMCIsCiAgICAgICAgICAgICAgICAgICAgIm9wZW4iOiBzdHIoYyk
sICJoaWdoIjogc3RyKGMgKyAxKSwgImxvdyI6IHN0cihjIC0gMSksCiAgICAgICAgICAgICAgICAgIC
AgImNsb3NlIjogc3RyKGMpLCAibGlxdWlkaXR5IjogbGlxdWlkaXR5fSkKICAgIHJldHVybiBvdXQKC
gphc3luYyBkZWYgX2FjY291bnQoY2xpZW50LCBoZWFkZXJzLCBhY2NvdW50X2lkPSJhY2N0LTEiLAog
ICAgICAgICAgICAgICAgICAgaW5pdGlhbF9iYWxhbmNlPSIxMDAwMDAwIikgLT4gc3RyOgogICAgIiI
iVHdvLWFjdCBjb25maXJtYXRpb24gZmxvdyAoUzcuMikuIFJldHVybnMgYWNjb3VudCByb3cgaWQuIi
IiCiAgICBwYXlsb2FkID0geyJhY3Rpb24iOiAiY3JlYXRlIiwgImFjY291bnRfaWQiOiBhY2NvdW50X
2lkLAogICAgICAgICAgICAgICAibmFtZSI6ICJUZXN0IiwgImJhc2VfY3VycmVuY3kiOiAiVVNEIiwK
ICAgICAgICAgICAgICAgImluaXRpYWxfYmFsYW5jZSI6IGluaXRpYWxfYmFsYW5jZSwKICAgICAgICA
gICAgICAgIm1hcmdpbl9wYXJhbXMiOiB7Im1hcmdpbl9yYXRlIjogIjAuNSJ9fQogICAgcjEgPSAoYX
dhaXQgY2xpZW50LnBvc3QoZiJ7UFR9L2FjY291bnRzIiwgaGVhZGVycz1oZWFkZXJzLAogICAgICAgI
CAgICAgICAgICAgICAgICAgICAganNvbj1wYXlsb2FkKSkuanNvbigpCiAgICBhc3NlcnQgcjFbIm91
dGNvbWUiXSA9PSAicGVuZGluZ19jb25maXJtYXRpb24iLCByMQogICAgcjIgPSAoYXdhaXQgY2xpZW5
0LnBvc3QoZiJ7UFR9L2FjY291bnRzL2NvbmZpcm0iLCBoZWFkZXJzPWhlYWRlcnMsCiAgICAgICAgIC
AgICAgICAgICAgICAgICAgICBqc29uPXsqKnBheWxvYWQsCiAgICAgICAgICAgICAgICAgICAgICAgI
CAgICAgICAgICAiY29uZmlybWF0aW9uX3JlZiI6CiAgICAgICAgICAgICAgICAgICAgICAgICAgICAg
ICAgICByMVsiY29uZmlybWF0aW9uX3JlZiJdfSkpLmpzb24oKQogICAgYXNzZXJ0IHIyWyJvdXRjb21
lIl0gPT0gImFwcGxpZWQiLCByMgogICAgcmV0dXJuIHIyWyJyZWNvcmRfaWQiXQoKCmFzeW5jIGRlZi
Bfb3JkZXIoY2xpZW50LCBoZWFkZXJzLCBhY2NvdW50X2lkPSJhY2N0LTEiLCBxdWFudGl0eT0iMSIsC
iAgICAgICAgICAgICAgICAgaWRlbT1Ob25lLCBiYXJzPU5vbmUsIG9yZGVyX3R5cGU9Im1hcmtldCIs
CiAgICAgICAgICAgICAgICAgbGltaXRfcHJpY2U9Tm9uZSkgLT4gZGljdDoKICAgIHJldHVybiAoYXd
haXQgY2xpZW50LnBvc3QoZiJ7UFR9L29yZGVycyIsIGhlYWRlcnM9aGVhZGVycywganNvbj17CiAgIC
AgICAgImFjY291bnRfaWQiOiBhY2NvdW50X2lkLCAiaW5zdHJ1bWVudF9pZCI6ICJmb3JleC5ldXJ1c
2QiLAogICAgICAgICJzaWRlIjogImJ1eSIsICJvcmRlcl90eXBlIjogb3JkZXJfdHlwZSwgInF1YW50
aXR5IjogcXVhbnRpdHksCiAgICAgICAgImxpbWl0X3ByaWNlIjogbGltaXRfcHJpY2UsCiAgICAgICA
gImlkZW1wb3RlbmN5X2tleSI6IGlkZW0gb3IgZiJrLXt1dWlkNCgpLmhleFs6OF19IiwKICAgICAgIC
Aic25hcHNob3RfcmVmIjogInNuYXAtMSIsICJiYXJzIjogYmFycyBvciBfYmFycygpLAogICAgICAgI
CJ3aW5kb3dfc3RhcnQiOiAiMjAyNi0wOS0wMVQwMDowMDowMCswMDowMCIsCiAgICAgICAgIndpbmRv
d19lbmQiOiAiMjAyNi0wOS0wMVQxMDowMDowMCswMDowMCJ9KSkuanNvbigpCgoKIyAtLS0gRTE6IGV
uZC10by1lbmQgbGlmZWN5Y2xlIC0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS
0tLS0tLS0tLS0tLS0KCgpAcHl0ZXN0Lm1hcmsuYXN5bmNpbwphc3luYyBkZWYgdGVzdF9lMV9mdWxsX
2xpZmVjeWNsZV9kcmFmdF90b19zZXR0bGVkKHBhcGVyX2NsaWVudCk6CiAgICBoZWFkZXJzID0gYXdh
aXQgX2FkbWluKHBhcGVyX2NsaWVudCkKICAgIGF3YWl0IF9hY2NvdW50KHBhcGVyX2NsaWVudCwgaGV
hZGVycykKICAgIHBsYWNlZCA9IGF3YWl0IF9vcmRlcihwYXBlcl9jbGllbnQsIGhlYWRlcnMpCiAgIC
Bhc3NlcnQgcGxhY2VkWyJvdXRjb21lIl0gPT0gInJlZ2lzdGVyZWQiCiAgICBhc3NlcnQgcGxhY2VkW
yJkZWNpc2lvbiJdID09ICJwYXNzIgogICAgYXNzZXJ0IHBsYWNlZFsic3RhdGUiXSA9PSAicmlza19w
YXNzZWQiCiAgICBvcmRlcl9pZCA9IHBsYWNlZFsib3JkZXJfaWQiXQoKICAgIHJ1biA9IChhd2FpdCB
wYXBlcl9jbGllbnQucG9zdCgKICAgICAgICBmIntQVH0vb3JkZXJzL3tvcmRlcl9pZH0vcnVuIiwgaG
VhZGVycz1oZWFkZXJzLAogICAgICAgIGpzb249eyJiYXJzIjogX2JhcnMoKSwgImNvc3RfbW9kZWwiO
iBBTk5FWF9DT1NUU30pKS5qc29uKCkKICAgIGFzc2VydCBydW5bIm91dGNvbWUiXSA9PSAiZmlsbGVk
IiwgcnVuCiAgICBhc3NlcnQgcnVuWyJzdGF0ZSJdID09ICJzZXR0bGVkIgogICAgZm9yIGYgaW4gcnV
uWyJmaWxscyJdOgogICAgICAgIGFzc2VydCBmWyJmaWxsX2NsYXNzIl0gPT0gInBhcGVyX3NpbXVsYX
RlZCIKICAgIGFzc2VydCAicGFwZXItc2ltdWxhdGVkIiBpbiBydW5bImRpc2NsYWltZXIiXQoKICAgI
GV2ZW50cyA9IChhd2FpdCBwYXBlcl9jbGllbnQuZ2V0KAogICAgICAgIGYie1BUfS9vcmRlcnMve29y
ZGVyX2lkfS9ldmVudHMiLCBoZWFkZXJzPWhlYWRlcnMpKS5qc29uKClbImV2ZW50cyJdCiAgICBjaGF
pbiA9IFsoZVsiZnJvbV9zdGF0ZSJdLCBlWyJ0b19zdGF0ZSJdKSBmb3IgZSBpbiBldmVudHNdCiAgIC
Bhc3NlcnQgY2hhaW4gPT0gWygiZHJhZnQiLCAidmFsaWRhdGVkIiksICgidmFsaWRhdGVkIiwgInJpc
2tfcGFzc2VkIiksCiAgICAgICAgICAgICAgICAgICAgICgicmlza19wYXNzZWQiLCAiZXhlY3V0aW5n
IiksICgiZXhlY3V0aW5nIiwgImZpbGxlZCIpLAogICAgICAgICAgICAgICAgICAgICAoImZpbGxlZCI
sICJzZXR0bGVkIildCgogICAgYmFsYW5jZXMgPSAoYXdhaXQgcGFwZXJfY2xpZW50LmdldCgKICAgIC
AgICBmIntQVH0vYmFsYW5jZXMiLCBoZWFkZXJzPWhlYWRlcnMpKS5qc29uKClbImJhbGFuY2VzIl0KI
CAgIGFzc2VydCBiYWxhbmNlcywgImJhbGFuY2Ugc25hcHNob3Qgd3JpdHRlbiIKICAgIHJlY29ucyA9
IChhd2FpdCBwYXBlcl9jbGllbnQuZ2V0KAogICAgICAgIGYie1BUfS9yZWNvbmNpbGlhdGlvbnMiLCB
oZWFkZXJzPWhlYWRlcnMpKS5qc29uKClbInJlY29uY2lsaWF0aW9ucyJdCiAgICBhc3NlcnQgcmVjb2
5zIGFuZCByZWNvbnNbMF1bIm91dGNvbWUiXSA9PSAiY29uc2lzdGVudCIKCiAgICBhc3luYyB3aXRoI
HNlc3Npb25fc2NvcGUoKSBhcyBzZXNzaW9uOgogICAgICAgIGF1ZGl0cyA9IHthIGZvciAoYSwpIGlu
IChhd2FpdCBzZXNzaW9uLmV4ZWN1dGUoCiAgICAgICAgICAgIHNlbGVjdChWMkF1ZGl0RXZlbnQuYWN
0aW9uKS53aGVyZSgKICAgICAgICAgICAgICAgIFYyQXVkaXRFdmVudC5kb21haW4gPT0gInYyLnBhcG
VyX3RyYWRpbmciKSkpLmFsbCgpfQogICAgZm9yIGV4cGVjdGVkIGluICgicGFwZXIuYWNjb3VudC5jc
mVhdGVkIiwgInBhcGVyLnJpc2sucGFzc2VkIiwKICAgICAgICAgICAgICAgICAgICAgInBhcGVyLm9y
ZGVyLmV4ZWN1dGVkIiwKICAgICAgICAgICAgICAgICAgICAgInBhcGVyLnJlY29uY2lsaWF0aW9uLmN
vbXBsZXRlZCIpOgogICAgICAgIGFzc2VydCBleHBlY3RlZCBpbiBhdWRpdHMsIGV4cGVjdGVkCgoKQH
B5dGVzdC5tYXJrLmFzeW5jaW8KYXN5bmMgZGVmIHRlc3RfZTFfcGFydGlhbF9maWxsX3ZvaWRlZF9yZ
W1haW5kZXIocGFwZXJfY2xpZW50KToKICAgICIiIkFOTkVYLVAgQ2FzZSBBIHRocm91Z2ggdGhlIEFQ
STogMiBmaWxscyBAOTcuNjUsIHJlbWFpbmRlciB2b2lkZWQuIiIiCiAgICBoZWFkZXJzID0gYXdhaXQ
gX2FkbWluKHBhcGVyX2NsaWVudCkKICAgIGF3YWl0IF9hY2NvdW50KHBhcGVyX2NsaWVudCwgaGVhZG
VycykKICAgIHBsYWNlZCA9IGF3YWl0IF9vcmRlcihwYXBlcl9jbGllbnQsIGhlYWRlcnMsIHF1YW50a
XR5PSI1IiwKICAgICAgICAgICAgICAgICAgICAgICAgICBvcmRlcl90eXBlPSJsaW1pdCIsIGxpbWl0
X3ByaWNlPSI5Ny41IikKICAgIGFzc2VydCBwbGFjZWRbImRlY2lzaW9uIl0gPT0gInBhc3MiCiAgICB
ydW4gPSAoYXdhaXQgcGFwZXJfY2xpZW50LnBvc3QoCiAgICAgICAgZiJ7UFR9L29yZGVycy97cGxhY2
VkWydvcmRlcl9pZCddfS9ydW4iLCBoZWFkZXJzPWhlYWRlcnMsCiAgICAgICAganNvbj17ImJhcnMiO
iBfYmFycygpLCAiY29zdF9tb2RlbCI6IEFOTkVYX0NPU1RTfSkpLmpzb24oKQogICAgYXNzZXJ0IHJ1
blsib3V0Y29tZSJdID09ICJwYXJ0aWFsbHlfZmlsbGVkIgogICAgYXNzZXJ0IHJ1blsic3RhdGUiXSA
9PSAic2V0dGxlZCIKICAgIGFzc2VydCBsZW4ocnVuWyJmaWxscyJdKSA9PSAyCiAgICBhc3NlcnQgYW
xsKGZbImVmZmVjdGl2ZV9wcmljZSJdID09ICI5Ny42NSIgZm9yIGYgaW4gcnVuWyJmaWxscyJdKQogI
CAgZXZlbnRzID0gKGF3YWl0IHBhcGVyX2NsaWVudC5nZXQoCiAgICAgICAgZiJ7UFR9L29yZGVycy97
cGxhY2VkWydvcmRlcl9pZCddfS9ldmVudHMiLAogICAgICAgIGhlYWRlcnM9aGVhZGVycykpLmpzb24
oKVsiZXZlbnRzIl0KICAgIHNldHRsZWQgPSBbZSBmb3IgZSBpbiBldmVudHMgaWYgZVsiZXZlbnRfY2
xhc3MiXSA9PSAib3JkZXIuc2V0dGxlZCJdCiAgICBhc3NlcnQgc2V0dGxlZCBhbmQgc2V0dGxlZFswX
VsiZGV0YWlscyJdWyJ2b2lkZWRfcmVtYWluZGVyIl0gPT0gIjEiCgoKIyAtLS0gRTI6IGlkZW1wb3Rl
bmN5IC8gcmVwbGF5IC8gcmFjZSAtLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0
tLS0tLS0tCgoKQHB5dGVzdC5tYXJrLmFzeW5jaW8KYXN5bmMgZGVmIHRlc3RfZTJfaWRlbXBvdGVuY3
lfa2V5X3JldXNlKHBhcGVyX2NsaWVudCk6CiAgICBoZWFkZXJzID0gYXdhaXQgX2FkbWluKHBhcGVyX
2NsaWVudCkKICAgIGF3YWl0IF9hY2NvdW50KHBhcGVyX2NsaWVudCwgaGVhZGVycykKICAgIGZpcnN0
ID0gYXdhaXQgX29yZGVyKHBhcGVyX2NsaWVudCwgaGVhZGVycywgaWRlbT0iaWRlbS0xIikKICAgIHN
lY29uZCA9IGF3YWl0IF9vcmRlcihwYXBlcl9jbGllbnQsIGhlYWRlcnMsIGlkZW09ImlkZW0tMSIpCi
AgICBhc3NlcnQgZmlyc3RbIm91dGNvbWUiXSA9PSAicmVnaXN0ZXJlZCIKICAgIGFzc2VydCBzZWNvb
mRbIm91dGNvbWUiXSA9PSAicmV1c2VkIgogICAgYXNzZXJ0IHNlY29uZFsib3JkZXJfaWQiXSA9PSBm
aXJzdFsib3JkZXJfaWQiXQogICAgYXN5bmMgd2l0aCBzZXNzaW9uX3Njb3BlKCkgYXMgc2Vzc2lvbjo
KICAgICAgICBkZWNpc2lvbnMgPSBsaXN0KChhd2FpdCBzZXNzaW9uLmV4ZWN1dGUoCiAgICAgICAgIC
AgIHNlbGVjdChWMlBhcGVyUmlza0RlY2lzaW9uKS53aGVyZSgKICAgICAgICAgICAgICAgIFYyUGFwZ
XJSaXNrRGVjaXNpb24uaW50ZW50X2lkID09IGZpcnN0WyJvcmRlcl9pZCJdKQogICAgICAgICkpLnNj
YWxhcnMoKS5hbGwoKSkKICAgICAgICBhc3NlcnQgbGVuKGRlY2lzaW9ucykgPT0gMSAgIyBleGFjdGx
5LW9uY2UgcmlzayBldmFsdWF0aW9uIGhlbGQKICAgICAgICBhdWRpdHMgPSBbYSBmb3IgKGEsKSBpbi
AoYXdhaXQgc2Vzc2lvbi5leGVjdXRlKAogICAgICAgICAgICBzZWxlY3QoVjJBdWRpdEV2ZW50LmFjd
Glvbikud2hlcmUoCiAgICAgICAgICAgICAgICBWMkF1ZGl0RXZlbnQuYWN0aW9uID09ICJwYXBlci5v
cmRlci5yZXVzZWQiKSkpLmFsbCgpXQogICAgICAgIGFzc2VydCBhdWRpdHMKCgpAcHl0ZXN0Lm1hcms
uYXN5bmNpbwphc3luYyBkZWYgdGVzdF9lMl9yZXJ1bl9jb252ZXJnZXNfbm9fc2Vjb25kX2ZpbGxfc2
V0KHBhcGVyX2NsaWVudCk6CiAgICBoZWFkZXJzID0gYXdhaXQgX2FkbWluKHBhcGVyX2NsaWVudCkKI
CAgIGF3YWl0IF9hY2NvdW50KHBhcGVyX2NsaWVudCwgaGVhZGVycykKICAgIHBsYWNlZCA9IGF3YWl0
IF9vcmRlcihwYXBlcl9jbGllbnQsIGhlYWRlcnMpCiAgICBydW4xID0gKGF3YWl0IHBhcGVyX2NsaWV
udC5wb3N0KAogICAgICAgIGYie1BUfS9vcmRlcnMve3BsYWNlZFsnb3JkZXJfaWQnXX0vcnVuIiwgaG
VhZGVycz1oZWFkZXJzLAogICAgICAgIGpzb249eyJiYXJzIjogX2JhcnMoKSwgImNvc3RfbW9kZWwiO
iBBTk5FWF9DT1NUU30pKS5qc29uKCkKICAgIGFzc2VydCBydW4xWyJvdXRjb21lIl0gPT0gImZpbGxl
ZCIKICAgIHJ1bjIgPSAoYXdhaXQgcGFwZXJfY2xpZW50LnBvc3QoCiAgICAgICAgZiJ7UFR9L29yZGV
ycy97cGxhY2VkWydvcmRlcl9pZCddfS9ydW4iLCBoZWFkZXJzPWhlYWRlcnMsCiAgICAgICAganNvbj
17ImJhcnMiOiBfYmFycygpLCAiY29zdF9tb2RlbCI6IEFOTkVYX0NPU1RTfSkpLmpzb24oKQogICAgY
XNzZXJ0IHJ1bjJbIm91dGNvbWUiXSA9PSAicmVmdXNlZCIgICMgc2V0dGxlZDogb25seSByaXNrX3Bh
c3NlZCBydW5zCiAgICBhc3luYyB3aXRoIHNlc3Npb25fc2NvcGUoKSBhcyBzZXNzaW9uOgogICAgICA
gIGZpbGxzID0gbGlzdCgoYXdhaXQgc2Vzc2lvbi5leGVjdXRlKAogICAgICAgICAgICBzZWxlY3QoVj
JQYXBlckZpbGwpLndoZXJlKAogICAgICAgICAgICAgICAgVjJQYXBlckZpbGwuaW50ZW50X2lkID09I
HBsYWNlZFsib3JkZXJfaWQiXSkKICAgICAgICApKS5zY2FsYXJzKCkuYWxsKCkpCiAgICAgICAgYXNz
ZXJ0IGxlbihmaWxscykgPT0gMSAgIyBubyBzZWNvbmQgYXJ0aWZhY3Qgc2V0CgoKIyAtLS0gRTM6IGZ
haWx1cmUgdGF4b25vbXkgLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS
0tLS0tLS0tLS0tLS0tCgoKQHB5dGVzdC5tYXJrLmFzeW5jaW8KYXN5bmMgZGVmIHRlc3RfZTNfcmlza
19ibG9ja19saW1pdF9uYW1lZF9hbmRfbWVhc3VyZWQocGFwZXJfY2xpZW50KToKICAgIGhlYWRlcnMg
PSBhd2FpdCBfYWRtaW4ocGFwZXJfY2xpZW50KQogICAgYXdhaXQgX2FjY291bnQocGFwZXJfY2xpZW5
0LCBoZWFkZXJzKQogICAgcGxhY2VkID0gYXdhaXQgX29yZGVyKHBhcGVyX2NsaWVudCwgaGVhZGVycy
wgcXVhbnRpdHk9Ijk5OTk5OTk5IikKICAgIGFzc2VydCBwbGFjZWRbImRlY2lzaW9uIl0gPT0gImJsb
2NrIgogICAgYXNzZXJ0IHBsYWNlZFsic3RhdGUiXSA9PSAicmlza19ibG9ja2VkIgogICAgYXNzZXJ0
IGFueShyWyJmYWlsaW5nIl0gPT0gIm1heF9vcmRlcl9xdWFudGl0eSIKICAgICAgICAgICAgICAgZm9
yIHIgaW4gcGxhY2VkWyJyZWFzb25zIl0pCiAgICBhc3luYyB3aXRoIHNlc3Npb25fc2NvcGUoKSBhcy
BzZXNzaW9uOgogICAgICAgIGQgPSAoYXdhaXQgc2Vzc2lvbi5leGVjdXRlKAogICAgICAgICAgICBzZ
WxlY3QoVjJQYXBlclJpc2tEZWNpc2lvbikud2hlcmUoCiAgICAgICAgICAgICAgICBWMlBhcGVyUmlz
a0RlY2lzaW9uLmludGVudF9pZCA9PSBwbGFjZWRbIm9yZGVyX2lkIl0pCiAgICAgICAgKSkuc2NhbGF
yX29uZSgpCiAgICAgICAgYXNzZXJ0IGQuZGVjaXNpb24gPT0gImJsb2NrIgogICAgICAgIGFzc2VydC
BkLmNvbmZpcm1hdGlvbl9yZWYgaXMgTm9uZSAgIyBDLTFkOiBubyByZWYgbWludGVkCiAgICAgICAgY
XNzZXJ0IGQuZXZhbHVhdGVkX2xpbWl0c1sibWF4X29yZGVyX3F1YW50aXR5Il1bInZlcmRpY3QiXSA9
PSAiZmFpbCIKICAgICAgICBhc3NlcnQgZC5yaXNrX2NvbmZpZ192ZXJzaW9uID09ICJwcmMtMSIKCgp
AcHl0ZXN0Lm1hcmsuYXN5bmNpbwphc3luYyBkZWYgdGVzdF9lM192YWxpZGF0aW9uX3JlamVjdGVkKH
BhcGVyX2NsaWVudCk6CiAgICBoZWFkZXJzID0gYXdhaXQgX2FkbWluKHBhcGVyX2NsaWVudCkKICAgI
GF3YWl0IF9hY2NvdW50KHBhcGVyX2NsaWVudCwgaGVhZGVycykKICAgIHIgPSAoYXdhaXQgcGFwZXJf
Y2xpZW50LnBvc3QoZiJ7UFR9L29yZGVycyIsIGhlYWRlcnM9aGVhZGVycywganNvbj17CiAgICAgICA
gImFjY291bnRfaWQiOiAiYWNjdC0xIiwgImluc3RydW1lbnRfaWQiOiAiZm9yZXguZXVydXNkIiwKIC
AgICAgICAic2lkZSI6ICJob2xkLW1lIiwgIm9yZGVyX3R5cGUiOiAibWFya2V0IiwgInF1YW50aXR5I
jogIi0xIiwKICAgICAgICAiaWRlbXBvdGVuY3lfa2V5IjogImstYmFkIiwgInNuYXBzaG90X3JlZiI6
ICJzIiwKICAgICAgICAiYmFycyI6IFtdfSkpLmpzb24oKQogICAgYXNzZXJ0IHJbIm91dGNvbWUiXSA
9PSAicmVqZWN0ZWQiCiAgICBmYWlsaW5nID0ge3hbImZhaWxpbmciXSBmb3IgeCBpbiByWyJyZWFzb2
5zIl19CiAgICBhc3NlcnQgeyJzaWRlIiwgInF1YW50aXR5IiwgImJhcnMifSA8PSBmYWlsaW5nCgoKQ
HB5dGVzdC5tYXJrLmFzeW5jaW8KYXN5bmMgZGVmIHRlc3RfZTNfZXhwaXJlZF93aW5kb3dfZXhoYXVz
dGlvbihwYXBlcl9jbGllbnQpOgogICAgaGVhZGVycyA9IGF3YWl0IF9hZG1pbihwYXBlcl9jbGllbnQ
pCiAgICBhd2FpdCBfYWNjb3VudChwYXBlcl9jbGllbnQsIGhlYWRlcnMpCiAgICBwbGFjZWQgPSBhd2
FpdCBfb3JkZXIocGFwZXJfY2xpZW50LCBoZWFkZXJzLCBvcmRlcl90eXBlPSJsaW1pdCIsCiAgICAgI
CAgICAgICAgICAgICAgICAgICAgbGltaXRfcHJpY2U9IjUwIiwgcXVhbnRpdHk9IjEiKQogICAgYXNz
ZXJ0IHBsYWNlZFsiZGVjaXNpb24iXSA9PSAicGFzcyIKICAgIHJ1biA9IChhd2FpdCBwYXBlcl9jbGl
lbnQucG9zdCgKICAgICAgICBmIntQVH0vb3JkZXJzL3twbGFjZWRbJ29yZGVyX2lkJ119L3J1biIsIG
hlYWRlcnM9aGVhZGVycywKICAgICAgICBqc29uPXsiYmFycyI6IF9iYXJzKCksICJjb3N0X21vZGVsI
jogQU5ORVhfQ09TVFN9KSkuanNvbigpCiAgICBhc3NlcnQgcnVuWyJvdXRjb21lIl0gPT0gImV4cGly
ZWQiCiAgICBhc3NlcnQgcnVuWyJzdGF0ZSJdID09ICJleHBpcmVkIgoKCkBweXRlc3QubWFyay5hc3l
uY2lvCmFzeW5jIGRlZiB0ZXN0X2UzX3F1YXJhbnRpbmVfb25fc25hcHNob3RfdGFtcGVyKHBhcGVyX2
NsaWVudCk6CiAgICAiIiJTMi41L1E2OiBjb250ZW50IG1pc21hdGNoIGF0IHJ1biA9PiBxdWFyYW50a
W5lZF91bmtub3duIHRlcm1pbmFsLiIiIgogICAgaGVhZGVycyA9IGF3YWl0IF9hZG1pbihwYXBlcl9j
bGllbnQpCiAgICBhd2FpdCBfYWNjb3VudChwYXBlcl9jbGllbnQsIGhlYWRlcnMpCiAgICBwbGFjZWQ
gPSBhd2FpdCBfb3JkZXIocGFwZXJfY2xpZW50LCBoZWFkZXJzKQogICAgdGFtcGVyZWQgPSBfYmFycy
hjbG9zZXM9WyI1MCJdICogMTApCiAgICBydW4gPSAoYXdhaXQgcGFwZXJfY2xpZW50LnBvc3QoCiAgI
CAgICAgZiJ7UFR9L29yZGVycy97cGxhY2VkWydvcmRlcl9pZCddfS9ydW4iLCBoZWFkZXJzPWhlYWRl
cnMsCiAgICAgICAganNvbj17ImJhcnMiOiB0YW1wZXJlZCwgImNvc3RfbW9kZWwiOiBBTk5FWF9DT1N
UU30pKS5qc29uKCkKICAgIGFzc2VydCBydW5bIm91dGNvbWUiXSA9PSAicXVhcmFudGluZWQiCiAgIC
Bhc3NlcnQgcnVuWyJzdGF0ZSJdID09ICJxdWFyYW50aW5lZF91bmtub3duIgogICAgYXN5bmMgd2l0a
CBzZXNzaW9uX3Njb3BlKCkgYXMgc2Vzc2lvbjoKICAgICAgICBhdWRpdHMgPSBbYSBmb3IgKGEsKSBp
biAoYXdhaXQgc2Vzc2lvbi5leGVjdXRlKAogICAgICAgICAgICBzZWxlY3QoVjJBdWRpdEV2ZW50LmF
jdGlvbikud2hlcmUoCiAgICAgICAgICAgICAgICBWMkF1ZGl0RXZlbnQuYWN0aW9uID09ICJwYXBlci
5vcmRlci5xdWFyYW50aW5lZCIpKSkuYWxsKCldCiAgICAgICAgYXNzZXJ0IGF1ZGl0cwoKCiMgLS0tI
EMtMSBob2xkIHNlYW0gKFMyLjYpIC0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0t
LS0tLS0tLS0tLS0tLS0tLS0tLQoKCkhFTERfQkFSUyA9IE5vbmUgICMgc2V0IHBlciBjYWxsOiB0aGU
gU0FNRSBiYXJzIG11c3QgYmUgcGlubmVkIGFuZCByZXBsYXllZAoKCmFzeW5jIGRlZiBfaGVsZF9vcm
RlcihjbGllbnQsIGhlYWRlcnMsIGJhcnM9Tm9uZSkgLT4gZGljdDoKICAgICIiIk5vdGlvbmFsIGluc
2lkZSB0aGUgaG9sZCBiYW5kOiBbODBrLCAxMDBrXSA9PiBxdHkgODUwIEAgfjEwMC4KICAgIFRoZSBi
YXJzIGdpdmVuIGhlcmUgYXJlIGNvbnRlbnQtcGlubmVkIG9uIHRoZSBpbnRlbnQgKFM0LjEpIOKAlCB
hbnkKICAgIGxhdGVyIHJ1biBNVVNUIHJlcGxheSB0aGUgc2FtZSBieXRlcyBvciBiZSBxdWFyYW50aW
5lZC4iIiIKICAgIHBsYWNlZCA9IGF3YWl0IF9vcmRlcihjbGllbnQsIGhlYWRlcnMsIHF1YW50aXR5P
SI4NTAiLCBiYXJzPWJhcnMpCiAgICBhc3NlcnQgcGxhY2VkWyJkZWNpc2lvbiJdID09ICJob2xkIiwg
cGxhY2VkCiAgICBhc3NlcnQgcGxhY2VkWyJzdGF0ZSJdID09ICJyaXNrX2hvbGQiCiAgICBhc3NlcnQ
gcGxhY2VkWyJjb25maXJtYXRpb25fcmVmIl0KICAgIHJldHVybiBwbGFjZWQKCgpAcHl0ZXN0Lm1hcm
suYXN5bmNpbwphc3luYyBkZWYgdGVzdF9jMV9ob2xkX2NvbmZpcm1fdGhlbl9leGVjdXRlKHBhcGVyX
2NsaWVudCk6CiAgICBoZWFkZXJzID0gYXdhaXQgX2FkbWluKHBhcGVyX2NsaWVudCkKICAgIGF3YWl0
IF9hY2NvdW50KHBhcGVyX2NsaWVudCwgaGVhZGVycykKICAgIGxpcXVpZF9iYXJzID0gX2JhcnMobGl
xdWlkaXR5PSIxMDAwIikgICMgcGlubmVkIGF0IHBsYWNlbWVudCAoUzQuMSkKICAgIGhlbGQgPSBhd2
FpdCBfaGVsZF9vcmRlcihwYXBlcl9jbGllbnQsIGhlYWRlcnMsIGJhcnM9bGlxdWlkX2JhcnMpCiAgI
CBjb25maXJtZWQgPSAoYXdhaXQgcGFwZXJfY2xpZW50LnBvc3QoCiAgICAgICAgZiJ7UFR9L29yZGVy
cy9jb25maXJtIiwgaGVhZGVycz1oZWFkZXJzLAogICAgICAgIGpzb249eyJvcmRlcl9pZCI6IGhlbGR
bIm9yZGVyX2lkIl0sCiAgICAgICAgICAgICAgImNvbmZpcm1hdGlvbl9yZWYiOiBoZWxkWyJjb25maX
JtYXRpb25fcmVmIl0sCiAgICAgICAgICAgICAgInJlc29sdmVfdG8iOiAiY29uZmlybSJ9KSkuanNvb
igpCiAgICBhc3NlcnQgY29uZmlybWVkWyJvdXRjb21lIl0gPT0gImFwcGxpZWQiCiAgICBhc3NlcnQg
Y29uZmlybWVkWyJzdGF0ZSJdID09ICJyaXNrX3Bhc3NlZCIKICAgIHJ1biA9IChhd2FpdCBwYXBlcl9
jbGllbnQucG9zdCgKICAgICAgICBmIntQVH0vb3JkZXJzL3toZWxkWydvcmRlcl9pZCddfS9ydW4iLC
BoZWFkZXJzPWhlYWRlcnMsCiAgICAgICAganNvbj17ImJhcnMiOiBsaXF1aWRfYmFycywgICMgc2FtZ
SBwaW5uZWQgYnl0ZXMgcmVwbGF5ZWQKICAgICAgICAgICAgICAiY29zdF9tb2RlbCI6IEFOTkVYX0NP
U1RTfSkpLmpzb24oKQogICAgYXNzZXJ0IHJ1blsib3V0Y29tZSJdID09ICJmaWxsZWQiCiAgICBhc3l
uYyB3aXRoIHNlc3Npb25fc2NvcGUoKSBhcyBzZXNzaW9uOgogICAgICAgIGQgPSAoYXdhaXQgc2Vzc2
lvbi5leGVjdXRlKAogICAgICAgICAgICBzZWxlY3QoVjJQYXBlclJpc2tEZWNpc2lvbikud2hlcmUoC
iAgICAgICAgICAgICAgICBWMlBhcGVyUmlza0RlY2lzaW9uLmludGVudF9pZCA9PSBoZWxkWyJvcmRl
cl9pZCJdKQogICAgICAgICkpLnNjYWxhcl9vbmUoKQogICAgICAgIGFzc2VydCBkLmRlY2lzaW9uID0
9ICJob2xkIiAgIyB0aGUgcm93IE5FVkVSIG11dGF0ZXMgKEMtMWEpCiAgICAgICAgZXZlbnRzID0gbG
lzdCgoYXdhaXQgc2Vzc2lvbi5leGVjdXRlKAogICAgICAgICAgICBzZWxlY3QoVjJQYXBlck9yZGVyR
XZlbnQpLndoZXJlKAogICAgICAgICAgICAgICAgVjJQYXBlck9yZGVyRXZlbnQuaW50ZW50X2lkID09
IGhlbGRbIm9yZGVyX2lkIl0pCiAgICAgICAgKSkuc2NhbGFycygpLmFsbCgpKQogICAgICAgIGNvbmZ
pcm1zID0gW2UgZm9yIGUgaW4gZXZlbnRzIGlmIGUuZXZlbnRfY2xhc3MgPT0gImhvbGQuY29uZmlybW
VkIl0KICAgICAgICBhc3NlcnQgbGVuKGNvbmZpcm1zKSA9PSAxCiAgICAgICAgYXNzZXJ0IGNvbmZpc
m1zWzBdLmRldGFpbHNbImNvbmZpcm1hdGlvbl9yZWYiXSA9PSBkLmNvbmZpcm1hdGlvbl9yZWYKCgpA
cHl0ZXN0Lm1hcmsuYXN5bmNpbwphc3luYyBkZWYgdGVzdF9jMV9ob2xkX2NhbmNlbChwYXBlcl9jbGl
lbnQpOgogICAgaGVhZGVycyA9IGF3YWl0IF9hZG1pbihwYXBlcl9jbGllbnQpCiAgICBhd2FpdCBfYW
Njb3VudChwYXBlcl9jbGllbnQsIGhlYWRlcnMpCiAgICBoZWxkID0gYXdhaXQgX2hlbGRfb3JkZXIoc
GFwZXJfY2xpZW50LCBoZWFkZXJzKQogICAgY2FuY2VsbGVkID0gKGF3YWl0IHBhcGVyX2NsaWVudC5w
b3N0KAogICAgICAgIGYie1BUfS9vcmRlcnMvY29uZmlybSIsIGhlYWRlcnM9aGVhZGVycywKICAgICA
gICBqc29uPXsib3JkZXJfaWQiOiBoZWxkWyJvcmRlcl9pZCJdLAogICAgICAgICAgICAgICJjb25maX
JtYXRpb25fcmVmIjogaGVsZFsiY29uZmlybWF0aW9uX3JlZiJdLAogICAgICAgICAgICAgICJyZXNvb
HZlX3RvIjogImNhbmNlbCJ9KSkuanNvbigpCiAgICBhc3NlcnQgY2FuY2VsbGVkWyJvdXRjb21lIl0g
PT0gImFwcGxpZWQiCiAgICBhc3NlcnQgY2FuY2VsbGVkWyJzdGF0ZSJdID09ICJjYW5jZWxsZWQiCiA
gICBhc3luYyB3aXRoIHNlc3Npb25fc2NvcGUoKSBhcyBzZXNzaW9uOgogICAgICAgIGF1ZGl0cyA9IF
thIGZvciAoYSwpIGluIChhd2FpdCBzZXNzaW9uLmV4ZWN1dGUoCiAgICAgICAgICAgIHNlbGVjdChWM
kF1ZGl0RXZlbnQuYWN0aW9uKS53aGVyZSgKICAgICAgICAgICAgICAgIFYyQXVkaXRFdmVudC5hY3Rp
b24gPT0gInBhcGVyLm9yZGVyLmhvbGRfY2FuY2VsbGVkIikpKS5hbGwoKV0KICAgICAgICBhc3NlcnQ
gYXVkaXRzCgoKQHB5dGVzdC5tYXJrLmFzeW5jaW8KYXN5bmMgZGVmIHRlc3RfYzFfZm91cl9yZWZ1c2
FsX2NsYXNzZXMocGFwZXJfY2xpZW50KToKICAgICIiIkMtMWIuNDogZG91YmxlLWNvbmZpcm0sIHdyb
25nLXJlZiwgc3RhbGUtYWZ0ZXItY2FuY2VsLAogICAgbm90LWNvbmZpcm1hYmxlIOKAlCBlYWNoIHR5
cGVkICsgZHVyYWJseSBhdWRpdGVkLiIiIgogICAgaGVhZGVycyA9IGF3YWl0IF9hZG1pbihwYXBlcl9
jbGllbnQpCiAgICBhd2FpdCBfYWNjb3VudChwYXBlcl9jbGllbnQsIGhlYWRlcnMpCgogICAgIyB3cm
9uZy1yZWYKICAgIGhlbGQgPSBhd2FpdCBfaGVsZF9vcmRlcihwYXBlcl9jbGllbnQsIGhlYWRlcnMpC
iAgICByID0gKGF3YWl0IHBhcGVyX2NsaWVudC5wb3N0KAogICAgICAgIGYie1BUfS9vcmRlcnMvY29u
ZmlybSIsIGhlYWRlcnM9aGVhZGVycywKICAgICAgICBqc29uPXsib3JkZXJfaWQiOiBoZWxkWyJvcmR
lcl9pZCJdLCAiY29uZmlybWF0aW9uX3JlZiI6ICJmb3JnZWQiLAogICAgICAgICAgICAgICJyZXNvbH
ZlX3RvIjogImNvbmZpcm0ifSkpLmpzb24oKQogICAgYXNzZXJ0IHJbIm91dGNvbWUiXSA9PSAicmVmd
XNlZCIKICAgIGFzc2VydCByWyJyZWFzb25zIl1bMF1bImZhaWxpbmciXSA9PSAicGFwZXIuY29uZmly
bWF0aW9uLnJlZl9taXNtYXRjaCIKCiAgICAjIGRvdWJsZS1jb25maXJtCiAgICBvayA9IChhd2FpdCB
wYXBlcl9jbGllbnQucG9zdCgKICAgICAgICBmIntQVH0vb3JkZXJzL2NvbmZpcm0iLCBoZWFkZXJzPW
hlYWRlcnMsCiAgICAgICAganNvbj17Im9yZGVyX2lkIjogaGVsZFsib3JkZXJfaWQiXSwKICAgICAgI
CAgICAgICAiY29uZmlybWF0aW9uX3JlZiI6IGhlbGRbImNvbmZpcm1hdGlvbl9yZWYiXSwKICAgICAg
ICAgICAgICAicmVzb2x2ZV90byI6ICJjb25maXJtIn0pKS5qc29uKCkKICAgIGFzc2VydCBva1sib3V
0Y29tZSJdID09ICJhcHBsaWVkIgogICAgciA9IChhd2FpdCBwYXBlcl9jbGllbnQucG9zdCgKICAgIC
AgICBmIntQVH0vb3JkZXJzL2NvbmZpcm0iLCBoZWFkZXJzPWhlYWRlcnMsCiAgICAgICAganNvbj17I
m9yZGVyX2lkIjogaGVsZFsib3JkZXJfaWQiXSwKICAgICAgICAgICAgICAiY29uZmlybWF0aW9uX3Jl
ZiI6IGhlbGRbImNvbmZpcm1hdGlvbl9yZWYiXSwKICAgICAgICAgICAgICAicmVzb2x2ZV90byI6ICJ
jb25maXJtIn0pKS5qc29uKCkKICAgIGFzc2VydCByWyJvdXRjb21lIl0gPT0gInJlZnVzZWQiCiAgIC
Bhc3NlcnQgclsicmVhc29ucyJdWzBdWyJmYWlsaW5nIl0gPT0gXAogICAgICAgICJwYXBlci5jb25ma
XJtYXRpb24uYWxyZWFkeV9jb25zdW1lZCIKCiAgICAjIHN0YWxlLWFmdGVyLWNhbmNlbAogICAgaGVs
ZDIgPSBhd2FpdCBfaGVsZF9vcmRlcihwYXBlcl9jbGllbnQsIGhlYWRlcnMpCiAgICAoYXdhaXQgcGF
wZXJfY2xpZW50LnBvc3QoCiAgICAgICAgZiJ7UFR9L29yZGVycy9jb25maXJtIiwgaGVhZGVycz1oZW
FkZXJzLAogICAgICAgIGpzb249eyJvcmRlcl9pZCI6IGhlbGQyWyJvcmRlcl9pZCJdLAogICAgICAgI
CAgICAgICJjb25maXJtYXRpb25fcmVmIjogaGVsZDJbImNvbmZpcm1hdGlvbl9yZWYiXSwKICAgICAg
ICAgICAgICAicmVzb2x2ZV90byI6ICJjYW5jZWwifSkpLmpzb24oKQogICAgciA9IChhd2FpdCBwYXB
lcl9jbGllbnQucG9zdCgKICAgICAgICBmIntQVH0vb3JkZXJzL2NvbmZpcm0iLCBoZWFkZXJzPWhlYW
RlcnMsCiAgICAgICAganNvbj17Im9yZGVyX2lkIjogaGVsZDJbIm9yZGVyX2lkIl0sCiAgICAgICAgI
CAgICAgImNvbmZpcm1hdGlvbl9yZWYiOiBoZWxkMlsiY29uZmlybWF0aW9uX3JlZiJdLAogICAgICAg
ICAgICAgICJyZXNvbHZlX3RvIjogImNvbmZpcm0ifSkpLmpzb24oKQogICAgYXNzZXJ0IHJbIm91dGN
vbWUiXSA9PSAicmVmdXNlZCIKICAgIGFzc2VydCByWyJyZWFzb25zIl1bMF1bImZhaWxpbmciXSA9PS
AicGFwZXIuY29uZmlybWF0aW9uLmNhbmNlbGxlZCIKCiAgICAjIG5vdC1jb25maXJtYWJsZSAocGFzc
yBkZWNpc2lvbikKICAgIHBhc3NlZCA9IGF3YWl0IF9vcmRlcihwYXBlcl9jbGllbnQsIGhlYWRlcnMp
CiAgICBhc3NlcnQgcGFzc2VkWyJkZWNpc2lvbiJdID09ICJwYXNzIgogICAgciA9IChhd2FpdCBwYXB
lcl9jbGllbnQucG9zdCgKICAgICAgICBmIntQVH0vb3JkZXJzL2NvbmZpcm0iLCBoZWFkZXJzPWhlYW
RlcnMsCiAgICAgICAganNvbj17Im9yZGVyX2lkIjogcGFzc2VkWyJvcmRlcl9pZCJdLCAiY29uZmlyb
WF0aW9uX3JlZiI6ICJhbnkiLAogICAgICAgICAgICAgICJyZXNvbHZlX3RvIjogImNvbmZpcm0ifSkp
Lmpzb24oKQogICAgYXNzZXJ0IHJbIm91dGNvbWUiXSA9PSAicmVmdXNlZCIKICAgIGFzc2VydCByWyJ
yZWFzb25zIl1bMF1bImZhaWxpbmciXSA9PSBcCiAgICAgICAgInBhcGVyLmNvbmZpcm1hdGlvbi5ub3
RfY29uZmlybWFibGUiCgogICAgYXN5bmMgd2l0aCBzZXNzaW9uX3Njb3BlKCkgYXMgc2Vzc2lvbjoKI
CAgICAgICByZWZ1c2FscyA9IFthIGZvciAoYSwpIGluIChhd2FpdCBzZXNzaW9uLmV4ZWN1dGUoCiAg
ICAgICAgICAgIHNlbGVjdChWMkF1ZGl0RXZlbnQuYWN0aW9uKS53aGVyZSgKICAgICAgICAgICAgICA
gIFYyQXVkaXRFdmVudC5hY3Rpb24gPT0gInBhcGVyLm9yZGVyLmNvbmZpcm1fcmVmdXNlZCIpKSkuYW
xsKCldCiAgICAgICAgYXNzZXJ0IGxlbihyZWZ1c2FscykgPj0gNCAgIyBldmVyeSByZWZ1c2FsIGR1c
mFibHkgYXVkaXRlZAoKCkBweXRlc3QubWFyay5hc3luY2lvCmFzeW5jIGRlZiB0ZXN0X2MxZF9ibG9j
a191bnJlYWNoYWJsZV9ieV9jb25maXJtYXRpb24ocGFwZXJfY2xpZW50KToKICAgICIiIkMtMWQgYm9
0aCBhcm1zOiAoMSkgY29uZmlybSBvbiBibG9ja2VkID0+IG5vdF9jb25maXJtYWJsZTsKICAgICgyKS
Bmb3JnZWQgcmlza19ibG9ja2VkLT5leGVjdXRpbmcgYXBwZW5kIHJlZnVzZWQgdHlwZWQuIiIiCiAgI
CBoZWFkZXJzID0gYXdhaXQgX2FkbWluKHBhcGVyX2NsaWVudCkKICAgIGF3YWl0IF9hY2NvdW50KHBh
cGVyX2NsaWVudCwgaGVhZGVycykKICAgIGJsb2NrZWQgPSBhd2FpdCBfb3JkZXIocGFwZXJfY2xpZW5
0LCBoZWFkZXJzLCBxdWFudGl0eT0iOTk5OTk5OTkiKQogICAgYXNzZXJ0IGJsb2NrZWRbImRlY2lzaW
9uIl0gPT0gImJsb2NrIgoKICAgICMgYXJtIDE6IGNvbmZpcm1hdGlvbiBhdHRlbXB0CiAgICByID0gK
GF3YWl0IHBhcGVyX2NsaWVudC5wb3N0KAogICAgICAgIGYie1BUfS9vcmRlcnMvY29uZmlybSIsIGhl
YWRlcnM9aGVhZGVycywKICAgICAgICBqc29uPXsib3JkZXJfaWQiOiBibG9ja2VkWyJvcmRlcl9pZCJ
dLCAiY29uZmlybWF0aW9uX3JlZiI6ICJhbnkiLAogICAgICAgICAgICAgICJyZXNvbHZlX3RvIjogIm
NvbmZpcm0ifSkpLmpzb24oKQogICAgYXNzZXJ0IHJbIm91dGNvbWUiXSA9PSAicmVmdXNlZCIKICAgI
GFzc2VydCByWyJyZWFzb25zIl1bMF1bImZhaWxpbmciXSA9PSBcCiAgICAgICAgInBhcGVyLmNvbmZp
cm1hdGlvbi5ub3RfY29uZmlybWFibGUiCgogICAgIyBhcm0gMjogZm9yZ2VkIHRyYW5zaXRpb24gKHZ
vY2FidWxhcnkgY29udGVudCBhc3NlcnRpb24gKyBhcHBlbmQgcmVmdXNhbCkKICAgIGZyb20gYXBwLn
YyLnBhcGVyX3RyYWRpbmcuY29udHJhY3RzIGltcG9ydCBMRUdBTF9UUkFOU0lUSU9OUwogICAgYXNzZ
XJ0IG5vdCBhbnkoZiA9PSAicmlza19ibG9ja2VkIiBmb3IgZiwgX3QgaW4gTEVHQUxfVFJBTlNJVElP
TlMpCiAgICBmcm9tIGFwcC52Mi5wYXBlcl90cmFkaW5nLm9yZGVycyBpbXBvcnQgYXBwZW5kX2V2ZW5
0CiAgICBhc3luYyB3aXRoIHNlc3Npb25fc2NvcGUoKSBhcyBzZXNzaW9uOgogICAgICAgIG91dGNvbW
UgPSBhd2FpdCBhcHBlbmRfZXZlbnQoCiAgICAgICAgICAgIHNlc3Npb24sIGludGVudF9yb3dfaWQ9Y
mxvY2tlZFsib3JkZXJfaWQiXSwKICAgICAgICAgICAgZnJvbV9zdGF0ZT0icmlza19ibG9ja2VkIiwg
dG9fc3RhdGU9ImV4ZWN1dGluZyIsCiAgICAgICAgICAgIGV2ZW50X2NsYXNzPSJleGVjdXRpb24uc3R
hcnRlZCIsIGRldGFpbHM9e30sIGFjdG9yX2lkPSJ0IiwKICAgICAgICAgICAgbW9kZT0iUEFQRVIiLC
BvcGVyYXRvcl9pZD0idCIsIGNvcnJlbGF0aW9uX2lkPU5vbmUsCiAgICAgICAgICAgIGRhdGFfY2xhc
3M9InNpbXVsYXRlZCIpCiAgICAgICAgYXNzZXJ0IG91dGNvbWUucmVmdXNlZAogICAgICAgIGFzc2Vy
dCBvdXRjb21lLnJlYXNvbnNbMF1bImZhaWxpbmciXSA9PSAidHJhbnNpdGlvbiIKCiAgICAjIHJ1biB
hbHNvIHJlZnVzZWQgdmlhIG1heV9leGVjdXRlCiAgICBydW4gPSAoYXdhaXQgcGFwZXJfY2xpZW50Ln
Bvc3QoCiAgICAgICAgZiJ7UFR9L29yZGVycy97YmxvY2tlZFsnb3JkZXJfaWQnXX0vcnVuIiwgaGVhZ
GVycz1oZWFkZXJzLAogICAgICAgIGpzb249eyJiYXJzIjogX2JhcnMoKSwgImNvc3RfbW9kZWwiOiBB
Tk5FWF9DT1NUU30pKS5qc29uKCkKICAgIGFzc2VydCBydW5bIm91dGNvbWUiXSA9PSAicmVmdXNlZCI
KCgpAcHl0ZXN0Lm1hcmsuYXN5bmNpbwphc3luYyBkZWYgdGVzdF9jYW5jZWxfc2VtYW50aWNzKHBhcG
VyX2NsaWVudCk6CiAgICAiIiJUZXJtaW5hbC1jYW5jZWwgcmVmdXNlZDsgaG9sZC1jYW5jZWwgcmVka
XJlY3RlZCB0byB0aGUgQy0xIGFjdC4iIiIKICAgIGhlYWRlcnMgPSBhd2FpdCBfYWRtaW4ocGFwZXJf
Y2xpZW50KQogICAgYXdhaXQgX2FjY291bnQocGFwZXJfY2xpZW50LCBoZWFkZXJzKQogICAgcGxhY2V
kID0gYXdhaXQgX29yZGVyKHBhcGVyX2NsaWVudCwgaGVhZGVycykKICAgIHJ1biA9IChhd2FpdCBwYX
Blcl9jbGllbnQucG9zdCgKICAgICAgICBmIntQVH0vb3JkZXJzL3twbGFjZWRbJ29yZGVyX2lkJ119L
3J1biIsIGhlYWRlcnM9aGVhZGVycywKICAgICAgICBqc29uPXsiYmFycyI6IF9iYXJzKCksICJjb3N0
X21vZGVsIjogQU5ORVhfQ09TVFN9KSkuanNvbigpCiAgICBhc3NlcnQgcnVuWyJzdGF0ZSJdID09ICJ
zZXR0bGVkIgogICAgciA9IChhd2FpdCBwYXBlcl9jbGllbnQucG9zdCgKICAgICAgICBmIntQVH0vb3
JkZXJzL2NhbmNlbCIsIGhlYWRlcnM9aGVhZGVycywKICAgICAgICBqc29uPXsib3JkZXJfaWQiOiBwb
GFjZWRbIm9yZGVyX2lkIl19KSkuanNvbigpCiAgICBhc3NlcnQgclsib3V0Y29tZSJdID09ICJyZWZ1
c2VkIiAgIyB0ZXJtaW5hbAoKICAgIGhlbGQgPSBhd2FpdCBfaGVsZF9vcmRlcihwYXBlcl9jbGllbnQ
sIGhlYWRlcnMpCiAgICByID0gKGF3YWl0IHBhcGVyX2NsaWVudC5wb3N0KAogICAgICAgIGYie1BUfS
9vcmRlcnMvY2FuY2VsIiwgaGVhZGVycz1oZWFkZXJzLAogICAgICAgIGpzb249eyJvcmRlcl9pZCI6I
GhlbGRbIm9yZGVyX2lkIl19KSkuanNvbigpCiAgICBhc3NlcnQgclsib3V0Y29tZSJdID09ICJyZWZ1
c2VkIiAgIyBob2xkcyByZXNvbHZlIHZpYSBjb25maXJtYXRpb24gYWN0CiAgICBhc3NlcnQgImNvbmZ
pcm1hdGlvbiBtZWNoYW5pc20iIGluIHJbInJlYXNvbnMiXVswXVsibm90ZSJdCgoKIyAtLS0gVC0yOi
Btb2RlIGdhdGUgLyBULTE2OiBSQkFDIC0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tL
S0tLS0tLS0tLS0tLS0tCgoKQHB5dGVzdC5tYXJrLmFzeW5jaW8KYXN5bmMgZGVmIHRlc3RfdDJfcGFw
ZXJfd3JpdGVyc19yZWZ1c2VkX291dHNpZGVfcGFwZXJfbW9kZShyZXNlYXJjaF9jbGllbnQpOgogICA
gaGVhZGVycyA9IGF3YWl0IF9hZG1pbihyZXNlYXJjaF9jbGllbnQpCiAgICByID0gYXdhaXQgcmVzZW
FyY2hfY2xpZW50LnBvc3QoZiJ7UFR9L2FjY291bnRzIiwgaGVhZGVycz1oZWFkZXJzLCBqc29uPXsKI
CAgICAgICAiYWN0aW9uIjogImNyZWF0ZSIsICJhY2NvdW50X2lkIjogImEiLCAibmFtZSI6ICJ4IiwK
ICAgICAgICAiYmFzZV9jdXJyZW5jeSI6ICJVU0QiLCAiaW5pdGlhbF9iYWxhbmNlIjogIjEifSkKICA
gIGFzc2VydCByLnN0YXR1c19jb2RlID09IDQwMwogICAgYXNzZXJ0ICJub3QgcGVybWl0dGVkIGluIH
RoaXMgbW9kZSIgaW4gci5qc29uKClbImRldGFpbCJdCiAgICByID0gYXdhaXQgcmVzZWFyY2hfY2xpZ
W50LnBvc3QoZiJ7UFR9L29yZGVycyIsIGhlYWRlcnM9aGVhZGVycywganNvbj17CiAgICAgICAgImFj
Y291bnRfaWQiOiAiYSIsICJpbnN0cnVtZW50X2lkIjogIngiLCAic2lkZSI6ICJidXkiLAogICAgICA
gICJxdWFudGl0eSI6ICIxIiwgImlkZW1wb3RlbmN5X2tleSI6ICJrIiwgInNuYXBzaG90X3JlZiI6IC
JzIn0pCiAgICBhc3NlcnQgci5zdGF0dXNfY29kZSA9PSA0MDMKCgpAcHl0ZXN0Lm1hcmsuYXN5bmNpb
wphc3luYyBkZWYgdGVzdF90MTZfcmJhY19kZW5pZWRfYW5kX3VuYXV0aGVudGljYXRlZChwYXBlcl9j
bGllbnQpOgogICAgaGVhZGVycyA9IGF3YWl0IF9vcGVyYXRvcl9oZWFkZXJzKHBhcGVyX2NsaWVudCk
KICAgICMgb3BlcmF0b3IgbGFja3MgYWxsIHYyLnBhcGVyLiogKGFkbWluLW9ubHkgdjEgc3VyZmFjZS
kKICAgIGZvciBwYXRoLCBib2R5IGluICgoZiJ7UFR9L2FjY291bnRzIiwgeyJhY3Rpb24iOiAiY3JlY
XRlIiwKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICJhY2NvdW50X2lk
IjogImEiLCAibmFtZSI6ICJ4IiwKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICA
gICAgICJiYXNlX2N1cnJlbmN5IjogIlVTRCIsCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIC
AgICAgICAgICAgICAiaW5pdGlhbF9iYWxhbmNlIjogIjEifSksCiAgICAgICAgICAgICAgICAgICAgI
CAgKGYie1BUfS9vcmRlcnMiLCB7ImFjY291bnRfaWQiOiAiYSIsCiAgICAgICAgICAgICAgICAgICAg
ICAgICAgICAgICAgICAgICAgICAgImluc3RydW1lbnRfaWQiOiAieCIsCiAgICAgICAgICAgICAgICA
gICAgICAgICAgICAgICAgICAgICAgICAgInNpZGUiOiAiYnV5IiwgInF1YW50aXR5IjogIjEiLAogIC
AgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICJpZGVtcG90ZW5jeV9rZXkiOiAia
yIsCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgInNuYXBzaG90X3JlZiI6
ICJzIn0pLAogICAgICAgICAgICAgICAgICAgICAgIChmIntQVH0vb3JkZXJzL2NhbmNlbCIsIHsib3J
kZXJfaWQiOiAieCJ9KSk6CiAgICAgICAgciA9IGF3YWl0IHBhcGVyX2NsaWVudC5wb3N0KHBhdGgsIG
hlYWRlcnM9aGVhZGVycywganNvbj1ib2R5KQogICAgICAgIGFzc2VydCByLnN0YXR1c19jb2RlID09I
DQwMwogICAgICAgIGFzc2VydCByLmpzb24oKVsiZGV0YWlsIl0gPT0gIlBlcm1pc3Npb24gZGVuaWVk
IiAgIyBnZW5lcmljIChCRS0xKQogICAgciA9IGF3YWl0IHBhcGVyX2NsaWVudC5nZXQoZiJ7UFR9L29
yZGVycyIpCiAgICBhc3NlcnQgci5zdGF0dXNfY29kZSA9PSA0MDEKCgpAcHl0ZXN0Lm1hcmsuYXN5bm
Npbwphc3luYyBkZWYgdGVzdF9lbnZlbG9wZV9hbmRfZGlzY2xhaW1lcl9vbl9yZWFkcyhwYXBlcl9jb
GllbnQpOgogICAgaGVhZGVycyA9IGF3YWl0IF9hZG1pbihwYXBlcl9jbGllbnQpCiAgICByID0gKGF3
YWl0IHBhcGVyX2NsaWVudC5nZXQoZiJ7UFR9L2ZpbGxzIiwgaGVhZGVycz1oZWFkZXJzKSkuanNvbig
pCiAgICBmb3Iga2V5IGluICgibW9kZSIsICJjb3JyZWxhdGlvbl9pZCIsICJ0aW1lc3RhbXAiLCAiZG
lzY2xhaW1lciIpOgogICAgICAgIGFzc2VydCBrZXkgaW4gcgogICAgYXNzZXJ0ICJuZXZlciBicm9rZ
XItY29uZmlybWVkIiBpbiByWyJkaXNjbGFpbWVyIl0K
'@
$LandPath = Join-Path $BackendRoot "tests\test_v2_be8_orders.py"
New-Item -ItemType Directory -Force -Path (Split-Path $LandPath) | Out-Null
if (Test-Path $LandPath) {
    $Cur = (Get-FileHash -Path $LandPath -Algorithm SHA256).Hash.ToLower()
    if ($Cur -eq "46c9cee65ca01033849f4b4176b3ae270673a25e9fa6151850533264920f1b01") { Write-Evidence ("pre-landing witnessed (already pinned bytes): tests\test_v2_be8_orders.py") }
    else { throw ("STOP (A4 FOREIGN-STATE ADJUDICATION LAW): new-file target exists with foreign bytes: " + $LandPath + " sha " + $Cur + " . Nothing modified for this file; report to ITRGA.") }
} else {
    [IO.File]::WriteAllBytes($LandPath, (B64-Decode -B64Chunk $Ftests_test_v2_be8_orders_py))
    $Cur = (Get-FileHash -Path $LandPath -Algorithm SHA256).Hash.ToLower()
    if ($Cur -ne "46c9cee65ca01033849f4b4176b3ae270673a25e9fa6151850533264920f1b01") { throw ("FAIL: post-write hash drift on " + $LandPath) }
    Write-Evidence ("landed + verified: tests\test_v2_be8_orders.py")
}

# file: tests\test_v2_be8_boundaries.py  (pin a42a19f80338...)
$Ftests_test_v2_be8_boundaries_py = @'
IiIiVjIgQkUtOCBib3VuZGFyeS9pc29sYXRpb24gdGVzdHMg4oCUIEJPLVYyLUJFLTgtMDAxIFQtMS9
ULTMvVC00L1QtMTYvVC0xOC4KCkQtMSBtYXJrZXItZXhlbXB0aW9uIGJvdGggYXJtcyArIGJvdW5kYX
J5OyBzZWFsZWQtcmVnaXN0cnkgY2Vuc3VzOwpuby1hZGFwdGVyLUFCQyBzY2FuOyBpbXBvcnQgc2Nhb
iAoTjEvTjIpOyBQR0YtMDIxIHNvdXJjZSBzY2FuOyBBUEktc3VyZmFjZQpjZW5zdXMgKEMzKTsgVjEg
cGluIHJlLWhhc2g7IHByaW9yLWJhbmQgY29udHJhY3QgcmVncmVzc2lvbi4KIiIiCgpmcm9tIF9fZnV
0dXJlX18gaW1wb3J0IGFubm90YXRpb25zCgppbXBvcnQgYXN0CmltcG9ydCBoYXNobGliCmZyb20gcG
F0aGxpYiBpbXBvcnQgUGF0aAoKaW1wb3J0IHB5dGVzdAoKQkFDS0VORCA9IFBhdGgoX19maWxlX18pL
nJlc29sdmUoKS5wYXJlbnRzWzFdClBBUEVSX0RJUiA9IEJBQ0tFTkQgLyAiYXBwL3YyL3BhcGVyX3Ry
YWRpbmciCgoKIyAtLS0gVC0xOiBELTEgbWFya2VyIGxhdywgYm90aCBhcm1zICsgYm91bmRhcnkgLS0
tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0KCgpkZWYgdGVzdF9kMV9leGVtcHRpb25fc2NvcG
VkX2V4YWN0bHlfdjJfcGFwZXJfcHJlZml4KCk6CiAgICAiIiJBcm0gMTogdjIucGFwZXIuKiByb3dzI
HBhc3MgdGhlIGd1YXJkICh3b3VsZCBkaWUgd2l0aG91dCBELTEpLiIiIgogICAgZnJvbSBhcHAudjIu
cmJhYy5wZXJtaXNzaW9ucyBpbXBvcnQgKAogICAgICAgIFYyX0ZPUkJJRERFTl9QRVJNSVNTSU9OX01
BUktFUlMsCiAgICAgICAgVjJfUk9MRV9QRVJNSVNTSU9OUywKICAgICAgICBhc3NlcnRfcGVybWlzc2
lvbl92b2NhYnVsYXJ5X3NhZmUsCiAgICApCgogICAgYXNzZXJ0X3Blcm1pc3Npb25fdm9jYWJ1bGFye
V9zYWZlKCkgICMgbXVzdCBub3QgcmFpc2Ugd2l0aCBwYXBlciByb3dzIGluCiAgICBwYXBlcl9yb3dz
ID0ge3AgZm9yIHBlcm1zIGluIFYyX1JPTEVfUEVSTUlTU0lPTlMudmFsdWVzKCkKICAgICAgICAgICA
gICAgICAgZm9yIHAgaW4gcGVybXMgaWYgcC5zdGFydHN3aXRoKCJ2Mi5wYXBlci4iKX0KICAgIGFzc2
VydCBsZW4ocGFwZXJfcm93cykgPT0gOAogICAgIyB0aGUgY29sbGlzaW9uIGlzIHJlYWw6IHdpdGhvd
XQgdGhlIGV4ZW1wdGlvbiB0aGVzZSBXT1VMRCBkaWUKICAgIGFzc2VydCBhbnkobSBpbiBwIGZvciBw
IGluIHBhcGVyX3Jvd3MKICAgICAgICAgICAgICAgZm9yIG0gaW4gVjJfRk9SQklEREVOX1BFUk1JU1N
JT05fTUFSS0VSUykKCgpkZWYgdGVzdF9kMV9tYXJrZXJzX3N0aWxsX2RpZV9lbHNld2hlcmUobW9ua2
V5cGF0Y2gpOgogICAgIiIiQXJtIDIgKG11c3QtZGllKTogdjIucmVzZWFyY2gub3JkZXIuKiByZWplY
3RlZC4iIiIKICAgIGltcG9ydCBhcHAudjIucmJhYy5wZXJtaXNzaW9ucyBhcyBwZXJtc19tb2QKCiAg
ICBmb3JnZWQgPSBkaWN0KHBlcm1zX21vZC5WMl9ST0xFX1BFUk1JU1NJT05TKQogICAgZm9yZ2VkWyJ
hZG1pbiJdID0gZm9yZ2VkWyJhZG1pbiJdIHwgeyJ2Mi5yZXNlYXJjaC5vcmRlci5wbGFjZSJ9CiAgIC
Btb25rZXlwYXRjaC5zZXRhdHRyKHBlcm1zX21vZCwgIlYyX1JPTEVfUEVSTUlTU0lPTlMiLCBmb3JnZ
WQpCiAgICB3aXRoIHB5dGVzdC5yYWlzZXMoVmFsdWVFcnJvciwgbWF0Y2g9IlYyX1BFUk1JU1NJT05f
Rk9SQklEREVOIik6CiAgICAgICAgcGVybXNfbW9kLmFzc2VydF9wZXJtaXNzaW9uX3ZvY2FidWxhcnl
fc2FmZSgpCgoKZGVmIHRlc3RfZDFfYm91bmRhcnlfcGFwZXJ3b3JrX2RpZXMobW9ua2V5cGF0Y2gpOg
ogICAgIiIiQm91bmRhcnkgYXJtIChtdXN0LWRpZSk6IHYyLnBhcGVyd29yay4qIGlzIE5PVCBleGVtc
HQg4oCUIHRoZSB0ZXN0CiAgICBpcyBhIGxpdGVyYWwgcHJlZml4ICd2Mi5wYXBlci4nIGluY2x1ZGlu
ZyB0aGUgdHJhaWxpbmcgZG90LiIiIgogICAgaW1wb3J0IGFwcC52Mi5yYmFjLnBlcm1pc3Npb25zIGF
zIHBlcm1zX21vZAoKICAgIGZvcmdlZCA9IGRpY3QocGVybXNfbW9kLlYyX1JPTEVfUEVSTUlTU0lPTl
MpCiAgICBmb3JnZWRbImFkbWluIl0gPSBmb3JnZWRbImFkbWluIl0gfCB7InYyLnBhcGVyd29yay5vc
mRlci5mb3JnZSJ9CiAgICBtb25rZXlwYXRjaC5zZXRhdHRyKHBlcm1zX21vZCwgIlYyX1JPTEVfUEVS
TUlTU0lPTlMiLCBmb3JnZWQpCiAgICB3aXRoIHB5dGVzdC5yYWlzZXMoVmFsdWVFcnJvciwgbWF0Y2g
9IlYyX1BFUk1JU1NJT05fRk9SQklEREVOIik6CiAgICAgICAgcGVybXNfbW9kLmFzc2VydF9wZXJtaX
NzaW9uX3ZvY2FidWxhcnlfc2FmZSgpCgoKIyAtLS0gVC00OiBzZWFsZWQgcmVnaXN0cnkgKyBubyBhZ
GFwdGVyIGludGVyZmFjZSAtLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLQoKCmRlZiB0ZXN0
X3NlYWxlZF9yZWdpc3RyeV9zaW5nbGVfZW50cnlfZnJvemVuKCk6CiAgICBmcm9tIHR5cGVzIGltcG9
ydCBNYXBwaW5nUHJveHlUeXBlCgogICAgZnJvbSBhcHAudjIucGFwZXJfdHJhZGluZy5jb250cmFjdH
MgaW1wb3J0IEVYRUNVVElPTl9CQUNLRU5EUwoKICAgIGFzc2VydCBpc2luc3RhbmNlKEVYRUNVVElPT
l9CQUNLRU5EUywgTWFwcGluZ1Byb3h5VHlwZSkKICAgIGFzc2VydCBkaWN0KEVYRUNVVElPTl9CQUNL
RU5EUykgPT0gewogICAgICAgICJwYXBlciI6ICJhcHAudjIucGFwZXJfdHJhZGluZy5zaW11bGF0b3I
ifQogICAgd2l0aCBweXRlc3QucmFpc2VzKFR5cGVFcnJvcik6CiAgICAgICAgRVhFQ1VUSU9OX0JBQ0
tFTkRTWyJsaXZlIl0gPSAiYW55d2hlcmUiICAjIGZyb3plbiBsaXRlcmFsCgoKZGVmIHRlc3Rfbm9fY
WRhcHRlcl9hYmNfYW55d2hlcmVfaW5fZG9tYWluKCk6CiAgICAiIiJTNi4xOiBubyBFeGVjdXRpb25B
ZGFwdGVyIGludGVyZmFjZS9BQkMgZXhpc3RzIOKAlCB0aGUgc3Vic3RpdHV0aW9uCiAgICBzdXJmYWN
lIE4yIGZvcmJpZHMgaXMgc3RydWN0dXJhbGx5IGFic2VudC4iIiIKICAgIGZvciBmIGluIFBBUEVSX0
RJUi5nbG9iKCIqLnB5Iik6CiAgICAgICAgdHJlZSA9IGFzdC5wYXJzZShmLnJlYWRfdGV4dCgpKQogI
CAgICAgIGZvciBub2RlIGluIGFzdC53YWxrKHRyZWUpOgogICAgICAgICAgICBpZiBpc2luc3RhbmNl
KG5vZGUsIGFzdC5DbGFzc0RlZik6CiAgICAgICAgICAgICAgICBiYXNlX25hbWVzID0ge2dldGF0dHI
oYiwgImlkIiwgZ2V0YXR0cihiLCAiYXR0ciIsICIiKSkKICAgICAgICAgICAgICAgICAgICAgICAgIC
AgICAgZm9yIGIgaW4gbm9kZS5iYXNlc30KICAgICAgICAgICAgICAgIGFzc2VydCAiQUJDIiBub3Qga
W4gYmFzZV9uYW1lcywgZiJBQkMgaW4ge2YubmFtZX0iCiAgICAgICAgICAgICAgICBhc3NlcnQgImFk
YXB0ZXIiIG5vdCBpbiBub2RlLm5hbWUubG93ZXIoKSwgbm9kZS5uYW1lCiAgICAgICAgdGV4dCA9IGY
ucmVhZF90ZXh0KCkubG93ZXIoKQogICAgICAgIGFzc2VydCAiZXhlY3V0aW9uYWRhcHRlciIgbm90IG
luIHRleHQsIGYubmFtZQogICAgICAgIGFzc2VydCAiYWJzdHJhY3RtZXRob2QiIG5vdCBpbiB0ZXh0L
CBmLm5hbWUKCgpkZWYgdGVzdF9pbXBvcnRfc2Nhbl9wYXBlcl9kb21haW5faXNvbGF0ZWQoKToKICAg
ICIiIlQtMy9OMS9OMjogbm8gYnJva2VyL2V4ZWN1dGlvbi9jcmVkZW50aWFsL25ldHdvcmsgbW9kdWx
lIHJlYWNoYWJsZQogICAgZnJvbSB0aGUgcGFwZXIgZG9tYWluIGdyYXBoLiIiIgogICAgYmFubmVkX3
Rva2VucyA9ICgiZXhlY3V0aW9uIiwgImJyb2tlciIsICJsaXZlX3NlcnZpY2UiLAogICAgICAgICAgI
CAgICAgICAgICAidHJhZGluZ19pbnRlbGxpZ2VuY2UiLCAibWFya2V0LmxpdmUiLCAiYXBwLm1hcmtl
dCIsCiAgICAgICAgICAgICAgICAgICAgICJjcmVkZW50aWFsIiwgInNlY3JldCIsICJ2YXVsdCIsICJ
rZXlyaW5nIikKICAgIGJhbm5lZF9uZXR3b3JrID0gKCJyZXF1ZXN0cyIsICJodHRweCIsICJ1cmxsaW
IiLCAic29ja2V0IiwgImFpb2h0dHAiLAogICAgICAgICAgICAgICAgICAgICAgIndlYnNvY2tldCIpC
iAgICBmb3IgZiBpbiBQQVBFUl9ESVIuZ2xvYigiKi5weSIpOgogICAgICAgIHRyZWUgPSBhc3QucGFy
c2UoZi5yZWFkX3RleHQoKSkKICAgICAgICBmb3Igbm9kZSBpbiBhc3Qud2Fsayh0cmVlKToKICAgICA
gICAgICAgbmFtZXMgPSBbXQogICAgICAgICAgICBpZiBpc2luc3RhbmNlKG5vZGUsIGFzdC5JbXBvcn
QpOgogICAgICAgICAgICAgICAgbmFtZXMgPSBbYS5uYW1lIGZvciBhIGluIG5vZGUubmFtZXNdCiAgI
CAgICAgICAgIGVsaWYgaXNpbnN0YW5jZShub2RlLCBhc3QuSW1wb3J0RnJvbSkgYW5kIG5vZGUubW9k
dWxlOgogICAgICAgICAgICAgICAgbmFtZXMgPSBbbm9kZS5tb2R1bGVdCiAgICAgICAgICAgIGZvciB
uYW1lIGluIG5hbWVzOgogICAgICAgICAgICAgICAgbG93ID0gbmFtZS5sb3dlcigpCiAgICAgICAgIC
AgICAgICBmb3IgdG9rZW4gaW4gYmFubmVkX3Rva2VucyArIGJhbm5lZF9uZXR3b3JrOgogICAgICAgI
CAgICAgICAgICAgIGFzc2VydCB0b2tlbiBub3QgaW4gbG93LCBmIntmLm5hbWV9IGltcG9ydHMge25h
bWV9IgoKCmRlZiB0ZXN0X3BnZjAyMV9ub19maWxlc3lzdGVtX2NvbmRpdGlvbmFsX2JlaGF2aW9yKCk
6CiAgICAiIiJULTE4OiBubyBQYXRoLmV4aXN0cy9pc19kaXIvaXNfZmlsZSBicmFuY2hpbmc7IG5vIG
VudiByZWFkcy4KICAgIChUaGUgbWlncmF0aW9uIHJlYWRzIGZpbGVzIGJ5IGRlc2lnbiDigJQgZG9tY
WluIG1vZHVsZXMgb25seS4pIiIiCiAgICBmb3IgZiBpbiBQQVBFUl9ESVIuZ2xvYigiKi5weSIpOgog
ICAgICAgIHRleHQgPSBmLnJlYWRfdGV4dCgpCiAgICAgICAgZm9yIG1hcmtlciBpbiAoIi5leGlzdHM
oKSIsICIuaXNfZGlyKCkiLCAiLmlzX2ZpbGUoKSIsCiAgICAgICAgICAgICAgICAgICAgICAgIm9zLm
Vudmlyb24iLCAib3MuZ2V0ZW52Iik6CiAgICAgICAgICAgIGFzc2VydCBtYXJrZXIgbm90IGluIHRle
HQsIGYie21hcmtlcn0gaW4ge2YubmFtZX0iCgoKZGVmIF9jb2RlX3dpdGhvdXRfZG9jc3RyaW5ncyhw
YXRoOiBQYXRoKSAtPiBzdHI6CiAgICAiIiJTb3VyY2Ugd2l0aCBkb2NzdHJpbmdzIHN0cmlwcGVkOiB
0aGUgc2NhbiB0YXJnZXRzIENPREUgdm9jYWJ1bGFyeTsKICAgIHRoZSBOMSBkZWNsYXJhdGlvbiBzZW
50ZW5jZXMgaW4gbW9kdWxlIGRvY3N0cmluZ3MgYXJlIG5vdCBjb2RlLiIiIgogICAgdHJlZSA9IGFzd
C5wYXJzZShwYXRoLnJlYWRfdGV4dCgpKQogICAgZm9yIG5vZGUgaW4gYXN0LndhbGsodHJlZSk6CiAg
ICAgICAgaWYgaXNpbnN0YW5jZShub2RlLCAoYXN0Lk1vZHVsZSwgYXN0LkNsYXNzRGVmLCBhc3QuRnV
uY3Rpb25EZWYsCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgYXN0LkFzeW5jRnVuY3Rpb25EZW
YpKToKICAgICAgICAgICAgYm9keSA9IG5vZGUuYm9keQogICAgICAgICAgICBpZiAoYm9keSBhbmQga
XNpbnN0YW5jZShib2R5WzBdLCBhc3QuRXhwcikKICAgICAgICAgICAgICAgICAgICBhbmQgaXNpbnN0
YW5jZShib2R5WzBdLnZhbHVlLCBhc3QuQ29uc3RhbnQpCiAgICAgICAgICAgICAgICAgICAgYW5kIGl
zaW5zdGFuY2UoYm9keVswXS52YWx1ZS52YWx1ZSwgc3RyKSk6CiAgICAgICAgICAgICAgICBib2R5Wz
BdLnZhbHVlLnZhbHVlID0gIiIKICAgIHJldHVybiBhc3QudW5wYXJzZSh0cmVlKQoKCmRlZiB0ZXN0X
25vX3NlY3JldF9vcl9jcmVkZW50aWFsX3ZvY2FidWxhcnkoKToKICAgICIiIk4xOiB6ZXJvIGNyZWRl
bnRpYWwvc2VjcmV0IGFjY2VzcyB2b2NhYnVsYXJ5IGluIGRvbWFpbiBDT0RFCiAgICAoZG9jc3RyaW5
ncyBzdHJpcHBlZCDigJQgdGhlIGlzb2xhdGlvbiBkZWNsYXJhdGlvbnMgbmFtZSB0aGUgY29uY2VwdA
ogICAgdG8gZm9yYmlkIGl0OyB0aGUgY29kZSBtYXkgbm90IGNhcnJ5IGl0KS4iIiIKICAgIGZvciBmI
GluIFBBUEVSX0RJUi5nbG9iKCIqLnB5Iik6CiAgICAgICAgdGV4dCA9IF9jb2RlX3dpdGhvdXRfZG9j
c3RyaW5ncyhmKS5sb3dlcigpCiAgICAgICAgZm9yIHRva2VuIGluICgiYXBpX2tleSIsICJwYXNzd29
yZCIsICJjcmVkZW50aWFsIiwgImtleXJpbmciLAogICAgICAgICAgICAgICAgICAgICAgInByaXZhdG
Vfa2V5IiwgImF1dGhfdG9rZW4iKToKICAgICAgICAgICAgYXNzZXJ0IHRva2VuIG5vdCBpbiB0ZXh0L
CBmInt0b2tlbn0gaW4ge2YubmFtZX0iCgoKIyAtLS0gVC0xNjogQVBJIGNlbnN1cyAoQzMpIC0tLS0t
LS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0KCgpkZWYgdGV
zdF9hcGlfc3VyZmFjZV9jZW5zdXNfZXhhY3QoKToKICAgICIiIlBPU1QgPSBleGFjdGx5IHRoZSA2IG
dvdmVybmVkIHdyaXRlcnM7IHplcm8gUFVUL1BBVENIL0RFTEVURS4iIiIKICAgIGZyb20gYXBwLnYyL
nBhcGVyX3RyYWRpbmcuYXBpIGltcG9ydCByb3V0ZXIKCiAgICBwb3N0cywgZ2V0cywgb3RoZXJzID0g
c2V0KCksIHNldCgpLCBzZXQoKQogICAgZm9yIHJvdXRlIGluIHJvdXRlci5yb3V0ZXM6CiAgICAgICA
gbWV0aG9kcyA9IHJvdXRlLm1ldGhvZHMgLSB7IkhFQUQiLCAiT1BUSU9OUyJ9CiAgICAgICAgaWYgIl
BPU1QiIGluIG1ldGhvZHM6CiAgICAgICAgICAgIHBvc3RzLmFkZChyb3V0ZS5wYXRoKQogICAgICAgI
GlmICJHRVQiIGluIG1ldGhvZHM6CiAgICAgICAgICAgIGdldHMuYWRkKHJvdXRlLnBhdGgpCiAgICAg
ICAgZm9yIG0gaW4gbWV0aG9kcyAtIHsiUE9TVCIsICJHRVQifToKICAgICAgICAgICAgb3RoZXJzLmF
kZCgobSwgcm91dGUucGF0aCkpCiAgICBhc3NlcnQgcG9zdHMgPT0gewogICAgICAgICIvcGFwZXIvYW
Njb3VudHMiLCAiL3BhcGVyL2FjY291bnRzL2NvbmZpcm0iLCAiL3BhcGVyL29yZGVycyIsCiAgICAgI
CAgIi9wYXBlci9vcmRlcnMvY29uZmlybSIsICIvcGFwZXIvb3JkZXJzL2NhbmNlbCIsCiAgICAgICAg
Ii9wYXBlci9vcmRlcnMve29yZGVyX2lkfS9ydW4ifQogICAgYXNzZXJ0IGdldHMgPT0gewogICAgICA
gICIvcGFwZXIvYWNjb3VudHMiLCAiL3BhcGVyL29yZGVycyIsCiAgICAgICAgIi9wYXBlci9vcmRlcn
Mve29yZGVyX2lkfS9ldmVudHMiLCAiL3BhcGVyL2ZpbGxzIiwKICAgICAgICAiL3BhcGVyL3Bvc2l0a
W9ucyIsICIvcGFwZXIvYmFsYW5jZXMiLCAiL3BhcGVyL3Jpc2stZGVjaXNpb25zIiwKICAgICAgICAi
L3BhcGVyL3JlY29uY2lsaWF0aW9ucyJ9CiAgICBhc3NlcnQgb3RoZXJzID09IHNldCgpICAjIEMzOiB
ubyBQVVQvUEFUQ0gvREVMRVRFCgoKIyAtLS0gdm9jYWJ1bGFyeSBpbnRlZ3JpdHkgLS0tLS0tLS0tLS
0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tCgoKZGVmIHRlc3Rfd
m9jYWJ1bGFyeV9pbnRlZ3JpdHkoKToKICAgIGZyb20gYXBwLnYyLnBhcGVyX3RyYWRpbmcuY29udHJh
Y3RzIGltcG9ydCAoCiAgICAgICAgQ09ORklSTUFUSU9OX1JFRlVTQUxTLAogICAgICAgIEZJTExfQ0x
BU1NFUywKICAgICAgICBMRUdBTF9UUkFOU0lUSU9OUywKICAgICAgICBPUkRFUl9TVEFURVMsCiAgIC
AgICAgUklTS19ERUNJU0lPTlMsCiAgICAgICAgVEVSTUlOQUxfU1RBVEVTLAogICAgICAgIFRJTUVfS
U5fRk9SQ0VfVjEsCiAgICApCgogICAgYXNzZXJ0IEZJTExfQ0xBU1NFUyA9PSAoInBhcGVyX3NpbXVs
YXRlZCIsKQogICAgYXNzZXJ0IFJJU0tfREVDSVNJT05TID09ICgicGFzcyIsICJibG9jayIsICJob2x
kIikKICAgIGFzc2VydCBUSU1FX0lOX0ZPUkNFX1YxID09ICgicmVwbGF5X3dpbmRvdyIsKQogICAgYX
NzZXJ0IHNldChURVJNSU5BTF9TVEFURVMpIDw9IHNldChPUkRFUl9TVEFURVMpCiAgICBhc3NlcnQgb
GVuKENPTkZJUk1BVElPTl9SRUZVU0FMUykgPT0gNAogICAgZm9yIGZybSwgdG8gaW4gTEVHQUxfVFJB
TlNJVElPTlM6CiAgICAgICAgYXNzZXJ0IGZybSBpbiBPUkRFUl9TVEFURVMgYW5kIHRvIGluIE9SREV
SX1NUQVRFUwogICAgIyBubyB0cmFuc2l0aW9uIGxlYXZlcyBhIHRlcm1pbmFsIHN0YXRlCiAgICBmb3
IgZnJtLCBfdG8gaW4gTEVHQUxfVFJBTlNJVElPTlM6CiAgICAgICAgYXNzZXJ0IGZybSBub3QgaW4gV
EVSTUlOQUxfU1RBVEVTCgoKZGVmIHRlc3RfbW9kZV9sYXdfdDIoKToKICAgIGZyb20gYXBwLnYyLm1v
ZGUuY29udHJhY3QgaW1wb3J0IERFRkVSUkVEX01PREVTLCBWQUxJRF9NT0RFUwoKICAgIGFzc2VydCB
WQUxJRF9NT0RFUyA9PSAoIlJFU0VBUkNIIiwgIlNJTVVMQVRJT04iLCAiUEFQRVIiKQogICAgYXNzZX
J0IERFRkVSUkVEX01PREVTID09ICgiTElWRSIsKQoKCiMgLS0tIHJlZ3Jlc3Npb246IFYxIHBpbnMgK
yBwcmlvciBiYW5kcyAtLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0K
CgpkZWYgdGVzdF9yZWdyZXNzaW9uX3YxX3JldXNlX3BpbnNfdW5jaGFuZ2VkKCk6CiAgICAiIiJUaGU
gc2l4IFYxIHBpbnMgcmUtaGFzaCB1bmNoYW5nZWQgKFQtNyBsaW5lYWdlOyBWMSBwYXBlci1sZWRnZX
IKICAgIHN1cmZhY2UgYnl0ZS1mcm96ZW4gcGVyIFExIHN1cGVyc2VkZS13aXRoLWZyb3plbi1ib3VuZ
GFyeSkuIiIiCiAgICBwaW5zID0gewogICAgICAgICJhcHAvbWwvZGF0YXNldC9jaHJvbm9sb2d5X2d1
YXJkLnB5IjogIjdkYmM2NjVkYzRiNDNmMzEiLAogICAgICAgICJhcHAvbWwvZGF0YXNldC9zcGxpdF9
lbmdpbmUucHkiOiAiZTg5M2I5MmM2Y2NjZTE4OCIsCiAgICAgICAgImFwcC9tbC9kYXRhc2V0L3NuYX
BzaG90X2J1aWxkZXIucHkiOiAiYjA4ZWY0YjFkZWMwNzU2NyIsCiAgICAgICAgImFwcC9tbC9kYXRhc
2V0L3NlcnZpY2UucHkiOiAiNmM1ZDcyYTg5NDIwNTBiNCIsCiAgICAgICAgImFwcC9leGVjdXRpb25f
cmVzZWFyY2gvc2ltdWxhdGlvbi5weSI6ICJmMTYzZTYxMGJhMWE2MjE1IiwKICAgICAgICAiYXBwL21
sL2Vjb25vbWljL3NlcnZpY2UucHkiOiAiYzQ5NTI3ZWQxMmY0ZDJjYSIsCiAgICB9CiAgICBmb3Igcm
VsLCBwaW4gaW4gcGlucy5pdGVtcygpOgogICAgICAgIGFjdHVhbCA9IGhhc2hsaWIuc2hhMjU2KAogI
CAgICAgICAgICAoQkFDS0VORCAvIHJlbCkucmVhZF9ieXRlcygpKS5oZXhkaWdlc3QoKVs6MTZdCiAg
ICAgICAgYXNzZXJ0IGFjdHVhbCA9PSBwaW4sIGYie3JlbH06IHthY3R1YWx9ICE9IHtwaW59IgoKCmR
lZiB0ZXN0X3JlZ3Jlc3Npb25fcHJpb3JfYmFuZF9jb250cmFjdHNfdW50b3VjaGVkKCk6CiAgICAiIi
JCRS00Li5CRS03IGNvbnRyYWN0IHZvY2FidWxhcmllcyB1bmNoYW5nZWQgYnkgdGhlIEJFLTggcGFja
2FnZS4iIiIKICAgIGZyb20gYXBwLnYyLnBvcnRmb2xpb19yZXNlYXJjaC5jb250cmFjdHMgaW1wb3J0
ICgKICAgICAgICBCQVNJU19MQUJFTFMsCiAgICAgICAgUE9SVEZPTElPX0JBU0VTLAogICAgKQogICA
gZnJvbSBhcHAudjIucmVzZWFyY2gudHlwaW5nIGltcG9ydCBGQU1JTElFUwogICAgZnJvbSBhcHAudj
IucmVzZWFyY2hfZ292ZXJuYW5jZS5jb250cmFjdHMgaW1wb3J0ICgKICAgICAgICBERVBMT1lNRU5UX
0NMQVNTRVMsCiAgICAgICAgU0lHTkFMX0ZBTUlMSUVTLAogICAgICAgIFNJR05BTF9TVEFURVMsCiAg
ICApCiAgICBmcm9tIGFwcC52Mi5yZXNlYXJjaF9qb2JzLmNvbnRyYWN0cyBpbXBvcnQgKAogICAgICA
gIENPTlNUUlVDVElCTEVfUkVTVUxUX0NMQVNTRVMsCiAgICAgICAgQ09TVF9VTklUU19WMSwKICAgIC
AgICBSRVNVTFRfQ0xBU1NfVEFYT05PTVksCiAgICApCgogICAgYXNzZXJ0IFBPUlRGT0xJT19CQVNFU
yA9PSAoImh5cG90aGV0aWNhbCIsKQogICAgYXNzZXJ0IEJBU0lTX0xBQkVMUyA9PSAoImh5cG90aGV0
aWNhbC1yZXNlYXJjaCIsKQogICAgYXNzZXJ0IFNJR05BTF9GQU1JTElFUyA9PSAoInN0cnVjdHVyYWw
iLCAicHJlZGljdGl2ZSIpCiAgICBhc3NlcnQgU0lHTkFMX1NUQVRFUyA9PSAoImVtaXR0ZWQiLCAid2
l0aGhlbGQiLCAiZXhwaXJlZCIsICJyZWZ1c2VkIikKICAgIGFzc2VydCBERVBMT1lNRU5UX0NMQVNTR
VMgPT0gKCJyZXNlYXJjaCIsICJzaGFkb3ciLCAiY2hhbXBpb24iLAogICAgICAgICAgICAgICAgICAg
ICAgICAgICAgICAgICAgImNoYWxsZW5nZXIiLCAicmV0aXJlZCIpCiAgICBhc3NlcnQgbGVuKEZBTUl
MSUVTKSA9PSAxMAogICAgYXNzZXJ0IFJFU1VMVF9DTEFTU19UQVhPTk9NWSA9PSAoImJhY2t0ZXN0Ii
wgInNpbXVsYXRpb24iLCAicGFwZXIiLAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgI
CAgImxpdmUiKQogICAgYXNzZXJ0IENPTlNUUlVDVElCTEVfUkVTVUxUX0NMQVNTRVMgPT0gKCJiYWNr
dGVzdCIsICJzaW11bGF0aW9uIikKICAgIGFzc2VydCBDT1NUX1VOSVRTX1YxID09ICgicHJpY2UiLCA
iZnJhY3Rpb24iKQo=
'@
$LandPath = Join-Path $BackendRoot "tests\test_v2_be8_boundaries.py"
New-Item -ItemType Directory -Force -Path (Split-Path $LandPath) | Out-Null
if (Test-Path $LandPath) {
    $Cur = (Get-FileHash -Path $LandPath -Algorithm SHA256).Hash.ToLower()
    if ($Cur -eq "a42a19f803385fe6829e9623e97878935fbe89add3670f20a37282364e72a99e") { Write-Evidence ("pre-landing witnessed (already pinned bytes): tests\test_v2_be8_boundaries.py") }
    else { throw ("STOP (A4 FOREIGN-STATE ADJUDICATION LAW): new-file target exists with foreign bytes: " + $LandPath + " sha " + $Cur + " . Nothing modified for this file; report to ITRGA.") }
} else {
    [IO.File]::WriteAllBytes($LandPath, (B64-Decode -B64Chunk $Ftests_test_v2_be8_boundaries_py))
    $Cur = (Get-FileHash -Path $LandPath -Algorithm SHA256).Hash.ToLower()
    if ($Cur -ne "a42a19f803385fe6829e9623e97878935fbe89add3670f20a37282364e72a99e") { throw ("FAIL: post-write hash drift on " + $LandPath) }
    Write-Evidence ("landed + verified: tests\test_v2_be8_boundaries.py")
}

# file: app\v2\mode\contract.py  (pin 3346e0eee27d...)
$Fapp_v2_mode_contract_py = @'
IiIiVjIgTW9kZSBDb250cmFjdCDigJQgc2luZ2xlIHNvdXJjZSBvZiB0cnV0aCBmb3IgVjIgZW52aXJ
vbm1lbnQgbW9kZS4KCk1vZGUgaXMgZGV0ZXJtaW5lZCBieSBBWElPTV9WMl9NT0RFIGVudmlyb25tZW
50IHZhcmlhYmxlIE9OTFkuCk5vIGRhdGFiYXNlIHRhYmxlLiBObyBBUEkgbXV0YXRpb24uIE5vIGNsa
WVudCBpbnB1dCBhY2NlcHRlZC4KClN1cHBvcnRlZCBtb2RlczogUkVTRUFSQ0gsIFNJTVVMQVRJT04s
IFBBUEVSCkRlZmVycmVkIG1vZGVzOiBMSVZFIChCRS0xMCkKClBBUEVSIGF1dGhvcml6ZWQgYnkgQk8
tVjItQkUtOC0wMDEgRC0zIHVuZGVyIElUUkdBIHJ1bGluZyBELTIKKElUUkdBLVJFVi1WMi1CRS04LU
RFU0lHTi0wMDEgwqc2KTogbmFycm93ZXN0IGV4dGVuc2lvbjsgTElWRSByZW1haW5zCnJlZnVzZWQ7I
HBhcGVyIHdyaXRlcnMgcmVxdWlyZSBtb2RlID09ICJQQVBFUiIgZXhwbGljaXRseS4KIiIiCgpmcm9t
IF9fZnV0dXJlX18gaW1wb3J0IGFubm90YXRpb25zCgppbXBvcnQgb3MKCmZyb20gYXBwLmNvcmUubG9
nZ2luZyBpbXBvcnQgZ2V0X2xvZ2dlcgoKbG9nZ2VyID0gZ2V0X2xvZ2dlcihfX25hbWVfXywgY2F0ZW
dvcnk9IlNZU1RFTSIpCgpWQUxJRF9NT0RFUyA9ICgiUkVTRUFSQ0giLCAiU0lNVUxBVElPTiIsICJQQ
VBFUiIpCgojIERlZmVycmVkIG1vZGVzIOKAlCByZWNvZ25pemVkIGJ1dCBuZXZlciBhdXRob3JpemVk
IHVudGlsIHRoZWlyIGJhbmQKREVGRVJSRURfTU9ERVMgPSAoIkxJVkUiLCkKCgpkZWYgZ2V0X21vZGU
oKSAtPiBzdHI6CiAgICAiIiJSZXR1cm4gdGhlIGNvbmZpZ3VyZWQgVjIgbW9kZS4gSW1tdXRhYmxlIG
F0IHJ1bnRpbWUuCgogICAgU291cmNlOiBBWElPTV9WMl9NT0RFIGVudmlyb25tZW50IHZhcmlhYmxlL
gogICAgRGVmYXVsdDogUkVTRUFSQ0ggKGlmIG5vdCBzZXQpLgogICAgIiIiCiAgICBtb2RlID0gb3Mu
ZW52aXJvbi5nZXQoIkFYSU9NX1YyX01PREUiLCAiUkVTRUFSQ0giKS51cHBlcigpCiAgICBpZiBtb2R
lIG5vdCBpbiBWQUxJRF9NT0RFUzoKICAgICAgICByYWlzZSBWYWx1ZUVycm9yKAogICAgICAgICAgIC
BmIkFYSU9NX1YyX01PREUgbXVzdCBiZSBvbmUgb2Yge1ZBTElEX01PREVTfSwgZ290OiB7bW9kZX0uI
CIKICAgICAgICAgICAgZiJMSVZFIG1vZGUgaXMgZGVmZXJyZWQgdG8gYSBmdXR1cmUgYmFuZC4iCiAg
ICAgICAgKQogICAgcmV0dXJuIG1vZGUKCgpkZWYgaXNfcmVzZWFyY2gobW9kZTogc3RyKSAtPiBib29
sOgogICAgIiIiQ2hlY2sgaWYgbW9kZSBpcyBSRVNFQVJDSC4iIiIKICAgIHJldHVybiBtb2RlID09IC
JSRVNFQVJDSCIKCgpkZWYgaXNfc2ltdWxhdGlvbihtb2RlOiBzdHIpIC0+IGJvb2w6CiAgICAiIiJDa
GVjayBpZiBtb2RlIGlzIFNJTVVMQVRJT04uIiIiCiAgICByZXR1cm4gbW9kZSA9PSAiU0lNVUxBVElP
TiIKCgpkZWYgdmFsaWRhdGVfbW9kZV92YWx1ZShtb2RlOiBzdHIpIC0+IHN0cjoKICAgICIiIlZhbGl
kYXRlIGEgbW9kZSBzdHJpbmcuIFJldHVybnMgdGhlIG1vZGUgaWYgdmFsaWQuIiIiCiAgICBpZiBtb2
RlIG5vdCBpbiBWQUxJRF9NT0RFUzoKCiAgICAgICAgcmFpc2UgVmFsdWVFcnJvcigKICAgICAgICAgI
CAgZiJJbnZhbGlkIG1vZGU6IHttb2RlfS4gTXVzdCBiZSBvbmUgb2Yge1ZBTElEX01PREVTfSIKICAg
ICAgICApCiAgICByZXR1cm4gbW9kZQo=
'@
$LandPath = Join-Path $BackendRoot "app\v2\mode\contract.py"
New-Item -ItemType Directory -Force -Path (Split-Path $LandPath) | Out-Null
if (!(Test-Path $LandPath)) { throw ("STOP: modified-file target missing at the floor: " + $LandPath) }
$Cur = (Get-FileHash -Path $LandPath -Algorithm SHA256).Hash.ToLower()
if ($Cur -eq "3346e0eee27d6f13a2d6d02e2df06089879c563789a113cf0bf014223c040b59") { Write-Evidence ("already landed (pinned bytes): app\v2\mode\contract.py") }
else {
    $FloorText = [IO.File]::ReadAllText($LandPath)
    if ($FloorText -notmatch [regex]::Escape('VALID_MODES = ("RESEARCH", "SIMULATION")')) { throw ("STOP: floor marker absent in app\v2\mode\contract.py - the tree is not at the 0047 floor for this file; nothing modified; report to ITRGA.") }
    [IO.File]::WriteAllBytes($LandPath, (B64-Decode -B64Chunk $Fapp_v2_mode_contract_py))
    $Cur2 = (Get-FileHash -Path $LandPath -Algorithm SHA256).Hash.ToLower()
    if ($Cur2 -ne "3346e0eee27d6f13a2d6d02e2df06089879c563789a113cf0bf014223c040b59") { throw ("FAIL: post-write hash drift on " + $LandPath) }
    Write-Evidence ("amended app\v2\mode\contract.py (floor marker proven) -> 3346e0eee27d...")
}

# file: app\v2\rbac\permissions.py  (pin 064019ca4953...)
$Fapp_v2_rbac_permissions_py = @'
IiIiVjIgUkJBQyBQZXJtaXNzaW9ucyDigJQgcmVhZC1vbmx5IHNlZWRlZCBwZXJtaXNzaW9uIGRlZml
uaXRpb25zLgoKUGVyIDE3X0lOU1RJVFVUSU9OQUxfU0VDVVJJVFlfU1RBTkRBUkQubWQgUGFydCBWST
oKLSBEZWZhdWx0IERlbnkKLSBFeHBsaWNpdCBQZXJtaXNzaW9uIEdyYW50Ci0gTGVhc3QgUHJpdmlsZ
WdlCi0gQ29tcGxldGUgQXVkaXRhYmlsaXR5CgpQZXJtaXNzaW9ucyBhcmUgc2VlZGVkIGR1cmluZyBt
aWdyYXRpb24uIE5vIHJ1bnRpbWUgbXV0YXRpb24uCiIiIgoKZnJvbSBfX2Z1dHVyZV9fIGltcG9ydCB
hbm5vdGF0aW9ucwoKZnJvbSBlbnVtIGltcG9ydCBFbnVtCgoKY2xhc3MgVjJQZXJtaXNzaW9uKHN0ci
wgRW51bSk6CiAgICAiIiJWMiBwZXJtaXNzaW9uIHN0cmluZ3MuIiIiCgogICAgTU9ERV9SRUFEID0gI
nYyLm1vZGUucmVhZCIKICAgIENBUEFCSUxJVFlfUkVBRCA9ICJ2Mi5jYXBhYmlsaXR5LnJlYWQiCiAg
ICBBVURJVF9SRUFEID0gInYyLmF1ZGl0LnJlYWQiCiAgICBBVURJVF9SRUFEX0FMTCA9ICJ2Mi5hdWR
pdC5yZWFkX2FsbCIKICAgIExJTkVBR0VfUkVBRCA9ICJ2Mi5saW5lYWdlLnJlYWQiCiAgICBMSU5FQU
dFX1JFQURfQUxMID0gInYyLmxpbmVhZ2UucmVhZF9hbGwiCiAgICBFUlJPUl9SRUFEID0gInYyLmVyc
m9yLnJlYWQiCiAgICAjIEJFLTIgbWFya2V0IGRhdGEgKEJPLVYyLUJFLTItMDAxKQogICAgTUFSS0VU
REFUQV9SRUFEID0gInYyLm1hcmtldGRhdGEucmVhZCIKICAgIE1BUktFVERBVEFfUkVBRF9BTEwgPSA
idjIubWFya2V0ZGF0YS5yZWFkX2FsbCIKICAgIE1BUktFVERBVEFfVkVSSUZZID0gInYyLm1hcmtldG
RhdGEudmVyaWZ5IgogICAgTUFSS0VUREFUQV9DQVRBTE9HX1JFRlJFU0ggPSAidjIubWFya2V0ZGF0Y
S5jYXRhbG9nLnJlZnJlc2giCiAgICAjIEJFLTMgUDEgcHJvdmlkZXIgKEJPLVYyLUJFLTMtUDEtMDAx
KSDigJQgcmVhZC1vbmx5CiAgICBQUk9WSURFUl9SRUFEID0gInYyLm1hcmtldGRhdGEucHJvdmlkZXI
ucmVhZCIKICAgIFBST1ZJREVSX1JFQURfSElTVE9SWSA9ICJ2Mi5tYXJrZXRkYXRhLnByb3ZpZGVyLn
JlYWRfaGlzdG9yeSIKICAgICMgQkUtMyBQMiAoQk8tVjItQkUtMy1QMi0wMDEpIOKAlCBhZG1pbi1vb
mx5IGNvbnRyYWN0IHRlc3QKICAgIFBST1ZJREVSX0NPTlRSQUNUX1RFU1QgPSAidjIubWFya2V0ZGF0
YS5wcm92aWRlci5jb250cmFjdF90ZXN0IgogICAgIyBCRS00IHJlc2VhcmNoIHJlYWQgbW9kZWxzICh
CTy1WMi1CRS00LTAwMTsgUi0xKQogICAgUkVTRUFSQ0hfTUNfUkVBRCA9ICJ2Mi5yZXNlYXJjaC5tYX
JrZXRfY29udGV4dC5yZWFkIgogICAgUkVTRUFSQ0hfQ0lfUkVBRCA9ICJ2Mi5yZXNlYXJjaC5jaGFyd
F9pbnRlbGxpZ2VuY2UucmVhZCIKICAgIFJFU0VBUkNIX01DX0NPTVBVVEUgPSAidjIucmVzZWFyY2gu
bWFya2V0X2NvbnRleHQuY29tcHV0ZSIKICAgICMgQkUtNSByZXNlYXJjaCBnb3Zlcm5hbmNlIChCTy1
WMi1CRS01LTAwMSkKICAgIFJFU0VBUkNIX01MR09WX1JFQUQgPSAidjIucmVzZWFyY2gubWxfZ292ZX
JuYW5jZS5yZWFkIgogICAgUkVTRUFSQ0hfTUxHT1ZfREVDSURFID0gInYyLnJlc2VhcmNoLm1sX2dvd
mVybmFuY2UuZGVjaWRlIgogICAgUkVTRUFSQ0hfU0lHTkFMX1JFQUQgPSAidjIucmVzZWFyY2guc2ln
bmFsLnJlYWQiCiAgICBSRVNFQVJDSF9TSUdOQUxfRU1JVCA9ICJ2Mi5yZXNlYXJjaC5zaWduYWwuZW1
pdCIKICAgIFJFU0VBUkNIX01MRElBR19SRUFEID0gInYyLnJlc2VhcmNoLm1sX2RpYWdub3N0aWNzLn
JlYWQiCiAgICAjIEJFLTYgcG9ydGZvbGlvIHJlc2VhcmNoIChCTy1WMi1CRS02LTAwMSkKICAgIFJFU
0VBUkNIX1BGX1JFQUQgPSAidjIucmVzZWFyY2gucG9ydGZvbGlvLnJlYWQiCiAgICBSRVNFQVJDSF9Q
Rl9ERUZJTkUgPSAidjIucmVzZWFyY2gucG9ydGZvbGlvLmRlZmluZSIKICAgIFJFU0VBUkNIX1BGUkl
TS19SRUFEID0gInYyLnJlc2VhcmNoLnBvcnRmb2xpb19yaXNrLnJlYWQiCiAgICBSRVNFQVJDSF9QRl
JJU0tfQ09NUFVURSA9ICJ2Mi5yZXNlYXJjaC5wb3J0Zm9saW9fcmlzay5jb21wdXRlIgogICAgIyBCR
S03IHJlc2VhcmNoIGpvYnMgKEJPLVYyLUJFLTctMDAxKQogICAgUkVTRUFSQ0hfSk9CU19SRUFEID0g
InYyLnJlc2VhcmNoLmpvYnMucmVhZCIKICAgIFJFU0VBUkNIX0pPQlNfU1VCTUlUID0gInYyLnJlc2V
hcmNoLmpvYnMuc3VibWl0IgogICAgUkVTRUFSQ0hfSk9CU19DQU5DRUwgPSAidjIucmVzZWFyY2guam
9icy5jYW5jZWwiCiAgICBSRVNFQVJDSF9SRUdJU1RSWV9SRUFEID0gInYyLnJlc2VhcmNoLnJlZ2lzd
HJ5LnJlYWQiCiAgICBSRVNFQVJDSF9SRUdJU1RSWV9XUklURSA9ICJ2Mi5yZXNlYXJjaC5yZWdpc3Ry
eS53cml0ZSIKICAgIFJFU0VBUkNIX1JFU1VMVFNfUkVBRCA9ICJ2Mi5yZXNlYXJjaC5yZXN1bHRzLnJ
lYWQiCiAgICAjIEJFLTggcGFwZXIgdHJhZGluZyAoQk8tVjItQkUtOC0wMDEgRC0zOyBELTEgc2NvcG
VkIG1hcmtlciBleGVtcHRpb24pCiAgICBQQVBFUl9BQ0NPVU5UU19SRUFEID0gInYyLnBhcGVyLmFjY
291bnRzLnJlYWQiCiAgICBQQVBFUl9BQ0NPVU5UU19NQU5BR0UgPSAidjIucGFwZXIuYWNjb3VudHMu
bWFuYWdlIgogICAgUEFQRVJfT1JERVJTX1JFQUQgPSAidjIucGFwZXIub3JkZXJzLnJlYWQiCiAgICB
QQVBFUl9PUkRFUlNfUExBQ0UgPSAidjIucGFwZXIub3JkZXJzLnBsYWNlIgogICAgUEFQRVJfT1JERV
JTX0NBTkNFTCA9ICJ2Mi5wYXBlci5vcmRlcnMuY2FuY2VsIgogICAgUEFQRVJfT1JERVJTX0NPTkZJU
k0gPSAidjIucGFwZXIub3JkZXJzLmNvbmZpcm0iCiAgICBQQVBFUl9GSUxMU19SRUFEID0gInYyLnBh
cGVyLmZpbGxzLnJlYWQiCiAgICBQQVBFUl9SSVNLX1JFQUQgPSAidjIucGFwZXIucmlzay5yZWFkIgo
KCiMgUm9sZSDihpIgcGVybWlzc2lvbnMgbWFwcGluZwpWMl9ST0xFX1BFUk1JU1NJT05TOiBkaWN0W3
N0ciwgZnJvemVuc2V0W3N0cl1dID0gewogICAgImFkbWluIjogZnJvemVuc2V0KHsKICAgICAgICBWM
lBlcm1pc3Npb24uTU9ERV9SRUFELnZhbHVlLAogICAgICAgIFYyUGVybWlzc2lvbi5DQVBBQklMSVRZ
X1JFQUQudmFsdWUsCiAgICAgICAgVjJQZXJtaXNzaW9uLkFVRElUX1JFQUQudmFsdWUsCiAgICAgICA
gVjJQZXJtaXNzaW9uLkFVRElUX1JFQURfQUxMLnZhbHVlLAogICAgICAgIFYyUGVybWlzc2lvbi5MSU
5FQUdFX1JFQUQudmFsdWUsCiAgICAgICAgVjJQZXJtaXNzaW9uLkxJTkVBR0VfUkVBRF9BTEwudmFsd
WUsCiAgICAgICAgVjJQZXJtaXNzaW9uLkVSUk9SX1JFQUQudmFsdWUsCiAgICAgICAgVjJQZXJtaXNz
aW9uLk1BUktFVERBVEFfUkVBRC52YWx1ZSwKICAgICAgICBWMlBlcm1pc3Npb24uTUFSS0VUREFUQV9
SRUFEX0FMTC52YWx1ZSwKICAgICAgICBWMlBlcm1pc3Npb24uTUFSS0VUREFUQV9WRVJJRlkudmFsdW
UsCiAgICAgICAgVjJQZXJtaXNzaW9uLk1BUktFVERBVEFfQ0FUQUxPR19SRUZSRVNILnZhbHVlLAogI
CAgICAgIFYyUGVybWlzc2lvbi5QUk9WSURFUl9SRUFELnZhbHVlLAogICAgICAgIFYyUGVybWlzc2lv
bi5QUk9WSURFUl9SRUFEX0hJU1RPUlkudmFsdWUsCiAgICAgICAgVjJQZXJtaXNzaW9uLlBST1ZJREV
SX0NPTlRSQUNUX1RFU1QudmFsdWUsCiAgICAgICAgVjJQZXJtaXNzaW9uLlJFU0VBUkNIX01DX1JFQU
QudmFsdWUsCiAgICAgICAgVjJQZXJtaXNzaW9uLlJFU0VBUkNIX0NJX1JFQUQudmFsdWUsCiAgICAgI
CAgVjJQZXJtaXNzaW9uLlJFU0VBUkNIX01DX0NPTVBVVEUudmFsdWUsCiAgICAgICAgVjJQZXJtaXNz
aW9uLlJFU0VBUkNIX01MR09WX1JFQUQudmFsdWUsCiAgICAgICAgVjJQZXJtaXNzaW9uLlJFU0VBUkN
IX01MR09WX0RFQ0lERS52YWx1ZSwKICAgICAgICBWMlBlcm1pc3Npb24uUkVTRUFSQ0hfU0lHTkFMX1
JFQUQudmFsdWUsCiAgICAgICAgVjJQZXJtaXNzaW9uLlJFU0VBUkNIX1NJR05BTF9FTUlULnZhbHVlL
AogICAgICAgIFYyUGVybWlzc2lvbi5SRVNFQVJDSF9NTERJQUdfUkVBRC52YWx1ZSwKICAgICAgICBW
MlBlcm1pc3Npb24uUkVTRUFSQ0hfUEZfUkVBRC52YWx1ZSwKICAgICAgICBWMlBlcm1pc3Npb24uUkV
TRUFSQ0hfUEZfREVGSU5FLnZhbHVlLAogICAgICAgIFYyUGVybWlzc2lvbi5SRVNFQVJDSF9QRlJJU0
tfUkVBRC52YWx1ZSwKICAgICAgICBWMlBlcm1pc3Npb24uUkVTRUFSQ0hfUEZSSVNLX0NPTVBVVEUud
mFsdWUsCiAgICAgICAgVjJQZXJtaXNzaW9uLlJFU0VBUkNIX0pPQlNfUkVBRC52YWx1ZSwKICAgICAg
ICBWMlBlcm1pc3Npb24uUkVTRUFSQ0hfSk9CU19TVUJNSVQudmFsdWUsCiAgICAgICAgVjJQZXJtaXN
zaW9uLlJFU0VBUkNIX0pPQlNfQ0FOQ0VMLnZhbHVlLAogICAgICAgIFYyUGVybWlzc2lvbi5SRVNFQV
JDSF9SRUdJU1RSWV9SRUFELnZhbHVlLAogICAgICAgIFYyUGVybWlzc2lvbi5SRVNFQVJDSF9SRUdJU
1RSWV9XUklURS52YWx1ZSwKICAgICAgICBWMlBlcm1pc3Npb24uUkVTRUFSQ0hfUkVTVUxUU19SRUFE
LnZhbHVlLAogICAgICAgIFYyUGVybWlzc2lvbi5QQVBFUl9BQ0NPVU5UU19SRUFELnZhbHVlLAogICA
gICAgIFYyUGVybWlzc2lvbi5QQVBFUl9BQ0NPVU5UU19NQU5BR0UudmFsdWUsCiAgICAgICAgVjJQZX
JtaXNzaW9uLlBBUEVSX09SREVSU19SRUFELnZhbHVlLAogICAgICAgIFYyUGVybWlzc2lvbi5QQVBFU
l9PUkRFUlNfUExBQ0UudmFsdWUsCiAgICAgICAgVjJQZXJtaXNzaW9uLlBBUEVSX09SREVSU19DQU5D
RUwudmFsdWUsCiAgICAgICAgVjJQZXJtaXNzaW9uLlBBUEVSX09SREVSU19DT05GSVJNLnZhbHVlLAo
gICAgICAgIFYyUGVybWlzc2lvbi5QQVBFUl9GSUxMU19SRUFELnZhbHVlLAogICAgICAgIFYyUGVybW
lzc2lvbi5QQVBFUl9SSVNLX1JFQUQudmFsdWUsCiAgICB9KSwKICAgICJvcGVyYXRvciI6IGZyb3plb
nNldCh7CiAgICAgICAgVjJQZXJtaXNzaW9uLk1PREVfUkVBRC52YWx1ZSwKICAgICAgICBWMlBlcm1p
c3Npb24uQ0FQQUJJTElUWV9SRUFELnZhbHVlLAogICAgICAgIFYyUGVybWlzc2lvbi5BVURJVF9SRUF
ELnZhbHVlLAogICAgICAgIFYyUGVybWlzc2lvbi5MSU5FQUdFX1JFQUQudmFsdWUsCiAgICAgICAgVj
JQZXJtaXNzaW9uLkVSUk9SX1JFQUQudmFsdWUsCiAgICAgICAgVjJQZXJtaXNzaW9uLk1BUktFVERBV
EFfUkVBRC52YWx1ZSwKICAgICAgICBWMlBlcm1pc3Npb24uTUFSS0VUREFUQV9WRVJJRlkudmFsdWUs
CiAgICAgICAgVjJQZXJtaXNzaW9uLlBST1ZJREVSX1JFQUQudmFsdWUsCiAgICAgICAgVjJQZXJtaXN
zaW9uLlJFU0VBUkNIX01DX1JFQUQudmFsdWUsCiAgICAgICAgVjJQZXJtaXNzaW9uLlJFU0VBUkNIX0
NJX1JFQUQudmFsdWUsCiAgICAgICAgVjJQZXJtaXNzaW9uLlJFU0VBUkNIX01MR09WX1JFQUQudmFsd
WUsCiAgICAgICAgVjJQZXJtaXNzaW9uLlJFU0VBUkNIX1NJR05BTF9SRUFELnZhbHVlLAogICAgICAg
IFYyUGVybWlzc2lvbi5SRVNFQVJDSF9NTERJQUdfUkVBRC52YWx1ZSwKICAgICAgICBWMlBlcm1pc3N
pb24uUkVTRUFSQ0hfUEZfUkVBRC52YWx1ZSwKICAgICAgICBWMlBlcm1pc3Npb24uUkVTRUFSQ0hfUE
ZSSVNLX1JFQUQudmFsdWUsCiAgICAgICAgVjJQZXJtaXNzaW9uLlJFU0VBUkNIX0pPQlNfUkVBRC52Y
Wx1ZSwKICAgICAgICBWMlBlcm1pc3Npb24uUkVTRUFSQ0hfUkVTVUxUU19SRUFELnZhbHVlLAogICAg
ICAgICMgQkUtOCBub3RlOiBvcGVyYXRvciBwYXBlciBncmFudHMgZGVmZXJyZWQg4oCUIHRoZSBCTy1
WMi1CRS04LTAwMQogICAgICAgICMgVC0xMyBjZW5zdXMgcGluICg1NyA9IDQ5ICsgZXhhY3RseSA4IH
Jvd3MpIGJpbmRzOyB0aGUgUzcuMQogICAgICAgICMgcm9sZXMgY29sdW1uJ3Mgb3BlcmF0b3IgcmVhZ
HMgd291bGQgbWFrZSAxMi4gRGlzY2xvc2VkIGluIHRoZQogICAgICAgICMgZGVsaXZlcnkgcmVwb3J0
OyBhZG1pbi1vbmx5IHYxIHN1cmZhY2UuCiAgICB9KSwKfQoKIyBGb3JiaWRkZW4gcGVybWlzc2lvbiB
tYXJrZXJzIOKAlCBhbnkgVjIgcGVybWlzc2lvbiBjb250YWluaW5nIHRoZXNlIGlzIHJlamVjdGVkCl
YyX0ZPUkJJRERFTl9QRVJNSVNTSU9OX01BUktFUlMgPSAoCiAgICAiZ2F0ZSIsCiAgICAiZXhlY3V0a
W9uIiwKICAgICJleGVjdXRlIiwKICAgICJvcmRlciIsCiAgICAiYnJva2VyIiwKICAgICJhY2NvdW50
IiwKICAgICJwb3NpdGlvbiIsCiAgICAibGl2ZSIsCiAgICAiY2FwaXRhbCIsCiAgICAibWFyZ2luIiw
KKQoKIyBTQUwgY2xhc3NpZmljYXRpb24gZm9yIGVhY2ggcGVybWlzc2lvbgpWMl9QRVJNSVNTSU9OX1
NBTDogZGljdFtzdHIsIHN0cl0gPSB7CiAgICBWMlBlcm1pc3Npb24uTU9ERV9SRUFELnZhbHVlOiAiU
0FMLTIiLAogICAgVjJQZXJtaXNzaW9uLkNBUEFCSUxJVFlfUkVBRC52YWx1ZTogIlNBTC0yIiwKICAg
IFYyUGVybWlzc2lvbi5BVURJVF9SRUFELnZhbHVlOiAiU0FMLTMiLAogICAgVjJQZXJtaXNzaW9uLkF
VRElUX1JFQURfQUxMLnZhbHVlOiAiU0FMLTQiLAogICAgVjJQZXJtaXNzaW9uLkxJTkVBR0VfUkVBRC
52YWx1ZTogIlNBTC0zIiwKICAgIFYyUGVybWlzc2lvbi5MSU5FQUdFX1JFQURfQUxMLnZhbHVlOiAiU
0FMLTQiLAogICAgVjJQZXJtaXNzaW9uLkVSUk9SX1JFQUQudmFsdWU6ICJTQUwtMiIsCiAgICBWMlBl
cm1pc3Npb24uTUFSS0VUREFUQV9SRUFELnZhbHVlOiAiU0FMLTIiLAogICAgVjJQZXJtaXNzaW9uLk1
BUktFVERBVEFfUkVBRF9BTEwudmFsdWU6ICJTQUwtNCIsCiAgICBWMlBlcm1pc3Npb24uTUFSS0VURE
FUQV9WRVJJRlkudmFsdWU6ICJTQUwtMyIsCiAgICBWMlBlcm1pc3Npb24uTUFSS0VUREFUQV9DQVRBT
E9HX1JFRlJFU0gudmFsdWU6ICJTQUwtMyIsCiAgICBWMlBlcm1pc3Npb24uUFJPVklERVJfUkVBRC52
YWx1ZTogIlNBTC0yIiwKICAgIFYyUGVybWlzc2lvbi5QUk9WSURFUl9SRUFEX0hJU1RPUlkudmFsdWU
6ICJTQUwtNCIsCiAgICBWMlBlcm1pc3Npb24uUFJPVklERVJfQ09OVFJBQ1RfVEVTVC52YWx1ZTogIl
NBTC00IiwKICAgIFYyUGVybWlzc2lvbi5SRVNFQVJDSF9NQ19SRUFELnZhbHVlOiAiU0FMLTIiLAogI
CAgVjJQZXJtaXNzaW9uLlJFU0VBUkNIX0NJX1JFQUQudmFsdWU6ICJTQUwtMiIsCiAgICBWMlBlcm1p
c3Npb24uUkVTRUFSQ0hfTUNfQ09NUFVURS52YWx1ZTogIlNBTC0zIiwKICAgIFYyUGVybWlzc2lvbi5
SRVNFQVJDSF9NTEdPVl9SRUFELnZhbHVlOiAiU0FMLTIiLAogICAgVjJQZXJtaXNzaW9uLlJFU0VBUk
NIX01MR09WX0RFQ0lERS52YWx1ZTogIlNBTC0zIiwKICAgIFYyUGVybWlzc2lvbi5SRVNFQVJDSF9TS
UdOQUxfUkVBRC52YWx1ZTogIlNBTC0yIiwKICAgIFYyUGVybWlzc2lvbi5SRVNFQVJDSF9TSUdOQUxf
RU1JVC52YWx1ZTogIlNBTC0zIiwKICAgIFYyUGVybWlzc2lvbi5SRVNFQVJDSF9NTERJQUdfUkVBRC5
2YWx1ZTogIlNBTC0yIiwKICAgIFYyUGVybWlzc2lvbi5SRVNFQVJDSF9QRl9SRUFELnZhbHVlOiAiU0
FMLTIiLAogICAgVjJQZXJtaXNzaW9uLlJFU0VBUkNIX1BGX0RFRklORS52YWx1ZTogIlNBTC0zIiwKI
CAgIFYyUGVybWlzc2lvbi5SRVNFQVJDSF9QRlJJU0tfUkVBRC52YWx1ZTogIlNBTC0yIiwKICAgIFYy
UGVybWlzc2lvbi5SRVNFQVJDSF9QRlJJU0tfQ09NUFVURS52YWx1ZTogIlNBTC0zIiwKICAgIFYyUGV
ybWlzc2lvbi5SRVNFQVJDSF9KT0JTX1JFQUQudmFsdWU6ICJTQUwtMiIsCiAgICBWMlBlcm1pc3Npb2
4uUkVTRUFSQ0hfSk9CU19TVUJNSVQudmFsdWU6ICJTQUwtMyIsCiAgICBWMlBlcm1pc3Npb24uUkVTR
UFSQ0hfSk9CU19DQU5DRUwudmFsdWU6ICJTQUwtMyIsCiAgICBWMlBlcm1pc3Npb24uUkVTRUFSQ0hf
UkVHSVNUUllfUkVBRC52YWx1ZTogIlNBTC0yIiwKICAgIFYyUGVybWlzc2lvbi5SRVNFQVJDSF9SRUd
JU1RSWV9XUklURS52YWx1ZTogIlNBTC0zIiwKICAgIFYyUGVybWlzc2lvbi5SRVNFQVJDSF9SRVNVTF
RTX1JFQUQudmFsdWU6ICJTQUwtMiIsCiAgICBWMlBlcm1pc3Npb24uUEFQRVJfQUNDT1VOVFNfUkVBR
C52YWx1ZTogIlNBTC0yIiwKICAgIFYyUGVybWlzc2lvbi5QQVBFUl9BQ0NPVU5UU19NQU5BR0UudmFs
dWU6ICJTQUwtMyIsCiAgICBWMlBlcm1pc3Npb24uUEFQRVJfT1JERVJTX1JFQUQudmFsdWU6ICJTQUw
tMiIsCiAgICBWMlBlcm1pc3Npb24uUEFQRVJfT1JERVJTX1BMQUNFLnZhbHVlOiAiU0FMLTMiLAogIC
AgVjJQZXJtaXNzaW9uLlBBUEVSX09SREVSU19DQU5DRUwudmFsdWU6ICJTQUwtMyIsCiAgICBWMlBlc
m1pc3Npb24uUEFQRVJfT1JERVJTX0NPTkZJUk0udmFsdWU6ICJTQUwtMyIsCiAgICBWMlBlcm1pc3Np
b24uUEFQRVJfRklMTFNfUkVBRC52YWx1ZTogIlNBTC0yIiwKICAgIFYyUGVybWlzc2lvbi5QQVBFUl9
SSVNLX1JFQUQudmFsdWU6ICJTQUwtMiIsCn0KCgpkZWYgcGVybWlzc2lvbnNfZm9yX3JvbGUocm9sZT
ogc3RyKSAtPiBmcm96ZW5zZXRbc3RyXToKICAgICIiIlJldHVybiBwZXJtaXNzaW9ucyBmb3IgYSByb
2xlLiBVbmtub3duIHJvbGVzIGRlZmF1bHQtZGVueS4iIiIKICAgIHJldHVybiBWMl9ST0xFX1BFUk1J
U1NJT05TLmdldChyb2xlLCBmcm96ZW5zZXQoKSkKCgpkZWYgaGFzX3Blcm1pc3Npb24ocm9sZTogc3R
yLCBwZXJtaXNzaW9uOiBzdHIpIC0+IGJvb2w6CiAgICAiIiJDaGVjayBpZiBhIHJvbGUgaGFzIGEgc3
BlY2lmaWMgcGVybWlzc2lvbi4iIiIKICAgIHJldHVybiBwZXJtaXNzaW9uIGluIHBlcm1pc3Npb25zX
2Zvcl9yb2xlKHJvbGUpCgoKZGVmIGFzc2VydF9wZXJtaXNzaW9uX3ZvY2FidWxhcnlfc2FmZSgpIC0+
IE5vbmU6CiAgICAiIiJSZWZ1c2UgcGVybWlzc2lvbiB2b2NhYnVsYXJpZXMgdGhhdCBlbmNvZGUgZm9
yYmlkZGVuIGV4ZWN1dGlvbiBwb3dlcnMuCgogICAgRC0xIHNjb3BlZCBleGVtcHRpb24gKElUUkdBLV
JFVi1WMi1CRS04LURFU0lHTi0wMDEgwqc1LCBiaW5kaW5nCiAgICBjb25kaXRpb25zIGhvbm9yZWQpO
iBwZXJtaXNzaW9ucyB3aXRoIEVYQUNUTFkgdGhlIGxpdGVyYWwgcHJlZml4CiAgICAndjIucGFwZXIu
JyBhcmUgZXhlbXB0IGZyb20gdGhlIG1hcmtlciBzY2FuIOKAlCB0aGUgc2VhbGVkIHBhcGVyIGRvbWF
pbgogICAgbGVnaXRpbWF0ZWx5IG5hbWVzIGFjY291bnQvb3JkZXIvbWFyZ2luL3Bvc2l0aW9uLiBUaG
UgbWFya2VycyByZW1haW4KICAgIHJlamVjdGVkIGluIGV2ZXJ5IG90aGVyIG5hbWVzcGFjZSAoJ3YyL
nBhcGVyd29yay4qJyBpcyBOT1QgZXhlbXB0OgogICAgdGhlIHRlc3QgaXMgYSBsaXRlcmFsIHByZWZp
eCBpbmNsdWRpbmcgdGhlIHRyYWlsaW5nIGRvdCkuIExpdmUKICAgIHZvY2FidWxhcnkgc3RpbGwgY2F
ubm90IGV4aXN0IHRvIGJlIG5hbWVkLgogICAgIiIiCiAgICBmb3IgcGVybWlzc2lvbl9zZXQgaW4gVj
JfUk9MRV9QRVJNSVNTSU9OUy52YWx1ZXMoKToKICAgICAgICBmb3IgcGVybWlzc2lvbiBpbiBwZXJta
XNzaW9uX3NldDoKICAgICAgICAgICAgbG93ZXIgPSBwZXJtaXNzaW9uLmxvd2VyKCkKICAgICAgICAg
ICAgaWYgbG93ZXIuc3RhcnRzd2l0aCgidjIucGFwZXIuIik6CiAgICAgICAgICAgICAgICBjb250aW5
1ZSAgIyBELTE6IHNpbmdsZSBsaXRlcmFsIHByZWZpeCB0ZXN0LCBub3RoaW5nIGJyb2FkZXIKICAgIC
AgICAgICAgaWYgYW55KG1hcmtlciBpbiBsb3dlciBmb3IgbWFya2VyIGluIFYyX0ZPUkJJRERFTl9QR
VJNSVNTSU9OX01BUktFUlMpOgogICAgICAgICAgICAgICAgcmFpc2UgVmFsdWVFcnJvcihmIlYyX1BF
Uk1JU1NJT05fRk9SQklEREVOOiB7cGVybWlzc2lvbn0iKQoKCiMgU2VlZCBkYXRhIGZvciB2Ml9wZXJ
taXNzaW9uIHRhYmxlClYyX1BFUk1JU1NJT05fU0VFRDogbGlzdFtkaWN0W3N0ciwgc3RyXV0gPSBbXQ
pmb3Igcm9sZSwgcGVybXMgaW4gVjJfUk9MRV9QRVJNSVNTSU9OUy5pdGVtcygpOgogICAgZm9yIHBlc
m0gaW4gcGVybXM6CiAgICAgICAgVjJfUEVSTUlTU0lPTl9TRUVELmFwcGVuZCh7CiAgICAgICAgICAg
ICJyb2xlIjogcm9sZSwKICAgICAgICAgICAgInBlcm1pc3Npb24iOiBwZXJtLAogICAgICAgICAgICA
ic2FsIjogVjJfUEVSTUlTU0lPTl9TQUwuZ2V0KHBlcm0sICJTQUwtMiIpLAogICAgICAgIH0pCg==
'@
$LandPath = Join-Path $BackendRoot "app\v2\rbac\permissions.py"
New-Item -ItemType Directory -Force -Path (Split-Path $LandPath) | Out-Null
if (!(Test-Path $LandPath)) { throw ("STOP: modified-file target missing at the floor: " + $LandPath) }
$Cur = (Get-FileHash -Path $LandPath -Algorithm SHA256).Hash.ToLower()
if ($Cur -eq "064019ca495328e2f1c00e9735f6c97f3e786cadcccb52b673a353bed5c5a99b") { Write-Evidence ("already landed (pinned bytes): app\v2\rbac\permissions.py") }
elseif ($Cur -eq "a3dff08218b2afa7029b678396673c317fe1852f9785697bb35a36cbf0cd3b3a") {
    [IO.File]::WriteAllBytes($LandPath, (B64-Decode -B64Chunk $Fapp_v2_rbac_permissions_py))
    $Cur2 = (Get-FileHash -Path $LandPath -Algorithm SHA256).Hash.ToLower()
    if ($Cur2 -ne "064019ca495328e2f1c00e9735f6c97f3e786cadcccb52b673a353bed5c5a99b") { throw ("FAIL: post-write hash drift on " + $LandPath) }
    Write-Evidence ("amended app\v2\rbac\permissions.py: a3dff08218b2... -> 064019ca4953...")
} else { throw ("STOP: amended-file target at an unpinned state: app\v2\rbac\permissions.py sha " + $Cur + " . Expected floor " + 'a3dff08218b2afa7029b678396673c317fe1852f9785697bb35a36cbf0cd3b3a' + " or landed " + '064019ca495328e2f1c00e9735f6c97f3e786cadcccb52b673a353bed5c5a99b' + " . Nothing modified for this file; report to ITRGA.") }

# file: app\v2\api\router.py  (pin 530f91ec709b...)
$Fapp_v2_api_router_py = @'
IiIiVjIgQVBJIFJvdXRlciDigJQgYWdncmVnYXRlIHJvdXRlciBmb3IgYWxsIFYyIGVuZHBvaW50cy4
iIiIKCmZyb20gX19mdXR1cmVfXyBpbXBvcnQgYW5ub3RhdGlvbnMKCmZyb20gZGF0ZXRpbWUgaW1wb3
J0IGRhdGV0aW1lLCB0aW1lem9uZQoKZnJvbSBmYXN0YXBpIGltcG9ydCBBUElSb3V0ZXIsIFJlcXVlc
3QKCmZyb20gYXBwLnYyLmFwaS5hdWRpdCBpbXBvcnQgcm91dGVyIGFzIGF1ZGl0X3JvdXRlcgpmcm9t
IGFwcC52Mi5hcGkuY2FwYWJpbGl0eSBpbXBvcnQgcm91dGVyIGFzIGNhcGFiaWxpdHlfcm91dGVyCmZ
yb20gYXBwLnYyLmFwaS5saW5lYWdlIGltcG9ydCByb3V0ZXIgYXMgbGluZWFnZV9yb3V0ZXIKZnJvbS
BhcHAudjIuYXBpLm1vZGUgaW1wb3J0IHJvdXRlciBhcyBtb2RlX3JvdXRlcgpmcm9tIGFwcC52Mi5lc
nJvcnMuY29udHJhY3QgaW1wb3J0IFYyRXJyb3JDb2RlCmZyb20gYXBwLnYyLm1hcmtldGRhdGEuYXBp
LnJvdXRlciBpbXBvcnQgcm91dGVyIGFzIG1hcmtldGRhdGFfcm91dGVyCmZyb20gYXBwLnYyLm1vZGV
scy5lcnJvcnMgaW1wb3J0IFYyRXJyb3JUYXhvbm9teVJlc3BvbnNlCmZyb20gYXBwLnYyLnBhcGVyX3
RyYWRpbmcuYXBpIGltcG9ydCByb3V0ZXIgYXMgcGFwZXJfdHJhZGluZ19yb3V0ZXIKZnJvbSBhcHAud
jIucG9ydGZvbGlvX3Jlc2VhcmNoLmFwaSBpbXBvcnQgcm91dGVyIGFzIHBvcnRmb2xpb19yZXNlYXJj
aF9yb3V0ZXIKZnJvbSBhcHAudjIucmJhYy5kZXBlbmRlbmNpZXMgaW1wb3J0IFJlcXVpcmVWMkVycm9
yUmVhZApmcm9tIGFwcC52Mi5yZXNlYXJjaC5hcGkgaW1wb3J0IHJvdXRlciBhcyByZXNlYXJjaF9yb3
V0ZXIKZnJvbSBhcHAudjIucmVzZWFyY2hfZ292ZXJuYW5jZS5hcGkgaW1wb3J0IHJvdXRlciBhcyByZ
XNlYXJjaF9nb3Zlcm5hbmNlX3JvdXRlcgpmcm9tIGFwcC52Mi5yZXNlYXJjaF9qb2JzLmFwaSBpbXBv
cnQgcm91dGVyIGFzIHJlc2VhcmNoX2pvYnNfcm91dGVyCgpyb3V0ZXIgPSBBUElSb3V0ZXIocHJlZml
4PSIvdjIiLCB0YWdzPVsiVjIiXSkKCiMgSW5jbHVkZSBzdWItcm91dGVycwpyb3V0ZXIuaW5jbHVkZV
9yb3V0ZXIobW9kZV9yb3V0ZXIpCnJvdXRlci5pbmNsdWRlX3JvdXRlcihjYXBhYmlsaXR5X3JvdXRlc
ikKcm91dGVyLmluY2x1ZGVfcm91dGVyKGF1ZGl0X3JvdXRlcikKcm91dGVyLmluY2x1ZGVfcm91dGVy
KGxpbmVhZ2Vfcm91dGVyKQpyb3V0ZXIuaW5jbHVkZV9yb3V0ZXIobWFya2V0ZGF0YV9yb3V0ZXIpCnJ
vdXRlci5pbmNsdWRlX3JvdXRlcihyZXNlYXJjaF9yb3V0ZXIpICAjIEJFLTQgKEJPLVYyLUJFLTQtMD
AxIEQtNCkKcm91dGVyLmluY2x1ZGVfcm91dGVyKHJlc2VhcmNoX2dvdmVybmFuY2Vfcm91dGVyKSAgI
yBCRS01IChCTy1WMi1CRS01LTAwMSkKcm91dGVyLmluY2x1ZGVfcm91dGVyKHBvcnRmb2xpb19yZXNl
YXJjaF9yb3V0ZXIpICAjIEJFLTYgKEJPLVYyLUJFLTYtMDAxKQpyb3V0ZXIuaW5jbHVkZV9yb3V0ZXI
ocmVzZWFyY2hfam9ic19yb3V0ZXIpICAjIEJFLTcgKEJPLVYyLUJFLTctMDAxKQpyb3V0ZXIuaW5jbH
VkZV9yb3V0ZXIocGFwZXJfdHJhZGluZ19yb3V0ZXIpICAjIEJFLTggKEJPLVYyLUJFLTgtMDAxIEQtM
ykKCgpAcm91dGVyLmdldCgiL2Vycm9ycyIsIHJlc3BvbnNlX21vZGVsPVYyRXJyb3JUYXhvbm9teVJl
c3BvbnNlKQphc3luYyBkZWYgZ2V0X2Vycm9yX3RheG9ub215KAogICAgcmVxdWVzdDogUmVxdWVzdCw
KICAgIG9wZXJhdG9yOiBSZXF1aXJlVjJFcnJvclJlYWQsCikgLT4gVjJFcnJvclRheG9ub215UmVzcG
9uc2U6CiAgICAiIiJHZXQgVjIgZXJyb3IgdGF4b25vbXkgcmVmZXJlbmNlLiBSZWFkLW9ubHkuIiIiC
iAgICBlcnJvcl9jb2RlcyA9IFsKICAgICAgICB7ImNvZGUiOiBjb2RlLnZhbHVlLCAiY2F0ZWdvcnki
OiBjb2RlLm5hbWUuc3BsaXQoIl8iKVswXS5sb3dlcigpfQogICAgICAgIGZvciBjb2RlIGluIFYyRXJ
yb3JDb2RlCiAgICBdCiAgICBkb21haW5fc3RhdHVzZXMgPSBbImF2YWlsYWJsZSIsICJ1bmF2YWlsYW
JsZSIsICJzdGFsZSIsICJkZWdyYWRlZCIsICJ1bmtub3duIiwgImRlbmllZCJdCgogICAgcmV0dXJuI
FYyRXJyb3JUYXhvbm9teVJlc3BvbnNlKAogICAgICAgIGVycm9yX2NvZGVzPWVycm9yX2NvZGVzLAog
ICAgICAgIGRvbWFpbl9zdGF0dXNlcz1kb21haW5fc3RhdHVzZXMsCiAgICAgICAgbW9kZT1yZXF1ZXN
0LmFwcC5zdGF0ZS52Ml9tb2RlLAogICAgICAgIGNvcnJlbGF0aW9uX2lkPWdldGF0dHIocmVxdWVzdC
5zdGF0ZSwgImNvcnJlbGF0aW9uX2lkIiwgTm9uZSksCiAgICAgICAgdGltZXN0YW1wPWRhdGV0aW1lL
m5vdyh0aW1lem9uZS51dGMpLAogICAgKQo=
'@
$LandPath = Join-Path $BackendRoot "app\v2\api\router.py"
New-Item -ItemType Directory -Force -Path (Split-Path $LandPath) | Out-Null
if (!(Test-Path $LandPath)) { throw ("STOP: modified-file target missing at the floor: " + $LandPath) }
$Cur = (Get-FileHash -Path $LandPath -Algorithm SHA256).Hash.ToLower()
if ($Cur -eq "530f91ec709b1d66c5c5cb7e339af5714d581f57169cb5b4566d0c9c45aafecd") { Write-Evidence ("already landed (pinned bytes): app\v2\api\router.py") }
elseif ($Cur -eq "ad4afdd4eb5fe0c0676c45a9b779cb9eeeb16140163e6f7243fd3c9ad606f670") {
    [IO.File]::WriteAllBytes($LandPath, (B64-Decode -B64Chunk $Fapp_v2_api_router_py))
    $Cur2 = (Get-FileHash -Path $LandPath -Algorithm SHA256).Hash.ToLower()
    if ($Cur2 -ne "530f91ec709b1d66c5c5cb7e339af5714d581f57169cb5b4566d0c9c45aafecd") { throw ("FAIL: post-write hash drift on " + $LandPath) }
    Write-Evidence ("amended app\v2\api\router.py: ad4afdd4eb5f... -> 530f91ec709b...")
} else { throw ("STOP: amended-file target at an unpinned state: app\v2\api\router.py sha " + $Cur + " . Expected floor " + 'ad4afdd4eb5fe0c0676c45a9b779cb9eeeb16140163e6f7243fd3c9ad606f670' + " or landed " + '530f91ec709b1d66c5c5cb7e339af5714d581f57169cb5b4566d0c9c45aafecd' + " . Nothing modified for this file; report to ITRGA.") }

# file: app\db\models\__init__.py  (pin 0b188cbf69fb...)
$Fapp_db_models__init__py = @'
IiIiT1JNIG1vZGVscyBwYWNrYWdlIOKAlCBpbXBvcnQgc2lkZSBlZmZlY3RzIHJlZ2lzdGVyIG1ldGF
kYXRhIGZvciBBbGVtYmljLiIiIgoKZnJvbSBhcHAuZGIubW9kZWxzLmFkdmlzb3J5X3NpZ25hbCBpbX
BvcnQgQWR2aXNvcnlTaWduYWwKZnJvbSBhcHAuZGIubW9kZWxzLmFzc2lzdGFudF9yZXNlYXJjaF9yZ
XNwb25zZSBpbXBvcnQgQXNzaXN0YW50UmVzZWFyY2hSZXNwb25zZQpmcm9tIGFwcC5kYi5tb2RlbHMu
YXVkaXQgaW1wb3J0IEF1ZGl0RXZlbnQsIEF1ZGl0V3JpdGVGYWlsdXJlUmVjb3JkCmZyb20gYXBwLmR
iLm1vZGVscy5jYWxpYnJhdGlvbl9yZXBvcnQgaW1wb3J0IENhbGlicmF0aW9uUmVwb3J0CmZyb20gYX
BwLmRiLm1vZGVscy5jYW5kbGUgaW1wb3J0IENhbmRsZQpmcm9tIGFwcC5kYi5tb2RlbHMuY2hhcnRfc
mVzZWFyY2hfYW5ub3RhdGlvbiBpbXBvcnQgQ2hhcnRSZXNlYXJjaEFubm90YXRpb24KZnJvbSBhcHAu
ZGIubW9kZWxzLmNvcnJlbGF0aW9uX3JlcG9ydCBpbXBvcnQgQ29ycmVsYXRpb25SZXBvcnQKZnJvbSB
hcHAuZGIubW9kZWxzLmRhdGFzZXQgaW1wb3J0ICgKICAgIERhdGFzZXRMaW5lYWdlUmVjb3JkLAogIC
AgRGF0YXNldFF1YXJhbnRpbmVSZWNvcmQsCiAgICBEYXRhc2V0U2VyaWVzTWVtYmVyLAogICAgRGF0Y
XNldFNuYXBzaG90LAopCmZyb20gYXBwLmRiLm1vZGVscy5kYXRhc2V0X3NwbGl0IGltcG9ydCBEYXRh
c2V0U3BsaXRNYW5pZmVzdApmcm9tIGFwcC5kYi5tb2RlbHMuZWNvbm9taWNfcmVwb3J0IGltcG9ydCB
FY29ub21pY1JlcG9ydApmcm9tIGFwcC5kYi5tb2RlbHMuZXhlY3V0aW9uX2V4cGVyaW1lbnQgaW1wb3
J0IEV4ZWN1dGlvblJlc2VhcmNoRXhwZXJpbWVudApmcm9tIGFwcC5kYi5tb2RlbHMuZXhlY3V0aW9uX
3Jpc2tfcmVwb3J0IGltcG9ydCBFeGVjdXRpb25SaXNrUmVzZWFyY2hSZXBvcnQKZnJvbSBhcHAuZGIu
bW9kZWxzLmV4cGVyaW1lbnQgaW1wb3J0IEV4cGVyaW1lbnQKZnJvbSBhcHAuZGIubW9kZWxzLmZlYXR
1cmUgaW1wb3J0IEZlYXR1cmVSZWNvcmQKZnJvbSBhcHAuZGIubW9kZWxzLmZlYXR1cmVfZGVmaW5pdG
lvbiBpbXBvcnQgRmVhdHVyZURlZmluaXRpb24sIEZlYXR1cmVRdWFsaXR5UmVwb3J0CmZyb20gYXBwL
mRiLm1vZGVscy5nZW5lcmFsaXphdGlvbiBpbXBvcnQgRHJpZnRNb25pdG9yaW5nUmVjb3JkLCBHZW5l
cmFsaXphdGlvblJlcG9ydApmcm9tIGFwcC5kYi5tb2RlbHMuaW5nZXN0aW9uX3J1biBpbXBvcnQgSW5
nZXN0aW9uUnVuCmZyb20gYXBwLmRiLm1vZGVscy5tYW51YWxfdHJhZGVfam91cm5hbF9lbnRyeSBpbX
BvcnQgTWFudWFsVHJhZGVKb3VybmFsRW50cnlSZWNvcmQKZnJvbSBhcHAuZGIubW9kZWxzLm1hcmtld
F9tZXRhZGF0YSBpbXBvcnQgTWFya2V0U2VyaWVzTWV0YWRhdGEKZnJvbSBhcHAuZGIubW9kZWxzLm1v
ZGVsX2FydGlmYWN0IGltcG9ydCBNb2RlbEFydGlmYWN0CmZyb20gYXBwLmRiLm1vZGVscy5tb25pdG9
yaW5nX2FsZXJ0IGltcG9ydCBNb25pdG9yaW5nQWxlcnQKZnJvbSBhcHAuZGIubW9kZWxzLm9wZXJhdG
9yIGltcG9ydCBPcGVyYXRvcgpmcm9tIGFwcC5kYi5tb2RlbHMub3BlcmF0b3Jfd29ya3NwYWNlX3ByZ
WZlcmVuY2UgaW1wb3J0IE9wZXJhdG9yV29ya3NwYWNlUHJlZmVyZW5jZQpmcm9tIGFwcC5kYi5tb2Rl
bHMucG9ydGZvbGlvX3Jpc2tfcmVwb3J0IGltcG9ydCBQb3J0Zm9saW9SaXNrUmVwb3J0CmZyb20gYXB
wLmRiLm1vZGVscy5yZWZyZXNoX3Rva2VuIGltcG9ydCBSZWZyZXNoVG9rZW5SZWNvcmQKZnJvbSBhcH
AuZGIubW9kZWxzLnJlZ2ltZV9yZXBvcnQgaW1wb3J0IFJlZ2ltZVJlcG9ydApmcm9tIGFwcC5kYi5tb
2RlbHMucmVzZWFyY2hfbWFuYWdlbWVudCBpbXBvcnQgKAogICAgUmVzZWFyY2hDb2xsZWN0aW9uLAog
ICAgUmVzZWFyY2hDb2xsZWN0aW9uTWVtYmVyLAogICAgUmVzZWFyY2hUYWcsCikKZnJvbSBhcHAuZGI
ubW9kZWxzLnNjZW5hcmlvX3JlcG9ydCBpbXBvcnQgU2NlbmFyaW9SZXBvcnQKZnJvbSBhcHAuZGIubW
9kZWxzLnNpZ25hbF92YWxpZGF0aW9uX3JlcG9ydCBpbXBvcnQgU2lnbmFsVmFsaWRhdGlvblJlcG9yd
Apmcm9tIGFwcC5kYi5tb2RlbHMuc2ltdWxhdGVkX2V4ZWN1dGlvbiBpbXBvcnQgU2ltdWxhdGVkRXhl
Y3V0aW9uUnVuLCBTaW11bGF0ZWRGaWxsRXZlbnQKZnJvbSBhcHAuZGIubW9kZWxzLnNpbXVsYXRlZF9
leGVjdXRpb25fYW5hbHl0aWNzX3JlcG9ydCBpbXBvcnQgU2ltdWxhdGVkRXhlY3V0aW9uQW5hbHl0aW
NzUmVwb3J0CmZyb20gYXBwLmRiLm1vZGVscy5zaW11bGF0ZWRfcGFwZXJfbGVkZ2VyIGltcG9ydCBTa
W11bGF0ZWRQYXBlckxlZGdlckVudHJ5CmZyb20gYXBwLmRiLm1vZGVscy50cmFkZV9wbGFuX25vdGUg
aW1wb3J0IFRyYWRlUGxhbk5vdGVSZWNvcmQKCiMgVjIgbW9kZWxzIOKAlCBtdXN0IGJlIGltcG9ydGV
kIHNvIEFsZW1iaWMgdGFyZ2V0X21ldGFkYXRhIGluY2x1ZGVzIHRoZW0KZnJvbSBhcHAuZGIubW9kZW
xzLnYyX2F1ZGl0X2V2ZW50IGltcG9ydCBWMkF1ZGl0RXZlbnQKZnJvbSBhcHAuZGIubW9kZWxzLnYyX
2NhcGFiaWxpdHlfcmVjb3JkIGltcG9ydCBWMkNhcGFiaWxpdHlSZWNvcmQKZnJvbSBhcHAuZGIubW9k
ZWxzLnYyX2xpbmVhZ2VfcmVjb3JkIGltcG9ydCBWMkxpbmVhZ2VSZWNvcmQKZnJvbSBhcHAuZGIubW9
kZWxzLnYyX21hcmtldGRhdGEgaW1wb3J0ICgKICAgIFYyTWRBc09mVmVyaWZpY2F0aW9uLAogICAgVj
JNZEluc3RydW1lbnQsCiAgICBWMk1kSW50ZWdyaXR5RXhjZXB0aW9uLAogICAgVjJNZFNlcmllcywKI
CAgIFYyTWRTb3VyY2UsCiAgICBWMk1kU3ltYm9sTWFwLAopCmZyb20gYXBwLmRiLm1vZGVscy52Ml9w
YXBlcl90cmFkaW5nIGltcG9ydCAoCiAgICBWMlBhcGVyQWNjb3VudCwKICAgIFYyUGFwZXJCYWxhbmN
lU25hcHNob3QsCiAgICBWMlBhcGVyRmlsbCwKICAgIFYyUGFwZXJPcmRlckV2ZW50LAogICAgVjJQYX
Blck9yZGVySW50ZW50LAogICAgVjJQYXBlclBvc2l0aW9uU25hcHNob3QsCiAgICBWMlBhcGVyUmVjb
25jaWxpYXRpb24sCiAgICBWMlBhcGVyUmlza0RlY2lzaW9uLAopCmZyb20gYXBwLmRiLm1vZGVscy52
Ml9wZXJtaXNzaW9uIGltcG9ydCBWMlBlcm1pc3Npb24KZnJvbSBhcHAuZGIubW9kZWxzLnYyX3BvcnR
mb2xpbyBpbXBvcnQgKAogICAgVjJQb3J0Zm9saW9EZWZpbml0aW9uLAogICAgVjJQb3J0Zm9saW9SaX
NrUmVwb3J0LAopCmZyb20gYXBwLmRiLm1vZGVscy52Ml9wcm92aWRlciBpbXBvcnQgVjJNZFByb3ZpZ
GVyLCBWMk1kUHJvdmlkZXJTdGF0dXNIaXN0b3J5CmZyb20gYXBwLmRiLm1vZGVscy52Ml9yZXNlYXJj
aCBpbXBvcnQgKAogICAgVjJDaGFydEludGVsbGlnZW5jZVJlcG9ydCwKICAgIFYyQ29tcHV0YXRpb25
WZXJzaW9uLAogICAgVjJNYXJrZXRDb250ZXh0UmVwb3J0LAopCmZyb20gYXBwLmRiLm1vZGVscy52Ml
9yZXNlYXJjaF9nb3Zlcm5hbmNlIGltcG9ydCAoCiAgICBWMk1sRGlhZ25vc3RpY1JlcG9ydCwKICAgI
FYyTWxHb3Zlcm5hbmNlUmVjb3JkLAogICAgVjJNbExpZmVjeWNsZUV2ZW50LAopCmZyb20gYXBwLmRi
Lm1vZGVscy52Ml9yZXNlYXJjaF9qb2JzIGltcG9ydCAoCiAgICBWMkJhY2t0ZXN0SW5wdXQsCiAgICB
WMkNvc3RNb2RlbCwKICAgIFYyUmVzZWFyY2hKb2IsCiAgICBWMlJlc2VhcmNoSm9iQXR0ZW1wdCwKIC
AgIFYyUmVzZWFyY2hSZXN1bHQsCiAgICBWMlN0cmF0ZWd5VmVyc2lvbiwKKQpmcm9tIGFwcC5kYi5tb
2RlbHMudjJfc2lnbmFsIGltcG9ydCBWMlNpZ25hbFJlY29yZCwgVjJTaWduYWxTdGF0ZUV2ZW50CmZy
b20gYXBwLmRiLm1vZGVscy52YWxpZGF0aW9uX3JlcG9ydCBpbXBvcnQgVmFsaWRhdGlvblJlcG9ydAp
mcm9tIGFwcC5kYi5tb2RlbHMud3NfdGlja2V0IGltcG9ydCBXc1RpY2tldAoKX19hbGxfXyA9IFsKIC
AgICJBZHZpc29yeVNpZ25hbCIsCiAgICAiQXNzaXN0YW50UmVzZWFyY2hSZXNwb25zZSIsCiAgICAiQ
XVkaXRFdmVudCIsCiAgICAiQXVkaXRXcml0ZUZhaWx1cmVSZWNvcmQiLAogICAgIkNhbGlicmF0aW9u
UmVwb3J0IiwKICAgICJDYW5kbGUiLAogICAgIkNoYXJ0UmVzZWFyY2hBbm5vdGF0aW9uIiwKICAgICJ
Db3JyZWxhdGlvblJlcG9ydCIsCiAgICAiRGF0YXNldExpbmVhZ2VSZWNvcmQiLAogICAgIkRhdGFzZX
RRdWFyYW50aW5lUmVjb3JkIiwKICAgICJEYXRhc2V0U2VyaWVzTWVtYmVyIiwKICAgICJEYXRhc2V0U
25hcHNob3QiLAogICAgIkRhdGFzZXRTcGxpdE1hbmlmZXN0IiwKICAgICJFY29ub21pY1JlcG9ydCIs
CiAgICAiRXhlY3V0aW9uUmVzZWFyY2hFeHBlcmltZW50IiwKICAgICJFeGVjdXRpb25SaXNrUmVzZWF
yY2hSZXBvcnQiLAogICAgIkV4cGVyaW1lbnQiLAogICAgIkZlYXR1cmVEZWZpbml0aW9uIiwKICAgIC
JGZWF0dXJlUXVhbGl0eVJlcG9ydCIsCiAgICAiRmVhdHVyZVJlY29yZCIsCiAgICAiR2VuZXJhbGl6Y
XRpb25SZXBvcnQiLAogICAgIkRyaWZ0TW9uaXRvcmluZ1JlY29yZCIsCiAgICAiSW5nZXN0aW9uUnVu
IiwKICAgICJNYW51YWxUcmFkZUpvdXJuYWxFbnRyeVJlY29yZCIsCiAgICAiTWFya2V0U2VyaWVzTWV
0YWRhdGEiLAogICAgIk1vZGVsQXJ0aWZhY3QiLAogICAgIk1vbml0b3JpbmdBbGVydCIsCiAgICAiT3
BlcmF0b3IiLAogICAgIk9wZXJhdG9yV29ya3NwYWNlUHJlZmVyZW5jZSIsCiAgICAiUG9ydGZvbGlvU
mlza1JlcG9ydCIsCiAgICAiUmVmcmVzaFRva2VuUmVjb3JkIiwKICAgICJSZWdpbWVSZXBvcnQiLAog
ICAgIlJlc2VhcmNoQ29sbGVjdGlvbiIsCiAgICAiUmVzZWFyY2hDb2xsZWN0aW9uTWVtYmVyIiwKICA
gICJSZXNlYXJjaFRhZyIsCiAgICAiU2NlbmFyaW9SZXBvcnQiLAogICAgIlNpZ25hbFZhbGlkYXRpb2
5SZXBvcnQiLAogICAgIlNpbXVsYXRlZEV4ZWN1dGlvblJ1biIsCiAgICAiU2ltdWxhdGVkRmlsbEV2Z
W50IiwKICAgICJTaW11bGF0ZWRFeGVjdXRpb25BbmFseXRpY3NSZXBvcnQiLAogICAgIlNpbXVsYXRl
ZFBhcGVyTGVkZ2VyRW50cnkiLAogICAgIlRyYWRlUGxhbk5vdGVSZWNvcmQiLAogICAgIlZhbGlkYXR
pb25SZXBvcnQiLAogICAgIldzVGlja2V0IiwKICAgICMgVjIKICAgICJWMkF1ZGl0RXZlbnQiLAogIC
AgIlYyTGluZWFnZVJlY29yZCIsCiAgICAiVjJDYXBhYmlsaXR5UmVjb3JkIiwKICAgICJWMlBlcm1pc
3Npb24iLAogICAgIlYyTWRBc09mVmVyaWZpY2F0aW9uIiwKICAgICJWMk1kSW5zdHJ1bWVudCIsCiAg
ICAiVjJNZEludGVncml0eUV4Y2VwdGlvbiIsCiAgICAiVjJNZFNlcmllcyIsCiAgICAiVjJNZFNvdXJ
jZSIsCiAgICAiVjJNZFN5bWJvbE1hcCIsCiAgICAiVjJNZFByb3ZpZGVyIiwKICAgICJWMk1kUHJvdm
lkZXJTdGF0dXNIaXN0b3J5IiwKICAgICJWMkNvbXB1dGF0aW9uVmVyc2lvbiIsCiAgICAiVjJNYXJrZ
XRDb250ZXh0UmVwb3J0IiwKICAgICJWMkNoYXJ0SW50ZWxsaWdlbmNlUmVwb3J0IiwKICAgICJWMk1s
R292ZXJuYW5jZVJlY29yZCIsCiAgICAiVjJNbExpZmVjeWNsZUV2ZW50IiwKICAgICJWMk1sRGlhZ25
vc3RpY1JlcG9ydCIsCiAgICAiVjJTaWduYWxSZWNvcmQiLAogICAgIlYyU2lnbmFsU3RhdGVFdmVudC
IsCiAgICAiVjJQb3J0Zm9saW9EZWZpbml0aW9uIiwKICAgICJWMlBvcnRmb2xpb1Jpc2tSZXBvcnQiL
AogICAgIlYyQmFja3Rlc3RJbnB1dCIsCiAgICAiVjJDb3N0TW9kZWwiLAogICAgIlYyU3RyYXRlZ3lW
ZXJzaW9uIiwKICAgICJWMlJlc2VhcmNoSm9iIiwKICAgICJWMlJlc2VhcmNoSm9iQXR0ZW1wdCIsCiA
gICAiVjJSZXNlYXJjaFJlc3VsdCIsCiAgICAiVjJQYXBlckFjY291bnQiLAogICAgIlYyUGFwZXJPcm
RlckludGVudCIsCiAgICAiVjJQYXBlclJpc2tEZWNpc2lvbiIsCiAgICAiVjJQYXBlck9yZGVyRXZlb
nQiLAogICAgIlYyUGFwZXJGaWxsIiwKICAgICJWMlBhcGVyUG9zaXRpb25TbmFwc2hvdCIsCiAgICAi
VjJQYXBlckJhbGFuY2VTbmFwc2hvdCIsCiAgICAiVjJQYXBlclJlY29uY2lsaWF0aW9uIiwKXQo=
'@
$LandPath = Join-Path $BackendRoot "app\db\models\__init__.py"
New-Item -ItemType Directory -Force -Path (Split-Path $LandPath) | Out-Null
if (!(Test-Path $LandPath)) { throw ("STOP: modified-file target missing at the floor: " + $LandPath) }
$Cur = (Get-FileHash -Path $LandPath -Algorithm SHA256).Hash.ToLower()
if ($Cur -eq "0b188cbf69fb984bb076648eba17c2408d42a5fb29462b6d4ff1ff853f1c6e68") { Write-Evidence ("already landed (pinned bytes): app\db\models\__init__.py") }
elseif ($Cur -eq "32b0f7707fe2bd2556b4e01eed125becff9676f494a960e5a74c0c34de9855e9") {
    [IO.File]::WriteAllBytes($LandPath, (B64-Decode -B64Chunk $Fapp_db_models__init__py))
    $Cur2 = (Get-FileHash -Path $LandPath -Algorithm SHA256).Hash.ToLower()
    if ($Cur2 -ne "0b188cbf69fb984bb076648eba17c2408d42a5fb29462b6d4ff1ff853f1c6e68") { throw ("FAIL: post-write hash drift on " + $LandPath) }
    Write-Evidence ("amended app\db\models\__init__.py: 32b0f7707fe2... -> 0b188cbf69fb...")
} else { throw ("STOP: amended-file target at an unpinned state: app\db\models\__init__.py sha " + $Cur + " . Expected floor " + '32b0f7707fe2bd2556b4e01eed125becff9676f494a960e5a74c0c34de9855e9' + " or landed " + '0b188cbf69fb984bb076648eba17c2408d42a5fb29462b6d4ff1ff853f1c6e68' + " . Nothing modified for this file; report to ITRGA.") }

# file: tests\test_v2_mode.py  (pin 19020e26a80e...)
$Ftests_test_v2_mode_py = @'
IiIiVjIgTW9kZSBUZXN0cyDigJQgbW9kZSBlbmZvcmNlbWVudCwgYnlwYXNzIHJlZnVzYWwsIFBhcGV
yL0xpdmUgcmVmdXNhbC4iIiIKCmZyb20gX19mdXR1cmVfXyBpbXBvcnQgYW5ub3RhdGlvbnMKCmltcG
9ydCBvcwpmcm9tIHVuaXR0ZXN0Lm1vY2sgaW1wb3J0IHBhdGNoCgppbXBvcnQgcHl0ZXN0Cgpmcm9tI
GFwcC52Mi5tb2RlLmNvbnRyYWN0IGltcG9ydCBERUZFUlJFRF9NT0RFUywgVkFMSURfTU9ERVMsIGdl
dF9tb2RlCgoKY2xhc3MgVGVzdFYyTW9kZUNvbnRyYWN0OgogICAgIiIiVGVzdCBWMiBtb2RlIGNvbnR
yYWN0LiIiIgoKICAgIGRlZiB0ZXN0X21vZGVfZGVmYXVsdHNfdG9fcmVzZWFyY2goc2VsZik6CiAgIC
AgICAgIiIiTW9kZSBkZWZhdWx0cyB0byBSRVNFQVJDSCB3aGVuIEFYSU9NX1YyX01PREUgaXMgbm90I
HNldC4iIiIKICAgICAgICB3aXRoIHBhdGNoLmRpY3Qob3MuZW52aXJvbiwge30sIGNsZWFyPUZhbHNl
KToKICAgICAgICAgICAgb3MuZW52aXJvbi5wb3AoIkFYSU9NX1YyX01PREUiLCBOb25lKQogICAgICA
gICAgICBhc3NlcnQgZ2V0X21vZGUoKSA9PSAiUkVTRUFSQ0giCgogICAgZGVmIHRlc3RfbW9kZV9mcm
9tX2Vudl92YXIoc2VsZik6CiAgICAgICAgIiIiTW9kZSBpcyByZWFkIGZyb20gQVhJT01fVjJfTU9ER
SBlbnZpcm9ubWVudCB2YXJpYWJsZS4iIiIKICAgICAgICB3aXRoIHBhdGNoLmRpY3Qob3MuZW52aXJv
biwgeyJBWElPTV9WMl9NT0RFIjogIlNJTVVMQVRJT04ifSk6CiAgICAgICAgICAgIGFzc2VydCBnZXR
fbW9kZSgpID09ICJTSU1VTEFUSU9OIgoKICAgIGRlZiB0ZXN0X21vZGVfY2FzZV9pbnNlbnNpdGl2ZS
hzZWxmKToKICAgICAgICAiIiJNb2RlIHZhbHVlIGlzIGNhc2UtaW5zZW5zaXRpdmUuIiIiCiAgICAgI
CAgd2l0aCBwYXRjaC5kaWN0KG9zLmVudmlyb24sIHsiQVhJT01fVjJfTU9ERSI6ICJyZXNlYXJjaCJ9
KToKICAgICAgICAgICAgYXNzZXJ0IGdldF9tb2RlKCkgPT0gIlJFU0VBUkNIIgoKICAgIGRlZiB0ZXN
0X21vZGVfYWNjZXB0c19wYXBlcihzZWxmKToKICAgICAgICAiIiJQQVBFUiBtb2RlIGlzIHZhbGlkIG
FzIG9mIEJFLTggKEQtMiBydWxpbmcsCiAgICAgICAgSVRSR0EtUkVWLVYyLUJFLTgtREVTSUdOLTAwM
SDCpzY7IEJPLVYyLUJFLTgtMDAxIFQtMikuCiAgICAgICAgU3VwZXJzZWRpbmcgY2h1cm4gb2YgdGhl
IEJFLTEtZXJhIHJlamVjdGlvbiBwaW4g4oCUIGRpc2Nsb3NlZC4iIiIKICAgICAgICB3aXRoIHBhdGN
oLmRpY3Qob3MuZW52aXJvbiwgeyJBWElPTV9WMl9NT0RFIjogIlBBUEVSIn0pOgogICAgICAgICAgIC
Bhc3NlcnQgZ2V0X21vZGUoKSA9PSAiUEFQRVIiCgogICAgZGVmIHRlc3RfbW9kZV9yZWplY3RzX2xpd
mUoc2VsZik6CiAgICAgICAgIiIiTElWRSBtb2RlIGlzIHJlamVjdGVkIChkZWZlcnJlZCB0byBCRS0x
MCkuIiIiCiAgICAgICAgd2l0aCBwYXRjaC5kaWN0KG9zLmVudmlyb24sIHsiQVhJT01fVjJfTU9ERSI
6ICJMSVZFIn0pOgogICAgICAgICAgICB3aXRoIHB5dGVzdC5yYWlzZXMoVmFsdWVFcnJvciwgbWF0Y2
g9IkFYSU9NX1YyX01PREUgbXVzdCBiZSBvbmUgb2YiKToKICAgICAgICAgICAgICAgIGdldF9tb2RlK
CkKCiAgICBkZWYgdGVzdF9tb2RlX3JlamVjdHNfaW52YWxpZChzZWxmKToKICAgICAgICAiIiJJbnZh
bGlkIG1vZGUgdmFsdWVzIGFyZSByZWplY3RlZC4iIiIKICAgICAgICB3aXRoIHBhdGNoLmRpY3Qob3M
uZW52aXJvbiwgeyJBWElPTV9WMl9NT0RFIjogIklOVkFMSUQifSk6CiAgICAgICAgICAgIHdpdGggcH
l0ZXN0LnJhaXNlcyhWYWx1ZUVycm9yLCBtYXRjaD0iQVhJT01fVjJfTU9ERSBtdXN0IGJlIG9uZSBvZ
iIpOgogICAgICAgICAgICAgICAgZ2V0X21vZGUoKQoKICAgIGRlZiB0ZXN0X3ZhbGlkX21vZGVzX2lu
Y2x1ZGVfcGFwZXJfYXNfb2ZfYmU4KHNlbGYpOgogICAgICAgICIiIlZhbGlkIG1vZGVzIGFyZSBSRVN
FQVJDSCwgU0lNVUxBVElPTiwgUEFQRVIgKEQtMiwgQkUtOCkuIiIiCiAgICAgICAgYXNzZXJ0IFZBTE
lEX01PREVTID09ICgiUkVTRUFSQ0giLCAiU0lNVUxBVElPTiIsICJQQVBFUiIpCgogICAgZGVmIHRlc
3RfZGVmZXJyZWRfbW9kZXNfYXJlX2xpdmVfb25seShzZWxmKToKICAgICAgICAiIiJMSVZFIHJlbWFp
bnMgdGhlIHNvbGUgZGVmZXJyZWQgbW9kZSAoQkUtMTApLiIiIgogICAgICAgIGFzc2VydCBERUZFUlJ
FRF9NT0RFUyA9PSAoIkxJVkUiLCkK
'@
$LandPath = Join-Path $BackendRoot "tests\test_v2_mode.py"
New-Item -ItemType Directory -Force -Path (Split-Path $LandPath) | Out-Null
if (!(Test-Path $LandPath)) { throw ("STOP: modified-file target missing at the floor: " + $LandPath) }
$Cur = (Get-FileHash -Path $LandPath -Algorithm SHA256).Hash.ToLower()
if ($Cur -eq "19020e26a80ee7453abd34d88273d7e586c81b4bb075a9729a5016326e687ec4") { Write-Evidence ("already landed (pinned bytes): tests\test_v2_mode.py") }
else {
    $FloorText = [IO.File]::ReadAllText($LandPath)
    if ($FloorText -notmatch [regex]::Escape('def test_mode_rejects_paper')) { throw ("STOP: floor marker absent in tests\test_v2_mode.py - the tree is not at the 0047 floor for this file; nothing modified; report to ITRGA.") }
    [IO.File]::WriteAllBytes($LandPath, (B64-Decode -B64Chunk $Ftests_test_v2_mode_py))
    $Cur2 = (Get-FileHash -Path $LandPath -Algorithm SHA256).Hash.ToLower()
    if ($Cur2 -ne "19020e26a80ee7453abd34d88273d7e586c81b4bb075a9729a5016326e687ec4") { throw ("FAIL: post-write hash drift on " + $LandPath) }
    Write-Evidence ("amended tests\test_v2_mode.py (floor marker proven) -> 19020e26a80e...")
}

# second-pass re-verification of the whole landed set
foreach ($Fp2 in $FilePinsAfter) {
    $Parts2 = $Fp2.Split("|")
    $H2 = (Get-FileHash -Path (Join-Path $BackendRoot $Parts2[0]) -Algorithm SHA256).Hash.ToLower()
    if ($H2 -ne $Parts2[1]) { throw ("FAIL: A4 second-pass verification drift: " + $Parts2[0]) }
}
Write-Evidence "PASS: A4 - all 20 corpus files landed/witnessed and re-verified (sha256 twice)."

# A5. THE SINGLE SANCTIONED SCHEMA MUTATION
Write-Section "A5. alembic upgrade head (20260904_0048) - THE ONE SANCTIONED MUTATION"
Push-Location $BackendRoot
try {
    Write-Evidence ("APPLY: alembic upgrade head  (recorded " + ([DateTime]::UtcNow.ToString("yyyy-MM-ddTHH:mm:ssZ")) + ")")
    $OutUp = Invoke-Capped $Py @('-m', 'alembic', 'upgrade', 'head')
    $UpCode = $LASTEXITCODE
} finally { Pop-Location }
Emit-Output $OutUp
if ($UpCode -ne 0) { throw ("FAIL: A5 - alembic upgrade head exited " + $UpCode + " . The act is void at A5; the A2 anchor is intact; report to ITRGA before any further action.") }
Push-Location $BackendRoot
try {
    $OutCur2 = Invoke-Capped $Py @('-m', 'alembic', 'current')
    $Cur2Lines = @(@($OutCur2) | Where-Object { ([string]$_) -match $ApplyTargetRevision -and ([string]$_) -match [regex]::Escape("(head)") })
    if ($Cur2Lines.Count -ne 1) { throw ("FAIL: A5 - post-upgrade current = " + $ApplyTargetRevision + " (head) not observed: '" + (Norm-Text $OutCur2) + "'.") }
    $OutHeads2 = Invoke-Capped $Py @('-m', 'alembic', 'heads')
    $HeadLines2 = @(@($OutHeads2) | Where-Object { ([string]$_).Trim() -ne "" -and ([string]$_) -notmatch "^INFO" })
    if ($HeadLines2.Count -ne 1 -or (@($HeadLines2 | Where-Object { ([string]$_) -match $ApplyTargetRevision }).Count -ne 1)) { throw ("FAIL: A5 - single head " + $ApplyTargetRevision + " not observed: '" + (Norm-Text $OutHeads2) + "'.") }
} finally { Pop-Location }
Write-Evidence "PASS: A5 - upgrade applied; current = 20260904_0048 (head), single head."

# A6. POST-CENSUS vs BO/ACC LITERALS (independent recomputation)
Write-Section "A6. POST-CENSUS vs ACC LITERALS (58/57/10; exact members; rollhash triple)"
$OutC = Invoke-Capped $Py @($HelperCensus, $TargetDbPath)
if ($LASTEXITCODE -ne 0) { throw ("STOP: census helper failed: " + (Norm-Text $OutC)) }
$Post = (Norm-Text $OutC) | ConvertFrom-Json
if ($Post.triggers.Count -ne $ExpectTriggers) { throw ("STOP: trigger census " + $Post.triggers.Count) }
if ($Post.permissions.Count -ne $ExpectPerms) { throw ("STOP: permission census " + $Post.permissions.Count) }
if ($Post.compver.Count -ne $ExpectCompver) { throw ("STOP: compver census " + $Post.compver.Count) }
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
foreach ($Tn in @("v2_paper_account","v2_paper_order_intent","v2_paper_risk_decision","v2_paper_order_event","v2_paper_fill","v2_paper_position_snapshot","v2_paper_balance_snapshot","v2_paper_reconciliation")) {
    if ($Pst.paper_tables -notcontains $Tn) { throw ("FAIL: paper table missing: " + $Tn) }
}
if ($Pst.alembic_version.Count -ne 1 -or $Pst.alembic_version[0] -ne $ApplyTargetRevision) { throw "FAIL: alembic_version row not exactly 20260904_0048." }
if ([int]$Pst.compver_delete_guard -ne 1) { throw "FAIL: compver delete-guard not present exactly once." }
$OutPxs = Invoke-Capped $Py @($HelperRoll, $BackendRoot, "pxs")
if ($LASTEXITCODE -ne 0 -or (Norm-Text $OutPxs) -ne $PxsHash) { throw ("FAIL: PXS rolling-hash live recomputation " + (Norm-Text $OutPxs) + " != pinned literal.") }
$OutPrg = Invoke-Capped $Py @($HelperRoll, $BackendRoot, "prg")
if ($LASTEXITCODE -ne 0 -or (Norm-Text $OutPrg) -ne $PrgHash) { throw ("FAIL: PRG rolling-hash live recomputation " + (Norm-Text $OutPrg) + " != pinned literal.") }
Write-Evidence "PASS: A6 - censuses exactly 58 / 57 / 10; 16 paper guards + 8 permission triples + 8 paper tables + compver delete-guard present; compver DB rows == literals == live rollhash recomputation (triple agreement); RPE/RJE carried byte-identical."

# A7. LIVE GUARD PROBES (insert-probe-rollback; nothing persists)
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
Write-Evidence "PASS: A7 - six paper guards refuse live with exact messages."

# A8. FULL SUITE (1026 passed / 0 failed)
Write-Section "A8. FULL TEST SUITE (certified pins; tail witnessed)"
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
Write-Evidence ("PASS: A8 - suite summary: " + ([string]$SuiteSummary).Trim())

# A9. DRIFT GATE at head (PGF-014 format-independent)
Write-Section "A9. DRIFT GATE AT 20260904_0048 (format-independent)"
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
Write-Evidence "PASS: A9 - POST-drift gate at 20260904_0048: non-zero exit, zero BE-8 tokens, inheritance witness present."

# A10. APPLY-FINAL-STATE RECORD
Write-Section "A10. APPLY-FINAL-STATE RECORD (15-key VERIFY contract)"
$DbShaPost = (Get-FileHash -Path $TargetDbPath -Algorithm SHA256).Hash.ToLower()
Write-Evidence ("DB sha256 POST: " + $DbShaPost)
if ($DbShaPost -eq $SealedDbSha) { throw "FAIL: A10 - POST sha256 equals the sealed pre-state; the sanctioned mutation left no trace." }
$AnchorRecheck = (Get-FileHash -Path $AnchorPath -Algorithm SHA256).Hash.ToLower()
if ($AnchorRecheck -ne $DbShaPre) { throw "FAIL: A10 - anchor drifted during the act." }
# PGF-023: inside @(...) array literals the element comma binds before binary +;
# parenthesize every concatenated element.
$VLines = @(
    "STATE_FILE_ID=ITRGA-V2-0048-APPLY-FINAL-STATE-V1",
    ("TARGET_REVISION=" + $ApplyTargetRevision),
    ("TRIGGERS_TOTAL=" + $ExpectTriggersTotal),
    ("PERMISSIONS_TOTAL=" + $ExpectPermsTotal),
    ("COMPVER_TOTAL=" + $ExpectCompverTotal),
    ("COMPVER_RPE_HASH=" + $RpeHash),
    ("COMPVER_RJE_HASH=" + $RjeHash),
    ("COMPVER_PXS_HASH=" + $PxsHash),
    ("COMPVER_PRG_HASH=" + $PrgHash),
    ("SUITE_RESULT=" + ([string]$SuiteSummary).Trim()),
    ("DB_PATH=" + $TargetDbPath),
    ("DB_SHA256_POST=" + $DbShaPost),
    ("ANCHOR_SHA256=" + $AnchorRecheck),
    "TRANSCRIPT=0048-APPLY-RUN-V1.txt",
    ("UTC_COMPLETED=" + ([DateTime]::UtcNow.ToString("yyyy-MM-ddTHH:mm:ssZ")))
)
$VLines | Set-Content -Path $ApplyRecPath -Encoding UTF8
foreach ($Vl in $VLines) { Write-Evidence ("STATE: " + $Vl) }
Write-Evidence ""
Write-Evidence "APPLY PACK COMPLETE - PASS. The 0048 working-DB application act executed on the sealed console lineage. NEXT: run ITRGA_V2_0048_VERIFY_PACK_V1.ps1 (it chains against this record); keep the application STOPPED until verify PASSes. Send back operator-evidence\BE-8\0048-APPLY-RUN-V1.txt."
Write-Evidence ("UTC end: " + ([DateTime]::UtcNow.ToString("yyyy-MM-ddTHH:mm:ssZ")))

Remove-Helpers

