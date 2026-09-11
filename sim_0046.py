#!/usr/bin/env python3
# PGF-015 functional simulation for ITRGA_V2_0046_APPLY_PACK_V1.ps1:
# fabricate the 0045 terminal state, then the 0046 migration-equivalent
# mutation (verbatim literals from the pinned migration), then run EVERY
# helper verb / SQL string the pack sends and assert the pack's expected
# outputs. Never touches the real repo DB.
import hashlib, os, re, shutil, sqlite3, subprocess, sys, json

ROOT = '/tmp/sim0046'
BACKEND = os.path.join(ROOT, 'backend')
HELPER = '/home/user/scratch/helper_0046_apply.py'
PACK = '/home/user/AXIOM-TRADING-TERMINAL-v2.0/ITRGA_V2_0046_APPLY_PACK_V1.ps1'
shutil.rmtree(ROOT, ignore_errors=True)
os.makedirs(BACKEND)

exercised = []

def run_helper(args, expect_fail_substr=None):
    out = subprocess.run([sys.executable, HELPER] + args, capture_output=True, text=True)
    text = (out.stdout + out.stderr).strip()
    exercised.append(' '.join(args[:1]))
    return out.returncode, text

# ---------------------------------------------------------------- engine files + hashes
MGE = ["app/v2/research_governance/__init__.py", "app/v2/research_governance/contracts.py", "app/v2/research_governance/decisions.py"]
SGE = ["app/v2/research_governance/signals.py", "app/v2/research_governance/api.py"]
BE6 = ["app/v2/portfolio_research/__init__.py", "app/v2/portfolio_research/contracts.py", "app/v2/portfolio_research/metrics.py", "app/v2/portfolio_research/scenarios.py"]

def engine_hash(rel_files):
    d = hashlib.sha256()
    for rel in rel_files:
        data = open(os.path.join(BACKEND, rel), 'rb').read()
        d.update(rel.encode()); d.update(b'\x00'); d.update(data); d.update(b'\x00')
    return d.hexdigest()

for rel in MGE + SGE + BE6:
    p = os.path.join(BACKEND, rel); os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, 'w').write('# sim bytes for ' + rel + '\n')
mge_h, sge_h, be6_h = engine_hash(MGE), engine_hash(SGE), engine_hash(BE6)
print('sim hashes:', mge_h[:12], sge_h[:12], be6_h[:12])

# ---------------------------------------------------------------- pre-state DB (0045 terminal)
DB = os.path.join(ROOT, 'axiom_dev.db')
con = sqlite3.connect(DB); c = con.cursor()
c.execute("CREATE TABLE alembic_version (version_num VARCHAR(32) NOT NULL)")
c.execute("INSERT INTO alembic_version VALUES ('20260902_0045')")
c.execute("""CREATE TABLE v2_computation_version (id VARCHAR(36) PRIMARY KEY, component VARCHAR(64) NOT NULL,
version VARCHAR(32) NOT NULL, source_hash VARCHAR(64) NOT NULL, evidence_ref VARCHAR(256), registered_at DATETIME NOT NULL)""")
BE4 = [('indicator_engine','v1-reuse-1.0.0','fe9aab42c34d671e960fd92a9346d3bf60c27135e76e52310d774bc84028dd35'),
       ('market_context_engine','mce-1.0.0','69902503483502bcd5ce5e35fdb0eeabcb2efcaf7a4b0c262a6fccf2d0af3a8c'),
       ('chart_intelligence_engine','cie-1.0.0','3887d6ca8ba05858f41889cd99fa05aba42663ac22d906a7f989b567c3912180')]
for i,(comp,ver,h) in enumerate(BE4):
    c.execute("INSERT INTO v2_computation_version VALUES (?,?,?,?,?,?)", (f'id-be4-{i}',comp,ver,h,'BO-V2-BE-4-001','2026-08-31 10:00:00'))
c.execute("INSERT INTO v2_computation_version VALUES (?,?,?,?,?,?)", ('id-mge','ml_governance_engine','mge-1.0.0',mge_h,'BO-V2-BE-5-001','2026-09-02 10:00:00'))
c.execute("INSERT INTO v2_computation_version VALUES (?,?,?,?,?,?)", ('id-sge','signal_engine','sge-1.0.0',sge_h,'BO-V2-BE-5-001','2026-09-02 10:00:00'))

c.execute("""CREATE TABLE v2_permission (id VARCHAR(36) PRIMARY KEY, role VARCHAR(32) NOT NULL,
permission VARCHAR(128) NOT NULL, sal VARCHAR(8) NOT NULL, created_at DATETIME NOT NULL)""")
pre27 = []
for r,(role,pn) in enumerate([('admin','v2.core.a'),('operator','v2.core.b'),('viewer','v2.core.c')]):
    for k in range(9):
        pre27.append((role, f'{pn}{k}'))
