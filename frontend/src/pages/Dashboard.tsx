import { useState } from "react";
import AnalyticsChart from "../components/AnalyticsChart";
import Billing from "../components/Billing";
import UsageCard from "../components/UsageCard";
import UsersTable from "../components/UsersTable";
import AdminPanel from "../components/AdminPanel";
import { logout } from "../lib/api";

interface DashboardProps {
  currentUser: any;
  onLogout: () => void;
  onNotify: (message: string, tone?: "success" | "error") => void;
}

const baseTabs = [
  { key: "users", label: "Users" },
  { key: "usage", label: "Usage" },
  { key: "billing", label: "Billing" },
  { key: "analytics", label: "Analytics" },
];

export default function Dashboard({ currentUser, onLogout, onNotify }: DashboardProps) {
  const tabs = currentUser?.is_admin
    ? [...baseTabs, { key: "admin", label: "Admin Panel" }]
    : baseTabs;
  const [activeTab, setActiveTab] = useState<string>(tabs[0].key);

  const handleLogout = () => {
    logout();
    onLogout();
  };

  return (
    <div className="mx-auto flex min-h-screen max-w-6xl flex-col gap-8 px-6 py-10">
      <header className="flex flex-wrap items-center gap-4 rounded-2xl bg-white p-6 shadow">
        <div className="flex flex-1 flex-col gap-1">
          <h1 className="text-2xl font-semibold text-slate-900">Warmup SaaS Dashboard</h1>
          <p className="text-sm text-slate-500">
            Signed in as <span className="font-medium text-slate-800">{currentUser?.email}</span>
            {currentUser?.is_admin ? " · Admin" : ""}
          </p>
        </div>
        <button
          type="button"
          onClick={handleLogout}
          className="rounded-lg border border-slate-200 px-4 py-2 text-sm font-semibold text-slate-600 transition hover:border-rose-500 hover:text-rose-600"
        >
          Logout
        </button>
      </header>

      <nav className="flex flex-wrap gap-3">
        {tabs.map((tab) => (
          <button
            key={tab.key}
            onClick={() => setActiveTab(tab.key)}
            className={`rounded-full px-4 py-2 text-sm font-semibold transition ${
              activeTab === tab.key
                ? "bg-indigo-600 text-white shadow"
                : "bg-white text-slate-600 shadow hover:bg-indigo-50"
            }`}
          >
            {tab.label}
          </button>
        ))}
      </nav>

      <main className="flex-1 pb-12">
        {activeTab === "users" && <UsersTable />}
        {activeTab === "usage" && <UsageCard />}
        {activeTab === "billing" && <Billing onNotify={onNotify} />}
        {activeTab === "analytics" && <AnalyticsChart />}
        {activeTab === "admin" && <AdminPanel onNotify={onNotify} />}
      </main>
    </div>
  );
}
