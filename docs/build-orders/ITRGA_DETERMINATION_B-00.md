# ITRGA DETERMINATION — BO-B-00
## Backend Integrity & Reproducible Baseline

| Item | Value |
|------|-------|
| Review identity | ITRGA independent review of DA Delivery Report `DELIVERY_REPORT_B-00.md` |
| Build Order | `BO-B-00` (Operator-authorized 2026-08-19) |
| Reviewer | Independent Technical Review & Governance Authority (ITRGA) |
| Date | 2026-08-19 |
| Evidence standard | Level I (direct) / Level II (executed) / Level III (documentary) / Level IV (assertion) |
| Epistemic rule | No visibility = NOT PROVEN, not automatically FALSE |

---

## 1. What this review did

I attempted to independently verify every substantive claim in the DA's Delivery Report by inspecting the repository and artifacts in **ITRGA custody**. I did not assume, and I did not accept documentary claims as proof.

## 2. What I verified (Level I — direct, in my custody)

| Check | Result |
|-------|--------|
| `backend/app/market/adapters/simulated.py` present | Yes — but **byte-identical to HEAD** (`git diff --quiet` confirms zero change) |
| The defect B-00.1 claims to fix | **Still present** — line 157: `open_time = self._start_time + timedelta(minutes=self._seq)` (the future-dating mechanism, unchanged) |
| Claimed new mechanisms (`now_fn`, `_candidate_open_time`, `_hold_until_due`) | **Absent** — none present in the file |
| `backend/tests/test_b00_simulated_clock.py` (claimed new, sha `29eb50e3…`) | **Absent** |
| `backend/docs/PROVENANCE_LANDING_PROTOCOL.md` (claimed new, sha `17bf431e…`) | **Absent** |
| Evidence logs `docs/evidence/uiconv/b00_*.log` (7 artifacts, hashes cited) | **Absent** — directory does not exist |
| Patch artifact `b00.patch.txt` (sha `5662ec3d…`) | **Absent** — not in my custody |
| Claimed "18-element chain over baseline 34f4c62" | **Not present** — my clone's git history is **2 commits** (`34f4c62`, `60045b7`) |

**Conclusion of §2:** In every repository and artifact I hold, **no change attributable to BO-B-00 exists.** The baseline repository is unchanged; the defect is unfixed; none of the cited evidence is present.

## 3. What I could not verify (the report's positive claims)

The Delivery Report claims, among other things: a wall-clock-bind fix, 4 pinned tests, a soak with zero future-dated bars, 480 executed tests, a dependency classification with 0 unaccepted critical/high, and a written provenance protocol. **Each of these is supported only by hash references to artifacts that were not supplied to the review channel.**

Per evidence law, the report is a **Level III documentary claim**. A hash of an artifact is not the artifact. Without the patch content and the log contents in my custody, I cannot recompute, inspect, or execute anything.

## 4. Finding classification (completeness gap, not defect)

This is a **completeness gap**, not a demonstrated defect:

> The evidence required to determine compliance has not been supplied.

I am **not** finding that the work is false, fabricated, or undone. I am finding that I have **no evidence to examine**, and therefore the correct epistemic state is:

# NOT PROVEN

I do not convert this unknown into a negative finding, and I do not convert the DA's assertions into verified facts.

## 5. Governance observation (must be resolved at Operator level)

The report's §2 and deviation D1 state the delivery model: *"no commits, pushes, or pulls — the patch artifact is the record (custody model; Operator standing instruction)."* This raises two matters that only the Operator can resolve:

1. **Contradiction with BO-B-00 §9.** The Build Order — issued by the Operator — explicitly required **"commit ref + diff"** as Level-I evidence. D1 substitutes a detached patch on the basis of a "standing instruction" that I cannot verify from my custody and which contradicts the just-issued order. Either the evidence requirement stands (in which case a commit ref/diff must be supplied), or the Operator formally amends the BO's evidence model. The DA may not unilaterally change an evidence requirement.

2. **Provenance-failure risk.** The project's own records document prior "approved-in-substance-but-not-landed" failures. A delivery that exists only as detached, hash-referenced artifacts in a DA workspace — never landed in the repository ITRGA can inspect — reproduces that exact failure mode. If BO-B-00 is approved on hashes alone, the repository will again contain work that "passed review" but is absent. This is precisely what the programme's provenance discipline was created to prevent.

## 6. Required action (evidence needed to proceed)

To close this unit, **one** of the following must be supplied to the review channel:

- **Option A (preferred):** the actual artifacts in my custody — the patch file `b00.patch.txt` **and** the seven evidence logs (so I can apply, inspect, and re-execute), or
- **Option B:** a repository state I can independently inspect (committed/landed changes with real SHAs, matching the BO §9 requirement), including `simulated.py`, the test file, and the protocol document, plus executable evidence.

Additionally, the Operator should confirm on the record which evidence model governs: BO-B-00 §9's commit-ref requirement, or a formally amended detached-artifact model.

## 7. Determination

| Field | Value |
|-------|-------|
| Determination | **NOT PROVEN** |
| Reason | Evidence artifacts not in ITRGA custody; repository unchanged; defect present at baseline |
| Nature | Completeness gap (not a defect finding, not an accusation) |
| Next authorization state | **BLOCKED** pending evidence submission per §6 |
| What this is not | Not APPROVED, not REJECTED, not a claim that the DA's work is false |

## 8. Record

- Baseline HEAD: `60045b7` (2-commit history).
- `simulated.py` at HEAD contains the unfixed future-dating defect (line 157).
- No BO-B-00 artifacts present in ITRGA custody.

> **We don't guess. We prove.** And when the evidence is not in front of us, we say so plainly: NOT PROVEN.

**End of ITRGA Determination BO-B-00**
