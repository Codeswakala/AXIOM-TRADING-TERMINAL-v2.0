<#
===============================================================================
ITRGA_V2_0055_APPLY_PACK_V1.ps1
===============================================================================
Pack:      ITRGA-V2-0055-APPLY-PACK-V1
Act:       0055 working-database application act (single sanctioned mutation)
Implements: ITRGA-V2-0055-FIELD-APPLY-CARD-20260909 (the card remains the
           governing text; this pack is the authorized equivalent runner).
Authority: BO-V2-BE12C-001 SS1.g  ·  ITRGA-REV-V2-BE12C-CR-001 (APPROVED;
           findings V2-BE12C-DEL-001 HIGH / V2-BE12C-DEL-002 MEDIUM CLOSED;
           LOW-1 re-homed CLOSED; LOW-2 register-logged for 12E; BE-12C
           ACCEPTED; suite floor 1,265)
Mutation:  EXACTLY ONE —  python -m alembic upgrade 20260909_0055
           against the fielded working database axiom_dev.db.
           Rehearsal runs on a byte-copy ONLY. All guard/CHECK probes are
           refused-write and always rolled back.
Method:    NO python FILES of any kind (no .py artifacts, not even helpers):
           all SQL executes through the repo venv python in-process (-c
           snippets only). NO git operations. NO credential prompt of any
           kind. NO practice vault provisioning: AXIOM_BROKER_PRACTICE_* and
           any AXIOM_TD_* asserted ABSENT at act start and act end.
Drift law: A11 implements the CORRECTED gate from birth (ERRATUM
           E-0054-A11.4 law): exactly the 9 inherited V1 tokens, ZERO
           12B/12C/v2/live_exec tokens. Never the absolute-silence pin.
Run:       Set-Location C:\Users\victo\.vscode\AXIOM\axiom
           powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\ITRGA_V2_0055_APPLY_PACK_V1.ps1
Output:    operator-evidence\BE-12C\0055-APPLY-RUN-V1-<timestamp>.txt  (transcript)
           operator-evidence\BE-12C\0055-APPLY-FINAL-STATE.txt         (state record)
On any gate failure: the pack HALTS at the failing gate, prints expected vs
actual, does NOT retry, does NOT re-run any mutation. Send the transcript to
ITRGA. Restoration is via the anchor copy only under ITRGA instruction.
Do NOT re-run this pack post-apply: it halts at A1.1 by design (idempotence).
===============================================================================
#>

$ErrorActionPreference = 'Stop'
Set-Location C:\Users\victo\.vscode\AXIOM\axiom

# ---------------------------------------------------------------- constants --
$RepoRoot      = 'C:\Users\victo\.vscode\AXIOM\axiom'
$Backend       = 'C:\Users\victo\.vscode\AXIOM\axiom\backend'
$Py            = 'C:\Users\victo\.vscode\AXIOM\axiom\.venv\Scripts\python.exe'
$Target        = 'C:\Users\victo\.vscode\AXIOM\axiom\backend\axiom_dev.db'
$EvDir         = 'C:\Users\victo\.vscode\AXIOM\axiom\operator-evidence\BE-12C'
$MigFile       = 'C:\Users\victo\.vscode\AXIOM\axiom\backend\alembic\versions\20260909_0055_v2_be12c_modify_events.py'

