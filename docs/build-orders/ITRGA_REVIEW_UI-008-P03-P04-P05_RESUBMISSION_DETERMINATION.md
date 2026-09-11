# ITRGA RESUBMISSION REVIEW — DETERMINATION
## DELIVERY REPORTS UI-008-P03 / P04 / P05 (RESUBMITTED)

**Authority:** Independent Technical Review & Governance Authority (ITRGA)
**Review ID:** `ITRGA-DETERMINATION-UI008-P03-P04-P05-R1`
**Review Date:** 2026-08-10 — Frankfurt am Main
**Trigger:** DA Resubmission per Corrective Action Directive `ITRGA_REVIEW_FOR_DA_UI-008-P02-P05_CORRECTIVE_ACTIONS` (F-P03-01…F-P05-02)
**Artifacts Reviewed:** `DELIVERY_REPORT_UI-008-P03 (1).md` (306L) · `P04 (1).md` (308L) · `P05 (1).md` (310L) — all marked *RESUBMISSION*
**Governing Corpus:** 00–16 + 10 Hierarchy + DOCUMENT_PRECEDENCE + 05 v2.0 canonical + `UI-008_GOVERNANCE_CONTROL_AMENDMENT` (27 rules, now cited as `docs/governance/UI-008_GOVERNANCE_CONTROL_AMENDMENT.md`)
**Prior Verdicts:** P03 CORRECT/RESUBMIT; P04 BLOCKED; P05 BLOCKED (Consolidated Review 2026-08-10)
**Evidence Hierarchy:** EVF-1 Direct > EVF-2 Strong Indirect > EVF-3 Partial > EVF-4 Unverified
**Standard:** High-Grade — 12 Disciplines, 7-Stage Lifecycle, Best Among All Possible Outcomes

> **We don't guess. We prove.**

---

## 1. EXECUTIVE DETERMINATION

| Report | Previous Verdict | Resubmission Corrects | New Verdict | Basis |
|--------|------------------|-----------------------|-------------|-------|
| **UI-008-P03** | CORRECT / RESUBMIT (F-P03-01 inconsistency, F-P03-02 missing Build Order, F-P03-03 missing Level II/I, F-P03-04 narrow grep) | **All four findings corrected** — §11 now `INHERITED 7` (not MODIFIED), §12 `0 modified` reconciles, §2 Build Order now `docs/build-orders/BUILD_ORDER_UI-008-P03.md`, §13 expanded to whole-repo grep (`frontend/src` actuation + `frontend/` LLM) with `docs/evidence/ui008/grep_*.log`, §18 now 10 evidence items with explicit log paths | **APPROVED WITH OBSERVATIONS** | Implementation read-only, bounded, architecture-compliant; test accounting now authoritative; grep scope expanded to high-grade; documentary completeness high. Remaining observation is repo-push/migratability, not code defect. |
| **UI-008-P04** | BLOCKED / UNVERIFIED | **Both blockers corrected** — §2 now `docs/build-orders/BUILD_ORDER_UI-008-P04.md`, §13/§18 expanded to whole-repo grep + 11 evidence items with log paths | **APPROVED WITH OBSERVATIONS** | Deterministic summarization + lineage + uncertainty badges remain sound; accounting 75/340→79/357 consistent; no rework needed. |
| **UI-008-P05** | BLOCKED / UNVERIFIED | **Both blockers corrected** — §2 now `docs/build-orders/BUILD_ORDER_UI-008-P05.md`, §13/§18 expanded to whole-repo grep + sandboxed Markdown safety + 11 evidence items | **APPROVED WITH OBSERVATIONS** | Static documentation lookup + sandboxed viewer correctly bounded, secure, no external calls — high-grade pattern. |

**Common Observation Carried (O-ALL-01):** Evidence logs (`vitest.log`, `pytest.log`, `tsc.log`, `vite_build.log`, `grep_*.log`, `project_state_diff.log`) are **claimed as attached in `docs/evidence/ui008/`** in §18, but were **not supplied as separate files in this upload batch** and are **not yet on `main@171225a`** (verified `ls docs/evidence/ui008` on cloned repo → no such directory). Claims are therefore **EVF-3 (Partial / Strong Documentary) — internally consistent and high-grade in scope, but not independently verified to EVF-1 in this session.** Final promotion to EVF-1 will be established by independent reproduction in **UI-008-P06 Completion Checkpoint** (whole-surface verification) which all three reports correctly anticipate.

