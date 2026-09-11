# AXIOM BUILD ORDER — W4-U03

## Institutional Intelligence: Regime Detection Reports (explainable, as-of, uncertainty-mandatory, non-signal, market-agnostic)

**Build Order ID:** W4-U03
**Wave:** 4 — Institutional Intelligence · **Unit:** 03
**Version:** 1.0 · **Status:** ISSUED
**Authority:** ITRGA · **Date Issued:** 2026-07-16
**Authorized By:** ITRGA, following **W4-U02 APPROVED — CLEAN** (Platform v0.32.0; correlation reports
look-ahead-safe/non-signal/persisted-audited) + operator authorization ("authorized").

**Governing Documents (canonical order — `10_CONSTITUTIONAL_HIERARCHY`):**
`00_VISION` → `03_AXIOM_SPEC` → `04_PROJECT_ROADMAP` (Tier 3) → **`05_SYSTEM_ARCHITECTURE` v2.0 (Tier 4)**
→ **`07_ML_SPEC` (Tier 5)** → `07/08_UI_UX_SPEC` → `08/09` frameworks → Tier-7 registers → this Build Order.
**Binding decisions:** D-W2-001 **Option A**; Wave-4 guardrails **GR-1…GR-8**; this unit carries
**R-2, R-4, R-6, R-7** (`ITRGA_REVIEW_WAVE4_DESIGN_PLAN.md`).
**Governing plan:** `WAVE4_ENGINEERING_DESIGN_AND_IMPLEMENTATION_PLAN.md` §4.1 (artifact contract), §5.2
(regime methodology/controls), §9 (W4-U03).
**Builds on:** W4-U01 (`institutional_intelligence` context, `IntelligenceArtifactContract`, approved deps +
pure-Python fallbacks) + W4-U02 (correlation persistence/audit + raw-SELECT+audit-join proof standard).
**Baseline to meet/exceed:** backend **204** / frontend **11 files · 25 tests**; Platform **v0.32.0**; head
**20260716_0019**.
**Motto:** *We don't guess. We prove.*

---

## 1. Purpose

Deliver **Regime Detection Reports** — a research artifact that classifies market **context**
(e.g. trend / range / volatile / calm) over an **as-of-bounded** window, **with evidence + confidence/
uncertainty**, persisted and auditable. This is **research context for the operator, never a trade
instruction** (plan §5.2). The classification **shall be explainable** (transparent rules over normalized
features) — a learned/clustering model is permitted ONLY under strict governance (see R-7 / §2).

It reads persisted candles read-only, emits the W4-U01 `IntelligenceArtifactContract`, and is read-only. It
uses the **W4-U01-approved deps (numpy/pandas/scipy) or the pure-Python fallback** — nothing else.

---

## 2. Governance Envelope (READ FIRST — violation = automatic FAIL)

- ❌ **No look-ahead (R-2 — MANDATORY NAMED NEGATIVE TEST).** No candle/feature-window data beyond
  `as_of_end` may influence any regime label. Prove by a named test in the W3-U04/W4-U02 style (inject future
  data; assert excluded-count + unchanged label). Feature windows are **backward-looking only.**
- ❌ **Regime is NOT a signal/instruction (R-6 — MANDATORY NAMED TEST).** A regime report may not be emitted
  as, promoted into, or auto-converted to an advisory signal or any action. Prove structurally (inert
  contract — no order/remediation/signal payload) + a named test that a regime artifact **triggers nothing**.
- ❌ **No uncertainty-free label (GR-7).** Every regime label carries **evidence + a confidence/uncertainty**
  measure (and the feature values/thresholds that produced it). A bare label implying certainty is
  non-conformant. Report any statistical vs economic meaning separately (a regime is context, not an edge).
- ❌ **Market-agnostic (R-7 / D-W2-001 Option A / 07_ML_SPEC "shall avoid learning symbol identities").**
  - **Preferred:** explainable **rules over NORMALIZED features** (e.g. normalized volatility/trend
    statistics) — **no symbol identity as an input**. Prove by a named test that symbol identity is not a
    feature and that the same normalized inputs yield the same regime regardless of symbol.
  - **If any learned/clustering model is used at all:** it MUST be (a) **experiment-governed + pre-registered**
    (07_ML_SPEC "every experiment shall be pre-registered"), (b) trained on **normalized/generalized features
    with no symbol identity**, and (c) built only on a **dependency-spiked** library. A **per-market
    specialized model is FORBIDDEN** absent a prior GOVERNANCE_AMENDMENTS amendment. Absent all three, use
    rules.
