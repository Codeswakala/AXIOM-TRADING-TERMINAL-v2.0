# AXIOM V2 BE-2 — Market Data Abstraction and Historical Data Integrity Design Plan

| Field | Value |
|---|---|
| Document ID | AXIOM-V2-BE-2-DA-PLAN-001 |
| Version | 2.0.0 (corrections for ITRGA-REV-V2-BE-2-001, findings PLAN-001…004) |
| Status | **RESUBMITTED FOR ITRGA REVIEW** — not implementation authorization |
| Date | 2026-08-24 |
| Author | Development Authority (DA) |
| Responds to | ITRGA-REQ-V2-BE-2-001; ITRGA-REV-V2-BE-2-001 |
| Governing context | Active V1 constitutional hierarchy; V2 Charter (AXIOM-V2-GOV-CHARTER-001); Document 17; BE-1 final determination ITRGA-DET-V2-BE-1-001; V2 Backend Roadmap Band BE-2 |

---

# Revision 2.0.0 — Finding Closure Map

| Finding | Correction applied | Where |
|---|---|---|
| V2-BE2-PLAN-001 (snapshot truth model) | **Option B adopted**: artifact renamed **As-Of Verification Record** (`v2_md_asof_verification`); all "snapshot"/reproducibility claims removed from BE-2; explicitly declared tamper-evidence-only and non-reconstructive; true immutable snapshot storage deferred to a later authorized band | Part E.1 (rewritten), C.1, C.3, H.2 |
| V2-BE2-PLAN-002 (write boundary/idempotency) | New **Part D.0 Write-Boundary Contract**: GET endpoints are pure (zero persistence side effects except BE-1 sensitive-read audit); all BE-2 mutations occur only in two explicit, audited, idempotent POST operations; fingerprint dedup + state-transition rules defined for every exception type | Part D.0 (new), C.3, D.2 |
| V2-BE2-PLAN-003 (provenance governance boundary) | Explicit active-vocabulary clause: BE-2 responses may emit **only** `seed:synthetic`, `live:simulated`, and honest `unknown`; activating any other authority value requires a V2 Amendment Register entry naming the affected V1 rule | Part B.4 (amended) |
| V2-BE2-PLAN-004 (seed lifecycle) | New **Part C.4 Reference-Data Seed Lifecycle**: exact seed inventory, DB CHECK constraints, versioned seed manifest with SHA-256, governed change process; unrecognized V1 markers stay `unknown` and are never auto-registered | Part C.4 (new), B.5 |

---

# Part A — Authority, Scope, and V1 Compatibility

## A.1 Source Authorities

1. `00_VISION_AND_PRINCIPLES.md` — data honesty; uncertainty never hidden
2. `03_AXIOM_SPEC.md` — market-agnostic architecture; documentation discipline
3. `05_SYSTEM_ARCHITECTURE.md` — Market Intelligence System boundary (§11.3)
4. `17_INSTITUTIONAL_SECURITY_STANDARD.md` — SAL, ownership, retention, least privilege
5. V2 Charter invariants — no fabricated domain state; unknown is an allowed state; traceability
6. BE-1 approved primitives — V2 identifiers, audit, lineage, mode, RBAC, errors, temporal contracts
7. ITRGA-REQ-V2-BE-2-001 — authorized planning scope and mandatory exclusions

## A.2 BE-2 Objective

Establish a **provider-neutral internal market-data contract and historical-data
integrity foundation** in Research/Simulation mode only:

- canonical instrument identity and symbol mapping;
- source/provenance/freshness/availability taxonomy that makes it impossible to
  represent simulated or synthetic data as real or live;
- chronological-integrity controls (ordering, duplicates, gaps, staleness,
  timezone, future-data prevention);
- tamper-evident as-of verification records with read-only query contracts
  (truthfully scoped per Part E.1 — no reproducibility claim);
- truthful provenance mapping of the existing V1 simulated feed.

**BE-2 integrates no external provider and makes no real-data claim.**

## A.3 In-Scope

1. `backend/app/v2/marketdata/` bounded package: contracts, normalization
   boundary, integrity validators, verification service, repositories, API routes.
2. Six new V2 tables (Part C): instrument registry, symbol mapping, data-source
   registry, series catalog, integrity-exception (quarantine) records,
   as-of verification records.
3. One additive Alembic migration (+ append-only triggers where mandated).
4. Authenticated, RBAC-guarded, Research/Simulation-only read APIs under
   `/api/v2/marketdata/*` using the BE-1 response envelope.
5. Read-only V1-simulator provenance adapter (labelling, not rewiring).
6. Seeded read-only reference data (provenance vocabulary, canonical
   instruments for the existing simulated symbols, source registry entries).
7. Unit/integration/security/regression/failure-path tests; audit/lineage
   integration via BE-1 primitives; documentation/state/register updates.

## A.4 Out-of-Scope (Mandatory Exclusions — mirrors ITRGA-REQ-V2-BE-2-001 §3)

- Real external provider connection, provider credentials, vendor entitlements,
  commercial licensing, external ingestion, or any real-data claim
- Paper/Live mode, brokers, exchanges, accounts, positions, orders, fills,
  execution, reconciliation, external AI
