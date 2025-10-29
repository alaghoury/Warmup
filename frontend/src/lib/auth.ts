import { login as apiLogin, logout as apiLogout, register as apiRegister } from "./api";

const TOKEN_KEY = "token";

export async function login(email: string, password: string) {
  return apiLogin(email, password);
}

export async function register(payload: { name: string; email: string; password: string }) {
  return apiRegister(payload);
}

export function logout() {
  apiLogout();
}

export function getToken() {
  return window.localStorage.getItem(TOKEN_KEY);
}

export function isAuthed() {
  return Boolean(getToken());
}
