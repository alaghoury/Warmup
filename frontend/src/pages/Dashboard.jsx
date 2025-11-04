import React, { useEffect, useMemo, useState } from "react";
import { API_BASE_URL, apiRequest } from "../lib/api";
import LiveChecker from "../components/LiveChecker";

export default function Dashboard() {
  const [status, setStatus] = useState("loading");
  const [error, setError] = useState("");
  const [reputation, setReputation] = useState({
    history: [],
    latest: null,
    threshold: 15,
    alert: false,
  });
  const [toast, setToast] = useState("");
  const name =
    (typeof window !== "undefined" && window.localStorage.getItem("user")) || "Mohammed";

  useEffect(() => {
    let mounted = true;
    apiRequest("/v1/health")
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

  useEffect(() => {
    let mounted = true;
    apiRequest("/v1/reputation/stats")
      .then((data) => {
        if (!mounted) return;
        setReputation(data);
        if (data.alert && data.latest) {
          const latestScore =
            typeof data.latest.score === "number"
              ? data.latest.score.toFixed(2)
              : data.latest.score;
          setToast(`Reputation drop detected: latest score ${latestScore}`);
        }
      })
      .catch((err) => {
        console.warn("Failed to load reputation stats", err);
      });
    return () => {
      mounted = false;
    };
  }, []);

  const chartPath = useMemo(() => {
    if (!reputation.history.length) return "";
    const scores = reputation.history.map((point) => point.score);
    const minScore = Math.min(...scores, 0);
    const maxScore = Math.max(...scores, 100);
    const range = maxScore - minScore || 1;
    const width = 380;
    const height = 120;
    return reputation.history
      .map((point, index) => {
        const x = (index / Math.max(reputation.history.length - 1, 1)) * (width - 20) + 10;
        const y = height - ((point.score - minScore) / range) * (height - 20) - 10;
        return `${x},${y}`;
      })
      .join(" ");
  }, [reputation.history]);

  return (
    <div className="mx-auto flex max-w-5xl flex-col gap-6 p-4">
      <header className="text-center space-y-2">
        <h1 className="text-3xl font-bold text-gray-800">Welcome, {name} 👋</h1>
        <p className="text-gray-600">
          You’re now connected to the Warmup App backend successfully.
        </p>
      </header>

      {toast && (
        <div className="rounded border border-amber-300 bg-amber-50 px-4 py-3 text-sm text-amber-800">
          {toast}
        </div>
      )}

      <section className="grid gap-6 md:grid-cols-2">
        <div className="rounded-lg border border-gray-200 bg-white px-6 py-4 shadow-sm">
          <span className="text-sm uppercase tracking-wide text-gray-500">API Base URL</span>
          <span className="mt-1 block font-mono text-sm text-gray-800">{API_BASE_URL}</span>
          <span
            className={`mt-3 inline-flex items-center gap-1 rounded-full px-3 py-1 text-sm ${
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

        <div className="rounded-lg border border-gray-200 bg-white px-6 py-4 shadow-sm">
          <div className="mb-2 flex items-center justify-between">
            <h2 className="text-sm font-semibold uppercase tracking-wide text-gray-500">
              Reputation Score
            </h2>
            {reputation.latest && (
              <span className="text-sm font-medium text-gray-700">
                Latest:{" "}
                {typeof reputation.latest.score === "number"
                  ? reputation.latest.score.toFixed(1)
                  : reputation.latest.score}
              </span>
            )}
          </div>
          {reputation.history.length ? (
            <svg width={380} height={120} className="w-full">
              <rect width="100%" height="100%" rx={8} className="fill-slate-50" />
              <polyline
                fill="none"
                stroke={reputation.alert ? "#f97316" : "#2563eb"}
                strokeWidth={3}
                points={chartPath}
              />
            </svg>
          ) : (
            <p className="text-sm text-gray-500">Reputation history will appear after the first cycle.</p>
          )}
          <p className="mt-2 text-xs text-gray-500">
            Alerts trigger when the score drops more than {reputation.threshold} points.
          </p>
        </div>
      </section>

      <LiveChecker />
    </div>
  );
}
