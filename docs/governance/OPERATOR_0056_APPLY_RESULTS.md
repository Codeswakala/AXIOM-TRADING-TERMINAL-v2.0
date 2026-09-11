PS C:\Users\victo\.vscode\AXIOM\axiom> powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\ITRGA_V2_0056_APPLY_PACK_V1.ps1

==============================================================================
A0. RUN IDENTIFICATION
==============================================================================
Pack: ITRGA-V2-0056-APPLY-PACK-V1
Act: 0056 working-database application act (single sanctioned mutation)
Implements: ITRGA-V2-0056-FIELD-APPLY-CARD-20260909 (governing text)
Authority: BO-V2-BE12D-001 SS1.g / ITRGA-REV-V2-BE12D-001 (APPROVED)
Started: 2026-09-09 15:58:58 +03:00
Target file: C:\Users\victo\.vscode\AXIOM\axiom\backend\axiom_dev.db
FIELD LAW: both new tables pinned ZERO ROWS throughout; NO governor verb runs; the valve never opens.
Server credentials used: NONE. Provider credentials used: NONE.

STOP THE RUNNING APPLICATION. Continuing in 5 seconds; press Ctrl+C otherwise...

==============================================================================
A0b. AUTHORITY/PRACTICE ENVIRONMENT SWEEP (must print nothing)
==============================================================================
PASS: A0b: no AXIOM_TD_* / AXIOM_BROKER_PRACTICE_* variables

==============================================================================
A0c. FILE EXISTENCE
==============================================================================
PASS: A0c.1 venv python present
PASS: A0c.2 target db present
PASS: A0c.3 migration 0056 present

==============================================================================
A0d. 12D SOURCE-SET VISIBILITY (thirteen lxe files)
==============================================================================
  present  app/v2/live_exec/intents.py
  present  app/v2/live_exec/eligibility.py
  present  app/v2/live_exec/risk.py
  present  app/v2/live_exec/locks.py
  present  app/v2/live_exec/submissions.py
  present  app/v2/live_exec/ack_fills.py
  present  app/v2/live_exec/modify/__init__.py
  present  app/v2/live_exec/modify/engine.py
  present  app/v2/live_exec/activation/__init__.py
  present  app/v2/live_exec/activation/engine.py
  present  app/v2/live_exec/activation/template.py
  present  app/v2/live_exec/killswitch/__init__.py
  present  app/v2/live_exec/killswitch/engine.py
PASS: A0d: all thirteen lxe source files present (12D landed)

==============================================================================
A1. BASELINE REVISION STATE
==============================================================================
INFO  [alembic.runtime.migration] Context impl SQLiteImpl.
INFO  [alembic.runtime.migration] Will assume non-transactional DDL.
20260909_0055
PASS: A1.0 alembic current exit 0
PASS: A1.1 current is exactly 20260909_0055 (no (head) suffix)
20260909_0056 (head)
PASS: A1.2 repo head is 20260909_0056 (head)
Alembic version: alembic 1.19.0

==============================================================================
A2. THE 0056 FILE PIN (byte-still recital)
==============================================================================
  length  10521 (pinned 10521)
  sha256  1A43E5A211609934F6C720D1FF595A1BA1B9374EA6D0C111BD762FDBBA4D7CD2
PASS: A2.1 migration length
PASS: A2.2 migration sha256

==============================================================================
A3. TATTOO PRE + NAMED-OBJECT PRE-LISTS
==============================================================================
PASS: A3.1 triggers total == 86
PASS: A3.2 v2_permission == 77
PASS: A3.3 v2_computation_version == 15
PASS: A3.4 live_exec guard set pre == the eight 12B/12C names (activation/kill pairs ABSENT)
PASS: A3.5 compver pre == ONLY lxe-1.0.0 + lxe-1.1.0 (content-exact)
PASS: A3.6 the six 12D permission rows ABSENT pre-apply
PASS: A3.7 both 12D tables ABSENT pre-apply
  12A intent ledger rows (recorded): 1
  12A intent digests (recorded): 7ac49b2873c332439958604f611c19609377db261d73124534743a271e13e618

