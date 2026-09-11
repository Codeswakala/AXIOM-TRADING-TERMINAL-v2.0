# ITRGA Security-Standard Addendum — V2 BE-1 Design Plan

| Field | Value |
|---|---|
| Review ID | ITRGA-REV-V2-BE-1-002 |
| Submission | Resubmitted `AXIOM-V2-BE-1-DA-PLAN-001` |
| Governing standard | `17_INSTITUTIONAL_SECURITY_STANDARD.md` |
| Relationship | Addendum to `ITRGA-REV-V2-BE-1-001` |
| Determination | **CORRECTION REQUIRED — prior findings remain open; security-standard findings added** |

---

## 1. Security-standard validation

The plan correctly identifies Document 17 as mandatory and correctly cites security-by-design, zero trust, least privilege, default-deny, accountability, SAL classification, secure error handling, and threat modelling.

However, citation is not compliance. Several proposed BE-1 controls do not yet meet the stated mandatory requirements of Document 17.

## 2. Prior findings remain open

The resubmitted plan retains the same unresolved designs identified in `ITRGA-REV-V2-BE-1-001`:

1. competing mode sources (`AXIOM_V2_MODE` and `v2_mode_config` with `is_active`);
2. broad audit/lineage reads with undefined ownership/resource filtering;
3. append-only audit stated but not technically enforced;
4. naive external datetime coercion/warnings retained for V2 paths;
5. migration drift accepted as generically “unchanged” rather than bounded by a drift baseline;
6. capability `enabled`/feature-flag state without defined authority, mutation process, or governance synchronization.

These must be corrected in the plan, not merely acknowledged by the security-standard section.

## 3. Additional findings from Document 17

### Finding V2-BE1-SEC-001 — SAL-3/SAL-4 protections are classified but not designed

| Field | Detail |
|---|---|
| Severity | High |
| Security-standard basis | Document 17 §4.4: SAL-3 requires authentication, RBAC, encryption, audit logging, operator isolation, backup, and monitoring. SAL-4 requires strong cryptography, key rotation, secret management, continuous monitoring, enhanced audit logging, least privilege, administrative approval, and incident alerting. |
| Observed condition | The plan classifies audit/lineage/API resources as SAL-3 and mode/RBAC resources as SAL-4, but does not design encryption at rest/in transit, backup/recovery treatment, monitoring, key management/rotation, administrative-approval workflow, or incident alerting for these assets. |
| Required correction | For each BE-1 asset, state the actual applicable storage/transmission protection, encryption/key ownership, backup/recovery requirement, monitoring/audit event, and SAL-4 administrative control. Where a required infrastructure control is inherited from V1/deployment, identify the exact existing control and validation evidence; do not assume it. |
| Closure criterion | The BE-1 design has an implementable SAL-control matrix rather than a classification label only. |

### Finding V2-BE1-SEC-002 — Permanent retention conflicts with constitutional retention requirements

| Field | Detail |
|---|---|
| Severity | Medium |
| Security-standard basis | Document 17 §8.11: institutional information shall not be retained indefinitely; retention must consider operational necessity, governance, security, and future legal obligations; expired information must be archived or securely destroyed under approved policy. |
| Observed condition | B.4 and D.1 specify permanent retention for audit events and lineage records without a retention owner, review period, archive/disposal policy, legal/governance basis, or classification-specific treatment. |
| Required correction | Replace “permanent” with a governed retention lifecycle: owner, minimum retention period or explicit pending-policy state, archival/disposal mechanism, preservation-hold rule, review cadence, and disposition audit evidence. Immutable history does not require unlimited online retention. |
| Closure criterion | Audit/lineage retention complies with §8.11 and does not silently establish indefinite retention policy. |

### Finding V2-BE1-SEC-003 — Resource ownership and SAL-aware authorization are not defined

| Field | Detail |
|---|---|
| Severity | High |
| Security-standard basis | Document 17 §6.8 requires defined resource ownership; §6.13 requires SAL-aware authorization; §6.14 requires access/authorization event audit; §8.5 requires data owner responsibility for access approval, retention, classification, and integrity. |
| Observed condition | The plan labels records SAL-3/4 and proposes `v2.audit.read`/`v2.lineage.read` for both roles, but does not identify a resource owner, data owner, governance-record owner, classification enforcement rule, sensitive-read audit schema, or operator-vs-admin visibility decision. |
| Required correction | Add a resource-ownership and authorization matrix for every new table/API: owner, SAL, default visibility, operator scope, admin/governance exception, access approval, sensitive-read audit event, retention owner, and access-review requirement. |
| Closure criterion | Access to a SAL-3/4 resource is determinate, least-privilege, owner-governed, and auditable. |

### Finding V2-BE1-SEC-004 — Feature-flag/admin mutation contradicts BE-1’s read-only capability scope

| Field | Detail |
|---|---|
| Severity | Medium |
| Security-standard basis | Document 17 §6.9 requires enhanced authorization and comprehensive audit for administration; §6.14 requires audit of permission/resource policy changes. |
| Observed condition | The plan declares `enabled` feature flags and a threat test for “non-admin flag change,” but exposes no permitted mutation endpoint or governance process. It also claims feature flags are DB/admin-only, while BE-1 is scoped to non-actuating primitives and the requested capability registry is a read model. |
| Required correction | Choose one: (a) make BE-1 a read-only seeded registry with no runtime mutation capability; or (b) explicitly include a restricted administrative feature-flag mutation workflow with SAL-4 controls, approval/audit/revocation/review design and a tightly scoped Build Order. Option (a) is recommended for BE-1. |
| Closure criterion | There is no latent mutable security-control state without a defined authority and control path. |

## 4. Additional correction required

The corrected plan must contain:

- a BE-1 asset-to-SAL control matrix;
- retention/archival/disposal design rather than permanent retention;
- ownership/entitlement/classification matrix and sensitive-read auditing;
- a single mode source of truth and no mode activation DB state;
- enforced audit/lineage immutability design;
- drift-baseline/migration validation approach;
- read-only seeded capability registry or separately authorized administrative mutation design;
- V2 temporal acceptance rules that do not add naive-datetime warning paths.

## 5. Determination

**CORRECTION REQUIRED.** The Security Standard is applicable and strengthens—not replaces—the prior BE-1 review. No BE-1 implementation may start until the corrected design demonstrates enforceable compliance with both the existing V2 governance and Document 17.
