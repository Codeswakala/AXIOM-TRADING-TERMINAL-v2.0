# BUILD ORDER — W7-U05

## Plugin Contract Safety Foundation

**From:** AXIOM Independent Technical Review & Governance Authority (ITRGA)
**To:** Development Authority (DA), via Operator
**Wave:** 7 — Institutional Platform · **Unit:** W7-U05 · **Policy:** one unit per Build Order
**Date:** 2026-07-18
**Platform of record (pre-unit):** v0.58.0 · Alembic head `20260717_0037` · backend **383 passed** · frontend **20 files / 64 tests**
**Governing docs:** accepted `WAVE7_ENGINEERING_DESIGN_AND_IMPLEMENTATION_PLAN.md` §2 (Plugin architecture) + §4.2 + §5.5; `ITRGA_REVIEW_WAVE7_DESIGN_PLAN.md` (**R7-1**, R7-3, R7-6/GR7-6, GR7-8/GR7-9); `05_SYSTEM_ARCHITECTURE.md` §16 (broker containment) + §17 (Plugin Architecture — plugins interact ONLY through published extension contracts, core independent of plugin impls); `10_CONSTITUTIONAL_HIERARCHY.md`.
**Constitutional posture:** Governance Gate **CLOSED**. **Published extension contracts + refusal ONLY — NO dynamic/third-party plugin code execution this wave.** Plugins are the classic execution/exfiltration backdoor; this unit proves the lock, builds no door.
**Motto:** *We don't guess. We prove.*

---

## 1. Purpose

Establish the **plugin contract layer** for the institutional platform as a **safety foundation** — published, allowlisted extension **contracts** (report exporters, chart types, analytics view descriptors) and **built-in reference plugins only**, with **NO dynamic or third-party code execution** (R7-1). The unit's central proof is a **hostile-plugin refusal** (a plugin/contract that tries to import broker/order/account modules, open a venue socket, read secrets/other operators' data, mutate governed artifacts outside contracts, or reach the Gate is **refused and audited**) plus **§16/§17 containment** (core independent of plugins; no broker logic outside External Integration; plugins only via published contracts).

**HARD LINE (R7-1):** any dynamic/third-party plugin **code execution** — and any `plugin_execution_audit_events` table — is a **SEPARATE, hard-gated Build Order** (Operator + ITRGA + sandbox threat-model + runtime spike), never inside this or any feature unit. This unit executes nothing external.

---

## 2. Scope (build exactly this)

1. **Plugin contract layer** under `backend/app/institutional_platform/plugins/`:
   - explicit published **extension contract interfaces** (typed);
   - an **allowlist of capabilities** (read/research descriptors only — e.g. `report.export`, `chart.type`, `analytics.view`);
   - **built-in reference plugin(s)** implementing a contract (no dynamic loading, no third-party code, no `importlib`/`eval`/`exec`/entry-point dynamic dispatch);
   - a **refusal seam** that rejects any contract/plugin request outside the allowlist or that touches a forbidden capability, and **audits** the refusal.
2. **Optional plugin-contract-registry table** `plugin_contracts` (and/or `plugin_contract_capabilities`) → migration `20260717_0038` **only if the DA persists the contract registry**; if the registry is code-defined constants (preferred for a safety foundation), **no table** and head stays `20260717_0037`. **NO `plugin_execution_audit_events` table (R7-1).**
3. **Read-only API** to list published contracts/capabilities (authenticated, operator-scoped as applicable). No endpoint that executes a plugin.
4. Frontend plugin-contract **catalogue** surface **only if** the DA proposes one (browser evidence then applies); otherwise API-only (state so).

### FORBIDDEN (must be ABSENT — prove)
- **No dynamic code execution:** grep the plugin package for `eval|exec(|importlib|__import__|load_entry_point|pkg_resources|subprocess|compile(` → none (or only in disclosed refusal-test negative fixtures).
- **No broker/order/account/live/Gate reach from plugins (§16/§17):** grep `place_order|broker\.(connect|execute)|order_routing|account_balance|open_gate|gate_open|allow_execution|socket|requests\.|httpx\.` in the plugin package → none.
- **No `plugin_execution_audit_events` table** (R7-1). If any registry table persisted, forbidden columns (order/account/pnl/gate/secret/token) `information_schema` → 0 rows.

---

## 3. Binding refinements applied

- **R7-1 (ABSOLUTE) — contracts + refusal only, no dynamic/third-party execution.** Prove by construction + grep (no `eval/exec/importlib/entry-point/subprocess`); built-in reference plugins only; no execution-audit table.
- **R7-6 / GR7-6 (CENTRAL) — hostile-plugin refusal + least privilege.** A test must construct a hostile plugin/contract request (imports broker/order/account, opens a socket, reads secrets, mutates a governed artifact outside contract, or reaches the Gate) and prove it is **refused and audited** — analogous to the Wave-5 assistant anti-injection/refusal proofs. Deliver the refusal + its audit row.
- **§16/§17 containment:** broker logic only in External Integration; core independent of plugin implementations; plugins interact only through published contracts. Structural grep.
- **R7-3 operator scoping / GR7-8 no-secret:** any operator-scoped contract data is isolated (valid-token two-op spot-check if applicable); plugin/contract surfaces leak no secrets/PII; a plugin cannot read another operator's data or secrets.
- **Authorize-before-validate** on any mutation endpoint (carried).
- **GR7-9 persistence-capture** IF a registry table is persisted (raw SELECT + no-orphan audit JOIN → 0 + operator JOIN if scoped + forbidden-column `information_schema` → 0 rows).
- **GR7-1 Gate CLOSED** — no plugin/contract/role can open or reach the Gate; `test_gate_remains_closed_for_wave7` + broker suite green.