- ❌ **No model-retrain / mutation side effect (plan §5.2).** Producing a regime report retrains nothing,
  mutates no model/advisory status, triggers no auto-action. Prove by grep (`auto_retrain|model.status =|
  advisory_status =`) + a named "changes-nothing" test (W3-U06 keystone).
- ❌ **No execution / order / broker / gate path** (GR-1/GR-3). Gate stays CLOSED. Prove by **R-3 wave-wide
  grep** (command + output, incl. `gate_open|allow_execution`), residuals disclosed + benign.
- ❌ **No un-audited persisted report (R-4).** The new `regime_reports` table triggers the persistence-capture
  control with the **reinforced named proof**: Alembic head advance + committing script + **raw `psql SELECT
  ≥1 row` on `regime_reports`** + a **no-orphan audit JOIN** (`regime_report.created`, `orphan_count 0`), in
  this first submission. `research_status` mandatory. (This is the W4-U02 C-1 standard — deliver it inline.)
- ❌ **No unspiked compiled dependency** (R-1 standing). numpy/pandas/scipy (approved) or pure-Python only;
  scikit-learn/statsmodels FORBIDDEN unless separately spiked AND experiment-governed per R-7.
- ❌ **No client-side authoritative recompute** (GR-8) if any UI is added; presentation-only.
- ❌ **No regression** (Wave-0/1/2/3 + W4-U01/U02). Full suite green + **`LOCAL_CI_EXIT_CODE: 0`** + parity
  smoke. (Point the CI marker-check at the **W4-U03** transcript — retire the standing cosmetic OBS.)
- ✅ **Preserve:** advisory/research-first, tz-UTC, market-agnostic, all prior hardening, npm-audit 0,
  ruff/tsc clean.

**Any single ❌ ⇒ APPROVAL WITHHELD.**

---

## 3. Scope (Components A–D)

### A. Regime service (backend, `institutional_intelligence`)
- Classify regime over an **as-of-bounded, backward-looking** window from persisted candles (read-only).
- **Explainable rules over NORMALIZED features** (no symbol identity): compute normalized trend/volatility (or
  similar) statistics using approved numpy/scipy or the pure-Python fallback; map to a regime label via
  transparent thresholds stored in `config`/`method_version`.
- Attach **evidence + confidence/uncertainty** (the feature values, thresholds, and a confidence measure) and
  a `limitations` note (regime is research context, not a trade instruction; not causation of returns).
- Emit `IntelligenceArtifactContract` (`artifact_type = "regime_report"`): label, evidence, confidence/
  uncertainty, method_version, config (window/thresholds/timeframe), input_lineage + source_artifact_ids,
  `research_status`, report_hash, audit_correlation_id.
- **No-look-ahead enforced in windowing** (R-2). **No symbol identity as a feature** (R-7).

### B. Persistence + audit (R-4 — reinforced)
- New `regime_reports` table + Alembic migration; committing repository/script; immutable `regime_report.
  created` audit event on create; no orphan by construction.

### C. Read-only API
- `GET /api/v1/intelligence/regime-reports` (list) + `GET …/{report_id}` (detail) — authenticated, read-only.
- Unauth → **401**; POST → **405/404**. No emit/signal endpoint.

### D. (Optional) presentation-only surface
- If any UI is added (e.g. a regime-context panel), it is presentation-only, shows label + confidence/
  uncertainty + evidence + research/not-instruction disclaimer, has **no execution controls (R-3)** and no
  signal/action affordance, and requires **browser screenshots** from a reachable served session. If no UI,
  state so — API + tests suffice.

---

## 4. Required Evidence (operator-run on target — Windows/PowerShell + PostgreSQL)

Report `DELIVERY_REPORT_W4-U03.md` + raw `operator results.md`. **Prove build identity first.**

1. **Build identity** — new files/ADR exist; v0.33.0; `git log -1 --oneline`.
2. **R-2 no-look-ahead** — named negative test PASSED (future data excluded; label unchanged); ideally also a
   live artifact field (e.g. `excluded_future_count`) as the second proof.
3. **Uncertainty + explainability** — a produced regime report showing label + confidence/uncertainty +
   evidence (feature values/thresholds); a test asserting no bare-label-without-confidence is producible.
4. **R-7 market-agnostic** — named test that **symbol identity is not a feature** and identical normalized
   inputs yield the same regime across different symbols; if a learned model is used, show its
   pre-registration + normalized-feature + dependency-spike evidence (else state "explainable rules, no model").
