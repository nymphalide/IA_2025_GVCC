from fastapi import APIRouter
from app.logic.common.seed import get_new_seed
from app.logic.rl.solver import generate_rl_problem
from app.logic.rl.evaluator import evaluate_rl

from app.schemas.rl_schemas import (
    RLGenerateRequest,
    RLProblemResponse,
    ProblemText,
    RLAnswerRequest,
    RLEvaluationResponse
)

router = APIRouter()


@router.post("/generate/rl", response_model=RLProblemResponse)
async def gen_rl(request: RLGenerateRequest):
    new_seed = get_new_seed()

    params = request.dict()
    grid, q_data, text_dict, target, _ = generate_rl_problem(new_seed, params)

    return RLProblemResponse(
        seed=new_seed,
        grid=grid,
        q_data=q_data,
        text=ProblemText(**text_dict),
        question_target=target
    )


@router.post("/evaluate/rl", response_model=RLEvaluationResponse)
async def eval_rl(request: RLAnswerRequest):
    """
    Evaluează răspunsul RL.
    Folosește parametrii din request (ex: Gamma, Alpha) pentru a regenera valoarea corectă.
    """

    # Construim dicționarul de parametri pentru solver
    reconstruction_params = {
        "type": request.problem_type,
        "rows": request.rows,
        "cols": request.cols,
        "gamma": request.gamma,
        "step_reward": request.step_reward,
        "alpha": request.alpha
    }

    # Regenerăm problema
    _, _, _, _, correct_val = generate_rl_problem(request.problem_seed, reconstruction_params)

    return evaluate_rl(request.user_value, correct_val)