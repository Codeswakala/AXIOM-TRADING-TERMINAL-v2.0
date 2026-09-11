# AXIOM — DECISION MEMO (DA analysis for the Operator)
## BO-B-ML §12: retry or accept the honest negative?

| Item | Value |
|---|---|
| Document class | DA decision-support analysis — **the decision is the Operator's**; this memo provides the factual basis, nothing more |
| Date | 2026-08-20 |
| Predecessor facts | BO-B-ML delivered: honest negative, NOT PROMOTED (awaiting ITRGA determination) |

---

## 1. What the evidence actually says (the run, over real data)

| Measure | Value | Threshold | Reading |
|---|---|---|---|
| Walk-forward accuracy (347 folds, 52,560 bars) | 0.5028 | — | coin-flip level |
| Effect vs majority-class null | **+0.0028** | ≥ +0.05 | ~18× below floor |
| p-value | **0.322** | ≤ 0.05 | no significance |
| ECE | 0.0767 | ≤ 0.10 | passes (honest probabilities) |
| Brier | **0.2558** | ≤ 0.20 | uninformative — worse than the 0.25 balanced null |
| Economic net (6-class crypto costs) | **−163,559.5 bps** | > 0 | deeply negative |
| Cross-instrument hold-out (unseen XRP/ADA/DOGE) | 0.4938 | ≥ 0.50 | slightly below floor |

**The single most informative fact:** the model is *uniformly* uninformed. In-domain 0.5028 and hold-out 0.4938 are statistically indistinguishable from each other and from a coin flip. There is no sign of overfitting, no sign of a narrow exploitable regime — the three-feature linear model finds **no directional structure in hourly crypto returns at all**. This is the expected finding of a large literature; the result is credible precisely because it is boring.

## 2. Option A — RETRY (broader features / broader assets)

What a retry could change, honestly ranked:

1. **Feature breadth (DA's recommendation if retrying).** The v1 set (return_1, range_pct, rolling_return_3) is deliberately minimal. Candidates that carry ML Spec justification: realized-volatility bands, intra-bar range dynamics, session/time-of-day seasonality (crypto has documented calendar structure), cross-asset momentum spillovers (BTC leads altcoins — a market-agnostic "regime" feature, not a symbol-identity feature). Each addition must be justified against *this failure evidence* per BO-B-ML P1.3 discipline. **Caveat, stated plainly:** the honest prior for any linear model on hourly direction is that this stays negative — feature work improves the *rigor* of the negative, it does not promise promotion.
2. **Broader asset classes (OBS-BDATA-2).** The corpus is crypto-only. Forex/indices/commodities would need a new R1-style acquisition order (per-source license declarations, pinning, guard proof — the B-DATA machinery now exists to do this quickly). Cross-market structure may exist where single-market structure does not.
3. **Longer horizons.** Hourly direction is the hardest target; daily direction (the Kraken D1 corpus already in custody) is a strictly different, possibly more structured question. A retry could pre-register a D1 experiment — it would be a NEW research question under its own governance, not a re-run of this one.

## 3. Option B — ACCEPT the negative

Consequences, honestly:
- **B-03 (signals) stays gated** — no promoted model exists, and the BO's downstream dependency is explicit. The signal presentation machinery (already built and approved) remains an honest empty surface.
- **The programme is NOT blocked as a whole:** B-06 (assistant ask path — not model-dependent, design plan prepared), B-07 (hardening), and the F-units (F-00 hygiene, F-01 assistant surface, F-02..F-05 presentations) proceed regardless.
- The negative itself is a genuine scientific deliverable: a governed, reproducible, threshold-enforced answer to "does a linear model find hourly directional edge in this corpus?" — **No.** That answer protects the programme from ever shipping a coin-flip model as a signal source.

## 4. What the DA will NOT do under either option

- Will not tune, refit, relabel, or feature-engineer the current experiment into a pass (ML Spec research-integrity prohibitions; the threshold gate exists exactly to refuse this).
- Will not re-run the same experiment expecting a different answer (the pipeline is now deterministic — proven by the double-run test).
- Will not fabricate real data for additional asset classes (any new acquisition is an R1-style governed order with license declarations).

## 5. Requested Operator decision (also the programme's next authorization state)

1. **ITRGA determination on BO-B-ML** — in flight (the DA does not self-determine).
2. **§12 decision: RETRY or ACCEPT** — either can be executed immediately upon directive:
   - RETRY → a Build Order scoping the feature/asset/horizon retry, with the justification discipline above.
   - ACCEPT → B-03 formally stays gated; next issuable orders: **B-06** (design plan ready at `DESIGN_PLAN_B-06.md`) and the F-00/F-01 frontend units per the roadmap's parallel-start sequencing.

---

**End of Decision Memo** — analysis only; the Operator decides. Gate CLOSED · Production NOT CERTIFIED · We don't guess. We prove.
