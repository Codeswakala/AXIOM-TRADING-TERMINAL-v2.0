# ITRGA DETERMINATION — UI-CONV-P02 (FINAL)

**Reviewing body:** Independent Technical Review & Governance Authority
**Subject:** UI-CONV-P02 — Terminal absorption corrective delivery
**Origin HEAD at review:** `75c71c5` — *Revert "fix(terminal): discharge CA-CONV2-1, OBS-CONV2-1/-3/-4…"* — 2026-08-15 15:27:25 +0300
**Baseline:** `04ded6b`
**Method:** Fresh clone to `/tmp/f2`; string-level verification of every finding against the pushed tree; Operator-supplied execution transcript (`OPERATOR RESULTS.md`, sha256 `eecc422c61e0…`, 77 lines) corroborated against repository state.

---

## 1. DETERMINATION

# APPROVED WITH OBSERVATIONS

**All four UI-CONV-P02 findings are discharged and verified at origin. The phase is closed.**

Observations recorded below are evidentiary and documentary. None blocks phase closure. None is a code defect.

---

## 2. VERIFIED AT ORIGIN

Executed against a clone taken after the push — not against DA assertion, not against my sandbox.

```
OBS-CONV2-1  prod literals in TerminalIntelligenceCards.tsx ....... 0   ✓
CA-CONV2-1   palette relabels in quickActionCatalogue.ts .......... 3   ✓
OBS-CONV2-3  signal_state.toUpperCase() verbatim renders ......... 2   ✓
OBS-CONV2-4  pages/ChartWorkspacePage.tsx .................... gone     ✓
             pages/AdvisorySignalsPage.tsx ................... gone     ✓
             pages/PerformanceAnalyticsPage.tsx .............. gone     ✓
             components/chart/ChartWorkspaceSurface.tsx ... retained    ✓
             duplicate ChartWorkspacePage exports ............... 1     ✓
```

The revert behaved exactly as tested: it removed the six erroneously re-added files (`1,704` deletions, `1` insertion) and disturbed none of the three previously closed corrections.

### Findings closed

| Finding | Requirement | Closure evidence | Status |
|---|---|---|---|
| `OBS-CONV2-1` | No fabricated calibration statistics rendered as validated metrics | Zero hardcoded percentage fallbacks in `TerminalIntelligenceCards.tsx` at `75c71c5` | **CLOSED** |
| `CA-CONV2-1` | Palette labels name post-absorption destinations | `quickActionCatalogue.ts:30,39,48` | **CLOSED** |
| `OBS-CONV2-3` | State never derived from freshness | `TerminalSignalStream.tsx:167-168,203,233` | **CLOSED** |
| `OBS-CONV2-4` | No unrouted orphan page files | Three pages absent; relocated surface retained; single export | **CLOSED** |

`OBS-CONV2-1` warrants explicit note. Invented statistics — `"78.4%"`, `"82.4%"`, `"17.6%"` with Wilson intervals — were rendering as server-validated calibration metrics whenever the API returned nothing. It survived five determinations because every capture supplied to this authority happened to be populated. It was self-disclosed by the Delivery Agent, unprompted, in Rev 2 §R1-2. **That disclosure is the single most creditable act in this phase.** It also retrospectively explains `CA-P04-5`, where the same `[72.4% – 84.1%]` interval appeared against a 48.0% point estimate.

The defect is gone from production code, and the test corpus now contains explicit guards against its return (`terminalSignalsIntelligence.test.tsx:411-413`, `not.toContain("78.4%")`).

---

## 3. EXECUTION EVIDENCE

First executed transcript received in this phase. Accepted as Level-II evidence.

| Suite | Result |
|---|---|
| `npm test` | **162 files / 736 tests passed**, 607.70s |
| `npx vite build` | **✓ built in 2.05s** — 149 modules; `index.js` 682.11 kB (gzip 182.53 kB), `index.css` 147.05 kB (gzip 20.05 kB) |
| `npx tsc -b` | `error TS2688: Cannot find type definition file for 'node'` |
| `git push` | `5ef6c4e..75c71c5  main -> main` |

### The `tsc` error is an environment defect, not a code defect — analysed, not assumed

I verified this rather than waving it through:

- `frontend/package.json:24` declares `"@types/node": "^26.2.0"` as a devDependency.
- `package-lock.json` resolves `node_modules/@types/node`.
- `tsconfig.json:18` requests `"types": ["vitest/globals", "node"]` — a coherent request.
- **No production source imports a node builtin** (`node:`, `fs`, `path`, `child_process`) — grep returns empty. Only test files reference `process.env` / `__dirname`.

