<#
===============================================================================
ITRGA_V2_BE12_LOCKREFUSAL_400PIN_V5.ps1
===============================================================================
Pack:      ITRGA-V2-BE12-LOCKREFUSAL-400PIN-V5  (the ladder's TRUE LAST field act)
V5 NOTE:   V4 died at C2 on ERRATUM E-400PIN-C4 (token selected by a FLAT
           CONVENTION hypothesis - access_token then token - against the fielded
           LoginResponse: body.tokens.access_token, NESTED, response_model-enforced;
           the door answered 200+JSON with NO flat key; child died after ONE
           read-only login POST, before any arm POST; ZERO mutation, fourth
           straight; tripwire law HELD). E-400PIN-C3(+addendum) DISCHARGED BY
           THE V4 WITNESS (doc door proof-selected; both mount families and
           census exact; namespaced login door answered 200). Law now: EVERY
           door schema is pinned from the fielded source-of-record
           (response_model / model classes / envelope builders); every pin
           NAMES ITS SOURCE; absence diagnostics print key NAMES ONLY, values
           redacted, and must make the next death terminal.
           V1/V2/V3/V4 MUST NOT BE RE-RUN.
V4 NOTE:   V3 died at C2 on E-400PIN-C3 ADDENDUM SS5.1 (uniqueness pin met a
           DOUBLE-MOUNTED surface: auth + live-exec families exist at both
           root and /api/v1 prefixes; selection law completed: pinned presence,
           preferred namespace, never uniqueness) and SS5.2 (counting laws
           NAMED: 21 PATHS == 22 OPERATIONS per mount; mounts=2 => 42 total).
           V1/V2/V3 MUST NOT BE RE-RUN.
V3 NOTE:   V2 died at C2 on ERRATUM E-400PIN-C3 (doc door HARDCODED
           /api/v1/openapi.json instead of proof-enumerated; FastAPI serves
           the doc at root; unrouted path hit the SPA catch-all answering
           HTML; child died at a GET; ZERO mutation; tripwire law HELD -
           stdout-tagged PYERROR + halt banner fired). Law now: the doc door
           is ENUMERATED by candidate list + proof (200 + JSON-of-paths).
           V2 NOTE: V1/V2 MUST NOT BE RE-RUN (0054 precedent).
V2 NOTE:   V1 died at C2 on ERRATUM E-400PIN-C2 (starlette import wrote to
           stderr; PS5.1 + EAP=Stop turns native stderr into a terminating
           NativeCommandError that bypasses Assert-Gate). ZERO mutation (C1
           re-pins fired complete; the arm commits nothing; door-drives never
           started). Law enforced in THIS pack: engines audited stderr-silent;
           stdout-tagged PYERROR; PYTHONWARNINGS=ignore child-scoped plus
           logging.disable(CRITICAL) before app construction; cmd-wrap remains
           FORBIDDEN for %-bearing engines; PYTHONWARNINGS joins the sweeps.
           V1 MUST NOT BE RE-RUN (0054 precedent: corrected pack ships as V2).
Act:       closeout addendum battery - witness L1/L2/L4/L6 refusing on the
           fielded lineage (+ L1-order + L5-typing order-fixtures, evidence-only).
           NOTHING LANDS: surface arms commit nothing; door-drives always
           ROLLBACK; re-pins prove the lineage identical before and after.
Implements: ITRGA-V2-BE12-CLOSEOUT-ADDENDUM-CARD-0001 (governing text).
Authority: BO-V2-BE12E-001 closeout condition (i) | ITRGA_VERDICT_V2_BE12_DR5_GATE_001
           (SS4 fixed arm shapes) | DR-2 lock-stack | DR-F1 AM-2
           (REGISTERED_LOCKED_MODES = ('LIVE',)) | credential law (N-O18: file-fed).
Contract pins (card SS0): live door hardcodes credential_class=None; L2 window
           DISCHARGED BY CONSTRUCTION; injected class = sub_signing_failure
           (12D corpus L3296); passing eligibility shape = the suite's own
           _ELIGIBLE; evaluate door carries _actuation_door (register door NOT
           used - register COMMITS, nothing-lands law forbids it).
Transport: NO python FILES (-c snippets only); argv payloads carry ZERO 0x22
           bytes (E-0057-A10.5 DQUOTE-FREE law, extended class-wide: every
           python -c engine below is single-quote-disciplined).
Run:       Set-Location C:\Users\victo\.vscode\AXIOM\axiom
           powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\ITRGA_V2_BE12_LOCKREFUSAL_400PIN_V5.ps1
Output:    operator-evidence\BE-12E\BE12-400PIN-RUN-<timestamp>.txt (transcript)
           operator-evidence\BE-12E\BE12-400PIN-WITNESS.txt        (arm record)
On any gate failure: HALT at the failing arm; send the transcript; nothing is
re-run, nothing hand-fixed. The failure mode of this battery is "the app
refused to testify" - never "the file moved" (C1/C5 re-pins prove it).
===============================================================================
#>

$ErrorActionPreference = 'Stop'
Set-Location C:\Users\victo\.vscode\AXIOM\axiom

# ---------------------------------------------------------------- constants --
$RepoRoot   = 'C:\Users\victo\.vscode\AXIOM\axiom'
$Backend    = 'C:\Users\victo\.vscode\AXIOM\axiom\backend'
$Py         = 'C:\Users\victo\.vscode\AXIOM\axiom\.venv\Scripts\python.exe'
$Target     = 'C:\Users\victo\.vscode\AXIOM\axiom\backend\axiom_dev.db'
$EvDir      = 'C:\Users\victo\.vscode\AXIOM\axiom\operator-evidence\BE-12E'
$PwFile     = 'C:\Users\victo\axiom_admin_pw.txt'
$Lxe18Expect= '93f436bc90f1a8826154717e7b310be531a86bb8cc968a5f05d2f7b9112cd1f3'
$ZeroTables = @('v2_live_exec_submission','v2_live_exec_fill_event','v2_live_exec_modify_event','v2_live_activation_instrument','v2_live_kill_switch','v2_live_exec_reconciliation','v2_live_exec_incident')
$ArmId      = '__closeoutArm__'
$Route21    = 'activation+activation/template+evaluate+fills+incident/open+incident/{incident_id}+incident/{incident_id}/close+incidents+intents+intents/{intent_id}/submit+killswitch+killswitch/arm+killswitch/clear+killswitch/pull+modifies+reconcile/latest+reconcile/run+reconcile/{reconciliation_id}+submissions+submissions/{submission_id}/cancel+submissions/{submission_id}/modify'
$MountExp1  = 'ARM-MOUNT|/v2/live-exec|' + $Route21
$MountExp2  = 'ARM-MOUNT|/api/v1/v2/live-exec|' + $Route21
$Census     = 'ARM-CENSUS|mounts=2|total=42|per-mount-paths=21|per-mount-ops=22'

$ts             = Get-Date -Format yyyyMMddHHmmss
$TranscriptPath = Join-Path $EvDir ("BE12-400PIN-RUN-{0}.txt" -f $ts)
$WitnessPath    = Join-Path $EvDir 'BE12-400PIN-WITNESS.txt'

# --------------------------------------------------- fileless engines (-c) ---
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

# Surface arm: in-process ASGI door (BE-11 transport-swapped precedent).
# argv: 1=tag 2=login-path-hint (unused) ; env: AXIOM_ADMIN_PW (file-fed),
# AXIOM_DATABASE_URL, optional AXIOM_V2_MODE. Single-quote discipline throughout.
$CodeSurface = @'
import os,sys,logging
logging.disable(logging.CRITICAL)
from fastapi.testclient import TestClient
from app import main
try:
 pw=os.environ['AXIOM_ADMIN_PW']
 c=TestClient(main.create_app())
 cands=['/openapi.json','/api/v1/openapi.json','/api/openapi.json']
 doc=None
 for q in cands:
  r=c.get(q)
  if r.status_code==200 and r.text.lstrip().startswith('{'):
   try:
    d=r.json()
    if 'paths' in d:
     doc=(q,d); break
   except Exception:
    pass
 if doc is None:
  print('PYERROR|no candidate answered 200+JSON-of-paths: %r'%(cands,)); sys.exit(7)
 print('ARM-DOC|path='+doc[0])
 paths=list(doc[1]['paths'].keys())
 lx=sorted(p for p in paths if '/live-exec/' in p)
 fam={}
 for q in lx:
  base=q.split('/live-exec/',1)[0]+'/live-exec/'
  fam.setdefault(base,[]).append(q)
 for k in sorted(fam):
  names='+'.join(sorted(x.split(k,1)[1] for x in fam[k]))
  print('ARM-MOUNT|%s|%s'%(k.rstrip('/'),names))
 first=sorted(fam.keys())[0]
 ops=0
 for q in fam[first]:
  ops+=len(doc[1]['paths'][q])
 print('ARM-CENSUS|mounts=%d|total=%d|per-mount-paths=%d|per-mount-ops=%d'%(len(fam),len(lx),len(fam[first]),ops))
 login='/api/v1/auth/login'
 if login not in paths:
  print('PYERROR|pinned login door absent; auth candidates: %r'%([p for p in paths if p.endswith('/auth/login')],)); sys.exit(2)
 print('ARM-LOGIN|path='+login)
 r=c.post(login,json={'username':'admin','password':pw})
 print('ARM-LOGIN|http=%d'%r.status_code)
 if r.status_code!=200:
  print('PYERROR|login failed body=%r'%(r.text[:160],)); sys.exit(3)
 j=r.json()
 tj=j.get('tokens') if isinstance(j,dict) else None
 tok=tj.get('access_token') if isinstance(tj,dict) else None
 if not tok:
  bk=sorted(j.keys()) if isinstance(j,dict) else [type(j).__name__]
  tk=sorted(tj.keys()) if isinstance(tj,dict) else [type(tj).__name__]
  print('PYERROR|pinned tokens.access_token absent; body_keys=%r tokens_keys=%r (values redacted; pin source LoginResponse per E-400PIN-C4)'%(bk,tk)); sys.exit(4)
 h={'Authorization':'Bearer '+tok}
 ev='/api/v1/v2/live-exec/evaluate'
 if ev not in paths:
  print('PYERROR|pinned evaluate door absent; live-exec candidates: %r'%([p for p in lx if p.endswith('/evaluate')],)); sys.exit(5)
 print('ARM-EVAL|path='+ev)
 body={'account_present':True,'account_posture_class':'practice',
  'instrument_mapped':True,'session_open':True,
  'basis_present':True,'basis_age_hours':2.0,'max_age_hours':48.0,
  'quantity':'1','cited_price':'1.0','price_currency':'USD',
  'basis_currency':'USD','margin_available':'1000000.00'}
 r=c.post(ev,json=body,headers=h)
 print('ARM-EVAL|http=%d'%r.status_code)
 if r.status_code!=200:
  print('PYERROR|evaluate refused body=%r'%(r.text[:240],)); sys.exit(6)
 env=r.json()
 ar=env.get('actuation_refusal') or {}
 n=(ar.get('notes') or [{}])[0]
 print('ARM-%s|mode=%s|reason=%s|lock=%s|order=%s'%(
  sys.argv[1],env.get('mode'),ar.get('reason'),ar.get('lock'),n.get('order_position')))
except SystemExit:
 raise
except Exception as e:
 print('PYERROR|%r'%(e,)); sys.exit(1)
'@

# Door-drive arms: armature INSERT inside BEGIN, engine-typed refusals asserted
# in-process, ROLLBACK always, count re-verified. argv: 1=db path.
$CodeDoor = @'
import sqlite3,sys
sys.path.insert(0,'.')
from app.v2.live_exec.locks import ActuationRefused,ActuationState,require_actuation
db=sys.argv[1]
c=sqlite3.connect(db)
c.isolation_level=None
def drive(state):
 try:
  require_actuation(state)
  return 'NOTREFUSED'
 except ActuationRefused as e:
  n=(e.notes or [{}])[0]
  sc=n.get('sub_classes') or []
  return 'reason=%s|lock=%s|order=%s|sub=%s'%(e.reason,e.lock,n.get('order_position'),'+'.join(sc))
try:
 c.execute('BEGIN')
 c.execute('INSERT INTO v2_live_activation_instrument (id, sole, version, template_hash, funded_posture_ref, step_up_ref, operator_ref, actor_id, data_class, mode, operator_id, created_at) VALUES ('+chr(39)+sys.argv[2]+chr(39)+','+chr(39)+'SOLE'+chr(39)+','+chr(39)+'lai-1.0.0'+chr(39)+','+chr(39)+'h'+chr(39)+','+chr(39)+'probe'+chr(39)+','+chr(39)+'probe'+chr(39)+','+chr(39)+'probe'+chr(39)+','+chr(39)+'probe'+chr(39)+','+chr(39)+'live_marker'+chr(39)+','+chr(39)+'RESEARCH'+chr(39)+','+chr(39)+'itrga-closeout'+chr(39)+','+chr(39)+'2026-09-09 00:00:00'+chr(39)+')')
 rows=c.execute('SELECT COUNT(*) FROM v2_live_activation_instrument').fetchone()[0]
 print('ARM-ARMATURE|rows=%d'%rows)
 s=ActuationState(mode='RESEARCH',credential_class='practice_trade',activation_instrument_rows=rows,funded_posture=False,killswitch_armed=False)
 print('ARM-W3|'+drive(s))
 s=ActuationState(mode='RESEARCH',credential_class='practice_trade',activation_instrument_rows=rows,funded_posture=True,killswitch_armed=False,sub_failures=('sub_signing_failure',))
 print('ARM-W4|'+drive(s))
 s=ActuationState(mode='LIVE',credential_class=None,activation_instrument_rows=rows,funded_posture=False,killswitch_armed=False)
 print('ARM-W1o|'+drive(s)+' (order law: L1 before L3, armature present)')
 s=ActuationState(mode='RESEARCH',credential_class='practice_trade',activation_instrument_rows=rows,funded_posture=True,killswitch_armed=True)
 print('ARM-W4o|'+drive(s)+' (L5 engine-typing: EVIDENCE-ONLY, not a fielded firing)')
 c.execute('ROLLBACK')
 left=c.execute('SELECT COUNT(*) FROM v2_live_activation_instrument').fetchone()[0]
 print('ARM-ROLLBACK|left=%d'%left)
except Exception as e:
 try:
  c.execute('ROLLBACK')
 except Exception:
  pass
 print('PYERROR|%r'%(e,)); sys.exit(1)
finally:
 c.close()
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
  Write-Host 'This battery cannot mutate the lineage: surface arms commit nothing; door-drives roll back by construction.'
  Write-Host 'Send this transcript to ITRGA.'
  if ($script:TranscriptOn) { try { Stop-Transcript | Out-Null } catch { } ; $script:TranscriptOn = $false }
  exit 1
}

