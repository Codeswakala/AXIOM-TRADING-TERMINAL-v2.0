# AXIOM BUILD ORDER — W2-U05

## ML Research: Experiment Registry + Pre-Registration Workflow (the FINAL gate layer before models)

**Build Order ID:** W2-U05
**Wave:** 2 — Machine Learning Research Framework · **Unit:** 05
**Version:** 1.0 · **Status:** ISSUED
**Authority:** ITRGA · **Date Issued:** 2026-07-13
**Authorized By:** ITRGA, following **W2-U04 APPROVED** (Platform v0.16.0; dataset layer complete) + operator
authorization ("authorized").

**Governing Documents (canonical order — `10_CONSTITUTIONAL_HIERARCHY`):**
`00_VISION` → `03_AXIOM_SPEC` → `04_PROJECT_ROADMAP` (Tier 3) → **`05_SYSTEM_ARCHITECTURE` v2.0 (Tier 4)**
→ **`07_ML_SPEC` (Tier 5)** → `08/09` frameworks (Tier 6) → Tier-7 registers → this Build Order (Tier 8).
**Binding decision:** `docs/ITRGA_WAVE2_GOVERNANCE_DECISION_LOG.md` (D-W2-001, market-agnostic).
**Builds on:** W2-U01 (dataset + chronology guard) + W2-U02 (query port/metadata) + W2-U03 (feature store) +
W2-U04 (**reproducible snapshot + temporal split, with content/split hashes to pin**).
**Motto:** *We don't guess. We prove.*

---

## 1. Purpose

Deliver the **Experiment Registry** and **Pre-Registration Workflow** — the **final gate layer** of the ML
Research Framework's foundation. Per `07_ML_SPEC` §Experiment Governance: *"Every experiment shall be
pre-registered … No undocumented experiment exists."* This unit makes scientific integrity **structural**:
before any model is ever trained, an experiment must be **registered, immutable, and pinned to an exact
reproducible dataset** — so no result can later be untraceable, unreproducible, or retro-fitted (the
anti-p-hacking / anti-hidden-experiment guarantee of R18).

