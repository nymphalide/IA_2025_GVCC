from fastapi import APIRouter, Body

from app.logic.common.seed import get_new_seed
from app.logic.nash.solver import generate_and_solve_nash
from app.logic.nash.evaluator import evaluate_nash

from app.schemas.nash_schemas import (
    NashProblemResponse,
    NashAnswerRequest,
    NashEvaluationResponse,
    NashGenerateRequest,
    ProblemText
)

router = APIRouter()


@router.post("/generate/nash", response_model=NashProblemResponse)
async def generate_nash_problem(request: NashGenerateRequest):
    """
    Generates a Nash problem based on user preferences.
    """
    new_seed = get_new_seed()

    # Pass the request parameters to the solver
    params = {
        "rows": request.rows,
        "cols": request.cols,
        "random_size": request.random_size
    }

    matrix_obj, _, text_dict = generate_and_solve_nash(
        seed=new_seed,
        params=params
    )

    return NashProblemResponse(
        seed=new_seed,
        matrix=matrix_obj,
        text=ProblemText(**text_dict),
        difficulty=f"{matrix_obj.rows}x{matrix_obj.cols}"
    )


@router.post("/evaluate/nash", response_model=NashEvaluationResponse)
async def evaluate_nash_answer(user_answer: NashAnswerRequest):
    """
    Evaluează răspunsul utilizatorului.
    Reconstruiește problema folosind Seed-ul + Parametrii trimiși de frontend.
    """

    # Reconstruim parametrii originali
    reconstruction_params = {
        "rows": user_answer.rows,
        "cols": user_answer.cols,
        "random_size": user_answer.random_size
    }

    # Regenerăm soluția corectă folosind aceeași configurație
    _, correct_equilibria, _ = generate_and_solve_nash(
        seed=user_answer.problem_seed,
        params=reconstruction_params
    )

    return evaluate_nash(
        user_answer=user_answer,
        correct_equilibria=correct_equilibria
    )