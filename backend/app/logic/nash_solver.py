import random
from typing import List, Tuple, Optional
from app.logic.seed_generator import set_seed
from app.schemas.nash_schemas import NashMatrix
from app.logic.difficulty_config import (
    NASH_MATRIX_MIN_SIZE,
    NASH_MATRIX_MAX_SIZE,
    NASH_MIN_PAYOFF,
    NASH_MAX_PAYOFF
)


def _generate_random_matrix(rows: int, cols: int) -> List[List[Tuple[int, int]]]:
    """Generează o matrice cu valori aleatoare."""
    grid = []
    for _ in range(rows):
        row_data = []
        for _ in range(cols):
            p1 = random.randint(NASH_MIN_PAYOFF, NASH_MAX_PAYOFF)
            p2 = random.randint(NASH_MIN_PAYOFF, NASH_MAX_PAYOFF)
            row_data.append((p1, p2))
        grid.append(row_data)
    return grid


def solve_pure_nash(matrix: NashMatrix) -> List[Tuple[int, int]]:
    """
    Identifică toate Echilibrele Nash Pure într-o matrice dată.
    Algoritm:
    1. Pentru fiecare celulă (r, c), verifică dacă Jucătorul 1 poate obține un scor mai bun schimbând rândul.
    2. Verifică dacă Jucătorul 2 poate obține un scor mai bun schimbând coloana.
    3. Dacă ambele sunt false (scorul curent e maxim local), este un echilibru.
    """
    equilibria = []
    grid = matrix.grid

    for r in range(matrix.rows):
        for c in range(matrix.cols):
            p1_score, p2_score = grid[r][c]

            # 1. Verifică Jucătorul 1 (Schimbă rândurile, păstrează coloana c fixă)
            is_p1_best = True
            for other_r in range(matrix.rows):
                if other_r == r:
                    continue
                other_p1_score, _ = grid[other_r][c]
                if other_p1_score > p1_score:
                    is_p1_best = False
                    break

            # 2. Verifică Jucătorul 2 (Schimbă coloanele, păstrează rândul r fix)
            is_p2_best = True
            for other_c in range(matrix.cols):
                if other_c == c:
                    continue
                _, other_p2_score = grid[r][other_c]
                if other_p2_score > p2_score:
                    is_p2_best = False
                    break

            # Dacă pentru ambii jucători este cea mai bună mișcare locală
            if is_p1_best and is_p2_best:
                equilibria.append((r, c))

    return equilibria


def generate_and_solve_nash(seed: int) -> Tuple[NashMatrix, List[Tuple[int, int]]]:
    """
    Factory Method: Generează o problemă Nash reproductibilă bazată pe seed
    și returnează matricea + lista de soluții corecte.
    """
    set_seed(seed)

    # Determină dimensiunea matricei (ex: 2x2 sau 3x3)
    size = random.randint(NASH_MATRIX_MIN_SIZE, NASH_MATRIX_MAX_SIZE)
    rows = size
    cols = size

    # Generează grid-ul
    grid_data = _generate_random_matrix(rows, cols)

    matrix_obj = NashMatrix(rows=rows, cols=cols, grid=grid_data)

    # Rezolvă problema (găsește echilibrele)
    correct_equilibria = solve_pure_nash(matrix_obj)

    return matrix_obj, correct_equilibria