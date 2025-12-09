# app/api/nqueens_evaluation.py

from fastapi import APIRouter
from app.schemas.nqueens_schemas import (
    NQueensAnswerRequest,
    NQueensEvaluationResponse
)
from app.logic.nqueens_generator import generate_nqueens_problem
from app.logic.nqueens_evaluator import evaluate_nqueens_answer

router = APIRouter()

@router.post("/evaluate/nqueens", response_model=NQueensEvaluationResponse)
async def evaluate_nqueens_endpoint(answer: NQueensAnswerRequest):

    # reconstruieste problema doar pe baza seed-ului
    problem = generate_nqueens_problem(seed=answer.problem_seed)
    correct_solution = problem["solution"]

    return evaluate_nqueens_answer(answer, correct_solution)
