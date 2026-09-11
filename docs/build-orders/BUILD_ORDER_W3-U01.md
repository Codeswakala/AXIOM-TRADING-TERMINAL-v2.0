# AXIOM BUILD ORDER — W3-U01

## Live Research Advisor: Live Inference Engine + Governed Model Eligibility Gate (backend-only safe slice)

**Build Order ID:** W3-U01
**Wave:** 3 — Live Research Advisor · **Unit:** 01 (first Wave-3 unit — the safety foundation)
**Version:** 1.0 · **Status:** ISSUED
**Authority:** ITRGA · **Date Issued:** 2026-07-15
**Authorized By:** ITRGA, following **Wave 3 Design Plan ACCEPTED** (`docs/ITRGA_REVIEW_WAVE3_DESIGN_PLAN.md`)
+ operator Wave-3 scoping authorization.

**Governing Documents (canonical order — `10_CONSTITUTIONAL_HIERARCHY`):**
`00_VISION` → `03_AXIOM_SPEC` → `04_PROJECT_ROADMAP` (Tier 3) → **`05_SYSTEM_ARCHITECTURE` v2.0 (Tier 4)**
→ **`07_ML_SPEC` (Tier 5)** → `08/09` frameworks (Tier 6) → Tier-7 registers → this Build Order (Tier 8).
**Binding decision:** `docs/ITRGA_WAVE2_GOVERNANCE_DECISION_LOG.md` (D-W2-001, market-agnostic).
**Builds on:** the full Wave-2 governed-model lineage (W2-U05 experiment registry → U06 harness → U07
statistical → U08 calibration → U09 economic → U10 generalization/domain + model registry).
**Carries:** design-plan review **R-1** (governed, audited advisory-promotion approval).
**Motto:** *We don't guess. We prove.*

---

## 1. Purpose

Deliver the **safety foundation of the Live Research Advisor**: a **deterministic Live Inference Engine** and
a **Governed Model Eligibility Gate** — **backend-only, no operator-facing signal surface yet.** This is the
smallest safe slice (design plan §14): before AXIOM ever shows a signal to a human, prove that (a) inference
is deterministic, (b) **only a fully-governed, advisory-approved model can ever be eligible to emit**, and
(c) **no execution path exists** and the Constitutional Governance Gate stays CLOSED.

Per `05 v2.0` §6 (Trading Intelligence owns signals; *"does not directly interact with brokers"*), §15 (flow
ends at Operator Decision → CLOSED gate), §42 (deterministic inference), and `07_ML_SPEC` §Deployment Policy
(only validated/approved/registered models deploy). This unit builds the **gate and the deterministic scorer**
— the door's lock — and proves it refuses the ungoverned before any signal can leave the building.

**No signals to operators, no UI, no alerts, no live WS signal stream, no execution** — those are later
Wave-3 units and Wave 6. This unit is the checked precondition for all of them.

---

## 2. Governance Envelope (READ FIRST — violation = automatic FAIL)

- ❌ **No execution / orders / positions / broker connection / paper trading — real, demo, or paper.**
  W1-U03 Constitutional Governance Gate stays **CLOSED**; External Integration untouched. Any code path that
  could route to a broker/order/execution surface is an automatic FAIL (R17 — the brightest line). Prove by a
  shown **no-execution grep** + structural test.
- ❌ **No operator-facing signal / emission / UI / alert / live WS signal stream in THIS unit.** W3-U01 is
  backend-only: it produces a **deterministic inference result** and an **eligibility verdict** — it does
  **not** emit a signal to any operator surface. (Signal contract/persistence = W3-U02; UI = W3-U05.)
- ❌ **No ineligible model may be eligible to emit.** A model is **eligible only if** it has the complete
  Wave-2 lineage — experiment approved (U05) + statistical (U07) + calibration (U08) + economic (U09) +
  generalization/operating-domain (U10) report links + feature-version match + **model input excludes symbol
  identity** (D-W2-001) + **no execution capability** — **and** status `advisory_approved` (see R-1). Any
  missing element ⇒ **refused.** Prove each refusal by named test.
- ❌ **No `advisory_approved` without a governed, audited approval (R-1).** The research→advisory promotion
  must require an **explicit approval action + approver + UTC timestamp + audit event**, and must be
  **impossible without complete U05–U10 lineage.** A settable-flag promotion (no approval, no lineage) is an
  automatic FAIL. Prove: promotion refused without lineage; refused without recorded approval; only
  `advisory_approved` is eligible.
- ❌ **No non-deterministic inference.** Same `(model_artifact_id, model_version, feature_set_version, input/
  as_of, config)` ⇒ **same score** (§42). No random sampling, no live mutable model state. Prove by test
  (score twice → identical) + an **input hash** recorded.
- ❌ **No chronology violation at inference** (OBS-1 spirit, live): UTC `as_of_time`; **no future data**; no
  `seed:synthetic`-authoritative or forward-dated `live:simulated`-as-real input; no label/target
  construction at inference.
