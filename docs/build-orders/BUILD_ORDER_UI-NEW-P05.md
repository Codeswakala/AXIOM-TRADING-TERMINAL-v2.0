# BUILD ORDER — UI-NEW-P05
## Risk, Portfolio Analytics & Research Journal

| Field | Value |
|---|---|
| Instrument type | ITRGA Build Order (Directive §§29–31) |
| Issued by | Independent Technical Review & Governance Authority |
| Issued to | AXIOM Development Authority (DA) |
| Date | 2026-08-13 |
| Authorization | Operator, 2026-08-13 ("build order authorized") |
| Governing plan | `docs/plans/UI-NEW_ENGINEERING_DESIGN_PLAN.md` §V-P05, §N, §W — sha256 `8834aa91…` |
| Preceding determination | `ITRGA_DETERMINATION_UI-NEW-P04_FINAL.md` — APPROVED WITH OBSERVATIONS |
| Baseline of record | commit `6d98b9f4…` · tag `UI-NEW-P04_DELIVERY` `3feada13…` · 156 suites / 668 frontend / 415 backend / **1,083 total** · `index-4NwsWIhZ.js` 686.88 kB · Alembic `20260717_0037` |
| Governance Gate | CLOSED · Production NOT CERTIFIED |

---

## 1. Preconditions

**1.1 CA-P03-1 (GA-167) — carried, Operator-owned.** Origin still reads head `GA-166`, `grep -c "GA-167"` = 0, and `6d98b9f4…` is absent from origin. Per the Operator's standing decision this condition **binds P05 delivery approval, not P05 implementation**. Work may begin immediately.

> **P05 will not be APPROVED while CA-P03-1 stands.**

Closure: the Operator confirms authorship of GA-167 and the commit is pushed. The DA is **not** to create, edit, or transcribe GA-167.

**1.2 OBS-P01-1 — unpushed work is now a hard prerequisite.** Twelve review cycles of delivery evidence exist only in DA-local custody. **The delivery commit and tag for P05 must be pushed to origin before delivery review begins.** If the DA lacks push rights, say so plainly in §10 and identify who holds them — this is then an Operator action, not a DA failure.

**1.3 OBS-P05-1 — the CA-P04-5 regression guard.** P04's interval-bracketing fix was verified in the UI but no test evidences it. P05 must close this: see §9, test 8.

---

## 2. Purpose & scope

P05 fills the P01 bottom dock — the slot that has rendered `DOCKED SLOT · SCAFFOLD READY` since P01 — with risk analytics, trade planning notes and the research journal.

**IN scope**
1. `TerminalBottomDock.tsx` — tabbed drawer in `terminal-slot-bottom`, replacing the placeholder.
2. **Trade Planning Notes** tab — list and create/edit via `/api/v1/collaboration/trade-plans`.
3. **Research Journal** tab — list and create/edit via `/api/v1/collaboration/journal-entries`.
4. **Risk & Drawdown** tab — read-only, from `/api/v1/intelligence/portfolio-risk-reports`.
5. **Macro Scenarios** tab — read-only, from `/api/v1/intelligence/scenario-reports`.
6. `terminalRiskJournal.test.tsx` + `uinew_p05_security_invariants.test.ts`.

**OUT of scope — held**
- P06 whole-surface audit, whole-frontend token audit, handover.
- Any new backend endpoint, schema, migration, or dependency. Alembic head stays `20260717_0037`.
- Any client-side computation of a risk or statistical quantity (§4).
- Order book / depth ladder (C-1, permanent). Actuation of any kind (T-1).
- Retiring or altering `/charts` — that disposition is settled and out of scope.

---

## 3. 🔴 B-P05-1 — Trade plans are research notes; they carry no position semantics

This is the governing constraint of the phase. P05 is the second mutating phase, and "trade plan" is the most dangerous phrase in the programme.

`TradePlanNoteWrite` is the authoritative contract:

```
title, market_context, hypothesis, linked_signal_ids, linked_report_ids,
scenario_notes, risk_notes, invalidating_conditions_text,
decision_status: Literal["draft","archived","reviewed"]
```

**There is no entry price, no stop, no target, no size, no lot, no leverage, no side, no account.** The model is deliberately free of them.

