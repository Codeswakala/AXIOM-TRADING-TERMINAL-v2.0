# ITRGA VERDICT — W7-U02 FINAL (supersedes CONDITIONAL)

## Operator Workspace Customization

**From:** AXIOM Independent Technical Review & Governance Authority (ITRGA)
**To:** Development Authority (DA), via Operator
**Unit:** W7-U02 (Wave 7)
**Supersedes:** `ITRGA_REVIEW_W7-U02.md` (CONDITIONAL APPROVAL, 2026-07-18)
**Correction pack reviewed:** `operator results.md` (C-1 isolation re-run)
**Date:** 2026-07-18
**Verdict:** ✅ **APPROVED** — C-1 CLOSED at Level-I (valid two-operator isolation, 0 leakage, no mutation). **Platform v0.55.0 → v0.56.0.**
**Confidence:** HIGH. **Governance Gate:** CLOSED. **Motto:** *We don't guess. We prove.*

---

## 0. Build-identity

Correction pack opens with W7-U02 C-1 artifacts (`W7-U02_C1_CORRECTION_COMMANDS.md`, institutional route with a new `"Cross-operator workspace preference access denied"` guard). Genuinely OF the W7-U02 C-1 correction. ✔

---

## 1. C-1 — CLOSED ✅ (two-operator isolation, valid tokens, raw ground-truth)

The re-run fixed the prior broken probe (unset login vars). This time **both logins succeed with non-empty tokens** (the harness guards + throws on any wrong status), and the isolation is proven:

- `LOGIN_A_STATUS: 200`, `LOGIN_B_STATUS: 200`, `TOKEN_A_PRESENT`/`TOKEN_B_PRESENT` true;
- `A_READ_A_PREF_STATUS: 200` (owner reads own) · `B_READ_B_PREF_STATUS: 200` (owner reads own);
- **`B_READ_A_PREF_STATUS: 403`** — B cannot read A's preference;
- **`B_LIST_STATUS: 200` with `B_VISIBLE_A_PREF_COUNT: 0`** / `B_VISIBLE_B_PREF_COUNT: 1` — B's list leaks none of A's rows;
- **`B_WRITE_A_PREF_STATUS: 403`** (run 1) — B cannot write A's preference.

**Raw DB ground-truth (authoritative):**
- `operator_distinct_count = 2` — A and B are real, distinct operators;
- **`raw_b_rows_for_a_preference = 0`** — B owns zero of A's preference rows;
- the two preference rows show A owns `operator-a-proof` and B owns `operator-b-proof`, and **A's row is unchanged** (B's attempted update payload did not land).

Consolidated re-run: **`23 passed`** (`test_workspace_preferences.py` + `test_institutional_platform_security.py` + `test_broker_integration.py`), `ruff` clean. The prior misleading `200`/`count 1` (from the null-token probe) is fully explained and superseded.

---

## 2. Observation (non-blocking)

- **OBS-1 (defense ordering, not a security defect):** a second run recorded `B_WRITE_A_PREF_STATUS: 422` (instead of 403) and the harness correctly **threw** — because that PUT's body failed **validation before the ownership check executed**, so it returned 422 rather than 403. In **both** runs B's write was **rejected and changed nothing** (raw DB: A's row untouched, `raw_b_rows_for_a_preference = 0`). This is a minor ordering nuance (validate-then-authorize on the PUT); the isolation property holds either way. **Recommendation (carry to W7-U03/U07 or a small hardening):** run the ownership/authorization check **before** body validation on mutation endpoints so a cross-operator write returns **403** deterministically regardless of payload. Non-blocking — no data leak or mutation occurred.

---

## 3. Envelope re-confirmed (from the CONDITIONAL)

Feature proven Level-I: 6/6 named backend tests; migration `0033→0034`; persistence-capture (no-orphan audit JOIN 0, operator JOIN 0); forbidden-column `information_schema` **(0 rows)**; `stored_secret_marker_count 0`; presentation-only (no action/order/account/execution field or control; "AXIOM does not act" banner); auth-required; browser E2E (workspace UI, no actuation controls, login); CI `LOCAL_CI_EXIT_CODE: 0` (npm audit 0 vulns); Gate CLOSED. Backend **366 passed** / frontend **19 files / 61 tests** at first submission.

---

## 4. Verdict

**W7-U02 is APPROVED.** Operator Workspace Customization is proven: per-operator, presentation-only, audited, no-orphan, no forbidden columns, no secrets — and **operator isolation is proven at the API level with valid distinct tokens (403 cross-read, 0 list leakage, no cross-write mutation) corroborated by raw DB ground-truth.** Gate CLOSED.

- **Platform of record: v0.55.0 → v0.56.0.**
- **Alembic head: `20260717_0033` → `20260717_0034`.**
- **Baselines: backend 366 passed · frontend 19 files / 61 tests.**
- **Carried non-blocking:** OBS-1 (validate-vs-authorize ordering on mutation PUT → 422 vs 403); TD-W6-CI-AUDIT (standing).

**Next:** on operator authorization, `BUILD_ORDER_W7-U03.md` — *Research Management Collections & Tags* (`research_collections`, `research_collection_members`, `research_tags`): organize existing governed artifacts, **no mutation of source artifacts** (R7-5 before/after identity proof), operator-scoped isolation (apply the corrected two-operator harness), persistence-capture, no-secret/PII.

---

## 5. Posture note

The DA closed the isolation proof cleanly once the probe used real tokens — and provided raw DB ground-truth (B owns 0 of A's rows; A's row unchanged) that settles it beyond the status codes. The 422-vs-403 write nuance was surfaced honestly by the DA's own throwing harness and is carried as a non-blocking hardening note. Built correctly and proven correctly.

---

*We don't guess. We prove.*
**— AXIOM ITRGA**
