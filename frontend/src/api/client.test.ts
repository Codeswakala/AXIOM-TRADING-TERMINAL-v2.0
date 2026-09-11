import { describe, expect, it } from "vitest";
import { getWebSocketUrl } from "./client";

describe("api client helpers", () => {
  it("builds websocket url from window location when env not set", () => {
    const url = getWebSocketUrl("/ws/status");
    expect(url).toContain("/ws/status");
    expect(url.startsWith("ws://") || url.startsWith("wss://")).toBe(true);
  });
});
