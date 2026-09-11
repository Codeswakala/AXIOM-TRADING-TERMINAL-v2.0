<#
===============================================================================
ITRGA_V2_0057_APPLY_PACK_V1.ps1
===============================================================================
Pack:      ITRGA-V2-0057-APPLY-PACK-V1
Act:       0057 working-database application act (single sanctioned mutation)
Implements: ITRGA-V2-0057-FIELD-APPLY-CARD-20260909 (the card remains the
           governing text; this pack is the authorized equivalent runner).
Authority: BO-V2-BE12E-001 SS1.g  ·  ITRGA-REV-V2-BE12E-001 (base)  ·
           ITRGA-REV-V2-BE12E-CR-001 (CR-1 APPROVED; BE-12E ACCEPTED;
           suite floor 1,311; LOW DEL-005/DEL-006 register-logged, closeout-era)
Mutation:  EXACTLY ONE —  python -m alembic upgrade 20260909_0057
           against the fielded working database axiom_dev.db.
           Rehearsal runs on a byte-copy ONLY. All guard/CHECK probes are
           refused-write and always rolled back.
FIELD LAW (12E-specific): the 0057 tables are EVIDENCE LEDGERS (rows are
           lawful evidence by verb) — this act pins ZERO-ROW BY ELECTION at
           every witness point, on ALL SEVEN 12-series tables; NO ENGINE VERB
           runs on the fielded file (no reconcile run, no incident open/close;
           no governor verb; no force act). "The fielded lineage holds no
           runtime evidence rows of any band." Posture, not doctrine.
Method:    NO python FILES of any kind (-c snippets only). NO git operations.
           NO credential of any kind. AXIOM_BROKER_PRACTICE_* / AXIOM_TD_*
           asserted ABSENT at start and end.
Errata:    CHECK pins are RENDERED names (E-0055-A10.3, from birth —
           enumerated from the CR-1 migration coupon, cross-pinned by the
           A9 DDL print). Drift gate ITEMIZED (E-0054-A11.4).
Run:       Set-Location C:\Users\victo\.vscode\AXIOM\axiom
           powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\ITRGA_V2_0057_APPLY_PACK_V1.ps1
Output:    operator-evidence\BE-12E\0057-APPLY-RUN-V1-<timestamp>.txt  (transcript)
           operator-evidence\BE-12E\0057-APPLY-FINAL-STATE.txt         (state record)
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
$EvDir         = 'C:\Users\victo\.vscode\AXIOM\axiom\operator-evidence\BE-12E'
$MigFile       = 'C:\Users\victo\.vscode\AXIOM\axiom\backend\alembic\versions\20260909_0057_v2_be12e_reconciliation_incident.py'
$ProbeId       = '__guardprobe_0057__'