This unit also **carries reproducibility forward from the dataset layer**: an experiment must **pin an exact
`(snapshot content_hash + split manifest hash)`** from W2-U04, and must be **rejected** if it references a
mutated/unfrozen snapshot or an unhashed split (the W2-U04 review's forward recommendation, now mandatory).

**After this unit is approved, the hard model gate opens** — W2-U06 (baseline model harness) becomes
reviewable, but *only* by consuming a pre-registered, pinned experiment. This unit builds **governance
infrastructure**: an experiment *plan/record* is created, but **no model, no training, no inference, no
execution.**

---

## 2. Governance Envelope (READ FIRST — violation = automatic FAIL)

- ❌ **No model / training / inference / prediction.** The registry records experiment *plans*; it does not
  run them. A `model_family`/`model_spec` field may exist as **inert plan metadata**, but nothing trains.
- ❌ **No execution / broker / provider live connection / credentials.** W1-U03 Governance Gate CLOSED;
  External Integration untouched.
- ❌ **No undocumented experiment.** An experiment missing any mandatory field, or lacking approval, must be
  **rejected** — proven by negative test. *"No undocumented experiment exists."*
- ❌ **No unpinned / unreproducible experiment.** An experiment must pin an exact **frozen** snapshot
  content-hash **and** a split-manifest hash (W2-U04). An experiment referencing a **draft/unfrozen/mutated**
  snapshot or an **unhashed** split must be **rejected** — negative test.
- ❌ **No mutable experiment plan.** Once registered/approved, the plan is **immutable**; any change creates
  a **new version** (mirror the W2-U01/U04 immutability discipline). No silent post-hoc edits (anti-p-hacking).
- ❌ **No self-approval bypass.** The pre-registration → approval workflow must record an explicit approval
  step + timestamp + approver; an experiment cannot become "approved/runnable" without it.
- ❌ **No leakage/guard bypass introduced.** The registry must not offer a path that circumvents the W2-U01
  chronology guard, the W2-U03 causal/exclusion rules, or the W2-U04 temporal-split/embargo rules.
- ❌ **No DB reach-around; no secrets in logs/telemetry** (05 v2.0 §16/§77); **no PII in experiment notes.**
- ❌ **No regression** (Wave-0/1 + W2-U01–U04). Full suite + prior guard tests + parity smoke green.
- ✅ **Preserve:** advisory/research-first, single-uvicorn, canonical v2.0, tz-aware UTC, observability,
  dataset architecture + chronology guard + query port + feature store + snapshot/split engine, and all
  prior hardening. Audit trail uses the existing append-oriented governance/audit seam.

---

## 3. Scope — Components A–F

### Component A — Experiment Registry schema (`07_ML_SPEC` §Experiment Governance)
- Alembic-migrated PostgreSQL table(s) — conceptually `experiments` (+ `experiment_versions` if versioning
  is separate) — carrying the mandatory fields verbatim: **purpose, hypothesis, datasets, features, model,
  evaluation plan, approval timestamp, version** — plus, per W2-U04 pinning: **snapshot content_hash,
  split_manifest_hash, feature_set_version**, and status (`draft | pre_registered | approved | superseded`).
- **Uniqueness/identity:** an immutable `experiment_id` + version; content-hash of the plan for integrity.

### Component B — Pre-Registration Workflow
- A workflow/service to **create → pre-register → approve** an experiment. Pre-registration requires all
  mandatory fields; approval records approver + UTC timestamp. Only an **approved** experiment is runnable
  (a flag consumed later by W2-U06; this unit does not run anything).
- **Immutability:** an approved plan cannot be mutated; changes create a new version referencing the prior.

### Component C — Reproducible pinning + guard integration (carry-forward from W2-U04)
- The plan **pins** an exact frozen snapshot `content_hash` + split `manifest_hash` + `feature_set_version`.
- **Reject** an experiment that pins a **draft/unfrozen/mutated** snapshot, an **unhashed** split, or a
  hash that does not resolve to a real frozen artifact — negative test (`UNREPRODUCIBLE_EXPERIMENT_PIN` or
  similar reason).
- The evaluation-plan field must express a **temporal/walk-forward** validation intent (no random split) —
  consistent with W2-U04; a plan requesting a random split is rejected.

### Component D — Audit trail + integrity
- Every registry action (create/pre-register/approve/version) writes an **append-only audit event** via the
  existing audit seam (no secret/PII leakage; redaction from W1-U02). Registration + approval are
  reconstructable from the audit log.

### Component E — Governance, registers, ADR
- **ADR:** *Experiment Registry and Pre-Registration* (plan §11.3).
- **Registers:** record p-hacking/hidden-experiment risk as **mitigated (pre-registration + immutability +
  audit)**; unreproducible-experiment risk mitigated (hash pinning); update `PROJECT_STATE` / `CHANGELOG`;
  note that **W2-U06 (first model unit) becomes reviewable only after this unit is approved.**
- **OBS-1:** re-confirm the guard chain remains intact end-to-end (guard → features → snapshot → split →
  experiment); no registry path bypasses it.

### Component F — Verification & Delivery
- Full suite green (baseline **119** backend / **16** frontend) — 0 failed, no regression — **plus** new
  tests: mandatory-field completeness; **undocumented experiment REJECTED** (headline); **unpinned /
  unfrozen / unhashed-split experiment REJECTED** (headline); **pre-registered + approved experiment
  ACCEPTED**; approval-required-before-runnable; **immutable plan → new version on change**; random-split
  evaluation plan rejected; **audit events written**; port-only; no model/training/execution.
- Delivery Report per §5 (continue the captured `-vv` named-test standard).

### Explicitly OUT of scope (defer to W2-U06+)
Any model / training / inference / evaluation execution; calibration / economic / statistical validation
*runs* (their *plans* may be referenced as fields); live provider connections/credentials; numpy/pandas/
scikit-learn adoption **unless** a target-platform compatibility spike (Windows+Py3.14.6) is delivered *and
reviewed* per plan §4.2.

---

## 4. Success Criteria (Definition of Done)

- [ ] Experiment registry with the `07_ML_SPEC` mandatory fields (purpose/hypothesis/datasets/features/
      model/evaluation-plan/approval-timestamp/version) + **snapshot & split hash pinning**; migrated on PG.
- [ ] Pre-registration → approval workflow; only **approved** experiments are runnable; approval records
      approver + UTC timestamp.
- [ ] **Undocumented experiment REJECTED**; **unpinned/unfrozen/unhashed-split experiment REJECTED**;
      **pre-registered+approved experiment ACCEPTED** — all proven by named tests.
- [ ] Experiment plan **immutable** (change → new version); random-split evaluation plan rejected; guard
      chain not bypassable.
- [ ] Audit events written for create/pre-register/approve/version (no secret/PII leakage).
- [ ] No model/training/inference/execution; gate CLOSED; port-only; no secrets.
- [ ] ADR + registers synced; full suite green (119/16 + new tests); no regression; W2-U01–U04 tests still
      pass; conforms to `07_ML_SPEC` (§Experiment Governance / §Research Integrity) + 05 v2.0 (§16/§77).

---

## 5. Delivery Report & Evidence Requirements (MANDATORY — operator-run, target platform)

Operator-run, **Windows/PowerShell + PostgreSQL** evidence:
1. **Operator test console** (raw, `collected N`): backend `pytest` **≥119 + new tests, 0 failed**;
   frontend `vitest 16`; `ruff` clean; `tsc`/build clean.
2. **Migration evidence:** clean `alembic upgrade head` on `PostgresqlImpl` incl. experiment table(s); new
   head id shown.
3. **Rejection evidence (headline):** **undocumented experiment rejected**, and **unpinned/unfrozen/
   unhashed-split experiment rejected** — reason codes visible.
4. **Acceptance evidence:** a fully pre-registered + approved experiment is accepted, pinning a real frozen
   snapshot hash + split manifest hash; show the stored record.
5. **Immutability evidence:** an attempt to mutate an approved plan is rejected / creates a new version.
6. **Audit evidence:** a `SELECT`/log showing append-only audit events for create/pre-register/approve
   (persisted on PostgreSQL, in the spirit of the W2-U02 G-2 proof).
7. **Named-test capture:** `pytest <ml test files> -vv` **captured** (`| Tee-Object` / `-rA`) so each named
   W2-U05 test PASS is visible (continue the W2-U03/U04 standard).
8. **Containment evidence:** shown grep (R7) confirming **no model/training code** introduced
   (`fit(`/`predict(`/`train_test_split`/tree-libs empty) and port-only access.
9. **CI evidence:** orchestrated pipeline green on PostgreSQL (local acceptable; remote preferred),
   fail-closed.
10. **Parity smoke:** login → WS ticket 200 → live feed → candle fetch, unaffected.
11. Confidence **HIGH / MODERATE / LIMITED with justification — no fabricated percentages.**

---

## 6. Standards & Constraints
Clean architecture / bounded context / single ownership (ML Research owns the experiment registry);
dependency-inward; **pre-registration + immutability + audit = enforced scientific integrity**
(`07_ML_SPEC` §Experiment Governance / §Research Integrity; R18); **reproducible pinning** (snapshot+split
hash); **no undocumented / unpinned experiment**; no broker/execution/credentials (§15, gate CLOSED); no
secrets/PII (§77); tz-aware UTC. Every change in the registers (R20). Cross-platform (Windows + docker/PG).

---

## 7. Process
Implement → internal verify (suite + rejection/acceptance/immutability/audit tests) → doc sync
(PROJECT_STATE + registers + ADR) → Delivery Report with §5 evidence (operator-run, green, undocumented/
unpinned experiment refused, named tests captured) → **submit to ITRGA** → independent review → corrections
if required → approval → **only then does W2-U06 (first model unit) become reviewable.** The DA does not
self-approve, does not self-authorize the next unit, and does not open the broker gate.

---

## 8. Priority Guidance (if staged)
**A (registry schema + mandatory fields + pinning) → B (pre-registration/approval workflow) → C (pin
validation + reject unfrozen/unhashed) → D (audit trail) → E (ADR/registers) → F (verify).** Highest-value/
highest-risk: the **undocumented-experiment rejection** and the **unpinned/unfrozen-snapshot rejection** —
these are the anti-p-hacking and reproducibility guarantees the entire model program will rest on. *Prove
the bad experiment is refused* — do not assert it.

---

## 8b. Hard Gate — status
**This is the LAST gate layer.** With W2-U01–U04 proven and **W2-U05 approved**, the hard model gate opens:
**W2-U06 (Baseline Market-Agnostic Model Harness) becomes reviewable** — but only via a pre-registered,
pinned, approved experiment, and W2-U06 will additionally owe a **target-platform package-compatibility
spike** (numpy/scikit-learn on Windows+Py3.14.6) as its own acceptance gate (plan §4.2). Until W2-U05 is
APPROVED, **no model unit is reviewable.** Broker gate CLOSED throughout Wave 2.

---

*ITRGA — The last lock before the first model: every experiment written down before it runs, frozen so it
can't be quietly rewritten, and pinned to a dataset you can rebuild to the same hash. Prove an undocumented
or unpinned experiment is refused — and the model gate finally, legitimately, opens. We don't guess. We
prove.*
