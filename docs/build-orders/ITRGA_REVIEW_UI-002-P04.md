# ITRGA REVIEW — UI-002-P04
## Global Search Framework · Read-Only Source Adapters · Search Overlay (R-2 / R-5)

**Authority:** Institutional Technical Review & Governance Authority (ITRGA)
**Programme:** AXIOM Institutional UI Transformation · **Workstream:** UI-002 · **Phase:** P04
**Build Order:** `BUILD_ORDER_UI-002-P04.md`
**Evidence pack:** `DELIVERY_REPORT_UI-002-P04.md`, `operator results.md` (correct UI-002-P04 target transcript, 2776 lines), 2 served-session screenshots.
**Determination:** ✅ **APPROVED WITH OBSERVATIONS**
**Authorizes:** `BUILD_ORDER_UI-002-P05` (Context-Aware Workflow Integration & UI-002 Completion Checkpoint) and/or `P04b` (remaining search adapters) — **with a carried hard intake gate (OBS-P04(UI002)-1).**
**Motto:** *We don't guess. We prove.*

---

## 0. Build-identity — PASS
Correct P04 pack: **96** `UI-002-P04` refs, **64** named-test hits, **46** `UI-002-P03` refs. Not stale/wrong-pack. DA does not self-approve.

## 1. Verification matrix (Level-I, line-by-line) — substantively CLEAN
| # | Requirement | Evidence (line) | Verdict |
|---|---|---|---|
| **(c) R-5 read-only result model** | resultAction navigate / readonly / no mutation | `GlobalSearchResult` type-enforced; `test_ui002_global_search_returns_read_only_navigation_results` ✓ (L227); `test_ui002_global_search_never_registers_mutation_or_actuation_results` ✓ (L368) | **PASS** |
| **(d) R-2 first-slice sources EXACT** | workspace+signals+journal+research-collections only | `globalSearchSources.ts` wires `sourceId: workspace/signals/journal/research-collections` (L497–500) via existing read APIs `fetchAdvisorySignals/fetchJournalEntries/fetchResearchManagementBundle` (L491); no other adapters; `test_ui002_global_search_uses_workspace_registry_and_existing_read_sources` ✓ (L526) | **PASS** |
| **(e) No backend expansion** | no new endpoint/table/migration | search-source grep `/api/v1/search\|search_index\|new_search\|fuse.js\|fuzzysort` → **no output** (L650–659); `test_ui002_global_search_adds_no_backend_schema_or_dependency_change` ✓ (L803); alembic head `20260717_0037 (head)` (L128) | **PASS** |
| **(f) No query/artifact persistence** | R-5 | `test_ui002_global_search_does_not_persist_query_text_or_artifact_payloads` ✓ (L951) | **PASS** |
| (g) Six named tests displayed passing | verbose reporter | L227/368/526/803/951 + accessibility test ✓ | **PASS** |
| Accessibility | keyboard + result announcement | `test_ui002_global_search_accessibility_keyboard_and_result_announcement` ✓ | **PASS** |
| (h) No new dependency (UG-15) | first-party matching | no fuzzy lib in source (grep clean); `npm ci` = existing **142 packages** (established count, not new); audit 0 vulns | **PASS** |
| (i) Regression + growth | backend ≥414, frontend grown | frontend **30 files / 121 tests passed** (L1280–1281, up from 29f/115t = +6 P04 tests); backend **414 passed** (L1993, L2613) | **PASS** |
| (k) Networked CI | exit 0 + sentinel | `==> Local CI equivalent complete` + **`LOCAL_CI_EXIT_CODE: 0`** (L2775–2776); audit 0 vulns | **PASS** |
| (j) Browser (served) — R-6 | read-only jump-to | shots: global search overlay open; results across **workspace + signals/journal/research-collections** grouped by workflow (MONITOR/RESEARCH/INVESTIGATE), all labeled **"Navigate"**, "0 read-only navigation results" empty-state, "Search workspaces and read-only artifacts"; Gate CLOSED/research framing | **PASS** |
| Constitutional line | Gate CLOSED, no execution, read-only search | R-5 tests pass; no-actuation; no backend touch by P04 | **PASS** |
| **(a) OBS-P03(UI002)-1 intake gate / no-drift proof** | scoped diff clean + alembic head | `alembic current` = `20260717_0037` ✓; **but scoped diff returned `SCOPED_DIFF_FILENAMES_PRESENT`** — see §2 | **OBSERVATION (carried)** |

