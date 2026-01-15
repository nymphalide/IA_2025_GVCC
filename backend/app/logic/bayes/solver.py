import random
from app.logic.common.seed import set_seed


def generate_bayes_problem(seed: int | None = None, custom_priors: dict | None = None):

    if seed is not None:
        set_seed(seed)
        random.seed(seed)

    if custom_priors is not None:
        p_rain = round(custom_priors["p_rain"], 2)
        p_sprinkler = round(custom_priors["p_sprinkler"], 2)
    else:
        p_rain = round(random.uniform(0.2, 0.6), 2)
        p_sprinkler = round(random.uniform(0.2, 0.6), 2)

    # ⚠️ CONDITIONALS RĂMÂN RANDOM (CA ÎN VERSIUNEA TA ORIGINALĂ)
    p_w_rs = round(random.uniform(0.8, 0.99), 2)
    p_w_rns = round(random.uniform(0.5, 0.9), 2)
    p_w_nrs = round(random.uniform(0.5, 0.9), 2)
    p_w_nrns = round(random.uniform(0.01, 0.2), 2)

    problem = {
        "p_rain": p_rain,
        "p_sprinkler": p_sprinkler,
        "p_w_rs": p_w_rs,
        "p_w_rns": p_w_rns,
        "p_w_nrs": p_w_nrs,
        "p_w_nrns": p_w_nrns,
    }

    solution = compute_posterior(problem)

    return problem, solution



def compute_posterior(p):
    p_r = p["p_rain"]
    p_s = p["p_sprinkler"]

    # Total probability of WetGrass
    p_w = (
        p["p_w_rs"] * p_r * p_s +
        p["p_w_rns"] * p_r * (1 - p_s) +
        p["p_w_nrs"] * (1 - p_r) * p_s +
        p["p_w_nrns"] * (1 - p_r) * (1 - p_s)
    )

    posterior = (p["p_w_rs"] * p_r * p_s +
                 p["p_w_rns"] * p_r * (1 - p_s)) / p_w

    return round(posterior, 4)
