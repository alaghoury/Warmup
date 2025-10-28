import { useCallback, useEffect, useState } from "react";
import axios from "axios";
import UserForm from "./components/UserForm.jsx";
import UserList from "./components/UserList.jsx";

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL ?? "http://127.0.0.1:8000",
});

function App() {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const fetchUsers = useCallback(async () => {
    setLoading(true);
    setError("");
    try {
      const { data } = await api.get("/users");
      setUsers(data);
    } catch (err) {
      console.error(err);
      setError("Failed to load users");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchUsers();
  }, [fetchUsers]);

  const handleAdd = async (payload) => {
    setError("");
    try {
      await api.post("/users", payload);
      fetchUsers();
      return true;
    } catch (err) {
      if (err.response?.status === 409) {
        setError("Email already exists");
      } else {
        setError("Failed to add user");
      }
      return false;
    }
  };

  const handleDelete = async (id) => {
    setError("");
    try {
      await api.delete(`/users/${id}`);
      setUsers((prev) => prev.filter((user) => user.id !== id));
    } catch (err) {
      console.error(err);
      setError("Failed to delete user");
    }
  };

  return (
    <div className="app">
      <header>
        <h1>Warmup App</h1>
        <p>Manage users stored in the FastAPI backend.</p>
      </header>

      <section className="panel">
        <UserForm onSubmit={handleAdd} loading={loading} />
      </section>

      <section className="panel">
        <div className="panel-header">
          <h2>Users</h2>
          <button type="button" onClick={fetchUsers} disabled={loading}>
            Refresh
          </button>
        </div>
        {error && <p className="error">{error}</p>}
        <UserList
          users={users}
          loading={loading}
          onDelete={handleDelete}
        />
      </section>
    </div>
  );
}

export default App;
