#!/usr/bin/env python3
# Part 2: A2..A8 transformation on stage1.ps1 -> final pack.
import io, sys

s = io.open('/home/user/scratch/stage1.ps1', encoding='utf-8').read()
ops = []

def rep(old, new, tag):
    n = s.count(old)
    if n != 1:
        print('ANCHOR-COUNT-FAIL', tag, n); sys.exit(1)
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

# ============================================================
# R9. Header arithmetic correction (part-1 said 41/32; truth: 36/27)
# ============================================================
rep('''#      delivered (the packs re-pin all 41 provenance files by hash and
#      abort on ANY deviation: 9 chain migrations + 32 delivered BE-5 /
#      BE-6 files).''',
    '''#      delivered (the packs re-pin all 36 provenance files by hash and
#      abort on ANY deviation: 9 chain migrations + 27 delivered files;
#      the BE-5 and BE-6 delivered sets merged, with the four shared
#      paths pinned to the BE-6 Rev-2 literals).''', 'R9-headercount')

# ============================================================
# R10. A2 ANCHOR (filename + disclosure prose)
# ============================================================
rep('''    Write-Section "A2. ANCHOR (file-level backup; first side effect; evidence directory only)"

    $BackupStamp = Get-Date -Format "yyyyMMddHHmmss"
    $MainBackupPath = Join-Path $EvidenceDir (${LeafName} + ".pre-0045-" + ${BackupStamp} + ".bak")''',
    '''    Write-Section "A2. ANCHOR (file-level backup; first side effect; evidence directory only)"

    $BackupStamp = Get-Date -Format "yyyyMMddHHmmss"
    $MainBackupPath = Join-Path $EvidenceDir (${LeafName} + ".pre-0046-" + ${BackupStamp} + ".bak")''', 'R10-backupname')
rep('''    Write-Evidence "PASS: A2 - a proven rollback anchor exists before any mutation."''',
    '''    Write-Evidence "NOTE (pre-act disclosure N-1): the anchor binds the CURRENT-AS-IS image (it lawfully includes the post-0045 restart's bootstrap-admin row); the 0045-era byte pin is recorded only. Rollback restores exactly this image."
    Write-Evidence "PASS: A2 - a proven rollback anchor exists before any mutation."''', 'R10-anchornote')

# ============================================================
# R11. A3 PROVENANCE (9 chain + 27 delivered = 36 files)
# ============================================================
rep('Write-Section "A3. PROVENANCE (25 files re-pinned on disk: 8 chain migrations + 17 delivered BE-5 files; abort on any mismatch)"',
    'Write-Section "A3. PROVENANCE (36 files re-pinned on disk: 9 chain migrations + 27 delivered files; abort on any mismatch)"', 'R11-section')
rep('''        "20260902_0045_v2_be5_signal_contracts.py"
    )) {''',
    '''        "20260902_0045_v2_be5_signal_contracts.py",
        "20260903_0046_v2_be6_portfolio_research.py"
    )) {''', 'R11-chainlist')
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
    )) {''', 'R11-deliveredlist')
rep('Write-Evidence "PASS: A3 - all 25 files on disk hash to the pinned values (8 chain migrations 0038-0045; 17 delivered BE-5 files per REM-001 Rev 2)."',
    'Write-Evidence "PASS: A3 - all 36 files on disk hash to the pinned values (9 chain migrations 0038-0046; 27 delivered BE-5/BE-6 files per REM-001 Rev 2 and REM-Rev-2; the four shared paths pinned to the BE-6 Rev-2 literals)."', 'R11-pass')

# ============================================================
# R12. A4/A5 gates
# ============================================================
rep('Write-Evidence "PASS: A5.1 (T-1) - current revision is exactly ${ApplyTargetRevision} (chain 0043 -> 0044 -> 0045)."',
    'Write-Evidence "PASS: A5.1 (T-1) - current revision is exactly ${ApplyTargetRevision} (chain 0043 -> 0044 -> 0045 -> 0046)."', 'R12-a51')

# A5.2 trigger census block -> 32, added set = Be6GuardNames
rep_between('''    # A5.2: exactly 28 v2 triggers; set difference vs baseline exactly''',
            '''    # A5.3: the five tables; the two UNIQUE anchors; the six indexes (T-2/T-6).''',
            '''    # A5.2: exactly 32 v2 triggers; set difference vs baseline exactly
    # the four BE-6 guards (T-3/T-6; 28 -> 32).
    [void](Invoke-Py -PyArgs @("scalar", ${TargetDbPath}, "SELECT name FROM sqlite_master WHERE type='trigger' AND name LIKE 'v2_%' ORDER BY name;") -Label "A5 v2 trigger names (recorded)")
    $PostTrigNamesText = Get-PyScalar -Sql "SELECT name FROM sqlite_master WHERE type='trigger' AND name LIKE 'v2_%' ORDER BY name;" -Label "A5 v2 trigger set"
    $PostTrigNames = @($PostTrigNamesText -split "`n" | Where-Object { $_ -ne "" })
    if ($PostTrigNames.Count -ne 32) {
        throw "FAIL: A5 (T-3/T-6) - v2 trigger count '$($PostTrigNames.Count)', expected exactly 32 (28 + 4)."
    }
    $AddedNames = @($PostTrigNames | Where-Object { $PreTrigNames -notcontains $_ })
    $AddedSorted = @($AddedNames | Sort-Object)
    $ExpectedAddedSorted = @($Be6GuardNames | Sort-Object)
    if (($AddedSorted -join "`n") -ne ($ExpectedAddedSorted -join "`n")) {
        throw "FAIL: A5 (T-3/T-6) - the added trigger set is not exactly the four pinned BE-6 guards: added [$($AddedSorted -join ', ')]."
    }
    $RemovedNames = @($PreTrigNames | Where-Object { $PostTrigNames -notcontains $_ })
    if ($RemovedNames.Count -ne 0) {
        throw "FAIL: A5 (T-3/T-6) - inherited trigger(s) missing after the apply: [$($RemovedNames -join ', ')]."
    }
    Write-Evidence "PASS: A5.2 (T-3/T-6) - 32 v2 triggers; the added set is exactly the four BE-6 guard names; the 28 inherited are intact."

''', 'R12-a52', keep_end=True)

