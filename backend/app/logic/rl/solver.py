import random
from typing import Tuple, Dict, List, Any
from app.logic.common.seed import set_seed
from app.logic.rl.strings import RL_TEXT_RO
from app.schemas.rl_schemas import GridConfig


def _generate_grid_layout(rows, cols, seed):
    # Generare simplă: Terminale în colțuri opuse, un zid random
    random.seed(seed)
    walls = []

    # Plasăm un zid random (dar nu în colțuri)
    wall_r = random.randint(0, rows - 2)
    wall_c = random.randint(1, cols - 2)
    walls.append((wall_r, wall_c))

    terminals = {}
    # Terminal pozitiv (colț dreapta-sus)
    terminals[f"0,{cols - 1}"] = 1.0
    # Terminal negativ (sub cel pozitiv)
    terminals[f"1,{cols - 1}"] = -1.0

    return walls, terminals


def generate_value_iteration(seed: int, params: Dict[str, Any]):
    set_seed(seed)
    rows = params.get("rows", 3)
    cols = params.get("cols", 4)
    gamma = params.get("gamma", 0.9)
    step_reward = params.get("step_reward", -0.04)

    walls_list, terminals = _generate_grid_layout(rows, cols, seed)

    # --- FIX DIVERSIFICARE: Alegem o țintă aleatoare relevantă ---
    # Căutăm toate stările care sunt vecine cu un terminal (Verde sau Roșu)
    # Astfel, calculul Max() va avea cel puțin un termen interesant (1.0 sau -1.0).

    candidates = []

    # Iterăm prin toate terminalele
    for t_loc in terminals.keys():
        tr, tc = map(int, t_loc.split(','))

        # Verificăm cei 4 vecini
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = tr + dr, tc + dc

            # Verificăm validitatea stării candidate:
            # 1. Să fie în interiorul hărții
            if not (0 <= nr < rows and 0 <= nc < cols):
                continue
            # 2. Să nu fie zid
            if (nr, nc) in walls_list:
                continue
            # 3. Să nu fie ea însăși o stare terminală (vrem să calculăm pt o stare normală)
            if f"{nr},{nc}" in terminals:
                continue

            candidates.append((nr, nc))

    # Eliminăm duplicatele (o stare poate fi vecină cu două terminale)
    candidates = sorted(list(set(candidates)))

    if candidates:
        target_r, target_c = random.choice(candidates)
    else:
        # Fallback extrem (dacă terminalele sunt complet blocate de ziduri)
        # Alegem pur și simplu o celulă liberă random (deși calculul va fi plictisitor)
        valid_cells = []
        for r in range(rows):
            for c in range(cols):
                if (r, c) not in walls_list and f"{r},{c}" not in terminals:
                    valid_cells.append((r, c))

        target_r, target_c = random.choice(valid_cells) if valid_cells else (0, 0)

    target_key = f"{target_r},{target_c}"

    # 2. Calculăm valoarea corectă (O singură iterație Bellman)
    # U1(s) = R(s) + gamma * max_a( U0(s') )

    possible_values = []
    moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Nord, Sud, Vest, Est

    for dr, dc in moves:
        nr, nc = target_r + dr, target_c + dc

        # Logică perete/margine: Dacă lovim ceva, rămânem pe loc (target_r, target_c)
        if not (0 <= nr < rows and 0 <= nc < cols) or (nr, nc) in walls_list:
            nr, nc = target_r, target_c

        # Obținem utilitatea vecinului (U0)
        # U0 este 0 pentru neterminale, și Reward-ul pentru terminale
        neighbor_key = f"{nr},{nc}"
        u0_neighbor = terminals.get(neighbor_key, 0.0)

        possible_values.append(u0_neighbor)

    max_next_u = max(possible_values)
    correct_value = step_reward + gamma * max_next_u

    # 3. Construim textul
    text_data = {
        "title": RL_TEXT_RO["value_iteration"]["title"],
        "description": RL_TEXT_RO["value_iteration"]["description"].format(
            rows=rows, cols=cols, step_reward=step_reward, gamma=gamma
        ),
        "requirement": RL_TEXT_RO["value_iteration"]["requirement"].format(
            target=f"({target_r}, {target_c})"
        )
    }

    grid_obj = GridConfig(
        rows=rows, cols=cols, walls=walls_list,
        terminals=terminals, step_reward=step_reward, gamma=gamma
    )

    return grid_obj, None, text_data, target_key, correct_value


def generate_q_learning(seed: int, params: Dict[str, Any]):
    set_seed(seed)
    alpha = params.get("alpha", 0.1)
    gamma = params.get("gamma", 0.9)

    # Generăm date sintetice pentru scenariu
    states = ["A", "B", "C", "D", "E"]
    actions = ["Nord", "Sud", "Est", "Vest"]

    # Alegem random o tranziție
    curr_s = random.choice(states)
    action = random.choice(actions)
    next_s = random.choice([s for s in states if s != curr_s])  # Să se miște undeva
    reward = random.choice([-2, 2, 4, 10, -5])  # Valori tipice examen

    q_current = round(random.uniform(0.1, 0.5), 2)

    # Generăm valori Q pentru starea următoare
    q_next_vals = {a: round(random.uniform(0.0, 1.0), 2) for a in actions}
    max_q_next = max(q_next_vals.values())

    # Calculăm răspunsul corect
    # Q_new = Q_old + alpha * (R + gamma * max_Q_next - Q_old)
    td_target = reward + gamma * max_q_next
    td_error = td_target - q_current
    correct_value = q_current + alpha * td_error

    # Formatăm dicționarul pentru afișare
    q_next_str = ", ".join([f"{k}: {v}" for k, v in q_next_vals.items()])

    text_data = {
        "title": RL_TEXT_RO["q_learning"]["title"],
        "description": RL_TEXT_RO["q_learning"]["description"].format(
            state=curr_s, action=action, reward=reward, next_state=next_s,
            q_current=q_current, q_next_values=q_next_str,
            alpha=alpha, gamma=gamma
        ),
        "requirement": RL_TEXT_RO["q_learning"]["requirement"]
    }

    q_data = {
        "q_current": q_current,
        "max_q_next": max_q_next,
        "reward": reward
    }

    return None, q_data, text_data, "Q_UPDATE", correct_value


def generate_rl_problem(seed: int, params: Dict[str, Any]):
    p_type = params.get("type", "value_iteration")

    if p_type == "q_learning":
        return generate_q_learning(seed, params)
    else:
        return generate_value_iteration(seed, params)