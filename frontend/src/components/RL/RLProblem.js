import React, { useState, useEffect } from 'react';
import { generateRLProblem, evaluateRLAnswer } from '../../api/apiService';
import './RL.css';

function RLProblem({ autoGenerate = false, seed = null }) {
    const [problem, setProblem] = useState(null);
    
    // Config State
    const [config, setConfig] = useState({
        type: 'value_iteration',
        rows: 3,
        cols: 4,
        gamma: 0.9,
        randomGamma: true,
        step_reward: -0.04,
        randomStepReward: true,
        alpha: 0.1,
        randomAlpha: true
    });

    // MEMENTO PATTERN: Save config used for generation to reconstruct state during evaluation
    const [lastGenConfig, setLastGenConfig] = useState(null);

    const [userAnswer, setUserAnswer] = useState('');
    const [evaluation, setEvaluation] = useState(null);
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState(null);

    const handleGenerate = async () => {
        setIsLoading(true);
        setError(null);
        setEvaluation(null);
        setProblem(null);
        setUserAnswer('');

        try {
            // FIX: Ensure we always send numbers, never null, to satisfy Pydantic schema
            const payload = {
                seed: seed ?? Math.floor(Math.random() * 1_000_000),
                type: config.type,
                rows: parseInt(config.rows),
                cols: parseInt(config.cols),

                // Use the value from config, or a default fallback if empty. 
                // The backend ignores this specific value if random_gamma is true.
                gamma: parseFloat(config.gamma) || 0.9,
                random_gamma: config.randomGamma,

                step_reward: parseFloat(config.step_reward) || -0.04,
                random_step_reward: config.randomStepReward,

                alpha: parseFloat(config.alpha) || 0.1,
                random_alpha: config.randomAlpha
            };

            const res = await generateRLProblem(payload);
            setProblem(res.data);

            // Extract generated values to save for evaluation reconstruction
            let usedGamma = 0.9;
            let usedStepReward = -0.04;
            let usedAlpha = 0.1;

            // Values are returned in different structures depending on problem type
            if (res.data.grid) {
                usedGamma = res.data.grid.gamma;
                usedStepReward = res.data.grid.step_reward;
            } else if (res.data.q_data) {
                usedGamma = res.data.q_data.gamma;
                usedAlpha = res.data.q_data.alpha;
            }

            setLastGenConfig({
                type: config.type,
                rows: config.rows,
                cols: config.cols,
                gamma: usedGamma,
                step_reward: usedStepReward,
                alpha: usedAlpha
            });

        } catch (err) {
            console.error(err);
            setError("Eroare la generare. Verifică conexiunea cu serverul.");
        } finally {
            setIsLoading(false);
        }
    };

    useEffect(() => {
        if (autoGenerate) {
            handleGenerate();
        }
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [autoGenerate]);

    const handleEvaluate = async () => {
        if (!problem || userAnswer === '' || !lastGenConfig) {
            setError("Introduceți o valoare numerică.");
            return;
        }

        setIsLoading(true);
        setError(null);
        setEvaluation(null);

        try {
            const payload = {
                problem_seed: problem.seed,
                problem_type: lastGenConfig.type,
                user_value: parseFloat(userAnswer),

                // Reconstruction parameters
                rows: lastGenConfig.rows,
                cols: lastGenConfig.cols,
                gamma: lastGenConfig.gamma,
                step_reward: lastGenConfig.step_reward,
                alpha: lastGenConfig.alpha
            };

            const res = await evaluateRLAnswer(payload);
            setEvaluation(res.data);
        } catch (err) {
            console.error(err);
            setError("Eroare la evaluare.");
        } finally {
            setIsLoading(false);
        }
    };

    const handleKeyPress = (e) => {
        if (e.key === 'Enter') handleEvaluate();
    };

    const getResultClass = () => {
        if (!evaluation) return '';
        if (evaluation.percentage === 100) return 'result-success';
        return 'result-fail';
    };

    // --- RENDERERS ---

    const renderGrid = () => {
        if (!problem || !problem.grid) return null;

        const { rows, cols, walls, terminals } = problem.grid;
        // Helper to check if a cell is a wall
        const isWall = (r, c) => walls.some(w => w[0] === r && w[1] === c);

        let gridRows = [];
        for (let r = 0; r < rows; r++) {
            let gridCells = [];
            for (let c = 0; c < cols; c++) {
                const coordKey = `${r},${c}`;
                let cellClass = "grid-cell";
                let content = "";

                if (isWall(r, c)) {
                    cellClass += " cell-wall";
                } else if (terminals[coordKey] !== undefined) {
                    const val = terminals[coordKey];
                    cellClass += val > 0 ? " cell-win" : " cell-lose";
                    content = val;
                } else {
                    cellClass += " cell-empty";
                }

                // Highlight target if needed (optional logic)
                if (problem.question_target === coordKey) {
                    cellClass += " cell-target";
                    content = "TARGET"; // or overlay icon
                }

                gridCells.push(
                    <td key={c} className={cellClass}>
                        <div className="cell-content">
                            <span className="cell-coord">({r},{c})</span>
                            <span className="cell-value">{content}</span>
                        </div>
                    </td>
                );
            }
            gridRows.push(<tr key={r}>{gridCells}</tr>);
        }

        return (
            <div className="grid-display">
                <table className="grid-table">
                    <tbody>{gridRows}</tbody>
                </table>
            </div>
        );
    };

    return (
        <div className="rl-container">
            <h1 className="title">Reinforcement Learning</h1>

            {/* --- CONFIG PANEL --- */}
            {!autoGenerate && (
                <div className="rl-config-panel">
                    <div className="config-group">
                        <label>Tip Problemă</label>
                        <select
                            className="styled-select"
                            value={config.type}
                            onChange={e => setConfig({ ...config, type: e.target.value })}
                        >
                            <option value="value_iteration">Value Iteration (MDP)</option>
                            <option value="q_learning">Q-Learning Update</option>
                        </select>
                    </div>

                    <div className="config-group">
                        <label>
                            <input
                                type="checkbox"
                                checked={config.randomGamma}
                                onChange={e => setConfig({ ...config, randomGamma: e.target.checked })}
                            />
                            Gamma (γ) Aleator
                        </label>
                        {!config.randomGamma && (
                            <input
                                className="styled-input"
                                type="number" step="0.1" min="0" max="1"
                                value={config.gamma}
                                onChange={e => setConfig({ ...config, gamma: e.target.value })}
                            />
                        )}
                    </div>

                    {config.type === 'value_iteration' && (
                        <div className="config-group">
                            <label>
                                <input
                                    type="checkbox"
                                    checked={config.randomStepReward}
                                    onChange={e => setConfig({ ...config, randomStepReward: e.target.checked })}
                                />
                                Living Reward Aleator
                            </label>
                            {!config.randomStepReward && (
                                <input
                                    className="styled-input"
                                    type="number" step="0.01"
                                    value={config.step_reward}
                                    onChange={e => setConfig({ ...config, step_reward: e.target.value })}
                                />
                            )}
                        </div>
                    )}

                    {config.type === 'q_learning' && (
                        <div className="config-group">
                            <label>
                                <input
                                    type="checkbox"
                                    checked={config.randomAlpha}
                                    onChange={e => setConfig({ ...config, randomAlpha: e.target.checked })}
                                />
                                Alpha (α) Aleator
                            </label>
                            {!config.randomAlpha && (
                                <input
                                    className="styled-input"
                                    type="number" step="0.1" min="0" max="1"
                                    value={config.alpha}
                                    onChange={e => setConfig({ ...config, alpha: e.target.value })}
                                />
                            )}
                        </div>
                    )}

                    <button className="generate-btn" onClick={handleGenerate} disabled={isLoading}>
                        {isLoading ? "Se generează..." : "Generează Problemă"}
                    </button>
                </div>
            )}

            {error && <p className="error-message">{error}</p>}

            {/* --- WORKSPACE --- */}
            {problem && (
                <div className="game-workspace">
                    <div className="description-section">
                        <h3>{problem.text.title}</h3>
                        <p className="instruction" style={{ whiteSpace: "pre-line" }}>
                            {problem.text.description}
                        </p>
                        
                        {/* Only render Grid if it's Value Iteration */}
                        {problem.grid && renderGrid()}

                        <p className="instruction-req">
                            {problem.text.requirement}
                        </p>
                    </div>

                    <div className="answer-form">
                        <div className="form-group">
                            <label>Răspunsul tău (numeric):</label>
                            <input
                                type="number"
                                step="0.0001"
                                value={userAnswer}
                                onChange={(e) => setUserAnswer(e.target.value)}
                                onKeyPress={handleKeyPress}
                                placeholder="ex: 0.85"
                            />
                        </div>
                        <button className="submit-btn" onClick={handleEvaluate} disabled={isLoading}>
                            Evaluează
                        </button>
                    </div>
                </div>
            )}

            {/* --- EVALUATION RESULTS --- */}
            {evaluation && (
                <div className={`evaluation-result ${getResultClass()}`}>
                    <h2>Rezultat Evaluare</h2>
                    <div className="score-badge">{evaluation.percentage}%</div>
                    <p className="explanation"><strong>Explicație:</strong> {evaluation.explanation}</p>
                    
                    {evaluation.percentage < 100 && (
                        <p>
                            <strong>Valoarea Corectă:</strong> {evaluation.correct_value}
                        </p>
                    )}
                </div>
            )}
        </div>
    );
}

export default RLProblem;