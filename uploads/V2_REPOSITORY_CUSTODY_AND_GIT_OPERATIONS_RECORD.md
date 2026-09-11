# AXIOM V2 — Repository Custody and Git Operations Record

| Field | Value |
|---|---|
| Record ID | AXIOM-V2-GOV-CUSTODY-001 |
| Status | **Operator Clarification — Active** |
| Date | 2026-08-23 |
| Authority | Operator |
| Applies to | DA, ITRGA, V1/V2 transition governance, repository evidence, and chat-migration continuity |

---

## Operator clarification

> Any GitHub-related operation—including commit, push, pull, tag creation, branch management, repository publication, and remote repository synchronization—is an Operator task, not a DA or ITRGA task.

## Repository purpose

The repository is the shared project corpus available to the DA and ITRGA. Its purpose is to preserve and make available project files, governance, plans, Build Orders, evidence, Delivery Reports, source, and historical records when a chat is long, migrated, restarted, or replaced.

## Role boundary

| Role | Repository/Git responsibility |
|---|---|
| Operator | Clone/pull/push/commit/tag/branch/merge/publish/remote-custody operations; supplies commit/tag/diff evidence when required. |
| DA | Produces authorized implementation and documentation artifacts in its assigned workspace; reports the artifact set and evidence; does not perform GitHub operations. |
| ITRGA | Independently reviews the evidence corpus supplied in the review channel/workspace; does not perform GitHub operations or assume access to unpublished DA state. |

## Evidence consequence

A commit, tag, diff, branch, remote, or GitHub claim is an evidence claim. It is verified only when the Operator supplies the relevant repository evidence to the review corpus or when the review workspace has been explicitly synchronized by the Operator.

No visibility means **NOT PROVEN**, not automatically false.

## Operational consequence for Build Orders

Build Orders may require repository/provenance evidence, but must assign any GitHub operation to the Operator. DA completion criteria must be based on the authorized artifact set and direct non-Git evidence available in its workspace. ITRGA may require Operator-provided repository evidence before issuing a repository/provenance determination.

---

**End of Record**