5. **R-6 non-signal + no-mutation** — named tests: regime artifact cannot become/emit a signal or action; and
   producing a report changes/triggers nothing (no retrain/mutation); grep `auto_retrain|model.status =|
   advisory_status =` benign.
6. **R-4 persistence (reinforced)** — Alembic `upgrade head` + `alembic current` (new head); committing
   script; **raw `psql SELECT ≥1 row` on `regime_reports`**; **no-orphan audit JOIN** (`regime_report.created`,
   `orphan_count 0`).
7. **API** — unauth **401**; auth **list 200** + **detail 200** (show fields, non-blank echoes); POST →
   **405/404**.
8. **Dependency discipline** — approved numpy/pandas/scipy or fallback only; grep confirms no unspiked import.
9. **R-3 wave-wide grep** — command + output; residuals disclosed + benign; Gate CLOSED (broker gate tests).
10. **Full regression** — backend `pytest` **≥ (204 + new)**, 0 failed; frontend green; ruff/tsc/build clean;
    npm audit 0.
11. **CI** — `==> Local CI equivalent complete` + **`LOCAL_CI_EXIT_CODE: 0`** inline (marker-check pointed at
    the **W4-U03** transcript).
12. **Browser screenshots** if any UI; else explicit "no UI this unit." **Parity smoke.**

---

## 5. Acceptance Criteria (ITRGA will verify line-by-line)

- [ ] Build identity proven; Platform v0.33.0.
- [ ] **R-2** named no-look-ahead negative test PASSED (backward-looking feature windows).
- [ ] Every regime label carries **evidence + confidence/uncertainty**; bare-label rejected.
- [ ] **R-7** market-agnostic: symbol identity NOT a feature (named test); if learned model used, pre-registered
      + normalized + dependency-spiked; no per-market specialized model.
- [ ] **R-6** non-signal + **no model-retrain/mutation** side effect (named tests + benign grep).
- [ ] **R-4** `regime_reports`: Alembic head advanced; committing script + **raw SELECT ≥1 row** + no-orphan
      audit JOIN (`regime_report.created`, orphan 0).
- [ ] Read-only API 401 / list-200 / detail-200 / POST-405; non-blank detail echoes.
- [ ] Only approved deps or pure-Python fallback; no unspiked compiled import.
- [ ] **R-3** grep empty/benign (command+output); Gate CLOSED; no execution/broker path.
- [ ] regime = research/not-instruction framing in `limitations` (+ any UI); no D-W2-001 breach.
- [ ] No regression; full suite green; **`LOCAL_CI_EXIT_CODE: 0`** (marker-check at W4-U03 transcript); parity
      smoke; browser evidence if UI.
- [ ] DA does not self-approve, self-advance, build W4-U04+, adopt an unspiked dep, or open the Gate.

**A single CRITICAL, unmet mandatory evidence, or a red gate ⇒ APPROVAL WITHHELD.** On a clean pack, ITRGA
approves W4-U03, advances to **v0.33.0**, and (on operator authorization) issues `BUILD_ORDER_W4-U04.md`
(Scenario Simulation Research Reports) carrying **R-2/R-4/R-5/R-6**.

---

## 6. Out of Scope (do NOT build — automatic FAIL if present)

- Scenario/portfolio-risk/signal-validation features (W4-U04…U06, each own Build Order).
- Any execution/order/broker/account/position path; opening the Gate.
- Any unspiked compiled dependency; any per-market specialized model / symbol-identity feature (needs an
  amendment).
- Regime framed/emitted as a signal, instruction, or guaranteed/tradable edge; any model-retrain/mutation.
- Any Wave-5/6 work.

---

## 7. Notes to the Development Authority

The defining risk of this unit is a **hidden model that learns symbol identity or slips in an unspiked dep.**
The safe default is **explainable rules over normalized features** — and R-7 must be proven by a named test
(symbol identity is not an input; same normalized inputs → same regime across symbols). Keep look-ahead out
(R-2, proven), carry confidence on every label (no bare labels), prove the report **changes nothing** (R-6 +
no-mutation), and deliver the **raw SELECT + no-orphan audit inline** this time (the W4-U02 C-1 standard).
Point the CI marker-check at this unit's transcript to retire the standing cosmetic OBS. Prove build identity
first; disclose grep residuals with output.

DA does not self-approve, self-advance the version, build W4-U04+, adopt an unspiked dependency, add
execution/broker, or open the Gate. The next unit follows ITRGA's verdict + a new Build Order + operator
authorization.

> **We don't guess. We prove.** — ITRGA