function Invoke-Py { param([string]$Code, [string[]]$PsArgs)
  $env:PYTHONWARNINGS = 'ignore'
  try { $raw = & $Py -c $Code @PsArgs 2>&1; $code = $LASTEXITCODE }
  finally { Remove-Item Env:PYTHONWARNINGS -ErrorAction SilentlyContinue }
  return (New-Object PSObject -Property @{ Text = (ConvertTo-Text @($raw)).TrimEnd(); Code = $code })
}

function Invoke-Read { param([string]$Db, [string]$Sql)
  return (Invoke-Py $CodeRead @($Db,$Sql)).Text
}

function Invoke-Surface { param([string]$Tag, [bool]$ForceLive)
  if ($ForceLive) { $env:AXIOM_V2_MODE = 'LIVE' } else { Remove-Item Env:AXIOM_V2_MODE -ErrorAction SilentlyContinue }
  $env:AXIOM_DATABASE_URL = 'sqlite+aiosqlite:///' + ($Target -replace '\\','/')
  $env:AXIOM_ADMIN_PW = (Get-Content $PwFile -Raw).Trim()
  Push-Location $Backend
  try { $res = Invoke-Py $CodeSurface @($Tag) }
  finally {
    Pop-Location
    Remove-Item Env:AXIOM_V2_MODE -ErrorAction SilentlyContinue
    Remove-Item Env:AXIOM_DATABASE_URL -ErrorAction SilentlyContinue
    Remove-Item Env:AXIOM_ADMIN_PW -ErrorAction SilentlyContinue
  }
  Write-Host $res.Text
  return $res
}

