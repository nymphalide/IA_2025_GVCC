import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Navbar from './components/common/Navbar';
import MinMaxProblem from './components/MinMax/MinMaxProblem';
import NashProblem from './components/Nash/NashProblem';
import StrategyProblem from './components/Strategy/StrategyProblem';
import RLProblem from './components/RL/RLProblem';
import './App.css'; 

function App() {
  return (
    <Router>
      <div className="App">
        <Navbar />

        <div className="content-container">
          <Routes>
            {/* Default redirect to MinMax */}
            <Route path="/" element={<Navigate to="/minmax" replace />} />

            {/* Routes for each problem type */}
            <Route path="/minmax" element={<MinMaxProblem />} />
            <Route path="/nash" element={<NashProblem />} />
            <Route path="/strategy" element={<StrategyProblem />} />
            <Route path="/rl" element={<RLProblem />} />

            {/* Fallback for unknown routes */}
            <Route path="*" element={<div style={{padding: 20}}>404: Page Not Found</div>} />
          </Routes>
        </div>
      </div>
    </Router>
  );
}

export default App;
