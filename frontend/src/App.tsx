import { FormEvent, useEffect, useState } from 'react';

const API_BASE = '/api/v1';

type User = { id: number; name: string; email: string };
type Account = { id: number; label: string; status: string };
type Task = { id: number; account_id: number; kind: string; state: string };

async function fetchJson<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(path, {
    headers: { 'Content-Type': 'application/json', ...(init?.headers ?? {}) },
    ...init
  });

  if (!response.ok) {
    const text = await response.text();
    throw new Error(text || response.statusText);
  }

  return response.json() as Promise<T>;
}

export default function App() {
  const [users, setUsers] = useState<User[]>([]);
  const [accounts, setAccounts] = useState<Account[]>([]);
  const [tasks, setTasks] = useState<Task[]>([]);

  const [userForm, setUserForm] = useState({ name: '', email: '' });
  const [accountForm, setAccountForm] = useState({ label: '' });
  const [taskForm, setTaskForm] = useState({ accountId: '', kind: 'email' });

  const [error, setError] = useState<string | null>(null);
  const [notice, setNotice] = useState<string | null>(null);

  useEffect(() => {
    Promise.all([
      fetchJson<User[]>(`${API_BASE}/users`).then(setUsers),
      fetchJson<Account[]>(`${API_BASE}/accounts`).then(setAccounts),
      fetchJson<Task[]>(`${API_BASE}/tasks`).then(setTasks)
    ]).catch((err) => {
      console.error(err);
      setError('Failed to load initial data. Ensure the backend is running.');
    });
  }, []);

  const handleUserSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setError(null);
    setNotice(null);

    try {
      const payload = { name: userForm.name.trim(), email: userForm.email.trim() };
      const created = await fetchJson<User>(`${API_BASE}/users`, {
        method: 'POST',
        body: JSON.stringify(payload)
      });
      setUsers((prev) => [...prev, created]);
      setUserForm({ name: '', email: '' });
      setNotice('User added successfully.');
    } catch (err) {
      console.error(err);
      setError('Unable to create user.');
    }
  };

  const handleAccountSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setError(null);
    setNotice(null);

    try {
      const payload = { label: accountForm.label.trim() };
      const created = await fetchJson<Account>(`${API_BASE}/accounts`, {
        method: 'POST',
        body: JSON.stringify(payload)
      });
      setAccounts((prev) => [...prev, created]);
      setAccountForm({ label: '' });
      setNotice('Account created successfully.');
    } catch (err) {
      console.error(err);
      setError('Unable to create account.');
    }
  };

  const handleTaskSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setError(null);
    setNotice(null);

    if (!taskForm.accountId) {
      setError('Please choose an account.');
      return;
    }

    try {
      const payload = {
        account_id: Number(taskForm.accountId),
        kind: taskForm.kind
      };
      const created = await fetchJson<Task>(`${API_BASE}/tasks`, {
        method: 'POST',
        body: JSON.stringify(payload)
      });
      setTasks((prev) => [...prev, created]);
      setTaskForm({ accountId: '', kind: 'email' });
      setNotice('Task created successfully.');
    } catch (err) {
      console.error(err);
      setError('Unable to create task.');
    }
  };

  return (
    <main className="layout">
      <header>
        <h1>Warmup SaaS</h1>
        <p>Interact with the FastAPI backend through a simple dashboard.</p>
      </header>

      {error ? <div className="alert error">{error}</div> : null}
      {notice ? <div className="alert success">{notice}</div> : null}

      <section className="panels">
        <article>
          <h2>Users</h2>
          <p>List and create users via the backend API.</p>
          <form onSubmit={handleUserSubmit}>
            <label>
              Name
              <input
                value={userForm.name}
                onChange={(event) => setUserForm((prev) => ({ ...prev, name: event.target.value }))}
                required
              />
            </label>
            <label>
              Email
              <input
                type="email"
                value={userForm.email}
                onChange={(event) => setUserForm((prev) => ({ ...prev, email: event.target.value }))}
                required
              />
            </label>
            <button type="submit">Add user</button>
          </form>
          <table>
            <thead>
              <tr>
                <th>ID</th>
                <th>Name</th>
                <th>Email</th>
              </tr>
            </thead>
            <tbody>
              {users.length === 0 ? (
                <tr><td colSpan={3}>No users found.</td></tr>
              ) : (
                users.map((user) => (
                  <tr key={user.id}>
                    <td>{user.id}</td>
                    <td>{user.name}</td>
                    <td>{user.email}</td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </article>

        <article>
          <h2>Accounts</h2>
          <p>Keep track of warmup accounts.</p>
          <form onSubmit={handleAccountSubmit}>
            <label>
              Label
              <input
                value={accountForm.label}
                onChange={(event) => setAccountForm({ label: event.target.value })}
                required
              />
            </label>
            <button type="submit">Create account</button>
          </form>
          <table>
            <thead>
              <tr>
                <th>ID</th>
                <th>Label</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody>
              {accounts.length === 0 ? (
                <tr><td colSpan={3}>No accounts found.</td></tr>
              ) : (
                accounts.map((account) => (
                  <tr key={account.id}>
                    <td>{account.id}</td>
                    <td>{account.label}</td>
                    <td>{account.status}</td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </article>

        <article>
          <h2>Warming tasks</h2>
          <p>Assign tasks to the accounts above.</p>
          <form onSubmit={handleTaskSubmit}>
            <label>
              Account
              <select
                value={taskForm.accountId}
                onChange={(event) => setTaskForm((prev) => ({ ...prev, accountId: event.target.value }))}
                required
              >
                <option value="">Select account</option>
                {accounts.map((account) => (
                  <option key={account.id} value={account.id}>
                    {account.label} (#{account.id})
                  </option>
                ))}
              </select>
            </label>
            <label>
              Kind
              <select
                value={taskForm.kind}
                onChange={(event) => setTaskForm((prev) => ({ ...prev, kind: event.target.value }))}
              >
                <option value="email">email</option>
                <option value="social">social</option>
              </select>
            </label>
            <button type="submit">Create task</button>
          </form>
          <table>
            <thead>
              <tr>
                <th>ID</th>
                <th>Account</th>
                <th>Kind</th>
                <th>State</th>
              </tr>
            </thead>
            <tbody>
              {tasks.length === 0 ? (
                <tr><td colSpan={4}>No tasks found.</td></tr>
              ) : (
                tasks.map((task) => (
                  <tr key={task.id}>
                    <td>{task.id}</td>
                    <td>{task.account_id}</td>
                    <td>{task.kind}</td>
                    <td>{task.state}</td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </article>
      </section>
    </main>
  );
}
