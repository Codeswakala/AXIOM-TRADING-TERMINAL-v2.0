# AXIOM — OPERATOR DECISION RECORD
## Predictive Track: Deferral to Operational Readiness

| Item | Value |
|------|-------|
| Decision authority | **Operator** |
| Recorded by | ITRGA (governance record, not a determination) |
| Date | 2026-08-20 |
| Status | **ACTIVE** |

---

## 1. The decision (Operator, verbatim intent)

> "I'll stick with the negative status for now, further trials will be made when the project is operational with a full working UI."

Interpreted and recorded as:

1. **The predictive ML track's current status is accepted as a governed negative.** No model has been promoted; the fail-closed gate's refusals stand. This is a legitimate, twice-established research outcome (B-ML, B-ML2).
2. **No further predictive-ML Build Orders will be issued at this time.** The track is **deferred**, not terminated.
3. **Resumption condition:** further predictive trials resume **after** the project is operational with a full working UI — i.e. after the remaining backend and frontend units deliver a functioning terminal.

## 2. Consequential governance state

- **B-03 (predictive advisory signals) remains gated** — correctly, since no promoted model exists. It stays gated until a future trial promotes one.
- **No approved work is invalidated.** B-00 → B-ML2 all remain APPROVED WITH OBSERVATIONS. This decision operates forward only.
- **The threshold gate, tier rule, and research-integrity disciplines remain binding** for any future trial (they are the reason the negative is trustworthy, and they will be re-applied unchanged).

## 3. Housekeeping closed

- **OBS-BML2-1 closed** — the B-ML2 fail-first probe log has been relayed and verified against its declared hash (`e42ffff5…`). The full B-ML2 evidence set is now complete.
- **Standing corrective action CA-TRANSMIT-1 (relay-step integrity) remains open** — six consecutive deliveries exhibited declared-but-untransmitted artifacts. The relay must be fixed before the remaining units are reviewed, to avoid re-litigating transmission on every delivery.

## 4. Forward path (independent of any promoted model)

The Operator's "full working UI" condition is achievable **without** predictive ML, because the remaining units do not depend on a promoted model (verified in the Reconciliation Determination):

| Unit | Depends on promoted model? | Purpose |
|------|---------------------------|---------|
| B-04 Institutional Intelligence (correlation/regime/scenario/portfolio-risk/signal-validation) | **No** — deterministic computation | wire the already-written generation services |
| B-05 Monitoring & Alerts | **No** | wire drift/health/staleness/withheld alert emission |
| B-06 Governed Assistant ask path | **No** | expose the rule-based responder over HTTP + input surface |
| B-07 Cross-cutting hardening | **No** | observability, security, rate limiting, performance |
| F-00 → F-06 Frontend | **No** (F-02 split: structural signals render independently of predictive) | hygiene, assistant input, structural-signal presentation, intelligence/alerts/lineage, a11y/perf |
| X-01 End-to-end verification | **No** | the operator workflow proof, with structural (not predictive) intelligence |

**The primary intelligence of the operational terminal will be the deterministic market-structure layer** (BoS/CHoCH/FVG/OB/structure/swings — already operational), with predictive ML clearly-labeled and gated, and absent until a future trial justifies it.

## 5. Recommended next Build Order

**B-04 (Institutional Intelligence generation)** — the next unit on the backend critical path that is unblocked. It wires the already-written `create_report` services (correlation, regime, scenario, portfolio-risk, signal-validation) to governed generation endpoints, turning the currently-empty read-only surfaces into live, uncertainty-bearing, as-of-bounded research artifacts.

> **We don't guess. We prove.** The predictive track's negative is now the recorded, accepted state — deferred, not abandoned — and the programme proceeds toward a fully working terminal on the strongest foundation it has: honest, deterministic, professional market analysis.

**End of Operator Decision Record**
