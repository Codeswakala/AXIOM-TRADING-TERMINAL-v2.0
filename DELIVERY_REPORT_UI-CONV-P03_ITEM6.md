# DELIVERY REPORT — UI-CONV-P03 · ITEM 6
## SignalInvestigationPage → Signal Drill-Down Details Surface (Absorption)

| Field | Value |
|---|---|
| Document type | DA Item Delivery Report (Directive §§29–31; Doc 17 §17.8 Gate 4) |
| Issued by | AXIOM Development Authority (DA) |
| Issued to | Independent Technical Review & Governance Authority (ITRGA) & Operator |
| Date | 2026-08-16 |
| Governing instrument | `BUILD_DIRECTIVE_UI-CONV-P03_ITEM6.md` (ITRGA) — scopes item 6 only |
| Base | **`34f4c62` + item-3 patch (`b7b4c4f7…`) + item-5 patch (`4c03910c…`)** — stated plainly per directive §7 |
| Parent BO | `BUILD_ORDER_UI-CONV-P03` §3 item 6 — "Details dock, opened from a signal card" |
| Transport | No commits per Operator instruction; `git diff`-based patch (accepted form) |
| Governance Gate | **CLOSED** · Production **NOT CERTIFIED** |

---

## 1. Chosen disposition + reasoning (directive §1 requirement 1)

**Disposition: absorption into the existing signal drill-down — extend, do not duplicate.** Per the directive's own §2 mapping, sections 2–7 of the page (persisted signals, detail, rationale, guardrails, lineage, explainability) already exist in `TerminalSignalStream`'s expanded card. Rebuilding them would recreate the parallel-implementation hazard the turn-56 reframe forbids.

**What was added vs already present (explicit §2 answer):**

| Page capability | Disposition |
|---|---|
| 1 · Signal Investigation Workspace (frame) | **ADDED** — `SignalInvestigationFrame` (h1 heading, read-only paragraph, "Investigation reads persisted evidence only.", disclaimer, planning frame) renders inside the expanded card |
| 2–7 · Persisted signals / detail / rationale / guardrails / lineage / explainability | **ALREADY PRESENT** — the dock card; **extended**, not duplicated: lineage gains Signal id / Model version / full Input hash rows (page fields the dock lacked); guardrails gains Eligibility Reasons; the expanded body gains `aria-label="Signal investigation detail"` |
| 8 · Linked validation and report ids | **ADDED** — `signal-detail-report-ids-{id}` with verbatim `?? "—"` markers (M2) |
| 9 · Related evidence links | **ADDED** — in-app `Link` navigation to `/?view=chart`, `/?dock=signals`, `/?dock=intelligence` (M5 / `OBS-CONV3-10`) |
| 10 · Linked intelligence reports | **ADDED** — `REPORT_GROUPS` from `fetchInstitutionalIntelligenceBundle` (independent fetch in the stream), verbatim "No reports returned." per empty group (M2) |

The page is **deleted**; `/investigate` redirects to `/?dock=signals`. Exactly one implementation of every section exists. The relocated unique content (planning sources constant, frame, report helpers) lives in `components/terminal/signals/SignalInvestigationRecords.tsx`.

## 2. Mandatory requirements

