#!/usr/bin/env python3
# Surgical transformation: ITRGA_V2_0045_APPLY_PACK_V1.ps1 -> ITRGA_V2_0046_APPLY_PACK_V1.ps1
# Every replacement is anchored on a unique marker (count asserted == 1).
import io, sys

SRC = '/home/user/AXIOM-TRADING-TERMINAL-v2.0/ITRGA_V2_0045_APPLY_PACK_V1.ps1'
DST = '/home/user/AXIOM-TRADING-TERMINAL-v2.0/ITRGA_V2_0046_APPLY_PACK_V1.ps1'

s = io.open(SRC, encoding='utf-8').read()
ops = []

def rep(old, new, tag):
    n = s.count(old)
    if n != 1:
        print('ANCHOR-COUNT-FAIL', tag, n)
        sys.exit(1)
    ops.append((old, new, tag))

def rep_between(start, end, new, tag, keep_start=False, keep_end=False):
    # replace the region from start marker to end marker (both unique)
    c1, c2 = s.count(start), s.count(end)
    if c1 != 1 or c2 != 1:
        print('ANCHOR-COUNT-FAIL-BETWEEN', tag, c1, c2)
        sys.exit(1)
    i = s.find(start); j = s.find(end, i + len(start))
    if j < 0:
        print('ANCHOR-ORDER-FAIL', tag); sys.exit(1)
    old = s[i:j] if keep_end else s[i:j + len(end)]
    if keep_start:
        old = old[len(start):]
        new = start + new
    if keep_end:
        new = new + end
    rep(old, new, tag)

# ============================================================
# R1. HEADER (everything before Set-StrictMode)
# ============================================================
NEW_HEADER = '''# =====================================================================
# AXIOM V2 - 0046 WORKING-DATABASE APPLICATION ACT (BAND BE-6)
# ITRGA SQLITE APPLY ACT EVIDENCE PACK (V1)
# Pack ID: ITRGA-V2-0046-APPLY-PACK-V1
# Authority:
#   - ITRGA-DET-V2-BE-6-FINAL-001 (final determination; verdict C
#     full-verify PASS; instrument contract for this act in section 7.3)
#   - ITRGA-DET-V2-BE-6-ACCEPT-001 (acceptance record; BO-V2-BE-6-001
#     closed; sync package pinned)
#   - BO-V2-BE-6-001 (terminal state; its working-lineage half lands
#     through this act)
#   - ITRGA-ASSESSMENT-V2-0046-APPLY-SCOPE-V1 (scope assessment,
#     instrument contract and commissioning record of this act, incl.
#     the pre-act disclosure and the anchor-as-is policy)
#   - Delivery: AXIOM-V2-BE-6-DR-001 v1.0.1 (REVISION 2) + REM-Rev-2
#     evidence set (all 15 delivered-file hashes pinned to the Rev-2
#     literals)
# Pattern: ITRGA-V2-0045-APPLY-PACK-V1 -> ITRGA-V2-0043-APPLY-PACK-V1
#   (instruments of record of the two preceding working-DB application
#   acts; PGF-001 through PGF-015 lessons incorporated by construction:
#   pure ASCII, no compound braced expansions, helper command functions
#   with non-colliding parameter names, dialect-correct SQL,
#   content-based row comparisons, format-independent drift assertions,
#   quote-normalized operator input, canonical vocabulary, and
#   name-set/PRAGMA-only index introspection with uniqueness proven
#   BEHAVIORALLY - sqlite_master has no 'origin' column (PGF-015)).
#
# WHAT THIS PACK DOES:
#   Applies the verified band-BE-6 chain extension (migration
#   20260903_0046_v2_be6_portfolio_research) ONCE to the APPLICATION'S
#   WORKING SQLITE DATABASE FILE (backend\\axiom_dev.db) with exactly
#   one literal-revision invocation: alembic upgrade 20260903_0046.
#   It then proves the terminal state on SQLite:
#   revision exactly 20260903_0046; exactly 32 v2 triggers (28
#   inherited intact + 4 BE-6, exact names); the 4 BE-6 guard triggers
#   in force with their exact refusal messages via transactional probe
#   cycles that roll their throwaway rows back; the two BE-6 tables
#   with their pinned columns (PRAGMA name-sets), both uniqueness
#   anchors proven BEHAVIORALLY and both indexes exact-named; exactly 6
#   computation-version rows (the three BE-4 rows content-exact, the
#   mge/sge rows runtime-recomputed, the new portfolio_risk_engine row
#   proven by RUNTIME RECOMPUTATION of the four pinned engine source
#   files on this machine AND asserted equal to the pinned anchor);
#   exactly 41 permission rows (6 additive BE-6 rows content-exact, no
#   duplicates); both BE-6 tables empty; the inherited BE-1..BE-5 state
#   untouched (content-exact proofs + digest equality across the
#   mutation); drift re-baselined to exactly the 9 inherited V1 tokens
#   with zero V2/BE-6 tokens.
#
#   SQLite-specific design (as the proven predecessor packs):
#   - No database server: NO psql, NO password prompt, NO credential
#     of any kind. All SQL runs through the repo venv python (sqlite3
#     module) against the file directly.
#   - FILE-LEVEL ANCHOR copy to operator-evidence\\BE-6 BEFORE any
#     modification: the complete, credential-free rollback anchor.
#   - Exact-content comparison runs IN PYTHON (never position-based).
#   - Baseline authority = the ITRGA-verified 0045 terminal-state
#     constants, EMBEDDED in this pack (chain of custody: the 0045
#     act's instrument halted after the mutation but before its
#     state-record write; the V2 resumption verify re-proved the full
#     0045 terminal state on the working lineage and affirmed the
#     absence of the apply-final-state record - see the assessment).
#     Two-tier baseline: Tier 1 byte state RECORDED ONLY (forfeited by
#     the lawful post-0045 application restart; the anchor binds the
#     current-as-is image - the pre-act disclosure, item N-1); Tier 2
#     re-proves the entire 0045 terminal state by CONTENT and aborts on
#     any failure.
#   - Spot-checks assert the EXACT SQLite guard messages, including
#     transactional insert-probe-rollback cycles on the empty tables
#     (the probes change nothing), both uniqueness anchors proven
#     behaviorally, and three CHECK-vocabulary refusal probes.
#   - It does NOT create or delete any database file.
#   - It modifies ONLY the target file (the single sanctioned
#     mutation) and writes: the transcript, the anchor copy, and the
#     apply-final-state record (for the verify pack), all in
#     operator-evidence\\BE-6; plus a throwaway helper in the OS temp
#     directory (removed on exit).
#   - NO AUTHORITY VARIABLE EXISTS FOR THIS ACT: the pack enumerates
#     and removes any pre-existing AXIOM_TD_* / authority variables
#     and asserts their absence. It never sets one.
#
# BEFORE RUNNING: STOP THE RUNNING APPLICATION (it holds a live
#   connection to the target database file). Do NOT restart it before
#   the verify pack has also completed (the verify pack requires the
#   two new tables to still be empty).
#
# RUN MODE: this pack MUST be executed as a file. Pasting the script
#   into an interactive console is NOT an acceptable evidence mode
#   (PGF-004).
#
# OPERATOR INSTRUCTION CARD:
#   1. Before running anything, verify byte-identity of the TWO
#      issued artifacts against the ITRGA issuance note
#      (ITRGA_ISSUANCE_V2_0046_PACKS_001.md):
#        ITRGA_V2_0046_APPLY_PACK_V1.ps1   (this file; runs FIRST)
#        ITRGA_V2_0046_VERIFY_PACK_V1.ps1  (verify pack; runs SECOND)
#      If any hash does not match: STOP; do not run; report to ITRGA.
#   2. The BE-6 file set must already be in the repository exactly as
#      delivered (the packs re-pin all 41 provenance files by hash and
#      abort on ANY deviation: 9 chain migrations + 32 delivered BE-5 /
#      BE-6 files).
#   3. Execute ONLY this file, from the repository root:
#        powershell -NoProfile -ExecutionPolicy Bypass -File ".\\ITRGA_V2_0046_APPLY_PACK_V1.ps1"
#   4. Single expected input: the absolute path of the working
#      database file backend\\axiom_dev.db (a path, not a credential).
#      Nothing else is asked. No password. No API key.
#   5. Then run the verify pack (do NOT restart the application
#      between apply and verify):
#        powershell -NoProfile -ExecutionPolicy Bypass -File ".\\ITRGA_V2_0046_VERIFY_PACK_V1.ps1"
#   6. Send BOTH transcripts back to ITRGA:
#        operator-evidence\\BE-6\\0046-APPLY-RUN-V1.txt
#        operator-evidence\\BE-6\\0046-VERIFY-RUN-V1.txt
#      (this is the evidence envelope that places the BO-V2-BE-6-001
#      terminal state on the working lineage.)
#
# Save the two issued artifacts to the AXIOM repository root:
#   C:\\Users\\victo\\.vscode\\AXIOM\\axiom\\
# =====================================================================
'''
i = s.find('# =====================================================================\n# AXIOM V2 - 0044/0045')
j = s.find('Set-StrictMode -Version Latest')
assert i == 0 and j > 0
rep(s[i:j], NEW_HEADER + '\n', 'R1-header')

