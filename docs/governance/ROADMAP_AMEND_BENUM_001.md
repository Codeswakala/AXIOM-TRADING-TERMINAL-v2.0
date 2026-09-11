# ROADMAP AMENDMENT A-2026-09-06 — Band Re-enumeration (Backend Roadmap)
`ADOPTED BY THE OPERATOR — 2026-09-06`
`Registers ladder after two intelligence-band insertions, each explicitly adjudicated under ruling (b).`

Apply to `V2_BACKEND_ROADMAP.md` (the on-disk edition):

1. **INSERT** after `# Band BE-9 (Broker/Exchange Connectivity and Account Visibility)`:
   - `# Band BE-10 — Signal-Against-Account Intelligence`
   - Objective: project persisted signal vocabulary onto latest-complete broker-synced
     account state in state nouns only, per `ITRGA_REQ_V2_BE-10_001.md`;
     zero broker order types; zero action language; fail-closed staleness.
   - Status: **OPERATING (fielded 2026-09-08_0050, suite 1,121/0; closeout ITRGA-CAMPAIGN-BE10-CLOSE-001).**

2. **INSERT** after the new §BE-10:
   - `# Band BE-11 — Paper-Execution Bridge to Live Practice-Book Truth`
   - Objective: paper orders sized by live practice-book basis (BE-9 projection),
     gateway decisions and ledger math in `PAPER` mode only; drift reconciliation vs
     broker truth; scope per `ITRGA_REQ_V2_BE-11_001.md` upon its adoption.
   - Hard exclusions: zero broker-write verbs; zero terminal contact; price basis
     only via operator-cited inputs or (deferred) lawful fill-sim basis.

3. **RENUMBER**: existing `# Band BE-10 — Controlled Live Execution Gateway` → **`# Band BE-12 …`**
   (text otherwise unchanged; §5 completion condition keys to BE-12's certification).

4. **RENUMBER**: existing `# Band BE-11 — Governed External AI Provider Adapters` → **`# Band BE-13 …`** (unchanged).

5. Register cross-refs: maturity register v1.5.0 annotations (execution family → BE-12+) are
   corroborative records of this amendment; campaign documents already speak the new numbers.

The ladder now reads: BE-9 operating · BE-10 operating · BE-11 in commissioning · BE-12/BE-13 future.
