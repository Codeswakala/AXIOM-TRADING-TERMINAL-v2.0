# BUILD ORDER — UI-NEW-P04
## Quantitative Signals, Intelligence & Uncertainty Stream

| Field | Value |
|---|---|
| Instrument type | ITRGA Build Order (Directive §§29–31) |
| Issued by | Independent Technical Review & Governance Authority |
| Issued to | AXIOM Development Authority (DA) |
| Date | 2026-08-13 |
| Authorization | Operator, 2026-08-13 ("build order authorized") |
| Governing plan | `docs/plans/UI-NEW_ENGINEERING_DESIGN_PLAN.md` §V-P04, §N, §W — sha256 `8834aa91…` |
| Preceding determination | `ITRGA_DETERMINATION_UI-NEW-P03_FINAL.md` — APPROVED WITH OBSERVATIONS |
| Baseline of record | commit `eff7ed18…` · tag `UI-NEW-P03_DELIVERY` `83774faa…` · 154 suites / 650 frontend / 415 backend / **1,065 total** · `index-CZZFzIoY.js` 670.52 kB · Alembic `20260717_0037` |
| Governance Gate | CLOSED · Production NOT CERTIFIED |

---

## 1. Precondition carried from P03 — CA-P03-1

`GA-167` remains unrecorded at origin (`grep -c "GA-167"` = 0; register head `GA-166`) and commit `eff7ed18…` is absent from origin. Per the Operator's decision of 2026-08-13, P03 was approved with this condition **carried forward as a standing Operator-owned condition on P04**.

**This precondition binds P04 delivery approval, not P04 implementation.** The DA may begin work immediately. But:

> **P04 will not be APPROVED while CA-P03-1 stands.**

Two acts close it, both Operator-authorised: confirm authorship of GA-167 (the DA may not author constitutional amendments — `03_AXIOM_SPEC.md`), and push the delivery commit so the register is independently readable. **OBS-P01-1 (unpushed work) must discharge before P05 regardless.**

The DA is **not** to create, edit, or transcribe `GA-167`. If it is already transcribed in DA-local custody, say so plainly in §10 and identify who wrote it.

---

## 2. Purpose & scope

P04 docks quantitative advisory signals and institutional intelligence into the P01 right-dock, and overlays signal markers onto the P03 chart canvas.

**IN scope**
1. `TerminalSignalStream.tsx` — advisory signal feed in the right dock, consuming `GET /api/v1/signals/history`.
2. Signal markers overlaid on the P03 chart canvas at their `as_of_time` / symbol / timeframe.
3. Docked intelligence cards — cross-asset correlation and market-regime detection — from `GET /api/v1/intelligence/correlation-reports` and `/regime-reports`.
4. Calibration disclosure surface consuming `/api/v1/intelligence/signal-validation-reports`.
5. `terminalSignalsIntelligence.test.tsx` + `uinew_p04_security_invariants.test.ts`.

**OUT of scope — held**
- P05 bottom dock (trade plans, journal, scenarios, risk decomposition) — slot stays a placeholder.
- P06 whole-surface audit.
- Any new backend endpoint, schema, migration, or dependency. Alembic head stays `20260717_0037`.
- Any client-side computation of a statistical quantity (see B-P04-2).
- Order book / depth ladder (C-1, permanent). Actuation of any kind (T-1).

**Corrected path.** The plan §V-P04 cites `/api/v1/signals/history`. The router is `app/api/routes/advisory_signals.py` with `prefix="/signals"`, so the operative path **is** `/api/v1/signals/history` — plan and code agree. The file name differs from the plan's implication; that is not a defect and requires no action.

---

## 3. 🔴 B-P04-1 — The signal contract carries confidence but no bounds

This is the governing constraint of the phase, and the DA must resolve it before writing UI.

`AdvisorySignalRead` (`backend/app/models/advisory_signal.py`) exposes:

```
calibrated_confidence: float | None
raw_score:             float | None
calibration_status:    str
calibration_report_id: str | None
freshness_status:      str | None
input_staleness_seconds: int | None
explainability_summary:  dict[str, Any]
```

