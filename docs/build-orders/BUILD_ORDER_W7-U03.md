# BUILD ORDER — W7-U03

## Research Management Collections & Tags

**From:** AXIOM Independent Technical Review & Governance Authority (ITRGA)
**To:** Development Authority (DA), via Operator
**Wave:** 7 — Institutional Platform · **Unit:** W7-U03 · **Policy:** one unit per Build Order
**Date:** 2026-07-18
**Platform of record (pre-unit):** v0.56.0 · Alembic head `20260717_0034` · backend **366 passed** · frontend **19 files / 61 tests**
**Governing docs:** accepted `WAVE7_ENGINEERING_DESIGN_AND_IMPLEMENTATION_PLAN.md` §2 (Research management) + §5.2; `ITRGA_REVIEW_WAVE7_DESIGN_PLAN.md` (R7-3/R7-5/R7-7/GR7-8/GR7-9/GR7-10); `ITRGA_VERDICT_W7-U02_FINAL.md` (isolation harness + OBS-W7U02-AUTHZ-ORDER); `05_SYSTEM_ARCHITECTURE.md` §30/§11.1.
**Constitutional posture:** Governance Gate **CLOSED**. Metadata organization over existing governed artifacts — **no mutation of source artifacts**, no action/order/account/execution field or control.
**Motto:** *We don't guess. We prove.*

---

## 1. Purpose

Let operators **organize** existing governed research artifacts (advisory signals, institutional reports, scenarios, simulations, plans, journals, execution-research artifacts) into **collections** and apply **tags** — a metadata layer that **never mutates the original artifact's content or audit** (R7-5). Per-operator scoped (R7-3, corrected harness). First multi-table W7 unit.

---

## 2. Scope (build exactly this)

1. **Tables + migrations** from `20260717_0034`:
   - `research_collections` → `20260717_0035` (`operator_id` FK → `operators.id`; `name`, `description`, `research_status`, timestamps, `audit_correlation_id`)
   - `research_collection_members` → `20260717_0036` (FK → `research_collections`; `artifact_type`, `artifact_id` reference-only; `operator_id`; `audit_correlation_id`)
   - `research_tags` → `20260717_0037` (`operator_id`; `artifact_type`, `artifact_id` reference-only; `tag`; `audit_correlation_id`)
   - **Members/tags reference an artifact by (type, id) only — no FK that could cascade/mutate the source; no copy of source content beyond immutable reference metadata.**
2. **Committing service + operator-scoped read/write API** (create collection, add/remove member, add/remove tag, list/detail) — all scoped to the authenticated operator. **Authorize-before-validate** on mutation endpoints (OBS-W7U02-AUTHZ-ORDER: cross-operator mutation returns **403** deterministically, before body validation).
3. **Frontend research-management UI** (collection/tag explorer over existing artifacts), research-framed, no action/order/account controls.
4. **Audit rows** for collection/member/tag create + delete into immutable `audit_events` (no-orphan JOIN).
5. Frontend Vitest tests.

### FORBIDDEN fields (must be ABSENT — prove via `information_schema` on all three tables)
`order_payload, order_intent, broker_account_id, account_id, position_id, live_position_id, execution_status, real_pnl, pnl, balance, margin, capital, gate_state, open_gate, allow_execution` — **and no `source_artifact_content`/materialized copy of the source** (reference by id only).

---

## 3. Binding refinements applied

- **R7-5 (CENTRAL) — no mutation of source artifacts.** Tagging/collecting an artifact must NOT change its content or audit. Prove with the **before/after identity** pattern: capture a source artifact's row (hash or `Compare-Object`) before a tag/collection op, perform the op, re-capture → **identical** (source unchanged), and show the source's own audit trail gained **no** new mutation event. Cover ≥1 real governed artifact type.
- **R7-3 — per-operator isolation (corrected harness).** Two REAL operators with valid tokens: B cannot read/list/mutate A's collections/tags (403/empty) + raw 0-leakage. (Use the W7-U02 C-1 corrected harness — verify `LOGIN 200` + non-empty token first.)
- **OBS-W7U02-AUTHZ-ORDER — authorize-before-validate:** cross-operator mutation returns **403** regardless of body (not 422). Prove with a cross-operator write carrying an empty/invalid body → **403**.
- **R7-7 / GR7-8 — no secrets/PII** in collection/tag names/descriptions/metadata (`stored_secret_marker_count 0`).
- **GR7-9 — persistence-capture** for EACH of the three tables (raw SELECT ≥1 row + no-orphan audit JOIN → 0 + `operator_id`-vs-`operators` JOIN → 0; member/tag artifact reference resolves — lineage sanity).
- **GR7-10 — browser evidence.** **GR7-1 — Gate CLOSED.**

---

## 4. Mandatory tests (deliver names + raw PASS lines)

