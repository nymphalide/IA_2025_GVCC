import pytest
from fastapi.testclient import TestClient
from app.main import app

# Importăm solver-ul pentru a obține soluția corectă
from app.logic.minmax_solver import generate_and_solve_minmax as get_correct_solution

# Creăm un client de test pentru API
client = TestClient(app)

def test_generate_endpoint():
    """Test 3 (Endpoint): Verifică endpoint-ul de generare."""
    response = client.post("/api/generate/minmax")
    
    assert response.status_code == 200
    data = response.json()
    assert "seed" in data
    assert data["seed"] > 0
    assert "tree" in data
    assert data["tree"]["name"] == "R" # Verificăm dacă rădăcina se numește 'R'
    assert "difficulty" in data
    assert "L6_Depth" in data["difficulty"] # Verifică formatul nou (L6_Depth4)

def test_evaluate_endpoint():
    """Test 3 (Endpoint): Verifică fluxul complet (MODIFICAT PENTRU STRUCTURĂ DINAMICĂ)."""
    
    TEST_SEED = 42
    
    # --- ÎNAINTE DE TEST ---
    # Trebuie să aflăm răspunsul corect pentru TEST_SEED (42)
    # Apelăm solver-ul direct, așa cum o fac și endpoint-urile
    
    _, correct_val, correct_nodes, correct_depth = get_correct_solution(
        seed=TEST_SEED
    )
    
    # Conform testului unitar (seed=42):
    # correct_val = 10
    # correct_nodes = 8
    
    # --- START TEST ---
    
    # Pas 1: Testăm un răspuns corect (cu valorile dinamice calculate)
    test_payload_correct = {
        "problem_seed": TEST_SEED,
        "root_value": correct_val,
        "visited_nodes": correct_nodes
    }
    
    response_correct = client.post("/api/evaluate/minmax", json=test_payload_correct)
    
    assert response_correct.status_code == 200
    data_correct = response_correct.json()
    assert data_correct["percentage"] == 100
    assert data_correct["correct_answer"]["root_value"] == correct_val
    assert data_correct["correct_answer"]["visited_nodes"] == correct_nodes
    
    # Pas 2: Testăm un răspuns greșit
    test_payload_wrong = {
        "problem_seed": TEST_SEED,
        "root_value": 999, # Greșit
        "visited_nodes": -1 # Greșit
    }
    
    response_wrong = client.post("/api/evaluate/minmax", json=test_payload_wrong)
    assert response_wrong.status_code == 200
    data_wrong = response_wrong.json()
    assert data_wrong["percentage"] == 0
    assert "Valoarea rădăcinii este greșită" in data_wrong["explanation"]
    assert f"Corect: {correct_val}" in data_wrong["explanation"]