- Frontend redesign; browser-side authoritative aggregation
- V1 removal/rewrite or unapproved schema change (V1 `candles`,
  `market_series_metadata`, live service, hub, and adapters remain untouched)
- Provider-specific interface engineering beyond the neutral contract (no
  vendor SDK shapes, no entitlement models, no rate-limit frameworks — BE-3)
- Git/GitHub operations by the DA

## A.5 BE-1 Observations Carried Forward

| Observation | BE-2 treatment |
|---|---|
| OBS-V2-BE1-01 V1 lint/migration-drift debt | Carried; BE-2 adds no V1 changes; drift gate per Part G |
| OBS-V2-BE1-02 deployment SAL controls unverified | All SAL infrastructure controls classified deployment-owned assumptions (Part F); no certification claim |
| OBS-V2-BE1-03 PostgreSQL revalidation gate | BE-2 changes migration/models/metadata → **full PostgreSQL rerun is mandatory exit evidence** (Part G) |
| OBS-V2-BE1-04 repository custody | No DA Git operation; evidence via review channel |

## A.6 V1 Compatibility Matrix

| V1 element | BE-2 effect |
|---|---|
| `candles` table, `market_series_metadata` | Untouched; read-only referenced by provenance adapter |
| `app/market/live_service.py`, `hub.py`, `adapters/*` | Untouched; BE-2 does not alter the live seam |
| V1 market APIs (`/api/v1/market/*`) | Untouched; no behavioral change |
| V1 dataset snapshot models (`dataset_snapshots` …) | Untouched; BE-2 snapshots are market-data snapshots (different domain object); no FK into V1 tables |
| V1 tests (552) | Must pass unmodified |
| BE-1 V2 primitives | Reused, not modified: identifiers, audit, lineage, mode dependency, RBAC factory, error contracts, `require_utc()` |

## A.7 Confirmation

The DA confirms this plan designs only the authorized BE-2 scope, proposes no
provider integration, no real-data claim, no Paper/Live surface, and no V1
mutation.

---

# Part B — Canonical Data-Domain Model and Ownership

## B.1 Module Structure

```text
backend/app/v2/marketdata/
├── __init__.py
├── contracts.py          # frozen dataclasses/enums: instrument, source, quote,
│                         # bar, tick, depth, event, verification, provenance
├── provenance.py         # provenance/freshness/availability taxonomy + guards
├── identity.py           # canonical instrument identity + symbol mapping rules
├── normalization.py      # source-neutral normalization boundary (pure functions)
├── integrity.py          # ordering/duplicate/gap/stale/timezone/future validators
├── verification.py       # as-of verification record builder + content hashing
├── repositories.py       # read/append repositories (no update/delete on
│                         # append-only tables)
├── v1_adapter.py         # read-only V1 simulated-feed provenance adapter
└── api/
    ├── instruments.py    # read-only instrument/mapping endpoints
    ├── sources.py        # read-only source registry + status endpoints
    ├── series.py         # read-only series/bars query endpoints
    ├── verification.py   # read-only verification-record endpoints
    └── router.py         # mounted under /api/v2/marketdata
```

Single responsibility per module; normalization and integrity are pure
(no I/O) for deterministic testing.

## B.2 Source-of-Truth Ownership

| Domain object | Source of truth | Writer | Readers |
|---|---|---|---|
| Canonical instrument | `v2_md_instrument` | Migration seed only (BE-2); governed admin workflow deferred | All V2 read APIs |
| Symbol mapping | `v2_md_symbol_map` | Migration seed only | Normalization boundary |
| Data source registry | `v2_md_source` | Migration seed only | Provenance guards, APIs |
| Series catalog | `v2_md_series` | Catalog service via W-1 only (server-side) | Query APIs |
| Integrity exceptions | `v2_md_integrity_exception` | Integrity validators via W-1/W-2 only (append-only, fingerprint-deduplicated) | Audit/query APIs |
| As-of verification records | `v2_md_asof_verification` | Verification service via W-2 only (append-only) | Query APIs, future research bands |
| Bar payloads (Research/Simulation) | V1 `candles` (existing, labelled) | V1 live service (unchanged) | BE-2 read boundary with provenance attached |

**Design decision D-1:** BE-2 does **not** create a second bar-storage table.
Existing V1 `candles` remains the only bar store; BE-2 wraps reads with
canonical identity + mandatory provenance. This avoids dual-write integrity
risk, avoids duplicating ~identical schema, and keeps BE-2 additive. A future
band may introduce partitioned real-data storage when providers are authorized.

## B.3 Canonical Contracts (`contracts.py`)

Frozen dataclasses (values) and `str`-enums (vocabulary), all timezone-aware
UTC via BE-1 `require_utc()`:

- `CanonicalInstrument`: `instrument_id` (stable, e.g. `fx.eurusd`),
  `market_class`, `base/quote` or underlying, `display_symbol`, `precision`,
  `contract_metadata` (JSON, no secrets)
- `SymbolMapping`: `source_id`, `source_symbol`, → `instrument_id`, `direction`
- `DataSource`: `source_id`, `kind` (`simulator | seed | import | reserved`),
  `authority` (`simulated | synthetic | historical | reserved-live`),
  `mode_scope` (RESEARCH/SIMULATION), `active`
