# FE-0 / D0-5 — Evidence-Baseline Definition (Unit Evidence-Pack Standard)

| Field | Value |
|---|---|
| Document ID | AXIOM-V2-FE0-D05-001 |
| Parent | AXIOM-V2-FE0-DESIGN-PLAN-001 (under AXIOM-V2-DPR-001) |
| Author | DA · 2026-09-10 |
| Purpose | The pack structure that makes Operator visual approval evidence-shaped (§A.4): approval attaches to artifacts, never to recollection |

## 1. Pack identity

- Pack id: `FEPACK-<unit>-<seq>` (e.g. `FEPACK-FEU01-001`); a corrective cycle under the same unit increments `<seq>` — packs are never edited, only superseded whole.
- Home: `docs/evidence/frontend/<unit>/<pack-id>/` + `MANIFEST.md` listing EVERY file with md5+sha256 and byte size. **A file absent from the manifest is not evidence** (naming-of-numbers law: hashes measured, never recalled).
- The Operator Decision (§A.4) names the pack id; ITRGA determines on the same pack. One pack, three readers.

## 2. Mandatory pack contents (per unit)

| # | Artifact | Law |
|---|---|---|
| E-1 | **Contract citation** | The unit's page-contract file + hash the BO pinned; the pack proves THAT contract, no other |
| E-2 | **Captured renders** | Every C5 state-matrix cell × every C7 viewport that applies; filenames = `render_<viewport>_<source>_<state>.png`; each capture traceable to a C6 script step. A cell with no capture and no N/A reason = pack-incomplete |
| E-3 | **Interaction script transcript** | The C6 script executed verbatim, numbered step results, deviations typed (a deviation is a finding, not a silent re-run) |
| E-4 | **Prohibition-scan transcript** | The C9 needles, the exact command, full output, zero-hit or explained-allowlist result. Scanner never carries its own needle (standing harness law) |
| E-5 | **Accessibility evidence** | Keyboard-path transcript, focus-order capture, announcement strings as read, contrast measurements for the named pairs, reduced-motion capture |
| E-6 | **V1 regression evidence** | Frontend suite run transcript (count measured against the unit's C10 floor), route census re-measured, any byte-diffs of shared files listed |
| E-7 | **Delivered-file inventory** | Every created/modified file with md5+sha256 before/after; bounded-diff discipline (files outside the unit's scope moving = defect) |
| E-8 | **Delivery Report** | Template path per OD-FE0-001 §1.2b: `docs/templates/DELIVERY_REPORT_TEMPLATE.md` (md5 `5c8e9de9983cb3ddaec623722fb1d1ec`, 13-section V1-era form). **DA disclosure (measured, not resolved):** custody also holds `docs/templates/AXIOM_DA_DELIVERY_REPORT_TEMPLATE.md` (md5 `e54e0dc2dbf8231392eaf0b09faf7091`, the 17-section Operator-supplied house template used for every BE-12 Delivery Report). Both exist; the correction order names the former; which template governs FE-unit DRs = one-word clarification requested at BO-FE-U01 adoption (flag CF-1, correction filing §3) |
| E-9 | **Register updates** | `V2_CURRENT_STATE.md` bump + technical-debt register delta + campaign/frontend register line (per §E's project-state clause) |

## 3. Capture discipline

- Renders captured from a real running frontend against a seeded test backend — never mockups, never doctored DOM. The backend seed state used is itself recorded (seed script + hash) so captures are reproducible.
- Both viewports (1440×900, 390×844) captured from the same build; build identity (commit-clean statement + file hashes) recorded — the DA does not commit; the tree state is proven by E-7 hashes.
- Truthful-state rule for captures: error/degraded/denied states are produced by REAL conditions (stopped server, seeded 401, role-restricted operator), not injected props, wherever the real corridor exists (DEL-001-class defense carried from the backend campaign: injection-only evidence is never acceptance-grade).

## 4. Citation requirements

- Every claim in the Delivery Report that a state renders correctly cites `E-2` filename + `E-3` step number.
- Every "zero hits" claim cites the E-4 transcript line.
- Witness claims measured like hashes (DEL-006 law): a claim never exceeds what its artifact proves.

## 5. Determination-ready format

- Pack closes with `PACK_CLOSING.md`: pack id; contract hash; census lines (files, renders, scan needles, suite count); the DA's §15-style self-assessment; the explicit line **"This pack authorizes nothing; it awaits the Operator Decision naming it."**
- Corrective cycles (§A.5): new pack id, delta section listing what changed vs the rejected pack, rejected pack retained untouched (packs are append-only history).