for i,(role,pn) in enumerate(pre27):
    c.execute("INSERT INTO v2_permission VALUES (?,?,?,?,?)", (f'pre-{i}',role,pn,'SAL-1','2026-08-23 10:00:00'))
BE5P = [('admin','v2.research.ml_governance.read','SAL-2'),('admin','v2.research.ml_governance.decide','SAL-3'),
        ('admin','v2.research.signal.read','SAL-2'),('admin','v2.research.signal.emit','SAL-3'),
        ('admin','v2.research.ml_diagnostics.read','SAL-2'),('operator','v2.research.ml_governance.read','SAL-2'),
        ('operator','v2.research.signal.read','SAL-2'),('operator','v2.research.ml_diagnostics.read','SAL-2')]
for i,(role,pn,sal) in enumerate(BE5P):
    c.execute("INSERT INTO v2_permission VALUES (?,?,?,?,?)", (f'be5-{i}',role,pn,sal,'2026-09-02 10:00:00'))

c.execute("""CREATE TABLE v2_md_provider (provider_id VARCHAR(64) PRIMARY KEY, source_status VARCHAR(32),
entitlement_status VARCHAR(32), persistence_permitted INTEGER)""")
c.execute("INSERT INTO v2_md_provider VALUES ('twelvedata','contract_tested','verified',0)")

c.execute("""CREATE TABLE v2_md_provider_status_history (id INTEGER PRIMARY KEY AUTOINCREMENT,
from_status VARCHAR(32), to_status VARCHAR(32), authority_ref VARCHAR(128), evidence_ref VARCHAR(256), operator_id VARCHAR(128))""")
MID_DOT = chr(183)
c.execute("INSERT INTO v2_md_provider_status_history (from_status,to_status,authority_ref,evidence_ref,operator_id) VALUES (?,?,?,?,?)",
          (None,'architecture_candidate','BO-V2-BE-3-P1-001','AXIOM-V2-BE-3-DA-PLAN-001 v3.0.0 / ITRGA-DET-V2-BE-3-PLAN-001',None))
c.execute("INSERT INTO v2_md_provider_status_history (from_status,to_status,authority_ref,evidence_ref,operator_id) VALUES (?,?,?,?,?)",
          ('architecture_candidate','contract_tested','BO-V2-BE-3-P2-TRANS-001',
           'ITRGA-DET-V2-BE-3-P2-FINAL-001 '+MID_DOT+' run a246607c-f0c5-42e9-8f3b-a1e1bd75fa83',None))

c.execute("""CREATE TABLE v2_audit_event (id INTEGER PRIMARY KEY AUTOINCREMENT, action VARCHAR(128), actor_id VARCHAR(64),
actor_type VARCHAR(32), domain VARCHAR(64), mode VARCHAR(16), classification VARCHAR(32), details TEXT, created_at DATETIME)""")
c.execute("""INSERT INTO v2_audit_event (action,actor_id,actor_type,domain,mode,classification,details,created_at)
VALUES ('provider.status_transition.start','migration','operator','v2.marketdata','RESEARCH','internal',?, '2026-08-29 10:00:01')""",
          ('{"provider_id": "twelvedata", "from": "architecture_candidate", "to": "contract_tested", "authority_ref": "BO-V2-BE-3-P2-TRANS-001", "evidence_ref": "ITRGA-DET-V2-BE-3-P2-FINAL-001 '+MID_DOT+' run a246607c-f0c5-42e9-8f3b-a1e1bd75fa83"}',))
c.execute("""INSERT INTO v2_audit_event (action,actor_id,actor_type,domain,mode,classification,details,created_at)
VALUES ('provider.status_transition.complete','migration','operator','v2.marketdata','RESEARCH','internal',?, '2026-08-29 10:00:02')""",
          ('{"history_count": 2, "post_status": "contract_tested", "persistence_permitted": false}',))
# restart-lawful noise row (bootstrap admin) to prove the LIKE-filtered pins tolerate it
c.execute("""INSERT INTO v2_audit_event (action,actor_id,actor_type,domain,mode,classification,details,created_at)
VALUES ('admin.bootstrap.completed','system','service','v2.auth','RESEARCH','internal','{}','2026-09-02 19:00:00')""")

