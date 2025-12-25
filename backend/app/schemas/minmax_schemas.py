from pydantic import BaseModel
from typing import List, Optional, Dict, Any

# --- Sub-schemas for Text Content ---
class MinMaxProblemText(BaseModel):
    title: str
    description: str
    requirement: str

# --- Contractul API (Modele Pydantic) ---

# Folosim recursivitate pentru a defini structura arborelui
class MinMaxNode(BaseModel):
    name: str
    node_type: str  # "MIN" sau "MAX"
    value: Optional[int] = None
    children: List['MinMaxNode'] = []

# Actualizăm modelul pentru a se valida corect recursiv
MinMaxNode.update_forward_refs()


# --- Request Body for Generation ---
class MinMaxGenerateRequest(BaseModel):
    random_depth: bool = True
    depth: Optional[int] = None
    random_root: bool = True
    is_maximizing_player: Optional[bool] = None  # True = MAX, False = MIN


class MinMaxProblemResponse(BaseModel):
    seed: int
    tree: MinMaxNode
    difficulty: str = "EASY"
    tree_image_base64: Optional[str] = None
    text: MinMaxProblemText
    root_type: str = "MAX" 

    class Config:
        orm_mode = True 


class MinMaxAnswerRequest(BaseModel):
    """Ce trimite Frontend-ul când utilizatorul răspunde."""
    problem_seed: int
    root_value: int
    visited_nodes: int
    
    # --- MODIFICARE: Adăugăm parametrii de configurare pentru reconstrucția fidelă ---
    # Aceștia sunt necesari pentru ca validatorul să știe dacă userul a forțat anumite setări
    generated_random_depth: bool = True
    generated_depth: Optional[int] = None
    generated_random_root: bool = True
    generated_is_maximizing: Optional[bool] = None


class EvaluationResponse(BaseModel):
    percentage: int
    correct_answer: Dict[str, Any]
    explanation: str