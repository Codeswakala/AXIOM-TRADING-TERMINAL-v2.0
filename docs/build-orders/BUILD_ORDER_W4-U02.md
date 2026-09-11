# AXIOM BUILD ORDER — W4-U02

## Institutional Intelligence: Correlation Intelligence Reports (research, as-of, uncertainty-mandatory, non-signal)

**Build Order ID:** W4-U02
**Wave:** 4 — Institutional Intelligence · **Unit:** 02 (first analytical feature)
**Version:** 1.0 · **Status:** ISSUED
**Authority:** ITRGA · **Date Issued:** 2026-07-16
**Authorized By:** ITRGA, following **W4-U01 APPROVED — CLEAN** (Platform v0.31.0; TD-065 discharged for
numpy/pandas/scipy; inert artifact contract) + operator authorization ("authorized").

**Governing Documents (canonical order — `10_CONSTITUTIONAL_HIERARCHY`):**
`00_VISION` → `03_AXIOM_SPEC` → `04_PROJECT_ROADMAP` (Tier 3) → **`05_SYSTEM_ARCHITECTURE` v2.0 (Tier 4)**
→ **`07_ML_SPEC` (Tier 5)** → `07/08_UI_UX_SPEC` → `08/09` frameworks → Tier-7 registers → this Build Order.
**Binding decisions:** D-W2-001 **Option A**; Wave-4 guardrails **GR-1…GR-8**; plan refinements — this unit
carries **R-2, R-4, R-6** (`ITRGA_REVIEW_WAVE4_DESIGN_PLAN.md`).
**Governing plan:** `WAVE4_ENGINEERING_DESIGN_AND_IMPLEMENTATION_PLAN.md` §4.1 (artifact contract), §5.1
(correlation methodology/controls), §9 (W4-U02).
**Builds on:** W4-U01 (`institutional_intelligence` context, `IntelligenceArtifactContract`, approved deps
numpy 2.5.1 / pandas 3.0.3 / scipy 1.18.0, pure-Python fallbacks) + W2-U07 (uncertainty-mandatory precedent).
**Baseline to meet/exceed:** backend **198** / frontend **11 files · 25 tests**; Platform **v0.31.0**; head
**20260715_0018**.
**Motto:** *We don't guess. We prove.*

---

## 1. Purpose

Deliver **Correlation Intelligence Reports** — a research artifact quantifying the statistical relationship
between markets/timeframes over an **as-of-bounded** window, **with uncertainty**, persisted and auditable.
This is **research context for the operator, never a signal or instruction** (plan §5.1). It reads persisted
market data (candles) via the existing Market/Persistence context, computes correlation over the
`IntelligenceArtifactContract` from W4-U01, and exposes it read-only.

It uses the **W4-U01-approved deps** (numpy/pandas/scipy) OR the committed pure-Python fallback — nothing else.

---

## 2. Governance Envelope (READ FIRST — violation = automatic FAIL)

- ❌ **No look-ahead (R-2 — MANDATORY NAMED NEGATIVE TEST).** No data with timestamp **beyond `as_of_end`**
  may influence any correlation result. Prove by a named test in the W3-U04 `EXCLUDED_FUTURE_COUNT` style
  (inject a future candle; assert it is excluded and the result is unchanged). Prose "as-of windows" is
  insufficient — prove it.
- ❌ **No uncertainty-free / point-estimate correlation (GR-7).** Every correlation value **must** carry a
  confidence/uncertainty interval + **sample_count**. A bare coefficient implying precision is non-conformant
  (W2-U07). Report **statistical significance separately from economic usefulness** (do not imply a strong
  correlation is tradable).
- ❌ **Correlation is NOT a signal/instruction (R-6 — MANDATORY NAMED TEST).** A correlation report may not be
  emitted as, promoted into, or auto-converted to an advisory signal or any action. Prove structurally: the
  report cannot carry an order/remediation/signal payload (inherits the inert contract), and a named test
  asserts a correlation artifact **triggers nothing** (the W3-U06 "changes-nothing" keystone applied here).
