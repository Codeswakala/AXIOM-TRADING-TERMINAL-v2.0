/**
 * Dynamic CSS Design Token Resolver for Canvas2D contexts (B-P03-1 / RSK-NEW-02)
 *
 * TradingView lightweight-charts renders directly to HTML5 Canvas2D and requires
 * resolved RGB/RGBA color strings (e.g. "rgb(16, 185, 129)"). It cannot parse CSS variables
 * ("var(--ix-*)"). This resolver reads computed styles dynamically from document.documentElement,
 * ensuring 100% token purity without hardcoding hex literals in production TSX code.
 */

export function getComputedToken(tokenName: string, fallbackRgb = "rgb(11, 14, 20)"): string {
  if (typeof window !== "undefined" && typeof document !== "undefined" && document.documentElement) {
    const computedVal = getComputedStyle(document.documentElement)
      .getPropertyValue(tokenName)
      .trim();
    if (computedVal) {
      return computedVal;
    }
  }
  return fallbackRgb;
}
