from pydantic import BaseModel


class BayesGenerateResponse(BaseModel):
    problem: dict
    question: str


class BayesEvaluateRequest(BaseModel):
    correct_answer: float
    user_answer: float


class BayesEvaluateResponse(BaseModel):
    score: float
