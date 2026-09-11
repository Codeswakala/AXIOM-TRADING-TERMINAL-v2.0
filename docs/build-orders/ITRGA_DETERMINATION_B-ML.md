# ITRGA DETERMINATION — BO-B-ML
## Substantive Machine Learning: Real Model, Research-Tier Validation, Governed Promotion

| Item | Value |
|------|-------|
| Review identity | ITRGA independent review of DA Delivery Report `DELIVERY_REPORT_B-ML.md` |
| Build Order | `BO-B-ML` (Operator-authorized 2026-08-20) |
| Predecessors | BO-B-00 · BO-B-01 · BO-B-02 · BO-B-DATA (all APPROVED WITH OBSERVATIONS) |
| Date | 2026-08-20 |
| Evidence standard | Level I (direct) / Level II (executed) / Level III (documentary) |

---

## 1. What I verified (Level I/II — reproduced independently)

| Check | Result |
|-------|--------|
| Patch `bml.patch.txt` sha256 | `7a9d5324…` — **matches** |
| `git apply --check` + apply | **Clean** (exit 0) |
| 7 post-apply file SHAs | **All 7 match** the report's cited hashes |
| Model code review | **Genuine algorithm** — SGD logistic regression with L2, train-only standardization, true sigmoid probabilities, seeded determinism, identity-key assertion. Not a disguised baseline. |
| New B-ML tests (6) | **6/6 passed** |
| **Full backend suite** | **509 passed** — matches report (509 / 142.80s) |
| Fixture slice authenticity | **Verbatim real OKX BTCUSDT H1 data** — independently re-fetched and byte-compared, matches live source exactly |
| Execute log | Honest negative: `eligible=False`, 4 threshold reasons + NOT_ADVISORY_APPROVED, promotion refused |

## 2. Acceptance criteria vs. Build Order — line-by-line

| BO requirement | Status |
|-----------------|--------|
| P1.1 real algorithm, zero new deps | ✓ pure-Python logistic regression (SGD); dependency reasoning documented |
| P1.2 determinism / market-agnostic / explainable / real probabilities | ✓ all four pinned by tests; verified in code |
| P1.3 features (builtin v1 only) | ✓ no new features; justification given |
| P2.1 experiment approved over real data | ✓ `research_validation` tier, `historical:real`, forward-return labels |
| P2.2 walk-forward validation | ✓ 347 folds over 52,560 real bars |
| P2.3 calibration, real probabilities | ✓ ECE/Brier from real sigmoid outputs |
| P2.4 economic, six-class crypto cost model | ✓ `economically_unusable` |
| P2.5 cross-instrument generalization, unseen instruments | ✓ train BTC/ETH/SOL → hold-out XRP/ADA/DOGE |
| P3.1 gate evaluation | ✓ `GovernedModelEligibilityGate.evaluate()` |
| P3.2 promoted OR honest negative | ✓ **honest negative**, four threshold refusals, nothing overridden |

**All acceptance criteria met.**

## 3. The pivotal properties — verified

1. **The model is real.** I read the entire `logistic_regression.py`. It is a genuine SGD logistic regression: L2 regularization, standardization computed from the *training matrix only* (no leakage), sigmoid probabilities that genuinely vary with features, seeded RNG with fixed feature order for determinism, and an explicit identity-key assertion before training. This is a substantive learning algorithm — not the majority-class baseline, and not a wrapper around one.

2. **The negative result is the truth, honestly reported.** 347 walk-forward folds over 52,560 real bars: accuracy 0.5028, effect +0.0028 (floor 0.05), p=0.322 (ceiling 0.05). Brier 0.2558 (> 0.20). Net −163,559.5 bps after a full six-class crypto cost model. Cross-instrument hold-out 0.4938 (< 0.50 floor). Every number unambiguously fails its threshold, the gate refused promotion for exactly those reasons, and **nothing was overridden**. The artifact remains `research_only`.

3. **The generalization was a true out-of-sample test.** Train on BTC/ETH/SOL, evaluate on *unseen* XRP/ADA/DOGE. The degradation is small (+0.009, within the 0.10 bound) — meaning the model is *not* overfit, it is *uniformly uninformed*. That is a scientifically meaningful finding: hourly directional prediction from three price-normalized features on this crypto corpus has **no exploitable linear signal**, and the honest report says so plainly.