- ❌ **No symbol identity as model input** (D-W2-001) — proven at the inference-input boundary.
- ❌ **No DB reach-around** (§16 — consume market data/models via approved seams); **no secrets/PII** (§77).
- ❌ **No regression** (Wave-0/1 + W2-U01–U10). Full suite + prior tests + parity smoke.
- ✅ **Preserve:** advisory/research-first, tz-UTC, observability, the full governed-model chain, single-
  uvicorn, all prior hardening.

---

## 3. Scope — Components A–F

### Component A — Live Inference Engine (deterministic scorer) (§42; plan §5.1)
- A backend inference service that loads a **registered model artifact** and scores an input **deterministically**:
  canonical feature-vector ordering, pinned feature definitions, model artifact hash/version, UTC `as_of_time`,
  no randomness, no mutable model state. Record an **`inference_input_hash`** and return an inference result
  DTO (score + provenance: model_artifact_id/version, feature_set_version, experiment_id, as_of, input hash).
- **Test:** same inputs+version → **identical score + input hash** (twice).

### Component B — Governed Model Eligibility Gate (plan §5.2 — the safety core)
- An eligibility check returning **eligible / refused(reason)**. Eligible **iff** ALL: experiment approved
  (U05); statistical (U07) + calibration (U08) + economic (U09) + generalization/operating-domain (U10)
  report links present; feature-version matches artifact; model input excludes symbol identity; no execution
  capability; **status `advisory_approved`.**
- **Named refusals (each a negative test), e.g.:** `EXPERIMENT_NOT_APPROVED`, `MISSING_STATISTICAL_REPORT`,
  `MISSING_CALIBRATION_REPORT`, `MISSING_ECONOMIC_REPORT`, `MISSING_GENERALIZATION_REPORT`,
  `FEATURE_VERSION_MISMATCH`, `IDENTITY_IN_INFERENCE_INPUT`, `NOT_ADVISORY_APPROVED`.
- **Chronology/domain at input:** out-of-domain or future/synthetic-authoritative input → refused/withheld
  (reuse W2-U10 domain + W2-U01 chronology semantics).

### Component C — Advisory deployment-status lifecycle + GOVERNED promotion (R-1) (plan §5.3)
- Introduce the status lifecycle `research_only → advisory_candidate → advisory_approved → advisory_suspended
  → retired` on the model registry (Alembic migration). **Only `advisory_approved` is emit-eligible.**
- **Governed promotion:** promotion to `advisory_approved` requires an **explicit approval action (approver +
  UTC timestamp + audit event)** AND complete U05–U10 lineage. **Tests:** promotion refused without lineage;
  refused without recorded approval; a promoted model records an audit event; only `advisory_approved` passes
  the eligibility gate.

### Component D — No-execution boundary (the bright line — proven)
- **No execution/order/broker path** anywhere in the inference/gate code. **Shown grep (R7: cmd + empty
  output)** over the new code for `place_order|cancel_order|broker\.|order_intent dispatch|live_signal|execute`
  → empty; structural test that the inference/gate modules cannot import/call External Integration broker
  services; Governance Gate remains CLOSED.

### Component E — Governance, registers, ADR, persistence
- **ADR:** *Live Inference Engine + Eligibility Gate* (+ advisory-status lifecycle + governed-promotion policy).
- **Registers:** pre-list Wave-3 risks mitigated here (premature-execution → Critical/Controlled by gate +
  grep; ineligible-model-served → Critical/eligibility gate; non-deterministic-inference; ungoverned-promotion).
  Update `PROJECT_STATE`/`CHANGELOG`.
- **Persistence-capture control (HIGH-on-recurrence):** any NEW persisted artifact/columns introduced (e.g.
  advisory-status + promotion audit) must be shown persisted on PostgreSQL via a **committing-script +
  `SELECT ≥1 row`** proof, correct table, in **this first submission.**

### Component F — Verification & Delivery
- Full suite green (baseline **159** backend / **16** frontend) — 0 failed, no regression — **plus** new
  tests: deterministic score (twice→same + input hash); **each eligibility refusal by name**; **governed
  promotion (refused w/o lineage, refused w/o approval, audited on success, only advisory_approved eligible)**;
  identity-in-input refused; out-of-domain/chronology-violating input refused; **no-execution grep + structural**;
  no signal surface exists.
- Delivery Report per §5.

### Explicitly OUT of scope (later Wave-3 / Wave 6)
Operator-facing signal emission + signal contract/persistence (W3-U02); emit-time domain/calibration/economic
guardrails on *emitted* signals (W3-U03); live market inference adapter (W3-U04); dashboard/workspace (W3-U05);
alerts (W3-U06); analytics (W3-U07); any execution / broker / paper trading (Wave 6). **No UI, no alerts, no
signal emission in W3-U01.**

---

## 4. Success Criteria (Definition of Done)

- [ ] Deterministic Live Inference Engine: same inputs+version → identical score + recorded `inference_input_hash`.
- [ ] Governed eligibility gate: eligible **only** with full U05–U10 lineage + feature-version match + no
      identity + no execution capability + `advisory_approved`; **each refusal proven by named test.**
