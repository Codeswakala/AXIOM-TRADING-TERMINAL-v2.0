# ITRGA REVIEW — W6-U01

## Execution Research Safety Foundation — Gate-Closed Simulation Envelope

**From:** AXIOM Independent Technical Review & Governance Authority (ITRGA)
**To:** Development Authority (DA), via Operator
**Unit:** W6-U01 (Wave 6, first unit) · **Reviewed pack:** `DELIVERY_REPORT_W6-U01.md` + `operator results.md`
**Build Order:** `BUILD_ORDER_W6-U01.md` + `BUILD_ORDER_W6-U01_AMENDMENT_1.md`
**Review date:** 2026-07-17
**Platform of record (pre-unit):** v0.46.0 · Alembic head `20260717_0027` · backend 291 / frontend 17f·53t
**Verdict:** 🟡 **CONDITIONAL APPROVAL** — core safety envelope PROVEN; two *named* evidence items open (C-1, C-2). **Version bump to v0.47.0 HELD** until closure.
**Confidence:** HIGH on what was proven; the two conditions are evidence/disposition gaps, not suspected safety failures.
**Governance Gate:** CLOSED (verified). **Motto:** *We don't guess. We prove.*

---

## 0. Build-identity check (done FIRST — recurring stale-pack risk)

- `DELIVERY_REPORT_W6-U01.md` header: Unit `W6-U01`, Wave 6, cites the Build Order **and** Amendment 1, head `20260717_0027`. ✔ Correct unit.
- `operator results.md` **opens with a Wave-5 preamble** (`Test-Path ... ITRGA_VERDICT_W5-U07_FINAL.md`, `W5-U08_...`, the assistant-refusal `details->>'refusal_reason'` query at line 124, W5 CI at line 1412). This is a benign scroll-back artifact, **not** a stale pack: the substantive W6-U01 evidence is present from ~line 1517 onward (null_broker refusal source, `execution_research/` listing, `297 passed` at line 2215, `W6-U01_LOCAL_CI_TRANSCRIPT.txt` CI at lines 2287–2290). **Confirmed the pack is genuinely OF W6-U01.** I evaluated W6 only against the W6 portion.

---

## 1. What is PROVEN (Level-I, operator-run on target — verified line-by-line)

| # | Requirement | Evidence (operator transcript) | Result |
|---|---|---|---|
| 1 | Full backend regression | `collected 297 items` … `297 passed, 1280 warnings` (line 2215) — **+6 over the 291 baseline** = the six new safety tests | ✅ |
| 2 | Six named safety tests | `tests\test_execution_research_safety.py ......` (6 dots) | ✅ |
| 3 | Standing broker suite green (GR6-4) | `tests\test_broker_integration.py .......` (7) | ✅ |
| 4 | §16 broker containment (GR6-3) | grep for `place_order\|broker_endpoint\|BrokerClient\|mt5\|MetaTrader` outside `external_integration` → **only benign `session.execute()`/`hub.connect()`/`engine.connect()`** (disclosed R7 residual class); broker-specific hits resolve **only** in `external_integration/broker/null_broker.py` + `port.py` | ✅ |
| 5 | Bright-line, `execution_research/` (GR6-2) | grep `place_order\|go_live\|real_account\|account_balance\|margin\|broker\.(connect\|execute)` → **empty** ("Expected: no output above") | ✅ |
| 6 | Refusal is audited **by construction** | `null_broker.py`: `action="broker.connect.refused"` `reason_code=GATE_CLOSED_CONNECT_REFUSED`, and execute/place_order → `broker.execute.refused` `GATE_CLOSED_EXECUTE_REFUSED`, before `GovernanceGateClosedError` | ✅ (source + tests) |
| 7 | No migration (R6-1) | `alembic current` = `20260717_0027 (head)` on PostgresqlImpl; no `w6_u01\|execution_research\|simulation_envelope` migration file | ✅ |
| 8 | No new table (R6-1) | none added; refusal evidence targets existing immutable `audit_events` | ✅ |
| 9 | No UI (Build Order) | `Test-Path ExecutionResearchPage.tsx` → **False**; only benign `<span>W6-U01</span>` shell label; frontend **17f/53t** unchanged | ✅ |
| 10 | No broker SDK / LLM (GR6-12 hard bar) | `Select-String ... MetaTrader\|mt5\|ccxt\|ib_insync\|alpaca\|binance\|openai\|anthropic\|transformers\|langchain\|llama` → **no output** | ✅ |
| 11 | Git-Bash CI (GR6-11) | `& "C:\Program Files\Git\bin\bash.exe" scripts/local_ci.sh` → `==> Local CI equivalent complete` + `LOCAL_CI_EXIT_CODE: 0` → `W6-U01_LOCAL_CI_TRANSCRIPT.txt` (lines 2287–2290) | ✅ |
| 12 | Gate CLOSED (GR6-1/R6-4) | broker connect/execute refuse; `broker_integration_authorized`/`execution_authorized` false; no Gate-mutation code | ✅ |

**The safety envelope — "prove the lock before the door" — is proven.** Every *risk* item is green.

---

## 2. CONDITIONS (named evidence / disposition gaps — must close before FINAL)

