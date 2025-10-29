import { useEffect, useState } from "react";
import { checkoutPlan, getPlans, getSubscription } from "../lib/api";

type Plan = {
  id: number;
  slug: string;
  name: string;
  price_monthly: number;
  limits_json: Record<string, number>;
};

type Subscription = {
  id: number;
  status: string;
  plan: Plan;
};

interface BillingProps {
  onNotify: (message: string, tone?: "success" | "error") => void;
}

export default function Billing({ onNotify }: BillingProps) {
  const [plans, setPlans] = useState<Plan[]>([]);
  const [current, setCurrent] = useState<Subscription | null>(null);
  const [loading, setLoading] = useState(false);

  const load = async () => {
    setLoading(true);
    try {
      const [plansData, currentData] = await Promise.all([getPlans(), getSubscription()]);
      setPlans(plansData);
      setCurrent(currentData);
    } catch (err) {
      console.error("Failed to load billing info", err);
      onNotify("Unable to load billing details", "error");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    load();
  }, []);

  const choosePlan = async (slug: string) => {
    try {
      const response = await checkoutPlan(slug);
      onNotify(response.message ?? "Subscription updated", "success");
      const currentData = await getSubscription();
      setCurrent(currentData);
    } catch (err) {
      console.error("Failed to update subscription", err);
      onNotify("Unable to update subscription", "error");
    }
  };

  return (
    <section className="space-y-4">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-semibold text-slate-900">Billing</h3>
          <p className="text-sm text-slate-500">Manage your subscription plan.</p>
        </div>
        <button
          type="button"
          onClick={load}
          disabled={loading}
          className="rounded-lg border border-slate-200 px-3 py-1.5 text-sm font-medium text-slate-600 transition hover:border-indigo-500 hover:text-indigo-600 disabled:cursor-not-allowed disabled:opacity-60"
        >
          {loading ? "Refreshing…" : "Refresh"}
        </button>
      </div>
      <div className="rounded-xl bg-white p-4 shadow">
        {current ? (
          <p className="text-sm text-slate-600">
            Current plan: <span className="font-semibold text-slate-900">{current.plan.name}</span>
          </p>
        ) : (
          <p className="text-sm text-slate-500">No active subscription yet.</p>
        )}
      </div>
      <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-3">
        {plans.map((plan) => (
          <div key={plan.id} className="flex h-full flex-col rounded-xl border border-slate-200 bg-white p-5 shadow-sm">
            <div className="flex items-start justify-between gap-4">
              <div>
                <h4 className="text-lg font-semibold text-slate-900">{plan.name}</h4>
                <p className="mt-1 text-sm text-slate-500">${plan.price_monthly}/mo</p>
              </div>
              <span className="rounded-full bg-indigo-50 px-3 py-1 text-xs font-semibold uppercase text-indigo-600">
                {plan.slug}
              </span>
            </div>
            <ul className="mt-4 space-y-2 text-sm text-slate-600">
              {Object.entries(plan.limits_json ?? {}).map(([key, value]) => (
                <li key={key} className="flex items-center gap-2">
                  <span className="h-2 w-2 rounded-full bg-indigo-500"></span>
                  <span>
                    {key.replace(/_/g, " ")} — <strong>{value}</strong>
                  </span>
                </li>
              ))}
            </ul>
            <div className="mt-6">
              <button
                type="button"
                onClick={() => choosePlan(plan.slug)}
                disabled={current?.plan?.id === plan.id}
                className="w-full rounded-lg bg-indigo-600 py-2 text-sm font-semibold text-white transition hover:bg-indigo-500 disabled:cursor-not-allowed disabled:bg-slate-300"
              >
                {current?.plan?.id === plan.id ? "Selected" : "Select"}
              </button>
            </div>
          </div>
        ))}
      </div>
    </section>
  );
}