# A5.3 -> BE-6 schema census block
rep_between('''    # A5.3: the five tables; the two UNIQUE anchors; the six indexes (T-2/T-6).''',
            '''    # A5.4: computation-version rows exactly 5; BE-5 hashes proven by''',
            '''    # A5.3: the two BE-6 tables with their pinned columns (PRAGMA
    # name-sets; PGF-015), the named constraints in the stored DDL, the
    # two indexes, PK census; the BE-5 six-index set re-proven intact.
    $NewTableCount = Get-PyScalar -Sql "SELECT COUNT(*) FROM sqlite_master WHERE type='table' AND name IN ('v2_portfolio_definition','v2_portfolio_risk_report');" -Label "A5 BE-6 table presence"
    if ($NewTableCount -ne "2") {
        throw "FAIL: A5 (T-2/T-6) - BE-6 table count '${NewTableCount}', expected 2."
    }
    $PfdefCols = Get-PyScalar -Sql "SELECT name FROM pragma_table_info('v2_portfolio_definition') ORDER BY cid;" -Label "A5 v2_portfolio_definition columns"
    $ExpectedPfdefCols = @("id","portfolio_id","record_seq","supersedes","name","basis","allocations","base_currency","data_class","assumptions","mode","operator_id","correlation_id","created_at") -join "`n"
    if ($PfdefCols -ne $ExpectedPfdefCols) {
        throw "FAIL: A5 (T-2) - v2_portfolio_definition column set/order mismatch: '${PfdefCols}'."
    }
    $PfdefPk = Get-PyScalar -Sql "SELECT name FROM pragma_table_info('v2_portfolio_definition') WHERE pk > 0;" -Label "A5 pfdef primary key"
    if ($PfdefPk -ne "id") { throw "FAIL: A5 (T-2) - v2_portfolio_definition primary key is '${PfdefPk}', expected 'id'." }
    $PfriskCols = Get-PyScalar -Sql "SELECT name FROM pragma_table_info('v2_portfolio_risk_report') ORDER BY cid;" -Label "A5 v2_portfolio_risk_report columns"
    $ExpectedPfriskCols = @("id","portfolio_definition_id","as_of","time_basis","input_refs","inputs_hash","metrics","scenarios","status","basis_label","data_class","engine_versions","engine_versions_hash","mode","operator_id","correlation_id","created_at") -join "`n"
    if ($PfriskCols -ne $ExpectedPfriskCols) {
        throw "FAIL: A5 (T-2) - v2_portfolio_risk_report column set/order mismatch: '${PfriskCols}'."
    }
    $PfriskPk = Get-PyScalar -Sql "SELECT name FROM pragma_table_info('v2_portfolio_risk_report') WHERE pk > 0;" -Label "A5 pfrisk primary key"
    if ($PfriskPk -ne "id") { throw "FAIL: A5 (T-2) - v2_portfolio_risk_report primary key is '${PfriskPk}', expected 'id'." }
    $PfdefDdl = Get-PyScalar -Sql "SELECT sql FROM sqlite_master WHERE type='table' AND name='v2_portfolio_definition';" -Label "A5 pfdef DDL"
    foreach ($Anchor in @("uq_v2_pfdef_id_seq", "ck_v2_pfdef_basis", "ck_v2_pfdef_data_class")) {
        if ($PfdefDdl -notlike "*${Anchor}*") {
            throw "FAIL: A5 (T-2) - named constraint '${Anchor}' not present in v2_portfolio_definition DDL."
        }
    }
    $PfriskDdl = Get-PyScalar -Sql "SELECT sql FROM sqlite_master WHERE type='table' AND name='v2_portfolio_risk_report';" -Label "A5 pfrisk DDL"
    foreach ($Anchor in @("uq_v2_pfrisk_determinism_anchor", "ck_v2_pfrisk_status", "ck_v2_pfrisk_basis_label", "ck_v2_pfrisk_data_class")) {
        if ($PfriskDdl -notlike "*${Anchor}*") {
            throw "FAIL: A5 (T-2) - named constraint '${Anchor}' not present in v2_portfolio_risk_report DDL."
        }
    }
    # Index census (name-set only; PGF-015): the two named BE-6 indexes
    # exact; the uniqueness anchors appear as sqlite_autoindex entries
    # (PK + UNIQUE on each table) and are proven BEHAVIORALLY in A6.
    $Be6IdxFound = Get-PyScalar -Sql "SELECT name FROM sqlite_master WHERE type='index' AND name IN ('ix_v2_pfdef_portfolio','ix_v2_pfrisk_def') ORDER BY name;" -Label "A5 BE-6 index names"
    $ExpectedBe6IndexesText = $Be6Indexes -join "`n"
    if ($Be6IdxFound -ne $ExpectedBe6IndexesText) {
        throw "FAIL: A5 (T-2/T-6) - the two BE-6 index names are not exactly the pinned set: '${Be6IdxFound}'."
    }
    $PfdefAuto = Get-PyScalar -Sql "SELECT COUNT(*) FROM sqlite_master WHERE type='index' AND tbl_name='v2_portfolio_definition' AND name LIKE 'sqlite_autoindex%';" -Label "A5 pfdef autoindex census"
    if ([int]$PfdefAuto -lt 2) { throw "FAIL: A5 (T-2) - fewer than 2 autoindexes on v2_portfolio_definition (PK + UNIQUE anchor expected)." }
    $PfriskAuto = Get-PyScalar -Sql "SELECT COUNT(*) FROM sqlite_master WHERE type='index' AND tbl_name='v2_portfolio_risk_report' AND name LIKE 'sqlite_autoindex%';" -Label "A5 pfrisk autoindex census"
    if ([int]$PfriskAuto -lt 2) { throw "FAIL: A5 (T-2) - fewer than 2 autoindexes on v2_portfolio_risk_report (PK + UNIQUE anchor expected)." }
    # BE-5 schema set stays intact (no-touch, schema side).
    $IdxFound = Get-PyScalar -Sql "SELECT name FROM sqlite_master WHERE type='index' AND name IN ('ix_v2_mlgov_artifact','ix_v2_mlev_record','ix_v2_mldiag_artifact','ix_v2_sigev_signal','ix_v2_signal_family_state','ix_v2_signal_instrument') ORDER BY name;" -Label "A5 BE-5 index names (intact re-proof)"
    $ExpectedIndexesText = $Be5Indexes -join "`n"
    if ($IdxFound -ne $ExpectedIndexesText) {
        throw "FAIL: A5 (T-9) - the six BE-5 index names are no longer exactly the pinned set: '${IdxFound}'."
    }
    $Be5TableCountNow = Get-PyScalar -Sql "SELECT COUNT(*) FROM sqlite_master WHERE type='table' AND name IN ('v2_ml_governance_record','v2_ml_lifecycle_event','v2_ml_diagnostic_report','v2_signal_record','v2_signal_state_event');" -Label "A5 BE-5 tables intact"
    if ($Be5TableCountNow -ne "5") {
        throw "FAIL: A5 (T-9) - BE-5 table count changed ('${Be5TableCountNow}')."
    }
    Write-Evidence "PASS: A5.3 (T-2/T-6) - the two BE-6 tables present with the pinned column name-sets and PK 'id'; all seven named constraints present in the stored DDL; the two BE-6 indexes exact-named; autoindex census consistent with the PK + uniqueness anchors (behavioral proof in A6); the BE-5 schema set intact."

''', 'R12-a53', keep_end=True)

