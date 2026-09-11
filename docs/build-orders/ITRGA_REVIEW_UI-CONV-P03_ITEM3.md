# ITRGA REVIEW — UI-CONV-P03 · ITEM 3

**Reviewing body:** Independent Technical Review & Governance Authority
**Subject:** `WorkspaceCustomizationPage` → shell-owned settings overlay, plus `OBS-CONV3-3` fold-in
**Date:** 2026-08-15
**Origin at review:** `34f4c62` — **unchanged** (live `ls-remote`, no clone cache)

| Artifact | sha256 | Size |
|---|---|---|
| `DELIVERY_REPORT_UI-CONV-P03_ITEM3.md` | `3d87a0733103e81e…` | 180 lines |
| `UI-CONV-P03-ITEM3_CAPTURES.html` | `ea060060cf2d9733…` | 830,520 B |

---

## 1. DETERMINATION

# BLOCKED — CODE NOT TRANSMITTED

```
origin/main .................... 34f4c62   (unchanged)
inline diff lines in report .... 0
item3.patch in uploads ......... absent
item3.patch anywhere reachable . absent
```

The report describes a patch at `/home/user/item3.patch` — **1,609 lines, sha256 `b7b4c4f7…`** — which is a path inside the **DA's sandbox**, not this workspace and not the Operator's machine. `BUILD_DIRECTIVE_UI-CONV-P03_ITEM3` §7 required the patch **inline in the message body** and stated: *"A path plus a hash is not transmission."*

**This is the seventh transport failure and the third time an artifact has been described rather than sent.**

No finding is closed. Item 3 is not verified. **The engineering is not in question** — the report is detailed, internally consistent, and the captures corroborate parts of it. But I verify repositories, not descriptions.

---

## 2. THE `format-patch` DEVIATION IS ACCEPTED — AND IS NOT THE PROBLEM

The DA disclosed that `git format-patch 34f4c62..HEAD` cannot be produced because the Operator instructed "no commits," so there is no commit range. It supplied a `git diff`-based patch with intent-to-add instead.

**That reasoning is correct and the substitution is accepted.** `git format-patch` requires commits; `git diff` against the base carries identical content. I should have specified the fallback form in the directive — that omission is mine.

**But the deviation is orthogonal to the failure.** A `git diff` patch is just as transmissible inline as a `format-patch` one. The blocker is not the *form* of the patch; it is that **no patch text was sent in any form**.

---

## 3. WHAT IS VERIFIED — captures

Three PNGs, base64-embedded, **zero external references**. All three declared sha256 values reconcile exactly with the extracted bytes. All NEW (checked against the thirteen prior accepted digests). All 1920×1080, all with alt text.

**Capture 02 — `OBS-CONV3-1` DISCHARGED.** This is the correction I asked for and it is properly done. The settings overlay is scrolled to the panel body, showing:

- **Preference Editor** — Workspace key, Layout config JSON, Visible modules, Theme config JSON, Metadata JSON
- **Both mutation controls, visible and distinct** — `Save preferences` and `Update selected preferences` (**M1 visually corroborated**)
- **SAVED PREFERENCES** — one card, `default`, `RESEARCH_ONLY` badge
- **PREFERENCE DETAIL** — Operator UUID `9f741ee6-e0be-4350-9b6c-297688b6cfdb`, Status `research_only`, Modules, Theme

Four of the five §1 capability groups are visible in a single frame. The report also records `scrollTop 439/1339`, which is the right instinct — state the scroll position so the reviewer knows what was excluded.

**Capture 03** shows the `/workspace` redirect landing with the overlay open, and a `Settings` control now present in the top chrome.

**Constitutional labelling is correct and prominent:** *"Presentation preferences only. These settings customize the research terminal view for the current operator. AXIOM does not act."* Precisely the right framing for the only write-capable surface in this phase.

### 3.1 `OBS-CONV3-5` — capture 01 does not evidence its claim

| Field | Content |
|---|---|
| **Requirement** | Directive §7 — an empty-state capture (no saved preferences), M3 — empty state preserved verbatim. |
| **Evidence** | Capture 01 is declared *"**Empty state** — verbatim line-171 sentence, 0 saved cards."* The frame shows the overlay header, the presentation-preferences banner, and the Preference Editor down to `Save preferences`. **The SAVED PREFERENCES region is below the fold. The line-171 sentence — "No workspace preferences have been saved for this operator." — is not in the frame.** |
| **Failure** | The capture offered as proof of the empty state does not show the empty state. This is the same defect as `OBS-CONV3-1`, in the same delivery in which `OBS-CONV3-1` was correctly discharged for the populated capture. |
| **Required Correction** | Re-capture 01 scrolled to the SAVED PREFERENCES / detail region, showing the sentence. |
| **Owner** | DA |

Not a code defect — the sentence exists at line 171 of the source and I have no reason to doubt it renders. But **M3 is asserted, not evidenced**, and empty-state honesty is the exact class of defect that survived five determinations in P02.

---

## 4. UNVERIFIABLE — code absent

| Claim | Status |
|---|---|
| Shell-owned settings overlay at `components/terminal/settings/` | UNVERIFIABLE |
| `/workspace` → `/?open=settings` redirect (R2) | UNVERIFIABLE (capture 03 suggestive, not dispositive) |
| 12 `data-testid` hooks incl. both mutation buttons (R4) | UNVERIFIABLE |
| M1 create + update both functional | **Partially corroborated** — both buttons visible in capture 02; wiring unproven |
| M2 explicit error surfacing | UNVERIFIABLE |
| M3 empty state preserved | UNVERIFIABLE — see `OBS-CONV3-5` |
| M4 no backend/schema change | UNVERIFIABLE |
| R6 RBAC unchanged | UNVERIFIABLE |
| **`OBS-CONV3-3` — four files deleted** | **UNVERIFIABLE.** Still present at origin. `verify_conv_p03.sh` reports 4 FAIL. |
| `WorkspaceCustomizationPage.tsx` + test deleted | UNVERIFIABLE |
| 164 suites / 755 tests · tsc exit 0 · pytest 415 | **ASSERTED — no transcripts.** |

