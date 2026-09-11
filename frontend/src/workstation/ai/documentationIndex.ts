/**
 * Static Documentation & Knowledge Base Index (UI-008-P05)
 *
 * Pre-compiled, sandboxed knowledge base indexing:
 * 1. Governance Rules & Standards (Docs 00, 01, 02, 03, 04, 10, 11, 16, 17)
 * 2. System Architecture & Layers (Doc 05)
 * 3. Statistical & Mathematical Definitions (Wilson Score, Brier, ECE, Drawdown)
 * 4. Technical Indicators & Market Microstructure (EMA, ATR, RSI, MACD, Regime)
 *
 * Invariant:
 * - 100% static, local, deterministic client-side index.
 * - Zero external network calls; zero external LLMs.
 */

export interface DocItem {
  id: string;
  title: string;
  category: "governance" | "architecture" | "statistics" | "indicators";
  tags: string[];
  summary: string;
  contentMarkdown: string;
}

export const PLATFORM_DOCUMENTATION_INDEX: DocItem[] = [
  // 1. Governance Documents
  {
    id: "gov-00-vision",
    title: "00 — Vision and Principles",
    category: "governance",
    tags: ["vision", "principles", "integrity", "transparency", "constitution"],
    summary: "Foundational project constitution establishing scientific integrity, explainability, and transparency.",
    contentMarkdown: `### 00 — Vision and Principles

AXIOM exists to develop a professional, research-driven trading intelligence platform.
- **Scientific Integrity**: Measurable evidence precedes every conclusion.
- **Explainable AI**: Model confidence, features, and uncertainty must be disclosed.
- **Human-in-the-Loop**: Augment operator decision-making; AXIOM does not autonomously act.
- **Governance Gate**: Live broker execution remains strictly CLOSED until independent certification.`,
  },
  {
    id: "gov-03-spec",
    title: "03 — AXIOM Project Specification",
    category: "governance",
    tags: ["spec", "governance", "separation of duties", "definition of done"],
    summary: "Constitutional rules defining the tripartite separation of duties and wave lifecycle.",
    contentMarkdown: `### 03 — AXIOM Project Specification

- **Tripartite Authority**:
  - *Operator*: Owns vision and authorizes governance.
  - *Development Authority (DA)*: Designs, builds, tests, and documents.
  - *ITRGA*: Independently audits, verifies, and certifies.
- **Definition of Done**: Implementation complete, all tests passing, docs synchronized, evidence verified.`,
  },
  {
    id: "gov-10-hierarchy",
    title: "10 — Constitutional Hierarchy",
    category: "governance",
    tags: ["hierarchy", "precedence", "tiers", "governance"],
    summary: "Ten-tier constitutional precedence pyramid governing all platform engineering.",
    contentMarkdown: `### 10 — Constitutional Hierarchy

1. **Tier 1**: Vision & Principles
2. **Tier 2**: Constitutional Specification
3. **Tier 3**: Strategic Roadmap
4. **Tier 4**: Technical Constitution (System Architecture)
5. **Tier 5**: Domain Specifications (ML & UI/UX)
6. **Tier 6**: Institutional Reasoning Frameworks
7. **Tier 7**: Operational Governance & Security Standards
8. **Tier 8**: Execution Governance (Build Orders, Design Plans)
9. **Tier 9**: Engineering Evidence (Transcripts, Tests)
10. **Tier 10**: Institutional Investigation & Judgments`,
  },
  {
    id: "gov-17-security",
    title: "17 — Institutional Security Standard",
    category: "governance",
    tags: ["security", "zero trust", "rbac", "sal", "cybersecurity"],
    summary: "Supreme security constitution enforcing Zero Trust, Least Privilege, and SAL-1 through SAL-5.",
    contentMarkdown: `### 17 — Institutional Security Standard

- **Zero Trust Architecture**: Every request requires authentication and authorization.
- **Security Assurance Levels (SAL)**:
  - *SAL-1 (Public)* -> *SAL-2 (Internal)* -> *SAL-3 (Confidential)* -> *SAL-4 (Restricted)* -> *SAL-5 (Critical)*.
- **AI/ML Security**: Strict prohibition against ungrounded generative loops and external LLMs.
- **Zero Actuation**: All assistant surfaces must remain research-only without trading order paths.`,
  },

  // 2. System Architecture
  {
    id: "arch-05-layers",
    title: "05 — Canonical System Architecture",
    category: "architecture",
    tags: ["architecture", "layers", "bounded contexts", "clean architecture"],
    summary: "Eight-layer modular service-oriented architecture with decoupled bounded contexts.",
    contentMarkdown: `### 05 — Canonical System Architecture

1. **Presentation Layer**: React Workstation, Charts, Explorer, Assistant Surfaces.
2. **Application Layer**: Session orchestration, workflows, command registry.
3. **Domain Layer**: Bounded business contexts, research contracts.
4. **Artificial Intelligence Layer**: Grounded reasoning, chart annotations, report explanations.
5. **Machine Learning Layer**: Feature store, model registry, walk-forward validation.
6. **Data Layer**: Historical storage, market data service, SQLite/PostgreSQL persistence.
7. **Infrastructure Layer**: RBAC auth, structured logging, audit ledger.
8. **External Integration Layer**: Broker adapters (Gate CLOSED).`,
  },
  {
    id: "arch-ai-subsystem",
    title: "AI Subsystem & Bounded Contexts",
    category: "architecture",
    tags: ["ai", "assistant", "bounded context", "deterministic"],
    summary: "Architecture of the non-actuating, rule-based institutional AI research companion.",
    contentMarkdown: `### AI Subsystem & Bounded Contexts

- **Ownership**: \`frontend/src/workstation/ai/\` owns assistant UI logic.
- **Integration**: Consumes \`collaboration/assistant-responses\` and \`persistence/audit-events\` read-only endpoints.
- **Refusal Ledger**: Six constitutional refusal reasons persisted to the audit database.
- **Determinism**: Produces repeatable outputs given identical inputs without probabilistic temperature drift.`,
  },

  // 3. Mathematical & Statistical Definitions
  {
    id: "stat-wilson-score",
    title: "Wilson Score Intervals",
    category: "statistics",
    tags: ["wilson score", "binomial", "confidence interval", "uncertainty"],
    summary: "Asymmetric confidence interval formula for binomial success rates under finite samples.",
    contentMarkdown: `### Wilson Score Interval Formula

For observed proportion $p = \\frac{x}{n}$ and standard normal quantile $z$:

$$\\text{Center} = \\frac{p + \\frac{z^2}{2n}}{1 + \\frac{z^2}{n}}$$
$$\\text{Margin} = \\frac{z}{1 + \\frac{z^2}{n}} \\sqrt{\\frac{p(1-p)}{n} + \\frac{z^2}{4n^2}}$$
$$\\text{CI} = \\left[ \\text{Center} - \\text{Margin},\\; \\text{Center} + \\text{Margin} \\right]$$

*Application*: Used in Advisory Quality Review to prevent over-optimistic point estimates on small sample sizes.`,
  },
  {
    id: "stat-brier-ece",
    title: "Brier Score & Expected Calibration Error (ECE)",
    category: "statistics",
    tags: ["brier score", "ece", "calibration", "probability"],
    summary: "Strict probability calibration metrics evaluating model probability fidelity.",
    contentMarkdown: `### Brier Score & Expected Calibration Error

- **Brier Score**:
  $$\\text{BS} = \\frac{1}{N} \\sum_{t=1}^N (f_t - o_t)^2$$
  *Lower is better (0 = perfect calibration, 0.25 = uninformative 50/50 base rate).*

- **Expected Calibration Error (ECE)**:
  $$\\text{ECE} = \\sum_{m=1}^M \\frac{|B_m|}{N} \\big| \\text{acc}(B_m) - \\text{conf}(B_m) \\big|$$
  *Measures average difference between predicted confidence and observed empirical accuracy.*`,
  },
  {
    id: "stat-correlation-matrix",
    title: "Pearson & Spearman Correlation",
    category: "statistics",
    tags: ["correlation", "pearson", "spearman", "cross-market"],
    summary: "Linear and monotonic cross-market dependence metrics with sample stability intervals.",
    contentMarkdown: `### Cross-Market Correlation Metrics

- **Pearson Linear Correlation**:
  $$r_{xy} = \\frac{\\sum (x_i - \\bar{x})(y_i - \\bar{y})}{\\sqrt{\\sum (x_i - \\bar{x})^2 \\sum (y_i - \\bar{y})^2}}$$

- **Spearman Rank Correlation**:
  $$\\rho = 1 - \\frac{6 \\sum d_i^2}{n(n^2 - 1)}$$

*Institutional Standard*: Correlation values must always report sample size ($n$) and timeframe intervals.`,
  },

  // 4. Technical Indicators
  {
    id: "ind-atr-volatility",
    title: "Average True Range (ATR) & Volatility Regime",
    category: "indicators",
    tags: ["atr", "volatility", "regime", "range"],
    summary: "True Range formula and ATR-normalized volatility classification.",
    contentMarkdown: `### Average True Range (ATR) & Volatility Regimes

$$\\text{TR} = \\max\\big( \\text{High} - \\text{Low},\\; |\\text{High} - \\text{Close}_{\\text{prev}}|,\\; |\\text{Low} - \\text{Close}_{\\text{prev}}| \\big)$$
$$\\text{ATR}_t = \\frac{\\text{ATR}_{t-1} \\times (n-1) + \\text{TR}_t}{n}$$

- **Regime Thresholds**:
  - *Low Volatility*: $\\text{ATR} / \\text{SMA}(\\text{ATR}, 50) < 0.80$
  - *Normal Volatility*: $0.80 \\le \\text{Ratio} \\le 1.30$
  - *High Volatility / Expansion*: $\\text{Ratio} > 1.30$`,
  },
  {
    id: "ind-ema-relationships",
    title: "Exponential Moving Average (EMA)",
    category: "indicators",
    tags: ["ema", "trend", "moving average", "smoothing"],
    summary: "Recursive smoothing formula for trend following and dynamic support/resistance.",
    contentMarkdown: `### Exponential Moving Average (EMA)

$$\\alpha = \\frac{2}{N + 1}$$
$$\\text{EMA}_t = \\alpha \\times \\text{Price}_t + (1 - \\alpha) \\times \\text{EMA}_{t-1}$$

*Usage*: Evaluated across multiple timeframes (20, 50, 200 EMA) to detect trend persistence and structural alignment.`,
  },
];

export function searchDocumentation(query: string): DocItem[] {
  const trimmed = query.trim().toLowerCase();
  if (!trimmed) return PLATFORM_DOCUMENTATION_INDEX;

  const terms = trimmed.split(/\s+/).filter(Boolean);

  return PLATFORM_DOCUMENTATION_INDEX.filter((doc) => {
    const targetString = `${doc.title} ${doc.category} ${doc.tags.join(" ")} ${doc.summary} ${doc.contentMarkdown}`.toLowerCase();
    return terms.every((term) => targetString.includes(term));
  });
}