- `QuoteContract`, `BarContract`, `TickContract`, `DepthContract`,
  `MarketEventContract` — neutral shapes with mandatory `provenance` field;
  Tick/Depth/Event are **contract-only in BE-2** (no storage, no API) so the
  vocabulary exists without speculative tables
- `SeriesDescriptor`: instrument + timeframe + source + coverage window +
  read-time-computed freshness state
- `AsOfVerificationDescriptor`: Part E

## B.4 Provenance / Freshness / Availability Taxonomy (`provenance.py`)

Mandatory on every data-bearing response; never optional, never defaulted to a
"live" value.

```text
provenance.source_kind   = simulator | seed | import | reserved
provenance.authority     = seed:synthetic | live:simulated | historical:imported(reserved) | unknown
provenance.source_id     = registered source identifier
provenance.as_of         = UTC timestamp of last underlying datum
provenance.verification_id = optional (when a read is attested by a verification record)

freshness  = fresh | stale | expired | unknown        (server-computed from as_of + timeframe budget)
availability = available | partial | empty | quarantined | unavailable | unknown
```

Rules:
1. Existing V1 simulated stream data maps to `live:simulated`; V1 seeded
   backfill bars map to `seed:synthetic` (matching the V1 `source` markers
   already present, e.g. the `seed:synthetic` label in `market.py`).
2. `historical:imported` is **reserved vocabulary only** in BE-2 — defined so
   the taxonomy is stable, but no code path can produce it (guard raises
   `V2Error(VALIDATION_FAILED)` if constructed).
3. `unknown` is an allowed, honest state and is rendered as such.
4. A display-contract constant table maps each authority to a mandatory UI
   label (e.g. `SIMULATED`, `SYNTHETIC SEED`); the API returns the label so
   future frontend work cannot mislabel data. **No response can omit it.**

**Active-vocabulary governance boundary — AMENDED per V2-BE2-PLAN-003:**

> BE-2 active API responses may emit **only** the V1-authorized authority
> values `seed:synthetic` and `live:simulated`, plus honest `unknown` and the
> availability/freshness states. This is enforced three ways: (a) an
> emission-time guard (`ACTIVE_AUTHORITY_VALUES` frozen set) that raises
> `V2Error(VALIDATION_FAILED)` on any other value; (b) a DB CHECK constraint
> on `v2_md_source.authority` limiting stored active sources to the
> authorized values (`reserved-*` rows carry `active=false` and are refused
> at emission); (c) an API test asserting no BE-2 response ever contains an
> authority outside the active set.
>
> **Activation of `historical:imported`, any provider authority, or any
> real/live authority is a V1/V2 governance change, not an implementation
> decision.** It requires a specific `V2_AMENDMENT_REGISTER.md` entry naming
> the affected V1 capability rule (the established `seed:synthetic` /
> `live:simulated` product vocabulary), the replacement rule, effective
> scope, and the authorizing Build Order — per the V2 Charter §8 amendment
> process. BE-2 cannot and does not broaden the active product provenance
> vocabulary.

## B.5 Symbol Mapping and Canonical Identity (`identity.py`)

- `instrument_id` format: `<market_class>.<normalized_symbol>` lowercase,
  deterministic, validated by regex; uniqueness enforced by DB constraint.
- Mapping resolution is exact-match on (`source_id`, `source_symbol`);
  no fuzzy matching. Unmapped symbols → `availability=unknown` +
  integrity-exception record (`unmapped_symbol`), never a guess.
- Seeded scope: the existing simulated/seed symbols present in the V1
  workspace (EURUSD, BTCUSD and the other configured simulator symbols),
  mapped to canonical instruments. No speculative instrument universe.

## B.6 Normalization Boundary (`normalization.py`)

Pure functions: `(raw_row, source, mapping) → BarContract | IntegrityException`.
- Enforces `require_utc()` (naive datetimes rejected — no V1 warning path);
- normalizes decimal precision per instrument;
- attaches provenance; refuses rows whose source is not registered/active;
- provider-neutral by construction: input shape is the adapter-produced neutral
  row (the V1 adapter seam's `NormalizedCandleRow` already matches this
  boundary), not any vendor schema.

---

# Part C — Schema and Migration Design

## C.1 New Tables (six; all additive; one migration `20260824_0039_v2_be2_marketdata`)

| Table | Purpose | Mutability | Key columns (all `created_at DateTime(timezone=True)`) |
|---|---|---|---|
| `v2_md_instrument` | Canonical instrument registry | Read-only seeded (BE-2) | `id`, `instrument_id` UNIQUE, `market_class`, `display_symbol`, `precision`, `metadata` JSON |
| `v2_md_symbol_map` | Source symbol → instrument | Read-only seeded | `id`, `source_id`, `source_symbol`, `instrument_id` FK-by-value, UNIQUE(`source_id`,`source_symbol`) |
| `v2_md_source` | Data-source registry | Read-only seeded | `id`, `source_id` UNIQUE, `kind`, `authority`, `mode_scope`, `active` |
| `v2_md_series` | Series catalog (W-1-written only; freshness computed at read time, **not stored** — see D.0 Rule 2) | Upsert via W-1 only | `id`, `instrument_id`, `timeframe`, `source_id`, `first_open_time`, `last_open_time`, `bar_count`, UNIQUE(instrument,timeframe,source) |
| `v2_md_integrity_exception` | Quarantine/refusal records | **Append-only + triggers**; W-1/W-2-written only; fingerprint-deduplicated | `id`, `series_ref`, `exception_type`, **`fingerprint` UNIQUE** (D.0 Rule 3), `detail` JSON (redacted via BE-1 redaction), `observed_at`, `mode`, `correlation_id` |
| `v2_md_asof_verification` | As-of verification records (tamper-evidence only — Part E.1; renamed from `v2_md_snapshot` per V2-BE2-PLAN-001) | **Append-only + triggers**; W-2-written only | `id`, `verification_id` UNIQUE, `scope` JSON, `as_of`, `content_hash`, `row_count`, `source_ids` JSON, `mode`, `created_by_operator_id` |

