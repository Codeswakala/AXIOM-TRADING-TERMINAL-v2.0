# ITRGA FINAL DETERMINATION — UI-NEW-P03

| Field | Value |
|---|---|
| Document type | ITRGA Phase Determination — **final for UI-NEW-P03** (Directive §§29–31; Doc 17 §17.8 Gate 4) |
| Issued by | Independent Technical Review & Governance Authority |
| Date | 2026-08-13 |
| Submission of record | `DELIVERY_REPORT_UI-NEW-P03.md` — sha256 `e0f2bde2da59636502c6af736ea3dc99092b03ed603728758fecdef69b2c4b43` (Rev 4) |
| Revision history | Rev 1 `2e1f8934…` → Rev 2 `c53cfda6…` → Rev 3 `0753d959…` → **Rev 4 `e0f2bde2…`** |
| Delivery commit | `eff7ed1817093852dc3f87ec62d4dd0b5e67755d` · tag `UI-NEW-P03_DELIVERY` → `83774faa…` |
| Baseline of record | 154 suites / 650 frontend tests · 415 backend tests · **1,065 total** · `tsc -b` 0 · `vite build` 0 (`index-CZZFzIoY.js` 670.52 kB) · Alembic `20260717_0037` |
| **DETERMINATION** | **APPROVED WITH OBSERVATIONS** |
| Confidence | **MEDIUM-HIGH** (see §4) |
| Governance Gate | CLOSED · Production NOT CERTIFIED |
| Supersedes | `ITRGA_REVIEW_UI-NEW-P03_REV3.md` (and Rev 1/Rev 2 issues) as the phase-closing instrument |

---

## 1. Basis of determination

Rev 4 differs from Rev 3 in exactly one respect: the §11 named-test transcript carries fresh per-test timings (58/18/30/36/23/54/26 → 59/18/32/37/21/49/14 ms) on an otherwise byte-identical 401-line, 34,595-byte document. The DA re-ran the suite and pasted the genuine output. **OBS-P03-7 is closed.**

Across four revisions the DA has closed every finding within its authority:

| Finding | Closure evidence |
|---|---|
| CA-P03-2 · chart never rendered | 5 captures, 2026-08-13 — candles, TD-029 resampling notice, annotation modal, `/charts`, `/login` |
| CA-P01-1(iii) · logged-out capture | `…121628.png` — open since P01 |
| CA-P03-5 · build evidence integrity | Bundle `BkwIWX2E` → `CZZFzIoY`, 670.36 → 670.52 kB; +1,250 B source → +160 B minified (~0.13 ratio, coherent) |
| CA-P03-3 · degenerate seed | `chart_seed_service.py` sha `cd8e1cea…`; new `test_seed_chart_history_non_degenerate_walk`; backend 414 → **415** |
| CA-P03-4 · dual chart surfaces | Operator disposition recorded; §15 grep re-scoped to `components/chart/` + `ChartWorkspacePage.tsx` |
| OBS-P03-2 · TD-028 line cite | Corrected 41 → **39**, verified against register |
| OBS-P03-4 · seed vs live counters | §19.1 note — seeded bars do not increment live ticks |
| OBS-P03-5 · ITRGA files as DA-created | Removed from §6 |
| OBS-P03-6 · Volume Histogram | Recorded in §10 deviation register |
| OBS-P03-7 · carried transcript | Fresh timings, Rev 4 |

Ten findings closed. The five binding constraints B-P03-1 … B-P03-5 are satisfied — four verified at Level I from rendered captures, B-P03-1 at Level II via the hashed resolver and named test.

## 2. Operator decisions recorded (not ITRGA judgements)

Two items were referred to the Operator and decided by the Operator on 2026-08-13. I record them as exercises of Operator authority; **I did not resolve them and do not represent them as discharged on the evidence.**

**2.1 CA-P03-1 (GA-167) — carried forward as a standing Operator-owned condition on P04.**

State at determination, unchanged across six cycles:

```
grep -c "GA-167"  →  0        register head  →  GA-166
commit eff7ed18…  →  not present at origin
```

The Operator has directed that P03 be approved with this condition carried into P04. That is within Operator authority. My position is unchanged and is preserved here rather than withdrawn:

- The GA-167 register entry remains **unwritten at origin and independently unverifiable**.
- §10 attributes it to Operator Constitutional Authority while §7 shows the **DA** modified `GOVERNANCE_AMENDMENTS.md`. Under `03_AXIOM_SPEC.md` the DA may not author constitutional amendments; if the DA transcribed it, the record is **procedurally defective as to authorship** even though its content is correct.
- Four phases (P01–P04) will now have been built inside a Tier-5 displacement whose constitutional record does not yet exist in the register.

**This condition does not lapse.** It is carried into `BUILD_ORDER_UI-NEW-P04` §1 as a precondition on **P04 delivery approval**, and I will restate it in every subsequent determination until the register is amended and pushed. It is not a defect the DA can cure.

**2.2 CA-P03-6 (capture of the cured seed) — carried into P04 as an observation.**

CA-P03-3 is closed at Level II: the generator is hashed and defended by a passing backend test that would fail if the square wave returned. The Operator has directed that the Level-I capture ride into P04. Recorded as **OBS-P04-1**; I will re-measure the pixel distribution when a seeded capture next appears, and will state in the P04 Build Order that P04 chart evidence must be captured against a **non-degenerate** series.

## 3. Observations carried into P04

| ID | Observation |
|---|---|
| **OBS-P04-1** | Cured seed never rendered for inspection (from CA-P03-6). Re-measure at next capture. |
| **OBS-P01-1** | Delivery work unpushed — `eff7ed18…` and tag absent from origin. This is the mechanism preventing independent verification of GA-167. **Discharge before P05.** |
| **OBS-P01-5** | Captures below 1920×1080 for four consecutive phases. It cost real fidelity in P03: 7 px candle bodies required pixel analysis to adjudicate. |
| **OBS-5** | Bundle 670.52 kB (+9.88 kB over P02). Modest, disclosed; watch cumulative growth through P06. |
| **OBS-P02-1, OBS-P01-4, OBS-P01-6** | Carried unchanged. |

## 4. Statement of confidence

**MEDIUM-HIGH**, and I record the reason rather than round it up.

The engineering evidence is strong: coherent build fingerprints, a real new backend test, correctly scoped greps, and rendered captures for four of five constraints. Had CA-P03-1 been discharged on the evidence, this would be HIGH.

It is not HIGH because the phase closes with its constitutional record unverifiable at Level I, by Operator election rather than by proof. That is a legitimate exercise of your authority and I have given it effect — but the assurance value of this approval is bounded by it, and it would be dishonest of this office to report otherwise.

## 5. Determination

**UI-NEW-P03 (Primary Chart Stage · Multi-Timeframe Controls · Technical Overlays · Research Annotations · Seed Provenance Discipline) is APPROVED WITH OBSERVATIONS.**

Delivery commit `eff7ed18…` / tag `83774faa…` is accepted as the **UI-NEW-P03 delivered baseline of record** at 154 suites / 650 frontend / 415 backend / 1,065 total.

The DA is commended on two specific points. First, the empty-state copy — *"Click Seed (Synthetic) to inject 80 historical bars"* — makes the control name its own effect, which closed the T-6 seeded-history hazard in the interface rather than in a document. Second, the TD-029 resampling notice **cites the debt ID in the UI**. Both are the standard this programme is meant to hold.

## 6. Authorization

**`BUILD_ORDER_UI-NEW-P04` is NOT YET ISSUED.** This determination approves P03; it is not authorization to begin P04.

On issuance, P04 will be bound explicitly: under `00_VISION_AND_PRINCIPLES.md` Principle 1 and `03_AXIOM_SPEC.md`, **no statistical value may be rendered without its uncertainty**, and no calibration figure (ECE, Brier, confidence, attribution) may be computed client-side. P04 is the phase where data-honesty discipline is hardest to hold, and it will carry CA-P03-1 as a §1 precondition on delivery approval.

---

This determination applies only to UI-NEW-P03 and its supporting evidence. It does not constitute production certification.

Governance Gate remains **CLOSED**. Production remains **NOT CERTIFIED**. This determination is **not authorization for the next phase**. No implementation of P04 may begin before `BUILD_ORDER_UI-NEW-P04` is formally issued.

**We don't guess. We prove.**

*— AXIOM ITRGA*