$MigSha        = '869014E31CF31E0E92DCC23CA3F6711D7922298A4C76185B259E728D2C49554A'
$MigLen        = 8839
$Lxe6Expect    = 'b060f435c7c339fbe5e23daf8231af04bf62cd8cc43ccd7d8a5f5067b78bb8c2'
$Lxe8Expect    = 'd09306f1ab32f0dc6f26e5c7235b3e1f72c3175a1928d60673709c0b02a3809a'
$LxeRowPre     = 'live_exec_engine|lxe-1.0.0|b060f435c7c339fbe5e23daf8231af04bf62cd8cc43ccd7d8a5f5067b78bb8c2|BO-V2-BE12B-001'
$LxeRowNew     = 'live_exec_engine|lxe-1.1.0|d09306f1ab32f0dc6f26e5c7235b3e1f72c3175a1928d60673709c0b02a3809a|BO-V2-BE12C-001'
$LxeRowsExpect = $LxeRowPre + "`n" + $LxeRowNew
$PermRowsExpect= @('admin|v2.live_exec.modifies.read|SAL-2','admin|v2.live_exec.modify.write|SAL-4') -join "`n"
$GuardNamesAll = @('v2_live_exec_fill_event_immutable_delete','v2_live_exec_fill_event_immutable_update','v2_live_exec_intent_immutable_delete','v2_live_exec_intent_immutable_update','v2_live_exec_modify_event_immutable_delete','v2_live_exec_modify_event_immutable_update','v2_live_exec_submission_immutable_delete','v2_live_exec_submission_immutable_update')
$GuardNamesPre = @('v2_live_exec_fill_event_immutable_delete','v2_live_exec_fill_event_immutable_update','v2_live_exec_intent_immutable_delete','v2_live_exec_intent_immutable_update','v2_live_exec_submission_immutable_delete','v2_live_exec_submission_immutable_update') -join "`n"
$IndexNamesAll = @('ix_v2_lxfill_created','ix_v2_lxmod_created','ix_v2_lxsub_created','uq_v2_lxfill_identity','uq_v2_lxmod_identity','uq_v2_lxsub_intent')
$CvuOld        = 'REFUSED:V2 computation version registry is immutable; UPDATE prohibited'
$CvdOld        = 'REFUSED:V2 computation version registry is immutable; DELETE prohibited'
$CvdNewLiteral = 'REFUSED:V2 computation versions are immutable; DELETE prohibited'
$ModUpd        = 'REFUSED:V2 live exec modify events are immutable; UPDATE prohibited'
$ModDel        = 'REFUSED:V2 live exec modify events are immutable; DELETE prohibited'
$CkElection    = 'REFUSED:CHECK constraint failed: ck_v2_lxmod_election'
$CkVerb        = 'REFUSED:CHECK constraint failed: ck_v2_lxmod_verb'
$DriftWhitelist= @(
  'audit_write_failure_records',
  'ix_audit_write_failures_category_action',
  'ix_audit_write_failures_created',
  'ix_advisory_signals_expires_at',
  'ix_advisory_signals_freshness_status',
  'ix_ingestion_runs_symbol_started',
  'ix_model_artifacts_advisory_status',
  'ix_model_artifacts_artifact_hash',
  'ix_model_artifacts_experiment_id'
)
$DriftForbidden= @('v2_','live_exec','lxmod','modify_event')

$ts             = Get-Date -Format yyyyMMddHHmmss
$TranscriptPath = Join-Path $EvDir ("0055-APPLY-RUN-V1-{0}.txt" -f $ts)
$FinalStatePath = Join-Path $EvDir '0055-APPLY-FINAL-STATE.txt'
$Anchor         = Join-Path $EvDir ("axiom_dev.db.pre-0055-{0}.bak" -f $ts)
$Reh            = Join-Path $EvDir ("axiom_dev.db.rehearsal-0055-{0}.db" -f $ts)

# ------------------------------------------------------- fileless SQL engine -
# All SQL runs through the repo venv python via -c snippets. No .py files.
# Snippet bodies deliberately contain NO double-quote characters (PS5.1 native
# argument quoting breaks on embedded double quotes) and SQL literals arrive
# via argv only (never built inside snippet code).
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
 left=c.execute('SELECT COUNT(*) FROM '+sys.argv[2]+' WHERE id='+chr(39)+'__guardprobe_0055__'+chr(39)).fetchone()[0]
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
Write-Host 'Pack: ITRGA-V2-0055-APPLY-PACK-V1'
Write-Host 'Act: 0055 working-database application act (single sanctioned mutation)'
Write-Host 'Implements: ITRGA-V2-0055-FIELD-APPLY-CARD-20260909 (governing text)'
Write-Host 'Authority: BO-V2-BE12C-001 SS1.g / ITRGA-REV-V2-BE12C-CR-001 (APPROVED)'
Write-Host ("Started: {0}" -f (Get-Date -Format 'yyyy-MM-dd HH:mm:ss zzz'))
Write-Host ("Repo root: {0}" -f $RepoRoot)
Write-Host ("Target file: {0}" -f $Target)
Write-Host 'Server credentials used: NONE (SQLite file; python in-process; no .py files)'
Write-Host 'Provider credentials used: NONE. This act prompts for NO credential of any kind.'
Write-Host ''
Write-Host 'STOP THE RUNNING APPLICATION BEFORE CONTINUING (it holds a live connection to the target database file).'
Write-Host 'Continuing in 5 seconds; press Ctrl+C now if the application is still running...'
Start-Sleep -Seconds 5