==============================================================================
A4. HEALTH PRE + ANCHOR
==============================================================================
PASS: A4.1 integrity_check ok
PASS: A4.2 journal delete
PASS: A4.3 no sidecars
PASS: A4.4 anchor integrity ok
PASS: A4.5 anchor revision 20260909_0055
  anchor: C:\Users\victo\.vscode\AXIOM\axiom\operator-evidence\BE-12D\axiom_dev.db.pre-0056-20260909155857.bak
  anchor size 2641920 sha256 1413DDA4089B7D9981DE0A2C229C04CCF872D02B324F73A327E8285983579A6A

==============================================================================
A5. TRIPLE LXE PRE-COMPUTE GATES (halts precede any mutation)
==============================================================================
  6-file computed: b060f435c7c339fbe5e23daf8231af04bf62cd8cc43ccd7d8a5f5067b78bb8c2
PASS: A5a 12A/12B six-file lxe unmoved (b060f435...)
  8-file computed: d09306f1ab32f0dc6f26e5c7235b3e1f72c3175a1928d60673709c0b02a3809a
PASS: A5b 12C eight-file lxe unmoved (d09306f1...)
 13-file computed: d25c48579def993b63e6f84ca17e937c3e938f75b0ca1f78f8aea81b1e9c1705
PASS: A5c 12D thirteen-file lxe landed EXACTLY (d25c4857...)

==============================================================================
A6. REHEARSAL UPGRADE (byte-copy only)
==============================================================================
INFO  [alembic.runtime.migration] Context impl SQLiteImpl.
INFO  [alembic.runtime.migration] Will assume non-transactional DDL.
INFO  [alembic.runtime.migration] Running upgrade 20260909_0055 -> 20260909_0056, V2 BE-12D ù activation instrument + kill-switch (BO-V2-BE12D-001 º1.g).
PASS: A6.0 rehearsal upgrade exit 0
PASS: A6.1 exactly one Running upgrade line
PASS: A6.2 rehearsal console: token 'ERROR' absent
PASS: A6.2 rehearsal console: token 'Traceback' absent
PASS: A6.2 rehearsal console: token 'REFUSED' absent
PASS: A6.2 rehearsal console: token 'RuntimeError' absent
PASS: A6.2 rehearsal console: token 'NOT restored' absent
PASS: A6.3 rehearsal triggers 90
PASS: A6.4 rehearsal perms 83
PASS: A6.5 rehearsal compver 16
PASS: A6.6 rehearsal compver rows ALL THREE stand, content-exact
PASS: A6.7 rehearsal activation ZERO ROWS (no seeds)
PASS: A6.8 rehearsal kill_switch ZERO ROWS (no seeds)

==============================================================================
A7. REHEARSAL DOWNGRADE PROOF (full reversibility, on the copy)
==============================================================================
INFO  [alembic.runtime.migration] Context impl SQLiteImpl.
INFO  [alembic.runtime.migration] Will assume non-transactional DDL.
INFO  [alembic.runtime.migration] Running downgrade 20260909_0056 -> 20260909_0055, V2 BE-12D ù activation instrument + kill-switch (BO-V2-BE12D-001 º1.g).
PASS: A7.0 rehearsal downgrade exit 0
PASS: A7.1 exactly one Running downgrade line
PASS: A7.2 rehearsal console (incl. compver delete-guard dance silent): token 'ERROR' absent
PASS: A7.2 rehearsal console (incl. compver delete-guard dance silent): token 'Traceback' absent
PASS: A7.2 rehearsal console (incl. compver delete-guard dance silent): token 'REFUSED' absent
PASS: A7.2 rehearsal console (incl. compver delete-guard dance silent): token 'RuntimeError' absent
PASS: A7.2 rehearsal console (incl. compver delete-guard dance silent): token 'NOT restored' absent
PASS: A7.3 rehearsal revision restored 20260909_0055
PASS: A7.4 rehearsal triggers restored 86
PASS: A7.5 rehearsal perms restored 77
PASS: A7.6 rehearsal compver restored 15
PASS: A7.7 rehearsal both tables removed
PASS: A7.8 rehearsal compver == 1.0.0 + 1.1.0 only (1.2.0 removed)
NOTE (register-logged advisory, not a finding): recreated compver DELETE guard carries the migration literal (versions vs version registry); invariant identical; visible only on a downgraded chain.
PASS: A7.9 rehearsal recreated-guard refusal (documented literal)

