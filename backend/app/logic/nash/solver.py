import random
from typing import List, Tuple

from app.logic.common.seed import set_seed
from app.schemas.nash_schemas import NashMatrix
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


def generate_and_solve_nash(seed: int):
    set_seed(seed)

    size = random.randint(NASH_MATRIX_MIN_SIZE, NASH_MATRIX_MAX_SIZE)
    grid = _generate_random_matrix(size, size)

    matrix = NashMatrix(rows=size, cols=size, grid=grid)
    equilibria = solve_pure_nash(matrix)

    return matrix, equilibria
