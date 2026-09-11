# ITRGA REVIEW — UI-004-P04

## Validation & Economic-Usefulness Integrity Panels

| Field | Value |
|---|---|
| Reviewing authority | AXIOM Independent Technical Review & Governance Authority (ITRGA) |
| Programme | AXIOM Institutional UI Transformation |
| Workstream | UI-004 — Research & Intelligence Workspace |
| Phase | **UI-004-P04** |
| Build Order under review | `BUILD_ORDER_UI-004-P04.md` |
| Delivery report | `DELIVERY_REPORT_UI-004-P04.md` (364 lines) |
| Operator evidence | `operator results.md` (2272 lines, target `C:\Users\Swakala\.vscode\AXIOM\axiom`) + 5 served-session PNGs |
| Baseline of record | v0.62.0 · Alembic head `20260717_0037` · backend 414 · frontend 40f/170t |
| Governance Gate | **CLOSED** (held) |
| Production status | **NOT CERTIFIED** |
| **DETERMINATION** | **✅ APPROVED WITH OBSERVATIONS** |

> **Motto:** *We don't guess. We prove.*

---

## 0. Determination

**UI-004-P04 is APPROVED WITH OBSERVATIONS.**

The phase's constitutional substance is proven line-by-line on operator-run target evidence: the new
`ValidationEconomicIntegrityPanel` renders the §2.2 verbatim-verdict surface, the five mandated named
tests pass, no re-derivation / no cherry-picking / no client-side analytics engine / no actuation, no
schema/dependency/registry drift, backend 414, and Doc 16 brand B-1…B-7 hold.

The approval is qualified by **three binding Observations** driven by a real, non-relabeled finding: the
operator's **direct full frontend suite run FAILED (`2 failed | 173 passed (175)`, exit 1)** — two
**pre-existing baseline shell/navigation tests timed out at the 10 s `testTimeout`** — and the delivery
report §11.1 **misrepresented this as a flat "41 files / 175 tests passed."** The identical two tests
**pass 175/175 in the `local_ci.sh` re-run**, establishing this as an environment-induced `testTimeout`
flake on a contended machine rather than a UI-004-P04 code regression. Because the flake is confirmed
green in the same session and neither failing test touches P04's new panel, the phase is approved — but
the false-green report claim and the missing panel screenshot are recorded as corrective Observations.

**This determination authorizes the next Build Order (`BUILD_ORDER_UI-004-P05`) upon operator "authorized".**

---

## 1. Build identity (verified FIRST)

| Check | Command / Evidence | Result |
|---|---|---|
| Report is OF UI-004-P04 | `sed -n '1,20p'` + `grep -nE 'UI-004-P04'` DELIVERY | ✅ Phase `**UI-004-P04**`, BO/predecessor P03 correct |
| Report length | `wc -l DELIVERY_REPORT_UI-004-P04.md` | 364 lines |
| Transcript length | `wc -l "operator results.md"` | 2272 lines |
| Transcript is OF this phase | prompt lines target `DELIVERY_REPORT_UI-004-P04.md`, `BUILD_ORDER_UI-004-P04.md` | ✅ Not stale / not wrong-phase / not concatenated |

No stale prior-turn results, wrong-phase report, or concatenated transcript detected.

---

## 2. Mandatory evidence — Level-I line-by-line (transcript credited over report, R7)

| # | Requirement | Transcript evidence | Verdict |
|---|---|---|---|
| a | 5 named tests displayed passing | All 5 `✓` in targeted (`5 passed`) AND full run (lines 236–250) | ✅ |
| b | Verbatim §2.2 render (`research_only`/`not_assessed`/`warning:POORLY_CALIBRATED`, sample_count, limitations, source_artifact_ids, market_scope) | `Select-String` on `InstitutionalIntelligencePage.tsx` — all markers present, `className="mono"` | ✅ |
| c | No re-derivation grep clean (`recompute\|recalculat\|reclassif\|deriveConfidence\|upgrade.*verdict\|normaliz.*(verdict\|status)\|new .*Engine\|/api/v1/orders`) | Second command **no output** (verified: no forbidden-term lines in region) | ✅ |
| d | Verdict NOT reclassified/upgraded | `test_ui004_economic_usefulness_verdicts_are_not_rederived_or_upgraded` ✓; stored strings shown as-is | ✅ |
| e | No cherry-picking (sample counts / scope / limitations / warnings preserved) | `test_ui004_no_cherry_picking_...` ✓; browser shows sample_count=6, wilson intervals, withheld/expiry rates | ✅ |
| f | No client-side analytics engine | `test_ui004_validation_economic_panels_contain_no_client_side_analytics_engine` ✓ | ✅ |
| g | Research-only disclaimers preserved | `test_ui004_..._preserve_research_only_disclaimers` ✓; line 962–963 "not trading instructions, not financial advice" | ✅ |
| h | No-actuation grep clean | `buy\|sell\|place_order\|execute\|open_gate\|allow_execution\|account_id…` — no matches | ✅ |
| i | No-drift substitute | `alembic current 20260717_0037 (head)`; package.json/lock = `lightweight-charts@^4.2.0` only (no new dep); no new endpoint/schema/persistence marker; registry `research.intelligence` / `/intelligence` only, **no `/research-intelligence`** | ✅ |
| j | Backend suite ≥ 414 | `414 passed, 1919 warnings in 645.89s` | ✅ (414) |
| k | **Full frontend suite ≥ 40f/170t, no test lost** | **Direct run: `2 failed \| 173 passed (175)`, exit 1** — RED. CI-script re-run: `41 passed (41)` / `175 passed (175)` green | ⚠️ **FINDING → Observation (see §3)** |
| l | Doc 16 brand B-1…B-7 | tokens (`--ix-color-*`, `--font-mono`) only; hardcoded-color grep in production TSX **no output**; mono numerics/ids; non-color status text | ✅ |
| m | Browser served verbatim verdicts | 5 PNGs: GATE CLOSED / RESEARCH-ONLY / PRESENTATION SHELL; `economically_usable`, `50.0% calibrated`, sample_count=6, wilson intervals verbatim | ⚠️ Partial — **new P04 integrity panel not clearly captured (Observation O-3)** |
| n | Networked CI / TD-W6-CI-AUDIT | `npm audit` ran **online**, returned 2 **moderate** advisories (below high gate), **no ENOTFOUND/ECONNRESET** — flake did NOT occur this turn. `LOCAL_CI_EXIT_CODE:` printed **blank** (undefined var `$LASTEXITCODEnb`) — non-result R7 | ⚠️ Observation O-2 |

