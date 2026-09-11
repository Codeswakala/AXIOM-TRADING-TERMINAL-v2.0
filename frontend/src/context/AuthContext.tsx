import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useMemo,
  useState,
  type ReactNode,
} from "react";
import {
  fetchCurrentOperator,
  login as apiLogin,
  logoutRequest,
  type Operator,
} from "../api/client";
import { clearTokens, getAccessToken, setTokens } from "../auth/tokenStorage";

type AuthContextValue = {
  operator: Operator | null;
  loading: boolean;
  isAuthenticated: boolean;
  login: (username: string, password: string) => Promise<void>;
  logout: () => Promise<void>;
  refreshProfile: () => Promise<void>;
};

const AuthContext = createContext<AuthContextValue | undefined>(undefined);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [operator, setOperator] = useState<Operator | null>(null);
  const [loading, setLoading] = useState(true);

  const refreshProfile = useCallback(async () => {
    const token = getAccessToken();
    if (!token) {
      setOperator(null);
      return;
    }
    try {
      const me = await fetchCurrentOperator();
      setOperator(me);
    } catch {
      clearTokens();
      setOperator(null);
    }
  }, []);

  useEffect(() => {
    void (async () => {
      setLoading(true);
      await refreshProfile();
      setLoading(false);
    })();
  }, [refreshProfile]);

  const login = useCallback(async (username: string, password: string) => {
    const result = await apiLogin(username, password);
    setTokens(result.tokens.access_token, result.tokens.refresh_token);
    setOperator(result.operator);
  }, []);

  const logout = useCallback(async () => {
    try {
      if (getAccessToken()) {
        await logoutRequest();
      }
    } catch {
      /* still clear local session */
    }
    clearTokens();
    setOperator(null);
  }, []);

  const value = useMemo(
    () => ({
      operator,
      loading,
      isAuthenticated: operator != null,
      login,
      logout,
      refreshProfile,
    }),
    [operator, loading, login, logout, refreshProfile],
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth(): AuthContextValue {
  const ctx = useContext(AuthContext);
  if (!ctx) {
    throw new Error("useAuth must be used within AuthProvider");
  }
  return ctx;
}
