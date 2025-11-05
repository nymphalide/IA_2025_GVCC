from pydantic import BaseModel
from typing import List, Optional, Dict, Any

# --- Contractul API (Modele Pydantic) ---

# Folosim recursivitate pentru a defini structura arborelui
class MinMaxNode(BaseModel):
    name: str
    value: Optional[int] = None
    children: List['MinMaxNode'] = []

# Actualizăm modelul pentru a se valida corect recursiv
MinMaxNode.update_forward_refs()


class MinMaxProblemResponse(BaseModel):
    """Ce trimite API-ul când se cere o problemă MinMax."""
    seed: int
    tree: MinMaxNode
    difficulty: str = "EASY" # Placeholder pentru viitor
    tree_image_base64: Optional[str] = None

    class Config:
        orm_mode = True # Permite maparea la modele ORM (dacă e cazul)


class MinMaxAnswerRequest(BaseModel):
    """Ce trimite Frontend-ul când utilizatorul răspunde."""
    problem_seed: int
    root_value: int
    visited_nodes: int


class EvaluationResponse(BaseModel):
    """Ce răspunde API-ul după evaluare."""
    percentage: int
    correct_answer: Dict[str, Any]
    explanation: str