# AXIOM — ITRGA FORMAL BUILD ORDER

## `BUILD_ORDER_UI-008-P06`

**Authority:** Independent Technical Review & Governance Authority (ITRGA)
**Determination:** D-52 — UI-008-P05 APPROVED WITH OBSERVATIONS (Resubmission)
**Phase:** UI-008-P06 — Completion Checkpoint & Whole-Surface Verification
**Governing Design Plan:** `docs/plans/UI-008_ENGINEERING_DESIGN_PLAN.md` (Approved per D-46, §17 Completion Checkpoint)
**Governing Amendment:** `docs/governance/UI-008_GOVERNANCE_CONTROL_AMENDMENT.md` — All 27 Rules (Effective P03+)
**Preceding Milestone:** UI-008-P05 (D-52 APPROVED WITH OBSERVATIONS) — 82 suites / 371 tests · 414 backend · exit 0
**Clean Baseline:** Commit `30169a4` / Tag `UI-008-P01-M1_INTEGRATED` (via P02-P05 chain)
**Governance Gate:** CLOSED
**Production Status:** NOT CERTIFIED (Per `11_PRODUCTION_READINESS_CERTIFICATION.md` — Firewall Held Out-of-Band)
**Implementation Hold:** **LIFTED BY THIS BUILD ORDER — DA MAY BEGIN P06 VERIFICATION ONLY** (No new functional development authorized beyond verification/handover)

---

## 1. BUILD ORDER HEADER

| Field | Value |
|-------|-------|
| Build Order ID | `BUILD_ORDER_UI-008-P06` |
| Issued By | ITRGA |
| Issuance Date | 2026-08-10 |
| Status | **AUTHORIZED — DA MAY BEGIN IMPLEMENTATION** |
| Preceding Milestone | UI-008-P05 (D-52) — 82/371 · 414 · exit 0 |
| P05 Baseline | Frontend: 82 suites / 371 tests · Backend: 414 tests · Build: `tsc -b && vite build` exit 0 · Alembic 20260717_0037 |
| Next Milestone | UI-008-P06 Delivery Report → ITRGA Determination → **UI-008 COMPLETE Declaration** (if approved) |
| Amendment Controls | **All 27 rules of UI-008 GOVERNANCE CONTROL AMENDMENT apply** |
| Risk Level | Low (verification/handover only — no new functional surface) |

---

## 2. PHASE OBJECTIVE

Execute the **final completion checkpoint** for `UI-008 — Institutional AI Experience`. Perform **whole-surface, whole-repository verification** of all P01–P05 surfaces, close observations **O-ALL-01** (evidence logs on `main`) and **O-BO2-1** (governance docs migratability + branch reconciliation), and produce the **final handover package** for declaration of **UI-008 COMPLETE**.

This phase is **verification and governance closure, not feature development.**

---

## 3. EXACT SCOPE

### 3.1 In Scope — DA Is Authorized to Deliver:

| # | Deliverable | Description |
|---|-------------|-------------|
| 1 | **Whole-Repository Grep Proofs** | Actuation, external LLM, secrets, sandbox/eval — whole-repo, exit-code proof (see §5) |
| 2 | **Full Regression Suite** | Frontend 82/371 + Backend 414 — captured logs, no test added/removed without accounting |
| 3 | **TypeScript & Vite Build Proof** | `tsc -b` + `vite build` exit 0 — captured logs |
| 4 | **Browser Level I Evidence** | DOM snapshots / screenshots for P03 panel states, P04 badges/lineage tree, P05 split-pane/search/Markdown sandbox across `/intelligence`, `/investigation`, `/charts`, governance |
| 5 | **Accessibility Spot Check** | Axe or equivalent report for P03-P05 surfaces (WCAG 2.1 AA contrast, ARIA, keyboard, focus) — or documented justification if tool unavailable |
| 6 | **Branch & Governance Reconciliation** | Merge `origin/migration/ui008-da-itrga-reset@30169a4` into `main` (or clean re-apply) + re-publish `docs/plans/UI-008_ENGINEERING_DESIGN_PLAN.md` + `docs/governance/UI-008_GOVERNANCE_CONTROL_AMENDMENT.md` to `main` |
| 7 | **Project-State Final Synchronization** | `PROJECT_STATE.md` final UI-008 COMPLETE status, `CHANGELOG.md`, `RISK_REGISTER.md`, `TECHNICAL_DEBT_REGISTER.md` — with diff logs (or explicit NO CHANGE) |
| 8 | **Evidence Package** | `docs/evidence/ui008/` final package — vitest, pytest, tsc/vite, grep logs, diff logs, snapshots — committed to `main` |
| 9 | **Completion Handover Report** | Delivery Report with 20 sections per Amendment §13 + final **UI-008 COMPLETE** declaration readiness |
| 10 | **Observations Closure** | Explicit closure of O-ALL-01 (evidence on `main`) and O-BO2-1 (docs migratable) with evidence references |

