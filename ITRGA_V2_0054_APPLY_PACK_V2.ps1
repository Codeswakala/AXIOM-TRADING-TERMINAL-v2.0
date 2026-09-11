<#
===============================================================================
ITRGA_V2_0054_APPLY_PACK_V2.ps1
===============================================================================
Pack:      ITRGA-V2-0054-APPLY-PACK-V2
Act:       0054 working-database application act (single sanctioned mutation)
Supersedes: V1 runner (functional gates identical). V1 erratum, cosmetic only:
           (i) on the HALT path Stop-Transcript ran twice, printing a benign
           "host is not currently transcribing" error; (ii) the HALT message
           printed the anchor path even when the halt occurred BEFORE the
           anchor existed, wrongly implying a restore was needed. No gate
           semantics changed; V1's halt itself was correct and mutation-free.
           New in V2: A0d pre-flight prints the full present/missing list of
           the six lxe source files in one pass (hash gate A5 still governs).
Implements: ITRGA-V2-0054-FIELD-APPLY-CARD-20260908 (the card remains the
           governing text; this pack is the authorized equivalent runner).
Authority: BO-V2-BE12B-001 §1.g  ·  ITRGA-REV-V2-BE12B-CR-001 (APPROVED;
           finding V2-BE12B-DEL-001 CLOSED; BE-12B ACCEPTED; suite floor 1,240)
Mutation:  EXACTLY ONE —  python -m alembic upgrade 20260909_0054
           against the fielded working database axiom_dev.db.
           Rehearsal runs on byte-copies ONLY. All guard probes are
           refused-write and always rolled back.
Scope:     NO git operations. NO credential prompt of any kind. NO python
           FILES: all SQL executes through the repo venv python in-process
           (-c snippets; no .py artifacts). NO practice vault provisioning:
           AXIOM_BROKER_PRACTICE_* and any AXIOM_TD_* must be absent at act
           start and are asserted absent at act end.
Run:       Set-Location C:\Users\victo\.vscode\AXIOM\axiom
           powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\ITRGA_V2_0054_APPLY_PACK_V1.ps1
Output:    operator-evidence\BE-12B\0054-APPLY-RUN-V1-<timestamp>.txt  (transcript)
           operator-evidence\BE-12B\0054-APPLY-FINAL-STATE.txt         (state record)
On any gate failure: the pack HALTS at the failing gate, prints expected vs
actual, does NOT retry, does NOT re-run any mutation. Send the transcript to
ITRGA. Restoration is via the anchor copy only under ITRGA instruction.
===============================================================================
#>

$ErrorActionPreference = 'Stop'
Set-Location C:\Users\victo\.vscode\AXIOM\axiom

# ---------------------------------------------------------------- constants --
$RepoRoot      = 'C:\Users\victo\.vscode\AXIOM\axiom'
$Backend       = 'C:\Users\victo\.vscode\AXIOM\axiom\backend'
$Py            = 'C:\Users\victo\.vscode\AXIOM\axiom\.venv\Scripts\python.exe'
$Target        = 'C:\Users\victo\.vscode\AXIOM\axiom\backend\axiom_dev.db'
$EvDir         = 'C:\Users\victo\.vscode\AXIOM\axiom\operator-evidence\BE-12B'
$MigFile       = 'C:\Users\victo\.vscode\AXIOM\axiom\backend\alembic\versions\20260909_0054_v2_be12b_submission_fills.py'

