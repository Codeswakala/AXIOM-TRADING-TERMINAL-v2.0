# BUILD ORDER — W7-U07

## Enterprise Scalability & Multi-User Readiness Hardening

**From:** AXIOM Independent Technical Review & Governance Authority (ITRGA)
**To:** Development Authority (DA), via Operator
**Wave:** 7 — Institutional Platform · **Unit:** W7-U07 · **Policy:** one unit per Build Order
**Date:** 2026-07-19
**Platform of record (pre-unit):** v0.60.0 · Alembic head `20260717_0037` · backend **399 passed** · frontend **21 files / 67 tests**
**Governing docs:** accepted `WAVE7_ENGINEERING_DESIGN_AND_IMPLEMENTATION_PLAN.md` §2 (Enterprise scalability / Multi-user readiness) + §10 (standing security debt); `ITRGA_REVIEW_WAVE7_DESIGN_PLAN.md` (**R7-4 default-deny RBAC, R7-6 admin/admin123, R7-7**, GR7-5/GR7-7/GR7-8); `ITRGA_VERDICT_W7-U01_FINAL.md` (RBAC/isolation foundation); §68 Scalability; §77 no secrets in telemetry.
**Constitutional posture:** Governance Gate **CLOSED**. Hardening/readiness only — **no scale/perf feature may weaken auth, audit, redaction, or the Gate; no role may open the Gate or reach execution.**
**Motto:** *We don't guess. We prove.*

---

## 1. Purpose

Consolidate the institutional platform's **security readiness at scale** before closeout: re-prove **default-deny RBAC + two-operator isolation** across the now-larger surface, prove **enterprise scalability/observability does not weaken audit/Gate/redaction**, and **dispose the two carried items** — the **deferred abuse/rate guard** (W7-U04) and **`admin/admin123`** (R7-6). No new *feature* capability; a hardening/readiness unit.

---

## 2. Scope (build/prove exactly this)

1. **Multi-user readiness re-proof:** default-deny RBAC re-confirmed across institutional/research routes; **two-operator isolation** re-proven at the API level (valid tokens) on ≥2 representative operator-scoped resources; no role can open the Gate or reach execution (permission-vocabulary re-check).
2. **Abuse/rate guard (dispose W7-U04 defer):** either **implement** a rate/abuse guard on representative institutional routes (prove Nth request → **429**) **or** formally **defer** it with a named standing TD + rationale. State which.
3. **`admin/admin123` disposition (R7-6):** either **prove** the default credential is **rejected when the insecure-dev flag is OFF** (production-framing rejection — a login attempt with `admin/admin123` under production config → 401/refused), **or** formally defer with a named standing TD + rationale. State which.
4. **Scalability/observability hardening:** any perf/caching/observability change must preserve auth, audit no-orphan, §77 redaction, and Gate closure — prove by regression + spot checks (no weakening).
5. **Optional table** (e.g. RBAC persistence or rate-limit state) → migration `20260717_0038` **only if persisted**; else no table (head `20260717_0037`). State which; persistence-capture applies if persisted.
6. No UI required (hardening unit); if any UI/config surface is added, GR7-10 browser evidence applies.

### FORBIDDEN (must remain ABSENT — prove)
- No role/permission that can **open the Gate or reach execution/order/account** (R7-4 vocabulary re-check → 0 forbidden verbs).
- No scale/observability change that logs secrets/PII (§77) or drops audit rows (no-orphan preserved).
- No weakening of auth (all institutional routes still 401 unauth) or Gate closure.

---

## 3. Binding refinements applied

