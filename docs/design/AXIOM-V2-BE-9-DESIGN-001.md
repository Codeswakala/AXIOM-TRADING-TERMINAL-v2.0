# AXIOM V2 BE-9 — BROKER/EXCHANGE CONNECTIVITY AND ACCOUNT VISIBILITY
# READ-FIRST, RECONCILIATION-FIRST DESIGN

| Field | Value |
|---|---|
| Document ID | AXIOM-V2-BE-9-DESIGN-001 |
| Version | 1.2.1 (C-1/C-2/C-3 per ITRGA-REV-V2-BE-9-DESIGN-001 + S1 re-cut and provision pin per ITRGA-DIR-V2-BE-9-S1-REDIRECT-001 final edition — change-note §16) |
| Date | 2026-09-05 |
| Author | Replacement Development Authority (DA) |
| Requested by | ITRGA-REQ-V2-BE-9-001 v1.0.0 (via Operator, 2026-09-05) |
| Roadmap contract | `V2_BACKEND_ROADMAP.md` §"Band BE-9 — Broker/Exchange Connectivity and Account Visibility" |
| Baseline | **Sealed head `20260904_0048`** (DB sha256 `1d4005fafe972a775822d93016aefbda87c194c6f579a351429f6b6b6a61dd3e`, ITRGA-V2-BE8-0048-CLO-SEAL-001) · suite 1,026/0 · triggers 58 · permissions 57 · compver 10 |
| Status | DESIGN DOCUMENT ONLY — zero-code rule in force; no code, no migration, no register edits beyond this entry |

**Standing discipline: we don't guess. We prove.** Every assumption is
marked `ASSUMPTION`; every reused precedent cited (§3 of the REQ); every
N-control and roadmap bullet mapped where satisfied; Q1–Q9 answered in
S13 with recommendation + rationale.

---

## §0 — Design thesis

BE-9 is the first band where AXIOM touches an external party's system, so
the posture is inverted from every prior band: **the broker is the
authority; AXIOM holds projections** (V2-R-10). The design lands one
sandbox-scoped provider behind a **read-only-at-type-level adapter
contract** (no mutation verb exists to call — N1 is a vocabulary fact,
not a policy), an **operator-passphrase-unlocked encrypted credential
vault** whose resolved secrets never cross the request boundary (N4,
BE-3 P2 credential-boundary law generalized), **append-only
provenance-pinned projection tables** disjoint from the sealed paper
domain by type, storage, and name (N3), and a **reconciliation +
discrepancy surface shipped in the same band** — reconciliation-first
means the mismatch machinery is exit evidence, not roadmap futures.
Deterministic sync runs under the BE-7 idempotency law: a re-run
reconciles identically or refuses typed. Nothing in this band can
express, route, or imply an order submission; the V1 `BrokerPort`
protocol (which carries `OrderIntent`) is explicitly NOT reused — a
new read-only contract is cut instead (S1.4).

---

## S1 — Broker selection & adapter contract

### S1.1 Candidate selection (Q1 — re-cut per ITRGA-DIR-V2-BE-9-S1-REDIRECT-001, O-1 resolved)

**Provider selection (Operator decision on record, 2026-09-05):
Exness**, substrate = a locally installed **MetaTrader 5 terminal** on
the operator console, credential = a dedicated **demo account with the
investor (read-only) password** set.

Residency facts and eliminations (the re-cut rationale):
- **OANDA v20**: unavailable in the operator's country — eliminated on
  residency (the v1.0.0 recommendation is void on fact, not on merit).
- **Exness (SELECTED)**: relationship already held; demo account
  provisioning intent affirmative; the **investor password is a
  provider-side structural read-only arm of N1** — the vaulted
  credential cannot submit, amend, or cancel anything AT THE BROKER
  (Exness Personal Area "Set Read-Only Access"; MT4/MT5
  investor-password standard flow). Strictly stronger than the v1.0.0
  posture: N1 now holds at the provider, not merely at our type level.
- **FXCM**: eliminated — contradictory residency posture + demo expiry.
- **MT5 cloud relays** (third-party hosted bridges): eliminated on
  **N4** — third-party credential custody is disqualifying, investor
  password notwithstanding.
- **cTrader / IBKR**: recorded runner-ups (cTrader: no held
  relationship, weaker local footing; IBKR: equities-shaped, heavier
  gateway stack for a single-console posture).