### 3.2 Out of Scope — Explicitly NOT Authorized:

| # | Excluded Item | Reason |
|---|--------------|--------|
| 1 | New functional components or panels beyond P01-P05 | P06 is verification only |
| 2 | New backend endpoints, migrations, schema changes | No persistence change |
| 3 | WebSocket streams, real-time push, polling | Not in P06 design |
| 4 | Write/mutation API calls (POST/PUT/PATCH/DELETE) | Read-only invariant |
| 5 | External LLM integration (OpenAI, Anthropic, LangChain, etc.) | Constitutionally prohibited |
| 6 | Order / trade / execution / broker actuation controls | Absolutely prohibited — Gate CLOSED |
| 7 | Script execution in Markdown, `dangerouslySetInnerHTML`, `eval` | Prohibited — sandbox must hold |
| 8 | Styling or brand changes beyond existing tokens | 16 Brand Standard unchanged |
| 9 | Production deployment or Gate opening | 11 Firewall — ITRGA certification separate |
| 10 | Any work beyond UI-008 (e.g., UI-009+) | Phase-bounded |

---

## 4. TECHNICAL REQUIREMENTS

### 4.1 Verification Boundaries

| Boundary | Requirement |
|----------|-------------|
| Functional surfaces | All P01 skeleton + P01-M1 palette + P02 API seams + P03 context/panel + P04 summarizer/lineage/badges + P05 doc lookup — **read-only verification only** |
| Backend | Existing endpoints only (`/api/v1/collaboration/assistant-responses`, `/api/v1/persistence/audit-events`, etc.) — no new endpoints |
| Data | No mutation of `ResearchReport`, `AuditEvent`, `AssistantResponse` — clones only |
| Branch | `main` must be single authoritative worktree after reconciliation (no divergent `migration` state) |

### 4.2 Architecture Compliance (05 v2.0)

P06 must preserve layered architecture (Presentation → Application → Infrastructure), bounded contexts, single ownership, no circular deps. Verification is presentation-layer read surfaces only — no new bounded context.

### 4.3 State

No new UI states beyond P03-P05 (loading/error/empty/auth + badges/lineage/split-pane). Verification confirms existing states still render.

---

## 5. SECURITY REQUIREMENTS — CONSTITUTIONAL INVARIANTS (Non-Negotiable)

Any violation = **BLOCKER.**

| # | Prohibition | Enforcement — DA Must Provide |
|---|-------------|-------------------------------|
| 1 | No order, buy, sell, execute, trade, order ticket controls | **Whole-repo grep** `frontend/src` (see §8 E-4) — 0 functional matches |
| 2 | No external LLM API calls (OpenAI, Anthropic, LangChain, `external_llm`, Cohere, Mistral, Gemini) | **Whole-repo grep** `frontend/` — 0 functional matches |
| 3 | No `dangerouslySetInnerHTML` in `SandboxedMarkdownViewer` | Grep `dangerouslySetInnerHTML` in `frontend/src/workstation/ai/` — 0 matches |
| 4 | No `eval` / `new Function` | Grep `eval\(|new Function` in `frontend/src/workstation/ai/` — 0 matches |
| 5 | No hardcoded secrets / credentials | Whole-repo secrets scan grep — 0 real secrets (fixtures with `REPLACE_ME` acceptable, must be explained) |
| 6 | No unauthenticated data access | 401 handling inherited from P02/P03 — verified by existing tests |
| 7 | No cross-operator data leakage | JWT isolation — verified by existing tests + context isolation |

