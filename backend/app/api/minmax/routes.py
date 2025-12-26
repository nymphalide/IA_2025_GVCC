from fastapi import APIRouter

from app.logic.common.seed import get_new_seed
from app.logic.minmax.solver import generate_and_solve_minmax
from app.logic.minmax.visualizer import generate_tree_image_base64
from app.logic.minmax.evaluator import evaluate_minmax

from app.schemas.minmax_schemas import (
    MinMaxProblemResponse,
    MinMaxAnswerRequest,
    EvaluationResponse,
    MinMaxProblemText,
    MinMaxGenerateRequest
)

router = APIRouter()


@router.post("/generate/minmax", response_model=MinMaxProblemResponse)
async def generate_minmax_problem(request: MinMaxGenerateRequest):
    """
    Generează o problemă MinMax. 
    Acceptă parametri de configurare (depth, root type).
    """
    new_seed = get_new_seed()

    # Convertim modelul Pydantic în dicționar pentru solver
    params = request.dict()

    tree_structure, _, _, chosen_depth, text_dict, root_type_str = generate_and_solve_minmax(
        seed=new_seed,
        params=params
    )

    tree_image_b64 = generate_tree_image_base64(
        tree_structure.model_dump()
    )

    return MinMaxProblemResponse(
        seed=new_seed,
        tree=tree_structure,
        difficulty=f"L6_Depth{chosen_depth}",
        tree_image_base64=tree_image_b64,
        text=MinMaxProblemText(**text_dict),
        root_type=root_type_str
    )


@router.post("/evaluate/minmax", response_model=EvaluationResponse)
async def evaluate_minmax_answer(user_answer: MinMaxAnswerRequest):
    """
    Evaluează răspunsul utilizatorului.
    Reconstruiește problema folosind seed-ul ȘI parametrii originali de generare
    pentru a asigura că arborele evaluat este identic cu cel afișat utilizatorului.
    """
    
    # Reconstruim dicționarul de parametri pe baza datelor primite de la frontend
    # Acest lucru rezolvă problema desincronizării când utilizatorul alege manual MIN/MAX sau Adâncimea.
    reconstruction_params = {
        "random_depth": user_answer.generated_random_depth,
        "depth": user_answer.generated_depth,
        "random_root": user_answer.generated_random_root,
        "is_maximizing_player": user_answer.generated_is_maximizing
    }

    # Apelăm solverul cu parametrii de reconstrucție
    _, correct_root_value, correct_visited_nodes, _, _, _ = generate_and_solve_minmax(
        seed=user_answer.problem_seed,
        params=reconstruction_params
    )

    evaluation = evaluate_minmax(
        user_answer=user_answer,
        correct_value=correct_root_value,
        correct_nodes=correct_visited_nodes
    )

    return evaluation