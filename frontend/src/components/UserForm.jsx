import { useState } from "react";

function UserForm({ onSubmit, loading }) {
  const [form, setForm] = useState({ name: "", email: "" });
  const [status, setStatus] = useState("");

  const handleChange = (event) => {
    const { name, value } = event.target;
    setForm((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    setStatus("");
    if (!form.name.trim() || !form.email.trim()) {
      setStatus("Please provide both name and email");
      return;
    }
    const ok = await onSubmit({
      name: form.name.trim(),
      email: form.email.trim(),
    });
    if (ok) {
      setForm({ name: "", email: "" });
      setStatus("User added successfully");
    }
  };

  return (
    <form className="user-form" onSubmit={handleSubmit}>
      <div className="fields">
        <input
          type="text"
          name="name"
          placeholder="Name"
          value={form.name}
          onChange={handleChange}
          disabled={loading}
        />
        <input
          type="email"
          name="email"
          placeholder="Email"
          value={form.email}
          onChange={handleChange}
          disabled={loading}
        />
      </div>
      <button type="submit" disabled={loading}>
        {loading ? "Saving..." : "Add User"}
      </button>
      {status && <p className="status">{status}</p>}
    </form>
  );
}

export default UserForm;
