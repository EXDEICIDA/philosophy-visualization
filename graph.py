# Import the functions from your new utility file
from graph_utils import load_and_build_graph, create_styled_network, save_network_html
import webbrowser
import os  # Used for getting the full file path


def main():
    """
    Main function to run the graph generation process.
    """
    # Define file names
    nodes_csv = "philosophy_nodes.csv"
    edges_csv = "philosophy_edges.csv"
    authors_csv = "philosophy_authors.csv"
    output_html = "philosophy_extended_network.html"

    print("1. Loading and building graph data...")
    G = load_and_build_graph(nodes_csv, edges_csv, authors_csv)

    if G:
        print("2. Styling the network...")
        net = create_styled_network(G)

        print(f"3. Saving final HTML to {output_html}...")
        save_network_html(net, output_html)

        # --- This block opens the file in your browser ---
        print(f"4. Opening {output_html} in your browser...")
        try:
            # Get the full absolute path for the file
            full_path = os.path.realpath(output_html)
            webbrowser.open(f"file://{full_path}")
        except Exception as e:
            print(f"Could not open browser: {e}")
        # --- End of browser-opening block ---

        print("\nProcess finished.")


# This makes the script runnable by typing 'python graph.py'
if __name__ == "__main__":
    main()