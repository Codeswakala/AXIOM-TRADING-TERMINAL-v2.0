# ITRGA REQUEST — TD-AXIOM-GIT-PROVENANCE W-8 Baseline SHA / Closure-Record Sequencing

| Field | Value |
|---|---|
| Requesting authority | AXIOM Development Authority (DA) |
| Unit | `TD-AXIOM-GIT-PROVENANCE-REMEDIATION` |
| Authority chain | Build Order + P-2 Amendment 1 + D-2 Amendment 2 |
| Trigger | W-8 requires the baseline SHA in registers while W-3 requires that the baseline commit contain the same register changes; DA cannot self-declare debt closure before ITRGA review |
| DA posture | **HALTED before staging, index removal, commit, tag, hook activation, or history operation** |

## 1. Self-reference problem

W-3 requires a single anchored baseline commit. W-8 requires the Technical Debt Register to record that baseline commit’s exact SHA. A Git commit SHA cryptographically includes the complete tree, including the register content; a file inside that tree cannot contain the SHA of the commit that contains it without an impossible self-reference.

A post-commit register edit would require a second commit, after which:

```text
git diff --stat AXIOM_v0.62.0_BASELINE..HEAD
```

would no longer be empty at HEAD, contradicting mandatory evidence item (i) if the baseline tag remains on the first commit.

## 2. Authority-separation problem

W-8 says TD-AXIOM-GIT-PROVENANCE should be updated to Closed. Under the constitutional hierarchy and Build Order §7, the DA cannot close its own debt/remediation before independent review. The fact that the prospective baseline commit succeeds is implementation evidence, not an ITRGA closure determination.

## 3. Requested binding disposition

Please prescribe one exact valid record form. The DA recommends:

1. The one baseline commit includes the forward protocol and registers `TD-AXIOM-GIT-PROVENANCE` as **Remediation Implemented — ITRGA Review Pending**, referencing the immutable annotated tag `AXIOM_v0.62.0_BASELINE` but not an unknown self-SHA.
2. The runner prints and evidences the resolved SHA using `git rev-parse --verify AXIOM_v0.62.0_BASELINE`.
3. ITRGA’s later closure determination records the exact SHA and changes the debt to Closed only when it approves the unit.

This preserves one clean tagged baseline, makes the mandated tag/SHA evidence real, keeps `BASELINE..HEAD` empty at the baseline, and preserves the DA/ITRGA separation of authority.

If ITRGA instead authorizes a second metadata-only commit, please specify the tag/diff target and the exact compliant W-8 closure wording so the phase-diff proof cannot become a false-clean or a contradiction.

No product, source, test, configuration, dependency, schema, route, Gate, certification, or production change is proposed.
