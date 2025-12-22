from fastapi import APIRouter

from fastapi import APIRouter

from app.logic.common.seed import get_new_seed
from app.logic.strategy.generator import generate_strategy_problem
from app.logic.strategy.evaluator import evaluate_strategy_answer

from app.schemas.strategy_schemas import (
    StrategyProblemResponse,
    StrategyAnswerRequest,
    StrategyEvaluationResponse
)


router = APIRouter()


@router.post("/generate/strategy", response_model=StrategyProblemResponse)
async def gen_strategy():
    seed = get_new_seed()
    data = generate_strategy_problem(seed)

    return StrategyProblemResponse(
        seed=seed,
        problem_name=data["problem_name"],
        description=data["description"],
        options=data["options"],
        difficulty=data["difficulty"]
    )


@router.post("/evaluate/strategy", response_model=StrategyEvaluationResponse)
async def eval_strategy(user_answer: StrategyAnswerRequest):
    correct_data = generate_strategy_problem(
        user_answer.problem_seed
    )

    correct_strategy = correct_data["correct"]

    return evaluate_strategy_answer(
        user_answer=user_answer,
        correct_answer=correct_strategy
    )
