from pydantic import BaseModel
from typing import List

class TestRequest(BaseModel):
    num_questions: int

    minmax: bool = False
    nash: bool = False
    strategy: bool = False
    rl: bool = False
    csp: bool = False
    bayes: bool = False

class TestQuestion(BaseModel):
    type: str
    mode: str  # random | custom (mai târziu)

class TestResponse(BaseModel):
    questions: List[TestQuestion]
