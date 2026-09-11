import { fireEvent, render, screen } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";
import { FeedHealthBar } from "./FeedHealthBar";

describe("FeedHealthBar", () => {
  it("renders connection state and fires controls", () => {
    const onStart = vi.fn();
    const onStop = vi.fn();
    const onReconnect = vi.fn();
    render(
      <FeedHealthBar
        connectionState="connected"
        lastMessageAt="2024-01-01T00:00:00Z"
        messagesPerMinute={12}
        messageCount={40}
        lagHintMs={25}
        reconnectCount={1}
        feedStats={{
          running: true,
          auto_start: false,
          adapter: "simulated-multi",
          connected: true,
          market_class: "multi",
          symbol: "EURUSD,BTCUSD",
          symbols: ["EURUSD", "BTCUSD"],
          timeframe: "M1",
          messages_received: 40,
          persist_count: 40,
          persist_errors: 0,
          lag_ms: 20,
          last_message_at: "2024-01-01T00:00:00Z",
          last_persisted_at: null,
          started_at: null,
          subscribers: 1,
          last_candle: null,
          latest_by_symbol: {},
          last_error: null,
          reconnect_count: 0,
          adapter_details: {},
        }}
        error={null}
        onStart={onStart}
        onStop={onStop}
        onReconnect={onReconnect}
      />,
    );
    expect(screen.getByText("connected")).toBeInTheDocument();
    expect(screen.getByText("EURUSD, BTCUSD")).toBeInTheDocument();
    fireEvent.click(screen.getByText("Start feed"));
    fireEvent.click(screen.getByText("Stop feed"));
    fireEvent.click(screen.getByText("Reconnect WS"));
    expect(onStart).toHaveBeenCalled();
    expect(onStop).toHaveBeenCalled();
    expect(onReconnect).toHaveBeenCalled();
  });
});
