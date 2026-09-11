export type NotificationKind = "Information" | "Success" | "Warning" | "Error" | "Governance" | "System";

export type NotificationDefinition = {
  kind: NotificationKind;
  icon: string;
  label: string;
  semanticRole: string;
};

export type WorkstationNotification = {
  id: string;
  kind: NotificationKind;
  title: string;
  message: string;
};

export type GlobalDialogState = {
  title: string;
  body: string;
} | null;

export const NOTIFICATION_DEFINITIONS: Record<NotificationKind, NotificationDefinition> = {
  Information: { kind: "Information", icon: "ℹ", label: "Information", semanticRole: "information" },
  Success: { kind: "Success", icon: "✓", label: "Success", semanticRole: "success" },
  Warning: { kind: "Warning", icon: "!", label: "Warning", semanticRole: "warning" },
  Error: { kind: "Error", icon: "×", label: "Error", semanticRole: "critical" },
  Governance: { kind: "Governance", icon: "G", label: "Governance", semanticRole: "governance" },
  System: { kind: "System", icon: "S", label: "System", semanticRole: "secondary" },
};

export const NOTIFICATION_KINDS = Object.keys(NOTIFICATION_DEFINITIONS) as NotificationKind[];
