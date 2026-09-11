# AXIOM V2 BE-3 P2 — Status Transition Design Plan: `architecture_candidate → contract_tested` (Twelve Data)

| Field | Value |
|---|---|
| Document ID | AXIOM-V2-BE-3-P2-TRANS-PLAN-001 |
| Version | 1.1.0 (corrections for ITRGA-REV-V2-BE-3-P2-TRANS-PLAN-001, findings TR-001…TR-004) |
| Status | **RESUBMITTED FOR ITRGA REVIEW** — design only; confers no implementation authority |
| Date | 2026-08-29 |
| Author | Development Authority (DA) |
| Responds to | ITRGA-INT-V2-BE-3-P2-TRANSITION-001; ITRGA-REV-V2-BE-3-P2-TRANS-PLAN-001 |
| Initiating decision | AXIOM-V2-OD-BE-3-P2-003 (Operator, 2026-08-29) |
| Basis | ITRGA-DET-V2-BE-3-P2-FINAL-001 (band closed; contract verified with observations); ITRGA-REV-V2-BE-3-P2-CONTRACT-TEST-001 (all findings closed); run correlation `a246607c-f0c5-42e9-8f3b-a1e1bd75fa83` (completed, 0 indeterminate) |
| Preparation declaration | No implementation, migration, source change, status change, network activity, credential access, or Git/GitHub operation occurred while producing this plan. The workspace source tree is unchanged from the accepted P2 state |

---

# Revision 1.1.0 — Finding Closure Map (ITRGA-REV-V2-BE-3-P2-TRANS-PLAN-001)

| Finding | Correction | Where |
|---|---|---|
| TR-001 (no-op audit semantics undefined) | **ITRGA-recommended behavior adopted**: already-applied re-run is a **clean audited no-op — not a refusal**: `start` and `complete` both emitted with `no_op: "already-applied"`, history unchanged, alembic exit 0; aligned across all four sections | Part 1, 3.3, 4 (P-2), 6, 8 |
| TR-002 (authority-variable state per gate boundary) | §9 boundary table annotates the variable's state at every step: set for the 0042 upgrade; **still set** for the re-upgrade attempt (so P-1 passes and **P-5** is the proven refusal); NOT required for downgrade; unset as the final recorded gate step | Part 9 |
| TR-003 (refusal-audit write failure fallback) | Defined: refusal-audit insert failure → migration raises distinct identifiable error `REFUSAL AUDIT WRITE FAILED: <precondition-name>`; never proceeds silently; precondition name preserved in both the error and the SECURITY line; fault-injected test added | Part 4, 8 |
| TR-004 (revision typo) | §9 corrected to "downgrade to revision `20260825_0041`" | Part 9 |

---

# Part 1 — Authorization Basis (intake item 1)

This plan designs **exactly one** governed operation:

> `v2_md_provider` row `provider_id = 'twelvedata'`:
> `source_status`: `architecture_candidate → contract_tested`
> plus **one** append to `v2_md_provider_status_history` — nothing else.

- Authorized to be designed by AXIOM-V2-OD-BE-3-P2-003; evidentiary basis is
  ITRGA-DET-V2-BE-3-P2-FINAL-001 and the closed contract-test record
  (correlation `a246607c-f0c5-42e9-8f3b-a1e1bd75fa83`). These are **cited as
  the basis, not re-derived**: the transition mechanism never re-evaluates
  contract-test results; it verifies the recorded facts exist.
- The operation is **one-shot** and **idempotent**: a second execution on an
  already-transitioned database is a **clean audited no-op — not a refusal**
  (TR-001; defined precisely in Part 3.3/4/6), and fully audited in every
  path.
- **Exclusions:** every other provider; every other ladder state — in
  particular `integrated`, `authorized:*`, `production_certified`; any
  active-authority change; any entitlement change; any frontend work
  (OD-003 §3 backend-first directive); any Git operation.

# Part 2 — Mechanism Design (intake item 2, the central decision)

## 2.1 Chosen mechanism: one-shot governed migration

**Decision: a single Alembic migration (`20260829_0042_v2_be3_p2_transition`)
that handles the immutability triggers explicitly** — the same pattern the
P2 entitlement migration (0041) used and the PostgreSQL gate proved on both
dialects. A `SECURITY DEFINER` writer / runtime transition endpoint is
**rejected** for this chain.

**Why migration, not a runtime writer:**

1. **Minimal necessary change.** One state change for one provider does not
   justify a permanent application write path. A runtime transition writer
   would be standing mutable-status machinery — precisely what P1/P2 reviews
   repeatedly required us NOT to have. After this migration, the codebase
   still contains **no** application write path to provider status.
