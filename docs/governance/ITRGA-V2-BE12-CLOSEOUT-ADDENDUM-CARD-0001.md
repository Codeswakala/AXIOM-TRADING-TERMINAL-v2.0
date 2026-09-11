# ITRGA-V2-BE12-CLOSEOUT-ADDENDUM-CARD-0001
### Closeout addendum card — the four-lock 400-pin refusal battery on the fielded lineage. **THE LADDER'S TRUE LAST FIELD ACT.** Nothing lands: every witness is a refusal, a roll-back, or a read.

- **Date issued:** 2026-09-09
- **Authority:** BO-V2-BE12E-001 closeout condition (i) — *"ANY lock lacking a fielded-lineage witness is witnessed by a CLOSEOUT ADDENDUM card (read-only/400-pin pattern; operator-elective harness) BEFORE the DR-5 line issues"* · **ITRGA_VERDICT_V2_BE12_DR5_GATE_001** (this card is its §4 artifact; its arm-shapes are fixed there, homed here at contract depth) · DR-2 lock-stack · DR-F1 AM-2 (`REGISTERED_LOCKED_MODES = ("LIVE",)`) · five field cards 0053–0057 · credential law (N-O18)
- **Act class:** an in-harness refusal battery. TWO surface arms over the in-process ASGI door (BE-11 transport-swapped precedent; `TestClient(main.create_app())`) + door-drive arms over the fielded file's own engine with an armature transaction **always rolled back**. **NO ENGINE VERB runs; NO register POST; NO credential window is opened; the practice vault envs are never created.** Every child process's probe env is set for that child only and re-swept.
- **FIELD LAW (unchanged, re-asserted):** zero-row BY ELECTION / by doctrine on all seven 12-series tables, pinned BEFORE and AFTER by the pack itself. *"The fielded lineage holds no runtime evidence rows of any band."*

---

## §0 — CONTRACT PINS (homed from the delivery record; citations are the law)

