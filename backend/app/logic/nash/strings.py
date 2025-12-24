"""
Templates for Nash Equilibrium problems.
Using f-strings placeholders like {rows} and {cols} to allow dynamic text generation.
"""

NASH_TEXT_RO = {
    "title": "Teoria Jocurilor: Echilibrul Nash",
    "description": (
        "Se consideră un joc în formă normală cu 2 jucători. "
        "Jucătorul 1 are {rows} strategii posibile (alege rândul), iar "
        "Jucătorul 2 are {cols} strategii posibile (alege coloana).\n"
        "Valorile din fiecare celulă reprezintă (Payoff Jucător 1, Payoff Jucător 2)."
    ),
    "requirement": (
        "Identificați dacă există un Echilibru Nash Pur în această matrice.\n"
        "Dacă există, precizați coordonatele acestuia sub forma (Index Rând, Index Coloană).\n"
        "Dacă nu există, selectați opțiunea corespunzătoare."
    )
}