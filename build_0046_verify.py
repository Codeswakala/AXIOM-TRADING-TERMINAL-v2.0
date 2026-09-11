#!/usr/bin/env python3
# Surgical transformation: ITRGA_V2_0045_VERIFY_PACK_V1.ps1 -> ITRGA_V2_0046_VERIFY_PACK_V1.ps1
import io, sys

SRC = '/home/user/AXIOM-TRADING-TERMINAL-v2.0/ITRGA_V2_0045_VERIFY_PACK_V1.ps1'
APPLY = '/home/user/AXIOM-TRADING-TERMINAL-v2.0/ITRGA_V2_0046_APPLY_PACK_V1.ps1'
DST = '/home/user/AXIOM-TRADING-TERMINAL-v2.0/ITRGA_V2_0046_VERIFY_PACK_V1.ps1'

s = io.open(SRC, encoding='utf-8').read()
a = io.open(APPLY, encoding='utf-8').read()
ops = []

def rep(old, new, tag, src=None):
    t = s if src is None else src
    n = t.count(old)
    if n != 1:
        print('ANCHOR-COUNT-FAIL', tag, n); sys.exit(1)
    if src is None:
        ops.append((old, new, tag))

def rep_between(start, end, new, tag, keep_end=False):
    c1, c2 = s.count(start), s.count(end)
    if c1 != 1 or c2 != 1:
        print('ANCHOR-COUNT-FAIL-BETWEEN', tag, c1, c2); sys.exit(1)
    i = s.find(start); j = s.find(end, i + len(start))
    if j < 0:
        print('ANCHOR-ORDER-FAIL', tag); sys.exit(1)
    old = s[i:j] if keep_end else s[i:j + len(end)]
    if keep_end:
        new = new + end
    rep(old, new, tag)

def lift(start, end, tag, keep_end=False):
    # extract a block from the built apply pack
    c1, c2 = a.count(start), a.count(end)
    if c1 != 1 or c2 != 1:
        print('LIFT-COUNT-FAIL', tag, c1, c2); sys.exit(1)
    i = a.find(start); j = a.find(end, i + len(start))
    if j < 0:
        print('LIFT-ORDER-FAIL', tag); sys.exit(1)
    # keep_end=False -> EXCLUDE the end marker; True -> INCLUDE it.
    return a[i:j + len(end)] if keep_end else a[i:j]

# ============================================================
# V-R1. HEADER
# ============================================================
NEW_HEADER = '''# =====================================================================
# AXIOM V2 - 0046 WORKING-DATABASE VERIFICATION ACT (BAND BE-6)
# ITRGA SQLITE VERIFY ACT EVIDENCE PACK (V1)
# Pack ID: ITRGA-V2-0046-VERIFY-PACK-V1
# Authority:
#   - ITRGA-DET-V2-BE-6-FINAL-001 (final determination; C full-verify
#     PASS; instrument contract for the application act in section 7.3)
#   - ITRGA-DET-V2-BE-6-ACCEPT-001 (acceptance; BO-V2-BE-6-001 closed)
#   - BO-V2-BE-6-001 (terminal state; working-lineage half via this
#     apply+verify envelope)
#   - ITRGA-ASSESSMENT-V2-0046-APPLY-SCOPE-V1 (scope assessment,
#     instrument contract and commissioning record, incl. the pre-act
#     disclosure)
#   - ITRGA-V2-0046-APPLY-PACK-V1 (produces the state record and the
#     anchor this pack consumes; the verify act CANNOT precede the
#     apply act)
# Pattern: ITRGA-V2-0045-VERIFY-PACK-V1 -> ITRGA-V2-0043-VERIFY-PACK-V1
#   (instruments of record of the two preceding working-DB verification
#   acts; PGF-001 through PGF-015 incorporated by construction: pure
#   ASCII, helper command functions with non-colliding parameter names,
#   dialect-correct SQL, content-based comparisons, format-independent
#   drift assertions, name-set/PRAGMA-only index introspection with
#   uniqueness proven BEHAVIORALLY - sqlite_master has no 'origin'
#   column (PGF-015)).
#
# WHAT THIS PACK DOES (READ-ONLY against the target file; the only
#   mutation channels are the transactional probes, which always roll
#   their throwaway rows back):
#   - Binds the target file to the 0046 apply act byte-for-byte
#     (apply-final-state record consumed strictly; abort unless the
#     record is the 0046 PASS-state and the bytes match exactly).
#   - Independently re-proves the full terminal state: revision
#     exactly 20260903_0046; exactly 32 v2 triggers (28 inherited + 4
#     BE-6, exact names); the four BE-6 guard refusals with exact
#     messages plus the inherited compver guards on the new seed row;
#     both uniqueness anchors proven BEHAVIORALLY; three CHECK-vocabulary
#     probes refused; the two BE-6 tables with the pinned column
#     name-sets, all seven named constraints and both indexes; 6
#     computation-version rows (BE-4 pinned; mge/sge and
#     portfolio_risk_engine proven by RUNTIME RECOMPUTATION of the
#     engine files, the BE-6 recomputation asserted equal to the pinned
#     anchor); 41 permission rows (6 additive BE-6 rows content-exact,
#     no duplicates); both BE-6 tables empty and all five BE-5 tables
#     still empty; inherited BE-1..BE-3 anchors content-exact; drift
#     exactly the 9 inherited V1 tokens with zero BE-6/V2 tokens; no
#     authority variable present.
#   - Re-verifies the recovery anchor (file hash equal to the record;
#     the anchor is the CURRENT-AS-IS pre-image per pre-act disclosure
#     N-1: it lawfully includes the restart-era bootstrap-admin row).
#
# PREREQUISITES:
#   - The apply pack completed with verdict PASS (state record
#     present in operator-evidence\\BE-6).
#   - The application has NOT been restarted since the apply (the
#     state-record byte-binding enforces this; the
#     both-BE-6-tables-empty proof additionally assumes it).
#
# OPERATOR INSTRUCTION CARD:
#   1. Run ITRGA_V2_0046_APPLY_PACK_V1.ps1 FIRST (its PASS is the
#      precondition; this pack reads its state record).
#   2. Execute ONLY this file, from the repository root:
#        powershell -NoProfile -ExecutionPolicy Bypass -File ".\\ITRGA_V2_0046_VERIFY_PACK_V1.ps1"
#   3. Single expected input: the absolute path of the working
#      database file backend\\axiom_dev.db (a path, not a credential).
#   4. Send BOTH transcripts back to ITRGA:
#        operator-evidence\\BE-6\\0046-APPLY-RUN-V1.txt
#        operator-evidence\\BE-6\\0046-VERIFY-RUN-V1.txt
#      These two files close the 0046 application act and place the
#      BO-V2-BE-6-001 terminal state on the working lineage. Restart
#      the application only after this pack completes with PASS.
#
# =====================================================================
'''
i = s.find('# =====================================================================\n# AXIOM V2 - 0044/0045')
j = s.find('Set-StrictMode -Version Latest')
assert i == 0 and j > 0
rep(s[i:j], NEW_HEADER + '\n', 'V-R1-header')