### Required Security Tests

| # | Test | Pass Criterion |
|---|------|----------------|
| S-1 | Whole-repo actuation grep | `grep -R -i -E "buy|sell|place.*order|execute.*trade|order.*ticket" frontend/src` → exit 1 (CLEAN) |
| S-2 | Whole-repo LLM grep | `grep -R -i -E "openai|anthropic|langchain|external_llm|cohere|mistral|gemini" frontend/` → exit 1 (CLEAN) |
| S-3 | Sandbox safety grep | `dangerouslySetInnerHTML` → exit 1 ; `eval\(|new Function` → exit 1 |
| S-4 | Secrets scan | `api.?key|secret|jwt.?secret|password\s*=` → 0 real secrets |
| S-5 | Narrow-target grep (traceability) | `frontend/src/workstation/ai/` actuation/LLM → exit 1 (for continuity with P03-P05) |

---

## 6. UI/UX REQUIREMENTS

Verification, not new design. DA must demonstrate that P03-P05 surfaces still satisfy:

| # | Requirement | Verification |
|---|-------------|--------------|
| U-1 | P03 collapsible panel `aria-expanded`, P04 badges `HIGH/MODERATE/LIMITED` with `◆◆◆` + `%` + `95% CI`, P04 lineage arrows/hashes, P05 split-pane + 5 pills | DOM snapshots / screenshots |
| U-2 | Dark-first tokens `#0B0E14/#1A1F2C/#2563EB` (16 brand) | Visual inspection / CSS |
| U-3 | Keyboard: Tab/Enter/Space for chips/collapse, `Escape` for P05 dismiss | Manual or test evidence |
| A-1…A-4 | ARIA `region`/`group`/`search`/`list`, semantic headings, focus trapping, contrast >4.5:1 | Axe report or documented spot check |

---

## 7. TESTING REQUIREMENTS

### 7.1 New Tests

**None required.** P06 is verification — DA may add **0–2** verification-only tests if needed to prove whole-surface behavior, but must account for them per Amendment §8.

### 7.2 Regression — Mandatory Pass Criteria

| # | Requirement | Pass Criterion |
|---|-------------|----------------|
| R-1 | Frontend suite | **82 suites / 371 tests — 100% pass** (or higher if DA adds verification tests — must then be 82+/371+ and accounted) |
| R-2 | Backend suite | **414 tests — 100% pass** |
| R-3 | TypeScript build | `tsc -b` exit 0 **and** `vite build` exit 0 |

### 7.3 Negative Tests (Confirm Still Passing)

N-1 malformed data → error, N-2 empty → empty, N-3 timeout → error, N-4 401 → graceful — existing P02-P03 tests already cover; no new negative tests required unless verification reveals gap.

---

## 8. EVIDENCE REQUIREMENTS

### 8.1 Required Evidence for ITRGA Review (All Level II/I Must Be Committed to `main` in `docs/evidence/ui008/`)

