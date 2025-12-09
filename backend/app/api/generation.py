from fastapi import APIRouter
from app.logic.seed_generator import get_new_seed
from app.logic.minmax_solver import generate_and_solve_minmax
from app.schemas.minmax_schemas import MinMaxProblemResponse
# --- IMPORTUL CARE LIPSEA ---
from app.logic.tree_visualizer import generate_tree_image_base64
from app.logic.nash_solver import generate_and_solve_nash
from app.schemas.nash_schemas import NashProblemResponse

router = APIRouter()

@router.post("/generate/minmax", response_model=MinMaxProblemResponse)
async def generate_minmax_problem():
    """
    Generează o nouă problemă MinMax (L6).
    
    Generează un seed nou, apoi folosește seed-ul pentru a crea un arbore
    cu structură aleatorie (adâncime și lățime per nod).
    """
    # 1. Obține un seed nou și unic
    new_seed = get_new_seed()
    
    # 2. Generează problema
    # Solver-ul gestionează acum TOATĂ randomizarea (depth, breadth, valori)
    # și ne returnează structura și adâncimea aleasă.
    tree_structure, _, _, chosen_depth = generate_and_solve_minmax(
        seed=new_seed
    )

    # --- LINIA CARE LIPSEA ---
    # Generează imaginea PNG a arborelui
    tree_image_b64 = generate_tree_image_base64(tree_structure.model_dump())

    # 3. Returnează problema
    return MinMaxProblemResponse(
        seed=new_seed,
        tree=tree_structure,
        # Actualizăm stringul de dificultate (nu mai avem o lățime fixă)
        difficulty=f"L6_Depth{chosen_depth}", 
        tree_image_base64=tree_image_b64 # Acum variabila este definită
    )


@router.post("/generate/nash", response_model=NashProblemResponse)
async def generate_nash_problem():
    """
    Generează o matrice de joc (Formă Normală).
    Utilizează 'generate_and_solve_nash' pentru a crea structura pe baza unui seed unic.
    """
    new_seed = get_new_seed()

    # Generăm matricea (soluția o ignorăm aici, o recalculăm la evaluare)
    matrix_obj, _ = generate_and_solve_nash(seed=new_seed)

    return NashProblemResponse(
        seed=new_seed,
        matrix=matrix_obj,
        difficulty=f"{matrix_obj.rows}x{matrix_obj.cols}"
    )