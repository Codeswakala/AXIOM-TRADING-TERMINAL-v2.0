# BUILD ORDER INTAKE — UI-006-P06

**UI-006 Completion Checkpoint — integration evidence · mutation-boundary + constitutional + Doc 16 brand validation**

| Field | Value |
|---|---|
| Development Authority | AXIOM DA |
| Programme | AXIOM Institutional UI Transformation |
| Workstream | UI-006 — Unified Research Artifact Explorer |
| Phase | **UI-006-P06** |
| Build Order | `docs/build-orders/BUILD_ORDER_UI-006-P06.md` |
| Predecessor verdict | `docs/build-orders/ITRGA_REVIEW_UI-006-P05.md` — Approved with Observations |
| Baseline of record | v0.62.0 · Alembic head `20260717_0037` · backend 414 · frontend 54 files / 241 tests |
| Intake status | Accepted by DA under ITRGA Build Order; implementation confined to P06 completion checkpoint |
| Governance Gate | CLOSED |
| Production | NOT CERTIFIED |

---

## 1. Authority confirmation

ITRGA approved UI-006-P05 with observations and authorized issuance of the final UI-006 completion Build Order on operator authorization.

Recorded governance files:

```text
docs/build-orders/ITRGA_REVIEW_UI-006-P05.md
docs/build-orders/BUILD_ORDER_UI-006-P06.md
```

P06 is a completion checkpoint. It does not authorize a new UI workstream, a new route, a new backend capability, a schema change, live execution, external AI/LLM, or production deployment.

---

## 2. Accepted implementation scope

DA will perform completion-checkpoint work only:

1. record the P05 ITRGA approval and P06 Build Order;
2. add P06 completion named tests;
3. update stale P01/P03 presentation copy on `/research-management` to reflect the approved UI-006 completion posture;
4. preserve the existing route `/research-management` and UI-001/UI-002 shell integration;
5. re-affirm P04/P05 mutation boundaries: collections, memberships, and tags are organization-only, existing-store-bound, and do not mutate source artifacts;
6. prepare operator Level-I evidence commands for final ITRGA review;
7. explicitly disclose the TD-UI-POSTCSS-HIGH decision at this checkpoint.

No new product capability is accepted beyond integration/completion evidence and completion-posture copy alignment.

---

## 3. TD-UI-POSTCSS-HIGH decision path accepted for DA submission

No separate dependency-remediation Build Order was provided with P06. Therefore DA will **not** change package manifests, package lock, or dependencies inside this completion checkpoint.

DA selects **Path B — explicit re-acceptance for ITRGA/operator disposition**:

```text
TD-UI-POSTCSS-HIGH remains an open pre-certification residual.
It must be remediated or formally dispositioned before Production Readiness Certification under Doc 11.
DA does not relabel audit output green and does not self-approve the residual.
```

If ITRGA/operator instead require Path A remediation, a separate dependency-remediation authorization and evidence pack will be required.

---

## 4. Mandatory named tests accepted

```text
test_ui006_completion_artifact_explorer_discovery_organization_and_traceability_hold
test_ui006_completion_mutations_are_organization_only_and_existing_store_bound
test_ui006_completion_no_actuation_recompute_external_ai_schema_or_route_drift
test_ui006_completion_verbatim_no_cherry_picking_and_relationship_boundaries_hold
test_ui006_completion_accessibility_doc16_brand_and_ui001_ui002_integration_hold
```

---

## 5. Explicit non-authorizations

P06 does not authorize:

- UI-007 implementation or design shortcut;
- any new route such as `/artifacts` or `/artifact-explorer`;
- new backend/API endpoint;
- schema migration or new table;
- dependency remediation/change under Path B;
- new collection/tag mutation beyond the P04/P05 organization-only slices;
- tag delete, tag edit/rename, collection rename/update, or empty-collection delete;
- saved-filter persistence;
- relationship inference/scoring;
- recompute/inference/reclassification;
- external AI/LLM;
- order, broker, account, live, real-money, position, or capital paths;
- Governance Gate change;
- Production Readiness Certification.

---

**DA does not self-approve. Gate remains CLOSED. Production remains NOT CERTIFIED.**
