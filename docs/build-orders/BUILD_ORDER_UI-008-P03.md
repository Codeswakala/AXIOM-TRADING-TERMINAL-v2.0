# AXIOM — ITRGA FORMAL BUILD ORDER

## `BUILD_ORDER_UI-008-P03`

**Authority:** Independent Technical Review & Governance Authority (ITRGA)
**Phase:** UI-008-P03 — Contextual Assistant & Workspace Embedding
**Governing Design Plan:** `docs/plans/UI-008_ENGINEERING_DESIGN_PLAN.md` (Approved per D-46)
**Preceding Determination:** D-47 — UI-008-P02 APPROVED
**Amendment:** UI-008 GOVERNANCE CONTROL AMENDMENT (effective P03+)
**Governance Gate:** CLOSED
**Production Status:** NOT CERTIFIED

---

## 1. BUILD ORDER HEADER

| Field | Value |
|-------|-------|
| Build Order ID | `BUILD_ORDER_UI-008-P03` |
| Issued By | ITRGA |
| Issuance Date | 2026-08-10 |
| Status | **AUTHORIZED — DA MAY BEGIN IMPLEMENTATION** |
| Preceding Milestone | UI-008-P02 (D-47) |
| P02 Baseline | 71 suites / 319 tests · 414 backend · exit 0 |
| Next Milestone | UI-008-P03 Delivery Report |
| Amendment Controls | All 27 rules of UI-008 GOVERNANCE CONTROL AMENDMENT apply |

---

## 2. PHASE OBJECTIVE

Embed context-aware assistant sub-panels into the primary Context Panel across `/intelligence`, `/investigation`, and `/charts` workspaces, providing dynamic contextual prompts based on active symbol, timeframe, and research artifacts.

---

## 3. EXACT SCOPE

### 3.1 In Scope

The DA is authorized to implement:

| # | Deliverable | Description |
|---|-------------|-------------|
| 1 | **ContextualAssistantPanel Component** | New component for workspace-embedded assistant context |
| 2 | **Workspace Context Provider** | React Context providing active workspace state (symbol, timeframe, artifact) |
| 3 | **`/intelligence` Integration** | Market Intelligence context embedding |
| 4 | **`/investigation` Integration** | Signal Investigation context embedding |
| 5 | **`/charts` Integration** | Active Symbol context embedding |
| 6 | **Contextual Prompt Suggestions** | Automated prompts based on active context |
| 7 | **State Transitions** | Loading, error, empty, ready states |
| 8 | **Unit Tests** | Component and hook tests |
| 9 | **Integration Tests** | Context switching tests |
| 10 | **Regression Suite** | All existing tests continue passing |

### 3.2 Out of Scope

The following are **explicitly excluded** from this Build Order:

| # | Excluded Item | Reason |
|---|--------------|--------|
| 1 | Autonomous chart manipulation | Prohibited — operator confirmation required |
| 2 | Order execution controls | Absolutely prohibited |
| 3 | External LLM integration | Constitutionally prohibited |
| 4 | WebSocket real-time streams | Not in P03 design |
| 5 | New backend endpoints | Use existing endpoints only |
| 6 | Database migrations | Not required |
| 7 | AssistantReviewSubPanel enhancement | Deferred to future phase |
| 8 | DocumentationLookupSurface | P05 scope |
| 9 | ResearchReportSummarizer | P04 scope |
| 10 | Write/mutation API calls | Read-only only |

---

## 4. TECHNICAL REQUIREMENTS

### 4.1 Contextual Assistant Boundaries

| Boundary | Requirement |
|----------|-------------|
| **Supported Surfaces** | `/intelligence`, `/investigation`, `/charts` Context Panel regions |
| **Supported Contexts** | Active symbol, timeframe, selected artifact, market regime |
| **Allowed Data** | Read-only workspace state, symbol identifiers, timeframe parameters |
| **Prohibited Data** | Trading signals, order parameters, account data |
| **Read-Only Boundary** | No mutation calls; advisory display only |
| **Authentication** | JWT required; 401 handling inherited from P02 |
| **Refusal Behavior** | Context-based refusals must use existing taxonomy |

