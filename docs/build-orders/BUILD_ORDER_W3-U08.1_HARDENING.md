# AXIOM BUILD ORDER — W3-U08.1 (Wave-3 Residual Hardening)

## Close-out the two W3-U08 observations so Wave 3 leaves ZERO residuals

**Build Order ID:** W3-U08.1 (hardening follow-up to the CLOSED Wave 3)
**Wave:** 3 — Live Research Advisor · **Unit:** 08.1 (residual hardening; no new capability)
**Version:** 1.0 · **Status:** ISSUED
**Authority:** ITRGA · **Date Issued:** 2026-07-16
**Authorized By:** ITRGA, following **W3-U08 APPROVED WITH OBSERVATIONS** (Wave 3 CLOSED; Platform v0.30.0;
"Professional Advisor Platform Complete" declared) + operator direction ("address W3-U08 observations first").

**Governing Documents:** `10_CONSTITUTIONAL_HIERARCHY` order as prior · **Binding decision:** D-W2-001
Option A · **Closes:** OBS-1 + OBS-2 from `ITRGA_VERDICT_W3-U08_FINAL_AND_WAVE3_CLOSURE.md`.
**Motto:** *We don't guess. We prove.*

---

## 1. Purpose

Wave 3 is closed and the milestone declared, but the closeout carried **two non-blocking observations.** For a
high-grade project "there is no room for error," so before Wave 4 opens we retire both — leaving Wave 3 with
**zero residuals.** This is a **hardening/test-infra + evidence-completeness unit only.** It introduces **no
new product capability, no schema, no execution/broker path, and does not touch the CLOSED Governance Gate.**

---

## 2. Governance Envelope (violation = automatic FAIL)

- ❌ No new feature, endpoint, UI capability, schema, or migration (a test-harness/config change is permitted;
  a product-behavior change is not).
- ❌ No execution/broker/order path; Gate stays CLOSED; no autonomy.
- ❌ No masking of the flake by weakening/deleting the assertion or `xfail`-ing it to hide the race — the fix
  must make the test **deterministically green for the right reason** (correct connection lifecycle), not
  silence it.
- ✅ Preserve all prior behavior; full suite still green; advisory/research-first intact.

---

## 3. Scope (two items only)

### Item 1 — Close OBS-1: make `local_ci.sh` (SQLite) deterministically green
Root cause (already diagnosed): `tests/test_live_market.py::test_live_start_stop_and_status` fails
intermittently under the SQLite `StaticPool` **single-connection** test harness with
`aiosqlite … no active connection` — a commit/teardown race between the request-scoped seed write and the
background live-adapter writer sharing one connection. It is green on PostgreSQL and in the direct run.
**Fix the test harness so the race cannot occur**, e.g. one of:
- give the background live-adapter writer its own connection/session in the test harness (not the shared
  `StaticPool` connection); **or**
- serialize the adapter writer against the request-scoped seed under `StaticPool`; **or**
- scope the SQLite connection per-test so teardown cannot invalidate an in-flight commit.
Choose the least-invasive option that keeps production/PostgreSQL behavior unchanged. Document the chosen fix
in a short note/ADR addendum.

### Item 2 — Close OBS-2: complete the Wave-3 browser E2E screenshot archive
Supply the **four browser screenshots not captured at closeout**, from a single served session
(`127.0.0.1:8000`, all pages reachable):
1. **Login** screen (and the authenticated terminal shell after login).
2. **Operator Alerts / Monitoring** surface showing the read-only `MonitoringAlertsPanel` — an alert
   displayed with **no acknowledge/remediate/execute control**.
3. **No-execution** confirmation on a representative surface (nav + page show no buy/sell/order/broker element).
4. **Logged-out block** — navigating to an operator route (e.g. `/analytics` or `/alerts`) while logged out is
   refused (redirect/401 page), not rendered.
(The /signals and /analytics shots from W3-U08 already satisfy the other two of the six.)

---

## 4. Required Evidence (operator-run on target)

Report `DELIVERY_REPORT_W3-U08.1.md` + raw `operator results.md`:
1. **Item 1 fix proof:** show the changed test-harness code (diff/snippet); then **run `local_ci.sh` and show
   `LOCAL_CI_EXIT_CODE: 0`** with `==> Local CI equivalent complete`. Re-run it (or run the specific test) a
   few times / with `-p no:randomly` disabled or repeated to demonstrate **stability, not luck** — the flake
   must not reappear. Confirm full backend `pytest` still **192 passed** on PostgreSQL and **0 failed** on
   SQLite CI.
2. **Item 2 proof:** the four browser screenshots per §3.2, all from a reachable served session.
3. Full frontend `vitest` still green (11 files / 25 tests or higher); ruff/tsc/build clean; npm audit 0.
4. No new migration (head `20260715_0018`); no product-behavior change (state it explicitly).
5. Docs: brief note/ADR addendum recording the OBS-1 fix; update CHANGELOG (patch, e.g. v0.30.1) and mark
   OBS-1/OBS-2 CLOSED in PROJECT_STATE.

---

## 5. Acceptance Criteria (ITRGA will verify line-by-line)

- [ ] `local_ci.sh` → **`LOCAL_CI_EXIT_CODE: 0`** (green) + completion marker; flake shown stable across
      repeats; the fix is a correct connection-lifecycle change, not a silenced assertion.
- [ ] Full suite still green on both PostgreSQL (192) and SQLite CI (0 failed); frontend green; audit 0.
- [ ] Four browser screenshots supplied (login+shell, alerts panel read-only, no-exec, logged-out block),
      all reachable-served → **OBS-2 CLOSED**.
- [ ] No new capability/schema/execution/gate change; docs/CHANGELOG updated; OBS-1/OBS-2 marked CLOSED.

On a clean pack, ITRGA marks **Wave 3 residual-free** and (per operator direction) proceeds to pre-register
the Wave-4 constitutional guardrails + request the Wave-4 Design Plan.

---

## 6. Notes to the DA

This is a small, surgical unit — the goal is a **deterministically green CI gate for the right reason** and a
**complete evidence archive**, nothing more. Do not expand scope. Fix the harness, not the product.

> **We don't guess. We prove.** — ITRGA
