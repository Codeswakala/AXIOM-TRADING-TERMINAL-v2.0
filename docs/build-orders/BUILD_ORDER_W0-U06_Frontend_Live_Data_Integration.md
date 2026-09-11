# AXIOM Build Order
## W0-U06 — Frontend Live Data Integration & Operator Dashboard Foundation

**Build Order ID:** W0-U06  
**Wave:** 0 — Foundation  
**Unit:** 06  
**Version:** 1.0  
**Status:** ISSUED  
**Authority:** Independent Technical Review & Governance Authority (ITRGA)  
**Date Issued:** 2026-07-10  
**Authorized By:** ITRGA (following successful Operator-verified completion of W0-U05)  
**Classification:** Official Build Order  

**Governing Documents (in strict order of precedence):**
1. 00_VISION_AND_PRINCIPLES.md (highest philosophical authority)
2. 03_AXIOM_SPEC_v1.1.md (Project Constitution)
3. 09_ITRGA_REASONING_FRAMEWORK.md
4. ITRGA_ONBOARDING.md (ITRGA Operations Manual)
5. UNIVERSAL_ITRGA_REVIEWER_DIRECTIVE.md
6. AXIOM_SYSTEM_ARCHITECTURE_MERGED.md (v1.1)
7. 02_DESIGN_PHILOSOPHY.md
8. 08_UI_UX_SPEC.md
9. 04_PROJECT_ROADMAP.md

---

## 1. Purpose

This Build Order authorizes the Development Authority to integrate the authenticated live market data capability (delivered and Operator-verified in W0-U05) into the frontend and establish the foundational professional operator dashboard.

This unit is the first point at which live market intelligence becomes **visible and usable** to a human operator. It must be executed to the same institutional standard expected in a quantitative hedge fund or professional trading firm’s research platform.

---

## 2. Objectives

The unit must achieve the following to institutional standard:

1. Implement a secure, authenticated WebSocket client in the React frontend that connects to the live market data channel established in W0-U05 using the JWT session from W0-U04.
2. Create a professional, institutional-grade live market dashboard that displays real-time price updates for multiple symbols using data from the simulated adapter.
3. Provide clear, real-time visual feedback on live feed health (connection status, last update timestamp, message rate/latency indicators).
4. Ensure the entire live experience is gated behind the authenticated session — unauthenticated users must not see live data.
5. Preserve and enhance the single-uvicorn execution model (one command to run full stack after frontend build).
6. Deliver high-quality, maintainable frontend code aligned with 08_UI_UX_SPEC.md and the institutional dark theme.
7. Produce comprehensive tests for live data consumption and UI state.
8. Generate rigorous Architecture Decision Records that explain key frontend live data decisions with alternatives considered and consequences analyzed.
9. Fully document the implementation so another professional engineer can understand and extend it without reverse engineering.
10. The Delivery Report must be written as if it will be scrutinized under the UNIVERSAL_ITRGA_REVIEWER_DIRECTIVE.md and 09_ITRGA_REASONING_FRAMEWORK.md.

---

## 3. Scope

### Strictly In Scope
- Frontend WebSocket client with proper JWT authentication and basic reconnection logic.
- Live price display (table or card-based) for at least two symbols, updating in real time from the simulated feed.
- Prominent feed status indicator (connected / disconnected / last received time / basic rate).
- Integration with existing auth context from W0-U04 so unauthenticated users cannot access live data views.
- Professional layout using existing institutional dark theme and styling.
- Component and integration-style frontend tests.
- ADRs and documentation.
- Maintenance of the single-`uvicorn` developer experience.

### Explicitly Out of Scope
- Any form of charting or candlestick visualization (reserved for W0-U07).
- Order entry, position management, execution UI, or any trading actions.
- Advanced technical indicators or analysis tools (reserved for later units).
- Real external broker data sources (simulated feed remains in use).
- Persistent user preferences or multi-layout workspaces.
- Mobile-first or responsive redesign beyond current institutional workstation patterns.

---

## 4. Deliverables

The Development Authority must deliver the following as a complete, reviewable unit:

1. **Frontend Live Data Layer**
   - Secure WebSocket service/hook that authenticates using the current JWT session.
   - Proper connection lifecycle management (connect, disconnect, reconnect, error handling).
   - Clean TypeScript data models for incoming live messages.

