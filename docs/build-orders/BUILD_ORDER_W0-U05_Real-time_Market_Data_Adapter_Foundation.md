# AXIOM Build Order
## W0-U05 — Real-time Market Data Adapter Foundation

**Build Order ID:** W0-U05  
**Wave:** 0 — Foundation  
**Unit:** 05  
**Version:** 1.0  
**Status:** ISSUED  
**Authority:** Independent Technical Review & Governance Authority (ITRGA)  
**Date Issued:** 2026-07-10  
**Authorized By:** ITRGA (following Operator approval of W0-U04)  
**Classification:** Official Build Order  
**Governing Documents:**  
- 09_ITRGA_REASONING_FRAMEWORK.md  
- ITRGA_Enhanced_Investigation_Standards_v1.1.md  
- 03_AXIOM_SPEC_v1.1.md  
- 04_PROJECT_ROADMAP.md  
- GOVERNANCE_HIERARCHY.md  
- AXIOM_SYSTEM_ARCHITECTURE_MERGED.md (v1.1)  
- 02_DESIGN_PHILOSOPHY.md  
- 07_ML_SPEC.md  
- 00_VISION_AND_PRINCIPLES.md  

---

## 1. Purpose

This Build Order authorizes the Development Authority to implement the foundational **real-time / live market data adapter** for AXIOM.

Building on the historical ingestion (W0-U03) and authenticated operator model (W0-U04), this unit introduces the first capability to receive and process **live market data** (ticks or candles) while keeping the same normalization and persistence pipeline.

This is the critical bridge from historical research to live decision support.

---

## 2. Objectives

1. Define a clean, pluggable market data adapter interface.
2. Implement a basic live data adapter (initially using a simulated or simple WebSocket feed for one market class).
3. Normalize incoming live data to the same `NormalizedCandleRow` / Candle model used for historical data.
4. Persist live data through the existing repository layer with appropriate upsert / latest-value logic.
5. Expose live market status via authenticated API and WebSocket channel.
6. Integrate authentication (from W0-U04) so live data endpoints are protected.
7. Add basic observability for live feed health, lag, and connection status.
8. Create comprehensive tests (unit + integration with simulated feed).
9. Update EKMS with rigorous ADRs.
10. Fully apply the ITRGA Reasoning Framework in the Delivery Report.
11. Maintain the single-uvicorn developer experience.

---

## 3. Scope

### In Scope
- Adapter interface / abstract base (`MarketDataAdapter`).
- One concrete basic live adapter (simulated WebSocket or simple public feed for foundation — e.g., a mock or lightweight Binance/Alpha Vantage style if practical).
- Data normalization layer that re-uses historical ingestion logic where possible.
- Live data handler that routes normalized data into the Candle repository.
- Auth-protected endpoints:
  - `/api/v1/market/live/status`
  - `/api/v1/market/live/subscribe` (or WebSocket equivalent)
- WebSocket channel for live updates (building on existing `/ws/status`).
- Feed health / lag metrics in readiness and new `/market/live/stats`.
- Basic connection lifecycle (connect, disconnect, reconnect logic).
- Tests using a simulated feed (no external paid APIs required for foundation).
- At least two new ADRs.

### Explicitly Out of Scope
- Full multi-broker abstraction or production MT5/FIX connectors.
- High-frequency tick-by-tick storage (focus on candle aggregation or latest price).
- Order book / depth data.
- Any execution or trading logic.
- Advanced drift detection or ML features.
- Rate limiting / circuit breakers (basic only).

---

## 4. Deliverables

1. **Market Data Adapter Layer**
   - `app/market/adapters/` with base class and at least one concrete implementation.
   - Normalization utilities shared with historical ingestion.

2. **Live Data Service**
   - Service that manages adapter lifecycle.
   - Background task or async loop for receiving data.

3. **API & WebSocket**
   - Auth-protected live status and stats endpoints.
   - WebSocket updates for live market data (using existing WebSocket infrastructure).

4. **Persistence Integration**
   - Live data flows through the same `CandleRepository` with appropriate "latest" handling.

5. **Observability**
   - Feed connection status, last update time, lag.
   - Structured MARKET logs for live events.
   - Readiness probe includes live feed status.

6. **Testing**
   - Unit tests for adapter and normalization.
   - Integration tests using a simulated feed that pushes data.
   - Auth-protected live endpoint tests.

7. **Engineering Knowledge**
   - ADR-009: Live Market Data Adapter Architecture
   - ADR-010: Live vs Historical Data Unification Strategy
   - Updated Decision Log and Technical Debt Register.

8. **Documentation**
   - Live data adapter usage guide.
   - Updated `PROJECT_STATE.md`.
   - Reproduction instructions including single-uvicorn run.

9. **Delivery Report**
   - `DELIVERY_REPORT_W0-U05.md` that rigorously applies the full **09_ITRGA_REASONING_FRAMEWORK.md**.

---

## 5. Success Criteria / Definition of Done

- [ ] A simulated or basic live adapter can push normalized data that appears in the database.
- [ ] Live data is queryable via existing candle endpoints.
- [ ] Auth-protected live status and stats endpoints work.
- [ ] WebSocket delivers live updates to authenticated clients.
- [ ] Feed health is visible in `/ready`.
- [ ] All new tests pass.
- [ ] At least two new ADRs created with deep rationale.
- [ ] Delivery Report follows the ITRGA Reasoning Framework.
- [ ] Scope strictly respected.
- [ ] Single-uvicorn execution still works cleanly.
- [ ] Implementation is independently reviewable.

---

## 6. Constraints & Standards

- Must apply **09_ITRGA_REASONING_FRAMEWORK.md** in the Delivery Report.
- Re-use existing repository, normalization, and auth patterns from W0-U02–U04.
- Live data must not break historical data paths.
- All live endpoints must respect authentication from W0-U04.
- Future-compatible with multiple brokers and high-frequency data.

---

## 7. Operator Verification Expectations

Similar to previous units, after ITRGA approval the Operator is expected to:
- Run the new live adapter in the PostgreSQL environment.
- Verify that live/simulated data appears in the database.
- Confirm WebSocket delivery to frontend.
- Test auth protection on live endpoints.
- Provide evidence (logs, API responses).

---

## 8. References & Dependencies

- W0-U01 through W0-U04 (all approved)
- 09_ITRGA_REASONING_FRAMEWORK.md (mandatory)
- All prior governing documents

---

## 9. Authorization & Signature

**This Build Order is hereby issued by the Independent Technical Review & Governance Authority.**

**Issued By:** ITRGA  
**Date:** 2026-07-10  

**Next Action Required from Development Authority:**
1. Acknowledge receipt of Build Order W0-U05.
2. Implement while applying the full ITRGA Reasoning Framework.
3. Ensure the single-uvicorn pattern remains supported.
4. Submit the completed unit + comprehensive Delivery Report for independent review.

---

**End of Build Order W0-U05**

---

*ITRGA — Engineering truth through disciplined, evidence-based, multidisciplinary investigation.*