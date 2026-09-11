# AXIOM — BUILD ORDER BO-B-ML2
## Predictive Research Iteration: Feature & Target Expansion Under Multiple-Comparison Discipline

| Item | Value |
|------|-------|
| Build Order ID | `BO-B-ML2` |
| Programme | Backend Operationalization — predictive track (Operator directive 2026-08-20: "continue with the predictive track") |
| Authorizing authority | **Operator** |
| Predecessors | B-00 · B-01 · B-02 · B-DATA · B-ML (all APPROVED WITH OBSERVATIONS) · ITRGA Reconciliation Determination (CLARIFICATION REQUIRED, forward) |
| Governing documents | `07_ML_SPEC.md` · `SUBSTANTIVE_THRESHOLD_FRAMEWORK.md` (B-02) · `VALIDATION_TIER_SEPARATION.md` (B-01) · `09_DEVELOPER_REASONING_FRAMEWORK.md` §12 · ITRGA Reconciliation §11 (B-03 = predictive signals only) |
| Implementer | Development Authority (DA) |
| Reviewer | ITRGA |
| Status | **ISSUED — awaiting DA implementation** |
| Governance Gate | CLOSED (unchanged) · Production NOT CERTIFIED (unchanged) |

---

## 0. Purpose and honest framing

BO-B-ML produced a **valid negative result**: three price-derived features (return_1, range_pct, rolling_return_3) fed into a linear classifier have **no exploitable edge** for hourly direction on the crypto corpus (effect +0.0028, p=0.322, net −163,559.5 bps, hold-out 0.4938).

This order is the **predictive research iteration**: it expands the hypothesis space (features and/or target) to *test whether* a richer formulation contains predictive structure. It does **not** assume one exists, and it does **not** relax any threshold.

**Definition of success:** a genuinely governed retry was executed under multiple-comparison discipline, and the true outcome — a genuinely threshold-passing model, or another honest negative — was reported. Success is **not** "we found a signal." If nothing passes, that is a valid, valuable result and further sharpens the programme's understanding.

---

## 1. The core new discipline — multiple-comparisons control (binding)

A retry that tests many feature sets and targets inflates the false-positive rate: test ~20 combinations and one will look "significant" by chance. This order therefore binds the following, which no prior unit required:

1. **One pre-registered primary hypothesis.** Before running, the DA declares — via the experiment registry (`pre_register`, plan hash) — exactly one: target, feature set, model, and evaluation plan. This is the hypothesis the determination rests on.
2. **Secondary hypotheses are labeled.** Any additional hypotheses (alternate targets/features) are explicitly marked **secondary/exploratory** and may not be reported as if pre-registered.
3. **A bounded hypothesis budget.** Primary + **at most three** secondary hypotheses. No unbounded grid search.
4. **Multiple-comparison disclosure.** The Delivery Report must state the **number of hypotheses tested** and the chosen correction. If the primary is evaluated alone (α = 0.05), that is acceptable *and must be stated*; if the family is evaluated jointly, apply a stated correction (e.g. Bonferroni) or explicitly disclose that secondary results are uncorrected and inflation-prone.
5. **No post-hoc hypothesis selection.** Once results are seen, the primary hypothesis may not be swapped for a better-looking secondary. No p-hacking, no selective reporting (ML Spec research-integrity prohibitions).

---

## 2. Scope

### Phase 1 — Feature expansion (justified, bounded)

- **Candidate families (from ML Spec §Feature Engineering), each requiring a stated justification of what new information it adds over the v1 set:**
  - volatility (ATR-normalized, realized volatility)
  - momentum (ROC over longer horizons)
  - EMA/price relationships
  - Bollinger statistics
  - volume features
  - session/time-of-day features
  - **market-structure features derived from the deterministic indicator layer** (e.g. BoS/CHoCH event recency, swing-pivot distance, structure state) — this is the natural bridge between the predictive track and the Operator's professional-trader vision, and is explicitly permitted.
