# ITRGA-REQ-V2-BE-7-PLAN-001 — Band BE-7 review contract (Design-Plan Request + REQ checklist)

| Item | Value |
|---|---|
| From | ITRGA |
| To | Development Authority (DA), via the Operator custody channel |
| Date | 2026-09-03 |
| Authority | Operator BE-7 authorization of 2026-09-03, recorded in `ITRGA-CN-V2-BE-7-001` |
| Roadmap basis | `AXIOM-V2-BE-ROADMAP-001`, Band **BE-7 — Backtesting, Simulation, Replay, and Governed Research Jobs** (in-repo custody copy `uploads/V2_BACKEND_ROADMAP.md` §"Band BE-7", lines 281–312; verified present this session). The band contract is quoted in full in §0 below so the review is anchored to the authoritative text. |
| Request to | the DA: author the **Band BE-7 design plan** (`AXIOM-V2-BE-7-DA-PLAN-001`) answering REQ §1.1–§1.13 item-for-item, honouring Pins P-1…P-10, and closing with the boundary restatements. Transmission via the Operator custody channel, document-only, credential-scanned (§3). |

This contract authorizes nothing beyond planning. Implementation begins only under the issued Build Order, per the delivery model.

## 0. Band contract (roadmap text, verbatim)

**Objective.** Build reproducible, non-live strategy/simulation capabilities before any paper-order lifecycle.

**Scope.** (i) historical replay with as-of boundaries; (ii) backtest input/version registration; (iii) transaction-cost, spread, slippage, latency, and risk-model configuration; (iv) temporal-leakage prevention; (v) strategy-version lifecycle metadata; (vi) governed research job queue: owner, authorization, inputs, schedule, output, failure, audit; (vii) immutable research-result and replay artifacts.

**Controls.** (i) Backtest, simulation, paper, and live results are different typed result classes. (ii) No scheduled job may silently mutate an institutional artifact or interact with an execution adapter. (iii) Job retries must be idempotent and audited.

**Exit evidence.** (i) future-leakage tests; (ii) deterministic replay tests; (iii) queue/retry/cancel/failure evidence; (iv) result classification and lineage tests; (v) no-live-effect source/API scan.

## 1. REQ checklist (the review contract)

