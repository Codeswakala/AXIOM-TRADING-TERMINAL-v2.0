=====================================================================
ITRGA ISSUANCE NOTE — 0047 WORKING-DB APPLICATION PACKS (BAND BE-7)
ITRGA-ISS-V2-0047-PACKS-001 · v1.0.0 · 2026-09-04
=====================================================================
Authority: BO-V2-BE-7-001 + ITRGA-ACC-V2-BE-7-001 §5 + operator
authorization ("proceed", 2026-09-04). Design record:
ITRGA-PLAN-V2-0047-APPLY-001 (A0–A10 / B0–B7).

THE THREE ISSUED ARTIFACTS — save ALL THREE to the repository ROOT:
  C:\Users\victo\.vscode\AXIOM\axiom\

  1. ITRGA_V2_0047_APPLY_PACK_V1.ps1     (255,113 bytes)
     MD5 = 7B9329C829AB86F36FFBF770F4EF9D4D
  2. ITRGA_V2_0047_VERIFY_PACK_V1.ps1    (28,812 bytes)
     MD5 = 60F56E188222EB62A0130E74A18727B9
  3. ITRGA_V2_0047_BASELINE_PINS.txt     (repo-root pin file)
     MD5 = 32F9270B1B56E9A9B78A0501FD8A6F80

BYTE-IDENTITY LAW (PGF-011): before running anything, verify all three
MD5s with Get-FileHash -Algorithm MD5. Any mismatch: STOP, report to
ITRGA, run nothing.

RUN ORDER (strict; each as a FILE from the repository root, PS 5.1):
  powershell -NoProfile -ExecutionPolicy Bypass -File ".\ITRGA_V2_0047_APPLY_PACK_V1.ps1"
  …then, only on its PASS…
  powershell -NoProfile -ExecutionPolicy Bypass -File ".\ITRGA_V2_0047_VERIFY_PACK_V1.ps1"

PRECONDITIONS: STOP the running application first (it holds a live
connection to backend\axiom_dev.db). Single input per pack: the
absolute path of backend\axiom_dev.db (a path, not a credential).
Runtime ~10 min per pack (the full suite runs in each).

RETURN CHANNEL: operator-evidence\BE-7\0047-APPLY-RUN-V1.txt and
operator-evidence\BE-7\0047-VERIFY-RUN-V1.txt back to ITRGA. Keep
0047-APPLY-FINAL-STATE.txt / 0047-VERIFY-FINAL-STATE.txt in place.
Restart the application ONLY after the verify pack PASSes.
=====================================================================
