# AXIOM — ITRGA FORMAL BUILD ORDER

## `BUILD_ORDER_UI-008-P04`

**Authority:** Independent Technical Review & Governance Authority (ITRGA)
**Phase:** UI-008-P04 — Artifact Lineage & Report Summarization
**Governing Design Plan:** `docs/plans/UI-008_ENGINEERING_DESIGN_PLAN.md` (Approved per D-46)
**Preceding Determination:** D-48 — UI-008-P03 APPROVED
**Amendment:** UI-008 GOVERNANCE CONTROL AMENDMENT (effective P03+)
**Governance Gate:** CLOSED
**Production Status:** NOT CERTIFIED

---

## 1. BUILD ORDER HEADER

| Field | Value |
|-------|-------|
| Build Order ID | `BUILD_ORDER_UI-008-P04` |
| Issued By | ITRGA |
| Issuance Date | 2026-08-10 |
| Status | **AUTHORIZED — DA MAY BEGIN IMPLEMENTATION** |
| Preceding Milestone | UI-008-P03 (D-48) |
| P03 Baseline | 75 suites / 340 tests · 414 backend · exit 0 |
| Next Milestone | UI-008-P04 Delivery Report |
| Amendment Controls | All 27 rules of UI-008 GOVERNANCE CONTROL AMENDMENT apply |

---

## 2. PHASE OBJECTIVE

Provide explainable, deterministic summarization of institutional research reports and artifact lineage, including Regime Reports, Correlation Matrices, and Scenario Simulations with verbatim uncertainty metrics and visual lineage trees.

---

## 3. EXACT SCOPE

### 3.1 In Scope

The DA is authorized to implement:

| # | Deliverable | Description |
|---|-------------|-------------|
| 1 | **ResearchReportSummarizer Component** | Deterministic summarization view for research reports |
| 2 | **ArtifactLineageTree Component** | Visual lineage tree connecting inputs to outputs |
| 3 | **RegimeReport Summarization** | Regime classification explanations |
| 4 | **CorrelationReport Summarization** | Correlation matrix explanations |
| 5 | **ScenarioSimulation Summarization** | Scenario simulation explanations |
| 6 | **Uncertainty Metrics Display** | Verbatim calibration and confidence badges |
| 7 | **Read-Only Architecture** | Consumes existing artifact metadata only |
| 8 | **Unit Tests** | Component and summarization tests |
| 9 | **Lineage Integrity Tests** | Verification of lineage chain |
| 10 | **Regression Suite** | All existing tests continue passing |

### 3.2 Out of Scope

The following are **explicitly excluded** from this Build Order:

| # | Excluded Item | Reason |
|---|--------------|--------|
| 1 | Dynamic report generation | Not authorized — read-only only |
| 2 | Modification of historical records | Absolutely prohibited |
| 3 | Order execution controls | Absolutely prohibited |
| 4 | External LLM integration | Constitutionally prohibited |
| 5 | WebSocket real-time streams | Not in P04 design |
| 6 | New backend endpoints | Use existing endpoints only |
| 7 | Database migrations | Not required |
| 8 | DocumentationLookupSurface | P05 scope |
| 9 | ContextualAssistantPanel enhancement | Already delivered in P03 |
| 10 | Write/mutation API calls | Read-only only |

---

## 4. TECHNICAL REQUIREMENTS

### 4.1 Summarization Boundaries

| Boundary | Requirement |
|----------|-------------|
| **Input Sources** | Existing research reports, artifact metadata, lineage data |
| **Summarization Type** | Deterministic, rule-based display — no generative AI |
| **Output** | Read-only display of existing data |
| **Actuation** | None — display only |
| **Modifications** | None to underlying data |

### 4.2 Architecture Integration

| Component | Source | Reused |
|-----------|--------|--------|
| `assistantClient.ts` | P02 | ✅ Reused |
| `useAssistantResponses` | P02 | ✅ Reused |
| `useAssistantAudit` | P02 | ✅ Reused |
| `WorkspaceContext.tsx` | P03 | ✅ Reused |
| `ContextualAssistantPanel.tsx` | P03 | ✅ Extended |
| `AssistantCommandSurface.tsx` | P02 | ✅ Extended |
| `AssistantAuditSubSection.tsx` | P02 | ✅ Unchanged |