$MigSha        = '03CA0069A8C7DB59804A67755375EEDDE74334071D59B899C1076C3E1A8422A0'
$MigLen        = 11197
$Lxe6Expect    = 'b060f435c7c339fbe5e23daf8231af04bf62cd8cc43ccd7d8a5f5067b78bb8c2'
$Lxe8Expect    = 'd09306f1ab32f0dc6f26e5c7235b3e1f72c3175a1928d60673709c0b02a3809a'
$Lxe13Expect   = 'd25c48579def993b63e6f84ca17e937c3e938f75b0ca1f78f8aea81b1e9c1705'
$Lxe18Expect   = '93f436bc90f1a8826154717e7b310be531a86bb8cc968a5f05d2f7b9112cd1f3'
$LxeRow100     = 'live_exec_engine|lxe-1.0.0|b060f435c7c339fbe5e23daf8231af04bf62cd8cc43ccd7d8a5f5067b78bb8c2|BO-V2-BE12B-001'
$LxeRow110     = 'live_exec_engine|lxe-1.1.0|d09306f1ab32f0dc6f26e5c7235b3e1f72c3175a1928d60673709c0b02a3809a|BO-V2-BE12C-001'
$LxeRow120     = 'live_exec_engine|lxe-1.2.0|d25c48579def993b63e6f84ca17e937c3e938f75b0ca1f78f8aea81b1e9c1705|BO-V2-BE12D-001'
$LxeRow130     = 'live_exec_engine|lxe-1.3.0|93f436bc90f1a8826154717e7b310be531a86bb8cc968a5f05d2f7b9112cd1f3|BO-V2-BE12E-001'
$LxeRowsPre    = $LxeRow100 + "`n" + $LxeRow110 + "`n" + $LxeRow120
$LxeRowsPost   = $LxeRowsPre + "`n" + $LxeRow130
$PermRowsExpect= @(
  'admin|v2.live_exec.incident.close|SAL-4',
  'admin|v2.live_exec.incident.open|SAL-4',
  'admin|v2.live_exec.incident.read|SAL-2',
  'admin|v2.live_exec.reconcile.read|SAL-2',
  'admin|v2.live_exec.reconcile.run|SAL-4'
) -join "`n"
$NewPerms      = @('v2.live_exec.incident.close','v2.live_exec.incident.open','v2.live_exec.incident.read','v2.live_exec.reconcile.read','v2.live_exec.reconcile.run')
$GuardNamesPre = @('v2_live_activation_instrument_immutable_delete','v2_live_activation_instrument_immutable_update','v2_live_exec_fill_event_immutable_delete','v2_live_exec_fill_event_immutable_update','v2_live_exec_intent_immutable_delete','v2_live_exec_intent_immutable_update','v2_live_exec_modify_event_immutable_delete','v2_live_exec_modify_event_immutable_update','v2_live_exec_submission_immutable_delete','v2_live_exec_submission_immutable_update','v2_live_kill_switch_immutable_delete','v2_live_kill_switch_immutable_update')
$GuardNamesAll = @('v2_live_activation_instrument_immutable_delete','v2_live_activation_instrument_immutable_update','v2_live_exec_fill_event_immutable_delete','v2_live_exec_fill_event_immutable_update','v2_live_exec_incident_immutable_delete','v2_live_exec_incident_immutable_update','v2_live_exec_intent_immutable_delete','v2_live_exec_intent_immutable_update','v2_live_exec_modify_event_immutable_delete','v2_live_exec_modify_event_immutable_update','v2_live_exec_reconciliation_immutable_delete','v2_live_exec_reconciliation_immutable_update','v2_live_exec_submission_immutable_delete','v2_live_exec_submission_immutable_update','v2_live_kill_switch_immutable_delete','v2_live_kill_switch_immutable_update')
$IndexNamesAll = @('ix_v2_lxfill_created','ix_v2_lxinc_created','ix_v2_lxmod_created','ix_v2_lxrecon_created','ix_v2_lxsub_created','uq_v2_lai_sole','uq_v2_lks_sole','uq_v2_lxfill_identity','uq_v2_lxmod_identity','uq_v2_lxsub_intent')
$ZeroTables    = @('v2_live_exec_submission','v2_live_exec_fill_event','v2_live_exec_modify_event','v2_live_activation_instrument','v2_live_kill_switch','v2_live_exec_reconciliation','v2_live_exec_incident')
$CvuOld        = 'REFUSED:V2 computation version registry is immutable; UPDATE prohibited'
$CvdOld        = 'REFUSED:V2 computation version registry is immutable; DELETE prohibited'
$CvdNewLiteral = 'REFUSED:V2 computation versions are immutable; DELETE prohibited'
$ReconUpd      = 'REFUSED:V2 live exec reconciliation is immutable; UPDATE prohibited'
$ReconDel      = 'REFUSED:V2 live exec reconciliation is immutable; DELETE prohibited'
$IncUpd        = 'REFUSED:V2 live exec incidents are immutable; UPDATE prohibited'
$IncDel        = 'REFUSED:V2 live exec incidents are immutable; DELETE prohibited'
$CkLxreconOutcome = 'REFUSED:CHECK constraint failed: ck_v2_live_exec_reconciliation_ck_v2_lxrecon_outcome'
$CkLxreconClass   = 'REFUSED:CHECK constraint failed: ck_v2_live_exec_reconciliation_ck_v2_lxrecon_data_class'
$CkLxincSeverity  = 'REFUSED:CHECK constraint failed: ck_v2_live_exec_incident_ck_v2_lxinc_severity'
$CkLxincStatus    = 'REFUSED:CHECK constraint failed: ck_v2_live_exec_incident_ck_v2_lxinc_status'
$CkLxincClass     = 'REFUSED:CHECK constraint failed: ck_v2_live_exec_incident_ck_v2_lxinc_data_class'
$DriftWhitelist= @(
  'audit_write_failure_records','ix_audit_write_failures_category_action',
  'ix_audit_write_failures_created','ix_advisory_signals_expires_at',
  'ix_advisory_signals_freshness_status','ix_ingestion_runs_symbol_started',
  'ix_model_artifacts_advisory_status','ix_model_artifacts_artifact_hash',
  'ix_model_artifacts_experiment_id'
)
$DriftForbidden= @('v2_','live_exec','lxmod','modify_event','activation_instrument','kill_switch','lxrecon','lxinc','reconciliation','incident')

$ts             = Get-Date -Format yyyyMMddHHmmss
$TranscriptPath = Join-Path $EvDir ("0057-APPLY-RUN-V1-{0}.txt" -f $ts)
$FinalStatePath = Join-Path $EvDir '0057-APPLY-FINAL-STATE.txt'
$Anchor         = Join-Path $EvDir ("axiom_dev.db.pre-0057-{0}.bak" -f $ts)
$Reh            = Join-Path $EvDir ("axiom_dev.db.rehearsal-0057-{0}.db" -f $ts)

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
 left=c.execute('SELECT COUNT(*) FROM '+sys.argv[2]+' WHERE id='+chr(39)+sys.argv[5]+chr(39)).fetchone()[0]
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

