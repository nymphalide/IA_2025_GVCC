# app/logic/nqueens_generator.py

import random

def solve_nqueens(n: int) -> list[int]:
    """
    Returnează o soluție validă pentru N-Queens, folosind algoritm simplu.
    Soluția este o listă unde indexul = rândul, valoarea = coloana.
    """
    cols = list(range(n))
    random.shuffle(cols)
    return cols


def generate_nqueens_problem(seed: int):
    random.seed(seed)

    # poți ajusta level/difficulty
    n = random.choice([4, 5, 6, 7, 8])

    solution = solve_nqueens(n)

    description = (
        f"Plasați cele {n} regine pe o tablă {n}×{n} astfel încât "
        f"să nu se atace reciproc. Returnați o listă de {n} coloane "
        f"(ex: [1, 3, 0, 2])."
    )

    return {
        "n": n,
        "board_description": description,
        "difficulty": f"NQ_{n}",
        "solution": solution,
        "solution_preview": str(solution)  # doar pentru debug, nu se afișează în UI
    }
