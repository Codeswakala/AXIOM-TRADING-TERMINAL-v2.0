# ITRGA-ACC-V2-BE-10-001 — BAND ACCEPTANCE — BE-10: SIGNAL-AGAINST-ACCOUNT INTELLIGENCE
`STATUS: BAND ACCEPTED, AWAITING APPLY INSTRUCTION — 2026-09-06`
`Chain: REQ (adopted) → DR (accepted) → BO (commissioned) → BUILD (1,121/0, 44 tests)
→ INT sandbox act COMPLETE (this record).`

## Register line
`0050 APPLIED — BE-10 FIELDED — 2026-09-06 — fielded file head 20260908_0050
(sha-after 90660b5d13cba8a662dac60bee13233669504e41ff418296d36278b50481f9de) —
32/32 three-layer corpus pins — census live 76/65/12 — ace-1.0.0 rolling-hash
532ef0ce…85fd VERIFIED on the fielded bytes — 12 sealed map rows + source row
(import/unknown/active) — digest ×3 byte-identical scratch↔fielded
(6a4df886…707f) — suite 1,121/0 post-apply (fielded file as basis) —
corpus frozen (32 pins).`
Findings ledger update: the pre-act environment blip (run of suite under system
Python — argon2 absent; collection error) was an operator-session interpreter
issue, NOT a code/corpus/path defect; under (.venv) the identical suite passes
1,121/0. Register note N-O12: prepend interpreter pretense check
(python -c "import sys; print(sys.prefix)" — must name .venv) before any act.
N-O13 (ITRGA-owned, non-gating, CLOSED at first-read): register originally
claimed digest "byte-identical scratch↔fielded" — false at 2 chars
(scratch …8863cbc8fb6… vs fielded …8863c6bc8fb…); L7 re-stated: determinism
is PER-WORLD (×3 witnessed everywhere), seeded rows carry per-env identity;
the lawful equality wire==engine-on-same-world held (6a4df886…707f).

## §1 — Corpus (32 pins; band law: enumerate fresh, never stale literals)
BE-9's 22 standing pins, with router.py + permissions.py **replaced**, + 10 new:

Standing (20, unchanged from BE-9 acceptance):
4ead368e7b928b1373707597ec52a403ab98acf224e45fc60e2cb32a80db8420 alembic/versions/20260905_0049_v2_be9_broker_read.py
ff17b157efc52a42c8bdea833cd78b9c0ff9d4bff10da1cd640adee3bb12609d app/db/models/__init__.py
0f310930efdf96b5b2ec28e9f45a30bf1c330fbf9dd42ecc3290e5ffb7406bc0 app/db/models/v2_broker_read.py
7b6b39b8a0704b4a3936bc4326ea04f6c89e6267b6b138e6cef5e5aa763f71b2 app/v2/broker_read/__init__.py
41e94b7e9407fdaddd932f88001b1bef0a0778ad49079ac47e076e09817e4a16 app/v2/broker_read/api.py
f2862af9a7ad28e9b468b2d5b84c47e3a363227778cc3d449db785894f785176 app/v2/broker_read/contract.py
66ad41394baa6765cf349129e494311749a85226b6e49fc9607ac0a322a0a8de app/v2/broker_read/health.py
(N-O9, ITRGA-owned, non-gating, CLOSED 2026-09-06: this row originally carried
…a328f0a8de — a two-hex-char transcription slip; DA-F1 cross-verification
caught it pre-act against REM-001 + disk (…322a0a8de). Ruling: bytes are the
authority; corrected in place. P-1's corpus gate accordingly enumerates pins
from the REM-001 manifests ON DISK, never from any prose re-copy.)
92d55d2d3b593224ec3757bcb02cd40e3d22b2b413e2f91c431cbe7c7fc5c6a5 app/v2/broker_read/providers/__init__.py
782482977da2df897f3f32d35e532dc8103f360caa35d4fb1defc2f875bab1c0 app/v2/broker_read/providers/exness_mt5.py
9420e1a09fd366268adaa9000b53071415f4e04b60d4103864f99750528aba9c app/v2/broker_read/reconcile.py
d1e5d4b56c881db4547dcea88ea2e4f34e8642509916907c0a228f47714dfa09 app/v2/broker_read/sync.py
a647531f3c8d821b39c01bca3a3af25f8f9470d4670183cfcff918ceaf1564ea app/v2/broker_read/vault.py
1438bac0405e0e99bf4147871257f3774a51da6edbfc100236c9d48dc9d99e29 tests/test_broker_integration.py
e3ad90e7221d90dbde98969ca0176b04155d3cac1e45d9fa2034b81c6dc406d4 tests/test_execution_research_safety.py
9ba9fd8290d5861911582a5286752c7ed5aee71c06e56acb9f4ac4337355f91f tests/test_v2_be9_boundaries.py
12733c46f5fe495513fe2f44b66eadee5845abb35b03ca0b97bdc23131610d5e tests/test_v2_be9_contract.py
379b0be85b57e8da66e429b289cb047e05668ea6039b112c86f8aae11a32f612 tests/test_v2_be9_migration.py
038f5fc2a8f23e4755579f526ff30b3a7e087602ea49aa8c3f9c61f21a938ca9 tests/test_v2_be9_sync.py
b6877ffcc96bfb93d9f3f9dab70a0e8654056bcc69fde85db4555e8852637045 tests/test_wave6_closeout.py
3b228e0218eead067117ee6ba810aafadd9e0c869f4fd7a1ec47fc433accec40 tests/test_wave7_closeout.py