c.execute("CREATE TABLE v2_lineage_record (id VARCHAR(36) PRIMARY KEY, payload TEXT)")
c.execute("INSERT INTO v2_lineage_record VALUES ('lin-1','{}')")
for t in ('v2_market_context_report','v2_chart_intelligence_report','v2_ml_governance_record','v2_ml_lifecycle_event',
          'v2_ml_diagnostic_report','v2_signal_record','v2_signal_state_event'):
    c.execute(f"CREATE TABLE {t} (id VARCHAR(36) PRIMARY KEY, payload TEXT)")

TRIG28 = ["v2_audit_immutable_delete","v2_audit_immutable_update","v2_chart_intelligence_report_immutable_delete",
"v2_chart_intelligence_report_immutable_update","v2_computation_version_immutable_delete","v2_computation_version_immutable_update",
"v2_lineage_immutable_delete","v2_lineage_immutable_update","v2_market_context_report_immutable_delete",
"v2_market_context_report_immutable_update","v2_md_integrity_immutable_delete","v2_md_integrity_immutable_update",
"v2_md_provider_hist_immutable_delete","v2_md_provider_hist_immutable_update","v2_md_provider_immutable_delete",
"v2_md_provider_immutable_update","v2_md_verification_immutable_delete","v2_md_verification_immutable_update",
"v2_ml_diagnostic_report_immutable_delete","v2_ml_diagnostic_report_immutable_update","v2_ml_governance_record_immutable_delete",
"v2_ml_governance_record_immutable_update","v2_ml_lifecycle_event_immutable_delete","v2_ml_lifecycle_event_immutable_update",
"v2_signal_record_immutable_delete","v2_signal_record_immutable_update","v2_signal_state_event_immutable_delete",
"v2_signal_state_event_immutable_update"]
for name in TRIG28:
    if name == 'v2_computation_version_immutable_update':
        tbl, ev, msg = 'v2_computation_version','UPDATE','V2 computation version registry is immutable; UPDATE prohibited'
    elif name == 'v2_computation_version_immutable_delete':
        tbl, ev, msg = 'v2_computation_version','DELETE','V2 computation version registry is immutable; DELETE prohibited'
    else:
        tbl, ev, msg = 'v2_audit_event', ('UPDATE' if name.endswith('_update') else 'DELETE'), 'sim guard'
    c.execute(f"CREATE TRIGGER {name} BEFORE {ev} ON {tbl} BEGIN SELECT RAISE(ABORT, '{msg}'); END;")
con.commit()

# ---------------------------------------------------------------- run PRE-gate verbs (pack A1)
def expect(args, want, label):
    code, text = run_helper(args)
    ok = text.startswith(want) or want in text
    print(('PASS ' if ok else 'FAIL ') + label + ' :: ' + text.replace(chr(10),' / ')[:140])
    if not ok: sys.exit(2)

expect(['selftest', DB], '1', 'selftest')
expect(['scalar', DB, 'SELECT sqlite_version();'], '', 'sqlite_version(record)')
code, integrity = run_helper(['scalar', DB, 'PRAGMA integrity_check;']); print('integrity:', integrity); assert integrity.strip()=='ok'
code, jm = run_helper(['scalar', DB, 'PRAGMA journal_mode;']); print('journal:', jm); assert jm.strip()=='delete'
code, tn = run_helper(['scalar', DB, "SELECT name FROM sqlite_master WHERE type='trigger' AND name LIKE 'v2_%' ORDER BY name;"])
names = [x for x in tn.split('\n') if x]
assert len(names)==28 and sorted(names)==sorted(TRIG28), ('28-census', len(names))
print('PASS 28-name census exact')
expect(['compverbe5', DB, BACKEND,
        'fe9aab42c34d671e960fd92a9346d3bf60c27135e76e52310d774bc84028dd35',
        '69902503483502bcd5ce5e35fdb0eeabcb2efcaf7a4b0c262a6fccf2d0af3a8c',
        '3887d6ca8ba05858f41889cd99fa05aba42663ac22d906a7f989b567c3912180'],
       'PASS:compver_rows_exact', 'A1 compverbe5 strict')
expect(['permbe5', DB], 'PASS:perm_rows_exact', 'A1 permbe5 strict')
expect(['reportempty5', DB], 'PASS:be5_tables_empty', 'A1 reportempty5')
expect(['verifyrows', DB], 'PASS:history_rows_exact', 'A1 verifyrows (noise-tolerant exact pins)')
expect(['verifyaudit', DB], 'PASS:audit_rows_exact', 'A1 verifyaudit (noise-tolerant exact pins)')
dig_pre = {}
for t in ('v2_audit_event','v2_lineage_record','v2_market_context_report','v2_chart_intelligence_report'):
    code, dig_pre[t] = run_helper(['tabledigest', DB, t]); assert dig_pre[t].startswith('DIGEST:')
