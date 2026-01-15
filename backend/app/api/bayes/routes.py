from fastapi import APIRouter
from app.logic.bayes.solver import generate_bayes_problem
from app.logic.bayes.evaluator import evaluate_bayes_answer
from app.logic.bayes.strings import generate_problem_text
from app.schemas.bayes_schemas import (
    BayesGenerateRequest,
    BayesGenerateResponse,
    BayesEvaluateRequest,
    BayesEvaluateResponse
)

router = APIRouter()


@router.post("/generate", response_model=BayesGenerateResponse)
def generate_bayes(data: BayesGenerateRequest):
    custom_priors = None

    if data.p_rain is not None and data.p_sprinkler is not None:
        custom_priors = {
            "p_rain": data.p_rain,
            "p_sprinkler": data.p_sprinkler
        }

    problem, solution = generate_bayes_problem(
        custom_priors=custom_priors
    )

    return {
        "problem": {
            **problem,
            "solution": solution
        },
        "question": generate_problem_text(problem)
    }

@router.post("/evaluate", response_model=BayesEvaluateResponse)
def evaluate_bayes(data: BayesEvaluateRequest):
    score = evaluate_bayes_answer(
        correct=data.correct_answer,
        user_answer=data.user_answer
    )
    return {"score": score}
