# AXIOM ITRGA — REVIEW: W1-U01 (Core Platform: Service Architecture & API Hardening)

**Authority:** ITRGA · **Build Order:** `BUILD_ORDER_W1-U01.md` · **Delivery Report:** `DELIVERY_REPORT_W1-U01.md` (v0.9.0)
**Context:** First unit from a **newly-migrated Development Authority chat** — reviewed with heightened
scrutiny for governance-baseline drift, Wave-0 regression, and evidence authenticity.
**Evidence tier:** Delivery report only. **No operator-run target-platform evidence; no source inspected.**
**Date:** 2026-07-12 · **Standard:** `09_ITRGA_REASONING_FRAMEWORK` / `ITRGA_REVIEWER_ONBOARDING` (R1–R21).

---

## VERDICT: **PASS WITH OBSERVATIONS — CONDITIONAL. APPROVAL WITHHELD.**

The *implementation* is strong, correctly scoped, and governance-clean, and the new DA clearly inherited
the standard (canonical docs cited, no self-approval, honest about limits). **But the Build Order's
mandatory evidence set (§5) is essentially unmet:** every result is either **DA-sandbox (Level II)** or
**asserted (Level III)** — there is **no operator-run evidence on the target platform (Windows +
PostgreSQL)**, no auth transcript, no UTC output, no parity smoke. Under R3/R5/R9 that caps the verdict
below APPROVED. There is also **one genuine data-correctness design concern** (C-1). This is not a FAIL —
no CRITICAL defect is visible — but it cannot be approved on this evidence.

---

## 1. WHAT IS GENUINELY GOOD (credited — documentary/Level II)

- **Scope & governance discipline:** no execution/broker connection, no ML product, no chart expansion;
  MT5 untouched. Canonical `05 v2.0` cited; advisory-first preserved. Correct.
- **Component B (endpoint auth) substance is right:** operational endpoints (`/system/info`,
  `/persistence/*`, `/ingestion/*`, `/market/live/*`) → Bearer; **`/ws/status` → ticket** (closing
  TD-003); a minimal, defensible public set (`/health`, `/ready`, `/api`, `/auth/login`, `/auth/refresh`);
  a delivered **endpoint-auth inventory**. This is the correct hardening design.
- **Frontend kept in parity** (Bearer on system/candles; ws-ticket for status) — shows regression
  awareness.
- **Security hygiene:** removed the `admin/admin123` prefill; `run_dev.sh` no longer prints creds. Good.
- **Layering (A/D):** `PersistenceService` + thin controllers + repository→service→API aligns with
  05 v2.0 §11.2/§23. ADR-015/016 authored; registers synced; PG/CI limitation disclosed honestly.
- **Test growth 67→74 (+7)** is consistent with the new endpoint-auth + UTC suites.

The design would likely approve — *once proven on the target platform.*

---

## 2. THE BLOCKING FINDING

### F-1 (HIGH — mandatory evidence unmet) — no operator-run target-platform evidence
Build Order §5 makes operator-run evidence on the target platform **mandatory for approval**. What was
supplied is **DA-sandbox** or **asserted**, not operator Level-I:

| §5 required (mandatory) | Supplied | Status |
|---|---|---|
| Operator `pytest`/`vitest`/`tsc` console (raw, `collected N`, no regression) | DA-sandbox run: `74 passed` / `16 passed`. Commands are **bash/Linux env** (`python3 -m pytest`, inline `AXIOM_*=`), **not** the operator's Windows/PowerShell | ⚠️ **Level II only — MANDATORY item UNMET** |
| Endpoint-auth transcript (401 without / 200 with, incl `/ws/status`) | Asserted (`test_endpoint_auth.py` exists); **no transcript** | ❌ MISSING |
| tz-aware UTC evidence (query/response or test output) | Asserted (`test_time_utc.py`); **no output shown** | ❌ MISSING |
| CI green run **or** documented local equivalent | Alembic local **SQLite** equivalent → `head 0004` + ruff. Explicitly **no Postgres, no GitHub** | ⚠️ PARTIAL (SQLite, not the canonical PG path) |
| Parity smoke (login → chart/live → WS ticket 200) | Asserted in §6; **no runtime evidence** | ❌ MISSING |

This is the exact failure mode the standard exists to prevent (R1/R3/R4/R16). It is **more** important
this round, not less: a **fresh DA chat** means the code path has never been exercised on the operator's
actual machine under this DA. "74 tests pass in a Linux sandbox" does not establish that the newly
auth-locked endpoints, the ws-ticket-for-`/ws/status`, and the UTC changes behave correctly on
Windows+PostgreSQL — which is precisely where Wave-0 previously surfaced a genuine regression (the U08
ws-ticket 500 that passing tests missed).

### F-2 (MEDIUM — data-correctness design concern) — `ensure_utc()` silently coerces naive→UTC
DR §3.3: *"`ensure_utc()` treats naive datetimes as UTC for compatibility."* Build Order Component C
required tz-aware UTC **end-to-end** — i.e., eliminate naive datetimes, not *assume* them. Silently
coercing naive→UTC **masks** the very bug it's meant to fix: if any layer still produces a naive
timestamp (or a non-UTC local time mislabeled as UTC), this hides it rather than failing loudly. For a
platform heading into Wave-2 ML, a mislabeled timestamp is a **leakage/label-alignment hazard** (R18).
**Required:** at trusted internal boundaries (ingestion, candle storage, labels), naive datetimes should
be **rejected or explicitly logged**, not silently assumed UTC; reserve lenient coercion for external
inputs only, with the assumption recorded. Provide the `test_time_utc.py` output so I can see what's
actually asserted.

