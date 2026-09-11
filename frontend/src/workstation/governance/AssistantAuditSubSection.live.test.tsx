import { describe, it, expect } from "vitest";
import { render, screen, within } from "@testing-library/react";
import { AssistantAuditSubSection } from "./AssistantAuditSubSection";
import type { AssistantAuditEvent } from "../../api/assistantClient";

describe("UI-008-P02 AssistantAuditSubSection Live Audit Integration", () => {
  const mockAuditEvents: AssistantAuditEvent[] = [
    {
      id: "audit-evt-301",
      category: "SECURITY",
      action: "assistant.refused",
      actor: "operator_alpha",
      message: "Refusal: UNGROUNDED_QUERY_REFUSED (unsupported symbol requested)",
      resource_type: "assistant_response",
      resource_id: "resp-refusal-301",
      details: { reason: "UNGROUNDED_QUERY_REFUSED" },
      created_at: "2026-08-10T11:15:00Z",
    },
    {
      id: "audit-evt-302",
      category: "SECURITY",
      action: "assistant.refused",
      actor: "operator_beta",
      message: "Refusal: EXECUTION_ACTUATION_REFUSED (order placement attempt blocked)",
      resource_type: "assistant_response",
      resource_id: "resp-refusal-302",
      details: { reason: "EXECUTION_ACTUATION_REFUSED" },
      created_at: "2026-08-10T11:20:00Z",
    },
  ];

  // (T-2) Live audit events rendering
  it("renders live refusal audit events list when data is supplied", () => {
    render(<AssistantAuditSubSection liveAuditEvents={mockAuditEvents} />);

    const auditList = screen.getByTestId("assistant-audit-list");
    expect(auditList).toBeInTheDocument();

    const row1 = screen.getByTestId("audit-row-audit-evt-301");
    expect(row1).toBeInTheDocument();
    expect(within(row1).getByText("assistant.refused")).toBeInTheDocument();
    expect(within(row1).getByText(/UNGROUNDED_QUERY_REFUSED/i)).toBeInTheDocument();
    expect(within(row1).getByText(/Actor: operator_alpha/i)).toBeInTheDocument();

    const row2 = screen.getByTestId("audit-row-audit-evt-302");
    expect(row2).toBeInTheDocument();
    expect(within(row2).getByText(/EXECUTION_ACTUATION_REFUSED/i)).toBeInTheDocument();
  });

  // (T-3) Skeleton loading state
  it("renders skeleton loading indicator during audit events fetch", () => {
    render(<AssistantAuditSubSection loading={true} />);

    const skeleton = screen.getByTestId("audit-loading-skeleton");
    expect(skeleton).toBeInTheDocument();
    expect(skeleton.getAttribute("data-ui008-state")).toBe("loading");
    expect(screen.getByText(/Loading refusal audit records/i)).toBeInTheDocument();
  });

  // (T-4) Error state banner
  it("renders error state banner when audit fetch fails", () => {
    render(<AssistantAuditSubSection error="Failed to reach audit persistence service" />);

    const errorBanner = screen.getByTestId("audit-error-banner");
    expect(errorBanner).toBeInTheDocument();
    expect(errorBanner.getAttribute("data-ui008-state")).toBe("error");
    expect(errorBanner.textContent).toContain("Failed to reach audit persistence");
  });

  // (T-5) Empty state rendering
  it("renders empty state when audit event array is empty", () => {
    render(<AssistantAuditSubSection liveAuditEvents={[]} />);

    const empty = screen.getByTestId("p01-skeleton");
    expect(empty).toBeInTheDocument();
  });

  // (T-6) 401 Unauthorized handling state
  it("renders 401 unauthorized notice when operator session is unauthenticated", () => {
    render(<AssistantAuditSubSection isUnauthorized={true} />);

    const authBanner = screen.getByTestId("audit-auth-required");
    expect(authBanner).toBeInTheDocument();
    expect(authBanner.getAttribute("data-ui008-state")).toBe("unauthorized");
    expect(authBanner.textContent).toContain("Authentication required");
  });
});
