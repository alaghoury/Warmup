import { useEffect, useState } from "react";
import { getAnalyticsSummary } from "../lib/api";

interface AnalyticsSummary {
  total_users: number;
  total_api_calls: number;
}

export default function AnalyticsChart() {
  const [data, setData] = useState<AnalyticsSummary | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const load = async () => {
      try {
        const summary = await getAnalyticsSummary();
        setData(summary);
      } catch (err) {
        console.error("Failed to load analytics", err);
        setError("Unable to load analytics summary.");
      }
    };
    load();
  }, []);

  if (error) {
    return <div className="rounded-lg bg-rose-100 px-3 py-2 text-sm text-rose-700">{error}</div>;
  }

  if (!data) {
    return <div className="text-sm text-slate-500">Loading analytics…</div>;
  }

  return (
    <section className="grid gap-4 sm:grid-cols-2">
      <div className="rounded-xl bg-white p-5 shadow">
        <p className="text-xs uppercase tracking-wide text-slate-500">Total users</p>
        <p className="mt-2 text-3xl font-semibold text-slate-900">{data.total_users}</p>
      </div>
      <div className="rounded-xl bg-white p-5 shadow">
        <p className="text-xs uppercase tracking-wide text-slate-500">Total API calls</p>
        <p className="mt-2 text-3xl font-semibold text-slate-900">{data.total_api_calls}</p>
      </div>
    </section>
  );
}
