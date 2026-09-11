# AXIOM BUILD ORDER — W3-U08

## Live Research Advisor: Wave-3 Closeout & Hardening (the LAST Wave-3 unit)

**Build Order ID:** W3-U08
**Wave:** 3 — Live Research Advisor · **Unit:** 08 (FINAL)
**Version:** 1.0 · **Status:** ISSUED
**Authority:** ITRGA · **Date Issued:** 2026-07-16
**Authorized By:** ITRGA, following **W3-U07 APPROVED — CLEAN** (Platform v0.29.0; analytics/confidence viz,
uncertainty-mandatory, raw-score provably stripped) + operator authorization ("authorized").

**Governing Documents (canonical order — `10_CONSTITUTIONAL_HIERARCHY`):**
`00_VISION` → `03_AXIOM_SPEC` → `04_PROJECT_ROADMAP` (Tier 3) → **`05_SYSTEM_ARCHITECTURE` v2.0 (Tier 4)**
→ **`07_ML_SPEC` (Tier 5)** → `07_UI_UX_SPEC` → `08/09` frameworks → Tier-7 registers → this Build Order.
**Binding decision:** `docs/ITRGA_WAVE2_GOVERNANCE_DECISION_LOG.md` (D-W2-001, Option A).
**Governing plan:** `WAVE3_ENGINEERING_DESIGN_AND_IMPLEMENTATION_PLAN.md` §13 (W3-U08 line: *security,
evidence, docs, browser E2E, signal audit completeness, no-execution proof*) + §11 bright-line + §15 risks.
**Closes:** Wave 3 (Live Research Advisor) — W3-U01…U08.
**Motto:** *We don't guess. We prove.*

---

## 1. Purpose

W3-U08 is a **closeout & hardening** unit, not a new feature. Its job is to **prove — end to end, on the
target — that the whole Wave-3 advisory pipeline is safe, complete, audited, and honest**, and to leave the
codebase, docs, and governance registers in a clean, reconciled state so ITRGA can declare the
**"Professional Advisor Platform Complete"** milestone.

Concretely, W3-U08 must demonstrate that the assembled system (live inference → governed eligibility gate →
advisory-status lifecycle → signal contract/persistence → emit-time guardrails → live-market adapter →
operator advisory UI → monitoring/drift/health alerts → performance analytics/confidence viz) works together
and that **nothing in that chain can execute, mutate what it watches, emit an order, open the Governance Gate,
or present research as a guarantee.** This is the unit where we stop adding surface and instead **prove the
bright line holds across the entire wave.**

**No new user-facing capability is authorized.** If a genuine hardening fix is required (e.g. tighten an
auth check, add a missing audit event, close a small gap found during E2E), it is in-scope **as a hardening
correction** and must be called out explicitly with before/after evidence — it is not a licence to build W4+
features, execution, brokers, or the gate.

---

## 2. Governance Envelope (READ FIRST — violation = automatic FAIL)

- ❌ **No execution / no broker / no order path anywhere in the platform.** This is the keystone closeout
  proof. A **wave-wide structural grep** (backend + frontend) for execution/mutation patterns must return
  **command + empty output** (R7). Grep must include, at minimum:
  `place_order|cancel_order|submit_order|order_payload|\bexecute\b|\bbuy\b|\bsell\b|\bposition\b|broker\.|paper.?trade|auto_retrain|retrain_triggered\s*=\s*True|model\.status\s*=|advisory_status\s*=|remediation_payload`.
- ❌ **No opening of the Constitutional Governance Gate (05 v2.0 §15).** The gate stays CLOSED; the flow
  remains Recommendation → Operator Decision → (CLOSED Gate) → Future Broker Execution. Prove structurally
  (no gate-open/execution-enable code path).
- ❌ **No research shown as guaranteed/expected/promised return** (R-3). Every advisory/analytics surface
  keeps its advisory-research labelling + uncertainty. Prove by browser E2E screenshots across the surfaces.
- ❌ **No un-audited signal / no un-audited alert.** Every emitted/persisted advisory signal and every
  monitoring alert must have a corresponding **immutable audit event**. Prove by `psql` join/count.
- ❌ **No client-side authoritative recompute** (§30/§11.1/§3.4) — UI stays presentation-only.
- ❌ **No unauthenticated access; no secrets/PII in payloads or telemetry** (§77). All operator surfaces and
  read APIs require auth; logged-out access is blocked. Prove: unauth → 401 across the Wave-3 read endpoints;
  a browser logged-out attempt on an operator route is blocked.
- ❌ **No regression.** FULL suite green (Wave-0/1 + W2 + W3-U01…U07) — 0 failed — plus **green CI
  (capture the `LOCAL_CI_EXIT_CODE: 0` echo inline this time — the standing LOW, please close it at closeout)**
  and parity smoke. A red/failing test is a finding, not a footnote (R1/R12).
