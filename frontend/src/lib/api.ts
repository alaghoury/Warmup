export const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_URL ||
  "https://containers.back4app.com/apps/34869968-eedb-4e79-9487-bae4b25e43b6";

export async function fetchFromAPI(path: string, options?: RequestInit) {
  const res = await fetch(`${API_BASE_URL}${path}`, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });
  if (!res.ok) {
    const err = await res.text();
    throw new Error(`API ${res.status}: ${err}`);
  }
  return res.json();
}
