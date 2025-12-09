import React, { useState } from "react";
import "./NQueens.css";

import {
  generateNQueensProblem,
  evaluateNQueensAnswer,
} from "../../api/apiService";

function NQueensProblem() {
  const [problem, setProblem] = useState(null);
  const [input, setInput] = useState("");
  const [evaluation, setEvaluation] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleGenerate = async () => {
    setLoading(true);
    setEvaluation(null);

    try {
      const response = await generateNQueensProblem();
      setProblem(response.data);
    } catch (err) {
      console.error("Eroare generare:", err);
    } finally {
      setLoading(false);
    }
  };

  const handleEvaluate = async () => {
    if (!problem || !input.trim()) return;

    const config = input
      .split(",")
      .map((x) => parseInt(x.trim(), 10))
      .filter((x) => !isNaN(x));

    const payload = {
      problem_seed: problem.seed,
      configuration: config,
    };

    setLoading(true);
    try {
      const response = await evaluateNQueensAnswer(payload);
      setEvaluation(response.data);
    } catch (err) {
      console.error("Eroare evaluare:", err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="nqueens-container">

      {/* CONTROL PANEL */}
      <div className="control-panel">
        <h1>N-Queens</h1>

        <button className="generate-btn" onClick={handleGenerate} disabled={loading}>
          {loading ? "Se generează..." : "Generează Problemă"}
        </button>
      </div>

      {/* PROBLEM CARD */}
      {problem && (
        <div className="problem-card">
          <h3>Problemă generată:</h3>
          <p className="problem-description">{problem.board_description}</p>
          <p><b>N = {problem.n}</b></p>
        </div>
      )}

      {/* SOLUTION INPUT */}
      {problem && (
        <div className="problem-card">
          <h3>Introduceți soluția (ex: 0,2,4,1,3)</h3>
          <input
            className="solution-input"
            type="text"
            value={input}
            placeholder="0,2,4,1,3"
            onChange={(e) => setInput(e.target.value)}
          />
          <button className="evaluate-btn" onClick={handleEvaluate} disabled={loading}>
            {loading ? "Se evaluează..." : "Evaluează"}
          </button>
        </div>
      )}

      {/* EVALUATION CARD */}
      {evaluation && (
        <div
          className={
            "evaluation-card " +
            (evaluation.percentage === 100
              ? "result-success"
              : evaluation.percentage === 0
                ? "result-fail"
                : "result-partial")
          }
        >
          <h2>Scor: {evaluation.percentage}%</h2>
          <p>{evaluation.explanation}</p>

          {evaluation.percentage < 100 && (
            <p>
              <b>Soluția corectă:</b>{" "}
              {evaluation.correct_answer.solution.join(", ")}
            </p>
          )}
        </div>
      )}

    </div>
  );
}

export default NQueensProblem;