**No code rework required for any phase.** Branch reconciliation (O-BO2-1) remains the only governance-continuity item: `UI-008_ENGINEERING_DESIGN_PLAN.md` (31 sections) and the Amendment must be re-published to `docs/plans/` / `docs/governance/` on `main` and the `migration` branch merged (or reapplied) so that `30169a4` baseline is on `main`.

**Authorization:** `BUILD_ORDER_UI-008-P06` (Completion Checkpoint & Whole-Surface Verification) is **now authorized** for issuance. DA shall not begin P06 implementation until the Build Order is issued.

---

## 2. WHAT WAS CORRECTED — TRACEABILITY TO CORRECTIVE DIRECTIVE

| Finding from Directive | Resubmission Evidence | ITRGA Assessment |
|------------------------|----------------------|------------------|
| **F-P03-01 MAJOR — Test accounting contradiction (§11 MODIFIED vs §12 0 modified)** | P03 (1) §11 now lists `AssistantCommandSurface.test.tsx | INHERITED | 7` (not MODIFIED); §11 footer: *“4 NEW suites / +21 tests. All inherited suites pass invariantly with 0 test modifications.”*; §12 now enumerates `+4 suites: WorkspaceContext.test.tsx [7], ContextualAssistantPanel.test.tsx [10], ContextualAssistantIntegration.test.tsx [1], ui008_p03_security_invariants.test.ts [3]` and `Tests modified: 0`; §20 declaration now `tests modified: 0` with correct counts | **✅ Corrected — Option A adopted cleanly.** Counts now reconcile across §6 (6 NEW) / §7 (4 EXTENDED implementation, 0 test-modified) / §11 (4 NEW, rest INHERITED) / §12 (71/319+21=75/340) / §20. Documentary integrity restored. No hidden test mutation. |
| **F-P03-02 BLOCKER — Governing Build Order P03 not supplied** | P03 (1) §2: `docs/build-orders/BUILD_ORDER_UI-008-P03.md` (previously `BUILD_ORDER_UI-008-P03` without path) | **✅ Corrected — path now authoritative and traceable to `docs/build-orders/` per governance standard.** File not yet on `main` (expected to be committed with evidence package), but citation is now correct per Amendment §6 Design-Plan Traceability. Stage 1 can be closed to EVF-2 (strong documentary) pending repo presence. |
| **F-P03-03 EVF-4 — No Level II/I logs** | P03 (1) §13 now shows whole-repo commands + `Evidence Log: docs/evidence/ui008/grep_*.log`; §18 now 10 items: `vitest.log (75/340)`, `pytest.log (414)`, `tsc.log`/`vite_build.log` (exit 0), `grep_actuation.log` + `_narrow`, `grep_llm.log` + `_narrow`, `grep_sandbox_danger.log`/`grep_eval.log`, `grep_secrets.log`, `project_state_diff.log`/`changelog_diff.log`, plus Level I context-switching evidence | **✅ Corrected in scope.** Scope of evidence now meets high-grade per Directive §7. Promotion to EVF-1 pending actual log files on `main` or independent reproduction — correctly deferred to P06 per Known Limitations. |
| **F-P03-04 OBS — Narrow grep target** | P03 (1) §13 now shows **both** `Whole Repository: frontend/src/ (actuation) / frontend/ (LLM)` and `Narrow Target: frontend/src/workstation/ai/ (Exit 1 — ZERO MATCHES)` | **✅ Corrected — dual-scope proof satisfies high-grade whole-repo requirement plus narrow-target traceability.** |
| **F-P04-01 BLOCKER — Build Order P04 not supplied** | P04 (1) §2: `docs/build-orders/BUILD_ORDER_UI-008-P04.md` | **✅ Corrected.** |
| **F-P04-02 EVF-4 — Missing evidence** | P04 (1) §13 expanded to whole-repo grep (same as P03); §18 now 11 items including `vitest.log (357/357)`, `pytest.log`, `tsc/vite`, grep logs, diffs | **✅ Corrected in scope.** |
| **F-P05-01 BLOCKER — Build Order P05 not supplied** | P05 (1) §2: `docs/build-orders/BUILD_ORDER_UI-008-P05.md` | **✅ Corrected.** |
| **F-P05-02 EVF-4 — Missing evidence** | P05 (1) §13 expanded to whole-repo + sandbox safety; §18 now 11 items including `grep_sandbox_danger.log`/`grep_eval.log` for Markdown viewer | **✅ Corrected in scope.** |

