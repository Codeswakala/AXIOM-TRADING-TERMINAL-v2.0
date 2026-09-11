# AXIOM V2 BE-3 — Authorized Provider Adapters and Market Data Operations Design Plan

| Field | Value |
|---|---|
| Document ID | AXIOM-V2-BE-3-DA-PLAN-001 |
| Version | 3.1.0 (delivery-cycle corrections for ITRGA-REV-V2-BE-3-P1-DELIVERY-001, DEL-001/DEL-002) |
| Status | **RESUBMITTED FOR ITRGA REVIEW** — not implementation authorization |
| Date | 2026-08-24 |
| Author | Development Authority (DA) |
| Responds to | ITRGA-REQ-V2-BE-3-001; ITRGA-REV-V2-BE-3-001; ITRGA-REV-V2-BE-3-002 |
| Provider candidate | **Twelve Data** — Operator-selected 2026-08-24; status: **ARCHITECTURE CANDIDATE** (no account, no credential, no contract, no external call exists or is authorized by this plan) |
| Governing context | Active V1 hierarchy; V2 Charter; Document 17; BE-2 final determination ITRGA-DET-V2-BE-2-001 (incl. OBS-01…05); V2 Backend Roadmap Band BE-3 |

---

# Revision 2.0.0 — Finding Closure Map

| Finding | Correction applied | Where |
|---|---|---|
| V2-BE3-PLAN-001 (technical network deny) | New **Part A.4a P1 Network-Deny Policy**: no HTTP/WS transport constructed or invokable; `FixtureTransport` is the only transport type in P1; hard `network_enabled=False` constant validated at import; any live-transport invocation raises an audited safe refusal; tests prove no outbound call occurs even with an env key present | A.4a (new), G threat table, H.3 |
| V2-BE3-PLAN-002 (P2 = separate Build Order) | P2 removed from BE-3 implementation scope entirely: **P1 ends at fixture-only architecture candidate; P2 requires a separate DA design plan, ITRGA review, and Build Order** after an Operator provider-account/entitlement decision. No P1 code path can call, consume a key, or promote status | A.4, A.5, C.3, F.3 |
| V2-BE3-PLAN-003 (unverified commercial data) | All plan/tier/rate-limit/coverage/cost figures reclassified `unverified candidate documentation`; removed from runtime policy and seeds; P1 resilience tests use **synthetic policy fixtures labelled `synthetic:test-policy`**, never provider numbers | B.1, E.2, C.3 seeds |
| V2-BE3-PLAN-004 (custody + status mutation) | "Committed fixtures" → **workspace-reviewed static fixtures** (repository artifacts only via Operator post-approval custody); P1 seeds exactly one read-only `architecture_candidate` record; **no transition writer exists in P1** — ladder mutation is deferred to the future P2+ scope; status APIs read-only | C.3, H.1, H.2 |
| ITRGA decisions §3 (1–4) | Recorded as binding: P2 separate BO; reserved authority inactive-only pending Amendment Register + future BO; vault revisit mandatory in the P2 plan; no WebSocket in P1 | A.4, D.1, E.1, H.4 |

## Revision 3.0.0 additions (ITRGA-REV-V2-BE-3-002)

| Finding | Correction applied | Where |
|---|---|---|
| V2-BE3-PLAN-005 (credential resolver reads env) | P1 uses **`FixtureCredentialResolver` only** — always returns explicit `absent`; **never reads `AXIOM_TD_API_KEY` or any provider secret env var**; env-backed resolver preserved solely as P2 design pseudocode; test proves the placeholder env var is NOT read | D.1 (rewritten), A.4a §5 |
| V2-BE3-PLAN-006 (resilience persistence conflict) | **Recommended option adopted**: P1 resilience is pure in-memory fixture logic — no persisted outage/status transition, no `source_outage` exception type, no BE-2 schema extension, no audit rows from breaker transitions; persisted provider health/transition events deferred wholly to P2+ | E.2 (corrected), H.1 |
| V2-BE3-PLAN-007 (wording) | All P1 text normalized: `unverified provider candidate documentation`; `workspace-reviewed static fixtures`; `P2-only credential/rotation design`; free-tier phrasing removed from selection rationale | A.3, C.1, D.1, G |

---

# Part A — Authority, Scope, Provider Status, and Truthfulness Boundary

## A.1 Source Authorities

