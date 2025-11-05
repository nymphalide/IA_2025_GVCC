import pytest
from app.logic.minmax_solver import generate_and_solve_minmax

def test_minmax_reproducibility_and_correctness():
    """
    Test 1 (Solver): Verifică dacă un seed fix produce mereu același
    arbore (implicit), aceeași valoare și același număr de noduri vizitate.
    """
    # Un seed arbitrar ales pentru acest test
    test_seed = 42
    
    # Rularea 1
    tree1, val1, nodes1 = generate_and_solve_minmax(test_seed, depth=3, breadth=2)
    
    # Rularea 2 (cu același seed)
    tree2, val2, nodes2 = generate_and_solve_minmax(test_seed, depth=3, breadth=2)

    # Verificăm dacă rezultatele sunt identice
    assert val1 == val2
    assert nodes1 == nodes2
    # Verificăm și structura arborelui (convertită la dict pentru comparație ușoară)
    assert tree1.dict() == tree2.dict()
    
    # Verificăm valorile cunoscute pentru seed=42, depth=3, breadth=2
    # Aceste valori au fost obținute rulând testul o dată și copiind rezultatul
    assert val1 == 13
    assert nodes1 == 5