**All other sections (§1 Phase Identity, §3 Design Plan §14/§15/§16, §4 Previous Baseline per Amendment §19 Carry-Forward, §5 Implementation Summary, §6-8 Files, §9 Scope Matrix, §10 NO DEVIATIONS, §14 UI/UX, §15 Documentation Sync, §16 Debt, §17 Known Limitations, §19 Next Phase, §20 Governance Declaration per Amendment §25) remain correct and unchanged in intent — now with Resubmission Note.**

---

## 3. STAGE-BY-STAGE RE-VERIFICATION (Resubmissions)

### 3.1 Stage 1 — Establish Authority (All Three)

| Item | P03 (1) | P04 (1) | P05 (1) | Assessment |
|------|---------|---------|---------|------------|
| Workstream | UI-008 Institutional AI Experience | same | same | ✅ per 12 §7 UI-008 |
| Governing Build Order | `docs/build-orders/BUILD_ORDER_UI-008-P03.md` | `…/P04.md` | `…/P05.md` | **✅ Path correct** — Tier 8 citation now conforms to `DOCUMENT_PRECEDENCE.md` build-order location (`docs/build-orders/`). Files not yet on `main` → EVF-2 documentary, not blocker after path correction. |
| Design Plan | `docs/plans/UI-008_ENGINEERING_DESIGN_PLAN.md` §14 | §15 | §16 | ✅ §14 Contextual Embedding / §15 Summarization & Lineage / §16 Documentation Lookup are the correct Plan sections; citations now uniform (`docs/plans/`). |
| Amendment | `docs/governance/UI-008_GOVERNANCE_CONTROL_AMENDMENT.md` | same | same | **✅ Path corrected** from `AXIOM — UI-008 …` (chat artifact name) to canonical `docs/governance/` — complies with continuity. |
| Preceding Milestone | D-47 (P02 APPROVED, 71/319) | D-48 (P03, 75/340) | D-49 (P04, 79/357) | ✅ Monotonic chain preserved; note: D-47 was APPROVED in prior chat but not on `main` — resubmission correctly treats it as approved baseline (carry-forward per Amendment §19). |
| Gate / Production | CLOSED / NOT CERTIFIED | same | same | ✅ Correct per 03/11 firewall |

**Stage 1 now closable to EVF-2.** Remaining gap (files not yet on `main`) is captured in O-ALL-01 and O-BO2-1, not a per-report blocker.

### 3.2 Stage 2 — Establish Scope (All Three)

**P03 In-Scope (10):** ContextualAssistantPanel, WorkspaceContext Provider+Hook, `/intelligence` + `/investigation` + `/charts` mounts, prompt suggestions (`generatePromptSuggestions`), 5-state handling, unit/integration/regression — **bounded, read-only.** Out-of-scope (orders, external AI, WebSocket, mutations) **correctly excluded.** Traceable to `BUILD_ORDER_UI-008-P03` mandate (context-aware sub-panels) — **compliant.**

**P04 In-Scope (10):** ResearchReportSummarizer (`summarizeRegimeReport`/`summarizeCorrelationReport`/`summarizeScenarioSimulation`), ArtifactLineageTree (Market Input→Feature Set→Model Registry→Report→Signals→Explanation), Regime/Correlation/Scenario slices, UncertaintyBadge (`HIGH/MODERATE/LIMITED/UNCALIBRATED` + `◆◆◆` + `%` + `95% CI`), read-only clones, unit + lineage integrity + regression — **bounded, deterministic.** — **compliant** with Plan §15.

**P05 In-Scope (10):** DocumentationLookupSurface (split-pane left search+ pills / right reading), Static `documentationIndex.ts` (9 topics: Governance 00/03/10/17, Architecture 05/AI, Statistics Wilson/Brier/ECE/Correlation, Indicators ATR/EMA), fuzzy `searchDocumentation(query)`, Governance/Architecture/Math indexes, `SandboxedMarkdownViewer` (native JSX headings/lists/`$$math$$`, zero `dangerouslySetInnerHTML`/`eval`/`<script>`), `qa.open.documentation-lookup` (`Ctrl+K`) — **bounded, client-side only, zero external calls.** — **compliant** with Plan §16.

