# TD-AXIOM-GIT-PROVENANCE — D-2 Permitted Exception Manifest

| Field | Value |
|---|---|
| Authority | `ITRGA_RULING_TD-AXIOM-GIT-PROVENANCE_D2_EXCEPTION_COUNT.md` §4 |
| Status | Two formally adjudicated D-2 exceptions; no plaintext value is recorded |
| Counter rule | `D2_PERMITTED_EXCEPTION_COUNT` must equal this manifest length exactly; raw Class-A matches remain visible in evidence output |

## Reviewed occurrences

| path | line | class | identifier | value_sha256_first12 | justification | disposition |
|---|---:|---|---|---|---|---|
| `backend/app/core/config.py` | 23 | A | `PASSWORD` | `240be518fabd` | Pre-existing local development/bootstrap fixture; D-2 permits retention in this metadata-only unit. | `TD-AXIOM-DEV-CREDENTIAL-LITERALS` |
| `scripts/diagnose_ui007_p06_r6_audit_visibility.ps1` | 15 | A | `PASSWORD` | `240be518fabd` | Pre-existing local evidence-runner fixture; D-2 permits retention in this metadata-only unit. | `TD-AXIOM-DEV-CREDENTIAL-LITERALS` |

The guard applies an exception only when **path + identifier + value_sha256_first12** all match. A new path, changed key, or changed value is an unreviewed Class-A match and rejects the commit.