**PROVISION PIN (operator guidance 2026-09-05, DIR final edition):**
DEMO account, MetaTrader 5, **"Standard" type** (USD plumbing, no
commission field). Refused with reasons: **Standard Cent**
(cent-denominated balances pollute the money/reconciliation law —
S5's exact-compare Decimal law must not meet a 100× unit skew);
**Pro/Raw/Zero tiers** (needless commission/spread complexity for a
read-only band); **NO live account of any tier in this band**. Vault
credential = investor (read-only) password; sealed binding = exact
server hostname + account number + environment string.

**PROVISIONING STATUS (2026-09-05, operator on record — A-1 successor
DISCHARGED except the BO-time binding pins):**
- DEMO account **CREATED** (Standard, MT5).
- MT5 desktop connectivity probe on plain wifi **SUCCESSFUL** —
  baseline provider reachability proven outside the governed act
  (E-ENV-1 posture confirmed in the field).
- READ-ONLY ACCESS (investor password) **SET** on the demo —
  terminal-side per MT5 law (the Personal Area carries no toggle).
  **The N1 provider-side arm (a) HOLDS: the vault credential at BO is
  the investor password.**
- Remaining at BO: the binding pins only (server hostname + account
  number + environment string — operator-held until the BO/vault act).
- Optional, operator-side housekeeping, no governed act: a pre-BO
  sanity probe (MT5 desktop login with the investor credential on
  plain wifi).

The S1.4 contract binds regardless of provider (the review's own
condition) — the adapter remains the only file that changes on any
future redirect.

### S1.2 Capability matrix (read verbs only — the full vocabulary; MT5 substrate)

| Capability | MetaTrader5 Python surface (Windows-native, A-2 posture) | Read model fed |
|---|---|---|
| Account (documented singleton — the "list" verb returns exactly the one pinned account) | `account_info()` with the account-number pin | `v2_broker_account` |
| Balance/margin/currency | `account_info()` money fields | `v2_broker_balance` |
| Open positions | `positions_get()` | `v2_broker_position` |
| Open orders | `orders_get()` | `v2_broker_order` |
| Fills/transactions | `history_deals_get()` / `history_orders_get()` over DECLARED time windows | `v2_broker_fill` |
| Instruments + visibility/trade-mode facts | `symbols_get()` + `symbol_info()` | `v2_broker_instrument_permission` |

**There is no row for submission, amendment, or cancellation — the
capability matrix IS the closed vocabulary** (N1 type arm), and the
investor password makes the same statement AT THE BROKER (N1 provider
arm).

**Paging = time-window law (fills):** history fetched in declared
windows (`A-8`: 24h window size, 1h overlap, BO-settable); overlap
dedupes on the broker-assigned ticket/deal ids — the fill idempotency
anchors are unchanged (`transaction_ext_id` = MT5 deal ticket).
**Provenance blob per page pins:** provider id, **server hostname**,
account number, environment string, fetch basis (**server-time law**:
MT5 history calls are issued against terminal-reported server time;
local wall-clock recorded as a secondary fact, never the query basis),
and the window.

### S1.3 Error taxonomy → V2Error mapping (MT5 substrate; E-ENV-1 honored)

| Condition | Typed class (V2Error family) |
|---|---|
| **MT5 terminal unavailable / not connected** (process absent, not logged in, IPC init failure) | **`broker.terminal.unavailable`** — FIRST-CLASS per E-ENV-1; distinct from remote failure; pure fact, never improvised |
| Broker/server-side unreachable (terminal up, server down/rejecting) | `broker.unavailable` |
| Auth/investor-login invalid | `broker.auth.refused` (generic on the wire; NEVER echoes credential material — N4) |
| Unknown account/entity | `broker.entity.unknown` |
| Malformed/partial payload (`None` returns, truncated structs) | `broker.payload.invalid` (page discarded whole — S4.3) |
| Call timeout | `broker.timeout` |
| Fetch-budget ceiling hit | `broker.fetch_budget.exceeded` (S4 law) |

All surfaced through the BE-1 envelope; denial vocabulary generic
(no vault/credential terms — S8). Under `broker.terminal.unavailable`:
sync/reconcile fail typed, land NOTHING (the all-or-nothing law
covers it), and the fact goes to health (S7). **E-ENV-1 environmental
law recorded:** the operator's proxy regime defeats MT5 connectivity
even after MT5 proxy-setting tuning; plain-wifi is the working posture;
this design does NOT promise proxy traversal — proxy windows are a
sync-unavailable regime BY DESIGN; E1 evidence acts and sync runs are
documented as executed under compatible connectivity (plain wifi), with
a BO-time runbook note.

**Rate/time posture (local-terminal envelope):** no provider REST
headers exist; the token-bucket rule is replaced by a documented
**terminal-courtesy law** — sequential calls only, no parallel fan-out
in v1; the fetch-budget law (S4) is stated per-window.

### S1.4 The READ-ONLY adapter contract (N1 structural, type level)

New contract in `app/v2/broker_read/contract.py` — **the V1
`BrokerPort` protocol is NOT reused**: it carries `OrderIntent` and
capability description for future mutation; importing it would put a
mutation shape inside this band's type graph. Instead:

```
class BrokerReadContract(Protocol):        # closed six-verb vocabulary
    async def read_accounts(...) -> BrokerAccountsPage
    async def read_account_summary(...) -> BrokerSummaryPage
    async def read_positions(...) -> BrokerPositionsPage
    async def read_orders(...) -> BrokerOrdersPage
    async def read_transactions(...) -> BrokerTransactionsPage
    async def read_instrument_permissions(...) -> BrokerInstrumentsPage
```

- Every return type is a frozen dataclass page (BE-3 P2 pattern) with
  `provenance` (provider id, endpoint, fetched-at basis, page cursor)
  baked in.
- **No method named or shaped for mutation exists**; the boundary test
  walks the Protocol's members and asserts the six-name closed set —
  any seventh member fails the suite (the BE-8 API-census law applied
  to a type).
- Sealed instantiation (BE-4/5/6 provider-incident law): a frozen
  single-entry `MappingProxyType` registry `BROKER_READ_PROVIDERS =
  {"exness_mt5_demo": "app.v2.broker_read.providers.exness_mt5"}` — no
  registration function, no plugin path; the Q9-successor environment
  binding (below) lives beside it.
- **Q9 successor (binding; replaces the registry-literal-only rule per
  DIR §3.3):** the environment binding = **code-pinned server hostname
  + account number + environment string** in the sealed registry;
  **re-asserted at every vault unlock AND at every sync start**
  (mismatch = typed refusal + audit); pinned into every row's
  provenance. A config error cannot repoint reads because the binding
  is hash-pinned code, not config — three sites must agree: registry
  literal, unlock/sync assertion, row provenance.
- Pagination: time-window law for history (S1.2); windows size-capped
  by the fetch-budget law; sequential terminal-courtesy calls (no
  parallel fan-out in v1).
- Versioning posture: the adapter pins the MetaTrader5 package version
  + terminal build number in every provenance blob; a version change
  surfaces as a recorded fact, never a silent behavioral shift.

**N1 arms restated (DIR §3.6 — three independent layers):**
(a) **provider-side investor password** (NEW, strongest: the credential
itself cannot mutate at the broker); (b) type-level closed six-verb
vocabulary (existing; census-tested); (c) route census + import/token
scans (existing). Verbatim provider payloads in the order/instrument
tables remain subject to the payload-echo canary class (S2.4).

Roadmap bullets satisfied: *broker adapter contract* → S1.4; provider
selection → S1.1.

## S2 — Credential vault & scoped service identity

### S2.1 Storage scheme trade table (Q2)

| Option | At-rest protection | N4 blindness consequence | Verdict |
|---|---|---|---|
| Windows DPAPI (machine/user scope) | OS-bound; transparent to any process running as the user | Any same-user process (incl. the assistant's tooling, if ever local) could decrypt — blindness by convention only | REJECTED as sole layer |
| OS keychain (Credential Manager) | Same DPAPI root; enumerable by user-scope processes | Same weakness | REJECTED as sole layer |
| **Encrypted file + operator-held passphrase (recommended)** | AES-256-GCM over a scrypt/Argon2id-derived key; passphrase NEVER stored; file useless without the human | Decryption requires an interactive operator act; the assistant/API/tests structurally CANNOT decrypt — blindness is cryptographic, not conventional | **RECOMMENDED, wrapped in DPAPI as a second layer** |

**Recommendation:** encrypted vault file
(`operator-vault/broker_credentials.vault`, outside the repo tree, never
git-visible) — AES-256-GCM, Argon2id KDF, operator passphrase at unlock
time, DPAPI-wrapped as defense-in-depth on the Windows console
(`ASSUMPTION A-2`: single-Windows-workstation posture per the sealed act
record holds).

### S2.2 Unlock/decrypt boundary

Unlock is an **explicit, audited operator act** (`broker.vault.unlocked`
audit; passphrase read via no-echo prompt in the backend process only).
The decrypted token lives solely inside a request-scoped
`ResolvedBrokerCredential` — the **BE-3 P2 credential-boundary law
generalized verbatim**: value excluded from `repr`/`str`; never module
state, never serialized/logged/audited/returned; sole-resolution-module
rule with an import-boundary test (no module but the vault module may
import the backend). Lock on process exit or explicit
`broker.vault.locked` act; an idle TTL re-lock is a BO-time parameter
(`ASSUMPTION A-3`: default 8h).

### S2.3 Scoped service identity (redirect-adjusted; DIR §4 — same blindness law, new secret shape)

The stored secret is now the **investor (read-only) password + the
account-number/server-hostname tuple** for the dedicated **Exness demo
account** (never the master password; never the Operator's personal
live login). The identical blindness law applies to the whole tuple —
value-excluded-from-repr, request-scoped only, sole-resolution module.
Scope is verified at first unlock: the adapter executes a **scope
probe** — a read succeeds AND the terminal's trade-permission flag
reports read-only (the investor-login fact recorded into health; a
master-login detection = typed refusal + audit, the credential is
mis-provisioned). Rotation: new investor password set at the Exness
Personal Area, then a governed re-vault act (old value overwritten,
`broker.vault.rotated` audited); revocation is broker-side (change/
disable investor access) + vault wipe act.

### S2.3b Vault loss & recovery runbook (C-3 specification — honest, no new mechanics)

| Scenario | Procedure |
|---|---|
| **Vault file lost or corrupt** | Treat the stored credential as **presumed compromised**. Order of operations is fixed: (1) **broker-side revoke FIRST** (Exness Personal Area: change/disable the investor password — the credential dies at the source); (2) re-vault act: set a fresh investor password, `broker.vault.rotated` + `broker.vault.unlocked` audited; (3) scope probe re-runs and re-records (incl. the read-only-login assertion). No AXIOM data is at risk — projections carry no secrets. Exposure bound even pre-revoke: the investor password is structurally read-only at the broker (the N1 provider arm limits the blast radius to visibility, never mutation). |
| **Passphrase forgotten** | Cryptographically unrecoverable by design (that IS the N4 property — no escrow, no backdoor). Same procedure as vault-lost: broker-side investor-password change → fresh credential → new vault file under a new passphrase. |
| **DPAPI layer broken by machine churn** (reimage, user-profile migration, hardware change) | The DPAPI wrap fails to open; the inner AES-256-GCM file is intact but the wrap is dead. Recovery: if an operator-held encrypted backup exists (below), restore it and re-wrap on the new machine (passphrase still required — the inner layer never depended on the machine); otherwise vault-lost procedure. |
| **Backup posture** | An encrypted backup of the vault file is **OPTIONAL and operator-held** (offline medium, operator custody) — **never in the repo, never in any assistant-visible path**; taking or restoring a backup is an audited act (`broker.vault.backup_taken` / `broker.vault.restored`). The backup is the same AES-256-GCM bytes — useless without the passphrase. |
| **Machine migration (planned)** | Take the audited backup → migrate → restore + re-wrap under DPAPI on the new console → verify with an audited unlock + scope probe → destroy the transport medium copy (operator attestation). |

The runbook changes no mechanics: every path terminates in the
existing re-vault/rotate acts and the existing audit vocabulary.

### S2.4 N4 structural blindness proof plan

- **grep-class audit (executed in-suite):** scan `app/v2/broker_read/`
  + API + test fixtures for token-shaped literals and for any import of
  the vault backend outside the sole-resolution module; scan all
  response models and error paths for the credential field name.
- **Log/error canary test:** inject a canary token in a test vault,
  drive every error path (401, timeout, malformed), assert the canary
  never appears in logs, envelopes, audit rows, or drift output.
- **Payload-echo canary (review observation, folded):** provider
  payloads are stored verbatim in `v2_broker_order.payload` and
  `v2_broker_instrument_permission.visibility` — a provider could
  smuggle a token-shaped string into a payload. The canary suite
  therefore includes a **payload-echo probe**: a fixture payload
  carrying the canary token lands in the projection, and the test
  asserts the canary is absent from every log line, envelope, audit
  row, and health output while the projection row itself (the lawful
  storage site) is the only place the bytes exist.
- Assistant surface: no API returns vault content in any state; the
  vault file lives outside the workspace root the assistant sees
  (`operator-vault/` is Operator-console-only; `ASSUMPTION A-4`).

Roadmap bullet: *encrypted credential vault and scoped service
identity* → S2 whole.

## S3 — Read models (six tables; projections, never state)

**Module:** `app/v2/broker_read/` + `app/db/models/v2_broker_read.py`
(PG-002 same-unit registration). All rows carry the BE-1 regime
(`mode`/`operator_id`/`correlation_id`/`created_at`) + the **provenance
pin** (N3): `provider_id`, `provider_account_id`, `sync_run_id` FK,
`fetched_at_basis`, and `data_class` — pinned **`simulated`** in v1
under the 6-class taxonomy: practice accounts are simulated money;
`historical_real`/`live` remain corpus-gated (V2-TD-18); the taxonomy
value is provider-environment-derived and CHECK-constrained, so a
future live-read act is a separately-sanctioned data-class change,
never a config flip.

| # | Table | Semantics | Key columns beyond regime+provenance | Anchors |
|---|---|---|---|---|
| 1 | `v2_broker_account` | Append-only snapshot generations (`record_seq`+`supersedes`, BE-6 law) | `broker_account_ext_id`, `alias`, `currency`, `environment` CHECK `('practice')` v1 | uq `(provider_id, broker_account_ext_id, record_seq)` |
| 2 | `v2_broker_balance` | Append-only per-sync snapshot | `balance`, `margin_used`, `margin_available`, `unrealized_pl`, `currency` (TEXT-decimal, S5 money law) | uq `(sync_run_id, broker_account_ext_id)` |
| 3 | `v2_broker_position` | Append-only per-sync snapshot set | `instrument_ext_id`, `units_long`, `units_short`, `avg_price_long/short` | uq `(sync_run_id, broker_account_ext_id, instrument_ext_id)` |
| 4 | `v2_broker_order` | Append-only per-sync snapshot of OPEN orders (broker-side state; AXIOM never mutates) | `order_ext_id`, `order_state_ext`, `payload` (JSON, verbatim provider fields) | uq `(sync_run_id, order_ext_id)` |
| 5 | `v2_broker_fill` | **Append-only ledger** (transactions are immutable facts; since-id paging) | `transaction_ext_id`, `tx_type_ext`, `instrument_ext_id`, `units`, `price`, `tx_time_ext` | uq `(provider_id, broker_account_ext_id, transaction_ext_id)` — the idempotency anchor |
| 6 | `v2_broker_instrument_permission` | Append-only per-sync snapshot | `instrument_ext_id`, `visibility` (verbatim provider flags JSON), `display_name` | uq `(sync_run_id, broker_account_ext_id, instrument_ext_id)` |

Plus three infrastructure tables: **`v2_broker_sync_run`** (S4: run
lineage — trigger actor, scope, page counts, outcome CHECK
`('complete','partial_refused','failed')`, `inputs_hash`,
canonical `result_digest` per S4.1), **`v2_broker_reconcile_run`**
(C-2, S5.1: reconciliation lineage — the zero-discrepancy case leaves
evidence, not assertion), and **`v2_broker_discrepancy`** (S6).
**Nine tables total.** Immutability: UPDATE+DELETE guard pairs on all
9 (household trigger law) = **18 triggers (58 → 76)**; "current"
values are derivations (greatest `record_seq` / latest complete
`sync_run_id`), never UPDATEs — the BE-8 zero-UPDATE regime carried.

Freshness fields: every snapshot row carries `fetched_at_basis`;
staleness is **computed at read time against the newest complete sync
run** (never a stored mutable flag — PGF-012 spirit). Compver: +1
component `broker_read_engine = bre-1.0.0` over `{adapter,sync,
reconcile}.py` (10 → **11**, append-only law; rolling-hash recipe of
0047/0048). Permissions: S8 (+7, 57 → **64**).

N3 separation proof obligations (BE-8 machinery reused): disjoint
`v2_broker_*` vs `v2_paper_*` namespaces; no FK crosses the boundary;
a boundary test asserts no model, query, or API route joins the two
domains; provenance pins on every row make ambiguous-origin rows
schema-impossible (`provider_id` NOT NULL).

Roadmap bullets: *account/balance/position/order/fill/instrument-
permission read models* → tables 1–6.

## S4 — Sync & staleness architecture

- **Trigger model (Q4): operator-initiated only** (`POST
  /v2/broker/sync`) — no scheduler (V2-TD-24 family consistency; the
  tick source remains registered debt programme-wide). Admin-gated
  (S8); every run audited with actor.
- **Run shape:** one `v2_broker_sync_run` row (state `running` is not
  stored — the row is written ONCE at completion with its outcome:
  complete / partial_refused / failed; a crashed run simply never
  lands a row, and its page work is invisible by design — see
  atomicity).
- **Partial-data law (the REQ's half-fetched-page rule):** all pages of
  a scope are fetched into memory and content-validated BEFORE any row
  lands; the DB write is a single transaction covering the whole run.
  A failed page ⇒ the transaction never opens ⇒ `partial_refused`
  outcome row + typed refusal + audit. **A half-fetched page cannot
  half-land because landing is all-or-nothing per run.**
- **Idempotency & replay (BE-7 law):** fills dedupe on the
  `transaction_ext_id` anchor (re-sync inserts only unseen
  transactions, `broker.fill.reused` audited for skips); snapshot
  tables key on `sync_run_id` so a re-run creates a NEW generation and
  never touches prior rows; each run records a canonical
  `result_digest` under the C-1 canon below — two runs against
  unchanged broker state produce equal digests, giving the
  deterministic-replay attestation (×3 law at test time against a
  fixture provider).

### S4.1 The digest canon (C-1 specification, ITRGA-REV-V2-BE-9-DESIGN-001 §2)

`result_digest = SHA-256` over the **canonical substantive projection**
of the fetched payload set, defined exactly:

1. **Field inclusion rule (per read model — substantive fields ONLY):**
   - accounts: `broker_account_ext_id, alias, currency, environment`
   - balances: `broker_account_ext_id, balance, margin_used,
     margin_available, unrealized_pl, currency`
   - positions: `broker_account_ext_id, instrument_ext_id, units_long,
     units_short, avg_price_long, avg_price_short`
   - orders: `order_ext_id, broker_account_ext_id, order_state_ext` +
     the payload's substantive order fields (type, units, price,
     time-in-force as provider-named keys)
   - fills: `transaction_ext_id, broker_account_ext_id, tx_type_ext,
     instrument_ext_id, units, price, tx_time_ext`
   - instrument-permissions: `broker_account_ext_id,
     instrument_ext_id, visibility, display_name`
2. **Field EXCLUSION rule (retrieval-volatile, never hashed):**
   fetch timestamps/banners, provider request/trace ids, pagination
   cursors and cursor echoes, rate-limit headers, server-time fields,
   `lastTransactionID`-style high-water marks, and any field not in
   the inclusion list (allow-list law: unknown fields are excluded by
   construction, not by enumeration of exclusions).
3. **Ordering rule:** within each model, records sorted by their
   natural external key (`broker_account_ext_id`, then
   `instrument_ext_id` / `order_ext_id` / `transaction_ext_id` as
   applicable); models concatenated in the fixed order accounts →
   balances → positions → orders → fills → instrument-permissions.
   Retrieval order NEVER influences the digest.
4. **Encoding:** JSON canonical form — UTF-8, LF, sorted keys,
   separators `(",", ":")`, decimals as their exact provider string
   (never float), `None` omitted.

**Tests pinned (S11 E2):** (a) digest equality across an identical
fixture with shuffled page/record order (false-FAIL guard); (b) digest
inequality on a single substantive-value change (false-PASS guard);
(c) digest invariance under injected volatile-field changes (request
id, timestamps).
- **Unavailable/degraded provider:** typed `broker.unavailable` refusal;
  no partial landing; health surface records the failure fact (S7);
  read surfaces continue serving last-good with staleness banners (Q7).
- **Rate limits:** provider-declared limits honored via token bucket;
  429 ⇒ the run completes what it lawfully can or refuses whole per the
  partial-data law (no half-runs); the 429 fact lands in health.
- **Fetch-budget law (review observation, folded):** a per-scope
  page-count ceiling (BO-set; `ASSUMPTION A-7`: default 200 pages per
  model per run) bounds the single-transaction landing in memory. A
  pathological history exceeding the ceiling ⇒ typed refusal
  `broker.fetch_budget.exceeded` + `partial_refused` outcome row +
  audit — never an unbounded buffer, never a half-landing. Test:
  fixture exceeding the ceiling asserts the refusal + zero rows landed.

## S5 — Reconciliation (read-side, broker → AXIOM)

- **Comparison law:** broker payload (fresh fetch inside the
  reconciliation run) is the authority; AXIOM's latest complete
  projections are the comparand (V2-R-10). Reconciliation NEVER writes
  to projections — it writes discrepancy records only (alarm surface,
  BE-8 reconcile law).
- **Compared value classes:** balances (per account, per field),
  position units/avg-price (per instrument), open-order set equality
  (by `order_ext_id`), fill-ledger completeness (broker transaction ids
  vs `v2_broker_fill` anchors — missing-in-AXIOM detection),
  instrument-permission set equality.
- **Rounding/currency law:** Decimal end-to-end over TEXT-decimal
  columns (BE-8 money law); comparisons exact — **no tolerance bands in
  v1** (`ASSUMPTION A-5`: any mismatch, however small, is a discrepancy;
  tolerance would be a governed future change with citations). Currency
  compared as an explicit field; cross-currency arithmetic does not
  exist in v1 (single practice account currency).
- **Provenance of every compared value:** the discrepancy record embeds
  both sides verbatim with their provenance pins (broker fetch basis +
  AXIOM sync_run_id) — the record is self-proving.
- **Cadence:** on-demand governed act (`POST /v2/broker/reconcile`,
  admin) + automatically appended to every complete sync run
  (reconciliation-first: sync without comparison does not exist).

### S5.1 Reconcile-run lineage (C-2 specification — the clean run is evidenced, not asserted)

Every reconciliation — discrepant or clean — lands exactly one
append-only **`v2_broker_reconcile_run`** row:

| Column | Content |
|---|---|
| `reconcile_run_id` | primary identity |
| `sync_run_id` | FK to the sync run whose projections were compared (NULL only for standalone on-demand runs, which pin the newest complete sync id here) |
| `compare_scope` | JSON: models + accounts compared |
| `broker_side_digest` | the fresh broker fetch, canonicalized under **the S4.1 canon** (same rules, same encoding) |
| `projection_side_digest` | the AXIOM projections, canonicalized under the **same S4.1 canon** applied to projection rows (declared: identical inclusion/ordering/encoding rules — one canon, two sides) |
| `compared_counts` | JSON: records compared per model |
| `discrepancy_count` | landed discrepancies (0 for a clean run) |
| `outcome` | CHECK `('clean','discrepant')` — `clean` iff count = 0 |
| `actor_id` + BE-1 regime + provenance pins | household law |

Immutable (UPDATE+DELETE guarded — counted in the S3 tally of 18).
"Reconciliation ran clean" is now a Level-I row: both digests, both
provenances, the counts, and the zero. The E2 evidence gains: a clean
fixture run asserts `outcome='clean'`, equal-side digests recorded,
and ×3 digest stability; a seeded-mismatch run asserts
`outcome='discrepant'` with `discrepancy_count` == the seeded count.

## S6 — Discrepancy records

- **State machine (Q5):** `detected → triaged → owned →
  resolved | dismissed_with_reason`. Append-only event trail
  (`v2_broker_discrepancy` row immutable; state transitions are ledger
  events in `details`-bearing audit + a compact `state_events` JSON
  appended via new generations `record_seq`+`supersedes` — zero UPDATE,
  BE-8 regime). Terminal: `resolved`, `dismissed_with_reason` (reason
  mandatory, typed refusal without it).
- **Classes (Q5):** `amount_mismatch`, `missing_on_broker`,
  `missing_in_axiom`, `currency_mismatch`, `timestamp_window`
  (fact seen outside the expected sync window), `permission_visibility`
  (instrument set drift), `set_mismatch` (open orders). Closed CHECK.
- **Ownership:** `owned_by` operator id set at the `owned` transition;
  aging = derivation from `created_at` (no stored age); unowned
  discrepancies older than a BO-set threshold surface in health (S7).
- **RBAC:** triage/resolve = admin (`v2.broker.discrepancy.manage`);
  read = admin+operator. Every transition audited (BE-3 P2 lifecycle
  law).

Roadmap bullets: *read-side reconciliation* → S5; *discrepancy
record/state/ownership* → S6.

## S7 — Provider/broker operational health

Mirrors the BE-4/5/6 provider-health household: a read surface
(`GET /v2/broker/health`) reporting **classifier-visible facts only**:
provider id, environment, last sync run (id/outcome/basis), last
success basis, consecutive failures, last error class (typed class
only, never payload — `broker.terminal.unavailable` counts as its own
outcome class per E-ENV-1), vault lock state (`locked`/`unlocked` —
never key material), read-only-login assertion state (S2.3 scope
probe), unowned-discrepancy count.
**Three independent facts, GREEN requires ALL THREE (DIR §2.3 —
extending the Q6 law to the terminal substrate):**
1. `terminal` — MT5 process state (installed / running / logged-in),
2. `reachability` — broker/server contact outcome through the terminal,
3. `freshness` — age of the newest complete sync.
A running terminal with a dead server is `terminal_up_unreachable`;
a reachable broker with stale projections is `reachable_stale`; none
of these is ever GREEN — the health surface cannot assert what it has
not measured. Outage semantics for consumers: read models stay
servable with staleness banners (Q7); the health surface is the single
truth about why.

## S8 — RBAC & audit

**7 new permissions, namespace `v2.broker.*`** (57 → 64; no
forbidden-marker collision: `broker` sits in
`V2_FORBIDDEN_PERMISSION_MARKERS` — **DECISION-1 for the review:**
narrowest scoped exemption, literal prefix `v2.broker.` (the D-1
mechanism of BE-8 repeated; both-arms + boundary `v2.brokerage.*`
must-die tests):

| Permission | Roles | SAL |
|---|---|---|
| `v2.broker.accounts.read` | admin, operator | SAL-2 |
| `v2.broker.balances.read` | admin, operator | SAL-2 |
| `v2.broker.positions.read` | admin, operator | SAL-2 |
| `v2.broker.orders_fills.read` | admin, operator | SAL-2 |
| `v2.broker.sync.run` | admin | SAL-3 |
| `v2.broker.discrepancy.manage` | admin | SAL-3 |
| `v2.broker.vault.manage` (unlock/lock/rotate acts) | admin | SAL-4 |

Audit events on every privileged action (`broker.sync.started/
completed/refused`, `broker.vault.unlocked/locked/rotated`,
`broker.discrepancy.triaged/owned/resolved/dismissed`, `broker.fill.
reused`, …). Denial vocabulary: generic `"Permission denied"`; no
error message anywhere names vault paths, key derivation, or token
shapes (S2.4 canary enforces).

## S9 — API surface

Namespace `/api/v1/v2/broker/*`. BE-1 envelope everywhere; every read
response carries `provenance` + `staleness` blocks and the banner when
degraded (Q7).

- **Writers (POST only, C3 law): exactly 4** — `/sync`, `/reconcile`,
  `/vault` (single vault-act endpoint, `action ∈ unlock|lock|rotate`;
  `rotate` confirmation-gated per the BE-8 two-act pattern), and
  `/discrepancies/transition` (typed, audited S6 state moves).
- **Reads (GET): exactly 8** — `/accounts`, `/balances`, `/positions`,
  `/orders`, `/fills`, `/instrument-permissions`, `/discrepancies`,
  `/health`. Census asserted by the API-surface test (BE-8 law):
  **4 POST + 8 GET = 12 routes, zero PUT/PATCH/DELETE.**
- **N1 proof sketch:** no route path or body schema contains an order
  verb; the router census test pins the exact 12-route list; the
  adapter's six-verb contract is the only provider touchpoint; a
  code-path scan asserts no import chain from `v2/broker_read/` reaches
  any module matching the execution/adapter token predicate (BE-7/BE-8
  scan law with `paper` added to the banned set for THIS domain — the
  N3 wall from the broker side).
- **N2 proof sketch:** no frontend asset references a provider
  hostname; the provider base URL exists only in the adapter's sealed
  config binding (Q9); CORS surface unchanged; the read models serve
  AXIOM envelopes only.

## S10 — Migration plan (plan only; authored post-acceptance + BO)

- **Chain:** `20260905_0049_v2_be9_broker_read.py`, `down_revision =
  "20260904_0048"` (the sealed terminal; reference sha
  `1d4005fa…dd3e`), single head after apply.
- **Recounts (C-2-adjusted):** triggers 58 → **76** (+18: 9 tables ×
  2, incl. `v2_broker_reconcile_run`); permissions 57 → **64** (+7,
  DEL-004 revision-local literals, existing-set filter); compver
  10 → **11** (+1 `broker_read_engine=bre-1.0.0`, apply-time disk
  hashing, recipe unchanged). Per the review §4: this recount carries
  identically through the acceptance record, BO, pins, and future
  apply/verify pack literals (the 0048 exact-pin law, prospectively).
- **Drift law:** exactly the 9 inherited V1 tokens; zero BE-9 tokens;
  both heads; generational scoping of the 0048-era drift tests when
  0049 becomes head (established law).
- **Downgrade:** symmetric content-based teardown (0047/0048 chassis);
  no-touch test (prior rows byte-identical; trigger delta exactly the
  18 names).
- **Working-DB application:** separate sanctioned act at chain end on
  the proven console-pack chassis (identity gate = the sealed 0048
  sha `1d4005fa…dd3e` + `current == 20260904_0048`; E-0046-DUP;
  PGF-020…024; the halt-ruling lessons compiled in).

## S11 — Test plan mapped to exit evidence (§5)

Projected budget ~60 tests, 4 modules (final counts at BO; fail-first
with shipped failing-run witness — OBS-E statute):

| Exit item | Concrete inventory |
|---|---|
| **E1** sandbox contract evidence | Fixture-provider contract tests (recorded practice-environment payload fixtures, BE-3 P1 fixture-foundation law); adapter six-verb census; pagination/cursor laws; provider error taxonomy mapping ×6; Level-I transcript against the fixture provider; **live practice-endpoint contact = a separately-authorized evidence act at BO** (network law: zero network in the suite — socket guard stands; E1 field evidence follows the 0047/0048 witnessed-transcript pattern on the console) |
| **E2** reconciliation evidence | Equal-state run → `v2_broker_reconcile_run` row `outcome='clean'` with both-side digests recorded (C-2) + equal result digests ×3 (replay law); the three C-1 canon tests (shuffle-invariance, single-value sensitivity, volatile-invariance); seeded-mismatch runs → exact class detection per Q5 class (7 classes × detection + record content assertions + `discrepancy_count` == seeded count) |
| **E3** stale/unavailable/mismatch/partial | Provider-down typed refusal + last-good-with-banner read; stale freshness computation (reachable_stale health); partial-page → `partial_refused`, zero rows landed (transaction atomicity probe); malformed payload → page discarded whole |
| **E4** entitlement/least-privilege | RBAC matrix over the 7 permissions (403 generic, 401); scope-probe recording; vault acts admin-SAL-4-only; DECISION-1 both-arms + `v2.brokerage.*` boundary |
| **E5** security review surface | S12 + S2.4 canary tests (token never in logs/envelopes/audits/drift); import-boundary test (sole-resolution module); N3 domain-wall test; N1 type-census + code-path scan; PGF-021 source scan (no filesystem conditionals; config-driven provider binding) |
| Regression | Full suite ≥ 1,026 + budget, 0 failed; V1 six-pin floor re-hash; prior-band contract regression (incl. BE-8 vocabularies + paper-domain wall from BOTH sides) |

## S12 — Threat model & security review pre-read

- **Assets:** broker credential (highest); account data integrity;
  sync/reconciliation integrity; the N1 wall (no mutation reachability);
  the N3 wall (paper/broker disjointness).
- **Actors:** operator (trusted, passphrase holder); admin (trusted);
  future code (primary adversary — guarded by type census, sealed
  registry, scans, statutes); a compromised provider (bounded: read
  scope only, practice environment, projections never authoritative);
  network adversary (TLS; token in header only; no query-string
  secrets).
- **Abuse cases → mitigations:** adapter substitution → sealed frozen
  registry + compver pin + import scan; vault exfiltration →
  cryptographic blindness (passphrase never stored) + DPAPI second
  layer + sole-resolution module + canary suite; replay/split-brain
  sync → single-transaction landing + digest comparison + fill anchors;
  N1 violation → no verb exists (type census) + route census + token
  scan; N4 violation → S2.4 canaries; config error repointing reads
  (Q9) → single sealed binding, audited at unlock, environment string
  in every provenance pin.
- **Explicitly out of scope (honest):** order submission (BE-10);
  frontend broker anything; live (non-practice) data classes
  (corpus-gated); scheduled sync; multi-broker; credential sharing
  with any assistant surface — never.
- **Standing-law edits needed:** DECISION-1 (marker exemption
  `v2.broker.`) only. Mode law untouched (reads run in any lawful
  mode; writers audit the acting mode).

## S13 — Open questions Q1–Q9 (recommendation + rationale)

| Q | Recommendation | Rationale |
|---|---|---|
| **Q1** Broker | **RESOLVED by O-1 (DIR redirect): Exness demo over local MT5 terminal, investor (read-only) password** (S1.1 re-cut); Operator provisions + sets read-only access at BO prep (`A-1` successor). Design broker-shaped; the S1.4 contract binds regardless | OANDA residency-unavailable; Exness relationship held; the investor password adds a provider-side structural N1 arm (strictly stronger than v1.0.0); FXCM/cloud-relays/cTrader/IBKR eliminated with reasons (S1.1) |
| **Q2** Vault | Encrypted file (AES-256-GCM, Argon2id, operator passphrase) wrapped in DPAPI; NOT keystore-only | Cryptographic (not conventional) N4 blindness: without the human's passphrase nothing on the box can decrypt; keystore-only lets any same-user process read |
| **Q3** Persistence | Full projection tables with provenance pins (as favored) | Auditable, reconcilable, replayable; a pass-through cache can neither reconcile nor prove provenance — reconciliation-first forces projections |
| **Q4** Sync trigger | Operator-initiated only; admin permission; every run audited + lineage row + result digest; idempotent via fill anchors + generation snapshots | Scheduler = standing programme debt (V2-TD-24 family); BE-7 replay law satisfied by digest + anchors |
| **Q5** Discrepancy classes | The 7 classes of S6 (closed CHECK); ownership at `owned` transition; aging derived; dismissal requires reason (typed refusal without) | Covers set-, value-, currency-, time-, and visibility-drift; closed vocabulary keeps the state machine testable |
| **Q6** Health truthfulness | Freshness ⊥ reachability; GREEN = both; `reachable_stale` exists | The surface cannot assert what it has not measured — staleness is computed against the newest complete sync, never a flag |
| **Q7** Degraded reads | Last-good-with-banner on all six read surfaces (as favored); refusal only when NO complete sync has ever landed (`broker.no_data` typed) | Projections are snapshots by design; hiding them during outages destroys their value; the banner + health surface keep honesty |
| **Q8** Instrument permissions | Verbatim provider visibility flags stored as facts; exposed read-only with the N1 disclaimer field (`execution_capability: "none — read-model only (BE-9)"` on the surface); no downstream gating logic in v1 | Modeling "may trade" as anything but a stored fact would imply execution semantics this band must not have |
| **Q9** Vault↔config boundary | **Q9 successor (DIR §3.3, binding):** code-pinned **server hostname + account number + environment string** in the sealed registry; re-asserted at **every vault unlock AND every sync start** (mismatch = typed refusal + audit); pinned into every row's provenance; the vault stores ONLY the credential tuple | A config error cannot silently repoint: the binding is hash-pinned code, not config; three sites must agree — registry literal, unlock/sync assertion, row provenance |

## §14 — What this design chooses NOT to do (honesty register)

1. **No order submission, structurally:** no mutation verb in the
   contract type; no route; no imported mutation shape (V1 `BrokerPort`
   explicitly not reused). Saying it structurally, per the REQ.
2. No frontend broker calls; no provider hostname outside the adapter.
3. No live (non-practice) data; `historical_real`/`live` stay
   corpus-gated (V2-TD-18).
4. No scheduler; no multi-broker; no tolerance bands in reconciliation
   (v1 exact-compare, `A-5`).
5. No paper↔broker joins of any kind (N3 wall tested from both sides).
6. No code/migration in this phase — this document is the deliverable.

## §15 — Assumptions register

A-1 successor (S1.1; **O-1 RESOLVED — Exness/MT5/investor-password;
DISCHARGED 2026-09-05** per the DIR final edition: demo CREATED
(Standard type per the provision pin), plain-wifi connectivity probe
SUCCESSFUL, investor read-only access SET terminal-side; remaining at
BO = the binding pins only — server hostname + account number +
environment string, operator-held). A-2 (S2.1) single-Windows-console posture holds (now also the
MT5-terminal substrate posture). A-3 (S2.2) vault idle re-lock TTL 8h
default, BO-settable (**review O-2: ITRGA finds 8h acceptable; Operator
confirms at BO**). A-4 (S2.4) `operator-vault/` lives outside any
assistant-visible root. A-5 (S5) exact-compare reconciliation (no
tolerance) acceptable for v1. A-6 (S11) ~60-test budget refined at BO
(the C-1/C-2/observation tests add ≈8; the E-ENV-1 terminal-state tests
add ≈4). A-7 (S4) fetch-budget ceiling per-window (200 windows/model/
run default, BO-settable). A-8 (S1.2) history window 24h with 1h
overlap, BO-settable. **E-ENV-1 (environmental law, DIR §2):** the
operator's proxy regime defeats MT5 connectivity (tuning attempted);
plain-wifi is the working posture; proxy windows = sync-unavailable BY
DESIGN, not a bug; no proxy traversal promised. Each assumption is a
review surface, not a decision.

## §16 — Change-note v1.0.0 → v1.2.0 (ONLY these edits; items 1–5 per ITRGA-REV-V2-BE-9-DESIGN-001, item 6 per ITRGA-DIR-V2-BE-9-S1-REDIRECT-001)

1. **C-1 — new section S4.1 (digest canon law):** explicit
   canonicalization — per-model substantive-field inclusion lists;
   allow-list exclusion of retrieval-volatile fields (unknown fields
   excluded by construction); natural-external-key ordering + fixed
   model order (retrieval order never influences the digest); encoding
   pinned (JSON canonical: UTF-8, LF, sorted keys, exact-string
   decimals); the three pinned tests (shuffle-invariance,
   single-value sensitivity, volatile-invariance).
2. **C-2 — new section S5.1 + table 9 (`v2_broker_reconcile_run`):**
   every reconciliation (clean or discrepant) lands an append-only
   lineage row — both-side digests under the ONE S4.1 canon, scope,
   counts, `outcome CHECK ('clean','discrepant')`; "ran clean" is a
   Level-I row, not an assertion. **Consequential recounts carried
   everywhere:** 9 tables; triggers 58 → **76** (+18); S3 tally, S10
   plan + downgrade delta, S11 E2 inventory all adjusted; the review's
   §4 exact-pin prospection quoted in S10.
3. **C-3 — new section S2.3b (vault loss & recovery runbook):**
   vault-lost/corrupt (broker-side revoke FIRST, then re-vault);
   passphrase forgotten (unrecoverable by design — that IS N4; same
   path); DPAPI broken by machine churn (inner layer machine-
   independent; backup-restore or vault-lost path); optional
   operator-held encrypted backup (never in repo/assistant-visible
   paths; audited acts); planned machine migration. No new mechanics —
   every path ends in existing acts and audit vocabulary.
4. **Review observations folded (non-blocking, one line + one test
   each):** payload-echo canary probe (S2.4); fetch-budget ceiling +
   typed `broker.fetch_budget.exceeded` refusal (S4, new A-7).
5. **O-2 pendency recorded** in §15 (lands at BO). DECISION-1
   concurrence noted as granted at design acceptance.
6. **S1 re-cut per ITRGA-DIR-V2-BE-9-S1-REDIRECT-001 (O-1 RESOLVED —
   this bump makes the document v1.2.0):**
   - S1.1 re-cut: **Exness demo / local MT5 terminal / investor
     (read-only) password** selected on Operator decision of record;
     residency facts + eliminations (OANDA residency-unavailable; FXCM
     contradictory residency + demo expiry; MT5 cloud relays killed on
     N4 third-party custody; cTrader/IBKR runner-ups with reasons).
   - S1.2 re-cut: six-verb ↔ `MetaTrader5` Python mapping
     (`account_info` singleton with account-number pin /
     `positions_get` / `orders_get` / `history_deals_get` +
     `history_orders_get` over declared time windows /
     `symbols_get`+`symbol_info`); time-window paging law (A-8: 24h/1h
     overlap); anchors unchanged (deal tickets); provenance pins server
     hostname + account + environment + server-time fetch basis.
   - S1.3 re-cut: **`broker.terminal.unavailable` FIRST-CLASS** (E-ENV-1
     §2.1), distinct from `broker.unavailable`; terminal-courtesy law
     replaces the token bucket (no REST headers exist); E-ENV-1
     recorded as environmental law (proxy = sync-unavailable BY DESIGN,
     no traversal promised; E1 evidence documented under plain-wifi).
   - S1.4: registry key → `exness_mt5_demo`; **Q9 successor** (binding)
     — code-pinned server hostname + account number + environment,
     re-asserted at every unlock AND every sync start; N1 arms
     restated (provider-side investor password = the new strongest
     arm; type census; scans).
   - S2.3/S2.3b consequentials: secret = investor password +
     account/server tuple (same blindness law); scope probe adds the
     read-only-login assertion (master-login detection = typed
     refusal); runbook re-cut to investor-password
     revoke-first flow with the bounded-blast-radius note.
   - S7 delta: three independent health facts (terminal /
     reachability / freshness), GREEN requires all three;
     `terminal_up_unreachable` exists.
   - S13 Q1/Q9 rows re-cut; §15: A-1 successor, A-8, E-ENV-1 appended;
     A-6 budget +≈4 terminal-state tests.
   - Per DIR §4, expressly NOT re-opened: S1.4 contract shape, S2 vault
     mechanics, S3 projections/data_class pin, S4 all-or-nothing law,
     S5/S6, S8–S12, C-2 recounts, E1–E5 mapping.
7. **v1.2.0 → v1.2.1 (DIR final edition):** S1.1 gains the PROVISION
   PIN (Standard demo type; Standard Cent refused — cent-denominated
   balances vs the S5 money law; Pro/Raw/Zero refused — needless
   complexity; no live account any tier) and the PROVISIONING STATUS
   record (demo CREATED; plain-wifi probe SUCCESSFUL; investor
   read-only access SET terminal-side — **A-1 successor DISCHARGED
   except the BO-time binding pins**); §15 A-1 row updated to match.
   No other change.
8. Version/header bump + this change-note. **No other section altered.**

**We don't guess. We prove.**

**End of AXIOM-V2-BE-9-DESIGN-001 v1.2.1**
