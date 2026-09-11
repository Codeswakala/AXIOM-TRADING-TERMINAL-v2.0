# ITRGA — CAMPAIGN CLOSEOUT — BE-9 BROKER READ
`DOC-ID: ITRGA-CAMPAIGN-BE9-CLOSE-001 — STATUS: FIELDED → OPERATING — 2026-09-06`

## Register line
`BE-9 OPERATING — 2026-09-06 — corpus 22 pins — fielded head 20260905_0049 —
FIRST ROUTINE SYNC complete (investor posture) — posture witness
read_only_login true + health asserted true — directive F-E1-02 CLOSED —
campaign six-day arc: REQ→BO→DR→INT→E1×2→apply→first-sync — suite 1,077/0
at band-close — working-file fingerprint 56bf1922…→481316cd…`

## Provenance chain (the four records)
1. `ITRGA_EVID_V2_BE-9_E1_001.md` — E1 evidence record (clean ×2, three findings all closed).
2. `ITRGA_ACC_V2_BE-9_BAND_001.md` — band acceptance (22-pin corpus; 0049 act contract; apply registered; in-situ trigger witness supplement).
3. `BE9_0049_APPLY_CARD_PS.md` + apply witness — the fielding act (one-line upgrade, compver `bre-1.0.0|b0008cb9…` live on working DB).
4. `BE9_FIRSTSYNC_CARD_PS.md` + `BE9_FIRSTSYNC_WITNESS.txt` (two acts, one file) — the operating kickoff.

## Operating posture (standing)
- **Terminal:** investor session only (`476910140`, investor password, GUI dialog only). Master session never again for the AXIOM station.
- **Routine sync cadence:** operator's call (daily/weekly). Each sync is the same small card: transcript → app up (fielded URL) → login (no-echo) → unlock intent → sync → reconcile → readbacks → lock ×2 → census/sha → stop-transcript.
- **Expected steady-state signatures:** sync `complete`, reconcile `clean`/`0 discrepancies`, digest stable while broker content is static, permissions growing by supersession (319/sync witnessed), fills deduped (`fills_reused` ≥ 0 lawful).
- **Health honesty:** `read_only_login_asserted` must be `true` post-sync; if ever `false` — STOP (posture violation is an incident, not an inconvenience).
- **VR-D11 discipline:** any new drift, wall-clock or otherwise, gets enumerated-by-query and re-pinned fresh — never compare against stale literals.

## Lessons filed (non-gating)
1. PowerShell transcript encoding is volatile per-process (UTF-16 LE, UTF-16 BE, UTF-8 BOM all seen) — decode by content, not by assumption.
2. VS Code paste + heredoc/`if-else` splits: paste whole fences; single-line guards where practical.
3. Proxy networks: MT5 ignores system proxy & the native dialog may still fail under interception — WiFi/hotspot is the adjudicated fallback.
4. N-O6/N-O7 (probe-shape + paste-shape lapses, DA-owned): caught by STOP-LAWs before any harm; evidence came home honest every time.

## Campaign narrative (for future audits)
The band arrived with no memory (E0: expectations only). Days: INT bodies
pinned (compver b0008cb9 reproduced live ×3: sandbox, clone, working DB);
E1 two clean cycles on an enriched clone; overnight file drift enumerated and
pinned to the auth/audit surface; apply act single-line; four trigger
refusals witnessed verbatim in-situ; first routine sync under investor
posture. Every claim in this paragraph is backed by one of the four records.

**We don't guess. We prove. Band holds the front.**
