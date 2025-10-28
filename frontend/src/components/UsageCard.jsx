import React, { useEffect, useState } from "react";
import api from "../api.js";

export default function UsageCard() {
  const [usage, setUsage] = useState(null);
  const [error, setError] = useState("");

  useEffect(() => {
    api
      .get("/subscriptions/usage")
      .then((response) => setUsage(response.data))
      .catch((err) => {
        console.error(err);
        setError("Failed to load usage data");
      });
  }, []);

  if (error) {
    return <div style={{ color: "red" }}>{error}</div>;
  }

  if (!usage) {
    return <div>Loading usage...</div>;
  }

  return (
    <div>
      <h3>Usage</h3>
      <p>
        API calls: {usage.used_api_calls} / {usage.limit_api_calls} (remaining {" "}
        {usage.remaining_api_calls})
      </p>
      <progress max={usage.limit_api_calls} value={usage.used_api_calls}></progress>
    </div>
  );
}