- The form must expose **only** the fields above. No additional inputs, no "optional" numeric price fields, no side selector.
- `decision_status` renders exactly its three literal values. `"reviewed"` must not be styled or labelled as approval, authorisation, or readiness to trade.
- `research_disclaimer` is returned on every read and **must render on every plan**, not once per drawer.
- No aggregate across plans that implies a book: no net exposure, no combined risk, no plan count framed as positions.
- The tab is labelled for research. `T-3` read-only trading representations applies in full.

**Required:** a table in the delivery report mapping every form input to its `TradePlanNoteWrite` field. Any input without a backing field is a defect.

## 4. 🔴 B-P05-2 — Risk metrics render with their uncertainty and their assumptions

`PortfolioRiskReportRead` carries:

```
max_drawdown: float · realized_volatility: float · stress_loss: float
metrics: dict · uncertainty: dict · assumptions: dict · sample_count: int
input_lineage: dict · as_of_start / as_of_end
```

The P04 precedent governs: under `00_VISION_AND_PRINCIPLES.md` Principle 1, **no statistical value may be rendered without its uncertainty**, and none computed client-side.

- `max_drawdown`, `realized_volatility` and `stress_loss` must each render with their interval from `uncertainty`, or an explicit `[Uncertainty: Unavailable]` qualifier. **Bare risk numbers are prohibited.**
- **Every rendered interval must bracket its own point estimate** (`lower ≤ p ≤ upper`). This is the CA-P04-5 rule, now binding by name.
- `stress_loss` must render with its `assumptions` accessible without navigation. A stress number without its scenario assumptions is a misrepresentation.
- `as_of_start`/`as_of_end` and `sample_count` render with every metric — a risk figure without its window is meaningless.
- Zero client-side computation: no ratios, no annualisation, no re-scaling, no summing drawdowns. Format only.

## 5. 🔴 B-P05-3 — The journal is a record, and records must not silently change

`PUT /collaboration/trade-plans/{plan_id}` and `PUT /collaboration/journal-entries/{journal_id}` exist. **P05 is therefore the first phase with an edit path**, and edits to a research record carry audit weight.

- `created_at`, `updated_at` (plans) and `audit_correlation_id` must be visible on every record.
- Where a record has been edited (`updated_at` ≠ `created_at`), the UI must **say so visibly**. A silently-rewritten journal entry defeats the purpose of a journal.
- No delete affordance. The API exposes none; the UI must not imply one.
- `research_status` and `research_disclaimer` render on every entry.
- `emotion_tags` and `process_tags` render verbatim as operator-entered text. They must not be scored, aggregated into a sentiment metric, or interpreted.
- `linked_signal_ids` / `linked_report_ids` / `linked_plan_id` render as provenance links only — never as evidence that a plan was acted upon.

## 6. 🔴 B-P05-4 — The dock is presentation; tabs must not lose state or fabricate content

Plan §W acceptance for P05: *"Bottom dock tabs switch smoothly without layout jumps; research notes save to audit log."*

- Four tabs switch without unmounting the chart or watchlist, and without layout shift in the panes above.
- Empty states are explicit and honest, in the P03 idiom: no empty tab may render as a blank panel. Name what is absent and why.
- A failed write renders an explicit error. **Never** an optimistic success. P04's Rev 3 `Request failed (500)` on `/seed-history` reached an Operator screen undisclosed; that must not repeat in a write path.
- No draft may be presented as persisted until the API confirms it.

## 7. 🔴 B-P05-5 — Zero actuation, restated for a mutating phase

T-1 is absolute and P05 is where it will be tested hardest.

- Zero buy/sell/execute/order/broker/account/position/balance/margin controls or fields, anywhere in the dock.
- No control whose label implies action on a market: no "Execute Plan", "Activate", "Go Live", "Send".
- Writes go **only** to `/collaboration/trade-plans` and `/collaboration/journal-entries`. No other mutating endpoint may be called from the dock.
- Every write surface carries `RESEARCH-ONLY · NON-ACTUATING`.
- T-4 / T-5: no external LLM may generate, summarise, autocomplete or rewrite any plan, hypothesis, reflection or lesson field.

## 8. Conditions carried

