import React, { useState } from 'react';
import { generateMinMaxProblem, evaluateMinMaxAnswer } from '../../api/apiService';
import './MinMax.css';

function MinMaxProblem() {
    // State for problem received from API
    const [problem, setProblem] = useState(null); // { seed, tree }

    // State for user answer
    const [answer, setAnswer] = useState({ root_value: '', visited_nodes: '' });

    // State for evaluation result
    const [evaluation, setEvaluation] = useState(null); // { percentage, correct_answer, explanation }

    // State for loading and errors
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState(null);
    const [showJson, setShowJson] = useState(false);

    /**
     * Called when "Generate Problem" is clicked.
     */
    const handleGenerate = async () => {
        setIsLoading(true);
        setError(null);
        setProblem(null);
        setEvaluation(null);
        setAnswer({ root_value: '', visited_nodes: '' });

        try {
            const response = await generateMinMaxProblem();
            setProblem(response.data);
        } catch (err) {
            setError("Error generating problem. Is the API running? (Check console)");
            console.error(err);
        } finally {
            setIsLoading(false);
        }
    };

    /**
     * Called when answer form is submitted.
     */
    const handleSubmit = async (e) => {
        e.preventDefault();

        if (!problem || answer.root_value === '' || answer.visited_nodes === '') {
            setError("You must generate a problem and fill in both fields.");
            return;
        }

        setIsLoading(true);
        setError(null);
        setEvaluation(null);

        try {
            const answerData = {
                problem_seed: problem.seed,
                root_value: parseInt(answer.root_value, 10),
                visited_nodes: parseInt(answer.visited_nodes, 10)
            };

            const response = await evaluateMinMaxAnswer(answerData);
            setEvaluation(response.data);
        } catch (err) {
            setError("Error evaluating answer. (Check console)");
            console.error(err);
        } finally {
            setIsLoading(false);
        }
    };

    const handleInputChange = (e) => {
        const { name, value } = e.target;
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
            <h1>Demo Deliverable L6 - MinMax with Alpha-Beta</h1>

            {/* --- Section 1: Generation --- */}
            <div className="control-panel">
                <button onClick={handleGenerate} disabled={isLoading} className="primary-btn">
                    {isLoading ? 'Generating...' : 'Generate MinMax Problem'}
                </button>
                {error && <p className="error-msg">{error}</p>}
            </div>

            {/* --- Section 2: Display Problem --- */}
            {problem && (
                <div className="problem-card">
                    <h2>MinMax Problem with Alpha-Beta Pruning</h2>
                    <p className="problem-text">
                        Consider the tree below, where leaf nodes have numeric values,
                        and other nodes are MAX or MIN types.
                        Determine the value calculated at the root and the
                        number of leaf nodes evaluated during the traversal process
                        using the Alpha-Beta Pruning algorithm.
                    </p>

                    {/* JSON Spoiler */}
                    <div className="json-toggle">
                        <button
                            type="button"
                            onClick={() => setShowJson(prev => !prev)}
                            className="secondary-btn"
                        >
                            {showJson ? 'Hide JSON' : 'Show JSON'}
                        </button>

                        {showJson && (
                            <pre className="json-viewer">
                                {JSON.stringify(problem.tree, null, 2)}
                            </pre>
                        )}
                    </div>

                    {/* Tree Image */}
                    {problem.tree_image_base64 && (
                        <div className="image-wrapper">
                            <h3>Tree Representation:</h3>
                            <img
                                src={`data:image/png;base64,${problem.tree_image_base64}`}
                                alt="MinMax Tree"
                                className="tree-image"
                            />
                        </div>
                    )}

                    {/* --- Section 3: Answer Form --- */}
                    <form onSubmit={handleSubmit} className="answer-form">
                        <div className="form-group">
                            <label htmlFor="root_value">Calculated Root Value (R):</label>
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
                            <label htmlFor="visited_nodes">Leaf Nodes Visited:</label>
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
                            {isLoading ? 'Evaluating...' : 'Evaluate Answer'}
                        </button>
                    </form>
                </div>
            )}

            {/* --- Section 4: Evaluation --- */}
            {evaluation && (
                <div className={`evaluation-card ${getResultClass()}`}>
                    <h2>Evaluation Result</h2>
                    <h3>Score: {evaluation.percentage}%</h3>
                    <p><b>Explanation:</b> {evaluation.explanation}</p>
                    {evaluation.percentage < 100 && (
                        <p>
                            <b>Correct Answer:</b> Value = {evaluation.correct_answer.root_value},
                            Visited Nodes = {evaluation.correct_answer.visited_nodes}
                        </p>
                    )}
                </div>
            )}
        </div>
    );
}

export default MinMaxProblem;