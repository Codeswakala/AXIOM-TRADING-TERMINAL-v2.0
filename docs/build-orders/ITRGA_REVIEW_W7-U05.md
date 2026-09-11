# ITRGA REVIEW — W7-U05

## Plugin Contract Safety Foundation

**From:** AXIOM Independent Technical Review & Governance Authority (ITRGA)
**To:** Development Authority (DA), via Operator
**Unit:** W7-U05 (Wave 7) · **Reviewed pack:** `DELIVERY_REPORT_W7-U05.md` + `operator results.md`
**Build Order:** `BUILD_ORDER_W7-U05.md`
**Review date:** 2026-07-18
**Platform of record (pre-unit):** v0.58.0 · head `20260717_0037` · backend 383 / frontend 20f·64t
**Verdict:** ✅ **APPROVED (CLEAN)** — all hard plugin-safety controls proven at Level-I. **Platform v0.58.0 → v0.59.0.**
**Confidence:** HIGH. **Governance Gate:** CLOSED. **Motto:** *We don't guess. We prove.*

---

## 0. Build-identity check (done FIRST)

- `DELIVERY_REPORT_W7-U05.md`: Unit W7-U05, cites Build Order + W7-U04 FINAL; target v0.59.0, head `20260717_0037` **unchanged** (code-constants registry — no table, the preferred safety-foundation path). ✔
- `operator results.md`: fresh pack (ADR-068, `plugins/contracts.py`/`registry.py`/`service.py`, `test_plugin_contracts.py`, refusal seed script). ✔

---

## 1. What is PROVEN (Level-I)

| # | Requirement | Evidence | Result |
|---|---|---|---|
| b | Named tests | `test_plugin_contracts.py` **8/8 PASSED** (all §4 tests) | ✅ |
| — | Full backend regression | **391 passed** (+8 over 383); broker suite green | ✅ |
| c | Migration state | `alembic current = 20260717_0037` unchanged | ✅ |
| — | **No registry/execution table** | `information_schema.tables` for `plugin_contracts`, `plugin_contract_capabilities`, `plugin_execution_audit_events` → **(0 rows)**; `PLUGIN_EXECUTION_AUDIT_TABLE_PRESENT: False` | ✅ |
| d | **R7-1 no dynamic execution** | grep plugin package for `eval\|exec(\|importlib\|__import__\|load_entry_point\|pkg_resources\|subprocess\|compile(` → **"no output"** | ✅ |
| e | **§16/§17 containment** | grep `place_order\|broker.(connect\|execute)\|order_routing\|account_balance\|open_gate\|gate_open\|allow_execution\|socket\|requests.\|httpx.` → **"no output"** | ✅ |
| f | **Hostile-plugin refusal + RAW AUDIT ROW (R7-6 CENTRAL)** | refusal `reason_code=PLUGIN_CONTRACT_IMPORT_REFUSED`; raw `audit_events` row: `plugin_contract_request.refused \| plugin_contract_request \| builtin.report_export.markdown.v1 \| PLUGIN_CONTRACT_IMPORT_REFUSED \| accepted=false \| corr c5160298…`; `plugin_refusal_audit_count = 1` | ✅ |
| g | Allowlist read/research-only | `CAPABILITY_ALLOWLIST: report.export, chart.type, analytics.view`; `FORBIDDEN_CAPABILITY_MATCH_COUNT: 0` (no execute/order/broker/account/gate/position/capital/margin) | ✅ |
| h | Auth (GR7-5) | plugin-contracts endpoint UNAUTH → **401**, AUTH → **200**; `GOVERNANCE_GATE_CAPABILITY_PRESENT: False` | ✅ |
| i | No secrets/PII | marker check over contract surface → clean | ✅ |
| k | No barred dependency | "no dependency added"; no plugin-runtime/loader lib | ✅ |
| — | No UI | API-only (declared); no browser evidence required | ✅ |
| l | CI (GR7-11) | `LOCAL_CI_EXIT_CODE: 0` | ✅ |
| m | Gate CLOSED | `test_gate_remains_closed_for_wave7` PASS; broker suite green | ✅ |

**The plugin lock is proven and no door was built:** nothing executes dynamically, plugins cannot reach broker/order/account/live/Gate seams, a hostile plugin/contract request is refused **and audited** (raw row, `accepted=false`), capabilities are an allowlisted read/research vocabulary, and there is no execution-audit table.

---

## 2. Refinements — all satisfied

- **R7-1 (absolute):** contracts + refusal only; no `eval/exec/importlib/entry-point/subprocess` (grep empty); **no `plugin_execution_audit_events` table** (information_schema (0 rows)); code-constants registry (no table). ✅
- **R7-6 / GR7-6:** hostile-plugin refused + audited (raw audit row) — the Wave-5 anti-injection rigor applied to plugins. ✅
- **§16/§17:** containment grep clean; core independent of plugin implementations. ✅
- **GR7-5 / GR7-8:** auth 401/200; no secret/PII; Gate capability absent. ✅

---

## 3. Verdict

**W7-U05 is APPROVED (CLEAN).** The Plugin Contract Safety Foundation is proven: published, allowlisted, read/research-only extension contracts with built-in reference plugins, **no dynamic or third-party code execution**, **no execution-audit table**, provable §16/§17 containment, an **audited hostile-plugin refusal**, authenticated contract surface, and the Gate CLOSED. Plugins cannot become an execution or exfiltration backdoor.

- **Platform of record: v0.58.0 → v0.59.0.**
- **Alembic head: `20260717_0037` (unchanged — code-constants registry).**
- **Baselines: backend 391 passed · frontend 20 files / 64 tests.**
- **Standing (unchanged):** any dynamic/third-party plugin **execution** remains a FUTURE separate hard-gated Build Order (R7-1); TD-W6-CI-AUDIT; abuse/rate-guard candidate for W7-U07.

**Next:** on operator authorization, `BUILD_ORDER_W7-U06.md` — *Portfolio Research Dashboard / Advanced Reporting*: research aggregation over advisory/simulated artifacts + report/export, **no real account/position/balance/P&L** (forbidden-column proof), uncertainty + disclaimers (GR7-4 stat≠economic), operator scoping (valid-token harness), persistence-capture if any report table, browser evidence (first W7-U06 UI likely).

---

## 4. Posture note

The most constitutionally sensitive W7 unit, cleanly proven: nothing runs, containment holds, and a hostile plugin is refused and audited exactly as the assistant anti-injection proofs were in Wave 5. The DA used the now-standard self-throwing/valid-token harness throughout and delivered the raw audit row for the refusal without being asked twice. Built correctly and proven correctly.

---

*We don't guess. We prove.*
**— AXIOM ITRGA**
