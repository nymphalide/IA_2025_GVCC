from graphviz import Digraph
import base64

def generate_tree_image_base64(tree_dict):
    """Generează o imagine PNG base64 din structura de arbore dict."""
    dot = Digraph(format="png")
    dot.attr("node", shape="circle", style="filled", fontname="Arial")

    def add_nodes_edges(node, depth=0):
        label = node["name"]
        if node.get("value") is not None:
            label += f"\n({node['value']})"
        color = "#A0D8F1" if depth % 2 == 0 else "#FFD6A5"
        dot.node(node["name"], label=label, fillcolor=color)
        for child in node.get("children", []):
            dot.edge(node["name"], child["name"])
            add_nodes_edges(child, depth + 1)

    add_nodes_edges(tree_dict)

    # returnăm imaginea ca base64
    img_bytes = dot.pipe(format="png")
    return base64.b64encode(img_bytes).decode("utf-8")
