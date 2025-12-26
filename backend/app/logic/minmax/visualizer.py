from graphviz import Digraph
import base64


def generate_tree_image_base64(tree_dict):
    dot = Digraph(format="png")
    # Setări implicite pentru noduri
    dot.attr("node", shape="ellipse", style="filled", fontname="Arial", fontsize="12")

    def add_nodes_edges(node):
        # Identificatorul unic rămâne name-ul intern (R, R1, R2...) pentru structura grafului
        node_id = node["name"]
        
        # Determinăm eticheta vizuală (Label)
        # Dacă are valoare (frunză), afișăm valoarea.
        # Dacă este nod intern, afișăm tipul (MIN sau MAX).
        if node.get("value") is not None:
            label = str(node["value"])
            # Frunzele: alb simplu sau gri deschis
            fillcolor = "#ffffff"
            shape = "ellipse" # MODIFICAT: Frunzele rotunde, la fel ca nodurile interne
        else:
            label = node["node_type"] # "MIN" sau "MAX"
            shape = "ellipse" # Nodurile interne ca cercuri/elipse
            
            # Culori distincte pentru MIN vs MAX
            if node["node_type"] == "MAX":
                fillcolor = "#A0D8F1" # Albastru deschis pentru MAX
            else:
                fillcolor = "#FFD6A5" # Portocaliu deschis pentru MIN

        dot.node(node_id, label=label, fillcolor=fillcolor, shape=shape)

        for child in node.get("children", []):
            dot.edge(node_id, child["name"])
            add_nodes_edges(child)

    add_nodes_edges(tree_dict)
    img_bytes = dot.pipe(format="png")
    return base64.b64encode(img_bytes).decode("utf-8")