# ============================================================
# R2. PATH CONSTANTS
# ============================================================
rep('$EvidenceDir   = Join-Path $EvidenceRoot "BE-5"',
    '$EvidenceDir   = Join-Path $EvidenceRoot "BE-6"', 'R2-eviddir')
rep('$Transcript    = Join-Path $EvidenceDir "0045-APPLY-RUN-V1.txt"',
    '$Transcript    = Join-Path $EvidenceDir "0046-APPLY-RUN-V1.txt"', 'R2-transcript')
rep('''$PrevStateDir  = Join-Path $EvidenceRoot "BE-4"
$PrevStatePath = Join-Path $PrevStateDir "0043-APPLY-FINAL-STATE.txt"
$StateRecPath  = Join-Path $EvidenceDir "0045-APPLY-FINAL-STATE.txt"''',
    '$StateRecPath  = Join-Path $EvidenceDir "0046-APPLY-FINAL-STATE.txt"', 'R2-statepath')

# ============================================================
# R3. CONSTANTS BLOCK
# ============================================================
rep('''# Chain migration provenance pins (sha256). 0038-0043 re-pinned from
# the BE-4 act; 0044/0045 from the verified REM-001 Rev-2 literals.''',
    '''# Chain migration provenance pins (sha256). 0038-0045 re-pinned from
# the BE-4/BE-5 acts; 0046 from the verified REM-Rev-2 literal.''', 'R3-migcomment')
rep('''    "20260902_0045_v2_be5_signal_contracts.py"     = "9aa87508b6db4d74296f8dabfab33ae7fb84dc705326f141b4b42e2d4f981f52"
}
$ApplyTargetRevision = "20260902_0045"
$BaselineRevision    = "20260831_0043"''',
    '''    "20260902_0045_v2_be5_signal_contracts.py"     = "9aa87508b6db4d74296f8dabfab33ae7fb84dc705326f141b4b42e2d4f981f52"
    "20260903_0046_v2_be6_portfolio_research.py"   = "1e95ce499ec73bb5b8b0a628cfa01f1f26642c3cfcc080806cacce2532156962"
}
$ApplyTargetRevision = "20260903_0046"
$BaselineRevision    = "20260902_0045"''', 'R3-migrations')