==============================================================================
A8. THE APPLY (single sanctioned mutation, fielded file)
==============================================================================
Target: C:\Users\victo\.vscode\AXIOM\axiom\backend\axiom_dev.db
INFO  [alembic.runtime.migration] Context impl SQLiteImpl.
INFO  [alembic.runtime.migration] Will assume non-transactional DDL.
INFO  [alembic.runtime.migration] Running upgrade 20260909_0055 -> 20260909_0056, V2 BE-12D ù activation instrument + kill-switch (BO-V2-BE12D-001 º1.g).
PASS: A8.0 apply exit 0
PASS: A8.1 exactly one Running upgrade line
PASS: A8.2 apply console: token 'ERROR' absent
PASS: A8.2 apply console: token 'Traceback' absent
PASS: A8.2 apply console: token 'REFUSED' absent
PASS: A8.2 apply console: token 'RuntimeError' absent
PASS: A8.2 apply console: token 'NOT restored' absent

==============================================================================
A9. FIELDED TERMINAL STATE
==============================================================================
INFO  [alembic.runtime.migration] Context impl SQLiteImpl.
INFO  [alembic.runtime.migration] Will assume non-transactional DDL.
20260909_0056 (head)
PASS: A9.1 stamped 20260909_0056 (head)
PASS: A9.2 triggers 90
PASS: A9.3 perms 83
PASS: A9.4 compver 16
PASS: A9.5 twelve guard names exact
PASS: A9.6 eight indexes present exact
PASS: A9.7 activation table present, ZERO ROWS (field law)
PASS: A9.8 kill_switch table present, ZERO ROWS (field law)
PASS: A9.9 all five 12B/12C/12D tables present
PASS: A9.9b 12B submissions still 0
PASS: A9.9c 12B fill_events still 0
PASS: A9.9d 12C modify_events still 0
PASS: A9.10 six 12D permission rows content-exact
PASS: A9.11 compver rows ALL THREE stand, content-exact (DB == disk)
PASS: A9.12 12A intent ledger count unchanged
PASS: A9.13 12A intent digests unchanged
PASS: A9.14 disk 6-file lxe still b060f435...
PASS: A9.15 disk 13-file lxe still d25c4857... (apply moves no source bytes)
A9.16 â€” the rendered CHECK names from the DB's own DDL (E-0055-A10.3 record):
CREATE TABLE v2_live_activation_instrument (
        id VARCHAR(36) NOT NULL, 
        sole VARCHAR(4) NOT NULL, 
        version VARCHAR(16) NOT NULL, 
        template_hash VARCHAR(64) NOT NULL, 
        funded_posture_ref VARCHAR(128) NOT NULL, 
        step_up_ref VARCHAR(128) NOT NULL, 
        operator_ref VARCHAR(128) NOT NULL, 
        correlation_ref VARCHAR(64), 
        actor_id VARCHAR(128) NOT NULL, 
        data_class VARCHAR(32) NOT NULL, 
        mode VARCHAR(16) NOT NULL, 
        operator_id VARCHAR(128) NOT NULL, 
        created_at DATETIME NOT NULL, 
        CONSTRAINT pk_v2_live_activation_instrument PRIMARY KEY (id), 
        CONSTRAINT ck_v2_live_activation_instrument_ck_v2_lai_sole CHECK (sole IN ('SOLE')), 
        CONSTRAINT ck_v2_live_activation_instrument_ck_v2_lai_version CHECK (version IN ('lai-1.0.0')), 
        CONSTRAINT ck_v2_live_activation_instrument_ck_v2_lai_data_class CHECK (data_class IN ('live_marker'))
)
CREATE TABLE v2_live_kill_switch (
        id VARCHAR(36) NOT NULL, 
        sole VARCHAR(4) NOT NULL, 
        status VARCHAR(16) NOT NULL, 
        step_up_ref VARCHAR(128) NOT NULL, 
        actor_id VARCHAR(128) NOT NULL, 
        data_class VARCHAR(32) NOT NULL, 
        mode VARCHAR(16) NOT NULL, 
        operator_id VARCHAR(128) NOT NULL, 
        correlation_id VARCHAR(64), 
        created_at DATETIME NOT NULL, 
        CONSTRAINT pk_v2_live_kill_switch PRIMARY KEY (id), 
        CONSTRAINT ck_v2_live_kill_switch_ck_v2_lks_sole CHECK (sole IN ('SOLE')), 
        CONSTRAINT ck_v2_live_kill_switch_ck_v2_lks_status CHECK (status IN ('armed','pulled','cleared')), 
        CONSTRAINT ck_v2_live_kill_switch_ck_v2_lks_data_class CHECK (data_class IN ('evidence'))
)

