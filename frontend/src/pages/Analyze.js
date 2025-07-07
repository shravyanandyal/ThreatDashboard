import React, { useState } from 'react';
import axios from 'axios';

function Analyze() {
  const [desc, setDesc] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleAnalyze = () => {
    if (!desc.trim()) return;
    setLoading(true);
    setError(null);
    setResult(null);

    axios.post('http://localhost:5050/api/analyze', { description: desc })
      .then(res => {
        setResult(res.data.predicted_category);
      })
      .catch(err => {
        console.error(err);
        setError(err.response?.data?.error || "Unknown error");
      })
      .finally(() => setLoading(false));
  };

  return (
    <div>
      <h2>Analyze New Threat</h2>
      <textarea
        rows="6"
        cols="60"
        value={desc}
        onChange={e => setDesc(e.target.value)}
        placeholder="Paste a threat description here..."
      />
      <br />
      <button onClick={handleAnalyze} disabled={loading || !desc.trim()}>
        {loading ? "Analyzing…" : "Analyze"}
      </button>

      {result && (
        <div style={{ marginTop: "20px" }}>
          <strong>Predicted Category:</strong> {result}
        </div>
      )}
      {error && (
        <div style={{ marginTop: "20px", color: "red" }}>
          Error: {error}
        </div>
      )}
    </div>
  );
}

export default Analyze;