rep('''# Remaining 11 delivered BE-5 files (sha256; REM-001 Rev-2 literals).
$ExpectedDeliveredHashes = @{''',
    '''# Delivered application files (sha256): the 17 BE-5 set (REM-001 Rev-2
# literals) plus the 15 BE-6 set (REM-Rev-2 literals), pinned verbatim.
$ExpectedDeliveredHashes = @{''', 'R3-delcomment')
rep('''    "backend\\tests\\test_v2_be4_migration.py"            = "5935b9ea3c530dab3454daefa6c4e0ea3f2b46c957c923ccd62c6bb4eb5dce4d"
}''',
    '''    "backend\\tests\\test_v2_be4_migration.py"            = "5935b9ea3c530dab3454daefa6c4e0ea3f2b46c957c923ccd62c6bb4eb5dce4d"
    "backend\\app\\v2\\portfolio_research\\__init__.py"     = "a8241065ce6c4963c861137df3e43d5ba3468c66f6206013f4e7a252b31747a3"
    "backend\\app\\v2\\portfolio_research\\contracts.py"    = "bc1f3c25ef72b3203a1bf33f670e5bbead825c09dc02482c5a432a148125f036"
    "backend\\app\\v2\\portfolio_research\\metrics.py"      = "5409c7da2f578a1e8756ecc779beabe55ffc4cfa2509c46f19fb664d12ce2d78"
    "backend\\app\\v2\\portfolio_research\\scenarios.py"    = "e032224e90d389f9e73f3009f21359d37c2566c6ad53783d8775ef8333ba4e66"
    "backend\\app\\v2\\portfolio_research\\api.py"          = "7f8a12ac05e04cc3fedaa7a04319b0c3af25a31eb115d722b968e345d78815eb"
    "backend\\app\\db\\models\\v2_portfolio.py"             = "89ead20a39008df516806332e76e0c7394b5e94ce746bf49d0d760876ca35e4b"
    "backend\\tests\\test_v2_be6_metrics.py"               = "c8716bdd23b4901d07525eaef5fbfdf8cc98c4ceece0573dcfb5132af0f3fa8d"
    "backend\\tests\\test_v2_be6_migration.py"             = "5f082ae956a074b9bca56a1b3368f5e1ab6c2c2db457551df2ac0219ba81462c"
    "backend\\tests\\test_v2_be6_api.py"                   = "c983989b21dd38369f1a93dd82a7b0bf60686aa8ee4c79bb1b32fde81f6923db"
    "backend\\tests\\test_v2_be6_annex.py"                 = "352d9924cbd62f022c7b3ded351b9e35e5364d650b4568036e6082d0e4c1cfae"
    "backend\\app\\v2\\api\\router.py"                      = "8eae85bcf9c7d0ceb273f0ff942076a523f8165c66ba35e831277fd944a64a3d"
    "backend\\app\\v2\\rbac\\permissions.py"                = "2400e6e78339422086723495a6e3621aca5c1162e8cb5fefad00e91a9c02a097"
    "backend\\app\\db\\models\\__init__.py"                 = "3465a5b0633da8165dac6b08aff2907472f780f573523c5ed1e84c451955b1ff"
    "backend\\tests\\test_v2_be5_migration.py"             = "1eb4ade1b11b71b4ba8f000bc588cb13c6db589d0181297df844a4b97cf30f6e"
}''', 'R3-delivered')

# NOTE: the BE-5 set contains keys that collide by path with the BE-6
# set (router.py / permissions.py / models __init__.py /
# test_v2_be5_migration.py are delivered by BOTH bands; the BE-6 Rev-2
# pin supersedes the BE-5-era pin for those four paths). The four old
# entries are removed below so the hashtable has no duplicate keys.
for old_key, old_hash in [
    ('    "backend\\app\\v2\\api\\router.py"                      = "c9ee841429621801d5175d40c9dbbd07767f7be6b029fdf2498e27f3ffbbd19c"\n', 'router'),
    ('    "backend\\app\\v2\\rbac\\permissions.py"                = "45eb34e11add36355940d52116376fc387d86d264827ee1cae0cd46c1bcbf462"\n', 'perms'),
    ('    "backend\\app\\db\\models\\__init__.py"                 = "b569a8e430926847827b63e6bddc39d895d52f4b0849d069d01e57c1c1c6d5a7"\n', 'modelsinit'),
    ('    "backend\\tests\\test_v2_be5_migration.py"            = "6d36ad127d759e5240562689e6b8cd8268162951c7950aa248e05b72d3fc0e8c"\n', 'be5migtest'),
]:
    rep(old_key, '', 'R3-dedupe-' + old_hash)

# Guard-name arrays: add the BE-6 set after the BE-5 set.
rep('''$Be4GuardTriggers = @(''',
    '''# The four BE-6 guard triggers and their exact SQLite messages.
$Be6GuardNames = @(
    "v2_portfolio_definition_immutable_delete",
    "v2_portfolio_definition_immutable_update",
    "v2_portfolio_risk_report_immutable_delete",
    "v2_portfolio_risk_report_immutable_update"
)
$Be6UpdateMsgDef  = "V2 portfolio definitions are immutable; UPDATE prohibited"
$Be6DeleteMsgDef  = "V2 portfolio definitions are immutable; DELETE prohibited"
$Be6UpdateMsgRep  = "V2 portfolio risk reports are immutable; UPDATE prohibited"
$Be6DeleteMsgRep  = "V2 portfolio risk reports are immutable; DELETE prohibited"

# The full prior 28-name trigger census (verified on the working
# database by the 0045-VERIFY-RUN-V2 transcript; pinned verbatim).
$ExpectedPreTrig28 = @(
    "v2_audit_immutable_delete",
    "v2_audit_immutable_update",
    "v2_chart_intelligence_report_immutable_delete",
    "v2_chart_intelligence_report_immutable_update",
    "v2_computation_version_immutable_delete",
    "v2_computation_version_immutable_update",
    "v2_lineage_immutable_delete",
    "v2_lineage_immutable_update",
    "v2_market_context_report_immutable_delete",
    "v2_market_context_report_immutable_update",
    "v2_md_integrity_immutable_delete",
    "v2_md_integrity_immutable_update",
    "v2_md_provider_hist_immutable_delete",
    "v2_md_provider_hist_immutable_update",
    "v2_md_provider_immutable_delete",
    "v2_md_provider_immutable_update",
    "v2_md_verification_immutable_delete",
    "v2_md_verification_immutable_update",
    "v2_ml_diagnostic_report_immutable_delete",
    "v2_ml_diagnostic_report_immutable_update",
    "v2_ml_governance_record_immutable_delete",
    "v2_ml_governance_record_immutable_update",
    "v2_ml_lifecycle_event_immutable_delete",
    "v2_ml_lifecycle_event_immutable_update",
    "v2_signal_record_immutable_delete",
    "v2_signal_record_immutable_update",
    "v2_signal_state_event_immutable_delete",
    "v2_signal_state_event_immutable_update"
)

# The two BE-6 indexes (exact names).
$Be6Indexes = @(
    "ix_v2_pfdef_portfolio",
    "ix_v2_pfrisk_def"
)

# The pinned BE-6 engine-anchor (sha256 rolling digest over the four
# engine files, relpath+NUL+bytes+NUL in the pinned order; recomputed
# from the REM-Rev-2 literals and asserted equal at runtime).
$Be6EngineAnchor = "5c6d8f08809680506694032a5580616d6e15c13ecfa7a59a1d4a0fd869cec90a"

$Be4GuardTriggers = @(''', 'R3-be6names')