```
test_research_collection_persists_and_audit_no_orphan
test_research_collection_member_persists_and_audit_no_orphan
test_research_tag_persists_and_audit_no_orphan
test_tagging_or_collecting_does_not_mutate_source_artifact_or_its_audit   # R7-5 CENTRAL
test_research_management_is_operator_scoped_two_operator_isolation        # R7-3 (valid tokens)
test_cross_operator_mutation_returns_403_before_body_validation           # OBS authorize-first
test_research_management_tables_have_no_forbidden_or_source_content_columns
test_research_management_has_no_secret_or_pii_markers
test_research_management_requires_auth
test_gate_remains_closed_for_wave7
```
Frontend (Vitest), named:
```
ResearchManagementPage lists collections/tags over existing artifacts (read-only of others' data blocked)
ResearchManagementPage exposes no execution/order/account/actuation controls
ResearchManagementPage requires auth / blocks logged-out access
```
Plus standing `test_broker_integration.py` green. Full backend regression ≥ **366** + new; frontend ≥ **19 files** (report actual totals).

---

## 5. Mandatory evidence (operator-run on target — Level-I; + screenshots)

Deliver `DELIVERY_REPORT_W7-U03.md` + `operator results.md` (+ screenshots), **inline**:

**(a) Build identity.** `Test-Path` new files + proof the pack is OF **W7-U03**; version `0.57.0`.
**(b) Test transcript.** Named backend + frontend tests + broker suite + full totals.
**(c) Migration proof.** `alembic upgrade head` then `alembic current` = **`20260717_0037 (head)`**; three revision files exist.
**(d) PERSISTENCE-CAPTURE (GR7-9, INLINE, raw psql) — EACH of the three tables:** committing script; raw `SELECT ≥1 row`; **no-orphan audit JOIN → 0**; **`operator_id`-vs-`operators` JOIN → 0**.
**(e) Forbidden/source-content column proof.** `information_schema.columns` over all three tables for §2 forbidden list (+ no `source_artifact_content` / materialized-copy column) → **0 rows**.
**(f) R7-5 NO-MUTATION (raw, on target).** Before/after of a real source artifact (row hash / `Compare-Object`) across a tag+collection op → **identical**; and the source artifact's audit gained no mutation event. State the artifact type/id used (may be masked).
**(g) TWO-OPERATOR ISOLATION (R7-3, valid tokens).** `LOGIN_A/B 200` + tokens present; B read/list/mutate A's collection/tag → 403/empty; `B_VISIBLE_A_COUNT 0`; raw 0-leakage.
**(h) AUTHORIZE-BEFORE-VALIDATE (OBS).** cross-operator mutation with empty body → **403** (not 422).
**(i) No-secret/PII (R7-7).** `stored_secret_marker_count 0` across names/descriptions/metadata + grep clean.
**(j) BROWSER EVIDENCE (GR7-10).** served-session shots: research-management UI (collections/tags over existing artifacts) + **no actuation controls** + **logged-out block** (URL bar on the protected route → login, or unauth 401/302).
**(k) No barred dependency.** grep empty; state any dep change accurately.
**(l) CI (GR7-11).** Git-Bash → `LOCAL_CI_EXIT_CODE: 0`.
**(m) Gate-closed proof.** named test PASS + broker suite green.

---

## 6. Acceptance criteria

APPROVED requires ALL of (a)–(m); named tests + broker suite green; regression green with actual totals; raw SELECT ≥1 row per table; **no-orphan JOINs = 0** (audit + operators, all three tables); forbidden/source-content columns absent; **R7-5 source unchanged (before==after)**; **two-operator isolation + 0 leakage (valid tokens)**; **cross-operator mutation 403 before body validation**; no secret/PII; browser shots present; CI exit 0; Gate CLOSED.

- A single CRITICAL (any source-artifact mutation via tag/collection; any cross-operator leakage or cross-operator mutation that succeeds; any action/order/account/execution field or control; any secret/PII leak; any Gate mutation) ⇒ **WITHHELD.**
- Missing/unreachable/sandbox-only browser shots or a null-token isolation probe (R7 non-result) ⇒ **WITHHELD/CONDITIONAL** (W7-U02 C-1 lesson).
- Every *risk* item proven but a *named* proof missing ⇒ **CONDITIONAL** (→ `_FINAL` on closure).

On approval: platform bump to **v0.57.0**; head `20260717_0037`; onboarding updated; W7-U04 (API Ecosystem Catalogue & Versioned Research API Hardening) becomes next authorizable.

---

## 7. Reminders to DA

- **R7-5 is the red line:** organizing must never mutate the organized — prove source before==after + no new mutation audit.
- Isolation harness: verify `LOGIN 200` + non-empty token FIRST (W7-U02 C-1 lesson); authorize-before-validate so cross-operator writes are **403**.
- Members/tags reference artifacts by (type,id) only — no source-content copy, no cascading FK.
- Persistence-capture raw psql per table INLINE (no API read-back). Browser shots mandatory. Verify the pack is OF W7-U03; state dep changes accurately.

---

*We don't guess. We prove.*
**— AXIOM ITRGA**
