# app/schemas/strategy_schemas.py
from pydantic import BaseModel
from typing import List, Dict

class StrategyProblemResponse(BaseModel):
    seed: int
    problem_name: str
    description: str
    options: List[str]   # BFS, DFS, A*, Hill-Climbing, Backtracking
    difficulty: str

class StrategyAnswerRequest(BaseModel):
    problem_seed: int
    chosen_strategy: str

class StrategyEvaluationResponse(BaseModel):
    percentage: int
    correct_answer: str
    explanation: str
