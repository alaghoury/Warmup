import api from "./client";

export interface AuthResponse {
  access_token: string;
  token_type: string;
}

export async function login(email: string, password: string): Promise<AuthResponse> {
  const form = new FormData();
  form.append("username", email);
  form.append("password", password);
  const response = await api.post<AuthResponse>("/auth/login", form, {
    headers: { "Content-Type": "multipart/form-data" },
  });
  return response.data;
}

export interface RegisterPayload {
  name: string;
  email: string;
  password: string;
}

export async function register(payload: RegisterPayload) {
  const response = await api.post("/auth/register", payload);
  return response.data;
}
