import random
import time
import uuid


# Funcții esențiale pentru Reproductibilitate

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
    # Combinația asigură că numărul rezultat este mare și extrem de puțin probabil să fie duplicat.
    # Folosim modul operator (%) pentru a ne asigura că rezultatul este în limitele unui integer standard.
    unique_part = uuid.uuid4().int % 1000000000
    time_part = int(time.time() * 100)

    return time_part + unique_part


# Functie utilitara, optionala, dar buna pentru a nu folosi random.choice direct.
def safe_random_choice(sequence: list):
    """
    O functie wrapper simpla pentru a utiliza random.choice.
    """
    return random.choice(sequence)


# Bloc de testare locală (pentru a verifica funcționalitatea)
if __name__ == '__main__':
    print("--- Testare Modul Seed Generator ---")

    # 1. Testare Generare Seed Nou
    new_seed = get_new_seed()
    print(f"Seed nou generat: {new_seed}")

    # 2. Testare Reproductibilitate

    # Rulare 1
    set_seed(new_seed)
    results_run_1 = [random.randint(1, 100) for _ in range(5)]
    print(f"Rulare 1: {results_run_1}")

    # Rulare 2 (folosind ACELAȘI seed)
    set_seed(new_seed)
    results_run_2 = [random.randint(1, 100) for _ in range(5)]
    print(f"Rulare 2: {results_run_2}")

    is_identical = results_run_1 == results_run_2
    print(f"Secvențele sunt identice? {is_identical}")
    assert is_identical, "Eroare: Reproductibilitatea nu este garantată!"