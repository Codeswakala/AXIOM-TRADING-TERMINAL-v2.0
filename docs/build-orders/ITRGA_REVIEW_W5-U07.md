# ITRGA INDEPENDENT REVIEW — W5-U07 (Manual Research Journal)

| Field | Value |
|---|---|
| Reviewing authority | **AXIOM Independent Technical Review & Governance Authority (ITRGA)** |
| Unit | **W5-U07** — Manual Research Journal |
| Wave | 5 — Human-AI Collaboration |
| Build Order | `docs/BUILD_ORDER_W5-U07.md` |
| Evidence | `uploads/DELIVERY_REPORT_W5-U07.md` + `uploads/operator results.md` (1,440 lines) + 3 browser screenshots |
| DA-claimed platform | 0.45.0 |
| Review date | 2026-07-17 |
| **VERDICT** | **🟡 CONDITIONAL APPROVAL — C-1: logged-out-block browser screenshot not supplied (R5-6). Inert/not-a-broker-record + all other function APPROVED.** |
| Confidence | **HIGH** on safety/inertness; the gap is one named browser proof |

> **We don't guess. We prove.** A journal entry is proven to be a research log that cannot be a broker record — inert schema, no-P&L/no-broker test, no-orphan audit, CI green. The one gap is the mandatory logged-out screenshot.

---

## 1. Bottom line

The keystone is met to standard: a journal entry is **a research log, NOT a broker record** — inert schema
(forbidden columns **0 rows**), a **named no-P&L/no-broker-import test**, 9 named tests total (incl. triggers-
nothing + not-read-by-execution-or-signal-paths), no-orphan audit, and a browser surface with **no broker/
account/execution/P&L controls**. CI is green via the documented Git-Bash path (`LOCAL_CI_EXIT_CODE: 0`, 291
backend / 53 frontend). **The single gap:** the mandatory R5-6 browser set is **4 of 5** — the **logged-out
block** screenshot on `/journal` was not attached (the operator opened `/login` via `Start-Process` in the
checklist but no logged-out image was supplied). Per proportionality (R13), safety is fully proven ⇒
**CONDITIONAL APPROVAL**, with that one browser proof to supply. *(A secondary note: the explicit curl
API-status table was not run this turn, but auth + no-exec-endpoint are covered by two passing named tests —
accepted as equivalent; see §4 OBS.)*

---

## 2. R5-4 / GR-9 — journal is a research log, not a broker record (keystone) — PROVEN ✅

- **Inert schema:** `information_schema.columns` forbidden-column query → **`(0 rows)`** (no broker/account/
  execution/fill/quantity/lot_size/order_size/position_size/P&L columns).
- **9 named tests PASS:** `..._rejects_forbidden_fields_recursively`,
  **`..._rejects_pnl_and_broker_import_text`** (no-P&L/no-broker keystone),
  `..._schema_is_inert_no_broker_or_execution_columns`, `..._persists_and_audits_no_orphan`,
  `..._update_is_audited_and_remains_inert`, `..._triggers_nothing_beyond_entry_and_audit`,
  **`..._not_read_by_execution_or_signal_paths`**, `..._api_auth_create_list_detail_update`,
  `..._api_rejects_forbidden_payload_and_has_no_exec_endpoint`.
A journal entry cannot import, reconcile, or become a broker/execution record, and claims no P&L. ✅

## 3. Persistence, browser (partial), regression — PROVEN ✅

