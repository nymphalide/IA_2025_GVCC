"""
logic/minmax_solver.py

Acest modul conține logica fundamentală pentru:
1. Definirea structurii unui nod de arbore MinMax.
2. Implementarea algoritmului MinMax cu tăieri Alpha-Beta.
3. Generarea unui arbore aleatoriu (folosind seed) pentru o problemă MinMax.

Acest fișier corespunde task-urilor US-I.1 (Algoritm și Generare).
"""

import random
import math
from typing import List, Optional, Tuple

# --- Import din Modulul de Reproductibilitate (Pasul 2) ---
# Presupunem că seed_generator.py se află în același director 'logic'
# sau că structura pachetului permite importul.
try:
    from . import seed_generator
except ImportError:
    # Fallback pentru rulare locală (dacă __name__ == '__main__')
    import seed_generator


# ==============================================================================
# 1. STRUCTURI DE DATE INTERNE (Pasul 3.1)
# ==============================================================================

class Node:
    """
    Structura de date internă pentru a reprezenta un nod în arborele de joc.
    Aceasta este logica internă a solver-ului.

    NOTA: Membru 3 va defini un model Pydantic pentru API (ex: MinMaxNodeResponse)
    care va fi folosit pentru a trimite datele către Frontend. Vom crea
    o funcție de conversie când acel model este gata.
    """

    def __init__(self, node_id: str, is_max_node: bool, depth: int):
        self.node_id: str = node_id  # ID unic (ex: "A", "B1", "C2")
        self.is_max_node: bool = is_max_node  # True = Nod MAX, False = Nod MIN
        self.depth: int = depth  # Adâncimea în arbore
        self.children: List['Node'] = []  # Lista de noduri copil
        self.value: Optional[int] = None  # Valoarea euristică (doar pentru frunze)

    def add_child(self, child_node: 'Node'):
        self.children.append(child_node)

    def is_leaf(self) -> bool:
        return not self.children


class MinMaxSolution:
    """
    O clasă simplă pentru a stoca rezultatele cerute de problemă:
    1. Valoarea finală din rădăcină.
    2. Numărul de noduri frunză vizitate efectiv.
    """

    def __init__(self):
        # Valoarea finală calculată pentru rădăcină
        self.root_value: int = 0

        # Counter pentru cerința specifică a proiectului
        self.visited_leaf_nodes: int = 0


# ==============================================================================
# 2. ALGORITMUL MINMAX CU TĂIERI ALPHA-BETA (Pasul 3.2)
# ==============================================================================

def _run_minmax_alpha_beta(
        current_node: Node,
        alpha: float,
        beta: float,
        solution_tracker: MinMaxSolution
) -> int:
    """
    Funcția recursivă internă care implementează logica MinMax cu tăieri A-B.
    Actualizează 'solution_tracker' cu numărul de frunze vizitate.
    """

    # --- Cazul de Bază: Nod Terminal (Frunză) ---
    if current_node.is_leaf():
        # Cerința P1: Contorizăm doar frunzele care sunt evaluate efectiv.
        solution_tracker.visited_leaf_nodes += 1
        return current_node.value

    # --- Cazul Recursiv: Nod de Decizie (MAX sau MIN) ---

    if current_node.is_max_node:
        # --- Nod MAX (Încearcă să maximizeze scorul) ---
        best_value = -math.inf

        for child in current_node.children:
            # Apel recursiv pentru copil
            child_value = _run_minmax_alpha_beta(child, alpha, beta, solution_tracker)

            # Actualizare best_value (valoarea nodului MAX)
            best_value = max(best_value, child_value)

            # Actualizare Alpha (cea mai bună opțiune garantată pentru MAX)
            alpha = max(alpha, best_value)

            # --- Condiția de Tăiere (Beta Cutoff) ---
            # Dacă valoarea curentă (alpha) e mai mare decât cea mai bună opțiune
            # a lui MIN (beta) găsită pe o altă ramură, MIN nu va alege niciodată
            # această cale. Oprim explorarea.
            if alpha >= beta:
                break  # Tăiere Beta

        return best_value

    else:
        # --- Nod MIN (Încearcă să minimizeze scorul) ---
        best_value = math.inf

        for child in current_node.children:
            # Apel recursiv pentru copil
            child_value = _run_minmax_alpha_beta(child, alpha, beta, solution_tracker)

            # Actualizare best_value (valoarea nodului MIN)
            best_value = min(best_value, child_value)

            # Actualizare Beta (cea mai bună opțiune garantată pentru MIN)
            beta = min(beta, best_value)

            # --- Condiția de Tăiere (Alpha Cutoff) ---
            # Dacă valoarea curentă (beta) e mai mică decât cea mai bună opțiune
            # a lui MAX (alpha) găsită pe o altă ramură, MAX nu va alege niciodată
            # această cale. Oprim explorarea.
            if beta <= alpha:
                break  # Tăiere Alpha

        return best_value


