# AXIOM — ITRGA FORMAL BUILD ORDER

## `BUILD_ORDER_UI-008-P05`

**Authority:** Independent Technical Review & Governance Authority (ITRGA)
**Phase:** UI-008-P05 — Documentation Lookup & Operator Guidance
**Governing Design Plan:** `docs/plans/UI-008_ENGINEERING_DESIGN_PLAN.md` (Approved per D-46)
**Preceding Determination:** D-49 — UI-008-P04 APPROVED
**Amendment:** UI-008 GOVERNANCE CONTROL AMENDMENT (effective P03+)
**Governance Gate:** CLOSED
**Production Status:** NOT CERTIFIED

---

## 1. BUILD ORDER HEADER

| Field | Value |
|-------|-------|
| Build Order ID | `BUILD_ORDER_UI-008-P05` |
| Issued By | ITRGA |
| Issuance Date | 2026-08-10 |
| Status | **AUTHORIZED — DA MAY BEGIN IMPLEMENTATION** |
| Preceding Milestone | UI-008-P04 (D-49) |
| P04 Baseline | 79 suites / 357 tests · 414 backend · exit 0 |
| Next Milestone | UI-008-P05 Delivery Report |
| Amendment Controls | All 27 rules of UI-008 GOVERNANCE CONTROL AMENDMENT apply |

---

## 2. PHASE OBJECTIVE

Implement the in-app searchable documentation and knowledge lookup surface (`DocumentationLookupSurface.tsx`) indexing platform architecture, mathematical definitions, indicator formulas, and governance rules.

---

## 3. EXACT SCOPE

### 3.1 In Scope

The DA is authorized to implement:

| # | Deliverable | Description |
|---|-------------|-------------|
| 1 | **DocumentationLookupSurface Component** | Searchable documentation panel |
| 2 | **Static Document Index** | Index of platform documentation |
| 3 | **Fuzzy Search Functionality** | Fast client-side search |
| 4 | **Governance Documents Index** | Governance rules and standards |
| 5 | **Architecture Documents Index** | System architecture documentation |
| 6 | **Mathematical Definitions Index** | Formulas and definitions |
| 7 | **Markdown Rendering** | Safe, sandboxed rendering |
| 8 | **Command Palette Integration** | `qa.open.documentation-lookup` quick action |
| 9 | **Unit Tests** | Component and search tests |
| 10 | **Regression Suite** | All existing tests continue passing |

### 3.2 Out of Scope

The following are **explicitly excluded** from this Build Order:

| # | Excluded Item | Reason |
|---|--------------|--------|
| 1 | External web browsing | Not authorized |
| 2 | Uncontrolled search queries | Not authorized |
| 3 | External LLM lookups | Constitutionally prohibited |
| 4 | Dynamic content generation | Not authorized |
| 5 | New backend endpoints | Use existing static files only |
| 6 | Database migrations | Not required |
| 7 | Script execution in Markdown | Security risk — prohibited |
| 8 | Chart manipulation | P03 delivered |
| 9 | Report summarization | P04 delivered |
| 10 | Write/mutation operations | Read-only only |

---

## 4. TECHNICAL REQUIREMENTS

### 4.1 Documentation Sources

| Category | Source Location | Index Type |
|----------|----------------|------------|
| Governance Documents | `docs/governance/` | Static index |
| Architecture Documents | `docs/` | Static index |
| Mathematical Definitions | Embedded or `docs/` | Static index |
| Indicator Formulas | Embedded or `docs/` | Static index |

### 4.2 Search Requirements

| Requirement | Specification |
|-------------|---------------|
| Search Type | Client-side fuzzy search |
| Index | Static, pre-built |
| Performance | Fast response |
| Security | No external network calls |

### 4.3 Markdown Rendering

| Requirement | Specification |
|-------------|---------------|
| Renderer | Sandboxed |
| Script Execution | **PROHIBITED** |
| Links | Internal navigation only |
| Images | Inline allowed |

### 4.4 Architecture Integration

| Component | Source | Reused |
|-----------|--------|--------|
| `assistantClient.ts` | P02 | ✅ Reused |
| `useAssistantResponses` | P02 | ✅ Reused |
| `WorkspaceContext.tsx` | P03 | ✅ Reused |
| `ContextualAssistantPanel.tsx` | P03 | ✅ Reused |
| `ResearchReportSummarizer.tsx` | P04 | ✅ Reused |
| `AssistantCommandSurface.tsx` | P02/P03 | ✅ Extended |

