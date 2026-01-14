import React, { useState } from 'react';
import { generateStrategyProblem, evaluateStrategyAnswer } from '../../api/apiService';
import './Strategy.css';

function StrategyProblem() {
    const [problem, setProblem] = useState(null);

    // --- CONFIG STATE (ca la MinMax / Nash) ---
    const [config, setConfig] = useState({
        randomProblem: true,
        problemType: 'nqueens',

        randomInstance: true,

        n: 8,
        boardSize: 8,
        vertices: 50,
        density: 0.3,
        nDisks: 5,
        nPegs: 3
    });

    // --- LAST GENERATION CONFIG ---
    const [lastGenConfig, setLastGenConfig] = useState(null);

    // --- USER ANSWER ---
    const [selectedStrategy, setSelectedStrategy] = useState(null);

    // --- UI STATE ---
    const [evaluation, setEvaluation] = useState(null);
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState(null);

    const handleGenerate = async () => {
        setIsLoading(true);
        setError(null);
        setProblem(null);
        setEvaluation(null);
        setSelectedStrategy(null);

        try {
            const payload = {
                random_problem: config.randomProblem,
                problem_type: config.randomProblem ? null : config.problemType,

                random_instance: config.randomInstance,

                n: config.randomInstance ? null : parseInt(config.n, 10),
                board_size: config.randomInstance ? null : parseInt(config.boardSize, 10),
                vertices: config.randomInstance ? null : parseInt(config.vertices, 10),
                density: config.randomInstance ? null : parseFloat(config.density),
                n_disks: config.randomInstance ? null : parseInt(config.nDisks, 10),
                n_pegs: config.randomInstance ? null : parseInt(config.nPegs, 10),
            };

            const response = await generateStrategyProblem(payload);
            setProblem(response.data);

            // Salvăm exact configurația folosită
            setLastGenConfig(payload);

        } catch (err) {
            console.error(err);
            setError("Eroare la generarea problemei Strategy.");
        } finally {
            setIsLoading(false);
        }
    };

    const handleEvaluate = async () => {
        if (!problem || !selectedStrategy || !lastGenConfig) {
            setError("Generează o problemă și alege o strategie.");
            return;
        }

        setIsLoading(true);
        setError(null);
        setEvaluation(null);

        try {
            const answerPayload = {
                problem_seed: problem.seed,
                chosen_strategy: selectedStrategy,

                // --- PARAMETRI DE RECONSTRUCȚIE (ca la MinMax) ---
                generated_random_problem: lastGenConfig.random_problem,
                generated_problem_type: lastGenConfig.problem_type,

                generated_random_instance: lastGenConfig.random_instance,

                generated_n: lastGenConfig.n,
                generated_board_size: lastGenConfig.board_size,
                generated_vertices: lastGenConfig.vertices,
                generated_density: lastGenConfig.density,
                generated_n_disks: lastGenConfig.n_disks,
                generated_n_pegs: lastGenConfig.n_pegs,
            };

            const response = await evaluateStrategyAnswer(answerPayload);
            setEvaluation(response.data);

        } catch (err) {
            console.error(err);
            setError("Eroare la evaluarea răspunsului.");
        } finally {
            setIsLoading(false);
        }
    };

    const getResultClass = () => {
        if (!evaluation) return '';
        if (evaluation.percentage === 100) return 'result-success';
        if (evaluation.percentage === 0) return 'result-fail';
        return 'result-partial';
    };

    return (
        <div className="strategy-container">
            <h1 className="title">Strategy Selection Problem</h1>



        {/* --- CONFIG PANEL --- */}
<div className="strategy-panel">

    {/* Problem random */}
    <label>
        <input
            type="checkbox"
            checked={config.randomProblem}
            onChange={(e) => {
                const checked = e.target.checked;
                // dacă revenim la random problem, forțăm și random instance
                if (checked) {
                    setConfig({
                        ...config,
                        randomProblem: true,
                        randomInstance: true
                    });
                } else {
                    setConfig({
                        ...config,
                        randomProblem: false
                    });
                }
            }}
        />
        Problemă aleatoare
    </label>

    {/* Problem selector */}
    {!config.randomProblem && (
        <select
            value={config.problemType}
            onChange={(e) => setConfig({ ...config, problemType: e.target.value })}
        >
            <option value="nqueens">N-Queens</option>
            <option value="knight">Knight's Tour</option>
            <option value="graph_coloring">Graph Coloring</option>
            <option value="hanoi">Hanoi</option>
        </select>
    )}

    {/* Instance random */}
    <label>
        <input
            type="checkbox"
            checked={config.randomInstance}
            onChange={(e) => {
            if (config.randomProblem && !e.target.checked) {
                setError("Selectați mai întâi problema.");
                return;
            }
            setError(null);
            setConfig({ ...config, randomInstance: e.target.checked });
        }}

        />
        Instanță aleatoare
    </label>

    <button onClick={handleGenerate} disabled={isLoading} className="generate-btn">
        {isLoading ? "Se generează..." : "Generează Problema"}
    </button>
</div>

{/* --- CUSTOM INPUTS --- */}
{!config.randomProblem && !config.randomInstance && (
    <div className="custom-inputs">

        {config.problemType === "nqueens" && (
            <label>
                N:
                <input
                    type="number"
                    value={config.n}
                    onChange={(e) => setConfig({ ...config, n: e.target.value })}
                />
            </label>
        )}

        {config.problemType === "knight" && (
            <label>
                Board size:
                <input
                    type="number"
                    value={config.boardSize}
                    onChange={(e) => setConfig({ ...config, boardSize: e.target.value })}
                />
            </label>
        )}

        {config.problemType === "graph_coloring" && (
            <>
                <label>
                    Vertices:
                    <input
                        type="number"
                        value={config.vertices}
                        onChange={(e) => setConfig({ ...config, vertices: e.target.value })}
                    />
                </label>
                <label>
                    Density:
                    <input
                        type="number"
                        step="0.1"
                        value={config.density}
                        onChange={(e) => setConfig({ ...config, density: e.target.value })}
                    />
                </label>
            </>
        )}

        {config.problemType === "hanoi" && (
            <>
                <label>
                    Disks:
                    <input
                        type="number"
                        value={config.nDisks}
                        onChange={(e) => setConfig({ ...config, nDisks: e.target.value })}
                    />
                </label>
                <label>
                    Pegs:
                    <input
                        type="number"
                        value={config.nPegs}
                        onChange={(e) => setConfig({ ...config, nPegs: e.target.value })}
                    />
                </label>
            </>
        )}

    </div>
)}




            {error && <p className="error-message">{error}</p>}

            {/* --- PROBLEM DISPLAY --- */}
            {problem && (
                <div className="strategy-box">
                    <h3>{problem.problem_name}</h3>
                    <p>{problem.description}</p>

                    <div className="options-grid">
                        {problem.options.map(opt => (
                            <button
                                key={opt}
                                className={`opt-btn ${selectedStrategy === opt ? "selected" : ""}`}
                                onClick={() => setSelectedStrategy(opt)}
                            >
                                {opt}
                            </button>
                        ))}
                    </div>

                    <button
                        onClick={handleEvaluate}
                        disabled={isLoading || !selectedStrategy}
                        className="strategy-eval-btn"
                    >
                        Evaluează Răspuns
                    </button>
                </div>
            )}

            {/* --- EVALUATION --- */}
            {evaluation && (
                <div className={`evaluation-result ${getResultClass()}`}>
                    <h2>Rezultat</h2>
                    <div className="score-badge">{evaluation.percentage}%</div>
                    <p className="explanation"><strong>Explicație:</strong> {evaluation.explanation}</p>
                    {evaluation.percentage < 100 && (
                        <p><strong>Răspuns corect:</strong> {evaluation.correct_answer}</p>
                    )}
                </div>
            )}
        </div>
    );
}

export default StrategyProblem;
