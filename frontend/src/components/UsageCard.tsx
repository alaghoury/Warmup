import React, { useEffect, useState } from "react";
import api from "../api/client";

interface UsageData {
  used_api_calls: number;
  limit_api_calls: number;
  remaining_api_calls: number;
}

const UsageCard: React.FC = () => {
  const [data, setData] = useState<UsageData | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchUsage = async () => {
      try {
        const response = await api.get<UsageData>("/subscriptions/usage");
        setData(response.data);
      } catch (err) {
        console.error("Failed to load usage", err);
        setError("Unable to load usage metrics.");
      }
    };

    fetchUsage();
  }, []);

  if (error) {
    return <div style={{ color: "red" }}>{error}</div>;
  }

  if (!data) {
    return <div>Loading usage...</div>;
  }

  return (
    <section>
      <h3>Usage</h3>
      <p>
        API calls: {data.used_api_calls} / {data.limit_api_calls} (remaining {" "}
        {data.remaining_api_calls})
      </p>
      <progress max={data.limit_api_calls} value={data.used_api_calls} />
    </section>
  );
};

export default UsageCard;