2. **No trigger re-scoping.** A `SECURITY DEFINER`/triple-admitting trigger
   redesign would permanently weaken the guard's simplicity ("refuse all")
   into a policy engine ("refuse all except…"), enlarging the audit surface
   forever. The migration approach keeps the guard binary: it is absent only
   inside the governed migration run, exactly as in 0041.
3. **Dialect parity is already proven.** The drop → mutate → recreate →
   `_verify_guard_present` pattern passed the P2 PostgreSQL gate on both
   dialects, including interruption detection.
4. **Provenance.** A migration is inherently a versioned, hash-attested,
   ITRGA-reviewable artifact with deterministic downgrade; a runtime
   endpoint's invocation is a transient event.

## 2.2 Atomicity (proven, not asserted)

- **PostgreSQL:** the migration body (trigger drop, precondition assertions,
  provider UPDATE, history INSERT, trigger recreate, guard verification,
  audit events) executes inside Alembic's single transactional-DDL
  migration transaction. Any raise → full rollback: provider row, history,
  and audit all unchanged. Test: a fault-injected run (forced raise between
  UPDATE and INSERT) proves both rows unchanged afterward.
- **SQLite:** DDL is per-statement (known caveat, accepted in 0041). The
  migration orders statements so the DML pair (UPDATE + INSERT) executes in
  one transaction between guard drop and recreate, and `_verify_guard_present`
  plus a `_verify_transition_consistent` check (status and history row count
  must agree: `contract_tested` ⇔ count 2) raise loudly on any partial
  state. The interruption-detection test regime from 0041 is extended with
  the consistency check.

## 2.3 No permanent weakening (proven, not asserted)

Post-transition and post-downgrade, on both dialects, the evidence must show
UPDATE/DELETE refused **with the exact trigger error** for:
- any column of the `twelvedata` row (incl. an attempted second transition
  to `integrated`, `entitlement_status`, `persistence_permitted`);
- any other provider row (a seeded test-fixture row in tests);
- DELETE of any row;
- UPDATE/DELETE of any `v2_md_provider_status_history` row (both history
  triggers intact throughout — they are **never dropped** by this migration;
  the history INSERT is append-only and trigger-compatible).

# Part 3 — Invocation Surface (intake item 3)

**Migration-based — therefore the invocation surface is the Alembic command
itself, gated as follows:**

1. **Execution gate:** the migration refuses to run unless the environment
   carries the explicit authority reference
   `AXIOM_TD_TRANSITION_AUTHORITY_REF == "<transition Build Order ID>"`
   (exact string fixed by the future Build Order). Absent/mismatched → the
   refusal path (Part 4) fires and the migration aborts with zero side
   effects. This makes an accidental `alembic upgrade head` in an
   unprepared environment a refused, audited event — not a silent
   transition.
2. **Operator confirmation step:** the runbook (delivered with the
   implementation) requires the Operator to set the authority variable for
   the single verification run and unset it afterwards; the Delivery Report
   records this procedure. `alembic current` is echoed before and after.
3. **Idempotent re-run behavior (TR-001, pinned):** if the row is already
   `contract_tested` (e.g. re-running upgrade on an already-migrated
   database), the migration completes as a **clean audited no-op — not a
   refusal**: it emits `provider.status_transition.start` with
   `no_op: "already-applied"` in details, performs no mutation, emits
   `provider.status_transition.complete` with `no_op: "already-applied"`,
   leaves history unchanged (still exactly one transition row), and exits 0
   with a deterministic head.
4. No endpoint, no request body, no network reach, no new permission — the
   runtime API surface is untouched by this chain.

# Part 4 — Preconditions (intake item 4; default-deny)

All checks run **before** any mutation, inside the migration, in this order.
**Every failure → durable refusal audit + abort with zero side effects.**

| # | Precondition | Failure behavior |
|---|---|---|
| P-1 | `AXIOM_TD_TRANSITION_AUTHORITY_REF` equals the Build Order ID | refuse |
| P-2 | `twelvedata.source_status == 'architecture_candidate'` (if already `contract_tested` → **clean audited no-op per Part 3.3 — start/complete with `no_op: "already-applied"`, no refusal event, exit 0**; any other value → refuse) | refuse / no-op |
| P-3 | `entitlement_status == 'verified'` | refuse |
| P-4 | `persistence_permitted == false` (and must remain false — asserted again post-mutation) | refuse |
| P-5 | history row count for `twelvedata` == 1 (genesis only) | refuse |
| P-6 | Basis citation present: the migration embeds (as constants) `ITRGA-DET-V2-BE-3-P2-FINAL-001` and correlation `a246607c-f0c5-42e9-8f3b-a1e1bd75fa83` into the history row and audit details — cited, never re-derived | n/a (constant) |
| P-7 | `AXIOM_V2_MODE` valid (`RESEARCH`/`SIMULATION`) | refuse |
| P-8 | Reserved provider authority still inactive (`v2_md_source.twelvedata.active == false`) | refuse |

