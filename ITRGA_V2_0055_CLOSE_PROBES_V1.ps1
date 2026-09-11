<#
===============================================================================
ITRGA_V2_0055_CLOSE_PROBES_V1.ps1
===============================================================================
Pack:      ITRGA-V2-0055-CLOSE-PROBES-V1 (CLOSING WITNESS; complement to the
           halted apply run 0055-APPLY-RUN-V1-20260909120822)
Act:       NO MUTATION OF ANY KIND. This pack NEVER runs alembic upgrade or
           downgrade. It re-verifies the (already fielded) terminal state and
           completes the refused-write probe / health / drift / record
           sections that the V1 run never reached (halt at A10.3 was a
           PIN-FORM halt, corrected by ERRATUM E-0055-A10.3).
Implements: ITRGA-V2-0055-FIELD-APPLY-CARD-20260909 sections A9-A12 (as
           corrected) under ERRATUM E-0055-A10.3 (governing text for this run).
Authority: BO-V2-BE12C-001 SS1.g  ·  ITRGA-REV-V2-BE12C-CR-001 (APPROVED;
           BE-12C ACCEPTED; suite floor 1,265)
Pin fix:   CHECK-refusal expectations now carry the project's rendered
           naming convention (ck_<table>_<short-name>), taken from the DB's
           own DDL (printed for the record at C3.0). The CHECK vocabulary
           closure itself is identical (refusals still FIRE, still rolled
           back); only the expected string form changed.
Method:    NO python FILES (-c snippets only). NO git operations. NO
           credential of any kind. AXIOM_BROKER_PRACTICE_* / AXIOM_TD_*
           asserted ABSENT at start and end. Refused writes always rolled back.
Run:       Set-Location C:\Users\victo\.vscode\AXIOM\axiom
           powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\ITRGA_V2_0055_CLOSE_PROBES_V1.ps1
Output:    operator-evidence\BE-12C\0055-CLOSE-RUN-V1-<timestamp>.txt  (transcript)
           operator-evidence\BE-12C\0055-APPLY-FINAL-STATE.txt         (state record; the V1 run stopped before writing it — this pack writes it)
Opening gate: current revision MUST already be 20260909_0055 (head). Any
other value => HALT; this pack never repairs and never applies.
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

$Lxe6Expect    = 'b060f435c7c339fbe5e23daf8231af04bf62cd8cc43ccd7d8a5f5067b78bb8c2'
$Lxe8Expect    = 'd09306f1ab32f0dc6f26e5c7235b3e1f72c3175a1928d60673709c0b02a3809a'
$LxeRowPre     = 'live_exec_engine|lxe-1.0.0|b060f435c7c339fbe5e23daf8231af04bf62cd8cc43ccd7d8a5f5067b78bb8c2|BO-V2-BE12B-001'
$LxeRowNew     = 'live_exec_engine|lxe-1.1.0|d09306f1ab32f0dc6f26e5c7235b3e1f72c3175a1928d60673709c0b02a3809a|BO-V2-BE12C-001'
$LxeRowsExpect = $LxeRowPre + "`n" + $LxeRowNew
$PermRowsExpect= @('admin|v2.live_exec.modifies.read|SAL-2','admin|v2.live_exec.modify.write|SAL-4') -join "`n"
$GuardNamesAll = @('v2_live_exec_fill_event_immutable_delete','v2_live_exec_fill_event_immutable_update','v2_live_exec_intent_immutable_delete','v2_live_exec_intent_immutable_update','v2_live_exec_modify_event_immutable_delete','v2_live_exec_modify_event_immutable_update','v2_live_exec_submission_immutable_delete','v2_live_exec_submission_immutable_update')
$IndexNamesAll = @('ix_v2_lxfill_created','ix_v2_lxmod_created','ix_v2_lxsub_created','uq_v2_lxfill_identity','uq_v2_lxmod_identity','uq_v2_lxsub_intent')
$CvuOld        = 'REFUSED:V2 computation version registry is immutable; UPDATE prohibited'
$CvdOld        = 'REFUSED:V2 computation version registry is immutable; DELETE prohibited'
$ModUpd        = 'REFUSED:V2 live exec modify events are immutable; UPDATE prohibited'
$ModDel        = 'REFUSED:V2 live exec modify events are immutable; DELETE prohibited'
# CORRECTED per ERRATUM E-0055-A10.3 (rendered naming convention):
$CkElection    = 'REFUSED:CHECK constraint failed: ck_v2_live_exec_modify_event_ck_v2_lxmod_election'
$CkVerb        = 'REFUSED:CHECK constraint failed: ck_v2_live_exec_modify_event_ck_v2_lxmod_verb'
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
$TranscriptPath = Join-Path $EvDir ("0055-CLOSE-RUN-V1-{0}.txt" -f $ts)
$FinalStatePath = Join-Path $EvDir '0055-APPLY-FINAL-STATE.txt'

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
  Write-Host 'HALT: gate failed. Do NOT run any further command. Send this transcript to ITRGA.'
  Write-Host 'NOTE: this pack performs NO mutations; no anchor restoration is relevant to its failure.'
  if ($script:TranscriptOn) { try { Stop-Transcript | Out-Null } catch { } ; $script:TranscriptOn = $false }
  exit 1
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

