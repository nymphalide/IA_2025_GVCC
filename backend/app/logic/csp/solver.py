import random
import math
from typing import List, Dict, Tuple, Any, Optional
from app.logic.common.seed import set_seed
from app.logic.csp.strings import CSP_TEXT_RO
from app.schemas.csp_schemas import CspGraph, CspNode, CspEdge

# --- 1. DEFINIREA CONSTANTELOR ȘI A CULORILOR ---

COLOR_TRANSLATIONS = {
    "Blue": "Albastru",
    "Red": "Roșu",
    "Green": "Verde"
}

# Ordinea Română (Display): Albastru, Roșu, Verde -> ["Blue", "Red", "Green"]
RO_SORTED_COLORS = sorted(COLOR_TRANSLATIONS.keys(), key=lambda k: COLOR_TRANSLATIONS[k])

# --- DEFINIRE GRAFURI NOI (5, 7, 10 Noduri) ---

# GRAF 5: O structură simplă tip "Casă"
GRAPH_5 = {
    "nodes": [
        {"id": 1, "x": 50, "y": 10, "label": "1"}, # Vârf
        {"id": 2, "x": 90, "y": 40, "label": "2"},
        {"id": 3, "x": 75, "y": 90, "label": "3"},
        {"id": 4, "x": 25, "y": 90, "label": "4"},
        {"id": 5, "x": 10, "y": 40, "label": "5"}
    ],
    "edges": [
        (1,2), (2,3), (3,4), (4,5), (5,1), 
        (1,3), (1,4) 
    ]
}

# GRAF 7: Structură centrală tip floare/roată
GRAPH_7 = {
    "nodes": [
        {"id": 1, "x": 50, "y": 50, "label": "1"}, # Centru
        {"id": 2, "x": 50, "y": 10, "label": "2"},
        {"id": 3, "x": 85, "y": 30, "label": "3"},
        {"id": 4, "x": 85, "y": 70, "label": "4"},
        {"id": 5, "x": 50, "y": 90, "label": "5"},
        {"id": 6, "x": 15, "y": 70, "label": "6"},
        {"id": 7, "x": 15, "y": 30, "label": "7"}
    ],
    "edges": [
        (1,2), (1,3), (1,4), (1,5), (1,6), (1,7), 
        (2,3), (3,4), (4,5), (5,6), (6,7), (7,2)  
    ]
}

# GRAF 10: Structură complexă (inele interconectate)
GRAPH_10 = {
    "nodes": [
        # Inel Exterior (1-5)
        {"id": 1, "x": 50, "y": 5, "label": "1"},
        {"id": 2, "x": 95, "y": 35, "label": "2"},
        {"id": 3, "x": 80, "y": 90, "label": "3"},
        {"id": 4, "x": 20, "y": 90, "label": "4"},
        {"id": 5, "x": 5, "y": 35, "label": "5"},
        # Inel Interior (6-10)
        {"id": 6, "x": 50, "y": 25, "label": "6"},
        {"id": 7, "x": 75, "y": 45, "label": "7"},
        {"id": 8, "x": 65, "y": 75, "label": "8"},
        {"id": 9, "x": 35, "y": 75, "label": "9"},
        {"id": 10, "x": 25, "y": 45, "label": "10"}
    ],
    "edges": [
        # Inel Exterior
        (1,2), (2,3), (3,4), (4,5), (5,1),
        # Inel Interior (Stea)
        (6,8), (8,10), (10,7), (7,9), (9,6),
        # Conexiuni între inele
        (1,6), (2,7), (3,8), (4,9), (5,10)
    ]
}

# --- 2. LOGICA SOLVER ---

