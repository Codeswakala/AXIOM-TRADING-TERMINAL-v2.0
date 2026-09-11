# AXIOM BUILD ORDER — W3-U04

## Live Research Advisor: Live Market Inference Adapter (as-of / no-look-ahead live scoring — no UI/execution)

**Build Order ID:** W3-U04
**Wave:** 3 — Live Research Advisor · **Unit:** 04
**Version:** 1.0 · **Status:** ISSUED
**Authority:** ITRGA · **Date Issued:** 2026-07-15
**Authorized By:** ITRGA, following **W3-U03 APPROVED** (Platform v0.25.0; emit-time guardrails + staleness)
+ operator authorization ("authorized").

**Governing Documents (canonical order — `10_CONSTITUTIONAL_HIERARCHY`):**
`00_VISION` → `03_AXIOM_SPEC` → `04_PROJECT_ROADMAP` (Tier 3) → **`05_SYSTEM_ARCHITECTURE` v2.0 (Tier 4)**
→ **`07_ML_SPEC` (Tier 5)** → `08/09` frameworks (Tier 6) → Tier-7 registers → this Build Order (Tier 8).
**Binding decision:** `docs/ITRGA_WAVE2_GOVERNANCE_DECISION_LOG.md` (D-W2-001).
**Builds on:** W3-U01 (eligibility gate + deterministic engine) + W3-U02 (signal contract/persistence) +
W3-U03 (emit-time guardrails + staleness) + the W0/W1 live-market WebSocket/query seam + W2-U01 chronology
guard + W2-U03 feature store.
**Motto:** *We don't guess. We prove.*

---

## 1. Purpose

Deliver the **Live Market Inference Adapter** — the seam that feeds **live/near-real-time market data** into
the W3-U01 deterministic inference engine (and thence the W3-U02/U03 governed signal path), reusing the
existing **W1 live-market WebSocket/query seam** rather than reinventing transport. The single highest-risk
item is **as-of / no-look-ahead discipline on live data**: at inference time the model may see only
past/current data as of a trustworthy `as_of_time` — the *live* analogue of the W2-U01 chronology guard and
the W3-U03 staleness contract.

Per the accepted Wave-3 plan §5.4 (inference input discipline) and §12.2 (real-time path — reuse the W1 seam,
**no external broker/feed**): this unit connects the live feed to inference **as a research/advisory input**,
deterministically, and **stops before any operator-facing push** (that is W3-U05/U06). It remains
**advisory-only, backend, no UI/alerts/execution.**

---

## 2. Governance Envelope (READ FIRST — violation = automatic FAIL)

- ❌ **No execution / orders / broker connection / paper trading.** W1-U03 Governance Gate CLOSED (R17). The
  adapter feeds *data into inference*; it must not connect to a broker or dispatch anything. Prove by grep +
  structural.
- ❌ **No external broker/feed connection.** Reuse the **existing W1 simulated live-market seam** (ticket-
  based WebSocket / query port). **No new external market-data-provider or broker connection** is introduced
  (plan §12.2) — that would require its own explicit, gated Build Order. Prove by grep/structural + no new
  external egress.
- ❌ **No look-ahead at inference (the headline).** Inference input must be assembled from **only past/current
  data as of a trustworthy `as_of_time`** — no future candle/feature; a candle whose `open_time > as_of_time`
  must be **excluded** from the inference window. Prove by named test (a future candle cannot enter the
  inference input).
- ❌ **No stale live inference.** Reuse the W3-U03 staleness contract: if the freshest available data is older
  than the max as-of staleness, the inference/signal is **withheld (`STALE_INPUT`)**, not scored on stale
  data. Prove by test.
- ❌ **No non-deterministic live scoring.** Same live input (same as-of snapshot) + model version ⇒ same
  score + input hash (§42; W3-U01). No randomness, no mutable model state, no wall-clock leaking into
  features. Prove by test.
- ❌ **No `seed:synthetic`-authoritative or forward-dated `live:simulated`-as-real input** (OBS-1 spirit,
  live); **no symbol identity as model input** (D-W2-001). Carried, proven at the adapter boundary.
- ❌ **No operator UI / alert / live signal push this unit.** The adapter produces inference results (and,
  where governed, persisted signals via the W3-U02/U03 path) — it does **not** push to an operator surface.
- ❌ **No DB reach-around; no secrets** (§16/§77). **No regression** (Wave-0/1 + W2 + W3-U01/U02/U03). Full
  suite + prior tests + parity smoke; live-market seam still green.
