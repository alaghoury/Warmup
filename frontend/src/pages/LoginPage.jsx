import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { fetchFromAPI } from "../lib/api";

export default function LoginPage() {
  const navigate = useNavigate();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  const handleLogin = async (e) => {
    e.preventDefault();
    try {
      const data = await fetchFromAPI("/api/auth/login", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ email, password }),
      });
      const { access_token: token, user } = data ?? {};
      if (token) {
        if (typeof window !== "undefined") {
          window.localStorage.setItem("token", token);
          if (user?.name) {
            window.localStorage.setItem("user", user.name);
          }
        }
        navigate("/dashboard");
      } else {
        throw new Error("Missing access token");
      }
    } catch (err) {
      console.error(err);
      setError(err?.message || "Invalid email or password");
    }
  };

  return (
    <div className="bg-white p-8 rounded-xl shadow-md w-96">
      <h2 className="text-2xl font-bold text-center mb-4">Welcome back</h2>
      <form onSubmit={handleLogin} className="flex flex-col gap-4">
        <input
          type="email"
          placeholder="Email"
          className="border p-2 rounded"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        />
        <input
          type="password"
          placeholder="Password"
          className="border p-2 rounded"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />
        {error && <p className="text-red-500 text-sm text-center">{error}</p>}
        <button className="bg-blue-600 text-white p-2 rounded hover:bg-blue-700">
          Login
        </button>
      </form>
    </div>
  );
}
