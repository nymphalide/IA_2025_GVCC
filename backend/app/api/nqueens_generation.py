# app/api/nqueens_generation.py

from fastapi import APIRouter
from app.logic.seed_generator import get_new_seed
from app.logic.nqueens_generator import generate_nqueens_problem
from app.schemas.nqueens_schemas import NQueensProblemResponse

router = APIRouter()

@router.post("/generate/nqueens", response_model=NQueensProblemResponse)
async def generate_nqueens_problem_endpoint():

    seed = get_new_seed()
    data = generate_nqueens_problem(seed=seed)

    return NQueensProblemResponse(
        seed=seed,
        n=data["n"],
        board_description=data["board_description"],
        difficulty=data["difficulty"],
        solution_preview=data["solution_preview"]
    )
