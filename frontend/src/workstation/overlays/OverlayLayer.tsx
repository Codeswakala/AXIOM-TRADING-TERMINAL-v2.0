import type { RegisteredCommand } from "../commands/commandTypes";
import { GlobalSearchOverlay } from "../search/GlobalSearchOverlay";
import { CommandPalette } from "./CommandPalette";
import { GlobalDialogLayer } from "./GlobalDialogLayer";
import { NotificationLayer } from "./NotificationLayer";
import { WorkspaceSettingsOverlay } from "../../components/terminal/settings/WorkspaceSettingsOverlay";
import { GovernanceOverlay } from "../../components/terminal/governance/GovernanceOverlay";

export type OverlayLayerProps = {
  commands: readonly RegisteredCommand[];
  onNavigate: (route: string) => void;
};

export function OverlayLayer({ commands, onNavigate }: OverlayLayerProps) {
  return (
    <div className="ix-overlay-layer" aria-label="Overlay layer" data-region="F" data-overlay-layer="overlay">
      <CommandPalette commands={commands} />
      <GlobalSearchOverlay onNavigate={onNavigate} />
      <WorkspaceSettingsOverlay />
      <GovernanceOverlay />
      <GlobalDialogLayer />
      <NotificationLayer />
    </div>
  );
}
