import React from "react";

export default function Dashboard() {
  const name = localStorage.getItem("user") || "Mohammed";
  return (
    <div className="text-center">
      <h1 className="text-3xl font-bold text-gray-800 mb-4">Welcome, {name} 👋</h1>
      <p className="text-gray-600">You’re now connected to the Warmup App backend successfully.</p>
    </div>
  );
}
