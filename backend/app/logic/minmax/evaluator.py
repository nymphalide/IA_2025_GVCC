from typing import Dict, Any
from app.schemas.minmax_schemas import MinMaxAnswerRequest, EvaluationResponse


def evaluate_minmax(user_answer: MinMaxAnswerRequest, correct_value: int, correct_nodes: int) -> EvaluationResponse:
    percentage = 0
    explanation = ""

    if user_answer.root_value == correct_value:
        percentage += 50
        explanation += "Valoarea rădăcinii este corectă. "
    else:
        explanation += f"Valoarea rădăcinii este greșită (Trimis: {user_answer.root_value}, Corect: {correct_value}). "

    if user_answer.visited_nodes == correct_nodes:
        percentage += 50
        explanation += "Numărul de noduri frunză vizitate este corect."
    else:
        explanation += f"Numărul de noduri vizitate este greșit (Trimis: {user_answer.visited_nodes}, Corect: {correct_nodes})."

    correct_answer_dict: Dict[str, Any] = {
        "root_value": correct_value,
        "visited_nodes": correct_nodes
    }

    return EvaluationResponse(
        percentage=percentage,
        correct_answer=correct_answer_dict,
        explanation=explanation
    )