function Set-Equal { param([string[]]$A, [string[]]$B)
  if ($A.Count -ne $B.Count) { return $false }
  for ($i = 0; $i -lt $A.Count; $i++) { if ($A[$i] -ne $B[$i]) { return $false } }
  return $true
}

# ------------------------------------------------------------------- C0/BEGIN
New-Item -ItemType Directory -Force $EvDir | Out-Null
$script:TranscriptOn = $true
Start-Transcript -Path $TranscriptPath | Out-Null

try {

Write-Section 'C0. RUN IDENTIFICATION (CLOSING WITNESS)'
Write-Host 'Pack: ITRGA-V2-0055-CLOSE-PROBES-V1'
Write-Host 'Act: closing witness ONLY. NO mutations; NO alembic upgrade/downgrade anywhere in this pack.'
Write-Host 'Implements: CARD-20260909 sections A9-A12 under ERRATUM E-0055-A10.3 (pin-form correction)'
Write-Host 'Authority: BO-V2-BE12C-001 SS1.g / ITRGA-REV-V2-BE12C-CR-001 (APPROVED)'
Write-Host ("Started: {0}" -f (Get-Date -Format 'yyyy-MM-dd HH:mm:ss zzz'))
Write-Host ("Target file: {0}" -f $Target)
Write-Host 'Prior witness: 0055-APPLY-RUN-V1-20260909120822 (A0-A10.2 PASS; halt at A10.3 pin-form only)'
Write-Host 'Server credentials used: NONE. Provider credentials used: NONE.'
Write-Host ''
Write-Host 'Confirm the application is STOPPED. Continuing in 5 seconds; press Ctrl+C otherwise...'
Start-Sleep -Seconds 5

Write-Section 'C0b. AUTHORITY/PRACTICE ENVIRONMENT SWEEP (must print nothing)'
$sweep = @(Get-ChildItem env: | Where-Object { $_.Name -match '^AXIOM_(TD|BROKER_PRACTICE)' })
Assert-Gate ($sweep.Count -eq 0) 'C0b: no AXIOM_TD_* / AXIOM_BROKER_PRACTICE_* variables' 'absent' (($sweep | ForEach-Object { $_.Name }) -join ', ')

Write-Section 'C1. OPENING GATE — APPLY STATE ALREADY LOADED (this pack never repairs)'
$r = Invoke-Alembic $Target 'current'
Assert-Gate ($r.Code -eq 0) 'C1.0 alembic current exit 0' '0' ([string]$r.Code)
$cur = Get-AlembicCurrent $r.Text
Assert-Gate ($cur -eq '20260909_0055 (head)') 'C1.1 current is exactly 20260909_0055 (head) — apply already committed by the V1 run' '20260909_0055 (head)' $cur
$r = Invoke-Alembic $Target 'heads'
$headsLines = @($r.Text -split "`r?`n" | Where-Object { $_.Contains('(head)') })
Assert-Gate (($headsLines.Count -ge 1) -and $headsLines[0].Trim().StartsWith('20260909_0055')) 'C1.2 repo head is 20260909_0055 (head)' '20260909_0055 (head)' ($headsLines -join ' / ')

Write-Section 'C2. FIELDED TERMINAL STATE — FULL RE-VERIFY (card A9, all reads)'
Assert-Gate ((Invoke-Read $Target "SELECT COUNT(*) FROM sqlite_master WHERE type='trigger'") -eq '86') 'C2.1 triggers 86' '86' '(see above)'
Assert-Gate ((Invoke-Read $Target 'SELECT COUNT(*) FROM v2_permission') -eq '77') 'C2.2 perms 77' '77' '(see above)'
Assert-Gate ((Invoke-Read $Target 'SELECT COUNT(*) FROM v2_computation_version') -eq '15') 'C2.3 compver 15' '15' '(see above)'
$guardAll = ($GuardNamesAll | ForEach-Object { "'{0}'" -f $_ }) -join ','
$gpost = Invoke-Read $Target ("SELECT name FROM sqlite_master WHERE type='trigger' AND name IN ({0}) ORDER BY name" -f $guardAll)
Assert-Gate ($gpost -eq ($GuardNamesAll -join "`n")) 'C2.4 eight live_exec guard names exact' ($GuardNamesAll -join ' / ') ($gpost -replace "`r?`n",' / ')
$idxRows = Invoke-Read $Target ("SELECT name FROM sqlite_master WHERE type='index' AND name IN ({0}) ORDER BY name" -f (($IndexNamesAll | ForEach-Object { "'{0}'" -f $_ }) -join ','))
$idxSet = @($idxRows -split "`r?`n" | Where-Object { $_.Trim() -ne '' })
Assert-Gate (Set-Equal $idxSet $IndexNamesAll) 'C2.5 six 12B+12C indexes present exact' ($IndexNamesAll -join ' / ') ($idxRows -replace "`r?`n",' / ')
Assert-Gate ((Invoke-Read $Target 'SELECT COUNT(*) FROM v2_live_exec_modify_event') -eq '0') 'C2.6 modify_event table present and empty' '0' '(see above)'
Assert-Gate ((Invoke-Read $Target 'SELECT COUNT(*) FROM v2_live_exec_submission') -eq '0') 'C2.7 12B submissions still empty' '0' '(see above)'
Assert-Gate ((Invoke-Read $Target 'SELECT COUNT(*) FROM v2_live_exec_fill_event') -eq '0') 'C2.8 12B fill_events still empty' '0' '(see above)'
$permPost = Invoke-Read $Target "SELECT role, permission, sal FROM v2_permission WHERE permission IN ('v2.live_exec.modify.write','v2.live_exec.modifies.read') ORDER BY permission"
Assert-Gate ($permPost -eq $PermRowsExpect) 'C2.9 two 12C permission rows content-exact' $PermRowsExpect $permPost
$lxePost = Invoke-Read $Target "SELECT component, version, source_hash, evidence_ref FROM v2_computation_version WHERE component='live_exec_engine' ORDER BY version"
Assert-Gate ($lxePost -eq $LxeRowsExpect) 'C2.10 compver rows BOTH stand, content-exact (1.0.0 then 1.1.0)' $LxeRowsExpect $lxePost
$IntentCountPost = Invoke-Read $Target 'SELECT COUNT(*) FROM v2_live_exec_intent'
$IntentDigestsPost = Invoke-Read $Target 'SELECT digest FROM v2_live_exec_intent ORDER BY digest'
Write-Host ("  12A intent ledger rows: {0} (digests: {1})" -f $IntentCountPost, ($IntentDigestsPost -replace "`r?`n",'; '))
Assert-Gate ($IntentCountPost -eq '1') 'C2.11 12A intent ledger count == 1 (wire-proofed row standing)' '1' $IntentCountPost
$lxe6Post = Invoke-Lxe $Backend $CodeLxe6
Assert-Gate ($lxe6Post -eq $Lxe6Expect) 'C2.12 disk 6-file lxe still b060f435...' $Lxe6Expect $lxe6Post
$lxe8Post = Invoke-Lxe $Backend $CodeLxe8
Assert-Gate ($lxe8Post -eq $Lxe8Expect) 'C2.13 disk 8-file lxe still d09306f1...' $Lxe8Expect $lxe8Post

Write-Section 'C3. GUARD / CHECK REFUSALS (eight; card A10 with corrected pins)'
Write-Host 'C3.0 — the rendered CHECK names from the DB''s own DDL (erratum-record):'
$ddl = Invoke-Read $Target "SELECT sql FROM sqlite_master WHERE type='table' AND name='v2_live_exec_modify_event'"
Write-Host $ddl
$insMod = "INSERT INTO v2_live_exec_modify_event (id, submission_id, intent_id, verb, act_identity, request_payload, outcome, operator_election, actor_id, data_class, mode, operator_id, created_at) VALUES ('__guardprobe_0055__', 'gp', 'gp', 'cancel', 'gp-0055', '{}', 'applied', 'standard', 'gp', 'simulated', 'PAPER', 'itrga-gp', '2026-09-09 00:00:00')"
$gp = Invoke-GuardProbe $Target 'v2_live_exec_modify_event' $insMod "UPDATE v2_live_exec_modify_event SET raw_note='x' WHERE id='__guardprobe_0055__'"
Write-Host ($gp -join "`n")
Assert-Gate (($gp.Count -eq 2) -and ($gp[0] -eq $ModUpd) -and ($gp[1] -eq 'rolledback=1')) 'C3.1 modify_event UPDATE refusal exact + rolled back' $ModUpd ($gp -join ' / ')
$gp = Invoke-GuardProbe $Target 'v2_live_exec_modify_event' $insMod "DELETE FROM v2_live_exec_modify_event WHERE id='__guardprobe_0055__'"
Write-Host ($gp -join "`n")
Assert-Gate (($gp.Count -eq 2) -and ($gp[0] -eq $ModDel) -and ($gp[1] -eq 'rolledback=1')) 'C3.2 modify_event DELETE refusal exact + rolled back' $ModDel ($gp -join ' / ')
$ckel = Invoke-Refuse $Target "INSERT INTO v2_live_exec_modify_event (id, submission_id, intent_id, verb, act_identity, request_payload, outcome, operator_election, actor_id, data_class, mode, operator_id, created_at) VALUES ('__guardprobe_0055__', 'gp', 'gp', 'cancel', 'gp-0055-cke', '{}', 'applied', 'auto_recovery', 'gp', 'simulated', 'PAPER', 'itrga-gp', '2026-09-09 00:00:00')"
Assert-Gate ($ckel -eq $CkElection) 'C3.3 election CHECK refusal exact (rendered name; auto_recovery closed out)' $CkElection $ckel
$ckvb = Invoke-Refuse $Target "INSERT INTO v2_live_exec_modify_event (id, submission_id, intent_id, verb, act_identity, request_payload, outcome, operator_election, actor_id, data_class, mode, operator_id, created_at) VALUES ('__guardprobe_0055__', 'gp', 'gp', 'close', 'gp-0055-ckv', '{}', 'applied', 'standard', 'gp', 'simulated', 'PAPER', 'itrga-gp', '2026-09-09 00:00:00')"
Assert-Gate ($ckvb -eq $CkVerb) 'C3.4 verb CHECK refusal exact (rendered name; close does not exist)' $CkVerb $ckvb
$cvu = Invoke-Refuse $Target "UPDATE v2_computation_version SET version='probe' WHERE component='indicator_engine'"
Assert-Gate ($cvu -eq $CvuOld) 'C3.5 compver UPDATE refusal (ORIGINAL literal; guard untouched by upgrade)' $CvuOld $cvu
$cvd = Invoke-Refuse $Target "DELETE FROM v2_computation_version WHERE component='indicator_engine'"
Assert-Gate ($cvd -eq $CvdOld) 'C3.6 compver DELETE refusal (ORIGINAL literal)' $CvdOld $cvd
Assert-Gate ((Invoke-Read $Target 'SELECT COUNT(*) FROM v2_live_exec_modify_event') -eq '0') 'C3.7 modify_event still 0 after probes' '0' '(see above)'
Assert-Gate ((Invoke-Read $Target 'SELECT COUNT(*) FROM v2_live_exec_submission') -eq '0') 'C3.8 submissions still 0 after probes' '0' '(see above)'

Write-Section 'C4. HEALTH POST + DRIFT (ITEMIZED LAW) + ENVIRONMENT CLOSE'
Assert-Gate ((Invoke-Read $Target 'PRAGMA integrity_check') -eq 'ok') 'C4.1 integrity ok' 'ok' '(see above)'
Assert-Gate ((Invoke-Read $Target 'PRAGMA journal_mode') -eq 'delete') 'C4.2 journal delete' 'delete' '(see above)'
Assert-Gate ((-not (Test-Path ($Target + '-wal'))) -and (-not (Test-Path ($Target + '-shm')))) 'C4.3 no sidecars' 'absent' 'present'
Write-Host 'Drift law (ITEMIZED): every detected operation must name one of the 9 inherited V1 tokens; forbidden band tokens absent; silence is a pass-subset.'
$r = Invoke-Alembic $Target 'check'
foreach ($tok in $DriftForbidden) {
  Assert-Gate (-not ($r.Text -imatch [regex]::Escape($tok))) ("C4.4 drift: band token '{0}' absent" -f $tok) 'absent' 'present'
}
$opLines = @($r.Text -split "`r?`n" | Where-Object { $_ -imatch 'add_(table|index)|remove_index' })
$bad = @()
foreach ($ln in $opLines) {
  $hit = $false
  foreach ($w in $DriftWhitelist) { if ($ln -imatch [regex]::Escape($w)) { $hit = $true; break } }
  if (-not $hit) { $bad += $ln }
}
Assert-Gate ($bad.Count -eq 0) 'C4.5 drift: every detected operation names an inherited V1 token (9-item whitelist)' 'only the 9 inherited V1 tokens' ($bad -join ' / ')
Write-Host ("  drift operations witnessed (itemized): {0}" -f $opLines.Count)
$sweep = @(Get-ChildItem env: | Where-Object { $_.Name -match '^AXIOM_(TD|BROKER_PRACTICE)' })
Assert-Gate ($sweep.Count -eq 0) 'C4.6 environment close: still no TD/PRACTICE variables' 'absent' (($sweep | ForEach-Object { $_.Name }) -join ', ')

# ------------------------------------------------------------------ C5 RECORD
Write-Section 'C5. FINAL APPLY VERDICT + STATE RECORD (card A12 completion)'
$PostLen = (Get-Item $Target).Length
$PostSha = (Get-FileHash -Algorithm SHA256 $Target).Hash
$anchorFiles = @(Get-ChildItem $EvDir -Filter 'axiom_dev.db.pre-0055-*.bak' | Sort-Object Name)
$rehFiles    = @(Get-ChildItem $EvDir -Filter 'axiom_dev.db.rehearsal-0055-*.db' | Sort-Object Name)
$anchorName  = if ($anchorFiles.Count -gt 0) { $anchorFiles[$anchorFiles.Count - 1].Name } else { '(none found in BE-12C)' }
$rehName     = if ($rehFiles.Count -gt 0) { $rehFiles[$rehFiles.Count - 1].Name } else { '(none found in BE-12C)' }
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
  ('ANCHOR_FILENAME   {0}' -f $anchorName),
  ('REHEARSAL_COPY    {0} (retain until ITRGA acknowledges the witness; then delete)' -f $rehName),
  'CLOSING_MODE      close-probes per ERRATUM E-0055-A10.3 (pin-form correction; CHECK closure proven, rendered names)',
  'VERDICT           PASS'
)
$postFacts | Set-Content -Path $FinalStatePath -Encoding ascii
Write-Host ("post-apply size {0} sha256 {1}" -f $PostLen, $PostSha)
Write-Host ''
Write-Host "CLOSING VERDICT: PASS - fielded terminal witness completed for '$Target'."
Write-Host 'State: revision 20260909_0055 (head); tattoo 86/77/15; modify_event present-and-empty with immutable guard pair + closed CHECKs (four 12C refusals + two compver ORIGINAL literals, all rolled back); two 12C permission rows content-exact; compver BOTH rows standing (1.0.0 b060f435...; 1.1.0 d09306f1... == disk); 12A intent ledger standing (1 wire row); disk lxe hashes re-proven; integrity ok; drift gate ITEMIZED pass; no TD/PRACTICE variable at start or end; ZERO mutations performed by this pack.'
Write-Host ("Transcript: {0}" -f $TranscriptPath)
Write-Host ("State record: {0}" -f $FinalStatePath)
Write-Host 'NEXT: restart the application when ready. Send THIS transcript + the final-state record to ITRGA. The FIELDED verdict and register line are issued on receipt.'

} finally {
  Remove-Item Env:AXIOM_DATABASE_URL -ErrorAction SilentlyContinue
  if ($script:TranscriptOn) { try { Stop-Transcript | Out-Null } catch { } }
}
