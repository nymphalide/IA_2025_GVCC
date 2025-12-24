import random
from typing import List, Tuple, Dict, Any

from app.logic.common.seed import set_seed
from app.schemas.nash_schemas import NashMatrix
from app.logic.nash.strings import NASH_TEXT_RO  # Import templates

from app.logic.common.difficulty import (
    NASH_MATRIX_MIN_SIZE,
    NASH_MATRIX_MAX_SIZE,
    NASH_MIN_PAYOFF,
    NASH_MAX_PAYOFF
)


def _generate_random_matrix(rows: int, cols: int) -> List[List[Tuple[int, int]]]:
    grid = []
    for _ in range(rows):
        row = []
        for _ in range(cols):
            row.append((
                random.randint(NASH_MIN_PAYOFF, NASH_MAX_PAYOFF),
                random.randint(NASH_MIN_PAYOFF, NASH_MAX_PAYOFF)
            ))
        grid.append(row)
    return grid


def solve_pure_nash(matrix: NashMatrix) -> List[Tuple[int, int]]:
    equilibria = []
    grid = matrix.grid

    for r in range(matrix.rows):
        for c in range(matrix.cols):
            p1, p2 = grid[r][c]

            if all(p1 >= grid[rr][c][0] for rr in range(matrix.rows)) and \
                    all(p2 >= grid[r][cc][1] for cc in range(matrix.cols)):
                equilibria.append((r, c))

    return equilibria


def generate_and_solve_nash(seed: int, params: Dict[str, Any] = None):
    """
    params: dict with keys 'rows', 'cols', 'random_size'
    """
    set_seed(seed)

    # Defaults
    rows = 3
    cols = 3
    is_random = True

    # Process parameters if they exist (Generation mode)
    # If params is None (Evaluation mode), we must rely ONLY on the seed
    # to reconstruct the randomness.

    # NOTE: Since we are Stateless, the size must ALSO be deterministic based on Seed
    # OR the frontend must pass the config back.
    # To keep it simple and stateless:
    # We will generate the size RANDOMLY if params is None or random_size=True.
    # If specific params are given, we use them.

    if params:
        is_random = params.get("random_size", False)
        if not is_random:
            # Clamp values to safe limits (2 to 4)
            req_rows = params.get("rows", 3)
            req_cols = params.get("cols", 3)
            rows = max(2, min(4, req_rows))
            cols = max(2, min(4, req_cols))

    if is_random:
        # Use the seed to pick size
        rows = random.randint(NASH_MATRIX_MIN_SIZE, NASH_MATRIX_MAX_SIZE)
        cols = random.randint(NASH_MATRIX_MIN_SIZE, NASH_MATRIX_MAX_SIZE)

    grid = _generate_random_matrix(rows, cols)
    matrix = NashMatrix(rows=rows, cols=cols, grid=grid)
    equilibria = solve_pure_nash(matrix)

    # Hydrate the text template
    text_data = {
        "title": NASH_TEXT_RO["title"],
        "description": NASH_TEXT_RO["description"].format(rows=rows, cols=cols),
        "requirement": NASH_TEXT_RO["requirement"]
    }

    return matrix, equilibria, text_data