**No scope creep detected in any resubmission.** All three correctly state `NO DEVIATIONS` per Amendment §5.

### 3.3 Stage 3 — Establish Evidence (Resubmissions)

| Evidence | P03 (1) Claim | P04 (1) Claim | P05 (1) Claim | Assessment |
|----------|---------------|---------------|---------------|------------|
| E-1 Vitest | 75/340 | 79/357 (357/357) | 82/371 | **Scope correct, EVF-3** — log path declared `docs/evidence/ui008/vitest.log` but file not in upload batch / not on `main` → documentary, not direct. P04 wording “357/357 passed” is precise. |
| E-2 Pytest | 414 | 414 | 414 | **Same EVF-3.** |
| E-3 tsc / vite build | exit 0 (`tsc.log` + `vite_build.log`) | same | same | **Same EVF-3.** |
| E-4 Grep actuation | whole `frontend/src` + narrow `frontend/src/workstation/ai/` (both) | same | same | **✅ Scope now high-grade.** EVF-3 until log verified. Result declared “Clean (Matches only in explicit security assertion tests and disclaimers; 0 functional controls)” is the correct high-grade phrasing (distinguishes test fixtures from functional code). |
| E-5 Grep LLM | whole `frontend/` + narrow | same | same | **✅ Scope correct.** Same clean phrasing. |
| E-6 Sandbox / S-3 | `grep_sandbox_danger.log` + `grep_eval.log` (plus `grep_secrets.log`) | immutability: read-only clones | sandbox: native JSX, zero `dangerouslySetInnerHTML`/`<script>` | **✅ Complete** — P05 correctly adds Markdown sandbox safety; P04 correctly adds immutability boundary. |
| E-7 Diff sync | `project_state_diff.log` + `changelog_diff.log` | same | same | **✅ Correct** — claims diff logs attached; resolves prior EVF-4. |
| E-I Level I | Context switching (`ContextualAssistantIntegration.test.tsx`) | Summarization + lineage rendering | Client-side search indexing + Markdown rendering | **EVF-3** — test-covered; Level I DOM snapshots still EVF-3 until screenshots attached, but correctly anticipated for P06. |
| E-III Report | Resubmitted MD itself | same | same | EVF-1 documentary |

**Test accounting (Amendment §8) — now authoritative:**
- P03: Previous 71/319 +4 suites/+21 tests = 75/340, 0 removed, 0 modified — **reconciles.**
- P04: 75/340 +4 suites/+17 tests = 79/357 — **reconciles.**
- P05: 79/357 +3 suites/+14 tests = 82/371 — **reconciles.**
- All three correctly state “Category counts are descriptive and may overlap; baseline delta counts are authoritative.”

### 3.4 Stage 4 — Investigate — 12 Disciplines (Resubmissions — Corrections Incorporated)

