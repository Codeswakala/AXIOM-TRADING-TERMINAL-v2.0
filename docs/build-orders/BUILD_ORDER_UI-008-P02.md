# AXIOM — ITRGA FORMAL BUILD ORDER

## `BUILD_ORDER_UI-008-P02`

**Authority:** Independent Technical Review & Governance Authority (ITRGA)
**Determination:** D-46 — RE-BASELINE APPROVED WITH OBSERVATIONS
**Phase:** UI-008-P02 — API Seam & Data Integration
**Governing Design Plan:** `docs/plans/UI-008_ENGINEERING_DESIGN_PLAN.md` (Approved per D-46)
**Clean Baseline:** Commit `30169a4` / Tag `UI-008-P01-M1_INTEGRATED`
**Governance Gate:** CLOSED
**Production Status:** NOT CERTIFIED

---

## 1. BUILD ORDER HEADER

| Field | Value |
|-------|-------|
| Build Order ID | `BUILD_ORDER_UI-008-P02` |
| Issued By | ITRGA |
| Issuance Date | 2026-08-10 |
| Status | **AUTHORIZED — DA MAY BEGIN IMPLEMENTATION** |
| Re-baseline Reference | D-46 |
| Preceding Milestone | UI-008-P01-M1_INTEGRATED (D-45) |
| Next Milestone | UI-008-P02 Delivery Report |
| Implementation Hold | **LIFTED BY THIS BUILD ORDER** |

---

## 2. PHASE OBJECTIVE

Wire assistant presentation surfaces to existing **read-only** backend collaboration and persistence endpoints.

---

## 3. EXACT SCOPE

### 3.1 In Scope

The DA is authorized to implement:

| # | Deliverable | Description |
|---|-------------|-------------|
| 1 | **Typed API Client Service** | `frontend/src/api/assistantClient.ts` — HTTP client for `GET /api/v1/collaboration/assistant-responses` and `GET /api/v1/persistence/audit-events` |
| 2 | **React Hooks** | `useAssistantResponses` and `useAssistantAudit` hooks with loading, error, and empty states |
| 3 | **AssistantCommandSurface Update** | Connect skeleton surface to live API data |
| 4 | **AssistantAuditSubSection Update** | Fetch and render live refusal audit events |
| 5 | **401 Authentication Handling** | Guard against unauthenticated sessions with redirect/guard pattern |
| 6 | **Skeleton Loading States** | Display during data fetch |
| 7 | **Error States** | Display when API calls fail |
| 8 | **Empty States** | Display when no data exists |
| 9 | **API Mocking Tests** | Mock API responses for unit test coverage |
| 10 | **401 Unauthenticated Tests** | Verify unauth handling |
| 11 | **Empty Dataset Tests** | Verify empty state rendering |
| 12 | **Regression Suite** | All existing tests continue passing |

### 3.2 Out of Scope

The following are **explicitly excluded** from this Build Order:

| # | Excluded Item | Reason |
|---|--------------|--------|
| 1 | New backend endpoints | Not authorized; use existing endpoints only |
| 2 | Database migrations | Not required for read-only API |
| 3 | WebSocket streams | Not in P02 design |
| 4 | Write/mutation API calls | Read-only seam only |
| 5 | External LLM integration | Constitutionally prohibited |
| 6 | Order/trade/execution controls | Absolutely prohibited |
| 7 | AssistantReviewSubPanel enhancement | P03 scope |
| 8 | ContextualAssistantPanel creation | P03 scope |
| 9 | DocumentationLookupSurface | P05 scope |
| 10 | New component creation beyond P02 scope | Phase-bounded |

---

## 4. TECHNICAL REQUIREMENTS

### 4.1 API Endpoints

| Endpoint | Method | Auth | Expected Response |
|----------|--------|------|-------------------|
| `/api/v1/collaboration/assistant-responses` | GET | Bearer JWT | `List[AssistantResearchResponseRead]` |
| `/api/v1/persistence/audit-events` | GET | Bearer JWT | `List[AuditEventRead]` |

**Verification requirement:** DA must verify these endpoints exist and are read-only before implementation.

### 4.2 Data Handling

- All API responses are **read-only**
- No mutation (POST, PUT, PATCH, DELETE) calls authorized
- JWT Bearer token required for all requests
- 401 responses must be handled gracefully (redirect to login or display error)

### 4.3 Component Updates

