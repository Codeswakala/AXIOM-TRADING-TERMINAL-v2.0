# AXIOM BUILD ORDER — W1-U03

## External Integration: MT5 Integration **Framework** (Broker Abstraction / Adapter Contract — NO Connection, NO Execution)

**Build Order ID:** W1-U03
**Wave:** 1 — Core Platform · **Unit:** 03
**Version:** 1.0 · **Status:** ISSUED
**Authority:** ITRGA · **Date Issued:** 2026-07-13
**Authorized By:** ITRGA, following **W1-U02 APPROVED WITH OBSERVATIONS** (Platform v0.10.0) + explicit Operator authorization ("build order W1-U03 authorized").

**Governing Documents (canonical order — `10_CONSTITUTIONAL_HIERARCHY.md`):**
`00_VISION_AND_PRINCIPLES` → `03_AXIOM_SPEC` → `04_PROJECT_ROADMAP` → **`05_SYSTEM_ARCHITECTURE.md` v2.0 (CANONICAL)** →
`06_ML_SPEC` / `07_UI_UX_SPEC` → `08_DEVELOPER_REASONING_FRAMEWORK` / `09_ITRGA_REASONING_FRAMEWORK` →
Tier-7 (`QUALITY_GATE_SPEC`, `RISK_REGISTER`, `TECHNICAL_DEBT_REGISTER`, `GOVERNANCE_AMENDMENTS`, `PROJECT_STATE`) →
`UNIVERSAL_ITRGA_REVIEWER_DIRECTIVE.md`.

---

## 1. Purpose

Deliver the **MT5 integration *framework*** — the last named Wave-1 "Core Platform" component in
`04_PROJECT_ROADMAP` — as a **contract-only abstraction inside the External Integration System**
(05 v2.0 §8, §13, §16). The deliverable is the **shape of broker interoperability**, not broker
interoperability itself:

- the **adapter/port interface** every broker (MT5 first, others later via §17 plugin architecture)
  must satisfy;
- the **domain models / DTOs** at the boundary (symbol, instrument metadata, quote/tick, account
  descriptor, order *intent* — as inert data, never dispatched);
- an **anti-corruption boundary** so MT5's vocabulary never leaks into inner subsystems (05 v2.0 §12,
  §16 "broker-specific logic shall never appear outside the External Integration System");
- a **`NullBroker` / disabled reference adapter** that implements the contract but performs **no I/O,
  no network, no connection, no execution** — proving the seam compiles and is testable in isolation;
- the **Constitutional Governance Gate stub** (05 v2.0 §15) that stands *between* the platform and any
  future broker integration and is **hard-wired CLOSED** in this unit.

This is a **pure-architecture / seam-definition** unit. It adds an *interface and a wall* — **not** a
broker connection, **not** live MT5 data, **not** order placement. It establishes single ownership
(§13: "Broker connectivity → External Integration System") so future execution research (Wave 6) has a
clean, governance-gated place to live and can never be smuggled in earlier.

---

## 2. Governance Envelope (READ FIRST — violation = automatic FAIL)

This unit sits closest to the platform's brightest constitutional line. The envelope is therefore the
most important section of this Build Order.

- ❌ **No broker connection of any kind.** No `MetaTrader5` package call, no socket, no login to any
  MT5 terminal/server, no network egress to a broker, no credentials read or stored. If the delivery
  imports and *invokes* a real MT5 client against a live/demo terminal, it is an automatic **FAIL**.
- ❌ **No execution, no orders, no positions, no trades — real, demo, or paper.** Order *intent* may
  exist only as an **inert DTO**; nothing may dispatch it. "No live automated execution shall be
  authorized unless future governance explicitly approves it" (04_PROJECT_ROADMAP, Wave 6 note).
  Execution simulator / risk engine / paper trading / broker connectivity are **Wave 6**, not Wave 1.
- ❌ **The Constitutional Governance Gate (05 v2.0 §15) must be CLOSED and enforced.** The path
  Operator → (Governance Gate) → Future Broker Integration must be represented **and blocked**: any
  attempt to traverse it (call an execute/connect path) must raise a governance/`NotImplemented`-class
  error, be logged (redacted), and be covered by a **test proving the gate refuses**.
