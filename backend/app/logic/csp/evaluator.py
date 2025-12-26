from app.schemas.csp_schemas import CspAnswerRequest, CspEvaluationResponse
from app.logic.csp.solver import generate_csp_problem, solve_complete_csp, COLOR_TRANSLATIONS
from typing import Dict, List, Any

# Folosim maparea centralizată din solver.py pentru consistență
ENG_TO_RO_COLORS = COLOR_TRANSLATIONS

def evaluate_csp(user_answer: CspAnswerRequest) -> CspEvaluationResponse:
    seed = user_answer.problem_seed
    user_map = user_answer.user_assignments
    
    # Preluăm parametrii generatori.
    params = user_answer.generated_params
    if not params:
        params = {"random_graph": True, "random_algo": True, "random_prefill": True}

    # 1. Regenerăm snapshot-ul inițial pentru a vedea ce a fost pre-asignat
    initial_state = generate_csp_problem(seed, params)
    
    pre_assigned_map = initial_state["assignments"]
    all_variables = initial_state["all_variables"]

    # 2. Obținem soluția completă corectă (folosind același seed și params)
    # Deoarece solverul folosește acum RO_SORTED_COLORS, soluția va fi cea deterministică în RO.
    correct_assignments_full, _ = solve_complete_csp(seed, params)

    # 3. Identificăm nodurile pe care userul trebuia să le rezolve
    target_nodes = [node for node in all_variables if node not in pre_assigned_map]

    matches = 0
    total_target = len(target_nodes)
    mistakes = []
    correct_solution_text: List[str] = []

    # Sortăm nodurile numeric pentru afișare consistentă
    target_nodes.sort(key=lambda x: int(x))

    for node_id in target_nodes:
        correct_color_eng = correct_assignments_full.get(node_id)
        user_color_eng = user_map.get(node_id)
        
        correct_color_ro = ENG_TO_RO_COLORS.get(correct_color_eng, correct_color_eng)
        correct_solution_text.append(f"nodul {node_id} este {correct_color_ro}")

        if user_color_eng == correct_color_eng:
            matches += 1
        else:
            user_color_ro = ENG_TO_RO_COLORS.get(user_color_eng, "Nesetată")
            mistakes.append(f"Nod {node_id}: {user_color_ro} (Corect: {correct_color_ro})")

    if total_target == 0:
        percentage = 100
        explanation = "Nu au existat noduri de completat."
    else:
        percentage = int((matches / total_target) * 100)
        
        if percentage == 100:
            explanation = "Felicitări! Toate nodurile au fost completate corect conform algoritmului determinist (ordine alfabetică RO)."
        else:
            explanation = (
                f"Ai completat corect {matches} din {total_target} noduri. "
                f"Erori: {', '.join(mistakes[:3])}" + ("..." if len(mistakes) > 3 else "")
            )

    return CspEvaluationResponse(
        percentage=percentage,
        correct_solution=correct_solution_text,
        explanation=explanation
    )