- **Bounds (binding):** the primary hypothesis's feature set is **≤ 12 features**; every feature must be causal (no look-ahead, `assert_causal`), market-agnostic (no symbol/provider identity), and price-normalized where applicable.
- **Justification requirement:** each new feature's Delivery Report entry must state (a) the ML Spec basis, (b) the specific deficiency in the v1 set it addresses, and (c) the leakage/causality argument.

### Phase 2 — Target reformulation (pre-registered, bounded)

The primary hypothesis may target **one** of:
- forward-return **direction** at H1 (the B-ML target), **or** a longer horizon (H4/D1), **or**
- a **magnitude/volatility** target (e.g. next-bar range or realized-volatility quantile) — a legitimate reformulation given direction showed no edge.

The chosen target is part of the pre-registered hypothesis and may not be switched post hoc.

### Phase 3 — Research lifecycle (unchanged discipline)

Pre-register + approve → train → **walk-forward statistical validation** → **calibration** (real probabilities) → **economic validation** (full six-class crypto cost model, realistic costs) → **cross-instrument generalization** (train on some instruments, hold out **unseen** instruments) → **eligibility evaluation** via the unchanged fail-closed gate.

### Phase 4 — Outcome

- **Promotion** only on genuine passage of all thresholds (statistical, calibration, economic, generalization), with approver identity + reason.
- Otherwise an **honest negative** with full metrics, the hypothesis budget, and the multiple-comparison disclosure.

---

## 3. Exclusions (out of scope — do NOT do)

- **No** promotion of any model failing a threshold.
- **No** relaxation of the threshold gate, tier rule, or chronology guard.
- **No** p-hacking, post-hoc hypothesis changes, selective reporting, or unbounded grid search.
- **No** relabeling synthetic as real; **no** training at research tier on the B-01 synthetic corpus.
- **No** new ML library dependency without Doc 09 §12 justification (and if added, must be pinned + removable).
- **No** live data feed, broker, execution, actuation, or gate-opening; the model remains a research artifact and does not emit signals (B-03 is still gated on a *promoted* model per Reconciliation §11).
- **No** frontend changes; **no** assistant/intelligence/alerts work.
- **No** modification of the governance hierarchy or constitutional documents.
- **No** repository publication (custody model).

---

## 4. Exact deliverables

1. Pre-registration record (primary hypothesis + plan hash) — created **before** training.
2. Any new features with per-feature ML Spec justification.
3. Trained model artifact(s) (research-tier, real data).
4. Validation/calibration/economic/generalization reports (research-tier).
5. Eligibility evaluation with honest decision (PROMOTED or NOT-PROMOTED + reasons).
6. Delivery Report (§9) with the multiple-comparison disclosure and relay-accurate transmission manifest.

---

## 5. Dependencies

- **Upstream:** B-DATA (real corpus) · B-02 (threshold gate) · B-01 (snapshot/split/feature machinery) · B-ML (failure evidence = the justification baseline for new features).
- **Downstream:** B-03 (predictive signals) proceeds **only** if a model is promoted here.

---

## 6. Allowed files / components

- `backend/app/ml/features/*` (new causal, market-agnostic features with justification).
- `backend/app/ml/models/*` (model reuse or a justified extension; the logistic regression from B-ML is the default).
- `backend/app/ml/validation|calibration|economic|generalization|experiments/*` (consume; no weakening).
- `backend/app/trading_intelligence/inference/service.py` (consume the gate; do not weaken).
- `backend/tests/**` (new/churn tests).
- `backend/docs/**` (feature justification ADR if needed).
- The Delivery Report.

Anything outside this list is **not authorized**.

---

## 7. Security & integrity constraints (binding)

