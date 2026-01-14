# app/api/strategy/routes.py
from fastapi import APIRouter

from app.logic.common.seed import get_new_seed
from app.logic.strategy.generator import generate_strategy_problem
from app.logic.strategy.evaluator import evaluate_strategy_answer

from app.schemas.strategy_schemas import (
    StrategyProblemResponse,
    StrategyAnswerRequest,
    StrategyEvaluationResponse,
    StrategyGenerateRequest
)

router = APIRouter()


# ----------------------------
# GENERATE
# ----------------------------

@router.post("/generate/strategy", response_model=StrategyProblemResponse)
async def gen_strategy(request: StrategyGenerateRequest):
    seed = get_new_seed()

    params = request.dict()

    data = generate_strategy_problem(seed, params)

    return StrategyProblemResponse(
        seed=seed,
        problem_name=data["problem_name"],
        description=data["description"],
        options=data["options"],
        difficulty=data["difficulty"]
    )


# ----------------------------
# EVALUATE
# ----------------------------

@router.post("/evaluate/strategy", response_model=StrategyEvaluationResponse)
async def eval_strategy(user_answer: StrategyAnswerRequest):
    # Reconstruim EXACT parametrii de generare (ca la MinMax)

    reconstruction_params = {
        "random_problem": user_answer.generated_random_problem,
        "problem_type": user_answer.generated_problem_type,
        "random_instance": user_answer.generated_random_instance,

        "n": user_answer.generated_n,
        "board_size": user_answer.generated_board_size,
        "vertices": user_answer.generated_vertices,
        "density": user_answer.generated_density,
        "n_disks": user_answer.generated_n_disks,
        "n_pegs": user_answer.generated_n_pegs,
    }

    return evaluate_strategy_answer(
        user_answer=user_answer,
        generation_params=reconstruction_params
    )