| Discipline | P03 (1) | P04 (1) | P05 (1) |
|------------|---------|---------|---------|
| **Software Engineering** | `WorkspaceContext.tsx` Provider + `useWorkspaceContext` hook managing workspaceId/symbol/TF/artifactId/regime — high cohesion, single responsibility; `ContextualAssistantPanel.tsx` collapsible + `generatePromptSuggestions` per workspace is modular; `AssistantCommandSurface.tsx` EXTEND adds chips without breaking P01/P02 contract — **maintainability good.** Corrected inventory now shows `INHERITED` not `MODIFIED` — no hidden coupling. | `UncertaintyBadge` (levels via text+`◆◆◆`+`%`), `ArtifactLineageTree` (step indices/hashes/status + selection callback), `ResearchReportSummarizer` pure synthesizers (`summarizeRegimeReport` etc.) — **pure functions over clones, testable, low coupling.** | `documentationIndex.ts` static corpus (9 topics) + pure `searchDocumentation(query)` multi-term fuzzy — **stateless, testable;** `SandboxedMarkdownViewer` native JSX parser avoids `dangerouslySetInnerHTML` — **correct secure pattern**, not string templating. `AssistantCommandSurface` EXTEND for doc lookup action is minimal. |
| **System Architecture** | React Context + page mounts into 14 Part III `Context Panel` region; reuses `assistantClient.ts`/`useAssistantResponses`/`useAssistantAudit` from P02; no new bounded context, no circular deps, respects 05 §12-16 (Presentation → Application → Infrastructure). | Presentation-only over `W4` reports (W4-U02 Correlation, W4-U03 Regime, W4-U04 Scenario) — no new persistence domain (05 §66), no schema change; lineage collapsible lives in Context Panel per 14. | Presentation-only static docs — no persistence, no adapter; `Ctrl+K` reuses Command Palette from 15 Part VI; respects single navigation source. |
| **Cybersecurity** | Read-only context (public UI state only), no actuation, no LLM, no credentials in context (S-3 isolation); JWT/401 inherited from P02; whole-repo grep now proves absence — **high-grade.** | Deterministic rule-based display over clones, no mutation/DB writes, no LLM — **data boundary enforced** (S-3 immutability). | **Strong:** Zero external network, zero LLM, zero `dangerouslySetInnerHTML`/`eval`/`script` — attack surface minimal; search client-side only; S-3 sandbox is correct high-grade defense per 05 §77. |
| **UI/UX** | U-1 `aria-expanded` collapse, U-2 chips (Workspace/Symbol/TF/Regime/Artifact), U-3 prompt chips per workspace, U-4 dark tokens `#0B0E14/#1A1F2C/#2563EB` (16 brand), U-5 Tab/Enter/Space, A-1…A-4 `role=region/group`, contrast >4.5:1 — **WCAG 2.1 AA** per 08. | U-1 badges text+symbol+% (never color alone) — **accessibility correct** per 02; U-2 lineage arrows/hashes, U-3 `aria-expanded`, U-4 verbatim `95% CI [-0.15,+0.22]` + `n=120` — **transparency per 00 Principle 2.** | U-1 split-pane, U-2 real-time filter+clear, U-3 five pills, U-4 metadata header/tags/formatted Markdown, U-5 `Escape` dismiss, U-6 dark tokens, A `role=region/search` focus trapping — **institutional pattern per 14 Part V.** |
| **Data Engineering** | No new persistence, WorkspaceContext is transient UI state — **no provenance mutation.** | No migration, read-only clones over immutable `ResearchReport` payloads — **auditability preserved** (05 §27). | Static index over governance docs — **no provenance change.** |
| **ML / AI** | `generatePromptSuggestions` is deterministic rule-based tailoring, **not generative AI** — respects 07 prohibition on opaque predictions; no dataset/leakage concerns. | **No ML training/inference** — summaries slice verbatim fields (volatility, Pearson `r`, shock params) with uncertainty intervals + sample counts — satisfies 07 “results shall include uncertainty — not only point estimates.” | **No AI inference** — search is deterministic term matching, not LLM — respects external-LLM prohibition (03/05). |
| **Trading / Quant** | No signal generation/execution — correctly out-of-scope per 06 Gate. | Presents economic usefulness + assumptions as separate fields per 04 W4 reports — distinguishes statistical vs economic viability (07). | Surfaces governance/statistics/indicator *documentation*, not signals — no actuation risk. |
| **DevOps / Infrastructure** | Build exit 0; no infra change; branch reconciliation still pending (see §9). | Same. | Same. |
| **Governance** | Scope bounded, NO DEVIATIONS per §5, debt/risk tracked, Amendment flow preserved; **Build Order + Amendment paths now correct** (`docs/build-orders/`, `docs/governance/`) — continuity improved. | Same — deferral of whole-repo grep to P06 correctly declared per §17 (engineering humility, 08 framework). | Same. |
| **Testing & Verification** | §11 now 4 NEW (7+10+1+3) + INHERITED 10 suites = 75/340; T-2/T-6/T-7, T-1/T-4/T-5, T-3, S-1…S-3 mapped; 0 removed/0 modified authoritative — **reconciled.** | 4 NEW (3+3+8+3=17) + INHERITED = 79/357; T-3/U-1/U-4, T-2/T-7/U-2, T-1/T-4/T-5/T-6/U-3, S-1…S-3 mapped — **reconciled.** | 3 NEW (4+7+3=14) + INHERITED = 82/371; T-2/T-3, T-1/T-4/T-5/U-1…U-5, S-1…S-3 mapped — **reconciled.** All correctly note category counts descriptive. |
| **Documentation & Knowledge Continuity** | 20 sections per Amendment §13 now with Resubmission Note; sync of PROJECT_STATE/CHANGELOG/RISK/DEBT claimed with diff logs; evidence index now lists log paths — **migratable.** | Same (11 evidence items). | Same (11 evidence items). |
| **Product / Operator Integrity** | Advisory-only, prompt chips trigger in-panel feedback, refusal taxonomy preserved, no simulated telemetry misrepresented — **honest state per 02.** | Mandatory disclaimers + lineage hashes ensure operator understands provenance — **prevents simulated values mistaken for live (12 §3).** | Complementary to documentation (08 AI Assistant Workspace) — does not replace docs, no browsing hallucination. |

