import math

def evaluate_bayes_answer(correct: float, user_answer: float, tolerance: float = 0.02):
    diff = abs(correct - user_answer)

    if diff <= tolerance:
        return 100.0

    score = 100.0 * math.exp(-diff / (2 * tolerance))
    return round(score, 2)
