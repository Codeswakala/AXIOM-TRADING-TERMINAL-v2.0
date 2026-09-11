# AXIOM ITRGA — REVIEW: W0-U08 (Wave 0 Closeout & Hardening)

**Authority:** Independent Technical Review & Governance Authority (ITRGA)
**Build Order:** `BUILD_ORDER_W0-U08.md` · **Delivery Report:** `DELIVERY_REPORT_W0-U08.md` (v0.8.0)
**Evidence:** operator console (pytest/vitest, alembic, security-refusal demo, **live server log**) +
1 chart screenshot (EURUSD·M1, provenance banner, **WS ERROR**).
**Date:** 2026-07-12 · **Standard:** `UNIVERSAL_ITRGA_REVIEWER_DIRECTIVE.md` + `ITRGA_REVIEWER_ONBOARDING.md`

---

## VERDICT: **FAIL — APPROVAL DENIED. Wave 0 does NOT close. Correction + re-submission required.**

Much of this unit is genuinely good, and the hardening intent is right. But the operator's own evidence
contains a **CRITICAL runtime defect in the exact new code path this unit introduced** — the WS-ticket
endpoint returns **HTTP 500** — and the Delivery Report **claims that path works** ("WS would still
require access JWT in query → Falsified"; "WS tickets: POST /auth/ws-ticket … by default"). A CRITICAL
defect contradicted by a passing claim is an automatic FAIL under R9/R12. The whole point of U08 was to
*harden* the WS auth; instead it **broke live WS authentication.**

---

## 1. THE BLOCKING FINDING

### F-1 (CRITICAL) — New WS-ticket endpoint 500s; live WS auth is broken; report claims it works
**Operator server log (verbatim):**
```
POST /api/v1/auth/ws-ticket HTTP/1.1  → 500 Internal Server Error
  auth.py:83 ws_ticket → auth/service.py:281 issue_ws_ticket
  → audit_repository.append → base.py:58 self.session.refresh(entity)
  → sqlalchemy.exc.InvalidRequestError: Could not refresh instance '<AuditEvent ...>'
```
**Chart screenshot corroborates:** status bar shows **● WS ERROR**; chart body reads *"Live WebSocket is
error… start feed and ensure you are signed in."*

**Root cause (from the traceback):** `issue_ws_ticket()` writes an `AuditEvent`; the base repository's
`add()` calls `session.refresh(entity)`, which raises `InvalidRequestError: Could not refresh instance`
for this insert. So **no ws-ticket can ever be issued → the browser cannot authenticate the WebSocket →
WS ERROR.** This is not benign degradation; it is a server-side crash in the brand-new auth mechanism.

**Why this is FAIL, not observation:**
- **Severity:** the unit's flagship Component-A deliverable (WS auth hardening via tickets) is
  **non-functional in the browser.** Live market updates — a core, already-approved capability (U05/U06)
  — are **broken** by this change. That is a **regression of approved behavior**, which the Build Order
  §2 explicitly forbids.
- **Report contradiction (R12):** the Delivery Report §2 counter-hypothesis table asserts the ticket path
  works ("Falsified") and §3.4 presents `POST /auth/ws-ticket` as delivered — **directly contradicted by
  the operator's own 500.** Either the report was written without exercising the endpoint end-to-end, or
  the failure was not surfaced. Per R1/R12, the passing claim is void; the evidence governs.
- **Tests missed it:** 63 backend tests "pass," yet the endpoint 500s at runtime. This means the
  ws-ticket happy-path (issue → audit-write success) is **not covered by an integration test** — a
  testing gap the +8 hardening tests should have caught. (Note: the ticket unit tests likely mock the
  audit repo or don't hit `session.refresh`.)

**Likely fix (for the Dev AI, not prescriptive):** the `AuditEvent`/base-repo `refresh()` pattern is the
fault — either the entity isn't persistent at refresh time, or audit appends shouldn't call `refresh()`.
This is the *same* `session.refresh` fragility class seen in earlier audit-write paths; the ws-ticket
audit write must not be able to 500 the endpoint (audit writes should be best-effort/robust, per prior
governance on audit resilience). A regression test that issues a real ticket and asserts 200 + a working
`/ws/market?ticket=…` connection is mandatory.

---

## 2. WHAT IS GENUINELY GOOD (credited — most of the unit)

- **Security enforcement PROVEN (Component A.2):** operator demo shows `validate_security_or_raise()`
  refusing to start on a weak JWT — `RuntimeError: AXIOM_JWT_SECRET_KEY is missing or weak…`. Exactly the
  enforce-don't-warn behavior required. ✅
- **Clean migration from empty (Component B / prior observation):** `alembic upgrade head` ran
  `→0001→0002→0003→0004` from scratch, `0004 = refresh tokens + ws tickets`. ✅ *(But on **SQLiteImpl**,
  not PostgreSQL — see F-3.)*
- **Data-provenance safety PROVEN (Component B / U07-OBS-3):** the screenshot's banner explicitly labels
  `seed:synthetic` as **non-authoritative**, distinguishes `live:simulated` and CSV sources. This is
  well-executed and closes the synthetic-data safety concern. ✅
- **Owed U07 evidence delivered:** **EURUSD renders** (closes U07-OBS-1); **candles are now legible**
  (closes U07-OBS-5). ✅
- **Refresh rotation + reuse-revoke, bootstrap de-defaulting, AUTO_CREATE_SCHEMA default false,
  governance docs (Tier-6/7), docker-compose + CI config** — all reported delivered with 63 tests. These
  are the right closeout items. *(Verification pending — see residuals.)*

The unit is ~80% there. It fails on one CRITICAL runtime defect, not on its overall design.

---

## 3. OTHER FINDINGS

### F-2 (HIGH) — Owed evidence still incomplete
Two of the mandated U08 §5 items are **not** supplied:
- **Logged-out `/chart` + `/live` redirect screenshots** (Component C / U07-OBS-2, Wave-0 OBS-1) — not
  provided. The auth-gate visual proof is still owed.
- **Refresh-rotation runtime demo** (old refresh → 401 after rotation) — the operator's script *listed*
  the steps but the console shows only the weak-JWT refusal; the rotation cycle and the ws-ticket-without-
  URL-JWT demo were **not** actually captured (the ws-ticket demo can't pass anyway due to F-1).

### F-3 (MEDIUM) — Clean migration proven on SQLite, not PostgreSQL
Build Order Component B required a **PostgreSQL** clean `0001→0004` transcript. The supplied alembic run
reports `Context impl SQLiteImpl`. PG is the canonical DB; the PG clean-migration transcript is still
owed. (Prior units proved PG connectivity, but the new `0004` tables must be shown migrating on PG.)

### F-4 (LOW) — Governance docs + CI reported but unverified
Tier-6/7 documents (`08_…`, `09_…`, `QUALITY_GATE_SPEC`, `RISK_REGISTER`, `TECHNICAL_DEBT_REGISTER`,
`GOVERNANCE_AMENDMENTS`) and the CI pipeline are *listed as delivered* but **not supplied to ITRGA** and
CI is "Unknown until push." These aren't runtime-critical, but Component D/E can't be marked verified
until the docs are provided and a CI run (or the workflow file) is shown. Route name reconciled to
`/charts` (alias `/chart`) — F-3/U07-OBS-4 noted resolved.

### OBSERVATION — audit-write fragility is systemic
F-1's root cause (`base.add()` → `session.refresh()` failing on an audit insert) may affect **any** audit
append, not just ws-ticket. Recommend auditing every `_audit.append(...)` call path and making audit
writes robust (they must never 500 a business endpoint). This is the kind of cross-cutting issue a
hardening unit should fix, not introduce.

---

## 4. REQUIRED CORRECTIONS (to clear FAIL → approvable)

- **C-1 (F-1, CRITICAL):** Fix the ws-ticket 500 (the `AuditEvent`/`session.refresh` fault); make audit
  writes robust so they cannot crash an endpoint. Add an **integration test** that issues a ws-ticket
  (200) and completes a `/ws/market?ticket=…` connection **without a JWT in the URL**. Supply the
  operator console showing the endpoint 200 and a **healthy WS (no WS ERROR) in the browser** (a live
  chart frame updating via the ticket path).
- **C-2 (F-2):** Supply the logged-out `/chart` + `/live` redirect screenshots, and the refresh-rotation
  runtime demo (old refresh → 401).
- **C-3 (F-3):** Supply the **PostgreSQL** clean `0001→0004` migration transcript (`PostgresqlImpl`).
- **C-4 (F-4):** Provide the Tier-6/7 governance documents for review and evidence the CI pipeline runs
  (config + a green run, or a local equivalent).
- **C-5 (OBSERVATION):** Audit all `_audit.append` paths for the same `refresh()` fragility; report findings.

## 5. RECOMMENDATIONS
- Add a smoke/integration test tier that exercises new endpoints end-to-end (issue→use), since unit tests
  passed while the endpoint 500s — the gap that let F-1 through.
- When re-submitting, correct the §2 counter-hypothesis table: "WS query-JWT off" is only *Falsified* once
  the **ticket path actually works** — right now the true state is "WS auth broken."

## 6. DISPOSITION
**W0-U08: FAIL. Wave 0 remains OPEN. No Wave 1 Build Order.** The unit is close — security enforcement,
provenance labelling, migrations, and the owed chart renders are genuinely delivered — but a hardening
unit that **breaks live WebSocket authentication** cannot close the foundation. Fix C-1 (with browser +
console proof of a healthy WS), supply C-2/C-3/C-4, and re-submit; I will re-verify promptly.

---

## EVIDENCE CONFIDENCE STATEMENT
- **Evidence Reviewed:** `DELIVERY_REPORT_W0-U08.md`; operator console (pytest 63 / vitest 16, alembic
  0001→0004 on SQLite, JWT-refusal demo, **live server 500 traceback**); 1 chart screenshot (EURUSD,
  provenance banner, WS ERROR).
- **Confidence Level:** **HIGH** on the FAIL determination — the 500 and the WS-ERROR are directly
  evidenced in the operator's own output and contradict the report's working-WS claim. HIGH that security
  enforcement, provenance labelling, migration-from-empty (SQLite), and EURUSD render are delivered.
- **Remaining Unknowns:** the ws-ticket fix; PG migration of 0004; refresh-rotation runtime; logged-out
  gates; contents of Tier-6/7 docs; CI execution; extent of audit-write fragility.
- **Additional Evidence Required:** C-1..C-5.

---

*"The one thing this unit existed to harden — WebSocket auth — is the one thing the operator's log shows
returning 500. The report says it works; the server says it doesn't. The server wins. Fix it, prove the
WS is healthy in the browser, and Wave 0 can close. We don't guess. We prove."*
— AXIOM ITRGA