# ============================================================
# V-R2. PATHS
# ============================================================
rep('$EvidenceDir   = Join-Path $EvidenceRoot "BE-5"',
    '$EvidenceDir   = Join-Path $EvidenceRoot "BE-6"', 'V-R2-eviddir')
rep('$Transcript    = Join-Path $EvidenceDir "0045-VERIFY-RUN-V1.txt"',
    '$Transcript    = Join-Path $EvidenceDir "0046-VERIFY-RUN-V1.txt"', 'V-R2-transcript')
rep('$StateRecPath  = Join-Path $EvidenceDir "0045-APPLY-FINAL-STATE.txt"',
    '$StateRecPath  = Join-Path $EvidenceDir "0046-APPLY-FINAL-STATE.txt"', 'V-R2-staterec')
rep('$HelperDir  = Join-Path $env:TEMP "axiom_itrga_0045_verify_v1"',
    '$HelperDir  = Join-Path $env:TEMP "axiom_itrga_0046_verify_v1"', 'V-R2-helperdir')
rep('''Write-Host "This pack VERIFIES the 0044/0045 working-database state"
Write-Host "(read-only; transactional guard probes roll their probe rows back)."
Write-Host "The apply pack must have completed with PASS first."''',
    '''Write-Host "This pack VERIFIES the 0046 working-database state (band BE-6)"
Write-Host "(read-only; transactional probes roll their probe rows back)."
Write-Host "The apply pack must have completed with PASS first."''', 'V-R2-prompt')

# ============================================================
# V-R3. CONSTANTS (migrations, revision, delivered map, guard arrays)
# ============================================================
rep('''    "20260902_0045_v2_be5_signal_contracts.py"     = "9aa87508b6db4d74296f8dabfab33ae7fb84dc705326f141b4b42e2d4f981f52"
}
$ApplyTargetRevision = "20260902_0045"''',
    '''    "20260902_0045_v2_be5_signal_contracts.py"     = "9aa87508b6db4d74296f8dabfab33ae7fb84dc705326f141b4b42e2d4f981f52"
    "20260903_0046_v2_be6_portfolio_research.py"   = "1e95ce499ec73bb5b8b0a628cfa01f1f26642c3cfcc080806cacce2532156962"
}
$ApplyTargetRevision = "20260903_0046"''', 'V-R3-migrations')

# Delivered hashtable: replace wholesale with the apply pack's 27-key map (deduped, BE-6 pins on shared paths).
def slice_first(t, start, end, tag):
    if t.count(start) != 1:
        print('SLICE-START-FAIL', tag, t.count(start)); sys.exit(1)
    i = t.find(start); j = t.find(end, i + len(start))
    if j < 0:
        print('SLICE-END-FAIL', tag); sys.exit(1)
    return t[i:j + len(end)]

ap_map = slice_first(a, '$ExpectedDeliveredHashes = @{', '\n}\n', 'V-lift-delmap')
old_map = slice_first(s, '$ExpectedDeliveredHashes = @{', '\n}\n', 'V-R3-delmap-old')
rep(old_map, ap_map, 'V-R3-delmap')

# Guard arrays + drift: append BE-6 material after $TransitionGuardTriggers block close.
be6_names = lift('$Be6GuardNames = @(', '$Be4GuardTriggers = @(', 'V-lift-be6names')
rep('''$Be4GuardTriggers = @(
    "v2_chart_intelligence_report_immutable_delete",
    "v2_chart_intelligence_report_immutable_update",
    "v2_computation_version_immutable_delete",
    "v2_computation_version_immutable_update",
    "v2_market_context_report_immutable_delete",
    "v2_market_context_report_immutable_update"
)''',
    be6_names + '''$Be4GuardTriggers = @(
    "v2_chart_intelligence_report_immutable_delete",
    "v2_chart_intelligence_report_immutable_update",
    "v2_computation_version_immutable_delete",
    "v2_computation_version_immutable_update",
    "v2_market_context_report_immutable_delete",
    "v2_market_context_report_immutable_update"
)''', 'V-R3-be6names')

