# AXIOM Build Order
## W0-U03 — Market Data Ingestion Foundation

**Build Order ID:** W0-U03  
**Wave:** 0 — Foundation  
**Unit:** 03  
**Version:** 1.0  
**Status:** ISSUED  
**Authority:** Independent Technical Review & Governance Authority (ITRGA)  
**Date Issued:** 2026-07-10  
**Authorized By:** ITRGA (following successful approval of W0-U02)  
**Classification:** Official Build Order  
**Governing Documents:**  
- 09_ITRGA_REASONING_FRAMEWORK.md (mandatory application)  
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

This Build Order authorizes the Development Authority to implement the foundational market data ingestion capabilities for AXIOM.

This unit exercises the persistence layer delivered in W0-U02 by introducing controlled historical data loading, normalization, storage, and basic validation using the `candles` table.

It establishes the first real data flow in the platform while maintaining strict institutional standards.

---

## 2. Objectives

1. Implement a clean, extensible market data ingestion pipeline.
2. Support loading of historical OHLCV data from CSV and basic file sources.
3. Perform data normalization, validation, and deduplication using the approved Candle model.
4. Persist data reliably through the repository layer established in W0-U02.
5. Provide basic ingestion status, statistics, and error handling.
6. Expand observability for data ingestion operations.
7. Create comprehensive tests (unit + integration) exercising the full ingestion path.
8. Update the Engineering Knowledge Management System with relevant ADRs and records.
9. Maintain full compliance with the new ITRGA Reasoning Framework and all governing documents.
10. Preserve future extensibility for live feeds, multiple markets, and high-frequency data.

---

## 3. Scope

### In Scope
- Ingestion service / pipeline abstraction.
- CSV historical data loader (with schema validation).
- Data normalization (timestamp handling, price/volume cleaning, basic quality checks).
- Deduplication and upsert logic using the Candle natural key.
- Basic ingestion job orchestration (synchronous for foundation).
- API endpoints for triggering ingestion (verification only) and querying ingestion status.
- Enhanced health/readiness and new ingestion-specific metrics.
- Structured logging for ingestion events, errors, and statistics.
- Unit and integration tests using the W0-U02 test database patterns.
- At least two new Architecture Decision Records.
- Full Delivery Report applying the 09_ITRGA_REASONING_FRAMEWORK.md.

### Explicitly Out of Scope
- Live market data streaming / WebSocket feeds (deferred).
- Broker-specific data connectors (beyond basic abstraction).
- Real-time tick data.
- Advanced data cleaning, gap filling, or resampling.
- Any machine learning feature computation.
- Production-scale performance optimization or partitioning.
- Authentication-protected ingestion endpoints (basic foundation only).
- Multi-timeframe or cross-market aggregation logic.

---

## 4. Deliverables

The Development Authority shall deliver:

1. **Ingestion Pipeline**
   - `IngestionService` (or equivalent) with clear responsibilities.
   - CSV loader with configurable column mapping and validation.
   - Data normalization utilities.
   - Repository-backed persistence with upsert/deduplication.

2. **Domain & Persistence Enhancements**
   - Any necessary refinements to the Candle model or repository (documented).
   - Basic ingestion metadata table (optional but recommended for audit).

3. **API Surface (Verification)**
   - Endpoints for:
     - Triggering a test ingestion (from sample data)
     - Querying recent ingestion runs / statistics
     - Basic candle count per market

4. **Observability**
   - Ingestion-specific logging (records processed, errors, duration).
   - Updated `/ready` and new `/persistence/ingestion-stats` or similar.
   - Basic metrics (records ingested, last run time).

5. **Testing**
   - Unit tests for normalization, validation, deduplication.
   - Integration tests that load sample CSV data into the test database and verify persistence.
   - Test data fixtures (small, versioned sample CSVs).

6. **Engineering Knowledge Management**
   - ADR-005: Market Data Ingestion Architecture
   - ADR-006: Data Validation & Deduplication Strategy
   - Updated Decision Log and Technical Debt Register

7. **Documentation**
   - Ingestion usage guide (`docs/ingestion/`)
   - Updated `PROJECT_STATE.md`
   - Synchronization of governing documents

8. **Delivery Report**
   - `DELIVERY_REPORT_W0-U03.md` that fully applies the **09_ITRGA_REASONING_FRAMEWORK.md** (hypothesis-driven, multidisciplinary, evidence hierarchy, unknowns register, etc.).

---

## 5. Success Criteria / Definition of Done

This unit is complete only when **all** of the following are met:

- [ ] Sample historical CSV data can be ingested and stored in the database
- [ ] Data is correctly normalized and deduplicated on repeated loads
- [ ] Ingestion statistics and status are observable via API/health
- [ ] All tests pass (minimum 12–15 new tests recommended)
- [ ] Repository layer from W0-U02 is actively exercised
- [ ] At least two new ADRs created with rigorous rationale
- [ ] Delivery Report demonstrates full application of the ITRGA Reasoning Framework
- [ ] Scope strictly respected (no live feeds, no ML)
- [ ] Documentation is complete and reproducible
- [ ] Implementation aligns with merged System Architecture and all higher governing documents
- [ ] Unit is independently reviewable

---

## 6. Constraints & Standards

The Development Authority **must**:

- Strictly apply **09_ITRGA_REASONING_FRAMEWORK.md** when preparing the Delivery Report.
- Follow Clean Architecture and the merged System Architecture.
- Use the repository pattern established in W0-U02.
- Record all technical debt explicitly.
- Preserve future compatibility for live data, multi-market, and ML feature pipelines.
- Maintain intellectual honesty regarding what has and has not been verified.

---

## 7. Operator Verification Requirements (Critical)

Because previous units (especially W0-U02) were developed in sandbox environments without full production dependencies, the following **Operator Verification Steps** must be performed after ITRGA approval of this unit (and retroactively recommended for W0-U02).

### 7.1 Mandatory Operator Tests for W0-U02 (Persistence Layer)

The Operator (or their controlled environment) **shall** perform the following before relying on W0-U02 in further development:

1. Deploy or connect to a real **PostgreSQL** instance (version 14+ recommended).
2. Set `AXIOM_DATABASE_URL` to a valid PostgreSQL connection string.
3. Run `alembic upgrade head`.
4. Execute the full test suite against PostgreSQL (`pytest` with real DB).
5. Manually verify:
   - `/ready` reports database as `up` with non-zero latency.
   - Basic Candle CRUD works via the persistence API or scripts.
6. Document results (logs, screenshots, or terminal output) in the project.

**This verification closes TD-001b from W0-U02.**

### 7.2 Operator Tests for W0-U03 (This Unit)

After ITRGA approval of W0-U03, the Operator must independently verify:

1. **PostgreSQL Path**:
   - Run the new ingestion against a real PostgreSQL database.
   - Confirm data is correctly stored and deduplicated.

2. **Ingestion Functionality**:
   - Load at least two different sample CSV files (different markets/timeframes).
   - Verify normalization (timestamps, prices, volumes).
   - Confirm deduplication on repeated ingestion of the same file.

3. **Observability**:
   - Check ingestion logs and statistics endpoints.
   - Verify `/ready` and ingestion stats reflect activity.

4. **Reproducibility**:
   - Follow the reproduction instructions in the Delivery Report from a clean environment.
   - Confirm all tests still pass.

5. **Evidence Submission**:
   - The Operator should record verification results (especially PostgreSQL + real ingestion) and make them available for future ITRGA reviews.

These Operator tests are **not** part of the Development Authority's Delivery Report but are required for full institutional confidence.

---

## 8. References & Dependencies

- **Completed & Approved**: W0-U01 and W0-U02 (including ITRR-W0-U02-001)
- **New Constitutional Document**: 09_ITRGA_REASONING_FRAMEWORK.md
- **All prior governing documents** (current versions)
- Sample market data CSVs will be provided or generated within the unit.

---

## 9. Delivery Report Requirements

The Delivery Report **must** demonstrate explicit application of the **09_ITRGA_REASONING_FRAMEWORK.md**, including:

- Hypothesis-driven investigation approach
- Evidence hierarchy classification (Level I–IV)
- Multidisciplinary analysis (from the expanded list of disciplines)
- Counter-hypothesis analysis
- Consequence, risk, and alternative analysis
- Future compatibility assessment
- Unknowns Register
- Clear distinction between Verified Fact, Supported Inference, and Unknown
- Review Confidence Assessment with rationale

The report must be written with the mindset of an institutional engineering audit.

---

## 10. Authorization & Signature

**This Build Order is hereby issued by the Independent Technical Review & Governance Authority.**

**Issued By:** ITRGA  
**Date:** 2026-07-10  
**Reference:** Following approval of W0-U02 and formal adoption of 09_ITRGA_REASONING_FRAMEWORK.md

**Next Action Required from Development Authority:**
1. Acknowledge receipt of Build Order W0-U03.
2. Implement while applying the full ITRGA Reasoning Framework internally.
3. Produce a Delivery Report that rigorously follows 09_ITRGA_REASONING_FRAMEWORK.md.
4. Submit the completed unit + Delivery Report for independent ITRGA review.

---

**End of Build Order W0-U03**

---

*ITRGA — Engineering truth through disciplined, evidence-based, multidisciplinary investigation.*