- ❌ **No broker-specific logic outside the External Integration System** (05 v2.0 §16). MT5 types,
  enums, and error codes must not appear in Market Intelligence, Trading Intelligence, Application
  Services, or the UI. Inner subsystems see only the neutral contract.
- ❌ **No secrets/credentials in code, config defaults, logs, metrics, or the repo** (05 v2.0 §77;
  W1-U02 redaction standard). No broker password/login/server/API key committed or logged. Any
  future-credential field must be a placeholder documented as "not used in this unit."
- ❌ **No new markets, no ML/AI, no chart features, no new product behavior.** Canonical markets (§5)
  unchanged. This unit changes *structure*, not *capability*.
- ❌ **No regression** of any approved capability (Wave-0 + W1-U01 + W1-U02): enforced secret,
  non-default bootstrap, refresh rotation, WS tickets, endpoint auth, tz-aware UTC, structured
  logging + redaction + correlation IDs, metrics/health, CI gate.
- ✅ **Preserve:** advisory/research-first posture, single-uvicorn, canonical 05 v2.0 boundaries, single
  ownership, dependency-inward, interface-based Core Platform Services, and all prior hardening.

> **The success test of this unit is that AXIOM is now *ready* to integrate a broker in the future,
> while being *provably incapable* of doing so today.**

---

## 3. Scope — Components A–F

### Component A — Broker Adapter Port / Interface (05 v2.0 §8, §13, §16)
Define, inside the External Integration System (its own bounded context), the **broker port** — the
single interface any broker adapter must implement. It should express the *shape* of future capability
without enabling it, e.g.:
- lifecycle: `connect()` / `disconnect()` / `is_connected()` — **contract signatures only**; the
  reference implementation must be a no-op/disabled stub;
- capability discovery: `describe_capabilities()` (returns a capability descriptor: which markets,
  whether execution is supported — always `execution_enabled=False` this unit);
- read-shaped surface (for *future* use): `get_instruments()`, `get_account_info()`,
  `get_quote(symbol)` — defined in the interface, but the reference adapter returns "not available"
  / raises a documented disabled error;
- execution-shaped surface (defined so it can be *gated*, never used): `place_order(intent)` /
  `cancel_order(id)` — present in the interface **only** so the Governance Gate has something concrete
  to refuse; the reference adapter and the gate both **reject** these unconditionally.

Interface must be pure (no concrete broker import at the port level), documented, and independently
testable. Dependencies point inward toward this abstraction (§16).

### Component B — Boundary Domain Models / Anti-Corruption DTOs (05 v2.0 §12, §16)
Neutral, broker-agnostic data types at the boundary: `Instrument`, `BrokerAccount`, `BrokerQuote`
(inert, not wired to the live feed), `OrderIntent` (inert — a description of a hypothetical order, with
**no** dispatch path), `BrokerCapabilities`, and a typed error hierarchy
(`BrokerDisabledError`, `BrokerNotConnectedError`, `GovernanceGateClosedError`). These constitute the
anti-corruption layer: MT5-native vocabulary is **mapped** here and must not escape the subsystem.
Timestamps tz-aware UTC (W1-U01). No secrets in any model's repr/serialization (§77).

### Component C — `NullBroker` / Disabled Reference Adapter (the proof the seam is inert)
A concrete adapter that **implements the full port** but performs **zero I/O**:
- `connect()` → raises `BrokerDisabledError` (or returns a disabled status), logs a redacted, correlated
  line, and **never** opens a socket;
- all read methods → documented "disabled in this unit" behavior;
- all execution methods → **refused** (see Component D).
This adapter is what the platform is wired to today. It exists to prove the contract is real and
testable **without** any broker present. (An MT5-*named* adapter class MAY exist as a **skeleton that
only maps types and immediately delegates refusal to the gate** — but it must contain **no live MT5
call**; if in doubt, ship only `NullBroker` and leave MT5 as documented TODO.)

