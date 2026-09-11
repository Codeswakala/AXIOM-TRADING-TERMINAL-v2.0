import React from "react";
import ReactDOM from "react-dom/client";
import { BrowserRouter } from "react-router-dom";
import App from "./App";
import "./styles/global.css";

ReactDOM.createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    {/* BO-F-00.3 — React Router v7 future-flags decision: OPTION A (opt-in).
       Both flags are explicitly enabled here rather than recorded as
       technical debt; they change nothing about the current route tree but
       pin future-version behavior (transition wrapping + splat-relative
       path semantics) at the earliest point. */}
    <BrowserRouter future={{ v7_startTransition: true, v7_relativeSplatPath: true }}>
      <App />
    </BrowserRouter>
  </React.StrictMode>,
);
