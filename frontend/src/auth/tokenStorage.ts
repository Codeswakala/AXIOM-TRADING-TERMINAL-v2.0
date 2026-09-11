const ACCESS_KEY = "axiom_access_token";
const REFRESH_KEY = "axiom_refresh_token";

/**
 * REF-002-E1 (Operator election, 2026-09-10): "Remember me" is functional.
 * persist=true  → tokens in localStorage (survive the browser session;
 *                 the historical default behavior).
 * persist=false → tokens in sessionStorage (cleared when the session ends).
 * The choice applies to the NEXT setTokens call; reads check both stores.
 */
let persistTokens = true;

export function setTokenPersistence(persist: boolean): void {
  persistTokens = persist;
}

function activeStore(): Storage {
  return persistTokens ? localStorage : sessionStorage;
}

export function getAccessToken(): string | null {
  return localStorage.getItem(ACCESS_KEY) ?? sessionStorage.getItem(ACCESS_KEY);
}

export function getRefreshToken(): string | null {
  return localStorage.getItem(REFRESH_KEY) ?? sessionStorage.getItem(REFRESH_KEY);
}

export function setTokens(access: string, refresh: string): void {
  // Never leave stale copies in the other store.
  clearTokens();
  activeStore().setItem(ACCESS_KEY, access);
  activeStore().setItem(REFRESH_KEY, refresh);
}

export function clearTokens(): void {
  localStorage.removeItem(ACCESS_KEY);
  localStorage.removeItem(REFRESH_KEY);
  sessionStorage.removeItem(ACCESS_KEY);
  sessionStorage.removeItem(REFRESH_KEY);
}