==============================================================================
A10. GUARD / CHECK REFUSALS (twelve; refused or rolled back; field law re-pinned after)
==============================================================================
REFUSED:V2 live activation instrument is immutable; UPDATE prohibited
rolledback=1
PASS: A10.1 activation UPDATE refusal exact + rolled back
REFUSED:V2 live activation instrument is immutable; DELETE prohibited
rolledback=1
PASS: A10.2 activation DELETE refusal exact + rolled back
REFUSED:V2 live kill switch is immutable; UPDATE prohibited
rolledback=1
PASS: A10.3 kill_switch UPDATE refusal exact + rolled back
REFUSED:V2 live kill switch is immutable; DELETE prohibited
rolledback=1
PASS: A10.4 kill_switch DELETE refusal exact + rolled back
PASS: A10.5 activation sole CHECK refusal exact (rendered name)
PASS: A10.6 activation version CHECK refusal exact (rendered name)
PASS: A10.7 force-simulation DIES at schema (rendered name)
PASS: A10.8 kill_switch sole CHECK refusal exact (rendered name)
PASS: A10.9 kill_switch status CHECK refusal exact (engaged is not a state)
PASS: A10.10 kill_switch data_class CHECK refusal exact (evidence only)
PASS: A10.11 compver UPDATE refusal (ORIGINAL literal)
PASS: A10.12 compver DELETE refusal (ORIGINAL literal)
PASS: A10.13 activation ZERO ROWS after all probes (field law)
PASS: A10.14 kill_switch ZERO ROWS after all probes (field law)