| Component | Action | New Behavior |
|-----------|--------|--------------|
| `AssistantCommandSurface.tsx` | EXTEND | Display live assistant responses from API |
| `AssistantAuditSubSection.tsx` | EXTEND | Display live refusal audit events from API |
| `AssistantReviewSubPanel.tsx` | RETAIN (unchanged) | Deferred to P03 |

### 4.4 State Management

| State | Required |
|-------|----------|
| Loading state | Skeleton placeholder UI |
| Error state | Error banner with message |
| Empty state | "No data" message |
| Auth required state | 401 handling |

---

## 5. SECURITY REQUIREMENTS

### 5.1 Constitutional Invariants (Non-Negotiable)

The following are **absolute prohibitions** — any violation is a blocker:

| # | Prohibition | Enforcement |
|---|-------------|--------------|
| 1 | No order, buy, sell, execute, or trade controls | Grep test required |
| 2 | No external LLM API calls (OpenAI, Anthropic, etc.) | Grep test required |
| 3 | No unauthenticated data access | 401 handling required |
| 4 | No cross-operator data leakage | JWT isolation required |
| 5 | No hardcoded secrets or credentials | Code review required |

### 5.2 Required Security Tests

| # | Test | Pass Criterion |
|---|------|---------------|
| S-1 | Grep proof: no `order`, `buy`, `sell`, `execute`, `trade` in assistant surfaces | Zero matches |
| S-2 | Grep proof: no `openai`, `anthropic`, `langchain`, `external_llm` in source | Zero matches |
| S-3 | 401 unauthenticated session handling | Graceful rejection |
| S-4 | JWT token present on API requests | Bearer token included |

---

## 6. UI/UX REQUIREMENTS

### 6.1 Visual Requirements

| # | Requirement | Specification |
|---|-------------|---------------|
| U-1 | Skeleton loading | Display during API fetch |
| U-2 | Error display | Banner with error message and recovery guidance |
| U-3 | Empty state | Display "No assistant responses available" or equivalent |
| U-4 | Response display | List/table of assistant responses with timestamp, summary |
| U-5 | Audit display | List/table of refusal events with reason code, timestamp |
| U-6 | Dark-first theme | Consistent with AXIOM design system |
| U-7 | Keyboard navigation | Tab focus, Enter/Esc interactions |

### 6.2 Accessibility Requirements

| # | Requirement | Standard |
|---|-------------|----------|
| A-1 | ARIA labels | Required on interactive elements |
| A-2 | Focus management | Tab navigation must be logical |
| A-3 | Screen reader support | Semantic HTML required |
| A-4 | Color contrast | >4.5:1 ratio |

---

## 7. TESTING REQUIREMENTS

### 7.1 Unit Tests

| # | Test | Coverage |
|---|------|----------|
| T-1 | Component rendering with mock API response | AssistantCommandSurface |
| T-2 | Component rendering with mock API response | AssistantAuditSubSection |
| T-3 | Loading state rendering | Both components |
| T-4 | Error state rendering | Both components |
| T-5 | Empty state rendering | Both components |
| T-6 | 401 handling | Both components |
| T-7 | Hook logic | useAssistantResponses |
| T-8 | Hook logic | useAssistantAudit |

### 7.2 Regression Tests

| # | Requirement | Pass Criterion |
|---|-------------|----------------|
| R-1 | Frontend test suite | All 295 tests pass |
| R-2 | Backend test suite | All 414 tests pass |
| R-3 | TypeScript build | `tsc -b && vite build` exit 0 |

### 7.3 Negative Tests

| # | Test | Pass Criterion |
|---|------|---------------|
| N-1 | API returns malformed data | Error state displayed |
| N-2 | API returns empty array | Empty state displayed |
| N-3 | Network timeout | Error state displayed |
| N-4 | Unauthorized access | 401 handled gracefully |

---

## 8. EVIDENCE REQUIREMENTS

### 8.1 Required Evidence for ITRGA Review

| # | Evidence | Type | Requirement |
|---|----------|------|-------------|
| E-1 | Vitest test log | Level II | All tests pass |
| E-2 | Backend test log | Level II | All 414 tests pass |
| E-3 | TypeScript build output | Level II | Exit 0 |
| E-4 | Grep proof — actuation controls | Level II | Zero matches |
| E-5 | Grep proof — external LLM | Level II | Zero matches |
| E-6 | API endpoint verification | Level I | Backend route exists and is read-only |
| E-7 | 401 handling verification | Level I or II | Graceful rejection demonstrated |
| E-8 | Component screenshot (runtime) | Level I | Optional but recommended |
| E-9 | Delivery Report | Level III | Per §9 of this Build Order |

