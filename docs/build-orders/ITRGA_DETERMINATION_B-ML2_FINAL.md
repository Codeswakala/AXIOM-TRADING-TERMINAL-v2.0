# ITRGA DETERMINATION — BO-B-ML2 (FINAL)
## Predictive Research Iteration: Feature & Target Expansion

| Item | Value |
|------|-------|
| Review identity | ITRGA independent review of DA Delivery Report `DELIVERY_REPORT_B-ML2.md` |
| Build Order | `BO-B-ML2` (Operator-authorized 2026-08-20) |
| Prior determination | `ITRGA_DETERMINATION_B-ML2.md` — CORRECTION REQUIRED (0/6 evidence artifacts in custody) |
| This determination | **FINAL** — after Operator re-relayed the evidence |
| Date | 2026-08-20 |

---

## 1. Reversal of prior determination (correct epistemic update)

The prior determination was CORRECTION REQUIRED because only the Delivery Report had arrived — zero evidence artifacts. The Operator has now re-relayed the set. I have verified it and am issuing the substantive determination.

## 2. What I verified (Level I/II — reproduced independently)

| Check | Result |
|-------|--------|
| Patch `bml2.patch.txt` sha256 | `1649e26f…` — **matches** |
| `git apply --check` + apply | **Clean** (exit 0) |
| 4 post-apply file SHAs | **All 4 match** the report's cited hashes |
| 8 new v2 features in code | **Present** — all causal (`assert_causal`), market-agnostic, warm-up-disciplined |
| **Pre-registration ordering** | **3 hashes at log lines 12–14, all before any training/validation (line 18+)** — the hypothesis was genuinely fixed before results |
| Hypothesis budget | 1 primary + 2 secondary ≤ bound (1+3) — **met** |
| New B-ML2 tests (5) | **5/5 passed** |
| **Full backend suite** | **514 passed** — matches report (514 / 140.09s) |
| Execute-log metrics | **Match the report exactly** (effect, p, ECE, Brier, net bps, hold-out) |

## 3. Acceptance criteria vs. Build Order — line-by-line

| BO requirement | Status |
|-----------------|--------|
| §1.1 pre-registered primary, plan hash, before training | ✓ 3 hashes verified to precede training (log lines 12–14 vs 18+) |
| §1.2 secondaries labeled exploratory | ✓ "labeled exploratory" in registry + log |
| §1.3 bounded budget (1+3) | ✓ 3 total |
| §1.4 multiple-comparison disclosure | ✓ primary at α=0.05 stated; secondaries uncorrected + labeled |
| §1.5 no post-hoc selection | ✓ primary NOT swapped; pre-registration hashes fixed |
| Phase 1 features ≤12, causal, justified | ✓ 11 features; 8 new, each justified; causal asserted |
| Phase 2 target pre-registered | ✓ primary direction@H1; S2 magnitude as labeled secondary |
| Phase 3 full lifecycle | ✓ 3× validation/calibration/economic/generalization over real data |
| Phase 4 honest outcome | ✓ three honest negatives, zero promotions |

**All acceptance criteria met.**

## 4. The pivotal properties — verified

1. **The pre-registration discipline is genuine.** The three plan hashes were committed (log lines 12–14) before any training (line 18+). This is not a retrospective claim — the ordering is in the executed record. The primary was not swapped for the better-looking secondary.

2. **The multiple-comparison trap was caught exactly as designed.** Secondary S2 (magnitude target) produced a nominally significant p = 4.55e-05 — a "significant-looking" result — but its **effect +0.0331 is below the +0.05 floor**, its **calibration is worse than chance** (ECE 0.444, Brier 0.4685 vs the 0.25 null), and its **economics are the worst** (net −171,139.5 bps). The fail-closed gate refused it. This is the precise scenario the multiple-comparison discipline was built to expose, and it worked.

3. **The primary's honest verdict:** the expanded 11-feature set finds **no directional structure** — effect +0.00052 (~100× below floor), p=0.853, Brier 0.3099. Combined with B-ML's earlier result, this is now **two governed iterations, two feature sets, two targets**: hourly crypto prediction from price-derived causal features has **no exploitable linear edge** on this corpus. The negative is twice-established with full rigor.

## 5. Findings

### OBS-BML2-1 (Low, transmission — carried pattern)
`bml2_probe_prefix.log.txt` (manifest item 3, hash `e42ffff5…`) is **still** not in my custody, even after the re-relay (5 of 6 evidence artifacts arrived; the probe log did not). The substance is fully verifiable without it (the pre-fix absence of the v2 module is self-evident from the patch, and the fail-first claim is corroborated), so no outcome impact — but the recurring declared-but-untransmitted defect persists into a **sixth** consecutive delivery. This does not block; it reinforces the standing **CA-TRANSMIT-1** escalation already issued: the transmission step must be fixed at the relay.

## 6. Programme consequence

The predictive track has now been tested across **two full governed iterations**:

- B-ML: v1 features (3), direction@H1 → no edge.
- B-ML2: v2 features (11, incl. market-structure, volatility, momentum, volume, session), direction@H1 + magnitude secondary → no edge.

The finding is stable and rigorous: **hourly crypto direction (and magnitude regime) from price-derived causal features carries no exploitable linear signal on this corpus.** The honest negative is twice-established, and the threshold gate has now been proven in the negative direction across a bounded, pre-registered hypothesis space — exactly what it was built to guarantee.

**B-03 (predictive advisory signals) remains gated** — correctly, because no model has been promoted.

Per BO-B-ML2 §12, the next step is the Operator's decision:
- **Further reformulation** (e.g. non-linear models, order-flow features, a different timeframe regime), **or**
- **Broader real asset classes** via a new R1-style data order (the corpus is crypto-only — OBS-BDATA-2), **or**
- **Accept the predictive track's current negative status** and proceed with the rest of the programme (B-04 intelligence, B-05 alerts, B-06 assistant, B-07 hardening, X-01) on the basis that deterministic market-structure analysis is the primary intelligence, with predictive ML a complementary, evidence-gated research effort.

---

## 7. Determination

| Field | Value |
|-------|-------|
| Determination | **APPROVED WITH OBSERVATIONS** |
| Basis | All acceptance criteria met; 4/4 SHAs; pre-registration ordering verified; 5/5 new + 514/514 full suite; multiple-comparison discipline genuinely exercised |
| Observations | OBS-BML2-1 (probe log still absent — carried transmission pattern) |
| Next authorization state | **BO-B-ML2 CLOSED** — but **B-03 remains gated**; predictive-track next step is the Operator's §12 decision |
| What this is not | Not production certification; not gate-opening; not a claim of predictive skill (none exists) |

## 8. Record

- Patch: `1649e26f66bda3107c3e2f0d1e4687b9103b09f7835e46b7eff14cdf678cadb3`
- Post-apply: 4/4 file SHAs · 5/5 new · 514/514 full suite
- Pre-registration: 3 hashes precede training (log lines 12–14 vs 18+)
- Outcome: 3 honest negatives, 0 promotions; primary effect +0.00052, p=0.853

> **We don't guess. We prove.** The predictive track has now been tested twice, rigorously and honestly, and the answer both times is the same: no exploitable linear edge on hourly crypto from these features. That is a real, valuable scientific result — and the gate that kept a "significant-looking" exploratory finding from becoming a promoted model is proof the platform will not manufacture a signal. Approved.

**End of ITRGA Determination BO-B-ML2 (FINAL)**
