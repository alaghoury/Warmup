import { useState } from "react";
import { login } from "../lib/auth";

interface LoginProps {
  onAuthenticated: (user: any) => void;
  onSwitchToRegister: () => void;
  onError: (message: string) => void;
  onSuccess: (message: string) => void;
}

export default function Login({
  onAuthenticated,
  onSwitchToRegister,
  onError,
  onSuccess,
}: LoginProps) {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setLoading(true);
    try {
      const data = await login(email, password);
      onAuthenticated(data.user);
      onSuccess("Logged in successfully");
    } catch (error) {
      console.error("Login failed", error);
      onError("Invalid email or password");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="mx-auto w-full max-w-md rounded-2xl bg-white p-8 shadow-lg">
      <h2 className="text-2xl font-semibold text-slate-900">Welcome back</h2>
      <p className="mt-1 text-sm text-slate-500">Sign in to access your dashboard.</p>
      <form className="mt-6 space-y-4" onSubmit={handleSubmit}>
        <div>
          <label className="block text-sm font-medium text-slate-700">Email</label>
          <input
            type="email"
            value={email}
            onChange={(event) => setEmail(event.target.value)}
            required
            className="mt-1 w-full rounded-lg border-slate-300 bg-white focus:border-indigo-500 focus:ring-indigo-500"
          />
        </div>
        <div>
          <label className="block text-sm font-medium text-slate-700">Password</label>
          <input
            type="password"
            value={password}
            onChange={(event) => setPassword(event.target.value)}
            required
            className="mt-1 w-full rounded-lg border-slate-300 bg-white focus:border-indigo-500 focus:ring-indigo-500"
          />
        </div>
        <button
          type="submit"
          disabled={loading}
          className="w-full rounded-lg bg-indigo-600 py-2 text-white transition hover:bg-indigo-500 disabled:cursor-not-allowed disabled:opacity-70"
        >
          {loading ? "Signing in…" : "Login"}
        </button>
      </form>
      <button
        type="button"
        onClick={onSwitchToRegister}
        className="mt-4 w-full rounded-lg border border-slate-200 py-2 text-sm font-medium text-slate-700 transition hover:border-indigo-500 hover:text-indigo-600"
      >
        Need an account? Register
      </button>
    </div>
  );
}
