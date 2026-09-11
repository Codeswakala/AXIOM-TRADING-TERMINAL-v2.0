<#
===============================================================================
ITRGA_V2_0056_APPLY_PACK_V1.ps1
===============================================================================
Pack:      ITRGA-V2-0056-APPLY-PACK-V1
Act:       0056 working-database application act (single sanctioned mutation)
Implements: ITRGA-V2-0056-FIELD-APPLY-CARD-20260909 (the card remains the
           governing text; this pack is the authorized equivalent runner).
Authority: BO-V2-BE12D-001 SS1.g  ·  ITRGA-REV-V2-BE12D-001 (APPROVED;
           LOW V2-BE12D-DEL-001 register-logged for 12E; BE-12D ACCEPTED;
           suite floor 1,290)
Mutation:  EXACTLY ONE —  python -m alembic upgrade 20260909_0056
           against the fielded working database axiom_dev.db.
           Rehearsal runs on a byte-copy ONLY. All guard/CHECK probes are
           refused-write and always rolled back.
FIELD LAW (12D-specific): ZERO seed rows is the migration doctrine — both
           new tables are pinned ZERO ROWS at every witness point, before and
           after every probe. NO GOVERNOR VERB runs on the fielded file (no
           arm/pull/clear; activation has no writer by build); the kill-switch
           valve NEVER opens in this pack. Probe INSERTs prove only that the
           guards/CHECKs fire, and are always rolled back.
Method:    NO python FILES of any kind (-c snippets only). NO git operations.
           NO credential of any kind. AXIOM_BROKER_PRACTICE_* / AXIOM_TD_*
           asserted ABSENT at start and end.
Errata:    CHECK pins are RENDERED names (E-0055-A10.3, from birth —
           enumerated from the delivery's migration coupon, cross-pinned by
           the A9 DDL print). Drift gate ITEMIZED (E-0054-A11.4).
Run:       Set-Location C:\Users\victo\.vscode\AXIOM\axiom
           powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\ITRGA_V2_0056_APPLY_PACK_V1.ps1
Output:    operator-evidence\BE-12D\0056-APPLY-RUN-V1-<timestamp>.txt  (transcript)
           operator-evidence\BE-12D\0056-APPLY-FINAL-STATE.txt         (state record)
On any gate failure: HALT at the failing gate; no retry; no mutation re-run.
Send the transcript. Restoration is via the anchor only, under ITRGA order.
Do NOT re-run post-apply: it halts at A1.1 by design (idempotence).
===============================================================================
#>

$ErrorActionPreference = 'Stop'
Set-Location C:\Users\victo\.vscode\AXIOM\axiom

# ---------------------------------------------------------------- constants --
$RepoRoot      = 'C:\Users\victo\.vscode\AXIOM\axiom'
$Backend       = 'C:\Users\victo\.vscode\AXIOM\axiom\backend'
$Py            = 'C:\Users\victo\.vscode\AXIOM\axiom\.venv\Scripts\python.exe'
$Target        = 'C:\Users\victo\.vscode\AXIOM\axiom\backend\axiom_dev.db'
$EvDir         = 'C:\Users\victo\.vscode\AXIOM\axiom\operator-evidence\BE-12D'
$MigFile       = 'C:\Users\victo\.vscode\AXIOM\axiom\backend\alembic\versions\20260909_0056_v2_be12d_activation_killswitch.py'

$MigSha        = '1A43E5A211609934F6C720D1FF595A1BA1B9374EA6D0C111BD762FDBBA4D7CD2'
$MigLen        = 10521
$Lxe6Expect    = 'b060f435c7c339fbe5e23daf8231af04bf62cd8cc43ccd7d8a5f5067b78bb8c2'
$Lxe8Expect    = 'd09306f1ab32f0dc6f26e5c7235b3e1f72c3175a1928d60673709c0b02a3809a'
$Lxe13Expect   = 'd25c48579def993b63e6f84ca17e937c3e938f75b0ca1f78f8aea81b1e9c1705'
$LxeRow100     = 'live_exec_engine|lxe-1.0.0|b060f435c7c339fbe5e23daf8231af04bf62cd8cc43ccd7d8a5f5067b78bb8c2|BO-V2-BE12B-001'
$LxeRow110     = 'live_exec_engine|lxe-1.1.0|d09306f1ab32f0dc6f26e5c7235b3e1f72c3175a1928d60673709c0b02a3809a|BO-V2-BE12C-001'
$LxeRow120     = 'live_exec_engine|lxe-1.2.0|d25c48579def993b63e6f84ca17e937c3e938f75b0ca1f78f8aea81b1e9c1705|BO-V2-BE12D-001'
$LxeRowsPre    = $LxeRow100 + "`n" + $LxeRow110
$LxeRowsPost   = $LxeRowsPre + "`n" + $LxeRow120
$PermRowsExpect= @(
  'admin|v2.live_exec.activation.read|SAL-2',
  'admin|v2.live_exec.activation.template.read|SAL-3',
  'admin|v2.live_exec.killswitch.arm|SAL-4',
  'admin|v2.live_exec.killswitch.clear|SAL-4',
  'admin|v2.live_exec.killswitch.pull|SAL-4',
  'admin|v2.live_exec.killswitch.read|SAL-2'
) -join "`n"
$NewPerms      = @('v2.live_exec.activation.read','v2.live_exec.activation.template.read','v2.live_exec.killswitch.arm','v2.live_exec.killswitch.clear','v2.live_exec.killswitch.pull','v2.live_exec.killswitch.read')
$GuardNamesPre = @('v2_live_exec_fill_event_immutable_delete','v2_live_exec_fill_event_immutable_update','v2_live_exec_intent_immutable_delete','v2_live_exec_intent_immutable_update','v2_live_exec_modify_event_immutable_delete','v2_live_exec_modify_event_immutable_update','v2_live_exec_submission_immutable_delete','v2_live_exec_submission_immutable_update') -join "`n"
$GuardNamesAll = @('v2_live_activation_instrument_immutable_delete','v2_live_activation_instrument_immutable_update','v2_live_exec_fill_event_immutable_delete','v2_live_exec_fill_event_immutable_update','v2_live_exec_intent_immutable_delete','v2_live_exec_intent_immutable_update','v2_live_exec_modify_event_immutable_delete','v2_live_exec_modify_event_immutable_update','v2_live_exec_submission_immutable_delete','v2_live_exec_submission_immutable_update','v2_live_kill_switch_immutable_delete','v2_live_kill_switch_immutable_update')
$IndexNamesAll = @('ix_v2_lxfill_created','ix_v2_lxmod_created','ix_v2_lxsub_created','uq_v2_lai_sole','uq_v2_lks_sole','uq_v2_lxfill_identity','uq_v2_lxmod_identity','uq_v2_lxsub_intent')
$CvuOld        = 'REFUSED:V2 computation version registry is immutable; UPDATE prohibited'
$CvdOld        = 'REFUSED:V2 computation version registry is immutable; DELETE prohibited'
$CvdNewLiteral = 'REFUSED:V2 computation versions are immutable; DELETE prohibited'
$ActUpd        = 'REFUSED:V2 live activation instrument is immutable; UPDATE prohibited'
$ActDel        = 'REFUSED:V2 live activation instrument is immutable; DELETE prohibited'
$KsUpd         = 'REFUSED:V2 live kill switch is immutable; UPDATE prohibited'
$KsDel         = 'REFUSED:V2 live kill switch is immutable; DELETE prohibited'
$CkLaiSole     = 'REFUSED:CHECK constraint failed: ck_v2_live_activation_instrument_ck_v2_lai_sole'
$CkLaiVersion  = 'REFUSED:CHECK constraint failed: ck_v2_live_activation_instrument_ck_v2_lai_version'
$CkLaiClass    = 'REFUSED:CHECK constraint failed: ck_v2_live_activation_instrument_ck_v2_lai_data_class'
$CkLksSole     = 'REFUSED:CHECK constraint failed: ck_v2_live_kill_switch_ck_v2_lks_sole'
$CkLksStatus   = 'REFUSED:CHECK constraint failed: ck_v2_live_kill_switch_ck_v2_lks_status'
$CkLksClass    = 'REFUSED:CHECK constraint failed: ck_v2_live_kill_switch_ck_v2_lks_data_class'
$DriftWhitelist= @(
  'audit_write_failure_records','ix_audit_write_failures_category_action',
  'ix_audit_write_failures_created','ix_advisory_signals_expires_at',
  'ix_advisory_signals_freshness_status','ix_ingestion_runs_symbol_started',
  'ix_model_artifacts_advisory_status','ix_model_artifacts_artifact_hash',
  'ix_model_artifacts_experiment_id'
)
$DriftForbidden= @('v2_','live_exec','lxmod','modify_event','activation_instrument','kill_switch')

