# app/schemas/strategy_schemas.py
from pydantic import BaseModel
from typing import List, Optional


# ----------------------------
# GENERATE
# ----------------------------

class StrategyGenerateRequest(BaseModel):
    # Alegere problemă
    random_problem: bool = True
    problem_type: Optional[str] = None  # "nqueens", "knight", "graph_coloring", "hanoi"

    # Alegere instanță
    random_instance: bool = True

    # Parametri specifici (folosiți doar dacă random_instance = False)
    n: Optional[int] = None  # N-Queens
    board_size: Optional[int] = None  # Knight
    vertices: Optional[int] = None  # Graph coloring
    density: Optional[float] = None  # Graph coloring
    n_disks: Optional[int] = None  # Hanoi
    n_pegs: Optional[int] = None  # Hanoi


# ----------------------------
# PROBLEM RESPONSE
# ----------------------------

class StrategyProblemResponse(BaseModel):
    seed: int
    problem_name: str
    description: str
    options: List[str]   # BFS, DFS, A*, Hill-Climbing, Backtracking
    difficulty: str


# ----------------------------
# ANSWER / EVALUATE
# ----------------------------

class StrategyAnswerRequest(BaseModel):
    problem_seed: int
    chosen_strategy: str

    # --- PARAMETRII FOLOSIȚI LA GENERARE (pentru reconstrucție exactă) ---
    generated_random_problem: bool
    generated_problem_type: Optional[str]

    generated_random_instance: bool

    generated_n: Optional[int] = None
    generated_board_size: Optional[int] = None
    generated_vertices: Optional[int] = None
    generated_density: Optional[float] = None
    generated_n_disks: Optional[int] = None
    generated_n_pegs: Optional[int] = None


# ----------------------------
# EVALUATION RESPONSE
# ----------------------------

class StrategyEvaluationResponse(BaseModel):
    percentage: int
    correct_answer: str
    explanation: str
