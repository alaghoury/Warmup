import { FormEvent, useCallback, useEffect, useMemo, useState } from 'react';

const API_BASE = '/api/v1';

interface User {
  id: number;
  name: string;
  email: string;
}

interface Account {
  id: number;
  label: string;
  status: string;
}

interface Task {
  id: number;
  account_id: number;
  kind: string;
  state: string;
}

interface TaskCreateResponse extends Task {}

async function apiFetch<T>(url: string, options?: RequestInit): Promise<T> {
  const response = await fetch(url, {
    headers: { 'Content-Type': 'application/json', ...(options?.headers ?? {}) },
    ...options
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

  const [statusMessage, setStatusMessage] = useState<string | null>(null);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  const accountOptions = useMemo(() =>
    accounts.map((account) => ({ value: String(account.id), label: account.label })),
  [accounts]);

  const loadUsers = useCallback(async () => {
    try {
      const data = await apiFetch<User[]>(`${API_BASE}/users`);
      setUsers(data);
    } catch (error) {
      console.error(error);
      setErrorMessage('Failed to fetch users');
    }
  }, []);

  const loadAccounts = useCallback(async () => {
    try {
      const data = await apiFetch<Account[]>(`${API_BASE}/accounts`);
      setAccounts(data);
    } catch (error) {
      console.error(error);
      setErrorMessage('Failed to fetch accounts');
    }
  }, []);

  const loadTasks = useCallback(async () => {
    try {
      const data = await apiFetch<Task[]>(`${API_BASE}/tasks`);
      setTasks(data);
    } catch (error) {
      console.error(error);
      setErrorMessage('Failed to fetch tasks');
    }
  }, []);

  useEffect(() => {
    loadUsers();
    loadAccounts();
    loadTasks();
  }, [loadUsers, loadAccounts, loadTasks]);

  const handleUserSubmit = async (event: FormEvent) => {
    event.preventDefault();
    setErrorMessage(null);
    setStatusMessage(null);
    try {
      await apiFetch<User>(`${API_BASE}/users`, {
        method: 'POST',
        body: JSON.stringify({ name: userForm.name.trim(), email: userForm.email.trim() })
      });
      setUserForm({ name: '', email: '' });
      setStatusMessage('User added successfully.');
      loadUsers();
    } catch (error) {
      console.error(error);
      setErrorMessage('Failed to add user.');
    }
  };

  const handleAccountSubmit = async (event: FormEvent) => {
    event.preventDefault();
    setErrorMessage(null);
    setStatusMessage(null);
    try {
      await apiFetch<Account>(`${API_BASE}/accounts`, {
        method: 'POST',
        body: JSON.stringify({ label: accountForm.label.trim() })
      });
      setAccountForm({ label: '' });
      setStatusMessage('Account created successfully.');
      loadAccounts();
    } catch (error) {
      console.error(error);
      setErrorMessage('Failed to create account.');
    }
  };

  const handleTaskSubmit = async (event: FormEvent) => {
    event.preventDefault();
    setErrorMessage(null);
    setStatusMessage(null);

    if (!taskForm.accountId) {
      setErrorMessage('Select an account for the task.');
      return;
    }

    try {
      await apiFetch<TaskCreateResponse>(`${API_BASE}/tasks`, {
        method: 'POST',
        body: JSON.stringify({
          account_id: Number(taskForm.accountId),
          kind: taskForm.kind
        })
      });
      setTaskForm({ accountId: '', kind: 'email' });
      setStatusMessage('Task created successfully.');
      loadTasks();
    } catch (error) {
      console.error(error);
      setErrorMessage('Failed to create task.');
    }
  };

  return (
    <main>
      <h1>Warmup SaaS Control Panel</h1>
      <p>Manage your users, accounts, and warming tasks against the backend API.</p>

      {statusMessage ? <div className="success">{statusMessage}</div> : null}
      {errorMessage ? <div className="error">{errorMessage}</div> : null}

      <section>
        <h2>Users</h2>
        <form onSubmit={handleUserSubmit}>
          <label>
            Name
            <input
              value={userForm.name}
              onChange={(event) => setUserForm((prev) => ({ ...prev, name: event.target.value }))}
              placeholder="Jane Doe"
              required
            />
          </label>
          <label>
            Email
            <input
              type="email"
              value={userForm.email}
              onChange={(event) => setUserForm((prev) => ({ ...prev, email: event.target.value }))}
              placeholder="jane@example.com"
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
              <tr>
                <td colSpan={3}>No users yet.</td>
              </tr>
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
      </section>

      <section>
        <h2>Accounts</h2>
        <form onSubmit={handleAccountSubmit}>
          <label>
            Label
            <input
              value={accountForm.label}
              onChange={(event) => setAccountForm({ label: event.target.value })}
              placeholder="Primary Inbox"
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
              <tr>
                <td colSpan={3}>No accounts yet.</td>
              </tr>
            ) : (
              accounts.map((account) => (
                <tr key={account.id}>
                  <td>{account.id}</td>
                  <td>{account.label}</td>
                  <td>
                    <span className="status-tag">{account.status}</span>
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </section>

      <section>
        <h2>Warming Tasks</h2>
        <form onSubmit={handleTaskSubmit}>
          <label>
            Account
            <select
              value={taskForm.accountId}
              onChange={(event) => setTaskForm((prev) => ({ ...prev, accountId: event.target.value }))}
              required
            >
              <option value="" disabled>
                Select account
              </option>
              {accountOptions.map((option) => (
                <option key={option.value} value={option.value}>
                  {option.label}
                </option>
              ))}
            </select>
          </label>

          <label>
            Task type
            <select
              value={taskForm.kind}
              onChange={(event) => setTaskForm((prev) => ({ ...prev, kind: event.target.value }))}
            >
              <option value="email">Email</option>
              <option value="social">Social</option>
              <option value="custom">Custom</option>
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
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            {tasks.length === 0 ? (
              <tr>
                <td colSpan={4}>No tasks yet.</td>
              </tr>
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
      </section>
    </main>
  );
}
