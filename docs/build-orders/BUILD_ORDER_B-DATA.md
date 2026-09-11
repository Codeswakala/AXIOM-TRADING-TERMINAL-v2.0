# AXIOM — BUILD ORDER BO-B-DATA (R1)
## Real Historical Data Acquisition & Authority-Label Hardening

| Item | Value |
|------|-------|
| Build Order ID | `BO-B-DATA` |
| Programme | Backend Operationalization — the **R1 decision** (Operator, 2026-08-19: "proceed with R1") |
| Authorizing authority | **Operator** (R1: authorize acquisition of real historical data) |
| Predecessors | BO-B-00 · BO-B-01 · BO-B-02 (all APPROVED WITH OBSERVATIONS) |
| Governing documents | `07_ML_SPEC.md` · `05_SYSTEM_ARCHITECTURE.md` v2.0 · `VALIDATION_TIER_SEPARATION.md` (B-01 binding rule) · `17_INSTITUTIONAL_SECURITY_STANDARD.md` |
| Implementer | Development Authority (DA) |
| Reviewer | ITRGA |
| Status | **ISSUED — awaiting DA implementation** |
| Governance Gate | CLOSED (unchanged) · Production NOT CERTIFIED (unchanged) |

---

## 0. Purpose and the honest character of this unit

This order executes the Operator's **R1** decision: make **real historical market data** available so the substantive ML path (research / economic / generalization validation, and ultimately model promotion and B-03 signals) is no longer blocked.

This is **not a pure-code order**. It has two parts with a hard ordering:

- **Part A (prerequisite, must land and be verified first):** Authority-label hardening — fix the fixture-convention hazard so AUTHORITATIVE status can only be granted through an explicit, audited, honest label.
- **Part B (the payload):** Acquire, verify, and ingest a lawfully-sourced real historical OHLCV corpus, labeled `historical:real`, with documented provenance and pinned hashes.

**Operator responsibility — read this:** data licensing is a **legal** matter. The Operator retains final responsibility for the lawfulness of the chosen data source and its terms of use. The DA must document the source and its license; **ITRGA verifies provenance, honesty, and reproducibility — ITRGA does not and cannot issue a legal opinion** on a data license. A source whose license/ToS does not permit this use is disallowed by this order regardless of engineering quality.

---

## 1. Objective

1. Remove the path by which data could silently acquire AUTHORITATIVE status through legacy fixture labels.
2. Establish a real, lawfully-sourced, honestly-labeled historical corpus that passes the ChronologyGuard at authoritative tier and can back `research_validation`, `economic_validation`, and `generalization_validation` snapshots.
3. Make the corpus **reproducible/auditable** even though real data cannot be regenerated: pinned files + hashes + provenance records.

---

## 2. Scope

### Part A — Authority-label hardening (prerequisite; OBS-B01-2 / OBS-B02-3)

- **A1.** Tighten `authority_from_source()` so **AUTHORITATIVE is granted only through an explicit, declared real-data label** — `historical:real` (or a governed equivalent with identical semantics). 
- **A2.** Remove or downgrade the legacy fixture convention: `sample:*` / `csv:*` / `test` must **no longer** map to AUTHORITATIVE. Map them to a **non-authoritative** authority (e.g. UNKNOWN or a new explicit `fixture` class) so a real file ingested without an honest label can never enter an authoritative snapshot.
- **A3.** Fix the sample-ingestion default (`app/api/routes/ingestion.py` line ~126, `source=payload.source or f"sample:{payload.sample_name}"`) so it cannot manufacture an authoritative label by default.
- **A4.** Pin the new behavior with tests: (a) `historical:real` → AUTHORITATIVE; (b) `sample:*`/`csv:*`/`test` → non-authoritative; (c) a real-data ingest without an explicit `historical:real` label is quarantined from a research-tier snapshot.
- **A5.** Reconcile any existing W2-U01 tests that pinned the old convention — the report must disclose each changed test and the reason (same discipline as B-02 deviation D1). No test may be silently deleted to force green.

