import React, {useState, useEffect} from 'react';
import {generateRLProblem, evaluateRLAnswer} from '../../api/apiService';
import './RL.css';

function RLProblem({autoGenerate = false, seed = null}) {
    const [problem, setProblem] = useState(null);
    const [config, setConfig] = useState({
        type: 'value_iteration', // 'value_iteration' or 'q_learning'
        rows: 3,
        cols: 4,
        gamma: 0.9,
        step_reward: -0.04,
        alpha: 0.1 // Adăugat explicit în state pentru consistență
    });
    const [userAnswer, setUserAnswer] = useState('');
    const [evaluation, setEvaluation] = useState(null);
    const [isLoading, setIsLoading] = useState(false);

    const handleGenerate = async () => {
        setIsLoading(true);
        setEvaluation(null);
        setProblem(null);
        setUserAnswer('');

        try {
            const payload = {
                seed: seed ?? Math.floor(Math.random() * 1_000_000),

                // dacă suntem în test → random by default
                type: autoGenerate ? 'value_iteration' : config.type,

                rows: autoGenerate ? undefined : config.rows,
                cols: autoGenerate ? undefined : config.cols,
                gamma: autoGenerate ? undefined : config.gamma,
                step_reward: autoGenerate ? undefined : config.step_reward,
                alpha: autoGenerate ? undefined : config.alpha,
            };

            const res = await generateRLProblem(payload);

            setProblem(res.data);
        } catch (err) {
            console.error(err);
            alert("Eroare la generare (Verifică consola)");
        } finally {
            setIsLoading(false);
        }
    };

    useEffect(() => {
        if (autoGenerate) {
            handleGenerate();
        }
    }, [autoGenerate]);


    const handleEvaluate = async () => {
        if (!problem || !userAnswer) return;

        try {
            // --- MODIFICARE AICI: Trimitem toți parametrii de fizică ---
            const payload = {
                problem_seed: problem.seed,
                problem_type: problem.problem_type, // ← CRUCIAL
                user_value: parseFloat(userAnswer),

                rows: problem.grid?.rows,
                cols: problem.grid?.cols,
                gamma: problem.grid?.gamma,
                step_reward: problem.grid?.step_reward,
                alpha: config.alpha
            };


            const res = await evaluateRLAnswer(payload);
            setEvaluation(res.data);
        } catch (err) {
            console.error(err);
            alert("Eroare la evaluare");
        }
    };

    const handleKeyPress = (e) => {
        if (e.key === 'Enter') handleEvaluate();
    };

    // Helper pt randarea grilei
    const renderGrid = () => {
        if (!problem || !problem.grid) return null;

        const {rows, cols, walls, terminals} = problem.grid;
        let gridRender = [];

        // Convert walls list to Set for O(1) lookup
        const wallsSet = new Set(walls.map(w => `${w[0]},${w[1]}`));

        for (let r = 0; r < rows; r++) {
            let rowRender = [];
            for (let c = 0; c < cols; c++) {
                const key = `${r},${c}`;
                let cellClass = "grid-cell";
                let content = "";

                if (wallsSet.has(key)) {
                    cellClass += " cell-wall";
                } else if (terminals[key]) {
                    const val = terminals[key];
                    cellClass += val > 0 ? " cell-win" : " cell-lose";
                    content = val;
                }

                rowRender.push(
                    <td key={c} className={cellClass}>
                        <span className="cell-coord">{r},{c}</span>
                        <span className="cell-value">{content}</span>
                    </td>
                );
            }
            gridRender.push(<tr key={r}>{rowRender}</tr>);
        }

        return (
            <div className="grid-display">
                <table className="grid-table">
                    <tbody>{gridRender}</tbody>
                </table>
            </div>
        );
    };

    return (
        <div className="rl-container">
            <h1 className="title">Reinforcement Learning</h1>

            {/* --- Configuration Panel --- */}
            {!autoGenerate && (
                <div className="rl-config-panel">
                    <div className="config-group">
                        <label>Tip Problemă</label>
                        <select
                            className="styled-select"
                            value={config.type}
                            onChange={e => setConfig({...config, type: e.target.value})}
                        >
                            <option value="value_iteration">Value Iteration (MDP)</option>
                            <option value="q_learning">Q-Learning Update</option>
                        </select>
                    </div>

                    {config.type === 'value_iteration' && (
                        <>
                            <div className="config-group">
                                <label>Gamma (γ)</label>
                                <input
                                    className="styled-input"
                                    type="number"
                                    step="0.1"
                                    min="0" max="1"
                                    value={config.gamma}
                                    onChange={e => setConfig({...config, gamma: parseFloat(e.target.value)})}
                                />
                            </div>
                            <div className="config-group">
                                <label>Living Reward</label>
                                <input
                                    className="styled-input"
                                    type="number"
                                    step="0.01"
                                    value={config.step_reward}
                                    onChange={e => setConfig({...config, step_reward: parseFloat(e.target.value)})}
                                />
                            </div>
                        </>
                    )}

                    {/* Optional: Add Alpha input for Q-Learning if desired, currently using default 0.1 */}
                    {config.type === 'q_learning' && (
                        <div className="config-group">
                            <label>Alpha (α)</label>
                            <input
                                className="styled-input"
                                type="number"
                                step="0.1"
                                min="0" max="1"
                                value={config.alpha}
                                onChange={e => setConfig({...config, alpha: parseFloat(e.target.value)})}
                            />
                        </div>
                    )}

                    <button className="generate-btn" onClick={handleGenerate} disabled={isLoading}>
                        {isLoading ? "Se generează..." : "Generează Problemă"}
                    </button>
                </div>
            )}

            {/* --- Main Workspace --- */}
            {problem && (
                <div className="game-workspace">
                    <h2 className="problem-title">{problem.text.title}</h2>

                    {/* Render Grid only for Value Iteration */}
                    {config.type === 'value_iteration' && renderGrid()}

                    <p className="instruction" style={{whiteSpace: 'pre-line'}}>
                        {problem.text.description}
                    </p>
                    <div className="instruction-req">
                        {problem.text.requirement}
                    </div>

                    <div className="answer-section">
                        <label style={{fontWeight: '600', color: '#555'}}>Răspunsul tău (valoare numerică):</label>
                        <div className="input-wrapper">
                            <input
                                className="answer-input"
                                type="number"
                                step="0.001"
                                placeholder="ex: 0.76"
                                value={userAnswer}
                                onChange={(e) => setUserAnswer(e.target.value)}
                                onKeyPress={handleKeyPress}
                            />
                            <button className="submit-btn" onClick={handleEvaluate}>Verifică</button>
                        </div>
                    </div>
                </div>
            )}

            {/* --- Results --- */}
            {evaluation && (
                <div className={`rl-result ${evaluation.percentage === 100 ? 'rl-success' : 'rl-fail'}`}>
                    <span className="score-badge">{evaluation.percentage}%</span>
                    <p><strong>Explicație:</strong> {evaluation.explanation}</p>
                    {evaluation.percentage < 100 && (
                        <p style={{marginTop: '10px'}}>
                            Valoarea corectă era: <strong>{evaluation.correct_value}</strong>
                        </p>
                    )}
                </div>
            )}
        </div>
    );
}

export default RLProblem;