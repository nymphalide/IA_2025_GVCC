import random
from typing import Tuple, List, Optional, Dict, Any

from app.logic.common.seed import set_seed
from app.schemas.minmax_schemas import MinMaxNode
from app.logic.minmax.strings import MINMAX_TEXT_RO
from app.logic.common.difficulty import (
    MINMAX_L6_MIN_BREADTH,
    MINMAX_L6_MAX_BREADTH, 
    MINMAX_L6_MIN_DEPTH,  
    MINMAX_L6_MAX_DEPTH 
)

leaf_nodes_visited_count = 0


class SolverNode:
    def __init__(self, name: str, node_type: str, value: Optional[int] = None, children: List['SolverNode'] = None):
        self.name = name
        self.node_type = node_type  # "MIN" sau "MAX"
        self.value = value
        self.children = children if children else []


def _generate_tree_recursive(depth: int, max_depth: int, name_prefix: str, is_max: bool) -> SolverNode:
    # Determinăm tipul nodului curent
    current_type = "MAX" if is_max else "MIN"

    # Cazul de bază: am ajuns la adâncimea maximă -> generăm o frunză cu valoare
    if depth == max_depth:
        # Frunzele au valori, tipul părintelui dictează ce se întâmplă, dar nodul în sine e doar valoare
        return SolverNode(name=name_prefix, node_type=current_type, value=random.randint(1, 20))

    children = []
    current_node_breadth = random.randint(
        MINMAX_L6_MIN_BREADTH,
        MINMAX_L6_MAX_BREADTH
    )

    for i in range(current_node_breadth):
        child_name = f"{name_prefix}{i+1}"
        # Copiii vor avea tipul opus (negăm is_max)
        children.append(
            _generate_tree_recursive(depth + 1, max_depth, child_name, not is_max)
        )

    return SolverNode(name=name_prefix, node_type=current_type, children=children)


def _convert_to_schema(node: SolverNode) -> MinMaxNode:
    if not node.children:
        return MinMaxNode(name=node.name, node_type=node.node_type, value=node.value, children=[])

    return MinMaxNode(
        name=node.name,
        node_type=node.node_type,
        children=[_convert_to_schema(child) for child in node.children]
    )


def _alpha_beta(node: SolverNode, alpha: float, beta: float) -> int:
    """
    Implementare Alpha-Beta Pruning care decide strategia (MIN/MAX)
    bazându-se strict pe tipul nodului din arbore (node.node_type).
    """
    global leaf_nodes_visited_count

    # 1. Cazul de bază: Nod frunză (sau nod fără copii)
    if not node.children:
        leaf_nodes_visited_count += 1
        return node.value if node.value is not None else 0

    # 2. Logică bazată pe tipul nodului
    # Verificăm explicit tipul stocat în nod pentru a garanta consistența cu vizualizarea
    if node.node_type == "MAX":
        value = -float('inf')
        for child in node.children:
            # Apel recursiv
            value = max(value, _alpha_beta(child, alpha, beta))
            alpha = max(alpha, value)
            
            # Pruning Alpha-Beta
            if alpha >= beta:
                break
        return value
    
    else: # node.node_type == "MIN"
        value = float('inf')
        for child in node.children:
            # Apel recursiv
            value = min(value, _alpha_beta(child, alpha, beta))
            beta = min(beta, value)
            
            # Pruning Alpha-Beta
            if alpha >= beta:
                break
        return value


def generate_and_solve_minmax(seed: int, params: Dict[str, Any] = None) -> Tuple[MinMaxNode, int, int, int, Dict[str, str], str]:
    global leaf_nodes_visited_count

    set_seed(seed)
    
    # --- 1. Configurare ADÂNCIME (Depth) ---
    # IMPORTANT: Consumăm întotdeauna numărul aleator pentru a păstra sincronizarea RNG
    random_depth = random.randint(MINMAX_L6_MIN_DEPTH, MINMAX_L6_MAX_DEPTH)
    
    chosen_depth = random_depth
    if params:
        if not params.get("random_depth", True):
            req_depth = params.get("depth")
            if req_depth is not None:
                chosen_depth = max(0, min(12, req_depth))

    # --- 2. Configurare RĂDĂCINĂ (Root Type) ---
    # IMPORTANT: Consumăm întotdeauna numărul aleator pentru a păstra sincronizarea RNG
    random_is_max = random.choice([True, False])
    
    start_is_maximizing = random_is_max
    if params:
        if params.get("random_root", True):
            # Dacă userul vrea random, folosim ce a ales RNG-ul
            start_is_maximizing = random_is_max
        else:
            # Dacă userul a forțat o valoare, o folosim pe aceea (dar RNG-ul a fost deja consumat mai sus)
            user_choice = params.get("is_maximizing_player")
            if user_choice is not None:
                start_is_maximizing = user_choice

    # --- 3. Generare Arbore ---
    internal_tree = _generate_tree_recursive(
        depth=0,
        max_depth=chosen_depth,
        name_prefix="R",
        is_max=start_is_maximizing
    )

    # --- 4. Rezolvare ---
    leaf_nodes_visited_count = 0
    # Algoritmul citește tipul direct din rădăcina arborelui
    root_value = _alpha_beta(
        internal_tree, -float('inf'), float('inf')
    )

    schema_tree = _convert_to_schema(internal_tree)

    text_data = MINMAX_TEXT_RO.copy()
    root_type_str = "MAX" if start_is_maximizing else "MIN"

    return schema_tree, root_value, leaf_nodes_visited_count, chosen_depth, text_data, root_type_str