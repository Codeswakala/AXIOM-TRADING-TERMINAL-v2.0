import hashlib
import re
import sqlite3
import sys

MID_DOT = chr(183)

MGE_FILES = (
    "app/v2/research_governance/__init__.py",
    "app/v2/research_governance/contracts.py",
    "app/v2/research_governance/decisions.py",
)
SGE_FILES = (
    "app/v2/research_governance/signals.py",
    "app/v2/research_governance/api.py",
)
BE6_FILES = (
    "app/v2/portfolio_research/__init__.py",
    "app/v2/portfolio_research/contracts.py",
    "app/v2/portfolio_research/metrics.py",
    "app/v2/portfolio_research/scenarios.py",
)


def ro_connect(db_path):
    uri = "file:" + db_path.replace("\\", "/") + "?mode=ro"
    return sqlite3.connect(uri, uri=True)


def rw_connect(db_path):
    return sqlite3.connect(db_path)


def engine_hash(backend_dir, rel_files):
    # The pinned compver provenance algorithm, recomputed from the
    # on-disk source files: sha256 over (relpath\0 + bytes + \0) per
    # file, in the pinned order.
    import os
    digest = hashlib.sha256()
    for rel in rel_files:
        path = os.path.join(backend_dir, rel.replace("/", os.sep))
        with open(path, "rb") as handle:
            data = handle.read()
        digest.update(rel.encode("utf-8"))
        digest.update(b"\x00")
        digest.update(data)
        digest.update(b"\x00")
    return digest.hexdigest()


