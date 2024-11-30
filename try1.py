import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from data_cleaning import load_data



def load_data(node_interest_file, edge_file):

    # Load node-interest data
    node_interest_df = pd.read_csv(node_interest_file)
    nodes_with_interests = list(zip(node_interest_df['Node'], node_interest_df['Random_Variable']))

    # Load edge data
    edge_df = pd.read_csv(edge_file)
    edges = list(zip(edge_df.iloc[:, 0], edge_df.iloc[:, 1]))

    G = nx.Graph()
    for node, interest in nodes_with_interests:
        G.add_node(node, interest=interest)

    # Add edges
    G.add_edges_from(edges)
    return G, nodes_with_interests, edges
    


def connect_groups(G, nodes_with_interests):
    """
    Connects groups of nodes based on specific rules.

    Args:
        G (networkx.Graph): The input graph.
        nodes_with_interests (list of tuples): List of (node, interest) pairs.
    """
    # Group nodes by their interest
    groups = {i: [] for i in range(7)}  # Assuming interests range from 0 to 6
    for node, interest in nodes_with_interests:
        groups[interest].append(node)

    # Define group connection rules
    group_connections = {
        3: [0, 1],
        4: [1, 2],
        5: [0, 2],
        6: [3, 4, 5]
    }

    # Add edges based on the rules
    for group, connected_groups in group_connections.items():
        for connected_group in connected_groups:
            # Connect all nodes in the current group to all nodes in the connected group
            for node1 in groups[group]:
                for node2 in groups[connected_group]:
                    if not G.has_edge(node1, node2):  # Avoid duplicate edges
                        G.add_edge(node1, node2)

# def calculate_betweenness_with_interests(nodes_with_interests, edges):
    # """
    # Calculates betweenness centrality for a graph where nodes have interests.
    
    # Args:
    #     nodes_with_interests (list of tuples): A list where each tuple is (node, interest).
    #     edges (list of tuples): A list of edges as (node1, node2).
        
    # Returns:
    #     dict: A dictionary where keys are node interests (0-6) and values are lists of tuples
    #           (node, betweenness centrality).
    # """
    # # Create the graph
    # G = nx.Graph()
    
    # # Add nodes with interests
    # for node, interest in nodes_with_interests:
    #     G.add_node(node, interest=interest)
    
    # # Add edges
    # G.add_edges_from(edges)
    
    # # Calculate betweenness centrality
    # betweenness = nx.betweenness_centrality(G)

    # # Group centrality scores by interests
    # interests_centrality = {i: [] for i in range(7)}  # Assuming interests are 0-6
    # for node, centrality in betweenness.items():
    #     interest = G.nodes[node].get('interest', None)
    #     if interest is not None:
    #         interests_centrality[interest].append((node, centrality))

   

    # return interests_centrality


def main(node_interest_file, edge_file):
    # Load data from CSV files
    nodes_with_interests, edges = load_data(node_interest_file, edge_file)

    # Create the graph
    G = nx.Graph()

    # Add nodes with interests
    G.add_nodes_from([(node, {'interest': interest}) for node, interest in nodes_with_interests])

    # Add edges from the edge file
    G.add_edges_from(edges)

    # Connect groups based on specified rules
    connect_groups(G, nodes_with_interests)

    # Calculate betweenness centrality grouped by interests
    betweenness = nx.betweenness_centrality(G)

    # Group centrality scores by interests
    interests_centrality = {i: [] for i in range(7)}  # Assuming interests are 0-6
    for node, centrality in betweenness.items():
        interest = G.nodes[node].get('interest', None)
        if interest is not None:
            interests_centrality[interest].append((node, centrality))

    # Print results
    for interest, centralities in interests_centrality.items():
        print(f"Interest {interest}:")
        for node, centrality in centralities:
            print(f"  Node {node}: Betweenness Centrality = {centrality:.4f}")

 

# Example usage
node_interest_file = '/Users/tzuying/Desktop/CS5002_final project/selected_nodes_intetests.csv'  # Replace with your actual file path
edge_file = '/Users/tzuying/Desktop/CS5002_final project/selected_nodes_edges_file.csv'  # Replace with your actual file path

G, _, _ = load_data(node_interest_file, edge_file)
# main(node_interest_file, edge_file)



def visualize_betweenness_centrality(graph):
    """
    Visualizes a graph with nodes and edges highlighted based on betweenness centrality.
    
    Args:
        graph (networkx.Graph): The input graph.
    """
    # Calculate betweenness centrality for nodes and edges
    node_centrality = nx.betweenness_centrality(graph)

    # Normalize centrality values for visualization
    max_node_centrality = max(node_centrality.values()) if node_centrality else 1

    # Scale node size and color based on centrality
    node_sizes = [500 * (node_centrality[node] / max_node_centrality + 0.1) for node in graph.nodes()]
    node_colors = [node_centrality[node] for node in graph.nodes()]

    # Draw the graph
    plt.figure(figsize=(12, 8))
    pos = nx.spring_layout(graph, seed=42)

    # Draw edges in light gray
    nx.draw_networkx_edges(
        graph,
        pos,
        edge_color="gray",
        width=1.0
    )

    # Draw nodes
    nx.draw_networkx_nodes(
        graph,
        pos,
        node_color=node_colors,
        node_size=node_sizes,
        cmap=plt.cm.Reds
    )

    # Add colorbar for node betweenness centrality
    ax = plt.gca()  # Get current axes
    cbar_node = plt.colorbar(
        plt.cm.ScalarMappable(cmap=plt.cm.Reds, norm=plt.Normalize(vmin=min(node_centrality.values()), vmax=max_node_centrality)),
        ax=ax,
        shrink=0.7,
        pad=0.07
    )
    cbar_node.set_label("Node Betweenness Centrality", fontsize=10)

    plt.title("Graph Highlighting Nodes Based on Betweenness Centrality")
    plt.axis("off")
    plt.show()

visualize_betweenness_centrality(G)
