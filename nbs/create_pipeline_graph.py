from pathlib import Path

import matplotlib.pyplot as plt
import networkx as nx

# Ensure the images directory exists
images_path = Path(__file__).parent.parent / "images"
images_path.mkdir(exist_ok=True)

# Create a directed graph
G = nx.DiGraph()

# Define the main pipeline components as nodes
nodes = {
    "input_recipes": "Input Recipe Files\n(Markdown)",
    "input_questions": "Input Questions\n(CSV)",
    "input_order": "Order Data\n(CSV)",
    "input_distances": "Planet Distances\n(CSV)",
    "input_illegal": "Illegal Ingredients\n(CSV)",
    "input_techniques": "Techniques Requirements\n(JSON)",
    "recipes_process": "Recipe Processing\n(LLM Extraction)",
    "questions_process": "Question Processing\n(LLM Extraction)",
    "restaurants_process": "Restaurant Processing\n(LLM Extraction)",
    "recipe_data": "Processed Recipe Data",
    "restaurant_data": "Processed Restaurant Data",
    "question_data": "Processed Question Data",
    "matching": "Recipe-Question Matching",
    "output_json": "Results\n(JSON)",
    "output_csv": "Final Output\n(CSV)",
}

# Add nodes to the graph with specific positions
positions = {
    "input_recipes": (0, 4),
    "input_questions": (0, 2),
    "input_order": (0, 3),
    "input_distances": (0, 1),
    "input_illegal": (6, 0),
    "input_techniques": (6, -1),
    "recipes_process": (4, 2.5),
    "restaurants_process": (2, 4),
    "questions_process": (2, 1.5),
    "restaurant_data": (4, 4),  # Moved to align with restaurants_process
    "recipe_data": (6, 2.5),
    "question_data": (6, 1.5),
    "matching": (8, 2.5),
    "output_json": (10, 2.5),
    "output_csv": (11, 2.5),
}

# Categorize nodes
input_nodes = [
    "input_recipes",
    "input_questions",
    "input_order",
    "input_distances",
    "input_illegal",
    "input_techniques",
]
output_nodes = ["output_json", "output_csv"]
processed_data_nodes = ["recipe_data", "restaurant_data", "question_data"]
processing_nodes = [
    node
    for node in nodes.keys()
    if node not in input_nodes
    and node not in output_nodes
    and node not in processed_data_nodes
]

# Define node colors and shapes by category
node_colors = []
node_shapes = []

# Add nodes to graph with category attributes
for node_id, label in nodes.items():
    if node_id in input_nodes:
        category = "input"
        color = "lightblue"
        shape = "s"  # square
    elif node_id in output_nodes:
        category = "output"
        color = "lightsalmon"  # light orange
        shape = "d"  # diamond
    elif node_id in processed_data_nodes:
        category = "processed_data"
        color = "lavender"  # light purple
        shape = "h"  # hexagon
    else:
        category = "processing"
        color = "lightgreen"
        shape = "o"  # circle
    G.add_node(node_id, label=label, category=category, color=color, shape=shape)

# Define connections between components
edges = [
    ("input_recipes", "recipes_process"),
    ("input_recipes", "restaurants_process"),
    ("input_order", "recipes_process"),
    ("input_questions", "questions_process"),
    ("input_distances", "questions_process"),
    ("recipes_process", "recipe_data"),
    ("restaurants_process", "restaurant_data"),
    ("questions_process", "question_data"),
    ("recipe_data", "matching"),
    (
        "restaurant_data",
        "recipes_process",
    ),  # Changed: restaurant_data now feeds into recipes_process
    ("question_data", "matching"),
    ("input_techniques", "matching"),
    ("input_illegal", "matching"),
    ("matching", "output_json"),
    ("output_json", "output_csv"),
]

# Add edges to graph
G.add_edges_from(edges)

# Create the figure
plt.figure(figsize=(16, 10))

# Get node attributes for drawing
node_colors = [G.nodes[n]["color"] for n in G.nodes()]
node_shapes = {
    shape: [n for n, attrs in G.nodes(data=True) if attrs["shape"] == shape]
    for shape in set(nx.get_node_attributes(G, "shape").values())
}

# Draw nodes with different shapes
for shape, nodes_with_shape in node_shapes.items():
    if not nodes_with_shape:
        continue

    nx.draw_networkx_nodes(
        G,
        pos=positions,
        nodelist=nodes_with_shape,
        node_shape=shape,
        node_color=[G.nodes[n]["color"] for n in nodes_with_shape],
        node_size=8000,
        alpha=1,
        linewidths=1.5,
    )

# Draw edges and labels
nx.draw_networkx_edges(
    G,
    pos=positions,
    edge_color="gray",
    arrows=True,
    arrowsize=20,
)

# Add labels to nodes
node_labels = nx.get_node_attributes(G, "label")
nx.draw_networkx_labels(G, positions, labels=node_labels, font_size=10)

# Add title
plt.title("HackAPizza DAGGS Pipeline", fontsize=16)

# Add legend
legend_elements = [
    plt.Line2D(
        [0],
        [0],
        marker="s",
        color="w",
        markerfacecolor="lightblue",
        markersize=15,
        label="Input",
    ),
    plt.Line2D(
        [0],
        [0],
        marker="o",
        color="w",
        markerfacecolor="lightgreen",
        markersize=15,
        label="Processing",
    ),
    plt.Line2D(
        [0],
        [0],
        marker="h",
        color="w",
        markerfacecolor="lavender",
        markersize=15,
        label="Processed Data",
    ),
    plt.Line2D(
        [0],
        [0],
        marker="d",
        color="w",
        markerfacecolor="lightsalmon",
        markersize=15,
        label="Output",
    ),
]
plt.legend(handles=legend_elements, loc="upper right")

# Save the figure
plt.tight_layout()
plt.savefig(images_path / "pipeline_graph.png", dpi=300, bbox_inches="tight")
plt.close()

print("Pipeline graph created and saved to images/pipeline_graph.png")
