# ITRGA VERDICT — W6-U01 FINAL (supersedes CONDITIONAL)

## Execution Research Safety Foundation — Gate-Closed Simulation Envelope

**From:** AXIOM Independent Technical Review & Governance Authority (ITRGA)
**To:** Development Authority (DA), via Operator
**Unit:** W6-U01 (Wave 6, first unit)
**Supersedes:** `ITRGA_REVIEW_W6-U01.md` (CONDITIONAL APPROVAL, 2026-07-17)
**Correction pack reviewed:** `DELIVERY_REPORT_W6-U01_CORRECTION.md` + `operator results.md` (correction turn)
**Build Order:** `BUILD_ORDER_W6-U01.md` + `BUILD_ORDER_W6-U01_AMENDMENT_1.md`
**Date:** 2026-07-17
**Verdict:** ✅ **APPROVED** — both conditions CLOSED at Level-I. **Platform bumped v0.46.0 → v0.47.0.**
**Confidence:** HIGH. **Governance Gate:** CLOSED (re-verified). **Motto:** *We don't guess. We prove.*

---

## 0. Build-identity check

- `DELIVERY_REPORT_W6-U01_CORRECTION.md` — Unit W6-U01, cites `ITRGA_REVIEW_W6-U01.md` + Amendment 1, verdict CONDITIONAL, C-1/C-2 named. ✔
- `operator results.md` (correction turn) — opens with `Test-Path ITRGA_REVIEW_W6-U01.md`, `DELIVERY_REPORT_W6-U01_CORRECTION.md`, `W6-U01_C1_C2_CORRECTION_COMMANDS.md` (all correction-turn artifacts). **Fresh pack, genuinely OF the W6-U01 correction.** ✔

---

## 1. C-1 — CLOSED ✅ (live-DB refusal-audit proof)

The operator ran the **exact Amendment-1 §3 query** on the target PostgreSQL:
```
psql ... -c "SELECT details->>'reason_code' AS reason_code, COUNT(*) AS refusal_count
             FROM audit_events
             WHERE details->>'reason_code' IN ('GATE_CLOSED_CONNECT_REFUSED','GATE_CLOSED_EXECUTE_REFUSED')
             GROUP BY details->>'reason_code' ORDER BY reason_code;"
```
Output:
```
         reason_code         | refusal_count
-----------------------------+---------------
 GATE_CLOSED_CONNECT_REFUSED |             1
 GATE_CLOSED_EXECUTE_REFUSED |             1
```
Both codes present, `refusal_count ≥ 1`, from the immutable `audit_events` table. This is the named raw SELECT the CONDITIONAL required — a source-grep of a constant no longer stands in for it.

**Bonus — the audit contract (Amendment 1 §4) is independently proven** via the detail-row query:
```
 action                 | resource_type      | reason_code                 | gate_state | simulation_only | live_broker_connection_attempted | live_order_attempted
 broker.execute.refused | broker_integration | GATE_CLOSED_EXECUTE_REFUSED | CLOSED     | true            | false                            | false
 broker.connect.refused | broker_integration | GATE_CLOSED_CONNECT_REFUSED | CLOSED     | true            | false                            | false
```
Stable `action`/`resource_type` corpus discriminators ✔; `gate_state=CLOSED` ✔; `simulation_only=true` ✔; `live_broker_connection_attempted=false` and `live_order_attempted=false` ✔. **The audit row itself proves no live attempt occurred.**

---

## 2. C-2 — CLOSED ✅ (dependency-delta disposition + report correction)

Operator-run evidence confirms the CONDITIONAL's hypothesis (pre-existing libs reconciled), at Level-I:

- **`python-jose` / `passlib` / `bcrypt`** appear under **`# Auth (W0-U04)`** in `backend/requirements.txt` — **pre-existing** authentication dependencies from Wave 0; the `pyproject.toml` entries are packaging-parity reconciliation, not W6-introduced capability.
- `Select-String` over `execution_research/*.py` + `null_broker.py` for `jose|passlib|bcrypt` → **no output** — W6-U01 code does not import/use them.
- `execution_research/` imports **only** `pydantic` + local constants; grep for `requests|httpx|socket|websocket|ccxt|MetaTrader|openai|anthropic|broker|credential|api_key|secret|token|password` → **no output**.
- `vite` / `vitest` / `@vitejs/plugin-react` are frontend **build/test tooling** (dev/build/test scripts); frontend source imports no broker/exchange/LLM SDK.
- **GR6-12 hard bar intact:** no broker/exchange SDK, no LLM/tokenizer, no new runtime capability.
- **Report wording corrected** (`DELIVERY_REPORT_W6-U01_CORRECTION.md` §3.2): the over-broad "No dependency added" is replaced with the accurate "no *barred* and no *W6-U01-introduced* dependency," with the cumulative-baseline deltas explained. Accuracy defect resolved.

---

## 3. Standing safety envelope — re-confirmed green in the correction run

- `pytest tests/test_execution_research_safety.py tests/test_broker_integration.py -q` → **`13 passed`** (6 safety + 7 broker); the six named W6 tests confirmed by name in the verbose warnings summary.
- `ruff check .` → **All checks passed!**
- Frontend: **17 files / 53 tests passed**, `npm audit` **0 vulnerabilities**, build OK.
- (From the original pack, unchanged: full backend **297 passed**; §16 containment holds; bright-line grep on `execution_research/` empty; no migration `head 20260717_0027`; no new table; no UI; Git-Bash CI `LOCAL_CI_EXIT_CODE: 0`; Gate CLOSED.)

---

## 4. Verdict

**W6-U01 is APPROVED.** The Wave-6 execution-research safety foundation is proven: the Governance Gate is CLOSED, the Null/Simulated broker **refuses connect and execute** with an **audited, live-DB-verified** refusal trail (no-live-attempt flags false), broker logic is contained to External Integration (§16), the new `execution_research` context is inert (pydantic-only, no network/broker/credential/LLM), and no table/UI/migration/barred-dependency was introduced. **The lock is proven before the door.**

- **Platform of record: v0.46.0 → v0.47.0.**
- **Alembic head: `20260717_0027` (unchanged).**
- **Baselines: backend 297 passed · frontend 17 files / 53 tests.**
- No residuals carried. (Standing project-wide: any future compiled/LLM/broker dep owes its own spike; LLM stays future hard-gated.)

**Next:** on operator authorization, `BUILD_ORDER_W6-U02.md` — *Simulated Execution Runs & Fill Events* (`simulated_execution_runs`, `simulated_fill_events`), the first W6 persisted artifacts — with R6-2 (operator_id research-FK + no-orphan join against users), R6-3 (no-real-P&L text contract), R6-4 (Gate-closed proof line), R6-6 (immutable fill/policy versions), and full persistence-capture (raw SELECT + no-orphan audit JOIN) required on first submission.

---

## 5. Posture note

The DA closed both conditions cleanly, with operator-run evidence on target — including going beyond C-1 to supply the full audit-contract detail row. This is the standard: built correctly **and proven** correctly.

---

*We don't guess. We prove.*
**— AXIOM ITRGA**
