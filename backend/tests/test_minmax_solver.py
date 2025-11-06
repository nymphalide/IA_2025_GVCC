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
    # Funcția returnează acum 4 valori (tree, val, nodes, depth)
    tree1, val1, nodes1, depth1 = generate_and_solve_minmax(test_seed)
    
    # Rularea 2 (cu același seed)
    tree2, val2, nodes2, depth2 = generate_and_solve_minmax(test_seed)

    # Verificăm dacă rezultatele sunt identice
    assert val1 == val2
    assert nodes1 == nodes2
    assert depth1 == depth2
    # Verificăm și structura arborelui (convertită la dict pentru comparație ușoară)
    assert tree1.dict() == tree2.dict()
    
    # Verificăm valorile cunoscute pentru seed=42 (cu noua logică)
    # (seed=42 -> depth=4, root_breadth=2, C1_breadth=3, C2_breadth=2, ...)
    # Aceste valori au fost obținute rulând testul o dată și copiind rezultatul
    
    # Pentru seed=42:
    # 1. chosen_depth = randint(3, 4) -> 4
    # 2. root_breadth = randint(2, 3) -> 2
    # 3. C1_breadth = randint(2, 3) -> 3
    # 4. C2_breadth = randint(2, 3) -> 2
    # ... etc.
    # Leaf values: 18, 10, 1, 10, 20, 1, 7, 7, 18, 12, 10, 16, 12, 5
    
    assert depth1 == 4
    assert val1 == 10 
    assert nodes1 == 8