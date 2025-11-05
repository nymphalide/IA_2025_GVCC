import random
from app.logic.seed_generator import set_seed
from app.schemas.minmax_schemas import MinMaxNode
from typing import Tuple, List, Optional # <--- LINIA ACEASTA A FOST ADĂUGATĂ/MODIFICATĂ

# Variabilă globală pentru a număra nodurile frunză vizitate
# Resetată la fiecare apel principal
leaf_nodes_visited_count = 0

class SolverNode:
    """Clasa internă pentru algoritmul de rezolvare."""
    def __init__(self, name: str, value: Optional[int] = None, children: List['SolverNode'] = None):
        self.name = name
        self.value = value
        self.children = children if children else []

def _generate_tree_recursive(depth: int, max_depth: int, breadth: int, name_prefix: str) -> SolverNode:
    """Funcție recursivă internă pentru generarea arborelui."""
    
    # Cazul de bază: am ajuns la adâncimea maximă (frunză)
    if depth == max_depth:
        # Generăm o valoare aleatorie pentru frunză
        return SolverNode(name=name_prefix, value=random.randint(1, 20))
    
    # Cazul recursiv: nod intern
    children = []
    for i in range(breadth):
        child_name = f"{name_prefix}{i+1}"
        child_node = _generate_tree_recursive(depth + 1, max_depth, breadth, child_name)
        children.append(child_node)
        
    return SolverNode(name=name_prefix, children=children)

def _convert_to_schema(node: SolverNode) -> MinMaxNode:
    """Convertește nodul intern (SolverNode) în nodul Pydantic (MinMaxNode) pentru API."""
    if not node.children:
        return MinMaxNode(name=node.name, value=node.value, children=[])
    
    return MinMaxNode(
        name=node.name,
        children=[_convert_to_schema(child) for child in node.children]
    )

def _alpha_beta(node: SolverNode, depth: int, alpha: float, beta: float, is_maximizing_player: bool) -> int:
    """
    Implementarea algoritmului MinMax cu tăieri Alpha-Beta.
    Complexitate Timp: O(b^d) (worst case), O(b^(d/2)) (best case / average)
    Complexitate Spațiu: O(d) (datorită stivei de recursivitate)
    """
    global leaf_nodes_visited_count

    # Cazul de bază: am ajuns la o frunză sau adâncime maximă
    if not node.children:
        leaf_nodes_visited_count += 1
        return node.value

    if is_maximizing_player:
        value = -float('inf')
        for child in node.children:
            value = max(value, _alpha_beta(child, depth + 1, alpha, beta, False))
            alpha = max(alpha, value)
            if alpha >= beta:
                break # Tăiere Beta
        return value
    else: # Jucător Minimizator
        value = float('inf')
        for child in node.children:
            value = min(value, _alpha_beta(child, depth + 1, alpha, beta, True))
            beta = min(beta, value)
            if alpha >= beta:
                break # Tăiere Alpha
        return value

# --- Funcția Publică ---

def generate_and_solve_minmax(seed: int, depth: int = 3, breadth: int = 2) -> Tuple[MinMaxNode, int, int]:
    """
    Generează un arbore MinMax și îl rezolvă folosind Alpha-Beta.
    Returnează: (Structura Arborelui (schema), Valoarea Rădăcină, Noduri Frunză Vizitate)
    """
    global leaf_nodes_visited_count
    
    # 1. Asigură Reproductibilitatea
    set_seed(seed)
    
    # 2. Generează structura internă a arborelui
    # (Adâncimea 3 și lățimea 2 rezultă în 2^3 = 8 frunze)
    internal_tree = _generate_tree_recursive(depth=0, max_depth=depth, breadth=breadth, name_prefix="R")
    
    # 3. Resetează contorul și Rezolvă
    leaf_nodes_visited_count = 0
    root_value = _alpha_beta(
        node=internal_tree, 
        depth=0, 
        alpha=-float('inf'), 
        beta=float('inf'), 
        is_maximizing_player=True # Rădăcina este MAX
    )
    
    # 4. Convertește arborele la formatul Pydantic (pentru JSON)
    schema_tree = _convert_to_schema(internal_tree)
    
    return (schema_tree, root_value, leaf_nodes_visited_count)