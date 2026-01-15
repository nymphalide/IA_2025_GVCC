import React, {useState, useEffect} from 'react';
import {
    generateBayesProblem,
    evaluateBayesAnswer
} from "../../api/apiService";
import "./Bayes.css";

function BayesProblem({autoGenerate = false, seed = null}) {
    const [problem, setProblem] = useState(null);
    const [answer, setAnswer] = useState("");
    const [evaluation, setEvaluation] = useState(null);
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState(null);

    const [isRandom, setIsRandom] = useState(true);
    const [pRain, setPRain] = useState("");
    const [pSprinkler, setPSprinkler] = useState("");

    const handleGenerate = async () => {
        setIsLoading(true);
        setError(null);
        setProblem(null);
        setEvaluation(null);
        setAnswer("");

        try {
            const payload = {
                seed: seed ?? Math.floor(Math.random() * 1_000_000),

                custom_priors: autoGenerate
                    ? null
                    : isRandom
                        ? null
                        : {
                            p_rain: parseFloat(pRain),
                            p_sprinkler: parseFloat(pSprinkler),
                        },
            };

            const res = await generateBayesProblem(payload);
            setProblem(res.data);
        } catch (err) {
            console.error(err);
            setError("Eroare la generarea problemei Bayes.");
        } finally {
            setIsLoading(false);
        }
    };

    useEffect(() => {
        if (autoGenerate) {
            handleGenerate();
        }
    }, [autoGenerate]);

    const handleSubmit = async () => {
        if (!problem || answer === "") {
            setError("Introduceți un răspuns numeric.");
            return;
        }

        setIsLoading(true);
        setError(null);
        setEvaluation(null);

        try {
            const payload = {
                correct_answer: problem.problem.solution,
                user_answer: parseFloat(answer)
            };

            const res = await evaluateBayesAnswer(payload);
            setEvaluation(res.data);
        } catch (err) {
            console.error(err);
            setError("Eroare la evaluarea răspunsului.");
        } finally {
            setIsLoading(false);
        }
    };

    const getResultClass = () => {
        if (!evaluation) return "";
        if (evaluation.score === 100) return "result-success";
        if (evaluation.score === 0) return "result-fail";
        return "result-partial";
    };

    return (
        <div className="bayes-container">
            <h1 className="title">Rețele Bayesiene</h1>

            {/* --- GENERARE --- */}
            {!autoGenerate && (
                <div className="config-panel">
                    <label>
                        <input
                            type="checkbox"
                            checked={isRandom}
                            onChange={() => setIsRandom(!isRandom)}
                        />
                        Random
                    </label>

                    {!isRandom && (
                        <>
                            <input
                                type="number"
                                step="0.01"
                                min="0"
                                max="1"
                                placeholder="Ploaie"
                                value={pRain}
                                onChange={(e) => setPRain(Math.min(1, Math.max(0, e.target.value)))}
                            />
                            <input
                                type="number"
                                step="0.01"
                                min="0"
                                max="1"
                                placeholder="Stropitoare"
                                value={pSprinkler}
                                onChange={(e) =>
                                    setPSprinkler(Math.min(1, Math.max(0, e.target.value)))
                                }
                            />
                        </>
                    )}

                    <button
                        onClick={handleGenerate}
                        disabled={isLoading}
                        className="generate-btn"
                    >
                        {isLoading ? "Se procesează..." : "Generează problemă"}
                    </button>
                </div>
            )}


            {error && <p className="error-message">{error}</p>}

            {problem && (
                <div className="game-workspace bayes-workspace">

                    {/* --- CARD: REȚEA --- */}
                    <div className="bayes-card">
                        <h3>Rețeaua Bayesiană</h3>
                        <div className="bayes-network">
                            <span>🌧️ Ploaie</span>
                            <span>→</span>
                            <span>🌱 Iarbă Umedă</span>
                            <br/>
                            <span>🚿 Stropitoare</span>
                            <span>→</span>
                            <span>🌱 Iarbă Umedă</span>
                        </div>
                    </div>

                    {/* --- CARD: PROBABILITĂȚI --- */}
                    <div className="bayes-card">
                        <h3>Probabilități</h3>

                        <div className="prob-group">
                            <strong>Prioruri</strong>
                            <ul>
                                <li>P(Ploaie) = {problem.problem.p_rain}</li>
                                <li>P(Stropitoare) = {problem.problem.p_sprinkler}</li>
                            </ul>
                        </div>

                        <div className="prob-group">
                            <strong>Condiționate</strong>
                            <ul>
                                <li>P(Iarbă Umedă | Ploaie, Stropitoare) = {problem.problem.p_w_rs}</li>
                                <li>P(Iarbă Umedă | Ploaie, ¬Stropitoare) = {problem.problem.p_w_rns}</li>
                                <li>P(Iarbă Umedă | ¬Ploaie, Stropitoare) = {problem.problem.p_w_nrs}</li>
                                <li>P(Iarbă Umedă | ¬Ploaie, ¬Stropitoare) = {problem.problem.p_w_nrns}</li>
                            </ul>
                        </div>
                    </div>

                    {/* --- CARD: ÎNTREBARE --- */}
                    <div className="bayes-card question-card">
                        <h3>Întrebare</h3>
                        <p>
                            Știind că <strong>iarba este umedă</strong>, care este probabilitatea
                            ca <strong>a plouat</strong>?
                        </p>
                    </div>

                    {/* --- RĂSPUNS --- */}
                    <div className="answer-form">
                        <div className="form-group">
                            <label>P(Ploaie | Iarbă Umedă)</label>
                            <input
                                type="number"
                                step="0.01"
                                value={answer}
                                onChange={(e) => setAnswer(e.target.value)}
                                placeholder="ex: 0.65"
                            />
                        </div>

                        <button
                            onClick={handleSubmit}
                            disabled={isLoading}
                            className="submit-btn"
                        >
                            Evaluează răspuns
                        </button>
                    </div>
                </div>
            )}

            {evaluation && (
                <div className={`evaluation-result ${getResultClass()}`}>
                    <h2>Rezultat evaluare</h2>

                    <div className="score-badge">
                        {evaluation.score}%
                    </div>

                    <div className="correct-answer">
                        <strong>Răspuns corect:</strong>{" "}
                        {problem.problem.solution}
                    </div>
                </div>
            )}
        </div>
    );
}

export default BayesProblem;
