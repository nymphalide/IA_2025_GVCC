import React, {useState, useEffect} from 'react';
import {generateMinMaxProblem, evaluateMinMaxAnswer} from '../../api/apiService';
import './MinMax.css';

function MinMaxProblem({autoGenerate = false, seed = null}) {
    // Starea pentru problema primită de la API
    const [problem, setProblem] = useState(null);
    // { seed, tree, text, ... }

    // --- CONFIG STATE (Controale Parametri) ---
    // Acestea sunt valorile din controalele UI (ce vede utilizatorul acum)
    const [config, setConfig] = useState({
        randomDepth: true,
        depth: 3,
        randomRoot: true,
        rootType: 'MAX'
    });

    // --- GENERATION CONFIG STATE ---
    // Acestea sunt setările care au fost folosite efectiv la ultima generare.
    // Le salvăm separat pentru a le trimite la evaluare, chiar dacă utilizatorul schimbă controalele între timp.
    const [lastGenConfig, setLastGenConfig] = useState(null);

    // Starea pentru răspunsul utilizatorului
    const [answer, setAnswer] = useState({root_value: '', visited_nodes: ''});

    // Starea pentru rezultatul evaluării
    const [evaluation, setEvaluation] = useState(null);

    // Starea pentru încărcare și erori
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState(null);
    const [showJson, setShowJson] = useState(false);

    /**
     * Apelată la apăsarea butonului "Generează Problema MinMax".
     * Trimite parametrii configurați către backend.
     */
    const handleGenerate = async () => {


        setIsLoading(true);
        setError(null);
        setProblem(null);
        setEvaluation(null);
        setAnswer({root_value: '', visited_nodes: ''});

        try {
            const isMaxPlayer = config.rootType === 'MAX';

            const payload = {
                seed: seed ?? Math.floor(Math.random() * 1_000_000),
                random_depth: config.randomDepth,
                depth: config.randomDepth
                    ? null
                    : Math.max(1, parseInt(config.depth, 10)),
                random_root: config.randomRoot,
                is_maximizing_player: config.randomRoot ? null : isMaxPlayer
            };


            const response = await generateMinMaxProblem(payload);
            setProblem(response.data);

            // Salvăm configurația folosită pentru a o trimite înapoi la evaluare
            setLastGenConfig(payload);

        } catch (err) {
            setError("Eroare la generarea problemei. API-ul este pornit? (Verifică consola)");
            console.error(err);
        } finally {
            setIsLoading(false);
        }
    };

    useEffect(() => {
        if (autoGenerate) {
            handleGenerate();
        }
    }, [autoGenerate]);

    /**
     * Apelată la trimiterea formularului de răspuns.
     */
    const handleSubmit = async (e) => {
        e.preventDefault();
        if (!problem || answer.root_value === '' || answer.visited_nodes === '') {
            setError("Trebuie să generați o problemă și să completați ambele câmpuri.");
            return;
        }

        setIsLoading(true);
        setError(null);
        setEvaluation(null);

        try {
            const answerData = {
                problem_seed: problem.seed,
                root_value: parseInt(answer.root_value, 10),
                visited_nodes: parseInt(answer.visited_nodes, 10),

                // --- TRIMITERE PARAMETRI PENTRU RECONSTRUCȚIE ---
                generated_random_depth: lastGenConfig.random_depth,
                generated_depth: lastGenConfig.depth,
                generated_random_root: lastGenConfig.random_root,
                generated_is_maximizing: lastGenConfig.is_maximizing_player
            };

            const response = await evaluateMinMaxAnswer(answerData);
            setEvaluation(response.data);
        } catch (err) {
            setError("Eroare la evaluarea răspunsului. (Verifică consola)");
            console.error(err);
        } finally {
            setIsLoading(false);
        }
    };

    const handleInputChange = (e) => {
        const {name, value} = e.target;
        setAnswer(prev => ({
            ...prev,
            [name]: value
        }));
    };

    const getResultClass = () => {
        if (!evaluation) return '';
        if (evaluation.percentage === 100) return 'result-success';
        if (evaluation.percentage === 0) return 'result-fail';
        return 'result-partial';
    };

    return (
        <div className="minmax-container">
            <h1 className="title">Problemă MinMax cu Alpha-Beta</h1>

            {/* --- Secțiunea 1: Configurare & Generare --- */}

            {/* --- Secțiunea 1: Configurare & Generare --- */}
            {!autoGenerate && (
                <div className="config-panel">

                    {/* 1. Control Adâncime */}
                    <div className="config-group">
                        <label>
                            <input
                                type="checkbox"
                                checked={config.randomDepth}
                                onChange={(e) =>
                                    setConfig({...config, randomDepth: e.target.checked})
                                }
                            />
                            Adâncime Aleatoare
                        </label>

                        {!config.randomDepth && (
                            <div className="config-inputs">
                                <input
                                    type="number"
                                    min="0"
                                    max="12"
                                    value={config.depth}
                                    onChange={(e) =>
                                        setConfig({...config, depth: e.target.value})
                                    }
                                />
                            </div>
                        )}
                    </div>

                    {/* 2. Control Tip Rădăcină */}
                    <div className="config-group">
                        <label>
                            <input
                                type="checkbox"
                                checked={config.randomRoot}
                                onChange={(e) =>
                                    setConfig({...config, randomRoot: e.target.checked})
                                }
                            />
                            Nod Rădăcină Aleator
                        </label>

                        {!config.randomRoot && (
                            <div className="config-inputs">
                                <select
                                    value={config.rootType}
                                    onChange={(e) =>
                                        setConfig({...config, rootType: e.target.value})
                                    }
                                >
                                    <option value="MAX">MAX</option>
                                    <option value="MIN">MIN</option>
                                </select>
                            </div>
                        )}
                    </div>

                    {/* 3. Buton Generare */}
                    <button
                        onClick={handleGenerate}
                        disabled={isLoading}
                        className="generate-btn"
                    >
                        {isLoading ? 'Se procesează...' : 'Generează Problemă'}
                    </button>
                </div>
            )}


            {error && <p className="error-message">{error}</p>}

            {/* --- Secțiunea 2: Afișare Problemă (Workspace) --- */}
            {problem && (
                <div className="game-workspace">
                    <div className="tree-section">
                        <h3>{problem.text.title}</h3>

                        <p className="instruction">
                            {problem.text.description}
                        </p>

                        <p className="instruction-req">
                            {problem.text.requirement}
                        </p>

                        <div className="json-toggle">
                            <button
                                type="button"
                                onClick={() => setShowJson(prev => !prev)}
                                className="secondary-btn"
                            >
                                {showJson ? 'Ascunde JSON' : 'Arată JSON'}
                            </button>

                            {showJson && (
                                <pre className="json-viewer">
                                    {JSON.stringify(problem.tree, null, 2)}
                                </pre>
                            )}
                        </div>

                        {problem.tree_image_base64 && (
                            <div className="image-wrapper">
                                <img
                                    src={`data:image/png;base64,${problem.tree_image_base64}`}
                                    alt="Arbore MinMax"
                                    className="tree-image"
                                />
                            </div>
                        )}
                    </div>

                    {/* --- Secțiunea 3: Formular Răspuns --- */}
                    <form onSubmit={handleSubmit} className="answer-form">
                        <div className="form-group">
                            <label htmlFor="root_value">Valoarea în rădăcină (R):</label>
                            <input
                                type="number"
                                id="root_value"
                                name="root_value"
                                value={answer.root_value}
                                onChange={handleInputChange}
                                required
                            />
                        </div>
                        <div className="form-group">
                            <label htmlFor="visited_nodes">Noduri frunză vizitate:</label>
                            <input
                                type="number"
                                id="visited_nodes"
                                name="visited_nodes"
                                value={answer.visited_nodes}
                                onChange={handleInputChange}
                                required
                            />
                        </div>

                        <button type="submit" disabled={isLoading} className="submit-btn">
                            Evaluează Răspuns
                        </button>
                    </form>
                </div>
            )}

            {/* --- Secțiunea 4: Afișare Evaluare --- */}
            {evaluation && (
                <div className={`evaluation-result ${getResultClass()}`}>
                    <h2>Rezultat Evaluare</h2>
                    <div className="score-badge">{evaluation.percentage}%</div>
                    <p className="explanation"><strong>Explicație:</strong> {evaluation.explanation}</p>
                    {evaluation.percentage < 100 && (
                        <p>
                            <strong>Răspuns corect:</strong> Valoare = {evaluation.correct_answer.root_value},
                            Noduri Vizitate = {evaluation.correct_answer.visited_nodes}
                        </p>
                    )}
                </div>
            )}
        </div>
    );
}

export default MinMaxProblem;
