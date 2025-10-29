import React, { useEffect, useState } from "react";
import api from "../api/client";

type User = {
  id: number;
  name: string;
  email: string;
};

const UsersTable: React.FC = () => {
  const [users, setUsers] = useState<User[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const loadUsers = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await api.get<User[]>("/users");
      setUsers(response.data);
    } catch (err) {
      console.error("Failed to load users", err);
      setError("Unable to load users. Please try again later.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadUsers();
  }, []);

  return (
    <section>
      <header style={{ display: "flex", alignItems: "center", gap: 12 }}>
        <h3 style={{ margin: 0 }}>Users</h3>
        <button onClick={loadUsers} disabled={loading}>
          {loading ? "Refreshing..." : "Refresh"}
        </button>
      </header>
      {error && <div style={{ color: "red", marginTop: 8 }}>{error}</div>}
      <table
        style={{ width: "100%", borderCollapse: "collapse", marginTop: 12 }}
      >
        <thead>
          <tr>
            <th style={{ borderBottom: "1px solid #ddd", textAlign: "left" }}>
              ID
            </th>
            <th style={{ borderBottom: "1px solid #ddd", textAlign: "left" }}>
              Name
            </th>
            <th style={{ borderBottom: "1px solid #ddd", textAlign: "left" }}>
              Email
            </th>
          </tr>
        </thead>
        <tbody>
          {users.map((user) => (
            <tr key={user.id}>
              <td style={{ padding: "6px 4px" }}>{user.id}</td>
              <td style={{ padding: "6px 4px" }}>{user.name}</td>
              <td style={{ padding: "6px 4px" }}>{user.email}</td>
            </tr>
          ))}
          {users.length === 0 && !loading && (
            <tr>
              <td colSpan={3} style={{ padding: "8px", textAlign: "center" }}>
                No users found yet.
              </td>
            </tr>
          )}
        </tbody>
      </table>
    </section>
  );
};

export default UsersTable;
