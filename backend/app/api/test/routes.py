from fastapi import APIRouter, HTTPException
from app.schemas.test_schema import TestRequest, TestResponse
import random

router = APIRouter(prefix="/test", tags=["Test"])

QUESTION_TYPES = {
    "minmax": "minmax",
    "nash": "nash",
    "strategy": "strategy",
    "rl": "rl",
    "csp": "csp",
    "bayes": "bayes",
}


@router.post("/", response_model=TestResponse)
def generate_test(request: TestRequest):
    selected = [
        name for name, key in QUESTION_TYPES.items()
        if getattr(request, name)
    ]

    if not selected:
        raise HTTPException(
            status_code=400,
            detail="At least one question type must be selected."
        )

    n = request.num_questions
    k = len(selected)

    if n <= 0:
        raise HTTPException(
            status_code=400,
            detail="Number of questions must be > 0."
        )

    questions = []

    # cazul: n >= număr capitole bifate
    if n >= k:
        questions.extend(selected)  # minim una din fiecare
        remaining = n - k
        questions.extend(random.choices(selected, k=remaining))
    else:
        # cazul: n < capitole bifate → random subset
        questions.extend(random.sample(selected, k=n))

    random.shuffle(questions)

    return TestResponse(
        questions=[
            {"type": q, "mode": "random"} for q in questions
        ]
    )