# ============================================================
# V-R4. HELPER INJECTIONS (identical to the apply pack's proven code)
# ============================================================
rep('''SGE_FILES = (
    "app/v2/research_governance/signals.py",
    "app/v2/research_governance/api.py",
)''',
    '''SGE_FILES = (
    "app/v2/research_governance/signals.py",
    "app/v2/research_governance/api.py",
)
BE6_FILES = (
    "app/v2/portfolio_research/__init__.py",
    "app/v2/portfolio_research/contracts.py",
    "app/v2/portfolio_research/metrics.py",
    "app/v2/portfolio_research/scenarios.py",
)''', 'V-R4-be6files')
rep('''    if cmd in ("scalar", "verifyrows", "verifyaudit", "compverbe5",
               "permbe5", "reportempty5", "tabledigest"):''',
    '''    if cmd in ("scalar", "verifyrows", "verifyaudit", "compverbe5",
               "permbe5", "reportempty5", "compverbe6", "permbe6",
               "reportempty2", "tabledigest"):''', 'V-R4-cmdtuple')
for anchor_start, anchor_end, tag in [
    ('            elif cmd == "compverbe6":', '            elif cmd == "permbe5":', 'compverbe6'),
    ('            elif cmd == "permbe6":', '            elif cmd == "reportempty5":', 'permbe6'),
    ('            elif cmd == "reportempty2":', '            elif cmd == "tabledigest":', 'reportempty2'),
]:
    body = lift(anchor_start, anchor_end, 'V-lift-' + tag)
    rep(anchor_end, body + anchor_end, 'V-R4-' + tag)
uniq_body = lift('    if cmd == "uniqbe6":', '\n    print("FAIL:unknown_command=" + cmd)', 'V-lift-uniq')
rep('    print("FAIL:unknown_command=" + cmd)', uniq_body + '\n    print("FAIL:unknown_command=" + cmd)', 'V-R4-uniq')

# ============================================================
# V-R5. RUN-ID PROSE + UniqProbe function injection
# ============================================================
rep('''Write-Evidence "Pack: ITRGA-V2-0045-VERIFY-PACK-V1"
Write-Evidence "Act: band BE-5 (0044+0045) working-database verification act (read-only; transactional probes roll back)"
Write-Evidence "Determination: ITRGA-DET-V2-BE-5-FINAL-001 (C full-verify PASS; C-2 scope = apply+verify envelope)"
Write-Evidence "Build order: BO-V2-BE-5-001 (terminal state T-1...T-12)"''',
    '''Write-Evidence "Pack: ITRGA-V2-0046-VERIFY-PACK-V1"
Write-Evidence "Act: band BE-6 (0046) working-database verification act (read-only; transactional probes roll back)"
Write-Evidence "Determination: ITRGA-DET-V2-BE-6-FINAL-001 (C full-verify PASS) + ITRGA-DET-V2-BE-6-ACCEPT-001"
Write-Evidence "Build order: BO-V2-BE-6-001 (terminal state; working-lineage half via this envelope)"
Write-Evidence "Scope/commissioning: ITRGA-ASSESSMENT-V2-0046-APPLY-SCOPE-V1 (incl. pre-act disclosure N-1)"''', 'V-R5-runid')

rep('''    Write-Evidence "PASS: exact refusal message observed; throwaway row rolled back."
}

# ---------------------------------------------------------------------
# B0. RUN IDENTIFICATION''',
    '''    Write-Evidence "PASS: exact refusal message observed; throwaway row rolled back."
}

function Invoke-ExpectedUniqProbe {
    param(
        [Parameter(Mandatory = $true)][string]$Label,
        [Parameter(Mandatory = $true)][string]$Flavor
    )

    Write-Evidence ""
    Write-Evidence "EXPECTED-UNIQUENESS-PROBE: ${Label}"

    $Out = Invoke-Py -PyArgs @("uniqbe6", ${TargetDbPath}, ${Flavor}) -Label $Label
    $Text = (Norm-Text $Out).Trim()

    if ($Text -notlike "REFUSED:*") {
        throw "FAIL: expected uniqueness refusal did not occur (duplicate insert succeeded or helper error): ${Label}"
    }
    if ($Text -notlike "*UNIQUE constraint failed*") {
        throw "FAIL: the refusal was not a UNIQUE-constraint refusal: ${Label} (observed '${Text}')"
    }
    Write-Evidence "PASS: duplicate insert refused by the uniqueness anchor (behavioral proof); throwaway rows rolled back."
}

# ---------------------------------------------------------------------
# B0. RUN IDENTIFICATION''', 'V-R5-uniqfn')

