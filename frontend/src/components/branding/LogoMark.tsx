/**
 * The AXIOM brand mark.
 *
 * POST-CLOSURE Operator directive (2026-08-19): the Operator supplied the
 * project logo as an image asset. It is rendered from
 * `/branding/axiom-logo.png` (public asset, no bundle cost) — used exactly as
 * provided, 410x408, opaque dark-background square.
 *
 * The GA-173 compass+epsilon SVG remains ONLY as the load-failure fallback
 * (the mark must never render blank), per the brand discipline of keeping the
 * mark visible on every surface.
 */

import { useState } from "react";

export interface LogoMarkProps {
  className?: string;
  testid?: string;
  title?: string;
}

const LOGO_ASSET_PATH = "/branding/axiom-logo.png";

export function LogoMark({
  className = "",
  testid,
  title = "AXIOM logo",
}: LogoMarkProps) {
  const [assetFailed, setAssetFailed] = useState(false);

  if (assetFailed) {
    // Fallback: the GA-173 compass + epsilon inline SVG.
    return (
      <svg
        viewBox="0 0 64 32"
        className={`axiom-logo-mark ${className}`.trim()}
        data-testid={testid}
        role="img"
        aria-label={title}
        width={64}
        height={32}
        fill="none"
        stroke="currentColor"
        strokeWidth={1.8}
        strokeLinecap="round"
        strokeLinejoin="round"
      >
        <title>{title}</title>
        <path d="M12.5 8.5 A 6 6 0 0 1 23.5 8.5" strokeWidth={1.2} />
        <circle cx="18" cy="9" r="2.2" fill="currentColor" stroke="none" />
        <line x1="18" y1="9" x2="9.5" y2="27.5" />
        <line x1="18" y1="9" x2="26.5" y2="27.5" />
        <path d="M9.5 27.5 L8 29.5 L11 29.5 Z" fill="currentColor" stroke="none" />
        <path d="M26.5 27.5 L25 29.5 L28 29.5 Z" fill="currentColor" stroke="none" />
        <path d="M46 7 C 38 7 34 11 34 16 C 34 21 38 25 46 25 C 49.5 25 51.8 23.6 52.8 21.6" />
        <line x1="35.5" y1="16" x2="50" y2="16" />
      </svg>
    );
  }

  return (
    <img
      src={LOGO_ASSET_PATH}
      alt={title}
      className={`axiom-logo-mark ${className}`.trim()}
      data-testid={testid}
      role="img"
      aria-label={title}
      onError={() => setAssetFailed(true)}
    />
  );
}