$CodeLxe18 = @'
import hashlib,sys
from pathlib import Path
refs=('app/v2/live_exec/intents.py','app/v2/live_exec/eligibility.py','app/v2/live_exec/risk.py','app/v2/live_exec/locks.py','app/v2/live_exec/submissions.py','app/v2/live_exec/ack_fills.py','app/v2/live_exec/modify/__init__.py','app/v2/live_exec/modify/engine.py','app/v2/live_exec/activation/__init__.py','app/v2/live_exec/activation/engine.py','app/v2/live_exec/activation/template.py','app/v2/live_exec/killswitch/__init__.py','app/v2/live_exec/killswitch/engine.py','app/v2/live_exec/reconcile/__init__.py','app/v2/live_exec/reconcile/money.py','app/v2/live_exec/reconcile/engine.py','app/v2/live_exec/incident/__init__.py','app/v2/live_exec/incident/engine.py')
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
  $raw = & $Py -c $CodeGuard $Db $Table $InsertSql $ProbeSql $ProbeId 2>&1
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
Write-Host 'Pack: ITRGA-V2-0057-APPLY-PACK-V1'
Write-Host 'Act: 0057 working-database application act (single sanctioned mutation)'
Write-Host 'Implements: ITRGA-V2-0057-FIELD-APPLY-CARD-20260909 (governing text)'
Write-Host 'Authority: BO-V2-BE12E-001 SS1.g / ITRGA-REV-V2-BE12E-001 + REV-V2-BE12E-CR-001 (APPROVED)'
Write-Host ("Started: {0}" -f (Get-Date -Format 'yyyy-MM-dd HH:mm:ss zzz'))
Write-Host ("Target file: {0}" -f $Target)
Write-Host 'FIELD LAW: evidence ledgers — zero-row BY ELECTION on all seven 12-series tables; NO engine verb runs (no reconcile run, no incident open/close; no governor verb; no force).'
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
Assert-Gate (Test-Path $MigFile) 'A0c.3 migration 0057 present' $MigFile '(missing)'

