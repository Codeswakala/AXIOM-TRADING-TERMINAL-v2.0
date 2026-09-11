# ITRGA DETERMINATION — UI-CONV-P03 · ITEM 5

**Reviewing body:** Independent Technical Review & Governance Authority
**Subject:** `GovernanceEvidencePage` → shell-owned governance overlay
**Date:** 2026-08-15
**Base:** `34f4c62` + verified item-3 patch (`b7b4c4f7…`) — **as declared by the DA**
**Verification:** `/tmp/i5` — pristine clone → item 3 applied → item 5 applied

| Artifact | sha256 | Content |
|---|---|---|
| `DELIVERY_REPORT_UI-CONV-P03_ITEM5.md` | `c62564fa0cc67374…` | 130 lines |
| `OPERATOR RESULTS.md` (DA transmission) | `32911ccb28fb0daf…` | 1,705 lines — transcripts + **1,689-line patch** |

---

## 1. DETERMINATION

# APPROVED WITH OBSERVATIONS

**Item 5 is verified in applied source. Every mandatory requirement is met.** One observation concerns evidence transmission, not engineering.

This is the most technically demanding item of the phase — 1,072 lines, seven exported constant tables, six external test suites coupled to the page — and it was executed cleanly with an unprompted disclosure of a real defect in already-approved work.

---

## 2. TRANSPORT — HASH-CONFIRMED, SECOND CONSECUTIVE CYCLE

```
extracted patch ........ 1,689 lines · 18 diff --git headers
sha256 ................. 4c03910c76fdcbf2…   ← EXACT match to declared
git apply --check ...... exit 0   (on 34f4c62 + item3)
git apply .............. APPLIED OK
```

**Base declared unambiguously** — *"`34f4c62` + the verified item-3 patch (`b7b4c4f7…`) — stated plainly per directive §7"*. This is exactly what I asked for, and it eliminates the stale-baseline class of error that produced the `5ef6c4e` regression. The patch applied first time on the stated base.

Transcripts were placed **before** the diff this cycle, which is cleaner to parse. LF endings, terminating newline — `OBS-CONV3-7` **closed**.

---

## 3. MANDATORY REQUIREMENTS — ALL VERIFIED

### M1 — Six governance suites re-pointed, none deleted ✓

All eight files in `workstation/governance/` intact. `grep -rn 'pages/GovernanceEvidencePage'` returns **one hit: a provenance comment** in `governanceRecords.ts:4` documenting the relocation. Zero live imports. `pages/GovernanceEvidencePage.tsx` **deleted** — deletion discipline held without prompting for the second consecutive item.

### M2 — `reasonCodeFor` verbatim ✓

Relocated to `governanceRecords.ts:201-209`, byte-identical including the regex `/^[A-Z0-9_]+_REFUSED$/` and the **`"—"` honest-absence fallback**. Named export retained for `AuditExplorer.test.tsx`.

### M3 — Four constitutional declarations visible ✓

```
GovernanceOverlay.tsx:475  <h3>Production certification boundary</h3>
                     :678  <h2>Standing Residuals</h2>
                     :707  <h2>Read-Only Governance Boundary</h2>
                     :738  <h2>Inert Display Rules</h2>
```

I searched for concealment machinery — `<details>`, accordion, `collapsed`, `activeTab`, `useState(open)`. **The single match is a docblock comment at :25 stating the rule itself.** No collapse mechanism exists. All four render as plain always-visible sections. Named test `test_uiconv_p03_governance_four_constitutional_declarations_visible_without_interaction` asserts them.

### M4 — No backend/schema change ✓

Three read endpoints unchanged. No backend source-inspection test referenced this page (I verified this before issuing the directive), and none required re-pointing.

### M5 — Per-section independent degradation ✓

**30 references** to the six independent loading/error state variables. Each panel consumes its own props. A failed audit fetch does not blank the certification boundary — the specific failure mode the requirement exists to prevent.

### Seven constant tables relocated ✓

All seven `UI007_*` tables present exactly once in `governanceRecords.ts`. Treated correctly as **declared governance state**, not converted to API calls. The directive's distinction was understood.

### Standing requirements

| Req | Result |
|---|---|
| **R2** `/governance` no 404 | `GovernanceRedirect` :52-53 → `/?open=governance`; registry `Component:` :378 ✓ |
| **R3** no fabricated runtime fallbacks | 0 ✓ |
| **R4** testids | **17** on the overlay (baseline 0) ✓ |
| **R6** RBAC | 16/16 wrappers, roles unchanged, 0 `unprivileged` ✓ |
| **`OBS-CONV3-4`** | **No stage claim made** — `grep 'view=governance'` in `TradingTerminalWorkspace.tsx` returns nothing ✓ |

---

## 4. THE DISCLOSURE — CREDITED, AND IT MATTERS

The DA reported, unprompted:

> the shell's overlay layer is `pointer-events: none`; neither the item-3 settings backdrop nor the item-5 governance backdrop re-enabled hit-testing, making both dialogs **click-transparent in real browsers** (jsdom tests cannot hit-test, which is why the defect escaped item 3's acceptance).

**I verified all three claims:**

```
InstitutionalWorkspaceShell.css:191,213   pointer-events: none     ← confirmed
WorkspaceSettingsOverlay.css:11           pointer-events: auto     ← item-3 fix, shipped here
GovernanceOverlay.css:10                  pointer-events: auto     ← item-5
```