# A5.4 -> compverbe6
rep_between('''    # A5.4: computation-version rows exactly 5; BE-5 hashes proven by''',
            '''    # A5.5: permission rows (T-4/T-6): 8 additive BE-5 content-exact;''',
            '''    # A5.4: computation-version rows exactly 6 (T-5/T-6; P-4): BE-4
    # pinned by value; mge/sge AND the BE-6 anchor by RUNTIME
    # RECOMPUTATION of the engine files; the recomputed BE-6 value is
    # asserted equal to the pinned anchor before the row check.
    $CompverOut = Invoke-Py -PyArgs @(
        "compverbe6", ${TargetDbPath}, ${BackendRoot},
        "fe9aab42c34d671e960fd92a9346d3bf60c27135e76e52310d774bc84028dd35",
        "69902503483502bcd5ce5e35fdb0eeabcb2efcaf7a4b0c262a6fccf2d0af3a8c",
        "3887d6ca8ba05858f41889cd99fa05aba42663ac22d906a7f989b567c3912180",
        ${Be6EngineAnchor}
    ) -Label "A5 computation-version rows (6; mge/sge/BE-6 recomputed)"
    $CompverText = (Norm-Text $CompverOut).Trim()
    if ($CompverText -notlike "PASS:compver6_rows_exact*") {
        throw "FAIL: A5 (T-5/T-6) - computation-version check failed: ${CompverText}"
    }
    if ($CompverText -notlike "*INFO:pre_recomputed=${Be6EngineAnchor}*") {
        throw "FAIL: A5 (T-5/T-6; P-4) - the runtime-recomputed BE-6 engine anchor does not equal the pinned anchor."
    }
    Write-Evidence "PASS: A5.4 (T-5/T-6; P-4) - exactly 6 computation-version rows; BE-4 rows content-exact; mge/sge source hashes equal the runtime recomputation; the portfolio_risk_engine row (pre-1.0.0, evidence_ref BO-V2-BE-6-001) hash equals the runtime recomputation of the four pinned files AND the pinned anchor."

''', 'R12-a54', keep_end=True)

