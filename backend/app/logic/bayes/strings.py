def generate_problem_text(p):
    return f"""
Considerați următoarea rețea bayesiană:

- P(Ploaie) = {p['p_rain']}
- P(Stropitoare) = {p['p_sprinkler']}

Probabilități condiționate:
- P(Iarbă Umedă | Ploaie, Stropitoare) = {p['p_w_rs']}
- P(Iarbă Umedă | Ploaie, ¬Stropitoare) = {p['p_w_rns']}
- P(Iarbă Umedă | ¬Ploaie, Stropitoare) = {p['p_w_nrs']}
- P(Iarbă Umedă | ¬Ploaie, ¬Stropitoare) = {p['p_w_nrns']}

Întrebare:
Știind că iarba este umedă, care este probabilitatea ca a plouat?
"""
