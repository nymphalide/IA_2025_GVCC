from pydantic import BaseModel
from typing import List, Tuple, Optional, Any


# --- Sub-schemas for Text Content ---
class ProblemText(BaseModel):
    title: str
    description: str
    requirement: str


# --- Modele de Date (Pydantic) ---

class NashMatrix(BaseModel):
    """
    Reprezintă matricea de plăți (Payoff Matrix).
    rows: Numărul de rânduri (Strategii Jucător 1)
    cols: Numărul de coloane (Strategii Jucător 2)
    grid: O listă de liste de tupluri.
          Ex: grid[row][col] = (payoff_p1, payoff_p2)
    """
    rows: int
    cols: int
    grid: List[List[Tuple[int, int]]]


# --- Request Body for Generation ---
class NashGenerateRequest(BaseModel):
    rows: int = 3
    cols: int = 3
    random_size: bool = False


class NashProblemResponse(BaseModel):
    """Ce trimite API-ul când se cere o problemă Nash."""
    seed: int
    matrix: NashMatrix
    text: ProblemText
    difficulty: str = "Custom"


class NashAnswerRequest(BaseModel):
    """
    Ce trimite Frontend-ul când utilizatorul răspunde.
    Include acum și parametrii de configurare pentru a asigura reproductibilitatea.
    """
    problem_seed: int
    has_equilibrium: bool
    equilibrium_point: Optional[Tuple[int, int]] = None

    # Parametri necesari pentru reconstrucția exactă a problemei
    rows: int = 3
    cols: int = 3
    random_size: bool = False


class NashEvaluationResponse(BaseModel):
    """Ce răspunde API-ul după evaluare."""
    percentage: int
    correct_answer: Any
    explanation: str