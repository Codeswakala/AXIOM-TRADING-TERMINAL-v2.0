# AXIOM BUILD ORDER — W4-U08

## Institutional Intelligence: Wave-4 Closeout & Hardening (the LAST Wave-4 unit — milestone gate)

**Build Order ID:** W4-U08
**Wave:** 4 — Institutional Intelligence · **Unit:** 08 (FINAL)
**Version:** 1.0 · **Status:** ISSUED
**Authority:** ITRGA · **Date Issued:** 2026-07-16
**Authorized By:** ITRGA, following **W4-U07 APPROVED WITH OBSERVATIONS** (Platform v0.37.0; dashboard proven in browser) + operator authorization ("authorized").

**Governing Documents (canonical order — `10_CONSTITUTIONAL_HIERARCHY`):**
`00_VISION` → `03_AXIOM_SPEC` → `04_PROJECT_ROADMAP` (Tier 3) → **`05_SYSTEM_ARCHITECTURE` v2.0 (Tier 4)**
→ **`07_ML_SPEC` (Tier 5)** → `07/08_UI_UX_SPEC` → `08/09` frameworks → Tier-7 registers → this Build Order.
**Binding decisions:** D-W2-001 **Option A**; Wave-4 guardrails **GR-1…GR-8**; refinements **R-1…R-8**.
**Governing plan:** `WAVE4_ENGINEERING_DESIGN_AND_IMPLEMENTATION_PLAN.md` §7/§8/§9 (W4-U08 = full-wave
no-execution proof, artifact-audit completeness, auth/read-only, docs reconciliation, milestone candidate).
**Closes:** Wave 4 (Institutional Intelligence) — W4-U01…U08. **Closes OBS-1** (W4-U07 interval-bounds render).
**Precedent:** W3-U08 (Wave-3 closeout — proof unit, not new surface).
**Baseline to meet/exceed:** backend **233** / frontend **12 files · 29 tests**; Platform **v0.37.0**; head
**20260716_0023**.
**Motto:** *We don't guess. We prove.*

---

## 1. Purpose

W4-U08 is a **closeout & hardening** unit, not a new feature. Its job is to **prove — end to end, on the
target — that the whole Institutional Intelligence layer is safe, complete, audited, honest, and still
research-only**, close the one open observation (OBS-1), reconcile docs/registers, and leave the codebase in a
clean state so ITRGA can declare the **"Institutional Intelligence Layer Complete"** milestone.

Concretely, prove that the five W4 report families (correlation, regime, scenario, portfolio-risk,
signal-validation) and the dashboard together **cannot execute, cannot open the Gate, cannot carry an order/
sizing/account/position/signal payload, and never present research as a guarantee**, and that **every W4
artifact is audited (no orphan).** This is the unit where the Wave-4 bright line is proven across the whole
wave.

**No new user-facing analytical capability is authorized.** The only permitted code change is the **OBS-1
hardening fix** (render the uncertainty interval bounds instead of "— to —") + any genuine closeout hardening,
each called out with before/after evidence.

---

## 2. Governance Envelope (READ FIRST — violation = automatic FAIL)

- ❌ **No execution / order / broker / account / position / sizing path anywhere across Wave 4.** Keystone
  closeout proof. A **wave-wide structural grep** (backend + frontend) must return **command + empty/benign
  output** (R7), including at minimum:
  `place_order|cancel_order|submit_order|order_payload|order_size|position_size|quantity|stop_loss|take_profit|broker_account|account_id|position_id|live_position|\bexecute\b|\bbuy\b|\bsell\b|broker\.|paper.?trade|auto_retrain|model\.status\s*=|advisory_status\s*=|remediation_payload|gate_open|allow_execution`.
  (Residuals limited to the artifact contracts' **forbidden-key lists** + established benign seams, each
  disclosed — the W4-U04/U05 standard.)
- ❌ **No opening of the Constitutional Governance Gate (05 v2.0 §15).** Gate stays CLOSED; broker gate tests
  pass; broker-seam grep empty.