### 4.2 Architecture (from P02 state)

| Component | Location | Description |
|-----------|----------|-------------|
| `assistantClient.ts` | `frontend/src/api/` | P02 API client (unchanged) |
| `useAssistantResponses` | `frontend/src/workstation/ai/` | P02 hook (reused) |
| `useAssistantAudit` | `frontend/src/workstation/ai/` | P02 hook (reused) |
| `AssistantCommandSurface.tsx` | `frontend/src/workstation/ai/` | P02 component (extended) |
| `AssistantAuditSubSection.tsx` | `frontend/src/workstation/governance/` | P02 component (unchanged) |

### 4.3 Component Design

| Component | Action | Description |
|-----------|--------|-------------|
| `ContextualAssistantPanel.tsx` | NEW | Embedded assistant in Context Panel |
| `WorkspaceContext.tsx` | NEW | React Context for workspace state |
| `useWorkspaceContext` | NEW | Hook for accessing context |
| `AssistantCommandSurface.tsx` | EXTEND | Add contextual prompt suggestions |

---

## 5. SECURITY REQUIREMENTS

### 5.1 Constitutional Invariants (Non-Negotiable)

| # | Prohibition | Enforcement |
|---|-------------|--------------|
| 1 | No order, buy, sell, execute, or trade controls | Grep test required |
| 2 | No external LLM API calls | Grep test required |
| 3 | No unauthenticated data access | Inherited from P02 |
| 4 | No cross-operator data leakage | JWT isolation |
| 5 | No autonomous chart manipulation | Read-only context only |
| 6 | No hardcoded secrets | Code review |

### 5.2 Required Security Tests

| # | Test | Pass Criterion |
|---|------|---------------|
| S-1 | Grep proof: actuation controls | Zero matches |
| S-2 | Grep proof: external LLM | Zero matches |
| S-3 | Context isolation | No cross-workspace data leakage |

---

## 6. UI/UX REQUIREMENTS

### 6.1 Visual Requirements

| # | Requirement | Specification |
|---|-------------|---------------|
| U-1 | Collapsible panel | Non-intrusive in Context Panel |
| U-2 | Context chips | Display active symbol/timeframe |
| U-3 | Prompt suggestions | Non-intrusive chips |
| U-4 | Dark-first theme | Consistent with AXIOM design |
| U-5 | Keyboard navigation | Tab, Enter, Esc |

### 6.2 Accessibility Requirements

| # | Requirement | Standard |
|---|-------------|----------|
| A-1 | ARIA labels | Required |
| A-2 | Focus management | Logical tab order |
| A-3 | Screen reader | Semantic HTML |
| A-4 | Contrast | >4.5:1 |

---

## 7. TESTING REQUIREMENTS

### 7.1 New Tests

| # | Test | Coverage |
|---|------|----------|
| T-1 | ContextualAssistantPanel rendering | Component |
| T-2 | Workspace context provider | Hook |
| T-3 | Context switching | Integration |
| T-4 | Prompt suggestion generation | Unit |
| T-5 | State transitions | Component |
| T-6 | Symbol context | Integration |
| T-7 | Timeframe context | Integration |

### 7.2 Regression Tests

| # | Requirement | Pass Criterion |
|---|-------------|----------------|
| R-1 | Frontend test suite | All 319 tests pass |
| R-2 | Backend test suite | All 414 tests pass |
| R-3 | TypeScript build | `tsc -b && vite build` exit 0 |

---

## 8. EVIDENCE REQUIREMENTS

### 8.1 Required Evidence

