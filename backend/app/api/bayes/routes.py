from fastapi import APIRouter
from app.logic.bayes.solver import generate_bayes_problem
from app.logic.bayes.evaluator import evaluate_bayes_answer
from app.logic.bayes.strings import generate_problem_text
from app.schemas.bayes_schemas import (
    BayesGenerateResponse,
    BayesEvaluateRequest,
    BayesEvaluateResponse
)

router = APIRouter()


@router.get("/generate", response_model=BayesGenerateResponse)
def generate_bayes(seed: int | None = None):
    problem, solution = generate_bayes_problem(seed)

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
