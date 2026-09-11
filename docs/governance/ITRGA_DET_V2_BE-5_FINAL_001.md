# ITRGA FINAL DETERMINATION — V2 BE-5 (Predictive ML, Signal, and Research Governance Expansion)

- **DETERMINATION_ID:** `ITRGA-DET-V2-BE-5-FINAL-001`
- **Review chain:** `ITRGA-RVW-V2-BE-5-DR-001` (corrections C-1/C-2, CLOSED at intake re-open) → full-depth review of corrected package → this determination.
- **Subject delivery:** `AXIOM-V2-BE-5-DR-001` **v1.0.1** (corrected), evidence milestone `AXIOM-V2-BE-5-EM-001`.
- **Build Order:** `BO-V2-BE-5-001` (Operator-authorized).
- **Date of determination:** 2026-09-02.
- **Reviewer:** ITRGA (master-onboarding law: full-depth review; I author no code/design; corrections issued and resolved through re-delivery).

---

## 1. Verdict

**C — PASS: full-verify.**

Band BE-5 (0044+0045) is verified complete against every terminal-state pin of BO-V2-BE-5-001 (T-1…T-12), all five review pins P-1…P-5, and every governing-document law in scope. The correction cycle (C-1/C-2) executed cleanly: C-1 fully closed with executed post-fix evidence; C-2 correctly acknowledged and bounded to its own scope (working-DB application — unresolved by design at delivery time; its resolution is an Operator-side act). Recommendation for acceptance and registry synchronization is at §7 of this determination.

This verdict rests on: (a) the corrected Delivery Report v1.0.1, (b) three hash-pinned evidence artifacts whose cited MD5 and SHA-256 values the ITRGA recomputed **bit-exact from the transferred files**, and (c) an independent line-for-line source review of all 19 manifested files plus four independent cross-verifications (§3).

**Verified suite state:** `856 passed, 0 failed` (789 prior + **67 new BE-5 tests**: 24 decisions, 9 migration, 15 API, 3 diagnostics, 16 lifecycle) in a single continuous run (321.76 s); the 2 warnings sit in pre-existing V1-era modules and are not BE-5-attributable.

---

## 2. Terminal-state verification against BO-V2-BE-5-001

| Term | Pin | Result | Level | Notes |
|---|---|---|---|---|
| T-1 | Chain extension 0043→0044, artifacts named/pinned | **PASS** | I | Migration literals reviewed line-for-line; revision ids, parentage, docstrings match; per-file SHA-256 pins disclosed. |
| T-2 | 3 tables, columns/CHECKs/UNIQUE per pin; `record_seq`, `supersedes` (**post-C-1**), `model_type`, `instrument_class`, no `updated_at_event_id` | **PASS** | I | Every CHECK vocabulary compared literal-by-literal against the BO pin set; UNIQUE(artifact, seq) at schema AND behavioral in tests (INSERT dup refused, next seq allowed). P-1/P-2/P-3 exact. |
| T-3 | 6 triggers, exact names+messages, UPDATE-AND-DELETE, fail-closed on absence; 18→24 | **PASS** | I | `_TRIGGERS` tables match the 6 pinned messages verbatim; `_verify_triggers_present` raises on absence; executed message match asserted in tests via `str(excinfo.value) == message`; count 24 verified post-upgrade. |
| T-4 | 7 permission rows, admin×4 / operator×3, SAL-aligned; 27→34 | **PASS** | I | Revision-local literals (DEL-004), idempotent re-run guard; content-exact assertion incl. SAL column; count 34. |
| T-5 | compver 3→4; mge-1.0.0 pinned co-delivered; source hash = pinned algorithm over real file bytes | **PASS** | I | `_mge_source_hash()` performs `sha256(rel\0\|\|bytes\0 …)` over the 3 pinned mge files **at migration time on the Operator's disk** — exactly the mandated provenance; provenance-verification test asserts the row's hash equals a recomputation over the same files. |
| T-6 | 0045: 2 tables, 4 triggers (24→28), +1 permission (34→35), compver sge-1.0.0 (4→5) | **PASS** | I | sge files pinned = {signals.py, api.py}; same hash discipline; symmetric downgrade restores exact guard incl. recreation-verify. |
| T-7 | Decision contracts 5/5 RESEARCH-executable, spec citations, V1-config threshold citations, ≥1 pass + ≥1 typed refusal each; promotion enforces statuses+RESEARCH-mode+rollback-response-lifecycle+ladder+currency | **PASS** | I | 24 decision tests incl. exact-bound values; thresholds asserted equal to **live V1 config dataclass defaults** (no invented numbers); every refusal typed with `spec_citation`; `test_stale_record_seq_refused` proves generation-currency at the writer. |
| T-8 | Signal paths with uncertainty, provenance, limitations, expiry, typed states; permanent refusal rows | **PASS** | I | Refusal-as-record: row persisted with `state='refused'`, typed `state_reason`, `payload` NULL, event appended — permanent/apped-only; expiry = event-append, record row untouched and DB-immutable (`test_expiry_appends_event_row_immutable` proves row column unchanged). Withheld-derivation rule absent by design (no withheld producer band-locally) — see O-5. |
| T-9 | Zero V1/BE-1..4 mutating contact; additive permissions/RBAC only | **PASS** | I | No-touch group byte-compares BE-3 provider status/history and BE-4 compver before/after 0044/0045; RBAC modification is additive-only (enum + mappings, no renames/removals); V1 reuse proven by hash (§3-d). |
| T-10 | No new drift; zero BE-5 tokens at 0044/0045 heads; full declaration | **PASS** | I+ | Format-independent parametric gate at both revisions; direct executed runs appended to the API transcript: non-head → revision-offset refusal form; head (0045) → itemized form with **distinct tokens 9 = exactly the inherited V1 set**, BE-5/V2 tokens []. Declaration in DR §8.3 reaffirmed. |
| T-11 | Migration tests (content-based, PGF-012), no-touch, downgrade cycle, drift gates green | **PASS** | II | 9/9 migration tests passed in the raw transcript, on dedicated file-based SQLite chains with the consumed-authority env gate set **only inside tests** (comments reference the accepted transition-test pattern). |
| T-12 | API + RBAC + full suite ≥853, zero failed; fail-closed proofs | **PASS** | II | 856 PASSED / 0 FAILED, one run; RBAC: operator denied writes with generic message; unauthenticated 401; no-touch tests passed. |

