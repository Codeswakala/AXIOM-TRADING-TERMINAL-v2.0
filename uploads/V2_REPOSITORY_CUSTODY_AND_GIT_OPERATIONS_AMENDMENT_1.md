# AXIOM V2 — Repository Custody and Git Operations Amendment 1

| Field | Value |
|---|---|
| Amendment ID | AXIOM-V2-GOV-CUSTODY-001-A1 |
| Status | **Operator Clarification — Active** |
| Date | 2026-08-23 |
| Amends | `V2_REPOSITORY_CUSTODY_AND_GIT_OPERATIONS_RECORD.md` |
| Authority | Operator |

---

## Operator decision

> GitHub commits, tags, pushes, pulls, branches, merges, and remote synchronization are not performed after each Build Order. They are performed only by the Operator after a significant project section has been fully approved by the Operator, so the repository remains a clean secondary backup and recovery record.

## Binding operational rule

```text
DA implements authorized work in its workspace
→ DA supplies Delivery Report and non-Git evidence to ITRGA
→ ITRGA reviews and determines the submitted work
→ Operator approves the significant completed section
→ Operator performs any commit/tag/push/publication operation
→ Repository becomes the clean approved recovery/continuity record
```

## Role implications

- The DA must not commit, tag, push, pull, branch, merge, or otherwise perform GitHub/Git operations.
- ITRGA must not require a pre-review commit, tag, remote publication, or Git evidence as a condition for reviewing a DA Delivery Report.
- ITRGA may review DA-supplied files, direct non-Git command output, workspace evidence, and Delivery Reports before repository publication.
- Operator repository evidence may be used after Operator approval to register the clean approved baseline, but it is not a prerequisite to ITRGA review or determination.
- A repository commit/tag is a post-approval custody/recovery record. It is not DA evidence of correctness.

## Superseded operational wording

Any prior V2 Build Order or custody wording that requires a DA-created tag, pre-review commit, pre-review Git diff, or Operator repository evidence **before** ITRGA can review/approve a delivery is superseded by this amendment.

## Evidence rule

For DA delivery review:

- direct test/build/migration/runtime output remains admissible Level-II evidence when supplied;
- submitted files and documents remain reviewable at their applicable evidence tier;
- absence of a pre-review repository commit is not a completeness gap;
- no visibility of unpublished DA workspace remains `NOT PROVEN`, not automatically false.

---

**End of Amendment**
