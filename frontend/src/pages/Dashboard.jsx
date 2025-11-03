import React, { useEffect, useState } from "react";
import { API_BASE_URL, fetchFromAPI } from "../lib/api";

export default function Dashboard() {
  const [status, setStatus] = useState("loading");
  const [error, setError] = useState("");
  const name =
    (typeof window !== "undefined" && window.localStorage.getItem("user")) || "Mohammed";

  useEffect(() => {
    let mounted = true;
    fetchFromAPI("/api/v1/health")
      .then((res) => {
        if (!mounted) return;
        setStatus(res?.status === "ok" ? "ok" : "unknown");
      })
      .catch((err) => {
        console.error(err);
        if (mounted) {
          setError(err.message);
          setStatus("error");
        }
      });
    return () => {
      mounted = false;
    };
  }, []);

  return (
    <div className="text-center space-y-3">
      <h1 className="text-3xl font-bold text-gray-800">Welcome, {name} 👋</h1>
      <p className="text-gray-600">You’re now connected to the Warmup App backend successfully.</p>
      <div className="inline-flex flex-col items-center justify-center rounded-lg border border-gray-200 bg-white px-6 py-4 shadow-sm">
        <span className="text-sm uppercase tracking-wide text-gray-500">API Base URL</span>
        <span className="font-mono text-sm text-gray-800">{API_BASE_URL}</span>
        <span
          className={`mt-2 inline-flex items-center gap-1 rounded-full px-3 py-1 text-sm ${
            status === "ok"
              ? "bg-emerald-100 text-emerald-700"
              : status === "loading"
              ? "bg-yellow-100 text-yellow-700"
              : "bg-red-100 text-red-700"
          }`}
        >
          {status === "ok" && "Backend healthy"}
          {status === "loading" && "Checking health..."}
          {status === "error" && `Health check failed${error ? `: ${error}` : ""}`}
          {status === "unknown" && "Unexpected response"}
        </span>
      </div>
    </div>
  );
}
