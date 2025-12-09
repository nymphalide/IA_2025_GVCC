# app/logic/nqueens_evaluator.py

from app.schemas.nqueens_schemas import NQueensEvaluationResponse

def evaluate_nqueens_answer(user_answer, correct_solution):

    user_config = user_answer.configuration

    # dimensiune greșită
    if len(user_config) != len(correct_solution):
        return NQueensEvaluationResponse(
            percentage=0,
            correct_answer={"solution": correct_solution},
            explanation="Configurația are o dimensiune greșită."
        )

    # complet corect
    if user_config == correct_solution:
        return NQueensEvaluationResponse(
            percentage=100,
            correct_answer={"solution": correct_solution},
            explanation="Configurația introdusă este complet corectă."
        )

    # scor parțial
    correct_positions = sum(
        1 for uc, cc in zip(user_config, correct_solution) if uc == cc
    )
    percentage = int((correct_positions / len(correct_solution)) * 100)

    return NQueensEvaluationResponse(
        percentage=percentage,
        correct_answer={"solution": correct_solution},
        explanation=f"Ați plasat corect {correct_positions}/{len(correct_solution)} regine."
    )
