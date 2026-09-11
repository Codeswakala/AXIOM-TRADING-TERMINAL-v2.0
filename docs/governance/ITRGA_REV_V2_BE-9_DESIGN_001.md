# ITRGA FULL-DEPTH DESIGN REVIEW — BE-9 (Broker/Exchange Connectivity & Account Visibility)
# ITRGA-REV-V2-BE-9-DESIGN-001 · v1.0.0 · 2026-09-05

- **Object:** `AXIOM-V2-BE-9-DESIGN-001` v1.0.0 (DA, 2026-09-05; 30,178 B; sha256
  `cdbc728a7c297c386a1724ee185b690a06fe1b551366f5ae3df375616c3dfe4f`; md5 `75c356cefd47d00e1707ff5e8a7014ad`)
- **Against:** ITRGA-REQ-V2-BE-9-001 v1.0.0; roadmap §BE-9; sealed record of BE-8
- **Intake note:** delivery arrived via Operator attachment without a byte/sha
  delivery note; ITRGA computed and pins the values above. Future deliveries:
  declare as REQ'd §7.1.

## Determination

**PASS with corrections.** The design is the strongest first-cut delivered to date:
structural N1–N4 (not conventional), correct reuse of precedent law, honest
registers. Three corrections (C-1…C-3) are required in a design **v1.1.0**; two
matters are **for the Operator** (O-1…O-2). Acceptance follows v1.1.0; no code,
no migration before acceptance + BO, per standing chain.

## 1 — Contract compliance (REQ §4/§5/§6 sweep, machine-checked + read)

All of S1–S13 present; Q1–Q9 answered with recommendation + rationale; E1–E5
mapped; §14 honesty and §15 assumptions registers present; chain pinned to the
sealed head `20260904_0048` with correct recounts (triggers 58→74, permissions
57→64, compver 10→11), six-verb closed adapter vocabulary, sealed provider
registry, provenance pins throughout (10+ sites).

**Structural-law assessments (deep read):**
- **N1 — strong.** Closed six-verb `Protocol`, no mutation shape in the type
  graph, V1 `BrokerPort` expressly not reused, route census (exactly 4 POST +
  8 GET), adapter type-census test, code-path scan. This is the required posture.
- **N2 — adequate.** No provider hostname outside the adapter (Q9's
  code-bound-not-config binding); frontend reads AXIOM envelopes only.
- **N3 — strong.** Disjoint namespaces, no cross-FK, `provider_id` NOT NULL
  provenance pins, `data_class` CHECK-pinned `simulated` with the taxonomy
  gate (V2-TD-18) making live-read a separately-sanctioned change, both-sides
  wall tests (`paper` token added to the broker domain's banned scan set — a
  good mirror of the BE-8 wall).
- **N4 — strong with C-3 carve-out below.** Cryptographic blindness
  (passphrase-unlocked encrypted file; DPAPI as second layer, not the layer),
  sole-resolution module + import-boundary test, canary suite across
  logs/envelopes/audits/drift, generic denials.
- **Read-first / reconciliation-first — satisfied.** Reconciliation ships in
  band, attached to every complete sync (S5 cadence), projections never
  authoritative (V2-R-10), discrepancy machinery fully designed (7 classes,
  state machine, ownership, derived aging).

## 2 — Corrections required for v1.1.0 (evidence-cited)

**C-1 — Digest canon law (S4 result_digest).** "Two runs against unchanged
broker state produce equal digests" is only true if the canonicalization
EXCLUDES retrieval-volatile fields (fetched-at banners, provider request ids,
pagination cursor echoes) and fixes member ordering (sort keys before hashing;
JSON canonical form). As written, the replay attestation (×3 law) could false-
FAIL on benign volatiles or false-PASS under re-ordering. **v1.1.0 must state
the canon explicitly:** field inclusion/exclusion rule per the six read models,
ordering rule, encoding (UTF-8, LF, sorted keys, decimal-as-string), plus one
test asserting digest equality across a re-ordered identical fixture and digest
inequality on a single-value change.

**C-2 — Reconcile-run lineage for the zero-discrepancy case (S5).** The design
stores compared sides only inside discrepancy records; an equal run leaves no
artifacts of *what* was compared, so "reconciliation ran clean" is asserted,
not evidenced. **v1.1.0 must add:** a `v2_broker_reconcile_run` lineage row
(or extension of the sync-run row) per reconciliation — run id, compare scope,
input digests of BOTH sides (broker fetch canon == C-1; projection-canon
declared), counts compared, discrepancy count landed, actor — append-only,
immutability triggers (recount +2 triggers → 76, adjust S3/S10 tallies and the
permissions/compver plan consistently, or justify folding into the sync-run row
with equal evidence power).

**C-3 — Vault loss/recovery runbook (S2).** The design pins the cryptographic
posture but silent on loss: encrypted file lost/corrupt, passphrase forgotten,
DPAPI layer broken by machine churn. **v1.1.0 must add a runbook section:**
vault-lost ⇒ re-vault act (new token from broker console, old presumed
compromised ⇒ broker-side revoke first), backup posture (encrypted backup of
the vault file is OPTIONAL and operator-held; never in repo; audited), machine
migration procedure. No mechanics changes required — a one-section honest
runbook.

Non-blocking observations (recorded, not gating):
- Verbatim provider JSON in `v2_broker_order.payload`/`v2_broker_instrument_
  permission.visibility`: the S2.4 canary suite must treat provider-payload
  echo as a leak class (a provider could smuggle a token-shaped string into a
  payload; the canary should include a *payload-echo* probe, not only error
  paths). v1.1.0: one sentence + one test line.
- Fetch-budget law for pathological histories (S1.4's size-cap noted): a
  per-scope page-count ceiling + abort with typed refusal keeps the single-
  transaction landing bounded in memory. Line + test in v1.1.0 recommended.
- DECISION-1 (`v2.broker.` marker exemption): ITRGA concurs — narrowest-scope
  literal prefix exemption with both-arms + `v2.brokerage.*` must-die boundary
  mirrors D-1 exactly. Granted at design acceptance.

## 3 — For the Operator (answers precede BO, not necessarily v1.1.0)

- **O-1 (ASSUMPTION A-1): broker selection.** DA recommends OANDA v20 fxTrade
  Practice with sound criteria (true endpoint+credential disjointness, full
  six-read coverage without write scope, token auth, corpus overlap).
  **Operator declares:** confirm OANDA practice (and provision the service
  identity at BO), or redirect; a non-OANDA selection triggers re-review of
  S1.1–S1.3 only (the S1.4 contract binds regardless — correctly designed).
- **O-2 (ASSUMPTION A-3): vault idle re-lock TTL.** Default 8h acceptable at
  design level; confirm or set at BO. ITRGA recommendation: 8h for a single-
  console posture is acceptable given audit on unlock/lock.

## 4 — Standing posture

- Zero-code rule: holds. BO may be authored only after design acceptance.
- The C-2 recount (if the lineage table is chosen over extending sync-run)
  must be carried identically through the acceptance record, BO, pins, and
  future apply/verify pack literals — the 0048 cycle's exact-pin law applied
  prospectively.
- Field artifacts of this review: this document; design bytes pinned in the
  intake note above.

**Directions:** DA → design v1.1.0 covering C-1…C-3 (byte/sha declared).
Operator → O-1/O-2 (declare at convenience; only O-1 can force a re-review).
ITRGA → full-depth review of v1.1.0 on receipt; acceptance record thereafter.

— ITRGA-REV-V2-BE-9-DESIGN-001 · v1.0.0 · 2026-09-05