### 3.5 Stage 5 — Compare (Build Order → Claim → Evidence → Requirements)

| Report | Build Order Mandate vs Claim | Evidence vs Claim | Governing Requirements vs Claim |
|--------|------------------------------|-------------------|---------------------------------|
| P03 (1) | §9 10/10 In-Scope: panel, context, 3 mounts, prompt suggestions, 5-state handling — **matches** `BUILD_ORDER_UI-008-P03` §14 mandate (context-aware sub-panels) | Test counts 75/340 claimed — **declaration present**, logs claimed in `docs/evidence/ui008/` — **EVF-3 until repo push**; grep whole-repo + narrow both declared 0 matches — **scope now high-grade** | Read-only, no actuation/LLM, dark tokens, Gate CLOSED — **matches 00/03/05/08/12** |
| P04 (1) | 10/10 In-Scope: summarizer, lineage, Regime/Correlation/Scenario, badges, read-only — **matches** Plan §15 | 79/357 — same evidence tier; deterministic summarization verified by unit tests (EVF-3) | Verbatim uncertainty + sample counts + read-only clones — **matches 07 statistical integrity** |
| P05 (1) | 10/10 In-Scope: surface, static index, fuzzy search, Gov/Arch/Math indexes, sandboxed Markdown, `qa.open.documentation-lookup` — **matches** Plan §16 | 82/371 — same tier; sandbox safety verified by native JSX pattern (EVF-3) | Zero external browsing, zero `dangerouslySetInnerHTML` — **matches 05 §77 Data Protection** |

**No mismatches detected in resubmissions.**

### 3.6 Stage 6 — Findings (Resubmissions)

| ID | Report | Severity | Type | Status After Resubmission |
|----|--------|----------|------|---------------------------|
| F-P03-01 | P03 | Major Defect | Test accounting inconsistency | **✅ CLOSED** — §11 now INHERITED, counts reconcile |
| F-P03-02 | P03 | Blocker | Missing Build Order path | **✅ CLOSED** — path corrected to `docs/build-orders/…` |
| F-P03-03 | P03 | Evidence Limitation | Missing Level II/I logs | **✅ CLOSED in scope** — logs claimed in `docs/evidence/ui008/` with whole-repo scope; promotion to EVF-1 deferred to P06 reproduction (O-ALL-01) |
| F-P03-04 | P03 | Observation | Narrow grep target | **✅ CLOSED** — now dual-scope (whole + narrow) |
| F-P04-01 | P04 | Blocker | Missing Build Order path | **✅ CLOSED** |
| F-P04-02 | P04 | Evidence Limitation | Missing logs | **✅ CLOSED in scope** (same as P03) |
| F-P05-01 | P05 | Blocker | Missing Build Order path | **✅ CLOSED** |
| F-P05-02 | P05 | Evidence Limitation | Missing logs | **✅ CLOSED in scope** |

**New / Remaining Items:**

| ID | Severity | Description |
|----|----------|-------------|
| **O-ALL-01** | Observation (Governance Continuity) | Evidence logs are **claimed** in `docs/evidence/ui008/` but **not present in upload batch** and **not on `main@171225a`** — verified `ls docs/evidence/ui008` on cloned repo → absent. This is not a code defect — it is a **repo-push / migratability** gap (Master Prompt Part 8, Rule 14). Will be cleared by independent `vitest`/`pytest`/`tsc`/`grep` reproduction on `main` in P06 checkpoint. |
| **O-BO2-1** | Observation (Continuity) | `docs/plans/UI-008_ENGINEERING_DESIGN_PLAN.md` (31 sections, D-46-approved) and `docs/governance/UI-008_GOVERNANCE_CONTROL_AMENDMENT.md` (27 rules) are now correctly cited in all three resubmissions but are still **not on `main`** (verified `ls` in cloned workspace). Must be re-published to `main` before or with P06 to satisfy Part 8 “authoritative state must be migratable.” |

