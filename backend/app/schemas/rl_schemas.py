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
    type: str = "value_iteration"  # "value_iteration" sau "q_learning"
    rows: int = 3
    cols: int = 4
    gamma: float = 0.9
    step_reward: float = -0.04
    alpha: float = 0.1  # Doar pt Q-Learning


class RLProblemResponse(BaseModel):
    seed: int
    grid: Optional[GridConfig] = None
    q_data: Optional[Dict[str, Any]] = None
    text: ProblemText
    question_target: str


class RLAnswerRequest(BaseModel):
    """
    Payload trimis la evaluare.
    Trebuie să conțină TOȚI parametrii fizici pentru a recalcula corect valoarea (ex: Gamma=1.0).
    """
    problem_seed: int
    problem_type: str
    user_value: float

    # Parametri de reconstrucție
    rows: int = 3
    cols: int = 4
    gamma: float = 0.9
    step_reward: float = -0.04
    alpha: float = 0.1


class RLEvaluationResponse(BaseModel):
    percentage: int
    correct_value: float
    explanation: str