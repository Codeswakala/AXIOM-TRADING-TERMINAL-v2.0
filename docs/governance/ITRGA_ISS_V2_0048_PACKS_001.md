# ITRGA ISSUANCE 001 — 0048 APPLY + VERIFY PACKS (CONSOLE RE-TARGET EDITION)
# ITRGA-ISS-V2-0048-PACKS-001 · v1.0.0 · 2026-09-05 · AXIOM V2 / BE-8
# Office of the Independent Technical Review & Governance Authority (ITRGA)
# Authority chain: BO-V2-BE-8-001 T-1…T-18 → ITRGA-ACC-V2-BE-8-INT-001 (INT ACCEPTED
# + DRIFT GATE) → ITRGA-ACT-V2-BE-8-0048-001 → AXIOM-V2-BE-8-0048-HALT-001 (act VOID at
# §3.3, halt LAWFUL) → ITRGA-RULE-V2-BE8-HALT-0048-001 §2 (re-target RULED; the
# Operator's authorization of 2026-09-05 stands for the same act).
# Pattern: ITRGA-V2-0047-APPLY-PACK-V4 / RESUME ed-2 / VERIFY-V5 ed-3 households.

## §1 — Artifacts of record (hash-gate by MD5 FIRST)

| Instrument | Bytes | MD5 |
|---|---|---|
| `ITRGA_V2_0048_APPLY_PACK_V1.ps1` | 331,016 | `E4467526A38D655B2AA44BC8611D77ED` |
| `ITRGA_V2_0048_VERIFY_PACK_V1.ps1` | 37,223 | `F30B63D52087D566D5FF13E736972018` |
| `ITRGA_V2_0048_BASELINE_PINS.txt` | 764 | `13FCCFB0C0E174AA63AD14CB818FD52F` |

All three at the repository root. First editions — nothing retired.

## §2 — Law carried (recital)

- **E-0046-DUP**: refuse-if-completed records (apply/verify); console sweep — the backend directory must hold exactly one `axiom_dev.db*` entry; anchor lives under `operator-evidence\BE-8\`.
- **Sealed-lineage identity gate** (the R1 ruling's core): pre-mutation DB sha256 must equal `27bda311…c776f` AND `alembic current == 20260903_0047 (head)`, single head. Deviation => typed `act.target.not_working_lineage`, no mutation possible.
- **Pure-read law**: everything before A5 (APPLY) and the entire VERIFY pack is read-only on the DB (VERIFY attests unchanged bytes across its own run); the one sanctioned mutation is `alembic upgrade head` 20260903_0047 → 20260904_0048.
- **Independent re-proof**: VERIFY parses the apply record strictly (15-key set) and re-computes every gate from live bytes — corpus 20-file census, V1 six-pin floor, censuses 58/57/10 with exact members, compver triple (DB row == embedded literal == on-box rolling-hash recomputation of the 4 source files: PXS `c58a06a5…d106c0`, PRG `ed6434fa…376b1b`), 8 paper tables, compver delete-guard == 1, six live transactional guard probes with exact migration-literal messages, suite floor 1026, drift gate (non-zero exit, zero BE-8 tokens, inheritance witness).
- **PGF-021** (no filesystem-conditional behavior): every Test-Path is a hard stop-gate, never silent branching.
- **PGF-022** (output-shape gates): suite/current/heads/drift gates validated offline against real captured shapes before issuance (§3).
- **PGF-023/PGF-017/PGF-018/PGF-020** lessons: parenthesized concatenations in evidence/records; native stderr via Invoke-Capped; probes were mapped tuple-by-tuple against the migration's own `_TRIGGERS` literals (16 parsed, 6 plan entries exact on name/table/event/message).

## §3 — Pre-issuance proof battery (executed; results)

1. **Payload integrity**: the APPLY pack's 20 embedded base64 blocks were re-extracted and hashed — **20/20 == the §PINS corpus** (the same pin table as ITRGA-ACT-V2-BE-8-0048-001 §2).
2. **pwsh 7.4.6 AST**: APPLY 7,111 tokens **0 parse errors**; VERIFY 3,807 tokens **0 parse errors**.
3. **Ascii/punct battery**: printable-ASCII only both packs + pins; zero CR; parens 805/805, 362/362, 1/1; braces 247/247, 135/135, 0/0; zero `$(` subexpressions; here-strings 24/24 (APPLY); all native calls through Invoke-Capped (18/12 sites).
4. **Gate-shape proof (harness, 18 shapes, 18/18 CORRECT)**: suite gate (bare-green PASS incl. the recorded real tail shape `1026 passed, 2 warnings in 506.96s`; decorated-green PASS; 1025+1fail THROW; 2failed+1024passed THROW; counterfeit `21026 passed` THROW; wrong-floor `126 passed` THROW); current/heads parse gates (5 shapes); drift gates (witness PASS ×2; BE-8-token THROW; zero-exit THROW; no-witness THROW); pins strict-parse (real file PASS; tampered floor THROW by the value gate).
5. **Helper live-runs**: rollhash executed against the pin-verified corpus — prints exactly `c58a06a5…` / `ed6434fa…` (the pre-declared apply-time compver); poststate smoke-run returns the exact JSON contract (8 tables, version row, guard count).
6. **Pre-issuance defects caught and repaired by this battery** (recorded, not hidden): header-block joiner (char-per-line), one unquoted connector word in the amend-adjudication refusal line, and a definition-placement order for `$FilePinsAfter` (StrictMode would have thrown on the deviation branch). All three died inside the battery, never reached the field — the 0047-ed-1 lesson applied to itself.

## §4 — Field order

1. MD5-verify all three §1 artifacts FIRST.
2. Application STOPPED. Run `powershell -NoProfile -ExecutionPolicy Bypass -File ".\ITRGA_V2_0048_APPLY_PACK_V1.ps1"` from the repository root; answer the one prompt with the absolute DB path.
3. On APPLY PASS: run `.\ITRGA_V2_0048_VERIFY_PACK_V1.ps1`; keep the application STOPPED until VERIFY prints VERIFIED-COMPLETE-0048.
4. Return to ITRGA: `operator-evidence\BE-8\0048-APPLY-RUN-V1.txt` and `0048-VERIFY-RUN-V1.txt` (plus, verbatim, any STOP text if either pack halts).

Failure law unchanged: any STOP — modify nothing, return the transcript verbatim. A post-mutation halt correctly refuses at the identity gate on rerun (the DB is no longer sealed); a RESUME edition would be issued the 0047 way. The A2 anchor (sha == sealed lineage) is the lawful rollback surface, retained outside the apply path.

**We don't guess. We prove.**
— ITRGA-ISS-V2-0048-PACKS-001 · v1.0.0 · 2026-09-05