New BE-10 pins (10 new + 2 replacements; verified 12/12 at INT):
a80c3bdda61bb5f88c891f5b06a998180a53ddeb9136dc97f8b6edbeeded5b0f app/v2/account_context/__init__.py
028de7f1777a4baf376450a10ac119fdab5f225b72a8163fdcd015299f96b6cc app/v2/account_context/contract.py
8ba3f24d2a09a4f2157b0aba5ee0701a595fd743a9aefa110e7e2390a7e98e0a app/v2/account_context/engine.py
ad6efae4b5eb833b7f682bc73789fa18f164ff9eb1fe38879ed4abae3c797437 app/v2/account_context/api.py
c11ccb57f1a1624b78cd231a431fba99ec8684d13969ab0bb4ee8de9b43d6770 alembic/versions/20260908_0050_v2_be10_account_context.py
38ba60d4841ae59c6d5e4eb94687555bc841d506477cef2f478e4dc36da4ef56 tests/test_v2_be10_contract.py
f6da5e3ac3f8d26b19d5fc6a2e6e64419a5d79b9b566f9253cdd74e04f223f83 tests/test_v2_be10_boundaries.py
b5416f97d8cfaeb435190e5a3539098e8fdb698bb0b1bd98add2a8d9bc4306b0 tests/test_v2_be10_engine.py
ed41e74c8991a83d0bc785cb8e53befb9d7ea860d4f08b877625e14ed732d5f9 tests/test_v2_be10_api.py
c3629c8dca2d951f9aff77687a497582af70d951e1a868b14b7a68b70fda9e95 tests/test_v2_be10_migration.py
REPL af1b4e264cfcab94841c9530011281dce7a222af84f6a60fc2b40ffb59a76018 app/v2/api/router.py (was a0368d1b…)
REPL 06df4b951776d9f39efba7cdcf2587597c3f8bbfd1e54f98f789fd5f7ed3ffba app/v2/rbac/permissions.py (was 556e3b10…)

## §2 — Findings ledger
N-O10 (ITRGA-owned, non-gating, CLOSED 2026-09-06): 0050 apply-gate fired correctly
at 28/32; forensic diffs adjudicated the four FAILs as BE-9-era GOVERNED
post-REM-001 transformations — the Q9/D-5 operator pinning act (contract.py +
its test arms) and the N-O1 INT-review refinement (sync.py + test arm). All four
were frozen into the BE-9 acceptance corpus (22/22-verified at 0049 apply) and
are therefore the corpus of record. **PIN SUPERSESSION REGISTER (standing):**
corpus gate = REM-001 pins ⊕ {contract.py: `f2862af9a7ad28e9b468b2d5b84c47e3a363227778cc3d449db785894f785176`,
sync.py: `d1e5d4b56c881db4547dcea88ea2e4f34e8642509916907c0a228f47714dfa09`,
tests/test_v2_be9_boundaries.py: `9ba9fd8290d5861911582a5286752c7ed5aee71c06e56acb9f4ac4337355f91f`,
tests/test_v2_be9_contract.py: `12733c46f5fe495513fe2f44b66eadee5845abb35b03ca0b97bdc23131610d5e`}
⊕ REM-010 pins (10 new + 2 replacements). Any future act-gate must enumerate
ALL THREE layers; raw REM-001 is no longer sufficient alone.
N-O11 (ITRGA-owned, non-gating, CLOSED 2026-09-06): the supersession value typed
into the gate (and briefly into this doc) carried a 1-char tail slip vs the
BE-9 acceptance register (…d785894f765176 → …d785894f785176, digit 8→6);
caught by the gate's own full-hash verification, corrected by enumeration
from the register of record. Standing amendment: diagnostics print FULL
hashes, never 16-char truncations (tracing tails is the whole point).
N-O8 (DA-owned, non-gating, CLOSED): INT verify-v1 parsed stdout only while alembic logs to
stderr → one false STOP; the upgrade itself was clean and on-target. Caught by the script's
own assert (stop-law behavior correct — conservative failure). Transcript-silence mitigated
by file-invoked scripts + Tee logs (adopted as standing practice).
Fielded-file interrogation at R-0 (twice witnessed): 0049/64/11, sha intact — no incursion.

## §3 — Terminal identities / posture
Working DB head: 20260905_0049 (pre-act). Apply target: backend\axiom_dev.db.
Investor-posture law unchanged; BE-10 touches no vault, no terminal, no network.

## §4 — THE 0050 ACT CONTRACT (P-0…P-5; same law as 0049, band-tuned)
P-0 transcript + preview-kill + app quiescence; MT5 need not be closed (untouched by seed).
P-1 corpus gate: 32/32 pin-exact (enumeration from this doc's §1 in-box; fresh).
P-2 fresh gate: fielded-file sha + rev (expect 20260905_0049) + census (76/64/11) printed.
P-3 apply: `alembic upgrade head` on the fielded URL — EXPECT EXACTLY ONE LINE
`20260905_0049 -> 20260908_0050` — parse BOTH streams (N-O8 restated law).
P-4 post-verify: rev 20260908_0050 · census 76/65/12 · `v2.account_context.read` row ·
compver `ace-1.0.0` with source_hash == live-replicated rolling hash of engine.py ·
12 sealed map rows + source row (import/unknown/1) byte-witnessed · digest ×3 identical.
P-5 suite: `pytest` banner MUST read `1121 passed`; corpus re-gate 32/32; Stop-Transcript.
STOP-LAWS: wrong target · chain ≠ 1 line · census miss · seed mismatch · digest nondeterminism
· suite banner miss · any refusal/exception — paste and halt; E-0046-DUP law standing.

## §5 — Register disposal tail (post-act)
`backend\be10_int_scratch.db` disposed after acceptance; `int_be10_verify*.py` disposal;
witness files (`BE10_INT_WITNESS*.txt`, `BE10_INT_VERIFY_LOG*.txt`) persist as evidence.
