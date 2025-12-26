"""
Templates for CSP (Constraint Satisfaction Problems).
Stochează textul enunțurilor pentru a asigura Single Source of Truth.
"""

CSP_TEXT_RO = {
    "title": "Problema de Satisfacere a Constrângerilor (CSP)",
    "description": (
        "Se dă o hartă abstractă (graf) cu {node_count} regiuni (noduri). "
        "Unele regiuni sunt deja colorate. "
        "Trebuie să colorați restul regiunilor folosind culorile disponibile: {colors}, "
        "astfel încât două regiuni adiacente (conectate prin linie) să nu aibă aceeași culoare."
    ),
    "requirement": (
        "Completați culorile pentru nodurile rămase, simulând continuarea algoritmului Backtracking "
        "cu optimizarea {algorithm}.\n"
    ),
    "note": (
        "Observație: Algoritmul este determinist. În cazul în care există mai multe opțiuni valide (pentru alegerea variabilei "
        "sau a culorii), se alege întotdeauna opțiunea cu indexul cel mai mic (ordine crescătoare/alfabetică)."
    )
}