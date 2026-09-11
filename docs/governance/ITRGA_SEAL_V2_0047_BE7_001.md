# ITRGA ARCHIVE SEAL — BE-7 0047 ACT EVIDENCE SET
# ITRGA-SEAL-V2-0047-BE7-001 · v1.0.0 · 2026-09-04
# Seals the three field transcripts under ITRGA-CLO-V2-0047-BE7-ACT-001.
# Verification: each exhibit hashed, then content-checked against the
# witnessed machine ledger; all markers consistent; no edits were made.

| Exhibit | Bytes | SHA-256 | Verified markers |
|---|---|---|---|
| docs/governance/evidence/0047/0047-APPLY-RUN-V4.txt | 8,612 | 814d2f75b4ce7a3fb03581e9b59c166e92385e1067abf9d8f0bcd746d19fd3e3 | UTC start 2026-09-04T10:29:04Z; anchor section + anchor path; the sanctioned-mutation run (complete-as-ran lineage) |
| docs/governance/evidence/0047/0047-APPLY-RESUME-RUN-V1.txt | 14,968 | 4aaf5c4d1a258c1e3709e324138caf7190871880b7a048cccfa0cb5e4955b785 | RESUME ed-3 run, UTC start 16:00:03Z; 13 canonical STATE lines; 972 passed (1575.03s); COMPLETE - PASS; UTC_COMPLETED 16:28:07Z |
| docs/governance/evidence/0047/0047-VERIFY-RUN-V5.txt | 14,139 | 27d7b4ec6bdd579601f7ed20329654548293c00e477394ebfba8a71e76e827cd | VERIFY V5 ed-5 run, UTC start 17:56:16Z; ten probe OK lines; 972 passed (1177.17s); COMPLETE - PASS; UTC_COMPLETED 18:16:33Z |

Consistency cross-checks passed: DB sha 27bda311… / anchor 5bd60aff…
identical across runs; suite 972/0 twice; record UTCs match the state files
written on the box; instrument edition MD5s gated on-box before every run
(RESUME ed-3 BA6565C3…, VERIFY ed-5 97581F0E…; pins 32F9270B…).

ARCHIVE STATUS: SEALED. The 0047 act is closed with a complete, hashed
evidence set (this set + state records + anchor on the operator box; the
governance dossier CN -> REQ -> BO -> ACC -> CR -> CB-001/ACC -> ISS-006..009
-> CLO-001 -> this SEAL in docs/governance/).

**We don't guess. We prove.**
— ITRGA-SEAL-V2-0047-BE7-001 · 2026-09-04
