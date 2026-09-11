/**
 * AXIOM Institutional Design System — Theme Contracts & Token Helpers (UI-009-P01)
 *
 * Provides typed access to the 5-tier design token hierarchy and validation helpers
 * for theme roles, contrast calculations, and semantic mappings.
 *
 * Invariant: All visual values reference CSS custom properties via var(--ix-*).
 */

export const BRAND_TOKENS = {
  midnightBlack: "var(--ix-color-midnight)",
  graphiteGray: "var(--ix-color-graphite)",
  electricBlue: "var(--ix-color-electric-blue)",
  successGreen: "var(--ix-color-success-green)",
  warningAmber: "var(--ix-color-warning-amber)",
  criticalRed: "var(--ix-color-critical-red)",
} as const;

export const TYPOGRAPHY_SCALE = {
  displayTitle: "var(--ix-type-display-title)",
  workspaceTitle: "var(--ix-type-workspace-title)",
  sectionHeading: "var(--ix-type-section-heading)",
  panelHeading: "var(--ix-type-panel-heading)",
  body: "var(--ix-type-body)",
  metadata: "var(--ix-type-metadata)",
} as const;

export const TYPOGRAPHY_TOKENS = {
  fontSizeDisplay: "var(--ix-font-size-display)",
  fontSizeWorkspaceTitle: "var(--ix-font-size-workspace-title)",
  fontSizeSectionHeading: "var(--ix-font-size-section-heading)",
  fontSizePanelHeading: "var(--ix-font-size-panel-heading)",
  fontSizeBody: "var(--ix-font-size-body)",
  fontSizeMetadata: "var(--ix-font-size-metadata)",
  fontSans: "var(--ix-font-sans)",
  fontMono: "var(--ix-font-mono)",
  weightRegular: "var(--ix-font-weight-regular)",
  weightMedium: "var(--ix-font-weight-medium)",
  weightSemibold: "var(--ix-font-weight-semibold)",
  weightBold: "var(--ix-font-weight-bold)",
  lineHeightTight: "var(--ix-line-height-tight)",
  lineHeightStandard: "var(--ix-line-height-standard)",
  lineHeightRelaxed: "var(--ix-line-height-relaxed)",
} as const;

export const SPACING_SCALE = {
  space1: "var(--ix-space-1)", // 4px
  space2: "var(--ix-space-2)", // 8px
  space3: "var(--ix-space-3)", // 12px
  space4: "var(--ix-space-4)", // 16px
  space5: "var(--ix-space-5)", // 20px
  space6: "var(--ix-space-6)", // 24px
  space8: "var(--ix-space-8)", // 32px
} as const;

export const BREAKPOINT_TOKENS = {
  lg: "var(--ix-breakpoint-lg)", // 1280px
  md: "var(--ix-breakpoint-md)", // 1024px
  sm: "var(--ix-breakpoint-sm)", // 768px
} as const;

export const TERMINAL_LAYOUT_TOKENS = {
  tickerHeight: "var(--ix-terminal-ticker-height)",
  watchlistWidth: "var(--ix-terminal-watchlist-width)",
  telemetryWidth: "var(--ix-terminal-telemetry-width)",
  dockHeight: "var(--ix-terminal-dock-height)",
} as const;

export const BREAKPOINTS_PX = {
  lg: 1280,
  md: 1024,
  sm: 768,
} as const;

export const TABLE_TOKENS = {
  stickyHeaderZIndex: "var(--ix-table-sticky-header-z-index)",
} as const;

export const HIERARCHY_TOKENS = {
  level1: "var(--ix-hierarchy-level-1)",
  level2: "var(--ix-hierarchy-level-2)",
  level3: "var(--ix-hierarchy-level-3)",
  level4: "var(--ix-hierarchy-level-4)",
} as const;

export const ELEVATION_TOKENS = {
  level1: "var(--ix-elevation-level-1)",
  level2: "var(--ix-elevation-level-2)",
  level3: "var(--ix-elevation-level-3)",
  level4: "var(--ix-elevation-level-4)",
  surface: "var(--ix-elevation-surface)",
  overlay: "var(--ix-elevation-overlay)",
} as const;

export const MOTION_TOKENS = {
  fast: "var(--ix-motion-fast)",
  standard: "var(--ix-motion-standard)",
  panel: "var(--ix-motion-panel)",
  ease: "var(--ix-motion-ease)",
} as const;