### 4.3 Component Design

| Component | Action | Description |
|-----------|--------|-------------|
| `ResearchReportSummarizer.tsx` | NEW | Deterministic research report summarization |
| `ArtifactLineageTree.tsx` | NEW | Visual lineage tree component |
| `UncertaintyBadge.tsx` | NEW | Calibration/confidence display component |
| `AssistantCommandSurface.tsx` | EXTEND | Add summarization context access |

---

## 5. SECURITY REQUIREMENTS

### 5.1 Constitutional Invariants (Non-Negotiable)

| # | Prohibition | Enforcement |
|---|-------------|--------------|
| 1 | No order, buy, sell, execute, or trade controls | Grep test required |
| 2 | No external LLM API calls | Grep test required |
| 3 | No unauthenticated data access | JWT inherited from P02 |
| 4 | No cross-operator data leakage | JWT isolation |
| 5 | No modification of historical records | Read-only architecture |
| 6 | No hardcoded secrets | Code review |

### 5.2 Required Security Tests

| # | Test | Pass Criterion |
|---|------|---------------|
| S-1 | Grep proof: actuation controls | Zero matches |
| S-2 | Grep proof: external LLM | Zero matches |
| S-3 | Read-only boundary verification | No mutation calls |

---

## 6. UI/UX REQUIREMENTS

### 6.1 Visual Requirements

| # | Requirement | Specification |
|---|-------------|---------------|
| U-1 | Confidence level badges | High/Moderate/Limited indicators |
| U-2 | Lineage tree visualization | Visual tree connecting inputs to outputs |
| U-3 | Expandable sections | Drill-down for detailed explanations |
| U-4 | Uncertainty intervals | Verbatim uncertainty display |
| U-5 | Dark-first theme | Consistent with AXIOM design |

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
| T-1 | ResearchReportSummarizer rendering | Component |
| T-2 | ArtifactLineageTree visualization | Component |
| T-3 | UncertaintyBadge display | Component |
| T-4 | RegimeReport summarization | Integration |
| T-5 | CorrelationReport summarization | Integration |
| T-6 | ScenarioSimulation summarization | Integration |
| T-7 | Lineage integrity | Unit |

### 7.2 Regression Tests

| # | Requirement | Pass Criterion |
|---|-------------|----------------|
| R-1 | Frontend test suite | All 340 tests pass |
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
| E-6 | Summarization evidence | Level I/II | Verified |
| E-7 | Lineage tree evidence | Level I/II | Verified |
| E-8 | Delivery Report | Level III | Per §10 |

### 8.2 Evidence Hierarchy

- **Level I:** Direct runtime evidence (preferred)
- **Level II:** Automated test evidence (required)
- **Level III:** Documentary evidence (required)

---

## 9. DELIVERY REPORT REQUIREMENTS

The DA shall produce `DELIVERY_REPORT_UI-008-P04.md` containing all 20 sections per §13 of the Amendment:

| # | Section | Content |
|---|---------|---------|
| 1 | Phase identity | UI-008-P04 |
| 2 | Governing Build Order | BUILD_ORDER_UI-008-P04 |
| 3 | Design Plan reference | docs/plans/UI-008_ENGINEERING_DESIGN_PLAN.md §15 |
| 4 | Previous baseline | P03: 75 suites / 340 tests / 414 backend |
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
| 19 | Next phase recommendation | P05 |
| 20 | DA sign-off | Declaration |

### 9.1 Mandatory Deviation Register (§5)

```
## Deviations From Approved Build Order

[NO DEVIATIONS] — or — deviation table
```

### 9.2 Test Accounting (§8)

```
Previous Baseline:
- Frontend: 75 suites / 340 tests
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
- Commit: [P03 baseline reference]
- ITRGA: D-48

Inherited Components:
- assistantClient.ts (P02)
- useAssistantResponses (P02)
- useAssistantAudit (P02)
- WorkspaceContext.tsx (P03)
- ContextualAssistantPanel.tsx (P03)
- AssistantCommandSurface.tsx (P02/P03)
- AssistantAuditSubSection.tsx (P02)

Inherited Tests:
- 340 frontend tests (P03 baseline)
- 414 backend tests

Inherited Technical Debt:
- TD-UI-POSTCSS-HIGH
- OBS-P06-2

Inherited Observations:
- [list any]

New Phase Scope:
- [P04 deliverables]
```