def solve_minmax_tree(root_node: Node) -> MinMaxSolution:
    """
    Funcția publică (wrapper) pentru a porni algoritmul Alpha-Beta.

    Initializează tracker-ul de soluție și valorile inițiale pentru alpha/beta.

    Args:
        root_node (Node): Rădăcina arborelui de joc.

    Returns:
        MinMaxSolution: Un obiect conținând valoarea rădăcinii și
                        numărul de frunze vizitate.
    """
    # Inițializăm tracker-ul care va fi pasat recursiv
    solution = MinMaxSolution()

    # Inițializăm alpha (-inf) și beta (+inf)
    alpha_init = -math.inf
    beta_init = math.inf

    # Pornim recursivitatea de la rădăcină
    final_value = _run_minmax_alpha_beta(
        current_node=root_node,
        alpha=alpha_init,
        beta=beta_init,
        solution_tracker=solution
    )

    solution.root_value = final_value
    return solution


# ==============================================================================
# 3. GENERARE ARBORE (Pasul 3.3)
# ==============================================================================

# Constante pentru generare (pot fi modificate de nivelele de dificultate)
DEFAULT_MAX_DEPTH = 3  # Adâncimea (ex: 3 nivele de decizie)
DEFAULT_BREADTH_RANGE = (2, 3)  # Lățimea (min, max copii per nod)
LEAF_VALUE_RANGE = (1, 20)  # Intervalul valorilor frunzelor


def _generate_random_tree_recursive(
        current_node: Node,
        max_depth: int,
        breadth_range: Tuple[int, int],
        value_range: Tuple[int, int]
):
    """Funcție utilitară recursivă pentru a construi arborele."""

    # Cazul de bază: Am atins adâncimea maximă -> creăm o frunză
    if current_node.depth == max_depth:
        current_node.value = random.randint(*value_range)
        return

    # Cazul recursiv: Creăm noduri copil
    num_children = random.randint(*breadth_range)

    for i in range(num_children):
        child_id = f"{current_node.node_id}-{i + 1}"

        # Alternăm tipul nodului (MAX -> MIN, MIN -> MAX)
        child_is_max = not current_node.is_max_node

        child_node = Node(
            node_id=child_id,
            is_max_node=child_is_max,
            depth=current_node.depth + 1
        )

        # Apel recursiv pentru a construi sub-arborele copilului
        _generate_random_tree_recursive(
            child_node, max_depth, breadth_range, value_range
        )

        current_node.add_child(child_node)