def main():
    cmd = sys.argv[1]
    db_path = sys.argv[2]

    if cmd == "selftest":
        con = ro_connect(db_path)
        try:
            value = con.execute("SELECT 1 AS helper_self_test").fetchone()[0]
            print(value)
        finally:
            con.close()
        return

    if cmd in ("scalar", "verifyrows", "verifyaudit", "compverbe5",
               "permbe5", "reportempty5", "compverbe6", "permbe6",
               "reportempty2", "tabledigest"):
        con = ro_connect(db_path)
        try:
            if cmd == "scalar":
                sql = sys.argv[3]
                rows = con.execute(sql).fetchall()
                for row in rows:
                    print("|".join("" if v is None else str(v) for v in row))
            elif cmd == "verifyrows":
                rows = con.execute(
                    "SELECT from_status, to_status, authority_ref, evidence_ref, operator_id "
                    "FROM v2_md_provider_status_history ORDER BY id"
                ).fetchall()
                if len(rows) != 2:
                    print("FAIL:history_count=" + str(len(rows)))
                    return
                tuples = [tuple(r) for r in rows]
                exp_genesis = (
                    None,
                    "architecture_candidate",
                    "BO-V2-BE-3-P1-001",
                    "AXIOM-V2-BE-3-DA-PLAN-001 v3.0.0 / ITRGA-DET-V2-BE-3-PLAN-001",
                    None,
                )
                exp_transition = (
                    "architecture_candidate",
                    "contract_tested",
                    "BO-V2-BE-3-P2-TRANS-001",
                    "ITRGA-DET-V2-BE-3-P2-FINAL-001 " + MID_DOT
                    + " run a246607c-f0c5-42e9-8f3b-a1e1bd75fa83",
                    None,
                )
                if exp_genesis not in tuples or exp_transition not in tuples:
                    print("FAIL:rows=" + repr(tuples))
                    return
                print("PASS:history_rows_exact")
            elif cmd == "verifyaudit":
                rows = con.execute(
                    "SELECT action, actor_id, actor_type, domain, mode, classification, details "
                    "FROM v2_audit_event "
                    "WHERE action LIKE 'provider.status_transition%' "
                    "ORDER BY created_at"
                ).fetchall()
                if len(rows) != 2:
                    print("FAIL:audit_count=" + str(len(rows)))
                    return
                exp_start = (
                    "provider.status_transition.start",
                    "migration",
                    "operator",
                    "v2.marketdata",
                    "RESEARCH",
                    "internal",
                    '{"provider_id": "twelvedata", "from": "architecture_candidate", '
                    '"to": "contract_tested", "authority_ref": "BO-V2-BE-3-P2-TRANS-001", '
                    '"evidence_ref": "ITRGA-DET-V2-BE-3-P2-FINAL-001 ' + MID_DOT
                    + ' run a246607c-f0c5-42e9-8f3b-a1e1bd75fa83"}',
                )
                exp_complete = (
                    "provider.status_transition.complete",
                    "migration",
                    "operator",
                    "v2.marketdata",
                    "RESEARCH",
                    "internal",
                    '{"history_count": 2, "post_status": "contract_tested", '
                    '"persistence_permitted": false}',
                )
                if tuple(rows[0]) != exp_start:
                    print("FAIL:audit_start=" + repr(rows[0]))
                    return
                if tuple(rows[1]) != exp_complete:
                    print("FAIL:audit_complete=" + repr(rows[1]))
                    return
                print("PASS:audit_rows_exact")
            elif cmd == "compverbe5":
                # Exactly 5 rows: the 3 BE-4 components pinned by
                # value; the 2 BE-5 components pinned by RUNTIME
                # RECOMPUTATION of the engine file hashes.
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
                rows = con.execute(
                    "SELECT component, version, source_hash, evidence_ref, registered_at "
                    "FROM v2_computation_version"
                ).fetchall()
                if len(rows) != 5:
                    print("FAIL:compver_count=" + str(len(rows)))
                    return
                seen = {}
                for component, version, source_hash, evidence_ref, registered_at in rows:
                    if component in seen:
                        print("FAIL:compver_duplicate_component=" + str(component))
                        return
                    seen[component] = (version, source_hash,
                                       evidence_ref, registered_at)
                for component, (exp_version, exp_hash) in list(pins_be4.items()) + list(exp_be5.items()):
                    if component not in seen:
                        print("FAIL:compver_missing=" + component)
                        return
                    version, source_hash, evidence_ref, registered_at = seen[component]
                    if version != exp_version:
                        print("FAIL:compver_version=" + component + "=" + repr(version))
                        return
                    if source_hash != exp_hash:
                        print("FAIL:compver_hash=" + component + "=" + repr(source_hash)
                              + " expected=" + repr(exp_hash))
                        return
                    if not re.fullmatch(r"[0-9a-f]{64}", source_hash or ""):
                        print("FAIL:compver_hash_shape=" + component)
                        return
                    exp_ref = "BO-V2-BE-4-001" if component in pins_be4 else "BO-V2-BE-5-001"
                    if evidence_ref != exp_ref:
                        print("FAIL:compver_evidence_ref=" + component + "=" + repr(evidence_ref))
                        return
                    if not registered_at or len(str(registered_at)) < 19:
                        print("FAIL:compver_registered_at_shape=" + component)
                        return
                print("PASS:compver_rows_exact")
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
                print("INFO:pre_recomputed=" + be6_recomputed)
            elif cmd == "permbe5":
                rows = con.execute(
                    "SELECT role, permission, sal FROM v2_permission "
                    "WHERE permission LIKE 'v2.research.ml%' "
                    "OR permission LIKE 'v2.research.signal%'"
                ).fetchall()
                if len(rows) != 8:
                    print("FAIL:permbe5_count=" + str(len(rows)))
                    return
                expected = {
                    ("admin", "v2.research.ml_governance.read", "SAL-2"),
                    ("admin", "v2.research.ml_governance.decide", "SAL-3"),
                    ("admin", "v2.research.signal.read", "SAL-2"),
                    ("admin", "v2.research.signal.emit", "SAL-3"),
                    ("admin", "v2.research.ml_diagnostics.read", "SAL-2"),
                    ("operator", "v2.research.ml_governance.read", "SAL-2"),
                    ("operator", "v2.research.signal.read", "SAL-2"),
                    ("operator", "v2.research.ml_diagnostics.read", "SAL-2"),
                }
                if set(tuple(r) for r in rows) != expected:
                    print("FAIL:permbe5_rows=" + repr(sorted(tuple(r) for r in rows)))
                    return
                total = con.execute("SELECT COUNT(*) FROM v2_permission").fetchone()[0]
                dupes = con.execute(
                    "SELECT COUNT(*) - COUNT(DISTINCT role || '|' || permission) "
                    "FROM v2_permission"
                ).fetchone()[0]
                if dupes != 0:
                    print("FAIL:perm_duplicate_role_permission")
                    return
                print("PASS:perm_rows_exact")
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
                print("INFO:v2_permission_total=" + str(total))
            elif cmd == "reportempty5":
                counts = {}
                for table in ("v2_ml_governance_record", "v2_ml_lifecycle_event",
                              "v2_ml_diagnostic_report", "v2_signal_record",
                              "v2_signal_state_event"):
                    counts[table] = con.execute(
                        "SELECT COUNT(*) FROM " + table).fetchone()[0]
                if any(v != 0 for v in counts.values()):
                    print("FAIL:table_counts=" + repr(counts))
                    return
                print("PASS:be5_tables_empty")
            elif cmd == "reportempty2":
                counts = {}
                for table in ("v2_portfolio_definition", "v2_portfolio_risk_report"):
                    counts[table] = con.execute(
                        "SELECT COUNT(*) FROM " + table).fetchone()[0]
                if any(v != 0 for v in counts.values()):
                    print("FAIL:table_counts=" + repr(counts))
                    return
                print("PASS:be6_tables_empty")
            elif cmd == "tabledigest":
                table = sys.argv[3]
                rows = con.execute("SELECT * FROM " + table + " ORDER BY id").fetchall()
                digest = hashlib.sha256(
                    repr([tuple(r) for r in rows]).encode("utf-8")).hexdigest()
                print("DIGEST:" + str(len(rows)) + ":" + digest)
        finally:
            con.close()
        return

    if cmd == "tryrefuse":
        sql = sys.argv[3]
        con = rw_connect(db_path)
        try:
            try:
                con.execute(sql)
                con.rollback()
                print("SUCCESS_UNEXPECTED")
            except sqlite3.Error as exc:
                con.rollback()
                print("REFUSED:" + str(exc))
        finally:
            con.close()
        return

    if cmd == "guardprobe":
        insert_sql = sys.argv[3]
        probe_sql = sys.argv[4]
        con = rw_connect(db_path)
        try:
            con.execute(insert_sql)
            try:
                con.execute(probe_sql)
                outcome = "SUCCESS_UNEXPECTED"
            except sqlite3.Error as exc:
                outcome = "REFUSED:" + str(exc)
            con.rollback()
            print(outcome)
        finally:
            con.close()
        return

    if cmd == "uniqbe6":
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
    sys.exit(2)


main()