### F-3 (LOW — self-assessment overclaim) — confidence overstated
DR §10 rates "Backend correctness HIGH" and "Security hardening HIGH." With **zero operator-run
target-platform evidence**, the defensible rating is **LIMITED–MODERATE** on those dimensions. Rating
unproven-on-target work "HIGH" is the overconfidence `09_ITRGA_REASONING_FRAMEWORK` explicitly warns
against. (The report did correctly avoid percentages — credit — but the tier is still inflated.)

### F-4 (LOW — migration integrity, note) — DA re-created ITRGA documents in its own workspace
The DA created its own copies of `ITRGA_WAVE0_CLOSURE.md` and `BUILD_ORDER_W1-U01.md` under
`docs/build-orders/`. That's normal workspace hygiene, but I did not author those copies and cannot see
them. Confirm they are verbatim to the ITRGA originals (no drift introduced during migration). Non-blocking.

---

## 3. REQUIRED CORRECTIONS (to convert to APPROVED)

- **C-1 (F-1) — Supply operator-run evidence on the target platform (Windows/PowerShell + PostgreSQL):**
  (a) raw `pytest`/`vitest`/`tsc` console with `collected N`, no regression from 67/16; (b) an
  **endpoint-auth transcript** — the previously-public endpoints returning **401 without token / 200 with**,
  and **`/ws/status` rejecting unauthenticated / accepting ticket**; (c) the **`test_time_utc.py` output**;
  (d) a **parity smoke** (login → chart + live feed → `WS-TICKET 200`) proving no Wave-0 regression;
  (e) the **PostgreSQL** `alembic upgrade head` (you have Docker now — the SQLite equivalent is no longer
  the only option) and, ideally, the still-owed **green CI run** (Wave-0 carryover C-4b).
- **C-2 (F-2) — Harden `ensure_utc` at trusted boundaries:** reject/log naive datetimes at
  ingestion/candle/label boundaries rather than silently assuming UTC; keep lenient coercion for external
  inputs only, with the assumption documented. Provide evidence (test) of the stricter behavior.
- **C-3 (F-3) — Re-state confidence** at the evidence-justified tier once C-1 lands.
- **C-4 (F-4) — Confirm** the DA's copies of the ITRGA closure/Build-Order docs are unaltered.

## 4. RECOMMENDATIONS (non-blocking)
- Add an **integration/E2E smoke** in CI that exercises auth-gated endpoints end-to-end (the U08 lesson:
  unit tests passed while a live endpoint 500'd; the same risk applies to newly auth-locked routes).
- When `/ws/status` moved to ticket-auth, confirm the dashboard status socket still connects on the
  operator's machine (this is a likely regression point — include it in the parity smoke).

## 5. DISPOSITION
**W1-U01: PASS WITH OBSERVATIONS — CONDITIONAL. Not approved. No next Build Order.** The implementation
is sound and correctly scoped; approval is withheld solely because the **mandatory operator-run
target-platform evidence is absent** (F-1) and one **data-correctness concern** (F-2) must be resolved.
These are small to close given Docker is now available. Supply C-1 (esp. the auth transcript, UTC output,
parity smoke, and a PostgreSQL migration) and reconcile C-2, and I will approve promptly.

**Standing note for the new DA:** you inherited the standard well (canonical citations, honest limits, no
self-approval). The one habit to correct: **a delivery is "ready for ITRGA" only when operator-run,
target-platform evidence is attached** — not when the sandbox suite is green. Sandbox green is necessary,
never sufficient.

---

## EVIDENCE CONFIDENCE STATEMENT
- **Evidence Reviewed:** `DELIVERY_REPORT_W1-U01.md` (DA-sandbox test results, Alembic-on-SQLite,
  ruff, asserted auth/UTC/parity). Cross-checked vs `BUILD_ORDER_W1-U01.md`, 05 v2.0, and Wave-0 history.
- **Confidence Level:** **MODERATE** on the *design/implementation intent*; **LIMITED** on runtime
  correctness on the target platform (no operator Level-I evidence; source not inspected). No approval
  rests on report-claims.
- **Remaining Unknowns:** behavior on Windows+PostgreSQL; actual 401/200 auth behavior; UTC test output;
  whether `/ws/status` ticket-auth regressed the dashboard socket; PG migration of current head; CI run;
  the `ensure_utc` boundary strictness; integrity of the DA's copied ITRGA docs.
- **Additional Evidence Required:** C-1 (operator target-platform evidence set), C-2 (UTC strictness),
  C-4 (doc-copy integrity).

---

*"A fresh chat, a strong build — and zero proof on the operator's own machine. Sandbox-green is not
target-proven, and 'assume naive is UTC' is a bug in waiting for an ML platform. Bring the Windows +
Postgres console, the 401/200 transcript, and the parity smoke, tighten the UTC boundary, and this
approves. We don't guess. We prove."*
— AXIOM ITRGA