$MigSha        = 'F22A39669FA4695F4B5E2543DE41D4493BD54826A93949D862C94DFD9B4FA386'
$MigLen        = 10086
$LxeExpect     = 'b060f435c7c339fbe5e23daf8231af04bf62cd8cc43ccd7d8a5f5067b78bb8c2'
$LxeRowExpect  = 'live_exec_engine|lxe-1.0.0|b060f435c7c339fbe5e23daf8231af04bf62cd8cc43ccd7d8a5f5067b78bb8c2|BO-V2-BE12B-001'
$PermRowsExpect= @('admin|v2.live_exec.fills.read|SAL-2','admin|v2.live_exec.submissions.read|SAL-2','admin|v2.live_exec.submit.write|SAL-4') -join "`n"
$GuardNamesAll = @('v2_live_exec_fill_event_immutable_delete','v2_live_exec_fill_event_immutable_update','v2_live_exec_intent_immutable_delete','v2_live_exec_intent_immutable_update','v2_live_exec_submission_immutable_delete','v2_live_exec_submission_immutable_update')
$GuardNamesPre = @('v2_live_exec_intent_immutable_delete','v2_live_exec_intent_immutable_update') -join "`n"
$NewIndexes    = @('ix_v2_lxfill_created','ix_v2_lxsub_created','uq_v2_lxfill_identity','uq_v2_lxsub_intent')
$CvuOld        = 'REFUSED:V2 computation version registry is immutable; UPDATE prohibited'
$CvdOld        = 'REFUSED:V2 computation version registry is immutable; DELETE prohibited'
$CvdNewLiteral = 'REFUSED:V2 computation versions are immutable; DELETE prohibited'
$SubUpd        = 'REFUSED:V2 live exec submissions are immutable; UPDATE prohibited'
$SubDel        = 'REFUSED:V2 live exec submissions are immutable; DELETE prohibited'
$FilUpd        = 'REFUSED:V2 live exec fill events are immutable; UPDATE prohibited'
$FilDel        = 'REFUSED:V2 live exec fill events are immutable; DELETE prohibited'

$ts             = Get-Date -Format yyyyMMddHHmmss
$TranscriptPath = Join-Path $EvDir ("0054-APPLY-RUN-V2-{0}.txt" -f $ts)
$FinalStatePath = Join-Path $EvDir '0054-APPLY-FINAL-STATE.txt'
$Anchor         = Join-Path $EvDir ("axiom_dev.db.pre-0054-{0}.bak" -f $ts)
$Reh            = Join-Path $EvDir ("axiom_dev.db.rehearsal-0054-{0}.db" -f $ts)

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
 left=c.execute('SELECT COUNT(*) FROM '+sys.argv[2]+' WHERE id='+chr(39)+'__guardprobe_0054__'+chr(39)).fetchone()[0]
 print('rolledback=%d'%(1 if left==0 else 0))
finally:
 c.close()
'@

$CodeLxe = @'
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

