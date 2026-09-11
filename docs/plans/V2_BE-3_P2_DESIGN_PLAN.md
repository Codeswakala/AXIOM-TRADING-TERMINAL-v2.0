# AXIOM V2 BE-3 P2 — Provider Candidate Evaluation Design Plan

| Field | Value |
|---|---|
| Document ID | AXIOM-V2-BE-3-P2-DA-PLAN-001 |
| Version | 3.0.0 (corrections for ITRGA-REV-V2-BE-3-P2-PLAN-002, findings PLAN-005…008) |
| Status | **RESUBMITTED FOR ITRGA REVIEW** — design only; not implementation authorization |
| Date | 2026-08-25 |
| Author | Development Authority (DA) |
| Responds to | ITRGA-REQ-V2-BE-3-P2-PLAN-001; ITRGA-REV-V2-BE-3-P2-PLAN-001; ITRGA-REV-V2-BE-3-P2-PLAN-002 |
| Predecessor | BE-3 P1 — ITRGA-DET-V2-BE-3-P1-FINAL-001 (APPROVED WITH OBSERVATIONS; Operator accepted) |
| Provider candidate | Twelve Data — `architecture_candidate · unverified · persistence_permitted=false` (locked P1 state) |
| Operator account decision | **None exists.** This plan designs the gate; it does not assume its outcome |
| Preparation declaration | No account, credential, env read, DNS/socket/HTTP/WS activity, provider payload, persistence, status change, or implementation occurred while producing this plan (§L) |

---

# Revision 2.0.0 — Finding Closure Map

| Finding | Correction | Where |
|---|---|---|
| PLAN-001 (raw-body retention = payload persistence) | **Preferred bounded model adopted**: raw bodies exist only transiently in process memory for schema validation + hash computation, discarded before any persistence; ALL retention provisions removed (incl. Operator-environment/encrypted forms); evidence schema enumerates the only allowed non-payload artifacts | E.3, E.5 (rewritten), F, H retention row, J, K |
| PLAN-002 (pre-authorized promotion migration) | Promotion migration **removed from requested P2 authorities**; explicit non-goal added: a successful P2 does not change provider status; promotion requires Operator review of the final determination → separate transition design plan → ITRGA review → separate transition Build Order → fresh PostgreSQL evidence | A.2, I.2, L.1, L.2, L.3 |
| PLAN-003 (proof claim exceeds sample) | **Full-universe option adopted**: live symbol-validation matrix expanded to all 12 mappings within a revised ≤35-call budget, so the A.1 claim and E.1 matrix use identical scope language | A.1, E.1, L.1 |
| PLAN-004 (CLI audit ambiguity) | **Option 1 adopted**: authenticated admin-authorized API endpoint ONLY; unauthenticated/local direct CLI path forbidden; audit-failure behavior defined (audit append failure aborts the run) | G (rewritten), J |

## Revision 3.0.0 additions (ITRGA-REV-V2-BE-3-P2-PLAN-002; PLAN-001…004 confirmed closed)

| Finding | Correction | Where |
|---|---|---|
| PLAN-005 (impossible audit atomicity) | Atomicity claim removed; **durable pre-call audit gate** adopted: `call_started` persisted BEFORE any network call (no durable start = no call); `call_completed` attempted after; completion-audit failure → stop all further calls + independent fail-safe incident channel + reconciliation before resumption; call states `completed / refused-before-call / indeterminate-after-start` defined and reported | G (rewritten), J, L.1 |
| PLAN-006 (unenforced call budget) | **Run-scoped server-side attempt-budget token mechanism**: initialized at 35; debited before EVERY network attempt incl. auth probes and retries; atomic refusal at zero; attempt number + remaining budget recorded in evidence; boundary tests prove retries cannot exceed the cap | E.1a (new), G, J, L.1 |
| PLAN-007 (dialect parity for guard lifecycle) | Entitlement migration defined **per dialect**: PostgreSQL trigger/function AND SQLite trigger drop → update → re-create, ordering preserving the immutable-state contract; SQLite lifecycle + mutation-refusal tests required alongside the fresh PostgreSQL verification; per-dialect migration/test matrix added | B.3, I.2, J, L.1 |
| PLAN-008 (footer version) | Footer corrected to the current version; version consistency rule adopted (footer auto-checked against header before submission) | Footer |