### Part B — Real historical data acquisition & ingestion

- **B1. Source selection & license declaration.** The DA selects a real historical OHLCV source whose license/ToS permits this use (examples of candidate classes — not prescriptions — include public exchange historical klines, or public-domain/CC-licensed market datasets). The DA must document: source name, access method (API/URL/download), license or ToS reference, permitted-use statement, and retrieval date.
- **B2. Corpus definition.** Multi-market, multi-symbol H1 (or finer) OHLCV, honest date ranges, no backfilled/fabricated bars. The corpus must be **sufficient for research-tier use** (realistic symbol count and history length) — not a token sample.
- **B3. Retrieval & pinning.** Retrieve via a documented, repeatable method; **pin the retrieved files** (committed or hash-recorded) so the corpus is auditable even though re-retrieval would yield different data. Record per-file SHA-256.
- **B4. Ingestion with honest labels.** Ingest through the governed seam with explicit `source="historical:real"`; every series persists a `market_series_metadata` row with `source_authority=AUTHORITATIVE`.
- **B5. Guard compliance.** The ingested real data must pass the **ChronologyGuard at authoritative tier** (no future-dated, out-of-order, duplicate, or naive-timestamp bars) — evidence of the guard run with zero quarantines (or a fully-disclosed quarantine breakdown).
- **B6. Research-tier snapshot proof.** Freeze at least one snapshot at `research_validation` tier over the real corpus, demonstrating the tier rule now accepts genuinely authoritative data (and — negative control — that a synthetic-labeled series is still rejected at that tier).

---

## 3. Exclusions (out of scope — do NOT do)

- **No** live data feed, broker connection, or streaming (this is historical data only).
- **No** execution, actuation, gate-opening, account/broker/trading state.
- **No** data whose license/ToS does not permit this use — regardless of convenience.
- **No** fabrication, gap-filling with synthetic/simulated bars, or relabeling synthetic data as real.
- **No** research *conclusions* drawn in this unit (a research-tier snapshot may be created as proof; no statistical/economic/generalization **claims** — those belong to the substantive ML unit).
- **No** model training or promotion in this unit.
- **No** inference, signals, alerts, or intelligence (B-03+).
- **No** frontend changes.
- **No** modification of the governance hierarchy or constitutional documents.
- **No** repository publication (custody model).

---

## 4. Exact deliverables

1. Part A code change (`market_data_query.py`, `ingestion.py`) + tests, with per-file SHAs.
2. Part A test evidence (executed).
3. A **Data Source & License Declaration** (document) for the chosen real-data source.
4. The pinned real corpus files + per-file SHA-256 manifest.
5. Ingestion evidence: `market_series_metadata` rows with AUTHORITATIVE authority; `ingestion/runs` + `stats` + `candle-counts` non-zero with `historical:real` labels.
6. ChronologyGuard-at-authoritative-tier evidence (zero-quarantine run, or disclosed breakdown).
7. One `research_validation` snapshot proof (+ negative control for synthetic rejection).
8. Delivery Report (§11) with transmission manifest.

---

## 5. Dependencies

- **Upstream:** BO-B-02 (closed). The threshold gate and tier rule are inputs; this unit unblocks their *substantive* use.
- **Internal ordering:** **Part A must land and be ITRGA-verified before Part B data is ingested.** Part B data ingested under the un-hardened labels would be a governance violation and will be rejected.
- **Downstream:** the substantive ML unit (real model + promotion) and B-03 (signals) consume this corpus.

---

## 6. Allowed files / components

- `backend/app/ml/dataset/market_data_query.py` (Part A).
- `backend/app/api/routes/ingestion.py`, `backend/app/ingestion/*` (Part A default-label fix; Part B ingestion path if needed).
- `backend/tests/**` (new/churn tests for both parts).
- `backend/docs/**` (Data Source & License Declaration; any ADR).
- Corpus data files (pinned) and a SHA manifest.
- The Delivery Report.

Anything outside this list is **not authorized**.

---

## 7. Security & integrity constraints (binding)

