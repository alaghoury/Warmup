import React, { useEffect, useState } from "react";
import api from "../api.js";

export default function UsersTable() {
  const [users, setUsers] = useState([]);
  const [error, setError] = useState("");

  async function load() {
    try {
      const response = await api.get("/users");
      setUsers(response.data);
    } catch (err) {
      console.error(err);
      setError("Failed to load users");
    }
  }

  useEffect(() => {
    load();
  }, []);

  return (
    <div>
      <h3>Users</h3>
      {error && <div style={{ color: "red" }}>{error}</div>}
      <table border="1" cellPadding="6">
        <thead>
          <tr>
            <th>ID</th>
            <th>Name</th>
            <th>Email</th>
          </tr>
        </thead>
        <tbody>
          {users.map((user) => (
            <tr key={user.id}>
              <td>{user.id}</td>
              <td>{user.name}</td>
              <td>{user.email}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