function Invoke-Lxe { param([string]$BackendDir)
  $raw = & $Py -c $CodeLxe $BackendDir 2>&1
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
Write-Host 'Pack: ITRGA-V2-0054-APPLY-PACK-V2'
Write-Host 'Act: 0054 working-database application act (single sanctioned mutation)'
Write-Host 'Implements: ITRGA-V2-0054-FIELD-APPLY-CARD-20260908 (governing text)'
Write-Host 'Authority: BO-V2-BE12B-001 SS1.g / ITRGA-REV-V2-BE12B-CR-001 (APPROVED)'
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
Assert-Gate (Test-Path $MigFile) 'A0c.3 migration 0054 present' $MigFile '(missing)'

Write-Section 'A0d. 12B SOURCE-SET VISIBILITY (six lxe files; full list before the hash gate)'
$lxeRel = @('app/v2/live_exec/intents.py','app/v2/live_exec/eligibility.py','app/v2/live_exec/risk.py','app/v2/live_exec/locks.py','app/v2/live_exec/submissions.py','app/v2/live_exec/ack_fills.py')
$missing = @()
foreach ($rel in $lxeRel) {
  $p = Join-Path $Backend ($rel -replace '/','\')
  if (Test-Path $p) { Write-Host ("  present  {0}" -f $rel) } else { Write-Host ("  MISSING  {0}" -f $rel); $missing += $rel }
}
Assert-Gate ($missing.Count -eq 0) 'A0d: all six lxe source files present (12B landed)' '6/6 present' (($missing.Count.ToString() + ' missing: ') + ($missing -join ', '))

# ------------------------------------------------------------------ A1 BASE.
Write-Section 'A1. BASELINE REVISION STATE'
$r = Invoke-Alembic $Target 'current'
Assert-Gate ($r.Code -eq 0) 'A1.0 alembic current exit 0' '0' ([string]$r.Code)
$cur = Get-AlembicCurrent $r.Text
Assert-Gate ($cur -eq '20260909_0053') 'A1.1 current is exactly 20260909_0053 (no (head) suffix)' '20260909_0053' $cur
$r = Invoke-Alembic $Target 'heads'
$headsLines = @($r.Text -split "`r?`n" | Where-Object { $_.Contains('(head)') })
Assert-Gate (($headsLines.Count -ge 1) -and $headsLines[0].Trim().StartsWith('20260909_0054')) 'A1.2 repo head is 20260909_0054 (head)' '20260909_0054 (head)' ($headsLines -join ' / ')
& $Py -m alembic --version 2>&1 | ForEach-Object { Write-Host ("Alembic version: {0}" -f (ConvertTo-Text @($_))) }

Write-Section 'A2. THE 0054 FILE PIN (byte-still recital)'
$migLenActual = (Get-Item $MigFile).Length
$migShaActual = (Get-FileHash -Algorithm SHA256 $MigFile).Hash
Write-Host ("  length  {0} (pinned {1})" -f $migLenActual, $MigLen)
Write-Host ("  sha256  {0}" -f $migShaActual)
Assert-Gate ($migLenActual -eq $MigLen) 'A2.1 migration length' $MigLen ([string]$migLenActual)
Assert-Gate ($migShaActual -ieq $MigSha) 'A2.2 migration sha256' $MigSha $migShaActual

Write-Section 'A3. TATTOO PRE + NAMED-OBJECT PRE-LISTS'
$tpre = Invoke-Read $Target "SELECT COUNT(*) FROM sqlite_master WHERE type='trigger'"
Assert-Gate ($tpre -eq '80') 'A3.1 triggers total == 80' '80' $tpre
$ppre = Invoke-Read $Target 'SELECT COUNT(*) FROM v2_permission'
Assert-Gate ($ppre -eq '72') 'A3.2 v2_permission == 72' '72' $ppre
$cpre = Invoke-Read $Target 'SELECT COUNT(*) FROM v2_computation_version'
Assert-Gate ($cpre -eq '13') 'A3.3 v2_computation_version == 13' '13' $cpre
$guardAll = ($GuardNamesAll | ForEach-Object { "'{0}'" -f $_ }) -join ','
$gpre = Invoke-Read $Target ("SELECT name FROM sqlite_master WHERE type='trigger' AND name IN ({0}) ORDER BY name" -f $guardAll)
Assert-Gate ($gpre -eq $GuardNamesPre) 'A3.4 live_exec guard set pre == the 12A intent pair' $GuardNamesPre $gpre
$lxeAbsent = Invoke-Read $Target "SELECT COUNT(*) FROM v2_computation_version WHERE component='live_exec_engine'"
Assert-Gate ($lxeAbsent -eq '0') 'A3.5 live_exec_engine compver row ABSENT pre-apply' '0' $lxeAbsent
$newPermsAbsent = Invoke-Read $Target "SELECT COUNT(*) FROM v2_permission WHERE permission IN ('v2.live_exec.submit.write','v2.live_exec.submissions.read','v2.live_exec.fills.read')"
Assert-Gate ($newPermsAbsent -eq '0') 'A3.6 the three 12B permission rows ABSENT pre-apply' '0' $newPermsAbsent
$IntentCountPre = Invoke-Read $Target 'SELECT COUNT(*) FROM v2_live_exec_intent'
$IntentDigestsPre = Invoke-Read $Target 'SELECT digest FROM v2_live_exec_intent ORDER BY digest'
Write-Host ("  12A intent ledger rows (recorded): {0}" -f $IntentCountPre)
Write-Host ("  12A intent digests (recorded): {0}" -f ($IntentDigestsPre -replace "`r?`n","; "))

Write-Section 'A4. HEALTH PRE + ANCHOR (proven rollback anchor before any mutation)'
Assert-Gate ((Invoke-Read $Target 'PRAGMA integrity_check') -eq 'ok') 'A4.1 integrity_check ok' 'ok' '(see above)'
Assert-Gate ((Invoke-Read $Target 'PRAGMA journal_mode') -eq 'delete') 'A4.2 journal delete' 'delete' '(see above)'
Assert-Gate ((-not (Test-Path ($Target + '-wal'))) -and (-not (Test-Path ($Target + '-shm')))) 'A4.3 no sidecars' 'absent' 'present'
Copy-Item $Target $Anchor
$script:AnchorCreated = $true
Assert-Gate ((Invoke-Read $Anchor 'PRAGMA integrity_check') -eq 'ok') 'A4.4 anchor integrity ok' 'ok' '(see above)'
$anchorRev = Invoke-Read $Anchor 'SELECT version_num FROM alembic_version'
Assert-Gate ($anchorRev -eq '20260909_0053') 'A4.5 anchor revision 20260909_0053' '20260909_0053' $anchorRev
$AnchorLen = (Get-Item $Anchor).Length
$AnchorSha = (Get-FileHash -Algorithm SHA256 $Anchor).Hash
Write-Host ("  anchor: {0}" -f $Anchor)
Write-Host ("  anchor size {0} sha256 {1}" -f $AnchorLen, $AnchorSha)

Write-Section 'A5. LXE PRE-COMPUTE GATE (CR-1 land-state proof; halts before any mutation)'
$lxeActual = Invoke-Lxe $Backend
Write-Host ("  computed: {0}" -f $lxeActual)
Write-Host ("  expected: {0}" -f $LxeExpect)
Assert-Gate ($lxeActual -eq $LxeExpect) 'A5 lxe rolling hash == CR-1 final bytes (b060f435...)' $LxeExpect $lxeActual

# --------------------------------------------------------------- A6 REHEARSAL
Write-Section 'A6. REHEARSAL UPGRADE (byte-copy only)'
Copy-Item $Target $Reh
$r = Invoke-Alembic $Reh 'upgrade 20260909_0054'
Assert-Gate ($r.Code -eq 0) 'A6.0 rehearsal upgrade exit 0' '0' ([string]$r.Code)
Assert-Gate ((Count-Hits $r.Text 'Running upgrade 20260909_0053 -> 20260909_0054') -eq 1) 'A6.1 exactly one Running upgrade line' '1' ([string](Count-Hits $r.Text 'Running upgrade 20260909_0053 -> 20260909_0054'))
Assert-NoBadTokens $r.Text 'A6.2 rehearsal console'
Assert-Gate ((Invoke-Read $Reh "SELECT COUNT(*) FROM sqlite_master WHERE type='trigger'") -eq '84') 'A6.3 rehearsal triggers 84' '84' '(see above)'
Assert-Gate ((Invoke-Read $Reh 'SELECT COUNT(*) FROM v2_permission') -eq '75') 'A6.4 rehearsal perms 75' '75' '(see above)'
Assert-Gate ((Invoke-Read $Reh 'SELECT COUNT(*) FROM v2_computation_version') -eq '14') 'A6.5 rehearsal compver 14' '14' '(see above)'
$lxeReh = Invoke-Read $Reh "SELECT component, version, source_hash, evidence_ref FROM v2_computation_version WHERE component='live_exec_engine'"
Assert-Gate ($lxeReh -eq $LxeRowExpect) 'A6.6 rehearsal lxe compver row content-exact' $LxeRowExpect $lxeReh

Write-Section 'A7. REHEARSAL DOWNGRADE PROOF (full reversibility, on the copy)'
$r = Invoke-Alembic $Reh 'downgrade 20260909_0053'
Assert-Gate ($r.Code -eq 0) 'A7.0 rehearsal downgrade exit 0' '0' ([string]$r.Code)
Assert-Gate ((Count-Hits $r.Text 'Running downgrade 20260909_0054 -> 20260909_0053') -eq 1) 'A7.1 exactly one Running downgrade line' '1' ([string](Count-Hits $r.Text 'Running downgrade 20260909_0054 -> 20260909_0053'))
Assert-NoBadTokens $r.Text 'A7.2 rehearsal console (incl. compver delete-guard dance silent)'
Assert-Gate ((Invoke-Read $Reh 'SELECT version_num FROM alembic_version') -eq '20260909_0053') 'A7.3 rehearsal revision restored 20260909_0053' '20260909_0053' '(see above)'
Assert-Gate ((Invoke-Read $Reh "SELECT COUNT(*) FROM sqlite_master WHERE type='trigger'") -eq '80') 'A7.4 rehearsal triggers restored 80' '80' '(see above)'
Assert-Gate ((Invoke-Read $Reh 'SELECT COUNT(*) FROM v2_permission') -eq '72') 'A7.5 rehearsal perms restored 72' '72' '(see above)'
Assert-Gate ((Invoke-Read $Reh 'SELECT COUNT(*) FROM v2_computation_version') -eq '13') 'A7.6 rehearsal compver restored 13' '13' '(see above)'
Assert-Gate ((Invoke-Read $Reh "SELECT COUNT(*) FROM sqlite_master WHERE type='table' AND name IN ('v2_live_exec_submission','v2_live_exec_fill_event')") -eq '0') 'A7.7 rehearsal tables removed' '0' '(see above)'
Write-Host 'NOTE (register-logged advisory, not a finding): the recreated compver DELETE guard carries the migration-literal message ''V2 computation versions are immutable; DELETE prohibited'' (vs the inherited ''registry'' wording); invariant identical; visible only on a downgraded chain.'
$cvdReh = Invoke-Refuse $Reh "DELETE FROM v2_computation_version WHERE component='indicator_engine'"
Assert-Gate ($cvdReh -eq $CvdNewLiteral) 'A7.8 rehearsal recreated-guard refusal (documented literal)' $CvdNewLiteral $cvdReh

# ----------------------------------------------------------------- A8 APPLY
Write-Section 'A8. THE APPLY (single sanctioned mutation, fielded file)'
Write-Host ("Target: {0}" -f $Target)
$r = Invoke-Alembic $Target 'upgrade 20260909_0054'
Assert-Gate ($r.Code -eq 0) 'A8.0 apply exit 0' '0' ([string]$r.Code)
Assert-Gate ((Count-Hits $r.Text 'Running upgrade 20260909_0053 -> 20260909_0054') -eq 1) 'A8.1 exactly one Running upgrade line' '1' ([string](Count-Hits $r.Text 'Running upgrade 20260909_0053 -> 20260909_0054'))
Assert-NoBadTokens $r.Text 'A8.2 apply console'

# -------------------------------------------------------------- A9 TERMINAL
Write-Section 'A9. FIELDED TERMINAL STATE'
$r = Invoke-Alembic $Target 'current'
$cur = Get-AlembicCurrent $r.Text
Assert-Gate ($cur -eq '20260909_0054 (head)') 'A9.1 stamped 20260909_0054 (head)' '20260909_0054 (head)' $cur
Assert-Gate ((Invoke-Read $Target "SELECT COUNT(*) FROM sqlite_master WHERE type='trigger'") -eq '84') 'A9.2 triggers 84' '84' '(see above)'
Assert-Gate ((Invoke-Read $Target 'SELECT COUNT(*) FROM v2_permission') -eq '75') 'A9.3 perms 75' '75' '(see above)'
Assert-Gate ((Invoke-Read $Target 'SELECT COUNT(*) FROM v2_computation_version') -eq '14') 'A9.4 compver 14' '14' '(see above)'
$gpost = Invoke-Read $Target ("SELECT name FROM sqlite_master WHERE type='trigger' AND name IN ({0}) ORDER BY name" -f $guardAll)
Assert-Gate ($gpost -eq ($GuardNamesAll -join "`n")) 'A9.5 six live_exec guard names exact' ($GuardNamesAll -join ' / ') ($gpost -replace "`r?`n",' / ')
$idxRows = Invoke-Read $Target "SELECT name FROM sqlite_master WHERE type='index' AND name IN ('ix_v2_lxfill_created','ix_v2_lxsub_created','uq_v2_lxfill_identity','uq_v2_lxsub_intent') ORDER BY name"
$idxSet = @($idxRows -split "`r?`n" | Where-Object { $_.Trim() -ne '' })
Assert-Gate (Set-Equal $idxSet (,'ix_v2_lxfill_created' + ,'ix_v2_lxsub_created' + ,'uq_v2_lxfill_identity' + ,'uq_v2_lxsub_intent')) 'A9.6 four 12B indexes present' ($NewIndexes -join ' / ') ($idxRows -replace "`r?`n",' / ')
Assert-Gate ((Invoke-Read $Target 'SELECT COUNT(*) FROM v2_live_exec_submission') -eq '0') 'A9.7 submission table present and empty' '0' '(see above)'
Assert-Gate ((Invoke-Read $Target 'SELECT COUNT(*) FROM v2_live_exec_fill_event') -eq '0') 'A9.8 fill_event table present and empty' '0' '(see above)'
$permPost = Invoke-Read $Target "SELECT role, permission, sal FROM v2_permission WHERE permission IN ('v2.live_exec.submit.write','v2.live_exec.submissions.read','v2.live_exec.fills.read') ORDER BY permission"
Assert-Gate ($permPost -eq $PermRowsExpect) 'A9.9 three 12B permission rows content-exact' $PermRowsExpect $permPost
$lxePost = Invoke-Read $Target "SELECT component, version, source_hash, evidence_ref FROM v2_computation_version WHERE component='live_exec_engine'"
Assert-Gate ($lxePost -eq $LxeRowExpect) 'A9.10 fielded lxe compver row content-exact (DB == disk)' $LxeRowExpect $lxePost
$IntentCountPost = Invoke-Read $Target 'SELECT COUNT(*) FROM v2_live_exec_intent'
$IntentDigestsPost = Invoke-Read $Target 'SELECT digest FROM v2_live_exec_intent ORDER BY digest'
Assert-Gate ($IntentCountPost -eq $IntentCountPre) 'A9.11 12A intent ledger count unchanged' $IntentCountPre $IntentCountPost
Assert-Gate ($IntentDigestsPost -eq $IntentDigestsPre) 'A9.12 12A intent digests unchanged' $IntentDigestsPre $IntentDigestsPost

Write-Section 'A10. GUARD REFUSALS (six; always rolled back)'
$insSub = "INSERT INTO v2_live_exec_submission (id, intent_id, lane, terminal_state, order_request, digest, actor_id, data_class, mode, operator_id, created_at) VALUES ('__guardprobe_0054__', 'gp', 'practice', 'rejected', '{}', 'gp', 'gp', 'simulated', 'PAPER', 'itrga-gp', '2026-09-08 00:00:00')"
$gp = Invoke-GuardProbe $Target 'v2_live_exec_submission' $insSub "UPDATE v2_live_exec_submission SET raw_note='x' WHERE id='__guardprobe_0054__'"
Write-Host ($gp -join "`n")
Assert-Gate (($gp.Count -eq 2) -and ($gp[0] -eq $SubUpd) -and ($gp[1] -eq 'rolledback=1')) 'A10.1 submission UPDATE refusal exact + rolled back' $SubUpd ($gp -join ' / ')
$gp = Invoke-GuardProbe $Target 'v2_live_exec_submission' $insSub "DELETE FROM v2_live_exec_submission WHERE id='__guardprobe_0054__'"
Write-Host ($gp -join "`n")
Assert-Gate (($gp.Count -eq 2) -and ($gp[0] -eq $SubDel) -and ($gp[1] -eq 'rolledback=1')) 'A10.2 submission DELETE refusal exact + rolled back' $SubDel ($gp -join ' / ')
$insFil = "INSERT INTO v2_live_exec_fill_event (id, submission_id, fill_event_identity, correlation_basis, correlation_ref, fill_payload, actor_id, data_class, mode, operator_id, created_at) VALUES ('__guardprobe_0054__', 'gp', 'gp-0054', 'server_ack_ref', 'gp', '{}', 'gp', 'simulated', 'PAPER', 'itrga-gp', '2026-09-08 00:00:00')"
$gp = Invoke-GuardProbe $Target 'v2_live_exec_fill_event' $insFil "UPDATE v2_live_exec_fill_event SET correlation_ref='x' WHERE id='__guardprobe_0054__'"
Write-Host ($gp -join "`n")
Assert-Gate (($gp.Count -eq 2) -and ($gp[0] -eq $FilUpd) -and ($gp[1] -eq 'rolledback=1')) 'A10.3 fill_event UPDATE refusal exact + rolled back' $FilUpd ($gp -join ' / ')
$gp = Invoke-GuardProbe $Target 'v2_live_exec_fill_event' $insFil "DELETE FROM v2_live_exec_fill_event WHERE id='__guardprobe_0054__'"
Write-Host ($gp -join "`n")
Assert-Gate (($gp.Count -eq 2) -and ($gp[0] -eq $FilDel) -and ($gp[1] -eq 'rolledback=1')) 'A10.4 fill_event DELETE refusal exact + rolled back' $FilDel ($gp -join ' / ')
$cvu = Invoke-Refuse $Target "UPDATE v2_computation_version SET version='probe' WHERE component='indicator_engine'"
Assert-Gate ($cvu -eq $CvuOld) 'A10.5 compver UPDATE refusal (ORIGINAL literal; guard untouched by upgrade)' $CvuOld $cvu
$cvd = Invoke-Refuse $Target "DELETE FROM v2_computation_version WHERE component='indicator_engine'"
Assert-Gate ($cvd -eq $CvdOld) 'A10.6 compver DELETE refusal (ORIGINAL literal)' $CvdOld $cvd
Assert-Gate ((Invoke-Read $Target 'SELECT COUNT(*) FROM v2_live_exec_submission') -eq '0') 'A10.7 submissions still 0 after probes' '0' '(see above)'
Assert-Gate ((Invoke-Read $Target 'SELECT COUNT(*) FROM v2_live_exec_fill_event') -eq '0') 'A10.8 fill_events still 0 after probes' '0' '(see above)'

Write-Section 'A11. HEALTH POST + DRIFT + ENVIRONMENT CLOSE'
Assert-Gate ((Invoke-Read $Target 'PRAGMA integrity_check') -eq 'ok') 'A11.1 integrity ok' 'ok' '(see above)'
Assert-Gate ((Invoke-Read $Target 'PRAGMA journal_mode') -eq 'delete') 'A11.2 journal delete' 'delete' '(see above)'
Assert-Gate ((-not (Test-Path ($Target + '-wal'))) -and (-not (Test-Path ($Target + '-shm')))) 'A11.3 no sidecars' 'absent' 'present'
$r = Invoke-Alembic $Target 'check'
Assert-Gate (-not $r.Text.Contains('New upgrade operations detected')) 'A11.4 drift silent (no new upgrade operations)' 'absent' '(present - see output above)'
$sweep = @(Get-ChildItem env: | Where-Object { $_.Name -match '^AXIOM_(TD|BROKER_PRACTICE)' })
Assert-Gate ($sweep.Count -eq 0) 'A11.5 environment close: still no TD/PRACTICE variables' 'absent' (($sweep | ForEach-Object { $_.Name }) -join ', ')

# ------------------------------------------------------------------ A12 VERDICT
Write-Section 'A12. FINAL APPLY VERDICT'
$PostLen = (Get-Item $Target).Length
$PostSha = (Get-FileHash -Algorithm SHA256 $Target).Hash
$postFacts = @(
  ('RUN_TIMESTAMP     {0}' -f (Get-Date -Format 'yyyy-MM-dd HH:mm:ss zzz')),
  ('POST_REVISION     20260909_0054'),
  ('POST_TRIGGERS     84'),
  ('POST_PERMISSIONS  75'),
  ('POST_COMPVER      14'),
  ('POST_SIZE_BYTES   {0}' -f $PostLen),
  ('POST_SHA256       {0}' -f $PostSha),
  ('LXE_COMPVER       b060f435c7c339fbe5e23daf8231af04bf62cd8cc43ccd7d8a5f5067b78bb8c2'),
  ('ANCHOR_FILENAME   {0}' -f (Split-Path $Anchor -Leaf)),
  ('ANCHOR_SIZE_BYTES {0}' -f $AnchorLen),
  ('ANCHOR_SHA256     {0}' -f $AnchorSha),
  ('REHEARSAL_COPY    {0} (retain until ITRGA acknowledges the witness; then delete)' -f (Split-Path $Reh -Leaf)),
  'VERDICT           PASS'
)
$postFacts | Set-Content -Path $FinalStatePath -Encoding ascii
Write-Host ("post-apply size {0} sha256 {1}" -f $PostLen, $PostSha)
Write-Host ''
Write-Host "APPLY VERDICT: PASS - migration 20260909_0054_v2_be12b_submission_fills applied ONCE to '$Target'."
Write-Host 'Terminal state: revision 20260909_0054; tattoo 84/75/14; two 12B tables present-and-empty with four immutable guards (six exact refusals incl. both compver ORIGINAL literals); three 12B permission rows content-exact; lxe compver row == disk (b060f435...); 12A intent ledger untouched (count + digests proven); integrity ok; drift silent; anchor + rehearsal copy in operator-evidence\BE-12B; no TD/PRACTICE variable at start or end.'
Write-Host ("Transcript: {0}" -f $TranscriptPath)
Write-Host ("State record: {0}" -f $FinalStatePath)
Write-Host 'NEXT: restart the application when ready. Send the transcript + state record to ITRGA. The fielding verdict (FIELDED) and the register line are issued on receipt.'

} finally {
  Remove-Item Env:AXIOM_DATABASE_URL -ErrorAction SilentlyContinue
  if ($script:TranscriptOn) { try { Stop-Transcript | Out-Null } catch { } }
}
