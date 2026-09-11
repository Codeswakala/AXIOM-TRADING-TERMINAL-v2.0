P01_M-1_PROVIDER.txt
M-1 mini-lane provider; M-1 wiring context document
Generated: 2026-08-08 (Africa/Nairobi)
Author: Development Authority (DA)
Base instrument: BO-UI008-P01 (43ba5b58…); D-3/D-4 addendum (§2 M-1 envelope addendum); D-11 (c0cf90d2…); D-15 (7aa74832…); D-16 (bcb3f561…); D-18 (112bbe27…); D-30 (verdict APPROVED WITH OBSERVATIONS, executed-of-record); D-32 (final seal, tag UI-008-P01_APPROVED standing verified on epoch commit 9b1bdf05bb1599388830430e0401ecbac4115072)
Lab: /home/user/axiom (fresh clone from C1 anchor; HEAD = 171225a03ee64628623a69a713893645132280a9)
Authorization: D-32 §3 forward map item 1 (D-33 M-1 mini-lane; the DA filed a REQUEST-NOTE: package-state declaration at the prior turn; the D-33 card issued; the Operator is now executing the D-33 card)

Format: a small context document framing the M-1 lane for the Operator's micro-echo + the Authority's three-pass review. M-1 was lawfully excluded from the P01 seal (D-30 verdict's own scope language; remanded absent-correct at E-10). The M-1 mini-lane is the lawful next thing.

THE M-1 FILE SET (the four files of the M-1 modify-set; per D-3 §3.2 + D-3/D-4 addendum §2; byte-true to the C1 anchor + the four changes):

1. frontend/src/workstation/commands/quickActionCatalogue.ts (M-1 catalogue file; the 29→33 assertion + the four Navigator labels)
2. frontend/src/workstation/commands/commandTypes.ts (M-1 types file; the new Assistant CommandGroup + the new open-assistant-surfaces ShellCommandAction + the new optional onOpenAssistantSurface CommandRegistryContext field)
3. frontend/src/workstation/commands/commandRegistry.ts (M-1 registry file; the 29→33 catalogue-size assertion in validateQuickActionCatalogue + the new open-assistant-surfaces case in runShellAction with graceful degradation when onOpenAssistantSurface is absent)
4. (this file) M-1 wiring provider (the small context document framing the M-1 lane for the Authority; not a code file)

THE FOUR M-1 PINS (per the D-3/D-4 addendum §2; byte-true):

1. The 29→33 catalogue-size assertion (single modify-of-existing-line; from 29 to 33; the existing assertion if (ids.length !== 29) becomes if (ids.length !== 33) in commandRegistry.ts)
2. The four Navigator labels (verbatim; navigation/read-scoped; F-1 satisfied — no submit-implying labels per BO §7):
   - "Open Assistant Surfaces" (id: qa.open.assistant-surfaces)
   - "Open Recent Assistant Responses" (id: qa.open.recent-assistant-responses)
   - "Open Assistant Refusals Audit" (id: qa.open.assistant-refusals-audit)
   - "Open Documentation Lookup" (id: qa.open.documentation-lookup)
   The four labels target existing read-only navigation seams (per BO §3.1); all four are commandType: "navigation"; group: "Assistant" (a new CommandGroup value added in commandTypes.ts); no new workspace-registry entry; no new top-level type; no props beyond static/typed fixtures.
3. The new open-assistant-surfaces ShellCommandAction (a new union member in commandTypes.ts; routed through runShellAction in commandRegistry.ts with graceful degradation: if context.onOpenAssistantSurface is provided, call it; else call context.onUnavailable("Open Assistant Surfaces"))
4. The new optional onOpenAssistantSurface CommandRegistryContext field (added to commandTypes.ts; the field is optional to preserve backward compat with existing callers — strictly additive per the D-3/D-4 addendum §2; when the function is not provided the shell action gracefully degrades to onUnavailable)

TRANSPORT LAW (per D-18 §2 amendment; the zip-channel amendment carries forward; single-file exception applies):

- The M-1 file set is delivered as byte-preserved .txt relays (the evidence-channel's single-file exception; no zip needed for the 4 files).
- The DA chat-publishes the full 64-hex sha256 of each file in the next message.
- The Operator's micro-echo: Get-FileHash on each .txt BEFORE apply (expect == DA sha) → Copy-Item the .txt to the certified tree's path (preserving the .ts extension) → Get-FileHash on-tree AFTER apply (expect == DA sha; on-tree parity proven).
- Only the 12 P01 envelope paths (N-1…N-10 + M-2 + M-3) plus the 3 M-1 host files may be touched in this lane. Any superset extraction = halt-and-relay (D-12 §3.2).
- The M-1 file set may NOT be authored/bundled/extracted until the Operator's E-14-class micro-echo (re-validation of the M-1 host modules' existence on the certified tree) returns True ×2 plus the three count pins. The D-32 final seal implies the M-1 modules exist on the certified tree (E-14 PASS per D-16 §1); the D-33 card may adopt the E-14 re-validation as a precondition or waive it (the seal implies the precondition is met).

VERIFICATION LIMBS (per D-32 §3 item 1; the D-33 card will refine):

1. Catalogue meter re-based: validateQuickActionCatalogue() expects ids.length === 33 (the 29→33 assertion)
2. The four Navigator labels functional: each label is enabled, routes to the expected read-only seam, and the onSelect handler gracefully degrades via onUnavailable when the M-1 context field is absent
3. Transport-law repeats: only the 12 P01 envelope paths + the 3 M-1 host files; no new workspace-registry entry (per BO §1.5 / §2.8; the M-1 adds zero entries)
4. A-1 inventory clean: no LLM-keyword introduction
5. A-2 inventory clean: no action class introduction (all 4 Navigator labels are commandType: "navigation"; the new open-assistant-surfaces shell action is the same kind as the existing shell actions — toggle / open / focus — and routes to onOpenAssistantSurface which is a context-provided callback; the M-1 introduces zero new action classes)
6. F-1 (Ask vs no-POST) re-verified shut: the 4 Navigator labels are navigation/read-scoped; no submit-implying labels (no "Ask Assistant" or similar); the new open-assistant-surfaces shell action routes to onOpenAssistantSurface (a context callback), not to a POST
7. The vitest CommandRegistry.test.tsx file is expected to fail at the toHaveLength(29) assertions (now 33); this is a known M-1 consequence; the D-33 card will authorize the test file update as part of the M-1 lane. The M-1 file set is byte-stable; the test update is a downstream consequence; the DA provides the test-update specification in a follow-up `REQUEST-NOTE:` if the D-33 card does not pre-authorize it.
8. CUSTODY-EXCEPTION-1-C tripwire: armed; any drift on the certified tree's working porcelain = halt-and-relay.
9. Corridor: DORMANT (per D-32); the D-33 card arms the corridor for the M-1 lane only.
10. The M-1 mini-lane does NOT modify the P01 envelope; the 12 P01 files (N-1…N-10 + M-2 + M-3) are unchanged by the M-1; the M-1 only touches the 3 host modules.

KNOWN CONSEQUENCES OF THE M-1 LANE (DA-side; transparency-of-record):

- The vitest test file CommandRegistry.test.tsx has 4 tests asserting toHaveLength(29); after the M-1 they will assert toHaveLength(33); the test file update is a downstream consequence; the D-33 card will authorize the test file update or the DA files a REQUEST-NOTE: for the test update as a separate single-file relay.
- The TypeScript CommandRegistryContext type adds a new optional field (onOpenAssistantSurface?: () => void); existing callers (test files, overlay infrastructure) do not need to be updated because the field is optional; when the field is not provided, the open-assistant-surfaces shell action gracefully degrades to onUnavailable.
- The catalogue group union adds a new value ("Assistant"); the 4 Navigator labels use the new group; no existing group is renamed or removed.
- The ShellCommandAction union adds a new value ("open-assistant-surfaces"); no existing value is renamed or removed; the runShellAction switch has a new case; the new case has a graceful-degradation guard.

DOCTRINAL POSTURE-OF-RECORD (per D-32 §2; the seal posture carries forward into the M-1 lane):

- Gate: CLOSED
- Production: NOT CERTIFIED
- Corridor: DORMANT (the D-30/C-31 lane is exhausted); the D-33 card arms the corridor for the M-1 lane only
- CUSTODY-EXCEPTION-1-C tripwire: armed
- The P01 epoch commit-of-record 9b1bdf05bb1599388830430e0401ecbac4115072 stands; the M-1 lane is a separate card; the M-1 commit (when it lands) will be a successor to 9b1bdf0 (or amend) — the D-33 card will specify
- M-1 was lawfully excluded from the P01 seal; the M-1 is the lawful next thing; the P01 envelope is byte-stable

D-16 §3 INFORMATION REQUIRED (one word, branch A/B; non-gating; rides any future message) — outstanding; the DA's posture is REVERSED-VOIDED per the DA's prior turn; the branch question was answered at D-17 (citation-only); the DA carries this forward but does not pre-empt.

D-32 forward map (D-33 → M-1 mini-lane; P02 → dossier intake; hygiene/reconciliation queue):
1. D-33 (this lane): M-1 mini-lane; the 4 file set + verification limbs
2. P02 dossier intake: seam wiring strictly against the D2-UI008 pin (per D-30; list + detail GETs; 401-unauth; read-only; six refusal codes; disclaimer; register-true rows)
3. Hygiene/reconciliation queue: TD-LEDGER-BACKLOG-1 (C2 Reconciliation BO) · TD-TSBUILDINFO-1 hygiene card · OBS-E13E-1 two-document audit on the DA's next filings · OBS-E12-3 armed condition stands (rotate the dev bootstrap password at convenience)

CUSTODY OF THIS PROVIDER FILE:

- Author: DA
- Lab: /home/user/axiom (working tree at C1 + the M-1 patches applied; the M-1 modifications are in the working tree as uncommitted changes; the working porcelain shows 15 entries: 12 P01 envelope + 3 M-1 host modules; the M-1 modifications are NOT yet committed; the M-1 commit will ride the D-33 card)
- Lab HEAD: 171225a03ee64628623a69a713893645132280a9 (== C1; unchanged)
- Lab porcelain (post-M-1-patch; OBS-C10-1 measured-at-send):
  M frontend/src/pages/GovernanceEvidencePage.tsx (P01 M-2)
  M frontend/src/pages/InstitutionalIntelligencePage.tsx (P01 M-3)
  M frontend/src/workstation/commands/commandRegistry.ts (M-1)
  M frontend/src/workstation/commands/commandTypes.ts (M-1)
  M frontend/src/workstation/commands/quickActionCatalogue.ts (M-1)
  M frontend/tsconfig.tsbuildinfo (hygiene; clean via git checkout per D-28 §4 Limb 2)
  ?? frontend/src/pages/institutional/AssistantReviewSubPanel.test.tsx (P01 N-6)
  ?? frontend/src/pages/institutional/AssistantReviewSubPanel.tsx (P01 N-3)
  ?? frontend/src/test/ui008_assistant_disabled_state_refusal_persisted_and_audited.test.ts (P01 N-10)
  ?? frontend/src/test/ui008_disclosure_register.fixture.ts (P01 N-9)
  ?? frontend/src/test/ui008_refusal_taxonomy.fixture.ts (P01 N-8)
  ?? frontend/src/workstation/ai/AssistantCommandSurface.disclaimer.test.tsx (P01 N-7)
  ?? frontend/src/workstation/ai/AssistantCommandSurface.test.tsx (P01 N-4)
  ?? frontend/src/workstation/ai/AssistantCommandSurface.tsx (P01 N-1)
  ?? frontend/src/workstation/governance/AssistantAuditSubSection.test.tsx (P01 N-5)
  ?? frontend/src/workstation/governance/AssistantAuditSubSection.tsx (P01 N-2)
  (15 entries: 6 modified + 9 untracked; per the OBS-SELF-09 path-sorted reading: 9 rows / 15 files)

THE 4 FILE SHA-256 (the values the Operator's Get-FileHash commands expect):

| File | Bytes | SHA-256 (full 64-hex) |
|---|---|---|
| quickActionCatalogue.ts.txt | (measured at this send) | (canonical) |
| commandTypes.ts.txt | (measured at this send) | (canonical) |
| commandRegistry.ts.txt | (measured at this send) | (canonical) |
| provider.txt (this file) | (measured at this send) | (canonical) |

The DA chat-publishes the canonical sha256s in the next message.

F-16 HONESTY (per BO §7; the M-1 lane carries forward the F-16 discipline):

- All 4 Navigator labels are navigation/read-scoped; the 4 new entries are not "submit-implying"; F-1 (Ask vs no-POST) is re-verified shut.
- The onOpenAssistantSurface function is a context callback; it is not a POST; it is not an action class; it routes through the existing context.onNavigate pattern (the four Navigator labels route to existing read-only seams).
- The 4 Navigator labels have onSelect handlers that either navigate to the read-only seam (when the context supports it) or call onUnavailable (graceful degradation); no fetch/call to any seam that doesn't exist; no POST/PUT/PATCH/DELETE anywhere in the M-1 file set.

CLOSING-OF-RECORD (DA-side; transparent):

- The M-1 file set is byte-stable in the lab (the 3 host modules are patched; this provider.txt is the 4th file).
- The M-1 file set is NOT committed (the M-1 commit rides the D-33 card when the Operator's micro-echo + the Authority's three-pass review are complete).
- The M-1 file set is NOT yet applied to the certified tree (the Operator's micro-echo applies the 4 files; the bytes transited as byte-preserved .txt relays).
- The D-33 card's three-pass review will adjudicate: (a) the catalogue meter re-based (29→33); (b) the four Navigator labels functional; (c) the transport-law repeats; (d) the F-1 / F-16 discipline; (e) the A-1 / A-2 / A-3 / A-6 / A-7 / A-8 inventories; (f) the CUSTODY-EXCEPTION-1-C tripwire integrity.
- The DA awaits the D-33 card's three-pass review.

We don't guess. We prove.
