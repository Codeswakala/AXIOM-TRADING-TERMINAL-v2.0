# BUILD ORDER — UI-CONV-P02
## Duplicate Surface Absorption & Single Statistical Code Path

| Field | Value |
|---|---|
| Instrument type | ITRGA Build Order (Directive §§29–31) — **second phase of the CONVERGENCE programme** |
| Issued by | Independent Technical Review & Governance Authority |
| Issued to | AXIOM Development Authority (DA) |
| Date | 2026-08-13 |
| Authorization | Operator, 2026-08-13 ("authorized") |
| Governing blueprint | `AXIOM_UI_TRANSFORMATION_BLUEPRINT.md` §4, §5 |
| Preceding determination | `ITRGA_DETERMINATION_UI-CONV-P01_FINAL.md` — APPROVED WITH OBSERVATIONS |
| Baseline of record | `UI-CONV-P01_DELIVERY` · 1,119+ platform tests · Alembic `20260717_0037` |
| Governance Gate | CLOSED · Production NOT CERTIFIED |

---

## 1. Preconditions

**1.1 CA-P03-1 (GA-167) — carried, Operator-owned, 15 cycles.** Origin head `GA-166`. Binds **delivery approval**, not implementation. The DA is **not** to create, edit, or transcribe GA-167.

**1.2 F-BRAND-1 — the compass+Epsilon mark remains BLOCKED** pending Operator-recorded **GA-173** (Doc 16 §262). The AX Monogram is retained. Staged assets stay unmounted.

**1.3 OBS-CERT-2 — corpus at origin.** Declare status plainly in §10; push rights are Operator-held.

---

## 2. Purpose & scope

This is the phase the programme has been building toward since P03. It eliminates the duplicate surfaces that caused `CA-P03-4` and created the conditions for the fabricated-Brier defect.

**IN scope**
1. Absorb `/charts` into the terminal chart stage; retire `ChartWorkspacePage.tsx` (868 lines) and the `/chart` alias.
2. Absorb `/signals` into the SIGNALS dock; retire `AdvisorySignalsPage.tsx` (328 lines).
3. Absorb `/analytics` into the INTELLIGENCE dock; retire `PerformanceAnalyticsPage.tsx` (186 lines).
4. **Single statistical rendering path** (§3) — one component renders any given statistic, everywhere.
5. `PriceChart.tsx` token remediation (§5).
6. Signal **detail drill-down** so no capability is lost in absorption (§4).
7. `uiconv_p02_absorption.test.tsx` + `uiconv_p02_security_invariants.test.ts`.

**OUT of scope — held**
- Re-homing investigate / compare-scenarios / portfolio-research / research-management / governance / workspace — **CONV-P03**.
- Any new indicator, drawing tool, or chart capability — CHART programme.
- Any new backend endpoint, schema, migration or dependency. Alembic stays `20260717_0037`.
- The compass+Epsilon mark (§1.2).
- Order entry, order book, depth ladder — permanently excluded.

---

## 3. 🔴 B-CONV2-1 — One statistic, one code path

This is the governing constraint. I have measured the defect it exists to remove.

`AdvisorySignalsPage.tsx:56` defines `formatConfidence()` and renders at line 224:

```tsx
<strong>{formatConfidence(signal.calibrated_confidence)}</strong>
```

**A bare percentage with no uncertainty** — the exact pattern I prohibited in Build Order P04 §3 and that the terminal was built to avoid. Meanwhile `PerformanceAnalyticsPage.tsx:21` defines a *second*, independent `intervalText()` implementation with its own `uncertainty.lower/upper` handling and its own withholding logic at line 109.

So the platform currently renders calibrated confidence through **three** separate code paths — two legacy, one terminal — with different rules. That is precisely how a Brier score came to be sourced from an endpoint that never returned one.