**There is no uncertainty, interval, lower, or upper field on the signal.** Wilson score intervals exist, but in a different subsystem — `app/institutional_intelligence/signal_validation.py` returns `{method: "wilson_score_interval", lower, upper, confidence_level, sample_count}` under `/intelligence/signal-validation-reports`.

`00_VISION_AND_PRINCIPLES.md` Principle 1 and `03_AXIOM_SPEC.md` require that **no statistical value be rendered without its uncertainty.** Therefore:

- Rendering `calibrated_confidence` as a bare percentage **violates Principle 1** and is prohibited.
- The DA must bind confidence to its interval by joining `calibration_report_id` / the signal-validation report, and render both together, or
- Where no interval is retrievable for a given signal, the UI must render the confidence **with an explicit "uncertainty unavailable" qualifier** — never a naked number.

**The existing `AdvisorySignalsPage.tsx` renders `formatConfidence(signal.calibrated_confidence)` inside a `confidence-box` with no bounds.** The DA must not replicate that pattern into the terminal. If the DA judges the existing page non-compliant, **report it as a finding in §10 — do not fix it**; it is outside P04 scope and belongs to a remediation Build Order.

**Required:** a table in the delivery report mapping every rendered statistical value to its uncertainty source, or to its explicit unavailability qualifier.

## 4. 🔴 B-P04-2 — Zero client-side statistics

No ECE, Brier score, Wilson interval, calibration bin, base rate, correlation coefficient, or regime probability may be computed in the browser. Every such figure is rendered **only** as received from the backend.

Backend computes these server-side today — `brier`, `ece`, and bin schemes in `app/ml/calibration/service.py`; Wilson bounds in `signal_validation.py`. The frontend's job is formatting and disclosure, nothing else.

Permitted client-side: unit conversion for display (e.g. `0.732` → `73.2%`), rounding with disclosed precision, and sorting/filtering. **Prohibited:** any arithmetic that produces a new statistical claim, including averaging confidences across signals, deriving a "net bias," or aggregating regime scores.

## 5. 🔴 B-P04-3 — Signals are advisory research notes, never instructions

`signal_direction` will contain directional values. Rendering them is permitted; **framing them as instruction is not.**

- No imperative language: no "Buy", "Sell", "Enter", "Exit", "Take profit", "Act now".
- Direction must render with its governing state — `signal_state`, `state_reason`, `eligibility_reasons`, `operating_domain_status`, `economic_verdict` — never in isolation.
- `withheld`, `expired`, and `superseded` states must be visually distinct from `emitted` and must **not** be silently filtered out. Suppressing withheld signals would misrepresent model behaviour.
- Every signal surface carries `RESEARCH-ONLY · NON-ACTUATING`.
- `risk_notes` and `rationale` render verbatim; no summarisation, no truncation without an explicit expand affordance.

## 6. 🔴 B-P04-4 — Freshness and staleness are honesty surfaces

`freshness_status`, `input_staleness_seconds`, `signal_validity_seconds`, and `expires_at` exist precisely so a stale signal cannot masquerade as current.

- An expired or stale signal must be **visibly** marked as such, not merely sorted lower.
- `expires_at` in the past ⇒ explicit expired treatment.
- Never render a signal without its as-of time. Relative times ("3m ago") must be accompanied by the absolute UTC timestamp, consistent with the P01 clock discipline.

## 7. 🔴 B-P04-5 — Model provenance is mandatory, per signal

Every rendered signal must expose, without requiring navigation away: `model_artifact_id`, `model_version`, `feature_set_version`, and `inference_input_hash` (truncation permitted with full value available on hover/expand).

`explainability_summary` renders as **feature attribution only**. It must not be reframed as a causal claim, a recommendation, or a narrative. No external LLM may generate, summarise, or rewrite any part of it (T-4, T-5).

## 8. Conditions carried from P01–P03

