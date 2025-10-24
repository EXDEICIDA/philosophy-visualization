from graph_utils import load_and_build_graph, create_styled_network, save_network_html
import os
import shutil

def main():
    """
    Main function to run the graph generation process.
    """
    # Define file names and directories
    nodes_csv = "philosophy_nodes.csv"
    edges_csv = "philosophy_edges.csv"
    authors_csv = "philosophy_authors.csv"
    
    # GitHub Pages directory
    output_dir = "docs"
    output_html = os.path.join(output_dir, "index.html")
    lib_source_dir = "lib"
    lib_dest_dir = os.path.join(output_dir, "lib")

    print("1. Loading and building graph data...")
    G = load_and_build_graph(nodes_csv, edges_csv, authors_csv)

    if G:
        print("2. Styling the network...")
        net = create_styled_network(G)

        print(f"3. Saving final HTML to {output_html}...")
        save_network_html(net, output_html)

        # --- Copy lib directory for GitHub Pages ---
        print(f"4. Copying '{lib_source_dir}' to '{lib_dest_dir}'...")
        try:
            # Remove the destination directory if it exists, to ensure a clean copy
            if os.path.exists(lib_dest_dir):
                shutil.rmtree(lib_dest_dir)
            shutil.copytree(lib_source_dir, lib_dest_dir)
            print("   Successfully copied 'lib' directory.")
        except Exception as e:
            print(f"   Error copying 'lib' directory: {e}")
        # --- End of copy block ---

        print("\nProcess finished. To deploy on GitHub Pages:")
        print("1. Commit and push the 'docs' directory to your GitHub repository.")
        print("2. In your repository settings, go to 'Pages'.")
        print("3. Under 'Build and deployment', select 'Deploy from a branch' and choose the 'main' branch with the '/docs' folder.")
        print("4. Your site will be live at the URL provided by GitHub.")


# This makes the script runnable by typing 'python graph.py'
if __name__ == "__main__":
    main()