- [ ] Advisory-status lifecycle migrated; **governed promotion** (approval action + approver + UTC + audit;
      impossible without lineage) — refusals + audited success proven; only `advisory_approved` emit-eligible.
- [ ] Chronology/domain at inference input enforced (no future/synthetic-authoritative; out-of-domain refused);
      **no symbol identity in inference input.**
- [ ] **No execution/order/broker path** (grep empty + structural test); gate CLOSED; **no operator-facing
      signal/UI/alert in this unit.**
- [ ] Any new persisted artifact shown on PostgreSQL via committing-script `SELECT ≥1 row` (first submission).
- [ ] ADR + registers synced; full suite green (159/16 + new tests); no regression; W2-U01–U10 tests still
      pass; conforms to 05 v2.0 (§6/§15/§16/§42/§77) + `07_ML_SPEC` §Deployment Policy + D-W2-001.

---

## 5. Delivery Report & Evidence Requirements (MANDATORY — operator-run, target platform)

Operator-run, **Windows/PowerShell + PostgreSQL** evidence:
1. **(If compiled dep) wheel-spike** on Win/Py3.14.6; else pure-Python + stated.
2. **Operator test console** (raw, `collected N`): backend `pytest` **≥159 + new tests, 0 failed**; frontend
   `vitest 16`; `ruff` clean; `tsc`/build clean.
3. **Migration evidence:** clean `alembic upgrade head` on `PostgresqlImpl` incl. advisory-status/promotion-
   audit changes; new head id shown.
4. **Determinism evidence (captured `-vv`):** score twice → identical score + input hash.
5. **Eligibility-refusal evidence (captured `-vv`, by name):** each refusal reason (missing-lineage-link ×
   U05/U07/U08/U09/U10, feature-version-mismatch, identity-in-input, not-advisory-approved).
6. **Governed-promotion evidence:** promotion refused without lineage; refused without recorded approval;
   audited success; only `advisory_approved` eligible.
7. **No-execution evidence:** shown grep (R7: cmd + empty output) for execution/order/broker/live_signal in
   the new code + structural test; Governance Gate CLOSED.
8. **Persisted-PG proof (committing-script, first submission, correct table):** the advisory-status/promotion
   record via raw `psql SELECT` returning ≥1 row + its audit event.
9. **No-signal-surface evidence:** confirmation (grep/structural) that no operator-facing signal/emit/alert/
   UI endpoint was added in W3-U01.
10. **CI green on PostgreSQL** through completion, fail-closed (capture the completion marker).
11. **Parity smoke:** login → WS ticket 200 → live feed → candle fetch, unaffected.
12. Confidence **HIGH / MODERATE / LIMITED with justification — no fabricated percentages.**

---

## 6. Standards & Constraints
Clean architecture / bounded context (Trading Intelligence / ML boundary owns inference + gate); **advisory-
only, no execution** (R17; §15 gate CLOSED); **only governed `advisory_approved` models eligible** (§Deployment
Policy; governed promotion R-1); **deterministic inference** (§42); **chronology + domain + identity honest at
input** (W2-U01/U10 + D-W2-001); **no signal surface this unit**; reproducible; no secrets (§77); tz-UTC;
persisted-artifact committing proof first submission (HIGH-on-recurrence). Every change in the registers (R20).
Cross-platform (Windows + docker/PostgreSQL).

---

## 7. Process
Implement (spike if needed) → internal verify (suite + determinism + eligibility refusals + governed promotion
+ no-execution + persisted-PG) → doc sync (PROJECT_STATE + registers + ADR) → Delivery Report with §5 evidence
(operator-run, green, refusals captured by name, no-execution proven, persisted proof) → **submit to ITRGA** →
independent review → corrections if required → approval → next Build Order (W3-U02). The DA does not
self-approve, self-authorize the next unit, emit a live signal, or open the broker gate.

---

## 8. Priority Guidance (if staged)
**A (deterministic engine + input hash) → C (advisory-status lifecycle + governed promotion, R-1) →
B (eligibility gate + named refusals) → D (no-execution bright line) → E (ADR/registers + persisted proof) →
F (verify).** Highest-value/highest-risk: the **eligibility gate refusals** and the **governed promotion** —
this unit's entire purpose is to make "only a fully-governed, approved model can ever be eligible to speak" a
*proven* precondition — plus the **no-execution bright line.** *Prove the ungoverned/ineligible model is
refused and no execution path exists* before any later unit lets a signal reach a human.

---

## 8b. Gate status
Research/advisory only — and **this unit produces NO operator-facing signal at all** (backend safety
foundation). No live signals, no execution (Wave 6), broker gate CLOSED. W3-U02 (Advisory Signal Contract +
Persistence) is the recommended next unit and requires its own Build Order.

---

*ITRGA — Before AXIOM says a single word to an operator, build the lock and prove it holds: inference that is
deterministic, a gate that lets only a fully-Wave-2-governed, formally-approved model become eligible to
speak, and a bright line with no execution behind it. No signal leaves this unit; it exists so that when one
finally does, it could only ever have come from a model that earned the right. We don't guess. We prove.*