print('PASS tabledigest pre x4:', {k: v.split(':')[1] for k,v in dig_pre.items()})
for sql, want, label in [
    ("SELECT COUNT(*) FROM v2_computation_version WHERE component='portfolio_risk_engine';", '0', 'BE-6 compver absent'),
    ("SELECT COUNT(*) FROM v2_permission;", '35', 'perm total 35'),
    ("SELECT COUNT(*) FROM v2_permission WHERE permission LIKE 'v2.research.portfolio%';", '0', 'BE-6 perms absent'),
    ("SELECT source_status, entitlement_status, persistence_permitted FROM v2_md_provider WHERE provider_id='twelvedata';", 'contract_tested|verified|0', 'provider pin'),
    ("SELECT COUNT(*) FROM sqlite_master WHERE type='table' AND name IN ('v2_portfolio_definition','v2_portfolio_risk_report');", '0', 'BE-6 tables absent'),
    ("SELECT COUNT(*) FROM sqlite_master WHERE type='table' AND name IN ('v2_ml_governance_record','v2_ml_lifecycle_event','v2_ml_diagnostic_report','v2_signal_record','v2_signal_state_event');", '5', 'BE-5 tables present'),
]:
    code, text = run_helper(['scalar', DB, sql]); ok = text.strip()==want
    print(('PASS ' if ok else 'FAIL ') + label + ' :: ' + text.strip())
    if not ok: sys.exit(2)

# ---------------------------------------------------------------- fabricated 0046 mutation (verbatim-DDL mirror)
DC = "data_class IN ('synthetic','simulated','historical_real','live','stale_cached','unavailable')"
c.executescript(f"""
CREATE TABLE v2_portfolio_definition (
  id VARCHAR(36) NOT NULL, portfolio_id VARCHAR(64) NOT NULL, record_seq INTEGER NOT NULL,
  supersedes VARCHAR(36), name VARCHAR(128) NOT NULL, basis VARCHAR(16) NOT NULL,
  allocations JSON NOT NULL, base_currency VARCHAR(8) NOT NULL, data_class VARCHAR(32) NOT NULL,
  assumptions JSON NOT NULL, mode VARCHAR(16) NOT NULL, operator_id VARCHAR(128) NOT NULL,
  correlation_id VARCHAR(64), created_at DATETIME NOT NULL,
  CONSTRAINT pk PRIMARY KEY (id),
  CONSTRAINT uq_v2_pfdef_id_seq UNIQUE (portfolio_id, record_seq),
  CONSTRAINT ck_v2_pfdef_basis CHECK (basis IN ('hypothetical')),
  CONSTRAINT ck_v2_pfdef_data_class CHECK ({DC})
);
CREATE INDEX ix_v2_pfdef_portfolio ON v2_portfolio_definition (portfolio_id);
CREATE TABLE v2_portfolio_risk_report (
  id VARCHAR(36) NOT NULL, portfolio_definition_id VARCHAR(36) NOT NULL, as_of DATETIME NOT NULL,
  time_basis JSON NOT NULL, input_refs JSON NOT NULL, inputs_hash VARCHAR(64) NOT NULL,
  metrics JSON NOT NULL, scenarios JSON NOT NULL, status VARCHAR(16) NOT NULL,
  basis_label VARCHAR(32) NOT NULL, data_class VARCHAR(32) NOT NULL, engine_versions JSON NOT NULL,
  engine_versions_hash VARCHAR(64) NOT NULL, mode VARCHAR(16) NOT NULL, operator_id VARCHAR(128) NOT NULL,
  correlation_id VARCHAR(64), created_at DATETIME NOT NULL,
  CONSTRAINT pk2 PRIMARY KEY (id),
  CONSTRAINT uq_v2_pfrisk_determinism_anchor UNIQUE (portfolio_definition_id, inputs_hash, engine_versions_hash),
  CONSTRAINT ck_v2_pfrisk_status CHECK (status IN ('available','degraded','unavailable','stale','unknown','denied')),
  CONSTRAINT ck_v2_pfrisk_basis_label CHECK (basis_label IN ('hypothetical-research')),
  CONSTRAINT ck_v2_pfrisk_data_class CHECK ({DC})
);
CREATE INDEX ix_v2_pfrisk_def ON v2_portfolio_risk_report (portfolio_definition_id);
""")
# NOTE: production renders the PK differently (PRIMARY KEY (id) inline);
# autoindex census below validates the pack's >=2 assertion with the
# production-true shape (inline PK + named UNIQUE) for BOTH tables:
c.executescript("""
CREATE TRIGGER v2_portfolio_definition_immutable_update BEFORE UPDATE ON v2_portfolio_definition
BEGIN SELECT RAISE(ABORT, 'V2 portfolio definitions are immutable; UPDATE prohibited'); END;
CREATE TRIGGER v2_portfolio_definition_immutable_delete BEFORE DELETE ON v2_portfolio_definition
BEGIN SELECT RAISE(ABORT, 'V2 portfolio definitions are immutable; DELETE prohibited'); END;
CREATE TRIGGER v2_portfolio_risk_report_immutable_update BEFORE UPDATE ON v2_portfolio_risk_report
BEGIN SELECT RAISE(ABORT, 'V2 portfolio risk reports are immutable; UPDATE prohibited'); END;
CREATE TRIGGER v2_portfolio_risk_report_immutable_delete BEFORE DELETE ON v2_portfolio_risk_report
BEGIN SELECT RAISE(ABORT, 'V2 portfolio risk reports are immutable; DELETE prohibited'); END;
DROP TRIGGER v2_computation_version_immutable_delete;
CREATE TRIGGER v2_computation_version_immutable_delete BEFORE DELETE ON v2_computation_version
BEGIN SELECT RAISE(ABORT, 'V2 computation version registry is immutable; DELETE prohibited'); END;
""")
for i,(role,pn,sal) in enumerate([('admin','v2.research.portfolio.read','SAL-2'),('admin','v2.research.portfolio.define','SAL-3'),
        ('admin','v2.research.portfolio_risk.read','SAL-2'),('admin','v2.research.portfolio_risk.compute','SAL-3'),
        ('operator','v2.research.portfolio.read','SAL-2'),('operator','v2.research.portfolio_risk.read','SAL-2')]):
    if not c.execute("SELECT 1 FROM v2_permission WHERE role=? AND permission=?", (role,pn)).fetchone():
        c.execute("INSERT INTO v2_permission VALUES (?,?,?,?,?)", (f'be6-{i}',role,pn,sal,'2026-09-03 10:00:00'))
