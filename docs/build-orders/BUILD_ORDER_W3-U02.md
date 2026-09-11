# AXIOM BUILD ORDER — W3-U02

## Live Research Advisor: Advisory Signal Contract + Signal Persistence (first governed signal — backend/API, no UI)

**Build Order ID:** W3-U02
**Wave:** 3 — Live Research Advisor · **Unit:** 02
**Version:** 1.0 · **Status:** ISSUED
**Authority:** ITRGA · **Date Issued:** 2026-07-15
**Authorized By:** ITRGA, following **W3-U01 APPROVED** (Platform v0.23.0; advisory safety foundation) +
operator authorization ("W3-U02 authorized").

**Governing Documents (canonical order — `10_CONSTITUTIONAL_HIERARCHY`):**
`00_VISION` → `03_AXIOM_SPEC` → `04_PROJECT_ROADMAP` (Tier 3) → **`05_SYSTEM_ARCHITECTURE` v2.0 (Tier 4)**
→ **`07_ML_SPEC` (Tier 5)** → `08/09` frameworks (Tier 6) → Tier-7 registers → this Build Order (Tier 8).
**Binding decision:** `docs/ITRGA_WAVE2_GOVERNANCE_DECISION_LOG.md` (D-W2-001, market-agnostic).
**Builds on:** W3-U01 (deterministic Live Inference Engine + Governed Model Eligibility Gate + advisory-status
lifecycle) + the full Wave-2 governed-model lineage (U05–U10).
**Motto:** *We don't guess. We prove.*

---

## 1. Purpose

Deliver the **Advisory Signal Contract + Signal Persistence** — the **first Wave-3 unit that produces a
governed advisory signal.** A signal is an **inert, auditable research record** that an `advisory_approved`
model's deterministic inference (W3-U01) *may* produce, carrying its full lineage, calibrated confidence,
rationale, domain/economic context, and a `emitted | withheld | warning` state — persisted to PostgreSQL with
an audit event, and readable via a **signal-history API.**

Per `05 v2.0` §6 (Trading Intelligence owns signals), §15 (flow ends at Operator Decision → CLOSED gate), and
the accepted Wave-3 plan (§6 signal contract, §6.3 "withhold rather than emit opaque advice"): this unit lets
a governed model *speak into a record*, gated by W3-U01's eligibility gate, and **stops there.**

**No operator-facing UI, no alerts, no live WS signal stream, no execution** — those are later Wave-3 units
(W3-U05/U06) and Wave 6. This unit produces the signal *record + history API*; a human reads it later through
a governed surface.

---

## 2. Governance Envelope (READ FIRST — violation = automatic FAIL)