# ============================================================
# V-R6. B0e STATE RECORD (14-key contract of the 0046 apply record)
# ============================================================
rep_between('    $State = Read-Pins -Path $StateRecPath -ExpectedKeys @(',
            'Write-Evidence "PASS: state record parsed; this run\'s verdict-binding post-0045 identity is known."',
            '''    $State = Read-Pins -Path $StateRecPath -ExpectedKeys @(
        "STATE_FILE_ID", "RUN_TIMESTAMP", "POST_SIZE_BYTES", "POST_LAST_WRITE",
        "POST_SHA256", "POST_REVISION", "POST_V2_TRIGGER_COUNT",
        "POST_COMPVER_COUNT", "POST_PERMISSION_COUNT",
        "BASELINE_TIER1_BYTE_EXACT", "BASELINE_POLICY",
        "ANCHOR_FILENAME", "ANCHOR_SIZE_BYTES", "ANCHOR_SHA256"
    ) -Label "0046 apply-final-state record"

    if ($State["STATE_FILE_ID"] -ne "ITRGA-V2-0046-APPLY-FINAL-STATE-V1") {
        throw "STOP: state record identity '$($State["STATE_FILE_ID"])' is not ITRGA-V2-0046-APPLY-FINAL-STATE-V1."
    }
    if ($State["POST_REVISION"] -ne ${ApplyTargetRevision}) {
        throw "STOP: state record revision '$($State["POST_REVISION"])' is not ${ApplyTargetRevision}."
    }
    if ($State["POST_V2_TRIGGER_COUNT"] -ne "32") {
        throw "STOP: state record trigger count '$($State["POST_V2_TRIGGER_COUNT"])' is not 32."
    }
    if ($State["POST_COMPVER_COUNT"] -ne "6") {
        throw "STOP: state record computation-version count '$($State["POST_COMPVER_COUNT"])' is not 6."
    }
    if ($State["POST_PERMISSION_COUNT"] -ne "41") {
        throw "STOP: state record permission count '$($State["POST_PERMISSION_COUNT"])' is not 41."
    }
    if ($State["POST_SIZE_BYTES"] -notmatch '^[0-9]+$') { throw "STOP: malformed POST_SIZE_BYTES in state record." }
    if ($State["POST_SHA256"] -notmatch '^[0-9a-f]{64}$') { throw "STOP: malformed POST_SHA256 in state record." }
    if ($State["ANCHOR_SHA256"] -notmatch '^[0-9a-f]{64}$') { throw "STOP: malformed ANCHOR_SHA256 in state record." }
    if ($State["ANCHOR_SIZE_BYTES"] -notmatch '^[0-9]+$') { throw "STOP: malformed ANCHOR_SIZE_BYTES in state record." }
    if ($State["BASELINE_TIER1_BYTE_EXACT"] -notmatch '^(True|False)$') { throw "STOP: malformed BASELINE_TIER1_BYTE_EXACT in state record." }
    if ($State["BASELINE_POLICY"] -ne "anchor-as-is (pre-act disclosure N-1)") {
        throw "STOP: state record BASELINE_POLICY '$($State["BASELINE_POLICY"])' is not the disclosed anchor-as-is policy."
    }

    Write-Evidence "Record: ${StateRecPath}"
    Write-Evidence "  RUN_TIMESTAMP                $($State["RUN_TIMESTAMP"])"
    Write-Evidence "  POST_SIZE_BYTES              $($State["POST_SIZE_BYTES"])"
    Write-Evidence "  POST_LAST_WRITE              $($State["POST_LAST_WRITE"])"
    Write-Evidence "  POST_SHA256                  $($State["POST_SHA256"])"
    Write-Evidence "  POST_REVISION                $($State["POST_REVISION"])"
    Write-Evidence "  POST_V2_TRIGGER_COUNT        $($State["POST_V2_TRIGGER_COUNT"])"
    Write-Evidence "  POST_COMPVER_COUNT           $($State["POST_COMPVER_COUNT"])"
    Write-Evidence "  POST_PERMISSION_COUNT        $($State["POST_PERMISSION_COUNT"])"
    Write-Evidence "  BASELINE_TIER1_BYTE_EXACT    $($State["BASELINE_TIER1_BYTE_EXACT"])  (policy-recorded; anchor-as-is per pre-act disclosure N-1)"
    Write-Evidence "  BASELINE_POLICY              $($State["BASELINE_POLICY"])"
    Write-Evidence "PASS: state record parsed; this run's verdict-binding post-0046 identity is known."''',
            'V-R6-b0e')

# ============================================================
# V-R7. B0f PROVENANCE (9 chain + 27 delivered = 36 files)
# ============================================================
rep('Write-Section "B0f. PROVENANCE (25 files re-pinned on disk; abort on any mismatch)"',
    'Write-Section "B0f. PROVENANCE (36 files re-pinned on disk: 9 chain migrations + 27 delivered files; abort on any mismatch)"', 'V-R7-section')
rep('''        "20260902_0045_v2_be5_signal_contracts.py"
    )) {''',
    '''        "20260902_0045_v2_be5_signal_contracts.py",
        "20260903_0046_v2_be6_portfolio_research.py"
    )) {''', 'V-R7-chainlist')
rep('''        "backend\\app\\db\\models\\__init__.py",
        "backend\\tests\\test_v2_be4_migration.py"
    )) {''',
    '''        "backend\\app\\db\\models\\__init__.py",
        "backend\\tests\\test_v2_be4_migration.py",
        "backend\\app\\v2\\portfolio_research\\__init__.py",
        "backend\\app\\v2\\portfolio_research\\contracts.py",
        "backend\\app\\v2\\portfolio_research\\metrics.py",
        "backend\\app\\v2\\portfolio_research\\scenarios.py",
        "backend\\app\\v2\\portfolio_research\\api.py",
        "backend\\app\\db\\models\\v2_portfolio.py",
        "backend\\tests\\test_v2_be6_metrics.py",
        "backend\\tests\\test_v2_be6_migration.py",
        "backend\\tests\\test_v2_be6_api.py",
        "backend\\tests\\test_v2_be6_annex.py"
    )) {''', 'V-R7-deliveredlist')
rep('Write-Evidence "PASS: B0f - all 25 files on disk hash to the pinned values."',
    'Write-Evidence "PASS: B0f - all 36 files on disk hash to the pinned values (9 chain migrations 0038-0046; 27 delivered BE-5/BE-6 files; the four shared paths pinned to the BE-6 Rev-2 literals)."', 'V-R7-pass')

# B3 prose
rep('Write-Evidence "PASS: B3 - the recovery anchor (pre-0045 pre-image) exists and is byte-identical to the apply act\'s record; integrity ok."',
    'Write-Evidence "PASS: B3 - the recovery anchor (pre-0046 pre-image; current-as-is per pre-act disclosure N-1, incl. the restart-era bootstrap-admin row) exists and is byte-identical to the apply act\'s record; integrity ok."', 'V-R7-b3')