# A5.5 -> permbe6
rep_between('''    # A5.5: permission rows (T-4/T-6): 8 additive BE-5 content-exact;''',
            '''    # A5.6: the five BE-5 tables are empty (T-2/T-6 posture).''',
            '''    # A5.5: permission rows (T-4/T-6): 6 additive BE-6 content-exact;
    # total exactly 41; no role+permission duplicates.
    $PermOut = Invoke-Py -PyArgs @("permbe6", ${TargetDbPath}) -Label "A5 permission rows (BE-6 additive set; total 41)"
    $PermText = (Norm-Text $PermOut).Trim()
    if ($PermText -notlike "PASS:perm6_rows_exact*") {
        throw "FAIL: A5 (T-4/T-6) - permission check failed: ${PermText}"
    }
    if ($PermText -notlike "*INFO:v2_permission_total=41*") {
        throw "FAIL: A5 (T-4/T-6) - permission total is not exactly 41."
    }
    Write-Evidence "PASS: A5.5 (T-4/T-6) - exactly 6 additive BE-6 permission rows (admin x4 incl. portfolio.define and portfolio_risk.compute at SAL-3, operator x2; SAL-aligned) content-exact; total 41; no role+permission duplicates."

''', 'R12-a55', keep_end=True)

# A5.6 -> both empty
rep('''    # A5.6: the five BE-5 tables are empty (T-2/T-6 posture).
    $EmptyOut = Invoke-Py -PyArgs @("reportempty5", ${TargetDbPath}) -Label "A5 BE-5 tables empty"
    $EmptyText = (Norm-Text $EmptyOut).Trim()
    if ($EmptyText -ne "PASS:be5_tables_empty") {
        throw "FAIL: A5 - the BE-5 tables are not empty: ${EmptyText}"
    }
    Write-Evidence "PASS: A5.6 - all five BE-5 tables are empty."''',
    '''    # A5.6: the two BE-6 tables are empty; the five BE-5 tables stay empty.
    $EmptyOut2 = Invoke-Py -PyArgs @("reportempty2", ${TargetDbPath}) -Label "A5 BE-6 tables empty"
    $EmptyText2 = (Norm-Text $EmptyOut2).Trim()
    if ($EmptyText2 -ne "PASS:be6_tables_empty") {
        throw "FAIL: A5 - the BE-6 tables are not empty: ${EmptyText2}"
    }
    $EmptyOut5 = Invoke-Py -PyArgs @("reportempty5", ${TargetDbPath}) -Label "A5 BE-5 tables still empty"
    $EmptyText5 = (Norm-Text $EmptyOut5).Trim()
    if ($EmptyText5 -ne "PASS:be5_tables_empty") {
        throw "FAIL: A5 (T-9) - the BE-5 tables are not empty: ${EmptyText5}"
    }
    Write-Evidence "PASS: A5.6 - both BE-6 tables are empty; all five BE-5 tables remain empty."''', 'R12-a56')

