import pandas as pd
import networkx as nx
from pyvis.network import Network

# --- Reusable Style Definitions ---

TYPE_COLORS = {
    "Field": "#1f77b4",  # blue
    "Subfield": "#ff7f0e",  # orange
    "Author": "#2ca02c",  # green
    "Work": "#d62728"  # red
}

TYPE_SIZES = {
    "Field": 35,  # H1: Biggest
    "Subfield": 20,  # H2: Medium
    "Author": 12,  # H3: Small
    "Work": 8  # H4: Smallest
}

LABEL_FONT_OPTIONS = """
{
  "nodes": {
    "font": {
      "face": "IBM Plex Mono",
      "size": 16,
      "mono": true
    }
  }
}
"""

# === THIS VARIABLE IS NOW UPDATED ===
TOOLTIP_STYLE = """
<style type="text/css">

  /* --- Fullscreen CSS --- */
  html, body {
    margin: 0 !important;
    padding: 0 !important;
    width: 100%;
    height: 100%;
    overflow: hidden; /* Prevents scrollbars */
  }

  /* --- PyVis/Bootstrap Override --- */
  .card, .card-body {
    padding: 0 !important;
    margin: 0 !important;
    border: none !important;
    width: 100%;
    height: 100%;
  }

  /* --- NEW: Remove Margin from PyVis's Empty h1 Tags --- */
  /* This is the fix for the top whitespace */
  h1, center {
    margin: 0 !important;
    padding: 0 !important;
  }
  /* --- End of new code --- */

  /* --- Import IBM Plex Mono from Google Fonts --- */
  @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono&display=swap');

  .vis-tooltip {
    /* --- Use the new font --- */
    font-family: "IBM Plex Mono", monospace; 
    font-size: 14px;
    background-color: #f0f0f0;
    color: #333;
    border: 1px solid #ccc;
    padding: 8px;
    border-radius: 4px;
    box-shadow: 0 2px 5px rgba(0,0,0,0.2);
  }
</style>
"""


# --- Graph Building Functions ---

def load_and_build_graph(nodes_file, edges_file, authors_file):
    """
    Loads all data from CSVs and builds the base NetworkX graph.
    """
    try:
        nodes = pd.read_csv(nodes_file)
        edges = pd.read_csv(edges_file)
        authors = pd.read_csv(authors_file)
    except FileNotFoundError as e:
        print(f"Error: Could not find file {e.filename}")
        print("Please make sure all CSV files are in the same directory.")
        return None

    G = nx.Graph()

    # === Add Nodes ===
    for _, row in nodes.iterrows():
        G.add_node(row['Label'], type=row['Type'], title=row['Label'])

    for _, row in authors.iterrows():
        G.add_node(row['Author'], type="Author", title=row['Author'])
        G.add_node(row['Work'], type="Work", title=f"\"{row['Work']}\"")

    # === Add Edges ===
    for _, row in edges.iterrows():
        G.add_edge(row['Source'], row['Target'], relation=row['Relationship'])

    for _, row in authors.iterrows():
        if pd.notna(row['Subfield']):
            G.add_edge(row['Subfield'], row['Author'], relation="wrote about")
        G.add_edge(row['Author'], row['Work'], relation="wrote")

    return G


def create_styled_network(G):
    """
    Takes a NetworkX graph and returns a styled PyVis network object.
    """
    net = Network(height="100vh", width="100%", bgcolor="#0a0a0a", font_color="white")
    net.barnes_hut(gravity=-25000, central_gravity=0.4, spring_length=130, spring_strength=0.05, damping=0.9)

    # Apply label fonts
    net.set_options(LABEL_FONT_OPTIONS)

    # Add all nodes with custom styles
    for node, data in G.nodes(data=True):
        node_type = data.get("type", "Subfield")
        color = TYPE_COLORS.get(node_type, "#cccccc")
        title = data.get("title", node)
        size = TYPE_SIZES.get(node_type, 10)
        net.add_node(node, label=node, title=title, color=color, size=size)

    # Add all edges
    for u, v, data in G.edges(data=True):
        relation_title = data.get("relation", "")
        net.add_edge(u, v, title=relation_title)

    return net


def save_network_html(net, filename):
    """
    Generates the HTML, injects custom tooltip CSS, and saves the file.
    """
    # 1. Generate the HTML content as a string
    html_content = net.generate_html(notebook=False)

    # 2. Insert custom tooltip style right before the </head> tag
    html_content = html_content.replace("</head>", f"{TOOLTIP_STYLE}\n</head>")

    # 3. Save the modified HTML to file
    try:
        with open(filename, "w", encoding="utf-8") as f:
            f.write(html_content)
        print(f"Successfully generated {filename} with custom styles.")
    except Exception as e:
        print(f"Error saving file: {e}")