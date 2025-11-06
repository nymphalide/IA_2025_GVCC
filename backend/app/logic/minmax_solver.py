import random
from app.logic.seed_generator import set_seed
from app.schemas.minmax_schemas import MinMaxNode
from typing import Tuple, List, Optional
# --- ADĂUGAT: Importăm limitele de configurare ---
from app.logic.difficulty_config import (
    MINMAX_L6_MIN_DEPTH,
    MINMAX_L6_MAX_DEPTH,
    MINMAX_L6_MIN_BREADTH,
    MINMAX_L6_MAX_BREADTH
)

# Variabilă globală pentru a număra nodurile frunză vizitate
# Resetată la fiecare apel principal
leaf_nodes_visited_count = 0

class SolverNode:
    """Clasa internă pentru algoritmul de rezolvare."""
    def __init__(self, name: str, value: Optional[int] = None, children: List['SolverNode'] = None):
        self.name = name
        self.value = value
        self.children = children if children else []

def _generate_tree_recursive(depth: int, max_depth: int, name_prefix: str) -> SolverNode: # <-- MODIFICAT: Am scos 'breadth'
    """
    Funcție recursivă internă pentru generarea arborelui.
    Lățimea (breadth) este determinată aleatoriu la fiecare nod.
    """
    
    # Cazul de bază: am ajuns la adâncimea maximă (frunză)
    if depth == max_depth:
        # Generăm o valoare aleatorie pentru frunză
        return SolverNode(name=name_prefix, value=random.randint(1, 20))
    
    # Cazul recursiv: nod intern
    children = []
    
    # --- MODIFICARE CHEIE ---
    # Fiecare nod își alege propria lățime (nr. de copii)
    # Deoarece seed-ul a fost setat în funcția publică, 
    # acest apel este determinist și reproductibil.
    current_node_breadth = random.randint(MINMAX_L6_MIN_BREADTH, MINMAX_L6_MAX_BREADTH)
    
    for i in range(current_node_breadth): # <-- Folosim lățimea aleatorie a nodului curent
        child_name = f"{name_prefix}{i+1}"
        child_node = _generate_tree_recursive(depth + 1, max_depth, child_name) # <-- Apel recursiv fără 'breadth'
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
    (Funcția aceasta rămâne neschimbată)
    """
    global leaf_nodes_visited_count

    # Cazul de bază: am ajuns la o frunză
    if not node.children:
        leaf_nodes_visited_count += 1
        # Asigurare: Dacă arborele are adâncimea 0 (doar rădăcină), 
        # ceea ce nu se întâmplă cu D>=3, dar e bine de avut
        if node.value is None:
             return 0 # Sau o altă valoare de fallback
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

# MODIFICAT: Semnătura s-a schimbat. 
# Nu mai acceptăm depth/breadth, le determinăm intern.
# Returnăm (schema, valoare, noduri, adâncimea_aleasă)
def generate_and_solve_minmax(seed: int) -> Tuple[MinMaxNode, int, int, int]:
    """
    Generează un arbore MinMax cu structură (adâncime și lățime) aleatorie
    și îl rezolvă folosind Alpha-Beta.
    
    Returnează: (Structura Arborelui (schema), Valoarea Rădăcină, Noduri Frunză Vizitate, Adâncimea Aleasă)
    """
    global leaf_nodes_visited_count
    
    # 1. Asigură Reproductibilitatea
    set_seed(seed)
    
    # 2. Determină aleatoriu structura (bazat pe seed)
    # Acesta este primul apel random după set_seed()
    chosen_depth = random.randint(MINMAX_L6_MIN_DEPTH, MINMAX_L6_MAX_DEPTH)
    
    # 3. Generează structura internă a arborelui
    # Următoarele apeluri random vor fi în interiorul _generate_tree_recursive
    # pentru lățimi (breadth) și valori frunze.
    internal_tree = _generate_tree_recursive(
        depth=0, 
        max_depth=chosen_depth, 
        name_prefix="R"
    )
    
    # 4. Resetează contorul și Rezolvă
    leaf_nodes_visited_count = 0
    root_value = _alpha_beta(
        node=internal_tree, 
        depth=0, 
        alpha=-float('inf'), 
        beta=float('inf'), 
        is_maximizing_player=True # Rădăcina este MAX
    )
    
    # 5. Convertește arborele la formatul Pydantic (pentru JSON)
    schema_tree = _convert_to_schema(internal_tree)
    
    # Returnăm și adâncimea aleasă, pentru a fi afișată în API
    return (schema_tree, root_value, leaf_nodes_visited_count, chosen_depth)