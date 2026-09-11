# ITRGA INDEPENDENT REVIEW — W5-U06 (Inert Trade Planning Workspace)

| Field | Value |
|---|---|
| Reviewing authority | **AXIOM Independent Technical Review & Governance Authority (ITRGA)** |
| Unit | **W5-U06** — Inert Trade Planning Workspace (GR-9 keystone) |
| Wave | 5 — Human-AI Collaboration |
| Build Order | `docs/BUILD_ORDER_W5-U06.md` |
| Evidence | `uploads/DELIVERY_REPORT_W5-U06.md` + `uploads/operator results.md` (533 lines) + 4 browser screenshots |
| DA-claimed platform | 0.44.0 |
| Review date | 2026-07-17 |
| **VERDICT** | **🟡 CONDITIONAL APPROVAL — C-1: `local_ci.sh` Git-Bash run + `LOCAL_CI_EXIT_CODE: 0` absent from the transcript. GR-9 inert + all safety/function APPROVED.** |
| Confidence | **HIGH** on safety/inertness; the gap is one missing *named* CI-evidence item |

> **We don't guess. We prove.** The trade plan is proven inert three ways and shows no order-ticket surface — the GR-9 keystone holds. The one gap is the CI-wrapper transcript with its inline exit code.

---

## 1. Bottom line

The GR-9 keystone is met to the strongest standard: a trade plan is **structurally a research note that cannot
be an order** — inert schema (forbidden columns **0 rows**), 9 named tests (incl. triggers-nothing and
**not-read-by-execution-or-signal-paths**), no order-ticket UI, and `/execute`+`/submit`+`/emit-signal`
endpoints proven **absent (405)**. Persistence is audited no-orphan; API create/list/detail/update work
read-only-safe; browser evidence is complete; no LLM. Every individual gate is green (pytest **282**, ruff,
npm audit 0, build ✓). **The single gap:** the pasted `operator results.md` **does not contain the
`& "C:\Program Files\Git\bin\bash.exe" scripts/local_ci.sh` run or the inline `LOCAL_CI_EXIT_CODE: 0`** — a
standing, named acceptance criterion (R5-8). Per proportionality (R13), safety is fully proven ⇒ **CONDITIONAL
APPROVAL**, with that one CI-evidence item to supply.

---

## 2. GR-9 / R5-4 — inert trade plan (keystone) — PROVEN ✅

- **Inert schema:** `information_schema.columns` forbidden-column query → **`(0 rows)`** (no order_payload/
  side/quantity/lot_size/order_size/position_size/entry_price_order/stop_loss/take_profit/broker_account_id/
  account_id/position_id/execution_status).
- **9 named tests PASS:** `..._rejects_forbidden_fields_recursively`, `..._rejects_unknown_and_guarantee_fields`,
  `..._schema_is_inert_no_order_ticket_columns`, `..._persists_and_audits_no_orphan`,
  `..._update_is_audited_and_remains_inert`, `..._triggers_nothing_beyond_plan_and_audit`,
  **`..._not_read_by_execution_or_signal_paths`**, `..._api_auth_create_list_detail_update`,
  `..._api_rejects_forbidden_payload_and_has_no_exec_endpoint`.
- **Endpoints proven absent (above spec):** `EXECUTE_STATUS:405`, `SUBMIT_STATUS:405`, `EMIT-SIGNAL_STATUS:405`.
A trade plan cannot be, contain, or reach an order. ✅

## 3. Persistence, API, no-order-ticket, browser — PROVEN ✅