- ❌ **No correlation-as-causation framing.** Any surface/text (and the artifact `limitations` field) states
  correlation ≠ causation and is research-only, not a guarantee.
- ❌ **No execution / order / broker / gate path** (GR-1/GR-3). Gate stays CLOSED. Prove by **R-3 wave-wide
  grep** (command + output, incl. `gate_open|allow_execution`), residuals disclosed + benign.
- ❌ **No un-audited persisted report (R-4).** The new `correlation_reports` table triggers the
  **persistence-capture control**: committing script + raw `psql SELECT ≥1 row` on the CORRECT table + a
  matching immutable **audit event** (no orphan), in this first submission. `research_status` mandatory.
- ❌ **No unspiked compiled dependency** (R-1 standing). Only numpy/pandas/scipy (W4-U01-approved) or the
  pure-Python fallback. scikit-learn/statsmodels/etc. are FORBIDDEN here (owe their own spike).
- ❌ **No D-W2-001 breach.** No symbol-identity-as-feature; correlation is a general statistical relation, not
  a per-market learned model.
- ❌ **No client-side authoritative recompute** (GR-8) if any UI is added — presentation-only, read the API.
- ❌ **No regression** (Wave-0/1/2/3 + W4-U01). Full suite green + **`LOCAL_CI_EXIT_CODE: 0`** + parity smoke.
- ✅ **Preserve:** advisory/research-first, tz-UTC, market-agnostic, all prior hardening, npm-audit 0, ruff/tsc
  clean.

**Any single ❌ ⇒ APPROVAL WITHHELD.**

---

## 3. Scope (Components A–D)

### A. Correlation service (backend, `institutional_intelligence`)
- Compute correlation between two (or more) market series over an **as-of-bounded** window
  (`as_of_start`…`as_of_end`), reading persisted candles read-only.
- **Estimator:** Pearson (via approved scipy/numpy) with a **bootstrap or analytic confidence interval** and
  **sample_count**; pure-Python fallback (`pearson_correlation` from W4-U01) available and tested. (Spearman
  optional, same controls, if included.)
- **No-look-ahead enforced in the windowing** (R-2) — the query/compute path structurally excludes
  timestamps > `as_of_end`.
- Emit results into the `IntelligenceArtifactContract` (`artifact_type = "correlation_report"`): value(s),
  uncertainty interval, sample_count, method_version, config (window/pair/timeframe), input_lineage +
  source_artifact_ids (which series/candle range), `limitations` (correlation≠causation, research-only),
  `research_status`, report_hash, audit_correlation_id.

### B. Persistence + audit (R-4)
- New table `correlation_reports` (or the agreed artifact table) + Alembic migration.
- Committing repository/script; on create, write an **immutable audit event** with correlation id.
- Foundation: no orphan by construction (every report ↔ an audit event).

### C. Read-only API
- `GET /api/v1/intelligence/correlation-reports` (list) and/or a detail read — **authenticated, read-only**.
- Unauth → **401**; write attempt (POST) → **405/404**. No emit/signal endpoint.

### D. (Optional) presentation-only surface
- If any UI is added (e.g. a correlation matrix/report view), it is **presentation-only** (reads the API,
  no client recompute), carries the research/advisory + correlation≠causation disclaimer, shows uncertainty +
  sample_count, has **no execution controls (R-3)** and **no signal/action affordance**, and requires
  **browser screenshots** from a reachable served session. If no UI this unit, state so — API + tests suffice.

---

## 4. Required Evidence (operator-run on target — Windows/PowerShell + PostgreSQL)

Report `DELIVERY_REPORT_W4-U02.md` + raw `operator results.md`. **Prove build identity first.**

1. **Build identity** — new files/ADR exist; v0.32.0; `git log -1 --oneline`.
2. **R-2 no-look-ahead** — named negative test PASSED (inject future candle; excluded-count/unchanged-result).
3. **Uncertainty** — a computed report showing value + interval + **sample_count**; a test asserting no
   point-estimate-only report is producible; significance vs economic-usefulness kept distinct.
4. **R-6 non-signal** — named test proving a correlation artifact cannot become/emit a signal or action, and
   the artifact carries no order/remediation/signal payload (inherits inert contract).
