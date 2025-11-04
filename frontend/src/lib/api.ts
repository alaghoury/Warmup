const DEFAULT_API_BASE_URL = "http://127.0.0.1:8000/api";

const rawBaseUrl =
  (import.meta.env?.VITE_BACKEND_URL as string | undefined) || DEFAULT_API_BASE_URL;
const normalizedBaseUrl = rawBaseUrl.endsWith("/") ? rawBaseUrl.slice(0, -1) : rawBaseUrl;

function buildApiUrl(path: string): string {
  const normalizedPath = path.startsWith("/") ? path : `/${path}`;
  return `${normalizedBaseUrl}${normalizedPath}`;
}

export const API_BASE_URL = `${normalizedBaseUrl}/`;

export async function apiRequest(path: string, options: RequestInit = {}) {
  const response = await fetch(buildApiUrl(path), {
    headers: { "Content-Type": "application/json", ...(options.headers || {}) },
    ...options,
  });

  if (!response.ok) {
    const message = await response.text();
    throw new Error(`API Error ${response.status}: ${message}`);
  }

  return response.json();
}

export const fetchFromAPI = apiRequest;
