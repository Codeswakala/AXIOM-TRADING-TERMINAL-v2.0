# ITRGA REVIEW — W7-U04

## API Ecosystem Catalogue & Versioned Research API Hardening

**From:** AXIOM Independent Technical Review & Governance Authority (ITRGA)
**To:** Development Authority (DA), via Operator
**Unit:** W7-U04 (Wave 7) · **Reviewed pack:** `DELIVERY_REPORT_W7-U04.md` + `operator results.md`
**Build Order:** `BUILD_ORDER_W7-U04.md`
**Review date:** 2026-07-18
**Platform of record (pre-unit):** v0.57.0 · head `20260717_0037` · backend 377 / frontend 20f·64t
**Verdict:** 🟡 **CONDITIONAL APPROVAL** — no-execution-surface + auth fully proven at API level; three named operator-run items are present only as passing tests + DR claims (C-1). **Version bump to v0.58.0 HELD.**
**Confidence:** HIGH. **Governance Gate:** CLOSED. **Motto:** *We don't guess. We prove.*

---

## 0. Build-identity check (done FIRST)

- `DELIVERY_REPORT_W7-U04.md`: Unit W7-U04, cites Build Order + W7-U03 FINAL; target v0.58.0, head `20260717_0037` **unchanged** (no catalogue table — generated approach, the preferred no-table path). ✔
- `operator results.md`: fresh pack (ADR-067, `api_catalogue.py`, `test_api_catalogue.py`); `ApiCataloguePage.tsx → False` (API-only, no UI — browser evidence correctly not required). ✔

---

## 1. What is PROVEN (Level-I)

| # | Requirement | Evidence | Result |
|---|---|---|---|
| b | Named tests | `test_api_catalogue.py` **6/6 PASSED** (incl. no-execution-endpoint, auth-required, no-secret, two-operator scoping, gate-closed) | ✅ |
| — | Full backend regression | **383 passed** (+6 over 377); broker suite green | ✅ |
| c | Migration state | `alembic current = 20260717_0037` unchanged; `CATALOGUE_TABLE_PERSISTED: False` (no table) | ✅ |
| d | **Catalogue + no-execution-surface (R7-2 CENTRAL, API-proven)** | `API_CATALOGUE_STATUS: 200`, `CATALOGUE_VERSION w7-u04.research_api_catalogue.v1`, **`ACTUATION_SURFACE_PRESENT: False`**, **`GOVERNANCE_GATE_CAPABILITY_PRESENT: False`**; **12 forbidden-endpoint probes** (execute/order/broker/account/open-gate/go-live at `/api/v1/` and `/api/v1/institutional-platform/`) all → **405** (self-throwing harness) | ✅ |
| e | Auth table (GR7-5) | api-catalogue / research-collections / research-tags / scenario-reports / signals-history all **UNAUTH 401 / AUTH 200** | ✅ |
| i | Abuse guard | `ABUSE_GUARD_STATUS: deferred` — **explicitly declared deferred** (BO-permitted for a catalogue unit) | ✅ (declared) |
| j | No barred dependency | "no dependency added"; no rate-limit lib | ✅ |
| k | CI (GR7-11) | `LOCAL_CI_EXIT_CODE: 0` | ✅ |
| m | Gate CLOSED | `test_gate_remains_closed_for_wave7` PASS; broker suite green; catalogue `governance_gate_capability_present: False` | ✅ |

**The central control — a research API catalogue with no execution surface — is fully proven at the API level** (12× 405 + `actuation_surface_present:false`), plus auth-gating across the catalogued routes.

---

## 2. CONDITION

### 🟡 C-1 — Three named §5 operator-run items are present only as passing pytest tests + DR claims (no operator-run API/grep evidence).
The Build Order §5(f)(g) named these as operator-run:
- **§5(f) two-operator scoping spot-check (valid tokens):** the operator pack **seeded** A/B + collections (distinct IDs `6c7c9da9…` / `cdb3b6f4…`) but contains **no operator-run API call** showing B (with B's token) reading A's collection → **403** (no such 403 outside the forbidden-probe/auth-table blocks).
- **§5(f) authorize-before-validate 403** for W7-U04's surface: not present as an operator-run probe.
- **§5(g) no-secret/PII response marker check:** no operator-run marker/grep output over the catalogue response.

All three are proven by **operator-run passing tests** (`test_api_surface_preserves_operator_scoping_two_operator`, `test_api_catalogue_response_has_no_secret_or_pii_markers` — Level-I via pytest on target) and **asserted** in the DR §7 index, but the **named standalone operator-run API/grep evidence is absent.** On this wave I have consistently required the operator-run API isolation/marker proof in addition to the unit test (W7-U02 C-1, W7-U03 C-1); §5(f)(g) named them. The DR §7 claim that they were delivered is a claim/evidence mismatch to correct.
**This is NOT evidence of a leak** (the scoping test passes; the seed exists) — but the named operator-run form is owed.
**To close C-1:** on target, with **valid distinct A/B tokens** (confirm `LOGIN 200` + non-empty token): (i) `B` GET `.../research-collections/<COLLECTION_A_ID>` → **403** and B's list shows 0 of A's rows; (ii) `B` mutate A's resource with empty body → **403** (authorize-before-validate); (iii) a marker/grep over the catalogue response → **no secret/PII**. Correct the DR §7 wording to match what was actually run.

---

## 3. Classification

- **C-1** — MEDIUM (three named operator-run proofs present only as passing tests + DR claims; consistent with the W7-U02/U03 standard requiring the operator-run API/grep form for isolation/no-leak).
- No CRITICAL, no HIGH. No-execution-surface (12× 405), auth (401/200), Gate CLOSED, no dep, CI green, head correct — all API-proven Level-I. Per proportionality (R13): every *risk* item proven (incl. scoping/no-secret by passing tests), the *named operator-run form* of three items missing ⇒ **CONDITIONAL**, not WITHHELD. **v0.58.0 HELD** (platform stays v0.57.0).

---

## 4. Not a finding / disclosed

- `ABUSE_GUARD_STATUS: deferred` is **acceptable and correctly declared** (the BO permitted defer-with-declaration for a catalogue unit) — not a finding; carry as a non-blocking note if a future unit hardens rate-limiting.
- No UI (`ApiCataloguePage.tsx → False`) → no browser evidence required; correct.
- No catalogue table persisted → no persistence-capture owed; correct (head 0037 unchanged).

---

## 5. Path to FINAL

On the C-1 operator-run rerun (valid-token B→A 403 + list-0 + authorize-before-validate 403 + no-secret marker) and the DR §7 wording correction, I will write `ITRGA_VERDICT_W7-U04_FINAL.md` superseding this CONDITIONAL, bump to **v0.58.0** (head `20260717_0037`), update onboarding, and W7-U05 (Plugin Contract Safety Foundation — R7-1: contracts + refusal only, no dynamic execution) becomes authorizable.

---

## 6. Posture note

Strong catalogue unit: the API surface is documented, authenticated, and — the point of the unit — **provably has no execution/order/account/broker/open-gate endpoint** (12× 405 + `actuation_surface_present:false`), with the abuse guard honestly declared deferred. The gap is purely the operator-run *form* of the scoping/no-secret proofs, which the tests already pass and the seed already sets up — close them with the valid-token harness (as at W7-U02/U03) and this unit is FINAL.

---

*We don't guess. We prove.*
**— AXIOM ITRGA**
