# ITRGA DETERMINATION — UI-CONV-P03 · ITEM 4

**Reviewing body:** Independent Technical Review & Governance Authority
**Subject:** `ResearchManagementPage` → `?view=research` full-height stage — **final item of the CONV programme**
**Date:** 2026-08-15
**Base:** `34f4c62` + item3 (`b7b4c4f7…`) + item5 (`4c03910c…`) + item6 (`f65da5c3…`)
**Verification:** `/tmp/i4` — pristine clone → chain applied → item 4 applied

| Artifact | sha256 | Lines |
|---|---|---|
| `item4.patch (1).txt` — **Rev B** | `a516c2c144c1f2f6` | 1,915 |
| `DELIVERY_REPORT_UI-CONV-P03_ITEM4.md` | `ad97217d3000a960` | 252 |
| `UI-CONV-P03-ITEM5_CAPTURES.html` | `9cef5bd1ae0262c5` | 5 PNGs |
| `UI-CONV-P03-ITEM6_CAPTURES.html` | `79a33b630136d49b` | 3 PNGs |

---

## 1. DETERMINATION

# APPROVED WITH OBSERVATIONS

**Item 4 is verified in applied source. Every mandatory requirement is met.** `OBS-CONV3-4` and `OBS-CONV3-5` are **CLOSED**. One observation remains: the item-4 capture gallery is described as attached but was not transmitted.

**All six items of UI-CONV-P03 are now approved in substance.** The phase determination follows in §8 — and it is not a simple pass.

---

## 2. TRANSPORT

```
Rev B ................ a516c2c144c1f2f6   1,915 lines (candidate was 1,138)
git apply --check .... exit 0  on 34f4c62 + item3 + item5 + item6
git apply ............ APPLIED
base declared ........ explicit, matches
```

The DA revised the pre-authorization candidate rather than resubmitting it — **+777 lines**, and the report states plainly which directive requirements the candidate did not satisfy (M5 per-source degradation, and one missing capture class). That is the correct response to a directive issued after a premature submission: treat the directive as binding, not as ratification of what already existed.

---

## 3. MANDATORY REQUIREMENTS — ALL VERIFIED

### M1 — The three field-allowlist write guards ✓

The highest-risk element of this item.

```
:212  export function assertCollectionOrganizationPayload(
:222  export function assertMemberReferencePayload(
:233  export function assertTagOrganizationPayload(

:217  throw new Error(`COLLECTION_ORGANIZATION_FIELD_NOT_ALLOWED:${unknown.join(",")}`)
:227  throw new Error(`MEMBER_REFERENCE_FIELD_NOT_ALLOWED:${unknown.join(",")}`)
:236  throw new Error(`TAG_ORGANIZATION_FIELD_NOT_ALLOWED:${unknown.join(",")}`)

:880  return assertCollectionOrganizationPayload({    ← WIRED
:887  return assertMemberReferencePayload({           ← WIRED
:1095 return assertTagOrganizationPayload({          ← WIRED
```

**M1a** verbatim with named exports · **M1b** all three still called at their write-path sites · **M1c** error strings intact. The failure mode I was guarding against — a guard that survives as an exported function nobody calls — did not occur.

### M2 — Backend constitutional guard, non-vacuous ✓ — **and stronger than required**

```python
page = root / "frontend" / "src" / "components" / "terminal" / "research" / "ResearchHubView.tsx"
text = page.read_text(encoding="utf-8").lower()
assert "unified research artifact explorer" in text        # ← non-vacuity assertion
forbidden = ("place_order", "submit order", "go live", "connect broker",
             "account_id", "order_ticket", "broker_account")
assert all(item not in text for item in forbidden)
```

I required the guard be re-pointed at the module that actually renders the hub. **The DA added a positive assertion that the file contains the explorer** — so if the path is ever re-pointed at a wrapper or barrel file, the test fails loudly instead of passing vacuously. That is a structural improvement on the guard as it existed before this phase, and it exceeds the directive.

### M3 — Six artifact suites + registry re-pointed ✓

All six present. Residual `pages/ResearchManagementPage` references: **7, all provenance comments.** `ResearchManagementPage.tsx` and its test **deleted**.

### M4 — B-4 extended: render before convert ✓

