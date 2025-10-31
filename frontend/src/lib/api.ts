const env = (import.meta.env ?? {}) as Record<string, string | undefined>;

const FALLBACK_BASE_URL = "https://containers.back4app.com/apps/34869968-eedb-4e79-9487-bae4b25e43b6";

const baseUrl =
  env.NEXT_PUBLIC_API_URL ??
  env.VITE_API_URL ??
  (typeof process !== "undefined" ? (process as any).env?.NEXT_PUBLIC_API_URL : undefined) ??
  FALLBACK_BASE_URL;

function buildUrl(path: string): string {
  if (/^https?:\/\//i.test(path)) {
    return path;
  }
  const normalizedBase = baseUrl.replace(/\/$/, "");
  const normalizedPath = path.startsWith("/") ? path.slice(1) : path;
  return `${normalizedBase}/${normalizedPath}`;
}

function mergeHeaders(headers?: HeadersInit): Headers {
  const merged = new Headers(headers ?? {});
  if (!merged.has("Accept")) {
    merged.set("Accept", "application/json");
  }
  const token =
    typeof window !== "undefined" ? window.localStorage?.getItem("token") : undefined;
  if (token && !merged.has("Authorization")) {
    merged.set("Authorization", `Bearer ${token}`);
  }
  return merged;
}

export async function fetchFromAPI<T = unknown>(
  path: string,
  options: RequestInit = {}
): Promise<T> {
  const { headers, ...rest } = options;
  const requestInit: RequestInit = {
    credentials: "include",
    ...rest,
    headers: mergeHeaders(headers),
  };

  const url = buildUrl(path);
  const response = await fetch(url, requestInit);
  const contentType = response.headers.get("content-type") ?? "";
  const isJson = contentType.includes("application/json");
  const payload = isJson ? await response.json() : await response.text();

  if (!response.ok) {
    const detail = typeof payload === "string" ? payload : payload?.detail;
    throw new Error(detail || `Request failed with status ${response.status}`);
  }

  return payload as T;
}

export function getApiBaseUrl(): string {
  return baseUrl;
}