---

# Part A — Purpose and Bounded Decision Question (required content #1)

## A.1 What a future P2 contract test would prove

P2 answers exactly one bounded question:

> **Does the real Twelve Data API, under a verified Operator entitlement,
> behave compatibly with the P1 fixture-derived adapter contract — request
> shapes, response schemas, error taxonomy, symbol semantics, and temporal
> semantics — within a minimal, controlled, evidence-captured call budget?**

A successful P2 would prove, with Level-I/II evidence:

1. authentication succeeds under the Operator's verified entitlement;
2. the documented response shapes match the P1 normalizer's expectations
   (or the deltas are enumerated and fixture corrections are identified);
3. documented error shapes (auth failure, rate limit, bad symbol) occur as
   modeled;
4. symbol mapping resolves for **all 12 canonical instruments — each
   individually exercised by a live request in the E.1 matrix** (claim scope
   identical to tested scope);
5. timestamps normalize to aware-UTC without violating the no-future rule;
6. the resilience state machine's assumptions (retryable classes,
   Retry-After presence) match observed behavior.

## A.2 What P2 would NOT prove

- Not data quality/completeness/latency fitness for research use (that is a
  later operational-evaluation scope);
- not commercial viability, licensing sufficiency for persistence, or
  redistribution rights beyond what the Operator's entitlement evidence
  states;
- not production readiness, SAL certification, or deployment security;
- not any Paper/Live/broker/execution capability;
- not a basis for ANY status change: **a successful P2 contract test does
  not itself change provider status.** Any future promotion to
  `contract_tested` requires: Operator review of the final P2 determination
  → separate DA transition design plan → ITRGA review → separate transition
  Build Order → implementation with fresh PostgreSQL evidence. P2 neither
  performs nor pre-authorizes that transition.

# Part B — Account/Entitlement Gate (required content #2)

## B.1 Hard gate

**No P2 implementation may start until the Operator makes a separate,
recorded account/entitlement decision** (`AXIOM-V2-OD-xxx`) covering: account
creation, tier selection, ToS acceptance, and supply of reviewable
entitlement evidence (plan page/receipt/tier description, pre-redacted).

## B.2 Evidence rule (mirrors ITRGA §6 posture)

Every commercial/coverage/price/limit/licensing/data-rights item remains
**NOT PROVEN** until Operator-provided reviewable evidence exists. NOT PROVEN
values: (a) never enter runtime policy, seeds, API responses, or product
state; (b) appear in the plan/implementation only as `unverified candidate
documentation`; (c) convert to verified values only via the entitlement
registry update in the P2 migration, sourced from the evidence document
referenced by ID.

## B.3 Registry effect (design)

On verified entitlement, a P2-scoped governed migration updates
`v2_md_provider`: `entitlement` JSON = verified values + evidence reference;
`entitlement_status` = `verified`. Because the P1 registry is
**DB-immutable**, the migration temporarily drops and re-creates the guard —
**per dialect, with identical post-state (PLAN-007)**:

| Step | PostgreSQL | SQLite |
|---|---|---|
| 1. Drop guard | `DROP TRIGGER v2_md_provider_immutable` (function retained) | `DROP TRIGGER v2_md_provider_immutable_update` + `_delete` |
| 2. Update row | entitlement JSON + `entitlement_status='verified'` | identical |
| 3. Re-create guard | `CREATE TRIGGER … EXECUTE FUNCTION prevent_v2_md_provider_mutation()` | re-create both SQLite triggers |
| Transaction note | Single transactional DDL+DML migration | SQLite DDL is effectively per-statement; the migration is ordered so the guard is never absent outside the migration run, and the post-state is verified by tests |

Post-migration invariant (both dialects): registry immutable again, with
UPDATE/DELETE refusal re-proven by direct mutation tests. SQLite lifecycle
(upgrade → refusal matrix → downgrade restoring `unverified` + prior guard →
re-upgrade) is DA-workspace test evidence; PostgreSQL lifecycle remains
Operator-run fresh verification. No application write path is created.

# Part C — Credential Architecture (required content #3; mandatory vault revisit per ITRGA decision §3.3)

## C.1 Custody chain

