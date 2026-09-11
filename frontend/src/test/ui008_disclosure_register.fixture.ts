// N-9: ui008_disclosure_register.fixture.ts
// Source: /home/user/axiom/frontend/src/test/ui008_disclosure_register.fixture.ts
// BO-UI008-P01 §3.9; D-2.6 conformance; 18-item register per the BO §3.9 enumeration
// D-2.6(i) correction: OBS-G1RS-1 and OBS-G1RS-2 render as two separate rows
// D-2.6(ii): severities byte-true to the authoritative register
// D-2.6(iii): source pin beside each rendering
// D-2.6(iv): TD-* rows byte-exact to TECHNICAL_DEBT_REGISTER

/**
 * A single entry in the carried-open register.
 *
 * - `id`: the register identifier
 * - `severityLabel`: the severity as byte-true to the authoritative register (or "—" if not in the register)
 * - `severityClass`: a low-cardinality class for the `ix-severity-*` CSS hook (D-2.6(ii))
 * - `icon`: a non-color identifier (Doc 16 B-1; never color alone; BO §3.7; test 22)
 * - `text`: the verbatim disclosure rendering; TD-* rows byte-exact to TECHNICAL_DEBT_REGISTER (D-2.6(iv))
 * - `sourcePin`: the instrument + line that supports this text (D-2.6(iii))
 * - `isComposed`: true if the text is a COMPOSED status line (not byte-carryable from a source);
 *   D-2.6(iii) honest-labeling requirement
 */
export type DisclosureSeverityClass = "high" | "medium" | "moderate" | "low" | "open" | "none";

export type DisclosureEntry = {
  readonly id: string;
  readonly severityLabel: string;
  readonly severityClass: DisclosureSeverityClass;
  readonly icon: string;
  readonly text: string;
  readonly sourcePin: string;
  readonly isComposed: boolean;
};

/**
 * The 18-item carried-open register of record (BO §3.9; D-2.6(i) correction).
 *
 * Source-of-record:
 * - TD-* rows: TECHNICAL_DEBT_REGISTER v3.0.13 (DA-side local; cited by reference per the
 *   CANDIDATE-class attestation discipline; the byte-exact substance is at the register file)
 * - OBS-* rows: the RCN-48 §4 standing register + the RCN-50/51/52 lineage pin chain
 * - F-REVERT-1: RCN-42 §4 standing; the long-form rendering is COMPOSED (F-3 mitigation)
 */