**This is a genuine defect in work I approved.** The item-3 settings overlay was click-transparent in a real browser, and my determination did not catch it — jsdom cannot hit-test, so the passing suite could not have revealed it, and capture 02 showed a rendered overlay which looks identical whether or not it accepts clicks.

The DA found it during capture work, fixed both files, and **stated it in §1 rather than burying it in a deviations appendix**. That is the third unprompted self-disclosure of this programme, after the fabricated-statistics disclosure in P02 and the `view`-unparsed disclosure before item 4.

**Recorded as a limitation of my own method:** jsdom-passing tests plus a static screenshot cannot establish interactivity. For any modal, overlay or click-target surface, the evidence standard should include an interaction trace or an explicit statement that hit-testing was verified in a real browser. I am adding this to the register rather than to the DA's finding list.

---

## 5. OBSERVATION — `OBS-CONV3-9`: CAPTURES NOT TRANSMITTED

| Field | Content |
|---|---|
| **Requirement** | Directive §7.5 — Level-I captures, single self-contained HTML, base64-embedded. |
| **Evidence** | Report §6 describes **five** captures with sha256 prefixes (`0ba51031…`, `172de913…`, …) and names the gallery `UI-CONV-P03-ITEM5_CAPTURES.html` (sha `9cef5bd1…`) at "workspace root" with raw PNGs at `/home/user/uiconv_p03_item5_captures/`. **No capture file was attached to this delivery.** Those are DA-sandbox paths. |
| **Failure** | Captures described rather than transmitted — the same class as the earlier transport failures, now isolated to evidence rather than code. |
| **Mitigating** | The claims those captures support are **independently verified in source**: M3 declarations (§3), refusal viewer (M2), R2 redirect, M5 independence. Nothing rests solely on an untransmitted capture. |
| **Required Correction** | Attach `UI-CONV-P03-ITEM5_CAPTURES.html` with the next delivery. Include the empty/error-state capture **scrolled to the affected region** — `OBS-CONV3-5` remains open across three cycles. |
| **Owner** | DA |

**This does not block approval.** Every acceptance criterion is verified in code. But capture 05 is offered as the live evidence of M5 independent degradation, and that is a *behavioural* claim under fault conditions — the kind that source inspection supports but does not fully prove. I am approving on the source verification and recording the gap.

---

## 6. EXECUTION EVIDENCE

```
Test Files  165 passed (165)
     Tests  762 passed (762)      ← +7 vs item 3
tsc -b      (no diagnostics — exit 0)
vite build  150 modules · index-BKjF7rb8.js 687.56 kB │ gzip 185.16 kB
pytest      415 passed, 1 warning
```

**1,177 tests green.** Bundle 685.94 → 687.56 kB (**+1.62 kB**) for an overlay module, CSS and the records module — proportionate and disclosed under `OBS-5`.

Transcripts are raw console output, as required. `OBS-CONV3-6` remains closed.

---

## 7. DEVIATIONS DISCLOSED

1. **Seeded audit fixture** — one synthetic `audit_events` row (`assistant.response_refused`, `details.reason_code = EXTERNAL_LLM_REFUSED`) in the local dev DB to evidence the refusal viewer. Local only; no seed script or schema changed. Same accepted class as `sig-004` / `scen-002`. Register entry `TD-UI-CONV-P03-AUDITREFUSAL-EVIDENCE-FIXTURE`. **Accepted.**
2. **Item-3 pointer-events fix** — §4. **Accepted and credited.**

Stage view **deliberately rejected** with reasoning: *"the directive's `OBS-CONV3-4` warning makes any stage claim load-bearing… Item 4 owns that build; item 5 must not front-load a rendering-branch obligation."* **Correct judgement.** The overlay pattern is item-3-proven and makes no claim the code cannot honour.

---

## 8. STATUS

| Item | State |
|---|---|
| **UI-CONV-P03 item 5** | **APPROVED WITH OBSERVATIONS** |
| M1–M5 | All verified |
| `OBS-CONV3-7` CRLF | **CLOSED** |
| `OBS-CONV3-9` captures not transmitted | **NEW** |
| `OBS-CONV3-5` empty-state capture fold | **Open — third cycle** |
| `OBS-CONV3-4` stage rendering inert | Open — **blocks item 4 route conversion** |
| `OBS-CONV3-8` verified work outside the repo | **Open — now four items** |
| `OBS-PROV-2`, `OBS-5`, `F-BRAND-1`, `OBS-CONV2-5` | Open |
| P02 closures ×4 | Verified intact |

**Phase progress:** items 1, 2, 3, 5 approved. **Item 6** (`SignalInvestigationPage`, 425 ln) and **item 4** (`ResearchManagementPage`, 1,391 ln) remain.

**`OBS-CONV3-8` is now the largest standing risk.** Four items of verified work exist only as patches in this workspace (`item3_verified.patch`, `item5.patch`) and in the DA sandbox. Origin remains `34f4c62`. `/tmp/ap` was cleared by the sandbox between turns this cycle — the exposure is demonstrated, not theoretical. I hold reconstructable copies; that is a mitigation, not a substitute for the repository.

---

Gate **CLOSED**.
Production **NOT CERTIFIED**.
This determination is **not authorization** for the next item.
**No implementation** beyond `BUILD_ORDER_UI-CONV-P03` scope.

**We don't guess. We prove.**