```tsx
stageView === "research" ? (
  <div className="research-stage-scroll" data-testid="research-stage-scroll">
    <ResearchHubView />
  </div>
) : ( <TerminalChartStage /> )
```

**M4b is satisfied rigorously.** The named test `test_uiconv_p03_view_research_deep_link_renders_research_hub_stage_content` asserts **rendered content**, not the attribute:

```
"Unified Research Artifact Explorer" · "Governed Data-Source Inventory"
artifact-explorer-frame · artifact-source-inventory · artifact-catalog
collection-organization-controls · tag-organization-controls · organization-records-preview
"No collections returned for this operator." · "No membership references returned." · "No tags returned."
```

Its comment states the intent: *"This named test fails if the stage branch only sets `data-stage-view`."* **M4d** regressions retained — `..._view_chart_deep_link_renders_chart_stage` and `..._unknown_view_degrades_to_default_multi_pane` both present. **M4c** ordering satisfied: render and conversion in one patch.

**`OBS-CONV3-4` is CLOSED.** The trap I flagged before item 3 — eleven capability groups vanishing behind a URL that looks like it works — did not materialise.

### M5 — Ten-endpoint independent degradation ✓

Rev B added per-source state and five named tests:

```
..._m5_single_source_failure_does_not_blank_hub
..._m5_two_source_failures_render_two_independent_errors
..._m5_all_sources_ready_reports_genuine_loaded_counts
..._m5_absence_renders_as_absence_no_fabricated_counts
..._m5_mutation_failure_renders_mutation_error_banner
```

Absence markers throughout (`?? "—"` at :958–1026, plus the three "No … returned." strings). The fourth test name is the requirement stated as an assertion.

### Standing requirements

| Req | Result |
|---|---|
| 11 capability groups | All present in `ResearchHubView.tsx` ✓ |
| 10 endpoint consumers | All 10 carried over ✓ |
| **R2** `/research-management` | `ResearchManagementRedirect` :63, registry :377 ✓ |
| **R4** testids | **20** (baseline 0) ✓ |
| **R6** RBAC | 16/16 wrappers, roles unchanged ✓ |
| `UI006_ARTIFACT_EXPLORER_SOURCES` | Relocated, not converted to API calls ✓ |

### Execution evidence

```
Test Files  166 passed (166)
     Tests  775 passed (775)      ← +5 vs item 6
tsc exit: 0        pytest: 415 passed
build: index-CEf2CVNG.js 687.85 kB │ gzip 186.39 kB
```

**1,190 tests green.** Bundle +5.05 kB over item 6, disclosed under `OBS-5`, attributed to the M5 per-source state machinery — a proportionate cost for a requirement I imposed.

---

## 4. `OBS-CONV3-5` — CLOSED after four cycles

The item-6 gallery arrived and **capture 3 finally shows an empty state rendering.** Five `No reports returned.` markers in frame across CROSS-MARKET RELATION, MARKET CONTEXT, HYPOTHETICAL RESEARCH, MARKET-SERIES RISK and ADVISORY QUALITY report groups, with the three evidence-link buttons above them.

That is the capture I asked for four cycles ago. The honest-absence path is now **visually confirmed**, not merely grepped.

## 5. `OBS-CONV3-9` — item-5 gallery received, M5 proven visually

Five PNGs, all hashes reconciling with the item-5 report's declared list (`0ba51031`, `172de913`, `0a2da80c`, `e854fb75`, `49b5474f`).

**Capture 5 is the strongest evidence in this delivery.** It shows the governance overlay with:

```
ERROR  Audit Error / Failed to fetch      ← audit seam failed
No Audit Rows                             ← honest empty, not a spinner
"In-memory only: showing 0 of 0 audit rows. A filtered view is not a full-scope governance claim."
EVIDENCE VIEWER  ← still rendering
```

**This is item 5's M5 requirement proven under real fault conditions** — a failed audit fetch surfaces its own error while the Evidence Viewer and the surrounding governance sections continue rendering. Source inspection established the state variables existed; this establishes the behaviour.

---

## 6. OBSERVATION — `OBS-CONV3-11`: item-4 gallery not transmitted

