import {useState} from "react";

export default function Test() {
    const [numQuestions, setNumQuestions] = useState(6);
    const [checks, setChecks] = useState({
        minmax: false,
        nash: false,
        strategy: false,
        rl: false,
        csp: false,
        bayes: false,
    });

    const [result, setResult] = useState(null);

    const toggle = (key) => {
        setChecks({...checks, [key]: !checks[key]});
    };

    const submit = async () => {
        const payload = {
            num_questions: numQuestions,
            ...checks,
        };

        const res = await fetch("http://localhost:8000/api/test", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify(payload),
        });

        const data = await res.json();
        const withSeeds = data.questions.map(q => ({
            ...q,
            seed: Math.floor(Math.random() * 1_000_000),
            mode: "random" // default
        }));


        setResult(withSeeds);

    };
    const toggleCustom = (index) => {
        setResult(prev =>
            prev.map((q, i) =>
                i === index
                    ? {...q, mode: q.mode === "random" ? "custom" : "random"}
                    : q
            )
        );
    };

    return (
        <div className="page">
            <h2>Generate Test</h2>

            <label>
                Number of questions
                <input
                    type="number"
                    min="1"
                    value={numQuestions}
                    onChange={(e) => setNumQuestions(Number(e.target.value))}
                />
            </label>

            <div className="checkbox-group">
                {Object.keys(checks).map((k) => (
                    <label key={k}>
                        <input
                            type="checkbox"
                            checked={checks[k]}
                            onChange={() => toggle(k)}
                        />
                        {k.toUpperCase()}
                    </label>
                ))}
            </div>

            <button className="primary-btn" onClick={submit}>
                Generate
            </button>

            {result && (
                <div className="result">
                    <h3>Generated test</h3>
                    <ul>
                        {result.map((q, i) => (
                            <li key={i}>
                                {i + 1}. {q.type.toUpperCase()}

                                <label style={{marginLeft: "1rem"}}>
                                    <input
                                        type="checkbox"
                                        checked={q.mode === "custom"}
                                        onChange={() => toggleCustom(i)}
                                    />
                                    Custom
                                </label>
                            </li>
                        ))}
                    </ul>


                    <button
                        className="primary-btn"
                        onClick={() => {
                            localStorage.setItem("currentTest", JSON.stringify(result));
                            localStorage.setItem("currentIndex", "0");
                            window.location.href = "/test/run";
                        }}
                    >
                        Next
                    </button>
                </div>
            )}
        </div>
    );

}