| # | Evidence | Type | Requirement | File |
|---|----------|------|-------------|------|
| E-1 | Vitest log | Level II | **82/371 pass** (or 82+/371+ if added) — full log, not summary | `docs/evidence/ui008/vitest.log` |
| E-2 | Pytest log | Level II | **414 pass** — full log | `docs/evidence/ui008/pytest.log` |
| E-3 | tsc + vite build logs | Level II | Both exit 0 — full logs + `echo EXIT:$?` | `docs/evidence/ui008/tsc.log`, `vite_build.log` |
| E-4 | Grep actuation — **whole `frontend/src`** | Level II | 0 functional matches — full transcript + `echo ACTUATION_GREP_EXIT:$?` | `docs/evidence/ui008/grep_actuation.log` |
| E-5 | Grep LLM — **whole `frontend/`** | Level II | 0 functional matches | `docs/evidence/ui008/grep_llm.log` |
| E-6 | Grep sandbox — `dangerouslySetInnerHTML` | Level II | 0 matches | `docs/evidence/ui008/grep_sandbox_danger.log` |
| E-7 | Grep eval — `eval(\|new Function` | Level II | 0 matches | `docs/evidence/ui008/grep_eval.log` |
| E-8 | Grep secrets scan | Level II | 0 real secrets (fixtures explained) | `docs/evidence/ui008/grep_secrets.log` |
| E-9 | Narrow-target greps (traceability) | Level II | 0 matches in `frontend/src/workstation/ai/` | `docs/evidence/ui008/grep_actuation_narrow.log`, `grep_llm_narrow.log` |
| E-10 | Project-state diffs | Level II | `git diff HEAD -- PROJECT_STATE.md` + `CHANGELOG.md` + `RISK_REGISTER.md` + `TECHNICAL_DEBT_REGISTER.md` (or explicit NO CHANGE) | `docs/evidence/ui008/project_state_diff.log`, `changelog_diff.log` etc. |
| E-11 | Branch reconciliation proof | Level II | `git log --oneline --all --graph` + `git diff main..HEAD` showing `main` now contains `30169a4` baseline + governance docs | `docs/evidence/ui008/branch_reconciliation.log` |
| E-12 | Browser Level I snapshots | Level I | DOM snapshots / screenshots: P03 panel, P04 badges/lineage, P05 split-pane/search/Markdown | `docs/evidence/ui008/snapshots/` |
| E-13 | Accessibility spot check | Level II | Axe report or documented spot check for P03-P05 | `docs/evidence/ui008/accessibility.log` |
| E-14 | Delivery Report | Level III | `DELIVERY_REPORT_UI-008-P06.md` with 20 sections per §9 | `DELIVERY_REPORT_UI-008-P06.md` |

**Evidence Hierarchy:** Level I (Direct Runtime — snapshots, HTTP transcripts) > Level II (Automated — vitest/pytest/tsc/grep) > Level III (Documentary — Delivery Report). Declarations without logs are EVF-4.

### 8.2 Commands to Generate Evidence (Run on `main` After Reconciliation)

```bash
# 1. Frontend + Backend + Build (from repo root)
npm ci
npm run test -- --run 2>&1 | tee docs/evidence/ui008/vitest.log; echo "VITEST_EXIT:$?"
pytest -q 2>&1 | tee docs/evidence/ui008/pytest.log; echo "PYTEST_EXIT:$?"
npx tsc -b 2>&1 | tee docs/evidence/ui008/tsc.log; echo "TSC_EXIT:$?"
npm run build 2>&1 | tee docs/evidence/ui008/vite_build.log; echo "BUILD_EXIT:$?"

# 2. Whole-repo security greps
grep -R -n -i -E "buy|sell|place.*order|execute.*trade|order.*ticket" --include="*.ts" --include="*.tsx" frontend/src 2>&1 | tee docs/evidence/ui008/grep_actuation.log; echo "ACTUATION_GREP_EXIT:$?"
grep -R -n -i -E "openai|anthropic|langchain|external_llm|cohere|mistral|gemini" --include="*.ts" --include="*.tsx" frontend/ 2>&1 | tee docs/evidence/ui008/grep_llm.log; echo "LLM_GREP_EXIT:$?"
grep -R -n "dangerouslySetInnerHTML" --include="*.tsx" frontend/src/workstation/ai/ 2>&1 | tee docs/evidence/ui008/grep_sandbox_danger.log; echo "SANDBOX_DANGER_EXIT:$?"
grep -R -n "eval\(|new Function" --include="*.ts" --include="*.tsx" frontend/src/workstation/ai/ 2>&1 | tee docs/evidence/ui008/grep_eval.log; echo "EVAL_GREP_EXIT:$?"
grep -R -n -i -E "api.?key|secret|jwt.?secret|password\s*=" --include="*.ts" --include="*.tsx" --include="*.env*" frontend/ 2>&1 | tee docs/evidence/ui008/grep_secrets.log; echo "SECRETS_GREP_EXIT:$?"
grep -R -n -i -E "buy|sell|place.*order|execute.*trade" --include="*.ts" --include="*.tsx" frontend/src/workstation/ai/ frontend/src/api/assistantClient.ts 2>&1 | tee docs/evidence/ui008/grep_actuation_narrow.log
grep -R -n -i -E "openai|anthropic|langchain|external_llm" --include="*.ts" --include="*.tsx" frontend/src/workstation/ai/ frontend/src/api/assistantClient.ts 2>&1 | tee docs/evidence/ui008/grep_llm_narrow.log

# 3. Documentation & branch diffs
git diff HEAD -- PROJECT_STATE.md 2>&1 | tee docs/evidence/ui008/project_state_diff.log
git diff HEAD -- CHANGELOG.md 2>&1 | tee docs/evidence/ui008/changelog_diff.log
git log --oneline --all --graph --decorate | head -n 40 2>&1 | tee docs/evidence/ui008/branch_reconciliation.log
```