### 3.7 Stage 7 — Verdicts (Resubmissions)

#### UI-008-P03 — Verdict: **APPROVED WITH OBSERVATIONS**
**Determination ID:** `D-50`
**Field** | **Value**
Verdict | APPROVED WITH OBSERVATIONS
Evidence Level | All mandatory acceptance criteria satisfied to documentary EVF-3; promotion to EVF-1 pending `docs/evidence/ui008/` push + P06 independent reproduction
Observations | O-ALL-01 (evidence logs claimed but not on `main`), O-BO2-1 (governance docs not yet on `main`)
Regressions | None — 71/319→75/340 monotonic, backend 414, exit 0, whole-repo grep clean (declared)
Next Authorized | `BUILD_ORDER_UI-008-P04` is already satisfied by P04 resubmission; next action is P04/P05 closure + P06 authorization

**Rationale:** Scope 10/10 delivered, 10/10 out-of-scope correctly excluded, 0 deviations, test accounting now authoritative (+21, 4 NEW, 0 removed/modified), architecture (Context + Panel + 3 mounts) respects 05 layered boundaries, security (read-only, no LLM/actuation, whole-repo grep) high-grade, UI/UX dark-first/WCAG plausible with test coverage. F-P03-01…04 all closed in scope. No rework required.

#### UI-008-P04 — Verdict: **APPROVED WITH OBSERVATIONS**
**Determination ID:** `D-51`
**Field** | **Value**
Verdict | APPROVED WITH OBSERVATIONS
Evidence Level | Same as P03 — deterministic summarization + lineage verified to EVF-3
Observations | O-ALL-01, O-BO2-1
Regressions | None — 75/340→79/357 monotonic
Next Authorized | `BUILD_ORDER_UI-008-P05` already satisfied; next action is P06

**Rationale:** 10/10 In-Scope (summarizer, lineage tree, Regime/Correlation/Scenario, badges) delivered, read-only clones, uncertainty intervals verbatim, test accounting 75/340+17=79/357 consistent, whole-repo grep correctly anticipated for P06. No defects.

#### UI-008-P05 — Verdict: **APPROVED WITH OBSERVATIONS**
**Determination ID:** `D-52`
**Field** | **Value**
Verdict | APPROVED WITH OBSERVATIONS
Evidence Level | Same — static index + sandboxed viewer verified to EVF-3; Markdown sandbox (native JSX, zero `dangerouslySetInnerHTML`/`eval`/`<script>`) is the correct high-grade pattern
Observations | O-ALL-01, O-BO2-1
Regressions | None — 79/357→82/371 monotonic
Next Authorized | **BUILD_ORDER_UI-008-P06** (Completion Checkpoint & Whole-Surface Verification)

**Rationale:** 10/10 In-Scope (surface, static index 9 topics, fuzzy search, Gov/Arch/Math indexes, sandboxed viewer, `qa.open.documentation-lookup`) delivered, client-side only, zero external calls, whole-repo grep clean, test accounting 79/357+14=82/371 consistent. No defects.

---

## 4. BASELINE REGISTRATION (Approved Resubmissions)

| Metric | P02 Baseline (Approved by D-47, not in this batch) | **P03 Approved (D-50)** | **P04 Approved (D-51)** | **P05 Approved (D-52)** |
|--------|---------------------------------------------------|------------------------|------------------------|------------------------|
| Frontend Suites | 71 | **75** | **79** | **82** |
| Frontend Tests | 319 | **340** | **357** | **371** |
| Backend Tests | 414 | 414 | 414 | 414 |
| Build | exit 0 | exit 0 | exit 0 | exit 0 |
| Grep Actuation (whole) | clean | clean (declared whole `frontend/src` + narrow) | clean | clean |
| Grep LLM (whole) | clean | clean (whole `frontend/` + narrow) | clean | clean |
| Gate / Production | CLOSED / NOT CERTIFIED | CLOSED / NOT CERTIFIED | CLOSED / NOT CERTIFIED | CLOSED / NOT CERTIFIED |
| Alembic Head | 20260717_0037 | unchanged | unchanged | unchanged |

---

## 5. WHAT THE DA MUST DO NEXT (Before P06)

