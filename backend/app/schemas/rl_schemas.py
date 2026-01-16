from pydantic import BaseModel
from typing import List, Tuple, Dict, Optional, Any


# --- Shared Structures ---

class GridConfig(BaseModel):
    rows: int
    cols: int
    walls: List[Tuple[int, int]]  # Coordonate pereți [(1,1), ...]
    terminals: Dict[str, float]  # "row,col": reward (ex: "0,3": 1.0)
    step_reward: float
    gamma: float


class ProblemText(BaseModel):
    title: str
    description: str
    requirement: str


# --- Requests / Responses ---

class RLGenerateRequest(BaseModel):
    type: str = "value_iteration"

    # Value Iteration specific
    rows: int = 3
    cols: int = 4

    # Parameters with Randomization options
    gamma: float = 0.9
    random_gamma: bool = True  # <--- NEW

    step_reward: float = -0.04
    random_step_reward: bool = True  # <--- NEW

    alpha: float = 0.1
    random_alpha: bool = True  # <--- NEW


class RLProblemResponse(BaseModel):
    seed: int
    grid: Optional[GridConfig] = None
    q_data: Optional[Dict[str, Any]] = None
    text: ProblemText
    question_target: str


class RLAnswerRequest(BaseModel):
    problem_seed: int
    problem_type: str
    user_value: float

    # Reconstruction parameters
    rows: int = 3
    cols: int = 4

    # We pass the EXACT values used in the problem (resolved from random)
    gamma: float
    step_reward: float
    alpha: float


class RLEvaluationResponse(BaseModel):
    percentage: int
    correct_value: float
    explanation: str