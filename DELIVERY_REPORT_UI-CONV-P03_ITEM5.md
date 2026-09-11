# DELIVERY REPORT — UI-CONV-P03 · ITEM 5
## GovernanceEvidencePage → Shell-Owned Governance & Evidence Overlay

| Field | Value |
|---|---|
| Document type | DA Item Delivery Report (Directive §§29–31; Doc 17 §17.8 Gate 4) |
| Issued by | AXIOM Development Authority (DA) |
| Issued to | Independent Technical Review & Governance Authority (ITRGA) & Operator |
| Date | 2026-08-15 |
| Governing instrument | `BUILD_DIRECTIVE_UI-CONV-P03_ITEM5.md` (ITRGA) — scopes item 5 only |
| Base | **`34f4c62` + the verified item-3 patch (`b7b4c4f7…`)** — stated plainly per directive §7 note on base disambiguation |
| Transport | No commits per Operator instruction; `git diff`-based patch (accepted form, item-3 precedent) |
| Governance Gate | **CLOSED** · Production **NOT CERTIFIED** |

---

## 1. Chosen home + reasoning (directive §4)

**Home: a shell-owned governance overlay in the overlay layer** — `components/terminal/governance/GovernanceOverlay.tsx`, mounted by `OverlayLayer`, opened by:

1. the **left module rail** (its Govern launcher navigates to `/governance`, which redirects),
2. the **legacy route `/governance`** (`GovernanceRedirect` → `/?open=governance`, never 404 — R2),
3. the **deep link `/?open=governance`**.

**Reasoning against each candidate:**

| Candidate | Verdict |
|---|---|
| Bottom-dock tab | **Rejected.** The dock holds five research tabs; governance is not a research artifact, and a 1,072-line constitutional surface cannot be compressed into a drawer without violating the turn-56 reframe. |
| Right dock (320 px) | **Rejected.** Four major capability groups with detail payloads, manifests, and posture grids — the same reasoning that rejected it for item 4. |
| Stage view (`?view=governance`) | **Rejected — deliberately.** The directive's `OBS-CONV3-4` warning makes any stage claim load-bearing: the stage rendering branch must be BUILT and PROVEN before a `?view=` URL may carry it. Item 4 owns that build; item 5 must not front-load a rendering-branch obligation while its own surface needs safe delivery. The overlay pattern is item-3-proven and makes no stage claim. |
| Shell overlay | **Chosen.** Same architecture as the item-3 settings surface: overlay state in `OverlayProvider`, mounted in `OverlayLayer`, opened from chrome/redirect/deep link. Full-height, scrollable, modal — appropriate for an occasional full-screen constitutional review surface. |

