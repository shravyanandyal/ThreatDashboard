import React, { useEffect, useState } from 'react';
import axios from 'axios';

function Dashboard() {
  const [stats, setStats] = useState({
    total_threats: 0,
    category_counts: [],
    severity_counts: []
  });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    axios.get('http://localhost:5050/api/threats/stats')
      .then(res => {
        setStats(res.data);
        setLoading(false);
      })
      .catch(err => {
        console.error("Failed to fetch stats", err);
        setLoading(false);
      });
  }, []);

  return (
    <div>
      <h2>Dashboard</h2>
      {loading ? (
        <p>Loading...</p>
      ) : (
        <>
          <p><strong>Total Threats:</strong> {stats.total_threats}</p>

          <h4>By Category:</h4>
          <ul>
            {stats.category_counts.map((item, idx) => (
              <li key={idx}>{item._id}: {item.count}</li>
            ))}
          </ul>

          <h4>By Severity:</h4>
          <ul>
            {stats.severity_counts.map((item, idx) => (
              <li key={idx}>Severity {item._id}: {item.count}</li>
            ))}
          </ul>
        </>
      )}
    </div>
  );
}

export default Dashboard;
