import { login as loginRequest, register as registerRequest, RegisterPayload } from "../api/auth";

const TOKEN_KEY = "token";

export async function login(email: string, password: string) {
  const data = await loginRequest(email, password);
  window.localStorage.setItem(TOKEN_KEY, data.access_token);
  return data;
}

export async function register(payload: RegisterPayload) {
  const data = await registerRequest(payload);
  return data;
}

export function logout() {
  window.localStorage.removeItem(TOKEN_KEY);
}

export function getToken() {
  return window.localStorage.getItem(TOKEN_KEY);
}

export function isAuthed() {
  return Boolean(getToken());
}