1. `00_VISION_AND_PRINCIPLES.md` — data honesty; no unverifiable claims
2. `03_AXIOM_SPEC.md` — market-agnostic architecture; governance before automation
3. `17_INSTITUTIONAL_SECURITY_STANDARD.md` — SAL, credentials, least privilege, zero trust
4. V2 Charter invariants — provider/broker secrets isolated; no fabricated state; unknown is allowed
5. BE-2 approved foundations — canonical instruments, source registry, provenance taxonomy, integrity validators, W-1/W-2 write boundary, verification records
6. ITRGA-REQ-V2-BE-3-001 — required contents and mandatory exclusions
7. BE-2 carried observations OBS-V2-BE2-01…05 (esp. 04 credential hygiene, 05 PostgreSQL revalidation)

## A.2 BE-3 Objective

Design (and, only under a future Build Order, implement) **one** external
market-data provider adapter — Twelve Data — behind the BE-2 provider-neutral
contract, such that:

- simulated/synthetic data can never be represented as real, and provider
  data can never be represented as anything but its verified entitlement;
- no secret can enter source, frontend, logs, evidence, or assistant context;
- provider failure degrades safely into the BE-2 honest-state vocabulary;
- provider maturity is tracked through the roadmap's hard-gate ladder and
  never overstated.

## A.3 Provider Selection Record (required content #1)

| Item | Value |
|---|---|
| Selected candidate | Twelve Data (twelvedata.com) |
| Selection authority | Operator decision, 2026-08-24 (relayed in-session; to be countersigned in the BE-3 Build Order or an Operator decision record) |
| Selection rationale | Multi-asset coverage (forex/crypto/stocks/indices/ETFs) matching AXIOM's market-agnostic mandate and the existing seeded instrument universe (forex majors + BTC/ETH/SOL + XAUUSD), per **unverified provider candidate documentation**; apparent availability of a low-commitment evaluation tier and an API-key auth model are likewise unverified candidate observations to be confirmed by the Operator in the future P2 entitlement step — nothing here asserts confirmed provider capability |
| Current status | **ARCHITECTURE CANDIDATE** — nothing beyond public documentation has been consulted; no account exists; no network call has been made or will be made under this plan |
| Alternatives recorded | Polygon.io (strong US equities/options; weaker FX-first fit), Binance public data (credential-free but crypto-only), OANDA v20 (forex-only) — retained in this record for future re-evaluation; switching candidates requires only a revised §A.3 + ITRGA re-review, since the adapter contract (Part C) is provider-neutral |

## A.4 In-Scope (design now; implementation only under BO-V2-BE-3-001)

**BE-3 implementation scope is P1 ONLY** (per ITRGA-REV-V2-BE-3-001 decision
§3.1). P1 is credential-free, network-free, fixture-only:

1. `backend/app/v2/marketdata/providers/` bounded package: provider contract,
   Twelve Data adapter skeleton, response-fixture normalizer, contract-test
   harness driven entirely by **workspace-reviewed static fixtures** (derived
   from public documentation examples — no live call; fixtures become
   repository artifacts only through Operator post-approval custody);
2. provider registry with exactly **one read-only seeded
   `architecture_candidate` record** and read-only status APIs (no transition
   writer exists in P1 — see C.3);
3. symbol-mapping extensions for Twelve Data symbology (e.g. `EUR/USD`,
   `BTC/USD`) → canonical instrument ids, seeded/versioned per BE-2 C.4 rules;
4. credential-resolver **interface only** returning honest absence (no secret
   value, no consumption path — the P1 adapter cannot use a key even if one
   exists in the environment; A.4a);
5. rate-limit/retry/backoff/circuit-breaker/outage state machine as pure
   logic, tested exclusively against **synthetic policy fixtures** labelled
   `synthetic:test-policy` (no provider figures — PLAN-003);
6. reconciliation and quality gates mapped onto BE-2 integrity validators;
7. one additive migration; tests; audit/lineage; documentation/registers.

**Phase P2 — NOT part of BE-3 implementation.** The first provider account,
credential, entitlement verification, external network call, live contract
test, status promotion, and any provenance activation each require, in
sequence: an Operator provider-account/entitlement decision → a **separate DA
design plan** (including the mandatory credential/vault revisit per ITRGA
decision §3.3) → **ITRGA review** → a **separate Build Order**. Nothing in a
P1 Build Order authorizes or optionally enables any P2 activity.

## A.4a P1 Network-Deny Policy (V2-BE3-PLAN-001 closure — technically enforced)

