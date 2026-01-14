from pydantic import BaseModel
from typing import Optional

class BayesGenerateResponse(BaseModel):
    problem: dict
    question: str


class BayesEvaluateRequest(BaseModel):
    correct_answer: float
    user_answer: float


class BayesEvaluateResponse(BaseModel):
    score: float

class BayesGenerateRequest(BaseModel):
    random: bool = True
    p_rain: Optional[float] = None
    p_sprinkler: Optional[float] = None
