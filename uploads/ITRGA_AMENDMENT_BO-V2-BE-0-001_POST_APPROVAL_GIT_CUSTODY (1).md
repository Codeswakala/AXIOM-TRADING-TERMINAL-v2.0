# ITRGA Amendment — BO-V2-BE-0-001 Post-Approval Git Custody

| Field | Value |
|---|---|
| Amendment ID | ITRGA-AMD-BO-V2-BE-0-001-RC2 |
| Status | Active |
| Date | 2026-08-23 |
| Amends | `BUILD_ORDER_V2_BE-0_GOVERNANCE_BASELINE_FOUNDATION.md` and RC1 |
| Authority | Operator custody clarification `AXIOM-V2-GOV-CUSTODY-001-A1` |

---

## 1. Replaced repository-evidence and tag requirements

All BO-V2-BE-0-001 requirements that make a commit, tag, Git diff, remote publication, or repository evidence a precondition to DA submission, ITRGA review, ITRGA determination, or BE-0 closure are replaced.

The DA must not create a commit or baseline tag.

The ITRGA must not require a pre-review repository commit/tag/diff as evidence of DA completion.

## 2. Replacement completion sequence

```text
DA completes BE-0 artifacts in its workspace
→ DA submits artifacts, Delivery Report, and non-Git test/build/migration evidence
→ ITRGA reviews and determines the delivery
→ Operator decides whether the significant BE-0 section is approved
→ Operator may commit/tag/push the approved section to the repository
→ Operator records/publishes the clean approved baseline
```

## 3. BE-0 acceptance criteria revised

For ITRGA BE-0 review, acceptance is based on:

- supplied authorized artifacts;
- artifact content and cross-document synchronization;
- direct non-Git evidence for claimed commands where required;
- bounded file/change inventory supplied by the DA;
- scope and governance compliance.

Repository provenance registration is an **Operator post-approval activity**, not DA delivery evidence. The absence of a Git commit/tag before the ITRGA determination is not a failure.

## 4. Current correction-package effect

The DA must correct any statement that it created commits/tags or performed Git operations. Any such claimed operation is outside the DA role under the active Operator clarification. The DA may report its local artifact inventory and non-Git command results only.

## 5. Unchanged restrictions

No new code, configuration, schema, provider, broker, account, paper-trading, execution, AI, production, or frontend work is authorized by this amendment.

---

**End of Amendment**