export const ASSISTANT_DISCLOSURE_REGISTER: readonly DisclosureEntry[] = [
  {
    id: "TD-AXIOM-DEV-CREDENTIAL-LITERALS",
    severityLabel: "OPEN · MEDIUM",
    severityClass: "medium",
    icon: "\u{1F4DD}",
    text: "TD-AXIOM-DEV-CREDENTIAL-LITERALS — OPEN · MEDIUM · pre-certification for Doc 11 §2. Amendment 2 records a two-entry hash manifest and separate counters; no plaintext is preserved in governance. A dedicated security-remediation Build Order (environment/fixture injection with no literal defaults) is the canonical path.",
    sourcePin: "TECHNICAL_DEBT_REGISTER v3.0.13 (DA-side local; cited by reference)",
    isComposed: false,
  },
  {
    id: "TD-078",
    severityLabel: "OPEN · MEDIUM",
    severityClass: "medium",
    icon: "\u{1F6E1}",
    text: "TD-078 — External LLM provider absent. Severity: Medium. W5-U01 intentionally uses deterministic local assistant; external LLM requires future gated Build Order. Closure: Future assistant provider unit.",
    sourcePin: "TECHNICAL_DEBT_REGISTER v3.0.13, TD-078 row (register row 84; pipe form per Authority citation: \"| TD-078 | External LLM provider absent | Medium | W5-U01 intentionally uses deterministic local assistant; external LLM requires future gated Build Order | Future assistant provider unit |\")",
    isComposed: true,
  },
  {
    id: "TD-UI-REACTROUTER-MODERATE",
    severityLabel: "OPEN · MODERATE",
    severityClass: "moderate",
    icon: "\u{1F6E1}",
    text: "TD-UI-REACTROUTER-MODERATE — Moderate react-router / react-router-dom advisories disclosed by npm audit after PostCSS remediation. Open, non-blocking; below high audit gate and not a production-readiness blocker unless elevated by future ITRGA certification review.",
    sourcePin: "TECHNICAL_DEBT_REGISTER v3.0.13 (DA-side local; cited by reference)",
    isComposed: false,
  },
  {
    id: "TD-UI005-COMPLETION-TIMEOUT",
    severityLabel: "OPEN · LOW",
    severityClass: "low",
    icon: "\u{23F1}",
    text: "TD-UI005-COMPLETION-TIMEOUT — UI-005 completion test test_ui005_completion_all_surfaces_are_existing_artifact_presentation_or_existing_research_notes uses a fixed 10-second timeout and can expire under CI resource contention. Open; environment-bound observation accepted at P04 final.",
    sourcePin: "TECHNICAL_DEBT_REGISTER v3.0.13 (DA-side local; cited by reference)",
    isComposed: false,
  },
  {
    id: "F-REVERT-1",
    severityLabel: "OPEN · HIGH · CONTAINED · NON-GATING",
    severityClass: "high",
    icon: "\u{1F6E1}",
    text: "F-REVERT-1 — OPEN · HIGH · CONTAINED · NON-GATING. Content limb CLOSED. Mechanism limb mechanism-model v3 of record. Agent limb OPEN. Zero harm ×14 to C1-tracked bytes. Origin never implicated ×18. Tripwire armed.",
    sourcePin: "RCN-42 §4 standing register; long-form is COMPOSED (D-2.6(iii))",
    isComposed: true,
  },
  {
    id: "OBS-CRU2A-1",
    severityLabel: "OPEN",
    severityClass: "open",
    icon: "\u{1F50D}",
    text: "OBS-CRU2A-1 — OPEN. Closure-adequacy verification (C1 content; closure-era sentinel object). Auto-reopen trigger defined; verified within the ML-1 relay bundle scope.",
    sourcePin: "RCN-47 §5; RCN-48 §4",
    isComposed: false,
  },
  {
    id: "OBS-E3B-2",
    severityLabel: "OPEN",
    severityClass: "open",
    icon: "\u{1F50D}",
    text: "OBS-E3B-2 — OPEN. (E3B-lineage observation carried.)",
    sourcePin: "RCN-48 §4",
    isComposed: false,
  },
  {
    id: "OBS-PGR-1",
    severityLabel: "OPEN",
    severityClass: "open",
    icon: "\u{1F50D}",
    text: "OBS-PGR-1 — OPEN. (PGR-lineage observation carried.)",
    sourcePin: "RCN-48 §4",
    isComposed: false,
  },
  {
    id: "OBS-NT-1",
    severityLabel: "OPEN",
    severityClass: "open",
    icon: "\u{1F50D}",
    text: "OBS-NT-1 — OPEN. (NT-lineage observation carried.)",
    sourcePin: "RCN-48 §4",
    isComposed: false,
  },
  {
    id: "OBS-G1RS-1",
    severityLabel: "OPEN",
    severityClass: "open",
    icon: "\u{1F4DD}",
    text: "OBS-G1RS-1 — quotation-craft. Tool-output rendering of P06-FINAL L161 drops the leading ** emphasis pair of the label. Forward standard: tool-output quotations carry emphasis bytes.",
    sourcePin: "RCN-48 §2.3 (craft observation)",
    isComposed: false,
  },
  {
    id: "OBS-G1RS-2",
    severityLabel: "OPEN",
    severityClass: "open",
    icon: "\u{1F4DD}",
    text: "OBS-G1RS-2 — narrative-craft. §1.2 'ML-1 was executed as part of D-1' is causal shorthand. Accurate; the following clause is the precision.",
    sourcePin: "RCN-48 §2.3 (craft observation)",
    isComposed: false,
  },
  {
    id: "OBS-D17-1(a)",
    severityLabel: "OPEN",
    severityClass: "open",
    icon: "\u{1F4D6}",
    text: "OBS-D17-1(a) — PART VI duplicated; the two blocks are byte-identical (SHA-256 00eec8df\u2026 ×2).",
    sourcePin: "RCN-49 §4 F-G2-7 register text",
    isComposed: false,
  },
  {
    id: "OBS-D17-1(b)",
    severityLabel: "OPEN",
    severityClass: "open",
    icon: "\u{1F4D6}",
    text: "OBS-D17-1(b) — PART VII absent from numbering.",
    sourcePin: "RCN-49 §4 F-G2-7 register text",
    isComposed: false,
  },
  {
    id: "OBS-D17-1(c)",
    severityLabel: "OPEN",
    severityClass: "open",
    icon: "\u{1F4D6}",
    text: "OBS-D17-1(c) — §9.9's cryptography-framework reference dangling.",
    sourcePin: "RCN-49 §4 F-G2-7 register text",
    isComposed: false,
  },
  {
    id: "OBS-SELF-01",
    severityLabel: "OPEN",
    severityClass: "open",
    icon: "\u{1F4DD}",
    text: "OBS-SELF-01 — editorial sub-erratum. RCN-44 §1 L20 carries a doubled token 'corpus corpus-check'; the reading of record is 'the corpus check'. Not load-bearing (RCN-07 §2); RCN-44 bytes stand immutable.",
    sourcePin: "RCN-45 editorial; sub-erratum",
    isComposed: false,
  },
  {
    id: "OBS-SELF-02",
    severityLabel: "\u2014",
    severityClass: "none",
    icon: "\u{1F4DD}",
    text: "OBS-SELF-02 — 18 events of record, adjudicated at RCN-42 §4(9) (not '§9'); the DA's 18-register pins ('per RCN-47 §5') are lineage-conformant with RCN-48 (κ) and are not a DA-side defect. Authority-side editorial.",
    sourcePin: "RCN-49 self-erratum; Authority-side",
    isComposed: false,
  },
  {
    id: "OBS-SELF-03",
    severityLabel: "\u2014",
    severityClass: "none",
    icon: "\u{1F4DD}",
    text: "OBS-SELF-03 — RCN-53 §4.3 (OBS-G2C-1) 'no provenance' for the phrase *6/6 GREEN* is narrowed by addendum: the phrase *does* carry provenance of record — the G-2 plan §7/§7.1 names the six-class battery envelope (the §7.1 six rows). OBS-G2C-1's discipline requirement (attribute-or-omit; the G2-C footer used the phrase unpinned) was and remains correct, and its closure (RCN-53 §3.2, W-11) stands. The overbroad evidence sentence is corrected; RCN-53's bytes stand immutable. The BO §4.4 table names the envelope classes precisely so the meter is pinned by enumeration, not by slogan.",
    sourcePin: "BO-UI008-P01 §8; RCN-53 self-erratum",
    isComposed: false,
  },
  {
    id: "OBS-G2DP-1",
    severityLabel: "\u2014",
    severityClass: "none",
    icon: "\u{1F4DD}",
    text: "OBS-G2DP-1 — citation-precision craft. (i) Marked-verbatim trim in G-2 §1: 'findings (§4)' dropped. Forward standard: marked-verbatim cells carry explicit ellipses/brackets. (ii) W5-review §4.5 pin: correct locus §3 / R5-6. (iii) RCN-32 §3.1 pin: correct pin-of-record CRU-1 row 15 + P07 BO/intake. Non-blocking; forward standard.",
    sourcePin: "RCN-49 §4 OBS-G2DP-1; craft observation",
    isComposed: false,
  },
] as const;