# ============================================================
# V-R8/V-R9/V-R10/V-R11. B4/B5 gates
# ============================================================
rep_between('    Write-Section "B4. COMPUTATION-VERSION ROWS (exactly 5; runtime recomputation)"',
            'Write-Evidence "PASS: B4 (T-5/T-6; P-4) - exactly 5 rows; BE-4 rows content-exact; mge/sge source hashes equal the runtime recomputation of the engine files; evidence_ref values exact."',
            '''    Write-Section "B4. COMPUTATION-VERSION ROWS (exactly 6; runtime recomputation incl. the BE-6 anchor)"

    $CompverOut = Invoke-Py -PyArgs @(
        "compverbe6", ${TargetDbPath}, ${BackendRoot},
        "fe9aab42c34d671e960fd92a9346d3bf60c27135e76e52310d774bc84028dd35",
        "69902503483502bcd5ce5e35fdb0eeabcb2efcaf7a4b0c262a6fccf2d0af3a8c",
        "3887d6ca8ba05858f41889cd99fa05aba42663ac22d906a7f989b567c3912180",
        ${Be6EngineAnchor}
    ) -Label "B4 computation-version rows"
    $CompverText = (Norm-Text $CompverOut).Trim()
    if ($CompverText -notlike "PASS:compver6_rows_exact*") {
        throw "FAIL: B4 - computation-version check failed: ${CompverText}"
    }
    if ($CompverText -notlike "*INFO:pre_recomputed=${Be6EngineAnchor}*") {
        throw "FAIL: B4 (P-4) - the runtime-recomputed BE-6 engine anchor does not equal the pinned anchor."
    }
    Write-Evidence "PASS: B4 (T-5/T-6; P-4) - exactly 6 rows; BE-4 rows content-exact; mge/sge source hashes equal the runtime recomputation; the portfolio_risk_engine row (pre-1.0.0, evidence_ref BO-V2-BE-6-001) equals the runtime recomputation of the four pinned files AND the pinned anchor."''',
            'V-R8-b4')

