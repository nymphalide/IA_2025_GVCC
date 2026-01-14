from typing import Dict, Any

from app.schemas.strategy_schemas import StrategyAnswerRequest, StrategyEvaluationResponse
from app.logic.strategy.generator import generate_strategy_problem


def evaluate_strategy_answer(
    user_answer: StrategyAnswerRequest,
    generation_params: Dict[str, Any]
) -> StrategyEvaluationResponse:
    """
    Reconstruiește problema pe baza seed + params și evaluează răspunsul utilizatorului.
    """

    # Regenerăm problema EXACT
    correct_data = generate_strategy_problem(
        seed=user_answer.problem_seed,
        params=generation_params
    )

    correct_strategy = correct_data["correct"]
    user_strategy = user_answer.chosen_strategy

    # Evaluare strictă (simplă și robustă)
    if user_strategy == correct_strategy:
        return StrategyEvaluationResponse(
            percentage=100,
            correct_answer=correct_strategy,
            explanation="Strategia aleasă este corectă pentru această instanță."
        )
    else:
        return StrategyEvaluationResponse(
            percentage=0,
            correct_answer=correct_strategy,
            explanation=(
                f"Strategia aleasă este greșită. "
                f"Ai ales {user_strategy}, dar strategia recomandată este {correct_strategy}."
            )
        )
