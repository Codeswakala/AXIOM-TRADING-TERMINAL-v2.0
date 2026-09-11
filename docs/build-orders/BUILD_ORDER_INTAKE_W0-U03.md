# Build Order Intake — W0-U03 (Developer Reasoning Framework)

| Item | Value |
|------|--------|
| Build Order | W0-U03 — Market Data Ingestion Foundation |
| Intake By | Development Authority |
| Date | 2026-07-10 |
| Status | ACCEPTED — reasoning complete; implementation authorized |
| Prerequisite | W0-U02 approved (per BO text) |

---

## 1. Problem Understanding

**Problem:** AXIOM has a persistence layer (`candles`) but no controlled path to load historical OHLCV into it.

**Why it exists:** Without ingestion, the platform cannot exercise multi-market data foundations or prepare for later live feeds / ML datasets.

**Owner subsystem:** Market Data Layer → application services → repositories → DB.

**Existing assets to reuse:** `Candle` ORM, `CandleRepository`, session/UoW, audit repository, health/ready.

---

## 2. Engineering Hypothesis

If we implement a synchronous, repository-backed CSV ingestion pipeline with validation, normalization, and natural-key upsert, then:

- sample historical data will persist reliably;
- repeated loads will not create duplicates;
- observability will expose run stats;
- the design will extend later to live feeds without redesigning the Candle natural key;

while remaining out of scope for live streaming, broker connectors, ML features, and advanced cleaning.

---

## 3. Decomposition

| Subproblem | Responsibility |
|------------|----------------|
| CSV parsing + schema mapping | Loader |
| Timestamp/price/volume normalize + quality flags | Normalization |
| Dedup / upsert by natural key | Repository enhancement |
| Job orchestration + stats | IngestionService |
| Run metadata (audit trail of jobs) | IngestionRun model + repo |
| Verification API | Thin routes |
| Fixtures + tests | tests/fixtures |

---

## 4. Alternatives Considered

| Option | Pros | Cons | Decision |
|--------|------|------|----------|
| A. Sync CSV pipeline via service + repos | Simple, testable, fits foundation | Not for HFT | **Selected** |
| B. Celery/async job queue | Scales jobs | Over-scope W0 | Deferred |
| C. Direct SQL bulk COPY only | Fast | Bypasses repository pattern | Rejected for foundation |
| D. Live WS feeds now | Realism | Explicitly out of scope | Rejected |

---

## 5. Risks

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Bad CSV / timezone ambiguity | High | Data quality | Explicit UTC parse + validation errors |
| Duplicate loads | High | Corrupt history | Natural key upsert |
| Postgres untested in sandbox | Medium | Path risk | Keep SQLite tests; document Operator verification §7 |
| Scope creep to live feeds | Medium | Governance | Hard boundaries in API/docs |

---

## 6. Constraints

- Must use W0-U02 repository layer  
- No live streaming, ticks, ML, advanced gap fill  
- Delivery Report must apply ITRGA reasoning structure (hypothesis, evidence levels, unknowns)  
- DA Reasoning Framework: reason → design → implement → validate → preserve knowledge  

---

## 7. Engineering Decision Approval

| Gate | Status |
|------|--------|
| Problem understood | ✓ |
| Architecture reviewed | ✓ |
| Alternatives evaluated | ✓ |
| Risks documented | ✓ |
| Hypothesis stated | ✓ |

**Proceed to implementation.**

---

**End of Intake W0-U03**