$ts             = Get-Date -Format yyyyMMddHHmmss
$TranscriptPath = Join-Path $EvDir ("0056-APPLY-RUN-V1-{0}.txt" -f $ts)
$FinalStatePath = Join-Path $EvDir '0056-APPLY-FINAL-STATE.txt'
$Anchor         = Join-Path $EvDir ("axiom_dev.db.pre-0056-{0}.bak" -f $ts)
$Reh            = Join-Path $EvDir ("axiom_dev.db.rehearsal-0056-{0}.db" -f $ts)

# ------------------------------------------------------- fileless SQL engine -
$CodeRead = @'
import sqlite3,sys
c=sqlite3.connect(sys.argv[1])
try:
 rows=c.execute(sys.argv[2]).fetchall()
 for r in rows:
  print('|'.join('<null>' if v is None else str(v) for v in r))
finally:
 c.close()
'@

$CodeRefuse = @'
import sqlite3,sys
c=sqlite3.connect(sys.argv[1])
c.isolation_level=None
try:
 c.execute('BEGIN')
 try:
  cur=c.execute(sys.argv[2])
  print('NOTREFUSED:rowcount=%d'%cur.rowcount)
 except sqlite3.Error as e:
  print('REFUSED:%s'%e)
 c.execute('ROLLBACK')
finally:
 c.close()
'@

$CodeGuard = @'
import sqlite3,sys
c=sqlite3.connect(sys.argv[1])
c.isolation_level=None
try:
 c.execute('BEGIN')
 try:
  c.execute(sys.argv[3])
 except sqlite3.Error as e:
  print('REFUSED-INSERT:%s'%e)
  c.execute('ROLLBACK')
  sys.exit(0)
 try:
  cur=c.execute(sys.argv[4])
  print('NOTREFUSED:rowcount=%d'%cur.rowcount)
 except sqlite3.Error as e:
  print('REFUSED:%s'%e)
 c.execute('ROLLBACK')
 left=c.execute('SELECT COUNT(*) FROM '+sys.argv[2]+' WHERE id='+chr(39)+'__guardprobe_0056__'+chr(39)).fetchone()[0]
 print('rolledback=%d'%(1 if left==0 else 0))
finally:
 c.close()
'@

$CodeLxe6 = @'
import hashlib,sys
from pathlib import Path
refs=('app/v2/live_exec/intents.py','app/v2/live_exec/eligibility.py','app/v2/live_exec/risk.py','app/v2/live_exec/locks.py','app/v2/live_exec/submissions.py','app/v2/live_exec/ack_fills.py')
b=Path(sys.argv[1]).resolve()
d=hashlib.sha256()
for r in refs:
 d.update(r.encode('utf-8'))
 d.update(b'\x00')
 d.update((b/r).read_bytes())
 d.update(b'\x00')
print(d.hexdigest())
'@

$CodeLxe8 = @'
import hashlib,sys
from pathlib import Path
refs=('app/v2/live_exec/intents.py','app/v2/live_exec/eligibility.py','app/v2/live_exec/risk.py','app/v2/live_exec/locks.py','app/v2/live_exec/submissions.py','app/v2/live_exec/ack_fills.py','app/v2/live_exec/modify/__init__.py','app/v2/live_exec/modify/engine.py')
b=Path(sys.argv[1]).resolve()
d=hashlib.sha256()
for r in refs:
 d.update(r.encode('utf-8'))
 d.update(b'\x00')
 d.update((b/r).read_bytes())
 d.update(b'\x00')
print(d.hexdigest())
'@

$CodeLxe13 = @'
import hashlib,sys
from pathlib import Path
refs=('app/v2/live_exec/intents.py','app/v2/live_exec/eligibility.py','app/v2/live_exec/risk.py','app/v2/live_exec/locks.py','app/v2/live_exec/submissions.py','app/v2/live_exec/ack_fills.py','app/v2/live_exec/modify/__init__.py','app/v2/live_exec/modify/engine.py','app/v2/live_exec/activation/__init__.py','app/v2/live_exec/activation/engine.py','app/v2/live_exec/activation/template.py','app/v2/live_exec/killswitch/__init__.py','app/v2/live_exec/killswitch/engine.py')
b=Path(sys.argv[1]).resolve()
d=hashlib.sha256()
for r in refs:
 d.update(r.encode('utf-8'))
 d.update(b'\x00')
 d.update((b/r).read_bytes())
 d.update(b'\x00')
