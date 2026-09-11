# DELIVERY REPORT — BO-F-01
## Assistant Input Surface (the ask path)

| Item | Value |
|------|-------|
| Build Order | `BO-F-01` (Operator directive 2026-08-21: "authorized") |
| Predecessors | B-06 (backend ask path) · F-00 (design foundation) · BO-B-AUDIT CLOSED (ITRGA 2026-08-21) · custody decision recorded (BO header) |
| Implementer | Development Authority (DA) |
| Deliverable class | Frontend implementation unit (chain position 32) |
| Governance Gate | CLOSED · Production NOT CERTIFIED (unchanged) |
| Determination | Awaiting ITRGA independent determination (BO §12) |

---

## 1. Claimed scope vs. this Build Order

Executed exactly BO-F-01 §2: F-01.1 ask client + hook, F-01.2 accessible input
+ grounding selector + submit, F-01.3 grounded/refusal rendering with honest
states, F-01.4 boundary invariants. §3 exclusions honored: no external LLM, no
actuation controls, no backend contract change (a pure consumer of B-06), no
ungrounded client-side generation, no design-language weakening, no repo
publication. §6 allowed files plus one disclosed addition (D1). The register
rows ship in the patch per the standing append-only convention (BO §9 binding).

## 2. What changed (files + SHAs + chain position)

Patch `f01.patch` — **chain position 32**, 5 files (3 modified + 2 new), zero
backend files. Applies clean onto `34f4c62` + elements 1–31; post-apply cmp
5/5; register hunk proven to apply onto a drifted (baseline-era) register too.
Patch sha256: `a9623927701474eadb3c308cb87a096e21f28f60d8e247abc29898dba7e7a9bb`.

| File | Change |
|---|---|
| `frontend/src/api/assistantClient.ts` | `askAssistant(prompt, groundingSourceIds)` → POST assistant-respond (Bearer, B-06 body contract, structured 4xx detail mapping, typed `ApiError` 401) + `useAskAssistant` hook; GET functions byte-untouched |
| `frontend/src/workstation/ai/ContextualAssistantPanel.tsx` | `AssistantAskComposer` (input + grounding picker + grounded/refusal render + honest states) integrated; `GROUNDING_FAMILIES` registry (8 families); chips pre-fill the input |
| `frontend/src/workstation/ai/ContextualAssistantPanel.css` | **New** — component stylesheet, pure `var(--ix-*)` token consumption (D1) |
| `frontend/src/test/f01_assistant_ask.test.tsx` | **New** — 17 tests (§7) |
| `docs/governance/TECHNICAL_DEBT_REGISTER.md` | This unit's rows + B-AUDIT CLOSED status row — pure-addition hunk in the patch (§8) |

## 3. Ask-surface description

- **Input:** labelled text input (`Ask the grounded assistant`), placeholder,
  `maxLength=1000` (B-06 bound), inside the form that owns the submit button —
  Enter submits (proven in-browser; jsdom lacks implicit submission, D2).
  Submit disabled while empty or submitting.
- **Grounding selector:** toggle → picker listing persisted artifacts across
  the eight B-06 families with a client-side GET (five B-04 report families,
  chart annotations, journal entries, trade-plan notes; dataset snapshots have
  no client GET — excluded honestly, D3). Checkbox selection with a client-side
  ≤10 cap (overflow checkboxes disabled; counter `n/10`), removable selected
  chips. **No selection is honest:** submit works and the backend's
  GROUNDING_REQUIRED refusal is rendered as the assistant's answer, not an error.
- **Suggestion chips:** now clickable pre-fill shortcuts (the existing
  `onSelectPrompt` contract preserved byte-for-byte).
- **Rendering:** grounded → `grounding_summary` + `source_artifact_ids` +
  `response_text` + mandatory disclaimer + muted `audit-correlation` id;
  refusal → classed badge (`Refused: <CLASS>`) + disclaimer, visually distinct
  border. Submitting skeleton, error banner, 401 notice — nothing fabricated
  while loading or on failure.

## 4. Screenshot evidence (Level-I, `docs/evidence/f01/`)

| Capture | File | Result |
|---|---|---|
| Empty state (before any ask) | `f01_ask_empty.png` | Input + disabled submit + empty recent list |
| Grounding picker | `f01_grounding_picker.png` | 2 real artifacts listed (correlation + regime, seeded from the real corpus) |
| Grounded answer | `f01_ask_grounded.png` | r=0.7321 summary, source id, disclaimer, audit-correlation `8f0600f8-8287-487e-a916-1dcc90fc962b` — a REAL B-06 round trip |
| Refusal | `f01_ask_refusal.png` | `Refused: ORDER_INSTRUCTION_REFUSED` rendered distinctly |
| Probe log | `f01_capture_log.txt` | a11y sampling, Enter-key submission, no-actuation scan (violations: none) |

The backend log for the capture window shows two `POST assistant-respond` 201s
with `assistant:ask_responded` pipeline events — and, notably, **zero
audit-savepoint errors under the concurrent page load** (the B-AUDIT fix
holding in the same stress shape that exposed it).