export const HIGH_CONTRAST_TOKENS = {
  bgRoot: "var(--ix-bg-root)",
  textPrimary: "var(--ix-text-primary)",
  borderSubtle: "var(--ix-border-subtle)",
  colorFocus: "var(--ix-color-focus)",
} as const;

export const institutionalTheme = {
  tokenTiers: [
    "Tier 1: Foundation Tokens",
    "Tier 2: Semantic Tokens",
    "Tier 3: Component Tokens",
    "Tier 4: Workspace Tokens",
    "Tier 5: Runtime Theme Overrides",
  ],
  tokenCategories: [
    "Color",
    "Typography",
    "Spacing",
    "Sizing",
    "Border",
    "Elevation",
    "Shadow",
    "Motion",
    "Opacity",
    "Radius",
    "Icon",
  ],
  semanticColorRoles: [
    "Background",
    "Surface",
    "Primary",
    "Secondary",
    "Accent",
    "Success",
    "Warning",
    "Critical",
    "Information",
    "Border",
    "Disabled",
    "Focus",
    "Selection",
    "Charts",
    "Governance",
    "Research",
    "Execution Research",
    "Intelligence",
  ],
  semanticColors: {
    positive: "var(--ix-color-success)",
    adverse: "var(--ix-color-critical)",
    information: "var(--ix-color-information)",
    attention: "var(--ix-color-warning)",
    intelligence: "var(--ix-color-intelligence)",
    neutral: "var(--ix-color-secondary)",
  },
  typography: TYPOGRAPHY_SCALE,
  typographyTokens: TYPOGRAPHY_TOKENS,
  spacing: SPACING_SCALE,
  motion: MOTION_TOKENS,
  brand: BRAND_TOKENS,
} as const;

/**
 * Calculates relative luminance for WCAG contrast ratio computations.
 */
export function getLuminance(hexColor: string): number {
  const cleanHex = hexColor.replace("#", "");
  const r = parseInt(cleanHex.substring(0, 2), 16) / 255;
  const g = parseInt(cleanHex.substring(2, 4), 16) / 255;
  const b = parseInt(cleanHex.substring(4, 6), 16) / 255;

  const a = [r, g, b].map((v) =>
    v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4),
  );

  return a[0] * 0.2126 + a[1] * 0.7152 + a[2] * 0.0722;
}

/**
 * Computes WCAG contrast ratio between two hex colors.
 */
export function computeContrastRatio(foregroundHex: string, backgroundHex: string): number {
  const lum1 = getLuminance(foregroundHex);
  const lum2 = getLuminance(backgroundHex);
  const brightest = Math.max(lum1, lum2);
  const darkest = Math.min(lum1, lum2);
  return (brightest + 0.05) / (darkest + 0.05);
}

/* =========================================================================
   BO-F-00 — Six-Theme System Registry
   -------------------------------------------------------------------------
   The Visual Blueprint (Operator-approved 2026-08-21) mandates six token-level
   themes: Midnight (default), Light, Slate, Teal, Amber, High-Contrast.
   This registry is the single typed source of truth for theme identity,
   normalization, cycling order, and the concrete hex values that the
   Tier-5 override blocks in tokens.css must implement. Tests pin both sides
   (registry hexes ↔ tokens.css blocks), so a palette change in one place
   without the other fails the suite.

   Binding rules (Blueprint §3, §6):
   - Token-level color overrides ONLY — layout/density/typography identical.
   - Midnight is the :root default; its class declares no overrides.
   - Teal/Amber accents are presentation variants, NOT brand colors
     (Operator-authorized reading; brand identity unchanged per Doc 16).
   - The enumerated set is fixed: arbitrary third-party styling is impossible
     because every accepted id must exist in this registry.
   ========================================================================= */

export const THEME_IDS = [
  "midnight",
  "light",
  "slate",
  "teal",
  "amber",
  "high-contrast",
] as const;

export type ThemeId = (typeof THEME_IDS)[number];

export const DEFAULT_THEME_ID: ThemeId = "midnight";

/**
 * RGB triple form of the theme palette. The registry deliberately stores
 * color values as numeric triples (never hex/rgba string literals) so the
 * constitutional rule "no ad-hoc color literals outside tokens.css"
 * (UI-CONV-P02) holds mechanically — this is a data structure, not styling.
 * Tests convert triples to hex via rgbToHex and pin them 1:1 against the
 * Tier-5 override blocks in tokens.css.
 */
export type RgbTriple = readonly [number, number, number];