# A5.7 no-touch
rep_between('''    # A5.7: inherited state untouched (no-touch proof).''',
            '''    # A5.8: file posture after the apply.''',
            '''    # A5.7: inherited state untouched (no-touch proof): provider row,
    # history and audit anchors content-exact; the four record-only
    # digests IDENTICAL pre/post; BE-4 compver rows intact.
    $ProvNow = Get-PyScalar -Sql "SELECT source_status, entitlement_status, persistence_permitted FROM v2_md_provider WHERE provider_id='twelvedata';" -Label "A5 inherited provider row"
    if ($ProvNow -ne "contract_tested|verified|0") {
        throw "FAIL: A5 (T-9) - inherited provider row changed: '${ProvNow}'."
    }
    $RowsNow = Invoke-Py -PyArgs @("verifyrows", ${TargetDbPath}) -Label "A5 inherited history exact-content"
    if ((Norm-Text $RowsNow).Trim() -ne "PASS:history_rows_exact") {
        throw "FAIL: A5 (T-9) - inherited history content changed."
    }
    $AuditNow = Invoke-Py -PyArgs @("verifyaudit", ${TargetDbPath}) -Label "A5 inherited audit exact-content"
    if ((Norm-Text $AuditNow).Trim() -ne "PASS:audit_rows_exact") {
        throw "FAIL: A5 (T-9) - inherited audit content changed."
    }
    $AuditDigestPost = Invoke-Py -PyArgs @("tabledigest", ${TargetDbPath}, "v2_audit_event") -Label "A5 audit-event table digest (post)"
    if ((Norm-Text $AuditDigestPost).Trim() -ne (Norm-Text $AuditDigestPre).Trim()) {
        throw "FAIL: A5 (T-9) - v2_audit_event content changed across the apply."
    }
    $LineageDigestPost = Invoke-Py -PyArgs @("tabledigest", ${TargetDbPath}, "v2_lineage_record") -Label "A5 lineage-record table digest (post)"
    if ((Norm-Text $LineageDigestPost).Trim() -ne (Norm-Text $LineageDigestPre).Trim()) {
        throw "FAIL: A5 (T-9) - v2_lineage_record content changed across the apply."
    }
    $McrDigestPost = Invoke-Py -PyArgs @("tabledigest", ${TargetDbPath}, "v2_market_context_report") -Label "A5 BE-4 market-context report digest (post)"
    if ((Norm-Text $McrDigestPost).Trim() -ne (Norm-Text $McrDigestPre).Trim()) {
        throw "FAIL: A5 (T-9) - v2_market_context_report content changed across the apply."
    }
    $CirDigestPost = Invoke-Py -PyArgs @("tabledigest", ${TargetDbPath}, "v2_chart_intelligence_report") -Label "A5 BE-4 chart-intelligence report digest (post)"
    if ((Norm-Text $CirDigestPost).Trim() -ne (Norm-Text $CirDigestPre).Trim()) {
        throw "FAIL: A5 (T-9) - v2_chart_intelligence_report content changed across the apply."
    }
    $Be4CompverCountNow = Get-PyScalar -Sql "SELECT COUNT(*) FROM v2_computation_version WHERE component IN ('indicator_engine','market_context_engine','chart_intelligence_engine');" -Label "A5 BE-4 compver rows intact"
    if ($Be4CompverCountNow -ne "3") {
        throw "FAIL: A5 (T-9) - BE-4 computation-version rows not intact: '${Be4CompverCountNow}'."
    }
    Write-Evidence "PASS: A5.7 (T-9) - inherited BE-1..BE-5 state untouched: provider row, history, audit anchors content-exact; v2_audit_event / v2_lineage_record / both BE-4 report-table digests identical pre/post; BE-4 compver rows intact."

''', 'R12-a57', keep_end=True)

