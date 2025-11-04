import React, { useState } from "react";

import { apiRequest } from "../lib/api";

export default function LiveChecker() {
  const [domain, setDomain] = useState("example.com");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any | null>(null);
  const [error, setError] = useState<string>("");

  async function handleCheck(e?: React.FormEvent) {
    e?.preventDefault();
    if (!domain) return;
    setLoading(true);
    setError("");
    try {
      const data = await apiRequest(
        `/v1/check/domain?domain=${encodeURIComponent(domain)}`,
      );
      setResult(data);
    } catch (err: any) {
      setError(err.message || "Failed to check domain");
      setResult(null);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="rounded-lg border border-gray-200 bg-white p-4 shadow-sm">
      <h3 className="text-lg font-semibold text-gray-800">Live Deliverability Checker</h3>
      <p className="text-sm text-gray-500">
        Enter a sending domain to check MX records, blacklist hits, and recent spam scores.
      </p>
      <form onSubmit={handleCheck} className="mt-3 flex flex-col gap-3 sm:flex-row">
        <input
          className="flex-1 rounded border border-gray-300 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none"
          placeholder="yourdomain.com"
          value={domain}
          onChange={(event) => setDomain(event.target.value)}
        />
        <button
          type="submit"
          className="rounded bg-blue-600 px-4 py-2 text-sm font-medium text-white hover:bg-blue-700 disabled:opacity-60"
          disabled={loading}
        >
          {loading ? "Checking..." : "Check"}
        </button>
      </form>
      {error && <p className="mt-3 rounded bg-red-100 px-3 py-2 text-sm text-red-700">{error}</p>}
      {result && !error && (
        <div className="mt-4 space-y-3 text-sm text-gray-700">
          <div>
            <span className="font-semibold">Domain:</span> {result.domain}
          </div>
          <div>
            <span className="font-semibold">MX Records:</span>{" "}
            {result.mx_records.length ? result.mx_records.join(", ") : "None"}
          </div>
          <div>
            <span className="font-semibold">Blacklist Hits:</span>{" "}
            {result.blacklist_hits.length ? result.blacklist_hits.join(", ") : "None"}
          </div>
          <div>
            <span className="font-semibold">Warnings:</span>{" "}
            {result.warnings.length ? result.warnings.join(" · ") : "Clear"}
          </div>
          <div className="rounded bg-gray-50 p-3">
            <p className="font-semibold text-gray-800">Spam Score Summary</p>
            <p>Average Score: {result.spam.average_score ?? "n/a"}</p>
            <p>Latest Score: {result.spam.latest_score ?? "n/a"}</p>
            <p>
              Last Checked:{" "}
              {result.spam.last_checked_at
                ? new Date(result.spam.last_checked_at).toLocaleString()
                : "n/a"}
            </p>
            <p>Samples stored: {result.spam.count}</p>
          </div>
        </div>
      )}
    </div>
  );
}