| Pin | Value | Citation |
|---|---|---|
| Mode contract | `REGISTERED_LOCKED_MODES = ("LIVE",)` — `mode_locked` answers ONLY from this tuple | DR-F1 AM-2; `locks.py` (12B CR-1 supplement §2.3) |
| Mode boot | `AXIOM_V2_MODE`, default **`"RESEARCH"`** (the fielded deployment's standing boot); flip is **per-boot env, non-mutating** | 12A source transcript; BE-11 appendum precedent |
| Live door at the surface | `_actuation_door` reads `ActuationState(mode=app.state.v2_mode, credential_class=None, activation_instrument_rows=0, funded_posture=False, killswitch_armed=False)` — **`credential_class=None` by delivered code** | 12A api.py §2.2 / 12B api.py §2.2 |
| Lock predicate law | L1 mode∉tuple · L2 class∉`("practice_trade",)` · L3 rows==0 · L4 ¬funded · L5 armed · L6 `sub_failures` proxied first-class (reason = first class; `sub_classes` echoed) | `locks.py` literal body |
| Passing eligibility shape (suite's own) | `account_present=T, account_posture_class="practice", instrument_mapped=T, session_open=T, basis_present=T, basis_age_hours=2.0, max_age_hours=48.0` ⇒ eligible | `_ELIGIBLE`, 12A test corpus |
| Injected L6 class (pinned by the delivered corpus) | **`sub_signing_failure`** (coupled in the 12D corpus as `killswitch_armed=True, sub_failures=("sub_signing_failure",)`) | 12D source transcript L3296 |
| Armature row (12D-review pattern; 0056 lawful-probe literal) | `(id, sole='SOLE', version='lai-1.0.0', template_hash, funded_posture_ref, step_up_ref, operator_ref, actor_id, data_class='live_marker', mode, operator_id, created_at)` — passes all three rendered CHECKs; INSERT-only is unguarded | 12D review §1.b.4; 0056 pack A10 literal |
| Auth | file-fed admin (`C:\Users\victo\axiom_admin_pw.txt`, N-O18 law) → `POST /api/v1/auth/login` → Bearer | BE-10 first-read precedent |
| Surface witness door | `POST …/live-exec/evaluate` (carries `_actuation_door` in the envelope, 200) — **the register door is deliberately NOT used: register COMMITS; the nothing-lands law forbids it** | 12A api.py §2.2 |

**Adjudicated interpretation, recorded in the open (two honest refinements since the gate verdict):**
1. **The gate-verdict's L2 probe window is DISCHARGED BY CONSTRUCTION.** The delivered live door hardcodes `credential_class=None`; no vault window could ever change its L2 answer (vault resolution feeds the PRACTICE lane's P3 only). The DR-arm phrase "practice credential vs LIVE seam" resolves, under the delivered predicate law and the 12A surface docstring ("posture_mismatch otherwise, since no practice_trade credential resolves"), to the fielded host's standing answer: **no actuation credential class resolves at this seam.** No window is opened; nothing about the refusal is weaker.
2. **A L6 "fielded firing" through HTTP is undefined** (injection classes arrive from downstream legs the BIOS forbids on this host); its witness is the engine typing the corpus-pinned class over the fielded file — acceptance-grade per the BO jurisdiction note. Same class for the L5 order-fixture: **evidence-only, engine-typing for the six-for-six envelope; L5's discharge-by-design stands untouched.**

## §1 — THE FOUR ARMS (+ two order-fixtures, evidence-only)

- **W1 — L1 `mode_locked` (SURFACE):** in-harness app booted with `AXIOM_V2_MODE=LIVE` in that child only (per-boot election; the deployment boot is untouched). Admin login (file-fed; 200 pinned). OpenAPI enumerated: **exactly 22 live-exec routes** (the standing §6-elective enumeration, recorded en passant). POST the evaluate door, suite-eligible body ⇒ HTTP 200; envelope: `actuation_refusal.reason == "mode_locked"` · `lock == "mode_locked"` · `notes[0].order_position == 1` · `mode == "LIVE"`.
- **W2 — L2 `posture_mismatch` (SURFACE):** same door, same body, mode env **absent** (standing boot) ⇒ `reason == "posture_mismatch"` · `lock` same · `order_position == 2` · `mode == "RESEARCH"` (the deployment's standing boot, pinned as fact).
- **W3 — L4 `funded_posture_required` (DOOR-DRIVE, armature, rolled back):** `BEGIN`; INSERT the armature row; `COUNT==1`; `require_actuation(mode="RESEARCH", credential_class="practice_trade", activation_instrument_rows=<read>, funded_posture=False, killswitch_armed=False)` ⇒ refuses `funded_posture_required`, lock same, `order_position == 4`; `ROLLBACK`; `COUNT==0`.
- **W4 — L6 `sub_*` proxied first-class (DOOR-DRIVE, same transaction family):** state as W3 but `funded_posture=True, sub_failures=("sub_signing_failure",)` ⇒ `reason == "sub_signing_failure"` (first-class proxy of the corpus-pinned class) · `lock == "sub_contract_failure"` · `notes[0].sub_classes == ["sub_signing_failure"]` · `order_position == 6`.
- **Order-fixtures, evidence-only (same drive):** W1o — `mode="LIVE"` **with the armature present** ⇒ `mode_locked`, order 1 (**the DR's canonical order law: L1 before L3, witnessed on the fielded lineage**); W4o — `killswitch_armed=True` ⇒ `killswitch_armed`, order 5 (engine-typing completeness for the six-envelope transcript; **NOT a fielded firing** — L5 discharged-by-design stands).

## §2 — HYGIENE + RE-PINS (the pack enforces; the card pins)

Pre-entry and post-battery, identical asserts (any drift since the cards = the finding; halt): fielded head == `20260909_0057` · tattoo 94/88/17 · **election on all seven 12-series tables == 0** · 18-file lxe build hash == `93f436bc…` (the arms run against the EXACT fielded build). Environment: operator-shell sweeps of `^AXIOM_(TD|BROKER_PRACTICE|V2_MODE|ADMIN_PW|DATABASE_URL)` clean at open and close; probe envs exist inside named children only (`AXIOM_V2_MODE=LIVE` the W1 child; `AXIOM_DATABASE_URL` the app-boot children; `AXIOM_ADMIN_PW` file-fed into the login children) and are unset immediately after each child exits. **The transcript never carries a secret; a login failure prints the status code, never the credential.**

## §3 — THE RUN (one command)

```powershell
Set-Location C:\Users\victo\.vscode\AXIOM\axiom
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\ITRGA_V2_BE12_LOCKREFUSAL_400PIN_V1.ps1
```

Records: `operator-evidence\BE-12E\BE12-400PIN-RUN-<timestamp>.txt` (transcript) + `operator-evidence\BE-12E\BE12-400PIN-WITNESS.txt` (arm lines + re-pins + verdict).

## §4 — HALT RULES (standing)

Any gate FAIL ⇒ halt at the failing arm; nothing re-run; no hand-fix; the fielded lineage is proven undrifted by the C1 re-pins alone (the battery itself cannot mutate it: HTTP arms commit nothing, door-drives roll back by construction). Restoration questions remain under the standing anchor law; none is expected — the battery's failure mode is *the app refused to testify*, never *the file moved*.

## §5 — WITNESS-RETURN

Send both record files. On receipt ITRGA: closes gate condition (i) against `ITRGA_VERDICT_V2_BE12_DR5_GATE_001` §1 (L1/L2/L4/L6 → DISCHARGED); chronicle line; and issues the **DR-5 CLOSEOUT VERDICT — the ladder's last act** — with the line of the gate verdict §2 entering the register EXACTLY:

`BE-12 CAPABILITY-COMPLETE · ACTIVATION INSTRUMENT: NOT IN EXISTENCE · funded account: NONE (activation prerequisite) · LIVE mode: REGISTERED-LOCKED · LIVE real-network behavior: NOT PROVEN (≠ FALSE)`

**END OF CARD — ITRGA-V2-BE12-CLOSEOUT-ADDENDUM-CARD-0001**