- **Owner:** Operator. **Residence:** Operator environment only, supplied at
  process start via a single environment variable (name defined in the P2
  Build Order; this plan deliberately does not operationalize it) or an
  optional file-based secret mount (`*_FILE` convention) for
  container/CI use.
- **Vault decision (revisit conclusion):** a dedicated vault service remains
  **not justified** for one key/one provider. Instead P2 specifies a
  `SecretBackend` interface with two implementations: `EnvSecretBackend`
  (P2 initial) and `FileSecretBackend`; a future multi-provider band can add
  a vault backend without contract change. Rationale: minimal necessary
  change; the isolation properties come from the access rules below, not
  from storage technology.

## C.2 Access isolation

- Exactly **one** module (`providers/credentials.py`, P2-new) may resolve
  the secret; an import-boundary test asserts no other module imports the
  backend; the resolved value lives only in adapter-request scope, never in
  module/global state, never in a dataclass repr (`repr=False`), never
  serialized.
- **No frontend/source/log/evidence exposure:** the existing redaction
  patterns (incl. `apikey=`) apply to every log/audit sink; the leak-hunt
  test extends to P2 transcripts; evidence templates are pre-redacted
  (OBS-V2-BE2-04 discipline); the P1 rule that no API response model carries
  credential fields continues.
- **Test-safe absence:** with no secret configured, resolution returns the
  explicit `absent` state → adapter reports honest
  `availability=unavailable`, never an error trace naming the variable, and
  the P1 `FixtureCredentialResolver` remains the default for all non-P2 test
  runs.

## C.3 Rotation / revocation

Rotation = Operator replaces the env/file value and restarts the process
(re-read at start; no caching beyond process life). Revocation = Operator
revokes the key at the provider **and** removes it from the environment;
the incident path (§K) covers suspected exposure. No key material is ever
written to disk, database, or evidence by AXIOM.

# Part D — Network Authorization Boundary (required content #4)

## D.1 Enablement preconditions (ALL required, checked at runtime)

```text
1. P2 Build Order exists and is referenced in configuration
   (AXIOM_TD_P2_AUTHORITY_REF = "BO-V2-BE-3-P2-001"; exact-match check)
2. entitlement_status == 'verified' in v2_md_provider
3. Secret resolves (present, non-placeholder)
4. Explicit enablement flag set for the verification session
   (AXIOM_TD_CONTRACT_TEST_ENABLED=true; default false)
5. Mode is RESEARCH or SIMULATION (BE-1 dependency)
```

Failing any precondition → **audited refusal** (full BE-1 audit event — P2
paths run inside an authenticated operator-invoked context, §G) and honest
`unavailable`. Default state of the system is therefore **deny**.

## D.2 Transport policy

- Single `NetworkTransport` implementation constructed only by the P2
  contract-test runner; nowhere else in the codebase may construct it
  (import-boundary + constructor-site test).
- **Fixed host allowlist:** exactly `api.twelvedata.com`; the `PlannedRequest`
  builder remains the only URL source; any other host → refusal.
- HTTPS only; TLS verification always on (no insecure flag exists);
  connect/read timeouts fixed (5s/15s); no redirects followed off-host;
  no WebSocket/streaming transport in P2 at all.
- DNS/socket use occurs only inside the transport for the allowlisted host;
  the P1 socket-guard remains active for every non-P2 test suite.
- Egress control note: OS/container-level egress restriction to the
  allowlisted host is a deployment-owned control (recorded as an Operator
  runbook item, not claimed as an application control).

# Part E — Contract-Test Scope (required content #5)

## E.1 Minimal request classes (bounded call budget ≤ 35 calls/run)

| Class | Requests | Proves |
|---|---|---|
| AUTH | 1 valid-key probe; 1 deliberately-absent-key probe | Auth acceptance + documented 401 shape |
| BARS-DEEP | `time_series` for 3 representative instruments (fx major, crypto, metal), 1 timeframe (M1), small `outputsize` | Full response-schema validation vs P1 normalizer; OHLC/volume presence; ordering |
| SYMBOL-SWEEP | 1 minimal `time_series` request (smallest `outputsize`) for **each of the remaining 9 canonical instruments** | Live symbol resolution + echo verification for the complete 12-instrument universe (with BARS-DEEP) — matching the A.1 claim exactly |
| QUOTE | 1 quote request | Quote shape |
| SYMBOLS-NEG | 1 unknown-symbol request | Documented error/empty shape; unmapped refusal path |
| LIMITS | Observed opportunistically (Retry-After/headers on any 429) — **no deliberate limit-exhaustion runs** | Rate-limit shape if encountered |

