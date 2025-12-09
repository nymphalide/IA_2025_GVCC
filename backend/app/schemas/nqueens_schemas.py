# app/schemas/nqueens_schemas.py

from pydantic import BaseModel
from typing import List, Dict, Any


class NQueensProblemResponse(BaseModel):
    seed: int
    n: int
    board_description: str
    difficulty: str
    # NU trimitem soluția corectă
    # doar pentru debug, dacă vrei
    solution_preview: str | None = None


class NQueensAnswerRequest(BaseModel):
    problem_seed: int
    configuration: List[int]  # ex: [1, 3, 0, 2]


class NQueensEvaluationResponse(BaseModel):
    percentage: int
    correct_answer: Dict[str, Any]
    explanation: str