**Durable refusal audit under rollback semantics (design detail):** an
aborted migration transaction would roll back an in-transaction audit row.
Therefore the refusal audit event (`provider.status_transition.refused`,
naming the failed precondition only) is written through a **dedicated
short-lived independent connection** (own engine connect → insert → commit
→ close) *before* the migration raises — the same durable-unit principle as
the P2 `_durable_audit` correction (DEL-001), applied to the migration
context. The SECURITY log line fires as well. Tests prove: refusal audit row
exists after an aborted run while provider/history rows are unchanged.

**Fallback if the refusal-audit insert itself fails (TR-003, pinned):** the
migration raises a **distinct, identifiable error** —
`REFUSAL AUDIT WRITE FAILED: <precondition-name>` — never proceeds silently,
and never masks the failed precondition: the precondition name appears in
both the raised error and the SECURITY log line (which fires regardless of
the audit-sink state). The alembic non-zero exit remains the outer backstop.
A lost refusal record therefore reads as a loud, attributable failure —
never as success (Charter invariant 8).

# Part 5 — History Semantics and Downgrade (intake item 5)

## 5.1 Upgrade: exactly one new history row

```text
provider_id   = twelvedata
from_status   = architecture_candidate
to_status     = contract_tested
authority_ref = <transition Build Order ID>
evidence_ref  = ITRGA-DET-V2-BE-3-P2-FINAL-001 · run a246607c-f0c5-42e9-8f3b-a1e1bd75fa83
operator_id   = null (migration context; the executing Operator is recorded in the audit events and runbook)
created_at    = aware-UTC
```
History count: **1 → 2.**

## 5.2 Downgrade: reversal append, never deletion (explicit choice + rationale)

**Choice:** downgrade restores `source_status = architecture_candidate` and
**retains** the transition history row, appending a **reversal row**
(`contract_tested → architecture_candidate`, authority_ref = this
migration's downgrade + the Build Order ID, evidence_ref noting
"governed downgrade"). History count on downgrade: **2 → 3.**

**Rationale (stated, not inherited):** the 0041 precedent (restore state,
retain history) is followed for the state restoration — but 0041 never wrote
history, so its precedent is silent on the row's fate. Deleting the
transition row would require dropping the **history** immutability triggers,
which this plan refuses to do under any path: the append-only history
guarantee outranks downgrade symmetry. A truthful ledger records that the
transition happened and was reversed; it does not pretend the transition
never occurred. Re-upgrade after such a downgrade finds count == 3 ≠ 1:
P-5 refuses — **by design**, a post-reversal re-transition requires a fresh
governed decision (documented as the expected behavior, with the recovery
path being a new ITRGA-authorized chain).

# Part 6 — Audit Design (intake item 6)

Actions follow the existing `provider.*` convention; all rows append-only
`v2_audit_event`, actor_type `operator`, SAL-4 context, mode stamped,
non-payload details only:

| Action | When | Details (non-payload) |
|---|---|---|
| `provider.status_transition.start` | After preconditions pass, before mutation | provider_id, from/to, authority_ref, evidence_ref, precondition snapshot (booleans) |
| `provider.status_transition.complete` | After mutation + guard verification | history_count (2), post-state snapshot (status/entitlement_status/persistence flags) |
| `provider.status_transition.refused` | Any precondition failure (independent durable connection, Part 4) | failed precondition name only |
| `provider.status_transition.start` / `.complete` with `no_op: "already-applied"` | Already-applied re-run (TR-001) — clean no-op path, in-transaction, no mutation | `no_op` marker; history_count (unchanged, 2) |
| `provider.status_transition.downgraded` | On governed downgrade | reversal note, history_count (3) |

`start`/`complete` ride the migration transaction (atomic with the change —
if the transition rolls back, so do they, correctly); `refused` is
independently durable (it must survive the abort).

# Part 7 — Post-Transition Invariants (intake item 7; proven, not asserted)

Each is a named test and a PostgreSQL-pack query, not a statement:

1. `persistence_permitted == false` (queried post-transition);
2. reserved authority inactive (`v2_md_source.twelvedata.active == false`;
   emission guard untouched — no source file changes outside the migration);
3. entitlement JSON byte-identical pre/post (queried and compared);
4. no payload stored (no new tables/columns; schema diff empty beyond none);
5. no network (the migration imports no transport; socket-guard applies to
   the whole test suite as always);
6. no other provider row touched (fixture row unchanged);
7. no new endpoint (route inventory diff empty; the runtime API surface
   hash-unchanged — provenance manifest shows migration + tests only).