- ❌ **No silent scope creep / no new migration unless a hardening fix genuinely requires one** (and if so,
  justify + show the `psql SELECT ≥1 row` on the correct table per the persistence-capture control).
- ✅ **Preserve:** advisory/research-first, UX presentation-only, tz-UTC display, market-agnostic (D-W2-001
  Option A), all prior hardening, npm-audit 0 high/critical, ruff/tsc clean.

**Any single violation of the ❌ list ⇒ APPROVAL WITHHELD.**

---

## 3. Scope (Components A–F)

### A. Full-wave regression & CI (the "nothing broke assembling it" proof)
- Full backend `pytest` and full frontend `vitest` green, 0 failed. **Baseline to meet or exceed: backend
  192 / frontend 10 files / 24 tests** (W3-U07). Report exact totals.
- `local_ci.sh` via Git Bash → `==> Local CI equivalent complete` **and** an inline
  `LOCAL_CI_EXIT_CODE: 0` echo (close the standing LOW).
- ruff clean; `npm audit --audit-level=high` → 0; `tsc`/build clean.
- Alembic `upgrade head` + `alembic current` transcript (expected head `20260715_0018` unless a justified
  hardening migration is added).

### B. End-to-end browser proof of the advisory pipeline (MANDATORY — no approval without it)
From a **single running session** (backend + frontend up), capture browser screenshots that walk the whole
operator journey and show the bright line holding on screen:
1. **Login** and the terminal shell.
2. **Advisory Signals** surface — advisory disclaimer + distinct guardrail states (ADVISORY/WARNING/WITHHELD/
   EXPIRED); calibrated confidence shown, not raw score.
3. **Performance Analytics** surface — metrics with uncertainty (interval + sample count), the
   **"Confidence unreliable — calibration warning present."** band, disclaimer, no execution controls.
4. **Operator Alerts / monitoring** surface — an alert that informs, with no act/remediate control.
5. **No execution controls anywhere** — nav + each surface show no buy/sell/order/broker element.
6. **Logged-out block** — hitting an operator route while logged out is refused (not rendered).
   Each screenshot must show a reachable, served page (no `ERR_CONNECTION_REFUSED`). Replace/omit any stale
   unreachable capture (OBS from W3-U07).

### C. Signal & alert audit-trail completeness (the "everything is accountable" proof)
- Seed/emit a representative set of advisory signals (clean + guardrailed/withheld/expired) and at least one
  monitoring alert (drift/health) on the target.
- Prove via `psql`: (a) each persisted `advisory_signals` row has a matching immutable audit event;
  (b) each `monitoring_alerts` row has its `*.created` (and, where acknowledged, `*.acknowledged`) audit
  event; (c) show a `SELECT` with ≥1 row and the join/count that demonstrates **no orphan signal/alert**.
- Show the audit events are **immutable/append-only** (no update/delete path) and carry a correlation id.

### D. Wave-wide bright-line structural proof (the "it structurally cannot act" proof)
- Run the §2 execution/mutation grep over **all** of `backend/app` and `frontend/src` (state exclusions
  explicitly, e.g. test files / type-only files) — command **and** empty output.
- Confirm the schema carries **no** order/execution/remediation columns and that alerts/signals are inert
  (structurally cannot carry a directive) — cite the relevant `\d` table output.
- Confirm the Governance Gate remains closed (no code path opens it / enables broker execution).

### E. Security & hardening review
- Confirm **all Wave-3 read endpoints require auth** (unauth → 401 table): analytics, alerts, signal history,
  live-market read-backs. Confirm write attempts on read-only endpoints → 405/404.
- Confirm no secrets/tokens/PII in any Wave-3 payload or log/telemetry (§77) — show a sanitized sample.
- Address any genuine gap found as an explicit **hardening correction** with before/after evidence. If none
  found, state that explicitly (a clean review is a valid result — but it must be a *result*, not silence).

### F. Documentation & governance reconciliation
- Update and reconcile: `README.md`, `PROJECT_STATE.md`, `CHANGELOG.md` (→ **v0.30.0** on closeout),
  `04_PROJECT_ROADMAP.md` (Wave-3 marked complete), `RISK_REGISTER.md`, `TECHNICAL_DEBT_REGISTER.md`
  (carry forward TD-063/TD-064 and the standing wheel-compat spike as still-owed by a future compiled-ML unit;
  do **not** silently close them), `GOVERNANCE_AMENDMENTS.md` (no amendment expected — Option A stands; state
  so).