- ❌ **No research shown as guaranteed/expected/predicted; no raw score rendered; uncertainty everywhere**
  (GR-7/R-3). The dashboard keeps research framing + uncertainty on every metric.
- ❌ **No un-audited W4 artifact.** Every one of the five report tables must show a **no-orphan audit JOIN**
  (each row ↔ its immutable `*_report.created` event; `orphan_count 0`). Prove by `psql` for **all five**.
- ❌ **No client-side authoritative recompute** (GR-8) — dashboard stays presentation-only.
- ❌ **No unauthenticated access; no secrets/PII.** All W4 read endpoints require auth (unauth → 401 table);
  read-only write attempts → 405/404; dashboard logged-out blocked.
- ❌ **No new report type / no new analytical capability / no unspiked compiled dependency / no D-W2-001
  breach.** The only code change is OBS-1 (+ genuine hardening, disclosed). A schema migration is **not
  expected**; if OBS-1 or hardening genuinely needs one, justify it + persistence-capture proof.
- ❌ **No regression.** FULL suite green (Wave-0/1/2/3 + W4-U01…U07) — 0 failed — + **CI via documented
  Git-Bash path → `LOCAL_CI_EXIT_CODE: 0`** + parity smoke (transcript labelled W4-U08).
- ✅ **Preserve:** advisory/research-first, presentation-only UX, tz-UTC, market-agnostic (Option A), all
  prior hardening, npm-audit 0, ruff/tsc clean.

**Any single ❌ ⇒ APPROVAL WITHHELD.**

---

## 3. Scope (Components A–E)

### A. OBS-1 closure (the only functional change)
- Fix the dashboard so the **uncertainty interval bounds render** (numeric lower→upper), not "— to —", wherever
  the persisted report carries them. Before/after browser screenshot; a frontend test asserting the bounds
  render when present.

### B. Full-wave no-execution / bright-line proof
- Run the §2 wave-wide grep over all `backend/app` + `frontend/src` (test/type files excluded; state
  exclusions) — command **and** output; residuals limited to forbidden-key lists/benign seams, each disclosed.
- Confirm no W4 schema carries order/sizing/account/position/execution/remediation columns (cite the five
  `\d *_reports`); confirm the Gate remains closed (broker gate tests + broker-seam grep empty).

### C. Artifact-audit completeness (all five report families)
- For each of `correlation_reports`, `regime_reports`, `scenario_reports`, `portfolio_risk_reports`,
  `signal_validation_reports`: a **no-orphan audit JOIN** (`<type>_report.created`; `orphan_count 0`), using
  existing seeded rows or a fresh seed. Show `SELECT COUNT` per table.

### D. Security & auth
- **Auth table:** all five W4 read endpoints unauth **401** / auth **200**; read-only POST → **405/404**;
  dashboard logged-out blocked (browser). No secrets/PII in a sampled payload (§77).

### E. Documentation, registers & closeout index
- Reconcile: `README.md`, `PROJECT_STATE.md`, `CHANGELOG.md` (→ **v0.38.0**), `04_PROJECT_ROADMAP.md` (Wave-4
  marked complete), `RISK_REGISTER.md`, `TECHNICAL_DEBT_REGISTER.md` (carry forward any residual honestly; mark
  OBS-1 CLOSED), `GOVERNANCE_AMENDMENTS.md` (no amendment; Option A stands; Gate CLOSED — state so).
- ADR `ADR-047_Wave4_Closeout_and_Hardening.md` + a **Wave-4 Closeout Evidence Index** mapping W4-U01…U08 to
  their approval verdicts + keystone safety proofs (one traceable page for the milestone).

---

## 4. Required Evidence (operator-run on target — Windows/PowerShell + PostgreSQL + BROWSER)

Report `DELIVERY_REPORT_W4-U08.md` + raw `operator results.md` + browser screenshots. **Prove build identity
first** (Test-Path the closeout ADR/index; git HEAD; v0.38.0).

1. **Build identity** — closeout files exist; v0.38.0; `git log -1 --oneline`.
2. **OBS-1 fix** — before/after **browser screenshot** of a report card showing numeric interval bounds (not
   "— to —"); frontend test asserting bounds render.
