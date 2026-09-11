# ITRGA DETERMINATION — BO-B-02
## ML Research Machinery Executed + Substantive-Threshold Gate

| Item | Value |
|------|-------|
| Review identity | ITRGA independent review of DA Delivery Report `DELIVERY_REPORT_B-02.md` |
| Build Order | `BO-B-02` (Operator-authorized 2026-08-19) |
| Predecessors | BO-B-00 APPROVED-WITH-OBS · BO-B-01 APPROVED-WITH-OBS |
| Date | 2026-08-19 |
| Evidence standard | Level I (direct) / Level II (executed) / Level III (documentary) |

---

## 1. What I verified (Level I/II — reproduced independently)

| Check | Result |
|-------|--------|
| Patch `b02.patch.txt` sha256 | `d5e4a3c8…` — **matches** report |
| `git apply --check` + apply | **Clean** (exit 0) |
| 8 post-apply file SHAs | **All 8 match** the report's cited hashes exactly |
| New B-02 tests (threshold gate + lifecycle) | **11/11 passed** |
| Churned files (deviation D1: `test_live_inference_gate` + `test_signal_guardrails`) | **11/11 passed** |
| **Full backend suite** | **500 passed** (136.78s) — matches report (500 / 138.05s) |
| Transmission manifest (CA-B01-1) | **Complete** — all 6 declared artifacts present, SHAs verified |
| Threshold gate code | **Enforces real numeric checks** — fail-closed on malformed/absent values, per-gate reasons |

## 2. Acceptance criteria vs. Build Order — line-by-line

| BO requirement | Status |
|-----------------|--------|
| B-02.1 lifecycle executed (pre-register→…→eligibility) | ✓ 1 approved experiment, 1 model artifact, all 4 report types, honest eligibility evaluation |
| B-02.1 tier + data-class labels on all artifacts | ✓ pipeline_validation tier + synthetic labels persisted in notes |
| B-02.1 honest NOT-eligible decision recorded | ✓ eligible=False with 3 threshold reasons + NOT_ADVISORY_APPROVED; promotion refused |
| B-02.2 threshold framework documented (ADR) | ✓ `SUBSTANTIVE_THRESHOLD_FRAMEWORK.md` — numeric criteria per gate |
| B-02.2 gate enforces thresholds in code + new reasons | ✓ 4 new rejection reasons, enforced in `evaluate()` + `promote_to_advisory_approved()` |
| B-02.2 baseline fails, recorded not overridden | ✓ dev-DB run: accuracy 0.5134, effect +0.0134, p=0.239, Brier 0.2499, net −11,524 bps → 3 refusals, nothing overridden |
| B-02.3 generalization as distinct governed question | ✓ domain scope + hold-out separation + independence recorded |
| §7 calibration-probability gap disclosed | ✓ degenerate-prior probabilities with explicit `PROBABILITIES_ARE_DEGENERATE` label; Brier threshold still rejects |
| §3 exclusions | ✓ no promotion, no skill claims, no fabricated data, no new families, no inference/signals, no frontend, no gate/actuation |
| §8 standing-dependency note | ✓ R1/R2 correctly stated, nothing substituted |
| §9 CA-B01-1 transmission manifest | ✓ complete and verified |

**All acceptance criteria met.**

## 3. The pivotal properties — verified in both directions

1. **The gate fails closed.** `test_b02_malformed_report_fails_closed` + the four `*_THRESHOLD_NOT_MET` tests prove a present-but-failing/malformed report withholds. The code (`_statistical_threshold_reason` etc.) returns the reason on unparsable/absent values — "unverifiable is unpassable."

2. **The gate is not permanently closed.** `test_b02_gate_passes_all_thresholds_and_promotes` proves a genuinely threshold-passing model *is* eligible and promotable. This is the correct design: the gate enforces substance, it doesn't ban promotion.

3. **The baseline failed honestly, for the right reasons.** The majority-class baseline produced accuracy 0.5134 (effect +0.0134 < 0.05), Brier 0.2499 (> 0.20), economic net −11,524 bps → refused on STATISTICAL + CALIBRATION + ECONOMIC. Nothing was overridden. This is exactly the §5 correction ("reports exist ≠ eligible") made real.

## 4. Deviation D1 — reviewed and accepted, with one observation

Deviation D1 churned `test_signal_guardrails.py` (3 tests) and `test_live_inference_gate.py` (fixture). The report discloses this fully: the W3-U03 "warning tier" for post-promotion calibration/economic degradation is now **hard-withheld at emit** for threshold-failing values, with the warning tier retained only for within-threshold values.

**Assessment:** the change is directionally correct and *stricter* (fail-closed at emit), no test was deleted, no assertion weakened, and I independently confirmed 11/11 green on both churned files. 

**OBS-B02-1 (Info, semantic tightening):** the re-pinning of three W3-U03 tests changes the *behavioral contract* of the signal layer (from "warn on degradation" to "withhold on threshold-failing degradation"). This is a real semantic change to a previously-ITRGA-approved unit's behavior. It is justified — the BO-B-02 threshold gate logically supersedes a softer warning — but it should be recorded as a deliberate cross-unit semantic upgrade in `PROJECT_STATE.md`/the amendments register at the next documentation-touching unit, so the historical record reflects *why* W3-U03's warning tier narrowed. Not a defect; not blocking.

## 5. Standing dependency — Operator decision still required (unchanged from BO-B-02 §8)

This unit correctly **did not and could not** produce a promotable model, because:
- the corpus is synthetic (tier rule), and
- real historical market data does not exist in this project.

The substantive ML path — and therefore B-03 signal production with an eligible model — remains **blocked** on the Operator's R1/R2 decision:
- **R1** — authorize acquisition of real historical data (a future, separately-governed unit), or
- **R2** — accept the substantive path stays blocked until real data exists.

No amount of pipeline machinery (however well-executed, as here) removes this. I flag it as the single most important open item for the programme.

## 6. Other observations (non-blocking)

- **OBS-B02-2 (Info, carried):** `PROJECT_STATE.md` test inventory still stale (OBS-B00-3) — now further behind (executed 500 vs recorded 415/414).
- **OBS-B02-3 (Info, carried):** fixture-convention source labels (`sample:*` → AUTHORITATIVE) remain (OBS-B01-2) — a latent honesty risk for future real-data ingestion; should be tightened before any real-data acquisition (R1).

---

## 7. Determination

| Field | Value |
|-------|-------|
| Determination | **APPROVED WITH OBSERVATIONS** |
| Basis | All BO acceptance criteria met; 8/8 SHAs reproduced; 11/11 new + 11/11 churned + 500/500 full suite independently executed; gate verified fail-closed and threshold-driven in code; transmission manifest complete |
| Observations | OBS-B02-1 (signal-layer semantic tightening — record at next doc unit), OBS-B02-2, OBS-B02-3 (non-blocking) |
| Next authorization state | **B-02 CLOSED** — but B-03 (signals) is **gated on the Operator's R1/R2 real-data decision** |
| What this is not | Not production certification; not gate-opening; not authorization beyond BO-B-02 |

## 8. Record

- Patch sha256: `d5e4a3c876c0bff826cc05f3e9dd58a3f9382607df3bc5a93acbf253a035b1fe`
- Post-apply: 8/8 file SHAs · 11/11 new · 11/11 churned · 500/500 full suite
- Gate: fail-closed, threshold-driven, positive-promotion path proven

> **We don't guess. We prove.** The ML machinery now runs end-to-end under governance, and the promotion gate enforces substance, not existence. The baseline failed honestly, for the right reasons, and nothing was overridden. Approved.

**End of ITRGA Determination BO-B-02**
