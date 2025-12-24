from typing import List, Tuple
from app.schemas.nash_schemas import NashAnswerRequest, NashEvaluationResponse


def evaluate_nash(user_answer: NashAnswerRequest, correct_equilibria: List[Tuple[int, int]]) -> NashEvaluationResponse:
    """
    Compares the user's answer against the calculated correct equilibria.
    Returns a structured NashEvaluationResponse.
    """
    has_eq_correct = (len(correct_equilibria) > 0)
    percentage = 0
    explanation = ""

    if user_answer.has_equilibrium:
        if not has_eq_correct:
            percentage = 0
            explanation = "Greșit. Nu există niciun Echilibru Nash Pur în această matrice."
        else:
            if user_answer.equilibrium_point:
                # Convert list/tuple from Pydantic to a standard tuple for comparison
                user_pt = (
                    user_answer.equilibrium_point[0],
                    user_answer.equilibrium_point[1]
                )

                if user_pt in correct_equilibria:
                    percentage = 100
                    explanation = f"Corect! Punctul {user_pt} este un Echilibru Nash."
                else:
                    percentage = 50
                    explanation = (
                        f"Parțial corect. Există un echilibru, dar coordonatele {user_pt} "
                        f"sunt greșite. Soluții posibile: {correct_equilibria}"
                    )
            else:
                percentage = 50
                explanation = "Parțial corect. Există echilibru, dar nu ați specificat coordonatele."
    else:
        # User said NO equilibrium
        if not has_eq_correct:
            percentage = 100
            explanation = "Corect! Nu există niciun Echilibru Nash Pur."
        else:
            percentage = 0
            explanation = f"Greșit. Există cel puțin un echilibru la: {correct_equilibria}"

    return NashEvaluationResponse(
        percentage=percentage,
        correct_answer=correct_equilibria,
        explanation=explanation
    )