**Level legend:** I = code + artifact review (recomputation at operator run pending under C-2 scope where noted); II = executed transcript verified raw; I+ = both, including direct executed runs.

---

## 3. Independent ITRGA cross-verifications

Beyond reading the delivered artifacts, the following were independently executed against the ITRGA's own clone:

1. **Evidence-package integrity (REV 2):** recomputed MD5 + full SHA-256 of all three artifacts — **all six match the DR-cited values bit-exact.** The package is self-authenticating.
2. **V1 reuse-pin:** recomputed full SHA-256 of `backend/app/ml/{validation,calibration,economic}/service.py` in the ITRGA repo — **all three match the disclosed pins** (`029f3f36…64e09`, `5cc28c6e…8f06dc`, `c49527ed…5fa13`). The promoted reuse-without-rewrite claim is proven; thresholds are extracted from these live configs at runtime, not retyped.
3. **BE-4 drift-test presence:** the questioned baseline test exists in-tree (pre-BE-5 form), confirming the disclosed reason for the 4th modified file: with 0044/0045 appended, 0043 is no longer head, and the BE-5-era revised test absorbs the generational scoping correctly (PGF-014 discipline, format-independent assertion).
4. **Post-C-1 code re-read:** `signals.py::_current_governance` now resolves the record, derives currency via record_seq max-projection, and refuses superseded generations — matching the executed refusal in the API transcript; the C-1 regression test `test_predictive_superseded_generation_refused` (855→856) covers the exact scenario.

---

## 4. Violations scan: **ZERO**

| Domain | Result |
|---|---|
| Execution-adjacent vocabulary (orders/brokers/positions/gates) in band namespace | None (forbidden-marker assertion green; RBAC taxonomy clean) |
| Credential handling | None (T-12: none prompted; transcripts contain no secrets) |
| Network | None (socket guards active per-module; refusal on attempt) |
| LIVE/PAPER posture | None (RESEARCH-only, mode-gated; `mode='LIVE'` promotion refused in tests) |
| Mutable-state shortcuts | None (all artifact surfaces DB-trigger-guarded; expiry/promotion via append/version semantics only) |
| Threshold inventions | None (V1-config extraction; cited per decision) |
| Data-class fabrication | None (first-landing refusal set exact; `historical_real`/`live` unreachable by design) |
| Undisclosed changes | None detected; the 6-file post-C-1 change set is itemized in transcript §0 and matches the fix scope precisely |

---

## 5. Corrections register — chain HEALTHY

- **C-1 (`superseded_by` → `supersedes`): CLOSED.** Applied across migrations (both 0044+0045 as appropriate), models (both), entry-point templates, the full lockstep set, and the P-5 pin cells; +1 regression test; post-fix executed evidence in the Rev-2 API transcript; affected artifact hashes re-cited and verified. The absorbed collateral (two latent defects — the `current_only` IS-NULL filter and the latently inverted currency check) was discovered, fixed, and **honestly disclosed** in DR §4 P-1 rather than silently bundled. Disclosure quality is itself a positive finding.
- **C-2 (working-DB claims): ACKNOWLEDGED — ETERNAL REGISTER.** The DR scopes Level I correctly (static target-state of the working DB) and does not exceed evidence. Resolution requires the Operator's own apply/verify act on `backend\axiom_dev.db`; C-2 closes only on that evidence envelope.

---

## 6. Observations register (all non-blocking; recorded for the archive)