2. **Operator Live Dashboard**
   - Professional dashboard section or page displaying live prices for multiple symbols (minimum two).
   - Real-time updates visible without page refresh.
   - Clear, always-visible feed health/status indicators.

3. **Authentication Integration**
   - Live dashboard and data components are only functional for authenticated operators.
   - Appropriate handling when the user is not logged in or the session expires.

4. **Single-Process Execution Support**
   - The documented single-command development workflow must continue to work with one `uvicorn` after `npm run build` in the frontend.

5. **Testing**
   - Frontend component tests covering live data subscription, real-time update rendering, reconnection, and auth state.
   - At least one test that simulates incoming WebSocket messages.

6. **Engineering Knowledge Management**
   - ADR-011: Frontend Live Data Consumption & WebSocket Integration Strategy
   - ADR-012: State Management and UX Patterns for Real-Time Institutional Dashboards
   - Updated Technical Debt Register with explicit justification for any new debt.

7. **Documentation**
   - Clear reproduction instructions that emphasize the single-uvicorn workflow.
   - Updated `PROJECT_STATE.md`.
   - Sufficient inline and supporting documentation for professional handoff.

8. **Delivery Report**
   - `DELIVERY_REPORT_W0-U06.md` that demonstrates full, rigorous application of the 09_ITRGA_REASONING_FRAMEWORK.md and the UNIVERSAL_ITRGA_REVIEWER_DIRECTIVE.md.

---

## 5. Success Criteria (Definition of Done)

This unit is complete **only** when every item below is satisfied and can be independently verified:

- [ ] Authenticated frontend successfully establishes and maintains a connection to the live WebSocket.
- [ ] Live price updates from the simulated feed visibly update in the UI within seconds.
- [ ] At least two symbols display concurrent live updates.
- [ ] Feed connection status and last update time are clearly visible and accurate.
- [ ] Unauthenticated users cannot access or view live data components.
- [ ] All new frontend tests pass.
- [ ] The full stack (frontend + backend + live simulation) runs via a single `uvicorn` command after frontend build.
- [ ] Two high-quality ADRs exist that would satisfy institutional scrutiny (alternatives considered, consequences analyzed).
- [ ] The Delivery Report applies the full standards of the UNIVERSAL_ITRGA_REVIEWER_DIRECTIVE.md and 09_ITRGA_REASONING_FRAMEWORK.md.
- [ ] No unauthorized scope expansion.
- [ ] The implementation is independently reviewable by another senior engineer.

---

## 6. Constraints & Professional Standards

The Development Authority must operate under these non-negotiable constraints:

- Full adherence to the UNIVERSAL_ITRGA_REVIEWER_DIRECTIVE.md and 09_ITRGA_REASONING_FRAMEWORK.md when preparing the Delivery Report.
- The single-uvicorn developer experience is a first-class requirement.
- All live data access must use the authenticated session from W0-U04.
- UI/UX must meet the professional institutional standards defined in 08_UI_UX_SPEC.md (clarity, information density, professionalism).
- No trading, execution, or order-related functionality may be introduced.
- All technical debt must be explicitly recorded with rationale and planned resolution.
- Reproducibility of the development and runtime environment is mandatory.

---

## 7. References & Dependencies

- W0-U01 through W0-U05 (approved, with Operator verification where applicable)
- Live authenticated WebSocket channel from W0-U05
- Authentication system from W0-U04
- All governing documents listed at the top of this Build Order

---

## 8. Authorization

**This Build Order is issued by the Independent Technical Review & Governance Authority in strict accordance with the full institutional governance framework.**

**Issued By:** ITRGA  
**Date:** 2026-07-10  

**Next Action Required from the Development Authority:**
1. Acknowledge receipt of this Build Order.
2. Execute the unit while applying the highest professional standards defined in the UNIVERSAL_ITRGA_REVIEWER_DIRECTIVE.md and 09_ITRGA_REASONING_FRAMEWORK.md.
3. Produce a Delivery Report in which every claim is treated as a hypothesis requiring evidence.
4. Submit the completed unit together with all required evidence for independent ITRGA review.

---

**End of Build Order W0-U06**

*ITRGA — We don't guess. We prove.*