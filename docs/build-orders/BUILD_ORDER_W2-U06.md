# AXIOM BUILD ORDER — W2-U06

## ML Research: Baseline Market-Agnostic Model Harness (FIRST model unit — behind the model gate)

**Build Order ID:** W2-U06
**Wave:** 2 — Machine Learning Research Framework · **Unit:** 06 (first model-touching unit)
**Version:** 1.0 · **Status:** ISSUED
**Authority:** ITRGA · **Date Issued:** 2026-07-14
**Authorized By:** ITRGA, following **W2-U05 APPROVED** (Platform v0.17.0; foundation complete, model gate
OPEN) + operator authorization ("authorized").

**Governing Documents (canonical order — `10_CONSTITUTIONAL_HIERARCHY`):**
`00_VISION` → `03_AXIOM_SPEC` → `04_PROJECT_ROADMAP` (Tier 3) → **`05_SYSTEM_ARCHITECTURE` v2.0 (Tier 4)**
→ **`07_ML_SPEC` (Tier 5)** → `08/09` frameworks (Tier 6) → Tier-7 registers → this Build Order (Tier 8).
**Binding decision:** `docs/ITRGA_WAVE2_GOVERNANCE_DECISION_LOG.md` (D-W2-001, market-agnostic).
**Builds on (ALL must be honoured, not re-implemented):** W2-U01 dataset+chronology guard · W2-U02 query
port/metadata · W2-U03 feature store (causal, no symbol identity) · W2-U04 reproducible snapshot + temporal
split/embargo · **W2-U05 experiment registry (pre-registration + hash pinning + approval + audit)**.
**Motto:** *We don't guess. We prove.*

---

## 1. Purpose

Deliver the **first model** in AXIOM — a **baseline, market-agnostic model harness** that trains **only**
on a pre-registered, approved, hash-pinned experiment (W2-U05), consuming reproducible, temporally-split,
embargoed, leak-free snapshots (W2-U01/U04) and causal, symbol-identity-free features (W2-U03). This unit
proves the *machinery* of training + persisted model artifacts under governance — **not** predictive skill,
and **not** production use. It is deliberately the **simplest viable baseline** (`07_ML_SPEC` §Model Types),
chosen *after* a target-platform compatibility spike.

The whole five-unit foundation exists so that this — the first time a model touches data — is **incapable
of being trained on dishonest, unpinned, leaky, or symbol-identified data.** W2-U06's job is to demonstrate
that a model can only ever ride the rails the foundation built.

**Research/advisory only:** the harness produces a **registered model artifact + evaluation numbers for a
pre-registered experiment**. It produces **no live signals, no operator-facing predictions, no execution.**

---

## 2. Governance Envelope (READ FIRST — violation = automatic FAIL)

- ❌ **No training except via a pre-registered, APPROVED, hash-pinned experiment (W2-U05).** Training that
  bypasses the experiment registry — or references a `draft`/unapproved/unpinned experiment — is an
  automatic FAIL. The harness must **refuse** to train without an approved experiment (negative test).
- ❌ **No leakage / no non-temporal split.** The harness consumes the W2-U04 temporal splits + embargo
  as-is; it must **not** re-split, shuffle, or peek across the train/validation/test boundary. Re-deriving
  a random split, or ignoring the embargo, is an automatic FAIL.
- ❌ **No symbol identity as a model input (D-W2-001) — enforced at the MODEL INPUT boundary.** The feature
  matrix fed to `fit()` must exclude symbol/provider/market_class identity; a test must prove the model
  input vector contains no identity field (extend the W2-U03/U04 exclusion to the *model* boundary).
- ❌ **No execution / broker / provider live connection / credentials / live signals.** W1-U03 Governance
  Gate CLOSED; live operator-facing signals are **Wave 3**, execution **Wave 6**. The harness output is a
  research artifact, never a tradeable signal.