---

## 5. SECURITY REQUIREMENTS

### 5.1 Constitutional Invariants (Non-Negotiable)

| # | Prohibition | Enforcement |
|---|-------------|--------------|
| 1 | No order, buy, sell, execute, or trade controls | Grep test required |
| 2 | No external LLM API calls | Grep test required |
| 3 | No external web browsing | No network requests |
| 4 | No script execution in Markdown | Sandboxed renderer |
| 5 | No hardcoded secrets | Code review |

### 5.2 Required Security Tests

| # | Test | Pass Criterion |
|---|------|---------------|
| S-1 | Grep proof: actuation controls | Zero matches |
| S-2 | Grep proof: external LLM | Zero matches |
| S-3 | Markdown sandbox verification | No script execution |

---

## 6. UI/UX REQUIREMENTS

### 6.1 Visual Requirements

| # | Requirement | Specification |
|---|-------------|---------------|
| U-1 | Split-pane layout | Search + reading view |
| U-2 | Search input | Fast, responsive |
| U-3 | Results list | Scrollable |
| U-4 | Document viewer | Markdown rendering |
| U-5 | Keyboard shortcut | Esc to close |
| U-6 | Dark-first theme | Consistent with AXIOM |

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
| T-1 | DocumentationLookupSurface rendering | Component |
| T-2 | Search indexing | Unit |
| T-3 | Fuzzy search results | Unit |
| T-4 | Markdown rendering safety | Security |
| T-5 | Keyboard navigation | Accessibility |

### 7.2 Regression Tests

| # | Requirement | Pass Criterion |
|---|-------------|----------------|
| R-1 | Frontend test suite | All 357 tests pass |
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
| E-6 | Search functionality evidence | Level I/II | Verified |
| E-7 | Markdown safety evidence | Level II | Verified |
| E-8 | Delivery Report | Level III | Per §10 |

### 8.2 Evidence Hierarchy

- **Level I:** Direct runtime evidence (preferred)
- **Level II:** Automated test evidence (required)
- **Level III:** Documentary evidence (required)

---

## 9. DELIVERY REPORT REQUIREMENTS

The DA shall produce `DELIVERY_REPORT_UI-008-P05.md` containing all 20 sections per §13 of the Amendment:

| # | Section | Content |
|---|---------|---------|
| 1 | Phase identity | UI-008-P05 |
| 2 | Governing Build Order | BUILD_ORDER_UI-008-P05 |
| 3 | Design Plan reference | docs/plans/UI-008_ENGINEERING_DESIGN_PLAN.md §16 |
| 4 | Previous baseline | P04: 79 suites / 357 tests / 414 backend |
| 5 | Implementation summary | What was implemented |
| 6 | Files created | List with nature |
| 7 | Files modified | List with nature |
| 8 | Files removed | List (if any) |
| 9 | Scope compliance | In-scope / out-of-scope matrix |
| 10 | Deviations | Per §5 of Amendment |
| 11 | Test inventory | Per §9 of Amendment |
| 12 | Regression results | Per §10 of Amendment |
| 13 | Security evidence | Grep proofs, Markdown safety |
| 14 | UI/UX evidence | States verified |
| 15 | Documentation changes | State synchronization |
| 16 | Technical debt changes | New TD (if any) |
| 17 | Known limitations | Documented |
| 18 | Evidence index | Complete list |
| 19 | Next phase recommendation | P06 |
| 20 | DA sign-off | Declaration |

### 9.1 Mandatory Deviation Register (§5)

```
## Deviations From Approved Build Order

[NO DEVIATIONS] — or — deviation table
```

### 9.2 Test Accounting (§8)

```
Previous Baseline:
- Frontend: 79 suites / 357 tests
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
- Commit: [P04 baseline reference]
- ITRGA: D-49

Inherited Components:
- assistantClient.ts (P02)
- useAssistantResponses (P02)
- WorkspaceContext.tsx (P03)
- ContextualAssistantPanel.tsx (P03)
- ResearchReportSummarizer.tsx (P04)
- ArtifactLineageTree.tsx (P04)
- UncertaintyBadge.tsx (P04)
- AssistantCommandSurface.tsx (P02/P03)
- AssistantAuditSubSection.tsx (P02)

Inherited Tests:
- 357 frontend tests (P04 baseline)
- 414 backend tests

Inherited Technical Debt:
- TD-UI-POSTCSS-HIGH
- OBS-P06-2

Inherited Observations:
- [list any]

New Phase Scope:
- [P05 deliverables]
```