# ============================================================
# R13. A6 PROBE SUITE (whole block)
# ============================================================
rep_between('''    Write-Section "A6. GUARD SPOT-CHECKS (ten refusals; exact messages; two CHECK-vocabulary probes)"''',
            '''    # -----------------------------------------------------------------
    # A7. DRIFT RE-BASELINE (format-independent; PGF-014)''',
            '''    Write-Section "A6. GUARD SPOT-CHECKS (four BE-6 refusals with exact messages; inherited compver guards intact; two behavioral uniqueness proofs; three CHECK-vocabulary probes)"

    # compver holds six seed rows: direct UPDATE/DELETE probes fire on
    # any of them (inherited 0043 guards; the DELETE guard was dropped
    # and re-created inside the migration - exact intact proof here).
    Invoke-ExpectedRefusal -Label "A6: compver UPDATE on the BE-6 seed row (inherited guard intact)" -Sql "UPDATE v2_computation_version SET version='probe' WHERE component='portfolio_risk_engine';" -ExactMessage "V2 computation version registry is immutable; UPDATE prohibited"
    Invoke-ExpectedRefusal -Label "A6: compver DELETE on the BE-6 seed row (drop/re-created guard intact)" -Sql "DELETE FROM v2_computation_version WHERE component='portfolio_risk_engine';" -ExactMessage "V2 computation version registry is immutable; DELETE prohibited"

    # The two BE-6 tables are empty: transactional probe cycles (insert
    # a CHECK-conforming throwaway row; fire the guard; roll back).
    $PfdefInsert = "INSERT INTO v2_portfolio_definition (id, portfolio_id, record_seq, name, basis, allocations, base_currency, data_class, assumptions, mode, operator_id, created_at) VALUES ('guardprobe', 'guardprobe', 1, 'guardprobe', 'hypothetical', '{}', 'EUR', 'synthetic', '{}', 'RESEARCH', 'guardprobe', '2026-09-03 00:00:00');"
    Invoke-ExpectedGuardProbe -Label "A6: portfolio-definition UPDATE" -InsertSql ${PfdefInsert} -ProbeSql "UPDATE v2_portfolio_definition SET name='probe' WHERE id='guardprobe';" -ExactMessage ${Be6UpdateMsgDef}
    Invoke-ExpectedGuardProbe -Label "A6: portfolio-definition DELETE" -InsertSql ${PfdefInsert} -ProbeSql "DELETE FROM v2_portfolio_definition WHERE id='guardprobe';" -ExactMessage ${Be6DeleteMsgDef}

    $PfriskInsert = "INSERT INTO v2_portfolio_risk_report (id, portfolio_definition_id, as_of, time_basis, input_refs, inputs_hash, metrics, scenarios, status, basis_label, data_class, engine_versions, engine_versions_hash, mode, operator_id, created_at) VALUES ('guardprobe', 'guardprobe', '2026-09-03 00:00:00', '{}', '[]', 'guardprobe-in', '{}', '[]', 'available', 'hypothetical-research', 'synthetic', '{}', 'guardprobe-eng', 'RESEARCH', 'guardprobe', '2026-09-03 00:00:00');"
    Invoke-ExpectedGuardProbe -Label "A6: portfolio-risk-report UPDATE" -InsertSql ${PfriskInsert} -ProbeSql "UPDATE v2_portfolio_risk_report SET status='stale' WHERE id='guardprobe';" -ExactMessage ${Be6UpdateMsgRep}
    Invoke-ExpectedGuardProbe -Label "A6: portfolio-risk-report DELETE" -InsertSql ${PfriskInsert} -ProbeSql "DELETE FROM v2_portfolio_risk_report WHERE id='guardprobe';" -ExactMessage ${Be6DeleteMsgRep}

    # Behavioural uniqueness proofs (PGF-015; the anchors are proven by
    # attempted duplicate inserts, never by catalog introspection).
    Invoke-ExpectedUniqProbe -Label "A6: uq_v2_pfdef_id_seq (portfolio_id, record_seq)" -Flavor "pfdef"
    Invoke-ExpectedUniqProbe -Label "A6: uq_v2_pfrisk_determinism_anchor (portfolio_definition_id, inputs_hash, engine_versions_hash)" -Flavor "pfrisk"

    # CHECK-vocabulary probes (INSERT is allowed by the guards; the
    # named CHECK constraints must refuse).
    Invoke-ExpectedRefusal -Label "A6: CHECK probe - basis 'real' refused (ck_v2_pfdef_basis)" -Sql "INSERT INTO v2_portfolio_definition (id, portfolio_id, record_seq, name, basis, allocations, base_currency, data_class, assumptions, mode, operator_id, created_at) VALUES ('checkprobe', 'checkprobe', 7, 'checkprobe', 'real', '{}', 'EUR', 'synthetic', '{}', 'RESEARCH', 'checkprobe', '2026-09-03 00:00:00');" -ExactMessage "CHECK"
    Invoke-ExpectedRefusal -Label "A6: CHECK probe - status 'bogus' refused (ck_v2_pfrisk_status)" -Sql "INSERT INTO v2_portfolio_risk_report (id, portfolio_definition_id, as_of, time_basis, input_refs, inputs_hash, metrics, scenarios, status, basis_label, data_class, engine_versions, engine_versions_hash, mode, operator_id, created_at) VALUES ('checkprobe', 'checkprobe', '2026-09-03 00:00:00', '{}', '[]', 'checkprobe-in', '{}', '[]', 'bogus', 'hypothetical-research', 'synthetic', '{}', 'checkprobe-eng', 'RESEARCH', 'checkprobe', '2026-09-03 00:00:00');" -ExactMessage "CHECK"
    Invoke-ExpectedRefusal -Label "A6: CHECK probe - basis_label 'account-state' refused (ck_v2_pfrisk_basis_label)" -Sql "INSERT INTO v2_portfolio_risk_report (id, portfolio_definition_id, as_of, time_basis, input_refs, inputs_hash, metrics, scenarios, status, basis_label, data_class, engine_versions, engine_versions_hash, mode, operator_id, created_at) VALUES ('checkprobe', 'checkprobe', '2026-09-03 00:00:00', '{}', '[]', 'checkprobe-in2', '{}', '[]', 'available', 'account-state', 'synthetic', '{}', 'checkprobe-eng2', 'RESEARCH', 'checkprobe', '2026-09-03 00:00:00');" -ExactMessage "CHECK"

    # Probe hygiene: all throwaway rows rolled back; both BE-6 tables
    # and all five BE-5 tables still empty.
    $EmptyAfter2 = Invoke-Py -PyArgs @("reportempty2", ${TargetDbPath}) -Label "A6 BE-6 tables empty after probes"
    if ((Norm-Text $EmptyAfter2).Trim() -ne "PASS:be6_tables_empty") {
        throw "FAIL: A6 - the BE-6 tables are not empty after the probes."
    }
    $EmptyAfter5 = Invoke-Py -PyArgs @("reportempty5", ${TargetDbPath}) -Label "A6 BE-5 tables still empty after probes"
    if ((Norm-Text $EmptyAfter5).Trim() -ne "PASS:be5_tables_empty") {
        throw "FAIL: A6 - the BE-5 tables are not empty after the probes."
    }
    [void](Assert-CurrentExactly -ExpectedRev ${ApplyTargetRevision} -Label "A6 revision stable after probes")
    Write-Evidence "PASS: A6 - all four BE-6 guard refusals observed with the exact pinned messages; the inherited compver guards intact on the new seed row (incl. the drop/re-created DELETE guard); both uniqueness anchors proven behaviorally; all three CHECK probes refused; throwaway rows rolled back; tables confirmed empty; revision stable."

    ''', 'R13-a6', keep_end=True)

