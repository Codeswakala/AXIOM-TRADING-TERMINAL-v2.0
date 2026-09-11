# ITRGA REQUEST — TD-AXIOM-GIT-PROVENANCE D-2 Exception Count Disposition

| Field | Value |
|---|---|
| Requesting authority | AXIOM Development Authority (DA) |
| Governing Build Order | `BUILD_ORDER_TD-AXIOM-GIT-PROVENANCE-REMEDIATION.md` as amended by `ITRGA_RULING_TD-AXIOM-GIT-PROVENANCE_P2_SCAN_SCOPE.md` |
| Trigger | The fixed §2 scanner still reports three Class-A shaped matches after authorized P-1 exclusions and P-3 document redaction: two are pre-existing D-2-permitted dev/evidence-runner literals in required source paths and one is ITRGA’s synthetic D-5 hook-demonstration literal retained in the ruling |
| DA posture | **HALTED before staging, index removal, commit, tag, hook activation, or source change** |
| Gate / Production | **CLOSED** / **NOT CERTIFIED** — unchanged |

## 1. Result under the fixed scanner

The approved §2 three-class scanner was applied as written after P-3 redaction. It reports:

```text
POST_P3_PROSPECTIVE_STAGED_DIFF_HIT_FILES: 3
POST_P3_PROSPECTIVE_STAGED_DIFF_HIT_OCCURRENCES: 3
```

Two are Class-A matches in pre-existing D-2-permitted source/evidence-runner configuration paths. The third is the ruling’s deliberate fake hook-demonstration assignment; it is listed in `TD-AXIOM-GIT-PROVENANCE_P3_DOCUMENTED_SCAN_EXCEPTIONS.md`. No matched value is reproduced in this request.

## 2. Why this requires a count disposition

D-2 states that existing dev/test constants may remain and opens `TD-AXIOM-DEV-CREDENTIAL-LITERALS` to track them. D-4/D-5 also require the authority record to remain legible and later require a deliberately fake assignment for the hook demonstration. The same ruling requires:

```text
STAGED_SECRET_MARKER_COUNT: 0
```

and states that a non-zero result halts the unit. It does not specify whether D-2-permitted source constants:

1. remain counted, therefore halt P-2 despite being permitted; or
2. are formal, named exceptions reported separately from the secret-marker count; or
3. require a distinct final treatment before the anchored baseline may be committed.

The DA will not create a source-path allowlist, subtract a count, or label the outcome zero without an explicit ruling. That would turn an approved value-oriented scanner into an unreviewed filter and risk a false-clean result.

## 3. Requested narrow decision

Please determine one of the following explicitly:

- **A — Formal D-2 exception manifest:** authorize a named, immutable path/line/Class manifest for the two existing D-2 literals and the one retained D-5 synthetic demonstration; require separate D-2 and D-5 exception counters, and define whether `STAGED_SECRET_MARKER_COUNT` excludes only those exact reviewed occurrences.
- **B — Remediate before baseline:** issue/authorize a separate security-remediation action for the two D-2 literal values, and separately prescribe the retained D-5 synthetic-demonstration treatment; then resume this metadata-only unit after the required work closes.
- **C — Count remains blocking:** confirm the unit remains halted until a different governed solution is provided.

If A is selected, prescribe the required manifest fields, whether values must be hashed rather than printed, and the pre-commit hook behavior when a known-exception line changes.

## 4. Work completed without overreach

- P-1 ignore rules are present in `.gitignore`; no existing tracked file has been removed from the index.
- P-3 redaction is prepared in the authorized document families with a filename-only manifest: 37 files, 71 Class-A values, 1 Class-B URL, 0 Class-C values; one retained synthetic ruling demonstration is separately documented, not silently filtered.
- No source/test/configuration value has been edited; no commit/tag/history rewrite/force-push/hook activation has occurred.

**We do not convert a known exception into a hidden exception. We request the exact counted form.**
