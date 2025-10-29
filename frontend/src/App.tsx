import { useEffect, useState } from "react";
import Dashboard from "./pages/Dashboard";
import Login from "./pages/Login";
import Register from "./pages/Register";
import { getCurrentUser } from "./lib/api";
import { getToken } from "./lib/auth";

type View = "login" | "register" | "dashboard";

type ToastState = {
  message: string;
  tone: "success" | "error";
};

export default function App() {
  const [view, setView] = useState<View>(getToken() ? "dashboard" : "login");
  const [currentUser, setCurrentUser] = useState<any | null>(null);
  const [loadingUser, setLoadingUser] = useState(false);
  const [toast, setToast] = useState<ToastState | null>(null);

  const showToast = (message: string, tone: "success" | "error" = "success") => {
    setToast({ message, tone });
    setTimeout(() => setToast(null), 3000);
  };

  const loadUser = async () => {
    if (!getToken()) {
      setCurrentUser(null);
      return;
    }
    setLoadingUser(true);
    try {
      const data = await getCurrentUser();
      setCurrentUser(data);
      setView("dashboard");
    } catch (error) {
      console.error("Failed to load current user", error);
      setCurrentUser(null);
      setView("login");
    } finally {
      setLoadingUser(false);
    }
  };

  useEffect(() => {
    if (view === "dashboard" && getToken() && !currentUser) {
      loadUser();
    }
  }, [view]);

  const handleAuthenticated = (user: any) => {
    setCurrentUser(user);
    setView("dashboard");
  };

  const handleLogout = () => {
    setCurrentUser(null);
    setView("login");
    showToast("Logged out", "success");
  };

  return (
    <div className="min-h-screen bg-slate-100">
      {toast && (
        <div
          className={`fixed inset-x-0 top-4 mx-auto w-fit rounded-full px-4 py-2 text-sm font-medium shadow-lg transition ${
            toast.tone === "success" ? "bg-emerald-500 text-white" : "bg-rose-500 text-white"
          }`}
        >
          {toast.message}
        </div>
      )}
      {view === "dashboard" ? (
        loadingUser || !currentUser ? (
          <div className="flex min-h-screen items-center justify-center text-slate-500">
            Loading dashboard…
          </div>
        ) : (
          <Dashboard currentUser={currentUser} onLogout={handleLogout} onNotify={showToast} />
        )
      ) : view === "login" ? (
        <div className="flex min-h-screen items-center justify-center bg-gradient-to-br from-indigo-100 via-white to-slate-100 px-6 py-10">
          <Login
            onAuthenticated={(user) => handleAuthenticated(user)}
            onSwitchToRegister={() => setView("register")}
            onError={(message) => showToast(message, "error")}
            onSuccess={(message) => showToast(message, "success")}
          />
        </div>
      ) : (
        <div className="flex min-h-screen items-center justify-center bg-gradient-to-br from-indigo-100 via-white to-slate-100 px-6 py-10">
          <Register
            onAuthenticated={(user) => handleAuthenticated(user)}
            onSwitchToLogin={() => setView("login")}
            onError={(message) => showToast(message, "error")}
            onSuccess={(message) => showToast(message, "success")}
          />
        </div>
      )}
    </div>
  );
}