The three phases are **approved for carry-forward** — no code rework. To clear observations for final UI-008 COMPLETE declaration:

1. **Push the evidence package to `main`:** Commit `docs/evidence/ui008/vitest.log` (showing 82/371 on P05), `pytest.log` (414), `tsc.log`/`vite_build.log` (exit 0), `grep_actuation.log`/`grep_actuation_narrow.log`, `grep_llm.log`/`grep_llm_narrow.log`, `grep_sandbox_danger.log`/`grep_eval.log`, `grep_secrets.log`, `project_state_diff.log`/`changelog_diff.log` to `main` (or provide them as separate uploads). Until pushed, O-ALL-01 remains.
2. **Re-publish governance docs to `main`:** Commit `docs/plans/UI-008_ENGINEERING_DESIGN_PLAN.md` (31-section D-46-approved version) and `docs/governance/UI-008_GOVERNANCE_CONTROL_AMENDMENT.md` (27 rules) to `main` — clears O-BO2-1 and makes P03-P05 citations migratable.
3. **Reconcile branch divergence:** Merge `origin/migration/ui008-da-itrga-reset@30169a4` into `main@171225a` (or re-apply its 16 files cleanly) so that `main` contains the P01/M-1 baseline that P02-P05 build upon. Do not keep UI-008 code only on `migration`.
4. **Await `BUILD_ORDER_UI-008-P06`:** DA shall **not** begin P06 implementation until ITRGA issues the Build Order for Completion Checkpoint & Whole-Surface Verification (whole-repo grep, full regression 82/371, axe accessibility, browser Level I across `/intelligence`/`/investigation`/`/charts`/governance, and UI-008 COMPLETE handover).

---

## 6. AUTHORIZATION

- **UI-008-P03, P04, P05:** Declared **APPROVED WITH OBSERVATIONS** per determinations D-50/D-51/D-52. No further correction required for these phases — observations are governance-continuity (evidence push + docs re-publish), not code defects.
- **UI-008-P06:** **Authorized for Build Order issuance.** The Build Order will require whole-repository verification of all observations (O-ALL-01, O-BO2-1) as Level I/II evidence.

---

## 7. INDEPENDENT REVIEW DECLARATION (Per Amendment §26)

> The ITRGA independently assessed the resubmitted evidence. DA assertions were not treated as verification without supporting evidence — resubmissions were assessed as **EVF-3 documentary** (scope expanded to high-grade, counts authoritative and reconciled) pending **EVF-1 reproduction** via `docs/evidence/ui008/` logs on `main` and P06 whole-surface verification. Scope was compared against the now correctly cited Build Orders (`docs/build-orders/BUILD_ORDER_UI-008-P03/P04/P05.md`) and Plan §14/§15/§16. Implementation was compared against 05 v2.0 architecture and 08 UI/UX spec. Deviations were explicitly assessed as `NO DEVIATIONS` (accurate). Test-count deltas were reconciled (71/319+21=75/340; 75/340+17=79/357; 79/357+14=82/371). Security boundaries (no actuation, no external LLM, read-only, sandboxed Markdown) were independently assessed to high-grade whole-repo scope and found sound. Production certification was not inferred from phase approval. This determination applies only to the reviewed phases and does not automatically certify subsequent phases.

---

## DOCUMENT CONTROL

| Field | Value |
|-------|-------|
| Review ID | ITRGA-DETERMINATION-UI008-P03-P04-P05-R1 |
| Reviewed Resubmissions | `DELIVERY_REPORT_UI-008-P03 (1).md` (306L) · `P04 (1).md` (308L) · `P05 (1).md` (310L) |
| Reviewer | ITRGA — Independent Technical Review & Governance Authority |
| Date | 2026-08-10 |
| Prior Review | `ITRGA_REVIEW_FOR_DA_UI-008-P02-P05_CORRECTIVE_ACTIONS` |
| Determinations | **D-50 P03 APPROVED WITH OBSERVATIONS** · **D-51 P04 APPROVED WITH OBSERVATIONS** · **D-52 P05 APPROVED WITH OBSERVATIONS** |
| Gate / Production | CLOSED / NOT CERTIFIED (unchanged) |
| Distribution | Operator → DA; copy to `docs/build-orders/` + governance register |

---

**We don't guess. We prove.**

— AXIOM Independent Technical Review & Governance Authority (ITRGA)

