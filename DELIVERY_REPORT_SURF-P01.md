# SURF-P01 DELIVERY REPORT
## Execution Research dock → Terminal EXECUTION RESEARCH Stage View (ExecutionResearchView)

| Field | Value |
|---|---|
| Delivery | SURF-P01 — first item of the SURF programme (Build Order `BUILD_ORDER_SURF-P01.md`, Operator-authorized 2026-08-16) |
| Issued by | AXIOM Development Authority (DA) |
| Issued to | AXIOM ITRGA |
| Date | 2026-08-16 |
| Base chain | `34f4c62` + item3 `b7b4c4f7…` + item5 `4c03910c…` + item6 `f65da5c3…` + item4 Rev B `a516c2c1…` |
| Patch | `/home/user/surf_p01.patch` — sha256 `62c4d021e5b6f0a0ce4200cd2c9e51098d87adccccad37539cefd8699d85577f` (2,804 lines / 112,691 B / 16 files, LF, terminating newline) |
| Governance posture | Gate CLOSED · Production NOT CERTIFIED · advisory-only |

---

## 1. Chosen home + reasoning (S1)

**Full-height stage view — `/?view=execution`**, reached by the legacy redirect, the left
module rail, and the command palette. Reasons:

1. **Nine capability groups with per-item honesty fields and a new master-detail
   interaction (S2) do not fit the bottom dock.** The bottom dock is fixed at 180 px
   (`--ix-terminal-dock-height`) and already hosts five dense compact-card tabs; the
   item-4 disposition analysis applies verbatim — a cross-cutting hub with detail
   records "cannot be honestly presented in a drawer without severe compression."