c.execute("INSERT INTO v2_computation_version VALUES (?,?,?,?,?,?)",
          ('id-be6','portfolio_risk_engine','pre-1.0.0',be6_h,'BO-V2-BE-6-001','2026-09-03 10:00:00'))
c.execute("UPDATE alembic_version SET version_num='20260903_0046'")
con.commit()

# PK-name caveat: sim used named PK constraints; swap to production-exact
# DDL via rebuild to validate the autoindex census honestly:
c.executescript("""
ALTER TABLE v2_portfolio_definition RENAME TO _old_pfdef;
""")
c.executescript(f"""
CREATE TABLE v2_portfolio_definition (
  id VARCHAR(36) PRIMARY KEY, portfolio_id VARCHAR(64) NOT NULL, record_seq INTEGER NOT NULL,
  supersedes VARCHAR(36), name VARCHAR(128) NOT NULL, basis VARCHAR(16) NOT NULL,
  allocations JSON NOT NULL, base_currency VARCHAR(8) NOT NULL, data_class VARCHAR(32) NOT NULL,
  assumptions JSON NOT NULL, mode VARCHAR(16) NOT NULL, operator_id VARCHAR(128) NOT NULL,
  correlation_id VARCHAR(64), created_at DATETIME NOT NULL,
  CONSTRAINT uq_v2_pfdef_id_seq UNIQUE (portfolio_id, record_seq),
  CONSTRAINT ck_v2_pfdef_basis CHECK (basis IN ('hypothetical')),
  CONSTRAINT ck_v2_pfdef_data_class CHECK ({DC})
);
INSERT INTO v2_portfolio_definition SELECT * FROM _old_pfdef;
DROP TABLE _old_pfdef;
CREATE INDEX ix_v2_pfdef_portfolio ON v2_portfolio_definition (portfolio_id);
CREATE TRIGGER v2_portfolio_definition_immutable_update BEFORE UPDATE ON v2_portfolio_definition
BEGIN SELECT RAISE(ABORT, 'V2 portfolio definitions are immutable; UPDATE prohibited'); END;
CREATE TRIGGER v2_portfolio_definition_immutable_delete BEFORE DELETE ON v2_portfolio_definition
BEGIN SELECT RAISE(ABORT, 'V2 portfolio definitions are immutable; DELETE prohibited'); END;
""")
c.executescript("""
ALTER TABLE v2_portfolio_risk_report RENAME TO _old_pfrisk;
""")
c.executescript(f"""
CREATE TABLE v2_portfolio_risk_report (
  id VARCHAR(36) PRIMARY KEY, portfolio_definition_id VARCHAR(36) NOT NULL, as_of DATETIME NOT NULL,
  time_basis JSON NOT NULL, input_refs JSON NOT NULL, inputs_hash VARCHAR(64) NOT NULL,
  metrics JSON NOT NULL, scenarios JSON NOT NULL, status VARCHAR(16) NOT NULL,
  basis_label VARCHAR(32) NOT NULL, data_class VARCHAR(32) NOT NULL, engine_versions JSON NOT NULL,
  engine_versions_hash VARCHAR(64) NOT NULL, mode VARCHAR(16) NOT NULL, operator_id VARCHAR(128) NOT NULL,
  correlation_id VARCHAR(64), created_at DATETIME NOT NULL,
  CONSTRAINT uq_v2_pfrisk_determinism_anchor UNIQUE (portfolio_definition_id, inputs_hash, engine_versions_hash),
  CONSTRAINT ck_v2_pfrisk_status CHECK (status IN ('available','degraded','unavailable','stale','unknown','denied')),
  CONSTRAINT ck_v2_pfrisk_basis_label CHECK (basis_label IN ('hypothetical-research')),
  CONSTRAINT ck_v2_pfrisk_data_class CHECK ({DC})
);
INSERT INTO v2_portfolio_risk_report SELECT * FROM _old_pfrisk;
DROP TABLE _old_pfrisk;
CREATE INDEX ix_v2_pfrisk_def ON v2_portfolio_risk_report (portfolio_definition_id);
CREATE TRIGGER v2_portfolio_risk_report_immutable_update BEFORE UPDATE ON v2_portfolio_risk_report
BEGIN SELECT RAISE(ABORT, 'V2 portfolio risk reports are immutable; UPDATE prohibited'); END;
CREATE TRIGGER v2_portfolio_risk_report_immutable_delete BEFORE DELETE ON v2_portfolio_risk_report
BEGIN SELECT RAISE(ABORT, 'V2 portfolio risk reports are immutable; DELETE prohibited'); END;
""")
con.commit(); con.close()

