import { useEffect, useState } from "react";
import {
  activateUser,
  deactivateUser,
  getAdminStats,
  getAdminUsers,
} from "../lib/api";

interface AdminUser {
  id: number;
  name: string;
  email: string;
  is_active: boolean;
  is_admin: boolean;
  created_at: string;
}

interface AdminPanelProps {
  onNotify: (message: string, tone?: "success" | "error") => void;
}

export default function AdminPanel({ onNotify }: AdminPanelProps) {
  const [users, setUsers] = useState<AdminUser[]>([]);
  const [stats, setStats] = useState<{ total_users: number; active_users: number; recent_signups: number } | null>(
    null,
  );
  const [loading, setLoading] = useState(false);

  const load = async () => {
    setLoading(true);
    try {
      const [usersData, statsData] = await Promise.all([getAdminUsers(), getAdminStats()]);
      setUsers(usersData);
      setStats(statsData);
    } catch (error) {
      console.error("Failed to load admin data", error);
      onNotify("Unable to load admin data", "error");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    load();
  }, []);

  const toggleUser = async (user: AdminUser) => {
    try {
      if (user.is_active) {
        await deactivateUser(user.id);
        onNotify(`Deactivated ${user.email}`, "success");
      } else {
        await activateUser(user.id);
        onNotify(`Reactivated ${user.email}`, "success");
      }
      await load();
    } catch (error) {
      console.error("Failed to toggle user", error);
      onNotify("Unable to update user status", "error");
    }
  };

  return (
    <div className="space-y-6">
      <p className="rounded-xl border border-indigo-100 bg-indigo-50 px-4 py-3 text-sm text-indigo-700 shadow">
        Manage every account in your workspace. The initial superuser defined in your environment variables is always kept
        active and promoted to admin on startup.
      </p>
      <section className="grid gap-4 sm:grid-cols-3">
        <div className="rounded-xl bg-white p-4 shadow">
          <p className="text-xs uppercase tracking-wide text-slate-500">Total users</p>
          <p className="mt-2 text-2xl font-semibold">{stats?.total_users ?? "–"}</p>
        </div>
        <div className="rounded-xl bg-white p-4 shadow">
          <p className="text-xs uppercase tracking-wide text-slate-500">Active users</p>
          <p className="mt-2 text-2xl font-semibold">{stats?.active_users ?? "–"}</p>
        </div>
        <div className="rounded-xl bg-white p-4 shadow">
          <p className="text-xs uppercase tracking-wide text-slate-500">Signups (7 days)</p>
          <p className="mt-2 text-2xl font-semibold">{stats?.recent_signups ?? "–"}</p>
        </div>
      </section>
      <div className="overflow-hidden rounded-xl bg-white shadow">
        <div className="flex items-center justify-between border-b border-slate-100 px-4 py-3">
          <h3 className="text-base font-semibold text-slate-900">Manage users</h3>
          <button
            type="button"
            onClick={load}
            className="rounded-lg border border-slate-200 px-3 py-1.5 text-sm font-medium text-slate-600 transition hover:border-indigo-500 hover:text-indigo-600"
          >
            {loading ? "Refreshing…" : "Refresh"}
          </button>
        </div>
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-slate-100 text-left text-sm">
            <thead className="bg-slate-50 text-xs uppercase tracking-wide text-slate-500">
              <tr>
                <th className="px-4 py-2 font-medium">Name</th>
                <th className="px-4 py-2 font-medium">Email</th>
                <th className="px-4 py-2 font-medium">Status</th>
                <th className="px-4 py-2 font-medium">Role</th>
                <th className="px-4 py-2 font-medium">Joined</th>
                <th className="px-4 py-2"></th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100 bg-white">
              {users.map((user) => (
                <tr key={user.id}>
                  <td className="px-4 py-2 font-medium text-slate-900">{user.name}</td>
                  <td className="px-4 py-2 text-slate-600">{user.email}</td>
                  <td className="px-4 py-2">
                    <span
                      className={`inline-flex items-center gap-2 rounded-full px-3 py-1 text-xs font-semibold ${
                        user.is_active
                          ? "bg-emerald-100 text-emerald-700"
                          : "bg-slate-200 text-slate-700"
                      }`}
                    >
                      {user.is_active ? "Active" : "Inactive"}
                    </span>
                  </td>
                  <td className="px-4 py-2 text-slate-600">{user.is_admin ? "Admin" : "Member"}</td>
                  <td className="px-4 py-2 text-slate-500">
                    {new Date(user.created_at).toLocaleDateString()}
                  </td>
                  <td className="px-4 py-2">
                    <button
                      type="button"
                      onClick={() => toggleUser(user)}
                      className="rounded-lg border border-slate-200 px-3 py-1.5 text-xs font-semibold text-slate-600 transition hover:border-indigo-500 hover:text-indigo-600"
                    >
                      {user.is_active ? "Deactivate" : "Activate"}
                    </button>
                  </td>
                </tr>
              ))}
              {users.length === 0 && !loading && (
                <tr>
                  <td colSpan={6} className="px-4 py-8 text-center text-slate-500">
                    No users found yet.
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