CHECK constraints (PLAN-004): `v2_md_source.kind IN ('simulator','seed','import','reserved')`;
`v2_md_source.authority IN ('seed:synthetic','live:simulated','historical:imported','unknown')`
with the emission guard restricting *active* use to the authorized pair;
`v2_md_source.mode_scope IN ('RESEARCH','SIMULATION')`;
`v2_md_instrument.market_class` constrained to the V1 market-class vocabulary;
`v2_md_integrity_exception.exception_type` constrained to the D.2 enum.

Indexes: lookup paths only (`instrument_id`, (`source_id`,`source_symbol`),
series unique triple, `verification_id`, exception (`series_ref`,`observed_at`),
exception `fingerprint` UNIQUE).

## C.2 Migration Rules (BE-1 lessons applied)

1. Every timestamp column `sa.DateTime(timezone=True)`; every seed value
   timezone-aware UTC from the V2 temporal utility (BE-1 PG-001 lesson).
2. All six models imported in `app/db/models/__init__.py` **in the same
   change** so Alembic `target_metadata` includes them (PG-002 lesson).
3. Dialect-aware append-only triggers for `v2_md_integrity_exception` and
   `v2_md_asof_verification` — same PostgreSQL function/trigger and SQLite trigger
   patterns already approved in BE-1; downgrade drops triggers, then tables.
4. Seeds: exactly the Part C.4 canonical inventory (`sim.local` → `live:simulated`;
   `seed.local` → `seed:synthetic`; instruments/mappings for existing simulator
   symbols only), sourced from the versioned seed module with manifest hash.
5. Downgrade removes all BE-2 objects and returns head to `20260823_0038`.

## C.4 Reference-Data Seed Lifecycle — NEW per V2-BE2-PLAN-004

**Canonical seed inventory (exact, closed set for BE-2):**

| Table | Seed rows |
|---|---|
| `v2_md_source` | `sim.local` (kind `simulator`, authority `live:simulated`, active) · `seed.local` (kind `seed`, authority `seed:synthetic`, active). **No other source rows.** No `reserved`-kind row is seeded in BE-2. |
| `v2_md_instrument` | Exactly the instruments for the V1-configured simulator symbol set at implementation time (workspace-verifiable via `AXIOM_LIVE_MARKET_SYMBOLS` defaults and the simulator base-price table — e.g. `fx.eurusd`, `crypto.btcusd`, plus any other symbols the V1 simulator config enumerates). The Delivery Report lists the final enumerated set; nothing speculative. |
| `v2_md_symbol_map` | One exact-match row per (seeded source × seeded instrument) using the V1 symbol strings. |

**Seed manifest and hash:** the seed values live in one reviewable module,
`app/v2/marketdata/seed.py`, as frozen constants (BE-1 `V2_CAPABILITY_SEED` /
`V2_PERMISSION_SEED` pattern). The module computes a deterministic
`SEED_MANIFEST_HASH` (SHA-256 over the canonically-serialized seed set). The
migration embeds the seed *from that module*; a test asserts the DB contents
match the module manifest and its hash — any undocumented edit to seed data
changes the hash and fails the test, making drift-by-code-edit detectable at
Level II.

**Validation constraints:** the C.1 CHECK constraints bound every enum column
at the database layer; UNIQUE constraints bound identity (`instrument_id`,
(`source_id`,`source_symbol`), `source_id`). Contract-layer enums mirror the
CHECKs so invalid values fail in both layers.

**Governed change process:** reference data is read-only at runtime (no
mutation endpoint or service exists). A change to instruments/sources/mappings
requires: (1) a Build Order or ITRGA-accepted correction naming the change,
(2) a new additive migration revising the seed, (3) an updated
`SEED_MANIFEST_HASH` recorded in the Delivery Report, and (4) register/state
synchronization. An undocumented code/migration edit is distinguishable from
a governed change precisely because the governed change carries the manifest
hash delta in its Delivery Report evidence.

**Unrecognized V1 markers:** any V1 `candles.source` value not mapping to a
seeded source surfaces as `authority=unknown` with an `unmapped_symbol`-class
disclosure — it is **never auto-added** to the registry (auto-registration is
prohibited by the absence of any write path; D.0 Rule 2 enumerates all
writers, and none writes reference tables).

## C.3 Read-Model / API Design

All under `/api/v2/marketdata`, mounted in the existing V2 router; all
authenticated; all use BE-1 envelope (mode, correlation_id, timestamp) via
typed Pydantic response models. **GET endpoints are persistence-pure (D.0
Rule 1); the only mutation surface is the two enumerated POST operations
(D.0 Rule 2).**