**Required:**
- Exactly **one** shared component renders calibrated confidence, and **one** renders a metric-with-interval. Both live in the terminal component tree and are consumed everywhere.
- `formatConfidence` and `intervalText` in the legacy pages are **deleted, not adapted**.
- Every rendered statistic satisfies the standing invariant: bound to its own uncertainty, or an explicit `[Uncertainty: Unavailable]`; **every interval brackets its own point estimate** (`lower ≤ p ≤ upper`).
- No statistic is computed client-side (B-P04-2).
- The delivery report must contain a **statistic-to-component map**: every rendered statistic → the single component that renders it. Two entries pointing at different components for the same statistic is a defect.

**Note the good precedent to preserve.** `PerformanceAnalyticsPage.tsx:109` renders *"Metric withheld: uncertainty missing"* — the legacy page already refuses to show a number it cannot qualify. Carry that behaviour into the shared component; do not lose it in the merge.

## 4. 🔴 B-CONV2-2 — Absorb without losing capability

`ChartWorkspacePage.tsx` is 868 lines and carries affordances the terminal stage may not have: `Seed history`, `Reload history`, `Stop feed`, `bars=500`, CSV provenance labelling, and its own annotation surface. `AdvisorySignalsPage.tsx` carries filter dropdowns (market/symbol/timeframe/state) and a **signal detail view** with rationale, guardrails, lineage and explainability summary — richer than the terminal's signal card.

- **Inventory before deletion.** Produce a capability inventory for each retired page: affordance → new home → evidence. Anything without a home is a **deviation**, recorded, not dropped.
- The signal **detail drill-down** must exist in the terminal — opening a signal card reveals rationale, guardrails (state reason, domain, economic verdict, freshness, expires-at), lineage (model, experiment, feature set, calibration report) and explainability summary. This is `/investigate`'s substrate too; build it once.
- `/charts`, `/chart`, `/signals`, `/analytics` **redirect** to the terminal with the appropriate dock activated. No route 404s. Deep links continue to resolve.
- Retired files are **deleted**, not orphaned in the tree. Report line counts removed.

## 5. 🔴 B-CONV2-3 — `PriceChart.tsx`: remediate or retire

Baseline still carries seven hardcoded literals:

```
26: UP   = "#3dd68c"     29: TEXT = "#9aa8bc"     117: color     = "#3d8bfd"
27: DOWN = "#f31260"     30: BG   = "#0b0e11"     122: lineColor = "#3d8bfd"
28: GRID = "#1e2633"
```

P04 §7 reported this file cured; P06 §4 found literals persisting. **That reconciliation discrepancy closes here.**

- If `PriceChart.tsx` survives absorption, every literal resolves through `getComputedToken` against `--ix-*`. If it does not survive, delete it and say so.
- Whole-frontend ad-hoc hex audit, raw transcript, **honest count**. P06 established the baseline at two files; `global.css` closed in CONV-P01. State the true remaining count — a scoped zero will be treated as incorrectly scoped.
- `TD-005` status updated accordingly.

## 6. 🔴 B-CONV2-4 — Constitutional constraints, unchanged

- **T-1** — zero actuation anywhere in the absorbed surfaces, docks, or redirects.
- **C-1** — no order book, depth ladder, bid/ask size. `TD-023` is to be closed **WONTFIX** in the debt register this phase, with C-1 cited.
- **T-4 / T-5** — no external LLM generates, summarises or rewrites signal rationale, explainability text, or any operator-facing content.
- **T-6** — provenance labelling survives absorption: `seed:synthetic` vs `live:simulated` distinctions, and the TD-029 resampling notice, must render in the terminal exactly as they did on the retired pages.
- **Doc 16 B-7** — never colour alone.

## 7. Conditions carried

