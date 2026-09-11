# AXIOM V2 — Risk Register

| Field | Value |
|---|---|
| Document ID | AXIOM-V2-GOV-RISK-001 |
| Status | Active |
| Date | 2026-08-24 (updated by replacement DA — BE-1 remediation, DR-004) |
| Author | Development Authority (DA) |
| Build Order | BO-V2-BE-0-001; updated under BO-V2-BE-1-001 correction cycle |

---

## Risk Classification

| Severity | Definition |
|----------|------------|
| Critical | Could cause data loss, security breach, or production failure |
| High | Could cause significant functional or governance issues |
| Medium | Could cause moderate issues; manageable with discipline |
| Low | Minor risk; awareness sufficient |

---

## V2 Risk Register

| ID | Risk | Severity | Status | Mitigation | Band |
|----|------|----------|--------|------------|------|
| V2-R-01 | V2 scope creep beyond authorized band | Medium | Open | Strict exclusions per band; ITRGA review | All |
| V2-R-02 | V1 regression during V2 development | High | Open | V1 regression baseline captured; continuous regression testing | All |
| V2-R-03 | V2 architecture too rigid for future changes | Low | Open | Non-binding future candidates clearly marked; deferred decisions documented | BE-0 |
| V2-R-04 | Operator delays V2 Programme Charter | Medium | Open | DA cannot proceed without adoption; charter is Operator-owned | BE-0 |
| V2-R-05 | V2 documentation becomes stale | Low | Open | V2 Current State tracks programme state | All |
| V2-R-06 | Provider credential exposure | Critical | Deferred | Credential vault; never in API/logs/frontend | BE-3 |
| V2-R-07 | Broker credential exposure | Critical | Deferred | Credential vault; never in API/logs/frontend | BE-9 |
| V2-R-08 | Execution without authorization | Critical | Deferred | Default-deny; explicit authorization chain | BE-10 |
| V2-R-09 | Fabricated market data | High | **Mitigated (BE-2)** | Source provenance mandatory; integrity validators (ordering/duplicate/gap/stale/future/unmapped) with fingerprint-deduplicated quarantine; gaps disclosed never filled; no-future-data rule (DR AXIOM-V2-BE-2-DR-001) | BE-2 |
| V2-R-10 | Fabricated account state | High | Deferred | Authoritative broker read; reconciliation | BE-9 |
| V2-R-11 | AI prompt injection | High | Deferred | Input sanitization; output constraints; audit | BE-11 |
| V2-R-12 | Cross-mode data leakage | High | **Mitigated (BE-1)** | Mode-tagged queries; RBAC enforcement; server-side `AXIOM_V2_MODE` only; injection-refusal proven by API test (DR-004) | BE-1 |
| V2-R-18 | Cross-operator data disclosure via V2 read APIs | High | **Mitigated (BE-1)** | Server-side operator scoping at query level; two-operator API/DB isolation tests; admin `read_all` permission-gated and audited (DR-004) | BE-1 |
| V2-R-19 | Secret material persisted in V2 audit records | High | **Mitigated (BE-1)** | R-9.4 write-time refusal of secret/unknown classifications; redaction of value-borne secrets; refusal of unredactable key-borne secrets (DR-004) | BE-1 |
| V2-R-20 | V2 internal error leakage (stack traces/internal detail to client) | Medium | **Mitigated (BE-1)** | V2-scoped internal-error containment middleware; leak-free 500 proven by API test (DR-004) | BE-1 |
| V2-R-21 | PostgreSQL residual verification gap (post-downgrade trigger absence, native mutation refusal — PG-002 §4) | Medium | Open (Operator-run) | Operator executes existing command pack on dedicated verification DB | BE-1 |
| V2-R-22 | BE-2 PostgreSQL verification | — | **Closed** (ITRGA-DET-V2-BE-2-001 §2: Operator PostgreSQL 18.4 evidence verified; gate closed for reviewed source state) | Revalidation trigger remains per OBS-V2-BE2-05 | BE-2 |
| V2-R-23 | V1 candle mutability limits verification records to tamper-detection (no reconstruction) | Medium | Accepted (design; OBS-V2-BE2-01) | Truthful Option B contract (`reconstructive: false`); mismatch detection + deduplicated exception; reproducible snapshot storage deferred to future authorized band | BE-2 |
| V2-R-24 | PostgreSQL credential exposed in submitted Operator evidence transcript | Medium | **Open — Operator action** (OBS-V2-BE2-04) | Rotate credential if active; pre-redacted evidence templates adopted for all future packs | BE-2 evidence |
| V2-R-25 | BE-3 provider entitlement assumptions | — | **Partially closed (P2)**: bounded-evaluation entitlement VERIFIED via ITRGA-DET-V2-BE-3-P2-ENT-001 (Basic plan evidence); data-rights/persistence/redistribution remain NOT PROVEN and `persistence_permitted=false` | Recorded values live only in the governed migration | BE-3 P2 |
| V2-R-27 | BE-3 P2 PostgreSQL verification outstanding — NETLESS-001 §4 fresh-chain scope (incl. 0038→0040 P2-permission absence proof, since 0038 source changed) | High until closed | Open (Operator-run) | Pre-redacted output; execution checklist gated on it | BE-3 P2 |
| V2-R-28 | Live provider behavior unverified until the Operator's single bounded contract-test run | Medium | Open (gated) | Run authorized only after ITRGA accepts the non-network delivery; ≤35 attempts; no payload persistence; credential Operator-only | BE-3 P2 |
| V2-R-26 | BE-3 P1 PostgreSQL verification | — | **Closed** (ITRGA-DET-V2-BE-3-P1-FINAL-001 §2.2: full corrected-migration lifecycle proven on PostgreSQL) | Revalidation trigger remains for any future BE-3 schema/model/metadata/trigger change | BE-3 P1 |
| V2-R-29 | BE-4 synthetic-input evidence mistaken for market validation | Medium | **Mitigated (BE-4 CLOSED — ITRGA-DET-V2-BE-4-FINAL-001)** | `validation_tier="pipeline-validation"` stamped on every report artifact + DR declaration; epistemic notes in interpretations; no market conclusion claimed anywhere (DR AXIOM-V2-BE-4-DR-001) | BE-4 |
| V2-R-30 | BE-4 report immutability bypass | Medium | **Mitigated — guards IN FORCE on the working DB** (0043 act closed: 6 R-2 refusals proven twice, A6 + B7; 18 v2 triggers) | 6 R-2 DB guard triggers (verbatim-message tested) + append-only repositories + no-touch group; v2 trigger set 12→18 proven | BE-4 |
| V2-R-31 | Cross-timeframe over-claiming (unsupported conclusions) | Medium | **Mitigated (BE-4)** | R-4 fixed rule table enforced in the single typing gate; refusal cases tested at every class boundary; zero prediction/statistical emissions | BE-4 |
| V2-R-32 | 0043 working-DB apply act: single sanctioned mutation risk | Medium | **Closed** (ITRGA-DET-V2-0043-APPLY-001: single mutation executed and verified; anchor retained; T-1…T-11 all VERIFIED) | Battery was predictive (F1/F2 both decisive in production) | 0043 act |
| V2-R-33 | Signal truthfulness on synthetic data mistaken for market validity | Medium | **Mitigated (BE-5)** | 6-class data taxonomy on every artifact; historical_real/live refused with typed reasons at first landing; pipeline-validation tier declared (DR AXIOM-V2-BE-5-DR-001) | BE-5 |
| V2-R-34 | ML governance-writer bypass (promotion outside the governed path) | Medium | **Mitigated (BE-5)** | Full-immutability triggers (P-1) + single SAL-3 writer + append-only lifecycle events + audit; direct SQL refused by DB guards | BE-5 |
| V2-R-35 | Hypothetical portfolio/risk research mistaken for account state | Medium | **Mitigated (BE-6)** | Single-value basis ('hypothetical') and basis_label ('hypothetical-research') CHECKs, probed behaviorally; label on every artifact and response; forbidden account/order/position vocabulary guard green | BE-6 |
| V2-R-36 | Risk-metric overtrust (computed number read as market truth) | Medium | **Mitigated (BE-6)** | Full risk-metric contract mandatory per metric (method, citation, uncertainty, limitations, time_basis); both VaR methods reported separately, never merged; typed 'insufficient' instead of fabricated values | BE-6 |
| V2-R-37 | Scheduled-job silent mutation / execution-adapter reach | Medium | **Mitigated (BE-7)** | Writable-table allow-list (test-asserted); import scan with extended token predicate (trading_intelligence, adapter); no tick source in v1 (manual invocation only); 10 DB guards (DR AXIOM-V2-BE-7-DR-001) | BE-7 |
| V2-R-38 | Backtest/simulation results mistaken for paper/live performance | Medium | **Mitigated (BE-7)** | `paper`/`live` schema-impossible (CHECK) + typed refusals at construction points; mandatory performance_disclaimer on every result; four-class taxonomy with closed constructible set | BE-7 |
| V2-R-39 | Paper fills/P&L mistaken for real or broker-confirmed performance | Medium | **Mitigated (BE-8)** | N4 structural: fill_class CHECK single value 'paper_simulated' (no broker column exists); unconditional disclaimer on every response; zero broker vocabulary in the domain (scans) | BE-8 |
| V2-R-40 | Risk-gateway bypass (order executes without a pass decision) | Medium | **Mitigated (BE-8)** | Default-deny derived rule (may_execute, owned once); uq(intent_id) decision anchor (exactly-once as schema fact); append-only event ledger with exhaustive transition vocabulary; C-1d block confirmation-proof | BE-8 |
| V2-R-13 | Replay/duplicate orders | High | Deferred | Idempotency keys; duplicate detection | BE-8/10 |
| V2-R-14 | Stale data presented as live | Medium | **Mitigated (BE-2)** | Mandatory provenance block + display labels on every data response; read-time freshness; active-authority guard + DB CHECK bound vocabulary to simulated/synthetic/unknown (DR AXIOM-V2-BE-2-DR-001) | BE-2 |
| V2-R-15 | Paper/live mode confusion | Critical | Deferred | Server-side mode; unmistakable UI; isolation proof | BE-8 |
| V2-R-16 | V1 production not certified | High | Inherited | V2 cannot claim production status | All |
| V2-R-17 | V1 governance gate CLOSED | High | Inherited | V2 must maintain gate closure | All |

---

**End of Risk Register**
