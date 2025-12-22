from app.schemas.strategy_schemas import StrategyEvaluationResponse


def evaluate_strategy_answer(user_answer, correct_answer):
    user_selected = user_answer.chosen_strategy

    if user_selected == correct_answer:
        return StrategyEvaluationResponse(
            percentage=100,
            correct_answer=correct_answer,
            explanation="Răspuns corect."
        )

    return StrategyEvaluationResponse(
        percentage=0,
        correct_answer=correct_answer,
        explanation="Strategia selectată este incorectă."
    )