| Endpoint | Permission | Behavior |
|---|---|---|
| `GET /instruments` | `v2.marketdata.read` | Canonical instruments + mappings (pure) |
| `GET /instruments/{instrument_id}` | `v2.marketdata.read` | Detail envelope (pure) |
| `GET /sources` | `v2.marketdata.read` | Source registry + authority + active state (pure) |
| `GET /series` | `v2.marketdata.read` | Series catalog; freshness/availability computed at read time (pure) |
| `GET /series/{instrument_id}/{timeframe}/bars` | `v2.marketdata.read` | Bars (V1 store read through the boundary) + **mandatory provenance block**; `as_of` bounded by no-future rule (pure) |
| `GET /verification` | `v2.marketdata.read` | As-of verification records (operator-scoped; pure) |
| `GET /verification/{verification_id}` | `v2.marketdata.read` | Descriptor + scope + hash + `reconstructive: false` (pure) |
| `GET /verification/all` | `v2.marketdata.read_all` (SAL-4, admin) | Cross-operator; sensitive read audited (sole GET side effect, per BE-1 pattern) |
| `GET /integrity/exceptions` | `v2.marketdata.read` | Quarantine records (operator/mode-scoped; pure) |
| `POST /catalog/refresh` | `v2.marketdata.catalog.refresh` (admin, SAL-3) | **W-1** — idempotent catalog scan/upsert + deduplicated exception append; audited |
| `POST /verification` | `v2.marketdata.verify` (operator+admin, SAL-3) | **W-2** — append one verification record; audited + lineage |
| `POST /verification/{id}/verify` | `v2.marketdata.verify` | **W-2** — recompute hash; on mismatch transition append one `verification_mismatch` exception; audited |

New permissions (read-only seeded, BE-1 pattern): `v2.marketdata.read`
(operator+admin), `v2.marketdata.read_all` (admin), `v2.marketdata.verify`
(operator+admin), `v2.marketdata.catalog.refresh` (admin). Vocabulary passes
the existing forbidden-marker guard (no gate/execution/order/broker/account/
live/capital/margin tokens).

Error/degraded behavior: BE-1 error contract; empty series → `availability=
empty` with 200 + honest envelope (not 404 fabrication); quarantined series →
`availability=quarantined`; unregistered source/instrument → 404 with generic
detail; all failures correlation-tagged.

---

# Part D — Historical Temporal Integrity and Data Quality

## D.0 Write-Boundary Contract — NEW per V2-BE2-PLAN-002

**Rule 1 — Pure GETs.** Every `GET /api/v2/marketdata/*` endpoint is
persistence-pure: it creates **no** catalog rows, exception rows, or
verification records. The single permitted GET side effect is the BE-1
sensitive-read audit event on `read_all`-class endpoints (established BE-1
behavior). Repeated identical reads produce zero data mutations. Enforced by
integration tests that issue N identical GETs and assert unchanged row counts
across all BE-2 tables.

**Rule 2 — Enumerated writers.** Every BE-2 mutation occurs in exactly one of
two explicit, authenticated, audited, idempotent operations. No other code
path writes BE-2 tables.

| ID | Operation | Endpoint | Permission | Writes | Transaction boundary |
|---|---|---|---|---|---|
| W-1 | Catalog refresh | `POST /api/v2/marketdata/catalog/refresh` | `v2.marketdata.catalog.refresh` (admin; SAL-3) | Upserts `v2_md_series` (keyed on UNIQUE(instrument,timeframe,source)); appends deduplicated `v2_md_integrity_exception` rows discovered during scan | One transaction per series; BE-1 audit event `v2.marketdata / catalog.refresh` with correlation ID; result envelope reports created/updated/unchanged/exception counts |
| W-2 | Verification record create / re-verify | `POST /api/v2/marketdata/verification` and `POST /api/v2/marketdata/verification/{id}/verify` | `v2.marketdata.verify` (operator+admin; SAL-3) | Appends one `v2_md_asof_verification` (create) or one `verification_mismatch` exception row (re-verify, only on mismatch state change); BE-1 lineage + audit | Single transaction; audited both paths |

Both POSTs are Research/Simulation-mode-gated, carry the BE-1 envelope, and
are **not** data-mutation endpoints in the product sense: they materialize
derived/attestation state only; bar data remains untouched V1 property.
Freshness/staleness on GET responses is **computed at read time** from
`last_open_time` — it is never persisted by a GET (removes the read-path
upsert ambiguity in v1.0.0; `v2_md_series.freshness` column is dropped from
the schema and freshness becomes a response-time value).

**Rule 3 — Idempotency and deduplication.** `v2_md_integrity_exception` gains
a `fingerprint` column, UNIQUE-constrained, computed as:

```text
fingerprint = SHA-256(series_ref | exception_type | affected_natural_key | state_basis)
```

where `affected_natural_key` identifies the offending datum (e.g. duplicate/
out-of-order/future row's natural key, gap's missing-period start, unmapped
`source_symbol`) and `state_basis` is defined per type below. An insert that
collides on `fingerprint` is a no-op (`ON CONFLICT DO NOTHING` semantics) —
repeated detection of the same condition can never create duplicate rows or
duplicate audit events (audit fires only on actual insert).

