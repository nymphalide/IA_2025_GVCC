# app/logic/strategy_generator.py
import random

PROBLEMS = [
    {
        "name": "N-Queens",
        "description": "Pentru problema N-Queens, alegeți cea mai potrivită strategie de rezolvare.",
        "correct": "Backtracking",
    },
    {
        "name": "Generalized Hanoi",
        "description": "Pentru problema Generalized Hanoi, selectați cea mai potrivită strategie.",
        "correct": "DFS",
    },
    {
        "name": "Graph Coloring",
        "description": "Pentru problema de colorare a grafurilor, selectați cea mai potrivită strategie.",
        "correct": "Backtracking",
    },
    {
        "name": "Knight’s Tour",
        "description": "Pentru Knight’s Tour, alegeți cea mai potrivită strategie.",
        "correct": "DFS",
    }
]

OPTIONS = ["BFS", "DFS", "A*", "Backtracking", "Hill-Climbing"]

def generate_strategy_problem(seed: int):
    random.seed(seed)
    problem = random.choice(PROBLEMS)

    return {
        "problem_name": problem["name"],
        "description": problem["description"],
        "correct": problem["correct"],
        "options": OPTIONS,
        "difficulty": "THEORY"
    }