| # | Evidence | Type | Requirement |
|---|----------|------|-------------|
| E-1 | Vitest test log | Level II | All tests pass |
| E-2 | Backend test log | Level II | All 414 tests pass |
| E-3 | TypeScript build output | Level II | Exit 0 |
| E-4 | Grep proof — actuation | Level II | Zero matches |
| E-5 | Grep proof — external LLM | Level II | Zero matches |
| E-6 | Context switching evidence | Level I/II | Verified |
| E-7 | Workspace integration evidence | Level I/II | Verified |
| E-8 | Delivery Report | Level III | Per §10 |

### 8.2 Evidence Hierarchy

- **Level I:** Direct runtime evidence (preferred)
- **Level II:** Automated test evidence (required)
- **Level III:** Documentary evidence (required)

---

## 9. DELIVERY REPORT REQUIREMENTS

The DA shall produce `DELIVERY_REPORT_UI-008-P03.md` containing all 20 sections per §13 of the Amendment:

| # | Section | Content |
|---|---------|---------|
| 1 | Phase identity | UI-008-P03 |
| 2 | Governing Build Order | BUILD_ORDER_UI-008-P03 |
| 3 | Design Plan reference | docs/plans/UI-008_ENGINEERING_DESIGN_PLAN.md §14 |
| 4 | Previous baseline | P02: 71 suites / 319 tests / 414 backend |
| 5 | Implementation summary | What was implemented |
| 6 | Files created | List with nature |
| 7 | Files modified | List with nature |
| 8 | Files removed | List (if any) |
| 9 | Scope compliance | In-scope / out-of-scope matrix |
| 10 | Deviations | Per §5 of Amendment |
| 11 | Test inventory | Per §9 of Amendment |
| 12 | Regression results | Per §10 of Amendment |
| 13 | Security evidence | Grep proofs, auth handling |
| 14 | UI/UX evidence | States verified |
| 15 | Documentation changes | State synchronization |
| 16 | Technical debt changes | New TD (if any) |
| 17 | Known limitations | Documented |
| 18 | Evidence index | Complete list |
| 19 | Next phase recommendation | P04 |
| 20 | DA sign-off | Declaration |

### 9.1 Mandatory Deviation Register (§5)

```
## Deviations From Approved Build Order

[NO DEVIATIONS] — or — deviation table
```

### 9.2 Test Accounting (§8)

```
Previous Baseline:
- Frontend: 71 suites / 319 tests
- Backend: 414 tests

New tests physically added:
- [count] new tests

Tests removed:
- [count] removed

Tests modified:
- [count] modified

Current total:
- Frontend: [X] suites / [Y] tests
- Backend: 414 tests

Category counts are descriptive and may overlap; baseline delta counts are authoritative.
```

### 9.3 Carry-Forward Declaration (§19)

```
Previous Approved Baseline:
- Commit: [P02 baseline reference]
- ITRGA: D-47

Inherited Components:
- assistantClient.ts (P02)
- useAssistantResponses (P02)
- useAssistantAudit (P02)
- AssistantCommandSurface.tsx (P02)
- AssistantAuditSubSection.tsx (P02)

Inherited Tests:
- 319 frontend tests (P02 baseline)
- 414 backend tests

Inherited Technical Debt:
- TD-UI-POSTCSS-HIGH
- OBS-P06-2

Inherited Observations:
- [list any]

New Phase Scope:
- [P03 deliverables]
```

---

## 10. PROJECT-STATE SYNCHRONIZATION

Upon ITRGA approval of P03, DA shall update:

| Document | Update Required |
|----------|----------------|
| PROJECT_STATE.md | Record P03 approval |
| CHANGELOG.md | Record P03 completion |

If no change required, state explicitly:

```
PROJECT_STATE.md — NO CHANGE REQUIRED
Reason: [reason]
```

---

## 11. BUILD ORDER SEQUENCE