Write-Section 'A0b. AUTHORITY/PRACTICE ENVIRONMENT SWEEP (must print nothing)'
$sweep = @(Get-ChildItem env: | Where-Object { $_.Name -match '^AXIOM_(TD|BROKER_PRACTICE)' })
Assert-Gate ($sweep.Count -eq 0) 'A0b: no AXIOM_TD_* / AXIOM_BROKER_PRACTICE_* variables' 'absent' (($sweep | ForEach-Object { $_.Name }) -join ', ')

Write-Section 'A0c. FILE EXISTENCE'
Assert-Gate (Test-Path $Py)      'A0c.1 venv python present' $Py '(missing)'
Assert-Gate (Test-Path $Target)  'A0c.2 target db present'   $Target '(missing)'
Assert-Gate (Test-Path $MigFile) 'A0c.3 migration 0055 present' $MigFile '(missing)'

Write-Section 'A0d. 12C SOURCE-SET VISIBILITY (eight lxe files incl. the modify package)'
$lxeRel = @('app/v2/live_exec/intents.py','app/v2/live_exec/eligibility.py','app/v2/live_exec/risk.py','app/v2/live_exec/locks.py','app/v2/live_exec/submissions.py','app/v2/live_exec/ack_fills.py','app/v2/live_exec/modify/__init__.py','app/v2/live_exec/modify/engine.py')
$missing = @()
foreach ($rel in $lxeRel) {
  $p = Join-Path $Backend ($rel -replace '/','\')
  if (Test-Path $p) { Write-Host ("  present  {0}" -f $rel) } else { Write-Host ("  MISSING  {0}" -f $rel); $missing += $rel }
}
Assert-Gate ($missing.Count -eq 0) 'A0d: all eight lxe source files present (12C landed)' '8/8 present' (($missing.Count.ToString() + ' missing: ') + ($missing -join ', '))

# ------------------------------------------------------------------ A1 BASE.
Write-Section 'A1. BASELINE REVISION STATE'
$r = Invoke-Alembic $Target 'current'
Assert-Gate ($r.Code -eq 0) 'A1.0 alembic current exit 0' '0' ([string]$r.Code)
$cur = Get-AlembicCurrent $r.Text
Assert-Gate ($cur -eq '20260909_0054') 'A1.1 current is exactly 20260909_0054 (no (head) suffix)' '20260909_0054' $cur
$r = Invoke-Alembic $Target 'heads'
$headsLines = @($r.Text -split "`r?`n" | Where-Object { $_.Contains('(head)') })
Assert-Gate (($headsLines.Count -ge 1) -and $headsLines[0].Trim().StartsWith('20260909_0055')) 'A1.2 repo head is 20260909_0055 (head)' '20260909_0055 (head)' ($headsLines -join ' / ')
& $Py -m alembic --version 2>&1 | ForEach-Object { Write-Host ("Alembic version: {0}" -f (ConvertTo-Text @($_))) }

Write-Section 'A2. THE 0055 FILE PIN (byte-still recital)'
$migLenActual = (Get-Item $MigFile).Length
$migShaActual = (Get-FileHash -Algorithm SHA256 $MigFile).Hash
Write-Host ("  length  {0} (pinned {1})" -f $migLenActual, $MigLen)
Write-Host ("  sha256  {0}" -f $migShaActual)
Assert-Gate ($migLenActual -eq $MigLen) 'A2.1 migration length' $MigLen ([string]$migLenActual)
Assert-Gate ($migShaActual -ieq $MigSha) 'A2.2 migration sha256' $MigSha $migShaActual

Write-Section 'A3. TATTOO PRE + NAMED-OBJECT PRE-LISTS'
$tpre = Invoke-Read $Target "SELECT COUNT(*) FROM sqlite_master WHERE type='trigger'"
Assert-Gate ($tpre -eq '84') 'A3.1 triggers total == 84' '84' $tpre
$ppre = Invoke-Read $Target 'SELECT COUNT(*) FROM v2_permission'
Assert-Gate ($ppre -eq '75') 'A3.2 v2_permission == 75' '75' $ppre
$cpre = Invoke-Read $Target 'SELECT COUNT(*) FROM v2_computation_version'
Assert-Gate ($cpre -eq '14') 'A3.3 v2_computation_version == 14' '14' $cpre
$guardAll = ($GuardNamesAll | ForEach-Object { "'{0}'" -f $_ }) -join ','
$gpre = Invoke-Read $Target ("SELECT name FROM sqlite_master WHERE type='trigger' AND name IN ({0}) ORDER BY name" -f $guardAll)
Assert-Gate ($gpre -eq $GuardNamesPre) 'A3.4 live_exec guard set pre == the six 12A/12B names' $GuardNamesPre $gpre
$lxePre = Invoke-Read $Target "SELECT component, version, source_hash, evidence_ref FROM v2_computation_version WHERE component='live_exec_engine' ORDER BY version"
Assert-Gate ($lxePre -eq $LxeRowPre) 'A3.5 live_exec_engine compver pre == ONLY the lxe-1.0.0 row (content-exact)' $LxeRowPre $lxePre
$newPermsAbsent = Invoke-Read $Target "SELECT COUNT(*) FROM v2_permission WHERE permission IN ('v2.live_exec.modify.write','v2.live_exec.modifies.read')"
Assert-Gate ($newPermsAbsent -eq '0') 'A3.6 the two 12C permission rows ABSENT pre-apply' '0' $newPermsAbsent
$modTableAbsent = Invoke-Read $Target "SELECT COUNT(*) FROM sqlite_master WHERE type='table' AND name='v2_live_exec_modify_event'"
Assert-Gate ($modTableAbsent -eq '0') 'A3.7 v2_live_exec_modify_event ABSENT pre-apply' '0' $modTableAbsent
$IntentCountPre = Invoke-Read $Target 'SELECT COUNT(*) FROM v2_live_exec_intent'
$IntentDigestsPre = Invoke-Read $Target 'SELECT digest FROM v2_live_exec_intent ORDER BY digest'
Write-Host ("  12A intent ledger rows (recorded): {0}" -f $IntentCountPre)
Write-Host ("  12A intent digests (recorded): {0}" -f ($IntentDigestsPre -replace "`r?`n",'; '))

Write-Section 'A4. HEALTH PRE + ANCHOR (proven rollback anchor before any mutation)'
Assert-Gate ((Invoke-Read $Target 'PRAGMA integrity_check') -eq 'ok') 'A4.1 integrity_check ok' 'ok' '(see above)'
Assert-Gate ((Invoke-Read $Target 'PRAGMA journal_mode') -eq 'delete') 'A4.2 journal delete' 'delete' '(see above)'
Assert-Gate ((-not (Test-Path ($Target + '-wal'))) -and (-not (Test-Path ($Target + '-shm')))) 'A4.3 no sidecars' 'absent' 'present'
Copy-Item $Target $Anchor
$script:AnchorCreated = $true
Assert-Gate ((Invoke-Read $Anchor 'PRAGMA integrity_check') -eq 'ok') 'A4.4 anchor integrity ok' 'ok' '(see above)'
$anchorRev = Invoke-Read $Anchor 'SELECT version_num FROM alembic_version'
Assert-Gate ($anchorRev -eq '20260909_0054') 'A4.5 anchor revision 20260909_0054' '20260909_0054' $anchorRev
$AnchorLen = (Get-Item $Anchor).Length
$AnchorSha = (Get-FileHash -Algorithm SHA256 $Anchor).Hash
Write-Host ("  anchor: {0}" -f $Anchor)
Write-Host ("  anchor size {0} sha256 {1}" -f $AnchorLen, $AnchorSha)

Write-Section 'A5. DUAL LXE PRE-COMPUTE GATES (halts precede any mutation)'
$lxe6Actual = Invoke-Lxe $Backend $CodeLxe6
Write-Host ("  6-file computed: {0}" -f $lxe6Actual)
Write-Host ("  6-file expected: {0}" -f $Lxe6Expect)
Assert-Gate ($lxe6Actual -eq $Lxe6Expect) 'A5a 12A/12B six-file lxe hash unmoved (b060f435...)' $Lxe6Expect $lxe6Actual
$lxe8Actual = Invoke-Lxe $Backend $CodeLxe8
Write-Host ("  8-file computed: {0}" -f $lxe8Actual)
Write-Host ("  8-file expected: {0}" -f $Lxe8Expect)
Assert-Gate ($lxe8Actual -eq $Lxe8Expect) 'A5b CR-1 eight-file lxe hash landed EXACTLY (d09306f1...; prior 776417fb... VOID)' $Lxe8Expect $lxe8Actual

# --------------------------------------------------------------- A6 REHEARSAL
Write-Section 'A6. REHEARSAL UPGRADE (byte-copy only)'
Copy-Item $Target $Reh
$r = Invoke-Alembic $Reh 'upgrade 20260909_0055'
Assert-Gate ($r.Code -eq 0) 'A6.0 rehearsal upgrade exit 0' '0' ([string]$r.Code)
Assert-Gate ((Count-Hits $r.Text 'Running upgrade 20260909_0054 -> 20260909_0055') -eq 1) 'A6.1 exactly one Running upgrade line' '1' ([string](Count-Hits $r.Text 'Running upgrade 20260909_0054 -> 20260909_0055'))
Assert-NoBadTokens $r.Text 'A6.2 rehearsal console'
Assert-Gate ((Invoke-Read $Reh "SELECT COUNT(*) FROM sqlite_master WHERE type='trigger'") -eq '86') 'A6.3 rehearsal triggers 86' '86' '(see above)'
Assert-Gate ((Invoke-Read $Reh 'SELECT COUNT(*) FROM v2_permission') -eq '77') 'A6.4 rehearsal perms 77' '77' '(see above)'
Assert-Gate ((Invoke-Read $Reh 'SELECT COUNT(*) FROM v2_computation_version') -eq '15') 'A6.5 rehearsal compver 15' '15' '(see above)'
$lxeReh = Invoke-Read $Reh "SELECT component, version, source_hash, evidence_ref FROM v2_computation_version WHERE component='live_exec_engine' ORDER BY version"
Assert-Gate ($lxeReh -eq $LxeRowsExpect) 'A6.6 rehearsal compver rows BOTH stand, content-exact (1.0.0 then 1.1.0)' $LxeRowsExpect $lxeReh

Write-Section 'A7. REHEARSAL DOWNGRADE PROOF (full reversibility, on the copy)'
$r = Invoke-Alembic $Reh 'downgrade 20260909_0054'
Assert-Gate ($r.Code -eq 0) 'A7.0 rehearsal downgrade exit 0' '0' ([string]$r.Code)
Assert-Gate ((Count-Hits $r.Text 'Running downgrade 20260909_0055 -> 20260909_0054') -eq 1) 'A7.1 exactly one Running downgrade line' '1' ([string](Count-Hits $r.Text 'Running downgrade 20260909_0055 -> 20260909_0054'))
Assert-NoBadTokens $r.Text 'A7.2 rehearsal console (incl. compver delete-guard dance silent)'
Assert-Gate ((Invoke-Read $Reh 'SELECT version_num FROM alembic_version') -eq '20260909_0054') 'A7.3 rehearsal revision restored 20260909_0054' '20260909_0054' '(see above)'
Assert-Gate ((Invoke-Read $Reh "SELECT COUNT(*) FROM sqlite_master WHERE type='trigger'") -eq '84') 'A7.4 rehearsal triggers restored 84' '84' '(see above)'
Assert-Gate ((Invoke-Read $Reh 'SELECT COUNT(*) FROM v2_permission') -eq '75') 'A7.5 rehearsal perms restored 75' '75' '(see above)'
Assert-Gate ((Invoke-Read $Reh 'SELECT COUNT(*) FROM v2_computation_version') -eq '14') 'A7.6 rehearsal compver restored 14' '14' '(see above)'
Assert-Gate ((Invoke-Read $Reh "SELECT COUNT(*) FROM sqlite_master WHERE type='table' AND name='v2_live_exec_modify_event'") -eq '0') 'A7.7 rehearsal modify table removed' '0' '(see above)'
$lxeDown = Invoke-Read $Reh "SELECT component, version, source_hash, evidence_ref FROM v2_computation_version WHERE component='live_exec_engine' ORDER BY version"
Assert-Gate ($lxeDown -eq $LxeRowPre) 'A7.8 rehearsal compver == ONLY the lxe-1.0.0 row (1.1.0 removed)' $LxeRowPre $lxeDown
Write-Host 'NOTE (register-logged advisory, not a finding): the recreated compver DELETE guard carries the migration-literal message ''V2 computation versions are immutable; DELETE prohibited'' (vs the inherited ''registry'' wording); invariant identical; visible only on a downgraded chain.'
$cvdReh = Invoke-Refuse $Reh "DELETE FROM v2_computation_version WHERE component='indicator_engine'"
Assert-Gate ($cvdReh -eq $CvdNewLiteral) 'A7.9 rehearsal recreated-guard refusal (documented literal)' $CvdNewLiteral $cvdReh

# ----------------------------------------------------------------- A8 APPLY
Write-Section 'A8. THE APPLY (single sanctioned mutation, fielded file)'
Write-Host ("Target: {0}" -f $Target)
$r = Invoke-Alembic $Target 'upgrade 20260909_0055'
Assert-Gate ($r.Code -eq 0) 'A8.0 apply exit 0' '0' ([string]$r.Code)
Assert-Gate ((Count-Hits $r.Text 'Running upgrade 20260909_0054 -> 20260909_0055') -eq 1) 'A8.1 exactly one Running upgrade line' '1' ([string](Count-Hits $r.Text 'Running upgrade 20260909_0054 -> 20260909_0055'))
Assert-NoBadTokens $r.Text 'A8.2 apply console'

# -------------------------------------------------------------- A9 TERMINAL
Write-Section 'A9. FIELDED TERMINAL STATE'
$r = Invoke-Alembic $Target 'current'
$cur = Get-AlembicCurrent $r.Text
Assert-Gate ($cur -eq '20260909_0055 (head)') 'A9.1 stamped 20260909_0055 (head)' '20260909_0055 (head)' $cur
Assert-Gate ((Invoke-Read $Target "SELECT COUNT(*) FROM sqlite_master WHERE type='trigger'") -eq '86') 'A9.2 triggers 86' '86' '(see above)'
Assert-Gate ((Invoke-Read $Target 'SELECT COUNT(*) FROM v2_permission') -eq '77') 'A9.3 perms 77' '77' '(see above)'
Assert-Gate ((Invoke-Read $Target 'SELECT COUNT(*) FROM v2_computation_version') -eq '15') 'A9.4 compver 15' '15' '(see above)'
$gpost = Invoke-Read $Target ("SELECT name FROM sqlite_master WHERE type='trigger' AND name IN ({0}) ORDER BY name" -f $guardAll)
Assert-Gate ($gpost -eq ($GuardNamesAll -join "`n")) 'A9.5 eight live_exec guard names exact' ($GuardNamesAll -join ' / ') ($gpost -replace "`r?`n",' / ')
$idxRows = Invoke-Read $Target ("SELECT name FROM sqlite_master WHERE type='index' AND name IN ({0}) ORDER BY name" -f (($IndexNamesAll | ForEach-Object { "'{0}'" -f $_ }) -join ','))
$idxSet = @($idxRows -split "`r?`n" | Where-Object { $_.Trim() -ne '' })
Assert-Gate (Set-Equal $idxSet $IndexNamesAll) 'A9.6 six 12B+12C indexes present exact' ($IndexNamesAll -join ' / ') ($idxRows -replace "`r?`n",' / ')
Assert-Gate ((Invoke-Read $Target 'SELECT COUNT(*) FROM v2_live_exec_modify_event') -eq '0') 'A9.7 modify_event table present and empty' '0' '(see above)'
Assert-Gate ((Invoke-Read $Target "SELECT COUNT(*) FROM sqlite_master WHERE type='table' AND name IN ('v2_live_exec_submission','v2_live_exec_fill_event','v2_live_exec_modify_event')") -eq '3') 'A9.8 all three live_exec 12B/12C tables present' '3' '(see above)'
Assert-Gate ((Invoke-Read $Target 'SELECT COUNT(*) FROM v2_live_exec_submission') -eq '0') 'A9.8b 12B submissions still empty' '0' '(see above)'
Assert-Gate ((Invoke-Read $Target 'SELECT COUNT(*) FROM v2_live_exec_fill_event') -eq '0') 'A9.8c 12B fill_events still empty' '0' '(see above)'
$permPost = Invoke-Read $Target "SELECT role, permission, sal FROM v2_permission WHERE permission IN ('v2.live_exec.modify.write','v2.live_exec.modifies.read') ORDER BY permission"
Assert-Gate ($permPost -eq $PermRowsExpect) 'A9.9 two 12C permission rows content-exact' $PermRowsExpect $permPost
$lxePost = Invoke-Read $Target "SELECT component, version, source_hash, evidence_ref FROM v2_computation_version WHERE component='live_exec_engine' ORDER BY version"
Assert-Gate ($lxePost -eq $LxeRowsExpect) 'A9.10 fielded compver rows BOTH stand, content-exact (1.0.0 then 1.1.0; DB == disk)' $LxeRowsExpect $lxePost
$IntentCountPost = Invoke-Read $Target 'SELECT COUNT(*) FROM v2_live_exec_intent'
$IntentDigestsPost = Invoke-Read $Target 'SELECT digest FROM v2_live_exec_intent ORDER BY digest'
Assert-Gate ($IntentCountPost -eq $IntentCountPre) 'A9.11 12A intent ledger count unchanged' $IntentCountPre $IntentCountPost
Assert-Gate ($IntentDigestsPost -eq $IntentDigestsPre) 'A9.12 12A intent digests unchanged' $IntentDigestsPre $IntentDigestsPost
$lxe6Post = Invoke-Lxe $Backend $CodeLxe6
Assert-Gate ($lxe6Post -eq $Lxe6Expect) 'A9.13 disk 6-file lxe still b060f435... (apply moves no source bytes)' $Lxe6Expect $lxe6Post
$lxe8Post = Invoke-Lxe $Backend $CodeLxe8
Assert-Gate ($lxe8Post -eq $Lxe8Expect) 'A9.14 disk 8-file lxe still d09306f1... (apply moves no source bytes)' $Lxe8Expect $lxe8Post

Write-Section 'A10. GUARD / CHECK REFUSALS (six; always rolled back)'
$insMod = "INSERT INTO v2_live_exec_modify_event (id, submission_id, intent_id, verb, act_identity, request_payload, outcome, operator_election, actor_id, data_class, mode, operator_id, created_at) VALUES ('__guardprobe_0055__', 'gp', 'gp', 'cancel', 'gp-0055', '{}', 'applied', 'standard', 'gp', 'simulated', 'PAPER', 'itrga-gp', '2026-09-09 00:00:00')"
$gp = Invoke-GuardProbe $Target 'v2_live_exec_modify_event' $insMod "UPDATE v2_live_exec_modify_event SET raw_note='x' WHERE id='__guardprobe_0055__'"
Write-Host ($gp -join "`n")
Assert-Gate (($gp.Count -eq 2) -and ($gp[0] -eq $ModUpd) -and ($gp[1] -eq 'rolledback=1')) 'A10.1 modify_event UPDATE refusal exact + rolled back' $ModUpd ($gp -join ' / ')
$gp = Invoke-GuardProbe $Target 'v2_live_exec_modify_event' $insMod "DELETE FROM v2_live_exec_modify_event WHERE id='__guardprobe_0055__'"
Write-Host ($gp -join "`n")
Assert-Gate (($gp.Count -eq 2) -and ($gp[0] -eq $ModDel) -and ($gp[1] -eq 'rolledback=1')) 'A10.2 modify_event DELETE refusal exact + rolled back' $ModDel ($gp -join ' / ')
$ckel = Invoke-Refuse $Target "INSERT INTO v2_live_exec_modify_event (id, submission_id, intent_id, verb, act_identity, request_payload, outcome, operator_election, actor_id, data_class, mode, operator_id, created_at) VALUES ('__guardprobe_0055__', 'gp', 'gp', 'cancel', 'gp-0055-cke', '{}', 'applied', 'auto_recovery', 'gp', 'simulated', 'PAPER', 'itrga-gp', '2026-09-09 00:00:00')"
Assert-Gate ($ckel -eq $CkElection) 'A10.3 election CHECK refusal exact (auto_recovery not in closed vocabulary)' $CkElection $ckel
$ckvb = Invoke-Refuse $Target "INSERT INTO v2_live_exec_modify_event (id, submission_id, intent_id, verb, act_identity, request_payload, outcome, operator_election, actor_id, data_class, mode, operator_id, created_at) VALUES ('__guardprobe_0055__', 'gp', 'gp', 'close', 'gp-0055-ckv', '{}', 'applied', 'standard', 'gp', 'simulated', 'PAPER', 'itrga-gp', '2026-09-09 00:00:00')"
Assert-Gate ($ckvb -eq $CkVerb) 'A10.4 verb CHECK refusal exact (position verbs do not exist)' $CkVerb $ckvb
$cvu = Invoke-Refuse $Target "UPDATE v2_computation_version SET version='probe' WHERE component='indicator_engine'"
Assert-Gate ($cvu -eq $CvuOld) 'A10.5 compver UPDATE refusal (ORIGINAL literal; guard untouched by upgrade)' $CvuOld $cvu
$cvd = Invoke-Refuse $Target "DELETE FROM v2_computation_version WHERE component='indicator_engine'"
Assert-Gate ($cvd -eq $CvdOld) 'A10.6 compver DELETE refusal (ORIGINAL literal)' $CvdOld $cvd
Assert-Gate ((Invoke-Read $Target 'SELECT COUNT(*) FROM v2_live_exec_modify_event') -eq '0') 'A10.7 modify_event still 0 after probes' '0' '(see above)'
Assert-Gate ((Invoke-Read $Target 'SELECT COUNT(*) FROM v2_live_exec_submission') -eq '0') 'A10.8 submissions still 0 after probes' '0' '(see above)'

Write-Section 'A11. HEALTH POST + DRIFT (ITEMIZED LAW) + ENVIRONMENT CLOSE'
Assert-Gate ((Invoke-Read $Target 'PRAGMA integrity_check') -eq 'ok') 'A11.1 integrity ok' 'ok' '(see above)'
Assert-Gate ((Invoke-Read $Target 'PRAGMA journal_mode') -eq 'delete') 'A11.2 journal delete' 'delete' '(see above)'
Assert-Gate ((-not (Test-Path ($Target + '-wal'))) -and (-not (Test-Path ($Target + '-shm')))) 'A11.3 no sidecars' 'absent' 'present'
Write-Host 'Drift law (ERRATUM E-0054-A11.4, carried as standing law): exactly the 9 inherited V1 tokens; ZERO 12B/12C/v2/live_exec tokens; silence is a pass-subset; never the absolute-silence pin.'
$r = Invoke-Alembic $Target 'check'
foreach ($tok in $DriftForbidden) {
  Assert-Gate (-not ($r.Text -imatch [regex]::Escape($tok))) ("A11.4 drift: band token '{0}' absent" -f $tok) 'absent' 'present'
}
$opLines = @($r.Text -split "`r?`n" | Where-Object { $_ -imatch 'add_(table|index)|remove_index' })
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

# ------------------------------------------------------------------ A12 VERDICT
Write-Section 'A12. FINAL APPLY VERDICT'
$PostLen = (Get-Item $Target).Length
$PostSha = (Get-FileHash -Algorithm SHA256 $Target).Hash
$postFacts = @(
  ('RUN_TIMESTAMP     {0}' -f (Get-Date -Format 'yyyy-MM-dd HH:mm:ss zzz')),
  ('POST_REVISION     20260909_0055'),
  ('POST_TRIGGERS     86'),
  ('POST_PERMISSIONS  77'),
  ('POST_COMPVER      15'),
  ('POST_SIZE_BYTES   {0}' -f $PostLen),
  ('POST_SHA256       {0}' -f $PostSha),
  ('LXE_COMPVER_1_0_0 b060f435c7c339fbe5e23daf8231af04bf62cd8cc43ccd7d8a5f5067b78bb8c2'),
  ('LXE_COMPVER_1_1_0 d09306f1ab32f0dc6f26e5c7235b3e1f72c3175a1928d60673709c0b02a3809a'),
  ('ANCHOR_FILENAME   {0}' -f (Split-Path $Anchor -Leaf)),
  ('ANCHOR_SIZE_BYTES {0}' -f $AnchorLen),
  ('ANCHOR_SHA256     {0}' -f $AnchorSha),
  ('REHEARSAL_COPY    {0} (retain until ITRGA acknowledges the witness; then delete)' -f (Split-Path $Reh -Leaf)),
  'VERDICT           PASS'
)
$postFacts | Set-Content -Path $FinalStatePath -Encoding ascii
Write-Host ("post-apply size {0} sha256 {1}" -f $PostLen, $PostSha)
Write-Host ''
Write-Host "APPLY VERDICT: PASS - migration 20260909_0055_v2_be12c_modify_events applied ONCE to '$Target'."
Write-Host 'Terminal state: revision 20260909_0055; tattoo 86/77/15; v2_live_exec_modify_event present-and-empty with its immutable guard pair + closed CHECKs (four 12C refusals exact incl. both compver ORIGINAL literals); two 12C permission rows content-exact; compver BOTH rows standing (lxe-1.0.0 untouched; lxe-1.1.0 == disk d09306f1...); 12A intent ledger untouched (count + digests proven); 6-file and 8-file disk hashes re-proven; integrity ok; drift gate ITEMIZED per the E-0054-A11.4 law; anchor + rehearsal copy in operator-evidence\BE-12C; no TD/PRACTICE variable at start or end.'
Write-Host ("Transcript: {0}" -f $TranscriptPath)
Write-Host ("State record: {0}" -f $FinalStatePath)
Write-Host 'NEXT: restart the application when ready. Send the transcript + state record to ITRGA. The fielding verdict (FIELDED) and the register line are issued on receipt.'

} finally {
  Remove-Item Env:AXIOM_DATABASE_URL -ErrorAction SilentlyContinue
  if ($script:TranscriptOn) { try { Stop-Transcript | Out-Null } catch { } }
}
