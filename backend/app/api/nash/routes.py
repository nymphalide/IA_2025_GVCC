from fastapi import APIRouter

from fastapi import APIRouter

from app.logic.common.seed import get_new_seed
from app.logic.nash.solver import generate_and_solve_nash

from app.schemas.nash_schemas import (
    NashProblemResponse,
    NashAnswerRequest,
    NashEvaluationResponse
)


router = APIRouter()


@router.post("/generate/nash", response_model=NashProblemResponse)
async def generate_nash_problem():
    new_seed = get_new_seed()

    matrix_obj, _ = generate_and_solve_nash(
        seed=new_seed
    )

    return NashProblemResponse(
        seed=new_seed,
        matrix=matrix_obj,
        difficulty=f"{matrix_obj.rows}x{matrix_obj.cols}"
    )


@router.post("/evaluate/nash", response_model=NashEvaluationResponse)
async def evaluate_nash_answer(user_answer: NashAnswerRequest):
    _, correct_equilibria = generate_and_solve_nash(
        seed=user_answer.problem_seed
    )

    has_eq_correct = (len(correct_equilibria) > 0)
    percentage = 0
    explanation = ""

    if user_answer.has_equilibrium:
        if not has_eq_correct:
            percentage = 0
            explanation = "Greșit. Nu există niciun Echilibru Nash Pur în această matrice."
        else:
            if user_answer.equilibrium_point:
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