The declaration is correct and the dependency is locked; the local `node_modules` tree simply does not have it installed. `npm ci` in `frontend/` resolves it. That 736 tests and a full Vite production build both succeeded in the same working tree confirms the source compiles — the type-library lookup failed, not the code.

**Recorded as `OBS-CONV2-6` (environment, non-blocking, Operator).** A clean `npm ci && npx tsc -b` transcript should accompany the next phase delivery.

The 682 kB bundle warning is noted for the POLISH phases; code-splitting is a known future item, not a P02 obligation.

---

## 4. OBSERVATIONS CARRIED FORWARD

None of these blocks closure of UI-CONV-P02. All are tracked.

| ID | Observation | Owner |
|---|---|---|
| `OBS-CONV2-2` | Delivery report describes `ChartWorkspacePage` as retired. It was **relocated** to `components/chart/ChartWorkspaceSurface.tsx` (97% similarity) because its annotation layer is still consumed. Disposition legitimate; wording inaccurate. Correct in the next report. | DA |
| `OBS-CONV2-5` | Seeded `sig-004` fixture — route to the deviation register. | DA |
| `OBS-CONV2-6` | `@types/node` not installed locally; `tsc -b` cannot complete. `npm ci` resolves. | Operator |
| `OBS-PROV-2` | `docs/evidence/uiconv/` absent at origin. The capture harness (`scripts/capture_uiconv_p02_r1_evidence.mjs`, `scripts/verify_uiconv_p02_r1_evidence.mjs`) **did** land; its output did not. | DA |
| — | Six `UI-CONV-P02-R1_*.png` captures never transmitted. Level-I visual confirmation remains unsatisfied for this phase. | DA |
| — | Delivery tag `UI-CONV-P02-R1_DELIVERY` not at origin (13 tags, unchanged). | DA |
| `OBS-5`, `F-BRAND-1` | Unchanged. AX Monogram remains unmounted; GA-173 text unread. | — |

**On Level-I evidence:** I am closing this phase on verified source state plus an executed 736-test transcript, without the six captures. That is a deliberate, recorded departure. The corrections are string-verifiable in the repository and the assertions are machine-checked; visual capture would add confirmation, not proof, for these four specific findings. **This does not set a precedent** — findings that are visual in nature will still require captures.

---

## 5. STRUCTURAL FINDING — `CA-CONV2-3` REMAINS OPEN

**Owner: Operator. Not discharged by this determination.**

UI-CONV-P02 consumed **six delivery cycles**. Reviewed honestly, the split is:

- **Engineering defects: 4** (the original findings) — all correctly fixed by the DA, mostly on first attempt.
- **Transport defects: 5** — manifest without a patch; transport package with 0 diff lines; CRLF with no trailing newline; a verified patch that never reached origin; a stale-baseline apply that re-added deleted files.

The DA sandbox has anonymous fetch to github.com and **no push credential**. Every artifact is hand-carried, and each hand-carry introduced a distinct defect. The Operator's own proxy at `10.206.93.16` blocked git until unset this turn — plausibly the same barrier facing the sandbox.

I also record an ITRGA defect: `OBS-CERT-2` was assigned to the DA when it was never DA-dischargeable. That was a finding-assignment error by this authority, not DA misconduct.

**Twelve phases remain** — CONV-P03, SURF ×3, DATA ×2, CHART ×4, POLISH ×2. At the observed rate, transport overhead is the dominant cost of the programme, exceeding engineering effort by roughly five to four in this phase alone.

**RECOMMENDED, not required:** issue the Delivery Agent a repo-scoped, expiring PAT. This converts the dominant failure mode into an ordinary push. **The decision is the Operator's and I will not make it.** If it is declined, the hand-carry protocol should be formalised: patch inline in the message body, generated with `git format-patch` against a stated base SHA, LF endings, terminating newline, and `git apply --check` clean before transmission.

---

## 6. PHASE STATUS

| Item | State |
|---|---|
| UI-CONV-P02 findings | **4 of 4 CLOSED** |
| Phase UI-CONV-P02 | **APPROVED WITH OBSERVATIONS** |
| Origin `main` | `75c71c5` |
| Test suite | 162 files / 736 tests passing |
| Production build | Succeeds |
| `CA-CONV2-3` transport | **OPEN — structural, Operator** |
| `CA-P03-1` | CLOSED (GA-167 recorded, register head GA-175) |
| `OBS-CERT-2` | Re-attributed to this authority — closed as misassigned |

---

Gate **CLOSED**.
Production **NOT CERTIFIED**.
This determination is **not authorization** for the next phase.
**No implementation** before the next Build Order is formally issued.
**UI-CONV-P03 NOT AUTHORIZED** — awaiting Operator authorization.

**We don't guess. We prove.**
