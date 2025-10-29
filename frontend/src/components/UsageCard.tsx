import { useEffect, useState } from "react";
import { getUsage } from "../lib/api";

interface UsageData {
  used_api_calls: number;
  limit_api_calls: number;
  remaining_api_calls: number;
}

export default function UsageCard() {
  const [data, setData] = useState<UsageData | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const load = async () => {
      try {
        const usage = await getUsage();
        setData(usage);
      } catch (err) {
        console.error("Failed to load usage", err);
        setError("Unable to load usage metrics.");
      }
    };
    load();
  }, []);

  if (error) {
    return <div className="rounded-lg bg-rose-100 px-3 py-2 text-sm text-rose-700">{error}</div>;
  }

  if (!data) {
    return <div className="text-sm text-slate-500">Loading usage…</div>;
  }

  const percent = Math.min(100, Math.round((data.used_api_calls / Math.max(1, data.limit_api_calls)) * 100));

  return (
    <section className="overflow-hidden rounded-xl bg-white p-6 shadow">
      <h3 className="text-lg font-semibold text-slate-900">Usage</h3>
      <p className="mt-2 text-sm text-slate-500">
        API calls used this cycle. Remaining {data.remaining_api_calls} of {data.limit_api_calls}.
      </p>
      <div className="mt-6">
        <div className="flex items-center justify-between text-xs font-medium uppercase tracking-wide text-slate-500">
          <span>Usage</span>
          <span>{percent}%</span>
        </div>
        <div className="mt-2 h-3 w-full overflow-hidden rounded-full bg-slate-100">
          <div
            className="h-full rounded-full bg-indigo-500 transition-all"
            style={{ width: `${percent}%` }}
          ></div>
        </div>
        <div className="mt-3 text-sm text-slate-600">
          {data.used_api_calls.toLocaleString()} / {data.limit_api_calls.toLocaleString()} API calls
        </div>
      </div>
    </section>
  );
}
