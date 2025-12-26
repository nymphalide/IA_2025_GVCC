from pydantic import BaseModel
from typing import List, Dict, Optional, Any

# --- Text Content ---
class CspText(BaseModel):
    title: str
    description: str
    requirement: str
    note: str

# --- Data Models ---

class CspNode(BaseModel):
    id: int
    x: int
    y: int
    label: str

class CspEdge(BaseModel):
    source: int
    target: int

class CspGraph(BaseModel):
    nodes: List[CspNode]
    edges: List[CspEdge]

class CspProblemResponse(BaseModel):
    seed: int
    graph: CspGraph
    domains: Dict[str, List[str]]
    assignments: Dict[str, str]
    all_variables: List[str]
    available_colors: List[str]
    algorithm_name: str
    text: CspText
    difficulty: str

class CspGenerateRequest(BaseModel):
    random_graph: bool = True
    graph_size: Optional[int] = None
    
    random_algo: bool = True
    algorithm: Optional[str] = None
    
    random_prefill: bool = True
    prefill_level: Optional[str] = None

# --- MODIFICARE CRITICĂ PENTRU SINCRONIZARE ---
class CspAnswerRequest(BaseModel):
    problem_seed: int
    user_assignments: Dict[str, str]
    # Adăugăm parametrii care au generat problema pentru reconstrucție fidelă
    generated_params: Dict[str, Any]

class CspEvaluationResponse(BaseModel):
    percentage: int
    correct_solution: List[str]
    explanation: str