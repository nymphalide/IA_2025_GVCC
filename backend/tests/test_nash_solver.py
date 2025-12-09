import pytest
from app.logic.nash_solver import solve_pure_nash
from app.schemas.nash_schemas import NashMatrix


def test_nash_solver_prisoners_dilemma():
    """
    Testează logica folosind exemplul Prisoner's Dilemma.
    Matrice (payoffs simplificate):
    (-1, -1)  (-3, 0)
    (0, -3)   (-2, -2)

    Echilibru unic Nash: (-2, -2) la indexul [1, 1] (Confess/Confess)
    """
    grid = [
        [(-1, -1), (-3, 0)],
        [(0, -3), (-2, -2)]
    ]
    matrix = NashMatrix(rows=2, cols=2, grid=grid)

    solutions = solve_pure_nash(matrix)

    assert len(solutions) == 1
    assert solutions[0] == (1, 1)


def test_nash_solver_stag_hunt():
    """
    Testează un joc cu două echilibre (Stag Hunt).
    (5, 5)  (0, 3)
    (3, 0)  (4, 4)
    Echilibre: (0,0) și (1,1)
    """
    grid = [
        [(5, 5), (0, 3)],
        [(3, 0), (4, 4)]
    ]
    matrix = NashMatrix(rows=2, cols=2, grid=grid)

    solutions = solve_pure_nash(matrix)

    assert len(solutions) == 2
    assert (0, 0) in solutions
    assert (1, 1) in solutions


def test_nash_solver_no_equilibrium():
    """
    Testează un joc fără echilibru pur (ex: Matching Pennies modificat).
    (1, -1) (-1, 1)
    (-1, 1) (1, -1)
    """
    grid = [
        [(1, -1), (-1, 1)],
        [(-1, 1), (1, -1)]
    ]
    matrix = NashMatrix(rows=2, cols=2, grid=grid)

    solutions = solve_pure_nash(matrix)

    assert len(solutions) == 0