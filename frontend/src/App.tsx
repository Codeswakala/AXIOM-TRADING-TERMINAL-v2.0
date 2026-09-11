import { Route, Routes } from "react-router-dom";
import { AuthProvider } from "./context/AuthContext";
import { ProtectedRoute } from "./auth/ProtectedRoute";
import { LoginPage } from "./pages/LoginPage";
import { InstitutionalWorkspaceShell } from "./workstation/components/InstitutionalWorkspaceShell";
import { GatedRouteElement, WORKSPACE_REGISTRY } from "./workstation/registry/workspaceRegistry";

export default function App() {
  return (
    <AuthProvider>
      <Routes>
        <Route path="/login" element={<LoginPage />} />
        <Route
          element={
            <ProtectedRoute>
              <InstitutionalWorkspaceShell />
            </ProtectedRoute>
          }
        >
          {WORKSPACE_REGISTRY.map((definition) => (
            <Route
              key={definition.route}
              path={definition.route}
              element={<GatedRouteElement definition={definition} />}
            />
          ))}
        </Route>
      </Routes>
    </AuthProvider>
  );
}