rep_between('    Write-Section "B5. PERMISSION ROWS + BE-5 TABLES EMPTY + TRIGGER POSTURE"',
            '''    # -----------------------------------------------------------------
    # B6. INHERITED STATE UNTOUCHED (BE-1..BE-3 anchors, content-exact)''',
            '''    Write-Section "B5. PERMISSION ROWS + BE-6 TABLES EMPTY (+ BE-5 STILL EMPTY) + TRIGGER POSTURE"

    $PermOut = Invoke-Py -PyArgs @("permbe6", ${TargetDbPath}) -Label "B5 permission rows"
    $PermText = (Norm-Text $PermOut).Trim()
    if ($PermText -notlike "PASS:perm6_rows_exact*") {
        throw "FAIL: B5 - permission check failed: ${PermText}"
    }
    if ($PermText -notlike "*INFO:v2_permission_total=41*") {
        throw "FAIL: B5 (T-4/T-6) - permission total is not exactly 41."
    }

    $EmptyOut2 = Invoke-Py -PyArgs @("reportempty2", ${TargetDbPath}) -Label "B5 BE-6 tables empty"
    $EmptyText2 = (Norm-Text $EmptyOut2).Trim()
    if ($EmptyText2 -ne "PASS:be6_tables_empty") {
        throw "FAIL: B5 - the two BE-6 tables are not empty. The application may have been restarted between apply and verify. Report to ITRGA."
    }
    $EmptyOut5 = Invoke-Py -PyArgs @("reportempty5", ${TargetDbPath}) -Label "B5 BE-5 tables still empty"
    $EmptyText5 = (Norm-Text $EmptyOut5).Trim()
    if ($EmptyText5 -ne "PASS:be5_tables_empty") {
        throw "FAIL: B5 - the five BE-5 tables are not empty. Report to ITRGA."
    }

    [void](Invoke-Py -PyArgs @("scalar", ${TargetDbPath}, "SELECT name FROM sqlite_master WHERE type='trigger' AND name LIKE 'v2_%' ORDER BY name;") -Label "B5 v2 trigger names (recorded)")
    $TrigNamesText = Get-PyScalar -Sql "SELECT name FROM sqlite_master WHERE type='trigger' AND name LIKE 'v2_%' ORDER BY name;" -Label "B5 v2 trigger set"
    $TrigNames = @($TrigNamesText -split "`n" | Where-Object { $_ -ne "" })
    if ($TrigNames.Count -ne 32) {
        throw "FAIL: B5 (T-3/T-6) - v2 trigger count '$($TrigNames.Count)', expected exactly 32."
    }
    $Expected32Sorted = @(($ExpectedPreTrig28 + $Be6GuardNames) | Sort-Object)
    $TrigSorted = @($TrigNames | Sort-Object)
    if (($TrigSorted -join "`n") -ne ($Expected32Sorted -join "`n")) {
        throw "FAIL: B5 (T-3/T-6) - the v2 trigger name set is not exactly the pinned 32-name census (28 inherited + 4 BE-6)."
    }
    Write-Evidence "PASS: B5 (T-2/T-3/T-4/T-6) - exactly 6 additive BE-6 permission rows (total 41, no duplicates); both BE-6 tables empty and all five BE-5 tables still empty; 32 v2 triggers exact-named (28 inherited intact + 4 BE-6)."

    # BE-6 schema census (PRAGMA/name-set; PGF-015): columns, PKs, named
    # constraints in the stored DDL, the two indexes, autoindex census.
    $PfdefCols = Get-PyScalar -Sql "SELECT name FROM pragma_table_info('v2_portfolio_definition') ORDER BY cid;" -Label "B5 pfdef columns"
    $ExpectedPfdefCols = @("id","portfolio_id","record_seq","supersedes","name","basis","allocations","base_currency","data_class","assumptions","mode","operator_id","correlation_id","created_at") -join "`n"
    if ($PfdefCols -ne $ExpectedPfdefCols) {
        throw "FAIL: B5 (T-2) - v2_portfolio_definition column set/order mismatch."
    }
    $PfriskCols = Get-PyScalar -Sql "SELECT name FROM pragma_table_info('v2_portfolio_risk_report') ORDER BY cid;" -Label "B5 pfrisk columns"
    $ExpectedPfriskCols = @("id","portfolio_definition_id","as_of","time_basis","input_refs","inputs_hash","metrics","scenarios","status","basis_label","data_class","engine_versions","engine_versions_hash","mode","operator_id","correlation_id","created_at") -join "`n"
    if ($PfriskCols -ne $ExpectedPfriskCols) {
        throw "FAIL: B5 (T-2) - v2_portfolio_risk_report column set/order mismatch."
    }
    $PfdefPk = Get-PyScalar -Sql "SELECT name FROM pragma_table_info('v2_portfolio_definition') WHERE pk > 0;" -Label "B5 pfdef pk"
    if ($PfdefPk -ne "id") { throw "FAIL: B5 (T-2) - pfdef primary key is not 'id'." }
    $PfriskPk = Get-PyScalar -Sql "SELECT name FROM pragma_table_info('v2_portfolio_risk_report') WHERE pk > 0;" -Label "B5 pfrisk pk"
    if ($PfriskPk -ne "id") { throw "FAIL: B5 (T-2) - pfrisk primary key is not 'id'." }
    $PfdefDdl = Get-PyScalar -Sql "SELECT sql FROM sqlite_master WHERE type='table' AND name='v2_portfolio_definition';" -Label "B5 pfdef DDL"
    foreach ($Anchor in @("uq_v2_pfdef_id_seq", "ck_v2_pfdef_basis", "ck_v2_pfdef_data_class")) {
        if ($PfdefDdl -notlike "*${Anchor}*") { throw "FAIL: B5 (T-2) - '${Anchor}' missing from v2_portfolio_definition DDL." }
    }
    $PfriskDdl = Get-PyScalar -Sql "SELECT sql FROM sqlite_master WHERE type='table' AND name='v2_portfolio_risk_report';" -Label "B5 pfrisk DDL"
    foreach ($Anchor in @("uq_v2_pfrisk_determinism_anchor", "ck_v2_pfrisk_status", "ck_v2_pfrisk_basis_label", "ck_v2_pfrisk_data_class")) {
        if ($PfriskDdl -notlike "*${Anchor}*") { throw "FAIL: B5 (T-2) - '${Anchor}' missing from v2_portfolio_risk_report DDL." }
    }
    $Be6IdxFound = Get-PyScalar -Sql "SELECT name FROM sqlite_master WHERE type='index' AND name IN ('ix_v2_pfdef_portfolio','ix_v2_pfrisk_def') ORDER BY name;" -Label "B5 BE-6 index names"
    if ($Be6IdxFound -ne ($Be6Indexes -join "`n")) {
        throw "FAIL: B5 (T-2/T-6) - the two BE-6 index names are not exactly the pinned set."
    }
    $PfdefAuto = Get-PyScalar -Sql "SELECT COUNT(*) FROM sqlite_master WHERE type='index' AND tbl_name='v2_portfolio_definition' AND name LIKE 'sqlite_autoindex%';" -Label "B5 pfdef autoindex census"
    if ([int]$PfdefAuto -lt 2) { throw "FAIL: B5 (T-2) - fewer than 2 autoindexes on v2_portfolio_definition." }
    $PfriskAuto = Get-PyScalar -Sql "SELECT COUNT(*) FROM sqlite_master WHERE type='index' AND tbl_name='v2_portfolio_risk_report' AND name LIKE 'sqlite_autoindex%';" -Label "B5 pfrisk autoindex census"
    if ([int]$PfriskAuto -lt 2) { throw "FAIL: B5 (T-2) - fewer than 2 autoindexes on v2_portfolio_risk_report." }
    Write-Evidence "PASS: B5 (T-2) - both BE-6 tables carry the pinned column name-sets with PK 'id'; all seven named constraints present in the stored DDL; both BE-6 indexes exact-named; autoindex census consistent with the PK + uniqueness anchors (behavioral proof in B7)."

    ''', 'V-R9-b5', keep_end=True)

