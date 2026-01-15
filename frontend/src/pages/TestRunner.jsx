import {useState} from "react";
import MinMaxProblem from "../components/MinMax/MinMaxProblem";
import NashProblem from "../components/Nash/NashProblem";
import StrategyProblem from "../components/Strategy/StrategyProblem";
import RLProblem from "../components/RL/RLProblem";
import CspProblem from "../components/Csp/CspProblem";
import BayesProblem from "../components/Bayes/BayesProblem";


export default function TestRunner() {
    const test = JSON.parse(localStorage.getItem("currentTest")) || [];
    const [index, setIndex] = useState(
        Number(localStorage.getItem("currentIndex") || 0)
    );

    if (!test.length) {
        return <div>No test loaded</div>;
    }

    if (index >= test.length) {
        return <div>Test finished</div>;
    }

    const current = test[index];

    const next = () => {
        const nextIndex = index + 1;
        localStorage.setItem("currentIndex", String(nextIndex));
        setIndex(nextIndex);
    };

    return (
        <div className="page">
            <h2>
                Problem {index + 1} / {test.length} — {current.type.toUpperCase()}
            </h2>

            <div style={{marginBottom: "1rem"}}>
                {current.type === "minmax" && (
                    <MinMaxProblem
                        key={current.seed}
                        autoGenerate={current.mode === "random"}
                        seed={current.seed}
                    />

                )}


                {current.type === "nash" && (
                    <NashProblem
                        key={current.seed}
                        autoGenerate={current.mode === "random"}
                        seed={current.seed}
                    />
                )}


                {current.type === "strategy" && (
                    <StrategyProblem
                        key={current.seed}
                        autoGenerate={current.mode === "random"}
                        seed={current.seed}
                    />
                )}


                {current.type === "rl" && (
                    <RLProblem
                        key={current.seed}
                        autoGenerate={current.mode === "random"}
                        seed={current.seed}
                    />
                )}


                {current.type === "csp" && (
                    <CspProblem
                        key={current.seed}
                        autoGenerate={current.mode === "random"}
                        seed={current.seed}
                    />
                )}

                {current.type === "bayes" && (
                    <BayesProblem
                        key={current.seed}
                        autoGenerate={current.mode === "random"}
                        seed={current.seed}
                    />
                )}


            </div>

            <button className="primary-btn" onClick={next}>
                Next
            </button>
        </div>
    );
}
