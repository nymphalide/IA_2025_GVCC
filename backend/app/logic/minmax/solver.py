import random
from typing import Tuple, List, Optional

from app.logic.common.seed import set_seed
from app.schemas.minmax_schemas import MinMaxNode
from app.logic.common.difficulty import (
    MINMAX_L6_MIN_DEPTH,
    MINMAX_L6_MAX_DEPTH,
    MINMAX_L6_MIN_BREADTH,
    MINMAX_L6_MAX_BREADTH
)

leaf_nodes_visited_count = 0


class SolverNode:
    def __init__(self, name: str, value: Optional[int] = None, children: List['SolverNode'] = None):
        self.name = name
        self.value = value
        self.children = children if children else []


def _generate_tree_recursive(depth: int, max_depth: int, name_prefix: str) -> SolverNode:
    if depth == max_depth:
        return SolverNode(name=name_prefix, value=random.randint(1, 20))

    children = []
    current_node_breadth = random.randint(
        MINMAX_L6_MIN_BREADTH,
        MINMAX_L6_MAX_BREADTH
    )

    for i in range(current_node_breadth):
        child_name = f"{name_prefix}{i+1}"
        children.append(
            _generate_tree_recursive(depth + 1, max_depth, child_name)
        )

    return SolverNode(name=name_prefix, children=children)


def _convert_to_schema(node: SolverNode) -> MinMaxNode:
    if not node.children:
        return MinMaxNode(name=node.name, value=node.value, children=[])

    return MinMaxNode(
        name=node.name,
        children=[_convert_to_schema(child) for child in node.children]
    )


def _alpha_beta(node: SolverNode, depth: int, alpha: float, beta: float, is_maximizing_player: bool) -> int:
    global leaf_nodes_visited_count

    if not node.children:
        leaf_nodes_visited_count += 1
        return node.value if node.value is not None else 0

    if is_maximizing_player:
        value = -float('inf')
        for child in node.children:
            value = max(value, _alpha_beta(child, depth + 1, alpha, beta, False))
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return value
    else:
        value = float('inf')
        for child in node.children:
            value = min(value, _alpha_beta(child, depth + 1, alpha, beta, True))
            beta = min(beta, value)
            if alpha >= beta:
                break
        return value


def generate_and_solve_minmax(seed: int) -> Tuple[MinMaxNode, int, int, int]:
    global leaf_nodes_visited_count

    set_seed(seed)

    chosen_depth = random.randint(
        MINMAX_L6_MIN_DEPTH,
        MINMAX_L6_MAX_DEPTH
    )

    internal_tree = _generate_tree_recursive(
        depth=0,
        max_depth=chosen_depth,
        name_prefix="R"
    )

    leaf_nodes_visited_count = 0
    root_value = _alpha_beta(
        internal_tree, 0, -float('inf'), float('inf'), True
    )

    schema_tree = _convert_to_schema(internal_tree)

    return schema_tree, root_value, leaf_nodes_visited_count, chosen_depth
