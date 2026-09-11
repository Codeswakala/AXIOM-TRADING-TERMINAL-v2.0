# BUILD ORDER — W7-U04

## API Ecosystem Catalogue & Versioned Research API Hardening

**From:** AXIOM Independent Technical Review & Governance Authority (ITRGA)
**To:** Development Authority (DA), via Operator
**Wave:** 7 — Institutional Platform · **Unit:** W7-U04 · **Policy:** one unit per Build Order
**Date:** 2026-07-18
**Platform of record (pre-unit):** v0.57.0 · Alembic head `20260717_0037` · backend **377 passed** · frontend **20 files / 64 tests**
**Governing docs:** accepted `WAVE7_ENGINEERING_DESIGN_AND_IMPLEMENTATION_PLAN.md` §2 (API ecosystem) + §4.3 + §5.4; `ITRGA_REVIEW_WAVE7_DESIGN_PLAN.md` (R7-2/R7-3/R7-7/GR7-5/GR7-8/GR7-9); `ITRGA_VERDICT_W7-U01_FINAL.md` (route-inventory + no-execution-surface precedent); `05_SYSTEM_ARCHITECTURE.md` §43/§77 (approved API contracts / no secrets in telemetry).
**Constitutional posture:** Governance Gate **CLOSED**. Documented/authenticated **research** API surface — no execution/order/account endpoint, no secrets/PII, no Gate reach.
**Motto:** *We don't guess. We prove.*

---

## 1. Purpose

Publish a **documented, authenticated, versioned API catalogue** for the existing research/institutional endpoints, and harden the API surface: every route auth-gated, per-operator scoped, abuse-guarded, and — the central control (R7-2/GR7-5) — with **no execution/order/account/broker/open-gate endpoint anywhere**, proven by absence. This extends the W7-U01 route-inventory foundation to the whole research API. No new *feature* capability; a catalogue + hardening unit.

---

## 2. Scope (build exactly this)

1. **API catalogue** exposing the versioned research/institutional route inventory (path, methods, permission, version, description) via the existing FastAPI/OpenAPI patterns and an authenticated `route-inventory`/`api-catalogue` endpoint — building on W7-U01's `route-inventory` (which already asserts `actuation_surface_present:false`).
2. **API hardening across the research surface:** confirm auth on all institutional/research routes (401 unauth), per-operator scoping preserved, and an **abuse/rate guard** if proposed (e.g. rate-limit on the catalogue/list endpoints) — declare explicitly whether a rate guard is added.
3. **Optional catalogue table** `api_contract_catalog` (and/or `api_access_audit_summary`) → migration `20260717_0038` **only if persisted**; if generated from OpenAPI/route table at request time (preferred, OBS-2 of the design review), **no new table** and head stays `20260717_0037`.
4. **No execution surface** — the catalogue must **not** introduce, and must prove the absence of, any execution/order/account/broker/open-gate endpoint.
5. Frontend API-catalogue/docs surface **only if** the DA proposes one (browser evidence then applies); otherwise API-only (state so).

### FORBIDDEN (must be ABSENT — prove)
- **Endpoints:** any `.../execute`, `/order`, `/broker`, `/account`, `/open-gate`, `/go-live`, order-routing, or Gate-mutation route → **404/405**.
- **Columns (if any catalogue table persisted):** `order_payload, broker_account_id, account_id, position_id, execution_status, real_pnl, pnl, balance, margin, capital, gate_state, open_gate, allow_execution, secret, api_key, token` via `information_schema` → 0 rows.
- **Payloads:** no `access_token|refresh_token|jwt|password|secret|api_key|private_key|hashed_password` in any catalogue/API response.

---

## 3. Binding refinements applied