```
[ BUILD_ORDER_UI-008-P03 Issued ]  ← THIS DOCUMENT
         ↓
[ DA Implementation & Testing ]
         ↓
[ DA Delivery Report ]
         ↓
[ ITRGA Independent Review ]
         ↓
[ Correction (if required) ]
         ↓
[ ITRGA P03 Determination ]
         ↓
[ Next Authorized Build Order ]
```

---

## 12. ACCEPTANCE CRITERIA

| # | Criterion | Type | Evidence |
|---|-----------|------|----------|
| AC-1 | ContextualAssistantPanel renders in Context Panel | Mandatory | Runtime or test |
| AC-2 | Workspace context provider supplies active state | Mandatory | Test |
| AC-3 | Context switches when workspace changes | Mandatory | Integration test |
| AC-4 | Prompt suggestions based on context | Mandatory | Unit test |
| AC-5 | All loading/error/empty states functional | Mandatory | Component tests |
| AC-6 | All 319 frontend tests pass | Mandatory | Vitest log |
| AC-7 | All 414 backend tests pass | Mandatory | Pytest log |
| AC-8 | TypeScript build exits 0 | Mandatory | Build output |
| AC-9 | No actuation controls | Mandatory | Grep proof |
| AC-10 | No external LLM references | Mandatory | Grep proof |
| AC-11 | Delivery Report submitted | Mandatory | Document |

---

## 13. ISSUANCE

This Build Order is issued by the ITRGA and is effective upon receipt.

**The DA is authorized to begin implementation.**

---

## 14. REFERENCES

| Reference | Document |
|-----------|----------|
| Design Plan | `docs/plans/UI-008_ENGINEERING_DESIGN_PLAN.md` §14 |
| P03 Design | §14 of Design Plan |
| P02 Baseline | D-47: 71 suites / 319 tests · 414 backend · exit 0 |
| Amendment | UI-008 GOVERNANCE CONTROL AMENDMENT |
| System Architecture | `docs/governance/05_SYSTEM_ARCHITECTURE.md` |
| Security Standard | `17_INSTITUTIONAL_SECURITY_STANDARD.md` |

---

## 15. AMENDMENT COMPLIANCE

This Build Order incorporates all 27 rules of the UI-008 GOVERNANCE CONTROL AMENDMENT:

| Rule | Compliance |
|------|------------|
| §2 Historical Baseline | P02 D-47 preserved |
| §3 Single Active Phase | P03 = ACTIVE, P04+ = NOT AUTHORIZED |
| §4 Build Order Contract | Scope enforced |
| §5 Deviation Register | Required in Delivery Report |
| §6 Design-Plan Traceability | Required |
| §7 API/Architecture Changes | Documented if any |
| §8 Test Accounting | Mandatory |
| §9 Test Inventory | Per-suite listing |
| §10 Regression Baseline | P02 baseline comparison |
| §11 Evidence Hierarchy | Classified |
| §12 ITRGA Independence | Maintained |
| §13 Delivery Report Completeness | 20 sections required |
| §14 Project-State Sync | Required |
| §15 Authority Separation | Maintained |
| §16 No Silent Changes | Enforced |
| §17 Production Firewall | Maintained |
| §18 Phase Boundary | Enforced |
| §19 Carry-Forward | Required |
| §20 Correction Rule | Enforced |
| §21 No Premature Next-Phase | Enforced |
| §22 Chat Continuity | Applied |
| §23 Continuity Confirmation | Confirmed |
| §24 P03 Controls | Applied |
| §25 Delivery Declaration | Required |
| §26 ITRGA Declaration | Included |
| §27 Governing Principle | Applied |

---

**End of BUILD_ORDER_UI-008-P03**

---

*This Build Order is an ITRGA governance artifact. Implementation is authorized per this document and the UI-008 GOVERNANCE CONTROL AMENDMENT. Questions should be directed through the Operator.*

**We don't guess. We prove.**

*— AXIOM Independent Technical Review & Governance Authority (ITRGA)*