# The 8 BE-4/transition arrays stay. $Be5Indexes stays.

# ============================================================
# R4. HELPER SOURCE ADDITIONS
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
)''', 'R4-be6files')

rep('''    if cmd in ("scalar", "verifyrows", "verifyaudit", "compverbe5",
               "permbe5", "reportempty5", "tabledigest"):''',
    '''    if cmd in ("scalar", "verifyrows", "verifyaudit", "compverbe5",
               "permbe5", "reportempty5", "compverbe6", "permbe6",
               "reportempty2", "tabledigest"):''', 'R4-cmdtuple')

rep('''                print("PASS:compver_rows_exact")
                print("INFO:mge_recomputed=" + exp_be5["ml_governance_engine"][1])
                print("INFO:sge_recomputed=" + exp_be5["signal_engine"][1])''',
    '''                print("PASS:compver_rows_exact")
                print("INFO:mge_recomputed=" + exp_be5["ml_governance_engine"][1])
                print("INFO:sge_recomputed=" + exp_be5["signal_engine"][1])
            elif cmd == "compverbe6":
                # Exactly 6 rows: the 3 BE-4 components pinned by value;
                # the 2 BE-5 components and the BE-6 component pinned by
                # RUNTIME RECOMPUTATION of the engine file hashes. The
                # BE-6 recomputation is asserted equal to the pinned
                # anchor literal passed as argv[7] before the row check.
                backend_dir = sys.argv[3]
                pins_be4 = {
                    "indicator_engine": ("v1-reuse-1.0.0", sys.argv[4]),
                    "market_context_engine": ("mce-1.0.0", sys.argv[5]),
                    "chart_intelligence_engine": ("cie-1.0.0", sys.argv[6]),
                }
                exp_be5 = {
                    "ml_governance_engine": ("mge-1.0.0",
                                             engine_hash(backend_dir, MGE_FILES)),
                    "signal_engine": ("sge-1.0.0",
                                      engine_hash(backend_dir, SGE_FILES)),
                }
                be6_anchor_arg = sys.argv[7]
                be6_recomputed = engine_hash(backend_dir, BE6_FILES)
                if be6_recomputed != be6_anchor_arg:
                    print("FAIL:be6_anchor_mismatch recomputed=" + be6_recomputed
                          + " pinned=" + be6_anchor_arg)
                    return
                exp_be6 = {
                    "portfolio_risk_engine": ("pre-1.0.0", be6_recomputed),
                }
                rows = con.execute(
                    "SELECT component, version, source_hash, evidence_ref, registered_at "
                    "FROM v2_computation_version"
                ).fetchall()
                if len(rows) != 6:
                    print("FAIL:compver6_count=" + str(len(rows)))
                    return
                seen = {}
                for component, version, source_hash, evidence_ref, registered_at in rows:
                    if component in seen:
                        print("FAIL:compver6_duplicate_component=" + str(component))
                        return
                    seen[component] = (version, source_hash,
                                       evidence_ref, registered_at)
                exp_map = {}
                for src_map in (pins_be4, exp_be5, exp_be6):
                    exp_map.update(src_map)
                for component, (exp_version, exp_hash) in exp_map.items():
                    if component not in seen:
                        print("FAIL:compver6_missing=" + component)
                        return
                    version, source_hash, evidence_ref, registered_at = seen[component]
                    if version != exp_version:
                        print("FAIL:compver6_version=" + component + "=" + repr(version))
                        return
                    if source_hash != exp_hash:
                        print("FAIL:compver6_hash=" + component + "=" + repr(source_hash)
                              + " expected=" + repr(exp_hash))
                        return
                    if not re.fullmatch(r"[0-9a-f]{64}", source_hash or ""):
                        print("FAIL:compver6_hash_shape=" + component)
                        return
                    if component in pins_be4:
                        exp_ref = "BO-V2-BE-4-001"
                    elif component in exp_be5:
                        exp_ref = "BO-V2-BE-5-001"
                    else:
                        exp_ref = "BO-V2-BE-6-001"
                    if evidence_ref != exp_ref:
                        print("FAIL:compver6_evidence_ref=" + component + "=" + repr(evidence_ref))
                        return
                    if not registered_at or len(str(registered_at)) < 19:
                        print("FAIL:compver6_registered_at_shape=" + component)
                        return
                print("PASS:compver6_rows_exact")
                print("INFO:mge_recomputed=" + exp_be5["ml_governance_engine"][1])
                print("INFO:sge_recomputed=" + exp_be5["signal_engine"][1])
                print("INFO:pre_recomputed=" + be6_recomputed)''', 'R4-compverbe6')

rep('''                print("PASS:perm_rows_exact")
                print("INFO:v2_permission_total=" + str(total))''',
    '''                print("PASS:perm_rows_exact")
                print("INFO:v2_permission_total=" + str(total))
            elif cmd == "permbe6":
                rows = con.execute(
                    "SELECT role, permission, sal FROM v2_permission "
                    "WHERE permission LIKE 'v2.research.portfolio%'"
                ).fetchall()
                if len(rows) != 6:
                    print("FAIL:permbe6_count=" + str(len(rows)))
                    return
                expected = {
                    ("admin", "v2.research.portfolio.read", "SAL-2"),
                    ("admin", "v2.research.portfolio.define", "SAL-3"),
                    ("admin", "v2.research.portfolio_risk.read", "SAL-2"),
                    ("admin", "v2.research.portfolio_risk.compute", "SAL-3"),
                    ("operator", "v2.research.portfolio.read", "SAL-2"),
                    ("operator", "v2.research.portfolio_risk.read", "SAL-2"),
                }
                if set(tuple(r) for r in rows) != expected:
                    print("FAIL:permbe6_rows=" + repr(sorted(tuple(r) for r in rows)))
                    return
                total = con.execute("SELECT COUNT(*) FROM v2_permission").fetchone()[0]
                if total != 41:
                    print("FAIL:permbe6_total=" + str(total))
                    return
                dupes = con.execute(
                    "SELECT COUNT(*) - COUNT(DISTINCT role || '|' || permission) "
                    "FROM v2_permission"
                ).fetchone()[0]
                if dupes != 0:
                    print("FAIL:perm_duplicate_role_permission")
                    return
                print("PASS:perm6_rows_exact")
                print("INFO:v2_permission_total=" + str(total))''', 'R4-permbe6')

rep('''                print("PASS:be5_tables_empty")
            elif cmd == "tabledigest":''',
    '''                print("PASS:be5_tables_empty")
            elif cmd == "reportempty2":
                counts = {}
                for table in ("v2_portfolio_definition", "v2_portfolio_risk_report"):
                    counts[table] = con.execute(
                        "SELECT COUNT(*) FROM " + table).fetchone()[0]
                if any(v != 0 for v in counts.values()):
                    print("FAIL:table_counts=" + repr(counts))
                    return
                print("PASS:be6_tables_empty")
            elif cmd == "tabledigest":''', 'R4-reportempty2')

# uniqbe6 rw verb: insert baseline + duplicate within one transaction;
# expect the UNIQUE refusal; roll the throwaway rows back.
rep('''    print("FAIL:unknown_command=" + cmd)
    sys.exit(2)''',
    '''    if cmd == "uniqbe6":
        flavor = sys.argv[3]
        if flavor == "pfdef":
            base_sql = ("INSERT INTO v2_portfolio_definition (id, portfolio_id, "
                        "record_seq, name, basis, allocations, base_currency, "
                        "data_class, assumptions, mode, operator_id, created_at) "
                        "VALUES ('uniqprobe-a', 'uniqprobe', 1, 'uniqprobe', "
                        "'hypothetical', '{}', 'EUR', 'synthetic', '{}', "
                        "'RESEARCH', 'uniqprobe', '2026-09-03 00:00:00');")
            dup_sql = ("INSERT INTO v2_portfolio_definition (id, portfolio_id, "
                       "record_seq, name, basis, allocations, base_currency, "
                       "data_class, assumptions, mode, operator_id, created_at) "
                       "VALUES ('uniqprobe-b', 'uniqprobe', 1, 'uniqprobe', "
                       "'hypothetical', '{}', 'EUR', 'synthetic', '{}', "
                       "'RESEARCH', 'uniqprobe', '2026-09-03 00:00:00');")
        elif flavor == "pfrisk":
            base_sql = ("INSERT INTO v2_portfolio_risk_report (id, "
                        "portfolio_definition_id, as_of, time_basis, input_refs, "
                        "inputs_hash, metrics, scenarios, status, basis_label, "
                        "data_class, engine_versions, engine_versions_hash, mode, "
                        "operator_id, created_at) "
                        "VALUES ('uniqprobe-a', 'uniqprobe', '2026-09-03 00:00:00', "
                        "'{}', '[]', 'uniqprobe-in', '{}', '[]', 'available', "
                        "'hypothetical-research', 'synthetic', '{}', 'uniqprobe-eng', "
                        "'RESEARCH', 'uniqprobe', '2026-09-03 00:00:00');")
            dup_sql = ("INSERT INTO v2_portfolio_risk_report (id, "
                       "portfolio_definition_id, as_of, time_basis, input_refs, "
                       "inputs_hash, metrics, scenarios, status, basis_label, "
                       "data_class, engine_versions, engine_versions_hash, mode, "
                       "operator_id, created_at) "
                       "VALUES ('uniqprobe-b', 'uniqprobe', '2026-09-03 00:00:00', "
                       "'{}', '[]', 'uniqprobe-in', '{}', '[]', 'available', "
                       "'hypothetical-research', 'synthetic', '{}', 'uniqprobe-eng', "
                       "'RESEARCH', 'uniqprobe', '2026-09-03 00:00:00');")
        else:
            print("FAIL:unknown_flavor=" + flavor)
            sys.exit(2)
        con = rw_connect(db_path)
        try:
            con.execute(base_sql)
            try:
                con.execute(dup_sql)
                outcome = "SUCCESS_UNEXPECTED"
            except sqlite3.Error as exc:
                outcome = "REFUSED:" + str(exc)
            con.rollback()
            print(outcome)
        finally:
            con.close()
        return

    print("FAIL:unknown_command=" + cmd)
    sys.exit(2)''', 'R4-uniqbe6')

# Helper dir name per act.
rep('$HelperDir  = Join-Path $env:TEMP "axiom_itrga_0045_apply_v1"',
    '$HelperDir  = Join-Path $env:TEMP "axiom_itrga_0046_apply_v1"', 'R4-helperdir')

# ============================================================
# R5. COMMAND HELPER: add Invoke-ExpectedUniqProbe after GuardProbe
# ============================================================
rep('''    Write-Evidence "PASS: exact refusal message observed; throwaway row rolled back."
}

