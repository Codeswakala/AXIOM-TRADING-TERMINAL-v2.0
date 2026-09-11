# ITRGA REVIEW — UI-004-P01
## Research Workspace Frame · Data-Source Inventory · No-Recompute Guardrail

**Authority:** Institutional Technical Review & Governance Authority (ITRGA)
**Programme:** AXIOM Institutional UI Transformation · **Workstream:** UI-004 · **Phase:** P01
**Build Order:** `BUILD_ORDER_UI-004-P01.md`
**Evidence pack:** `DELIVERY_REPORT_UI-004-P01.md`, `operator results.md` (correct UI-004-P01 transcript, 1912 lines), 4 served-session screenshots.
**Determination:** ✅ **APPROVED** (CI env-flake waived by operator)
**Authorizes:** `BUILD_ORDER_UI-004-P02` (Advisory Signals integration; analytics split to P02b per R-3).
**Motto:** *We don't guess. We prove.*

---

## 0. Build-identity — PASS
Correct P01 pack: `DELIVERY_REPORT_UI-004-P01.md` Phase UI-004-P01; transcript **77** P01 refs; **28** named-test hits. Not stale/wrong-pack. DA does not self-approve. Operator disclosed network dropped mid-final-command (assessed §2, CI).

## 1. Verification matrix (Level-I, line-by-line)
| # | Requirement | Evidence (line) | Verdict |
|---|---|---|---|
| (b) Five named tests displayed passing | verbose reporter | mounts_inside_single_ui001_shell (L135) · registers_through_ui002_navigation_only (L136) · maps_every_surface_to_existing_sources (L137) · **contains_no_recompute_inference_or_signal_generation** (L138) · **preserves_gate_closed_research_only_branding** (L139) | **PASS** |
| **(c) 🔴 No-recompute/no-inference grep (R-6 spine)** | clean | `inferSignal\|runInference\|authoritativeRecompute\|emitSignal\|generateSignal\|recompute\|recalculat\|deriveConfidence\|new .*Engine\|/api/v1/orders` → **"Expected: no output above."** (L147–150) | **PASS** |
| (d) Data-source inventory (existing sources) | existing APIs only | surfaces read `fetchInstitutionalIntelligenceBundle` / `fetchAdvisorySignals` / `fetchAdvisoryAnalytics` / `fetchResearchManagementBundle`; browser cards show verbatim `economic_verdict`/`economic_usefulness`/`not_assessed` + sample counts + uncertainty + lineage; `maps_every_surface_to_existing_sources` ✓ | **PASS** |
| Verbatim-integrity / no-cherry-picking readiness | stored values as-is | report cards render `not_assessed` verbatim; sample counts + uncertainty + limitations ("Uncertainty missing" shown honestly) + lineage visible | **PASS** |
| (e) No-actuation source grep | clean | research-workspace source → clean | **PASS** |
| (f) No-drift + NO registry change (R-1) | head + registry | `alembic current` = **`20260717_0037 (head)`** (L368); only existing `lightweight-charts`; `workspaceRegistry.tsx` shows **pre-existing** `research.intelligence`/`/intelligence` — **no new/relabeled route** ("no /research-intelligence route"); enhanced existing route only | **PASS** |
| (g) Full-suite regression + growth (R-7) | ≥36f/151t, no test lost | full `vitest run` → **37 files / 156 tests passed** (L740–741; Tee'd file L758–759) = +1 file/+5 tests, no loss; backend **414 passed** (L1279, L1899) | **PASS** |
| **(h) 🔴 Doc 16 brand (B-1…B-7)** | palette/typography/institutional | tokens `--ix-color-primary/success/warning/critical` (B-2); `--font-mono` (B-3); `Stored-value guardrail`/`Gate CLOSED · Research-only` + institutional-not-retail copy (B-5); responsive `@media (max-width:760px)` (B-6); **no-hardcoded-color grep in production TSX → no output**; branding test passing | **PASS** |
| (i) Browser (served) — R-7 | frame + framing + brand | shots: Research & Intelligence workspace in-shell; **Stored-value guardrail** (Gate CLOSED · Research-only · Existing read sources only); data-source inventory cards (each → existing API); report cards verbatim (correlation/trend/portfolio_risk with `not_assessed`, sample counts, uncertainty, lineage); "Research context only… not financial advice… operator decides"; logged-out block | **PASS** |
| Constitutional line | Gate CLOSED, no recompute/AI/execution | R-6 grep + test; no external AI; no live data; no actuation | **PASS** |
| (j) Local CI | exit 0 or waived | `LOCAL_CI_EXIT_CODE: 1` — offline `npm audit` `read ECONNRESET` AFTER **backend 414 + full frontend 37f/156t green** = TD-W6-CI-AUDIT env-flake | **WAIVED by operator** |

## 2. CI disposition (network-drop-induced env-flake)
CI ran substantive gates green — backend **414**, full frontend **37f/156t** — then died at offline npm-audit (`read ECONNRESET`) → `LOCAL_CI_EXIT_CODE: 1`, no sentinel (run ended at audit). Operator disclosed the network disconnected during this command. Recurring **TD-W6-CI-AUDIT** class after all substantive gates green. **Operator waived** (consistent with all prior). Fix: networked rerun / graceful-audit; never `strict-ssl false`.

## 3. Determination & rationale
**APPROVED (clean; CI env-flake waived).** On the highest-risk domain workstream, its first phase establishes the constitutional spine cleanly: the research workspace is **presentation over existing governed data with the no-recompute guardrail proven** (named test + grep clean), every surface **maps to an existing governed read API**, stored verdicts (`not_assessed`, `economic_verdict`) render **verbatim** with sample counts/uncertainty/limitations/lineage (no-cherry-picking readiness), the advisory boundary is read-only, and there is **no registry change** (enhanced existing `/intelligence`, R-1 honored). Full-suite regression grew cleanly to **37f/156t with no test lost** (UI-003-P05 lesson honored), backend 414, head unchanged, no new dependency. The **Doc 16 brand gate (B-1…B-7) passes** (constitutional palette tokens, monospace typography, institutional-not-retail, responsive, no-hardcoded-color grep clean). The sole non-green item is the offline-audit CI exit-1 — network-drop-induced TD-W6-CI-AUDIT — **waived by operator**.

Per the vocabulary, **Approved authorizes progression.** → **`BUILD_ORDER_UI-004-P02` (Advisory Signals integration) is authorized**, with **analytics split to P02b (R-3)**, and carrying **R-6 (no-recompute spine)** + **R-7 (Level-I + Doc 16 + full-suite ≥ baseline)**. R-2 (raw-psql if saved-state) binds P05; R-4 (collections read-only) stands.

Baseline of record: v0.62.0 · head `20260717_0037` · backend **414** · frontend **37f·156t**. Residuals unchanged & non-blocking: TD-W7-U07-RATE-GUARD, TD-W6-CI-AUDIT, UI-002-P04b.

*We don't guess. We prove.*