# ============================================================
# V-R12. B7 PROBE SUITE
# ============================================================
rep_between('    Write-Section "B7. GUARD REFUSALS (ten; exact messages; transactional probes roll back) + CHECK probes"',
            '''    # -----------------------------------------------------------------
    # B8. AUTHORITY VARIABLES (absent)''',
            '''    Write-Section "B7. GUARD REFUSALS (four BE-6, exact messages; inherited compver guards intact on the new seed row; two behavioral uniqueness proofs; three CHECK probes)"

    Invoke-ExpectedRefusal -Label "B7: compver UPDATE on the BE-6 seed row (inherited guard intact)" -Sql "UPDATE v2_computation_version SET version='probe' WHERE component='portfolio_risk_engine';" -ExactMessage "V2 computation version registry is immutable; UPDATE prohibited"
    Invoke-ExpectedRefusal -Label "B7: compver DELETE on the BE-6 seed row (drop/re-created guard intact)" -Sql "DELETE FROM v2_computation_version WHERE component='portfolio_risk_engine';" -ExactMessage "V2 computation version registry is immutable; DELETE prohibited"

    $PfdefInsert = "INSERT INTO v2_portfolio_definition (id, portfolio_id, record_seq, name, basis, allocations, base_currency, data_class, assumptions, mode, operator_id, created_at) VALUES ('guardprobe', 'guardprobe', 1, 'guardprobe', 'hypothetical', '{}', 'EUR', 'synthetic', '{}', 'RESEARCH', 'guardprobe', '2026-09-03 00:00:00');"
    Invoke-ExpectedGuardProbe -Label "B7: portfolio-definition UPDATE" -InsertSql ${PfdefInsert} -ProbeSql "UPDATE v2_portfolio_definition SET name='probe' WHERE id='guardprobe';" -ExactMessage ${Be6UpdateMsgDef}
    Invoke-ExpectedGuardProbe -Label "B7: portfolio-definition DELETE" -InsertSql ${PfdefInsert} -ProbeSql "DELETE FROM v2_portfolio_definition WHERE id='guardprobe';" -ExactMessage ${Be6DeleteMsgDef}

    $PfriskInsert = "INSERT INTO v2_portfolio_risk_report (id, portfolio_definition_id, as_of, time_basis, input_refs, inputs_hash, metrics, scenarios, status, basis_label, data_class, engine_versions, engine_versions_hash, mode, operator_id, created_at) VALUES ('guardprobe', 'guardprobe', '2026-09-03 00:00:00', '{}', '[]', 'guardprobe-in', '{}', '[]', 'available', 'hypothetical-research', 'synthetic', '{}', 'guardprobe-eng', 'RESEARCH', 'guardprobe', '2026-09-03 00:00:00');"
    Invoke-ExpectedGuardProbe -Label "B7: portfolio-risk-report UPDATE" -InsertSql ${PfriskInsert} -ProbeSql "UPDATE v2_portfolio_risk_report SET status='stale' WHERE id='guardprobe';" -ExactMessage ${Be6UpdateMsgRep}
    Invoke-ExpectedGuardProbe -Label "B7: portfolio-risk-report DELETE" -InsertSql ${PfriskInsert} -ProbeSql "DELETE FROM v2_portfolio_risk_report WHERE id='guardprobe';" -ExactMessage ${Be6DeleteMsgRep}

    Invoke-ExpectedUniqProbe -Label "B7: uq_v2_pfdef_id_seq (portfolio_id, record_seq)" -Flavor "pfdef"
    Invoke-ExpectedUniqProbe -Label "B7: uq_v2_pfrisk_determinism_anchor (portfolio_definition_id, inputs_hash, engine_versions_hash)" -Flavor "pfrisk"

    Invoke-ExpectedRefusal -Label "B7: CHECK probe - basis 'real' refused (ck_v2_pfdef_basis)" -Sql "INSERT INTO v2_portfolio_definition (id, portfolio_id, record_seq, name, basis, allocations, base_currency, data_class, assumptions, mode, operator_id, created_at) VALUES ('checkprobe', 'checkprobe', 7, 'checkprobe', 'real', '{}', 'EUR', 'synthetic', '{}', 'RESEARCH', 'checkprobe', '2026-09-03 00:00:00');" -ExactMessage "CHECK"
    Invoke-ExpectedRefusal -Label "B7: CHECK probe - status 'bogus' refused (ck_v2_pfrisk_status)" -Sql "INSERT INTO v2_portfolio_risk_report (id, portfolio_definition_id, as_of, time_basis, input_refs, inputs_hash, metrics, scenarios, status, basis_label, data_class, engine_versions, engine_versions_hash, mode, operator_id, created_at) VALUES ('checkprobe', 'checkprobe', '2026-09-03 00:00:00', '{}', '[]', 'checkprobe-in', '{}', '[]', 'bogus', 'hypothetical-research', 'synthetic', '{}', 'checkprobe-eng', 'RESEARCH', 'checkprobe', '2026-09-03 00:00:00');" -ExactMessage "CHECK"
    Invoke-ExpectedRefusal -Label "B7: CHECK probe - basis_label 'account-state' refused (ck_v2_pfrisk_basis_label)" -Sql "INSERT INTO v2_portfolio_risk_report (id, portfolio_definition_id, as_of, time_basis, input_refs, inputs_hash, metrics, scenarios, status, basis_label, data_class, engine_versions, engine_versions_hash, mode, operator_id, created_at) VALUES ('checkprobe', 'checkprobe', '2026-09-03 00:00:00', '{}', '[]', 'checkprobe-in2', '{}', '[]', 'available', 'account-state', 'synthetic', '{}', 'checkprobe-eng2', 'RESEARCH', 'checkprobe', '2026-09-03 00:00:00');" -ExactMessage "CHECK"

    $EmptyAfter2 = Invoke-Py -PyArgs @("reportempty2", ${TargetDbPath}) -Label "B7 BE-6 tables empty after probes"
    if ((Norm-Text $EmptyAfter2).Trim() -ne "PASS:be6_tables_empty") {
        throw "FAIL: B7 - the BE-6 tables are not empty after the probes."
    }
    $EmptyAfter5 = Invoke-Py -PyArgs @("reportempty5", ${TargetDbPath}) -Label "B7 BE-5 tables still empty after probes"
    if ((Norm-Text $EmptyAfter5).Trim() -ne "PASS:be5_tables_empty") {
        throw "FAIL: B7 - the BE-5 tables are not empty after the probes."
    }
    Write-Evidence "PASS: B7 - all four BE-6 guard refusals observed with the exact pinned messages; the inherited compver guards intact on the new seed row; both uniqueness anchors proven behaviorally; all three CHECK probes refused; throwaway rows rolled back; tables confirmed empty."

    ''', 'V-R12-b7', keep_end=True)

# ============================================================
# V-R13. B9 DRIFT
# ============================================================
rep('    $DriftBanPattern = "v2_ml_governance_record|v2_ml_lifecycle_event|v2_ml_diagnostic_report|v2_signal_record|v2_signal_state_event|mlgov|mlev|mldiag|sigev|v2_md_|v2_permission|v2_computation_version|v2_market_context|v2_chart_intelligence|v2_audit_event|v2_lineage_record|ix_v2_"',
    '    $DriftBanPattern = "v2_portfolio_definition|v2_portfolio_risk_report|pfdef|pfrisk|v2_ml_governance_record|v2_ml_lifecycle_event|v2_ml_diagnostic_report|v2_signal_record|v2_signal_state_event|mlgov|mlev|mldiag|sigev|v2_md_|v2_permission|v2_computation_version|v2_market_context|v2_chart_intelligence|v2_audit_event|v2_lineage_record|ix_v2_"', 'V-R13-ban')
