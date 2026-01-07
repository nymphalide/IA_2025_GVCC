"""
Templates for CSP (Constraint Satisfaction Problems).
Stochează textul enunțurilor pentru a asigura Single Source of Truth.
"""

CSP_TEXT_RO = {
    "title": "CSP: Problema Colorării Grafurilor",
    "description": (
        "Această problemă exemplifică un motor CSP (Constraint Satisfaction Problem) generic, instanțiat pe problema colorării grafurilor. "
        "Modelarea CSP este definită prin: variabilele corespunzătoare nodurilor grafului, domeniile reprezentate "
        "de culorile disponibile ({colors}) și constrângeri binare de inegalitate, conform cărora două noduri adiacente nu pot avea aceeași culoare."
    ),
    "requirement": (
        "Având variabilele, domeniile și constrângerile date, simulați rularea algoritmului Backtracking "
        "cu optimizarea {algorithm}. "
        "Introduceți asignarea finală a tuturor variabilelor (nodurilor) rezultată în urma aplicării acestui algoritm."
    ),
    "note": (
        "Observație: Algoritmul implementat este determinist. În cazul în care există mai multe opțiuni valide "
        "(pentru alegerea variabilei sau a valorii din domeniu), se va alege întotdeauna opțiunea cu indexul cel mai mic "
        "(ordine crescătoare a ID-ului nodului sau ordine alfabetică a culorii)."
    )
}