print(d.hexdigest())
'@

# ------------------------------------------------------------------ helpers --
function ConvertTo-Text { param($Items)
  $lines = foreach ($i in $Items) {
    if ($i -is [System.Management.Automation.ErrorRecord]) { $i.Exception.Message } else { [string]$i }
  }
  return ($lines -join "`n")
}

function Write-Section { param([string]$Title)
  Write-Host ''
  Write-Host ('=' * 78)
  Write-Host $Title
  Write-Host ('=' * 78)
}

function Assert-Gate { param([bool]$Cond, [string]$Label, [string]$Expect, [string]$Actual)
  if ($Cond) { Write-Host ("PASS: {0}" -f $Label); return }
  Write-Host ("FAIL: {0}" -f $Label)
  Write-Host ("  EXPECTED: {0}" -f $Expect)
  Write-Host ("  ACTUAL  : {0}" -f $Actual)
  Write-Host ''
  Write-Host 'HALT: gate failed. Do NOT re-run this pack. Do NOT run any further command.'
  if ($script:AnchorCreated -and (Test-Path $Anchor)) {
    Write-Host ("Anchor copy (pre-image): {0}" -f $Anchor)
    Write-Host 'Restoration (if ITRGA instructs) is via the anchor only.'
  } else {
    Write-Host 'No mutation occurred before this halt: no anchor was created; nothing to restore.'
  }
  Write-Host 'Send this transcript to ITRGA.'
  if ($script:TranscriptOn) { try { Stop-Transcript | Out-Null } catch { } ; $script:TranscriptOn = $false }
  exit 1
}

function Count-Hits { param([string]$Text, [string]$Needle)
  return [regex]::Matches($Text, [regex]::Escape($Needle)).Count
}

function Invoke-Read { param([string]$Db, [string]$Sql)
  $raw = & $Py -c $CodeRead $Db $Sql 2>&1
  return (ConvertTo-Text @($raw)).TrimEnd()
}

function Invoke-Refuse { param([string]$Db, [string]$Sql)
  $raw = & $Py -c $CodeRefuse $Db $Sql 2>&1
  return (ConvertTo-Text @($raw)).TrimEnd()
}

function Invoke-GuardProbe { param([string]$Db, [string]$Table, [string]$InsertSql, [string]$ProbeSql)
  $raw = & $Py -c $CodeGuard $Db $Table $InsertSql $ProbeSql 2>&1
  return ((ConvertTo-Text @($raw)).TrimEnd() -split "`r?`n")
}

function Invoke-Lxe { param([string]$BackendDir, [string]$Code)
  $raw = & $Py -c $Code $BackendDir 2>&1
  return (ConvertTo-Text @($raw)).TrimEnd()
}

