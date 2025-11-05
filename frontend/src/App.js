import React, {useState} from 'react';
import {generateMinMaxProblem, evaluateMinMaxAnswer} from './apiService';
import './App.css';

function App() {
    // Starea pentru problema primită de la API
    const [problem, setProblem] = useState(null); // { seed, tree }

    // Starea pentru răspunsul utilizatorului
    const [answer, setAnswer] = useState({root_value: '', visited_nodes: ''});

    // Starea pentru rezultatul evaluării
    const [evaluation, setEvaluation] = useState(null); // { percentage, correct_answer, explanation }

    // Starea pentru încărcare și erori
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState(null);
    const [showJson, setShowJson] = useState(false);


    /**
     * Apelată la apăsarea butonului "Generează Problemă".
     */
    const handleGenerate = async () => {
        setIsLoading(true);
        setError(null);
        setProblem(null);
        setEvaluation(null);
        setAnswer({root_value: '', visited_nodes: ''}); // Resetăm formularul

        try {
            const response = await generateMinMaxProblem();
            setProblem(response.data); // Salvăm problema (seed + arbore)
        } catch (err) {
            setError("Eroare la generarea problemei. API-ul este pornit? (Verifică consola)");
            console.error(err);
        } finally {
            setIsLoading(false);
        }
    };

    /**
     * Apelată la trimiterea formularului de răspuns.
     */
    const handleSubmit = async (e) => {
        e.preventDefault(); // Oprește reîncărcarea paginii

        if (!problem || answer.root_value === '' || answer.visited_nodes === '') {
            setError("Trebuie să generați o problemă și să completați ambele câmpuri.");
            return;
        }

        setIsLoading(true);
        setError(null);
        setEvaluation(null);

        try {
            // Pregătim datele pentru API
            const answerData = {
                problem_seed: problem.seed,
                root_value: parseInt(answer.root_value, 10),
                visited_nodes: parseInt(answer.visited_nodes, 10)
            };

            const response = await evaluateMinMaxAnswer(answerData);
            setEvaluation(response.data); // Salvăm rezultatul evaluării
        } catch (err) {
            setError("Eroare la evaluarea răspunsului. (Verifică consola)");
            console.error(err);
        } finally {
            setIsLoading(false);
        }
    };

    /**
     * Actualizează starea 'answer' pe măsură ce utilizatorul scrie.
     */
    const handleInputChange = (e) => {
        const {name, value} = e.target;
        setAnswer(prev => ({
            ...prev,
            [name]: value
        }));
    };

    /**
     * Helper pentru a formata CSS-ul rezultatului.
     */
    const getResultClass = () => {
        if (!evaluation) return '';
        if (evaluation.percentage === 100) return 'result-success';
        if (evaluation.percentage === 0) return 'result-fail';
        return 'result-partial';
    };

    return (
        <div className="App">
            <h1>Demo Livrabil L6 - MinMax cu Alpha-Beta</h1>

            {/* --- Secțiunea 1: Generare --- */}
            <div className="container">
                <button onClick={handleGenerate} disabled={isLoading}>
                    {isLoading ? 'Se generează...' : 'Generează Problemă MinMax'}
                </button>
                {error && <p className="error">{error}</p>}
            </div>

            {/* --- Secțiunea 2: Afișare Problemă (dacă există) --- */}
            {problem && (
                <div className="container">

                    <h2>Problemă MinMax cu Pruning Alpha-Beta</h2>
                    <p className="problem-statement">
                        Se consideră arborele de mai jos, în care nodurile frunză au valori numerice,
                        iar celelalte noduri sunt de tip MAX sau MIN.
                        Determinați valoarea calculată în rădăcina arborelui și
                        numărul de noduri frunză evaluate în timpul procesului
                        de parcurgere folosind algoritmul Alpha-Beta Pruning.
                    </p>

                    {/* Spoiler JSON */}
                    <div className="json-toggle">
                        <button
                            type="button"
                            onClick={() => setShowJson(prev => !prev)}
                            className="json-button"
                        >
                            {showJson ? 'Ascunde JSON' : 'Arată JSON'}
                        </button>

                        {showJson && (
                            <pre className="json-viewer">
                                {JSON.stringify(problem.tree, null, 2)}
                            </pre>
                        )}
                    </div>

                    {/* 🔹 Afișează imaginea arborelui */}
                    {problem.tree_image_base64 && (
                        <>
                            <h3>Reprezentare grafică a arborelui:</h3>
                            <img
                                src={`data:image/png;base64,${problem.tree_image_base64}`}
                                alt="Arbore MinMax"
                                style={{
                                    maxWidth: "100%",
                                    border: "1px solid #ccc",
                                    borderRadius: "8px",
                                    marginTop: "10px",
                                }}
                            />
                        </>
                    )}


                    {/* --- Secțiunea 3: Formular Răspuns --- */}
                    <form onSubmit={handleSubmit} className="form-inline">
                        <div className="form-group-inline">
                            <label htmlFor="root_value">Valoarea calculată în rădăcină (R):</label>
                            <input
                                type="number"
                                id="root_value"
                                name="root_value"
                                value={answer.root_value}
                                onChange={handleInputChange}
                                required
                            />
                        </div>
                        <div className="form-group-inline">
                            <label htmlFor="visited_nodes">Numărul de noduri frunză vizitate:</label>
                            <input
                                type="number"
                                id="visited_nodes"
                                name="visited_nodes"
                                value={answer.visited_nodes}
                                onChange={handleInputChange}
                                required
                            />
                        </div>
                        <button type="submit" disabled={isLoading}>
                            {isLoading ? 'Se evaluează...' : 'Evaluează Răspuns'}
                        </button>
                    </form>

                </div>
            )}

            {/* --- Secțiunea 4: Afișare Evaluare (dacă există) --- */}
            {evaluation && (
                <div className={`container result ${getResultClass()}`}>
                    <h2>Rezultat Evaluare</h2>
                    <h3>Scor: {evaluation.percentage}%</h3>
                    <p><b>Explicație:</b> {evaluation.explanation}</p>
                    {evaluation.percentage < 100 && (
                        <p>
                            <b>Răspuns corect:</b> Valoare = {evaluation.correct_answer.root_value},
                            Noduri Vizitate = {evaluation.correct_answer.visited_nodes}
                        </p>
                    )}
                </div>
            )}

        </div>
    );
}

export default App;