- ✅ **Preserve:** advisory/research-first, tz-UTC, observability, deterministic inference, governed
  emission + emit-time guardrails + staleness, inert signal, read-only history API, all prior hardening.
  **Persisted-artifact committing proof (raw `SELECT` + API read-back) first submission** (control holding).

---

## 3. Scope — Components A–F

### Component A — Live market inference adapter (reuse W1 seam) (plan §12.2)
- An adapter that consumes the **existing W1 live-market seam** (simulated live feed via ticket WebSocket /
  the W2-U02 query port) and assembles a **point-in-time inference input** (`as_of_time` snapshot: the
  causal feature window as of that time) for the W3-U01 engine. **No new external broker/feed connection.**

### Component B — As-of / no-look-ahead discipline (the headline — live chronology guard)
- The inference window is built from **only candles/features with `open_time <= as_of_time`**; any future/
  not-yet-closed candle is **excluded**. `as_of_time` is a **trustworthy** anchor (from the feed/ingestion,
  not query-time wall-clock in a way that could admit future data). **Named test:** a future candle present
  in the feed **cannot enter** the inference input; scoring uses only as-of data.

### Component C — Staleness at live inference (reuse W3-U03 R-2)
- If the freshest available data is older than the configured max as-of staleness, the inference/signal is
  **withheld (`STALE_INPUT`)** — no scoring on stale data. **Named test.**

### Component D — Deterministic live scoring + input hash (W3-U01/§42)
- Same as-of snapshot + model version ⇒ **identical score + inference_input_hash.** No randomness/mutable
  state/wall-clock-in-features. **Named test** (score the same snapshot twice → identical).

### Component E — Integration with the governed path + governance
- Route the live inference result through the **W3-U01 eligibility gate + W3-U02 signal contract + W3-U03
  emit-time guardrails/staleness** (so a live signal, if produced, is governed exactly as a batch one) —
  **but still no operator push/UI/alert.** Confirm identity-excluded + `advisory_approved`-only + guardrails
  all apply to the live path.
- **ADR:** *Live Market Inference Adapter*. **Registers:** live-look-ahead / stale-live / external-feed-
  introduced risks mitigated; update `PROJECT_STATE`/`CHANGELOG`; note W3-U05 (UI)/U06 (alerts) deferrals.
- **Persisted proof:** any live-path signal persisted shown via **raw `SELECT` + API read-back** (both,
  first submission).

### Component F — Verification & Delivery
- Full suite green (baseline **177** backend / **16** frontend) — 0 failed, no regression — **plus** new
  tests: **future candle cannot enter inference input (no look-ahead)**; **stale live data → withheld
  (`STALE_INPUT`)**; **deterministic live scoring (twice → same score + hash)**; **no external broker/feed
  connection** (grep + structural); no-execution; identity-excluded; governed path applies to live inference;
  no UI/alert/push added; live-market seam + W3-U01/U02/U03 + broker tests green.
- Delivery Report per §5.

### Explicitly OUT of scope (later Wave-3 / Wave 6)
Operator dashboard/workspace/UI (W3-U05); alerts + live WS signal stream to operator (W3-U06); analytics
(W3-U07); any execution/broker/paper trading (Wave 6); external market-data-provider integration (future
gated). **No UI, no alerts, no operator push, no external feed in W3-U04.**

---

## 4. Success Criteria (Definition of Done)

- [ ] Live inference adapter reuses the **existing W1 seam**; **no new external broker/feed connection**
      (proven by grep/structural).
- [ ] **No look-ahead:** a future candle (`open_time > as_of_time`) cannot enter the inference input; scoring
      uses only as-of data — proven by named test.
- [ ] **Stale live data → withheld (`STALE_INPUT`)** (W3-U03 staleness reused) — proven.
- [ ] **Deterministic live scoring:** same as-of snapshot + version → identical score + input hash — proven.
- [ ] No `seed:synthetic`-authoritative / forward-dated input; no symbol identity as model input.
- [ ] Live inference routes through the governed path (eligibility + signal contract + emit-time guardrails)
      **with no operator push/UI/alert this unit**; gate CLOSED; no execution.
- [ ] Persisted proof (raw `SELECT` + API read-back) for any persisted live-path signal (first submission).
- [ ] ADR + registers synced; full suite green (177/16 + new tests); no regression; W3-U01/U02/U03 + W2 +
      broker + live-market tests still pass; conforms to 05 v2.0 (§6/§15/§16/§42/§77) + `07_ML_SPEC` + D-W2-001.