- ❌ **No fabricated results / no metric cherry-picking.** Report whatever the baseline produces — a weak
  baseline is a *fine and expected* result (this unit proves machinery, not skill). Selective reporting /
  post-hoc metric changes violate `07_ML_SPEC` §Research Integrity (R18).
- ❌ **No non-reproducible training.** Given the same pinned experiment + fixed seed + environment, a
  retrain must yield a **deterministic, reproducible model artifact hash / metrics** (or documented,
  bounded nondeterminism with a recorded seed). Prove by retrain → same result.
- ❌ **No adoption of an ML dependency that is not target-proven.** Any new package (numpy/scikit-learn/
  etc.) must pass the **Component A compatibility spike on Windows + Py3.14.6** *before* the harness is
  judged — a wheel/ABI failure at the operator run is an automatic FAIL (plan §4.2).
- ❌ **No secrets/PII in logs/telemetry/model artifacts** (05 v2.0 §77). **No DB reach-around** (§16).
- ❌ **No regression** (Wave-0/1 + W2-U01–U05). Full suite + all prior guard/registry tests + parity smoke.
- ✅ **Preserve:** advisory/research-first, single-uvicorn, canonical v2.0, tz-aware UTC, observability,
  the full dataset/feature/snapshot/split/experiment chain, and all prior hardening.

---

## 3. Scope — Components A–G

### Component A — Target-platform package-compatibility spike (STAGED SUB-GATE — do first)
- Before any model code is judged, deliver a **compatibility spike**: install + import + minimal smoke of
  the chosen baseline stack on **Windows + Python 3.14.6** (candidate: `numpy` + `scikit-learn`, or a
  pure-Python/`numpy`-only baseline if sklearn wheels are unavailable on 3.14.6). Record exact versions in
  an ADR/delivery note. **If the intended stack is not target-compatible, fall back to the simplest
  pure-Python/numpy baseline and document it** — do not ship an import that fails on the operator's machine
  (the W1-U01 lesson, pre-empted per plan §4.2). Pin versions in `requirements.txt`.
- **This spike is its own acceptance checkpoint:** ITRGA reviews the compatibility evidence as part of §5;
  a failed/again-untested wheel is a blocker regardless of the rest.

### Component B — Baseline model family (`07_ML_SPEC` §Model Types — simplest viable)
- Implement the **simplest defensible baseline** (e.g. logistic/linear or a shallow tree / gradient-boost
  *if* target-compatible; a trivial majority/mean baseline is acceptable as the floor). Market-agnostic:
  trained on normalized features across market classes, **no symbol identity.** Keep it minimal — this unit
  is about the harness + governance, not model sophistication.

### Component C — Training harness bound to a pinned experiment (the core governance link)
- A `train(experiment_id)` path that: **loads an APPROVED experiment** from the W2-U05 registry; resolves
  its pinned snapshot `content_hash` + split `manifest_hash` + `feature_set_version`; **verifies the pins
  resolve to real frozen artifacts**; builds the model-input matrix from the **temporal train split**
  (identity-free); fits the baseline; evaluates on the **validation/test splits** respecting the embargo.
- **Refuse** to train if: no experiment / experiment not `approved` / pins don't resolve / matrix contains
  identity / split is non-temporal — each a negative test (reason codes, e.g.
  `EXPERIMENT_NOT_APPROVED`, `UNRESOLVED_PIN`, `IDENTITY_IN_MODEL_INPUT`, `NON_TEMPORAL_SPLIT`).

### Component D — Model artifact + registry (research-only) (`07_ML_SPEC` §Model Registry / §Deployment Policy)
- Persist a **research model artifact** with the mandated registry fields: unique id, version, **training
  dataset snapshot id/hash**, **feature version**, hyperparameters, **evaluation metrics**, supported
  operating domain (markets/timeframes evaluated), approval/deployment status = **research only** (NOT
  production; no execution). Link the model back to its experiment_id (traceability).
- **Reproducibility:** retrain the same experiment + seed → deterministic artifact hash / metrics (or
  documented bounded nondeterminism with recorded seed). Prove twice → same.