- **Licensing is mandatory.** No data may be ingested whose license/ToS the DA cannot document as permitting this use. The declaration must be included in the Delivery Report.
- **Honesty is mandatory.** `historical:real` must mean genuinely real, sourced data. No relabeling, no synthetic backfill, no fabricated bars.
- No secrets/credentials in any changed file or report. Any API key needed for retrieval must **not** be committed; retrieval must be reproducible with the key held outside the artifact.
- The ChronologyGuard and tier rule must not be weakened. Part A must not open a new authority bypass.
- The threshold gate (B-02) is unaffected and must remain fail-closed.

---

## 8. Acceptance criteria

### Part A
- [ ] `historical:real` → AUTHORITATIVE (explicit label only).
- [ ] `sample:*` / `csv:*` / `test` → **non-authoritative** (no silent authority).
- [ ] Sample-ingestion default no longer manufactures an authoritative label.
- [ ] Tests pin all of the above; any W2-U01 test churn disclosed with reason.
- [ ] A real-data ingest without an explicit `historical:real` label is quarantined from a research-tier snapshot.

### Part B
- [ ] Source & License Declaration present, with license/ToS reference and permitted-use statement.
- [ ] Real corpus pinned with per-file SHA-256; honest date ranges; no fabricated bars.
- [ ] Ingested with `historical:real` labels; `market_series_metadata.source_authority=AUTHORITATIVE` verified.
- [ ] ChronologyGuard passes at authoritative tier (or a fully-disclosed quarantine breakdown).
- [ ] One `research_validation` snapshot frozen over real data (proof), + negative control (synthetic still rejected at that tier).

---

## 9. Evidence requirements (custody model + CA-B01-1 transmission manifest)

**Binding (CA-B01-1):** the Delivery Report must include a **transmission manifest** — every declared artifact → transmitted filename + hash. A declared-but-untransmitted artifact is an automatic **CORRECTION REQUIRED** on delivery process.

| Item | Class | Form |
|------|-------|------|
| Patch artifact + per-file SHAs + `git apply --check` transcript | Level I | patch + transcript |
| Executed test output (Part A + any churn) | Level II | run transcript |
| Data Source & License Declaration | Level III | document |
| Corpus pin manifest (file list + SHA-256) | Level I | manifest |
| Ingestion + metadata + guard evidence | Level I | query/probe output |
| Transmission manifest | — | table in Delivery Report |
| Delivery Report | Level III | §11 structure |

---

## 10. Rollback / containment

- Part A is a small, reversible code change (two files + tests).
- Part B data is additive rows; revert = drop ingested rows, revert patch. The pinned corpus files remain as audit artifacts.
- No schema migration is authorized by default; if strictly required it must be flagged and justified first.

---

## 11. Delivery Report structure (required)

1. Claimed scope vs. this Build Order
2. What changed (files + SHAs + chain position)
3. **Part A** — label-hardening description + test churn disclosure
4. **Data Source & License Declaration** (source, license/ToS, permitted-use statement, retrieval date, access method)
5. Corpus description (symbols, timeframes, date ranges, bar counts) + pin manifest
6. Ingestion + metadata + guard evidence (executed)
7. Research-tier snapshot proof + negative control
8. Test evidence (executed)
9. Deviations register
10. **Transmission manifest** (CA-B01-1)
11. Known limitations / technical debt (incl. any license caveats)

---

## 12. Completion condition

Complete when: Part A criteria met **first**, Part B criteria met, evidence (§9) transmitted and verified (transmission manifest complete), the Delivery Report submitted, **and ITRGA issues its independent determination** (which will include review of the source/license provenance — noting again that lawfulness is the Operator's legal responsibility, not ITRGA's legal opinion). A DA declaration of completion is not evidence and does not close this unit.

**Next authorization state:** upon ITRGA approval of BO-B-DATA, the substantive ML unit (real model + governed promotion) — and thereafter B-03 (signals) — may be issued, now unblocked by real data.

---

**End of Build Order BO-B-DATA (R1)**