### Component D — Constitutional Governance Gate (05 v2.0 §15) — CLOSED & ENFORCED
A single, explicit chokepoint representing "(Constitutional Governance Gate) → Future Broker Integration
(Roadmap Controlled)". In this unit it is **hard CLOSED**:
- any call that would connect a real broker or dispatch an order routes through the gate;
- the gate checks a governance flag that is **False and not operator-overridable via ordinary config**
  (execution is Wave-6-gated; a dev env var must **not** be able to open it — document this explicitly);
- when traversal is attempted, the gate **raises `GovernanceGateClosedError`**, logs a redacted,
  correlated WARNING, and increments a metric (e.g. `governance_gate_refusals_total`) if the metrics
  surface from W1-U02 is available.
- **A test must prove the gate refuses connect and refuses execute**, and that no code path can reach a
  broker with the gate closed.

### Component E — Wiring, Registration & Governance Register Sync
- Register the broker port + `NullBroker` via the existing DI/service wiring so inner subsystems depend
  on the **interface** only (§16). Confirm (by test + a grep-style structural check) that **no MT5 or
  broker-specific symbol appears outside the External Integration System**.
- **ADR** documenting the adapter/port + anti-corruption design and the gate-closed decision.
- **`RISK_REGISTER`:** add/confirm a risk entry for "future broker execution enablement" with the
  mitigation = Governance Gate + Wave-6 gating. Also address the carried **TD-012** (frontend `npm ci`
  5 vulnerabilities incl. 1 critical/1 high) — risk-assess and schedule (see Component F carryover).
- **`TECHNICAL_DEBT_REGISTER`:** record deferrals (real MT5 adapter, live quotes, execution simulator →
  Wave 6) and any skeleton left as TODO.
- Update `PROJECT_STATE`, `GOVERNANCE_AMENDMENTS` (if the gate introduces a standing rule),
  `04_PROJECT_ROADMAP` progress (MT5 integration **framework** delivered — connection/execution NOT).

### Component F — Verification & Delivery (+ two carried Wave-1 items)
- **New tests (all must pass):** port conforms; `NullBroker` opens no I/O; boundary DTOs
  serialize/deserialize with tz-aware UTC and **no secret leakage**; **gate refuses connect**; **gate
  refuses execute**; **structural test: no broker-specific symbol outside External Integration**.
- **Full existing suite green:** backend **81** / frontend **16** baseline (from W1-U02) — **0 failed**,
  no regression — **plus** the new tests.
- **Carried W1-U02 residuals to close/advance in this unit:**
  - **OBS-2 (green CI *run*):** deliver the **real green pipeline run** (log/screenshot) that was owed —
    alembic-on-PG / pytest / vitest / tsc / ruff — so the CI gate is proven by execution, not manually.
  - **TD-012:** risk-assess the critical/high frontend vulnerabilities in `RISK_REGISTER` and either
    remediate or record a scheduled, justified mitigation (do not silently carry a *critical*).
- Delivery Report per §5.

### Explicitly OUT of scope (defer to the debt register; Wave 6 unless noted)
Real MT5 terminal connection; live broker quotes/streaming; account login; order placement /
cancellation / modification (real, demo, or paper); execution simulator; risk engine; position
management; trade replay; paper trading; any broker credentials handling. TradingView deepening and new
markets are also out (separate units). None of these may appear as a *working* path in this unit.

---

## 4. Success Criteria (Definition of Done)

- [ ] Broker **port/interface** exists inside the External Integration System (own bounded context),
      pure and independently testable (05 v2.0 §8/§13/§16).
- [ ] Neutral boundary DTOs + typed error hierarchy (anti-corruption); tz-aware UTC; no secret leakage.
- [ ] **`NullBroker`/disabled reference adapter** implements the full port with **zero I/O** and opens
      no connection (proven by test).
- [ ] **Constitutional Governance Gate is CLOSED and enforced:** connect **and** execute are refused;
      no dev/config override can open it; refusal is logged (redacted, correlated) — proven by test.
