import { useEffect, useState } from "react";
import { getAllUsers } from "../lib/api";

type User = {
  id: number;
  name: string;
  email: string;
  is_active: boolean;
};

export default function UsersTable() {
  const [users, setUsers] = useState<User[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const loadUsers = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await getAllUsers();
      setUsers(data);
    } catch (err) {
      console.error("Failed to load users", err);
      setError("Unable to load users right now.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadUsers();
  }, []);

  return (
    <section className="space-y-4">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-semibold text-slate-900">Team members</h3>
          <p className="text-sm text-slate-500">People invited to your workspace.</p>
        </div>
        <button
          type="button"
          onClick={loadUsers}
          disabled={loading}
          className="rounded-lg border border-slate-200 px-3 py-1.5 text-sm font-medium text-slate-600 transition hover:border-indigo-500 hover:text-indigo-600 disabled:cursor-not-allowed disabled:opacity-60"
        >
          {loading ? "Refreshing…" : "Refresh"}
        </button>
      </div>
      {error && <div className="rounded-lg bg-rose-100 px-3 py-2 text-sm text-rose-700">{error}</div>}
      <div className="overflow-hidden rounded-xl bg-white shadow">
        <table className="min-w-full divide-y divide-slate-100 text-left text-sm">
          <thead className="bg-slate-50 text-xs uppercase tracking-wide text-slate-500">
            <tr>
              <th className="px-4 py-2 font-medium">Name</th>
              <th className="px-4 py-2 font-medium">Email</th>
              <th className="px-4 py-2 font-medium">Status</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-100 bg-white">
            {users.map((user) => (
              <tr key={user.id}>
                <td className="px-4 py-2 font-medium text-slate-900">{user.name}</td>
                <td className="px-4 py-2 text-slate-600">{user.email}</td>
                <td className="px-4 py-2">
                  <span
                    className={`inline-flex items-center rounded-full px-3 py-1 text-xs font-semibold ${
                      user.is_active ? "bg-emerald-100 text-emerald-700" : "bg-slate-200 text-slate-700"
                    }`}
                  >
                    {user.is_active ? "Active" : "Inactive"}
                  </span>
                </td>
              </tr>
            ))}
            {users.length === 0 && !loading && (
              <tr>
                <td colSpan={3} className="px-4 py-8 text-center text-slate-500">
                  No users found yet.
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </section>
  );
}