| ID | Condition | Status in P05 |
|---|---|---|
| CA-P03-1 | GA-167 unrecorded | **Blocks P05 delivery approval** (§1.1) |
| OBS-P01-1 | Work unpushed | **Hard prerequisite for delivery review** (§1.2) |
| OBS-P05-1 | No bracketing test | Close via §9 test 8 |
| OBS-P04-8 | Chart chips render bare percentages | Close or record as accepted debt |
| OBS-P04-6 | `Feed Lag: 1376.3849999999998 ms` raw float | **Close this phase** — third cycle |
| OBS-P04-3 | `terminalWatchlistDepth.test.tsx` absent from §7 | Explain or restore — fourth cycle |
| C-1 / T-1 / T-4 / T-5 | Permanent exclusions | Absolute |
| B-P02-1 | Field provenance discipline | Extend the table to all P05 fields |
| OBS-5 | Bundle growth | Disclose delta; justify if > +25 kB |

## 9. Mandatory named tests

Eight tests, displayed **passing by name** under the Vitest verbose reporter, in `terminalRiskJournal.test.tsx`:

1. `test_uinew_p05_trade_plan_form_exposes_no_price_stop_target_size_or_side_fields`
2. `test_uinew_p05_trade_plans_and_journal_entries_render_disclaimer_and_audit_correlation_id`
3. `test_uinew_p05_edited_records_visibly_disclose_updated_at_distinct_from_created_at`
4. `test_uinew_p05_risk_metrics_never_render_without_uncertainty_or_explicit_unavailable`
5. `test_uinew_p05_stress_loss_renders_with_its_assumptions_and_sample_window`
6. `test_uinew_p05_no_client_side_computation_of_drawdown_volatility_or_stress_values`
7. `test_uinew_p05_failed_writes_render_explicit_error_and_never_optimistic_success`
8. `test_uinew_p05_every_rendered_interval_brackets_its_own_point_estimate` — **closes OBS-P05-1; must cover P04 signal cards and P05 risk metrics**

Plus `uinew_p05_security_invariants.test.ts` covering T-1, T-3, T-4, T-5, T-6, T-7, S-1…S-5, C-1 and SAL classification.

**Floors, not targets.** Add what the implementation warrants; do not pad.

## 10. Mandatory evidence

(a) Delivery commit SHA + annotated tag `UI-NEW-P05_DELIVERY` with `git rev-parse` output — **pushed to origin** (§1.2).
(b) SHA-256 for **every** created and modified file. No placeholders (CA-P03-3 precedent).
(c) Full suite counts against **the delivered commit**, fresh transcript. Bundle hash must differ from `index-4NwsWIhZ.js` / 686.88 kB if any frontend source changed (CA-P03-5 precedent). If a named test is claimed, it must appear in the transcript (OBS-P05-1 precedent).
(d) Raw grep transcripts: T-1 (including `position`/`balance`/`margin`), T-4/T-5, C-1, secrets, `dangerouslySetInnerHTML`/`eval`/`new Function`, ad-hoc hex across **all** touched directories.
(e) Field-provenance table extended to every P05 field, including the B-P05-1 form-input mapping and the B-P05-2 uncertainty mapping.
(f) **Level-I captures at 1920×1080, attached to the submission as image files** (CA-P04-1 precedent — filenames and digests alone are not evidence): (i) Trade Planning tab with at least one plan showing disclaimer and audit ID; (ii) the create/edit form, showing no price/stop/size fields; (iii) Research Journal tab with an **edited** entry disclosing `updated_at`; (iv) Risk & Drawdown tab with metrics rendering intervals and assumptions; (v) an explicit write-failure or empty state.
(g) Deviation register — if zero, state zero and mean it.
(h) Technical debt reconciliation, verbatim quotations, correct line numbers.

## 11. Acceptance criteria

P05 is approvable when: B-P05-1…B-P05-5 are satisfied; the eight named tests display passing; the 1,083-test baseline is maintained or grown with no regression; `tsc -b` and `vite build` exit 0 against the delivered commit; Alembic head unchanged; evidence (a)–(h) complete; the commit is readable at origin; **and CA-P03-1 is closed by the Operator.**

## 12. Authorization

The DA is authorized to implement UI-NEW-P05 as scoped above, effective immediately.

This Build Order is not an approval of any future delivery. Correction is not approval. The DA may not self-approve. The Governance Gate remains **CLOSED**; production remains **NOT CERTIFIED**; no P06 implementation may begin before `BUILD_ORDER_UI-NEW-P06` is formally issued.

**We don't guess. We prove.**

*— AXIOM ITRGA*