| Exception type | `affected_natural_key` | `state_basis` | State-transition rule |
|---|---|---|---|
| `out_of_order` | Offending row natural key | constant | Recorded once per offending row, ever |
| `duplicate` | Duplicate candidate natural key | constant | Once per candidate row |
| `future_data` | Offending row natural key | constant | Once per row |
| `unmapped_symbol` | (`source_id`,`source_symbol`) | constant | Once per unmapped pair |
| `gap` | Series + missing-period start | coverage-window end at detection | New record only when a *new* missing period appears; an unchanged known gap re-detected is a fingerprint no-op |
| `stale` | Series ref | **transition edge** `fresh→stale` or `stale→expired` at detection boundary | Recorded only on state transition, not on every observation; recovery to fresh closes the episode (next stale episode = new detection boundary = new fingerprint) |
| `verification_mismatch` | Verification record id | first-detection edge | Once per record per mismatch transition |

**Rule 4 — Actor and lineage.** Every W-1/W-2 write records actor
(operator id), mode, correlation ID in the BE-1 audit event; W-2 additionally
appends lineage. Exceptions discovered by W-1 carry the refresh run's
correlation ID, joining scan → exceptions → audit into one traceable episode.

**Closure mapping:** every BE-2 write now has an explicit owner (W-1/W-2
actor), purpose, audit/lineage path, deduplication rule, and a named test
(H.1: pure-GET repetition test, fingerprint-dedup test per exception type,
stale-transition episode test, W-1 idempotent re-run test, W-2 re-verify
no-change no-op test).

## D.1 No-Future-Data Model

- Global rule: no served or verification-scoped datum may have `open_time >
  server-now (UTC)`; violation → refuse + `future_data` exception record.
- `as_of` queries: rows with `open_time <= as_of` only — reuses the
  as-of/no-look-ahead discipline established in W3-U04.
- Verification-record `as_of` is immutable; re-verification recomputes over
  rows with `open_time <= as_of` only (bounded-scope guarantee; per Part E.1
  this is tamper-evidence, not reproducibility).

## D.2 Integrity Validators (`integrity.py`) and Quarantine Behavior

| Check | Rule | On violation |
|---|---|---|
| Chronological ordering | Bars strictly increasing `open_time` per series | `out_of_order` exception; offending row refused from reads |
| Duplicates | UNIQUE natural key honored; duplicate candidate | `duplicate` exception; first-write wins; duplicate refused |
| Gaps | Missing expected periods per timeframe grid (session-aware; simulator = 24×7 grid) | `gap` exception recorded; data still served with `availability=partial` + gap list — gaps are disclosed, never filled silently |
| Staleness | `now − last_open_time` > timeframe budget (configurable per timeframe) | `freshness=stale/expired` on responses; exception recorded on transition |
| Timezone | Naive or non-UTC datetimes | `temporal_violation`; refused (BE-1 `require_utc()`) |
| Future data | D.1 | `future_data`; refused |
| Unmapped symbol | B.5 | `unmapped_symbol`; refused |

Quarantine = append-only `v2_md_integrity_exception` row + BE-1 audit event
(`v2.marketdata` domain) + exclusion of the offending rows from result sets,
with `availability=quarantined/partial` honestly disclosed. No destructive
cleanup: V1 rows are never modified or deleted.

## D.3 Audit and Lineage Integration

- Sensitive reads (`verification/all`) audited (BE-1 pattern).
- Verification-record creation (W-2) appends a BE-1 **lineage record**:
  artifact_type `md_asof_verification`, sources = contributing source_ids +
  series refs, operator, mode — making every record traceable end-to-end.
- Integrity exceptions carry `correlation_id` for join with audit trail.

---

# Part E — As-Of Verification Records and V1 Coexistence

## E.1 As-Of Verification Record Semantics (`verification.py`) — REWRITTEN per V2-BE2-PLAN-001 (Option B)

**Truth statement (binding on all BE-2 claims, APIs, docs, and tests):**

> The BE-2 artifact is an **As-Of Verification Record** — a tamper-evidence
> reference, **not a snapshot**. It cannot reconstruct or replay the original
> rows if the underlying V1 `candles` store changes. BE-2 provides **no
> reproducible historical snapshot capability.** True immutable
> snapshot-member/payload storage is explicitly deferred to a later authorized
> band.

Artifact definition (`v2_md_asof_verification`, renamed from `v2_md_snapshot`):

- `scope`: list of (instrument_id, timeframe, source_id) + bounded time window
- `as_of`: immutable UTC bound; no row with `open_time > as_of` participates
- `content_hash`: SHA-256 over the ordered natural keys + OHLCV of every row
  in scope at creation time — deterministic and recomputable
- `row_count`, `source_ids`, `mode`, `created_by_operator_id`
- Append-only + dialect triggers; versioning = new record, never edit
- Operator-scoped visibility; admin `read_all` audited

**What it guarantees:** later re-verification (Part D.0 W-2) recomputes the
hash over the same scope/as-of; a mismatch **proves** the underlying data
changed since the record was created (tamper-evidence, drift detection,
research-input attestation).

**What it does NOT guarantee (stated in the API response contract itself):**
reconstruction of the original rows. The detail response carries a fixed
field `reconstructive: false` and `capability: "verification-only"` so no
consumer can mistake it for a replayable snapshot.

