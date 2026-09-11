import {
  createContext,
  useCallback,
  useContext,
  useMemo,
  useState,
  type ReactNode,
} from "react";
import type { GlobalDialogState, NotificationKind, WorkstationNotification } from "./overlayTypes";
import {
  DEFAULT_THEME_ID,
  nextThemeId,
  normalizeThemeId,
  type ThemeId,
} from "../design/theme";

type OverlayContextValue = {
  commandOpen: boolean;
  openCommandPalette: () => void;
  closeCommandPalette: () => void;
  searchOpen: boolean;
  openGlobalSearch: () => void;
  closeGlobalSearch: () => void;
  /** UI-CONV-P03 item 3: workspace settings surface (shell-owned overlay). */
  settingsOpen: boolean;
  openSettings: () => void;
  closeSettings: () => void;
  /** UI-CONV-P03 item 5: governance & evidence surface (shell-owned overlay). */
  governanceOpen: boolean;
  openGovernance: () => void;
  closeGovernance: () => void;
  notifications: WorkstationNotification[];
  notify: (kind: NotificationKind, title: string, message: string) => void;
  dismissNotification: (id: string) => void;
  dialog: GlobalDialogState;
  openDialog: (dialog: NonNullable<GlobalDialogState>) => void;
  closeDialog: () => void;
  /** BO-F-00: six-theme vocabulary (Blueprint §3). */
  themeMode: ThemeId;
  /** BO-F-00: cycles midnight → light → slate → teal → amber → high-contrast. */
  toggleTheme: () => void;
  /** BO-F-00: set a specific theme (normalizes unknown/legacy values). */
  setTheme: (id: ThemeId) => void;
};

const OverlayContext = createContext<OverlayContextValue | null>(null);

export function OverlayProvider({ children }: { children: ReactNode }) {
  const [commandOpen, setCommandOpen] = useState(false);
  const [searchOpen, setSearchOpen] = useState(false);
  const [settingsOpen, setSettingsOpen] = useState(false);
  const [governanceOpen, setGovernanceOpen] = useState(false);
  const [notifications, setNotifications] = useState<WorkstationNotification[]>([]);
  const [dialog, setDialog] = useState<GlobalDialogState>(null);
  const [themeMode, setThemeMode] = useState<ThemeId>(DEFAULT_THEME_ID);

  const notify = useCallback((kind: NotificationKind, title: string, message: string) => {
    setNotifications((current) => [
      { id: `${Date.now()}-${current.length}`, kind, title, message },
      ...current,
    ].slice(0, 6));
  }, []);

  const dismissNotification = useCallback((id: string) => {
    setNotifications((current) => current.filter((notification) => notification.id !== id));
  }, []);

  const value = useMemo<OverlayContextValue>(
    () => ({
      commandOpen,
      openCommandPalette: () => setCommandOpen(true),
      closeCommandPalette: () => setCommandOpen(false),
      searchOpen,
      openGlobalSearch: () => setSearchOpen(true),
      closeGlobalSearch: () => setSearchOpen(false),
      settingsOpen,
      openSettings: () => setSettingsOpen(true),
      closeSettings: () => setSettingsOpen(false),
      governanceOpen,
      openGovernance: () => setGovernanceOpen(true),
      closeGovernance: () => setGovernanceOpen(false),
      notifications,
      notify,
      dismissNotification,
      dialog,
      openDialog: setDialog,
      closeDialog: () => setDialog(null),
      themeMode,
      // BO-F-00: toggle = fixed cycle through the six-theme vocabulary.
      toggleTheme: () => setThemeMode((current) => nextThemeId(current)),
      // BO-F-00: explicit setter used by the persisted-preference restore path.
      setTheme: (id) => setThemeMode(normalizeThemeId(id)),
    }),
    [commandOpen, dialog, dismissNotification, governanceOpen, notifications, notify, searchOpen, settingsOpen, themeMode],
  );

  return <OverlayContext.Provider value={value}>{children}</OverlayContext.Provider>;
}

export function useOverlayController(): OverlayContextValue {
  const value = useContext(OverlayContext);
  if (!value) throw new Error("OverlayProvider missing");
  return value;
}
