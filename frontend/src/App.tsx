import React, { useEffect, useState } from "react";
import api from "./api/client";
import Dashboard, { CurrentUser } from "./components/Dashboard";
import Login from "./components/Login";
import Register from "./components/Register";
import { isAuthed, logout } from "./lib/auth";

type View = "login" | "register" | "dashboard";

const App: React.FC = () => {
  const [view, setView] = useState<View>(isAuthed() ? "dashboard" : "login");
  const [user, setUser] = useState<CurrentUser | null>(null);
  const [loadingUser, setLoadingUser] = useState(false);

  const loadCurrentUser = async () => {
    if (!isAuthed()) {
      setUser(null);
      return;
    }
    setLoadingUser(true);
    try {
      const response = await api.get<CurrentUser>("/users/me");
      setUser(response.data);
      setView("dashboard");
    } catch (err) {
      console.error("Failed to load current user", err);
      logout();
      setUser(null);
      setView("login");
    } finally {
      setLoadingUser(false);
    }
  };

  useEffect(() => {
    if (view === "dashboard" && !user && isAuthed()) {
      loadCurrentUser();
    }
  }, [view]);

  const handleAuthSuccess = async () => {
    await loadCurrentUser();
  };

  const handleLogout = () => {
    logout();
    setUser(null);
    setView("login");
  };

  if (view === "dashboard") {
    if (loadingUser || !user) {
      return <div className="loader">Loading your dashboard...</div>;
    }
    return <Dashboard user={user} onLogout={handleLogout} />;
  }

  if (view === "login") {
    return (
      <Login
        onSuccess={handleAuthSuccess}
        onSwitchToRegister={() => setView("register")}
      />
    );
  }

  return (
    <Register
      onSuccess={handleAuthSuccess}
      onSwitchToLogin={() => setView("login")}
    />
  );
};

export default App;