Budget arithmetic: 2 + 3 + 9 + 1 + 1 = 16 planned calls; the ≤35 cap leaves
bounded headroom for per-call retry classes without permitting sweeps.

## E.1a Attempt-Budget Enforcement (PLAN-006 — executable control, not policy)

The 35-attempt cap is enforced by a **run-scoped, server-side token budget**:

```text
AttemptBudget(max_attempts=35)          # constructed once per run, server-side
  .debit() -> attempt_number | REFUSED  # called BEFORE every network attempt
```

Rules:
1. **Every** network attempt debits first — planned calls, authentication
   probes (valid and absent-key), and every retry of any class. There are no
   exempt attempt types.
2. Debit is atomic within the single-threaded runner; when zero tokens
   remain, the next debit returns REFUSED and **no further network call of
   any kind occurs** for the rest of the run (hard stop, honest
   `budget_exhausted` abort recorded).
3. The attempt number and remaining budget are recorded in each permitted
   audit/evidence record (E.5 schema gains `attempt_number` and
   `budget_remaining` integer fields — non-payload, non-secret).
4. Retries acquire budget identically: a retry that cannot debit is not
   made; the call is reported with its last known state.
5. Boundary tests (J): budget-exhaustion refusal at exactly 35; retry storms
   cannot exceed the cap (mock transport forcing max retries on every call
   still terminates ≤35 attempts); auth probes count; post-exhaustion
   attempt is refused without any transport construction.

Attempt-accounting table (planned):

| Class | Planned calls | Max retries each | Worst-case attempts |
|---|---|---|---|
| AUTH | 2 | 0 (auth outcomes are terminal) | 2 |
| BARS-DEEP | 3 | 3 | 12 |
| SYMBOL-SWEEP | 9 | 1 | 18 |
| QUOTE | 1 | 2 | 3 |
| SYMBOLS-NEG | 1 | 0 (expected error is terminal) | 1 |
| Worst-case total | 16 | — | **36 → bounded to 35 by the token gate** (the final attempt is refused; reported honestly) |

## E.2 Expected response/error categories

Success schemas (meta/values, quote), error schemas (401 auth, 404/400 bad
symbol, 429 with/without Retry-After), transport failures (timeout, TLS,
DNS) — each mapped to the P1 normalizer/resilience handling; any observed
shape not in the P1 model is recorded as a **fixture delta finding**, not
silently adapted.

## E.3 Schema/version, symbol, temporal semantics

- Deterministic evidence = request parameters + **cryptographic hash of the
  transient in-memory response body** (`input_snapshot_id` discipline from
  BE-2); the body itself is discarded from memory after validation/hashing
  and is never persisted (E.5). Provider version/plan indicator FIELD VALUES
  (short strings, not bodies) may be captured, redacted of any
  account-revealing identifier.
- Symbol semantics: only the 12 seeded mappings queried; echo-verification
  refusal (P1 rule) applies to live responses identically.
- Temporal semantics: every timestamp normalized to aware-UTC at the
  boundary; no-future-data check on every bar; timezone metadata captured
  when the provider supplies exchange-local times.

## E.4 Entitlement/authentication refusal behavior

401/403 responses must produce: honest `unavailable` state, an audited
refusal event, zero retries (non-retryable class), and no secret echo in any
captured output.

## E.5 Deterministic evidence capture — NO payload persistence (PLAN-001)

**Binding model (preferred bounded P2 model from the review):** raw provider
response bodies exist **only transiently in process memory**, solely for
schema validation and hash computation, and are discarded before any
transcript, audit, file, or database write occurs. **No provider payload
body — raw, partial, encrypted, compressed, or otherwise — is persisted
anywhere in P2, including the Operator environment.** ITRGA verification
relies on the recorded hashes and schema verdicts; if a future need for body
inspection arises, it must be separately proposed as a data-rights/retention
scope with explicit Operator authorization and governance review — it cannot
be implied by a spot-check request.