---

## 3. Finding of record — full-suite RED + false-green report claim

**Finding F-P04-1 (material, → Observations, not Corrective).**

- The operator's **direct `npm test` full run** reported:
  `Test Files 2 failed | 39 passed (41)` · `Tests 2 failed | 173 passed (175)` ·
  `FRONTEND_VITEST_EXIT_CODE: 1` · `FRONTEND_VITEST_FAILED:1`.
- The two failures are **`Test timed out in 10000ms`** on:
  1. `InstitutionalWorkspaceShell.test.tsx > WorkspaceHost mounts each existing page content by route (no page regression)`
  2. `WorkflowNavigationCompletion.test.tsx > UI-002-P05 … test_ui002_all_routes_keep_single_ui001_shell_navigation_system`
  Both iterate `CURRENT_PROTECTED_ROUTES` rendering the shell — **pre-existing baseline tests, unrelated to the P04 panel.**
- The **`local_ci.sh` re-run in the SAME session** reported `41 passed (41)` / `175 passed (175)` —
  the identical two tests PASS (env time 184 s vs 431 s on the failed run), establishing a
  **slow-machine `testTimeout` flake**, not a code regression.
- **Delivery report §11.1 stated "Frontend full suite: 41 files / 175 tests passed" as a flat fact** —
  a **false-green claim** that omitted the RED direct run. Per ITRGA doctrine a failing/red gate is a
  **finding not a footnote**, and the report must never present a red run as green.

**Why Approved-with-Observations, not Corrective:** the flake is proven green in-session on the same
machine, no failing test touches UI-004-P04 code, and every P04-specific mandatory gate passes. Operator
confirmed this disposition. The report misrepresentation and the flake root-cause are captured as binding
Observations rather than blocking the phase.

---

## 4. Observations (binding — resolve before / within UI-004-P05)

- **O-1 (report integrity):** DA must **correct DELIVERY_REPORT_UI-004-P04.md §11.1** to state the true
  direct-run result (`2 failed / 173 passed`, exit 1, both `testTimeout`) and the CI-script green re-run.
  A red run must never be reported as "175 passed." Future reports: report the **actual exit code** of
  each full run.
- **O-2 (testTimeout hardening + CI sentinel):** Raise `testTimeout` (or split/parallel-guard the
  route-iteration shell/nav tests) so `InstitutionalWorkspaceShell` and `WorkflowNavigationCompletion`
  do not flake at 10 s on contended machines. Fix the CI sentinel typo `$LASTEXITCODEnb` → `$LASTEXITCODE`
  so `LOCAL_CI_EXIT_CODE` is actually captured (this turn it was a **non-result, R7**).
- **O-3 (served-panel screenshot owed):** Next turn supply a served-session screenshot **scrolled to the
  new "Validation & Economic-Usefulness Integrity" panel** (Stored Validation Statuses / Stored
  Economic-Usefulness Verdicts / Scope, Sample Counts & Limitations cards) showing verbatim stored
  verdicts. This turn's PNGs proved P01/P02/P02b surfaces only.

---

## 5. Constitutional & brand posture

- **Governance Gate CLOSED** — no broker/order/account/position/balance/margin/execution/Gate path
  introduced (no-actuation grep clean; P04 boundaries §6 explicit).
- **No external LLM / no dynamic plugin / no authoritative recompute** — no-rederivation grep clean +
  named tests.
- **Verbatim-verdict constitution (§2.2) held** — stored `research_only` / `not_assessed` /
  `warning:POORLY_CALIBRATED` shown as-is, never upgraded to tradable/approved/economically-usable.
- **Doc 16 brand gate B-1…B-7 PASS** — AX monogram/identity unchanged; constitutional palette via tokens,
  no off-palette/hardcoded color; monospace numerics/ids/hashes; unified iconography; institutional (not
  retail) copy; non-color status text ("never color alone"); AXIOM-format documentation.
- **No-drift:** alembic head `20260717_0037` unchanged; no new table/migration/endpoint/dependency;
  registry unchanged (`/intelligence`).

---

## 6. Disposition

**UI-004-P04 — ✅ APPROVED WITH OBSERVATIONS.** Baseline advances to
**v0.62.0 · head 20260717_0037 · backend 414 · frontend 41f/175t** (as proven by the CI-script green run;
the direct-run flake is an environment artifact, not a lost test). Observations O-1…O-3 are binding.

Next authorized step on operator **"authorized"**: issue **`BUILD_ORDER_UI-004-P05`** (Research Artifacts,
Collections & Saved-View Preferences — binds R-2 raw-psql read-back if saved-state persisted, R-4
collections/tags READ-ONLY). O-1/O-2/O-3 fold forward into P05 acceptance.

Governance Gate remains **CLOSED**. Production remains **NOT CERTIFIED**.

*We don't guess. We prove.*
