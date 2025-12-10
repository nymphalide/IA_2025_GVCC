from fastapi import APIRouter
from app.logic.minmax_solver import generate_and_solve_minmax
from app.logic.evaluator import evaluate_minmax
from app.schemas.minmax_schemas import MinMaxAnswerRequest, EvaluationResponse
# Nu mai avem nevoie de random, set_seed sau difficulty_config aici

from app.logic.nash_solver import generate_and_solve_nash
from app.schemas.nash_schemas import NashAnswerRequest, NashEvaluationResponse

router = APIRouter()

@router.post("/evaluate/minmax", response_model=EvaluationResponse)
async def evaluate_minmax_answer(user_answer: MinMaxAnswerRequest):
    """
    Evaluează un răspuns la o problemă MinMax (L6).
    
    Primește răspunsul utilizatorului (care include seed-ul problemei).
    Regenerează problema folosind seed-ul pentru a obține soluția corectă.
    Compară și returnează un procentaj.
    """
    
    # 1. Regenerează problema și soluția corectă folosind DOAR seed-ul
    # Solver-ul va genera intern aceeași adâncime și aceleași lățimi
    # ca la pasul de generare.
    _, correct_root_value, correct_visited_nodes, _ = generate_and_solve_minmax(
        seed=user_answer.problem_seed
    )
    
    # 2. Evaluează răspunsul utilizatorului comparându-l cu soluția corectă
    evaluation = evaluate_minmax(
        user_answer=user_answer,
        correct_value=correct_root_value,
        correct_nodes=correct_visited_nodes
    )
    
    return evaluation


@router.post("/evaluate/nash", response_model=NashEvaluationResponse)
async def evaluate_nash_answer(user_answer: NashAnswerRequest):
    """
    Evaluează răspunsul utilizatorului pentru Echilibru Nash.
    Regenerează problema pe baza seed-ului și verifică existența și coordonatele.
    """
    # 1. Regenerare soluție corectă
    _, correct_equilibria = generate_and_solve_nash(seed=user_answer.problem_seed)

    has_eq_correct = (len(correct_equilibria) > 0)
    percentage = 0
    explanation = ""

    # 2. Logică de evaluare

    # Cazul A: Utilizatorul spune că există echilibru
    if user_answer.has_equilibrium:
        if not has_eq_correct:
            # Greșit: A zis că există, dar nu există
            percentage = 0
            explanation = "Greșit. Nu există niciun Echilibru Nash Pur în această matrice."
        else:
            # Există echilibre. Verificăm coordonatele trimise.
            if user_answer.equilibrium_point:
                user_pt = (user_answer.equilibrium_point[0], user_answer.equilibrium_point[1])
                if user_pt in correct_equilibria:
                    percentage = 100
                    explanation = f"Corect! Punctul {user_pt} este un Echilibru Nash."
                else:
                    percentage = 50
                    explanation = (f"Parțial corect. Există un echilibru, dar coordonatele {user_pt} "
                                   f"sunt greșite. Soluții posibile: {correct_equilibria}")
            else:
                percentage = 50
                explanation = "Parțial corect. Există echilibru, dar nu ați specificat coordonatele."

    # Cazul B: Utilizatorul spune că NU există echilibru
    else:
        if not has_eq_correct:
            percentage = 100
            explanation = "Corect! Nu există niciun Echilibru Nash Pur."
        else:
            percentage = 0
            explanation = f"Greșit. Există cel puțin un echilibru la: {correct_equilibria}"

    return NashEvaluationResponse(
        percentage=percentage,
        correct_answer=correct_equilibria,  # Returnăm lista de soluții
        explanation=explanation
    )