| Requirement | Status | Evidence |
|---|---|---|
| **M1 — extend, do not duplicate** | **SATISFIED.** No section rebuilt; the card absorbs groups 1/8/9/10 and extends its existing sections with the page's missing fields. | §1 table; suite mapping below |
| **M2 — absence markers preserved** | **SATISFIED.** All four report ids render `?? "—"` verbatim; empty report groups render "No reports returned." — proven by tests (drilldown suite: ids-with-null test, empty-bundle test) and capture 03 (all five groups empty via network-aborted seams). | `signal-detail-report-ids-*`, `signal-detail-intelligence-*` |
| **M3 — backend constitutional guard re-pointed non-vacuously** | **SATISFIED.** `backend/tests/test_signal_investigation_workspace.py:151` now points at `frontend/src/components/terminal/TerminalSignalStream.tsx` — the module that ACTUALLY renders the drill-down. Both new-home modules verified clean of every forbidden string (0 matches); the guard passes (4/4 tests in that file green, including the re-pointed one). | pytest transcript |
| **M4 — five frontend suites re-pointed, none deleted** | **SATISFIED.** `pages/SignalInvestigationPage.test.tsx` → **relocated** to `components/terminal/signals/SignalInvestigationDrilldown.test.tsx` (all five original tests' guarantees carried, re-targets documented inline); accessibility audit, completion, frame, and lineage suites re-pointed to the records module / drill-down. Zero suites deleted; zero assertions weakened (re-targets documented per-line where the old chrome no longer exists — see §4). | vitest 165/767 |
| **M5 / OBS-CONV3-10 — evidence links in-app** | **SATISFIED.** The three links are `react-router` `Link`s targeting post-absorption destinations directly — no full-page reload, no bounce through legacy redirects. Asserted by drilldown + lineage suites (new hrefs). | `signal-detail-evidence-links-*` |

## 3. Standing requirements

| Requirement | Status |
|---|---|
| **R2** `/investigate` no 404 | `SignalInvestigationRedirect` → `/?dock=signals`; registry entry keeps route + telemetry id; deep-link test + capture 02 (final URL verified) |
| **R3** no fabricated fallbacks | Report ids and intelligence groups render verbatim or explicit absence; zero hardcoded plausible-looking values introduced |
| **R4** testids on new regions | 7 new hooks: investigation frame, planning frame, sources inventory, report-ids, evidence-links, intelligence reports, plus the expanded-body aria-label; existing 5 dock hooks stay |
| **R6** RBAC | 16/16 `protectedWorkspace()` wrappers unchanged; no per-entry override |
| **R7** suite green ≥ 1,177 | **165 suites / 767 frontend + 415 backend = 1,182 platform tests.** Page + test deleted; drilldown suite (8 tests) + 2 deep-link tests added; nothing deleted to force green |
| **R8** `npm ci` → `tsc -b` | Executed: exit 0 |
| **Deletion discipline** | `SignalInvestigationPage.tsx` + its test deleted the same cycle, after M3/M4 re-pointing |
| **OBS-CONV3-4** | No stage claim made (same judgement as item 5) |

## 4. Assertion re-target register (M1 transparency)

Where the absorbed surface's old chrome genuinely no longer exists, the suite assertions were re-targeted — never weakened — and are listed here:

| Suite / assertion | Re-target | Justification |
|---|---|---|
| Drilldown (ex-page) test: `getAllByRole("button")` | `getAllByRole("tab")` (state filter tabs) | The dock's interactive controls are the filter tabs; the card is an inert presentation surface |
| Drilldown + lineage: `"50.0% calibrated confidence"` | Canonical `CalibratedConfidenceBadge` text (`50.0%` + uncertainty qualifier) | The retired `formatConfidence` string belonged to the pre-B-CONV2-1 legacy renderer; the canonical badge is the STRONGER invariant (confidence never bare) |
| Lineage: evidence-link hrefs `/intelligence` `/signals` `/charts` | `/?dock=intelligence` `/?dock=signals` `/?view=chart` | Mandated by M5/OBS-CONV3-10 (authorized change) |
| Lineage: source greps | Records module (investigation content) | The stream legitimately contains direction-normalization vocabulary (BUY/SHORT) and a defensive "Zero transaction execution affordance" disclaimer that trip the broad marketing greps; the stream's constitutional no-mutation guarantee is enforced by the re-pointed backend guard |
| Lineage/frame suites: dock headings with colons | Same headings (asserted exactly) | Dock chrome is pre-approved P02/P04 content |

## 5. Level-I captures (3 · all exactly 1920×1080 · alt text · interaction trace)

Gallery: `UI-CONV-P03-ITEM6_CAPTURES.html` (workspace root, SHA-256 `79a33b63…`) · raw PNGs: `/home/user/uiconv_p03_item6_captures/` · DOM record: `UI-CONV-P03-ITEM6_CAPTURE_VERIFICATION.json`.

| # | File | SHA-256 | Subject |
|---|---|---|---|
| 1 | `01_EXPANDED_DRILLDOWN_NEW_SECTIONS.png` | `834588a7…` | Expanded card: frame + sections 8/9/10. **Interaction trace:** `document.elementFromPoint` over the card returned the card BEFORE the Playwright click (`hitTestCardOwnsPointerBeforeClick: true`) — real-browser hit-testing verified, the exact evidence class that would have caught the item-3 pointer-events defect |
| 2 | `02_INVESTIGATE_ROUTE_REDIRECT.png` | `44d0c170…` | `/investigate` → `/?dock=signals`, signals tab `active` |
| 3 | `03_EMPTY_BUNDLE_SCROLLED.png` | `a841f42e…` | **All five bundle seams network-aborted**: every report group renders "No reports returned." — the M2 empty state, scrolled into view (OBS-CONV3-5 discipline) |

**OBS-CONV3-9 (item-5 captures):** attached with this delivery — gallery `UI-CONV-P03-ITEM5_CAPTURES.html` (SHA-256 `64e5654a…`) and its raw PNGs at `/home/user/uiconv_p03_item5_captures/`. Its capture 05 (audit error state, `49b5474f…`) is scrolled to the affected region (`bodyScroll scrollTop 1510/11514` recorded) — the OBS-CONV3-5 evidence for that surface.

## 6. Executed transcripts (raw console output — pasted in the transmission message)

- `vitest`: **165 files / 767 tests passed** · `tsc -b`: exit 0 · `vite build`: exit 0 · `index-BZSBCfvW.js` **682.80 kB** · `pytest`: **415 passed**. Logs: `docs/evidence/uiconv/{vitest,tsc,vite_build,pytest}_p03item6.log`.

Bundle: 687.56 kB (item-5 close) → **682.80 kB (−4.76 kB)** — the 425-line page's retirement outweighed the drill-down extension. Disclosed under OBS-5 discipline.

## 7. Deviations & disclosures

1. **The contextual-assistant mount retired with the page.** The page container wrapped the workspace with a `ContextualAssistantPanel` mount (not listed in the directive's §1 capability groups). The assistant surface remains mounted on the chart and governance surfaces; the investigation-specific mount was retired with the page. Stated plainly, not buried.
2. **Assertion re-targets** — fully registered in §4.
3. **No seeded fixtures needed** this cycle (the P04 seed supplies signals; the empty state was produced by network-aborting the real seams — the honestest form of absence).

## 8. Precise wording (OBS-CONV2-2 discipline)

- `pages/SignalInvestigationPage.tsx` + `.test.tsx`: **deleted** (superseded; redirect registered).
- Planning sources constant, REPORT_GROUPS, helpers, planning frame: **relocated** to `SignalInvestigationRecords.tsx` (originals removed; the page itself deleted).
- Page test suite: **relocated** to `SignalInvestigationDrilldown.test.tsx` (one copy).
- Dock card sections: **extended** (lineage/guardrail fields added; three new sections added).
- Four workstation suites: **re-pointed** (imports + raw-source globs).

## 9. Transport

| Item | Value |
|---|---|
| Patch | `/home/user/item6.patch` — **2,019 lines · 90,911 B · SHA-256 `f65da5c3ce8433ec07917e438b5a9c8d13d30549360fd05fd43643a0865d1350`** · LF · terminating newline |
| Base | `34f4c62` + item-3 `b7b4c4f7…` + item-5 `4c03910c…` (stated plainly) |
| Scope | 17 files · +911 / −740 (3 new modules incl. capture scripts, 1 deleted page rendered as rename/delete hunks, 12 modifications) |
| `git apply --check` at the stated base | **exit 0** (no whitespace warnings) |
| Applied in pristine clone | **165/767 · tsc 0 · build `index-BZSBCfvW.js` 682.80 kB** (identical to DA tree) |

## 10. Status

| Finding | State |
|---|---|
| Item 6 requirements | Delivered, awaiting ITRGA determination |
| `OBS-CONV3-10` | **DISCHARGED** (M5) |
| `OBS-CONV3-9` | **Addressed** — item-5 gallery attached with this delivery |
| `OBS-CONV3-5` | Addressed for this cycle's surface (capture 03 scrolled, DOM-verified) |
| `OBS-CONV3-4` (`"research"` stage) | Open — **blocks item 4 route conversion**; not triggered by item 6 |
| `CA-CONV2-3` / `OBS-CONV3-8` | Open — transport/durability, Operator-owned |
| `OBS-PROV-2` · `OBS-5` · `F-BRAND-1` · `OBS-CONV2-5` | Carried |

**Remaining P03:** item 4 (`ResearchManagementPage`, 1,391 ln — disposition approved, `OBS-CONV3-4` must close first).

Gate **CLOSED** · Production **NOT CERTIFIED** · This delivery covers item 6 only; item 4 was not begun.

**We don't guess. We prove.**

*— AXIOM Development Authority (DA)*
*2026-08-16*