# ============================================================
# R14. A7 drift: extended ban pattern + wording
# ============================================================
rep('    $DriftBanPattern = "v2_ml_governance_record|v2_ml_lifecycle_event|v2_ml_diagnostic_report|v2_signal_record|v2_signal_state_event|mlgov|mlev|mldiag|sigev|v2_md_|v2_permission|v2_computation_version|v2_market_context|v2_chart_intelligence|v2_audit_event|v2_lineage_record|ix_v2_"',
    '    $DriftBanPattern = "v2_portfolio_definition|v2_portfolio_risk_report|pfdef|pfrisk|v2_ml_governance_record|v2_ml_lifecycle_event|v2_ml_diagnostic_report|v2_signal_record|v2_signal_state_event|mlgov|mlev|mldiag|sigev|v2_md_|v2_permission|v2_computation_version|v2_market_context|v2_chart_intelligence|v2_audit_event|v2_lineage_record|ix_v2_"', 'R14-ban')
rep('''        throw "FAIL: A7 (T-10) - V2/BE-5 drift token detected in alembic check output; after the 0045 apply the BE-5 schema set must have left the drift set."''',
    '''        throw "FAIL: A7 (T-10) - V2/BE-6 drift token detected in alembic check output; after the 0046 apply the BE-6 schema set (like BE-5 before it) must have left the drift set."''', 'R14-banfail')
rep('        $DriftNote = "summary format (no itemized list in this alembic version; PGF-014): drift existence asserted (non-zero exit + a recorded drift marker); no V2/BE-5 token anywhere; the exact token set is pinned by the Level-II test evidence and the recorded lineage"',
    '        $DriftNote = "summary format (no itemized list in this alembic version; PGF-014): drift existence asserted (non-zero exit + a recorded drift marker); no V2/BE-5/BE-6 token anywhere; the exact token set is pinned by the Level-II test evidence and the recorded lineage"',
    'R14-summarynote')
rep('Write-Section "A7. DRIFT RE-BASELINE: alembic check (expected: exactly the 9 inherited V1 tokens; zero BE-5/V2 tokens; format-independent)"',
    'Write-Section "A7. DRIFT RE-BASELINE: alembic check (expected: exactly the 9 inherited V1 tokens; zero BE-6/V2 tokens; format-independent)"', 'R14-section')