# Part 8 — Test Design (intake item 8)

| Class | Tests |
|---|---|
| Precondition matrix | Each of P-1…P-5, P-7, P-8 independently failed → migration aborts, durable refusal audit row exists, provider row + history count unchanged (zero side effects) |
| Happy path | Fresh chain to 0041 → set authority ref → upgrade → status `contract_tested`, history 1→2 with exact field content, `start`/`complete` audit rows, all Part 7 invariants |
| Idempotence (TR-001) | Re-run upgrade on migrated DB → `start`+`complete` audit rows each carrying `no_op: "already-applied"`; NO `refused` event; history unchanged (one transition row); exit 0 |
| Immutability (post-transition) | UPDATE any column (incl. attempt `integrated`), UPDATE other-provider fixture row, DELETE rows, UPDATE/DELETE history rows → all refused with exact trigger error |
| Atomicity fault injection | Forced raise between UPDATE and history INSERT → both unchanged (PostgreSQL semantics via transaction; SQLite via consistency-check detection) |
| Downgrade | Restores `architecture_candidate`; reversal row appended (count 3); immutability re-proven; re-upgrade after reversal → P-5 refusal (documented behavior) |
| Interruption | Guard-absent simulation → `_verify_guard_present` raises "NOT restored"; status/history consistency check raises on partial state |
| Refusal-audit fallback (TR-003) | Fault-injected refusal-audit insert failure → distinct `REFUSAL AUDIT WRITE FAILED: <precondition-name>` error; precondition name in error + SECURITY line; zero state change |
| Regression | Full distinct-accounted suite (V1 + BE-1 + BE-2 + P1 + P2 + new transition tests) green; V2 lint clean |

# Part 9 — Fresh PostgreSQL Verification (intake item 9)

Same standard as the P2 gate; **new empty dedicated database**; sanctioned
pack (`-File` execution); pre-redacted, credential-free output;
`alembic current` echoed at every boundary:

Boundary table with the authority variable's state annotated at every step
(TR-002):

| Step | `AXIOM_TD_TRANSITION_AUTHORITY_REF` | Expected result |
|---|---|---|
| baseline → `20260717_0037` → `20260823_0038` → `20260824_0039` → `20260824_0040` | **unset** (not required) | Chain boundaries echoed via `alembic current`; P2 permission absent at 0040 (boundary re-proof) |
| → `20260825_0041` | **unset** (not required) | Entitlement verified; `architecture_candidate`; persistence false; history count 1 |
| → transition head `20260829_0042` | **SET** (single authorized step) | Pre/post state queries; history 1 → 2 with field content; audit proof by correlation (`start`/`complete` rows queried); immutability spot-checks: provider UPDATE/DELETE refused, history UPDATE/DELETE refused, other-provider fixture refused, attempt `integrated` refused |
| → downgrade to revision `20260825_0041` (TR-004) | **NOT required** (restoration path, audited via `provider.status_transition.downgraded`; consistent with the 0041 gate precedent, which downgraded without an authority variable) | `architecture_candidate` restored; reversal row (count 3); immutability re-proven |
| → re-upgrade attempt | **STILL SET** (so P-1 passes and **P-5 is the proven refusal**, exactly as Part 5.2 documents) | Documented P-5 refusal (history count 3 ≠ 1) with durable refusal audit row |
| final gate step | **UNSET — recorded in the transcript** | Variable lifecycle closed |

`alembic check` → inherited V1 drift set ONLY (explicitly distinguished);
no V2/P2/transition drift.

# Part 10 — Provenance and Delivery (intake item 10)

- **File scope (implementation, under the future Build Order only):** one
  new migration file + one new test module; **zero runtime source changes**.
- Source transcript with SHA-256 for every touched file (REM-001 policy —
  literal contents regardless of change class); single evidence transcript
  per run; Delivery Report per the established structure; state/risk/debt
  register synchronization.
- Redaction per credential law: no secret, no account identifier, no
  connection URL in any artifact.

# Part 11 — Explicit Non-Goals (intake §3 mirror)

No promotion beyond `contract_tested`; no ingestion/persistence/streaming/
reconciliation/circuit-breaker operationalization; no active-authority
activation; no entitlement change; no frontend work (backend-first
directive); no Git/GitHub operation; no production claim.

# Part 12 — Requested Future Authority

If this plan passes review, the transition Build Order would need to
authorize exactly: (a) migration `20260829_0042` as designed (incl. the
independent-connection refusal-audit mechanism); (b) its test module;
(c) the Operator PostgreSQL verification run with the authority variable set
for that single step. Nothing else.

**We don't guess. We prove.**

**End of Transition Design Plan v1.0.0**
