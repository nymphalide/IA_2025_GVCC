from fastapi import APIRouter
from app.logic.common.seed import get_new_seed
from app.logic.csp.solver import generate_csp_problem
from app.logic.csp.evaluator import evaluate_csp
from app.schemas.csp_schemas import (
    CspProblemResponse, CspGenerateRequest, 
    CspAnswerRequest, CspEvaluationResponse, CspText
)

router = APIRouter()

@router.post("/generate/csp", response_model=CspProblemResponse)
async def generate_csp(request: CspGenerateRequest):
    new_seed = get_new_seed()
    params = request.dict()
    data = generate_csp_problem(new_seed, params)
    
    return CspProblemResponse(
        seed=data["seed"],
        graph=data["graph"],
        domains=data["domains"],
        assignments=data["assignments"],
        all_variables=data["all_variables"],
        available_colors=data["available_colors"],
        algorithm_name=data["algorithm_name"],
        text=CspText(**data["text"]),
        difficulty=data["difficulty"]
    )

@router.post("/evaluate/csp", response_model=CspEvaluationResponse)
async def evaluate_csp_endpoint(user_answer: CspAnswerRequest):
    return evaluate_csp(user_answer)