# ---------------------------------------------------------------------
# A0. RUN IDENTIFICATION''',
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
# A0. RUN IDENTIFICATION''', 'R5-uniqfn')

# ============================================================
# R6. A0 RUN IDENTIFICATION PROSE
# ============================================================
rep('''Write-Evidence "Pack: ITRGA-V2-0045-APPLY-PACK-V1"
Write-Evidence "Act: band BE-5 (0044+0045) working-database application act (single sanctioned mutation: alembic upgrade 20260902_0045)"
Write-Evidence "Determination: ITRGA-DET-V2-BE-5-FINAL-001 (C full-verify PASS; C-1 closed; C-2 scope = this envelope)"
Write-Evidence "Build order: BO-V2-BE-5-001 (terminal state T-1...T-12)"
Write-Evidence "Baseline authority: operator-evidence\\BE-4\\0043-APPLY-FINAL-STATE.txt (chain of custody of the 0043 act)"''',
    '''Write-Evidence "Pack: ITRGA-V2-0046-APPLY-PACK-V1"
Write-Evidence "Act: band BE-6 (0046) working-database application act (single sanctioned mutation: alembic upgrade 20260903_0046)"
Write-Evidence "Determination: ITRGA-DET-V2-BE-6-FINAL-001 (C full-verify PASS; instrument contract in section 7.3) + ITRGA-DET-V2-BE-6-ACCEPT-001"
Write-Evidence "Build order: BO-V2-BE-6-001 (terminal state; working-lineage half via this act)"
Write-Evidence "Scope/commissioning: ITRGA-ASSESSMENT-V2-0046-APPLY-SCOPE-V1 (incl. the pre-act disclosure; item N-1 = anchor-as-is)"
Write-Evidence "Baseline authority: ITRGA-verified 0045 terminal-state constants EMBEDDED in this pack (chain of custody: the 0045 apply instrument halted after the mutation but before its state-record write (PGF-015); the 0045-VERIFY-RUN-V2 transcript re-proved the full terminal state on the working lineage; no apply-final-state record exists from the 0045 act)"''', 'R6-a0prose')

