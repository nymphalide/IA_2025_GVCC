# app/api/strategy_generation.py
from fastapi import APIRouter
from app.logic.seed_generator import get_new_seed
from app.logic.strategy_generator import generate_strategy_problem
from app.schemas.strategy_schemas import StrategyProblemResponse

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
