# ITRGA DESIGN REQUEST — BAND BE-9: BROKER/EXCHANGE CONNECTIVITY AND ACCOUNT VISIBILITY
# ITRGA-REQ-V2-BE-9-001 · v1.0.0 · 2026-09-05 · AXIOM Trading Terminal v2.0
# From: ITRGA · To: Replacement Development Authority (DA) · Via: Operator
# Basis: V2_BACKEND_ROADMAP "Band BE-9 — Broker/Exchange Connectivity and
# Account Visibility" · BE-8 closed (ITRGA-V2-BE8-0048-CLO-SEAL-001,
# act review ITRGA_ACTREVIEW_V2_BE8_0048; DA register sync staged
# ITRGA-DA-SYNC-V2-BE8-0048-001) · request issued at Operator direction
# 2026-09-05 ("proceed with BE-9; request the design plan").
# DELIVERABLE ASKED: a DESIGN DOCUMENT ONLY. No code, no migration, no
# register edits beyond any DA-side design-doc entry. (Zero-code rule in force.)

## §1 — Mandated objective (roadmap, verbatim)
"Integrate one authorized broker/account provider in a read-first,
reconciliation-first posture."
The design must specify: the broker adapter contract; an encrypted credential
vault and scoped service identity; account, balance, position, order, fill,
and instrument-permission read models; read-side broker-to-AXIOM
reconciliation; discrepancy record/state/ownership; provider/broker
operational health; account RBAC and audit.

## §2 — Non-negotiable controls (from the roadmap's explicit exclusions — each
must be honored STRUCTURALLY, not by convention)
N1. NO order submission in this band. The adapter contract must be incapable
    of expressing a mutation call — read-only verbs at type level; no code
    path from the adapter to any order-submit surface.
N2. NO frontend broker calls. The read models are server-side only; the
    frontend consumes AXIOM v2 API surfaces (BE-1 envelopes), never the
    provider.
N3. NO mixed paper/live accounts. The BE-8 paper domain (sealed 2026-09-05)
    and any broker-sourced account data are disjoint domains by type and by
    storage; no consumer query can read one as the other; no account row
    carries ambiguous provenance (every read-model row pins its source).
N4. NO assistant access to broker credentials. Credentials live only in the
    vault; the assistant, the API layer, logs, error envelopes, drift
    outputs, and test fixtures are structurally credential-blind (risk
    register V2-R-07: never in API/logs/frontend — binding).
Be advised: BE-9 is the FIRST band where AXIOM touches an external party's
system. Read-first is the whole posture (risk register V2-R-10: the broker
is the authoritative account read; AXIOM read models are projections, never
state). RECONCILIATION-FIRST means the reconciliation surface ships in the
same band, not later.

## §3 — Precedent law the design must reuse (prior bands, binding patterns)
- BE-1 contracts: V2Error envelope, generic denials without vocabulary
  leakage, mode/correlation_id/timestamp envelopes, redaction model —
  applied to every new read surface.
- BE-3 P2: status/lifecycle transition governance; append-only and
  immutability discipline for institutional records (discrepancy records
  inherit this law).
- BE-4/5/6: provider patterns — health/latency/staleness surfaces, sealed
  provider registries (structural instantiation law from the provider
  incident), replayable snapshots, freshness/entitlement modeling.
- BE-7: mutation-queue/idempotency patterns and deterministic replay law —
  applied to sync runs (a re-run reconciles identically; every artifact
  carries lineage).
- BE-8 (sealed): paper-domain isolation machinery — mode gating, sealed
  routing registries, structural separation proof obligations — reused for
  the N3 paper/broker separation.
- Compver/seeds law (RPE): append-only compver hash additions, recounts;
  drift-gate cleanliness with witness discipline (the inheritance-witness
  pattern of 0047/0048 remains in force).
- Environment law: no behavior conditional on filesystem/UI state; provider
  selection is config-driven and explicit; sandbox is a configuration, not
  a build.

## §4 — Required design sections (every section mandatory; cite where each
roadmap scope bullet and §2 control is satisfied)
S1  Broker selection & adapter contract: candidate broker/provider
    (sandbox/non-production evidence per §5 E1), capability matrix, the
    READ-ONLY contract surface (methods, payloads, pagination, rate limits,
    error taxonomy mapped to V2Error classes), versioning posture.
S2  Credential vault & service identity: storage scheme (encrypted at rest;
    OS-keystore vs encrypted-file trade table), scoped service identity
    model, unlock/decrypt boundary (which process, when, who), rotation,
    revocation, N4 structural blindness proof for assistant/API/log/test
    surfaces (incl. grep-class audit plan for leak paths).
S3  Read models: account, balance, position, order, fill, instrument-
    permission — table-by-table DDL sketch, provenance pins on every row
    (N3), freshness/staleness fields, immutability/update semantics
    (snapshot vs last-writer vs append-only), compver plan.
S4  Sync & staleness architecture: pull cadence, triggers (manual sync
    command? scheduled?), partial-data law (a half-fetched page must not
    half-land), unavailable/degraded-provider posture, rate-limit respect,
    sync-run lineage and idempotency (§3 BE-7).