- **R7-2 / GR7-5 (CENTRAL) — no execution surface, proven by absence:** deliver the **full research/institutional route inventory** + a probe that execution/order/account/broker/open-gate endpoints are **404/405**; the catalogue's own descriptor asserts `actuation_surface_present:false` / `governance_gate_capability_present:false`.
- **Auth on every route (GR7-5):** unauth → **401**; authenticated → 200/expected. Raw status table across the catalogued routes (or a representative set + the catalogue endpoint).
- **R7-3 per-operator scoping preserved:** any operator-scoped route in the catalogue still enforces scoping (spot-check with the corrected two-operator harness — valid tokens; B cannot read A's scoped resource). `operator_id → operators.id` if any table.
- **Authorize-before-validate (carried, OBS-W7U02 resolved):** any mutation endpoint returns **403** for cross-operator before body validation.
- **R7-7 / GR7-8 / §77 — no secrets/PII** in catalogue/API responses (marker check) + structured logs redacted.
- **Abuse guard:** if a rate/abuse guard is added, prove it (e.g. Nth request → 429); if not, state explicitly it is deferred (non-blocking for a catalogue unit, but must be declared).
- **GR7-9 persistence-capture** IF any catalogue table persisted (raw SELECT + no-orphan audit JOIN → 0 + operator JOIN if operator-scoped + forbidden-column `information_schema` → 0 rows).
- **GR7-1 Gate CLOSED.**

---

## 4. Mandatory tests (deliver names + raw PASS lines)

```
test_api_catalogue_lists_versioned_research_routes
test_api_catalogue_and_research_api_have_no_execution_or_broker_or_gate_endpoint   # R7-2 CENTRAL
test_all_catalogued_routes_require_auth
test_api_catalogue_response_has_no_secret_or_pii_markers
test_api_surface_preserves_operator_scoping_two_operator          # R7-3 (valid tokens)
test_gate_remains_closed_for_wave7
```
(+ `test_api_rate_or_abuse_guard_*` if a guard is added; + persistence-capture/forbidden-column tests if a catalogue table is persisted.)
Plus standing `test_broker_integration.py` green. Full backend regression ≥ **377** + new; frontend baseline ≥ **20 files** (report actual; +tests only if a UI surface is added).

---

## 5. Mandatory evidence (operator-run on target — Level-I)

Deliver `DELIVERY_REPORT_W7-U04.md` + `operator results.md` (+ screenshots IF a UI surface is added), **inline**:

**(a) Build identity.** `Test-Path` new files + proof the pack is OF **W7-U04**; version `0.58.0`.
**(b) Test transcript.** Named tests + broker suite + full backend total (+ frontend if UI).
**(c) Migration state.** If no table: `alembic current` = `20260717_0037` unchanged. If persisted: `alembic current` = `20260717_0038 (head)` + revision file.
**(d) API CATALOGUE + NO-EXECUTION-SURFACE (R7-2, raw).** Auth'd GET of the catalogue/route-inventory (200) showing versioned research routes + `actuation_surface_present:false` / `governance_gate_capability_present:false`; **probe** `POST .../execute|/order|/broker|/account|/open-gate` → **404/405** each.
**(e) AUTH status table (GR7-5).** For the catalogued routes (or representative set + catalogue endpoint): UNAUTH → **401**, AUTH → **200/expected**.
**(f) Operator scoping spot-check (R7-3, valid tokens).** `LOGIN_A/B 200` + tokens present; B cannot read A's operator-scoped resource (403/empty); + authorize-before-validate 403 on a mutation route.
**(g) No-secret/PII (R7-7/§77).** marker check over catalogue/API responses → clean.
**(h) Persistence-capture (IF table).** raw SELECT ≥1 row + no-orphan audit JOIN → 0 (+ operator JOIN if scoped) + forbidden-column `information_schema` → 0 rows.
**(i) Abuse guard.** if added, raw proof (e.g. 429 on Nth request); if not, explicit "deferred" statement.
**(j) No barred dependency.** grep empty (incl. any API-framework/rate-limit lib — if added, state + spike per GR7-12); state dep changes accurately.
**(k) CI (GR7-11).** Git-Bash → `LOCAL_CI_EXIT_CODE: 0`.
**(l) Gate-closed proof.** named test PASS + broker suite green.
**(m) Browser (only if UI added, GR7-10).** served-session shots: catalogue/docs surface, no actuation controls, logged-out block.

---

## 6. Acceptance criteria

APPROVED requires ALL applicable of (a)–(m); named tests + broker suite green; regression green with actual totals; **catalogue lists versioned research routes with `actuation_surface_present:false`**; **execution/order/account/broker/open-gate endpoints proven absent (404/405)**; all catalogued routes auth-gated (401 unauth); operator scoping preserved (valid-token two-operator spot-check); no secret/PII; persistence-capture if any table; abuse guard proven-or-declared-deferred; CI exit 0; Gate CLOSED. (If UI added: browser shots present.)

- A single CRITICAL (any execution/order/account/broker/open-gate endpoint present or reachable; any unauthenticated data exposure; any cross-operator leakage; any secret/PII leak; any Gate reach) ⇒ **WITHHELD.**
- A null-token scoping probe (R7 non-result) or a passing-test-without-the-named-raw-query where the BO names it ⇒ **CONDITIONAL** (W7-U02/U03 C-1 lessons).
- Every *risk* item proven but a *named* proof missing ⇒ **CONDITIONAL** (→ `_FINAL` on closure).

On approval: platform bump to **v0.58.0**; head `20260717_0037` (or `20260717_0038` if a catalogue table is persisted); onboarding updated; W7-U05 (Plugin Contract Safety Foundation — R7-1: contracts + refusal only, no dynamic execution) becomes next authorizable.

---

## 7. Reminders to DA

- **The catalogue documents the research API — it must never document or expose an execution endpoint.** Prove no-execution-surface by absence (404/405) + the catalogue's own `actuation_surface_present:false`.
- Auth on every catalogued route (401 unauth); operator scoping preserved (valid-token harness); authorize-before-validate on any mutation.
- No secrets/PII in catalogue responses (§77). Declare any rate-limit/API dependency + spike. State whether a table and/or UI is added; if so, persistence-capture / browser evidence apply.
- Verify the pack is OF W7-U04; verify probe tokens (LOGIN 200 + non-empty) before trusting status codes (W7-U02 lesson).

---

*We don't guess. We prove.*
**— AXIOM ITRGA**