rep('        throw "FAIL: B9 (T-10) - V2/BE-5 drift token detected in alembic check output."',
    '        throw "FAIL: B9 (T-10) - V2/BE-6 drift token detected in alembic check output."', 'V-R13-banfail')
rep('        $DriftNote = "summary format (PGF-014): drift existence asserted (non-zero exit + a recorded drift marker); no V2/BE-5 token anywhere; the exact token set stands per the Level-II test evidence and the recorded lineage"',
    '        $DriftNote = "summary format (PGF-014): drift existence asserted (non-zero exit + a recorded drift marker); no V2/BE-5/BE-6 token anywhere; the exact token set stands per the Level-II test evidence and the recorded lineage"', 'V-R13-note')
rep('Write-Section "B9. DRIFT: alembic check (expected: exactly the 9 inherited V1 tokens; zero BE-5/V2 tokens)"',
    'Write-Section "B9. DRIFT: alembic check (expected: exactly the 9 inherited V1 tokens; zero BE-6/V2 tokens)"', 'V-R13-section')

# ============================================================
# V-R14. B10 VERDICT + ENVELOPE
# ============================================================
rep('''    Write-Evidence "VERIFY VERDICT: PASS - the working database in '${TargetDbPath}' is byte-identical to the PASS-state recorded by the apply act and independently re-proves the BO-V2-BE-5-001 terminal state: revision 20260902_0045; 28 v2 triggers (ten BE-5 guards exact-messaged; inherited guards intact); five BE-5 tables with anchors and six indexes; 5 computation-version rows (mge/sge hashes runtime-recomputed); 35 permission rows (8 additive BE-5 exact); five BE-5 tables empty; inherited BE-1..BE-3 anchors content-exact; drift exactly the 9 inherited V1 tokens with zero BE-5/V2 tokens; no authority variable present; recovery anchor verified."
    Write-Evidence "Transcript: ${Transcript}"
    Write-Evidence ""
    Write-Evidence "EVIDENCE ENVELOPE TO SEND TO ITRGA (closes C-2):"
    Write-Evidence "  operator-evidence\\BE-5\\0045-APPLY-RUN-V1.txt"
    Write-Evidence "  operator-evidence\\BE-5\\0045-VERIFY-RUN-V1.txt"
    Write-Evidence "The application may now be restarted."''',
    '''    Write-Evidence "VERIFY VERDICT: PASS - the working database in '${TargetDbPath}' is byte-identical to the PASS-state recorded by the apply act and independently re-proves the BO-V2-BE-6-001 terminal state on the working lineage: revision exactly 20260903_0046 (transcript of record attests the single sanctioned upgrade); 32 v2 triggers exact-named (28 inherited intact + 4 BE-6 guards exact-messaged); both BE-6 tables with the pinned column name-sets, PK 'id', all seven named constraints in the stored DDL, both uniqueness anchors PROVEN BEHAVIORALLY and both indexes exact-named; 6 computation-version rows (BE-4 pinned by value; mge/sge and portfolio_risk_engine runtime-recomputed, the BE-6 recomputation equal to the pinned anchor); 41 permission rows (6 additive BE-6 exact, no duplicates); both BE-6 tables empty and all five BE-5 tables still empty; inherited BE-1..BE-3 anchors content-exact; drift exactly the 9 inherited V1 tokens with zero BE-6/V2 tokens; no authority variable present; recovery anchor (current-as-is, pre-act disclosure N-1) verified byte-exact against the apply record."
    Write-Evidence "Transcript: ${Transcript}"
    Write-Evidence ""
    Write-Evidence "EVIDENCE ENVELOPE TO SEND TO ITRGA (closes the 0046 application act):"
    Write-Evidence "  operator-evidence\\BE-6\\0046-APPLY-RUN-V1.txt"
    Write-Evidence "  operator-evidence\\BE-6\\0046-VERIFY-RUN-V1.txt"
    Write-Evidence "The application may now be restarted."''', 'V-R14-verdict')

# ============================================================
# V-R15 (applied FIRST): the embedded python helper becomes
# byte-identical to the 0046 apply pack's proven helper (it already
# carries BE6_FILES, the extended command tuple and the compverbe6 /
# permbe6 / reportempty2 / uniqbe6 verbs), so the six V-R4 splice ops
# are subsumed and skipped.
_ap_h_start = a.find("$HelperSource = @'")
_ap_h_end = a.find("\n'@", _ap_h_start) + 3
_vf_h_start = s.find("$HelperSource = @'")
_vf_h_end = s.find("\n'@", _vf_h_start) + 3
assert _ap_h_start > 0 and _ap_h_end > 3 and _vf_h_start > 0 and _vf_h_end > 3
ops2 = [(s[_vf_h_start:_vf_h_end], a[_ap_h_start:_ap_h_end], 'V-R15-helper-byte-identity')]
skipped = []
for old, new, tag in ops:
    if tag.startswith('V-R4'):
        skipped.append(tag)
        continue
    ops2.append((old, new, tag))

for old, new, tag in ops2:
    assert s.count(old) == 1, ('final-anchor-fail', tag, s.count(old))
    s = s.replace(old, new, 1)
io.open(DST, 'w', encoding='utf-8', newline='\n').write(s)
print('VERIFY BUILD OK:', len(ops2), 'ops applied,', len(skipped), 'helper splices subsumed;',
      s.count(chr(10)) + 1, 'lines')