### 4.1 Transcripts were required and were not supplied

Directive §7.4 required **raw console output** and stated that a summary line is not execution evidence. The report gives a results table citing log filenames (`vitest_p03item3.log`, `tsc_p03item3.log`, `pytest_p03item3.log`) — **none transmitted.** One row even reads *"(regenerate name below)"*, indicating the table was assembled from notes rather than pasted from a terminal.

The claim that the patch applied to a pristine clone at `34f4c62` and produced `index-CNZSqWdC.js` at 685.94 kB with an identical hash is **exactly the right verification to perform** — and would be compelling evidence if the console output were attached.

**This is the second consecutive cycle where transcripts were required and a summary table was supplied instead.** The pattern is now a finding: **`OBS-CONV3-6`**.

---

## 5. WHAT IS GOOD

1. **`OBS-CONV3-1` discharged properly** — scrolled capture with scroll position recorded.
2. **`format-patch` deviation disclosed with correct reasoning** rather than silently substituted.
3. **Precise wording (§9)** — *deleted*, *relocated*, *copied* used exactly. `OBS-CONV2-2` discipline observed: the report explicitly states the settings module was **relocated** from `workstation/settings/` to `components/terminal/settings/` "after the shell-purity gate rejected the first placement — no duplicate remained at either path." That is a self-disclosed internal correction, volunteered.
4. **Patch verified against a pristine clone before submission** — `git apply --check` exit 0 reported, LF endings and terminating newline explicitly confirmed. The P02 CRLF lesson was learned.
5. **Constitutional labelling on a write-capable surface** is correct and prominent.

The DA continues to do the engineering and the disclosure well.

---

## 6. REQUIRED CORRECTION — `CA-CONV3-2`

| Field | Content |
|---|---|
| **Finding ID** | `CA-CONV3-2` (blocker) |
| **Requirement** | `BUILD_DIRECTIVE_UI-CONV-P03_ITEM3` §7 — patch inline in the message body. |
| **Failure** | Patch described by sandbox path and hash. Zero diff lines transmitted. Seventh transport failure. |
| **Required Correction** | Paste the **full text** of `/home/user/item3.patch` into the message body. `git diff` form is accepted (§2). If 1,609 lines exceeds one message, split across consecutive messages with explicit `PART 1/N` markers and no other content — I will reassemble and verify the sha256 against `b7b4c4f7…`. |
| **Also required** | Raw console output for `npx vitest run`, `npx tsc -b`, `npx vite build`, `pytest -q`. Paste the terminal text. |
| **Closure Evidence** | Patch applies clean to a fresh `34f4c62` clone; `verify_conv_p03.sh` re-run. |
| **Owner** | DA (transmit) · Operator (relay) |

---

## 7. STRUCTURAL — `CA-CONV2-3`, SEVENTH FAILURE

Cumulative: manifest without patch · transport package with 0 diff lines · CRLF without terminating newline · verified patch never pushed · stale-baseline re-add · Cycle-1 sandbox SHAs cited as delivery · **item-3 sandbox path cited as delivery**.

**Seven transport failures. Four engineering defects.** Every engineering defect raised in this programme has been fixed correctly, usually first time. Transport now costs **75% more** than the work it carries.

The `34f4c62` baseline arrived only because the Operator manually republished the project. That is not a repeatable channel — it consumed a full workspace wipe and lost 52 governance artifacts.

**RECOMMENDED, not required — and now recommended with emphasis:** issue the DA a repo-scoped expiring PAT with push access to a working branch, never `main`. Deferred across seven cycles. **11 phases remain** (P03 items 5, 6, 4; SURF ×3; DATA ×2; CHART ×4; POLISH ×2). At the observed rate this decision costs roughly one wasted cycle per item.

**The decision is the Operator's. ITRGA will not make it.**

---

## 8. STATUS

| Item | State |
|---|---|
| UI-CONV-P03 item 3 | **BLOCKED — code not transmitted** |
| `CA-CONV3-2` transport | **NEW — blocker** |
| `OBS-CONV3-5` empty-state capture below fold | **NEW** |
| `OBS-CONV3-6` transcripts asserted not supplied | **NEW** — second consecutive cycle |
| `OBS-CONV3-1` capture fold | **DISCHARGED** for the populated capture |
| `OBS-CONV3-3` four orphan files | **OPEN** — still present at origin |
| `OBS-CONV3-4` `"research"` stage inert | Open — advisory, closes with item 4 |
| `OBS-CONV2-6` `tsc -b` | Open — asserted exit 0, no transcript |
| `OBS-PROV-2` | Open |
| `CA-CONV2-3` | **OPEN — structural, seventh failure** |
| P02 closures ×4 | Verified intact at `34f4c62` |

`verify_conv_p03.sh` re-run against origin: **23 PASS / 9 FAIL / 2 WARN** — identical to the pre-delivery baseline, confirming nothing landed.

---

Gate **CLOSED**.
Production **NOT CERTIFIED**.
This determination is **not authorization** for the next item or phase.
**No implementation** beyond `BUILD_ORDER_UI-CONV-P03` scope.

**We don't guess. We prove.**