- **O-1 — report typography:** DR §3 section header still reads "789 + 66 = 855" while its table and both transcripts correctly total 856. Typo-class remnant of the +1 regression test; **accepted**, no re-delivery warranted (a re-delivery would cascade every artifact hash for zero semantic gain).
- **O-2 — pin-quote remnant:** DR §3 T-2 cell quotes the BO's pre-C-1 `superseded_by` wording while the delivered artifacts use the corrected `supersedes`. The governing surface (BO + C-1 record + verified literals) is unambiguous; **accepted** as a textual quote, with this row as the standing gloss.
- **O-3 — `correlation_id` nullable at schema:** the delivered DDL makes `correlation_id` nullable on all five new tables where the plan text read as NOT NULL. Every sanctioned writer supplies it (auto-mint when absent), and the BE-1 contract surfaces (audit events, lineage records) carry correlation through the same envelope — so the contract's purpose is preserved while a direct SQL insert could technically omit it. **Accepted deviation** of the softened-constraint class; recommend a future tightening migration only if the platform ever exposes direct DB writers. Recorded, no action in-band.
- **O-4 — defensive family coercion in `signals.py`:** in the (API-unreachable) defensive branch, an out-of-vocabulary refusal still lands a permanent record coerced to family `predictive`, with the verbatim value preserved in `state_reason`. Unreachable via the governed template (400 first) and gives every emission request a permanent record — consistent with §5.1 (b); **accepted** as a wart, noted so future maintainers do not mistake it for an actual vocabulary expansion.
- **O-5 — `withheld` state:** the tiny-state vocabulary includes `withheld` with full DDL CHECKs, events and tests — but no band-local producer transitions rows into it (no scheduler/human-withhold endpoint in this band). Consistent with §5.3(b) (structural completeness; composition at the band's own boundary). No action.
- **O-6 — read-projection test weight:** `test_governance_list_current_only_projection` seeds a single generation, so the API-tier list filter would not catch an ALL-vs-CURRENT regression by itself. The projection semantics are nonetheless proven in the executed Level I evidence ($governance rows (4) → current_only total (2)$ with the exact seq/supersedes pairs) and the write-path currency gate has a dedicated regression test. **Accepted**; a multi-generation list assertion remains available as a future hardening test, out of scope here.

No observation contradicts the roadmap or a governing law; none triggered the issue-correction gate.

---

## 7. Recommendation to the Operator

1. **Accept the delivery** — verdict C-PASS; maturity rows `02-MACHINE_LEARNING_PREDICTIVE` (6-ML) and `03-SIGNALS_STRATEGY` (4-SIGNAL) move to **COMPLETE** via this determination, subject only to the working-DB evidence envelope (C-2).
2. **Registry synchronization (Rev 13)** exactly as DR §7.1: compose V2-ROADMAP (BE-5 paragraph + terminal-state block), V2_MILESTONES (BE-5 COMPLETE row with evidence date), V2-MASTER-CAPABILITY-TRACK (6-ML + 4-SIGNAL → COMPLETE with reference date), V2-MATURITY-APPENDIX (02/07 entries), V2-SPECS-INDEX (add 09_EXECUTION_FUTURES_SPEC), V2-EVIDENCE-INDEX, re-serialize after the last Op-level edit.
3. **File placement:** apply DR §9.1 (F1/F2/F3 exact destinations, no renames); the DR's own self-declared paths/hashes/sizes are consistent with the verified package.
4. **Optional-but-recommended: run the ITRGA-style live-apply/verify cycle on the working dev DB and archive both transcripts in-band** — that envelope closes C-2 and satisfies T-1/T-2 end-to-end on the working lineage. If the Operator prefers, the same cycle can run on a scratch copy first; either way the envelopes are the evidence C-2 lacks.
5. **Upon the above:** close BO-V2-BE-5-001; the roadmap chain moves to BE-6 planning under the standard ITRGA commissioning flow. **No BE-5 rework is open.** The DR's §10 roadmap note (execution/gate futures; signal family readiness; corpus-registration track) is logged for the next commissioning act.

---

## 8. Attestation

- ITRGA cloning/repo state verified unchanged throughout review (HEAD `fd8d649`; zero commits by this office; all ITRGA artifacts untracked in `docs/governance/`).
- No development performed; no plan/report co-authorship; review conducted at full depth as mandated by the Operator's standing rule (2026-09-02).
- All recomputations cited in §3 were executed independently in the ITRGA workspace; raw commands retained in session log.

**ISCRIVED AND CLOSED as DETERMINATION `ITRGA-DET-V2-BE-5-FINAL-001` — verdict C: full-verify PASS. Awaiting only the Operator's acceptance authorization; no further ITRGA action is pre-authorized beyond this delivery.**

---

### ADDENDUM 2026-09-02 (same day) — acceptance received

The Operator authorized final acceptance on 2026-09-02. Effects per §7: maturity rows COMPLETE; BO-V2-BE-5-001 CLOSED; registry-sync package issued. Record: **`ITRGA-DET-V2-BE-5-ACCEPT-001`**. Working-DB application completed same day: **`ITRGA-DET-V2-0045-APPLY-001`** (C-2 CLOSED). BE-5 chain terminates here.
