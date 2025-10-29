import React, { useEffect, useState } from "react";
import api from "../api/client";
import UsersTable from "./UsersTable";
import UsageCard from "./UsageCard";
import Billing from "./Billing";
import AnalyticsChart from "./AnalyticsChart";

export interface CurrentUser {
  id: number;
  email: string;
  name: string;
  is_active: boolean;
}

interface DashboardProps {
  user: CurrentUser;
  onLogout: () => void;
}

type TabKey = "users" | "usage" | "billing" | "analytics";

const Dashboard: React.FC<DashboardProps> = ({ user, onLogout }) => {
  const [activeTab, setActiveTab] = useState<TabKey>("users");
  const [health, setHealth] = useState<boolean | null>(null);

  useEffect(() => {
    const checkHealth = async () => {
      try {
        const response = await api.get<{ ok: boolean }>("/health");
        setHealth(response.data.ok);
      } catch (err) {
        console.error("Health check failed", err);
        setHealth(false);
      }
    };

    checkHealth();
  }, []);

  return (
    <div className="dashboard">
      <header className="dashboard__header">
        <div>
          <h1>Warmup SaaS</h1>
          <p className="dashboard__subtitle">
            Signed in as <strong>{user.name}</strong> ({user.email})
          </p>
        </div>
        <div className="dashboard__status">
          API: <span className={health ? "status-ok" : "status-fail"}>{health ? "Online" : "Offline"}</span>
        </div>
        <button className="dashboard__logout" onClick={onLogout}>
          Logout
        </button>
      </header>
      <nav className="dashboard__tabs">
        {(["users", "usage", "billing", "analytics"] as TabKey[]).map((tab) => (
          <button
            key={tab}
            className={tab === activeTab ? "tab tab--active" : "tab"}
            onClick={() => setActiveTab(tab)}
          >
            {tab.charAt(0).toUpperCase() + tab.slice(1)}
          </button>
        ))}
      </nav>
      <main className="dashboard__content">
        {activeTab === "users" && <UsersTable />}
        {activeTab === "usage" && <UsageCard />}
        {activeTab === "billing" && <Billing />}
        {activeTab === "analytics" && <AnalyticsChart />}
      </main>
    </div>
  );
};

export default Dashboard;