function Invoke-Door {
  Push-Location $Backend
  try { $res = Invoke-Py $CodeDoor @($Target,$ArmId) }
  finally { Pop-Location }
  Write-Host $res.Text
  return $res
}

function Assert-RepoState {
  Assert-Gate ((Invoke-Read $Target 'SELECT version_num FROM alembic_version') -eq '20260909_0057') 'fielded head == 20260909_0057' '20260909_0057' '(see above)'
  Assert-Gate ((Invoke-Read $Target "SELECT COUNT(*) FROM sqlite_master WHERE type='trigger'") -eq '94') 'triggers == 94' '94' '(see above)'
  Assert-Gate ((Invoke-Read $Target 'SELECT COUNT(*) FROM v2_permission') -eq '88') 'permissions == 88' '88' '(see above)'
  Assert-Gate ((Invoke-Read $Target 'SELECT COUNT(*) FROM v2_computation_version') -eq '17') 'compver == 17' '17' '(see above)'
  foreach ($zt in $ZeroTables) {
    Assert-Gate ((Invoke-Read $Target ("SELECT COUNT(*) FROM {0}" -f $zt)) -eq '0') ("THE ELECTION: {0} at 0 rows" -f $zt) '0' '(see above)'
  }
  Assert-Gate ((Invoke-Py $CodeLxe18 @($Backend)).Text -eq $Lxe18Expect) '18-file lxe build == 93f436bc... (arms run against the exact fielded build)' $Lxe18Expect '(see above)'
}