## 4. Findings

### OBS-BML-1 (Low, report precision) — numeric transcription discrepancies in §1
The report's §1 summary table quotes **ECE 0.0406 · Brier 0.2515** and **net −162,219.5 bps**, while the transmitted execute log (and the report's own §6/§7) show **ECE 0.0767 · Brier 0.2558** and **net −163,559.5 bps**. The §1 figures do not match the executed evidence. The direction and outcome are identical in every case (all four thresholds fail regardless of which set is used), so this does not affect the determination — but report-to-evidence numeric precision is a governance-record quality matter. The §1 table should be corrected to the executed numbers.

### OBS-BML-2 (Low, transmission process) — `bml_probe_prefix.log` declared but not transmitted
The manifest declares `bml_probe_prefix.log.txt` (hash `ec0ae2ef…`) as transmitted; it is not in my custody. This is the same R3 pattern observed across prior deliveries (CA-DATA-1). The fail-first claim's substance is corroborated by the fact that the pre-fix module genuinely did not exist (the new file is in the patch), so no outcome impact — but the manifest's transmission claim is again inaccurate for one item.

## 5. Deviation D7 — reviewed, accepted, with a carried limitation

Deviation D7 fixes a genuine reproducibility defect: the W2-U04 split engine ordered cross-series rows sharing an `as_of` by a uuid `row_id`, so split membership (and every downstream metric) drifted between runs on identical data. The fix adds a deterministic tie-break. This is correct and important — it is the reason the entire run is now reproducible.

The disclosed limitation is honest: snapshot/split/artifact **hashes** still embed uuid source/row ids and differ per run instance, so **content and metrics are deterministic while fingerprints are not**. The DA flagged full fingerprint determinism as a future hardening unit. I concur and record it as carried debt.

## 6. Programme consequence — the honest negative is the current state

Per BO-B-ML §0 and §12, this negative result is a **valid, valuable deliverable** (ML Spec: "failed experiments documented with the same rigor as successful ones"). It also determines the next step, which belongs to the Operator:

- **B-03 (signals) remains gated** — no promoted model exists, exactly as the dependency model required.
- The Operator must now choose (BO-B-ML §12):
  - **Retry** — with a richer feature set (each new feature justified against this failure evidence) and/or broader asset classes (the corpus is crypto-only per OBS-BDATA-2); or
  - **Accept the negative** — hourly directional prediction at this feature set on this data has no exploitable linear signal, and the programme proceeds on that basis.

Either way, the integrity of the threshold gate is now **proven in the negative direction**: the programme will not manufacture an eligible model from a feature set that has no edge. That is the single most important property this entire backend operationalization was built to guarantee.

---

## 7. Determination

| Field | Value |
|-------|-------|
| Determination | **APPROVED WITH OBSERVATIONS** |
| Basis | All BO acceptance criteria met; 7/7 SHAs reproduced; 6/6 new + 509/509 full suite; model verified genuine in code; fixture verified real; honest negative correctly reported |
| Observations | OBS-BML-1 (report numeric precision), OBS-BML-2 (transmission, carried R3 pattern) |
| Next authorization state | **BO-B-ML CLOSED** — but **B-03 remains gated**; the Operator's §12 retry/accept decision governs the substantive path |
| What this is not | Not production certification; not gate-opening; not a claim that the model has any predictive skill (it does not) |

## 8. Record

- Patch: `7a9d532454ebcd04aefd303e519b10959a04c59fcef698584791353c2dadd173`
- Post-apply: 7/7 file SHAs · 6/6 new · 509/509 full suite
- Model: genuine SGD logistic regression, verified in code
- Outcome: honest negative — effect +0.0028, p=0.322, Brier 0.2558, net −163,559.5 bps, hold-out 0.4938

> **We don't guess. We prove.** The programme now has what it set out to build: a real model, run through a real governed research pipeline over real data, held to real thresholds — and it told the truth. There is no edge here, and AXIOM said so instead of pretending otherwise. That is the platform working as intended. Approved.

**End of ITRGA Determination BO-B-ML**
