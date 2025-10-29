import React, { useEffect, useState } from "react";
import api from "../api/client";

interface AnalyticsSummary {
  total_users: number;
  total_api_calls: number;
}

const AnalyticsChart: React.FC = () => {
  const [data, setData] = useState<AnalyticsSummary | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchSummary = async () => {
      try {
        const response = await api.get<AnalyticsSummary>("/analytics/summary");
        setData(response.data);
      } catch (err) {
        console.error("Failed to load analytics", err);
        setError("Unable to load analytics summary.");
      }
    };

    fetchSummary();
  }, []);

  if (error) {
    return <div style={{ color: "red" }}>{error}</div>;
  }

  if (!data) {
    return <div>Loading analytics...</div>;
  }

  return (
    <section>
      <h3>Analytics</h3>
      <p>Total users: {data.total_users}</p>
      <p>Total API calls: {data.total_api_calls}</p>
    </section>
  );
};

export default AnalyticsChart;
