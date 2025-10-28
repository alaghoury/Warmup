import React, { useEffect, useState } from "react";
import AuthForm from "./components/AuthForm.jsx";
import UsersTable from "./components/UsersTable.jsx";
import UsageCard from "./components/UsageCard.jsx";
import Billing from "./components/Billing.jsx";
import AnalyticsChart from "./components/AnalyticsChart.jsx";
import { isAuthed, logout } from "./lib/auth.js";
import api from "./api";

export default function App() {
  const [tab, setTab] = useState("users");
  const [health, setHealth] = useState(null);

  useEffect(() => {
    api
      .get("/health")
      .then((response) => setHealth(response.data))
      .catch(() => setHealth({ ok: false }));
  }, []);

  if (!isAuthed()) {
    return <AuthForm onSuccess={() => window.location.reload()} />;
  }

  return (
    <div style={{ padding: 16, fontFamily: "system-ui" }}>
      <header style={{ display: "flex", gap: 12, alignItems: "center" }}>
        <h1>Warmup SaaS</h1>
        <span style={{ color: health?.ok ? "green" : "red" }}>
          API: {health?.ok ? "OK" : "Down"}
        </span>
        <nav style={{ display: "flex", gap: 8 }}>
          {["users", "usage", "billing", "analytics"].map((key) => (
            <button
              key={key}
              onClick={() => setTab(key)}
              disabled={tab === key}
              style={{ textTransform: "capitalize" }}
            >
              {key}
            </button>
          ))}
        </nav>
        <div style={{ marginLeft: "auto" }}>
          <button
            onClick={() => {
              logout();
              window.location.reload();
            }}
          >
            Logout
          </button>
        </div>
      </header>

      <main style={{ marginTop: 16 }}>
        {tab === "users" && <UsersTable />}
        {tab === "usage" && <UsageCard />}
        {tab === "billing" && <Billing />}
        {tab === "analytics" && <AnalyticsChart />}
      </main>
    </div>
  );
}