---

## 10. PROJECT-STATE SYNCHRONIZATION

Upon ITRGA approval of P05, DA shall update:

| Document | Update Required |
|----------|----------------|
| PROJECT_STATE.md | Record P05 approval |
| CHANGELOG.md | Record P05 completion |

If no change required, state explicitly:

```
PROJECT_STATE.md — NO CHANGE REQUIRED
Reason: [reason]
```

---

## 11. BUILD ORDER SEQUENCE

```
[ BUILD_ORDER_UI-008-P05 Issued ]  ← THIS DOCUMENT
         ↓
[ DA Implementation & Testing ]
         ↓
[ DA Delivery Report ]
         ↓
[ ITRGA Independent Review ]
         ↓
[ Correction (if required) ]
         ↓
[ ITRGA P05 Determination ]
         ↓
[ Next Authorized Build Order ]
```

---

## 12. ACCEPTANCE CRITERIA

| # | Criterion | Type | Evidence |
|---|-----------|------|----------|
| AC-1 | DocumentationLookupSurface renders | Mandatory | Runtime or test |
| AC-2 | Static document index built | Mandatory | Verified |
| AC-3 | Fuzzy search returns results | Mandatory | Test evidence |
| AC-4 | Markdown renders safely | Mandatory | Security test |
| AC-5 | Command palette integration works | Mandatory | Test evidence |
| AC-6 | All 357 frontend tests pass | Mandatory | Vitest log |
| AC-7 | All 414 backend tests pass | Mandatory | Pytest log |
| AC-8 | TypeScript build exits 0 | Mandatory | Build output |
| AC-9 | No actuation controls | Mandatory | Grep proof |
| AC-10 | No external LLM references | Mandatory | Grep proof |
| AC-11 | Markdown sandbox verified | Mandatory | Security test |
| AC-12 | Delivery Report submitted | Mandatory | Document |

---

## 13. ISSUANCE

This Build Order is issued by the ITRGA and is effective upon receipt.

**The DA is authorized to begin implementation.**

---

## 14. REFERENCES

| Reference | Document |
|-----------|----------|
| Design Plan | `docs/plans/UI-008_ENGINEERING_DESIGN_PLAN.md` §16 |
| P05 Design | §16 of Design Plan |
| P04 Baseline | D-49: 79 suites / 357 tests · 414 backend · exit 0 |
| Amendment | UI-008 GOVERNANCE CONTROL AMENDMENT |
| System Architecture | `docs/governance/05_SYSTEM_ARCHITECTURE.md` |
| Security Standard | `17_INSTITUTIONAL_SECURITY_STANDARD.md` |

---

## 15. AMENDMENT COMPLIANCE

This Build Order incorporates all 27 rules of the UI-008 GOVERNANCE CONTROL AMENDMENT:

| Rule | Compliance |
|------|------------|
| §2 Historical Baseline | P04 D-49 preserved |
| §3 Single Active Phase | P05 = ACTIVE, P06 = NOT YET AUTHORIZED |
| §4 Build Order Contract | Scope enforced |
| §5 Deviation Register | Required in Delivery Report |
| §6 Design-Plan Traceability | Required |
| §7 API/Architecture Changes | Documented if any |
| §8 Test Accounting | Mandatory |
| §9 Test Inventory | Per-suite listing |
| §10 Regression Baseline | P04 baseline comparison |
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
| §24 P05 Controls | Applied |
| §25 Delivery Declaration | Required |
| §26 ITRGA Declaration | Included |
| §27 Governing Principle | Applied |

---

**End of BUILD_ORDER_UI-008-P05**

---

*This Build Order is an ITRGA governance artifact. Implementation is authorized per this document and the UI-008 GOVERNANCE CONTROL AMENDMENT. Questions should be directed through the Operator.*

**We don't guess. We prove.**

*— AXIOM Independent Technical Review & Governance Authority (ITRGA)*