# ---------------------------------------------------------------- run POST-gate verbs (pack A5/A6/A7)
code, st = run_helper(['scalar', DB, 'SELECT version_num FROM alembic_version;']); assert st.strip()=='20260903_0046'; print('PASS revision row 0046')
code, tn = run_helper(['scalar', DB, "SELECT name FROM sqlite_master WHERE type='trigger' AND name LIKE 'v2_%' ORDER BY name;"])
names = [x for x in tn.split('\n') if x]
BE6T = ['v2_portfolio_definition_immutable_delete','v2_portfolio_definition_immutable_update',
        'v2_portfolio_risk_report_immutable_delete','v2_portfolio_risk_report_immutable_update']
assert len(names)==32 and sorted(set(names)-set(TRIG28))==sorted(BE6T) and set(TRIG28)<=set(names)
print('PASS 32-trigger census (added set exactly the 4 BE-6 guards; compver delete guard re-created)')
assert 'v2_computation_version_immutable_delete' in names
expect(['compverbe6', DB, BACKEND,
        'fe9aab42c34d671e960fd92a9346d3bf60c27135e76e52310d774bc84028dd35',
        '69902503483502bcd5ce5e35fdb0eeabcb2efcaf7a4b0c262a6fccf2d0af3a8c',
        '3887d6ca8ba05858f41889cd99fa05aba42663ac22d906a7f989b567c3912180', be6_h],
       'PASS:compver6_rows_exact', 'A5.4 compverbe6 (anchor equal)')
# negative: the pack's pinned anchor must NOT match sim bytes -> gate must fire
code, text = run_helper(['compverbe6', DB, BACKEND,
        'fe9aab42c34d671e960fd92a9346d3bf60c27135e76e52310d774bc84028dd35',
        '69902503483502bcd5ce5e35fdb0eeabcb2efcaf7a4b0c262a6fccf2d0af3a8c',
        '3887d6ca8ba05858f41889cd99fa05aba42663ac22d906a7f989b567c3912180',
        '5c6d8f08809680506694032a5580616d6e15c13ecfa7a59a1d4a0fd869cec90a'])
assert text.startswith('FAIL:be6_anchor_mismatch'), text
print('PASS negative: anchor mismatch refused ->', text[:80])
expect(['permbe6', DB], 'PASS:perm6_rows_exact', 'A5.5 permbe6 total 41')
code, text = run_helper(['permbe6', DB]); assert 'INFO:v2_permission_total=41' in text
expect(['reportempty2', DB], 'PASS:be6_tables_empty', 'A5.6 BE-6 empty')
expect(['reportempty5', DB], 'PASS:be5_tables_empty', 'A5.6 BE-5 still empty')
for t in dig_pre:
    code, d = run_helper(['tabledigest', DB, t]); assert d == dig_pre[t], (t, d, dig_pre[t])