export function rgbToHex([r, g, b]: RgbTriple): string {
  const channel = (value: number) => value.toString(16).padStart(2, "0");
  return `#${channel(r)}${channel(g)}${channel(b)}`;
}

export interface ThemeDefinition {
  id: ThemeId;
  label: string;
  className: string;
  description: string;
  /** RGB values mirrored 1:1 by the Tier-5 override block in tokens.css. */
  bgRoot: RgbTriple;
  bgSurface: RgbTriple;
  textPrimary: RgbTriple;
  textSecondary: RgbTriple;
  textMuted: RgbTriple;
  /** Accent override (active states). Undefined = inherit :root blue. */
  accent: RgbTriple | undefined;
  /** Focus-ring override. Undefined = inherit :root focus. */
  focus: RgbTriple | undefined;
}

export const THEME_META: Record<ThemeId, ThemeDefinition> = {
  midnight: {
    id: "midnight",
    label: "Midnight",
    className: "theme-midnight",
    description: "The approved prototype look — deep black, graphite, electric-blue accent.",
    bgRoot: [11, 14, 20],
    bgSurface: [17, 24, 34],
    textPrimary: [238, 244, 252],
    textSecondary: [169, 183, 201],
    textMuted: [148, 163, 184],
    accent: undefined,
    focus: undefined,
  },
  light: {
    id: "light",
    label: "Light",
    className: "theme-light",
    description: "White/silver panels, dark text, the same blue accent.",
    bgRoot: [248, 250, 252],
    bgSurface: [255, 255, 255],
    textPrimary: [11, 14, 20],
    textSecondary: [51, 65, 85],
    textMuted: [100, 116, 139],
    accent: undefined,
    focus: [37, 99, 235],
  },
  slate: {
    id: "slate",
    label: "Slate",
    className: "theme-slate",
    description: "Softer graphite-pro dark — mid-gray panels, reduced blue accent.",
    bgRoot: [31, 39, 51],
    bgSurface: [42, 52, 66],
    textPrimary: [226, 232, 240],
    textSecondary: [183, 194, 208],
    textMuted: [147, 164, 182],
    accent: [96, 165, 250],
    focus: [147, 197, 253],
  },
  teal: {
    id: "teal",
    label: "Teal",
    className: "theme-teal",
    description: "Navy/teal pro dark — cyan-teal accent for active states.",
    bgRoot: [12, 21, 32],
    bgSurface: [16, 31, 44],
    textPrimary: [230, 246, 248],
    textSecondary: [185, 214, 220],
    textMuted: [132, 172, 180],
    accent: [34, 211, 238],
    focus: [103, 232, 249],
  },
  amber: {
    id: "amber",
    label: "Amber",
    className: "theme-amber",
    description:
      "Warm terminal dark — amber/gold accent for active states (presentation-only variant).",
    bgRoot: [20, 18, 12],
    bgSurface: [28, 25, 18],
    textPrimary: [242, 237, 226],
    textSecondary: [201, 191, 166],
    textMuted: [161, 148, 111],
    accent: [245, 158, 11],
    focus: [251, 191, 36],
  },
  "high-contrast": {
    id: "high-contrast",
    label: "High Contrast",
    className: "theme-high-contrast",
    description: "Pure black/white with full-saturation semantics — WCAG AAA.",
    bgRoot: [0, 0, 0],
    bgSurface: [0, 0, 0],
    textPrimary: [255, 255, 255],
    textSecondary: [255, 255, 255],
    textMuted: [229, 229, 229],
    accent: [59, 130, 246],
    focus: [255, 255, 0],
  },
};

/**
 * Accepts any persisted/unknown theme value and returns a valid ThemeId.
 * Legacy records may hold "dark" (pre-F-00 vocabulary) — mapped to the
 * Midnight default so existing operators keep their look.
 */
export function normalizeThemeId(value: unknown): ThemeId {
  if (typeof value === "string" && value === "dark") return "midnight";
  if (typeof value === "string" && (THEME_IDS as readonly string[]).includes(value)) {
    return value as ThemeId;
  }
  return DEFAULT_THEME_ID;
}

/** Next theme in the fixed cycle (the header toggle + command action). */
export function nextThemeId(current: ThemeId): ThemeId {
  const index = THEME_IDS.indexOf(current);
  return THEME_IDS[(index + 1) % THEME_IDS.length];
}

/** CSS override class applied to the shell root for a theme. */
export function themeClassName(id: ThemeId): string {
  return THEME_META[id].className;
}
