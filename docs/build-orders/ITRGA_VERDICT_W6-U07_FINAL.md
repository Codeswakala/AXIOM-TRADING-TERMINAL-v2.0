# ITRGA VERDICT — W6-U07 FINAL (supersedes CONDITIONAL)

## Execution Research Workspace UI (first Wave-6 UI)

**From:** AXIOM Independent Technical Review & Governance Authority (ITRGA)
**To:** Development Authority (DA), via Operator
**Unit:** W6-U07 (Wave 6)
**Supersedes:** `ITRGA_REVIEW_W6-U07.md` (CONDITIONAL APPROVAL, 2026-07-18)
**Correction pack reviewed:** `DELIVERY_REPORT_W6-U07_CORRECTION.md` + `operator results.md` (correction turn) + 4 screenshots
**Date:** 2026-07-18
**Verdict:** ✅ **APPROVED** — C-1 CLOSED-BY-WAIVER (operator-authorized), C-2 CLOSED (operator-authorized, auth-test sufficient). **Platform bumped v0.52.0 → v0.53.0.**
**Confidence:** HIGH. **Governance Gate:** CLOSED (re-verified). **Motto:** *We don't guess. We prove.*

---

## 0. Build-identity

`DELIVERY_REPORT_W6-U07_CORRECTION.md` cites `ITRGA_REVIEW_W6-U07.md` (CONDITIONAL), names C-1/C-2; operator pack is the correction rerun (`W6-U07_C1_LOCAL_CI_TRANSCRIPT.txt`). Genuinely OF the W6-U07 correction. ✔

---

## 1. C-1 — CLOSED BY WAIVER (operator-authorized)

The networked Git-Bash CI rerun **again exited `LOCAL_CI_EXIT_CODE: 1`** — root cause once more environmental: `npm audit` could not reach `registry.npmjs.org` (first submission: DNS `getaddrinfo ENOTFOUND`; this rerun: TLS `write EPROTO … wrong version number`, i.e. the advisory endpoint unreachable behind the network path). In both runs the substantive gates passed — **backend 345 passed**, frontend deps installed, build succeeds — and the DR's own online run reported `npm audit: found 0 vulnerabilities`. The failure is connectivity to the advisory endpoint, **not** a code failure and **not** a reported vulnerability.

**Operator decision (this turn): accept a documented environmental waiver.** C-1 is recorded **CLOSED-BY-WAIVER**:
- **Substitute proof (all green in the transcript):** backend **345 passed**, frontend **18 files / 58 tests**, TypeScript/build clean; prior online `npm audit: 0 vulnerabilities`.
- **Standing technical-debt item (TD-W6-CI-AUDIT):** re-run the documented Git-Bash CI on a network-reachable host to capture a clean `LOCAL_CI_EXIT_CODE: 0` (and/or make the audit step degrade gracefully when the registry is unreachable). Non-blocking, tracked.
- The red exit was **investigated and proven environmental, not relabeled green** — it is recorded here as a waiver with its root cause, consistent with the W4-U03 standing rule.

## 2. C-2 — CLOSED (operator-authorized; passing auth test sufficient)

The delivered logged-out screenshot is a login page **without a URL bar**, indistinguishable from opening `/login`; no operator-run unauth HTTP check (401/302→/login) was supplied. Route protection **is** proven at Level-I by the operator-run frontend test `ExecutionResearchWorkspace > requires auth via protected route and blocks logged-out access` (PASS), and `/execution-research` is a protected route in `App.tsx`.

**Operator decision (this turn): accept the passing auth test as sufficient** for this item, relaxing the GR6-10 browser-shot requirement **for C-2 only**. C-2 is **CLOSED**. (Standing GR6-10 remains in force for future UI units; this is a scoped, operator-authorized relaxation for W6-U07's logged-out item, where the underlying protection is independently test-proven.)

---

## 3. Envelope re-confirmed (from the CONDITIONAL, all Level-I)

- Frontend **18 files / 58 tests** incl. the 5 named W6-U07 tests (SIMULATED label; read-only artifacts; no exec controls; analytics uncertainty; auth/logged-out).
- Backend **345 passed** unchanged (no regression); broker+safety suite **13 passed**; no new table/migration (head `20260717_0033`).
- No-actuation frontend grep clean; no barred dependency.
- **Browser (served `localhost:8000/execution-research`):** SIMULATED banner + not-live disclaimer; display-only ("no authoritative recomputation"); artifact cards (Runs 8 / Fills 10 / Ledger 7 / Risk 3 / Experiments 4 / Analytics 3); SIMULATED-labelled run/fill/ledger/risk detail; analytics `uncertainty` + `economic usefulness: not_assessed` + `not_real_p_and_l`; **no execution/actuation controls** on any surface.
- Gate CLOSED (backend test + broker suite + UI states Gate CLOSED).

---

## 4. Observations (non-blocking)

- **OBS-1 (accuracy):** the correction report §2 states a clean `LOCAL_CI_EXIT_CODE: 0` was captured, but the transcript shows **exit 1**. Recorded for honesty — the disposition is the operator-authorized waiver (C-1), not the claimed exit-0. DA should not report an exit code it did not capture.
- **OBS-2:** TD-W6-CI-AUDIT carried forward (networked CI audit exit-0). Non-blocking.

---

## 5. Verdict

**W6-U07 is APPROVED.** The first Wave-6 UI is proven in the browser: a served, SIMULATED-framed, display-only Execution Research Workspace over the six persisted simulated artifact types, with no execution/actuation controls, analytics honest about uncertainty and `not_assessed` economics, and the Governance Gate CLOSED. C-1 (CI exit) is CLOSED-BY-WAIVER as a twice-proven environmental limitation; C-2 (logged-out) is CLOSED on the passing operator-run auth test — both per operator authorization this turn.

- **Platform of record: v0.52.0 → v0.53.0.**
- **Alembic head: `20260717_0033` (unchanged).**
- **Baselines: backend 345 passed · frontend 18 files / 58 tests.**
- **Carried non-blocking:** TD-W6-CI-AUDIT (networked CI `npm audit` exit-0).

**Next:** on operator authorization, `BUILD_ORDER_W6-U08.md` — **Wave-6 Closeout & Hardening** (the last unit): full-wave no-live-execution grep, Gate-CLOSED proof, artifact no-orphan completeness across all six W6 tables, browser E2E, docs/register reconciliation → milestone **"Execution Research Environment Complete."**

---

## 6. Posture note

The DA closed the substantive UI proof in the browser; the two residual items were evidence-form gaps whose underlying properties were independently proven (env-flake CI; test-proven route protection). Dispositioned by operator authorization, with the CI red recorded — not relabeled — and a TD carried. Built correctly and proven correctly.

---

*We don't guess. We prove.*
**— AXIOM ITRGA**