## 5. Boundary-invariant evidence

- **No actuation:** the composer test + the capture scan assert the surface
  text contains no order/broker/execution/account vocabulary; the only buttons
  are ask/submit/toggle/checkbox/chip/collapse.
- **No external LLM:** the ask goes to the local backend only (client code has
  no third-party origin; the B-06 backend persists `external_llm_used: false`).
- **Disclosures preserved:** the panel's mandatory disclaimer, the RESEARCH-ONLY
  framing, and the deterministic-local self-description all remain; the result
  block re-renders the backend's own disclaimer text.

## 6. Test evidence (executed)

- Workspace full frontend suite: **906 passed / 176 files** (889 floor + 17
  new), 161.08s, exit 0 — `f01_vitest_fullsuite.log`.
- Typecheck: `tsc -b` exit 0, zero diagnostics — `f01_tsc.log`.
- Production build: green (chunk-size warning pre-existing).
- Clone-side (gold standard): pristine `34f4c62` → 32 elements → `npm ci` →
  tsc clean → **906 passed** — `f01_cloneside_vitest.log`.
- New tests: client POST contract/auth/401/structured-422; composer
  accessibility (label/placeholder/in-form/disabled-empty); trimmed-prompt
  submit; grounded render fields; refusal distinct + not-an-error; 401; error;
  grounding cap-10 + remove; empty-grounding submit; no-actuation scan; chip
  pre-fill; panel disclaimer; hook lifecycle; family registry pin.

## 7. Deviations register

| ID | Deviation | Assessment |
|----|-----------|------------|
| D1 | `ContextualAssistantPanel.css` — a new stylesheet file, not named in §6 | The component's stylesheet (the named component's own file umbrella); pure token consumption, no hex literals, passes the design-governance scans. |
| D2 | Enter-key unit test drives `form.submit` instead of the key event | jsdom does not implement HTML implicit form submission; the keyboard path is proven in the Level-I capture (real Enter press produced the ask). |
| D3 | Grounding picker offers 8 families, not dataset snapshots | No client-side GET exists for snapshots; ids of other families cover the B-06 contract. Picker note text states the honest empty case. |
| D4 | New test file under `frontend/src/test/**` | Explicitly allowed by §6. |

## 8. Register rows in patch (confirmed)

The patch's register hunk is a zero-context pure-addition (12 appended lines):
TD-B-AUDIT-UNIT-STATUS (CLOSED — APPROVED WITH OBSERVATIONS),
OBS-B-AUDIT-1 (residual future unit), TD-F01-UNIT (this unit). Verified in the
transcript to apply onto the chain-31 register (cmp byte-identical) AND onto a
baseline-era drifted register (DRIFT-PROOF OK). Append-only convention honored.

## 9. Transmission manifest (relay-accurate, CA-TRANSMIT-1)

All files newly transmitted with this delivery; byte-identical copies in
`/home/user/f01_transmission/`, cmp-verified; hashes mechanically verified
against the folder before this message (sha256sum -c MANIFEST.txt exit 0). This
report's own sha256 is declared in the DA's closing message; `MANIFEST.txt`
carries it.

| # | File | sha256 |
|---|---|---|
| 1 | `f01_transmission/f01.patch.txt` | `a9623927701474eadb3c308cb87a096e21f28f60d8e247abc29898dba7e7a9bb` |
| 2 | `f01_transmission/f01_applycheck_transcript.txt` | `66956a1d575e99982076f8f1df581989215f99f6c142cea17392098cfe8d4423` |
| 3 | `f01_transmission/f01_ask_empty.png` | `49b908cec104af222c0667f132575ab1a218e8e9eb77aa157048ccb1d2b14a84` |
| 4 | `f01_transmission/f01_ask_grounded.png` | `e2d297555bdf9d630e03c5b2d5646c5dfcdf2fb3154ae69d43b7595a9305b8f5` |
| 5 | `f01_transmission/f01_ask_refusal.png` | `7f2a1b07d7f3a4bbf04fe3b1abed4a5d2364b206cfa557da34c9613afdf76cd8` |
| 6 | `f01_transmission/f01_capture_log.txt` | `a85f751d321311747fc6ca398d45b657c8bb51729122fa63544ec3a86450c776` |
| 7 | `f01_transmission/f01_cloneside_vitest.log.txt` | `0be16e7293648b602dc39ce073f92d515d964cbf7ce8acdc211cd9c58bdb2475` |
| 8 | `f01_transmission/f01_grounding_picker.png` | `d19e1d15f1e4826687138d63b02868cdfc495f5400dac84b0bd2059c91bd1deb` |
| 9 | `f01_transmission/f01_tsc.log.txt` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| 10 | `f01_transmission/f01_vitest_fullsuite.log.txt` | `9302d84e58d22f2748cc7017b07fbf1c68fe5613311fca54a9beb8a29b5d9570` |

---

**Gate CLOSED · Production NOT CERTIFIED · We don't guess. We prove.**