- [ ] **No broker-specific symbol outside External Integration** (proven by structural test/check).
- [ ] **No broker connection, no execution, no orders, no credentials** anywhere (proven by review +
      tests + the DA's own negative evidence).
- [ ] Registers/ADR/PROJECT_STATE/roadmap synced; TD-012 risk-assessed; deferrals recorded.
- [ ] **OBS-2 closed:** a real green CI run covering all gates against PostgreSQL is provided.
- [ ] Full suite green (backend 81 / frontend 16 + new tests); single-uvicorn preserved; advisory-first
      + all prior hardening intact; conforms to 05 v2.0 (§5/§8/§12/§13/§15/§16/§17/§77).

---

## 5. Delivery Report & Evidence Requirements (MANDATORY — operator-run, target platform)

Per the reinforced standard (sandbox-green ≠ target-proven; a runtime traceback in evidence overrides any
report claim; a failing test inside the evidence is a finding, not a footnote). Provide **operator-run,
Windows/PowerShell + PostgreSQL** evidence:

1. **Operator test console** (raw, `collected N`): backend `pytest`, frontend `vitest`, `tsc`, `ruff` —
   **0 failed**, no regression from **81 / 16** + the new tests. The gate-refusal and no-I/O tests must
   be visible in the run.
2. **Gate-closed evidence:** console/test output showing an attempted **connect** and an attempted
   **execute/place_order** are **refused** (`GovernanceGateClosedError`/`BrokerDisabledError`), with the
   corresponding **redacted, correlated log line** — and confirmation the refusal metric incremented (if
   metrics available).
3. **No-I/O / no-connection evidence:** proof the disabled adapter opens no socket/network — e.g. the
   test asserting no connection is attempted, and (ideally) confirmation that the `MetaTrader5` client is
   **not invoked** (import-guarded / not called).
4. **Boundary-containment evidence:** a grep-style search showing **no MT5/broker-specific symbol**
   (`MetaTrader5`, `mt5.`, broker enums) **outside** the External Integration System. *(R7: a blank grep
   is only a pass when the search is correct and shown — paste the exact command and its output.)*
5. **No-secret evidence:** grep proving no credential/login/password/API-key literals in the new code or
   config, and none in logs (extend the W1-U02 redaction pattern).
6. **OBS-2 CI evidence:** a **real green pipeline run** (log/screenshot) covering alembic-on-PG / pytest /
   vitest / tsc / ruff, failing on any failure.
7. **Parity smoke (no regression):** login → WS ticket 200 → live feed → candle fetch, unaffected by the
   new seam.
8. Confidence stated **HIGH / MODERATE / LIMITED with justification — NO fabricated percentages.**

---

## 6. Standards & Constraints

Clean architecture: bounded context + **single ownership** (05 v2.0 §12/§13); **dependency-inward**,
interface-based, no circular deps, **no shared mutable state** (§16); **broker-specific logic ONLY in
External Integration** (§16); **plugin-ready** for future brokers (§17); execution behind the
**Constitutional Governance Gate**, Roadmap-Controlled (§15). **No secrets in code/telemetry** (§77);
tz-aware UTC (W1-U01); structured logging + redaction + correlation from W1-U02 reused (never
re-implemented). Every change recorded in the debt/decision/amendment registers. Cross-platform
(Windows + docker/PostgreSQL).

---

## 7. Process

Implement → internal verify → doc sync (PROJECT_STATE + registers + ADR + roadmap) → Delivery Report with
§5 evidence (operator-run, green, **gate proven closed**, no failing tests) → **submit to ITRGA** →
independent review → corrections if required → approval → next Build Order. **The DA does not
self-approve, does not self-authorize the next unit, and does not open the Governance Gate.**

---

## 8. Priority Guidance (if staged)

**A (port/interface) → B (boundary DTOs + errors) → D (Governance Gate — CLOSED & enforced) →
C (`NullBroker` disabled adapter) → E (wiring + registers/ADR) → F (verification + OBS-2 CI + TD-012).**

The **Governance Gate (D)** is the highest-risk, highest-value item in this unit and must be built and
proven *before* any adapter surface is wired, so there is never a window where a broker path exists
without a closed gate in front of it. Redaction and boundary-containment (no MT5 symbols outside the
subsystem) are the next-highest risks.

---

*ITRGA — Build the door and the lock before you build anything that could walk through it. The framework
must make future broker integration **possible**; this unit must make present broker execution
**impossible**. We don't guess. We prove.*
