import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import random


def initialize_counts(total_rows):
    """
    Calculates the portion of each value (0-6) such that the total counts do not exceed total_rows.
    """
    # Define proportions for each value
    proportions = {
        0: 0.43, # one common interest
        1: 0.32, # two common interests
    }

    counts = {value: int(total_rows * proportion) for value, proportion in proportions.items()}

    # Assign remaining rows to value 6
    counts[2] = total_rows - sum(counts.values()) # three common interests

    # Ensure no group exceeds the total number of rows
    for value in counts:
        counts[value] = min(counts[value], total_rows)

    # Ensure the sum of counts matches total_rows by reducing excess
    while sum(counts.values()) > total_rows:
        for value in sorted(counts.keys(), reverse=True):  # Adjust higher groups first
            if counts[value] > 0:
                counts[value] -= 1
                if sum(counts.values()) <= total_rows:
                    break

    return counts

def add_random_col(input_file, output_file):

    df = pd.read_csv(input_file)
    if df.empty or len(df.columns) < 1:
        raise ValueError("Input CSV must have at least one column.")
    
    total_rows = len(df)

    counts = initialize_counts(total_rows)
    
    values = []
    for value, count in counts.items():
        values.extend([value] * count)
    
 
    random.shuffle(values)
    
    # Add the new column to the DataFrame
    df['interest'] = values
    
    # Save the updated DataFrame to the output file
    df.to_csv(output_file, index=False)
    print(f"Updated CSV saved to {output_file}")


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
    

def calculate_betweenness_with_interests(edges_file, interests_file):
    """
    Calculate betweenness centrality for nodes based on their relationships
    and group by interests.
    """
    # load data and use the selected nodes, edges to create a subgraph
    edges_df = pd.read_csv(edges_file, header=None, names=["source", "target"])
    subgraph = nx.Graph()
    subgraph.add_edges_from(zip(edges_df["source"], edges_df["target"]))
    subgraph = nx.relabel_nodes(subgraph, str)
    interests_df = pd.read_csv(interests_file, header=None, names=["node", "interest"])


    # If two nodes have share interests, weight their edges.
    for _, row in interests_df.iterrows():
        node = row["node"]
        interest = row["interest"]
        if subgraph.has_node(node):
            subgraph.nodes[node]["interest"] = interest

        # Ensure all nodes have valid interests
    for node in subgraph.nodes():
        if "interest" not in subgraph.nodes[node]:
            subgraph.nodes[node]["interest"] = -1  # Default interest

    # Assign weights to edges
    for u, v in subgraph.edges():
        interest_u = int(subgraph.nodes[u].get("interest"))
        interest_v = int(subgraph.nodes[v].get("interest"))
        
        
        if interest_u == 0 and interest_v == 0:
            subgraph[u][v]["weight"] = 0.8
        elif interest_u == 1 and interest_v == 1:
            subgraph[u][v]["weight"] = 0.5
        elif interest_u == 2 and interest_v == 2:
            subgraph[u][v]["weight"] = 0.2      
        else:
            subgraph[u][v]["weight"] = 1  # Default weight


    for u, v, attr in subgraph.edges(data=True):
        print(f"Edge ({u}, {v}): Weight = {attr['weight']}")


   
    betweenness_centrality = nx.betweenness_centrality(subgraph, weight="weight")

    # create a csv file to store btw centrality data in descending
    sorted_btw = [(node, centrality) for node, centrality in betweenness_centrality.items() if centrality > 0]
    sorted_btw = sorted(sorted_btw, key=lambda x: x[1], reverse=True)
    btw_table = pd.DataFrame(sorted_btw, columns=['Node', 'Betweenness Centrality'])
    btw_table.to_csv('top_betweenness_centrality.csv', index=False)
    print('successfully create a btw csv file')

    print(btw_table.head())
    return btw_table


def visualize_betweenness_by_interest(graph, btw_data, interest=None):
    
    graph = nx.relabel_nodes(graph, str)
    centrality_dict = dict(zip(btw_data['Node'], btw_data['Betweenness Centrality']))

    max_centrality = max(centrality_dict.values()) if centrality_dict else 1
    node_sizes = [500 * (centrality_dict.get(node, 0) / max_centrality + 0.1) for node in graph.nodes()]
    node_colors = [centrality_dict.get(node, 0) for node in graph.nodes()]


    plt.figure(figsize=(12, 8))
    pos = nx.spring_layout(graph, seed=42)

    nx.draw_networkx_edges(
        graph,
        pos,
        edge_color="gray",
        width=1.0
    )

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
        plt.cm.ScalarMappable(cmap=plt.cm.Reds, norm=plt.Normalize(vmin=min(centrality_dict.values(), default=0), vmax=max_centrality)),
        ax=ax,
        shrink=0.7,
        pad=0.07
    )

    cbar_node.set_label("Node Betweenness Centrality", fontsize=10)

    title = f"Betweenness Centrality Visualization" + (f" (Interest {interest})" if interest is not None else "")
    plt.title(title)
    plt.axis("off")
    plt.axis('equal')
    plt.show()



def main():

    add_random_col('selected_nodes.csv', 'selected_nodes_intetests.csv')
    node_interest_file = 'selected_nodes_intetests.csv'
    edge_file = 'filtered_edges_selected_nodes_edges.csv'
    btw_data = calculate_betweenness_with_interests(edge_file, node_interest_file)

    edges_df = pd.read_csv(edge_file, header=None, names=["source", "target"])
    graph = nx.Graph()
    graph.add_edges_from(zip(edges_df["source"], edges_df["target"]))

    visualize_betweenness_by_interest(graph, btw_data)

main()

