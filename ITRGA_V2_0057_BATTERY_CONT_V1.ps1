<#
===============================================================================
ITRGA_V2_0057_BATTERY_CONT_V1.ps1
===============================================================================
Pack:      ITRGA-V2-0057-BATTERY-CONT-V1  (RESUME WINDOW of card 0057)
Act:       discharge the UNWITNESSED RESIDUE of card 0057 (parent-card gates
           A10.5 - A12) after the lawful apparatus halt of run V1 at A10.5.
           NO ALEMBIC VERB RUNS ('current'/'check' are read-only inspections).
           NO MUTATION of any kind beyond refused-or-rolled-back probe writes.
           The single sanctioned mutation completed in run V1 (A8 PASSED; the
           terminal state was pinned at A9.1-A9.16 BEFORE the halt).
Implements: ITRGA-V2-0057-BATTERY-CONT-CARD-20260909 (governing text).
Authority: BO-V2-BE12E-001 SS1.g | ITRGA-REV-V2-BE12E-001 (base) |
           ITRGA-REV-V2-BE12E-CR-001 (CR-1 APPROVED; BE-12E ACCEPTED;
           suite floor 1,311) | ITRGA-V2-0057-FIELD-APPLY-CARD-20260909 |
           ITRGA ERRATUM E-0057-A10.5 (this pack is its discharge witness).
CUMULATIVE-WITNESS RULE (card SS-B): card 0057 gates stand witnessed across
           V1 (A0 - A9.16, A10.1 - A10.4, on file) + this continuation
           (B1 non-drift entry panel; B2.1-B2.7 == A10.5-A10.11; B3 == A10.12;
           B4 == A11; B5 == A12). NO GATE IS EVER RE-RUN.
DQUOTE-FREE PROBE LAW (E-0057-A10.5 SS3.1): every probe SQL below contains
           ZERO 0x22 bytes; JSON neighbor columns carry '{}' / '[]'; each
           probe's semantic payload is the violated value alone. A PARSER-class
           refusal ("unrecognized token", "syntax error") voids the probe as
           witness (E-0057-A10.5 SS3.2): the named CHECK is then unwitnessed;
           halt and send the transcript; fix nothing.
FIELD LAW (unchanged): the 0057 tables are EVIDENCE LEDGERS - this act pins
           ZERO-ROW BY ELECTION at entry and exit, on ALL SEVEN 12-series
           tables; NO ENGINE VERB runs (no reconcile run, no incident
           open/close; no governor verb; no force act). "The fielded lineage
           holds no runtime evidence rows of any band." Posture, not doctrine.
Method:    NO python FILES of any kind (-c snippets only). NO git operations.
           NO credential of any kind. AXIOM_BROKER_PRACTICE_* / AXIOM_TD_*
           asserted ABSENT at start and end.
Errata:    rendered CHECK names pinned (E-0055-A10.3); drift gate itemized
           (E-0054-A11.4); DQUOTE-free probe law (E-0057-A10.5).
Run:       Set-Location C:\Users\victo\.vscode\AXIOM\axiom
           powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\ITRGA_V2_0057_BATTERY_CONT_V1.ps1
Output:    operator-evidence\BE-12E\0057-BATTERY-CONT-RUN-V1-<timestamp>.txt (transcript)
           operator-evidence\BE-12E\0057-APPLY-FINAL-STATE.txt              (state record)
