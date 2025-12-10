import React, { useState } from "react";
import "./Strategy.css";

import {
  generateStrategyProblem,
  evaluateStrategyAnswer,
} from "../../api/apiService";

function StrategyProblem() {
  const [problem, setProblem] = useState(null);
  const [selected, setSelected] = useState(null);
  const [evaluation, setEvaluation] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleGenerate = async () => {
    setLoading(true);
    setEvaluation(null);
    setSelected(null);

    try {
      const response = await generateStrategyProblem();
      setProblem(response.data);
    } catch (err) {
      console.error("Eroare generare:", err);
    } finally {
      setLoading(false);
    }
  };

  const handleEvaluate = async () => {
    if (!problem || !selected) return;

    const payload = {
      problem_seed: problem.seed,
      chosen_strategy: selected,   // ← FIX #1
    };

    setLoading(true);
    try {
      const response = await evaluateStrategyAnswer(payload);
      setEvaluation(response.data);
    } catch (err) {
      console.error("Eroare evaluare:", err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="strategy-container">
      <h1>Strategy Identification</h1>

      {/* --- PANEL IDENTIC CU MINMAX --- */}
      <div className="strategy-panel">
        <button className="generate-btn" onClick={handleGenerate} disabled={loading}>
          {loading ? "Se generează..." : "Generează Problemă"}
        </button>
      </div>

      {problem && (
        <div className="strategy-box">
          <h3>{problem.problem_name}</h3>
          <p>{problem.description}</p>

          <div className="options-grid">
            {problem.options.map((opt) => (
              <button
                key={opt}
                className={"opt-btn " + (selected === opt ? "selected" : "")}
                onClick={() => setSelected(opt)}
              >
                {opt}
              </button>
            ))}
          </div>

          <button className="strategy-eval-btn" onClick={handleEvaluate} disabled={loading || !selected}>
            {loading ? "Se evaluează..." : "Evaluează"}
          </button>
        </div>
      )}

      {evaluation && (
        <div className="strategy-box">
          <h2>Scor: {evaluation.percentage}%</h2>
          <p>{evaluation.explanation}</p>

          {evaluation.correct_answer && (
            <p>
              <b>Răspuns corect:</b> {evaluation.correct_answer}
            </p>
          )}
        </div>
      )}
    </div>
  );
}

export default StrategyProblem;