| Field | Content |
|---|---|
| **Requirement** | Directive §8.7 — Level-I captures **attached**. |
| **Evidence** | Report §6 is headed *"Level-I captures — ATTACHED (directive §8.7, all five required classes)"* and names `UI-CONV-P03-ITEM4_CAPTURES.html` with raw PNGs at `/home/user/uiconv_p03_item4_captures/`. **Only the item-5 and item-6 galleries were attached.** No item-4 gallery is present. |
| **Failure** | The report asserts attachment that did not occur. Captures 02, 04 and 05 are cited as evidence for R2, M5 and the mutation control. |
| **Mitigating** | Every claim those captures support is independently verified in source: R2 redirect (:63, :377), M5 (five named tests + per-source state), mutation controls (M1b call sites). Nothing rests solely on them. |
| **Required Correction** | Attach `UI-CONV-P03-ITEM4_CAPTURES.html`. |
| **Owner** | DA |

Also unmet: the **interactivity evidence** required by §8.7 — an interaction trace or explicit statement that hit-testing was verified in a real browser. Given that the item-3 `pointer-events` defect passed acceptance on jsdom-passing tests plus a static screenshot, and item 4 introduces a **new full-height stage view** rather than an overlay, this should be supplied before phase closure.

**Not blocking item 4.** The word "ATTACHED" in a section heading for files that were not attached is a wording defect of the `OBS-CONV2-2` class — state what is true.

---

## 7. ITEM 4 — STATUS

**APPROVED WITH OBSERVATIONS.** Closed: `OBS-CONV3-4`, `OBS-CONV3-5`, `OBS-CONV3-9` (items 5–6). New: `OBS-CONV3-11`.

---

## 8. UI-CONV-P03 PHASE — AND WHY IT CANNOT BE CERTIFIED COMPLETE

| Item | Surface | Substance |
|---|---|---|
| 1 | Portfolio Research → PORTFOLIO dock | APPROVED |
| 2 | Scenario Comparison → SCENARIOS dock | APPROVED |
| 3 | Workspace Customization → settings overlay | APPROVED |
| 5 | Governance Evidence → governance overlay | APPROVED |
| 6 | Signal Investigation → drill-down extension | APPROVED |
| 4 | Research Management → `?view=research` stage | **APPROVED** |

**All six items approved in substance. The phase is NOT certified complete.**

```
origin/main = 34f4c62      commits since = 0
```

Every item of UI-CONV-P03 exists **only as patch files** — in this workspace and the DA sandbox. `/tmp` has already been cleared once mid-review. The repository contains none of it.

**`OBS-CONV3-8` is now the binding constraint on phase closure.** I can certify that the work is correct — I have applied it, read it, and tested the claims. I cannot certify that the platform *has* it. Those are different statements, and conflating them would be the precise failure this authority exists to prevent.

**Determination of record:**

> **UI-CONV-P03: APPROVED IN SUBSTANCE — NOT LANDED.**
> Phase closure is withheld pending the verified patch chain reaching origin.

The chain applies cleanly in order — `34f4c62` → item3 → item5 → item6 → item4 — and I hold all four patches with reconciled hashes. Landing it is mechanical:

```bash
git checkout -b conv-p03 34f4c62
git apply item3.patch && git apply item5.patch && git apply item6.patch && git apply item4.patch
# suites, then commit and push
```

On that push I will re-clone, re-verify, and issue the phase determination and the CONV programme assessment.

---

## 9. STATUS

| Finding | State |
|---|---|
| **Item 4** | **APPROVED WITH OBSERVATIONS** |
| `OBS-CONV3-4` research stage inert | **CLOSED** |
| `OBS-CONV3-5` empty-state capture | **CLOSED** — four cycles |
| `OBS-CONV3-9` items 5–6 galleries | **CLOSED** |
| `OBS-CONV3-11` item-4 gallery + interactivity | **NEW** |
| `OBS-CONV3-8` work outside the repository | **Open — binding on phase closure** |
| `OBS-PROV-2` `docs/evidence/` | Open |
| `OBS-5` bundle | Open — POLISH-P01 |
| `F-BRAND-1`, `OBS-CONV2-5` | Open |
| P02 closures ×4 | Verified intact |

---

Gate **CLOSED**.
Production **NOT CERTIFIED**.
This determination approves **item 4**. It is **not** a phase determination for UI-CONV-P03, and not authorization for SURF, DATA, CHART or POLISH.

**We don't guess. We prove.**