The fixture-only boundary is enforced by code and tests, not by DA statement
or credential absence:

1. **No transport exists.** The P1 package constructs no HTTP or WebSocket
   client anywhere: no `httpx.Client/AsyncClient`, no `aiohttp`, no raw
   sockets. The adapter's only transport type is `FixtureTransport`, which
   reads static files and cannot be parameterized with a URL or host.
2. **Hard constant, validated at import.** `providers/contract.py` defines
   `P1_NETWORK_ENABLED: Final[bool] = False`. `ProviderAdapter.__init__`
   asserts the transport is a `FixtureTransport`; constructing the adapter
   with any other transport raises `V2Error(VALIDATION_FAILED)` with a
   **security-log-only refusal** (`provider.network_refused`).
   **Accountability model (DEL-002, revised control):** these refusals fire
   in programmatic contexts with no authenticated actor/session/correlation
   (no P1 API surface reaches them), so a BE-1 audit event — which requires
   an actor and DB session — cannot be truthfully appended; a synthetic
   actor would violate the no-fabricated-state invariant. The control is a
   structured SECURITY log line (action name only) + safe V2Error, tested by
   caplog assertion. Any future authorized scope exposing these paths behind
   an authenticated surface must upgrade the refusal to a full audit event
   in its own Build Order.
3. **Live-invocation refusal.** The contract exposes
   `fetch_live(*_, **__)`-class entry points only as explicit refusal stubs:
   any invocation raises the audited refusal above. There is no code path
   from any API endpoint to a network operation.
4. **URL builder inert.** The single URL-builder function exists for P2
   design continuity but returns a `PlannedRequest` value object (host
   allowlist `api.twelvedata.com`, redacted rendering); nothing in P1 accepts
   a `PlannedRequest` for execution.
5. **Tests prove the deny holds even when a key variable exists.** The P1
   test suite sets `AXIOM_TD_API_KEY=TD_TEST_KEY_PLACEHOLDER` in-process
   solely to prove **P1 does not read it** (PLAN-005): (a) adapter
   construction with a non-fixture transport refuses and audits; (b)
   live-entry invocation refuses and audits; (c) a socket-guard fixture
   (monkeypatched `socket.socket`/`getaddrinfo` failing the test on any
   outbound attempt) passes across the entire P1 provider suite; (d) the
   `FixtureCredentialResolver` returns `absent` regardless of the variable,
   and an env-access guard (patched `os.environ`/`os.getenv` recorder)
   asserts no provider-secret variable name is ever queried by P1 code;
   (e) the placeholder value appears in no log/audit/response capture
   (leak-hunt).
6. **Static assertion.** A test greps the providers package for forbidden
   transport imports (`httpx`, `aiohttp`, `websockets`, `socket`) so a future
   edit cannot silently introduce one without failing Level-II evidence.

## A.5 Mandatory Exclusions (mirrors ITRGA-REQ-V2-BE-3-001 §3)

- No live trading or provider-to-broker coupling; no Paper/Live, broker,
  exchange, account, order, position, fill, execution, reconciliation-to-
  account capability
- No provider account creation, credential, vendor contract, or actual
  external network call under BE-3 at all — these belong exclusively to the
  future separately planned/reviewed/ordered P2 scope (PLAN-002)
- No external AI/assistant integration; no frontend implementation
- No unlicensed data, no fabricated provider status, no claim of integration
  that has not been evidenced
- No representation of provider data as available until entitlement is
  verified; no representation of simulated data as real (BE-2 guards remain)
- No DA Git/GitHub operations

## A.6 V1/BE-1/BE-2 Compatibility

| Element | BE-3 effect |
|---|---|
| V1 candles/services/adapters/APIs | Untouched |
| BE-2 tables/APIs/guards | Untouched in behavior; extended additively (new provider table; new seeded mapping rows via governed seed-change process C.4) |
| Active provenance vocabulary | **Unchanged in P1.** Provider data emission requires activating a new authority value (Part E) via an explicit `V2_AMENDMENT_REGISTER.md` entry — planned as part of the P2 promotion decision, exactly as BE-2's PLAN-003 correction requires |
| BE-1 primitives | Reused unchanged (mode, RBAC factory, audit, lineage, temporal, errors) |

---

# Part B — Legal / Licensing / Entitlement Boundary (required content #2)

## B.1 Assessment Framework

Because no contract exists, this section defines the **verification checklist
that must be completed and evidenced before P2**, not conclusions:

| Item | Verification required before any live call |
|---|---|
| Terms of service acceptance | Operator (account owner) accepts ToS; record retained by Operator |
| Plan/tier entitlement | ALL tier/limit/coverage/cost figures are **unverified candidate documentation** in P1 (PLAN-003): recorded only in this plan's research notes, NOT seeded, NOT runtime policy, NOT displayed as provider fact. Verified entitlement data enters the registry only in the future P2 scope from Operator-supplied evidence |
| Data-use rights | Internal research/display use verified against ToS; **redistribution assumed PROHIBITED until proven otherwise** — the API will never expose provider payloads to any surface beyond the authenticated research terminal |
| Retention rights | Whether provider bars may be persisted (historical store) vs display-only; until verified, BE-3 P1 persists **no provider payload data at all** — the adapter normalizes to BE-2 contracts in memory for contract tests against fixtures only |
| Attribution requirements | Captured into the display contract if required |
| Credential terms | Per-seat/per-app key usage rules recorded |

## B.2 Enforcement Design

- The provider registry row carries `entitlement_status`:
  `unverified | verified:<tier> | expired | revoked` — default `unverified`.
- The adapter refuses activation while `entitlement_status = unverified`
  (server-side check, audited refusal — same pattern as BE-1 gate refusals).
- Data-retention flag `persistence_permitted: false` until legally verified;
  while false, any code path attempting provider-bar persistence raises
  `V2Error(VALIDATION_FAILED)` (tested).

---

# Part C — Provider-Neutral Adapter Contract (required contents #3, #5, #6)

## C.1 Contract (maps 1:1 onto BE-2 canonical contracts)

```text
backend/app/v2/marketdata/providers/
├── contract.py       # ProviderAdapter protocol + capability descriptor
├── status.py         # source-status ladder + transition guards
├── twelvedata/
│   ├── adapter.py    # TwelveDataAdapter(ProviderAdapter) — P1: fixture-fed
│   ├── normalize.py  # TD JSON → BE-2 BarContract/QuoteContract (pure)
│   ├── symbols.py    # TD symbology ↔ canonical instrument_id mapping rules
│   └── fixtures/     # workspace-reviewed static documentation-derived
│                     # samples (repository artifacts only via Operator
│                     # post-approval custody)
├── resilience.py     # rate-limit/retry/backoff/circuit-breaker state machine
└── health.py         # source-health model (latency/freshness/outage states)
```

`ProviderAdapter` protocol (contract-level, provider-neutral):

- `descriptor() -> ProviderDescriptor` (id, markets, capabilities, entitlement status, source status)
- `fetch_bars(instrument_id, timeframe, window) -> list[BarContract]` — P1: fixtures only
- `fetch_quote(instrument_id) -> QuoteContract` — P1: fixtures only
- `health() -> SourceHealth`
- No streaming in BE-3 P1/P2 scope (WebSocket deferred to a later order —
  bounded-scope discipline)

Every returned contract carries mandatory BE-2 provenance; the adapter cannot
construct provenance directly — it must request it from the provenance module,
which enforces the active-vocabulary guard (Part E).

## C.2 Symbol Mapping and Reference Governance (required content #5)

- Twelve Data symbology (`EUR/USD`, `BTC/USD`, `XAU/USD`) mapped to canonical
  ids via new seeded `v2_md_symbol_map` rows (`source_id = "twelvedata"`),
  added through the BE-2 C.4 governed seed process: new migration, updated
  `SEED_MANIFEST_HASH`, Delivery-Report hash delta.
- Exact-match only; unmapped symbols → `unmapped_symbol` exception (existing
  fingerprint dedup); never auto-registered.
- Initial mapping scope: exactly the existing 12-instrument canonical
  universe. Instrument-universe expansion is a separate governed seed change.

## C.3 Source-Status Ladder (required content #6, roadmap hard gate)

New table `v2_md_provider` (registry) with the ladder vocabulary:

```text
architecture_candidate → contract_tested → integrated
        → authorized:<environment> → production_certified
```

