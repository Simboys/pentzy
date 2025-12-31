import { useEffect, useState } from "react";
import API from "../api/api";

export default function Dashboard() {
  const [data, setData] = useState({});

  useEffect(() => {
    API.get("/dashboard/summary")
      .then((res) => setData(res.data))
      .catch(() => window.location.href = "/");
  }, []);

  return (
    <div>
      <h2>Dashboard</h2>
      <p>Total Findings: {data.total_findings}</p>
      <p>Critical: {data.critical}</p>
      <p>High: {data.high}</p>
    </div>
  );
}