3. **Full-wave grep** (§2) — command + output; residuals disclosed + benign.
4. **Artifact-audit completeness** — no-orphan JOIN + `COUNT` for **all five** W4 report tables (`orphan 0`).
5. **Auth table** — five W4 endpoints 401/200, POST 405/404; dashboard logged-out blocked (browser).
6. **Inert-schema + gate-closed** — five `\d *_reports` (no order/sizing/account/position cols); broker gate
   tests pass; broker-seam grep empty; no-secrets sample.
7. **Full regression** — backend `pytest` **≥233 (+ any new)**, 0 failed; frontend **≥12·29 (+ OBS-1 test)**;
   ruff/tsc/build clean; npm audit 0; no new migration (or justified + persistence proof).
8. **CI** — documented Git-Bash invocation → `==> Local CI equivalent complete` + **`LOCAL_CI_EXIT_CODE: 0`**
   (transcript W4-U08). **Parity smoke.**
9. **Docs/registers** — diff summary (v0.38.0, Wave-4 complete, OBS-1 closed, TD carried, Option A/Gate CLOSED)
   + ADR-047 + Wave-4 Closeout Evidence Index.

---

## 5. Acceptance Criteria (ITRGA will verify line-by-line)

- [ ] Build identity proven; Platform v0.38.0.
- [ ] **OBS-1 CLOSED:** interval bounds render numerically (before/after browser shot + test).
- [ ] **Full-wave bright-line grep** empty/benign (command+output); five inert `\d *_reports`; Gate CLOSED
      (broker tests + seam grep empty).
- [ ] **Artifact-audit completeness:** all five W4 report tables show no-orphan JOIN (`orphan_count 0`).
- [ ] **Auth:** five endpoints 401/200, POST 405/404; dashboard logged-out blocked (browser); no secrets/PII.
- [ ] No new report type / capability / unspiked dep / D-W2-001 breach; no new migration (or justified).
- [ ] No regression; full suite green; **CI via Git-Bash → `LOCAL_CI_EXIT_CODE: 0`**; parity smoke.
- [ ] Docs/registers reconciled (v0.38.0, Wave-4 complete, OBS-1 closed); ADR-047 + Wave-4 Closeout Evidence
      Index present; Option A/Gate CLOSED confirmed.
- [ ] DA does not self-approve, self-advance, self-declare the milestone, adopt an unspiked dep, or open the
      Gate.

**A single CRITICAL, unmet mandatory evidence, or a red gate ⇒ APPROVAL WITHHELD.** On a clean pack, ITRGA
approves W4-U08, advances to **v0.38.0**, and declares the **"Institutional Intelligence Layer Complete"**
milestone.

---

## 6. Out of Scope (do NOT build — automatic FAIL if present)

- Any new analytical capability / report type / learned model / operator-facing feature beyond OBS-1.
- Any execution/order/broker/account/position/sizing path; opening the Gate.
- Any unspiked compiled dependency; any per-market model / symbol-identity feature.
- Any Wave-5/6 work; self-declaring the milestone (ITRGA authority).

---

## 7. Notes to the Development Authority

This is a **proof unit**: the deliverable is incontrovertible evidence that the whole Institutional Intelligence
layer is safe, complete, and audited — plus the one small OBS-1 fix. Mirror the W3-U08 closeout's rigor: prove
build identity first; run the wave-wide grep with command + output (residuals = forbidden-key lists/benign
seams, disclosed); show **no-orphan audit for all five report tables**; the five-endpoint auth table; the
dashboard logged-out block in the browser; and the OBS-1 before/after. Run CI via the **documented Git-Bash
path** for a clean exit 0 (transcript W4-U08). Leave docs/registers honestly reconciled.

DA does not self-approve, self-advance the version, self-declare the milestone, begin any Wave-5 work, add
execution/broker, or open the Gate. The milestone declaration follows ITRGA's verdict.

> **We don't guess. We prove.** — ITRGA