**P1 mutation boundary (PLAN-004; hardened per DEL-001):** P1 seeds exactly
**one read-only `architecture_candidate` record** for Twelve Data and exposes
**read-only** status APIs. The registry row itself is **database-immutable**:
UPDATE/DELETE triggers on `v2_md_provider` (both dialects) refuse any change
to status/entitlement/persistence fields — a future transition design must
ship its own governed migration to alter these guards. **No transition writer, promotion, or demotion path exists in
P1** — the ladder columns and (append-only, trigger-protected) status-history
table are created by the migration for schema stability, but the history
holds only the single seeded genesis row and no code can append to it.
Transition writing — always evidence-gated with a recorded authority
(Build Order / determination / Operator decision id) — is deferred entirely
to the future P2+ Build Order. The status endpoint never derives status from
code existence: the adapter existing keeps status `architecture_candidate`
(the roadmap's explicit hard gate), and in P1 nothing can change it.

---

# Part D — Credential / Vault / Rotation / Isolation Design (required content #4)

## D.1 Custody Model (Document 17 Part V/VIII; OBS-V2-BE2-04 lesson)

- **No secret in source, fixtures, tests, logs, audit details, evidence,
  chat, or assistant context — ever.** The BE-1 redaction pack already
  covers `api[_-]key` patterns; a Twelve Data-specific pattern
  (`apikey=<value>` query form) is added to the redaction rules and tested.
- **P1 resolver: `FixtureCredentialResolver` only (PLAN-005).** It always
  returns an explicit `CredentialState.ABSENT` and **contains no code path
  that reads `AXIOM_TD_API_KEY` or any provider secret environment
  variable** — a real Operator key can never enter P1 process memory, under
  any environment configuration. Tests prove non-reading via an env-access
  guard even with a placeholder variable set (A.4a §5).
- The environment/vault-backed resolver
  (`get("twelvedata") → vault/env → key`) is preserved **only as P2 design
  pseudocode** in this document — it is not executable P1 code and will be
  authoritatively specified in the future P2 design plan, where the full
  credential/vault design revisit is mandatory (ITRGA decision §3.3) before
  any Operator key is used.
- The key is Operator-provisioned in the Operator environment only; the DA
  workspace never holds a real value (tests use `TD_TEST_KEY_PLACEHOLDER`).
- URL construction: Twelve Data authenticates via `apikey` query parameter —
  the adapter builds URLs through one function that (a) never logs the full
  URL, (b) emits a redacted form (`apikey=[REDACTED]`) to any diagnostic
  surface, (c) is covered by a leak-hunt test grepping captured logs/audit
  rows for the placeholder value.
- Rotation: **P2-only credential/rotation design** — the rotation
  procedure, resolver re-read semantics, and storage rules belong to the
  future P2 plan. P1 has no credential to rotate. (Vault-service deferral
  remains recorded; it is a P2-plan decision, not a P1 behavior.)
- Evidence hygiene (OBS-V2-BE2-04): the P2 evidence template pre-redacts
  connection strings/keys; the Delivery Report checklist includes an
  explicit no-secret sweep step.

## D.2 Isolation

- Credential access is confined to the adapter module; no API response,
  Pydantic model, audit detail, or exception message can carry it
  (write-time secret refusal from BE-1 R-9.4 already rejects key-bearing
  audit payloads — regression-tested against the TD pattern).
- Frontend/browser can never reach the provider: all provider access is
  server-side behind the BE-2 read boundary (Charter invariant 4).

---

# Part E — Provenance, Failure, and Degraded-State Model (required content #7)

## E.1 Provenance Extension (governed, not silent)

- New authority value `live:provider:twelvedata` and kind `provider` are
  **defined as reserved vocabulary** in BE-3 P1 (schema CHECK extended;
  emission guard NOT extended — the value remains unemittable, exactly like
  `historical:imported`).
- **Activation** (adding it to `ACTIVE_AUTHORITY_VALUES` + display label
  `LIVE — TWELVE DATA (DELAYED per entitlement)`) happens only at the
  `integrated` promotion, via an explicit `V2_AMENDMENT_REGISTER.md` entry
  naming the affected rule (V1/BE-2 active-vocabulary boundary), authorized
  in the promoting Build Order. This is the same discipline ITRGA imposed in
  BE-2 PLAN-003/DEL-001, applied proactively.
- Provider data and simulated data can therefore never blur: distinct source
  rows, distinct authority values, mandatory display labels, DB CHECK +
  emission guard at both ends.

## E.2 Resilience State Machine (pure logic, fixture-tested in P1)

| Concern | Design |
|---|---|
| Rate limits | Token-bucket parameterized by a policy object. **P1 uses only synthetic policy fixtures labelled `synthetic:test-policy`** (e.g. 5 req/min purely as a test constant — explicitly NOT a provider figure, PLAN-003); pre-emptive refusal with `DATA_UNAVAILABLE`-class honest state when exhausted; never silent queuing beyond a bounded window. Verified provider limits enter policy only in P2 from Operator-supplied entitlement evidence |
| Retry/backoff | Idempotent GETs only; max 3 attempts; exponential backoff with jitter (1s/2s/4s base); retry only on transport/5xx/429-with-Retry-After; never on 4xx entitlement errors |
| Circuit breaker | CLOSED → OPEN after N consecutive failures (synthetic test-policy thresholds); OPEN emits `availability=unavailable` + `freshness=unknown` immediately (no hammering); HALF_OPEN probe after a synthetic interval. **P1 boundary (PLAN-006, recommended option adopted): the breaker is pure in-memory fixture logic — its transitions are NOT persisted, NOT audited, and introduce NO new exception type or BE-2 schema change.** Persisted provider-health/outage events (including any `source_outage` vocabulary, its schema, ownership, idempotency, and audit design) are wholly deferred to the future P2/provider-operations scope |
| Outage/disconnect | Source health surface: `healthy | degraded | outage | unknown`; BE-2 read-time freshness continues to govern staleness honestly |
| Latency/freshness | Per-request latency recorded into health (rolling window, in-memory); provider `as_of` mapped into provenance; delayed-data entitlement surfaced in the display label |
| Degraded truthfulness | Every degraded state maps onto the BE-2 vocabulary (`stale/expired/unavailable/unknown`); no cached value is served as fresh; cache TTL bounded by timeframe budget |

## E.3 Temporal Integrity (required content #8)

- All provider timestamps normalized to aware-UTC at the adapter boundary
  (`require_utc` on exchange-timezone-converted values; TD returns exchange
  or UTC timestamps per endpoint — normalization is fixture-tested per case).
- No-future-data rule enforced on every normalized bar (BE-2 validator reused);
  violating rows quarantined with existing fingerprint semantics.
- Historical requests are as-of-bounded; BE-2 As-Of Verification Records work
  unchanged over any future provider-persisted series (none in P1).
- Snapshot/version: provider responses carry no version — the adapter stamps
  `input_snapshot_id = sha256(request-params + response-body)` on lineage
  for contract-test reproducibility.

---

# Part F — Data Quality, Reconciliation, and Contract Testing (required content #9)

## F.1 Quality Gates (reuse BE-2 validators; provider-specific additions)

- Ordering/duplicate/gap/stale/future checks run on every normalized batch.
- Provider-specific: OHLC sanity (`low ≤ open,close ≤ high`), non-negative
  volume, precision-vs-instrument check, symbol-echo verification (response
  symbol must map back to the requested canonical id — misdelivery refusal).
- **P1 boundary (consistent with PLAN-006):** validators run inside the
  fixture contract-test harness **in memory only** — P1 persists no
  integrity exception from fixture runs (fixture data is test input, not
  platform data). The persisted, fingerprint-deduplicated exception path
  (`series_ref = instrument:timeframe:twelvedata`, owner = invoking actor,
  BE-2 semantics) is the specified design for live provider batches and
  activates only in the future P2+ scope.

## F.2 Reconciliation (design; live execution is P2+)

- Cross-source comparison harness: provider bars vs existing simulated series
  are **never merged**; reconciliation compares distributions/ranges only to
  detect gross misdelivery (e.g., wrong-symbol data), producing research
  artifacts, not corrections.
- Contract-test reconciliation: fixture responses normalized twice must be
  byte-identical (determinism gate).

## F.3 Contract-Test Plan

**P1 (workspace static fixtures, no network):** every documented response shape for
`time_series` (bars) and `quote` endpoints, plus documented error shapes
(401 invalid key, 429 rate limit, empty symbol, malformed JSON, partial
batch) — normalizer + resilience machine fully covered without network.

**P2 (future separate scope — design plan + ITRGA review + Build Order
required; NOT executable under BE-3):** the concept is recorded for
continuity only — a scripted command pack (BE-2 PostgreSQL-pack pattern)
executing a bounded call set in the Operator environment with the Operator's
key; literal pre-redacted transcripts through the review channel; promotion
`architecture_candidate → contract_tested` with evidence attached to the
transition row. All of it is specified authoritatively in the future P2
design plan, not here.

---

# Part G — Security Design Under Document 17 (required content #10)

| Asset | SAL | Owner | Controls |
|---|---|---|---|
| Provider API key | **SAL-4** | Operator | **Does not exist in P1** — no account, no key, and P1 code cannot read provider-secret env vars (FixtureCredentialResolver + env-access guard test). Redaction patterns for the TD key form are still added defensively + leak-hunt test. Residence/rotation/vault design is P2-plan scope |
| `v2_md_provider` registry/status history | SAL-3 | Governance record (Operator data owner) | Append-only + triggers; status transitions carry authority references; read API authenticated; mutation only via governed promotion path |
| Provider entitlement data | SAL-2 | Operator | Registry JSON; no secrets |
| Contract-test fixtures | SAL-1/2 | DA under governance | Static, documentation-derived, secret-free (checked by leak-hunt test) |
| Provider payloads (P2 transient) | SAL-2 | — | Not persisted in BE-3 (B.2 `persistence_permitted=false`); in-memory normalization only |

Threat model (delta over BE-2's):

| Threat | Control | Test |
|---|---|---|
| Secret leakage (source/log/audit/evidence) | D.1 chain; redaction extension; write-time audit refusal; leak-hunt test | Unit + integration + evidence checklist |
| Simulated-as-real / real-as-simulated blending | Distinct sources + reserved authority + dual guards (E.1); no merge paths | API emission tests |
| Fabricated provider status | Ladder transitions require recorded authority; API reads ladder only | Status API test + trigger immutability |
| Entitlement bypass | `entitlement_status` gate refuses activation; audited refusal | Refusal test |
| Provider outage cascading | Circuit breaker + honest degraded states; no retry storms | State-machine tests (all transitions) |
| SSRF/URL manipulation | Single URL builder, fixed base host allowlist (`api.twelvedata.com`), no caller-supplied URLs | Unit test |
| Response poisoning (wrong symbol/future data/absurd values) | Symbol-echo check, no-future rule, OHLC sanity, quarantine | Fixture failure-path tests |
| RBAC | New read permissions (`v2.marketdata.provider.read`) + admin status-history read; default deny; vocabulary guard passes | Default-deny tests |

Logging/redaction: provider interactions log method/endpoint-class/latency/
status only — never full URLs, never payload bodies at INFO, never keys.
Retention: registry/status history follows the BE-2 governance-record
retention pattern; transient payloads not retained (P1/P2).
Encryption/transmission: HTTPS-only enforced by the URL builder;
at-rest/TLS-termination remain deployment-owned (OBS-V2-BE2-02 unchanged).

---

# Part H — Schema/Migration, Evidence Model, File Scope, Risks, Delivery (required contents #11, #12)

## H.1 Schema (one additive migration `20260824_0040_v2_be3_provider`)

| Table | Purpose | Mutability |
|---|---|---|
| `v2_md_provider` | Provider registry: id, display name, markets JSON, entitlement JSON, `entitlement_status`, `persistence_permitted` (default false), current `source_status`, created_at | Status/entitlement changes via governed transition writer only |
| `v2_md_provider_status_history` | Append-only ladder transitions: provider_id, from_status, to_status, authority_ref (BO/determination/decision id), evidence_ref, operator_id, created_at | **Append-only + triggers (both dialects); P1 contains only the seeded genesis row — no application write path exists (PLAN-004)** |

Plus: `v2_md_source` CHECK extension to admit reserved `provider` kind /
`live:provider:twelvedata` authority (inactive-only — the BE-2
`ck_v2_md_source_active_authority` gains the same treatment: active rows
remain restricted to the current approved set); new seeded symbol-map rows;
new permissions (`v2.marketdata.provider.read` operator+admin;
`v2.marketdata.provider.read_history` admin SAL-4). Downgrade drops BE-3
objects cleanly to `20260824_0039`.

Drift gate: unchanged BE-2 rule — post-upgrade `alembic check` may contain
only inherited V1 drift; any `v2_md_provider*` operation is a blocking defect.

**PostgreSQL (OBS-V2-BE2-05):** migration/models/metadata change → full fresh
Operator PostgreSQL rerun is mandatory BE-3 exit evidence; command pack will
include the new CHECK refusals and status-history trigger tests; evidence
template pre-redacts credentials (OBS-V2-BE2-04).

## H.2 File Scope (implementation tranche P1)

New: `app/v2/marketdata/providers/**` (≈8 modules + fixtures),
`app/db/models/v2_provider.py`, migration `20260824_0040`,
`tests/test_v2_provider.py` (unit), `tests/test_v2_provider_integration.py`.
Modified: `app/db/models/__init__.py` (metadata imports),
`app/v2/rbac/permissions.py`/`dependencies.py` (new permissions),
`app/v2/marketdata/api/router.py` + new `api/providers.py` (status read API),
`app/v2/audit/redaction.py` (TD key pattern), BE-2 seed module (mapping rows,
new manifest hash). No V1 file touched.

## H.3 Evidence Model / Acceptance Criteria

| Gate | Evidence |
|---|---|
| No secret anywhere | Leak-hunt test output; redaction unit tests; evidence checklist sweep |
| **Network deny + credential non-access (P1)** | Socket-guard suite pass; non-fixture-transport construction refusal (audited); live-entry refusal (audited); forbidden-import static assertion; **env-access guard proving no provider-secret variable is ever queried**; `FixtureCredentialResolver` returns `absent` regardless of environment; leak-hunt on placeholder value — all with a placeholder env variable present |
| Status ladder truthful | API returns `architecture_candidate` with adapter present; **no mutation path exists** (P1); trigger immutability on the history table |
| Entitlement gate | Activation refusal while `unverified` (audited) |
| Contract tests | Full fixture suite green (success + all failure shapes); determinism gate |
| Resilience | State-machine transition matrix fully tested (rate-limit refusal, backoff schedule, breaker OPEN/HALF_OPEN/CLOSED, outage honesty) |
| Provenance safety | Reserved authority unemittable (guard + CHECK, both dialects); no merge path test |
| Migration | SQLite + Operator PostgreSQL lifecycle (upgrade/tables/triggers/CHECKs/refusals/drift/downgrade/re-upgrade) |
| Regression | Full suite green (V1 552 + BE-1 78 + BE-2 45 + new BE-3 set, distinct accounting) |
| Delivery | DR + full literal source transcript (REM-001 policy) + evidence annex + registers/state updates |

## H.4 Risks and Debt

| ID | Item | Class | Disposition |
|---|---|---|---|
| BE3-R-01 | Entitlement/data-rights/limit data entirely unverified until Operator account exists | Risk (contained in P1) | PLAN-003 treatment: unverified data excluded from seeds/policy/display; P1 uses synthetic test policies; live calls structurally impossible (A.4a) |
| BE3-R-02 | Fixture drift vs actual API behavior | Risk (Medium) | P2 contract test is the promotion gate; fixtures marked documentation-derived |
| BE3-R-03 | Credential/vault service design deferred | Debt (scoped) | P1 holds no credential at all; full credential/vault design revisit is a mandatory element of the future P2 plan (ITRGA decision §3.3) |
| BE3-R-04 | WebSocket/streaming excluded | Deferral | Separate future order |
| BE3-R-05 | Provider-payload persistence excluded pending data-rights verification | Deferral | `persistence_permitted` gate; future governed change |

## H.5 Open Decisions — RESOLVED by ITRGA-REV-V2-BE-3-001 §3

1. P1/P2 split: **P2 requires a separate design plan, ITRGA review, and Build
   Order** (binding; incorporated throughout this revision).
2. Reserved provider authority: approved as inactive/unemittable P1 vocabulary
   only; activation requires a future V2 Amendment Register entry AND a future
   Build Order.
3. Vault deferral: acceptable for P1 (no key/network); **credential/vault
   design revisit is mandatory in the P2 plan** before any Operator key use.
4. Streaming deferral: approved; no WebSocket transport in P1.

## H.6 Delivery Report Structure

Identity (BO, plan, baseline, provider status) · scope delivered/excluded ·
constraint compliance table · file inventory + SHA-256 manifest · verification
(distinct test accounting; fixture-suite results; migration lifecycle;
PostgreSQL disposition) · secret-sweep declaration · known limitations ·
handover (status ladder state, P2 prerequisites, next authorization).

---

**Truthfulness summary:** after BE-3 (P1), AXIOM will contain a fully
tested Twelve Data adapter that has never spoken to Twelve Data and
**structurally cannot** (no transport exists; socket-guard-proven), reports
itself as exactly what it is (`architecture_candidate`, immutable in P1),
cannot emit provider authority vocabulary, cannot hold or use a secret, and
carries no unverified provider figure in any seed, policy, or display — and
the platform's existing simulated/synthetic data remains labelled exactly as
it is today.

**We don't guess. We prove.**

**End of BE-3 Design Plan v1.0.0**