- ADR: `ADR-038_Wave3_Closeout_and_Hardening.md` summarizing the closeout scope and the bright-line proof.
- Produce a concise **Wave-3 Closeout Evidence Index** mapping each W3 unit (U01…U08) to its approval verdict
  and its keystone safety proof, so the milestone rests on a single traceable page.

---

## 4. Required Evidence (operator-run on target — Windows/PowerShell + PostgreSQL)

Report `DELIVERY_REPORT_W3-U08.md` + raw `operator results.md`. Non-waivable, and **prove build identity
first** (the W3-U07 correction precedent): show the closeout artifacts exist (`Test-Path` the new
ADR/closeout-index) before the gates.

1. **Build identity**: `Test-Path` new closeout files; `git log -1 --oneline` (or equivalent) confirming the
   build under test is W3-U08.
2. **Full backend `pytest`** — total ≥ 192, 0 failed; **full frontend `vitest`** — 10 files / 24 tests (or
   higher if hardening added tests), 0 failed. Named, not just counts, for any new/changed tests.
3. **`local_ci.sh`** transcript with the completion marker **and** inline `LOCAL_CI_EXIT_CODE: 0`.
4. **Alembic** `upgrade head` + `alembic current`.
5. **Browser E2E screenshots** per §3.B (1–6), single running session, all pages reachable.
6. **Audit-trail `psql` proof** per §3.C — `SELECT` ≥1 row + no-orphan join/count for signals and alerts.
7. **Wave-wide grep** per §3.D — command + empty output (backend + frontend).
8. **Auth table** per §3.E — unauth 401 across Wave-3 read endpoints; read-only write → 405/404.
9. **Registers/docs diff summary** per §3.F — showing TD/risk items carried forward, roadmap Wave-3 complete,
   CHANGELOG → v0.30.0.
10. **Parity smoke** (ws-ticket 200, persist_errors 0) as in prior closeouts.

---

## 5. Acceptance Criteria (ITRGA will verify line-by-line)

- [ ] Build identity proven; full suite green (≥192 backend / 10 files·24 tests frontend), 0 failed; CI marker
      **+ inline `LOCAL_CI_EXIT_CODE: 0`**; ruff/tsc clean; npm audit 0; parity smoke clean.
- [ ] End-to-end browser evidence (§3.B 1–6) — every advisory/analytics/alert surface shown reachable,
      advisory-labelled, with uncertainty/calibration honesty, and **no execution controls**; logged-out
      route blocked.
- [ ] Signal & alert **audit completeness** proven (§3.C) — no orphan; immutable/append-only; correlation id.
- [ ] Wave-wide **bright-line grep** empty (command + output) + inert-schema citation + gate-closed proof.
- [ ] Security review (§3.E) — auth 401 table; read-only 405/404; no secrets/PII; hardening findings (if any)
      fixed with before/after evidence, or an explicit "no gap found" result.
- [ ] Docs/registers reconciled (§3.F); ADR-038 + Wave-3 Closeout Evidence Index present; TD-063/TD-064 +
      wheel-compat spike carried forward (not silently closed); GOVERNANCE_AMENDMENTS confirms Option A stands.
- [ ] No regression across Wave-0/1/2 + W3-U01…U07.
- [ ] DA does **not** self-approve, self-advance the version, add execution/brokers, or open the Gate.

**A single CRITICAL, an unmet mandatory evidence item, or a red gate ⇒ APPROVAL WITHHELD.** On a clean pack,
ITRGA approves W3-U08, advances the platform to **v0.30.0**, and declares the **"Professional Advisor
Platform Complete"** milestone.

---

## 6. Out of Scope (do NOT build — automatic FAIL if present)

- Any execution/order/broker/paper-trade capability; opening the Governance Gate.
- Any Wave-4+ feature, external live-data provider connection, or per-market specialized model (would need a
  GOVERNANCE_AMENDMENTS amendment; D-W2-001 Option A stands).
- Auto-retrain / auto-remediation / any autonomy that acts rather than informs.
- New analytics metrics presented without uncertainty, or any surface implying guaranteed returns.

---

## 7. Notes to the Development Authority

W3-U08 is a **proof unit**: the deliverable is not new surface, it is **incontrovertible evidence that the
whole wave is safe and complete.** The strongest closeout you can submit mirrors the W3-U07 correction's
excellence — prove build identity first, make every claim data-driven and reproducible on target, show the
negative results as command + output (never a blank), and leave the docs/registers honestly reconciled. Please
finally capture the inline `LOCAL_CI_EXIT_CODE: 0` — closeout is the right place to retire that standing LOW.

DA does not self-approve, self-advance the version, begin any Wave-4 work, add execution/brokers, or open the
Gate. A new Build Order (or the milestone declaration) follows ITRGA's verdict.

> **We don't guess. We prove.** — ITRGA
