import React from 'react';
import './Nash.css';

function NashProblem() {
    return (
        <div className="nash-container">
            <h1>Game Theory: Nash Equilibrium</h1>
            <div className="placeholder-content">
                <p>⚠️ <strong>Under Development</strong> (Livrabil 3)</p>
                <p>This module will allow you to:</p>
                <ul>
                    <li>Generate random payoff matrices (Normal Form Games).</li>
                    <li>Identify Pure Nash Equilibria.</li>
                    <li>Verify if specific coordinates represent an equilibrium.</li>
                </ul>
                <div className="mock-matrix">
                    [ Placeholder for Matrix UI ]
                </div>
            </div>
        </div>
    );
}

export default NashProblem;