Write-Section 'A0d. 12E SOURCE-SET VISIBILITY (eighteen lxe files)'
$lxeRel = @('app/v2/live_exec/intents.py','app/v2/live_exec/eligibility.py','app/v2/live_exec/risk.py','app/v2/live_exec/locks.py','app/v2/live_exec/submissions.py','app/v2/live_exec/ack_fills.py','app/v2/live_exec/modify/__init__.py','app/v2/live_exec/modify/engine.py','app/v2/live_exec/activation/__init__.py','app/v2/live_exec/activation/engine.py','app/v2/live_exec/activation/template.py','app/v2/live_exec/killswitch/__init__.py','app/v2/live_exec/killswitch/engine.py','app/v2/live_exec/reconcile/__init__.py','app/v2/live_exec/reconcile/money.py','app/v2/live_exec/reconcile/engine.py','app/v2/live_exec/incident/__init__.py','app/v2/live_exec/incident/engine.py')
$missing = @()
foreach ($rel in $lxeRel) {
  $p = Join-Path $Backend ($rel -replace '/','\')
  if (Test-Path $p) { Write-Host ("  present  {0}" -f $rel) } else { Write-Host ("  MISSING  {0}" -f $rel); $missing += $rel }
}
Assert-Gate ($missing.Count -eq 0) 'A0d: all eighteen lxe source files present (12E landed)' '18/18 present' (($missing.Count.ToString() + ' missing: ') + ($missing -join ', '))

Write-Section 'A1. BASELINE REVISION STATE'
$r = Invoke-Alembic $Target 'current'
Assert-Gate ($r.Code -eq 0) 'A1.0 alembic current exit 0' '0' ([string]$r.Code)
$cur = Get-AlembicCurrent $r.Text
Assert-Gate ($cur -eq '20260909_0056') 'A1.1 current is exactly 20260909_0056 (no (head) suffix)' '20260909_0056' $cur
$r = Invoke-Alembic $Target 'heads'
$headsLines = @($r.Text -split "`r?`n" | Where-Object { $_.Contains('(head)') })
Assert-Gate (($headsLines.Count -ge 1) -and $headsLines[0].Trim().StartsWith('20260909_0057')) 'A1.2 repo head is 20260909_0057 (head)' '20260909_0057 (head)' ($headsLines -join ' / ')
& $Py -m alembic --version 2>&1 | ForEach-Object { Write-Host ("Alembic version: {0}" -f (ConvertTo-Text @($_))) }

Write-Section 'A2. THE 0057 FILE PIN (byte-still recital)'
$migLenActual = (Get-Item $MigFile).Length
$migShaActual = (Get-FileHash -Algorithm SHA256 $MigFile).Hash
Write-Host ("  length  {0} (pinned {1})" -f $migLenActual, $MigLen)
Write-Host ("  sha256  {0}" -f $migShaActual)
Assert-Gate ($migLenActual -eq $MigLen) 'A2.1 migration length' $MigLen ([string]$migLenActual)
Assert-Gate ($migShaActual -ieq $MigSha) 'A2.2 migration sha256' $MigSha $migShaActual

Write-Section 'A3. TATTOO PRE + NAMED-OBJECT PRE-LISTS'
Assert-Gate ((Invoke-Read $Target "SELECT COUNT(*) FROM sqlite_master WHERE type='trigger'") -eq '90') 'A3.1 triggers total == 90' '90' '(see above)'
Assert-Gate ((Invoke-Read $Target 'SELECT COUNT(*) FROM v2_permission') -eq '83') 'A3.2 v2_permission == 83' '83' '(see above)'
Assert-Gate ((Invoke-Read $Target 'SELECT COUNT(*) FROM v2_computation_version') -eq '16') 'A3.3 v2_computation_version == 16' '16' '(see above)'
$guardAll = ($GuardNamesAll | ForEach-Object { "'{0}'" -f $_ }) -join ','
$gpre = Invoke-Read $Target ("SELECT name FROM sqlite_master WHERE type='trigger' AND name IN ({0}) ORDER BY name" -f $guardAll)
Assert-Gate ($gpre -eq ($GuardNamesPre -join "`n")) 'A3.4 guard set pre == the twelve 12A/12B/12C/12D names (recon/incident pairs ABSENT)' ($GuardNamesPre -join ' / ') ($gpre -replace "`r?`n",' / ')
$lxePre = Invoke-Read $Target "SELECT component, version, source_hash, evidence_ref FROM v2_computation_version WHERE component='live_exec_engine' ORDER BY version"
Assert-Gate ($lxePre -eq $LxeRowsPre) 'A3.5 compver pre == ONLY lxe-1.0.0 + 1.1.0 + 1.2.0 (content-exact)' $LxeRowsPre $lxePre
$permIn = ($NewPerms | ForEach-Object { "'{0}'" -f $_ }) -join ','
Assert-Gate ((Invoke-Read $Target ("SELECT COUNT(*) FROM v2_permission WHERE permission IN ({0})" -f $permIn)) -eq '0') 'A3.6 the five 12E permission rows ABSENT pre-apply' '0' '(see above)'
Assert-Gate ((Invoke-Read $Target "SELECT COUNT(*) FROM sqlite_master WHERE type='table' AND name IN ('v2_live_exec_reconciliation','v2_live_exec_incident')") -eq '0') 'A3.7 both 12E tables ABSENT pre-apply' '0' '(see above)'
foreach ($zt in @('v2_live_exec_submission','v2_live_exec_fill_event','v2_live_exec_modify_event','v2_live_activation_instrument','v2_live_kill_switch')) {
  Assert-Gate ((Invoke-Read $Target ("SELECT COUNT(*) FROM {0}" -f $zt)) -eq '0') ("A3.8 standing posture: {0} at 0 rows" -f $zt) '0' '(see above)'
}
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
Assert-Gate ((Invoke-Read $Anchor 'SELECT version_num FROM alembic_version') -eq '20260909_0056') 'A4.5 anchor revision 20260909_0056' '20260909_0056' '(see above)'
$AnchorLen = (Get-Item $Anchor).Length
$AnchorSha = (Get-FileHash -Algorithm SHA256 $Anchor).Hash
Write-Host ("  anchor: {0}" -f $Anchor)
Write-Host ("  anchor size {0} sha256 {1}" -f $AnchorLen, $AnchorSha)

Write-Section 'A5. QUAD LXE PRE-COMPUTE GATES (halts precede any mutation)'
$lxe6 = Invoke-Lxe $Backend $CodeLxe6
Write-Host ("  6-file computed: {0}" -f $lxe6)
Assert-Gate ($lxe6 -eq $Lxe6Expect) 'A5a 12A/12B six-file lxe unmoved (b060f435...)' $Lxe6Expect $lxe6
$lxe8 = Invoke-Lxe $Backend $CodeLxe8
Write-Host ("  8-file computed: {0}" -f $lxe8)
Assert-Gate ($lxe8 -eq $Lxe8Expect) 'A5b 12C eight-file lxe unmoved (d09306f1...)' $Lxe8Expect $lxe8
$lxe13 = Invoke-Lxe $Backend $CodeLxe13
Write-Host (" 13-file computed: {0}" -f $lxe13)
Assert-Gate ($lxe13 -eq $Lxe13Expect) 'A5c 12D thirteen-file lxe byte-still through CR-1 (d25c4857...)' $Lxe13Expect $lxe13
$lxe18 = Invoke-Lxe $Backend $CodeLxe18
Write-Host (" 18-file computed: {0}" -f $lxe18)
Assert-Gate ($lxe18 -eq $Lxe18Expect) 'A5d 12E eighteen-file lxe landed EXACTLY at CR-1 bytes (93f436bc...)' $Lxe18Expect $lxe18

Write-Section 'A6. REHEARSAL UPGRADE (byte-copy only)'
Copy-Item $Target $Reh
$r = Invoke-Alembic $Reh 'upgrade 20260909_0057'
Assert-Gate ($r.Code -eq 0) 'A6.0 rehearsal upgrade exit 0' '0' ([string]$r.Code)
Assert-Gate ((Count-Hits $r.Text 'Running upgrade 20260909_0056 -> 20260909_0057') -eq 1) 'A6.1 exactly one Running upgrade line' '1' ([string](Count-Hits $r.Text 'Running upgrade 20260909_0056 -> 20260909_0057'))
Assert-NoBadTokens $r.Text 'A6.2 rehearsal console'
Assert-Gate ((Invoke-Read $Reh "SELECT COUNT(*) FROM sqlite_master WHERE type='trigger'") -eq '94') 'A6.3 rehearsal triggers 94' '94' '(see above)'
Assert-Gate ((Invoke-Read $Reh 'SELECT COUNT(*) FROM v2_permission') -eq '88') 'A6.4 rehearsal perms 88' '88' '(see above)'
Assert-Gate ((Invoke-Read $Reh 'SELECT COUNT(*) FROM v2_computation_version') -eq '17') 'A6.5 rehearsal compver 17' '17' '(see above)'
$lxeReh = Invoke-Read $Reh "SELECT component, version, source_hash, evidence_ref FROM v2_computation_version WHERE component='live_exec_engine' ORDER BY version"
Assert-Gate ($lxeReh -eq $LxeRowsPost) 'A6.6 rehearsal compver rows ALL FOUR stand, content-exact (1.3.0 == disk recompute on the copy too)' $LxeRowsPost $lxeReh
Assert-Gate ((Invoke-Read $Reh 'SELECT COUNT(*) FROM v2_live_exec_reconciliation') -eq '0') 'A6.7 rehearsal reconciliation ZERO ROWS (no seeds)' '0' '(see above)'
Assert-Gate ((Invoke-Read $Reh 'SELECT COUNT(*) FROM v2_live_exec_incident') -eq '0') 'A6.8 rehearsal incident ZERO ROWS (no seeds)' '0' '(see above)'

Write-Section 'A7. REHEARSAL DOWNGRADE PROOF (full reversibility, on the copy)'
$r = Invoke-Alembic $Reh 'downgrade 20260909_0056'
Assert-Gate ($r.Code -eq 0) 'A7.0 rehearsal downgrade exit 0' '0' ([string]$r.Code)
Assert-Gate ((Count-Hits $r.Text 'Running downgrade 20260909_0057 -> 20260909_0056') -eq 1) 'A7.1 exactly one Running downgrade line' '1' ([string](Count-Hits $r.Text 'Running downgrade 20260909_0057 -> 20260909_0056'))
Assert-NoBadTokens $r.Text 'A7.2 rehearsal console (incl. compver delete-guard dance silent)'
Assert-Gate ((Invoke-Read $Reh 'SELECT version_num FROM alembic_version') -eq '20260909_0056') 'A7.3 rehearsal revision restored 20260909_0056' '20260909_0056' '(see above)'
Assert-Gate ((Invoke-Read $Reh "SELECT COUNT(*) FROM sqlite_master WHERE type='trigger'") -eq '90') 'A7.4 rehearsal triggers restored 90' '90' '(see above)'
Assert-Gate ((Invoke-Read $Reh 'SELECT COUNT(*) FROM v2_permission') -eq '83') 'A7.5 rehearsal perms restored 83' '83' '(see above)'
Assert-Gate ((Invoke-Read $Reh 'SELECT COUNT(*) FROM v2_computation_version') -eq '16') 'A7.6 rehearsal compver restored 16' '16' '(see above)'
Assert-Gate ((Invoke-Read $Reh "SELECT COUNT(*) FROM sqlite_master WHERE type='table' AND name IN ('v2_live_exec_reconciliation','v2_live_exec_incident')") -eq '0') 'A7.7 rehearsal both tables removed' '0' '(see above)'
$lxeDown = Invoke-Read $Reh "SELECT component, version, source_hash, evidence_ref FROM v2_computation_version WHERE component='live_exec_engine' ORDER BY version"
Assert-Gate ($lxeDown -eq $LxeRowsPre) 'A7.8 rehearsal compver == 1.0.0 + 1.1.0 + 1.2.0 only (1.3.0 removed)' $LxeRowsPre $lxeDown
Write-Host 'NOTE (register-logged advisory, standing family): recreated compver DELETE guard carries the migration literal (versions vs version registry); invariant identical; visible only on a downgraded chain.'
$cvdReh = Invoke-Refuse $Reh "DELETE FROM v2_computation_version WHERE component='indicator_engine'"
Assert-Gate ($cvdReh -eq $CvdNewLiteral) 'A7.9 rehearsal recreated-guard refusal (documented literal)' $CvdNewLiteral $cvdReh

Write-Section 'A8. THE APPLY (single sanctioned mutation, fielded file)'
Write-Host ("Target: {0}" -f $Target)
$r = Invoke-Alembic $Target 'upgrade 20260909_0057'
Assert-Gate ($r.Code -eq 0) 'A8.0 apply exit 0' '0' ([string]$r.Code)
Assert-Gate ((Count-Hits $r.Text 'Running upgrade 20260909_0056 -> 20260909_0057') -eq 1) 'A8.1 exactly one Running upgrade line' '1' ([string](Count-Hits $r.Text 'Running upgrade 20260909_0056 -> 20260909_0057'))
Assert-NoBadTokens $r.Text 'A8.2 apply console'

Write-Section 'A9. FIELDED TERMINAL STATE'
$r = Invoke-Alembic $Target 'current'
$cur = Get-AlembicCurrent $r.Text
Assert-Gate ($cur -eq '20260909_0057 (head)') 'A9.1 stamped 20260909_0057 (head)' '20260909_0057 (head)' $cur
Assert-Gate ((Invoke-Read $Target "SELECT COUNT(*) FROM sqlite_master WHERE type='trigger'") -eq '94') 'A9.2 triggers 94' '94' '(see above)'
Assert-Gate ((Invoke-Read $Target 'SELECT COUNT(*) FROM v2_permission') -eq '88') 'A9.3 perms 88' '88' '(see above)'
Assert-Gate ((Invoke-Read $Target 'SELECT COUNT(*) FROM v2_computation_version') -eq '17') 'A9.4 compver 17' '17' '(see above)'
$gpost = Invoke-Read $Target ("SELECT name FROM sqlite_master WHERE type='trigger' AND name IN ({0}) ORDER BY name" -f $guardAll)
Assert-Gate ($gpost -eq ($GuardNamesAll -join "`n")) 'A9.5 sixteen guard names exact' ($GuardNamesAll -join ' / ') ($gpost -replace "`r?`n",' / ')
$idxRows = Invoke-Read $Target ("SELECT name FROM sqlite_master WHERE type='index' AND name IN ({0}) ORDER BY name" -f (($IndexNamesAll | ForEach-Object { "'{0}'" -f $_ }) -join ','))
$idxSet = @($idxRows -split "`r?`n" | Where-Object { $_.Trim() -ne '' })
Assert-Gate (Set-Equal $idxSet $IndexNamesAll) 'A9.6 ten indexes present exact' ($IndexNamesAll -join ' / ') ($idxRows -replace "`r?`n",' / ')
Assert-Gate ((Invoke-Read $Target ("SELECT COUNT(*) FROM sqlite_master WHERE type='table' AND name IN ({0})" -f (($ZeroTables | ForEach-Object { "'{0}'" -f $_ }) -join ','))) -eq '7') 'A9.7 all seven 12-series tables present' '7' '(see above)'
foreach ($zt in $ZeroTables) {
  Assert-Gate ((Invoke-Read $Target ("SELECT COUNT(*) FROM {0}" -f $zt)) -eq '0') ("A9.8 THE ELECTION: {0} at 0 rows" -f $zt) '0' '(see above)'
}
$permPost = Invoke-Read $Target ("SELECT role, permission, sal FROM v2_permission WHERE permission IN ({0}) ORDER BY permission" -f $permIn)
Assert-Gate ($permPost -eq $PermRowsExpect) 'A9.9 five 12E permission rows content-exact' $PermRowsExpect $permPost
$lxePost = Invoke-Read $Target "SELECT component, version, source_hash, evidence_ref FROM v2_computation_version WHERE component='live_exec_engine' ORDER BY version"
Assert-Gate ($lxePost -eq $LxeRowsPost) 'A9.10 compver rows ALL FOUR stand, content-exact (1.3.0 == disk; registry''s last row names the last build)' $LxeRowsPost $lxePost
$IntentCountPost = Invoke-Read $Target 'SELECT COUNT(*) FROM v2_live_exec_intent'
$IntentDigestsPost = Invoke-Read $Target 'SELECT digest FROM v2_live_exec_intent ORDER BY digest'
Assert-Gate ($IntentCountPost -eq $IntentCountPre) 'A9.11 12A intent ledger count unchanged' $IntentCountPre $IntentCountPost
Assert-Gate ($IntentDigestsPost -eq $IntentDigestsPre) 'A9.12 12A intent digests unchanged' $IntentDigestsPre $IntentDigestsPost
$lxe6Post = Invoke-Lxe $Backend $CodeLxe6
Assert-Gate ($lxe6Post -eq $Lxe6Expect) 'A9.13 disk 6-file lxe still b060f435...' $Lxe6Expect $lxe6Post
$lxe13Post = Invoke-Lxe $Backend $CodeLxe13
Assert-Gate ($lxe13Post -eq $Lxe13Expect) 'A9.14 disk 13-file lxe still d25c4857...' $Lxe13Expect $lxe13Post
$lxe18Post = Invoke-Lxe $Backend $CodeLxe18
Assert-Gate ($lxe18Post -eq $Lxe18Expect) 'A9.15 disk 18-file lxe still 93f436bc... (apply moves no source bytes)' $Lxe18Expect $lxe18Post
Write-Host 'A9.16 — the rendered CHECK names from the DB''s own DDL (E-0055-A10.3 record):'
Write-Host (Invoke-Read $Target "SELECT sql FROM sqlite_master WHERE type='table' AND name='v2_live_exec_reconciliation'")
Write-Host (Invoke-Read $Target "SELECT sql FROM sqlite_master WHERE type='table' AND name='v2_live_exec_incident'")

Write-Section 'A10. GUARD / CHECK REFUSALS (eleven; refused or rolled back; the election re-pinned after)'
$insRecon = "INSERT INTO v2_live_exec_reconciliation (id, scope, outcome, drift_facts, digest, actor_id, data_class, mode, operator_id, created_at) VALUES ('$ProbeId', '{""w"":""gp""}', 'clean', NULL, 'dd', 'gp', 'evidence', 'RESEARCH', 'itrga-gp', '2026-09-09 00:00:00')"
$gp = Invoke-GuardProbe $Target 'v2_live_exec_reconciliation' $insRecon "UPDATE v2_live_exec_reconciliation SET outcome='parity_break' WHERE id='$ProbeId'"
Write-Host ($gp -join "`n")
Assert-Gate (($gp.Count -eq 2) -and ($gp[0] -eq $ReconUpd) -and ($gp[1] -eq 'rolledback=1')) 'A10.1 reconciliation UPDATE refusal exact + rolled back (NO-VALVE law: no sanctioned transition exists)' $ReconUpd ($gp -join ' / ')
$gp = Invoke-GuardProbe $Target 'v2_live_exec_reconciliation' $insRecon "DELETE FROM v2_live_exec_reconciliation WHERE id='$ProbeId'"
Write-Host ($gp -join "`n")
Assert-Gate (($gp.Count -eq 2) -and ($gp[0] -eq $ReconDel) -and ($gp[1] -eq 'rolledback=1')) 'A10.2 reconciliation DELETE refusal exact + rolled back' $ReconDel ($gp -join ' / ')
$insInc = "INSERT INTO v2_live_exec_incident (id, opened_by, severity, instruments_pinned, recovery_path, status, closed_at, closed_by, digest, step_up_ref, actor_id, data_class, mode, operator_id, created_at) VALUES ('$ProbeId', 'gp', 'SEV-2', '[""forex.eurusd""]', 'manual review', 'open', NULL, NULL, 'dd', NULL, 'gp', 'evidence', 'RESEARCH', 'itrga-gp', '2026-09-09 00:00:00')"
$gp = Invoke-GuardProbe $Target 'v2_live_exec_incident' $insInc "UPDATE v2_live_exec_incident SET status='closed' WHERE id='$ProbeId'"
Write-Host ($gp -join "`n")
Assert-Gate (($gp.Count -eq 2) -and ($gp[0] -eq $IncUpd) -and ($gp[1] -eq 'rolledback=1')) 'A10.3 incident UPDATE refusal exact + rolled back (the valve stays sealed in the field; PLURAL message as delivered)' $IncUpd ($gp -join ' / ')
$gp = Invoke-GuardProbe $Target 'v2_live_exec_incident' $insInc "DELETE FROM v2_live_exec_incident WHERE id='$ProbeId'"
Write-Host ($gp -join "`n")
Assert-Gate (($gp.Count -eq 2) -and ($gp[0] -eq $IncDel) -and ($gp[1] -eq 'rolledback=1')) 'A10.4 incident DELETE refusal exact + rolled back' $IncDel ($gp -join ' / ')
$p = Invoke-Refuse $Target "INSERT INTO v2_live_exec_reconciliation (id, scope, outcome, drift_facts, digest, actor_id, data_class, mode, operator_id, created_at) VALUES ('$ProbeId', '{" + [char]34 + "w" + [char]34 + ":" + [char]34 + "gp" + [char]34 + "}', 'weird', NULL, 'dd', 'gp', 'evidence', 'RESEARCH', 'itrga-gp', '2026-09-09 00:00:00')"
Assert-Gate ($p -eq $CkLxreconOutcome) 'A10.5 reconciliation outcome CHECK refusal exact (rendered name)' $CkLxreconOutcome $p
$p = Invoke-Refuse $Target "INSERT INTO v2_live_exec_reconciliation (id, scope, outcome, drift_facts, digest, actor_id, data_class, mode, operator_id, created_at) VALUES ('$ProbeId', '{}', 'clean', NULL, 'dd', 'gp', 'simulated', 'RESEARCH', 'itrga-gp', '2026-09-09 00:00:00')"
Assert-Gate ($p -eq $CkLxreconClass) 'A10.6 reconciliation data_class CHECK refusal exact (evidence-only, rendered name)' $CkLxreconClass $p
$p = Invoke-Refuse $Target "INSERT INTO v2_live_exec_incident (id, opened_by, severity, instruments_pinned, recovery_path, status, digest, actor_id, data_class, mode, operator_id, created_at) VALUES ('$ProbeId', 'gp', 'SEV-9', '[]', 'x', 'open', 'dd', 'gp', 'evidence', 'RESEARCH', 'itrga-gp', '2026-09-09 00:00:00')"
Assert-Gate ($p -eq $CkLxincSeverity) 'A10.7 THE FIELD''S OWN SEV-9 ARM: severity CHECK refusal exact (the word that closed DEL-001, dying at schema on the fielded file)' $CkLxincSeverity $p
$p = Invoke-Refuse $Target "INSERT INTO v2_live_exec_incident (id, opened_by, severity, instruments_pinned, recovery_path, status, digest, actor_id, data_class, mode, operator_id, created_at) VALUES ('$ProbeId', 'gp', 'SEV-2', '[]', 'x', 'engaged', 'dd', 'gp', 'evidence', 'RESEARCH', 'itrga-gp', '2026-09-09 00:00:00')"
Assert-Gate ($p -eq $CkLxincStatus) 'A10.8 incident status CHECK refusal exact (open/closed only)' $CkLxincStatus $p
$p = Invoke-Refuse $Target "INSERT INTO v2_live_exec_incident (id, opened_by, severity, instruments_pinned, recovery_path, status, digest, actor_id, data_class, mode, operator_id, created_at) VALUES ('$ProbeId', 'gp', 'SEV-2', '[]', 'x', 'open', 'dd', 'gp', 'simulated', 'RESEARCH', 'itrga-gp', '2026-09-09 00:00:00')"
Assert-Gate ($p -eq $CkLxincClass) 'A10.9 incident data_class CHECK refusal exact (evidence-only, rendered name)' $CkLxincClass $p
$cvu = Invoke-Refuse $Target "UPDATE v2_computation_version SET version='probe' WHERE component='indicator_engine'"
Assert-Gate ($cvu -eq $CvuOld) 'A10.10 compver UPDATE refusal (ORIGINAL literal)' $CvuOld $cvu
$cvd = Invoke-Refuse $Target "DELETE FROM v2_computation_version WHERE component='indicator_engine'"
Assert-Gate ($cvd -eq $CvdOld) 'A10.11 compver DELETE refusal (ORIGINAL literal)' $CvdOld $cvd
foreach ($zt in $ZeroTables) {
  Assert-Gate ((Invoke-Read $Target ("SELECT COUNT(*) FROM {0}" -f $zt)) -eq '0') ("A10.12 THE ELECTION RE-PINNED: {0} at 0 rows after all probes" -f $zt) '0' '(see above)'
}

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
  ('POST_REVISION     20260909_0057'),
  ('POST_TRIGGERS     94'),
  ('POST_PERMISSIONS  88'),
  ('POST_COMPVER      17'),
  ('POST_SIZE_BYTES   {0}' -f $PostLen),
  ('POST_SHA256       {0}' -f $PostSha),
  ('LXE_COMPVER_1_0_0 b060f435c7c339fbe5e23daf8231af04bf62cd8cc43ccd7d8a5f5067b78bb8c2'),
  ('LXE_COMPVER_1_1_0 d09306f1ab32f0dc6f26e5c7235b3e1f72c3175a1928d60673709c0b02a3809a'),
  ('LXE_COMPVER_1_2_0 d25c48579def993b63e6f84ca17e937c3e938f75b0ca1f78f8aea81b1e9c1705'),
  ('LXE_COMPVER_1_3_0 93f436bc90f1a8826154717e7b310be531a86bb8cc968a5f05d2f7b9112cd1f3'),
  ('FIELD_LAW         seven 12-series tables at 0 rows BY ELECTION (before and after every probe; no engine verb ever ran; the fielded lineage holds no runtime evidence rows of any band)'),
  ('ANCHOR_FILENAME   {0}' -f (Split-Path $Anchor -Leaf)),
  ('ANCHOR_SIZE_BYTES {0}' -f $AnchorLen),
  ('ANCHOR_SHA256     {0}' -f $AnchorSha),
  ('REHEARSAL_COPY    {0} (retain until ITRGA acknowledges the witness; then delete)' -f (Split-Path $Reh -Leaf)),
  'VERDICT           PASS'
)
$postFacts | Set-Content -Path $FinalStatePath -Encoding ascii
Write-Host ("post-apply size {0} sha256 {1}" -f $PostLen, $PostSha)
Write-Host ''
Write-Host "APPLY VERDICT: PASS - migration 20260909_0057_v2_be12e_reconciliation_incident applied ONCE to '$Target'."
Write-Host 'Terminal state: revision 20260909_0057; tattoo 94/88/17; reconciliation + incident present with guard pairs and closed CHECKs, all seven 12-series tables ZERO ROWS by election (before/after every probe); five 12E permission rows content-exact; compver ALL FOUR rows standing (1.0.0/1.1.0/1.2.0 untouched, disk-re-proving; 1.3.0 == disk 93f436bc..., the registry''s last row naming the last build); eleven guard/CHECK refusals exact under RENDERED names (incl. the field''s own SEV-9 arm); 12A ledger untouched; disk hashes 6/8/13/18-file re-proven; integrity ok; drift itemized; no TD/PRACTICE variable; no engine verb ran anywhere.'
Write-Host ("Transcript: {0}" -f $TranscriptPath)
Write-Host ("State record: {0}" -f $FinalStatePath)
Write-Host 'NEXT: restart the application when ready. Send transcript + state record to ITRGA. The FIELDED verdict and register line are issued on receipt; FIELDED then frees the DR-5 closeout verdict — the ladder''s last act.'

} finally {
  Remove-Item Env:AXIOM_DATABASE_URL -ErrorAction SilentlyContinue
  if ($script:TranscriptOn) { try { Stop-Transcript | Out-Null } catch { } }
}