### Component E — Evaluation output (inert; NOT a live signal)
- Produce **research evaluation numbers** (e.g. train/val/test metric(s) appropriate to the baseline) bound
  to the experiment. These are **stored research artifacts** — explicitly **not** operator-facing signals,
  not dispatched anywhere. (Deeper statistical/calibration/economic validation are W2-U07/U08/U09 — this
  unit reports only the raw baseline metric honestly.)

### Component F — Governance, registers, ADR
- **ADR:** *Baseline Model Harness* (stack choice + compatibility result + governance binding).
- **Registers:** record model-overfitting/weak-baseline as expected/observed (not a defect); package-
  compat risk closed/updated; add any new risk (e.g. nondeterminism); update `PROJECT_STATE`/`CHANGELOG`.
- **Re-confirm** the guard chain end-to-end (guard→features→snapshot→split→experiment→model) is not
  bypassable; broker gate CLOSED; D-W2-001 at model input.

### Component G — Verification & Delivery
- Full suite green (baseline **127** backend / **16** frontend) — 0 failed, no regression — **plus** new
  tests: **train-without-approved-experiment REFUSED**; **unresolved/unfrozen pin REFUSED**; **identity in
  model input REFUSED**; **non-temporal split REFUSED**; **reproducible retrain → same artifact/metrics**;
  model artifact carries mandated registry fields + research-only status; baseline trains + evaluates on a
  pinned experiment end-to-end; no live signal emitted.
- Delivery Report per §5 (continue the captured `-vv` named-test standard; use the committing-script method
  for any persisted-PG proof, per the W2-U05 C-2 precedent).

### Explicitly OUT of scope (defer)
Statistical validation suite (W2-U07); calibration (W2-U08); economic validation (W2-U09); multi-market
generalization + drift + model registry maturation (W2-U10); any live/operator-facing signal (Wave 3);
execution (Wave 6); advanced model families beyond the simplest target-compatible baseline (governed
additions later).

---

## 4. Success Criteria (Definition of Done)

- [ ] **Compatibility spike passes on Windows + Py3.14.6** (install/import/smoke), exact versions pinned;
      or a documented pure-Python/numpy fallback if wheels unavailable.
- [ ] Baseline model (simplest viable, market-agnostic, **no symbol identity**) trains via a `train(
      experiment_id)` path that **only** accepts an APPROVED, hash-pinned experiment.
- [ ] **Refusals proven by name:** train-without-approved-experiment, unresolved/unfrozen pin, identity in
      model input, non-temporal split — each REJECTED.
- [ ] Model artifact persisted with mandated registry fields + snapshot/feature hashes + **research-only
      status**; linked to its experiment_id; **reproducible retrain → same artifact/metrics** (or documented
      seeded determinism).
- [ ] Evaluation numbers produced as **inert research artifacts** (no live signal, no operator-facing
      output, no dispatch).
- [ ] No execution/broker/live-signal; gate CLOSED; no secrets in artifacts/logs; no DB reach-around; no
      fabricated/cherry-picked metrics.
- [ ] ADR + registers synced; full suite green (127/16 + new tests); no regression; W2-U01–U05 tests still
      pass; conforms to `07_ML_SPEC` (§Model Types / §Training Framework / §Model Registry / §Deployment
      Policy research-only / §Research Integrity) + 05 v2.0 (§16/§77) + D-W2-001.

---

## 5. Delivery Report & Evidence Requirements (MANDATORY — operator-run, target platform)

Operator-run, **Windows/PowerShell + PostgreSQL** evidence:
1. **Compatibility-spike evidence (staged, first):** install + import + smoke of the chosen stack on
   Windows/Py3.14.6, exact versions shown (`pip show`/`import; print(version)`). If fallback chosen, show
   why + the fallback working.
2. **Operator test console** (raw, `collected N`): backend `pytest` **≥127 + new tests, 0 failed**;
   frontend `vitest 16`; `ruff` clean; `tsc`/build clean.