Lineage: creation appends a BE-1 lineage record with artifact_type
`md_asof_verification` (not `md_snapshot`), preserving traceability without
overclaiming.

Naming rule: the token "snapshot" is removed from all BE-2 table, module,
API, permission, contract, and documentation names. `SnapshotDescriptor` in
B.3 is renamed `AsOfVerificationDescriptor`. The word may appear only in the
deferred-capability note above.

**Design decision D-2 (revised):** Option B accepted as the truthful minimal
model for BE-2. Rationale: an immutable member/payload copy (Option A) is a
material storage/architecture commitment better designed alongside real
provider data (BE-3+) and the research bands that consume it; BE-2 keeps the
integrity value (tamper-evidence) without a reproducibility claim it cannot
honor. Risk BE2-R-01 is updated accordingly (Part H.2): the residual risk is
now *limited detection scope* (mutation is detected, not prevented or
recoverable), and reproducible-snapshot capability is registered as an
explicit deferred capability, not silent debt.

## E.2 V1 Simulator Adapter Coexistence (`v1_adapter.py`)

- Read-only mapping layer: V1 `candles.source` markers → registered BE-2
  sources (`sim.local`, `seed.local`); rows with unrecognized markers surface
  as `authority=unknown` (disclosed, not guessed).
- The V1 live service keeps writing exactly as today; BE-2 never writes bars.
- Deterministic simulator regression: existing V1 market tests remain green;
  new BE-2 tests assert the boundary labels simulator output `live:simulated`
  and seed backfill `seed:synthetic` on real rows.
- No migration of V1 data; no dual-run cutover needed (read-boundary only).

---

# Part F — Security Design (Document 17)

## F.1 SAL Classification and Ownership Matrix

| Asset | SAL | Owner | Default visibility | Sensitive-read audit | Retention |
|---|---|---|---|---|---|
| `v2_md_instrument`, `v2_md_symbol_map`, `v2_md_source` | SAL-2 (reference data) | DA-maintained seed under governance | All authenticated V2 readers | No | Governance-record preservation; changes only via future governed migration |
| `v2_md_series` | SAL-2 | Market-data service (W-1 writer) | All authenticated V2 readers | No | Recomputable catalog; retained while series exists |
| `v2_md_integrity_exception` | SAL-3 | Market-data service (Operator = data owner) | Mode+operator-scoped | Via correlation joins | Min. 24 months then archival review (pending-policy state recorded; no indefinite silent retention) |
| `v2_md_asof_verification` | SAL-3 | Creating operator (admin `read_all` = SAL-4 exception) | Operator-scoped | Yes (`read_all`) | Attestation hold: retain while any referencing research artifact exists; review cadence 12 months |
| Bar payloads | SAL-2 (simulated/synthetic only in BE-2) | V1 platform (unchanged) | Per V1 + V2 read permission | No | V1 policy (unchanged) |

## F.2 Controls

- **Default deny:** both new permissions explicitly granted; unknown roles get
  nothing (BE-1 RBAC reused).
- **Secret/data minimization:** market data contains no credentials by design;
  `detail` JSON on exception records passes BE-1 redaction before storage;
  the BE-1 secret-write refusal applies to all audit events BE-2 emits;
  no secret-bearing configuration is introduced (no provider keys exist in
  BE-2 at all — strongest possible control: absence).
- **Mode isolation:** every read path passes the BE-1 mode dependency;
  records carry `mode`; Paper/Live vocabulary cannot enter (guard).
- **Deployment-owned controls** (encryption at rest, TLS, backup, monitoring):
  classified assumptions per OBS-V2-BE1-02; owner = deployment; BE-2 evidence
  makes no infrastructure-control claim.

## F.3 Threat Model (STRIDE-condensed)

| Threat | Vector | Control | Test |
|---|---|---|---|
| Data-authority spoofing (simulated shown as live) | Response construction | Mandatory provenance block; reserved-vocabulary guard; display-contract constants | API test asserts label on every data response; guard raises on `historical:imported` construction |
| Tampering with history | UPDATE/DELETE on verification/exception tables | DB triggers both dialects | Mutation-refusal tests (SQLite + PostgreSQL) |
| Verification-record repudiation | Untraceable record origin | Lineage record + operator attribution + audit | Lineage-linkage integration test |
| Information disclosure | Cross-operator verification-record reads | Operator scoping at query level; admin read_all SAL-4 + audited | Two-operator API isolation tests |
| Future-data injection / look-ahead | Crafted `as_of` or future rows | D.1 guards server-side | Failure-path tests with future timestamps |
| Mode elevation | Header/query/body mode injection | `AXIOM_V2_MODE` only (BE-1) | Injection-refusal API test |
| DoS via unbounded queries | Huge window/series requests | `limit` caps + bounded window validation | Boundary tests |

---

# Part G — Migration/Drift Containment and PostgreSQL Plan

1. **Drift gate (BE-1 rule, unchanged):** post-upgrade `alembic check` may
   contain only the documented inherited V1 drift baseline. Any `v2_md_*`
   or other V2 operation in the diff is a blocking defect. Programmatic
   assertion included in the migration-lifecycle test (BE-1 pattern).
2. **SQLite (DA workspace):** fresh-DB upgrade → tables/triggers/seeds →
   mutation refusal → drift gate → downgrade removal → re-upgrade, with
   literal captured output.