2. **The right dock (320 px) is ruled out by the Build Order itself** ("almost
   certainly too narrow").
3. **Overlays are for secondary, transient surfaces** (settings, governance); the
   execution research workspace is a primary research surface.
4. **The stage mechanism already exists** (item-4 research stage) and is the proven
   pattern for full-height primary views; the blueprint's word "dock" predates the
   CONV architecture decision, and the Build Order explicitly delegates the choice to
   the DA with reasoning ("a dock tab, overlay, or stage view").

## 2. Capability disposition — every §2.3 group mapped

| §2.3 capability group | Component in `ExecutionResearchView.tsx` | Reachable in the stage |
|---|---|---|
| Execution Research Workspace | header + disclaimer | Yes |
| Investigation Context | investigation-context section (5 in-app Links, post-absorption targets) | Yes |
| Persisted SIMULATED artifacts | artifact-counts region (genuine counts) | Yes |
| Simulated Runs | runs group + RunCard (all rows, no slices) | Yes |
| Simulated Fills | fills group + FillCard (fills for every run) | Yes |
| Paper Research Ledger | ledger group + LedgerCard | Yes |
| Risk Research Reports | risk group + RiskReportCard | Yes |
| Replay Experiments | experiments group + ExperimentCard | Yes |
| Analytics & Comparison | analytics group + AnalyticsCard | Yes |
| Replay scope · Assumptions · Limitations | RunCard sections — preserved verbatim | Yes |
| Request evidence | RiskReportCard section — preserved verbatim | Yes |
| Pre-registration plan · As-of window · Replay lineage · Included scope | ExperimentCard sections — preserved verbatim | Yes |
| Included scope · Metrics | AnalyticsCard sections — preserved verbatim | Yes |
| (NEW, S2) per-artifact detail record | detail panel via the six surfaced detail GETs | Yes |

## 3. Endpoint coverage — all 17 endpoints

| Endpoint | State |
|---|---|
| `GET /simulated-runs` | already surfaced (bundle) — now also `fetchSimulatedRunsList` |
| `GET /simulated-runs/{run_id}` | **surfaced** — `fetchSimulatedExecutionRunDetail` |
| `GET /simulated-runs/{run_id}/fills` | **surfaced as a standalone read seam** — `fetchSimulatedRunFills` (previously reachable only inside the bundle) |
| `GET /simulated-fills/{fill_id}` | **surfaced** — `fetchSimulatedFillDetail` |
| `GET /simulated-ledger-entries` | already surfaced (bundle) — now also `fetchSimulatedLedgerEntriesList` |
| `GET /simulated-ledger-entries/{ledger_entry_id}` | **surfaced** — `fetchSimulatedLedgerEntryDetail` |
| `GET /execution-risk-reports` | already surfaced (bundle) — now also `fetchExecutionRiskReportsList` |
| `GET /execution-risk-reports/{report_id}` | **surfaced** — `fetchExecutionRiskReportDetail` |
| `GET /execution-experiments` | already surfaced (bundle) — now also `fetchExecutionExperimentsList` |
| `GET /execution-experiments/{experiment_id}` | **surfaced** — `fetchExecutionExperimentDetail` |
| `GET /simulated-analytics-reports` | already surfaced (bundle) — now also `fetchSimulatedAnalyticsReportsList` |
| `GET /simulated-analytics-reports/{report_id}` | **surfaced** — `fetchSimulatedAnalyticsReportDetail` |
| `POST /simulated-runs` | **out of scope (POST)** — no client function, no UI |
| `POST /simulated-ledger-entries` | **out of scope (POST)** — no client function, no UI |
| `POST /execution-risk-reports` | **out of scope (POST)** — no client function, no UI |
| `POST /execution-experiments` | **out of scope (POST)** — no client function, no UI |
| `POST /simulated-analytics-reports` | **out of scope (POST)** — no client function, no UI |

Twelve read-only client functions added in `api/client.ts` (six list, six detail);
zero POST client functions exist (`grep` confirms). All carry `auth = true`.

## 4. M1 — frontend T-1 guard (assertion text + non-vacuity anchor)

Added to `backend/tests/test_execution_research_safety.py`:

```python
def test_execution_research_ui_module_has_no_live_execution_controls() -> None:
    ui = root / "frontend" / "src" / "components" / "terminal" / "execution" / "ExecutionResearchView.tsx"
    text = ui.read_text(encoding="utf-8").lower()
    assert "execution research workspace" in text   # non-vacuity anchor
    assert "simulated" in text                      # non-vacuity anchor
    assert "non-actuating" in text                  # M2 label anchor
    forbidden = ("place_order", "submit order", "go live", "connect broker",
                 "broker_account", "order_ticket", "account_id",
                 "execute_order", "live_trade")
    assert all(item not in text for item in forbidden)
```

**Confirmation: passes.** Safety suite 7/7 green; the module was additionally swept
against the 47 markers of the two UI-005 source-grep suites — zero hits (the sweep
includes comments; the module deliberately avoids "execute", "broker", "position",
"balance", "margin", "capital", "allocation", etc. even in prose).

## 5. M2 — SIMULATED · NON-ACTUATING labelling

- One label at **each of the six artifact groups** (runs, fills, ledger, risk,
  experiments, analytics) via `data-testid="execution-sim-badge-{family}"` — six badges,
  machine-counted in capture 01 (`capture01_sim_badges: 6`).
- Plus the header mono tag and the `SIMULATED.` disclaimer. M3: no actuation affordance
  exists anywhere — the only new controls are "View detail", "Close detail", and
  "Refresh Research"; the relocated suite's button-text sweep is green.

## 6. S3 disposition — truncation removed

The silent fills truncation is **removed at the source**: `fetchExecutionResearchBundle`
now fetches fills for **every** returned run (the `runs.slice(0, 5)` line is gone, with
a comment naming the quiet-inaccuracy class), and the new view loads fills per-run
through `fetchSimulatedRunFills` for all runs. No disclosure string was needed because
no truncation remains anywhere. The research hub (item 4) benefits identically.

## 7. R-requirements

| Req | Result |
|---|---|
| R1 | All §2.3 groups preserved; per-item honesty sections verbatim (assessed by the relocated + context suites) |
| R2 | `ResearchManagementRedirect`-pattern redirect: `ExecutionResearchRedirect` → `/?view=execution`; capture 05 proves the landing |
| R3 | Absence renders as absence — 6 group empty markers + "0 rows loaded" (capture 03); genuine counts only; no fabricated values |
| R4 | Six independent read seams, item-4 M5 pattern; per-source status rows; 6 named tests; capture 04 proves 1 error row + 5 ready with the hub intact |
| R5 | RBAC unchanged — registry entry still `protectedWorkspace`, id/route/telemetry/order unchanged; 16/16 wrappers asserted green |
| R6 | **167 suites / 785 frontend + 416 backend = 1,201 tests green** (floor 1,190 — exceeded; +10 frontend: relocated suite +3, degradation +6, deep-link +1; +1 backend: M1 guard) |
| R7 | `npm ci` before `tsc -b` in both trees |
| R8 | `ExecutionResearchPage.tsx` + its test **deleted** in the same cycle after re-pointing all four coupled suites (context, completion, frame, page suite relocated) |

## 8. Re-targets and disclosures (unprompted)

1. **Read-seam text re-targets (3 assertion sites):** the Investigation Context panel
   previously declared `fetchExecutionResearchBundle` as its read seam; the surface now
   reads through six independent seams, so the panel text and two source-text
   assertions were re-pointed to the new seam names ("execution-research read seams" /
   `fetchSimulatedRunsList`). Assertion intent (existing read seams, no fabricated
   data) is preserved — re-target, not weakening.
2. **Context links converted from raw `<a href>` to react-router `Link`** targeting
   post-absorption destinations directly (`/?dock=signals`, `/?panel=scenarios`,
   `/?panel=portfolio`) — the OBS-CONV3-10 class; two suites' renders were wrapped in
   `MemoryRouter` to accommodate, with zero assertion changes beyond §1.
3. **`SignalInvestigationRecords.tsx`** execution-research row: `existingRoute` →
   `/?view=execution`, read seam updated — the item-6 module's declared inventory now
   states the post-absorption home (one frame-suite assertion re-pointed accordingly).
4. **Bundle delta +9.77 kB** (687.85 → 697.62 kB, `index-SwOPTjUM.js`) — OBS-5: the new
   view module and twelve client functions; no new module enters the bundle beyond the
   relocated page's replacement.
5. **The five POSTs remain untouched** — verified by grep (0 client functions) and by
   design (no create affordance; the only UI additions are read affordances).
6. Two test failures surfaced during development were **implementation/test precision
   issues corrected honestly** (fills-dependency error row counted; ambiguous text
   query narrowed) — no failing test was deleted or weakened to reach green.

## 9. Level-I captures (all five required classes)

Gallery: `SURF-P01_CAPTURES.html` — sha256
`4e5c9cf839010fb0c5f51068c4a546ac1fcf808ccc37d93d3d757969cf92f2f0`
(self-contained, base64 PNGs, alt text, per-image SHA-256). Raw PNGs:
`/home/user/surf_p01_captures/`. Machine-recorded DOM state:
`SURF-P01_CAPTURE_VERIFICATION.json` (also copied to `docs/evidence/uiconv/`).

| Capture | Class | Proof | SHA-256 |
|---|---|---|---|
| 01 Populated stage + labelling | populated surface, M2 labels, interaction trace | `data-stage-view="execution"`; centre label "Execution Research Stage"; 12/12 region testids; 6/6 seams ready; 3 run cards; **hit-test TRUE** before real click | `a13725928cf38df5f3023ff09f5217e038b3777e9f98920eb1a2330ad807bd18` |
| 02 Detail record | detail via surfaced GET | detail panel 0→1; record shows policy/fill model/status/source artifacts/replay scope/assumptions + Fills heading — retrieved via `fetchSimulatedExecutionRunDetail` | `d81d5adea1af5efc76173a378c47d66cf709bf98002b98037cee3410171ab50c` |
| 03 Empty bundle, scrolled | empty state scrolled (OBS-CONV3-5 discipline) | 6/6 absence markers; 6× "0 rows loaded"; scroll metrics recorded; marker in-viewport TRUE | `aa43bd952a65d3ebd64b3eb220ac06f2888a686485f01d1b14e14075e444e702` |
| 04 Single-seam failure | independent degradation | ledger seam aborted → 1 error row ("Paper ledger · Failed to fetch") + 5 ready; hub intact; error row in viewport TRUE | `1ad1cdf4e2aadeca8ce4cee14e156c0c8092d17c5c5957408cf7b810a4370334` |
| 05 Redirect landing | `/execution-research` redirect | final URL `http://localhost:5173/?view=execution`; view mounted; stage attr "execution" | `78b91290d617757f53a35d54be20b2f667cba1a13c64b39818a371109624a190` |

All five PNGs are exactly 1920×1080 RGB.

## 10. Raw console transcripts (excerpts; full logs in `docs/evidence/uiconv/`)

```
$ git clone /home/user/axiom /tmp/surfverify && cd /tmp/surfverify
$ git apply item3.patch && git apply item5.patch && git apply item6.patch && git apply item4.patch
$ git apply --check surf_p01.patch
GIT_APPLY_CHECK_EXIT=0
$ git apply surf_p01.patch
$ diff -rq /tmp/surfverify /home/user/axiom <exclusions>    # full-tree audit
AUDIT_DONE                                                   # no differences
$ npm ci --no-audit --no-fund
added 148 packages in 2s
$ npx tsc -b --force --pretty false
tsc exit: 0
$ npx vitest run
Test Files  167 passed (167)
     Tests  785 passed (785)
$ AXIOM_DATABASE_URL='sqlite+aiosqlite:///:memory:' ... .venv/bin/python -m pytest -q
416 passed, 1 warning in 130.11s (0:02:10)
$ .venv/bin/python -m pytest tests/test_execution_research_safety.py -q
7 passed, 1 warning in 0.66s
$ npm run build
dist/assets/index-SwOPTjUM.js   697.62 kB │ gzip: 188.09 kB
✓ built in 361ms
$ sha256sum dist/assets/index-*.js
1f591fa7c5ecc3181e17734fab003afcc0f17079767832515e736587fe5f5c2f  (DA tree)
1f591fa7c5ecc3181e17734fab003afcc0f17079767832515e736587fe5f5c2f  (verify tree)  ← identical
```

## 11. Transport

- Patch: `/home/user/surf_p01.patch` (sha256 above) — full patch pasted inline in the
  transmission message (hash-reconciled). Uploadable copy: `/home/user/surf_p01.patch.txt`
  (byte-identical). LF endings, terminating newline, base chain stated explicitly.
- No commits, no pushes — the repository is Operator-only (governance correction,
  2026-08-16); the verified patch is the artifact of record.

---

**Gate CLOSED · Production NOT CERTIFIED**

*— AXIOM Development Authority (DA)*
*2026-08-16*

---

## 12. POST-DETERMINATION ADDENDUM (2026-08-16) — OBS-SURF1-1 CORRECTION

ITRGA issued `ITRGA_DETERMINATION_SURF-P01`: **APPROVED WITH OBSERVATIONS**. The hard
POST exclusion was verified (0 client functions), M1/M2/M3 and S1–S4 verified, R1–R7
verified. One new finding: **`OBS-SURF1-1`** — capture 04 did not evidence its claim.

**ITRGA is correct, and the flaw is the DA's instrument, not the surface:**

1. The capture's filename claimed `..._DEGRADATION_SCROLLED.png` while
   `capture04_scroll_metrics` recorded `scrollTop: 0` — the inner scroll container had
   not moved.
2. The visibility check measured the error row against `window.innerHeight` instead of
   the scroll container's visible clip, and the pre-scroll step used
   `scrollIntoViewIfNeeded`, which does not scroll when the section's *top edge* is
   already visible. A check built that way can return `true` for an element below the
   container's fold. That is the same instrument-flaw class the DA disclosed for the
   item-4 pre-scroll hit-test — and it went undetected here. ITRGA's ruling that a
   measurement which can affirm an invisible element cannot discharge a visual
   requirement is accepted as a standing instrument standard.

**Correction executed (Rev B capture set):** the capture script now (1) records the
pre-scroll `scrollTop` explicitly, (2) scrolls the inner container by a computed
offset so the error row is centred in it, (3) measures the row's rect against the
**container's** clip rect with recorded coordinates, and (4) re-measures `scrollTop`
**after** the screenshot so the rendered frame provably matches the recorded state.
Rev B capture 04 records: `scroll_before_explicit_scroll: 0` → `scrollTop: 93`
(container 2822/798) → `errorRowWithinContainer: {withinContainer: true, rowTop:
426.7, rowBottom: 533.3, containerTop: 81, containerBottom: 879}` →
`scrollTop_after_screenshot: 93`.

**Rev B artifact hashes (supersede the Rev A set; ITRGA's `8fdcce6050a59b4a` JSON and
`4e5c9cf839010fb0` gallery remain valid as the Rev A record):**

| File | SHA-256 |
|---|---|
| Gallery `SURF-P01_CAPTURES.html` (Rev B) | `89de351c807ae7d06b39858fc52886aeb2c11ae8e316eb7f8b68e16582c3e6d8` |
| `SURF-P01_CAPTURE_VERIFICATION.json` (Rev B) | `bae4108a4f893e0cef98bc108cc2050ef7edc43ef4acbb52a6a8edd3939d8580` |
| PNG 01 | `bf79f6d6b4dd2313a384bd7d588b9fa048b87de1615cde462df99b24dfe947f9` |
| PNG 02 | `5ec23bfb115426e5b2b12a7f87a7e3ddfffa13e74dc9bba44a18d645e5dd903d` |
| PNG 03 | `6a3b0ec28efbd38c4d9259b92fec9ec007ae824cb69a091c7d7da03b13d83057` |
| PNG 04 (corrected) | `62d5c85b14c36b93e469cb7976e2548d04b9787667dd4cfc38a5876dba77a1d6` |
| PNG 05 | `16f378671e709cadffd90eb2ea26ae0bdd8df06beb82caf6c60c0b0d5b6b310e` |

Disclosure: captures 01/02/03/05 were re-shot in the same run; their substance is
unchanged (same verification records) but their pixel hashes differ because the shell
UTC clock and live ticker re-render. Only capture 04's substance changed. The capture
script change is instrument-only and lives in the DA working tree; the approved
`surf_p01.patch.txt` (`62c4d021e5b6f0a0…`) is untouched.

**Standing:** SURF-P01 APPROVED WITH OBSERVATIONS · `OBS-SURF1-1` correction
submitted for ITRGA credit · `OBS-5` (bundle) open for POLISH-P01 · `OBS-CONV2-5`,
`F-BRAND-1` open · SURF-P02 (Alerts, TD-061) **not authorized** — no implementation
until its Build Order is issued.

---

## 13. POST-REVIEW ADJUNCT (2026-08-17) — ITRGA_REVIEW_OBS-SURF1-1_CORRECTION

ITRGA reviewed the OBS-SURF1-1 correction: **PARTIALLY DISCHARGED — INSTRUMENT FIXED,
IMAGE NOT TRANSMITTED**. The Rev B instrument is **ACCEPTED** (the geometric
containment check, the before/after scrollTop records, and the
`scrollTop_after_screenshot` guard were credited as materially better than Rev A;
SURF-P01's approval stands unchanged). The remaining half is transport, not code:
ITRGA holds the Rev A gallery (`4e5c9cf839010fb0`), which still embeds the superseded
capture 04; the Rev B gallery was never transmitted.

**DA verification before re-transmission:** the Rev B gallery
`SURF-P01_CAPTURES.html` (`89de351c807ae7d06b39858fc52886aeb2c11ae8e316eb7f8b68e16582c3e6d8`)
was byte-audited — all five embedded base64 PNGs hash identically to the raw files
in `/home/user/surf_p01_captures/`, including the corrected capture 04
(`62d5c85b14c36b93e469cb7976e2548d04b9787667dd4cfc38a5876dba77a1d6`, which shows the
`Paper ledger / Failed to fetch` error row inside the scrolled container). The
artifact is verified ready; only its transmission to ITRGA remains outstanding
(Operator queue).

---

## 14. POST-FINDING ADJUNCT (2026-08-17) — OBS-SURF1-2 CORRECTION

ITRGA issued `ITRGA_FINDING_OBS-SURF1-2_SOURCE_STATUS_COLLAPSE.md`: **OBS-SURF1-1 fully
DISCHARGED** (transport + instrument), and a new presentation defect — the Source
Status panel (and the artifact-counts panel) collapse in the stage view.

**Diagnosis confirmed by measurement, not assertion.** A diagnostic probe
(`scripts/diagnose_surf1_2.mjs`) recorded the pre-fix geometry: the stage scroll
container is a flex column, and `flex-shrink: 1` compressed every direct panel child
to its 120px `min-height` — the Source Status panel measured **120px** while its inner
grid measured **166px** (cards 76px each), and the counts panel measured 120px against
a 375px grid. The overflowing grids were painted behind the next panel's opaque
background: geometrically present, visually unreadable. The research hub was
unaffected because its sections sit inside the `.research-hub-view` block wrapper; the
execution view's fragment children are direct flex items — the asymmetry that let this
surface through SURF-P01's review.

**Correction (standalone patch `surf_p01_obs1-2.patch`,
sha256 `69964afec17b9c0f1a68b12e7577e41402669f7c487722808e487b3dccf4b853`,
293 lines / 13,279 B, 4 files, LF, base `34f4c62` + item3 + item5 + item6 + item4 +
surf_p01):** the ITRGA-prescribed flex-context rule —

```css
.research-stage-scroll > *,
.stage-view-scroll > * {
  flex-shrink: 0;
}
```

— applied to both stage containers in `TerminalMultiPane.css` (the research selector
keeps the hub's guarantee as a single flex item). Plus: a named test
`test_surf_p01_obs1_2_stage_panels_keep_intrinsic_height_rule_present` pinning the rule
in the shipped stylesheet (jsdom cannot lay out; the rendered proof is the capture
set), and a legibility instrument in `capture_surf_p01.mjs` that records panel height,
grid height, every card rect, and `cardsFullyInsidePanel` for captures 01/03/04.

**Post-fix measurements (Rev C captures, JSON `429e6d1b6d76828eb285033680c792c1184f1001559bd5076f9d448c990e0d1b`):**

| Capture | Panel | Cards |
|---|---|---|
| 01 populated | Source Status **298px** (grid 166 inside) · counts **440px** (grid 375 inside) | all `cardsFullyInsidePanel: true` |
| 03 empty | Source Status 298px · counts 440px | all inside |
| 04 seam failure | Source Status **329px**; error card **107px** (Paper ledger / Failed to fetch) | `cardsFullyInsidePanel: true`; row inside container (426.5–533.1 within 81–879); scrollTop 218 before AND after the screenshot |

**Rev C artifacts:**

| File | SHA-256 |
|---|---|
| Gallery `SURF-P01_CAPTURES.html` (Rev C) | `0906c712ceb439d7a52145550b0c06618c5f77e08926d1c80d38dc85e0d0cf95` |
| `SURF-P01_CAPTURE_VERIFICATION.json` (Rev C) | `429e6d1b6d76828eb285033680c792c1184f1001559bd5076f9d448c990e0d1b` |
| PNG 01/02/03/04/05 | `e183b216…97e6d` · `94719262…f700c` · `9bb7d09d…8bfc4` · **`2b68fce5…1a551` (closure evidence)** · `ebb77dc4…cd9ec` |

**Verification:** `git apply --check` exit 0 in a pristine clone (base chain + five
patches); the four correction paths diff-identical to the DA tree; **167 suites / 786
frontend + 416 backend = 1,202 tests green**; `tsc` 0; build JS `index-DsImsBhr.js`
697.62 kB with sha256 identical across trees (`1f591fa7…`); CSS asset
`index-BOtZgdCY.css` identical (`29ad19ea…`). Bundle size unchanged (697.62 kB) — CSS
and tests only.
