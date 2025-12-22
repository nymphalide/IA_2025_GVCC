from fastapi import APIRouter

from app.logic.common.seed import get_new_seed
from app.logic.minmax.solver import generate_and_solve_minmax
from app.logic.minmax.visualizer import generate_tree_image_base64
from app.logic.minmax.evaluator import evaluate_minmax

from app.schemas.minmax_schemas import (
    MinMaxProblemResponse,
    MinMaxAnswerRequest,
    EvaluationResponse
)

router = APIRouter()


@router.post("/generate/minmax", response_model=MinMaxProblemResponse)
async def generate_minmax_problem():
    new_seed = get_new_seed()

    tree_structure, _, _, chosen_depth = generate_and_solve_minmax(
        seed=new_seed
    )

    tree_image_b64 = generate_tree_image_base64(
        tree_structure.model_dump()
    )

    return MinMaxProblemResponse(
        seed=new_seed,
        tree=tree_structure,
        difficulty=f"L6_Depth{chosen_depth}",
        tree_image_base64=tree_image_b64
    )


@router.post("/evaluate/minmax", response_model=EvaluationResponse)
async def evaluate_minmax_answer(user_answer: MinMaxAnswerRequest):
    _, correct_root_value, correct_visited_nodes, _ = generate_and_solve_minmax(
        seed=user_answer.problem_seed
    )

    evaluation = evaluate_minmax(
        user_answer=user_answer,
        correct_value=correct_root_value,
        correct_nodes=correct_visited_nodes
    )

    return evaluation