---

## 9. DELIVERY REPORT REQUIREMENTS

DA shall produce `DELIVERY_REPORT_UI-008-P06.md` with **all 20 sections per Amendment §13:**

| # | Section | Content |
|---|---------|---------|
| 1 | Phase Identity | UI-008-P06 — Completion Checkpoint & Whole-Surface Verification |
| 2 | Governing Build Order | `BUILD_ORDER_UI-008-P06` (this document) |
| 3 | Design Plan Reference | `docs/plans/UI-008_ENGINEERING_DESIGN_PLAN.md` §17 |
| 4 | Previous Baseline | P05: 82 suites / 371 tests · 414 backend (D-52) |
| 5 | Implementation Summary | What was verified (not built) — whole-surface scope |
| 6 | Files Created | List with nature (likely 0 new functional files; evidence files only) |
| 7 | Files Modified | List (likely 0 or only docs/evidence/ + PROJECT_STATE/CHANGELOG) |
| 8 | Files Removed | List (likely 0) |
| 9 | Scope Compliance | In-scope (10 verification deliverables) / Out-of-scope (10 exclusions) matrix — must show NO DEVIATIONS |
| 10 | Deviations | Per Amendment §5 — `NO DEVIATIONS` or deviation table |
| 11 | Test Inventory | Per §9 — per-suite listing; must reconcile 82/371 baseline (0 new or explicit +N) |
| 12 | Regression Results | Per §10 — previous 82/371 vs current (must be ≥82/371) |
| 13 | Security Evidence | Grep transcripts E-4…E-9 — whole-repo proofs |
| 14 | UI/UX Evidence | Level I snapshots + accessibility spot check |
| 15 | Documentation Changes | PROJECT_STATE.md / CHANGELOG.md / RISK / DEBT — with diff logs or explicit NO CHANGE |
| 16 | Technical Debt Changes | 0 new (or explicit new debt with rationale) — `TD-UI-POSTCSS-HIGH`, `OBS-P06-2` carried |
| 17 | Known Limitations | Likely “None — UI-008 verification complete” or remaining observation |
| 18 | Evidence Index | Complete list E-1…E-14 |
| 19 | Next Phase Recommendation | `UI-008 COMPLETE` declaration (or next workstream if any) |
| 20 | DA Sign-off | Governance Declaration per Amendment §25 |

### 9.1 Mandatory Registers

**Deviation Register (§5):**
```text
## Deviations From Approved Build Order

[NO DEVIATIONS] — or deviation table with rationale
```

**Test Accounting (§8):**
```text
Previous Baseline:
- Frontend: 82 suites / 371 tests
- Backend: 414 tests

New tests physically added:
- [0 or N — list suites]

Tests removed: 0 (or N)
Tests modified: 0 (or N — explain)

Current total:
- Frontend: [82 or 82+N] suites / [371 or 371+N] tests
- Backend: 414 tests
```

