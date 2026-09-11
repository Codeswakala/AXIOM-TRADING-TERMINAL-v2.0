# AXIOM — B-ML Algorithm Justification
## Real model choice & dependency reasoning (BO-B-ML P1.1 · Doc 09 §12)

| Item | Value |
|---|---|
| Instrument | `BO-B-ML` §P1.1 (Operator-authorized 2026-08-20) |
| Decision | **Pure-Python logistic regression via seeded SGD** (`app/ml/models/logistic_regression.py`) |
| Dependency outcome | **Zero new dependencies** — standard library only |

## Why logistic regression

- The research question is directional prediction (next-bar close direction) from a
  small, price-normalized, causal feature set. A linear probabilistic classifier is
  the canonical first substantive model: interpretable, well-understood calibration
  behavior, and honest about its capacity.
- It emits **real sigmoid probabilities** — required by the B-02 calibration gate
  (the degenerate-prior workaround of the baseline is explicitly not acceptable here).
- Coefficients + scaler are surfaced in the artifact payload — the explainability
  requirement (P1.2) is satisfied natively, not bolted on.

## Why pure Python (Doc 09 §12 dependency reasoning)

1. **Necessity.** The SGD core is ~60 lines of arithmetic. No compiled stack
   (numpy/scipy/sklearn) is *necessary* for a 3-feature linear model; introducing
   one would trade zero capability for real risk. Not justified.
2. **Maintenance & security.** Zero new supply-chain surface: the B-00.2
   severity/exception policy is untouched; every line is auditable by ITRGA.
3. **Portability.** Runs on the existing interpreter matrix unchanged; no wheel,
   no platform coupling, no future spike (cf. TD-065 compiled-wheel discipline).

## Determinism & reproducibility

- Seeded RNG (`seed=42` for the research run), fixed feature order (sorted),
  fixed epoch count and learning rate. Identical inputs reproduce identical
  coefficients, probabilities, and artifact hash — pinned by
  `test_bml_model_is_deterministic_given_seed`.
- The research-run model is reconstructible from the split manifest alone:
  same seed + same train rows → byte-identical coefficient set (verified in the
  runner: `reconstructed model rows=31530`).

## Honest outcome note (written after the run)

The model was trained and evaluated on real OKX H1 data with full rigor and
**failed the statistical, calibration (Brier leg), and economic gates**. That
negative result is the deliverable of this unit per the BO's definition of
success — recorded, never overridden, never tuned-to-pass.

---

**End of B-ML Algorithm Justification (BO-B-ML P1.1)**