**Evidence schema (exhaustive — the ONLY artifacts the runner may persist):**

```text
per-call record:
  request_class        (AUTH | BARS-DEEP | SYMBOL-SWEEP | QUOTE | SYMBOLS-NEG | LIMITS)
  instrument_id        (canonical id or null)
  redacted_request     (PlannedRequest.redacted() form; apikey=[REDACTED])
  response_status      (HTTP status class + code)
  body_sha256          (hash of transient body; body itself discarded)
  schema_verdict       (pass | delta-finding ref | error-shape ref)
  error_category       (auth | symbol | rate-limit | transport | none)
  attempt_number       (PLAN-006: budget debit sequence number)
  budget_remaining     (PLAN-006: tokens left after debit)
  call_state           (completed | refused-before-call | indeterminate-after-start)
  latency_ms
  timestamp_utc
run record:
  correlation_id, authority_ref, precondition snapshot (booleans),
  per-class pass/fail counts, delta-finding list, abort reason (if any)
```

A leak-hunt over the produced transcript (no secret, no body fragments —
verified by asserting transcript size bounds and schema-only fields) is part
of the run's own evidence.

# Part F — Data/Provenance Boundary (required content #6)

- **No active provider authority in P2.** `live:provider:twelvedata` remains
  reserved/unemittable; activation stays a separate future Amendment
  Register entry + Build Order (unchanged from P1 approvals).
- **No persistence of provider payloads — absolute in P2 (PLAN-001).**
  `persistence_permitted` remains `false`; raw bodies are transient
  process-memory values discarded after validation/hashing; **no retention
  path exists in any environment, Operator's included, encrypted or
  otherwise.** Only the E.5 evidence-schema artifacts (hashes, verdicts,
  statuses, latencies) are persisted. This plan explicitly does NOT propose
  ingestion; approved market-data ingestion would be a later band with its
  own data-rights evidence.
- Provider data can therefore never reach the BE-2 read boundary, candles
  store, or any API response in P2.

# Part G — Audit/Accountability Design (required content #7)

P2 contract testing runs as an **authenticated, operator-invoked** action —
unlike the P1 actor-less construction paths — so full BE-1 audit applies:

| Event | When | Audit content |
|---|---|---|
| `provider.contract_test.start` | Run start | actor (admin operator), correlation ID, authority_ref (P2 BO), enablement precondition snapshot (booleans only), budget max |
| `provider.contract_test.call_started` | **Durably persisted BEFORE each network call** | actor, correlation, request class, instrument, redacted request, attempt number, budget remaining |
| `provider.contract_test.call_completed` | After response/failure | status class, latency, body hash, schema verdict, error category (non-payload fields only) |
| `provider.contract_test.refused` | Any precondition/budget refusal | failed gate name; safe generic detail |
| `provider.contract_test.complete` | Run end | per-class counts of `completed` / `refused-before-call` / `indeterminate-after-start`, delta findings, abort reason |

**Invocation surface (PLAN-004, option 1 adopted): an authenticated,
admin-authorized API endpoint ONLY** — `POST` under the V2 surface (exact
route fixed in the P2 BO), protected by new permission
`v2.marketdata.provider.contract_test` (admin, SAL-4, default-deny, generic
denial), with server-side authentication via the existing operator JWT
session, server-generated correlation ID, and normal BE-1 audit context.
**An unauthenticated or local direct CLI path is forbidden** — no code path
may reach the contract-test runner except through the authenticated
endpoint's dependency chain (import-boundary test in J).

**Audit-failure behavior (PLAN-005 — durable sequence, no atomicity claim):**
external network I/O cannot share a transaction with a database write, so
the design uses a **durable pre-call audit gate** instead:

1. `call_started` is persisted (committed) **before** the network call; if
   it cannot be durably written, **the network call is not made** — no
   un-attributed provider contact is possible.
2. After the response/failure, `call_completed` is attempted with the
   allowed non-payload fields.
3. If the completion audit fails, the runner **stops all further calls
   immediately**, raises a fail-safe incident record through an
   independently available channel (SECURITY log + process-exit marker file
   in the run's evidence directory — a channel that does not depend on the
   failed database path), and the run cannot resume until the durable
   `call_started` record is reconciled against provider-side reality by the
   Operator/ITRGA.