## 2. The no-drift proof — investigated; STRUCTURAL FALSE-POSITIVE, no violation (OBS-P04(UI002)-1)
The intake harness ran cleanly this time and printed a definite result — but the result was **`SCOPED_DIFF_FILENAMES_PRESENT`**, listing backend files (`api/router.py`, `routes/ws.py`, `db/models/*`, `pyproject.toml`) **and `frontend/package.json` + `package-lock.json`**. ITRGA investigated rather than reflexively failing or passing:

- The list **includes Wave-0 migrations** (`20260710_0001_w0_u02`, `w0_u03`, `w0_u04`, `20260711_0004_w0_u08`) and the entire Wave-0-onward backend — files no UI-002 frontend phase could author. This is a **`git diff` of the whole uncommitted working tree vs a bare/empty baseline** (no `git log`/committed baseline exists in the DA repo). It is therefore **cumulative history, NOT the P04 delta** — the same artifact seen at P02.
- `frontend/package.json`/`package-lock.json` appear for the same cumulative reason; **no P04 dependency was added** — the search-source grep for fuzzy libs is clean, `npm ci` installed the **existing 142-package** set, and `test_ui002_global_search_adds_no_backend_schema_or_dependency_change` passes.
- **Conclusion:** no evidence of any actual P04 backend/manifest/dependency change; head unchanged; all constitutional gates green. **However, the mandated diff method cannot isolate a phase delta in a repo with no committed baseline** — so the *positive* "P04 is UI-only" proof is structurally unobtainable this way. The `SCOPED_DIFF_FILENAMES_PRESENT` is a **false-positive for drift**, not a finding of drift.

Per operator disposition, this is **Approved with Observations**, with the meaningful no-drift proof **carried to the next delivery report** (not blocking now).

## 3. Observations
- **🔴 OBS-P04(UI002)-1 — carried HARD intake gate for the next delivery (P05 / P04b):** the DA must establish a **phase-isolating baseline** (commit the current tree, or tag/`git stash` per phase) and, with the next delivery, supply a **meaningful UI-only diff that isolates the P04 (+P05/P04b) delta** — e.g. `git diff --stat <pre-P04-ref>..HEAD` or `git diff --stat HEAD` against a committed baseline — **positively showing no backend/API/schema/migration/dependency change** (empty for backend + `package.json`/`package-lock.json`). This supersedes OBS-P03(UI002)-1 and definitively closes the P02→P04 diff-method churn. Include `alembic current` = `20260717_0037`.
- (No substantive/constitutional observation — P04's implementation is clean.)

## 4. Determination & rationale
**APPROVED WITH OBSERVATIONS.** UI-002-P04 global search is substantively clean and constitutional: **R-2 first slice is exactly workspace + signals + journal + research-collections** over existing read APIs; the **R-5 read-only guarantees are type-enforced and test-proven** (read-only navigation results, no mutation/actuation results registrable, no query/artifact persistence); **no backend endpoint/table/migration and no new dependency** (first-party matching, audit 0 vulns); regression grew cleanly (backend 414, frontend 30f/121t); networked CI is green with the sentinel; and the browser confirms read-only jump-to results grouped by workflow. The single outstanding item is the **no-drift proof method**: the mandated scoped `git diff` returned `SCOPED_DIFF_FILENAMES_PRESENT`, which ITRGA determined is a **structural false-positive** (cumulative working tree vs a non-existent committed baseline, including W0 migrations) — not evidence of any P04 drift, and corroborated as non-violating by the head/dep/endpoint checks. Per operator disposition it is carried (OBS-P04(UI002)-1) to be proven meaningfully with the next delivery via a phase-isolating baseline, rather than blocking progression now.

Per the UI-Transformation vocabulary, **Approved with Observations authorizes progression.** → **`BUILD_ORDER_UI-002-P05` (Context-Aware Workflow Integration & UI-002 Completion Checkpoint) is authorized** (and P04b for the remaining search adapters), **carrying OBS-P04(UI002)-1 as a hard intake gate** on the next delivery.

Baseline of record: v0.62.0 · head `20260717_0037` · backend **414** · frontend **30f·121t**. Residuals unchanged & non-blocking: TD-W7-U07-RATE-GUARD, TD-W6-CI-AUDIT (did not recur).

*We don't guess. We prove.*