rep('Write-Evidence "Read-write scope: exactly one mutation (alembic upgrade 20260902_0045) on the target file; plus the transcript, the anchor copy, and the apply-final-state record in operator-evidence\\BE-5; plus the throwaway helper (removed on exit)."',
    'Write-Evidence "Read-write scope: exactly one mutation (alembic upgrade 20260903_0046) on the target file; plus the transcript, the anchor copy, and the apply-final-state record in operator-evidence\\BE-6; plus the throwaway helper (removed on exit)."', 'R6-scope')

# ============================================================
# R7. A0b BASELINE AUTHORITY BLOCK (embedded constants)
# ============================================================
OLD_A0B_START = '''# ---------------------------------------------------------------------
# A0b. BASELINE AUTHORITY (the 0043 apply-final-state record, strict)
# ---------------------------------------------------------------------'''
OLD_A0B_END = '''Push-Location $BackendRoot'''
NEW_A0B = '''# ---------------------------------------------------------------------
# A0b. BASELINE AUTHORITY (EMBEDDED ITRGA-verified 0045 terminal-state
# constants; Tier-1 byte state RECORDED ONLY - pre-act disclosure N-1)
# ---------------------------------------------------------------------

Write-Section "A0b. BASELINE AUTHORITY (embedded 0045 terminal-state constants; no external state record)"

Write-Evidence "Chain of custody:"
Write-Evidence "  1. The 0045 apply instrument (V1) executed the sanctioned mutation but halted on an instrument defect (PGF-015) before writing its apply-final-state record; the defect class was corrected in the V2 resumption instrument."
Write-Evidence "  2. The 0045 VERIFY pack (V2) re-proved the complete 0045 terminal state on the working lineage; recorded verdict PASS in operator-evidence\\BE-5\\0045-VERIFY-RUN-V2.txt, and affirmed the absence of the apply-final-state record as the state marker."
Write-Evidence "  3. The 0045 final file bytes recorded there (size 1445888, sha256 8d0e5a36....578ab0) are FORFEITED as a gate: the post-0045 application restart lawfully wrote a bootstrap-admin row (disclosed pre-act, assessment item N-1). The anchor below binds the CURRENT-AS-IS image; content re-proof (Tier 2, gate A1) carries strictness."
Write-Evidence "Embedded 0045 terminal-state constants (each re-proven by content in gate A1):"
Write-Evidence "  POST_REVISION             20260902_0045"
Write-Evidence "  POST_V2_TRIGGER_COUNT     28 (exact 28-name set pinned in this pack)"
Write-Evidence "  POST_COMPVER_COUNT        5 (3 BE-4 pins + mge/sge runtime recomputation)"
Write-Evidence "  POST_PERMISSION_COUNT     35 (8 additive BE-5 rows content-exact)"
Write-Evidence "  BE-5 TABLES               all five present and empty"
Write-Evidence "  PROVIDER ROW              twelvedata = contract_tested|verified|0"
Write-Evidence "  INHERITED ANCHORS         history/audit exact (0043-era pins)"
Write-Evidence "  BE-6 PRE-EXISTENCE        none (tables/triggers/rows/permissions all absent)"
Write-Evidence "PASS: baseline authority bound (embedded constants; strict Tier-2 re-proof in A1; Tier-1 recorded-only by policy)."

'''
rep_between(OLD_A0B_START, OLD_A0B_END, NEW_A0B, 'R7-a0b', keep_end=True)

# ============================================================
# R8. A0c/A0d headings fine. A1 BLOCK replacement (whole section)
# ============================================================
OLD_A1_START = '''    Write-Section "A1. BASELINE (pre-mutation; two-tier authority; abort on content failure)"'''
OLD_A1_END = '''    # -----------------------------------------------------------------
    # A2. ANCHOR (first side effect; target: the evidence directory)
    # -----------------------------------------------------------------'''