5. **R-4 persistence** — Alembic `upgrade head` + `alembic current` (new head); committing script; **raw
   `psql SELECT ≥1 row` on `correlation_reports`**; matching **audit event** (no-orphan join/count).
6. **API** — unauth **401**; auth **200** returning a report with uncertainty + sample_count + lineage; POST
   → **405/404**.
7. **Dependency discipline** — show the compute uses only approved numpy/pandas/scipy or the fallback; grep
   confirms no unspiked compiled import (`sklearn`/`statsmodels`/etc.).
8. **R-3 wave-wide grep** — command + output; residuals disclosed + benign; Gate CLOSED (broker gate tests).
9. **Full regression** — backend `pytest` **≥ (198 + new)**, 0 failed; frontend green; ruff/tsc/build clean;
   npm audit 0.
10. **CI** — `==> Local CI equivalent complete` + **`LOCAL_CI_EXIT_CODE: 0`** inline (point the marker-check at
    the W4-U02 transcript — OBS-B from W4-U01).
11. **Browser screenshots** if any UI added (§3.D); else explicit "no UI this unit."
12. **Parity smoke.**

---

## 5. Acceptance Criteria (ITRGA will verify line-by-line)

- [ ] Build identity proven; Platform v0.32.0.
- [ ] **R-2** named no-look-ahead negative test PASSED (future data excluded).
- [ ] Every correlation carries **uncertainty interval + sample_count**; point-estimate-only rejected;
      significance reported separately from economic usefulness.
- [ ] **R-6** named test: correlation artifact cannot become/emit a signal or action; inert (no order/
      remediation/signal payload).
- [ ] **R-4** `correlation_reports`: Alembic head advanced; committing script + **raw SELECT ≥1 row** + audit
      event (no orphan).
- [ ] Read-only API 401/200/405; no emit/signal endpoint.
- [ ] Only W4-U01-approved deps or the pure-Python fallback; **no unspiked compiled import**.
- [ ] **R-3** grep empty/benign (command+output); Gate CLOSED; no execution/broker path.
- [ ] correlation≠causation / research-only framing in artifact `limitations` (+ any UI); no D-W2-001 breach.
- [ ] No regression; full suite green; **`LOCAL_CI_EXIT_CODE: 0`**; parity smoke; browser evidence if UI.
- [ ] DA does not self-approve, self-advance, build W4-U03+, adopt an unspiked dep, or open the Gate.

**A single CRITICAL, unmet mandatory evidence, or a red gate ⇒ APPROVAL WITHHELD.** On a clean pack, ITRGA
approves W4-U02, advances to **v0.32.0**, and (on operator authorization) issues `BUILD_ORDER_W4-U03.md`
(Regime Detection Reports) carrying **R-2/R-4/R-6/R-7**.

---

## 6. Out of Scope (do NOT build — automatic FAIL if present)

- Regime/scenario/portfolio-risk/signal-validation features (W4-U03…U06, each own Build Order).
- Any execution/order/broker/account/position path; opening the Gate.
- Any unspiked compiled dependency (scikit-learn/statsmodels/etc.).
- Correlation framed/emitted as a signal, instruction, or guaranteed/tradable edge.
- Any per-market specialized model / symbol-identity feature (D-W2-001 Option A).
- Any Wave-5/6 work.

---

## 7. Notes to the Development Authority

This is the first Wave-4 unit that computes something — so the two things that must be incontrovertible are
**(1) no future data touches the result (R-2, proven by a named negative test, not prose)** and **(2) a
correlation is context, not a signal (R-6, proven by a named test + the inert contract).** Carry the
uncertainty on every value (no false precision), persist with a raw SELECT + audit (R-4), use only the
approved deps or the fallback, and keep the CI exit code inline (and point its marker-check at this unit's
transcript). Prove build identity first; disclose grep residuals with output.

DA does not self-approve, self-advance the version, build W4-U03+, adopt an unspiked dependency, add
execution/broker, or open the Gate. The next unit follows ITRGA's verdict + a new Build Order + operator
authorization.

> **We don't guess. We prove.** — ITRGA