| Control | Evidence |
|---|---|
| **R5-7 no-orphan** | raw `SELECT` (research_only entry `21a43824…`) + audit JOIN (resource_id + correlation_id + action `manual_trade_journal_entry.created`) → **`orphan_count 0`** |
| Browser (4 of 5) | `/journal` rendered (served); "**Manual research reflection only.** Not financial advice, not a trade record, not a trade instruction… AXIOM does not act." disclaimer; reflection editor + detail with **text/tag fields only** (title/reflection/linked plan+signal+report ids/emotion+process tags/lesson notes); **no broker/account/execution/P&L/order controls** — only "Save reflection"/"Update selected reflection" |
| **R5-2 no LLM/dep** | collaboration grep no `openai\|anthropic\|transformers\|langchain\|llama`; page grep no broker/account/execution/fill/P&L; no new dep |
| **R5-8 grep + gate** | wave-wide grep residuals benign (disclosed); Gate CLOSED |
| CI | **`& "C:\Program Files\Git\bin\bash.exe" scripts/local_ci.sh` → `Local CI equivalent complete` + `LOCAL_CI_EXIT_CODE: 0`** (transcript W5-U07); backend **291 passed** (282→291, +9), frontend **53 tests**, ruff clean, npm audit 0; migration `20260717_0027` |
| AI path | none this unit (correctly stated) |

---

## 4. Condition to close (+ observation)

### C-1 (must close) — logged-out-block browser screenshot on `/journal`
The mandatory R5-6 browser set requires (among the shots) a **logged-out block**: an unauthenticated visit to
`/journal` refused/redirected to login (not rendered). This turn supplied the shell + journal-editor + journal-
detail shots but **no logged-out image** (the operator's `Start-Process http://localhost:8000/login` +
checklist note is not a captured screenshot of the blocked `/journal` route). Supply that one screenshot.

*Why not waived:* the logged-out block is a **named, mandatory** UI-safety proof for every operator surface
(W4-U07 C-2 precedent) — auth is corroborated by the passing `..._api_auth_...` test, but the on-screen block
must be shown, as for every prior Wave-5 UI.

### OBS (non-blocking) — explicit curl API-status table not run this turn
The unauth-401 / exec-submit-emit-405 curl table wasn't captured on target this turn; auth + no-exec-endpoint
are covered by `test_manual_journal_api_auth_create_list_detail_update` and
`test_manual_journal_api_rejects_forbidden_payload_and_has_no_exec_endpoint` (both PASS). Accepted as
equivalent — optionally add the curl table with the C-1 re-shot for a complete archive.

---

## 5. Findings ledger

| ID | Severity | Finding | Disposition |
|---|---|---|---|
| **C-1** | LOW–MEDIUM | Logged-out-block browser screenshot on `/journal` not supplied (R5-6 mandatory set 4 of 5) | **Condition — supply the logged-out screenshot** |
| OBS | LOW | Explicit curl API-status table not run on target (covered by 2 passing named tests) | Non-blocking; optional |
| — | — | R5-4/GR-9 inert + no-P&L/no-broker (schema 0 rows + 9 tests) · R5-7 no-orphan · browser 4/5 · R5-2 no-LLM · gate-closed · 291 tests · CI exit 0 | ✅ proven |

**No CRITICAL/HIGH. No safety/governance breach.** One named UI browser proof outstanding ⇒ **CONDITIONAL
APPROVAL** (not withheld — every risk item is proven; the journal surface itself is browser-proven).

---

## 6. Disposition & next step

- **W5-U07 — 🟡 CONDITIONAL APPROVAL.** Inert/not-a-broker-record journal + all function **APPROVED**. Platform
  advances to **v0.45.0 on closure of C-1** (until then v0.44.0 remains the version of record for ITRGA
  purposes).
- **To close:** supply the **logged-out-block browser screenshot** on `/journal` (unauthenticated → login).
  No re-implementation. On that, ITRGA issues the FINAL verdict, advances to v0.45.0, and (on operator
  authorization) issues `BUILD_ORDER_W5-U08.md` (Wave-5 Closeout — the LAST Wave-5 unit → "Human-AI
  Collaborative Workspace Complete").
- Commendation: the keystone is exactly right — inert schema (0 forbidden columns), a **dedicated no-P&L/
  no-broker-import test**, a not-read-by-exec test, no-orphan audit, and a journal UI with **no broker/account/
  P&L affordance at all**. The gap is one missing screenshot.
- DA does not self-advance the version, self-close C-1, build W5-U08, ship an LLM, add a broker/account/
  execution linkage, or open the Gate.

> **We don't guess. We prove.** — ITRGA
