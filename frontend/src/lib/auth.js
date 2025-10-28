import api from "../api";

export async function login(email, password) {
  const form = new FormData();
  form.append("username", email);
  form.append("password", password);
  const response = await api.post("/auth/login", form);
  localStorage.setItem("token", response.data.access_token);
  return response.data;
}

export async function register(name, email, password) {
  const response = await api.post("/auth/register", { name, email, password });
  return response.data;
}

export function logout() {
  localStorage.removeItem("token");
}

export function isAuthed() {
  return Boolean(localStorage.getItem("token"));
}