On any gate failure: HALT at the failing gate; no retry. If a B1 entry gate
fails, the fielded file drifted since the halt - that IS the finding; send the
transcript; restore nothing on your own authority. The original V1 anchor is
the only restoration path and only under ITRGA instruction.
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
$Lxe13Expect   = 'd25c48579def993b63e6f84ca17e937c3e938f75b0ca1f78f8aea81b1e9c1705'
$Lxe18Expect   = '93f436bc90f1a8826154717e7b310be531a86bb8cc968a5f05d2f7b9112cd1f3'
$LxeRow100     = 'live_exec_engine|lxe-1.0.0|b060f435c7c339fbe5e23daf8231af04bf62cd8cc43ccd7d8a5f5067b78bb8c2|BO-V2-BE12B-001'
$LxeRow110     = 'live_exec_engine|lxe-1.1.0|d09306f1ab32f0dc6f26e5c7235b3e1f72c3175a1928d60673709c0b02a3809a|BO-V2-BE12C-001'
$LxeRow120     = 'live_exec_engine|lxe-1.2.0|d25c48579def993b63e6f84ca17e937c3e938f75b0ca1f78f8aea81b1e9c1705|BO-V2-BE12D-001'
$LxeRow130     = 'live_exec_engine|lxe-1.3.0|93f436bc90f1a8826154717e7b310be531a86bb8cc968a5f05d2f7b9112cd1f3|BO-V2-BE12E-001'
$LxeRowsPost   = $LxeRow100 + "`n" + $LxeRow110 + "`n" + $LxeRow120 + "`n" + $LxeRow130
$PermRowsExpect= @(
  'admin|v2.live_exec.incident.close|SAL-4',
  'admin|v2.live_exec.incident.open|SAL-4',
  'admin|v2.live_exec.incident.read|SAL-2',
  'admin|v2.live_exec.reconcile.read|SAL-2',
  'admin|v2.live_exec.reconcile.run|SAL-4'
) -join "`n"
$PermIn        = "'v2.live_exec.incident.close','v2.live_exec.incident.open','v2.live_exec.incident.read','v2.live_exec.reconcile.read','v2.live_exec.reconcile.run'"
$GuardNamesAll = @('v2_live_activation_instrument_immutable_delete','v2_live_activation_instrument_immutable_update','v2_live_exec_fill_event_immutable_delete','v2_live_exec_fill_event_immutable_update','v2_live_exec_incident_immutable_delete','v2_live_exec_incident_immutable_update','v2_live_exec_intent_immutable_delete','v2_live_exec_intent_immutable_update','v2_live_exec_modify_event_immutable_delete','v2_live_exec_modify_event_immutable_update','v2_live_exec_reconciliation_immutable_delete','v2_live_exec_reconciliation_immutable_update','v2_live_exec_submission_immutable_delete','v2_live_exec_submission_immutable_update','v2_live_kill_switch_immutable_delete','v2_live_kill_switch_immutable_update')
$GuardAll      = ($GuardNamesAll | ForEach-Object { "'{0}'" -f $_ }) -join ','
$IndexNamesAll = @('ix_v2_lxfill_created','ix_v2_lxinc_created','ix_v2_lxmod_created','ix_v2_lxrecon_created','ix_v2_lxsub_created','uq_v2_lai_sole','uq_v2_lks_sole','uq_v2_lxfill_identity','uq_v2_lxmod_identity','uq_v2_lxsub_intent')
$ZeroTables    = @('v2_live_exec_submission','v2_live_exec_fill_event','v2_live_exec_modify_event','v2_live_activation_instrument','v2_live_kill_switch','v2_live_exec_reconciliation','v2_live_exec_incident')
$CvuOld        = 'REFUSED:V2 computation version registry is immutable; UPDATE prohibited'
$CvdOld        = 'REFUSED:V2 computation version registry is immutable; DELETE prohibited'
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

# --- V1-transcript fielded constants (entry non-drift assertions; card SS-D) ---
$V1IntentCount  = '1'
$V1IntentDigest = '7ac49b2873c332439958604f611c19609377db261d73124534743a271e13e618'
$AnchorName     = 'axiom_dev.db.pre-0057-20260909212101.bak'
$AnchorLenExpect= 2670592
$AnchorShaExpect= 'DC0FAA2429AF6510C4E77B4DE056661842D71C0D9AF9948A933F7584DF651CCC'
$RehName        = 'axiom_dev.db.rehearsal-0057-20260909212101.db'
$Anchor         = Join-Path $EvDir $AnchorName

$ts             = Get-Date -Format yyyyMMddHHmmss
$TranscriptPath = Join-Path $EvDir ("0057-BATTERY-CONT-RUN-V1-{0}.txt" -f $ts)
$FinalStatePath = Join-Path $EvDir '0057-APPLY-FINAL-STATE.txt'

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
  Write-Host ("Original V1 anchor (pre-image of the completed apply): {0}" -f $Anchor)
  Write-Host 'Restoration (if ITRGA instructs) is via that anchor only.'
  Write-Host 'If a B1 entry gate failed, the fielded file drifted since the halt - that IS the finding.'
  Write-Host 'Send this transcript to ITRGA.'
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

# ------------------------------------------------------------------- B0/BEGIN
New-Item -ItemType Directory -Force $EvDir | Out-Null
$script:TranscriptOn = $true
Start-Transcript -Path $TranscriptPath | Out-Null