==============================================================================
A11. HEALTH POST + DRIFT (ITEMIZED LAW) + ENVIRONMENT CLOSE
==============================================================================
PASS: A11.1 integrity ok
PASS: A11.2 journal delete
PASS: A11.3 no sidecars
Drift law (ITEMIZED, E-0054-A11.4): exactly the 9 inherited V1 tokens; band tokens absent; silence is a pass-subset.
INFO  [alembic.runtime.migration] Context impl SQLiteImpl.
INFO  [alembic.runtime.migration] Will assume non-transactional DDL.
INFO  [alembic.runtime.plugins] setting up autogenerate plugin alembic.autogenerate.schemas
INFO  [alembic.runtime.plugins] setting up autogenerate plugin alembic.autogenerate.tables
INFO  [alembic.runtime.plugins] setting up autogenerate plugin alembic.autogenerate.types
INFO  [alembic.runtime.plugins] setting up autogenerate plugin alembic.autogenerate.constraints
INFO  [alembic.runtime.plugins] setting up autogenerate plugin alembic.autogenerate.defaults
INFO  [alembic.runtime.plugins] setting up autogenerate plugin alembic.autogenerate.comments
INFO  [alembic.runtime.plugins] setting up autogenerate plugin alembic.autogenerate.checkconstraint_byname
INFO  [alembic.autogenerate.compare.tables] Detected added table 'audit_write_failure_records'
INFO  [alembic.autogenerate.compare.constraints] Detected added index 'ix_audit_write_failures_category_action' on '('category', 'action')'
INFO  [alembic.autogenerate.compare.constraints] Detected added index 'ix_audit_write_failures_created' on '('created_at',)'
INFO  [alembic.autogenerate.compare.constraints] Detected removed index 'ix_advisory_signals_expires_at' on 'advisory_signals'
INFO  [alembic.autogenerate.compare.constraints] Detected removed index 'ix_advisory_signals_freshness_status' on 'advisory_signals'
INFO  [alembic.autogenerate.compare.constraints] Detected removed index 'ix_ingestion_runs_symbol_started' on 'ingestion_runs'
INFO  [alembic.autogenerate.compare.constraints] Detected removed index 'ix_model_artifacts_advisory_status' on 'model_artifacts'
INFO  [alembic.autogenerate.compare.constraints] Detected removed index 'ix_model_artifacts_artifact_hash' on 'model_artifacts'
INFO  [alembic.autogenerate.compare.constraints] Detected removed index 'ix_model_artifacts_experiment_id' on 'model_artifacts'
ERROR [alembic.util.messaging] New upgrade operations detected: [('add_table', Table('audit_write_failure_records', MetaData(), Column('id', String(length=36), table=<audit_write_failure_records>, primary_key=True, nullable=False, default=CallableColumnDefault(<function AuditWriteFailureRecord.<lambda> at 0x000001A52931A560>)), Column('category', String(length=64), table=<audit_write_failure_records>, nullable=False), Column('action', String(length=96), table=<audit_write_failure_records>, nullable=False), Column('message', Text(), table=<audit_write_failure_records>, nullable=False), Column('actor', String(length=128), table=<audit_write_failure_records>, nullable=False, default=ScalarElementColumnDefault('system')), Column('resource_type', String(length=64), table=<audit_write_failure_records>), Column('resource_id', String(length=128), table=<audit_write_failure_records>), Column('correlation_id', String(length=64), table=<audit_write_failure_records>), Column('details', JSON(), table=<audit_write_failure_records>), Column('failure_reason', Text(), table=<audit_write_failure_records>, nullable=False), Column('attempts', Integer(), table=<audit_write_failure_records>, nullable=False, default=ScalarElementColumnDefault(1)), Column('created_at', DateTime(timezone=True), table=<audit_write_failure_records>, nullable=False, default=CallableColumnDefault(<function utc_now at 0x000001A52931A4B0>)), schema=None)), ('add_index', Index('ix_audit_write_failures_category_action', Column('category', String(length=64), table=<audit_write_failure_records>, nullable=False), Column('action', String(length=96), table=<audit_write_failure_records>, nullable=False))), ('add_index', Index('ix_audit_write_failures_created', Column('created_at', DateTime(timezone=True), table=<audit_write_failure_records>, nullable=False, default=CallableColumnDefault(<function utc_now at 0x000001A52931A4B0>)))), ('remove_index', Index('ix_advisory_signals_expires_at', Column('expires_at', DATETIME(), table=<advisory_signals>))), ('remove_index', Index('ix_advisory_signals_freshness_status', Column('freshness_status', VARCHAR(length=64), table=<advisory_signals>))), ('remove_index', Index('ix_ingestion_runs_symbol_started', Column('symbol', VARCHAR(length=64), table=<ingestion_runs>, nullable=False), Column('started_at', DATETIME(), table=<ingestion_runs>, nullable=False))), ('remove_index', Index('ix_model_artifacts_advisory_status', Column('advisory_status', VARCHAR(length=64), table=<model_artifacts>))), ('remove_index', Index('ix_model_artifacts_artifact_hash', Column('artifact_hash', VARCHAR(length=128), table=<model_artifacts>))), ('remove_index', Index('ix_model_artifacts_experiment_id', Column('experiment_id', VARCHAR(length=96), table=<model_artifacts>)))]
FAILED: New upgrade operations detected: [('add_table', Table('audit_write_failure_records', MetaData(), Column('id', String(length=36), table=<audit_write_failure_records>, primary_key=True, nullable=False, default=CallableColumnDefault(<function AuditWriteFailureRecord.<lambda> at 0x000001A52931A560>)), Column('category', String(length=64), table=<audit_write_failure_records>, nullable=False), Column('action', String(length=96), table=<audit_write_failure_records>, nullable=False), Column('message', Text(), table=<audit_write_failure_records>, nullable=False), Column('actor', String(length=128), table=<audit_write_failure_records>, nullable=False, default=ScalarElementColumnDefault('system')), Column('resource_type', String(length=64), table=<audit_write_failure_records>), Column('resource_id', String(length=128), table=<audit_write_failure_records>), Column('correlation_id', String(length=64), table=<audit_write_failure_records>), Column('details', JSON(), table=<audit_write_failure_records>), Column('failure_reason', Text(), table=<audit_write_failure_records>, nullable=False), Column('attempts', Integer(), table=<audit_write_failure_records>, nullable=False, default=ScalarElementColumnDefault(1)), Column('created_at', DateTime(timezone=True), table=<audit_write_failure_records>, nullable=False, default=CallableColumnDefault(<function utc_now at 0x000001A52931A4B0>)), schema=None)), ('add_index', Index('ix_audit_write_failures_category_action', Column('category', String(length=64), table=<audit_write_failure_records>, nullable=False), Column('action', String(length=96), table=<audit_write_failure_records>, nullable=False))), ('add_index', Index('ix_audit_write_failures_created', Column('created_at', DateTime(timezone=True), table=<audit_write_failure_records>, nullable=False, default=CallableColumnDefault(<function utc_now at 0x000001A52931A4B0>)))), ('remove_index', Index('ix_advisory_signals_expires_at', Column('expires_at', DATETIME(), table=<advisory_signals>))), ('remove_index', Index('ix_advisory_signals_freshness_status', Column('freshness_status', VARCHAR(length=64), table=<advisory_signals>))), ('remove_index', Index('ix_ingestion_runs_symbol_started', Column('symbol', VARCHAR(length=64), table=<ingestion_runs>, nullable=False), Column('started_at', DATETIME(), table=<ingestion_runs>, nullable=False))), ('remove_index', Index('ix_model_artifacts_advisory_status', Column('advisory_status', VARCHAR(length=64), table=<model_artifacts>))), ('remove_index', Index('ix_model_artifacts_artifact_hash', Column('artifact_hash', VARCHAR(length=128), table=<model_artifacts>))), ('remove_index', Index('ix_model_artifacts_experiment_id', Column('experiment_id', VARCHAR(length=96), table=<model_artifacts>)))]
PASS: A11.4 drift: band token 'v2_' absent
PASS: A11.4 drift: band token 'live_exec' absent
PASS: A11.4 drift: band token 'lxmod' absent
PASS: A11.4 drift: band token 'modify_event' absent
PASS: A11.4 drift: band token 'activation_instrument' absent
PASS: A11.4 drift: band token 'kill_switch' absent
PASS: A11.5 drift: every detected operation names an inherited V1 token (9-item whitelist)
  drift operations witnessed (itemized): 8