# ============================================================
# R15. A8 state record + verdict
# ============================================================
rep_between('''    $StateLines = @(''',
            '''    Write-Evidence "Apply-final-state record written: ${StateRecPath}"''',
            '''    $StateLines = @(
        "# ITRGA-V2-0046-APPLY-FINAL-STATE-V1",
        "# Written by ITRGA-V2-0046-APPLY-PACK-V1 at the end of a PASS.",
        "# Consumed strictly by ITRGA-V2-0046-VERIFY-PACK-V1.",
        "# This run's post-0046 bytes are seed-time-dependent; this record",
        "# is the verdict-binding identity register for exactly this run.",
        "STATE_FILE_ID=ITRGA-V2-0046-APPLY-FINAL-STATE-V1",
        "RUN_TIMESTAMP=$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss zzz')",
        "POST_SIZE_BYTES=${FinalSize}",
        "POST_LAST_WRITE=${FinalWrite}",
        "POST_SHA256=${FinalHash}",
        "POST_REVISION=${ApplyTargetRevision}",
        "POST_V2_TRIGGER_COUNT=32",
        "POST_COMPVER_COUNT=6",
        "POST_PERMISSION_COUNT=41",
        "BASELINE_TIER1_BYTE_EXACT=${Tier1ByteExact}",
        "BASELINE_POLICY=anchor-as-is (pre-act disclosure N-1)",
        "ANCHOR_FILENAME=$((Split-Path ${MainBackupPath} -Leaf))",
        "ANCHOR_SIZE_BYTES=${AnchorSize}",
        "ANCHOR_SHA256=${MainBackupHash}"
    )
    Set-Content -Path $StateRecPath -Value $StateLines -Encoding ASCII
    Write-Evidence "Apply-final-state record written: ${StateRecPath}"''', 'R15-staterec')

rep('''    Write-Evidence "APPLY VERDICT: PASS - band BE-5 (20260902_0044 + 20260902_0045) was applied ONCE to the application's working SQLite database file '${TargetDbPath}'."
    Write-Evidence "Terminal state on the working lineage (BO-V2-BE-5-001): revision 20260902_0045; 28 v2 triggers (18 inherited intact + 10 BE-5, exact names and exact refusal messages); five BE-5 tables with both uniqueness anchors and the six indexes; 5 computation-version rows (mge/sge hashes proven by runtime recomputation); 35 permission rows (8 additive BE-5, content-exact); all five BE-5 tables empty; inherited BE-1..BE-4 state untouched (content-exact proofs); drift re-baselined to exactly the 9 inherited V1 tokens with zero BE-5/V2 tokens; anchor created and verified."
    Write-Evidence "Transcript: ${Transcript}"
    Write-Evidence "State record: ${StateRecPath} (required by the verify pack; do not move or edit it.)"
    Write-Evidence "NEXT: run ITRGA_V2_0045_VERIFY_PACK_V1.ps1 NOW - BEFORE restarting the application (the verify pack requires the five new tables to still be empty)."''',
    '''    Write-Evidence "APPLY VERDICT: PASS - band BE-6 (20260903_0046) was applied ONCE to the application's working SQLite database file '${TargetDbPath}'."
    Write-Evidence "Terminal state on the working lineage (BO-V2-BE-6-001, working-DB half): revision exactly 20260903_0046 via the single sanctioned upgrade; 32 v2 triggers (28 inherited intact + 4 BE-6, exact names and exact refusal messages); the two BE-6 tables with the pinned columns, all seven named constraints, both uniqueness anchors proven behaviorally and both indexes exact-named; 6 computation-version rows (BE-4 pinned by value; mge/sge and portfolio_risk_engine proven by runtime recomputation, the BE-6 recomputation equal to the pinned anchor); 41 permission rows (6 additive BE-6, content-exact); both BE-6 tables empty; inherited BE-1..BE-5 state untouched (content-exact proofs + digest equality across the mutation); drift re-baselined to exactly the 9 inherited V1 tokens with zero BE-6/V2 tokens; anchor (current-as-is, pre-act disclosure N-1) created and verified."
    Write-Evidence "Transcript: ${Transcript}"
    Write-Evidence "State record: ${StateRecPath} (required by the verify pack; do not move or edit it.)"
    Write-Evidence "NEXT: run ITRGA_V2_0046_VERIFY_PACK_V1.ps1 NOW - BEFORE restarting the application (the verify pack requires the two new tables to still be empty and binds to this run's state record)."''', 'R15-verdict')

# ============================================================
# Apply
# ============================================================
for old, new, tag in ops:
    assert s.count(old) == 1, tag
    s = s.replace(old, new, 1)
io.open('/home/user/AXIOM-TRADING-TERMINAL-v2.0/ITRGA_V2_0046_APPLY_PACK_V1.ps1', 'w', encoding='utf-8', newline='\n').write(s)
print('PART2 OK:', len(ops), 'ops applied; pack written;', s.count(chr(10)) + 1, 'lines')
