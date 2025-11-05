import pytest
from app.logic.evaluator import evaluate_minmax
from app.schemas.minmax_schemas import MinMaxAnswerRequest

# Răspunsul corect pe care îl vom folosi ca bază
CORRECT_VALUE = 13
CORRECT_NODES = 5

def test_evaluation_100_percent():
    """Test 2 (Evaluare): Cazul 100% corect."""
    user_answer = MinMaxAnswerRequest(
        problem_seed=1, 
        root_value=CORRECT_VALUE, 
        visited_nodes=CORRECT_NODES
    )
    result = evaluate_minmax(user_answer, CORRECT_VALUE, CORRECT_NODES)
    assert result.percentage == 100

def test_evaluation_50_percent_value():
    """Test 2 (Evaluare): Cazul 50% (doar valoarea corectă)."""
    user_answer = MinMaxAnswerRequest(
        problem_seed=1, 
        root_value=CORRECT_VALUE, # Corect
        visited_nodes=99           # Greșit
    )
    result = evaluate_minmax(user_answer, CORRECT_VALUE, CORRECT_NODES)
    assert result.percentage == 50

def test_evaluation_50_percent_nodes():
    """Test 2 (Evaluare): Cazul 50% (doar nodurile corecte)."""
    user_answer = MinMaxAnswerRequest(
        problem_seed=1, 
        root_value=99,           # Greșit
        visited_nodes=CORRECT_NODES # Corect
    )
    result = evaluate_minmax(user_answer, CORRECT_VALUE, CORRECT_NODES)
    assert result.percentage == 50

def test_evaluation_0_percent():
    """Test 2 (Evaluare): Cazul 0% (totul greșit)."""
    user_answer = MinMaxAnswerRequest(
        problem_seed=1, 
        root_value=99,  # Greșit
        visited_nodes=99  # Greșit
    )
    result = evaluate_minmax(user_answer, CORRECT_VALUE, CORRECT_NODES)
    assert result.percentage == 0