---

## 4. Mandatory tests (deliver names + raw PASS lines)

```
test_plugin_contract_layer_has_no_dynamic_or_thirdparty_code_execution     # R7-1 grep/construction
test_plugin_contract_disallows_broker_order_account_gate_imports            # §16/§17 containment
test_hostile_plugin_request_refused_and_audited                            # R7-6 CENTRAL
test_plugin_capabilities_are_allowlisted_read_research_only
test_no_plugin_execution_audit_events_table                                # R7-1 (table absent)
test_plugin_contract_surface_requires_auth
test_plugin_contract_has_no_secret_or_pii_markers
test_gate_remains_closed_for_wave7
```
(+ persistence-capture/forbidden-column/operator-scoping tests IF a registry table is persisted.)
Plus standing `test_broker_integration.py` green. Full backend regression ≥ **383** + new; frontend baseline ≥ **20 files** (report actual; +tests only if a UI surface is added).

---

## 5. Mandatory evidence (operator-run on target — Level-I)

Deliver `DELIVERY_REPORT_W7-U05.md` + `operator results.md` (+ screenshots IF a UI surface is added), **inline**:

**(a) Build identity.** `Test-Path` new plugin-package files + proof the pack is OF **W7-U05**; version `0.59.0`.
**(b) Test transcript.** Named tests + broker suite + full backend total (+ frontend if UI).
**(c) Migration state.** If no registry table: `alembic current` = `20260717_0037` unchanged. If persisted: `alembic current` = `20260717_0038 (head)` + revision file. **Confirm no `plugin_execution_audit_events` table exists** (`information_schema.tables` → absent).
**(d) R7-1 NO-DYNAMIC-EXECUTION grep (raw).** grep the plugin package for `eval|exec(|importlib|__import__|load_entry_point|pkg_resources|subprocess|compile(` → empty (or only disclosed refusal-test negative fixtures).
**(e) §16/§17 CONTAINMENT grep (raw).** plugin package for `place_order|broker\.(connect|execute)|order_routing|account_balance|open_gate|gate_open|allow_execution|socket|requests\.|httpx\.` → empty; broker logic still only in External Integration.
**(f) HOSTILE-PLUGIN REFUSAL (R7-6, raw).** Show a hostile plugin/contract request is refused (test PASS) **and** its **audit row** (raw `psql` on `audit_events` — a `*_REFUSED`/plugin-refusal reason code, `COUNT ≥ 1`), analogous to Wave-5 assistant refusal proofs.
**(g) ALLOWLIST proof.** the published capability allowlist printed — read/research descriptors only, no execute/order/account/gate capability.
**(h) AUTH (GR7-5).** contract-list endpoint UNAUTH → 401, AUTH → 200.
**(i) No-secret/PII (GR7-8).** marker check over contract surface → clean.
**(j) Persistence-capture (IF registry table).** raw SELECT ≥1 row + no-orphan audit JOIN → 0 (+ operator JOIN if scoped) + forbidden-column `information_schema` → 0 rows.
**(k) No barred dependency.** grep empty (no plugin-runtime/loader lib — if any proposed, it is barred/needs spike per GR7-12); state dep changes accurately.
**(l) CI (GR7-11).** Git-Bash → `LOCAL_CI_EXIT_CODE: 0`.
**(m) Gate-closed proof.** named test PASS + broker suite green.
**(n) Browser (only if UI added, GR7-10).** served shots: contract catalogue, no actuation controls, logged-out block.

---

## 6. Acceptance criteria

APPROVED requires ALL applicable of (a)–(n); named tests + broker suite green; regression green; **no-dynamic-execution grep empty**; **§16/§17 containment clean**; **hostile-plugin request refused + audited (raw audit row)**; allowlist read/research-only; **no `plugin_execution_audit_events` table**; auth on contract surface; no secret/PII; persistence-capture if any table; CI exit 0; Gate CLOSED.

- A single CRITICAL (any dynamic/third-party plugin code execution; any plugin path to broker/order/account/live/Gate; a hostile plugin NOT refused; a `plugin_execution_audit_events` table; any secret/PII leak; any Gate reach) ⇒ **WITHHELD.**
- A refusal proven only by test without its named raw audit row, or a null-token scoping probe ⇒ **CONDITIONAL** (W6-U04 / W7-U02 C-1 lessons).
- A red gate is a finding, never relabeled green.

On approval: platform bump to **v0.59.0**; head `20260717_0037` (or `20260717_0038` if a registry table is persisted); onboarding updated; W7-U06 (Portfolio Research Dashboard / Advanced Reporting) becomes next authorizable.

---

## 7. Reminders to DA

- **R7-1 is absolute: contracts + refusal only, execute NOTHING external this wave.** No `eval/exec/importlib/entry-point/subprocess`; no `plugin_execution_audit_events` table. Dynamic execution is a future separate hard-gated Build Order.
- **The hostile-plugin refusal is the central proof** — construct a malicious plugin/contract request and show it is refused AND audited (raw audit row), like the Wave-5 assistant anti-injection proofs.
- Prefer code-defined contract constants over a persisted registry for a safety foundation; if you persist a registry, deliver persistence-capture. State whether a table/UI is added.
- Verify the pack is OF W7-U05; verify any probe tokens (LOGIN 200 + non-empty) before trusting status codes.

---

*We don't guess. We prove.*
**— AXIOM ITRGA**
