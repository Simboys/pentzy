import { useEffect, useState } from "react";
import API from "../api/api";

export default function Findings() {
  const [findings, setFindings] = useState([]);

  useEffect(() => {
    API.get("/findings").then((res) => setFindings(res.data));
  }, []);

  return (
    <table border="1">
      <thead>
        <tr>
          <th>CVE</th>
          <th>Severity</th>
          <th>Asset</th>
          <th>Tool</th>
        </tr>
      </thead>
      <tbody>
        {findings.map((f) => (
          <tr key={f.id}>
            <td>{f.cve_id}</td>
            <td>{f.severity}</td>
            <td>{f.asset}</td>
            <td>{f.tool}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}