| ID | Condition | Status in CONV-P02 |
|---|---|---|
| CA-P03-1 | GA-167 unrecorded | **Blocks delivery approval** — Operator |
| F-BRAND-1 | Compass+Epsilon mark | **Blocked pending GA-173** |
| OBS-CONV-2 | `prefers-reduced-motion` unevidenced | **Close this phase** — Level-I capture |
| OBS-CONV-3 | Palette route coverage Level-II only | **Close this phase** — empty-query capture |
| OBS-CONV-4 | Capture 06 not attached | Re-attach |
| OBS-CONV-5 | No corrective-actions ledger in Rev 2 | **Reinstate the ledger** |
| OBS-CERT-3 | `PriceChart.tsx` fallbacks | **Closes here** (§5) |
| OBS-5 | Bundle growth | Expect a **decrease** — 1,382 lines retired. Justify any increase. |

## 8. Mandatory named tests

Eight, displayed **passing by name**, in `uiconv_p02_absorption.test.tsx`:

1. `test_uiconv_p02_calibrated_confidence_renders_through_exactly_one_shared_component`
2. `test_uiconv_p02_no_bare_confidence_percentage_renders_anywhere_in_frontend`
3. `test_uiconv_p02_every_rendered_interval_brackets_its_own_point_estimate`
4. `test_uiconv_p02_retired_routes_redirect_to_terminal_with_correct_dock_active`
5. `test_uiconv_p02_signal_detail_exposes_rationale_guardrails_lineage_and_explainability`
6. `test_uiconv_p02_every_retired_page_capability_has_a_verified_new_home`
7. `test_uiconv_p02_seed_and_live_provenance_labels_survive_absorption`
8. `test_uiconv_p02_zero_adhoc_hex_across_whole_frontend_outside_tokens_css`

Plus `uiconv_p02_security_invariants.test.ts` (T-1, T-4, T-5, T-6, T-7, S-1…S-5, C-1).

## 9. Mandatory evidence

(a) Delivery commit + annotated tag `UI-CONV-P02_DELIVERY`, `git rev-parse` output; origin-push status stated plainly.
(b) SHA-256 for every created and modified file; **list every deleted file with its retired line count**.
(c) Suite counts against the delivered commit, fresh transcript. Bundle hash **must** differ. Every named test claimed must appear in the transcript (OBS-P05-1 precedent).
(d) Raw **whole-frontend** grep transcripts: ad-hoc hex, T-1, T-4/T-5, C-1, secrets, `dangerouslySetInnerHTML`/`eval`/`new Function`. Honest counts.
(e) **Statistic-to-component map** (§3) and **capability inventory** for each retired page (§4).
(f) **Level-I captures at 1920×1080, attached as image files**: (i) terminal with SIGNALS dock showing a signal detail drill-down; (ii) INTELLIGENCE dock with calibration metrics and intervals; (iii) `/signals` redirecting to the terminal with SIGNALS active; (iv) chart stage with seeded data and provenance label; (v) command palette with **empty query** showing all routes grouped (closes OBS-CONV-3); (vi) `prefers-reduced-motion` login variant (closes OBS-CONV-2).
(g) Deviation register — any capability without a new home belongs here.
(h) Debt reconciliation, verbatim, correct line numbers; **`TD-023` closed WONTFIX**, `TD-005` updated.
(i) **Corrective-actions ledger** reinstated (OBS-CONV-5).

## 10. Acceptance criteria

Approvable when: B-CONV2-1…B-CONV2-4 satisfied; eight named tests display passing; baseline maintained or grown with zero regression; `tsc -b` and `vite build` exit 0 against the delivered commit; Alembic head unchanged; evidence (a)–(i) complete; **and CA-P03-1 closed by the Operator.**

## 11. Authorization

The DA is authorized to implement UI-CONV-P02 as scoped above, effective immediately.

Where a mockup and a governing document disagree, the governing document wins. This Build Order is not an approval of any future delivery. Correction is not approval. The DA may not self-approve. The Governance Gate remains **CLOSED**; production remains **NOT CERTIFIED**; no CONV-P03 implementation may begin before its Build Order is formally issued.

**We don't guess. We prove.**

*— AXIOM ITRGA*