| ID | Condition | Status in P04 |
|---|---|---|
| CA-P03-1 | GA-167 unrecorded | **Blocks P04 delivery approval** (§1) |
| OBS-P04-1 | Cured seed never rendered | Chart evidence in P04 must be captured against a **non-degenerate** series; ITRGA will re-measure pixels |
| OBS-P01-1 | Work unpushed | **Discharge before P05** |
| OBS-P01-5 | Captures below 1920×1080, four phases | §10(f) captures **must** be 1920×1080 |
| C-1 | No order book / depth ladder | Permanent exclusion |
| T-1 | Zero actuation | Absolute |
| T-4 / T-5 | Zero external LLM; assistant subordination | Absolute |
| B-P02-1 | Field provenance discipline | Extend the §19.1 table to all P04 fields |
| OBS-5 | Bundle growth | Disclose delta; justify if > +25 kB |

## 9. Mandatory named tests

Seven tests, displayed **passing by name** under the Vitest verbose reporter, in `terminalSignalsIntelligence.test.tsx`:

1. `test_uinew_p04_signal_stream_renders_only_backend_signals_with_no_client_fabrication`
2. `test_uinew_p04_calibrated_confidence_never_renders_without_uncertainty_or_explicit_unavailable`
3. `test_uinew_p04_no_client_side_computation_of_ece_brier_wilson_or_correlation`
4. `test_uinew_p04_signal_direction_renders_with_state_and_never_as_instruction`
5. `test_uinew_p04_withheld_expired_and_superseded_signals_remain_visible_and_distinct`
6. `test_uinew_p04_stale_and_expired_signals_are_explicitly_marked_with_absolute_utc_time`
7. `test_uinew_p04_model_version_feature_set_and_input_hash_render_for_every_signal`

Plus `uinew_p04_security_invariants.test.ts` covering T-1, T-4, T-5, T-6, T-7, S-1…S-5, C-1, and SAL classification.

**These are floors, not targets.** Add whatever the implementation warrants; do not pad.

## 10. Mandatory evidence

(a) Delivery commit SHA + annotated tag `UI-NEW-P04_DELIVERY` with `git rev-parse` output.
(b) SHA-256 for **every** created and modified file — no "Verified Fix" placeholders (CA-P03-3 precedent).
(c) Full suite counts against **the delivered commit**, with a fresh transcript. Bundle hash and size **must** differ from `index-CZZFzIoY.js` / 670.52 kB if any frontend source changed (CA-P03-5 precedent).
(d) Raw grep transcripts: T-1, T-4/T-5, C-1, secrets, `dangerouslySetInnerHTML`/`eval`/`new Function`, and ad-hoc hex — the hex grep scoped across **all** touched directories, not just `components/terminal/`.
(e) Field-provenance table extended to every P04 field, including the B-P04-1 uncertainty mapping.
(f) **Level-I captures at 1920×1080**: (i) signal stream with at least one `emitted` signal showing confidence **with** bounds; (ii) a `withheld` or `expired` signal rendered distinctly; (iii) signal markers on the chart over a **non-degenerate** seeded series; (iv) an intelligence card (correlation or regime); (v) a signal with uncertainty **unavailable**, showing the qualifier.
(g) Deviation register — if zero, state zero explicitly and mean it.
(h) Technical debt reconciliation with **verbatim** quotations and **correct line numbers** (CA-P01-2 / OBS-P03-2 precedent).

## 11. Acceptance criteria

P04 is approvable when: all five constraints B-P04-1…B-P04-5 are satisfied; the seven named tests display passing; the 1,065-test baseline is maintained or grown with no regression; `tsc -b` and `vite build` exit 0 against the delivered commit; Alembic head unchanged; evidence (a)–(h) complete; **and CA-P03-1 is closed by the Operator.**

Plan §W acceptance for P04 — *"ML advisory signals render with calibrated confidence percentages; uncertainty intervals format deterministically"* — is met only when confidence and interval render **together**, per B-P04-1.

## 12. Authorization

The DA is authorized to implement UI-NEW-P04 as scoped above, effective immediately.

This Build Order is not an approval of any future delivery. Correction is not approval. The DA may not self-approve. The Governance Gate remains **CLOSED**; production remains **NOT CERTIFIED**; no P05 implementation may begin before `BUILD_ORDER_UI-NEW-P05` is formally issued.

**We don't guess. We prove.**

*— AXIOM ITRGA*
