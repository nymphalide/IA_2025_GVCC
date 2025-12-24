import React, { useState } from 'react';
import { generateNashProblem, evaluateNashAnswer } from '../../api/apiService';
import './Nash.css';

function NashProblem() {
    // Stare pentru problema curentă
    const [problem, setProblem] = useState(null); 
    // Format: { seed, matrix, text, difficulty }

    // Stare pentru configurarea generării (Customization)
    const [config, setConfig] = useState({
        rows: 3,
        cols: 3,
        random_size: true
    });

    // Stare pentru răspunsul utilizatorului
    const [answer, setAnswer] = useState({
        hasEquilibrium: null, 
        row: '',
        col: ''
    });

    // Stare pentru rezultate și UI
    const [evaluation, setEvaluation] = useState(null);
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState(null);

    /**
     * Funcție Helper: Colorează textul "Jucătorul 1" și "Jucătorul 2"
     */
    const formatTextWithColors = (text) => {
        if (!text) return null;
        
        // Spargem textul pentru a găsi instanțele de Jucător 1/2
        const parts = text.split(/(Jucătorul [12])/g);

        return parts.map((part, index) => {
            if (part === 'Jucătorul 1') {
                return <span key={index} className="text-p1">Jucătorul 1</span>;
            }
            if (part === 'Jucătorul 2') {
                return <span key={index} className="text-p2">Jucătorul 2</span>;
            }
            return part;
        });
    };

    /**
     * Generează o nouă matrice de joc cu setările curente
     */
    const handleGenerate = async () => {
        setIsLoading(true);
        setError(null);
        setProblem(null);
        setEvaluation(null);
        setAnswer({ hasEquilibrium: null, row: '', col: '' }); 

        try {
            // Trimitem configurația către API
            const response = await generateNashProblem({
                rows: parseInt(config.rows),
                cols: parseInt(config.cols),
                random_size: config.random_size
            });
            setProblem(response.data);
        } catch (err) {
            console.error("Eroare generare:", err);
            setError("Nu s-a putut genera problema. Verifică backend-ul.");
        } finally {
            setIsLoading(false);
        }
    };

    /**
     * Trimite răspunsul la API
     */
    const handleSubmit = async (e) => {
        e.preventDefault();
        
        if (!answer.hasEquilibrium) {
            setError("Selectează dacă există sau nu un echilibru.");
            return;
        }
        if (answer.hasEquilibrium === 'yes' && (answer.row === '' || answer.col === '')) {
            setError("Introdu coordonatele (Index Rând/Coloană).");
            return;
        }

        setIsLoading(true);
        setError(null);
        setEvaluation(null);

        try {
            const payload = {
                problem_seed: problem.seed,
                has_equilibrium: answer.hasEquilibrium === 'yes',
                equilibrium_point: answer.hasEquilibrium === 'yes'
                    ? [parseInt(answer.row, 10), parseInt(answer.col, 10)]
                    : null
            };

            const response = await evaluateNashAnswer(payload);
            setEvaluation(response.data);
        } catch (err) {
            console.error("Eroare evaluare:", err);
            setError("Eroare la evaluare.");
        } finally {
            setIsLoading(false);
        }
    };

    const getResultClass = () => {
        if (!evaluation) return '';
        if (evaluation.percentage === 100) return 'nash-success';
        if (evaluation.percentage === 0) return 'nash-fail';
        return 'nash-partial';
    };

    return (
        <div className="nash-container">
            <h1 className="title">Teoria Jocurilor: Echilibrul Nash</h1>
            
            {/* --- Config Panel --- */}
            <div className="config-panel">
                <div className="config-group">
                    <label>
                        <input 
                            type="checkbox" 
                            checked={config.random_size}
                            onChange={(e) => setConfig({...config, random_size: e.target.checked})}
                        />
                        Dimensiune Aleatoare
                    </label>
                </div>

                {!config.random_size && (
                    <div className="config-inputs">
                        <label>
                            Rânduri (2-4):
                            <input 
                                type="number" min="2" max="4" 
                                value={config.rows}
                                onChange={(e) => setConfig({...config, rows: e.target.value})}
                            />
                        </label>
                        <label>
                            Coloane (2-4):
                            <input 
                                type="number" min="2" max="4" 
                                value={config.cols}
                                onChange={(e) => setConfig({...config, cols: e.target.value})}
                            />
                        </label>
                    </div>
                )}

                <button 
                    onClick={handleGenerate} 
                    disabled={isLoading} 
                    className="generate-btn"
                >
                    {isLoading ? 'Se procesează...' : 'Generează Matrice'}
                </button>
            </div>
            {error && <p className="error-message">{error}</p>}

            {/* --- Game Workspace --- */}
            {problem && (
                <div className="game-workspace">
                    <div className="matrix-section">
                        <h3>{problem.text.title}</h3>
                        
                        {/* Text formatat cu culori */}
                        <p className="instruction">
                            {formatTextWithColors(problem.text.description)}
                        </p>
                        
                        <p className="instruction-req">
                            {problem.text.requirement}
                        </p>
                        
                        <table className="payoff-matrix">
                            <tbody>
                                <tr>
                                    <td className="matrix-header"></td>
                                    {problem.matrix.grid[0].map((_, idx) => (
                                        <td key={`h-${idx}`} className="matrix-header-col">Col {idx}</td>
                                    ))}
                                </tr>
                                {problem.matrix.grid.map((row, rIndex) => (
                                    <tr key={rIndex}>
                                        <td className="matrix-header-row">Rând {rIndex}</td>
                                        {row.map((cell, cIndex) => (
                                            <td key={cIndex} className="payoff-cell">
                                                <span className="p1-score">{cell[0]}</span>, 
                                                <span className="p2-score">{cell[1]}</span>
                                            </td>
                                        ))}
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </div>

                    <form onSubmit={handleSubmit} className="nash-form">
                        <h3>Răspunsul Tău:</h3>
                        <div className="question-group">
                            <p>Există un echilibru Nash pur?</p>
                            <label className="radio-label">
                                <input 
                                    type="radio" name="hasEq" value="yes"
                                    checked={answer.hasEquilibrium === 'yes'}
                                    onChange={() => setAnswer({...answer, hasEquilibrium: 'yes'})} 
                                /> Da
                            </label>
                            <label className="radio-label">
                                <input 
                                    type="radio" name="hasEq" value="no" 
                                    checked={answer.hasEquilibrium === 'no'}
                                    onChange={() => setAnswer({...answer, hasEquilibrium: 'no'})}
                                /> Nu
                            </label>
                        </div>

                        {answer.hasEquilibrium === 'yes' && (
                            <div className="coords-inputs">
                                <p>Coordonate (ex: 0, 0):</p>
                                <div className="input-row">
                                    <label>Index Rând:
                                        <input 
                                            type="number" min="0" max={problem.matrix.rows - 1}
                                            value={answer.row}
                                            onChange={(e) => setAnswer({...answer, row: e.target.value})}
                                            required
                                        />
                                    </label>
                                    <label>Index Col:
                                        <input 
                                            type="number" min="0" max={problem.matrix.cols - 1}
                                            value={answer.col}
                                            onChange={(e) => setAnswer({...answer, col: e.target.value})}
                                            required
                                        />
                                    </label>
                                </div>
                            </div>
                        )}

                        <button type="submit" className="submit-btn" disabled={isLoading}>
                            Verifică Răspunsul
                        </button>
                    </form>
                </div>
            )}

            {/* --- Results --- */}
            {evaluation && (
                <div className={`nash-result ${getResultClass()}`}>
                    <h2>Rezultat Evaluare</h2>
                    <div className="score-badge">{evaluation.percentage}%</div>
                    <p className="explanation"><strong>Explicație:</strong> {evaluation.explanation}</p>
                    
                    {evaluation.percentage < 100 && (
                        <div className="correct-answer-box">
                            <strong>Soluții Corecte (Indexe): </strong>
                            {evaluation.correct_answer.length > 0 
                                ? JSON.stringify(evaluation.correct_answer) 
                                : "Niciunul"}
                        </div>
                    )}
                </div>
            )}
        </div>
    );
}

export default NashProblem;