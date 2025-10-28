import React, { useState } from "react";
import { login, register } from "../lib/auth.js";

export default function AuthForm({ onSuccess }) {
  const [mode, setMode] = useState("login");
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  async function handleSubmit(event) {
    event.preventDefault();
    setError("");
    try {
      if (mode === "login") {
        await login(email, password);
      } else {
        await register(name, email, password);
        await login(email, password);
      }
      onSuccess?.();
    } catch (err) {
      console.error(err);
      setError("Authentication failed");
    }
  }

  return (
    <div style={{ maxWidth: 360, margin: "64px auto" }}>
      <h2>{mode === "login" ? "Login" : "Register"}</h2>
      <form onSubmit={handleSubmit} style={{ display: "grid", gap: 8 }}>
        {mode === "register" && (
          <input
            placeholder="Name"
            value={name}
            onChange={(event) => setName(event.target.value)}
            required
          />
        )}
        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(event) => setEmail(event.target.value)}
          required
        />
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(event) => setPassword(event.target.value)}
          required
        />
        <button type="submit">{mode === "login" ? "Login" : "Create account"}</button>
        {error && <span style={{ color: "red" }}>{error}</span>}
      </form>
      <button
        onClick={() => setMode(mode === "login" ? "register" : "login")}
        style={{ marginTop: 8 }}
      >
        {mode === "login" ? "Create an account" : "Have an account? Login"}
      </button>
    </div>
  );
}
