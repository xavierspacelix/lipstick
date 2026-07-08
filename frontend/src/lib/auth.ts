export function isAuthenticated(): boolean {
  return document.cookie.includes("access_token=");
}

export function getRedirectUrl(): string | null {
  const params = new URLSearchParams(window.location.search);
  return params.get("redirect");
}
