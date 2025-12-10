import React, { useState } from 'react';
import { generateNashProblem, evaluateNashAnswer } from '../../api/apiService';
import './Nash.css';

function NashProblem() {
    // Stare pentru problema curentă (matricea)
    const [problem, setProblem] = useState(null); 
    // Format problem: { seed, matrix: { rows, cols, grid: [[ [p1,p2], ...], ...] }, difficulty }

    // Stare pentru răspunsul utilizatorului
    const [answer, setAnswer] = useState({
        hasEquilibrium: null, // 'yes' sau 'no'
        row: '',
        col: ''
    });

    // Stare pentru rezultate și UI
    const [evaluation, setEvaluation] = useState(null);
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState(null);

    /**
     * Generează o nouă matrice de joc
     */
    const handleGenerate = async () => {
        setIsLoading(true);
        setError(null);
        setProblem(null);
        setEvaluation(null);
        setAnswer({ hasEquilibrium: null, row: '', col: '' }); // Reset form

        try {
            const response = await generateNashProblem();
            setProblem(response.data);
        } catch (err) {
            console.error("Eroare generare:", err);
            setError("Nu s-a putut genera problema. Verifică dacă backend-ul rulează.");
        } finally {
            setIsLoading(false);
        }
    };

    /**
     * Trimite răspunsul la API
     */
    const handleSubmit = async (e) => {
        e.preventDefault();
        
        // Validare simplă
        if (!answer.hasEquilibrium) {
            setError("Te rog selectează dacă există sau nu un echilibru.");
            return;
        }
        if (answer.hasEquilibrium === 'yes' && (answer.row === '' || answer.col === '')) {
            setError("Dacă există un echilibru, trebuie să introduci coordonatele (Index Rând/Coloană).");
            return;
        }

        setIsLoading(true);
        setError(null);
        setEvaluation(null);

        try {
            // Pregătim payload-ul conform NashAnswerRequest din Python
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
            setError("A apărut o eroare la evaluarea răspunsului.");
        } finally {
            setIsLoading(false);
        }
    };

    /**
     * Helper pentru stilizarea rezultatului
     */
    const getResultClass = () => {
        if (!evaluation) return '';
        if (evaluation.percentage === 100) return 'nash-success';
        if (evaluation.percentage === 0) return 'nash-fail';
        return 'nash-partial';
    };

    return (
        <div className="nash-container">
            <h1 className="title">Teoria Jocurilor: Echilibrul Nash</h1>
            
            <div className="nash-controls">
                <button 
                    onClick={handleGenerate} 
                    disabled={isLoading} 
                    className="generate-btn"
                >
                    {isLoading ? 'Se procesează...' : 'Generează Matrice Nouă'}
                </button>
                {error && <p className="error-message">{error}</p>}
            </div>

            {problem && (
                <div className="game-workspace">
                    <div className="matrix-section">
                        <h3>Matricea Plăților (Jucător 1, Jucător 2)</h3>
                        <p className="instruction">
                            Identificați dacă există un Echilibru Nash <strong>Pur</strong>.<br/>
                            Valorile sunt (<span className="p1-score">Payoff J1</span>, <span className="p2-score">Payoff J2</span>). 
                            <span className="p1-score"> J1</span> alege rândul, 
                            <span className="p2-score"> J2</span> alege coloana.
                        </p>
                        
                        <table className="payoff-matrix">
                            <tbody>
                                {/* Header pentru indexul coloanelor */}
                                <tr>
                                    <td className="matrix-header"></td>
                                    {problem.matrix.grid[0].map((_, idx) => (
                                        <td key={`h-${idx}`} className="matrix-header-col">Col {idx}</td>
                                    ))}
                                </tr>
                                
                                {/* Rândurile matricei */}
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
                                    type="radio" 
                                    name="hasEq" 
                                    value="yes"
                                    checked={answer.hasEquilibrium === 'yes'}
                                    onChange={() => setAnswer({...answer, hasEquilibrium: 'yes'})} 
                                /> Da
                            </label>
                            <label className="radio-label">
                                <input 
                                    type="radio" 
                                    name="hasEq" 
                                    value="no" 
                                    checked={answer.hasEquilibrium === 'no'}
                                    onChange={() => setAnswer({...answer, hasEquilibrium: 'no'})}
                                /> Nu
                            </label>
                        </div>

                        {answer.hasEquilibrium === 'yes' && (
                            <div className="coords-inputs">
                                <p>Introduceți coordonatele unui echilibru (ex: 0, 0):</p>
                                <div className="input-row">
                                    <label>
                                        Index Rând:
                                        <input 
                                            type="number" 
                                            min="0"
                                            max={problem.matrix.rows - 1}
                                            value={answer.row}
                                            onChange={(e) => setAnswer({...answer, row: e.target.value})}
                                            required
                                        />
                                    </label>
                                    <label>
                                        Index Coloană:
                                        <input 
                                            type="number" 
                                            min="0"
                                            max={problem.matrix.cols - 1}
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