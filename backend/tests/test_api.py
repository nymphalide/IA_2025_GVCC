import pytest
from fastapi.testclient import TestClient
from app.main import app

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

def test_evaluate_endpoint():
    """Test 3 (Endpoint): Verifică fluxul complet (generate + evaluate)."""
    
    # Pas 1: Generăm o problemă folosind un seed CUNOSCUT (din test_minmax_solver)
    # Pentru a face asta, "păcălim" API-ul suprascriind dependența get_new_seed
    # (Metodă mai avansată)
    
    # Pentru L6, testăm mai simplu: folosim seed-ul 42
    # știm că răspunsul corect este val=13, nodes=5
    
    test_payload = {
        "problem_seed": 42,
        "root_value": 13, # Răspuns corect
        "visited_nodes": 5  # Răspuns corect
    }
    
    response = client.post("/api/evaluate/minmax", json=test_payload)
    
    assert response.status_code == 200
    data = response.json()
    assert data["percentage"] == 100
    assert data["correct_answer"]["root_value"] == 13
    
    # Testăm un răspuns greșit
    test_payload_wrong = {
        "problem_seed": 42,
        "root_value": 99, # Greșit
        "visited_nodes": 99 # Greșit
    }
    
    response_wrong = client.post("/api/evaluate/minmax", json=test_payload_wrong)
    assert response_wrong.status_code == 200
    data_wrong = response_wrong.json()
    assert data_wrong["percentage"] == 0
    assert "Valoarea rădăcinii este greșită" in data_wrong["explanation"]