S5  Reconciliation (read-side, broker-to-AXIOM): the comparison law
    (authoritative source = broker; V2-R-10), match/mismatch classes,
    cadence, rounding/currency law, provenance of every compared value.
S6  Discrepancy records: state machine (detected → triaged → owned →
    resolved/dismissed-with-reason), ownership model, immutability and
    audit lineage (BE-3 P2 law), RBAC for triage/resolve.
S7  Provider/broker operational health: health surface mirroring BE-4/5/6
    (status, latency, last-success, classifier-visible facts only), outage
    semantics for consumers of the read models.
S8  RBAC & audit: capability/permission rows for the new surfaces
    (view account/balances/positions/orders/fills; run sync; triage
    discrepancy), audit events on every privileged action, denial
    vocabulary review (generic, no leakage toward credential/vault terms).
S9  API surface: versioned v2 routes, BE-1 envelopes, exact refusal classes;
    proof sketch that no route can reach a mutation verb (N1) and none
    proxies to the provider from the frontend (N2).
S10 Migration plan: alembic chain position (single new head after
    20260904_0048 — the sealed BE-8 terminal; recounts 58/57/10 baseline),
    drift-gate cleanliness, downgrade completeness, seeds. (The migration
    itself is authored only after design acceptance + BO; this section is
    the plan, sealed DB reference sha256 1d4005fafe972a775822d93016aefbda
    87c194c6f579a351429f6b6b6a61dd3e.)
S11 Test plan mapped to exit evidence §5 (each evidence item → concrete
    test inventory incl. negative tests: stale, unavailable, mismatch,
    partial-data, credential-leak canaries, replay/idempotency races).
S12 Threat model & security review pre-read: assets (credentials, account
    data, sync integrity), actors, abuse cases (N1–N4 violations, adapter
    substitution, vault exfiltration, replay, split-brain sync),
    mitigations; the ITRGA determination input.
S13 Open questions: each Q1..Q8 in §6 answered with the DA's recommended
    resolution + rationale (roadmap citations prioritized).

## §5 — Exit evidence the design must be able to produce (roadmap, verbatim)
E1 Sandbox or non-production broker contract evidence.
E2 Read-side reconciliation evidence.
E3 Stale, unavailable, mismatch, and partial-data handling.
E4 Entitlement/least-privilege test evidence.
E5 Security review (design supplies the review surface; the determination
   is mine after implementation acceptance).

## §6 — Open design questions (DA must answer in S13)
Q1 Broker identity: which single authorized broker/provider, and what
   sandbox/non-production access is available NOW for E1? If selection is
   not yet made, state the criteria and a recommendation — the design may
   be broker-shaped but must pin the contract surface regardless.
Q2 Vault scheme: Windows DPAPI/machine-store vs OS keychain vs encrypted
   file with operator-held passphrase? Recommend for THIS operator console
   (single Windows workstation posture per the sealed act record), with
   the N4 blindness consequences of each.
Q3 Read-model persistence: full projection tables (auditable, reconcilable,
   stable snapshots) vs pass-through cache? Projection-with-provenance is
   favored; justify any deviation.
Q4 Sync trigger model: operator-initiated sync vs scheduled background?
   Who may trigger, and how is each sync run idempotent and replayable
   (BE-7 law)?
Q5 Discrepancy semantics: what classes exist beyond amount-mismatch
   (missing-on-broker, missing-in-AXIOM, currency, timestamp-window,
   permission-visibility), and what is the ownership/aging/dismissal law?
Q6 Health truthfulness: how does the health surface avoid asserting GREEN
   on stale data (freshness separate from reachability)?
Q7 Degraded-read posture: when the provider is down, do read surfaces
   serve last-good snapshots with explicit staleness banners, or refuse?
   (Last-good-with-banner is favored; decide per surface.)
Q8 Instrument-permission reads: how are "what this account may see/trade"
   modeled and enforced downstream without implying execution capability
   (N1)?
Q9 Vault↔config boundary: where does provider selection (sandbox vs live-
   read endpoints) live so a config error cannot silently repoint reads
   at a different account? (Environment law; explicit, audited binding.)

## §7 — Process and gates
1. DA delivers: docs/design/AXIOM-V2-BE-9-DESIGN-001.md (exact ID; version
   1.0.0; every §4 section present; §6 questions each answered; byte-count
   and sha256 declared in the delivery note).
2. ITRGA full-depth review follows; corrections are issued on evidence;
   acceptance precedes any planning of implementation.
3. Only after design acceptance: CN/PLAN/BO for implementation; code and
   migration may be proposed only by BO amendment thereafter. No code now.
4. Register edits: none in this phase beyond any DA-side design-doc entry;
   the live register may record the design phase as OPENED at the DA's
   discretion (DA-owned edit). The BE-8/0048 staged line
   (ITRGA-DA-SYNC-V2-BE8-0048-001) lands first, on DA's own schedule.

Standing rules for the DA: cite prior-band precedent where reused (§3);
measure, don't assert; mark every assumption; keep the design honest about
what it chooses NOT to do (esp. no-execution N1 — say it structurally).
We don't guess. We prove.

— ITRGA-REQ-V2-BE-9-001 · v1.0.0 · 2026-09-05
