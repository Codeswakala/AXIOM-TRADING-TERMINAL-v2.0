# BUILD ORDER DRAFT — BO-FE-U02 (Global Chrome)

| Field | Value |
|---|---|
| Document ID | AXIOM-V2-BO-FE-U02-DRAFT-001 |
| Class | **DRAFT — PENDING OPERATOR ADOPTION. On adoption, implementation authority vests in the DA for this unit's scope ONLY; before adoption it authorizes NOTHING** |
| Date drafted | 2026-09-11 (ITRGA hand, adjudicable instrument) |
| Executing authority | **DA only.** ITRGA does not implement |
| Prior unit disposition | **FE-U01 CLOSED** — `AXIOM-V2-DET-FE-U01-002` (TRANSMISSION-ADAPTED, 2026-09-11): `FEPACK-FEU01-004` accepted; census floor re-based to **189 files / 1,017 tests / 0 failures**. §C.4 gate cleared; this BO becomes issuable |
| Unit content (roadmap pin) | AXIOM-V2-FE-ROADMAP-002 §C row FE-U02: **Global chrome** — header (identity, command/search, operator identity, time, mode badge, global health) · left nav rail (keyboard, collapse, role-aware) · route announcements · tokens/primitives consumed by all later units; band FE-1 scope/guardrails inherited verbatim |
| Pinned contract | **PC-FEU02-1 — NOT YET FILED.** Format per D04 (`AXIOM_V2_FE0_D04_PAGE_CONTRACT_FORMAT_AND_FEU01_SIGNIN.md`, md5 `4521605b…`). Filing is the docs-only precondition §6.2; E-1 re-keys to its filed identity thereafter |
| Pinned elections | Door posture **pattern (b)** · AAE-006/AAE-007 binding at chrome scope · **REF-002-E1** (affordances may exist; absence answered with truthful unavailability, never faux success) binding chrome-wide · **F-B3-SCOPE** law — see §2.9 boundary consequence · FE **custody law RATIFIED** (`DET-FE-U01-002` §5.3) — see §4/E-8 packaging |
| Programme frame | U2 roadmap (adopted) governs; **U3 formal adoption word pending — recorded, non-blocking** (same disposition as U01: this BO carries its own authority) · DPR-001 acceptance path §4.4 |
| Reference consultation posture | Roadmap-U2's "references PENDING" clause is hereby updated in effect: **REF-001/REF-003 absorbed canonically, REF-002 absorbed-as-proxy (documentary)** — chrome design may now cite the absorbed set as review inputs at their declared grades |
| Unit loop (§A.3) | This BO = step 1. Then: DA contract filing (docs-only) → fail-first tests → DA implementation → evidence pack `FEPACK-FEU02-001` → **Operator visual approval (decision naming pack id)** → ITRGA determination → U02 closure; only then U03 (home terminal) becomes draftable |

## 1. UNIT SCOPE — exactly ONE surface family (§A.1)

**In scope:** the chrome family itself — the app shell/layout primitive wrapping every routed surface; the header strip (identity block, command/search affordance, operator identity chip, time, **mode badge**, **global health**); the left nav rail (route set, role-aware visibility, keyboard traversal, collapse); the route announcer (a11y); and the **tokens/primitives** (color, type, spacing, motion) codified as the shared baseline. Delivered as the `*Shell`/`*Header`/`*NavRail`/`tokens` file family — actual identities declared in PC-FEU02-1 and inventoried at E-7.
**Out of scope:** every surface rendered *under* the chrome (all later units — U03 home terminal first); any affordance whose target capability does not exist (U14 paper / U15 broker / U16 live cues — absolute); F-4/F-5 (backend-coupled, own future BOs); FE-U17 console; any backend change; the `/login` door's interior (U01, closed — the door remains chrome-free per pattern (b)). Files moving outside this unit's scope = defect (E-7).

## 2. REQUIRED CHANGES (contract clauses abbreviated; the contract governs)

