import React, { useState } from 'react';
import { generateCspProblem, evaluateCspAnswer } from '../../api/apiService';
import './Csp.css';

function CspProblem() {
    // UI State
    const [config, setConfig] = useState({
        randomGraph: true,
        graphSize: '5',
        randomAlgo: true,
        algo: 'FC',
        randomPrefill: true,
        prefill: 'MED'
    });
    const [usedConfig, setUsedConfig] = useState(null);
    const [problem, setProblem] = useState(null);
    const [userAnswers, setUserAnswers] = useState({});
    const [evaluation, setEvaluation] = useState(null);
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState(null);

    // Mapare culori vizuale (Hex)
    const colorMap = {
        "Red": "#e74c3c",   // Roșu
        "Green": "#2ecc71", // Verde
        "Blue": "#3498db",  // Albastru
        "Unknown": "#ecf0f1"
    };

    // Mapare text afișare - Trebuie să corespundă cu backend
    const displayColorMap = {
        "Red": "Roșu",
        "Green": "Verde",
        "Blue": "Albastru"
    };

    const handleGenerate = async () => {
        setIsLoading(true);
        setError(null);
        setProblem(null);
        setEvaluation(null);
        setUserAnswers({});

        try {
            const payload = {
                random_graph: config.randomGraph,
                graph_size: config.randomGraph ? null : parseInt(config.graphSize),
                random_algo: config.randomAlgo,
                algorithm: config.randomAlgo ? null : config.algo,
                random_prefill: config.randomPrefill,
                prefill_level: config.randomPrefill ? null : config.prefill
            };

            const response = await generateCspProblem(payload);
            setProblem(response.data);
            setUsedConfig(payload);
            
            setUserAnswers(response.data.assignments);
            
        } catch (err) {
            console.error(err);
            setError("Eroare la generarea problemei CSP.");
        } finally {
            setIsLoading(false);
        }
    };

    const handleAnswerChange = (nodeId, color) => {
        setUserAnswers(prev => ({ ...prev, [nodeId]: color }));
    };

    const handleSubmit = async () => {
        if (!problem) return;

        const totalNodes = problem.graph.nodes.length;
        if (Object.keys(userAnswers).length < totalNodes) {
            setError(`Ați completat doar ${Object.keys(userAnswers).length} din ${totalNodes} noduri.`);
            return;
        }

        setIsLoading(true);
        setEvaluation(null);
        setError(null);

        try {
            const payload = {
                problem_seed: problem.seed,
                user_assignments: userAnswers,
                generated_params: usedConfig 
            };

            const response = await evaluateCspAnswer(payload);
            setEvaluation(response.data);
        } catch (err) {
            console.error(err);
            setError("Eroare la evaluare.");
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

    const formatCorrectSolution = (lines) => {
        if (!Array.isArray(lines)) return "";
        const compactLines = lines.map(line => {
            const match = line.match(/nodul\s+(\d+)\s+este\s+([\wĂÂÎȘȚăâîșț]+)/i);
            if (match) return `Nod ${match[1]} = ${match[2]}`;
            return line;
        });
        return compactLines.join(", ");
    };

    const renderGraph = () => {
        if (!problem) return null;

        const { nodes, edges } = problem.graph;
        const scale = 3.5; 
        const radius = 15;

        return (
            <svg width="350" height="350" className="graph-svg">
                {edges.map((e, idx) => {
                    const n1 = nodes.find(n => n.id === e.source);
                    const n2 = nodes.find(n => n.id === e.target);
                    return (
                        <line 
                            key={`edge-${idx}`}
                            x1={n1.x * scale} y1={n1.y * scale}
                            x2={n2.x * scale} y2={n2.y * scale}
                            stroke="#95a5a6" strokeWidth="3"
                        />
                    );
                })}
                {nodes.map((n) => {
                    const isAssigned = userAnswers[n.id] !== undefined;
                    const fillColor = isAssigned ? colorMap[userAnswers[n.id]] : colorMap["Unknown"];
                    
                    return (
                        <g key={`node-${n.id}`}>
                            <circle 
                                cx={n.x * scale} cy={n.y * scale} r={radius}
                                fill={fillColor}
                                stroke="#2c3e50" strokeWidth="2"
                            />
                            <text 
                                x={n.x * scale} y={n.y * scale + 5} 
                                textAnchor="middle" fill={isAssigned ? "white" : "#333"}
                                fontWeight="bold" fontSize="14px"
                                style={{pointerEvents: 'none'}}
                            >
                                {n.label}
                            </text>
                        </g>
                    );
                })}
            </svg>
        );
    };

    return (
        <div className="csp-container">
            {/* TERMINOLOGIE ACTUALIZATĂ AICI */}
            <h1 className="title">CSP: Problema Colorării Grafurilor</h1>
            <div className="config-panel">
                <div className="config-group">
                    <label>
                        <input 
                            type="checkbox" 
                            checked={config.randomGraph}
                            onChange={(e) => setConfig({...config, randomGraph: e.target.checked})}
                        />
                        Graf Aleator
                    </label>
                    {!config.randomGraph && (
                        <div className="config-inputs">
                            <select value={config.graphSize} onChange={(e) => setConfig({...config, graphSize: e.target.value})}>
                                <option value="5">5 Noduri</option>
                                <option value="7">7 Noduri</option>
                                <option value="10">10 Noduri</option>
                            </select>
                        </div>
                    )}
                </div>
                <div className="config-group">
                    <label>
                        <input 
                            type="checkbox" 
                            checked={config.randomAlgo}
                            onChange={(e) => setConfig({...config, randomAlgo: e.target.checked})}
                        />
                        Algoritm Aleator
                    </label>
                    {!config.randomAlgo && (
                        <div className="config-inputs">
                            <select value={config.algo} onChange={(e) => setConfig({...config, algo: e.target.value})}>
                                <option value="FC">FC</option>
                                <option value="MRV">MRV</option>
                                <option value="AC-3">AC-3</option>
                            </select>
                        </div>
                    )}
                </div>
                <div className="config-group">
                    <label>
                        <input 
                            type="checkbox" 
                            checked={config.randomPrefill}
                            onChange={(e) => setConfig({...config, randomPrefill: e.target.checked})}
                        />
                        Grad Completare Aleator
                    </label>
                    {!config.randomPrefill && (
                        <div className="config-inputs">
                            <select value={config.prefill} onChange={(e) => setConfig({...config, prefill: e.target.value})}>
                                <option value="LOW">Minim (~25%)</option>
                                <option value="MED">Mediu (~50%)</option>
                                <option value="HIGH">Extins (~75%)</option>
                            </select>
                        </div>
                    )}
                </div>
                <button onClick={handleGenerate} disabled={isLoading} className="generate-btn">
                    {isLoading ? 'Se procesează...' : 'Generează Problemă'}
                </button>
            </div>
            {error && <p className="error-message">{error}</p>}
            {problem && (
                <div className="game-workspace">
                    <div className="description-section">
                        <h3>{problem.text.title}</h3>
                        <p className="instruction">{problem.text.description}</p>
                        <p className="instruction-req">{problem.text.requirement}</p>
                        <p className="note-text">{problem.text.note}</p>
                    </div>
                    <div className="graph-viz">
                        {renderGraph()}
                    </div>
                    <div className="csp-form">
                        <h3>Asignare Variabile (Finală)</h3>
                        <div className="inputs-grid">
                            {problem.all_variables.map(nodeId => {
                                const isPreassigned = problem.assignments[nodeId] !== undefined;
                                if (isPreassigned) return null; 
                                return (
                                    <div key={nodeId} className="input-card">
                                        <label>Nod {nodeId}</label>
                                        <select 
                                            value={userAnswers[nodeId] || ""}
                                            onChange={(e) => handleAnswerChange(nodeId, e.target.value)}
                                        >
                                            <option value="" disabled>Alege culoare...</option>
                                            {problem.available_colors && problem.available_colors.map(color => (
                                                <option key={color} value={color}>
                                                    {displayColorMap[color] || color}
                                                </option>
                                            ))}
                                        </select>
                                    </div>
                                );
                            })}
                        </div>
                        <button onClick={handleSubmit} disabled={isLoading} className="submit-btn">
                            Verifică Soluția
                        </button>
                    </div>
                </div>
            )}
            {evaluation && (
                <div className={`csp-result ${getResultClass()}`}>
                    <h2>Rezultat Evaluare</h2>
                    <div className="score-badge">{evaluation.percentage}%</div>
                    <p className="explanation"><strong>Explicație:</strong> {evaluation.explanation}</p>
                    {evaluation.percentage < 100 && (
                        <p>
                            <strong>Soluția Corectă:</strong> {formatCorrectSolution(evaluation.correct_solution)}
                        </p>
                    )}
                </div>
            )}
        </div>
    );
}

export default CspProblem;