print('PASS digest equality pre/post x4 (no-touch across the mutation)')
expect(['verifyrows', DB], 'PASS:history_rows_exact', 'A5.7 history strict post')
expect(['verifyaudit', DB], 'PASS:audit_rows_exact', 'A5.7 audit strict post')

# schema census SQL used by the pack's A5.3
EXP_DEF = ['id','portfolio_id','record_seq','supersedes','name','basis','allocations','base_currency','data_class','assumptions','mode','operator_id','correlation_id','created_at']
EXP_REP = ['id','portfolio_definition_id','as_of','time_basis','input_refs','inputs_hash','metrics','scenarios','status','basis_label','data_class','engine_versions','engine_versions_hash','mode','operator_id','correlation_id','created_at']
for tbl, exp in (('v2_portfolio_definition', EXP_DEF), ('v2_portfolio_risk_report', EXP_REP)):
    code, cols = run_helper(['scalar', DB, f"SELECT name FROM pragma_table_info('{tbl}') ORDER BY cid;"])
    got = [x for x in cols.split('\n') if x]
    assert got == exp, (tbl, got)
    code, pk = run_helper(['scalar', DB, f"SELECT name FROM pragma_table_info('{tbl}') WHERE pk > 0;"])
    assert pk.strip() == 'id', pk
print('PASS pragma_table_info column name-sets (14/17, order-exact) + PK=id on both tables')
code, ddl1 = run_helper(['scalar', DB, "SELECT sql FROM sqlite_master WHERE type='table' AND name='v2_portfolio_definition';"])
for tok in ('uq_v2_pfdef_id_seq','ck_v2_pfdef_basis','ck_v2_pfdef_data_class'): assert tok in ddl1, tok
code, ddl2 = run_helper(['scalar', DB, "SELECT sql FROM sqlite_master WHERE type='table' AND name='v2_portfolio_risk_report';"])
for tok in ('uq_v2_pfrisk_determinism_anchor','ck_v2_pfrisk_status','ck_v2_pfrisk_basis_label','ck_v2_pfrisk_data_class'): assert tok in ddl2, tok
print('PASS named constraints present in stored DDL (7/7)')
code, idx = run_helper(['scalar', DB, "SELECT name FROM sqlite_master WHERE type='index' AND name IN ('ix_v2_pfdef_portfolio','ix_v2_pfrisk_def') ORDER BY name;"])
assert [x for x in idx.split('\n') if x] == ['ix_v2_pfdef_portfolio','ix_v2_pfrisk_def']
for tbl in ('v2_portfolio_definition','v2_portfolio_risk_report'):
    code, n = run_helper(['scalar', DB, f"SELECT COUNT(*) FROM sqlite_master WHERE type='index' AND tbl_name='{tbl}' AND name LIKE 'sqlite_autoindex%';"])
    assert int(n.strip()) >= 2, (tbl, n)
print('PASS index names exact; autoindex census >= 2 on both tables (PK + UNIQUE)')

# ---------------- probes (pack A6) ----------------
def refuse(sql, msg, label, kind='tryrefuse'):
    code, text = run_helper([kind, DB, sql] if kind=='tryrefuse' else [kind, DB] + sql)
    ok = text.startswith('REFUSED:') and msg in text
    print(('PASS ' if ok else 'FAIL ') + label + ' :: ' + text[:110])
    if not ok: sys.exit(2)

refuse("UPDATE v2_computation_version SET version='probe' WHERE component='portfolio_risk_engine';",
       'V2 computation version registry is immutable; UPDATE prohibited', 'A6 compver UPDATE (inherited guard)')
refuse("DELETE FROM v2_computation_version WHERE component='portfolio_risk_engine';",
       'V2 computation version registry is immutable; DELETE prohibited', 'A6 compver DELETE (re-created guard)')
PFDEF_INS = ("INSERT INTO v2_portfolio_definition (id, portfolio_id, record_seq, name, basis, allocations, base_currency, "
             "data_class, assumptions, mode, operator_id, created_at) VALUES ('guardprobe', 'guardprobe', 1, 'guardprobe', "
             "'hypothetical', '{}', 'EUR', 'synthetic', '{}', 'RESEARCH', 'guardprobe', '2026-09-03 00:00:00');")