- **R7-4 default-deny RBAC re-proof:** unprivileged operator denied (403); permission vocabulary contains no Gate/execution/order/account verb (re-checked at scale).
- **R7-3 / GR7-7 two-operator isolation (valid tokens):** B cannot read/list/mutate A's institutional/research resources (403/empty + 0 leakage) on ≥2 resource types; authorize-before-validate 403.
- **R7-6 admin/admin123:** production-framing rejection proven (insecure-dev flag OFF → default credential refused) **or** formally deferred (named TD + rationale). No silent production shipping.
- **Abuse/rate guard:** implemented-and-proven (429) **or** formally deferred (named TD). No silent omission.
- **§77 / GR7-8 redaction preserved:** structured logs + any new observability output carry no secrets/PII (marker check).
- **Audit integrity at scale:** no-orphan audit preserved (spot-check a representative table's no-orphan JOIN → 0 after any caching/scale change).
- **GR7-1 Gate CLOSED:** no role/scale feature reaches the Gate; `test_gate_remains_closed_for_wave7` + broker suite green.
- **GR7-12:** any scalability/rate-limit/observability dependency owes a spike + security/no-leak review + ITRGA note; broker SDK barred.

---

## 4. Mandatory tests (deliver names + raw PASS lines)

```
test_rbac_default_denies_unprivileged_operator_at_scale
test_rbac_permission_vocabulary_excludes_gate_execution_account_capability
test_multi_user_two_operator_isolation_across_institutional_resources
test_authorize_before_validate_cross_operator_mutation_403
test_admin_default_credential_rejected_when_insecure_dev_off        # R7-6 (or documented-defer variant)
test_abuse_or_rate_guard_enforced_or_documented_deferred            # rate guard
test_scalability_change_preserves_audit_redaction_and_gate_closed
test_no_secret_or_pii_in_observability_or_logs                      # §77
test_gate_remains_closed_for_wave7
```
Plus standing `test_broker_integration.py` green. Full backend regression ≥ **399** + new; frontend baseline ≥ **21 files** (report actual).

---

## 5. Mandatory evidence (operator-run on target — Level-I)

Deliver `DELIVERY_REPORT_W7-U07.md` + `operator results.md` (+ screenshots IF UI/config surface added), **inline**:

**(a) Build identity.** `Test-Path` new files + proof the pack is OF **W7-U07**; version `0.61.0`.
**(b) Test transcript.** Named tests + broker suite + full backend total.
**(c) Migration state.** `alembic current` = `20260717_0037` (or `0038` if a table persisted + revision file).
**(d) RBAC default-deny + vocabulary (R7-4).** unprivileged → **403**; permission vocabulary printed → no Gate/execution/order/account verb.
**(e) TWO-OPERATOR ISOLATION (R7-3, valid tokens).** `LOGIN_A/B 200` + tokens present; B→A read/list/mutate on ≥2 resource types → 403/empty + `B_VISIBLE_A_COUNT 0`; authorize-before-validate 403.
**(f) admin/admin123 (R7-6).** raw proof: with insecure-dev flag OFF, login `admin/admin123` → **401/refused** (production-framing rejection); OR a formal defer statement + named TD.
**(g) Abuse/rate guard.** raw proof of enforcement (Nth request → **429**) OR a formal defer statement + named TD.
**(h) §77 redaction / no-secret.** marker check over logs/observability output → clean.
**(i) Audit integrity at scale.** a representative no-orphan audit JOIN → **0** (preserved after any scale change).
**(j) Persistence-capture (IF table).** raw SELECT + no-orphan audit JOIN → 0 (+ operator JOIN if scoped) + forbidden-column `information_schema` → 0 rows.
**(k) No barred dependency.** grep empty; declare + spike any scalability/rate-limit/observability dep (GR7-12).
**(l) CI (GR7-11).** Git-Bash → `==> Local CI equivalent complete` + `LOCAL_CI_EXIT_CODE: 0`.
**(m) Gate-closed proof.** named test PASS + broker suite green.

---

## 6. Acceptance criteria

APPROVED requires ALL applicable of (a)–(m); named tests + broker suite green; regression green; **RBAC default-deny + no Gate/execution verb**; **two-operator isolation + 0 leakage (valid tokens, ≥2 resources)**; **admin/admin123 production-rejection proven OR formally deferred (named TD)**; **abuse/rate guard enforced (429) OR formally deferred (named TD)**; §77 redaction clean; audit no-orphan preserved; persistence-capture if table; CI exit 0 (or waive per TD-W6-CI-AUDIT if offline-npm-audit recurs); Gate CLOSED.

- A single CRITICAL (any role/scale feature that can open the Gate or reach execution; any cross-operator leakage; any secret/PII in logs; any dropped/orphaned audit; auth weakened) ⇒ **WITHHELD.**
- A null-token isolation probe, or a named raw proof present only as a passing test where the BO names the raw form, ⇒ **CONDITIONAL** (W7-U02/U03/U04 lessons).

On approval: platform bump to **v0.61.0**; head `20260717_0037` (or `0038` if a table persisted); onboarding updated; **W7-U08 (Wave-7 Closeout & Platform Completion — R7-8: whole-project completion checkpoint → milestone "Institutional Platform Complete")** becomes the final authorizable unit.

---

## 7. Reminders to DA

- Hardening/readiness only — **no scale/perf feature may weaken auth, audit, redaction, or the Gate; no role may reach the Gate or execution.**
- **Dispose both carried items explicitly:** admin/admin123 (prove rejection or defer w/ TD) and abuse/rate guard (implement+429 or defer w/ TD) — no silent omission.
- Two-operator isolation with the valid-token harness (verify LOGIN 200 + non-empty token first). State whether a table/UI is added.
- Capture the CI exit-0 fully this time (W7-U06 truncation lesson). Verify the pack is OF W7-U07; state dep changes accurately.

---

*We don't guess. We prove.*
**— AXIOM ITRGA**