3. **PostgreSQL (Operator environment — mandatory per OBS-V2-BE1-03):** BE-2
   changes migration/models/metadata, so a full fresh dedicated non-production
   PostgreSQL verification is required exit evidence: upgrade to
   `20260824_0039`, `v2_md_*` table/trigger/function existence, native
   UPDATE/DELETE refusal output (also closing the PG-002 §4 residual pattern
   for the new tables), drift comparison (V1 baseline only), downgrade to
   `20260823_0038`, trigger/function absence after downgrade, re-upgrade.
   DA supplies an updated command pack; Operator executes; evidence returns
   through the review channel.
4. Rollback/containment: single additive migration; clean downgrade; no V1
   object touched; feature is dark (no frontend consumer) so rollback is
   schema-only.

---

# Part H — Evidence Model, Risks, Debt, and Delivery

## H.1 Test/Evidence Model

| Layer | Coverage (non-duplicating accounting; distinct file/case counts reported) |
|---|---|
| Unit | Contracts/vocabulary guards; identity rules; normalization (incl. rejection paths); every integrity validator (positive + violation); verification-hash determinism; exception fingerprint determinism; seed-manifest hash check; reserved/active-authority guards |
| Integration (real DB/API, BE-1 style) | Migration lifecycle + triggers + seeds + drift gate; bars endpoint returns provenance on real V1 rows; simulator regression labelling; gap/stale/future/duplicate paths producing deduplicated exception records + honest availability; **pure-GET repetition test (N identical reads → zero mutations)**; W-1 idempotent re-run; fingerprint-dedup per exception type; stale-transition episode semantics; W-2 create→re-verify hash-match and mismatch-transition paths; verification two-operator isolation + admin read_all + sensitive-read audit; DB-seed-matches-manifest test; active-authority emission guard; permission default-deny + generic denial; mode injection refusal; empty/degraded/error envelope states |
| Security | Threat-model table F.3 mapped 1:1 to named tests |
| Regression | Full V1 suite (552) + BE-1 V2 suite (78) unmodified and green |
| Failure-path | Unregistered source, unmapped symbol, naive datetime, future `as_of`, oversized window, quarantined series |

Exit evidence package: Delivery Report; plain-text source transcript with
SHA-256 for **every changed file regardless of change class** (REM-001 process
correction); literal SQLite command outputs; Operator PostgreSQL rerun
evidence; updated V2 Current State/Risk/Debt/Capability registers.

## H.2 New Risks

| ID | Risk | Severity | Mitigation |
|---|---|---|---|
| BE2-R-01 | V1 `candles` mutability limits BE-2 to tamper-detection (mutation is detected, not prevented or recoverable); no reproducible-snapshot capability exists in BE-2 | Medium | Truthful Option B scoping (E.1); hash re-verification detects drift; reproducible snapshot storage registered as an explicit deferred capability for a later authorized band |
| BE2-R-02 | Provenance vocabulary drift in future bands | Medium | Reserved-vocabulary guard + display-contract constants under governance |
| BE2-R-03 | Series catalog divergence from underlying store | Low | Catalog is recomputable; verification job contract defined (execution of scheduled jobs deferred to BE-7 job band) |
| BE2-R-04 | Over-engineering toward BE-3 providers | Low | Neutral-contract-only rule; ITRGA review criterion §5 respected; tick/depth/event contract-only |

## H.3 Anticipated Debt

| Item | Class | Disposition |
|---|---|---|
| Reproducible historical snapshot storage (immutable member/payload copy) | Deliberate deferral (PLAN-001 Option B) | Explicitly deferred to a later authorized band; BE-2 provides tamper-evidence only |
| Tick/depth/event contracts without storage | Deliberate deferral | Documented; storage requires future band authorization |
| Session calendars beyond 24×7 simulator grid | Deferral | Real session/venue calendars belong with real providers (BE-3) |
| Scheduled freshness/catalog verification job | Deferral | Job execution framework is BE-7 scope; BE-2 computes on read |

## H.4 Open Decisions for ITRGA

1. **D-1 confirmation:** wrap-V1-store approach vs. duplicated V2 bar storage
   (DA recommends wrap; rationale B.2). D-2 is resolved by PLAN-001 Option B
   adoption (verification-record model, E.1).
2. Retention numbers in F.1 (24/12-month review cadences) — proposed values,
   adjustable by determination.
3. Whether `GET /series/.../bars` should additionally require a per-series
   result cap in configuration (DA proposes fixed server-side cap, no config).

## H.5 Plan Summary

BE-2 delivers a provider-neutral market-data contract, truthful provenance for
all existing simulated/synthetic data (active vocabulary strictly
`seed:synthetic` / `live:simulated` / honest `unknown`), enforceable
historical integrity with honest degraded states, deduplicated audited
exception records behind an explicit two-writer boundary, and tamper-evident
(non-reconstructive) as-of verification records — six additive tables, one
migration, persistence-pure GETs plus two idempotent audited POST writers,
zero V1 mutation, zero provider surface, zero real-data claim — fully under
BE-1's mode, RBAC, audit, lineage, temporal, and error primitives.

**We don't guess. We prove.**

**End of BE-2 Design Plan v1.0.0**