### 🟡 C-1 — The Amendment-1 §3 refusal-audit `psql SELECT` was NOT run against the live DB.
Amendment 1 §3 named this mandatory evidence: a raw `psql` against `audit_events`:
```sql
SELECT details->>'reason_code' AS reason_code, COUNT(*) AS refusal_count
FROM audit_events
WHERE details->>'reason_code' IN ('GATE_CLOSED_CONNECT_REFUSED','GATE_CLOSED_EXECUTE_REFUSED')
GROUP BY details->>'reason_code' ORDER BY reason_code;
```
returning **`refusal_count ≥ 1` per code.**

What the transcript actually contains for W6:
- a **`Select-String` over `null_broker.py` source** showing the reason-code *constants* (lines 1573–1585) — this proves the code names the codes, **not** that a refusal row was committed and is queryable; and
- the **W5 preamble** assistant-refusal query (line 124, `resource_type='assistant_response'`, `refusal_reason`) — a different resource, not the W6 broker refusal.

Per the standing persistence-capture / R7 control, **a source-grep of a constant is not a substitute for the named raw SELECT returning committed rows.** This is the single named item that holds a clean approval.
**To close C-1:** run the exact Amendment-1 §3 query on the target PostgreSQL after exercising the connect/execute refusals (the tests already do this — ensure they commit to the reviewed DB, or run the null-broker refusals against it), and submit the raw `psql` command **and** output showing both codes with `refusal_count ≥ 1`.

### 🟡 C-2 — Undeclared dependency delta contradicts the "no dependency additions" claim.
The delivery report §4/§6 assert "no dependency added," and the operator note read "no dependency additions; backend pyproject **version bump only** is acceptable." But the actual `git diff` shows **more than a version bump**:
- `backend/pyproject.toml`: **added** `python-jose[cryptography]>=3.3.0`, `passlib[bcrypt]>=1.7.4`, `bcrypt>=4.0.0,<4.1.0` (plus `version 0.3.0 → 0.47.0`).
- `frontend/package.json`: **major bumps** `@vitejs/plugin-react ^4→^6`, `vite ^5→^8`, `vitest ^2→^4`.

**This is not a CRITICAL:** the GR6-12 *hard* bar (no broker/exchange/LLM SDK) is intact — the barred-list grep returned clean, and these are auth libs (jose/passlib/bcrypt) + build tooling (vite/vitest). Full suite + CI are green with them. **But** it is an undeclared change that (a) contradicts the report's own claim (accuracy — "no room for error"), and (b) vite/vitest **major** bumps are build-tooling changes not declared in the accepted Design Plan's dependency section (GR6-12 spirit re: unspiked tooling changes).
**To close C-2:** the DA must (i) explain WHY these entries changed in a Gate-closed, no-feature safety unit (most likely these libs were already installed/imported and the diff merely reconciles `pyproject.toml`/lockfile to reality — if so, state that and show they are pre-existing, not new capability); (ii) correct the delivery-report claim; and (iii) confirm no NEW runtime capability results. If any is a genuinely new runtime dependency, it must be justified against GR6-12 (and vite/vitest majors noted as tooling-only, not shipped).

---

## 3. Classification of findings

- **C-1** — MEDIUM (named mandatory-evidence gap; the underlying behavior is proven by tests + source, but the ordered raw-SELECT proof is absent).
- **C-2** — MEDIUM (accuracy defect + undeclared tooling/dep delta; hard bar intact, so not CRITICAL).
- No CRITICAL, no HIGH. No live-execution path, no broker logic outside External Integration, no Gate mutation, no new table/UI, Gate CLOSED — all proven.

Per ITRGA proportionality (R13): every *risk* item is Level-I proven; two *named* items (one evidence, one disposition) remain ⇒ **CONDITIONAL APPROVAL**, not WITHHELD, not clean APPROVAL. The **version bump to v0.47.0 is HELD**; platform of record remains **v0.46.0** until the `_FINAL` closure.

---

## 4. What is explicitly NOT a finding (disclosed so it is not re-litigated)

- The `session.execute()` / `hub.connect()` / `engine.connect()` grep hits outside External Integration are **benign ORM/WS/DB usage**, not broker logic (R7 residual class, command+output shown).
- The `<span>W6-U01</span>` frontend string is a **build-identity label**, not a UI feature/actuation control (`ExecutionResearchPage.tsx` = False).
- The Wave-5 preamble in `operator results.md` is a **scroll-back artifact**, not a stale pack.

---

## 5. Path to FINAL

On receipt of C-1 (raw refusal-audit SELECT, both codes ≥ 1) and C-2 (dependency-delta explanation + report correction), I will write `ITRGA_VERDICT_W6-U01_FINAL.md` **superseding this CONDITIONAL**, bump the platform to **v0.47.0**, update onboarding, and W6-U02 (simulated runs/fills) becomes the next authorizable Build Order. A single failing item stays a finding; nothing here is relabeled green.

---

## 6. Posture note

The DA delivered a clean, well-structured safety foundation: containment holds, the bright-line is empty, no migration/table/UI, no broker/LLM SDK, CI green, and the refusal seam is audited by construction. The two conditions are the difference between "built correctly" (evident) and "**proven** correctly" (the ITRGA bar). Close them and this unit is FINAL.

---

*We don't guess. We prove.*
**— AXIOM ITRGA**