- ❌ **No execution / orders / positions / broker / paper trading.** W1-U03 Constitutional Governance Gate
  stays **CLOSED**; External Integration untouched. **A signal is an inert record — it must contain NO
  executable order payload** and no path to dispatch one (R17; plan §6.2 "no signal may contain executable
  order payloads"). Prove by shown grep + structural test.
- ❌ **No signal from an ineligible/ungoverned model.** A signal may be **emitted only** when the W3-U01
  eligibility gate passes (full U05–U10 lineage + `advisory_approved` + feature-version + no-identity + no
  execution capability). An ineligible/`research_only`/out-of-domain/future-input case ⇒ the signal is
  **withheld** (state `withheld`, reason recorded), **never emitted.** Prove each by named test.
- ❌ **No opaque signal.** An emitted signal must carry its **rationale/explainability** (model, input,
  why, calibrated confidence + calibration state, domain validity, economic verdict, limitations/uncertainty).
  **If rationale cannot be produced ⇒ withhold, not emit** (plan §6.3). Prove by test.
- ❌ **No raw-score-as-confidence.** Displayed/stored operator-facing confidence must be the **calibrated**
  confidence (W2-U08); a poorly-calibrated model's signal is `warning`/withheld, never shown as certainty.
- ❌ **No unaudited / unpersisted signal.** Every emitted *and* withheld signal is **persisted with an audit
  event** (append-only). No in-memory-only signal. **Committing-proof-first-submission control applies**
  (persisted-PG proof, correct table, this delivery — HIGH-on-recurrence).
- ❌ **No operator-facing UI / alert / live WS signal stream this unit** (backend + read-only history API
  only). No chart/UI signal computation (UX presentation-only, §30/§11.1).
- ❌ **No chronology/identity violation** (carried from W3-U01): UTC as-of; no future/synthetic-authoritative
  input; no symbol identity as model input.
- ❌ **No secrets/PII in signal records/logs** (§77); **no DB reach-around** (§16).
- ❌ **No regression** (Wave-0/1 + W2-U01–U10 + W3-U01). Full suite + prior tests + parity smoke; broker gate
  + W3-U01 eligibility gate still green.
- ✅ **Preserve:** advisory/research-first, tz-UTC, observability, the full governed chain, deterministic
  inference, all prior hardening.

---

## 3. Scope — Components A–F

### Component A — Advisory Signal Contract (DTO + table) (plan §6.1)
- A signal record (Alembic-migrated `signals`/`advisory_signals` table) with the plan §6.1 fields, at least:
  `signal_id`, `created_at`/`as_of_time` (UTC), `market_class`/`provider`/`symbol`/`timeframe`,
  `model_artifact_id`/`model_version`/`feature_set_version`/`experiment_id`, **lineage links**
  (`statistical_report_id`/`calibration_report_id`/`economic_report_id`/`generalization_report_id`),
  `inference_input_hash`, `raw_score`, **`calibrated_confidence`**, `signal_direction`/classification,
  **`signal_state` (emitted | withheld | warning | expired | superseded)**, `operating_domain_status`,
  `calibration_status`, `economic_verdict`, `risk_notes`, **`rationale`/`explainability_summary`**,
  `audit_correlation_id`. **Inert — no order/executable payload field.**

### Component B — Governed emission (eligibility-gated) + state machine (plan §6.2)
- Signal production flows `candidate → eligible_checked → emitted | withheld | warning → expired |
  superseded`. **Emission requires the W3-U01 eligibility gate to pass**; failure ⇒ `withheld` with the gate
  refusal reason recorded (never `emitted`).
- **Named tests:** an `advisory_approved`+in-domain case ⇒ `emitted` (with full lineage + rationale +
  calibrated confidence); a `research_only`/ineligible model ⇒ `withheld` (`NOT_ADVISORY_APPROVED` etc.);
  out-of-domain ⇒ `withheld`/`warning` (`UNSUPPORTED_DOMAIN`); poorly-calibrated ⇒ `warning`/withheld;
  rationale-unavailable ⇒ withheld.

### Component C — Explainability + calibrated confidence (plan §6.3/§7)
- Every `emitted` signal carries a human-readable rationale + the required explainability elements; stored
  confidence is the **calibrated** confidence (not raw score). **No rationale ⇒ withhold.** Proven by test.

### Component D — Signal-history API (read-only) + audit
- A **read-only, authenticated** signal-history API (list/query persisted signals with their lineage +
  state + rationale). No emit-on-demand execution surface; no UI. Every signal (emitted/withheld) writes an
  **append-only audit event**.

### Component E — Inert / no-execution proof + governance
- **Shown grep (R7)** over the new signal code + routes for `place_order|cancel_order|broker\.|execute|
  order_intent dispatch` → **empty**; structural test that a signal record cannot carry/lead to an order
  payload and the signal path cannot call External Integration broker services; Governance Gate CLOSED.
- **ADR:** *Advisory Signal Contract and Persistence*. **Registers:** signal-not-audited / ineligible-signal-
  emitted / opaque-signal risks mitigated; update `PROJECT_STATE`/`CHANGELOG`.
- **Persisted-artifact committing proof (first submission, correct table):** an emitted signal + its audit
  event shown on PostgreSQL via committing script → `SELECT ≥1 row`; and a withheld signal shown persisted
  with its reason.

### Component F — Verification & Delivery
- Full suite green (baseline **164** backend / **16** frontend) — 0 failed, no regression — **plus** new
  tests: emitted-signal (governed, lineage+rationale+calibrated confidence); **withheld on ineligible/
  research_only/out-of-domain/poor-calibration/no-rationale** (each by name); signal is **inert (no order
  payload)**; signal-history API returns persisted signals (auth required); audit events written; no UI/alert/
  WS signal stream added; W3-U01 gate + broker gate still green.
- Delivery Report per §5.

### Explicitly OUT of scope (later Wave-3 / Wave 6)
Emit-time domain/calibration/economic *guardrail maturation* (W3-U03 — this unit gates on eligibility + basic
domain/calibration state; deeper guardrails there); live market inference adapter (W3-U04); dashboard/
workspace/UI (W3-U05); alerts + live WS signal stream (W3-U06); analytics (W3-U07); any execution/broker/paper
trading (Wave 6). **No UI, no alerts, no live signal push in W3-U02.**

---

## 4. Success Criteria (Definition of Done)

- [ ] Signal contract (DTO + PG table) with §6.1 fields incl. full lineage links, calibrated confidence,
      rationale, `signal_state`; **inert (no order/executable payload).**
- [ ] Emission **gated by the W3-U01 eligibility gate**; state machine `candidate→eligible_checked→emitted|
      withheld|warning→expired|superseded`.
- [ ] **Named withholds:** ineligible/`research_only`/out-of-domain/poor-calibration/no-rationale ⇒ withheld
      or warning (reason recorded), **never emitted.**
- [ ] Emitted signal carries rationale + explainability + **calibrated** confidence (not raw score).
- [ ] Read-only authenticated signal-history API; every signal (emitted/withheld) audited.
- [ ] **No execution/order payload/broker path** (grep empty + structural); gate CLOSED; **no UI/alert/WS
      signal stream this unit.**
- [ ] Persisted-PG proof (committing script, correct table, first submission): emitted + withheld signals +
      audit events shown.
- [ ] ADR + registers synced; full suite green (164/16 + new tests); no regression; W3-U01 + W2 + broker
      tests still pass; conforms to 05 v2.0 (§6/§15/§16/§77) + `07_ML_SPEC` + D-W2-001.

---

## 5. Delivery Report & Evidence Requirements (MANDATORY — operator-run, target platform)

Operator-run, **Windows/PowerShell + PostgreSQL** evidence:
1. **(If compiled dep) wheel-spike;** else pure-Python + stated.
2. **Operator test console** (raw, `collected N`): backend `pytest` **≥164 + new tests, 0 failed**; frontend
   `vitest 16`; `ruff` clean; `tsc`/build clean.
3. **Migration evidence:** clean `alembic upgrade head` on `PostgresqlImpl` incl. the signals table; new head.
4. **Emitted-signal evidence (captured `-vv`):** a governed `advisory_approved`+in-domain signal ⇒ `emitted`
   with full lineage + rationale + **calibrated** confidence.
5. **Withhold evidence (captured `-vv`, by name):** ineligible/`research_only`/out-of-domain/poor-calibration/
   no-rationale ⇒ **withheld/warning** with reason (never emitted).
6. **Inert / no-execution evidence:** shown grep (R7: cmd + empty output) for order/broker/execute in the
   signal code + routes; structural test (no order payload; no External Integration broker call); gate CLOSED.
7. **Signal-history API evidence:** authenticated read of persisted signals (401 without / 200 with);
   no emit/execution surface.
8. **Persisted-PG proof (committing script, first submission, correct table):** emitted signal `SELECT ≥1
   row` (lineage/state/rationale/calibrated_confidence) + withheld signal + audit events.
9. **CI green on PostgreSQL** through completion (capture the completion marker — the W3-U01 LOW note).
10. **Parity smoke:** login → WS ticket 200 → live feed → candle fetch, unaffected.
11. Confidence **HIGH / MODERATE / LIMITED with justification — no fabricated percentages.**

---

## 6. Standards & Constraints
Clean architecture / bounded context (Trading Intelligence owns signals; UX untouched this unit); **advisory-
only, inert signal, no execution** (R17; §15 gate CLOSED); **governed emission** (only W3-U01-eligible,
`advisory_approved` models emit); **calibrated confidence + rationale, or withhold**; **every signal
audited/persisted** (committing proof first submission, correct table, HIGH-on-recurrence); deterministic
inference reused (W3-U01); chronology/identity honest; no secrets (§77); tz-UTC; read-only authenticated
history API. Every change in the registers (R20). Cross-platform.

---

## 7. Process
Implement → internal verify (suite + emitted/withheld by name + inert/no-execution + history API + persisted-
PG) → doc sync (PROJECT_STATE + registers + ADR) → Delivery Report with §5 evidence (operator-run, green,
withholds by name, inert proven, persisted proof, no UI/alert/execution) → **submit to ITRGA** → independent
review → corrections if required → approval → next Build Order (W3-U03). The DA does not self-approve,
self-authorize the next unit, push a live signal to an operator surface, or open the broker gate.

---

## 8. Priority Guidance (if staged)
**A (signal contract/table, inert) → B (governed emission + state machine + named withholds) → C
(rationale + calibrated confidence, or withhold) → D (history API + audit) → E (no-execution proof + ADR/
registers + persisted proof) → F (verify).** Highest-value/highest-risk: the **governed-emission gate**
(only an eligible, approved model's signal is `emitted`; everything else `withheld`) and the **inert /
no-order-payload** guarantee — this is the first unit where a signal exists, so it must be *provably* a record
a human reads, never an action. *Prove the ungoverned signal is withheld and the signal carries no order.*

---

## 8b. Gate status
Research/advisory only — a signal is an **inert record**; **no execution (Wave 6), no operator UI/alert/live
push this unit, broker gate CLOSED.** W3-U03 (emit-time domain/calibration/economic guardrail maturation) is
the recommended next unit and needs its own Build Order.

---

*ITRGA — Now a governed model may finally speak — but only into a record: inert, fully-lineaged, carrying its
calibrated confidence and its reasons, or withheld if it cannot explain itself. Only a model that passed all
of Wave 2 and was approved to go live may be `emitted`; everything else is `withheld`, and no signal ever
carries an order. Prove the ungoverned signal is refused and the record holds no action — the platform
speaks; it still does not act. We don't guess. We prove.*