class CSPSolver:
    def __init__(self, graph_data: dict, algorithm: str):
        # 1. Inițializare Noduri (Sortate numeric)
        self.nodes = sorted([str(n["id"]) for n in graph_data["nodes"]], key=lambda x: int(x))
        
        # 2. Inițializare Adiacență (Vecini sortați numeric)
        self.adj = {n: [] for n in self.nodes}
        for u, v in graph_data["edges"]:
            su, sv = str(u), str(v)
            self.adj[su].append(sv)
            self.adj[sv].append(su)
        
        for n in self.adj:
            self.adj[n].sort(key=lambda x: int(x))

        self.algorithm = algorithm 
        
        # 3. Domenii inițiale (Sortate RO)
        self.domains = {n: RO_SORTED_COLORS[:] for n in self.nodes}
        
        self.assignments = {}
        self.assignment_history = [] 

    def check_constraint(self, var1, val1, var2, val2) -> bool:
        """
        Verifică constrângerea binară între două variabile.
        Aceasta este metoda centrală de abstractizare a CSP-ului.
        
        Pentru instanța curentă (Graph Coloring), constrângerea este INEGALITATEA.
        Dacă am avea N-Queens sau alte probleme, am schimba doar această metodă.
        """
        return val1 != val2

    def apply_initial_assignments(self, partial_map: Dict[str, str]):
        """
        Încarcă asignările parțiale și aplică constrângerile (pruning)
        pentru a asigura o stare inițială consistentă.
        """
        for var, val in partial_map.items():
            self.assignments[var] = val
            
            # Aplicăm constrângerile asupra vecinilor folosind metoda generică
            for neighbor in self.adj[var]:
                if neighbor not in self.assignments:
                    # Filtram domeniul vecinului bazat pe check_constraint
                    original_domain = self.domains[neighbor][:]
                    for neighbor_val in original_domain:
                        if not self.check_constraint(var, val, neighbor, neighbor_val):
                            if neighbor_val in self.domains[neighbor]:
                                self.domains[neighbor].remove(neighbor_val)
    
    def is_consistent(self, var, color, assignment):
        """Verifică conflictul cu vecinii deja asignați folosind constrângerea generică."""
        for neighbor in self.adj[var]:
            if neighbor in assignment:
                neighbor_val = assignment[neighbor]
                # Folosim check_constraint în loc de !=
                if not self.check_constraint(var, color, neighbor, neighbor_val):
                    return False
        return True

    def calculate_mrv_score(self, var):
        valid_count = 0
        possible_values = self.domains[var]
        
        for color in possible_values:
            if self.is_consistent(var, color, self.assignments):
                valid_count += 1
        return valid_count

    def select_unassigned_variable(self):
        unassigned = [v for v in self.nodes if v not in self.assignments]
        if not unassigned:
            return None

        candidates = []
        for var in unassigned:
            var_int = int(var)
            if self.algorithm == "MRV":
                score = self.calculate_mrv_score(var)
                candidates.append((score, var_int, var))
            else:
                candidates.append((0, var_int, var))
        
        candidates.sort()
        best_candidate = candidates[0][2]
        return best_candidate

    def order_domain_values(self, var):
        """Returnează valorile sortate conform ordinii RO_SORTED_COLORS."""
        current_domain = self.domains[var]
        return sorted(current_domain, key=lambda x: RO_SORTED_COLORS.index(x))

    def forward_check(self, var, value):
        pruned = {} 
        for neighbor in self.adj[var]:
            if neighbor not in self.assignments:
                # Verificăm fiecare valoare din domeniul vecinului față de noua asignare
                # folosind constrângerea generică
                to_remove = []
                for neighbor_val in self.domains[neighbor]:
                    if not self.check_constraint(var, value, neighbor, neighbor_val):
                        to_remove.append(neighbor_val)
                
                if to_remove:
                    if neighbor not in pruned: pruned[neighbor] = []
                    for val_to_remove in to_remove:
                        self.domains[neighbor].remove(val_to_remove)
                        pruned[neighbor].append(val_to_remove)
                    
                    if not self.domains[neighbor]:
                        return False, pruned
        return True, pruned

    def restore_domains(self, pruned):
        for var, values in pruned.items():
            for val in values:
                self.domains[var].append(val)
            self.domains[var].sort(key=lambda x: RO_SORTED_COLORS.index(x))

    def ac3(self):
        queue = [(xi, xj) for xi in self.nodes for xj in self.adj[xi]]
        local_domains = {k: v[:] for k, v in self.domains.items()}
        
        while queue:
            (xi, xj) = queue.pop(0)
            if self.revise(xi, xj, local_domains):
                if not local_domains[xi]:
                    return False, local_domains
                for xk in self.adj[xi]:
                    if xk != xj:
                        queue.append((xk, xi))
        return True, local_domains

    def revise(self, xi, xj, domains):
        removed = False
        to_remove = []
        for x in domains[xi]:
            found_support = False
            for y in domains[xj]:
                # Folosim constrângerea generică în loc de x != y
                if self.check_constraint(xi, x, xj, y):
                    found_support = True
                    break
            if not found_support:
                to_remove.append(x)
                removed = True
        
        for val in to_remove:
            domains[xi].remove(val)
        return removed

    def backtrack(self):
        var = self.select_unassigned_variable()
        if var is None:
            return True 

        for value in self.order_domain_values(var):
            if self.is_consistent(var, value, self.assignments):
                self.assignments[var] = value
                self.assignment_history.append(var)

                consistent = True
                pruned_info = {}
                old_domains_snapshot = None 

                if self.algorithm == "FC":
                    consistent, pruned_info = self.forward_check(var, value)
                elif self.algorithm == "AC-3":
                    old_domains_snapshot = {k: v[:] for k, v in self.domains.items()}
                    self.domains[var] = [value]
                    is_ac3_ok, new_domains = self.ac3()
                    if not is_ac3_ok:
                        consistent = False
                        self.domains = old_domains_snapshot
                    else:
                        self.domains = new_domains

                if consistent:
                    result = self.backtrack()
                    if result:
                        return True
                
                del self.assignments[var]
                self.assignment_history.pop()
                
                if self.algorithm == "FC":
                    self.restore_domains(pruned_info)
                elif self.algorithm == "AC-3":
                    if old_domains_snapshot:
                        self.domains = old_domains_snapshot
        
        return False

