import random
from typing import Dict, Any

from app.logic.common.seed import set_seed

# Strategiile disponibile (exact ca în UI)
ALL_STRATEGIES = ["BFS", "DFS", "A*", "Backtracking", "Hill-Climbing"]

PROBLEM_TYPES = ["nqueens", "knight", "graph_coloring", "hanoi"]


# ============================================================
# DECIZIE STRATEGIE PE BAZĂ DE SCARĂ TEORETICĂ
# ============================================================

def _decide_strategy(problem_type: str, params: Dict[str, Any]) -> str:
    """
    Decide strategia recomandată pe baza tipului problemei și a ordinului de mărime.
    NU rulează algoritmi. Este un model teoretic de raționament.
    """

    if problem_type == "nqueens":
        n = int(params["n"])

        if n <= 20:
            return "Backtracking"
        elif n <= 200:
            # încă posibil cu CSP + pruning
            return "Backtracking"
        elif n <= 10000:
            # zona clasică de min-conflicts / local search
            return "Hill-Climbing"
        else:
            # instanțe masive -> doar euristic / stochastic
            return "Hill-Climbing"

    if problem_type == "knight":
        board = int(params["board_size"])
        size = board * board

        if size <= 36:
            return "DFS"
        elif size <= 400:
            return "DFS"
        else:
            # Warnsdorff / greedy-like => asimilăm cu Hill-Climbing
            return "Hill-Climbing"

    if problem_type == "graph_coloring":
        v = int(params["vertices"])
        density = float(params["density"])  # 0..1

        # graf mic
        if v <= 50:
            return "Backtracking"

        # graf mediu
        if v <= 500:
            if density < 0.3:
                return "Backtracking"
            else:
                return "Hill-Climbing"

        # graf mare
        if density < 0.2:
            # mare dar rar -> greedy / heuristic
            return "Hill-Climbing"
        else:
            # mare și dens -> doar aproximativ
            return "Hill-Climbing"

    if problem_type == "hanoi":
        n = int(params["n_disks"])
        pegs = int(params["n_pegs"])

        # Problema are soluție deterministă recursivă -> DFS conceptual
        return "DFS"

    # Fallback (nu ar trebui să ajungă aici)
    return random.choice(ALL_STRATEGIES)


# ============================================================
# GENERARE INSTANȚĂ (FĂRĂ LIMITE ARTIFICIALE)
# ============================================================

def _generate_instance(problem_type: str, params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Generează parametrii instanței, fie random, fie din input custom.
    NU limitează valorile mari.
    """

    instance = {}

    if problem_type == "nqueens":
        if params.get("random_instance", True):
            n = random.randint(8, 500)
        else:
            n = int(params.get("n", 8))

        instance["n"] = n

    elif problem_type == "knight":
        if params.get("random_instance", True):
            board = random.randint(6, 50)
        else:
            board = int(params.get("board_size", 8))

        instance["board_size"] = board

    elif problem_type == "graph_coloring":
        if params.get("random_instance", True):
            v = random.randint(20, 500)
            density = random.random()
        else:
            v = int(params.get("vertices", 50))
            density = float(params.get("density", 0.3))

        # normalizăm doar densitatea
        density = max(0.01, min(0.99, density))

        instance["vertices"] = v
        instance["density"] = round(density, 2)

    elif problem_type == "hanoi":
        if params.get("random_instance", True):
            n_disks = random.randint(3, 20)
            n_pegs = random.randint(3, 5)
        else:
            n_disks = int(params.get("n_disks", 5))
            n_pegs = int(params.get("n_pegs", 3))

        instance["n_disks"] = n_disks
        instance["n_pegs"] = n_pegs

    return instance


# ============================================================
# DESCRIERE PROBLEMĂ
# ============================================================

def _build_description(problem_type: str, instance: Dict[str, Any]) -> str:
    """
    Construiește enunțul problemei cu instanță concretă.
    """

    if problem_type == "nqueens":
        return (
            f"Avem problema N-Queens pentru N = {instance['n']}. "
            "Care este cea mai potrivită strategie de rezolvare pentru această instanță?"
        )

    if problem_type == "knight":
        return (
            f"Avem problema Knight's Tour pe o tablă de dimensiune "
            f"{instance['board_size']}x{instance['board_size']}. "
            "Care este cea mai potrivită strategie de rezolvare?"
        )

    if problem_type == "graph_coloring":
        return (
            f"Avem o problemă de colorare a unui graf cu {instance['vertices']} noduri "
            f"și densitate aproximativă {instance['density']}. "
            "Care este cea mai potrivită strategie de rezolvare?"
        )

    if problem_type == "hanoi":
        return (
            f"Avem problema Turnurile din Hanoi cu {instance['n_disks']} discuri "
            f"și {instance['n_pegs']} țăruși. "
            "Care este cea mai potrivită strategie de rezolvare?"
        )

    return "Care este cea mai potrivită strategie?"


# ============================================================
# GENERATOR PRINCIPAL
# ============================================================

def generate_strategy_problem(seed: int, params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Generator principal. Determinist în funcție de seed + params.
    """

    set_seed(seed)

    # 1. Alegem problema
    if params.get("random_problem", True):
        problem_type = random.choice(PROBLEM_TYPES)
    else:
        problem_type = params.get("problem_type", "nqueens")

    # 2. Generăm instanța
    instance = _generate_instance(problem_type, params)

    # 3. Decidem strategia (teoretic)
    correct_strategy = _decide_strategy(problem_type, instance)

    # 4. Construim enunțul
    description = _build_description(problem_type, instance)

    # 5. Dificultate (informativ)
    difficulty = "Custom" if not params.get("random_instance", True) else "Random"

    return {
        "problem_type": problem_type,
        "problem_name": problem_type,
        "instance": instance,
        "description": description,
        "options": ALL_STRATEGIES,
        "correct": correct_strategy,
        "difficulty": difficulty
    }
