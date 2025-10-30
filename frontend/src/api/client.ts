import axios from "axios";

export const TOKEN_KEY = "warmup_token";
export const TOKEN_EXP_KEY = "warmup_token_exp";

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || "http://127.0.0.1:8000/api",
  headers: { "Content-Type": "application/json" },
});

function isBrowser() {
  return typeof window !== "undefined" && typeof window.localStorage !== "undefined";
}

function persistAuthSession(accessToken: string, expiresIn?: number) {
  if (!isBrowser()) return;
  window.localStorage.setItem(TOKEN_KEY, accessToken);
  const lifetime = typeof expiresIn === "number" && Number.isFinite(expiresIn) ? expiresIn : 0;
  const expiresAt = Date.now() + lifetime * 1000;
  window.localStorage.setItem(TOKEN_EXP_KEY, expiresAt.toString());
}

export function clearAuthSession() {
  if (!isBrowser()) return;
  window.localStorage.removeItem(TOKEN_KEY);
  window.localStorage.removeItem(TOKEN_EXP_KEY);
}

export function getStoredToken(): string | null {
  if (!isBrowser()) return null;
  const token = window.localStorage.getItem(TOKEN_KEY);
  const expiresRaw = window.localStorage.getItem(TOKEN_EXP_KEY);
  if (!token || !expiresRaw) {
    return null;
  }
  const expiresAt = Number.parseInt(expiresRaw, 10);
  if (!Number.isFinite(expiresAt) || expiresAt <= Date.now()) {
    clearAuthSession();
    return null;
  }
  return token;
}

api.interceptors.request.use((config) => {
  const token = getStoredToken();
  if (token) {
    config.headers = config.headers ?? {};
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export interface AuthPayload {
  name?: string;
  email: string;
  password: string;
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
  expires_in: number;
  user: unknown;
}

function persistAuthResponse(data: AuthResponse) {
  persistAuthSession(data.access_token, data.expires_in);
}

export async function register(payload: AuthPayload) {
  const { data } = await api.post<AuthResponse>("/auth/register", payload);
  persistAuthResponse(data);
  return data;
}

export async function login(email: string, password: string) {
  const form = new FormData();
  form.append("username", email);
  form.append("password", password);
  const { data } = await api.post<AuthResponse>("/auth/login", form, {
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
  });
  persistAuthResponse(data);
  return data;
}

export async function getCurrentUser() {
  const { data } = await api.get("/auth/me");
  return data;
}

export async function getAllUsers() {
  const { data } = await api.get("/users");
  return data;
}

export async function deactivateUser(userId: number) {
  const { data } = await api.post(`/admin/users/${userId}/deactivate`);
  return data;
}

export async function activateUser(userId: number) {
  const { data } = await api.post(`/admin/users/${userId}/activate`);
  return data;
}

export async function getAdminUsers() {
  const { data } = await api.get("/admin/users");
  return data;
}

export async function getAdminStats() {
  const { data } = await api.get("/admin/stats");
  return data;
}

export async function getPlans() {
  const { data } = await api.get("/subscriptions/plans");
  return data;
}

export async function getSubscription() {
  const { data } = await api.get("/subscriptions/me");
  return data;
}

export async function checkoutPlan(slug: string) {
  const { data } = await api.post("/subscriptions/checkout", null, {
    params: { plan_slug: slug },
  });
  return data;
}

export async function getUsage() {
  const { data } = await api.get("/subscriptions/usage");
  return data;
}

export async function getAnalyticsSummary() {
  const { data } = await api.get("/analytics/summary");
  return data;
}

export function logout() {
  clearAuthSession();
}

export default api;