4. Timeout, cancellation, or process loss manifests as a `call_started`
   without `call_completed` and is reported as an **indeterminate** call —
   never silently treated as absent. Run completion criteria (L.1)
   distinguish `completed`, `refused-before-call`, and
   `indeterminate-after-start` attempts, and any indeterminate attempt
   requires reconciliation notes in the evidence.

Safe-error rules: BE-1 error contract; no stack traces; no secret or full
URL in any error path.

# Part H — SAL/Security Design (required content #8)

| Obligation | Design |
|---|---|
| Least privilege | New permission granted to admin only; single secret-resolver module; single transport constructor site |
| Administrative approval | Enablement requires the P2 BO reference in config + explicit session flag + verified entitlement (three independent administrative acts) |
| Secret management | Part C; SAL-4 asset; never persisted/logged/echoed; rotation/revocation defined |
| Encryption | TLS-only transport, verification always on; at-rest concerns n/a (no persistence) |
| Monitoring/alerting | Contract-test events are audited (queryable); circuit-breaker outage states surface honestly; production monitoring remains a deployment-owned prerequisite (OBS discipline) |
| Error handling | BE-1 safe-error contract on every path; 401/403 non-retryable; bounded timeouts |
| Retention | Evidence transcripts (E.5 schema artifacts only): governance-record retention (BE-2 pattern). **Raw provider bodies: never persisted — no retention provision exists (PLAN-001)** |
| Ownership | Secret: Operator. Evidence: governance record. Registry rows: governed migrations only |
| Threat model (delta) | Secret exfiltration via logs/evidence (redaction + leak-hunt + pre-redacted templates); host substitution/SSRF (fixed allowlist, no caller URLs); response poisoning (echo-verification, no-future, OHLC sanity); accidental enablement (three-factor precondition + default-deny); test-runner abuse (admin-only permission + audit) |

# Part I — State Machine and Database Implications (required content #9)

## I.1 P1 guards remain intact

This plan proposes **no change** to: P1 registry/history immutability
triggers, the absence of a transition writer, active-authority CHECKs, or
any BE-1/BE-2 guard. The P1 socket-guard test regime remains for all
non-P2-runner suites.

## I.2 Separately governed transitions (PLAN-002 corrected)

**Exactly ONE registry mutation is in P2 scope**, as an explicit migration
operation (never an application write):

1. **Entitlement verification:** migration records verified entitlement
   (§B.3) — dialect-aware drop guard → update row → re-create guard, with
   before/after evidence, contingent on future Operator entitlement
   evidence and approval. **Per-dialect verification (PLAN-007):** SQLite
   migration lifecycle + direct mutation-refusal tests in the DA workspace
   AND fresh Operator PostgreSQL lifecycle/trigger/function/refusal/
   downgrade/re-upgrade evidence (OBS-V2-BE2-05 / P1 OBS 3), pre-redacted
   output. The migration/test matrix in §J covers both dialects.

**Status promotion is OUT of P2 scope entirely:**

```text
A successful P2 contract test does not itself change provider status.
Any future promotion to contract_tested requires:
Operator review of the final P2 determination
→ separate DA transition design plan
→ ITRGA review
→ separate transition Build Order
→ implementation and fresh PostgreSQL evidence.
```

No P2 implementation migration may append a post-test history row or change
`source_status`. The P1 no-transition-writer constraint remains binding
throughout and after P2.

# Part J — Test/Evidence Matrix (required content #10)