PASS: A11.6 environment close: still no TD/PRACTICE variables

==============================================================================
A12. FINAL APPLY VERDICT
==============================================================================
post-apply size 2670592 sha256 DC0FAA2429AF6510C4E77B4DE056661842D71C0D9AF9948A933F7584DF651CCC

APPLY VERDICT: PASS - migration 20260909_0056_v2_be12d_activation_killswitch applied ONCE to 'C:\Users\victo\.vscode\AXIOM\axiom\backend\axiom_dev.db'.
Terminal state: revision 20260909_0056; tattoo 90/83/16; activation + kill_switch present with guard pairs and closed CHECKs, BOTH ZERO ROWS (before/after every probe); six 12D permission rows content-exact; compver ALL THREE rows standing (1.0.0/1.1.0 untouched; 1.2.0 == diskd25c4857...); twelve guard/CHECK refusals exact under RENDERED names; 12A ledger untouched; disk hashes 6/8/13-file re-proven; integrity ok; drift itemized; no TD/PRACTICE variable; no governor verb ran anywhere.
Transcript: C:\Users\victo\.vscode\AXIOM\axiom\operator-evidence\BE-12D\0056-APPLY-RUN-V1-20260909155857.txt
State record: C:\Users\victo\.vscode\AXIOM\axiom\operator-evidence\BE-12D\0056-APPLY-FINAL-STATE.txt
NEXT: restart the application when ready. Send transcript + state record to ITRGA. The FIELDED verdict and register line are issued on receipt.
PS C:\Users\victo\.vscode\AXIOM\axiom> 