try {

Write-Section 'B0. RUN IDENTIFICATION (RESUME WINDOW of card 0057)'
Write-Host 'Pack: ITRGA-V2-0057-BATTERY-CONT-V1'
Write-Host 'Act: discharge of the unwitnessed residue (parent-card gates A10.5-A12); NO alembic verb; probes refused/rolled back only.'
Write-Host 'Implements: ITRGA-V2-0057-BATTERY-CONT-CARD-20260909 (governing text)'
Write-Host 'Authority: BO-V2-BE12E-001 SS1.g / REV-V2-BE12E-001 + REV-V2-BE12E-CR-001 (APPROVED) / ERRATUM E-0057-A10.5'
Write-Host ("Started: {0}" -f (Get-Date -Format 'yyyy-MM-dd HH:mm:ss zzz'))
Write-Host ("Target file: {0}" -f $Target)
Write-Host 'Prior witness on file: V1 run transcript of 2026-09-09T21:21:01+03:00 (A0-A9.16, A10.1-A10.4 WITNESSED; A10.5 void as witness; apply lawful+complete).'
Write-Host 'FIELD LAW: evidence ledgers - zero-row BY ELECTION on all seven 12-series tables; NO engine verb runs (no reconcile run, no incident open/close; no governor verb; no force).'
Write-Host 'Server credentials used: NONE. Provider credentials used: NONE.'
Write-Host ''
Write-Host 'STOP THE RUNNING APPLICATION. Continuing in 5 seconds; press Ctrl+C otherwise...'
Start-Sleep -Seconds 5

Write-Section 'B0b. AUTHORITY/PRACTICE ENVIRONMENT SWEEP (must print nothing)'
$sweep = @(Get-ChildItem env: | Where-Object { $_.Name -match '^AXIOM_(TD|BROKER_PRACTICE)' })
Assert-Gate ($sweep.Count -eq 0) 'B0b: no AXIOM_TD_* / AXIOM_BROKER_PRACTICE_* variables' 'absent' (($sweep | ForEach-Object { $_.Name }) -join ', ')

Write-Section 'B0c. FILE EXISTENCE (incl. the original V1 anchor)'
Assert-Gate (Test-Path $Py)      'B0c.1 venv python present' $Py '(missing)'
Assert-Gate (Test-Path $Target)  'B0c.2 target db present'   $Target '(missing)'
Assert-Gate (Test-Path $MigFile) 'B0c.3 migration 0057 present' $MigFile '(missing)'
Assert-Gate (Test-Path $Anchor)  'B0c.4 original V1 anchor present (restoration path, untouched)' $AnchorName '(missing)'

Write-Section 'B1. TERMINAL-STATE NON-DRIFT ENTRY PANEL (V1 constants asserted before ANY probe)'
$migLenNow = (Get-Item $MigFile).Length
$migShaNow = (Get-FileHash -Algorithm SHA256 $MigFile).Hash
Assert-Gate ($migLenNow -eq $MigLen)  'B1.0a migration 0057 byte length unchanged' $MigLen $migLenNow
Assert-Gate ($migShaNow -eq $MigSha)  'B1.0b migration 0057 sha256 unchanged (the A2 byte-still recital, standing)' $MigSha $migShaNow
$r = Invoke-Alembic $Target 'current'
$cur = Get-AlembicCurrent $r.Text
Assert-Gate ($cur -eq '20260909_0057 (head)') 'B1.1 fielded head still 20260909_0057 (head)' '20260909_0057 (head)' $cur
Assert-Gate ((Invoke-Read $Target "SELECT COUNT(*) FROM sqlite_master WHERE type='trigger'") -eq '94') 'B1.2 triggers 94' '94' '(see above)'
Assert-Gate ((Invoke-Read $Target 'SELECT COUNT(*) FROM v2_permission') -eq '88') 'B1.3 perms 88' '88' '(see above)'
Assert-Gate ((Invoke-Read $Target 'SELECT COUNT(*) FROM v2_computation_version') -eq '17') 'B1.4 compver 17' '17' '(see above)'
$gNow = Invoke-Read $Target ("SELECT name FROM sqlite_master WHERE type='trigger' AND name IN ({0}) ORDER BY name" -f $GuardAll)
Assert-Gate ($gNow -eq ($GuardNamesAll -join "`n")) 'B1.5 sixteen guard names exact' ($GuardNamesAll -join ' / ') ($gNow -replace "`r?`n",' / ')
$idxRows = Invoke-Read $Target ("SELECT name FROM sqlite_master WHERE type='index' AND name IN ({0}) ORDER BY name" -f (($IndexNamesAll | ForEach-Object { "'{0}'" -f $_ }) -join ','))
$idxSet = @($idxRows -split "`r?`n" | Where-Object { $_.Trim() -ne '' })
Assert-Gate (Set-Equal $idxSet $IndexNamesAll) 'B1.6 ten indexes present exact' ($IndexNamesAll -join ' / ') ($idxRows -replace "`r?`n",' / ')
Assert-Gate ((Invoke-Read $Target ("SELECT COUNT(*) FROM sqlite_master WHERE type='table' AND name IN ({0})" -f (($ZeroTables | ForEach-Object { "'{0}'" -f $_ }) -join ','))) -eq '7') 'B1.7 all seven 12-series tables present' '7' '(see above)'
foreach ($zt in $ZeroTables) {
  Assert-Gate ((Invoke-Read $Target ("SELECT COUNT(*) FROM {0}" -f $zt)) -eq '0') ("B1.8 THE ELECTION AT ENTRY: {0} at 0 rows before any probe" -f $zt) '0' '(see above)'
}
$permNow = Invoke-Read $Target ("SELECT role, permission, sal FROM v2_permission WHERE permission IN ({0}) ORDER BY permission" -f $PermIn)
Assert-Gate ($permNow -eq $PermRowsExpect) 'B1.9 five 12E permission rows content-exact' $PermRowsExpect $permNow
$lxeNow = Invoke-Read $Target "SELECT component, version, source_hash, evidence_ref FROM v2_computation_version WHERE component='live_exec_engine' ORDER BY version"
Assert-Gate ($lxeNow -eq $LxeRowsPost) 'B1.10 compver ALL FOUR rows stand content-exact (1.3.0 == disk; registry''s last row names the last build)' $LxeRowsPost $lxeNow
$icNow = Invoke-Read $Target 'SELECT COUNT(*) FROM v2_live_exec_intent'
Assert-Gate ($icNow -eq $V1IntentCount) 'B1.11 12A intent ledger count == V1 witness' $V1IntentCount $icNow
$idNow = Invoke-Read $Target 'SELECT digest FROM v2_live_exec_intent ORDER BY digest'
Assert-Gate ($idNow -eq $V1IntentDigest) 'B1.12 12A intent digest == V1 witness' $V1IntentDigest $idNow
$lxe6Now = Invoke-Lxe $Backend $CodeLxe6
Assert-Gate ($lxe6Now -eq $Lxe6Expect) 'B1.13 disk 6-file lxe b060f435... (12A/12B bytes still unmoved)' $Lxe6Expect $lxe6Now
$lxe13Now = Invoke-Lxe $Backend $CodeLxe13
Assert-Gate ($lxe13Now -eq $Lxe13Expect) 'B1.14 disk 13-file lxe d25c4857... (12D byte-still through CR-1)' $Lxe13Expect $lxe13Now
$lxe18Now = Invoke-Lxe $Backend $CodeLxe18
Assert-Gate ($lxe18Now -eq $Lxe18Expect) 'B1.15 disk 18-file lxe 93f436bc... (CR-1 final bytes; apply moved none)' $Lxe18Expect $lxe18Now
$AnchorLen = (Get-Item $Anchor).Length
$AnchorSha = (Get-FileHash -Algorithm SHA256 $Anchor).Hash
Assert-Gate ($AnchorLen -eq $AnchorLenExpect) 'B1.16 anchor size == V1 witness (2670592; byte-identical to the 0056 post-image: chain continuity)' $AnchorLenExpect $AnchorLen
Assert-Gate ($AnchorSha -eq $AnchorShaExpect) 'B1.17 anchor sha256 == V1 witness' $AnchorShaExpect $AnchorSha

Write-Section 'B2. THE SEVEN UNWITNESSED REFUSALS (DQUOTE-free probe law; each refusal exact, render-named)'
Write-Host 'B2 == parent-card A10.5-A10.11. Every write refused or rolled back by engine construction (BEGIN/ROLLBACK).'
$p = Invoke-Refuse $Target "INSERT INTO v2_live_exec_reconciliation (id, scope, outcome, drift_facts, digest, actor_id, data_class, mode, operator_id, created_at) VALUES ('$ProbeId', '{}', 'weird', NULL, 'dd', 'gp', 'evidence', 'RESEARCH', 'itrga-gp', '2026-09-09 00:00:00')"
Assert-Gate ($p -eq $CkLxreconOutcome) 'B2.1 reconciliation outcome CHECK refusal exact (rendered name) [A10.5]' $CkLxreconOutcome $p
$p = Invoke-Refuse $Target "INSERT INTO v2_live_exec_reconciliation (id, scope, outcome, drift_facts, digest, actor_id, data_class, mode, operator_id, created_at) VALUES ('$ProbeId', '{}', 'clean', NULL, 'dd', 'gp', 'simulated', 'RESEARCH', 'itrga-gp', '2026-09-09 00:00:00')"
Assert-Gate ($p -eq $CkLxreconClass) 'B2.2 reconciliation data_class CHECK refusal exact (evidence-only, rendered name) [A10.6]' $CkLxreconClass $p
$p = Invoke-Refuse $Target "INSERT INTO v2_live_exec_incident (id, opened_by, severity, instruments_pinned, recovery_path, status, digest, actor_id, data_class, mode, operator_id, created_at) VALUES ('$ProbeId', 'gp', 'SEV-9', '[]', 'x', 'open', 'dd', 'gp', 'evidence', 'RESEARCH', 'itrga-gp', '2026-09-09 00:00:00')"
Assert-Gate ($p -eq $CkLxincSeverity) 'B2.3 THE FIELD''S OWN SEV-9 ARM: severity CHECK refusal exact (the word that closed DEL-001, dying at schema on the fielded file) [A10.7]' $CkLxincSeverity $p
$p = Invoke-Refuse $Target "INSERT INTO v2_live_exec_incident (id, opened_by, severity, instruments_pinned, recovery_path, status, digest, actor_id, data_class, mode, operator_id, created_at) VALUES ('$ProbeId', 'gp', 'SEV-2', '[]', 'x', 'engaged', 'dd', 'gp', 'evidence', 'RESEARCH', 'itrga-gp', '2026-09-09 00:00:00')"
Assert-Gate ($p -eq $CkLxincStatus) 'B2.4 incident status CHECK refusal exact (open/closed only, rendered name) [A10.8]' $CkLxincStatus $p
$p = Invoke-Refuse $Target "INSERT INTO v2_live_exec_incident (id, opened_by, severity, instruments_pinned, recovery_path, status, digest, actor_id, data_class, mode, operator_id, created_at) VALUES ('$ProbeId', 'gp', 'SEV-2', '[]', 'x', 'open', 'dd', 'gp', 'simulated', 'RESEARCH', 'itrga-gp', '2026-09-09 00:00:00')"
Assert-Gate ($p -eq $CkLxincClass) 'B2.5 incident data_class CHECK refusal exact (evidence-only, rendered name) [A10.9]' $CkLxincClass $p
$cvu = Invoke-Refuse $Target "UPDATE v2_computation_version SET version='probe' WHERE component='indicator_engine'"
Assert-Gate ($cvu -eq $CvuOld) 'B2.6 compver UPDATE refusal (ORIGINAL literal) [A10.10]' $CvuOld $cvu
$cvd = Invoke-Refuse $Target "DELETE FROM v2_computation_version WHERE component='indicator_engine'"
Assert-Gate ($cvd -eq $CvdOld) 'B2.7 compver DELETE refusal (ORIGINAL literal) [A10.11]' $CvdOld $cvd

Write-Section 'B3. THE ELECTION RE-PINNED (after all probes) [A10.12]'
foreach ($zt in $ZeroTables) {
  Assert-Gate ((Invoke-Read $Target ("SELECT COUNT(*) FROM {0}" -f $zt)) -eq '0') ("B3 THE ELECTION RE-PINNED: {0} at 0 rows after all probes" -f $zt) '0' '(see above)'
}

Write-Section 'B4. HEALTH POST + DRIFT (ITEMIZED LAW) + ENVIRONMENT CLOSE [A11]'
Assert-Gate ((Invoke-Read $Target 'PRAGMA integrity_check') -eq 'ok') 'B4.1 integrity ok' 'ok' '(see above)'
Assert-Gate ((Invoke-Read $Target 'PRAGMA journal_mode') -eq 'delete') 'B4.2 journal delete' 'delete' '(see above)'
Assert-Gate ((-not (Test-Path ($Target + '-wal'))) -and (-not (Test-Path ($Target + '-shm')))) 'B4.3 no sidecars' 'absent' 'present'
Write-Host 'Drift law (ITEMIZED, E-0054-A11.4): exactly the 9 inherited V1 tokens; band tokens absent; silence is a pass-subset.'
$r = Invoke-Alembic $Target 'check'
foreach ($tok in $DriftForbidden) {
  Assert-Gate (-not ($r.Text -imatch [regex]::Escape($tok))) ("B4.4 drift: band token '{0}' absent" -f $tok) 'absent' 'present'
}
$opLines = @($r.Text -split "`r?`n" | Where-Object { $_ -imatch 'add_(table|index)|remove_index|removed (table|index)' })
$bad = @()
foreach ($ln in $opLines) {
  $hit = $false
  foreach ($w in $DriftWhitelist) { if ($ln -imatch [regex]::Escape($w)) { $hit = $true; break } }
  if (-not $hit) { $bad += $ln }
}
Assert-Gate ($bad.Count -eq 0) 'B4.5 drift: every detected operation names an inherited V1 token (9-item whitelist)' 'only the 9 inherited V1 tokens' ($bad -join ' / ')
Write-Host ("  drift operations witnessed (itemized): {0}" -f $opLines.Count)
$sweep = @(Get-ChildItem env: | Where-Object { $_.Name -match '^AXIOM_(TD|BROKER_PRACTICE)' })
Assert-Gate ($sweep.Count -eq 0) 'B4.6 environment close: still no TD/PRACTICE variables' 'absent' (($sweep | ForEach-Object { $_.Name }) -join ', ')

Write-Section 'B5. FINAL APPLY VERDICT + STATE RECORD [A12; cumulative-witness rule recorded]'
$PostLen = (Get-Item $Target).Length
$PostSha = (Get-FileHash -Algorithm SHA256 $Target).Hash
$postFacts = @(
  ('RUN_TIMESTAMP     {0}' -f (Get-Date -Format 'yyyy-MM-dd HH:mm:ss zzz')),
  ('WITNESS_RULE      CUMULATIVE: run V1 (A0-A9.16, A10.1-A10.4; 2026-09-09T21:21:01+03:00) + this continuation (B1-B5 == card gates A10.5-A12); no gate re-run'),
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
  ('FIELD_LAW         seven 12-series tables at 0 rows BY ELECTION (entry and after every probe; no engine verb ever ran; the fielded lineage holds no runtime evidence rows of any band)'),
  ('ANCHOR_FILENAME   {0}' -f $AnchorName),
  ('ANCHOR_SIZE_BYTES {0}' -f $AnchorLen),
  ('ANCHOR_SHA256     {0}' -f $AnchorSha),
  ('REHEARSAL_COPY    {0} (retain until ITRGA acknowledges the witness; then delete)' -f $RehName),
  'VERDICT           PASS'
)
$postFacts | Set-Content -Path $FinalStatePath -Encoding ascii
Write-Host ("post-apply size {0} sha256 {1}" -f $PostLen, $PostSha)
Write-Host ''
Write-Host "APPLY VERDICT: PASS - migration 20260909_0057_v2_be12e_reconciliation_incident applied ONCE to '$Target' (run V1, A8 WITNESSED); unwitnessed residue discharged by this continuation."
Write-Host 'Terminal state: revision 20260909_0057; tattoo 94/88/17; reconciliation + incident present with guard pairs and closed CHECKs, all seven 12-series tables ZERO ROWS by election (entry + after every probe); five 12E permission rows content-exact; compver ALL FOUR rows standing (1.0.0/1.1.0/1.2.0 untouched, disk-re-proving; 1.3.0 == disk 93f436bc..., the registry''s last row naming the last build); eleven guard/CHECK refusals exact under RENDERED names across V1 + this pack (incl. the field''s own SEV-9 arm, refused as B2.3); 12A ledger unchanged; disk hashes 6/13/18-file re-proven; integrity ok; drift itemized; no TD/PRACTICE variable; no engine verb ran anywhere.'
Write-Host ("Transcript: {0}" -f $TranscriptPath)
Write-Host ("State record: {0}" -f $FinalStatePath)
Write-Host 'NEXT: restart the application when ready. Send THIS transcript + the state record to ITRGA (the V1 witness is already on file). The FIELDED verdict and register line are issued on receipt; FIELDED then frees the DR-5 closeout verdict - the ladder''s last act.'

} finally {
  Remove-Item Env:AXIOM_DATABASE_URL -ErrorAction SilentlyContinue
  if ($script:TranscriptOn) { try { Stop-Transcript | Out-Null } catch { } }
}
