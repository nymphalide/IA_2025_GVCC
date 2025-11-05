from fastapi import APIRouter
from app.logic.minmax_solver import generate_and_solve_minmax
from app.logic.evaluator import evaluate_minmax
from app.schemas.minmax_schemas import MinMaxAnswerRequest, EvaluationResponse

router = APIRouter()

@router.post("/evaluate/minmax", response_model=EvaluationResponse)
async def evaluate_minmax_answer(user_answer: MinMaxAnswerRequest):
    """
    Evaluează un răspuns la o problemă MinMax (L6).
    
    Primește răspunsul utilizatorului (care include seed-ul problemei).
    Regenerează problema folosind seed-ul pentru a obține soluția corectă.
    Compară și returnează un procentaj.
    """
    
    # 1. Regenerează problema și soluția corectă folosind seed-ul primit
    # Acesta este pasul crucial pentru reproductibilitate!
    _, correct_root_value, correct_visited_nodes = generate_and_solve_minmax(
        seed=user_answer.problem_seed,
        depth=3,
        breadth=2
    )
    
    # 2. Evaluează răspunsul utilizatorului comparându-l cu soluția corectă
    evaluation = evaluate_minmax(
        user_answer=user_answer,
        correct_value=correct_root_value,
        correct_nodes=correct_visited_nodes
    )
    
    return evaluation