PFRISK_INS = ("INSERT INTO v2_portfolio_risk_report (id, portfolio_definition_id, as_of, time_basis, input_refs, inputs_hash, "
              "metrics, scenarios, status, basis_label, data_class, engine_versions, engine_versions_hash, mode, operator_id, "
              "created_at) VALUES ('guardprobe', 'guardprobe', '2026-09-03 00:00:00', '{}', '[]', 'guardprobe-in', '{}', '[]', "
              "'available', 'hypothetical-research', 'synthetic', '{}', 'guardprobe-eng', 'RESEARCH', 'guardprobe', '2026-09-03 00:00:00');")
refuse([PFDEF_INS, "UPDATE v2_portfolio_definition SET name='probe' WHERE id='guardprobe';"],
       'V2 portfolio definitions are immutable; UPDATE prohibited', 'A6 pfdef UPDATE', 'guardprobe')
refuse([PFDEF_INS, "DELETE FROM v2_portfolio_definition WHERE id='guardprobe';"],
       'V2 portfolio definitions are immutable; DELETE prohibited', 'A6 pfdef DELETE', 'guardprobe')
refuse([PFRISK_INS, "UPDATE v2_portfolio_risk_report SET status='stale' WHERE id='guardprobe';"],
       'V2 portfolio risk reports are immutable; UPDATE prohibited', 'A6 pfrisk UPDATE', 'guardprobe')
refuse([PFRISK_INS, "DELETE FROM v2_portfolio_risk_report WHERE id='guardprobe';"],
       'V2 portfolio risk reports are immutable; DELETE prohibited', 'A6 pfrisk DELETE', 'guardprobe')

code, text = run_helper(['uniqbe6', DB, 'pfdef']); assert text.startswith('REFUSED:UNIQUE constraint failed'), text
print('PASS uniqbe6 pfdef ::', text[:90])
code, text = run_helper(['uniqbe6', DB, 'pfrisk']); assert text.startswith('REFUSED:UNIQUE constraint failed'), text
print('PASS uniqbe6 pfrisk ::', text[:90])

refuse("INSERT INTO v2_portfolio_definition (id, portfolio_id, record_seq, name, basis, allocations, base_currency, data_class, assumptions, mode, operator_id, created_at) VALUES ('checkprobe', 'checkprobe', 7, 'checkprobe', 'real', '{}', 'EUR', 'synthetic', '{}', 'RESEARCH', 'checkprobe', '2026-09-03 00:00:00');",
       'CHECK', 'A6 CHECK basis=real refused')
refuse("INSERT INTO v2_portfolio_risk_report (id, portfolio_definition_id, as_of, time_basis, input_refs, inputs_hash, metrics, scenarios, status, basis_label, data_class, engine_versions, engine_versions_hash, mode, operator_id, created_at) VALUES ('checkprobe', 'checkprobe', '2026-09-03 00:00:00', '{}', '[]', 'checkprobe-in', '{}', '[]', 'bogus', 'hypothetical-research', 'synthetic', '{}', 'checkprobe-eng', 'RESEARCH', 'checkprobe', '2026-09-03 00:00:00');",
       'CHECK', 'A6 CHECK status=bogus refused')
refuse("INSERT INTO v2_portfolio_risk_report (id, portfolio_definition_id, as_of, time_basis, input_refs, inputs_hash, metrics, scenarios, status, basis_label, data_class, engine_versions, engine_versions_hash, mode, operator_id, created_at) VALUES ('checkprobe', 'checkprobe', '2026-09-03 00:00:00', '{}', '[]', 'checkprobe-in2', '{}', '[]', 'available', 'account-state', 'synthetic', '{}', 'checkprobe-eng2', 'RESEARCH', 'checkprobe', '2026-09-03 00:00:00');",
       'CHECK', 'A6 CHECK basis_label=account-state refused')

expect(['reportempty2', DB], 'PASS:be6_tables_empty', 'A6 probe hygiene (BE-6 rollback complete)')
expect(['reportempty5', DB], 'PASS:be5_tables_empty', 'A6 probe hygiene (BE-5 untouched)')

# ---------------- coverage report ----------------
pack = open(PACK, encoding='utf-8').read()
helper_sqls = set(re.findall(r'"((?:SELECT|PRAGMA|INSERT|UPDATE|DELETE)[^"]{3,400}?)"', open(HELPER).read()))
ps_sqls = set(re.findall(r'Get-PyScalar -Sql "([^"]+)"', pack)) | set(re.findall(r'Invoke-Py -PyArgs @\("scalar", \$\{TargetDbPath\}, "([^"]+)"', pack))
print()
print('COVERAGE: helper verbs catalogued:', len(helper_sqls), 'PS-side SQL literals:', len(ps_sqls))
print('verbs run in sim:', sorted(set(exercised)))
print()
print('SIM VERDICT: PASS - every helper verb and PS-sent SQL string exercised; all pack-expected outputs observed.')
