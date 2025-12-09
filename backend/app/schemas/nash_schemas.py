from pydantic import BaseModel
from typing import List, Tuple, Optional, Any

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

class NashProblemResponse(BaseModel):
    """Ce trimite API-ul când se cere o problemă Nash."""
    seed: int
    matrix: NashMatrix
    difficulty: str = "Medium"

class NashAnswerRequest(BaseModel):
    """Ce trimite Frontend-ul când utilizatorul răspunde."""
    problem_seed: int
    has_equilibrium: bool
    # Coordonate opționale: [row_index, col_index] dacă există
    equilibrium_point: Optional[Tuple[int, int]] = None

class NashEvaluationResponse(BaseModel):
    """Ce răspunde API-ul după evaluare."""
    percentage: int
    correct_answer: Any # Poate fi un mesaj sau o listă de echilibre
    explanation: str