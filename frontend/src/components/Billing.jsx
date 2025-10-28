import React, { useEffect, useState } from "react";
import api from "../api.js";

export default function Billing() {
  const [plans, setPlans] = useState([]);
  const [current, setCurrent] = useState(null);
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");

  async function refreshSubscription() {
    try {
      const response = await api.get("/subscriptions/me");
      setCurrent(response.data);
    } catch (err) {
      console.error(err);
      setCurrent(null);
    }
  }

  useEffect(() => {
    api
      .get("/subscriptions/plans")
      .then((response) => setPlans(response.data))
      .catch((err) => {
        console.error(err);
        setError("Failed to load plans");
      });
    refreshSubscription();
  }, []);

  async function choosePlan(slug) {
    try {
      const response = await api.post("/subscriptions/checkout", null, {
        params: { plan_slug: slug },
      });
      setMessage(response.data.message || "Subscription updated");
      setError("");
      await refreshSubscription();
    } catch (err) {
      console.error(err);
      setMessage("");
      setError("Checkout failed");
    }
  }

  return (
    <div>
      <h3>Billing</h3>
      {current ? (
        <div>
          Current plan: <strong>{current.plan.name}</strong>
        </div>
      ) : (
        <div>No active subscription</div>
      )}
      {message && <div style={{ color: "green" }}>{message}</div>}
      {error && <div style={{ color: "red" }}>{error}</div>}
      <div
        style={{
          display: "grid",
          gap: 12,
          gridTemplateColumns: "repeat(auto-fit, minmax(220px, 1fr))",
          marginTop: 12,
        }}
      >
        {plans.map((plan) => (
          <div
            key={plan.id}
            style={{ border: "1px solid #ddd", padding: 12, borderRadius: 8 }}
          >
            <h4>{plan.name}</h4>
            <div>${plan.price_monthly}/mo</div>
            <pre style={{ whiteSpace: "pre-wrap" }}>
              {JSON.stringify(plan.limits_json, null, 2)}
            </pre>
            <button
              onClick={() => choosePlan(plan.slug)}
              disabled={current?.plan?.id === plan.id}
            >
              Select
            </button>
          </div>
        ))}
      </div>
    </div>
  );
}
