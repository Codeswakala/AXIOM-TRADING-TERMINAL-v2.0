import { describe, it, expect } from "vitest";
import {
  PLATFORM_DOCUMENTATION_INDEX,
  searchDocumentation,
} from "./documentationIndex";

describe("UI-008-P05 Documentation Index & Search (T-2, T-3)", () => {
  it("indexes platform documents across all 4 mandatory categories (T-2)", () => {
    expect(PLATFORM_DOCUMENTATION_INDEX.length).toBeGreaterThanOrEqual(8);

    const categories = new Set(PLATFORM_DOCUMENTATION_INDEX.map((d) => d.category));
    expect(categories.has("governance")).toBe(true);
    expect(categories.has("architecture")).toBe(true);
    expect(categories.has("statistics")).toBe(true);
    expect(categories.has("indicators")).toBe(true);
  });

  it("searchDocumentation returns all documents when query is empty", () => {
    const allDocs = searchDocumentation("");
    expect(allDocs).toHaveLength(PLATFORM_DOCUMENTATION_INDEX.length);
  });

  it("searchDocumentation performs client-side fuzzy search on keywords (T-3)", () => {
    const wilsonResults = searchDocumentation("Wilson Score");
    expect(wilsonResults.length).toBeGreaterThanOrEqual(1);
    expect(wilsonResults[0].id).toBe("stat-wilson-score");

    const zeroTrustResults = searchDocumentation("Zero Trust");
    expect(zeroTrustResults.length).toBeGreaterThanOrEqual(1);
    expect(zeroTrustResults[0].id).toBe("gov-17-security");

    const brierResults = searchDocumentation("brier score ece");
    expect(brierResults.length).toBeGreaterThanOrEqual(1);
    expect(brierResults[0].id).toBe("stat-brier-ece");

    const atrResults = searchDocumentation("atr volatility");
    expect(atrResults.length).toBeGreaterThanOrEqual(1);
    expect(atrResults[0].id).toBe("ind-atr-volatility");
  });

  it("searchDocumentation returns empty array for non-matching queries", () => {
    const noResults = searchDocumentation("xyzNonExistentTerm998877");
    expect(noResults).toHaveLength(0);
  });
});
