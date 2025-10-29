import { useState } from "react";
import { register } from "../lib/api";

interface RegisterProps {
  onAuthenticated: (user: any) => void;
  onSwitchToLogin: () => void;
  onError: (message: string) => void;
  onSuccess: (message: string) => void;
}

export default function Register({
  onAuthenticated,
  onSwitchToLogin,
  onError,
  onSuccess,
}: RegisterProps) {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setLoading(true);
    try {
      const data = await register({ name, email, password });
      onAuthenticated(data.user);
      onSuccess("Account created successfully");
    } catch (error: any) {
      console.error("Registration failed", error);
      const message = error?.response?.data?.detail ?? "Unable to register";
      onError(message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="mx-auto w-full max-w-md rounded-2xl bg-white p-8 shadow-lg">
      <h2 className="text-2xl font-semibold text-slate-900">Create your account</h2>
      <p className="mt-1 text-sm text-slate-500">Start your Warmup trial in seconds.</p>
      <form className="mt-6 space-y-4" onSubmit={handleSubmit}>
        <div>
          <label className="block text-sm font-medium text-slate-700">Name</label>
          <input
            type="text"
            value={name}
            onChange={(event) => setName(event.target.value)}
            required
            className="mt-1 w-full rounded-lg border-slate-300 bg-white focus:border-indigo-500 focus:ring-indigo-500"
          />
        </div>
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
            minLength={6}
            className="mt-1 w-full rounded-lg border-slate-300 bg-white focus:border-indigo-500 focus:ring-indigo-500"
          />
        </div>
        <button
          type="submit"
          disabled={loading}
          className="w-full rounded-lg bg-indigo-600 py-2 text-white transition hover:bg-indigo-500 disabled:cursor-not-allowed disabled:opacity-70"
        >
          {loading ? "Creating account…" : "Register"}
        </button>
      </form>
      <button
        type="button"
        onClick={onSwitchToLogin}
        className="mt-4 w-full rounded-lg border border-slate-200 py-2 text-sm font-medium text-slate-700 transition hover:border-indigo-500 hover:text-indigo-600"
      >
        Already have an account? Login
      </button>
    </div>
  );
}