---

## 5. Delivery Report & Evidence Requirements (MANDATORY — operator-run, target platform)

Operator-run, **Windows/PowerShell + PostgreSQL** evidence:
1. **(If compiled dep) wheel-spike;** else pure-Python + stated.
2. **Operator test console** (raw, `collected N`): backend `pytest` **≥177 + new tests, 0 failed**; frontend
   `vitest 16`; `ruff` clean; `tsc`/build clean.
3. **Migration evidence** (if schema added): clean `alembic upgrade head` on `PostgresqlImpl`, new head.
4. **No-look-ahead evidence (captured `-vv`, headline):** a future candle is **excluded** from the inference
   input; inference uses only `open_time <= as_of_time` data.
5. **Staleness evidence:** stale live data → withheld (`STALE_INPUT`).
6. **Deterministic-live evidence:** same as-of snapshot scored twice → identical score + input hash.
7. **No-external-feed / no-execution evidence:** shown grep (R7) that no new broker/external-feed connection
   and no execution/order path was added; adapter reuses the W1 seam; gate CLOSED.
8. **Governed-path evidence:** the live inference result is subject to eligibility + emit-time guardrails
   (identity-excluded, `advisory_approved`-only); **no operator push/UI/alert added.**
9. **Persisted-PG proof (first submission, both forms):** any persisted live-path signal via raw `psql
   SELECT ≥1 row` + authenticated API read-back.
10. **CI green on PostgreSQL** through completion (marker inline + exit 0).
11. **Parity smoke:** login → WS ticket 200 → live feed → candle fetch, unaffected.
12. Confidence **HIGH / MODERATE / LIMITED with justification — no fabricated percentages.**

---

## 6. Standards & Constraints
Advisory-only; **reuse the W1 live seam, no external broker/feed** (plan §12.2; §15 gate CLOSED); **as-of /
no-look-ahead at live inference** (the headline; W2-U01 chronology + §42 determinism); **stale → withheld**
(W3-U03 R-2); **no identity as model input** (D-W2-001); live path fully governed (eligibility + emit-time
guardrails); **no operator push/UI/alert/execution this unit**; no secrets (§77); tz-UTC; persisted-artifact
committing proof (both forms) first submission. Every change in the registers (R20). Cross-platform.

---

## 7. Process
Implement → internal verify (suite + no-look-ahead + stale + deterministic-live + no-external-feed + governed
path + persisted-PG) → doc sync (PROJECT_STATE + registers + ADR) → Delivery Report with §5 evidence
(operator-run, green, no-look-ahead + determinism + no-external-feed proven, persisted proof both forms) →
**submit to ITRGA** → independent review → corrections if required → approval → next Build Order (W3-U05).
The DA does not self-approve, self-authorize the next unit, push a live signal to an operator surface, or
open the broker gate.

---

## 8. Priority Guidance (if staged)
**A (adapter reusing W1 seam) → B (as-of / no-look-ahead — the headline) → C (staleness reuse) →
D (deterministic live scoring) → E (governed-path integration + no-external-feed proof + ADR/registers) →
F (verify, persisted both forms).** Highest-value/highest-risk: **no look-ahead at live inference** (a live
model that peeks at a not-yet-closed candle silently invalidates every downstream advisory) and **no external
broker/feed connection** (reuse the W1 seam; introducing an external connection is out of scope and
gate-adjacent). *Prove the future candle cannot enter the inference window and no external/broker connection
was added.*

---

## 8b. Gate status
Research/advisory only — live data feeds *inference*, not an operator surface. **No operator UI/alert/push
this unit, no execution (Wave 6), no external feed, broker gate CLOSED.** W3-U05 (Operator Advisory Dashboard
/ Signal Workspace — the first operator-facing UI, carrying design-plan R-3) is the recommended next unit and
needs its own Build Order.

---

*ITRGA — Now the model may score the market as it moves — but only ever as of a trustworthy moment, blind to
any candle that hasn't closed, silent when the data goes stale, deterministic to the digit, and over the
same live seam we already trust — no new broker, no external feed, no operator push. Prove the future cannot
leak into a live inference and no new connection was opened. The platform watches and reasons; it still does
not act, and it does not yet speak to the operator. We don't guess. We prove.*