3. **Migration evidence** (if schema added for model registry): clean `alembic upgrade head` on
   `PostgresqlImpl`, new head id shown. (If none, state so.)
4. **Refusal evidence (headline, captured `-vv` by name):** train-without-approved-experiment,
   unresolved/unfrozen-pin, identity-in-model-input, non-temporal-split — each **REJECTED** with reason
   code visible.
5. **End-to-end train evidence:** train a baseline on an **approved, pinned** experiment → a model artifact
   is produced with its registry fields + **research-only** status + link to experiment_id.
6. **Reproducibility evidence:** retrain the same experiment + seed → **identical artifact hash / metrics**
   (or documented seeded determinism).
7. **Persisted-PG proof (committing-script method, per W2-U05 C-2):** the model-registry row (and any audit
   event) shown via a raw `psql SELECT` returning ≥1 row.
8. **Identity-exclusion + no-live-signal evidence:** shown grep/test that the **model input** excludes
   identity, and that no operator-facing/live-signal endpoint was added.
9. **CI green on PostgreSQL** (local orchestration acceptable; remote preferred), fail-closed.
10. **Parity smoke:** login → WS ticket 200 → live feed → candle fetch, unaffected.
11. Confidence **HIGH / MODERATE / LIMITED with justification — no fabricated percentages** (and state the
    baseline metric **honestly**, however weak).

---

## 6. Standards & Constraints
Clean architecture / bounded context (ML Research owns the harness + model registry); dependency-inward;
**train only via approved+pinned experiment**; **temporal/embargoed splits consumed as-is** (no leakage;
R18); **no symbol identity at model input** (D-W2-001); **reproducible** (seeded, artifact-hashed);
**research-only** model status (`07_ML_SPEC` §Deployment Policy — no production/execution); **honest
reporting** (no cherry-picking); target-proven dependencies only; no secrets in artifacts/telemetry (§77);
tz-aware UTC; broker gate CLOSED (§15). Every change in the registers (R20). Cross-platform (Windows +
docker/PostgreSQL).

---

## 7. Process
Implement (spike first) → internal verify (suite + refusal/reproducibility/artifact tests) → doc sync
(PROJECT_STATE + registers + ADR) → Delivery Report with §5 evidence (operator-run, green, spike proven,
refusals captured, reproducible, honest metric) → **submit to ITRGA** → independent review → corrections if
required → approval → next Build Order (W2-U07). The DA does not self-approve, does not self-authorize the
next unit, and does not open the broker gate or emit live signals.

---

## 8. Priority Guidance (if staged)
**A (compatibility spike — gate it first) → B (simplest baseline) → C (train bound to approved+pinned
experiment + refusals) → D (research-only model artifact/registry + reproducibility) → E (inert evaluation)
→ F (ADR/registers) → G (verify).** Highest-value/highest-risk: **the refusals** (train-without-approval,
unresolved-pin, identity-at-input, non-temporal-split) and the **compatibility spike** — a model that can
be trained off-governance, or a stack that fails on the operator's machine, is the whole risk of this unit.
*Prove the model can only train on honest, pinned, approved, identity-free data — and prove the stack runs
on the target.* A weak baseline metric is an acceptable, expected outcome; **do not tune for skill here.**

---

## 8b. Gate status
**The model gate is OPEN and this is the first unit through it.** It remains bounded: **research/advisory
only — no live signals (Wave 3), no execution (Wave 6), broker gate CLOSED.** W2-U06 does not unlock
anything beyond itself; W2-U07 (statistical validation) is the recommended next unit and requires its own
Build Order.

---

*ITRGA — The first model, at last — but only on rails: trained solely through an approved, hash-pinned
experiment, on data it can rebuild to the same hash and split with a moat no label can cross, blind to every
symbol's name, and never speaking a live signal. Prove the stack runs on the target, prove the harness
refuses off-governance training, and report the baseline honestly however humble. Skill comes later; today
we prove the model can only ever learn the right way. We don't guess. We prove.*
