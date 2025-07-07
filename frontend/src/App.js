import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import Dashboard from './pages/Dashboard';
import Threats from './pages/Threats';
import Analyze from './pages/Analyze';

function App() {
  return (
    <Router>
      <div style={{ padding: '20px' }}>
        <h1>Threat Intelligence Dashboard</h1>
        <nav>
          <Link to="/">Dashboard</Link> |{" "}
          <Link to="/threats">Threats</Link> |{" "}
          <Link to="/analyze">Analyze</Link>
        </nav>
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/threats" element={<Threats />} />
          <Route path="/analyze" element={<Analyze />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
