# ITRGA REQUEST — TD-AXIOM-GIT-PROVENANCE P-2 Credential-Scan Scope Clarification

| Field | Value |
|---|---|
| Requesting authority | AXIOM Development Authority (DA) |
| Governing Build Order | `BUILD_ORDER_TD-AXIOM-GIT-PROVENANCE-REMEDIATION.md` |
| Unit | `TD-AXIOM-GIT-PROVENANCE-REMEDIATION` |
| Trigger | Mandatory P-2 credential preflight cannot reach the required zero result under the Build Order’s literal expression and required staging scope |
| DA posture | **HALTED — no commit, tag, redaction, hook activation, staging, or history rewrite performed after the finding** |
| Gate / Production | **CLOSED** / **NOT CERTIFIED** — unchanged |

## 1. Request

Please issue a narrow, binding clarification for P-2/P-3 before this unit proceeds.

The DA requests an approved **semantic staged-secret scanner** definition that detects secret *values* and unsafe credential assignments/URLs/tokens while excluding safe, non-secret language identifiers such as API response-field names and test model attributes. The clarification must also prescribe the treatment of already tracked evidence and database-backup material.

## 2. Evidence of the contradiction

The Build Order requires all of the following simultaneously:

1. stage product source, tests, governance docs, Build Orders, delivery reports, and ITRGA determinations;
2. run the supplied P-2 expression across everything staged;
3. produce `STAGED_SECRET_MARKER_COUNT: 0`;
4. make **no product source, test, configuration, or dependency change**.

Applied exactly to the candidate scope after excluding the P-1 evidence/evidence-runner paths, the required expression produced:

```text
P2_PREFLIGHT_SCOPE_TRACKED_FILES: 1105
P2_PREFLIGHT_MATCHED_FILES: 148
P2_PREFLIGHT_MATCHED_OCCURRENCES: 461
```

The marker expression includes `access_token` and `refresh_token`. Those strings occur as required, non-secret field names in the existing auth contract and tests. It also reaches pre-existing bootstrap/test constants and the Build Order’s own examples/scanner text. A literal zero is therefore structurally impossible without either editing otherwise in-scope source/tests/configuration or excluding required baseline content.

The first option is prohibited by §2; the second makes the proposed baseline incomplete. The DA will not choose either interpretation unilaterally.

## 3. Already tracked material requiring explicit disposition

- `docs/evidence/**` has 570 already tracked files. `.gitignore` does not untrack them; an approved procedure must state whether to remove them from the new baseline index with `git rm --cached` while preserving the local review corpus.
- A tracked database-backup path is also detected by the preflight and is already covered by the repository’s `*.db` ignore policy only for future untracked files.
- Some tracked Build Orders, governance records, and delivery reports contain literal local-development examples. P-3 permits redaction, but the Build Order itself contains the literal marker expression, so the canonical redacted text and final scanning treatment need authority direction.

## 4. Requested decision points

Please determine all of the following explicitly:

1. **P-2 matching semantics:** May the final scanner distinguish secrets/credential values from safe code identifiers such as `access_token` and `refresh_token`? If yes, provide the canonical pattern or approved allowlist and require its output to show only filename/line/marker-class, never the value.
2. **Bootstrap/test literals:** May existing test/dev constants remain where they are controlled fixture/configuration values, or is a separate security-remediation Build Order required? The DA will not change source/tests under this metadata-only order without authorization.
3. **Tracked evidence and database backup:** Authorize or decline index-only removal from the new baseline (`git rm --cached` without local deletion), and specify whether any current tracked historical artifact must remain in the new tree.
4. **P-3 canonical redaction:** Define which document families require redaction and whether the Build Order’s own examples/pattern are retained verbatim in the authority record but excluded from the semantic value scan.
5. **W-6 guard:** Approve the same semantic scanner for the recurrence guard so it blocks actual secret values and conflict markers without making all future commits impossible.

## 5. Proposed safe path — not implemented

Subject to the above decision, the DA proposes:

1. preserve the immutable original `22c735a` history;
2. remove already tracked evidence/backup artifacts from the new baseline index only, preserving local evidence review files;
3. redact only ITRGA-specified document literal values and produce a filename-only redaction manifest;
4. stage the full approved v0.62.0 source/tests/governance corpus;
5. run the ITRGA-approved semantic scanner to a real zero result;
6. perform the anchored commit, annotated baseline tag, honest retrospective tags, hook demonstration, forward protocol, and Level-I evidence runner.

No source, test, dependency, route, schema, migration, Gate, certification, execution, or production change is proposed.

**We do not guess a security control. We ask for its exact governed form.**
