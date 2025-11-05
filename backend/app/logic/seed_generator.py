import random
import time
import uuid

# --- Funcții esențiale pentru Reproductibilitate (din progress.txt) ---

def set_seed(seed_id: int) -> int:
    """
    Setează seed-ul generatorului de numere pseudo-aleatoare Python.
    Orice apel ulterior la random.randint, random.choice, etc.,
    va produce aceeași secvență de rezultate dacă seed_id este același.
    """
    random.seed(seed_id)
    return seed_id


def get_new_seed() -> int:
    """
    Generează un seed nou, unic, bazat pe o combinație de timp și UUID.
    Acest seed este folosit când utilizatorul cere o problemă complet nouă.
    """
    # Combinația asigură că numărul rezultat este mare și puțin probabil să fie duplicat.
    unique_part = uuid.uuid4().int % 100000000
    time_part = int(time.time() * 100)
    
    # Folosim o limită (ex: 2^31 - 1) pentru a fi siguri că încape într-un int standard
    return (time_part + unique_part) % 2147483647