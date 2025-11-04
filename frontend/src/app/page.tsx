"use client";
import { useState } from "react";
import { fetchFromAPI } from "@/lib/api";

export default function HomePage() {
  const [status, setStatus] = useState("Click to ping API");

  async function ping() {
    try {
      const data = await fetchFromAPI("/");
      setStatus(JSON.stringify(data));
    } catch (err: any) {
      setStatus(err.message);
    }
  }

  return (
    <main className="p-6">
      <h1 className="text-xl font-bold">Warmup SaaS</h1>
      <button
        onClick={ping}
        className="mt-4 bg-blue-600 text-white px-4 py-2 rounded"
      >
        Ping Backend
      </button>
      <p className="mt-4">{status}</p>
    </main>
  );
}