# --- 3. FUNCȚII PUBLICE ---

def get_graph_data(size: int):
    if size == 5: return GRAPH_5
    if size == 7: return GRAPH_7
    if size == 10: return GRAPH_10
    return GRAPH_5 

def generate_csp_problem(seed: int, params: Dict[str, Any]):
    set_seed(seed)
    
    # 1. Configurare
    graph_choices = [5, 7, 10]
    size = params.get("graph_size")
    if params.get("random_graph", True) or size not in graph_choices:
        size = random.choice(graph_choices)
    
    raw_data = get_graph_data(size)

    alg_choices = ["FC", "MRV", "AC-3"]
    algo = params.get("algorithm")
    if params.get("random_algo", True) or algo not in alg_choices:
        algo = random.choice(alg_choices)
    
    if params.get("random_prefill", True):
        ratio = random.choice([0.25, 0.50, 0.75])
    else:
        level = params.get("prefill_level")
        ratio = 0.25 if level == "LOW" else (0.50 if level == "MED" else 0.75)
    
    # 2. Golden Path Strategy
    temp_solver = CSPSolver(raw_data, algo)
    success = temp_solver.backtrack()

    partial_assignments = {}
    if success:
        target_count = max(1, int(size * ratio))
        all_nodes = list(temp_solver.assignments.keys())
        all_nodes.sort(key=lambda x: int(x))
        picked_nodes = random.sample(all_nodes, k=target_count)
        
        for node in picked_nodes:
            partial_assignments[node] = temp_solver.assignments[node]

    # 3. Final Solver
    final_solver = CSPSolver(raw_data, algo)
    final_solver.apply_initial_assignments(partial_assignments)

    # 4. Resetăm domeniile pentru Frontend (UI are nevoie de toate opțiunile vizuale)
    ui_domains = {n: RO_SORTED_COLORS[:] for n in final_solver.nodes}

    nodes_pyd = [CspNode(**n) for n in raw_data["nodes"]]
    edges_pyd = [CspEdge(source=u, target=v) for u, v in raw_data["edges"]]
    graph_obj = CspGraph(nodes=nodes_pyd, edges=edges_pyd)

    display_colors_text = [COLOR_TRANSLATIONS[c] for c in RO_SORTED_COLORS]
    
    text_data = {
        "title": CSP_TEXT_RO["title"],
        "description": CSP_TEXT_RO["description"].format(
            colors=", ".join(display_colors_text)
        ),
        "requirement": CSP_TEXT_RO["requirement"].format(algorithm=algo),
        "note": CSP_TEXT_RO["note"]
    }

    return {
        "seed": seed,
        "graph": graph_obj,
        "domains": ui_domains,
        "assignments": final_solver.assignments,
        "all_variables": final_solver.nodes,
        "available_colors": RO_SORTED_COLORS,
        "algorithm_name": algo,
        "text": text_data,
        "difficulty": f"Graph {size} | {algo}"
    }

def solve_complete_csp(seed: int, params: Dict[str, Any]):
    set_seed(seed)
    
    graph_choices = [5, 7, 10]
    size = params.get("graph_size")
    if params.get("random_graph", True) or size not in graph_choices:
        size = random.choice(graph_choices)
    
    raw_data = get_graph_data(size)

    alg_choices = ["FC", "MRV", "AC-3"]
    algo = params.get("algorithm")
    if params.get("random_algo", True) or algo not in alg_choices:
        algo = random.choice(alg_choices)
    
    if params.get("random_prefill", True):
        random.choice([0.25, 0.50, 0.75])
    
    solver = CSPSolver(raw_data, algo)
    solver.backtrack()

    return solver.assignments, solver.nodes