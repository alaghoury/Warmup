import React, { useEffect, useState } from "react";
import api from "../api.js";

export default function AnalyticsChart() {
  const [data, setData] = useState(null);
  const [error, setError] = useState("");

  useEffect(() => {
    api
      .get("/analytics/summary")
      .then((response) => setData(response.data))
      .catch((err) => {
        console.error(err);
        setError("Failed to load analytics");
      });
  }, []);

  if (error) {
    return <div style={{ color: "red" }}>{error}</div>;
  }

  if (!data) {
    return <div>Loading…</div>;
  }

  return (
    <div>
      <h3>Analytics</h3>
      <p>Total users: {data.total_users}</p>
      <p>Total API calls: {data.total_api_calls}</p>
    </div>
  );
}