NEW_A1 = '''    Write-Section "A1. BASELINE (pre-mutation; embedded-constant authority; Tier-2 content re-proof; abort on any failure)"

    # A1.1: current revision gate (read-only; explicit already-applied abort).
    [void](Assert-CurrentExactly -ExpectedRev ${BaselineRevision} -Label "A1 baseline current")
    Write-Evidence "PASS: A1.1 - current revision is exactly ${BaselineRevision} (an already-applied 0046 or any other value aborts here)."

    # A1.2: file state (Tier-1 RECORDED ONLY; forfeited as a gate by the
    # lawful post-0045 restart - pre-act disclosure N-1; the anchor binds
    # the current-as-is image).
    $B1File = Get-Item ${TargetDbPath}
    $B1Size  = $B1File.Length
    $B1Write = $B1File.LastWriteTime.ToString('yyyy-MM-dd HH:mm:ss zzz')
    $B1Hash  = (Get-FileHash ${TargetDbPath} -Algorithm SHA256).Hash.ToLower()
    Write-Evidence "Target file: ${TargetDbPath}"
    Write-Evidence "  size       ${B1Size} bytes (recorded; no external byte pin - anchor-as-is)"
    Write-Evidence "  last write ${B1Write} (recorded)"
    Write-Evidence "  sha256     ${B1Hash} (recorded; the 0045-era byte pin is forfeited by the disclosed bootstrap-admin write; content re-proof below carries strictness)"
    $Tier1ByteExact = $false
    Write-Evidence "NOTE: A1.2 Tier-1 byte-identity gate is FORFEITED BY POLICY for this act (recorded-only). Tier-2 content re-proof follows."

    # A1.3: integrity / journal / sidecars.
    [void](Invoke-Py -PyArgs @("scalar", ${TargetDbPath}, "SELECT sqlite_version();") -Label "A1 sqlite version (recorded)")
    $IntegrityOut = Invoke-Py -PyArgs @("scalar", ${TargetDbPath}, "PRAGMA integrity_check;") -Label "A1 integrity check"
    $IntegrityText = (Norm-Text $IntegrityOut).Trim()
    if ($IntegrityText -ne "ok") {
        throw "FAIL: A1 - integrity_check '${IntegrityText}', expected 'ok'. Stopping before any modification; report to ITRGA."
    }
    $JournalOut = Invoke-Py -PyArgs @("scalar", ${TargetDbPath}, "PRAGMA journal_mode;") -Label "A1 journal mode"
    $JournalText = (Norm-Text $JournalOut).Trim()
    if ($JournalText -ne "delete") {
        throw "FAIL: A1 - journal_mode '${JournalText}', expected 'delete'. Stopping before any modification; report to ITRGA."
    }
    foreach ($Suffix in @("-wal", "-shm")) {
        $SidePath = ${TargetDbPath} + $Suffix
        if (Test-Path $SidePath) {
            throw "FAIL: A1 - unexpected sidecar present: ${SidePath}. Stop the application first; then report to ITRGA if it persists."
        }
        Write-Evidence "Sidecar ${Suffix}: absent"
    }
    Write-Evidence "PASS: A1.3 - integrity ok; journal delete; no sidecars."

    # A1.4: trigger posture - exact 28-name census (pinned verbatim);
    # the four BE-6 guards absent.
    [void](Invoke-Py -PyArgs @("scalar", ${TargetDbPath}, "SELECT name FROM sqlite_master WHERE type='trigger' AND name LIKE 'v2_%' ORDER BY name;") -Label "A1 v2 trigger names (recorded)")
    $PreTrigNamesText = Get-PyScalar -Sql "SELECT name FROM sqlite_master WHERE type='trigger' AND name LIKE 'v2_%' ORDER BY name;" -Label "A1 v2 trigger set (snapshot)"
    $PreTrigNames = @($PreTrigNamesText -split "`n" | Where-Object { $_ -ne "" })
    if ($PreTrigNames.Count -ne 28) {
        throw "FAIL: A1 - v2 trigger count '$($PreTrigNames.Count)', expected exactly 28 (the 0045 terminal state). Stopping before any modification; report to ITRGA."
    }
    $PreTrigSorted = @($PreTrigNames | Sort-Object)
    $ExpectedPreSorted = @($ExpectedPreTrig28 | Sort-Object)
    if (($PreTrigSorted -join "`n") -ne ($ExpectedPreSorted -join "`n")) {
        throw "FAIL: A1 - the v2 trigger name set is not exactly the pinned 28-name 0045 census. Stopping before any modification; report to ITRGA."
    }
    foreach ($Be6Name in $Be6GuardNames) {
        if ($PreTrigNames -contains $Be6Name) {
            throw "FAIL: A1 - a BE-6 guard trigger is already present: ${Be6Name} (double-apply suspected). Stopping before any modification; report to ITRGA."
        }
    }
    Write-Evidence "PASS: A1.4 - exactly the pinned 28-name v2 trigger census (0045 terminal state); the four BE-6 guards absent."

    # A1.5: Tier-2 CONTENT re-proof of the 0045 terminal state (always
    # run): compver 5 rows incl. mge/sge RUNTIME RECOMPUTATION; perms
    # 35 with the BE-5 octet content-exact and zero BE-6 rows; provider
    # pin; inherited anchors exact; record-only digests captured; BE-6
    # schema fully absent.
    $CompverPreOut = Invoke-Py -PyArgs @(
        "compverbe5", ${TargetDbPath}, ${BackendRoot},
        "fe9aab42c34d671e960fd92a9346d3bf60c27135e76e52310d774bc84028dd35",
        "69902503483502bcd5ce5e35fdb0eeabcb2efcaf7a4b0c262a6fccf2d0af3a8c",
        "3887d6ca8ba05858f41889cd99fa05aba42663ac22d906a7f989b567c3912180"
    ) -Label "A1 compver 5-row content re-proof (mge/sge recomputed)"
    $CompverPreText = (Norm-Text $CompverPreOut).Trim()
    if ($CompverPreText -notlike "PASS:compver_rows_exact*") {
        throw "FAIL: A1 - the 5-row computation-version baseline failed content re-proof: ${CompverPreText}. Stopping before any modification; report to ITRGA."
    }
    $PreBe6Compver = Get-PyScalar -Sql "SELECT COUNT(*) FROM v2_computation_version WHERE component='portfolio_risk_engine';" -Label "A1 BE-6 compver absence"
    if ($PreBe6Compver -ne "0") {
        throw "FAIL: A1 - a BE-6 computation-version row is already present. Stopping; report to ITRGA."
    }
    $PermPreOut = Invoke-Py -PyArgs @("permbe5", ${TargetDbPath}) -Label "A1 permission baseline (BE-5 octet content-exact)"
    $PermPreText = (Norm-Text $PermPreOut).Trim()
    if ($PermPreText -notlike "PASS:perm_rows_exact*") {
        throw "FAIL: A1 - the permission baseline failed content re-proof: ${PermPreText}. Stopping; report to ITRGA."
    }
    $PrePermTotal = Get-PyScalar -Sql "SELECT COUNT(*) FROM v2_permission;" -Label "A1 permission count"
    if ($PrePermTotal -ne "35") {
        throw "FAIL: A1 - v2_permission row count '${PrePermTotal}', expected 35 (the 0045 terminal state). Stopping; report to ITRGA."
    }
    $PreBe6PermCount = Get-PyScalar -Sql "SELECT COUNT(*) FROM v2_permission WHERE permission LIKE 'v2.research.portfolio%';" -Label "A1 BE-6 permission absence"
    if ($PreBe6PermCount -ne "0") {
        throw "FAIL: A1 - BE-6 permission rows already present ('${PreBe6PermCount}'). Stopping; report to ITRGA."
    }
    $EmptyPre5 = Invoke-Py -PyArgs @("reportempty5", ${TargetDbPath}) -Label "A1 BE-5 tables empty (strict)"
    if ((Norm-Text $EmptyPre5).Trim() -ne "PASS:be5_tables_empty") {
        throw "FAIL: A1 - the five BE-5 tables are not empty at baseline. Stopping; report to ITRGA."
    }
    $ProvPre = Get-PyScalar -Sql "SELECT source_status, entitlement_status, persistence_permitted FROM v2_md_provider WHERE provider_id='twelvedata';" -Label "A1 inherited provider row"
    if ($ProvPre -ne "contract_tested|verified|0") {
        throw "FAIL: A1 - inherited provider row is '${ProvPre}', expected 'contract_tested|verified|0'. Stopping; report to ITRGA."
    }
    $RowsPre = Invoke-Py -PyArgs @("verifyrows", ${TargetDbPath}) -Label "A1 inherited history exact-content"
    if ((Norm-Text $RowsPre).Trim() -ne "PASS:history_rows_exact") {
        throw "FAIL: A1 - inherited history content differs from the pinned state. Stopping; report to ITRGA."
    }
    $AuditPre = Invoke-Py -PyArgs @("verifyaudit", ${TargetDbPath}) -Label "A1 inherited audit exact-content"
    if ((Norm-Text $AuditPre).Trim() -ne "PASS:audit_rows_exact") {
        throw "FAIL: A1 - inherited audit content differs from the pinned state. Stopping; report to ITRGA."
    }
    # Record-only digests (restart-lawful content; equality re-proven
    # across the mutation in A5.7): full audit event table, lineage
    # record table, and the two BE-4 report tables.
    $AuditDigestPre = Invoke-Py -PyArgs @("tabledigest", ${TargetDbPath}, "v2_audit_event") -Label "A1 audit-event table digest (pre; record-only)"
    $LineageDigestPre = Invoke-Py -PyArgs @("tabledigest", ${TargetDbPath}, "v2_lineage_record") -Label "A1 lineage-record table digest (pre; record-only)"
    $McrDigestPre = Invoke-Py -PyArgs @("tabledigest", ${TargetDbPath}, "v2_market_context_report") -Label "A1 BE-4 market-context report digest (pre; record-only)"
    $CirDigestPre = Invoke-Py -PyArgs @("tabledigest", ${TargetDbPath}, "v2_chart_intelligence_report") -Label "A1 BE-4 chart-intelligence report digest (pre; record-only)"
    $Be6TablesPre = Get-PyScalar -Sql "SELECT COUNT(*) FROM sqlite_master WHERE type='table' AND name IN ('v2_portfolio_definition','v2_portfolio_risk_report');" -Label "A1 BE-6 table absence"
    if ($Be6TablesPre -ne "0") {
        throw "FAIL: A1 - BE-6 tables already present ('${Be6TablesPre}'). Stopping; report to ITRGA."
    }
    Write-Evidence "PASS: A1.5 - 0045 terminal state re-proven by content: compver 5 (mge/sge recomputed on this machine); permissions 35 with the BE-5 octet exact and zero BE-6 rows; all five BE-5 tables empty; provider/history/audit anchors exact; four record-only digests captured; BE-6 schema fully absent (tables/compver/perms/triggers all zero)."

    # Alembic version (recorded environment evidence).
    Write-Evidence ""
    Write-Evidence "Alembic version (recorded environment evidence):"
    $prev = $ErrorActionPreference
    $ErrorActionPreference = "Continue"
    try {
        $VerOut  = & $Python -m alembic --version 2>&1
        $VerCode = $LASTEXITCODE
    } finally {
        $ErrorActionPreference = $prev
    }
    Emit-Output $VerOut
    if ($VerCode -ne 0) {
        throw "FAIL: A1 - could not record the alembic version (exit code ${VerCode}). Stopping before any modification; report to ITRGA."
    }

'''
rep_between(OLD_A1_START, OLD_A1_END, NEW_A1, 'R8-a1', keep_end=True)

# ============================================================
# PART 1 DONE. Print op count; part 2 applied by build_0046_apply2.py
# ============================================================
for old, new, tag in ops:
    assert s.count(old) == 1, tag
    s = s.replace(old, new, 1)
io.open('/home/user/scratch/stage1.ps1', 'w', encoding='utf-8', newline='\n').write(s)
print('PART1 OK:', len(ops), 'ops applied; stage1.ps1 written;', s.count(chr(10)) + 1, 'lines')
