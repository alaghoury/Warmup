import React, { useEffect, useState } from "react";
import api from "../api/client";

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

const Billing: React.FC = () => {
  const [plans, setPlans] = useState<Plan[]>([]);
  const [current, setCurrent] = useState<Subscription | null>(null);
  const [message, setMessage] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchBilling = async () => {
      try {
        const [plansResponse, currentResponse] = await Promise.all([
          api.get<Plan[]>("/subscriptions/plans"),
          api.get<Subscription | null>("/subscriptions/me"),
        ]);
        setPlans(plansResponse.data);
        setCurrent(currentResponse.data);
      } catch (err) {
        console.error("Failed to load billing info", err);
        setError("Unable to load billing details.");
      }
    };

    fetchBilling();
  }, []);

  const choosePlan = async (slug: string) => {
    try {
      const response = await api.post("/subscriptions/checkout", null, {
        params: { plan_slug: slug },
      });
      setMessage(response.data.message ?? "Subscription updated");
      const currentResponse = await api.get<Subscription | null>("/subscriptions/me");
      setCurrent(currentResponse.data);
      setError(null);
    } catch (err) {
      console.error("Failed to update subscription", err);
      setError("Unable to update subscription. Please try again later.");
    }
  };

  return (
    <section>
      <h3>Billing</h3>
      {error && <div style={{ color: "red" }}>{error}</div>}
      {message && <div style={{ color: "green" }}>{message}</div>}
      <div style={{ marginBottom: 12 }}>
        {current ? (
          <div>
            Current plan: <strong>{current.plan.name}</strong>
          </div>
        ) : (
          <div>No active subscription</div>
        )}
      </div>
      <div
        style={{
          display: "grid",
          gap: 12,
          gridTemplateColumns: "repeat(auto-fit, minmax(220px, 1fr))",
        }}
      >
        {plans.map((plan) => (
          <div
            key={plan.id}
            style={{ border: "1px solid #ddd", padding: 12, borderRadius: 8 }}
          >
            <h4 style={{ marginTop: 0 }}>{plan.name}</h4>
            <div style={{ fontWeight: "bold" }}>${plan.price_monthly}/mo</div>
            <pre style={{ whiteSpace: "pre-wrap" }}>
              {JSON.stringify(plan.limits_json, null, 2)}
            </pre>
            <button
              onClick={() => choosePlan(plan.slug)}
              disabled={current?.plan?.id === plan.id}
            >
              {current?.plan?.id === plan.id ? "Selected" : "Select"}
            </button>
          </div>
        ))}
      </div>
    </section>
  );
};

export default Billing;