| Control | Evidence |
|---|---|
| **R5-7 no-orphan** | raw `SELECT` (draft plan row) + audit JOIN (resource_id + correlation_id + action `trade_plan_note.created`) → **`orphan_count 0`**; repo no-orphan by construction |
| API | create → `CREATE_PLAN_ID` + `CREATE_DISCLAIMER_PRESENT: True`; unauth **401** / list **200** / detail **200**; update → `decision_status reviewed` (audited, inert); exec/submit/emit **405** |
| No order-ticket UI | page grep (`buy\|sell\|quantity\|stop loss\|take profit\|position\|execute\|broker_account\|account_id`) empty; frontend test; browser |
| **Browser (R5-6, 4 shots)** | Trade Planning workspace rendered (`/trade-plans`) with "**Research plan note only.** …not a trade instruction, not an order ticket. …AXIOM does not act."; editor with **text-only fields** (title/market_context/hypothesis/linked ids/scenario+risk notes/invalidating conditions) — **no buy/sell/quantity/SL/TP/position/execute controls**; detail view (research_status research_only); logged-out block |
| **R5-2 no LLM/dep** | collaboration grep no `openai\|anthropic\|transformers\|langchain\|llama`; no new dep |
| **R5-8 grep + gate** | wave-wide grep residuals all benign (forbidden-key lists / `no_order_payload` string / hardening strings / `aside`/disclaimer text), disclosed; Gate CLOSED |
| Regression | 49 named collab tests PASS; backend **282 passed** (273→282, +9), frontend **16 files / 48 tests** (+5); ruff clean; npm audit 0; migration `20260717_0026` |
| AI path | none this unit (correctly stated) |

---

## 4. Condition to close

### C-1 (must close) — supply the `local_ci.sh` Git-Bash run + inline `LOCAL_CI_EXIT_CODE: 0`
The transcript ends after the API/grep evidence; it does **not** include the documented CI-wrapper run
(`& "C:\Program Files\Git\bin\bash.exe" scripts/local_ci.sh`) with `==> Local CI equivalent complete` and
**`LOCAL_CI_EXIT_CODE: 0`**. This is a standing, named acceptance criterion (R5-8), and — per the project's own
history (the W4-U03 WSL exit-code artifact) — the wrapper's exit code is exactly what must be captured, not
inferred from individually-green gates. Supply that transcript snippet.

*Why not waived:* every individual gate is green, so this is low-risk — but it is a *named* mandatory item, and
I don't approve a named CI gate as green on inference. (This mirrors the W4-U02 C-1 disposition: core proven,
one named-proof item outstanding.)

---

## 5. Findings ledger

| ID | Severity | Finding | Disposition |
|---|---|---|---|
| **C-1** | LOW–MEDIUM | `local_ci.sh` Git-Bash run + inline `LOCAL_CI_EXIT_CODE: 0` absent from the transcript (R5-8) | **Condition — supply the CI transcript snippet** |
| — | — | GR-9/R5-4 inert (schema 0 rows + 9 tests + endpoints 405) · R5-7 no-orphan · no-order-ticket · browser · R5-2 no-LLM · gate-closed · 282 tests | ✅ proven |

**No CRITICAL/HIGH. No safety/governance breach.** One named CI-evidence item ⇒ **CONDITIONAL APPROVAL** (not
withheld — every risk item is proven; all individual gates are green).

---

## 6. Disposition & next step

- **W5-U06 — 🟡 CONDITIONAL APPROVAL.** GR-9 inert trade plan + all safety/function **APPROVED**. Platform
  advances to **v0.44.0 on closure of C-1** (until then v0.43.0 remains the version of record for ITRGA
  purposes).
- **To close:** supply the `local_ci.sh` run via the documented Git-Bash path showing `==> Local CI equivalent
  complete` + **`LOCAL_CI_EXIT_CODE: 0`** (transcript labelled W5-U06). No re-implementation.
- Commendation: the GR-9 proof is exactly the standard — inert schema (0 forbidden columns), a
  **not-read-by-execution-or-signal-paths** test, endpoints proven absent (405), and a browser surface with
  **no order-ticket patterns at all**. The single gap is the CI-wrapper transcript.
- **On closure → v0.44.0 →** ITRGA recommends **W5-U07 — Manual Research Journal** (R5-4 inert — no broker/
  account/execution fields; R5-6 browser; R5-7 inline; R5-8). DA does not self-advance the version, self-close
  C-1, build W5-U07, ship an LLM, add an actuating tool/execution/order/account linkage, or open the Gate.

> **We don't guess. We prove.** — ITRGA