# ------------------------------------------------------------------- C0/BEGIN
New-Item -ItemType Directory -Force $EvDir | Out-Null
$script:TranscriptOn = $true
Start-Transcript -Path $TranscriptPath | Out-Null

try {

Write-Section 'C0. RUN IDENTIFICATION'
Write-Host 'Pack: ITRGA-V2-BE12-LOCKREFUSAL-400PIN-V5'
Write-Host 'V5 NOTE: token pinned at body.tokens.access_token (fielded LoginResponse, response_model-enforced; E-400PIN-C4); every door schema pinned from source-of-record; C3+addendum DISCHARGED by the V4 witness. V1/V2/V3/V4 never to be re-run.'
Write-Host 'Act: witness L1/L2/L4/L6 refusing on the fielded lineage (+ order fixtures). NOTHING LANDS.'
Write-Host 'Implements: ITRGA-V2-BE12-CLOSEOUT-ADDENDUM-CARD-0001 (governing text, SS3a addendum pointer)'
Write-Host 'Authority: BO-V2-BE12E-001 closeout condition (i) / ITRGA_VERDICT_V2_BE12_DR5_GATE_001 SS4 / DR-2 / DR-F1 AM-2 / credential law N-O18 / ERRATA E-400PIN-C2 + E-400PIN-C3(+addendum; DISCHARGED) + E-400PIN-C4'
Write-Host ("Started: {0}" -f (Get-Date -Format 'yyyy-MM-dd HH:mm:ss zzz'))
Write-Host ("Target file: {0}" -f $Target)
Write-Host 'FIELD LAW (re-asserted): zero-row BY ELECTION on all seven 12-series tables, pinned before AND after; no engine verb; no register POST; no credential window; vault envs never created.'
Write-Host 'Admin credential: file-fed per N-O18 (never echoed, never echoed, never echoed).'
Write-Host ''
Write-Host 'The running application may stay stopped. Continuing in 5 seconds; press Ctrl+C otherwise...'
Start-Sleep -Seconds 5

Write-Section 'C0b. OPERATOR-SHELL ENVIRONMENT SWEEP (probe envs must be absent here)'
$sweep = @(Get-ChildItem env: | Where-Object { $_.Name -match '^AXIOM_(TD|BROKER_PRACTICE|V2_MODE|ADMIN_PW|DATABASE_URL)|^PYTHONWARNINGS$' })
Assert-Gate ($sweep.Count -eq 0) 'C0b: no TD/PRACTICE/V2_MODE/ADMIN_PW/DATABASE_URL variables in the operator shell' 'absent' (($sweep | ForEach-Object { $_.Name }) -join ', ')

Write-Section 'C0c. FILE EXISTENCE'
Assert-Gate (Test-Path $Py)     'C0c.1 venv python present' $Py '(missing)'
Assert-Gate (Test-Path $Target) 'C0c.2 fielded db present' $Target '(missing)'
Assert-Gate (Test-Path $PwFile) 'C0c.3 admin credential file present (N-O18; contents never printed)' $PwFile '(missing)'
Assert-Gate (Test-Path (Join-Path $Backend 'app\main.py')) 'C0c.4 app entry present' 'app\main.py' '(missing)'
Assert-Gate (Test-Path (Join-Path $Backend 'app\v2\live_exec\locks.py')) 'C0c.5 lock engine present' 'app\v2\live_exec\locks.py' '(missing)'

Write-Section 'C1. FIELDED-LINEAGE RE-PINS (pre-battery; any drift since the cards IS the finding)'
Assert-RepoState

Write-Section 'C2. W1 SURFACE ARM - L1 mode_locked (boot elected LIVE in this child only)'
$r1 = Invoke-Surface 'W1' $true
Assert-Gate ($r1.Code -eq 0) 'W1 surface child exit 0' '0' $r1.Code
Assert-Gate ($r1.Text.Contains($Census)) 'W1 census: double-mount pinned (2 mounts, 42 total, 21 PATHS == 22 OPERATIONS per mount)' $Census '(see above)'
Assert-Gate ($r1.Text.Contains($MountExp1)) 'W1 mount family /v2/live-exec: the 21 paths exact' 'constant-pinned 21' '(see above)'
Assert-Gate ($r1.Text.Contains($MountExp2)) 'W1 mount family /api/v1/v2/live-exec: the 21 paths exact' 'constant-pinned 21' '(see above)'
Assert-Gate ($r1.Text -match 'ARM-LOGIN\|path=/api/v1/auth/login') 'W1 login door == pinned namespaced presence' '/api/v1/auth/login' '(see above)'
Assert-Gate ($r1.Text -match 'ARM-LOGIN\|http=200') 'W1: admin login 200 (file-fed credential)' 'http=200' '(see above)'
Assert-Gate ($r1.Text -match 'ARM-EVAL\|http=200') 'W1: evaluate door answered 200 (eligibility pass; the door rides the envelope)' 'http=200' '(see above)'
Assert-Gate ($r1.Text -match 'ARM-W1\|mode=LIVE\|reason=mode_locked\|lock=mode_locked\|order=1') 'W1 L1: reason mode_locked / lock mode_locked / order_position 1 / mode LIVE' 'ARM-W1|mode=LIVE|reason=mode_locked|lock=mode_locked|order=1' '(see above)'

Write-Section 'C3. W2 SURFACE ARM - L2 posture_mismatch (standing boot: RESEARCH; no credential window by construction)'
$r2 = Invoke-Surface 'W2' $false
Assert-Gate ($r2.Code -eq 0) 'W2 surface child exit 0' '0' $r2.Code
Assert-Gate ($r2.Text.Contains($Census)) 'W2 census: double-mount pinned (2 mounts, 42 total, 21 paths == 22 operations per mount)' $Census '(see above)'
Assert-Gate ($r2.Text.Contains($MountExp1)) 'W2 mount family /v2/live-exec: 21 paths exact' 'constant-pinned 21' '(see above)'
Assert-Gate ($r2.Text.Contains($MountExp2)) 'W2 mount family /api/v1/v2/live-exec: 21 paths exact' 'constant-pinned 21' '(see above)'
Assert-Gate ($r2.Text -match 'ARM-LOGIN\|http=200') 'W2: admin login 200' 'http=200' '(see above)'
Assert-Gate ($r2.Text -match 'ARM-EVAL\|http=200') 'W2: evaluate door answered 200' 'http=200' '(see above)'
Assert-Gate ($r2.Text -match 'ARM-W2\|mode=RESEARCH\|reason=posture_mismatch\|lock=posture_mismatch\|order=2') 'W2 L2: reason posture_mismatch / lock same / order_position 2 / mode RESEARCH (deployment standing boot)' 'ARM-W2|mode=RESEARCH|reason=posture_mismatch|lock=posture_mismatch|order=2' '(see above)'

Write-Section 'C4. W3/W4 DOOR-DRIVE ARMS - L4 + L6 (armature transaction, ALWAYS rolled back)'
Write-Host 'Armature: the future-lawful live_marker row (0056 lawful-probe literal; the 12D-review armature pattern), INSERT-only is unguarded; ROLLBACK ends every story.'
$r3 = Invoke-Door
Assert-Gate ($r3.Code -eq 0) 'door-drive child exit 0' '0' $r3.Code
Assert-Gate ($r3.Text -match 'ARM-ARMATURE\|rows=1') 'armature row present inside the transaction (COUNT==1)' 'rows=1' '(see above)'
Assert-Gate ($r3.Text -match 'ARM-W3\|reason=funded_posture_required\|lock=funded_posture_required\|order=4\|sub=') 'W3 L4: reason funded_posture_required / lock same / order_position 4' 'ARM-W3|reason=funded_posture_required|lock=funded_posture_required|order=4|sub=' '(see above)'
Assert-Gate ($r3.Text -match 'ARM-W4\|reason=sub_signing_failure\|lock=sub_contract_failure\|order=6\|sub=sub_signing_failure') 'W4 L6: injected corpus-pinned class proxied FIRST-CLASS (reason == sub_signing_failure; lock == sub_contract_failure; order_position 6; sub_classes echo exact)' 'reason=sub_signing_failure|lock=sub_contract_failure|order=6|sub=sub_signing_failure' '(see above)'
Assert-Gate ($r3.Text -match 'ARM-W1o\|reason=mode_locked\|lock=mode_locked\|order=1') 'W1o order-fixture: L1 before L3 with the armature present (DR canonical order law, on the fielded lineage)' 'reason=mode_locked|...|order=1' '(see above)'
Assert-Gate ($r3.Text -match 'ARM-W4o\|reason=killswitch_armed\|lock=killswitch_armed\|order=5') 'W4o order-fixture: L5 engine-typing EVIDENCE-ONLY (NOT a fielded firing; L5 discharge-by-design stands)' 'reason=killswitch_armed|...|order=5' '(see above)'
Assert-Gate ($r3.Text -match 'ARM-ROLLBACK\|left=0') 'armature fully rolled back (COUNT==0 after)' 'left=0' '(see above)'

Write-Section 'C5. FIELDED-LINEAGE RE-PINS (post-battery: identical file, or the finding opens here)'
Write-Host 'The battery just attempted everything a deployment may fear; the lineage must be byte-identical in state:'
Assert-RepoState
$sweep = @(Get-ChildItem env: | Where-Object { $_.Name -match '^AXIOM_(TD|BROKER_PRACTICE|V2_MODE|ADMIN_PW|DATABASE_URL)|^PYTHONWARNINGS$' })
Assert-Gate ($sweep.Count -eq 0) 'C5 env close: probe envs re-swept absent (no window left open anywhere)' 'absent' (($sweep | ForEach-Object { $_.Name }) -join ', ')

Write-Section 'C6. WITNESS RECORD + VERDICT'
$witness = @(
  ('WITNESS_TIMESTAMP   {0}' -f (Get-Date -Format 'yyyy-MM-dd HH:mm:ss zzz')),
  ('CARD                ITRGA-V2-BE12-CLOSEOUT-ADDENDUM-CARD-0001'),
  ('FIELDED_HEAD        20260909_0057 (pre==post; C1==C5 re-pins identical)'),
  ('ROUTE_ENUM          22 live-exec routes (standing SS6-elective, recorded en passant)'),
  ('W1_L1               mode_locked | lock=mode_locked | order=1 | mode=LIVE (per-boot env election, child only)'),
  ('W2_L2               posture_mismatch | lock=posture_mismatch | order=2 | mode=RESEARCH (standing boot; live door credential_class=None by delivered code - no window possible)'),
  ('W3_L4               funded_posture_required | lock=funded_posture_required | order=4 (armature, rolled back)'),
  ('W4_L6               sub_signing_failure proxied FIRST-CLASS | lock=sub_contract_failure | order=6 | sub_classes=(sub_signing_failure)'),
  ('W1o_ORDER           mode_locked wins with armature present: L1 before L3 (DR canonical order law)'),
  ('W4o_ORDER           killswitch_armed typed by engine (order=5) - EVIDENCE-ONLY; L5 discharge-by-design stands'),
  ('ELECTION_POST       all seven 12-series tables == 0 rows; the fielded lineage holds no runtime evidence rows of any band'),
  'VERDICT             PASS - L1/L2/L4/L6 witnessed refusing on the fielded lineage; gate condition (i) evidence complete'
)
$witness | Set-Content -Path $WitnessPath -Encoding ascii
Write-Host ('witness record: ' + $WitnessPath)
Write-Host ''
Write-Host '400-PIN VERDICT: PASS - the four outstanding locks spoke on the fielded lineage: L1 mode_locked (surface, boot-elected LIVE), L2 posture_mismatch (surface, standing boot), L4 funded_posture_required (door-drive, armature rolled back), L6 sub_* proxied first-class (door-drive, corpus-pinned class). Order law re-witnessed twice. Nothing landed; C1==C5.'
Write-Host ("Transcript: {0}" -f $TranscriptPath)
Write-Host 'NEXT: send transcript + witness record to ITRGA. Gate verdict SS1 updates L1/L2/L4/L6 to DISCHARGED; then the DR-5 CLOSEOUT VERDICT issues - the ladder''s last act.'

} finally {
  Remove-Item Env:AXIOM_V2_MODE -ErrorAction SilentlyContinue
  Remove-Item Env:AXIOM_DATABASE_URL -ErrorAction SilentlyContinue
  Remove-Item Env:AXIOM_ADMIN_PW -ErrorAction SilentlyContinue
  Remove-Item Env:PYTHONWARNINGS -ErrorAction SilentlyContinue
  if ($script:TranscriptOn) { try { Stop-Transcript | Out-Null } catch { } }
}