- **REQ-1.1 Decomposition and unit structure.** Units listed with dependencies; each migration unit single-purpose; chain continues at revision **`20260903_0046`** — next revision number `0047` (date prefix assigned at issuance; `down_revision = "20260903_0046"`). Per migration unit: exact DDL (tables/columns/types/constraints/indexes); guard triggers with exact refusal-message strings; permission seeds SAL-aligned with projected global totals; data seeds (declared, "none" allowed); downgrade posture; post-unit drift declaration (exactly the 9 inherited V1 tokens, zero band tokens) and pinned totals before→after (v2 triggers 32 · permissions 41 · compver 6 · tests 911, per `ITRGA-DET-V2-BE-6-CLOSE-001`).
- **REQ-1.2 Historical replay with as-of boundaries.** The as-of model: boundary semantics, writer-enforced no-future rules, replay-window inputs, and replay determinism (same inputs ⇒ identical replay, byte-comparable summaries). Replay artifacts immutable with determinism anchors (REQ-1.9). Declare precisely what is consumed from the V1 snapshot/temporal-split lineage (W2-U04) versus built new.
- **REQ-1.3 Backtest input/version registration.** Versioned-immutable input registry: logical id + version, content-addressed dedupe/idempotency anchor, lineage to the BE-2 market-data read models actually consumed (declared tables, declared as-of discipline), and typed registration outcomes. No silent input mutation — any change is a new version.
- **REQ-1.4 Cost-model configuration contract.** Transaction-cost, spread, slippage, latency, and risk-model configuration as **declared data with citations** — constants cited from existing V1/V2 config where they exist, band-level-declared with unit and source otherwise; **no invented numbers presented as spec values**. Application of the cost model is pure and deterministic; configuration versions are immutable and referenced by every result.
- **REQ-1.5 Temporal-leakage prevention (structural — P-8).** Leakage guards made structural, not documentary: as-of cutoffs enforced at input assembly; feature-availability windows; label-horizon/embargo rejection; adhered-to ordering of decision timestamps vs data timestamps, with the ordering enforced in code paths the plan names. Enumerate the planned **future-leakage tests** (exit-evidence item 1) per guard.
- **REQ-1.6 Strategy-version lifecycle metadata.** Versioned-immutable strategy registration (`record_seq` + `supersedes` vocabulary continuity from BE-6; currency = greatest `record_seq`; UNIQUE on (logical id, record_seq)); typed-permanent lifecycle states; strategy metadata never carries credentials or execution bindings.
- **REQ-1.7 Governed research job queue.** Job model carrying exactly the contract fields — owner, authorization, inputs, schedule, output, failure, audit — plus attempt ledger; **idempotent retries** (attempt-indexed write anchors; a retry never double-applies an artifact); typed cancel semantics; every state transition audited with actor and reason. **Decide the message-queue technology** (`V2_ARCHITECTURE_PRINCIPLES.md` row 89: "depends on research job requirements" — the plan must choose: in-process / database-backed / other, and justify against RESEARCH-mode constraints; no external service, no new infrastructure credential).
- **REQ-1.8 Typed result classes (control — P-9).** Four typed classes — `backtest`, `simulation`, `paper`, `live` — with **only backtest and simulation constructible in this band**; `paper`/`live` are typed refusals at every construction point. Result rows carry their class structurally (CHECK single-value or closed-set as designed).
- **REQ-1.9 Immutable artifacts + determinism anchors (P-2).** Backtest/simulation/replay artifacts immutable; UNIQUE determinism anchor over (subject reference, inputs hash, engine-versions hash) with idempotent return (same inputs+versions ⇒ existing artifact); `engine_versions`/`engine_versions_hash` on every artifact (P-4); compver seed rows for each new engine with the C-2-style disclosure (application-act instrument re-pins engine files at run time).
- **REQ-1.10 The job-silence control made structural.** "No scheduled job may silently mutate an institutional artifact or interact with an execution adapter": the plan states the enforcement design (e.g., declared writable-table allow-list per job writer, guard triggers on artifact tables, no code path from job writers to any execution/adapter surface — including V1 live adapter modules — with the import/dependency scan that proves it) and the scheduled-trigger model within RESEARCH mode (tick source declared; no production/infra scheduler in scope).
- **REQ-1.11 Mode/audit/security.** BE-1 columns on every row (mode, operator_id, correlation_id, created_at); audit events enumerated (registration, job lifecycle, artifact creation, refusals); lineage rows joining results to inputs and literature (input registry ids, strategy versions, artifact ids); RBAC SAL-aligned with `denied` as a typed state; redaction gate untouched; the band prompts for no credential — stated.
- **REQ-1.12 Data honesty.** Six-class taxonomy on all new tables carrying data-class; first landing restricted to `synthetic`/`simulated`; `historical_real`/`live` refused with typed reasons (V2-TD-18 continuity); every evidence outcome declares its tier (pipeline-validation vs research-validation); no backtest/simulation result may be presented as live or future performance.
- **REQ-1.13 Test plan and worked-sample annex.** Fail-first per unit; declared per-unit budgets and projected floor from **911**; migration-up content tests in the 0043/0046 pattern; guard messages verbatim; CHECK-vocabulary probes (incl. result-class probes); versioning/idempotency/concurrency (duplicate-submit, retry races); the **exit-evidence set named per contract**: future-leakage tests; **deterministic replay tests backed by a worked-sample annex** (pinned synthetic series + pinned configuration + pinned expected outputs to stated precision — sufficient for the ITRGA to replay independently without executing the engine, P-7 continuity); queue/retry/cancel/failure evidence; result-classification + lineage tests; **no-live-effect source/API scan** methodology declared; socket/no-network guard.

## 2. Pins

P-1…P-7 carry unchanged from the BE-6 chain (versioned-immutable lineage; determinism anchors on immutable artifacts; typed permanent outcomes + six-class honesty; computation provenance via compver/version pins; structural proof over vocabulary; hypothetical-only structural guarantee; independent recomputation). BE-7 adds:

- **P-8 (temporal-leakage structural guarantee):** leakage prevention exists in enforced structure (as-of cutoffs, availability windows, horizon rejection) — provable by probes and future-leakage tests, not claims.
- **P-9 (result-class separation):** backtest/simulation vs paper/live separation exists in types, CHECKs, and construction points — provable by construction scans and typed refusals; no live-effect surface is constructible in this band.
- **P-10 (job idempotency and auditability):** every scheduled-job effect is attempt-idempotent and audit-lined; duplicates, retries, and cancels are provably side-effect-safe.

## 3. Custody and next acts

Document-only channel; no commits by DA or ITRGA (all commits belong to the Operator); credential scan before every transmission; the DA's plan arrives via the Operator. On a verified plan: ITRGA issues the Build Order under the existing authorization; implementation, evidence, Delivery Report, determination follow per unit, gated. The working-DB application of 0047 is a separate sanctioned act at chain end (instrument lineage per 0043/0045/0046, including the E-0046-DUP startup rule).

— ITRGA, 2026-09-03
