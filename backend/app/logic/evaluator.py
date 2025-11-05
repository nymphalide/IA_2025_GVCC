from app.schemas.minmax_schemas import MinMaxAnswerRequest, EvaluationResponse
from typing import Dict, Any

def evaluate_minmax(user_answer: MinMaxAnswerRequest, correct_value: int, correct_nodes: int) -> EvaluationResponse:
    """
    Evaluează răspunsul utilizatorului pentru MinMax.
    50% pentru valoarea corectă, 50% pentru numărul corect de noduri vizitate.
    """
    percentage = 0
    explanation = ""
    
    # Verifică valoarea rădăcinii (50%)
    if user_answer.root_value == correct_value:
        percentage += 50
        explanation += "Valoarea rădăcinii este corectă. "
    else:
        explanation += f"Valoarea rădăcinii este greșită (Trimis: {user_answer.root_value}, Corect: {correct_value}). "
        
    # Verifică numărul de noduri vizitate (50%)
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