---

## 10. PROJECT-STATE SYNCHRONIZATION

Upon ITRGA approval of P04, DA shall update:

| Document | Update Required |
|----------|----------------|
| PROJECT_STATE.md | Record P04 approval |
| CHANGELOG.md | Record P04 completion |

If no change required, state explicitly:

```
PROJECT_STATE.md — NO CHANGE REQUIRED
Reason: [reason]
```

---

## 11. BUILD ORDER SEQUENCE

```
[ BUILD_ORDER_UI-008-P04 Issued ]  ← THIS DOCUMENT
         ↓
[ DA Implementation & Testing ]
         ↓
[ DA Delivery Report ]
         ↓
[ ITRGA Independent Review ]
         ↓
[ Correction (if required) ]
         ↓
[ ITRGA P04 Determination ]
         ↓
[ Next Authorized Build Order ]
```

---

## 12. ACCEPTANCE CRITERIA

| # | Criterion | Type | Evidence |
|---|-----------|------|----------|
| AC-1 | ResearchReportSummarizer renders | Mandatory | Runtime or test |
| AC-2 | ArtifactLineageTree displays | Mandatory | Runtime or test |
| AC-3 | Uncertainty badges display | Mandatory | Component test |
| AC-4 | RegimeReport summarization works | Mandatory | Integration test |
| AC-5 | CorrelationReport summarization works | Mandatory | Integration test |
| AC-6 | ScenarioSimulation summarization works | Mandatory | Integration test |
| AC-7 | All 340 frontend tests pass | Mandatory | Vitest log |
| AC-8 | All 414 backend tests pass | Mandatory | Pytest log |
| AC-9 | TypeScript build exits 0 | Mandatory | Build output |
| AC-10 | No actuation controls | Mandatory | Grep proof |
| AC-11 | No external LLM references | Mandatory | Grep proof |
| AC-12 | Read-only boundary maintained | Mandatory | Architecture verification |
| AC-13 | Delivery Report submitted | Mandatory | Document |

---

## 13. ISSUANCE

This Build Order is issued by the ITRGA and is effective upon receipt.

**The DA is authorized to begin implementation.**

---

## 14. REFERENCES

| Reference | Document |
|-----------|----------|
| Design Plan | `docs/plans/UI-008_ENGINEERING_DESIGN_PLAN.md` §15 |
| P04 Design | §15 of Design Plan |
| P03 Baseline | D-48: 75 suites / 340 tests · 414 backend · exit 0 |
| Amendment | UI-008 GOVERNANCE CONTROL AMENDMENT |
| System Architecture | `docs/governance/05_SYSTEM_ARCHITECTURE.md` |
| Security Standard | `17_INSTITUTIONAL_SECURITY_STANDARD.md` |

---

## 15. AMENDMENT COMPLIANCE

This Build Order incorporates all 27 rules of the UI-008 GOVERNANCE CONTROL AMENDMENT:

| Rule | Compliance |
|------|------------|
| §2 Historical Baseline | P03 D-48 preserved |
| §3 Single Active Phase | P04 = ACTIVE, P05+ = NOT AUTHORIZED |
| §4 Build Order Contract | Scope enforced |
| §5 Deviation Register | Required in Delivery Report |
| §6 Design-Plan Traceability | Required |
| §7 API/Architecture Changes | Documented if any |
| §8 Test Accounting | Mandatory |
| §9 Test Inventory | Per-suite listing |
| §10 Regression Baseline | P03 baseline comparison |
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
| §24 P04 Controls | Applied |
| §25 Delivery Declaration | Required |
| §26 ITRGA Declaration | Included |
| §27 Governing Principle | Applied |

---

**End of BUILD_ORDER_UI-008-P04**

---

*This Build Order is an ITRGA governance artifact. Implementation is authorized per this document and the UI-008 GOVERNANCE CONTROL AMENDMENT. Questions should be directed through the Operator.*

**We don't guess. We prove.**

*— AXIOM Independent Technical Review & Governance Authority (ITRGA)*