def generate_minmax_problem(
        seed_id: int,
        difficulty: str = 'EASY'
) -> Tuple[Node, MinMaxSolution]:
    """
    Funcția principală de generare a unei probleme MinMax complete.

    1. Setează seed-ul (Pasul 2.2)
    2. Construiește arborele aleatoriu (Pasul 3.3)
    3. Rulează algoritmul MinMax pe el (Pasul 3.2)

    Args:
        seed_id (int): Seed-ul pentru reproductibilitate.
        difficulty (str): Nivelul de dificultate (va fi folosit în Sprint 3).

    Returns:
        Tuple[Node, MinMaxSolution]:
            - root_node: Rădăcina arborelui generat (pentru UI).
            - solution: Soluția corectă (pentru evaluare).
    """

    # --- 1. Setare Reproductibilitate (Cerință P1) ---
    seed_generator.set_seed(seed_id)

    # --- 2. Parametrizare Dificultate (Placeholder Sprint 3, US-II.3) ---
    # TODO: Ajustează parametrii în funcție de 'difficulty'
    if difficulty == 'MEDIUM':
        max_depth = 4
        breadth_range = (2, 3)
    elif difficulty == 'HARD':
        max_depth = 4
        breadth_range = (3, 4)
    else:  # EASY
        max_depth = DEFAULT_MAX_DEPTH
        breadth_range = DEFAULT_BREADTH_RANGE

    value_range = LEAF_VALUE_RANGE

    # --- 3. Generare Arbore (Pasul 3.3) ---
    # Începem de la rădăcină (Nod MAX, adâncime 0)
    root_node = Node(node_id="R", is_max_node=True, depth=0)

    _generate_random_tree_recursive(
        current_node=root_node,
        max_depth=max_depth,
        breadth_range=breadth_range,
        value_range=value_range
    )

    # --- 4. Rezolvare Arbore (Pasul 3.2) ---
    # Calculăm răspunsul corect imediat după generare
    solution = solve_minmax_tree(root_node)

    return root_node, solution


# ==============================================================================
# 4. BLOC DE TESTARE LOCALĂ (Pasul 4.3)
# ==============================================================================

def _print_tree_simple(node: Node, indent: str = ""):
    """Funcție utilitară pentru a vizualiza arborele generat."""
    if node.is_leaf():
        print(f"{indent}[{node.node_id}] -> LEAF: {node.value}")
    else:
        node_type = "MAX" if node.is_max_node else "MIN"
        print(f"{indent}[{node.node_id}] ({node_type})")
        for child in node.children:
            _print_tree_simple(child, indent + "  ")


if __name__ == '__main__':
    """
    Testare locală pentru a verifica corectitudinea și reproductibilitatea.
    Rulează acest fișier direct: python logic/minmax_solver.py
    """
    print("--- Testare Modul MinMax Solver ---")

    TEST_SEED = 42

    # --- Rulare 1 ---
    print(f"\n[Rulare 1] Generare cu Seed = {TEST_SEED}...")
    tree1, solution1 = generate_minmax_problem(seed_id=TEST_SEED, difficulty='EASY')

    print("Arbore Generat (Rulare 1):")
    _print_tree_simple(tree1)
    print(f"\nSoluție (Rulare 1):")
    print(f"  Valoare Rădăcină: {solution1.root_value}")
    print(f"  Frunze Vizitate:  {solution1.visited_leaf_nodes}")

    # --- Rulare 2 (Reproductibilitate) ---
    print(f"\n[Rulare 2] Generare cu Același Seed = {TEST_SEED}...")
    tree2, solution2 = generate_minmax_problem(seed_id=TEST_SEED, difficulty='EASY')

    # (Nu mai afișăm arborele, doar soluția)
    print(f"\nSoluție (Rulare 2):")
    print(f"  Valoare Rădăcină: {solution2.root_value}")
    print(f"  Frunze Vizitate:  {solution2.visited_leaf_nodes}")

    # --- Verificare (Cerință Pas 4.3) ---
    assert solution1.root_value == solution2.root_value, \
        "Eroare Reproductibilitate: Valorile rădăcinii diferă!"
    assert solution1.visited_leaf_nodes == solution2.visited_leaf_nodes, \
        "Eroare Reproductibilitate: Numărul de frunze vizitate diferă!"

    print(f"\n[SUCCES] Testul de reproductibilitate a trecut.")