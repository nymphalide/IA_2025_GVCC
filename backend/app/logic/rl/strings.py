"""
Templates for RL problems.
Include reguli explicite de fizică (coliziuni, acțiuni) pentru claritate.
"""

RL_TEXT_RO = {
    "value_iteration": {
        "title": "Procese Decizionale Markov: Actualizare Bellman", # Conform Curs 7, pg 2
        "description": (
            "Se consideră următorul grid de dimensiune {rows}x{cols} (vezi figura).\n" # Conform Examen A-MR
            "Stările Verzi sunt terminale cu recompensă +1.0.\n" # Conform Curs 7, pg 3
            "Stările Roșii sunt terminale cu recompensă -1.0.\n"
            "Orice stare neterminală are o recompensă r(s) = {step_reward}.\n" # Conform Curs 7, pg 3 (fără "cost de existență")
            "Factorul de discount este γ = {gamma}.\n\n" # Conform Curs 7, pg 41
            "REGULI DE TRANZIȚIE:\n"
            "1. Agentul poate alege 4 acțiuni: Nord, Sud, Est, Vest.\n"
            "2. Modelul este determinist (probabilitatea de tranziție P(s'|s,a) = 1 pentru direcția aleasă).\n" # Clarificare necesară pt rezolvare
            "3. IMPORTANT: Dacă agentul lovește un zid (negru) sau marginea gridului, acesta rămâne în starea curentă."
        ),
        "requirement": (
            "Presupunând că inițial utilitățile stărilor neterminale sunt 0, iar ale celor terminale sunt fixate la recompensele lor, "
            "calculați utilitatea U₁ (sau V₁) pentru starea {target} după o iterație de propagare (Bellman Update)." # Conform Curs 7, pg 2
        )
    },
    "q_learning": {
        "title": "Reinforcement Learning: Q-Learning Update",
        "description": (
            "Un agent explorează mediul și execută următoarea tranziție:\n"
            "• Stare curentă (s): {state}\n"
            "• Acțiune (a): {action}\n"
            "• Recompensă primită (r): {reward}\n"
            "• Stare nouă (s'): {next_state}\n\n"
            "Informații cunoscute din tabelul Q:\n"
            "• Valoarea curentă Q(s, a) = {q_current}\n"
            "• Estimările pentru starea nouă s': {q_next_values}\n\n"
            "Parametri:\n"
            "• Rata de învățare α = {alpha}\n"
            "• Factorul de discount γ = {gamma}"
        ),
        "requirement": (
            "Calculați noua valoare actualizată pentru Q(s, a) folosind regula Q-Learning."
        )
    }
}