**Carry-Forward Declaration (§19):**
```text
Previous Approved Baseline:
- Commit: 30169a4 / Tag UI-008-P01-M1_INTEGRATED (via P02-P05 chain)
- ITRGA: D-50 / D-51 / D-52

Inherited Components: assistantClient.ts, useAssistantResponses/audit, WorkspaceContext.tsx, ContextualAssistantPanel.tsx, ResearchReportSummarizer.tsx, ArtifactLineageTree.tsx, UncertaintyBadge.tsx, documentationIndex.ts, DocumentationLookupSurface.tsx, AssistantCommandSurface.tsx (P02-P05), AssistantAuditSubSection.tsx

Inherited Tests: 82 suites / 371 frontend + 414 backend (P05 D-52)

Inherited Debt: TD-UI-POSTCSS-HIGH, OBS-P06-2

Inherited Observations: O-ALL-01, O-BO2-1 (to be closed in this phase)

New Phase Scope: Whole-surface verification only (10 deliverables, §3.1)
```

---

## 10. PROJECT-STATE SYNCHRONIZATION

Upon ITRGA **APPROVED** of P06, DA shall update and commit (with diff logs in evidence):

| Document | Update Required |
|----------|-----------------|
| `PROJECT_STATE.md` | Record **UI-008-P06 APPROVED** and **UI-008 — Institutional AI Experience COMPLETE** (version increment per governance) |
| `CHANGELOG.md` | Record P06 completion |
| `RISK_REGISTER.md` | Verify no new risks, or record new risk with mitigation |
| `TECHNICAL_DEBT_REGISTER.md` | Verify 0 new debt, or record new debt with rationale |

If no change required for a file, Delivery Report §15 must state explicitly:
```text
PROJECT_STATE.md — NO CHANGE REQUIRED
Reason: [reason]
```

---

## 11. BUILD ORDER SEQUENCE

```text
[ BUILD_ORDER_UI-008-P06 Issued ]  ← THIS DOCUMENT
         ↓
[ DA Whole-Surface Verification & Evidence Capture ]
         ↓
[ DA Delivery Report (20 sections) ]
         ↓
[ ITRGA Independent Review (7-Stage + 12 Disciplines) ]
         ↓
[ Correction (if required) ]
         ↓
[ ITRGA P06 Determination → UI-008 COMPLETE (if APPROVED) ]
         ↓
[ UI-008 COMPLETE Declaration → Next Workstream or Production Readiness Certification (11) — Separate Governance ]
```

---

## 12. ACCEPTANCE CRITERIA

| # | Criterion | Type | Evidence |
|---|-----------|------|----------|
| AC-1 | Whole-repo actuation grep 0 functional matches (whole `frontend/src`) | Mandatory | E-4 transcript exit 1 |
| AC-2 | Whole-repo LLM grep 0 functional matches (whole `frontend/`) | Mandatory | E-5 exit 1 |
| AC-3 | Sandbox safety: 0 `dangerouslySetInnerHTML` + 0 `eval` | Mandatory | E-6/E-7 exit 1 |
| AC-4 | Secrets scan 0 real secrets | Mandatory | E-8 |
| AC-5 | Frontend regression 82/371 pass (or 82+/371+ with accounting) | Mandatory | E-1 vitest.log |
| AC-6 | Backend regression 414 pass | Mandatory | E-2 pytest.log |
| AC-7 | tsc + vite build exit 0 | Mandatory | E-3 |
| AC-8 | Branch + governance docs on `main` (merge proof + `docs/plans/` + `docs/governance/` on `main`) | Mandatory | E-11 + presence on `main` |
| AC-9 | Project-state docs synchronized (or explicit NO CHANGE) | Mandatory | E-10 diff logs |
| AC-10 | Browser Level I snapshots for P03-P05 surfaces + accessibility spot check | Mandatory | E-12/E-13 |
| AC-11 | No deviations beyond authorized verification scope | Mandatory | §10 `NO DEVIATIONS` |
| AC-12 | NO new actuation/LLM/execution/browsing/script controls introduced | Mandatory | E-4…E-7 |
| AC-13 | Observations O-ALL-01 + O-BO2-1 closed with evidence references | Mandatory | §15/§18 |
| AC-14 | Delivery Report with 20 sections per Amendment §13 + Governance Declaration §25 | Mandatory | Document |
| AC-15 | Evidence package committed to `main` in `docs/evidence/ui008/` | Mandatory | On `main` |