function Invoke-Alembic { param([string]$Db, [string]$ArgLine)
  $env:AXIOM_DATABASE_URL = 'sqlite+aiosqlite:///' + ($Db -replace '\\','/')
  Push-Location $Backend
  try {
    $raw = @(& cmd /c "`"$Py`" -m alembic $ArgLine 2>&1")
    $code = $LASTEXITCODE
  } finally { Pop-Location }
  $text = ConvertTo-Text $raw
  Write-Host $text
  $result = New-Object PSObject -Property @{ Text = $text; Code = $code }
  return $result
}

function Get-AlembicCurrent { param([string]$Text)
  $cands = @()
  foreach ($ln in ($Text -split "`r?`n")) {
    if ($ln.Trim() -match '^20\d{6}_\d{4}') { $cands += $ln.Trim() }
  }
  if ($cands.Count -eq 0) { return '(none found)' }
  return $cands[$cands.Count - 1]
}

function Assert-NoBadTokens { param([string]$Text, [string]$Label)
  foreach ($tok in @('ERROR','Traceback','REFUSED','RuntimeError','NOT restored')) {
    Assert-Gate (-not $Text.Contains($tok)) ("{0}: token '{1}' absent" -f $Label, $tok) ("absent") ("present") | Out-Null
  }
}

function Set-Equal { param([string[]]$A, [string[]]$B)
  if ($A.Count -ne $B.Count) { return $false }
  for ($i = 0; $i -lt $A.Count; $i++) { if ($A[$i] -ne $B[$i]) { return $false } }
  return $true
}

# ------------------------------------------------------------------- A0/BEGIN
New-Item -ItemType Directory -Force $EvDir | Out-Null
$script:TranscriptOn = $true
$script:AnchorCreated = $false
Start-Transcript -Path $TranscriptPath | Out-Null

try {

Write-Section 'A0. RUN IDENTIFICATION'
Write-Host 'Pack: ITRGA-V2-0056-APPLY-PACK-V1'
Write-Host 'Act: 0056 working-database application act (single sanctioned mutation)'
Write-Host 'Implements: ITRGA-V2-0056-FIELD-APPLY-CARD-20260909 (governing text)'
Write-Host 'Authority: BO-V2-BE12D-001 SS1.g / ITRGA-REV-V2-BE12D-001 (APPROVED)'
Write-Host ("Started: {0}" -f (Get-Date -Format 'yyyy-MM-dd HH:mm:ss zzz'))
Write-Host ("Target file: {0}" -f $Target)
Write-Host 'FIELD LAW: both new tables pinned ZERO ROWS throughout; NO governor verb runs; the valve never opens.'
Write-Host 'Server credentials used: NONE. Provider credentials used: NONE.'
Write-Host ''
Write-Host 'STOP THE RUNNING APPLICATION. Continuing in 5 seconds; press Ctrl+C otherwise...'
Start-Sleep -Seconds 5

Write-Section 'A0b. AUTHORITY/PRACTICE ENVIRONMENT SWEEP (must print nothing)'
$sweep = @(Get-ChildItem env: | Where-Object { $_.Name -match '^AXIOM_(TD|BROKER_PRACTICE)' })
Assert-Gate ($sweep.Count -eq 0) 'A0b: no AXIOM_TD_* / AXIOM_BROKER_PRACTICE_* variables' 'absent' (($sweep | ForEach-Object { $_.Name }) -join ', ')

Write-Section 'A0c. FILE EXISTENCE'
Assert-Gate (Test-Path $Py)      'A0c.1 venv python present' $Py '(missing)'
Assert-Gate (Test-Path $Target)  'A0c.2 target db present'   $Target '(missing)'
Assert-Gate (Test-Path $MigFile) 'A0c.3 migration 0056 present' $MigFile '(missing)'

Write-Section 'A0d. 12D SOURCE-SET VISIBILITY (thirteen lxe files)'
$lxeRel = @('app/v2/live_exec/intents.py','app/v2/live_exec/eligibility.py','app/v2/live_exec/risk.py','app/v2/live_exec/locks.py','app/v2/live_exec/submissions.py','app/v2/live_exec/ack_fills.py','app/v2/live_exec/modify/__init__.py','app/v2/live_exec/modify/engine.py','app/v2/live_exec/activation/__init__.py','app/v2/live_exec/activation/engine.py','app/v2/live_exec/activation/template.py','app/v2/live_exec/killswitch/__init__.py','app/v2/live_exec/killswitch/engine.py')
$missing = @()
foreach ($rel in $lxeRel) {
  $p = Join-Path $Backend ($rel -replace '/','\')
  if (Test-Path $p) { Write-Host ("  present  {0}" -f $rel) } else { Write-Host ("  MISSING  {0}" -f $rel); $missing += $rel }
}
Assert-Gate ($missing.Count -eq 0) 'A0d: all thirteen lxe source files present (12D landed)' '13/13 present' (($missing.Count.ToString() + ' missing: ') + ($missing -join ', '))

Write-Section 'A1. BASELINE REVISION STATE'
$r = Invoke-Alembic $Target 'current'
Assert-Gate ($r.Code -eq 0) 'A1.0 alembic current exit 0' '0' ([string]$r.Code)
$cur = Get-AlembicCurrent $r.Text
Assert-Gate ($cur -eq '20260909_0055') 'A1.1 current is exactly 20260909_0055 (no (head) suffix)' '20260909_0055' $cur
$r = Invoke-Alembic $Target 'heads'
$headsLines = @($r.Text -split "`r?`n" | Where-Object { $_.Contains('(head)') })
Assert-Gate (($headsLines.Count -ge 1) -and $headsLines[0].Trim().StartsWith('20260909_0056')) 'A1.2 repo head is 20260909_0056 (head)' '20260909_0056 (head)' ($headsLines -join ' / ')
& $Py -m alembic --version 2>&1 | ForEach-Object { Write-Host ("Alembic version: {0}" -f (ConvertTo-Text @($_))) }

Write-Section 'A2. THE 0056 FILE PIN (byte-still recital)'
$migLenActual = (Get-Item $MigFile).Length
$migShaActual = (Get-FileHash -Algorithm SHA256 $MigFile).Hash
Write-Host ("  length  {0} (pinned {1})" -f $migLenActual, $MigLen)
Write-Host ("  sha256  {0}" -f $migShaActual)
Assert-Gate ($migLenActual -eq $MigLen) 'A2.1 migration length' $MigLen ([string]$migLenActual)
Assert-Gate ($migShaActual -ieq $MigSha) 'A2.2 migration sha256' $MigSha $migShaActual

Write-Section 'A3. TATTOO PRE + NAMED-OBJECT PRE-LISTS'
Assert-Gate ((Invoke-Read $Target "SELECT COUNT(*) FROM sqlite_master WHERE type='trigger'") -eq '86') 'A3.1 triggers total == 86' '86' '(see above)'
Assert-Gate ((Invoke-Read $Target 'SELECT COUNT(*) FROM v2_permission') -eq '77') 'A3.2 v2_permission == 77' '77' '(see above)'
Assert-Gate ((Invoke-Read $Target 'SELECT COUNT(*) FROM v2_computation_version') -eq '15') 'A3.3 v2_computation_version == 15' '15' '(see above)'
$guardAll = ($GuardNamesAll | ForEach-Object { "'{0}'" -f $_ }) -join ','
$gpre = Invoke-Read $Target ("SELECT name FROM sqlite_master WHERE type='trigger' AND name IN ({0}) ORDER BY name" -f $guardAll)
Assert-Gate ($gpre -eq $GuardNamesPre) 'A3.4 live_exec guard set pre == the eight 12B/12C names (activation/kill pairs ABSENT)' $GuardNamesPre $gpre
$lxePre = Invoke-Read $Target "SELECT component, version, source_hash, evidence_ref FROM v2_computation_version WHERE component='live_exec_engine' ORDER BY version"
Assert-Gate ($lxePre -eq $LxeRowsPre) 'A3.5 compver pre == ONLY lxe-1.0.0 + lxe-1.1.0 (content-exact)' $LxeRowsPre $lxePre
$permIn = ($NewPerms | ForEach-Object { "'{0}'" -f $_ }) -join ','
Assert-Gate ((Invoke-Read $Target ("SELECT COUNT(*) FROM v2_permission WHERE permission IN ({0})" -f $permIn)) -eq '0') 'A3.6 the six 12D permission rows ABSENT pre-apply' '0' '(see above)'
Assert-Gate ((Invoke-Read $Target "SELECT COUNT(*) FROM sqlite_master WHERE type='table' AND name IN ('v2_live_activation_instrument','v2_live_kill_switch')") -eq '0') 'A3.7 both 12D tables ABSENT pre-apply' '0' '(see above)'
$IntentCountPre = Invoke-Read $Target 'SELECT COUNT(*) FROM v2_live_exec_intent'
$IntentDigestsPre = Invoke-Read $Target 'SELECT digest FROM v2_live_exec_intent ORDER BY digest'
Write-Host ("  12A intent ledger rows (recorded): {0}" -f $IntentCountPre)
Write-Host ("  12A intent digests (recorded): {0}" -f ($IntentDigestsPre -replace "`r?`n",'; '))

Write-Section 'A4. HEALTH PRE + ANCHOR'
Assert-Gate ((Invoke-Read $Target 'PRAGMA integrity_check') -eq 'ok') 'A4.1 integrity_check ok' 'ok' '(see above)'
Assert-Gate ((Invoke-Read $Target 'PRAGMA journal_mode') -eq 'delete') 'A4.2 journal delete' 'delete' '(see above)'
Assert-Gate ((-not (Test-Path ($Target + '-wal'))) -and (-not (Test-Path ($Target + '-shm')))) 'A4.3 no sidecars' 'absent' 'present'
Copy-Item $Target $Anchor
$script:AnchorCreated = $true
Assert-Gate ((Invoke-Read $Anchor 'PRAGMA integrity_check') -eq 'ok') 'A4.4 anchor integrity ok' 'ok' '(see above)'
Assert-Gate ((Invoke-Read $Anchor 'SELECT version_num FROM alembic_version') -eq '20260909_0055') 'A4.5 anchor revision 20260909_0055' '20260909_0055' '(see above)'
$AnchorLen = (Get-Item $Anchor).Length
$AnchorSha = (Get-FileHash -Algorithm SHA256 $Anchor).Hash
Write-Host ("  anchor: {0}" -f $Anchor)
Write-Host ("  anchor size {0} sha256 {1}" -f $AnchorLen, $AnchorSha)

Write-Section 'A5. TRIPLE LXE PRE-COMPUTE GATES (halts precede any mutation)'
$lxe6 = Invoke-Lxe $Backend $CodeLxe6
Write-Host ("  6-file computed: {0}" -f $lxe6)
Assert-Gate ($lxe6 -eq $Lxe6Expect) 'A5a 12A/12B six-file lxe unmoved (b060f435...)' $Lxe6Expect $lxe6
$lxe8 = Invoke-Lxe $Backend $CodeLxe8
Write-Host ("  8-file computed: {0}" -f $lxe8)
Assert-Gate ($lxe8 -eq $Lxe8Expect) 'A5b 12C eight-file lxe unmoved (d09306f1...)' $Lxe8Expect $lxe8
$lxe13 = Invoke-Lxe $Backend $CodeLxe13
Write-Host (" 13-file computed: {0}" -f $lxe13)
Assert-Gate ($lxe13 -eq $Lxe13Expect) 'A5c 12D thirteen-file lxe landed EXACTLY (d25c4857...)' $Lxe13Expect $lxe13

Write-Section 'A6. REHEARSAL UPGRADE (byte-copy only)'
Copy-Item $Target $Reh
$r = Invoke-Alembic $Reh 'upgrade 20260909_0056'
Assert-Gate ($r.Code -eq 0) 'A6.0 rehearsal upgrade exit 0' '0' ([string]$r.Code)
Assert-Gate ((Count-Hits $r.Text 'Running upgrade 20260909_0055 -> 20260909_0056') -eq 1) 'A6.1 exactly one Running upgrade line' '1' ([string](Count-Hits $r.Text 'Running upgrade 20260909_0055 -> 20260909_0056'))
Assert-NoBadTokens $r.Text 'A6.2 rehearsal console'
Assert-Gate ((Invoke-Read $Reh "SELECT COUNT(*) FROM sqlite_master WHERE type='trigger'") -eq '90') 'A6.3 rehearsal triggers 90' '90' '(see above)'
Assert-Gate ((Invoke-Read $Reh 'SELECT COUNT(*) FROM v2_permission') -eq '83') 'A6.4 rehearsal perms 83' '83' '(see above)'
Assert-Gate ((Invoke-Read $Reh 'SELECT COUNT(*) FROM v2_computation_version') -eq '16') 'A6.5 rehearsal compver 16' '16' '(see above)'
$lxeReh = Invoke-Read $Reh "SELECT component, version, source_hash, evidence_ref FROM v2_computation_version WHERE component='live_exec_engine' ORDER BY version"
Assert-Gate ($lxeReh -eq $LxeRowsPost) 'A6.6 rehearsal compver rows ALL THREE stand, content-exact' $LxeRowsPost $lxeReh
Assert-Gate ((Invoke-Read $Reh 'SELECT COUNT(*) FROM v2_live_activation_instrument') -eq '0') 'A6.7 rehearsal activation ZERO ROWS (no seeds)' '0' '(see above)'
Assert-Gate ((Invoke-Read $Reh 'SELECT COUNT(*) FROM v2_live_kill_switch') -eq '0') 'A6.8 rehearsal kill_switch ZERO ROWS (no seeds)' '0' '(see above)'

Write-Section 'A7. REHEARSAL DOWNGRADE PROOF (full reversibility, on the copy)'
$r = Invoke-Alembic $Reh 'downgrade 20260909_0055'
Assert-Gate ($r.Code -eq 0) 'A7.0 rehearsal downgrade exit 0' '0' ([string]$r.Code)
Assert-Gate ((Count-Hits $r.Text 'Running downgrade 20260909_0056 -> 20260909_0055') -eq 1) 'A7.1 exactly one Running downgrade line' '1' ([string](Count-Hits $r.Text 'Running downgrade 20260909_0056 -> 20260909_0055'))
Assert-NoBadTokens $r.Text 'A7.2 rehearsal console (incl. compver delete-guard dance silent)'
Assert-Gate ((Invoke-Read $Reh 'SELECT version_num FROM alembic_version') -eq '20260909_0055') 'A7.3 rehearsal revision restored 20260909_0055' '20260909_0055' '(see above)'
Assert-Gate ((Invoke-Read $Reh "SELECT COUNT(*) FROM sqlite_master WHERE type='trigger'") -eq '86') 'A7.4 rehearsal triggers restored 86' '86' '(see above)'
Assert-Gate ((Invoke-Read $Reh 'SELECT COUNT(*) FROM v2_permission') -eq '77') 'A7.5 rehearsal perms restored 77' '77' '(see above)'
Assert-Gate ((Invoke-Read $Reh 'SELECT COUNT(*) FROM v2_computation_version') -eq '15') 'A7.6 rehearsal compver restored 15' '15' '(see above)'
Assert-Gate ((Invoke-Read $Reh "SELECT COUNT(*) FROM sqlite_master WHERE type='table' AND name IN ('v2_live_activation_instrument','v2_live_kill_switch')") -eq '0') 'A7.7 rehearsal both tables removed' '0' '(see above)'
$lxeDown = Invoke-Read $Reh "SELECT component, version, source_hash, evidence_ref FROM v2_computation_version WHERE component='live_exec_engine' ORDER BY version"
Assert-Gate ($lxeDown -eq $LxeRowsPre) 'A7.8 rehearsal compver == 1.0.0 + 1.1.0 only (1.2.0 removed)' $LxeRowsPre $lxeDown
Write-Host 'NOTE (register-logged advisory, not a finding): recreated compver DELETE guard carries the migration literal (versions vs version registry); invariant identical; visible only on a downgraded chain.'
$cvdReh = Invoke-Refuse $Reh "DELETE FROM v2_computation_version WHERE component='indicator_engine'"
Assert-Gate ($cvdReh -eq $CvdNewLiteral) 'A7.9 rehearsal recreated-guard refusal (documented literal)' $CvdNewLiteral $cvdReh

Write-Section 'A8. THE APPLY (single sanctioned mutation, fielded file)'
Write-Host ("Target: {0}" -f $Target)
$r = Invoke-Alembic $Target 'upgrade 20260909_0056'
Assert-Gate ($r.Code -eq 0) 'A8.0 apply exit 0' '0' ([string]$r.Code)
Assert-Gate ((Count-Hits $r.Text 'Running upgrade 20260909_0055 -> 20260909_0056') -eq 1) 'A8.1 exactly one Running upgrade line' '1' ([string](Count-Hits $r.Text 'Running upgrade 20260909_0055 -> 20260909_0056'))
Assert-NoBadTokens $r.Text 'A8.2 apply console'

Write-Section 'A9. FIELDED TERMINAL STATE'
$r = Invoke-Alembic $Target 'current'
$cur = Get-AlembicCurrent $r.Text
Assert-Gate ($cur -eq '20260909_0056 (head)') 'A9.1 stamped 20260909_0056 (head)' '20260909_0056 (head)' $cur
Assert-Gate ((Invoke-Read $Target "SELECT COUNT(*) FROM sqlite_master WHERE type='trigger'") -eq '90') 'A9.2 triggers 90' '90' '(see above)'
Assert-Gate ((Invoke-Read $Target 'SELECT COUNT(*) FROM v2_permission') -eq '83') 'A9.3 perms 83' '83' '(see above)'
Assert-Gate ((Invoke-Read $Target 'SELECT COUNT(*) FROM v2_computation_version') -eq '16') 'A9.4 compver 16' '16' '(see above)'
$gpost = Invoke-Read $Target ("SELECT name FROM sqlite_master WHERE type='trigger' AND name IN ({0}) ORDER BY name" -f $guardAll)
Assert-Gate ($gpost -eq ($GuardNamesAll -join "`n")) 'A9.5 twelve guard names exact' ($GuardNamesAll -join ' / ') ($gpost -replace "`r?`n",' / ')
$idxRows = Invoke-Read $Target ("SELECT name FROM sqlite_master WHERE type='index' AND name IN ({0}) ORDER BY name" -f (($IndexNamesAll | ForEach-Object { "'{0}'" -f $_ }) -join ','))
$idxSet = @($idxRows -split "`r?`n" | Where-Object { $_.Trim() -ne '' })
Assert-Gate (Set-Equal $idxSet $IndexNamesAll) 'A9.6 eight indexes present exact' ($IndexNamesAll -join ' / ') ($idxRows -replace "`r?`n",' / ')
Assert-Gate ((Invoke-Read $Target 'SELECT COUNT(*) FROM v2_live_activation_instrument') -eq '0') 'A9.7 activation table present, ZERO ROWS (field law)' '0' '(see above)'
Assert-Gate ((Invoke-Read $Target 'SELECT COUNT(*) FROM v2_live_kill_switch') -eq '0') 'A9.8 kill_switch table present, ZERO ROWS (field law)' '0' '(see above)'
Assert-Gate ((Invoke-Read $Target "SELECT COUNT(*) FROM sqlite_master WHERE type='table' AND name IN ('v2_live_exec_submission','v2_live_exec_fill_event','v2_live_exec_modify_event','v2_live_activation_instrument','v2_live_kill_switch')") -eq '5') 'A9.9 all five 12B/12C/12D tables present' '5' '(see above)'
Assert-Gate ((Invoke-Read $Target 'SELECT COUNT(*) FROM v2_live_exec_submission') -eq '0') 'A9.9b 12B submissions still 0' '0' '(see above)'
Assert-Gate ((Invoke-Read $Target 'SELECT COUNT(*) FROM v2_live_exec_fill_event') -eq '0') 'A9.9c 12B fill_events still 0' '0' '(see above)'
Assert-Gate ((Invoke-Read $Target 'SELECT COUNT(*) FROM v2_live_exec_modify_event') -eq '0') 'A9.9d 12C modify_events still 0' '0' '(see above)'
$permPost = Invoke-Read $Target ("SELECT role, permission, sal FROM v2_permission WHERE permission IN ({0}) ORDER BY permission" -f $permIn)
Assert-Gate ($permPost -eq $PermRowsExpect) 'A9.10 six 12D permission rows content-exact' $PermRowsExpect $permPost
$lxePost = Invoke-Read $Target "SELECT component, version, source_hash, evidence_ref FROM v2_computation_version WHERE component='live_exec_engine' ORDER BY version"
Assert-Gate ($lxePost -eq $LxeRowsPost) 'A9.11 compver rows ALL THREE stand, content-exact (DB == disk)' $LxeRowsPost $lxePost
$IntentCountPost = Invoke-Read $Target 'SELECT COUNT(*) FROM v2_live_exec_intent'
$IntentDigestsPost = Invoke-Read $Target 'SELECT digest FROM v2_live_exec_intent ORDER BY digest'
Assert-Gate ($IntentCountPost -eq $IntentCountPre) 'A9.12 12A intent ledger count unchanged' $IntentCountPre $IntentCountPost
Assert-Gate ($IntentDigestsPost -eq $IntentDigestsPre) 'A9.13 12A intent digests unchanged' $IntentDigestsPre $IntentDigestsPost
$lxe6Post = Invoke-Lxe $Backend $CodeLxe6
Assert-Gate ($lxe6Post -eq $Lxe6Expect) 'A9.14 disk 6-file lxe still b060f435...' $Lxe6Expect $lxe6Post
$lxe13Post = Invoke-Lxe $Backend $CodeLxe13
Assert-Gate ($lxe13Post -eq $Lxe13Expect) 'A9.15 disk 13-file lxe still d25c4857... (apply moves no source bytes)' $Lxe13Expect $lxe13Post
Write-Host 'A9.16 — the rendered CHECK names from the DB''s own DDL (E-0055-A10.3 record):'
Write-Host (Invoke-Read $Target "SELECT sql FROM sqlite_master WHERE type='table' AND name='v2_live_activation_instrument'")
Write-Host (Invoke-Read $Target "SELECT sql FROM sqlite_master WHERE type='table' AND name='v2_live_kill_switch'")

Write-Section 'A10. GUARD / CHECK REFUSALS (twelve; refused or rolled back; field law re-pinned after)'
$insAct = "INSERT INTO v2_live_activation_instrument (id, sole, version, template_hash, funded_posture_ref, step_up_ref, operator_ref, actor_id, data_class, mode, operator_id, created_at) VALUES ('__guardprobe_0056__', 'SOLE', 'lai-1.0.0', 'hh', 'gp', 'gp', 'gp', 'gp', 'live_marker', 'RESEARCH', 'itrga-gp', '2026-09-09 00:00:00')"
$gp = Invoke-GuardProbe $Target 'v2_live_activation_instrument' $insAct "UPDATE v2_live_activation_instrument SET template_hash='x' WHERE id='__guardprobe_0056__'"
Write-Host ($gp -join "`n")
Assert-Gate (($gp.Count -eq 2) -and ($gp[0] -eq $ActUpd) -and ($gp[1] -eq 'rolledback=1')) 'A10.1 activation UPDATE refusal exact + rolled back' $ActUpd ($gp -join ' / ')
$gp = Invoke-GuardProbe $Target 'v2_live_activation_instrument' $insAct "DELETE FROM v2_live_activation_instrument WHERE id='__guardprobe_0056__'"
Write-Host ($gp -join "`n")
Assert-Gate (($gp.Count -eq 2) -and ($gp[0] -eq $ActDel) -and ($gp[1] -eq 'rolledback=1')) 'A10.2 activation DELETE refusal exact + rolled back' $ActDel ($gp -join ' / ')
$insKs = "INSERT INTO v2_live_kill_switch (id, sole, status, step_up_ref, actor_id, data_class, mode, operator_id, created_at) VALUES ('__guardprobe_0056__', 'SOLE', 'armed', 'gp', 'gp', 'evidence', 'RESEARCH', 'itrga-gp', '2026-09-09 00:00:00')"
$gp = Invoke-GuardProbe $Target 'v2_live_kill_switch' $insKs "UPDATE v2_live_kill_switch SET status='cleared' WHERE id='__guardprobe_0056__'"
Write-Host ($gp -join "`n")
Assert-Gate (($gp.Count -eq 2) -and ($gp[0] -eq $KsUpd) -and ($gp[1] -eq 'rolledback=1')) 'A10.3 kill_switch UPDATE refusal exact + rolled back' $KsUpd ($gp -join ' / ')
$gp = Invoke-GuardProbe $Target 'v2_live_kill_switch' $insKs "DELETE FROM v2_live_kill_switch WHERE id='__guardprobe_0056__'"
Write-Host ($gp -join "`n")
Assert-Gate (($gp.Count -eq 2) -and ($gp[0] -eq $KsDel) -and ($gp[1] -eq 'rolledback=1')) 'A10.4 kill_switch DELETE refusal exact + rolled back' $KsDel ($gp -join ' / ')
$p = Invoke-Refuse $Target "INSERT INTO v2_live_activation_instrument (id, sole, version, template_hash, funded_posture_ref, step_up_ref, operator_ref, actor_id, data_class, mode, operator_id, created_at) VALUES ('__guardprobe_0056__', 'TWIN', 'lai-1.0.0', 'hh', 'gp', 'gp', 'gp', 'gp', 'live_marker', 'RESEARCH', 'itrga-gp', '2026-09-09 00:00:00')"
Assert-Gate ($p -eq $CkLaiSole) 'A10.5 activation sole CHECK refusal exact (rendered name)' $CkLaiSole $p
$p = Invoke-Refuse $Target "INSERT INTO v2_live_activation_instrument (id, sole, version, template_hash, funded_posture_ref, step_up_ref, operator_ref, actor_id, data_class, mode, operator_id, created_at) VALUES ('__guardprobe_0056__', 'SOLE', 'lai-0.0.0', 'hh', 'gp', 'gp', 'gp', 'gp', 'live_marker', 'RESEARCH', 'itrga-gp', '2026-09-09 00:00:00')"
Assert-Gate ($p -eq $CkLaiVersion) 'A10.6 activation version CHECK refusal exact (rendered name)' $CkLaiVersion $p
$p = Invoke-Refuse $Target "INSERT INTO v2_live_activation_instrument (id, sole, version, template_hash, funded_posture_ref, step_up_ref, operator_ref, actor_id, data_class, mode, operator_id, created_at) VALUES ('__guardprobe_0056__', 'SOLE', 'lai-1.0.0', 'hh', 'gp', 'gp', 'gp', 'gp', 'simulated', 'RESEARCH', 'itrga-gp', '2026-09-09 00:00:00')"
Assert-Gate ($p -eq $CkLaiClass) 'A10.7 force-simulation DIES at schema (rendered name)' $CkLaiClass $p
$p = Invoke-Refuse $Target "INSERT INTO v2_live_kill_switch (id, sole, status, step_up_ref, actor_id, data_class, mode, operator_id, created_at) VALUES ('__guardprobe_0056__', 'TWIN', 'armed', 'gp', 'gp', 'evidence', 'RESEARCH', 'itrga-gp', '2026-09-09 00:00:00')"
Assert-Gate ($p -eq $CkLksSole) 'A10.8 kill_switch sole CHECK refusal exact (rendered name)' $CkLksSole $p
$p = Invoke-Refuse $Target "INSERT INTO v2_live_kill_switch (id, sole, status, step_up_ref, actor_id, data_class, mode, operator_id, created_at) VALUES ('__guardprobe_0056__', 'SOLE', 'engaged', 'gp', 'gp', 'evidence', 'RESEARCH', 'itrga-gp', '2026-09-09 00:00:00')"
Assert-Gate ($p -eq $CkLksStatus) 'A10.9 kill_switch status CHECK refusal exact (engaged is not a state)' $CkLksStatus $p
$p = Invoke-Refuse $Target "INSERT INTO v2_live_kill_switch (id, sole, status, step_up_ref, actor_id, data_class, mode, operator_id, created_at) VALUES ('__guardprobe_0056__', 'SOLE', 'armed', 'gp', 'gp', 'simulated', 'RESEARCH', 'itrga-gp', '2026-09-09 00:00:00')"
Assert-Gate ($p -eq $CkLksClass) 'A10.10 kill_switch data_class CHECK refusal exact (evidence only)' $CkLksClass $p
$cvu = Invoke-Refuse $Target "UPDATE v2_computation_version SET version='probe' WHERE component='indicator_engine'"
Assert-Gate ($cvu -eq $CvuOld) 'A10.11 compver UPDATE refusal (ORIGINAL literal)' $CvuOld $cvu
$cvd = Invoke-Refuse $Target "DELETE FROM v2_computation_version WHERE component='indicator_engine'"
Assert-Gate ($cvd -eq $CvdOld) 'A10.12 compver DELETE refusal (ORIGINAL literal)' $CvdOld $cvd
Assert-Gate ((Invoke-Read $Target 'SELECT COUNT(*) FROM v2_live_activation_instrument') -eq '0') 'A10.13 activation ZERO ROWS after all probes (field law)' '0' '(see above)'
Assert-Gate ((Invoke-Read $Target 'SELECT COUNT(*) FROM v2_live_kill_switch') -eq '0') 'A10.14 kill_switch ZERO ROWS after all probes (field law)' '0' '(see above)'

Write-Section 'A11. HEALTH POST + DRIFT (ITEMIZED LAW) + ENVIRONMENT CLOSE'
Assert-Gate ((Invoke-Read $Target 'PRAGMA integrity_check') -eq 'ok') 'A11.1 integrity ok' 'ok' '(see above)'
Assert-Gate ((Invoke-Read $Target 'PRAGMA journal_mode') -eq 'delete') 'A11.2 journal delete' 'delete' '(see above)'
Assert-Gate ((-not (Test-Path ($Target + '-wal'))) -and (-not (Test-Path ($Target + '-shm')))) 'A11.3 no sidecars' 'absent' 'present'
Write-Host 'Drift law (ITEMIZED, E-0054-A11.4): exactly the 9 inherited V1 tokens; band tokens absent; silence is a pass-subset.'
$r = Invoke-Alembic $Target 'check'
foreach ($tok in $DriftForbidden) {
  Assert-Gate (-not ($r.Text -imatch [regex]::Escape($tok))) ("A11.4 drift: band token '{0}' absent" -f $tok) 'absent' 'present'
}
$opLines = @($r.Text -split "`r?`n" | Where-Object { $_ -imatch 'add_(table|index)|remove_index|removed (table|index)' })
$bad = @()
foreach ($ln in $opLines) {
  $hit = $false
  foreach ($w in $DriftWhitelist) { if ($ln -imatch [regex]::Escape($w)) { $hit = $true; break } }
  if (-not $hit) { $bad += $ln }
}
Assert-Gate ($bad.Count -eq 0) 'A11.5 drift: every detected operation names an inherited V1 token (9-item whitelist)' 'only the 9 inherited V1 tokens' ($bad -join ' / ')
Write-Host ("  drift operations witnessed (itemized): {0}" -f $opLines.Count)
$sweep = @(Get-ChildItem env: | Where-Object { $_.Name -match '^AXIOM_(TD|BROKER_PRACTICE)' })
Assert-Gate ($sweep.Count -eq 0) 'A11.6 environment close: still no TD/PRACTICE variables' 'absent' (($sweep | ForEach-Object { $_.Name }) -join ', ')

Write-Section 'A12. FINAL APPLY VERDICT'
$PostLen = (Get-Item $Target).Length
$PostSha = (Get-FileHash -Algorithm SHA256 $Target).Hash
$postFacts = @(
  ('RUN_TIMESTAMP     {0}' -f (Get-Date -Format 'yyyy-MM-dd HH:mm:ss zzz')),
  ('POST_REVISION     20260909_0056'),
  ('POST_TRIGGERS     90'),
  ('POST_PERMISSIONS  83'),
  ('POST_COMPVER      16'),
  ('POST_SIZE_BYTES   {0}' -f $PostLen),
  ('POST_SHA256       {0}' -f $PostSha),
  ('LXE_COMPVER_1_0_0 b060f435c7c339fbe5e23daf8231af04bf62cd8cc43ccd7d8a5f5067b78bb8c2'),
  ('LXE_COMPVER_1_1_0 d09306f1ab32f0dc6f26e5c7235b3e1f72c3175a1928d60673709c0b02a3809a'),
  ('LXE_COMPVER_1_2_0 d25c48579def993b63e6f84ca17e937c3e938f75b0ca1f78f8aea81b1e9c1705'),
  ('FIELD_LAW         activation 0 rows / kill_switch 0 rows (before and after every probe; no governor verb ever ran)'),
  ('ANCHOR_FILENAME   {0}' -f (Split-Path $Anchor -Leaf)),
  ('ANCHOR_SIZE_BYTES {0}' -f $AnchorLen),
  ('ANCHOR_SHA256     {0}' -f $AnchorSha),
  ('REHEARSAL_COPY    {0} (retain until ITRGA acknowledges the witness; then delete)' -f (Split-Path $Reh -Leaf)),
  'VERDICT           PASS'
)
$postFacts | Set-Content -Path $FinalStatePath -Encoding ascii
Write-Host ("post-apply size {0} sha256 {1}" -f $PostLen, $PostSha)
Write-Host ''
Write-Host "APPLY VERDICT: PASS - migration 20260909_0056_v2_be12d_activation_killswitch applied ONCE to '$Target'."
Write-Host 'Terminal state: revision 20260909_0056; tattoo 90/83/16; activation + kill_switch present with guard pairs and closed CHECKs, BOTH ZERO ROWS (before/after every probe); six 12D permission rows content-exact; compver ALL THREE rows standing (1.0.0/1.1.0 untouched; 1.2.0 == disk d25c4857...); twelve guard/CHECK refusals exact under RENDERED names; 12A ledger untouched; disk hashes 6/8/13-file re-proven; integrity ok; drift itemized; no TD/PRACTICE variable; no governor verb ran anywhere.'
Write-Host ("Transcript: {0}" -f $TranscriptPath)
Write-Host ("State record: {0}" -f $FinalStatePath)
Write-Host 'NEXT: restart the application when ready. Send transcript + state record to ITRGA. The FIELDED verdict and register line are issued on receipt.'

} finally {
  Remove-Item Env:AXIOM_DATABASE_URL -ErrorAction SilentlyContinue
  if ($script:TranscriptOn) { try { Stop-Transcript | Out-Null } catch { } }
}
