from fastapi import APIRouter
from app.logic.seed_generator import get_new_seed
from app.logic.minmax_solver import generate_and_solve_minmax
from app.schemas.minmax_schemas import MinMaxProblemResponse

router = APIRouter()

@router.post("/generate/minmax", response_model=MinMaxProblemResponse)
async def generate_minmax_problem():
    """
    Generează o nouă problemă MinMax (L6).
    
    Generează un seed nou, apoi folosește seed-ul pentru a crea un arbore
    și a calcula soluția (deși soluția nu e returnată aici).
    """
    # 1. Obține un seed nou și unic
    new_seed = get_new_seed()
    
    # 2. Generează problema
    # Ne interesează doar structura arborelui pentru a o trimite utilizatorului
    # Soluția o vom regenera la evaluare folosind același seed
    tree_structure, _, _ = generate_and_solve_minmax(
        seed=new_seed, 
        depth=3, # Adâncime standard pentru L6
        breadth=2  # Lățime standard
    )
    
    # 3. Returnează problema
    return MinMaxProblemResponse(
        seed=new_seed,
        tree=tree_structure,
        difficulty="EASY_L6"
    )