All 15 criteria are **blocking.** One failure = CORRECT/RESUBMIT or REJECTED.

---

## 13. ISSUANCE

This Build Order is issued by the ITRGA and is **effective upon receipt.**

**The DA is authorized to begin P06 verification only** — no new functional development beyond §3.1.

---

## 14. REFERENCES

| Reference | Document |
|-----------|----------|
| Design Plan | `docs/plans/UI-008_ENGINEERING_DESIGN_PLAN.md` §17 (Completion Checkpoint) |
| P06 Design | §17 of Design Plan |
| P05 Baseline | D-52: 82 suites / 371 tests · 414 backend · exit 0 |
| Amendment | `docs/governance/UI-008_GOVERNANCE_CONTROL_AMENDMENT.md` (27 rules) |
| System Architecture | `docs/governance/05_SYSTEM_ARCHITECTURE.md` v2.0 |
| Security Standard | `docs/governance/17_INSTITUTIONAL_SECURITY_STANDARD.md` (cited in prior Build Orders) |
| Production Certification | `docs/governance/11_PRODUCTION_READINESS_CERTIFICATION.md` — **Firewalled, not in scope** |
| Brand Governance | `docs/governance/16_BRAND_GOVERNANCE_STANDARD.md` |

---

## 15. AMENDMENT COMPLIANCE — 27 RULES

| Rule | Compliance in This Build Order |
|------|-------------------------------|
| §2 Historical Baseline | P05 D-52 (82/371) preserved as previous baseline |
| §3 Single Active Phase | **P06 = ACTIVE**, P07+ = NOT AUTHORIZED, P01-P05 = CLOSED |
| §4 Build Order Contract | Scope §3.1/§3.2 enforced as contract; deviations require declaration |
| §5 Deviation Register | Required in Delivery Report §10 |
| §6 Design-Plan Traceability | Must reference Plan §17 |
| §7 API/Architecture Changes | Must be documented (likely 0) |
| §8 Test Accounting | Mandatory per §9.1 — previous/added/removed/modified/current |
| §9 Test Inventory | Per-suite listing per §11 |
| §10 Regression Baseline | P05 82/371 as baseline, vs current |
| §11 Evidence Hierarchy | Level I/II/III classified per §8 |
| §12 ITRGA Independence | Maintained — DA verifies, ITRGA determines |
| §13 Delivery Report Completeness | 20 sections required per §9 |
| §14 Project-State Sync | Required per §10 |
| §15 Authority Separation | DA verifies, ITRGA approves, Operator authorizes |
| §16 No Silent Changes | Enforced — whole-repo grep prevents silent actuation/LLM |
| §17 Production Firewall | Maintained — Gate CLOSED, NOT CERTIFIED |
| §18 Phase Boundary | Enforced — no new functional scope |
| §19 Carry-Forward | Required per §9.1 |
| §20 Correction Rule | Enforced — CORRECT/RESUBMIT if AC fails |
| §21 No Premature Next-Phase | Enforced — UI-008 COMPLETE only after P06 APPROVED |
| §22 Chat Continuity | Applied — branch reconciliation + docs re-publish required |
| §23 Continuity Confirmation | Confirmed — D-50/D-51/D-52 preserved |
| §24 P06 Controls | Applied — whole-surface verification |
| §25 Delivery Declaration | Required per §20 Governance Declaration |
| §26 ITRGA Declaration | Included in P06 Review |
| §27 Governing Principle | Applied — evidence before assertion |

---

**End of BUILD_ORDER_UI-008-P06**

*This Build Order is an ITRGA governance artifact. Implementation beyond §3.1 is out-of-scope and will not be reviewed.*

**We don't guess. We prove.**

— AXIOM Independent Technical Review & Governance Authority (ITRGA)

