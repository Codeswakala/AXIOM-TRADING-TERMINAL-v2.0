# BUILD ORDER INTAKE — UI-007-P04

**Evidence Viewer & Validation Summary Panels** — *(Read-Only)*

| Field | Value |
|---|---|
| Development Authority | AXIOM DA |
| Programme | AXIOM Institutional UI Transformation |
| Workstream | UI-007 — Governance & Evidence Workspace |
| Phase | **UI-007-P04** |
| Build Order | `docs/build-orders/BUILD_ORDER_UI-007-P04.md` |
| Predecessor verdict | `docs/build-orders/ITRGA_REVIEW_UI-007-P03.md` — Approved with Observations |
| Baseline of record | v0.62.0 · Alembic head `20260717_0037` · backend 414 · frontend 58 files / 261 tests |
| Intake status | Accepted under ITRGA Build Order; implementation confined to P04 |
| Governance Gate | CLOSED |
| Production | NOT CERTIFIED |

---

## 1. Authority confirmation

The supplied ITRGA determination records UI-007-P03 as **APPROVED WITH OBSERVATIONS** and identifies two mandatory P04 closures:

1. **OBS-P03-1:** completed operator-run regression, Alembic, and networked-CI transcript;
2. **OBS-P03-2:** a route-declaration-focused no-new-endpoint check that cannot false-match the pre-existing `governance_gate.py` module.

The supplied ITRGA Build Order authorizes only P04 read-only presentation on the existing protected `/governance` route.

---

## 2. Accepted implementation scope

DA accepts only the following P04 scope:

- a first-party evidence manifest/index showing stored fields from existing AXIOM evidence and governance records;
- validation summary panels over the existing `fetchInstitutionalIntelligenceBundle` read seam and its existing intelligence report APIs;
- visible stored status, method/version, sample count, scope, uncertainty, limitations, source identifiers, lineage, audit references, hashes, and dates where recorded;
- five named P04 tests;
- an operator evidence command pack that carries OBS-P03-1 and OBS-P03-2 to closure.

No backend route, service, schema, table, migration, dependency, registry contract, route, or persistence store is required or authorized.

---

## 3. Design decision

Three alternatives were assessed:

| Alternative | Decision | Rationale |
|---|---|---|
| New evidence-file-listing API and dynamic viewer | Rejected | Explicitly prohibited by G-7/R-3; it expands backend surface and evidence exposure. |
| Markdown renderer dependency | Rejected | Explicitly prohibited without a dependency spike; unnecessary for manifest disclosure. |
| Static first-party manifest plus existing validation read seam | **Selected** | Satisfies R-3: source-preserving evidence index without file discovery, a new dependency, or backend expansion; existing stored validation records remain available through already governed read APIs. |

The selected implementation is presentation-only. It does not synthesize evidence, alter a source verdict, calculate a new validation outcome, or present a filtered result as complete.

---

## 4. Explicit non-authorizations

P04 does not authorize:

- health, readiness, system-version, or API-posture panels (P05);
- P06 completion work;
- evidence upload, discovery, edit, delete, signing, approval, or redaction;
- audit, governance, Gate, certification, readiness, validation, or residual mutation;
- generated narrative, external AI/LLM, client-side analytical derivation, verdict relabeling, or full-scope claim from a filtered subset;
- new backend endpoint, service, schema, table, migration, dependency, markdown renderer, route, registry change, or saved-view persistence;
- order, broker, account, live, real-money, or production-certification capability.

---

## 5. Mandatory named tests accepted

```text
test_ui007_evidence_viewer_renders_existing_records_verbatim_no_ai_summary
test_ui007_validation_summaries_preserve_scope_sample_uncertainty_and_limitations_no_cherry_picking
test_ui007_evidence_viewer_no_recomputed_or_stronger_verdicts_than_source
test_ui007_evidence_viewer_contains_no_governance_mutation_gate_or_certification_control
test_ui007_evidence_viewer_accessibility_and_doc16_brand_hold
```

---

## 6. Evidence closure commitments

The P04 operator pack will:

- display all five named P04 tests passing by name;
- use a route-declaration-only endpoint check under `backend/app/api`, thereby excluding the pre-existing non-route `backend/app/external_integration/broker/governance_gate.py` and preventing the P03 false-positive;
- require a gated full frontend test exit-code sentinel, backend `pytest -q`, Alembic head confirmation, and networked local-CI result;
- distinguish a verified green result from an environment exception without relabeling a failure as success;
- require logged-in and logged-out browser evidence for the P04 panels.

**DA does not self-approve. Gate remains CLOSED. Production remains NOT CERTIFIED.**
