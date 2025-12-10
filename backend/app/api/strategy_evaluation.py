# app/api/strategy_evaluation.py
from fastapi import APIRouter
from app.logic.seed_generator import get_new_seed
from app.logic.strategy_generator import generate_strategy_problem
from app.logic.strategy_evaluator import evaluate_strategy_answer

from app.schemas.strategy_schemas import (
    StrategyAnswerRequest,
    StrategyEvaluationResponse
)

router = APIRouter()

@router.post("/evaluate/strategy", response_model=StrategyEvaluationResponse)
async def eval_strategy(user_answer: StrategyAnswerRequest):
    correct_data = generate_strategy_problem(user_answer.problem_seed)

    correct_strategy = correct_data["correct"]

    return evaluate_strategy_answer(
        user_answer=user_answer,
        correct_answer=correct_strategy
    )