| Level | Evidence |
|---|---|
| **Level I** (direct runtime) | Operator-environment contract-test transcript (redacted): per-call statuses, hashes, schema verdicts; precondition-refusal demonstrations; PostgreSQL migration lifecycle for any P2 migration |
| **Level II** (executed tests) | Pre-flight suite runnable WITHOUT network/secret: precondition default-deny matrix (each of the 5 preconditions independently absent → refusal + audit), import-boundary tests (secret module, transport constructor, **runner reachable only via the authenticated endpoint chain — PLAN-004**), identity/permission/correlation/audit-event tests for the endpoint (denial, attribution, server-generated correlation, **audit-append-failure → fail-closed abort**), redaction/leak-hunt extensions, **evidence-schema conformance test (transcript contains only E.5 fields; no body content)**, schema-validator unit tests against P1 fixtures, full V1/BE-1/BE-2/BE-3-P1 regression |
| **Level III** (documentation) | Provider candidate documentation (labeled unverified), Operator entitlement evidence (labeled verified-by-evidence-ID), this plan |
| Negative tests | Absent key, wrong-host planned request, disabled flag, unverified entitlement, unknown symbol, timeout injection (mocked transport), 401/429 fixture shapes; **PLAN-005 set:** start-audit failure → no call made; completion-audit failure → hard stop + incident channel + no next call; timeout/cancel → indeterminate reporting; **PLAN-006 set:** budget exhaustion at exactly 35, retry-storm bounded, auth probes debited, post-exhaustion refusal without transport construction; **PLAN-007 set:** SQLite entitlement-migration lifecycle + post-migration mutation-refusal matrix + downgrade restoration |
| **Abort/refusal criteria** | Any secret appearing in any captured output → immediate abort + incident path; any call outside the allowlist → abort; budget exceeded → abort; any unexplained schema delta affecting >1 request class → stop-and-report rather than adapt |

# Part K — Rollback / Revocation / Incident Design (required content #11)

- **Provider disablement:** clearing the enablement flag restores full P1
  deny posture instantly (no code change); removing the secret does the same
  independently.
- **Credential revocation:** Operator revokes at provider + removes from
  environment; DA never holds the value.
- **Suspected exposure incident:** abort runs → Operator revokes/rotates →
  security log + audit event recorded → incident note in risk register →
  evidence sweep re-run before any resubmission. (Sweep covers only E.5
  schema artifacts — no raw bodies exist anywhere to sweep.)
- **Rollback:** P2 migrations are additive/reversible (downgrade restores
  `unverified` entitlement and prior guard state); contract-test evidence is
  retained per §H; a failed P2 leaves the platform exactly in its P1
  approved state.

# Part L — Acceptance Criteria, Non-Goals, and Preparation Declaration (required content #12)

## L.1 Measurable gates for a future P2 Build Order

1. Operator account/entitlement decision recorded with reviewable evidence;
2. all §D.1 preconditions implemented with the default-deny matrix green;
3. pre-flight Level-II suite green with zero network/secret;
4. contract-test run within the token-enforced ≤35-attempt budget
   (attempt accounting complete: every attempt classified `completed`,
   `refused-before-call`, or `indeterminate-after-start`; zero
   unreconciled indeterminate attempts, or reconciliation notes attached),
   all request classes evidenced — including the SYMBOL-SWEEP covering all
   12 canonical instruments — zero secret leakage and zero body persistence
   (leak-hunt + evidence-schema check on transcripts); every network call
   preceded by a durable `call_started` audit record;
5. schema verdicts complete — pass, or deltas enumerated as findings;
6. audited events present for start/calls/refusals/completion;
7. per-dialect migration verification for any P2 migration: SQLite
   lifecycle + mutation-refusal tests AND Operator PostgreSQL verification
   (pre-redacted);
8. full regression green with distinct accounting.

## L.2 Non-goals (excluded from P2 entirely)

Provider data ingestion/persistence (including ANY raw-body retention, in
any environment, encrypted or otherwise); active provenance authority;
**any provider-status promotion or history append — P2 changes no status**;
WebSocket/streaming; additional providers;
Paper/Live/broker/execution/AI/frontend/production; any V1 change.

## L.3 Requested future authorities (explicit list)

If this plan is approved, the future P2 Build Order would need to authorize:
(a) the secret-resolver + network-transport modules under §C/§D constraints;
(b) the admin contract-test permission + authenticated API endpoint (§G);
(c) the entitlement-recording migration (contingent on Operator entitlement
evidence); (d) the Operator-environment contract-test run. **Nothing else —
expressly NOT any status promotion, transition migration, or history append
(PLAN-002).**

## L.4 Preparation declaration

During preparation of this plan the DA performed **no** account/credential
action, no provider-secret environment read, no DNS/socket/HTTP/WS/provider
network activity, no payload use/persistence, no authority activation, no
status/guard change, no transition writer, no P2 implementation or test
reaching a provider, and no Git/GitHub operation. All provider facts herein
remain unverified candidate documentation.

**We don't guess. We prove.**

**End of BE-3 P2 Design Plan v3.0.0**
