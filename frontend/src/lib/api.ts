import axios from "axios";

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || "http://127.0.0.1:8000/api",
  headers: { "Content-Type": "application/json" },
});

api.interceptors.request.use((config) => {
  const token = window.localStorage.getItem("token");
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

export async function register(payload: AuthPayload) {
  const { data } = await api.post("/auth/register", payload);
  window.localStorage.setItem("token", data.access_token);
  return data;
}

export async function login(email: string, password: string) {
  const form = new FormData();
  form.append("username", email);
  form.append("password", password);
  const { data } = await api.post("/auth/login", form, {
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
  });
  window.localStorage.setItem("token", data.access_token);
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
  window.localStorage.removeItem("token");
}

export default api;