**Item-5-disclosed correction to item 3 (found during this item's capture work):** the shell's overlay layer is `pointer-events: none`; neither the item-3 settings backdrop nor the item-5 governance backdrop re-enabled hit-testing, making both dialogs click-transparent in real browsers (jsdom tests cannot hit-test, which is why the defect escaped item 3's acceptance). Both CSS files now carry `pointer-events: auto` with explanatory comments. The item-3 file's correction ships in this patch and is stated here, not buried.

## 2. Capability disposition table (directive §1 inventory)

| §1 capability group | New location | Evidence |
|---|---|---|
| Governance & Evidence frame | `GovernanceEvidenceWorkspace` (export name preserved) rendered in the overlay body | `governance-frame` testid; completion suite green |
| Governance Status / Certification Status / Standing Residuals | StatusGrid sections — plain visible sections (M3) | `governance-certification-status`, `governance-standing-residuals` testids; capture 02 |
| Read-Only Governance Boundary (G-1…G-7) | Guardrails section — plain visible section (M3) | `governance-readonly-boundary`; capture 02 |
| Inert Display Rules (Gate / Production / Audit state) | Plain visible section (M3) | `governance-inert-display-rules`; capture 02 |
| Audit Explorer (list · `{selectedEvent.action}` · details payload · refusal reason-code viewer) | AuditExplorerPanel — unchanged, with testids | `governance-audit-explorer`, `governance-audit-event-detail`, `governance-audit-details-payload`, `governance-refusal-reason-viewer`; capture 01 (refusal code extracted from DOM) |
| Evidence Viewer (`{record.id}` · Validation Summary Panels · `{storedText(record.id)}`) | EvidenceViewerPanel + ValidationSummaryPanel — unchanged | `governance-evidence-viewer`, `governance-validation-panels` |
| Platform Health, Readiness & API Posture (incl. Production certification boundary) | PlatformOperationsPanel — unchanged; certification boundary card remains a visible `aria-label="Production certification remains separate"` card | `governance-platform-posture`; capture 03 |
| Governance Data-Source Inventory | Sources section — unchanged | `governance-sources-inventory` |
| **`reasonCodeFor`** | **Relocated verbatim** to `governanceRecords.ts` with its named export and the `"—"` absence marker (M2) | AuditExplorer suite imports it directly and passes unchanged |

**No capability removed, re-scoped, or collapsed.** The seven `UI007_*` constant tables and their record types **relocated** (not copied) to `governanceRecords.ts` — declared governance state, left static per directive §2.2.

## 3. Mandatory requirements M1–M5

| Requirement | Status |
|---|---|
| **M1 — six suites re-pointed, none deleted, assertions intact** | **CONFIRMED.** All six `workstation/governance/*.test.tsx` suites now import from `GovernanceOverlay` (component) and `governanceRecords` (constants/reasonCodeFor); raw-source globs re-pointed to both modules so every assertion holds against the union of content that was previously one file. Zero assertion changes. All six green. |
| **M2 — `reasonCodeFor` verbatim** | **CONFIRMED.** Byte-identical body, named export retained, `"—"` fallback intact; tested by the AuditExplorer suite unchanged. |
| **M3 — four declarations visible without interaction** | **CONFIRMED.** All four render as plain sections in the overlay body — no tooltip, no default-closed accordion, no secondary tab. Test `test_uiconv_p03_governance_four_constitutional_declarations_visible_without_interaction` asserts all four testids plus the certification-boundary card. Capture 02 shows them in frame. |
| **M4 — no backend or schema change** | **CONFIRMED.** Zero backend changes — the directive verified no source-inspection test references this page, and none needed re-pointing. Alembic head unchanged. |
| **M5 — per-section independent error/loading states** | **CONFIRMED.** Nine state variables across three independent fetches preserved; container loads all three but each panel consumes its own loading/error props. Tests: audit-failure and validation-failure each surface their own error while the other sections render and the declarations persist. Capture 05 evidences it live (audit seam aborted at network layer; validation/platform loaded; certification boundary visible; scrolled to the affected region). |

## 4. Standing requirements

| Requirement | Status |
|---|---|
| **R2** `/governance` no 404 | `GovernanceRedirect` → `/?open=governance`; capture 04 (final URL verified) + deep-link test |
| **R3** no fabricated runtime values | No new runtime fallbacks introduced; platform/audit/validation render absence as absence (error banners, empty states); `UI007_*` tables remain declared state |
| **R4** testids on every major region | **17 hooks**: overlay chrome ×4, frame, audit explorer, event detail, details payload, refusal viewer, evidence viewer, validation panels, platform posture, four declarations, sources inventory, body |
| **R6** RBAC | 16/16 `protectedWorkspace()` wrappers unchanged; no per-entry override added |
| **R7** suite green, nothing deleted to force green | **165 suites / 762 frontend tests + 415 backend = 1,177 platform tests (floor 1,170 exceeded)**. Page deleted once superseded; six suites re-pointed; five new overlay tests + two new deep-link tests added |
| **R8** `npm ci` → `tsc -b` | Executed: exit 0 |

## 5. Executed transcripts (raw console output — pasted in the transmission message)

- `vitest`: **165 files / 762 tests passed** · `tsc -b`: exit 0 (zero diagnostics) · `vite build`: exit 0 · `index-DsaFx8C4.js` **687.56 kB** · `pytest`: **415 passed**. Full raw output in the transmission message per directive §7.4. Logs on disk: `docs/evidence/uiconv/vitest_p03item5.log`, `tsc_p03item5.log`, `vite_build_p03item5.log`, `pytest_p03item5.log`.

Bundle delta: 685.94 kB (item-3 close) → **687.56 kB (+1.62 kB)** for the governance overlay module + CSS + records module. Disclosed under OBS-5 discipline.

## 6. Level-I captures (5 · all exactly 1920×1080 · alt text on every image)

Gallery: `UI-CONV-P03-ITEM5_CAPTURES.html` (workspace root, SHA-256 `9cef5bd1…`) · raw PNGs: `/home/user/uiconv_p03_item5_captures/` · DOM record: `UI-CONV-P03-ITEM5_CAPTURE_VERIFICATION.json`.

| # | File | SHA-256 | Subject |
|---|---|---|---|
| 1 | `01_AUDIT_EXPLORER_REFUSAL_CODE.png` | `0ba51031…` | Audit Explorer with refusal event selected; reason-code viewer renders `EXTERNAL_LLM_REFUSED` verbatim |
| 2 | `02_CONSTITUTIONAL_DECLARATIONS.png` | `172de913…` | Four M3 declarations in frame |
| 3 | `03_PLATFORM_POSTURE.png` | `0a2da80c…` | Platform posture incl. certification boundary card |
| 4 | `04_GOVERNANCE_ROUTE_REDIRECT.png` | `e854fb75…` | `/governance` → `/?open=governance`, overlay open |
| 5 | `05_AUDIT_ERROR_STATE_SCROLLED.png` | `49b5474f…` | **Error state scrolled to the affected region** — audit banner visible, validation/platform loaded, declarations persist (OBS-CONV3-5 discipline) |

## 7. Deviations & disclosures

1. **Seeded audit fixture row** — one synthetic `audit_events` row (`assistant.response_refused` with `details.reason_code = EXTERNAL_LLM_REFUSED`) inserted into the LOCAL dev database to evidence the refusal reason-code viewer (capture 01). Same class as the accepted `sig-004`/`scen-002` fixtures; local DB only; no seed script or schema changed. Deviation register entry: `TD-UI-CONV-P03-AUDITREFUSAL-EVIDENCE-FIXTURE` (pending next register update).
2. **Item-3 pointer-events defect** — found and fixed during capture work (both CSS files); disclosed in §1, not buried.
3. **Error-state capture method** — the audit seam was aborted at the Playwright network layer (backend otherwise up) rather than a whole-backend outage, because the auth context logs the operator out when the profile fetch fails with the backend fully down. The capture evidences M5's independence precisely; the method is recorded in the verification JSON.
4. **Bundle +1.62 kB** — disclosed.
5. **No commits** — per the Operator's standing instruction, all changes remain in the working tree; the patch is the artifact of record.

## 8. Precise wording (OBS-CONV2-2 discipline)

- `pages/GovernanceEvidencePage.tsx`: **deleted** (superseded; redirect registered; exactly one implementation remains).
- The seven `UI007_*` tables + `reasonCodeFor` + record types: **relocated** to `governanceRecords.ts` (originals removed from the page; the page itself deleted).
- `GovernanceEvidenceWorkspace` and the panels: **relocated** into `GovernanceOverlay.tsx` with export names and contracts preserved.
- Six governance test suites: **re-pointed** (imports + raw-source globs), not rewritten.

## 9. Transport

| Item | Value |
|---|---|
| Patch | `/home/user/item5.patch` — **1,689 lines · 73,135 B · SHA-256 `4c03910c76fdcbf2bdd19dd74a8935963e7a451ba036869d9daacc6bf5006dcc`** · LF · terminating newline |
| Base | `34f4c62` + item-3 patch `b7b4c4f7…` (stated plainly; ITRGA holds both) |
| Scope | 18 files · 3 new modules (GovernanceOverlay.tsx/.css/.test.tsx + governanceRecords.ts), 1 deleted page (rendered as a rename hunk by git), 12 modifications |
| `git apply --check` at the stated base | **exit 0** (no whitespace warnings) |
| Applied in pristine clone | **165 suites / 762 tests passed · tsc exit 0 · build `index-DsaFx8C4.js` 687.56 kB** (identical to DA tree) |

## 10. Status

| Finding | State |
|---|---|
| Item 5 requirements | Delivered, awaiting ITRGA determination |
| `OBS-CONV3-4` (`"research"` stage) | Open — advisory; **blocks item 4 route conversion**; not triggered by item 5 (no stage claim made) |
| `CA-CONV2-3` transport | Open — structural; inline-patch protocol in effect |
| `OBS-PROV-2` · `OBS-5` · `F-BRAND-1` · `OBS-CONV2-5` | Carried, unchanged |

Gate **CLOSED** · Production **NOT CERTIFIED** · This delivery covers item 5 only; items 4 and 6 were not begun.

**We don't guess. We prove.**

*— AXIOM Development Authority (DA)*
*2026-08-15*