1. **Truthful global health strip:** powered by real `GET /health` (unauthenticated) — reachable / degraded (only if a real degraded source is pinned in the contract) / unreachable / checking; stale > poll window renders "checking", never last value.
2. **Truthful mode badge:** the single identity word of the whole terminal — **RESEARCH · NON-ACTUATING** disposition rendered always visible; **no PAPER / BROKER / LIVE cue may exist** (capabilities absent; needle-enforced, §4/E-4).
3. **Operator identity chip:** session consumed as-is via `GET /api/v1/operator/me` (AAE-004 style); unauthenticated state renders neutral — the shell **asserts nothing about the operator pre-auth** (pattern (b) at chrome level).
4. **Command/search — elected ONE way in PC-FEU02-1:** either (a) shipped truthful — searches the *real* navigable registry (routes/actions that exist) with empty-state honesty, or (b) shipped visibly forthcoming/disabled with truthful notice. **Faux results, dead-toast placeholders, and silent no-ops prohibited.**
5. **Nav rail role-aware:** items keyed to the *real* entitlement surface only; collapse persisted honestly (declared storage election, mirroring REF-002-E1's remembered-preference pattern); full keyboard access to all shell landmarks.
6. **Route announcements:** announcer speaks route-change truth (title/context actually rendered); no fabricated context language.
7. **Identity block:** AXIOM identity per absorbed REF-003 family; **branding covenant held — `axiom-logo.png` is the only image asset**; any new asset class requires disclosure-and-election before existence.
8. **Tokens/primitives codified + baseline captured:** the token set every later unit consumes, with a visual-regression baseline committed for them (E-5/E-6 hooks).
9. **Shell replacement — F-B3-SCOPE boundary consequence:** the V1 `Terminal*` heritage shell family is **within** this unit's ownership; heritage literals of the SAL-2 / `GATE: CLOSED` / asserted-posture family living there are **expelled at this boundary** (whereas the same literals in files this unit does not own remain protected heritage pins until their owning unit). Neighbor files moved but re-styled must stay byte-still or come inside the boundary — no silent cosmetic drift.
10. **V1 registry preservation:** all 16 protected routes + `/chart` alias intact and reachable through the new rail (F-8).

## 3. FAIL-FIRST (mandatory)

Before any implementation byte: tests exist for the state-matrix cells (health tri-state+checking; badge needles zero; announcement truth; collapse persistence; role-aware nav sets; command/search elected behavior) and the prohibition needle scans run **red** against the as-built heritage shell. Red transcript into the pack (E-3 class).

## 4. EVIDENCE PACK — `FEPACK-FEU02-001` (per D0-5/D05, examination-rehearsed)

- **E-1** contract pin: PC-FEU02-1 at its **filed** identity (repo path + md5), transmitted doc-class.
- **E-2** renders: every state-matrix cell × **1440×900** and **390×844**, from a real running frontend against the seeded test backend; seed recorded (script+hash). **Real conditions, never injection-only (standing law):** health states via started/stopped test server; role sets via seeded accounts of real role; reduced motion via emulation.
- **E-3** interaction script transcript verbatim (typed deviations only).
- **E-4** needle scans, exact command + full output, **boundary-scoped per F-B3-SCOPE**: permanent family (`SAL-2`, `GATE: CLOSED`, asserted-posture literals, remember-control resurrection) + chrome-family (PAPER / BROKER / LIVE capability vocabulary, entry/stop/target/R:R, BUY/SELL CTAs, faux-search vocabulary) — zero hits inside the boundary; allowlisted constants each named.
- **E-5** accessibility evidence: landmark keyboard traversal, focus rings, announcement strings as read, contrast pairs, reduced-motion capture.
- **E-6** regression: full frontend suite transcript with count **re-measured against the re-based census floor (189 files / 1,017 cases — measured, never assumed)**; 16 protected routes + `/chart` alias intact; any shared-file byte-diff surfaced as finding.
- **E-7** delivered-file inventory (before/after md5+sha256), bounded diff disclosed.
- **E-8** Delivery Report on the house template — **packaged under the ratified custody law:** shipped *same-turn* with (i) the custody archive (V/X artifacts incl. manifest + transcripts, approval-bearing pixels, reference-register updates) and (ii) an **extraction-rehearsed operator battery runbook** with expectations pre-declared by the DA before any output exists (B-battery class). **Code never over the upload channel — channel law.**
- **E-9** register updates (`V2_CURRENT_STATE.md`, technical-debt delta, frontend campaign line re-keying this unit's row).
- Closes with `PACK_CLOSING.md` carrying the line: *"This pack authorizes nothing; it awaits the Operator Decision naming it."*

## 5. ACCEPTANCE PATH

1. DA delivers implementation + `FEPACK-FEU02-001` (custody-law packaged).
2. **Operator visual approval** — recorded as an Operator Decision naming `FEPACK-FEU02-001`.
3. ITRGA determination on the same pack (corrective cycles re-key to `-002+`, rejected packs retained append-only; transmission-adapted class available per the U01 law).
4. U02 closure → FE-U03's Build Order becomes draftable. One unit at a time, ever.

## 6. PRECONDITIONS

1. **Adoption of this BO by the Operator** (the implementation-bearing word for this unit).
2. **DA files PC-FEU02-1** under the D04 format (docs-only turn; doc-class transmission with md5 pin) **before fail-first evidence begins**; the contract rides ITRGA review (adjudicable; acceptance-with-correction posture); E-1 re-keys to the filed identity.
3. Standing pendings unchanged by this BO: U3 adoption word (non-blocking); FE-U17 uncommissioned (independently schedulable); FE-U14/15/16 gate-blocked; parked live campaign parked at F01; §G.3 heritage revert-disposition word still pending (recorded; does not touch this unit's boundary).

---

**This draft awaits your adoption word.** On adoption the DA begins at §6.2 — the chrome's contract filed first — then §3 fail-first: the frame that every later surface will live inside, rendered only ever as truthful as the capability beneath it.