### 8.2 Evidence Hierarchy

- **Level I (Direct Runtime):** Browser DOM snapshots, HTTP transcripts, raw database read-backs — preferred
- **Level II (Automated Tests):** Vitest logs, Pytest logs, grep output — required
- **Level III (Documentary):** Delivery Report — required

---

## 9. DELIVERY REPORT REQUIREMENTS

The DA shall produce `DELIVERY_REPORT_UI-008-P02.md` containing:

| # | Section | Content |
|---|---------|---------|
| 1 | Executive Summary | What was implemented, scope achieved |
| 2 | Implementation Details | Files created/modified, key decisions |
| 3 | Test Summary | Unit tests, regression results |
| 4 | Security Summary | Grep proofs, auth handling |
| 5 | UI/UX Summary | States verified (loading, error, empty, auth) |
| 6 | Evidence Index | List of evidence artifacts |
| 7 | Scope Compliance | In-scope items delivered, out-of-scope items excluded |
| 8 | Open Items | Any issues, limitations, deferred items |
| 9 | Next Phase Recommendation | P03, with justification |

---

## 10. GOVERNANCE REQUIREMENTS

### 10.1 Implementation Hold

Implementation **began** upon issuance of this Build Order.

### 10.2 Project State Update

Upon ITRGA approval of P02, DA shall update:
- `PROJECT_STATE.md` — record P02 approval
- `CHANGELOG.md` — record P02 completion

### 10.3 Technical Debt

No new technical debt items should be introduced without documentation. Any discovered issues should be recorded in the Technical Debt Register.

---

## 11. BUILD ORDER SEQUENCE

```
[ BUILD_ORDER_UI-008-P02 Issued ]  ← THIS DOCUMENT
         ↓
[ DA Implementation & Testing ]
         ↓
[ DA Delivery Report ]
         ↓
[ ITRGA Independent Review ]
         ↓
[ Correction (if required) ]
         ↓
[ ITRGA P02 Determination ]
         ↓
[ Next Authorized Build Order ]
```

---

## 12. ACCEPTANCE CRITERIA SUMMARY

| # | Criterion | Type | Evidence |
|---|-----------|------|----------|
| AC-1 | AssistantCommandSurface renders live responses | Mandatory | Runtime or mock test |
| AC-2 | AssistantAuditSubSection renders live audit events | Mandatory | Runtime or mock test |
| AC-3 | 401 handling works correctly | Mandatory | Test evidence |
| AC-4 | Loading, error, empty states functional | Mandatory | Test evidence |
| AC-5 | All 295 frontend tests pass | Mandatory | Vitest log |
| AC-6 | All 414 backend tests pass | Mandatory | Pytest log |
| AC-7 | TypeScript build exits 0 | Mandatory | Build output |
| AC-8 | No actuation controls | Mandatory | Grep proof |
| AC-9 | No external LLM references | Mandatory | Grep proof |
| AC-10 | Delivery Report submitted | Mandatory | Document |

---

## 13. ISSUANCE

This Build Order is issued by the ITRGA and is effective upon receipt.

**The DA is authorized to begin implementation.**

---

## 14. REFERENCES

| Reference | Document |
|-----------|----------|
| Design Plan | `docs/plans/UI-008_ENGINEERING_DESIGN_PLAN.md` |
| Re-baseline Determination | D-46 |
| Clean Baseline | Commit `30169a4` / `UI-008-P01-M1_INTEGRATED` |
| P01 Design | §12 of Design Plan |
| P02 Design | §13 of Design Plan |
| System Architecture | `docs/governance/05_SYSTEM_ARCHITECTURE.md` |
| Security Standard | `17_INSTITUTIONAL_SECURITY_STANDARD.md` |
| Production Certification | `docs/governance/11_PRODUCTION_READINESS_CERTIFICATION.md` |

---

**End of BUILD_ORDER_UI-008-P02**

---

*This Build Order is an ITRGA governance artifact. Implementation is authorized per this document. Questions should be directed through the Operator.*

**We don't guess. We prove.**

*— AXIOM Independent Technical Review & Governance Authority (ITRGA)*
