import React, { useState } from "react";
import { isAxiosError } from "axios";
import { login, register } from "../lib/auth";

interface RegisterProps {
  onSuccess: () => void;
  onSwitchToLogin: () => void;
}

const Register: React.FC<RegisterProps> = ({ onSuccess, onSwitchToLogin }) => {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setLoading(true);
    setError(null);
    try {
      await register({ name, email, password });
      await login(email, password);
      onSuccess();
    } catch (err) {
      console.error("Registration failed", err);
      if (isAxiosError(err) && err.response) {
        const status = err.response.status;
        const detail =
          typeof err.response.data === "string"
            ? err.response.data
            : err.response.data?.detail;
        if (status === 409) {
          setError(detail ?? "Email already registered.");
        } else if (status === 400) {
          setError(detail ?? "Invalid registration details.");
        } else {
          setError(detail ?? "Unexpected error while registering.");
        }
      } else {
        setError("Unable to register with those details.");
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-card">
      <h2>Create your account</h2>
      {error && <p className="auth-error">{error}</p>}
      <form className="auth-form" onSubmit={handleSubmit}>
        <label>
          Name
          <input
            type="text"
            value={name}
            onChange={(event) => setName(event.target.value)}
            required
          />
        </label>
        <label>
          Email
          <input
            type="email"
            value={email}
            onChange={(event) => setEmail(event.target.value)}
            required
          />
        </label>
        <label>
          Password
          <input
            type="password"
            value={password}
            onChange={(event) => setPassword(event.target.value)}
            required
          />
        </label>
        <button type="submit" disabled={loading}>
          {loading ? "Creating..." : "Register"}
        </button>
      </form>
      <button className="auth-switch" onClick={onSwitchToLogin}>
        Already have an account? Login
      </button>
    </div>
  );
};

export default Register;