- No secrets/credentials; no new network surface; training is local.
- Threshold gate, tier rule, chronology guard: **unchanged and not weakened**.
- Scientific integrity (ML Spec): walk-forward only; out-of-sample only; no look-ahead; no leakage; calibration and economic verdicts reported independently; negative results documented with full rigor; **multiple-comparison discipline per §1**.
- Any new dependency justified (Doc 09 §12) and within the B-00.2 severity/exception policy.

---

## 8. Acceptance criteria

### Phase 1
- [ ] Primary hypothesis pre-registered (plan hash) **before** training; hypothesis budget ≤ 1 primary + 3 secondary.
- [ ] New features each justified (ML Spec basis + deficiency addressed + causality/no-identity), ≤ 12 in the primary set.

### Phase 2
- [ ] Target chosen and pre-registered; no post-hoc target switch.

### Phase 3
- [ ] Walk-forward validation over real data (folds, effect, p, sample).
- [ ] Calibration with real probabilities (ECE, Brier).
- [ ] Economic with six-class realistic crypto cost model (verdict).
- [ ] Cross-instrument generalization over **unseen** instruments (hold-out + degradation).

### Phase 4
- [ ] Eligibility evaluated; EITHER promoted (all thresholds, approver + reason) OR honest negative with reasons.
- [ ] **Multiple-comparison disclosure present:** number of hypotheses tested + correction method + explicit statement that the primary is the determination basis.
- [ ] No post-hoc hypothesis selection (evidenced by the pre-registration hash vs the reported primary).

---

## 9. Evidence requirements (custody model + relay-accurate manifest)

**Binding (CA-B01-1 / CA-DATA-1):** transmission manifest must reflect what the Operator can actually relay (per-file splitting; pre-emptive reconstruction path for immutable corpus-derived evidence). A declared-but-untransmitted artifact is an automatic CORRECTION REQUIRED.

| Item | Class | Form |
|------|-------|------|
| Patch artifact + per-file SHAs + `git apply --check` transcript | Level I | patch + transcript |
| Pre-registration record (primary hypothesis + plan hash, timestamped before training) | Level I | registry/query output |
| Executed test output | Level II | run transcript |
| Research-run evidence (metrics + honest decision + hypothesis budget) | Level I | query/probe output |
| Feature justification (per new feature) | Level III | report section |
| Multiple-comparison disclosure | Level III | report section |
| Transmission manifest (relay-accurate) | — | table in Delivery Report |
| Delivery Report | Level III | §10 structure |

---

## 10. Delivery Report structure (required)

1. Claimed scope vs. this Build Order
2. What changed (files + SHAs + chain position)
3. **Pre-registration record** (primary hypothesis, plan hash, timestamp)
4. Feature additions + per-feature justification
5. Target choice + rationale
6. Experiment + reports (tier + data-class labels)
7. **Honest outcome: PROMOTED or NOT-PROMOTED, with full metrics and reasons**
8. **Multiple-comparison disclosure** (hypothesis count + correction + primary-basis statement)
9. Test evidence (executed)
10. Deviations register
11. Transmission manifest (relay-accurate)
12. Known limitations / technical debt

---

## 11. Rollback / containment

- Model/report/feature rows are additive; no schema migration authorized by default.
- A promotion is reversible via the registry.
- Any new feature definition is removable without affecting the rest of the platform.

---

## 12. Completion condition

Complete when: all §8 criteria met, evidence (§9) transmitted and verified, the Delivery Report submitted, **and ITRGA issues its independent determination**. The unit is complete whether the outcome is promotion or an honest negative — but a DA declaration of completion is not evidence and does not close this unit.

**Next authorization state:** upon ITRGA approval of BO-B-ML2:
- If a model is **promoted**, B-03 (predictive advisory signals) may be issued against it.
- If the outcome is **another honest negative**, the predictive track has now been tested across two governed iterations; the programme's next step is an Operator decision (further reformulation, broader real asset classes via a new R1-style data order, or accepting the predictive track's current negative status).

---

**End of Build Order BO-B-ML2**
