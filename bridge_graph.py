import pandas as pd
import numpy as np
import random
import networkx as nx
import matplotlib.pyplot as plt

def initialize_counts(total_rows):
    """
    Calculates the portion of each value (0–6) such that the total counts do not exceed total_rows.
    """
    # Define proportions for each value
    proportions = {
        0: 0.21,
        1: 0.23,
        2: 0.27,
        3: 0.09,
        4: 0.10,
        5: 0.08
    }

    
    counts = {value: int(total_rows * proportion) for value, proportion in proportions.items()}

    # Assign remaining rows to value 6
    counts[6] = total_rows - sum(counts.values())

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
    
    # Shuffle the values to randomize their order
    random.shuffle(values)
    
    # Add the new column to the DataFrame
    df['Random_Variable'] = values
    
    # Save the updated DataFrame to the output file
    df.to_csv(output_file, index=False)
    print(f"Updated CSV saved to {output_file}")

add_random_col('selected_nodes.csv', 'selected_nodes_intetests.csv')

def create_node_edge_graph(input_file):
    # Load the CSV file
    df = pd.read_csv(input_file)
    nodes = df['Node'].iloc
    edges = df['Random_Variable']
    
    #group nodes by their values
    groups = df.groupby('Random_Variable')['Node'].apply(list).to_dict()

    group_0 = groups.get(0, [])  
    group_1 = groups.get(1, [])  
    group_2 = groups.get(2, [])  
    group_3 = groups.get(3, [])  
    group_4 = groups.get(4, [])
    group_5 = groups.get(5, [])
    group_6 = groups.get(6, [])
  

    G = nx.Graph() # create a graph
    G.add_nodes_from(nodes) # add nodes

    # Connect nodes based on rules
    # 1. Fully connect nodes with value 0
    # G.add_edges_from((u, v) for i, u in enumerate(group_0) for v in group_0[i + 1:])
    # G.add_edges_from((u, v) for u in group_0 for v in group_2)
    # G.add_edges_from((u, v) for i, u in enumerate(group_1) for v in group_1[i + 1:])
    # G.add_edges_from((u, v) for u in group_1 for v in group_2)

    G.add_edges_from((u, v) for u in group_0 for v in group_3)
    G.add_edges_from((u, v) for u in group_1 for v in group_3)
    G.add_edges_from((u, v) for u in group_1 for v in group_4)
    G.add_edges_from((u, v) for u in group_2 for v in group_4)
    G.add_edges_from((u, v) for u in group_0 for v in group_5)
    G.add_edges_from((u, v) for u in group_2 for v in group_5)
    G.add_edges_from((u, v) for u in group_3 for v in group_6)
    G.add_edges_from((u, v) for u in group_4 for v in group_6)
    G.add_edges_from((u, v) for u in group_5 for v in group_6)


    return G, groups

def color_position(G, groups):
    color_palette = {
        0: "blue",
        1: "blue",
        2: "blue",
        3: "green",
        4: "green",
        5: "green",
        6: "red"
    }

    # Create a color map for the nodes
    color_map = []
    for node in G.nodes():
        for group, nodes in groups.items():
            if node in nodes:
                color_map.append(color_palette[group])
                break
        else:
            color_map.append("gray")  # Default color for nodes not in any group

    cluster_centers = {
        0: (10.0, 10.0),  
        1: (-10.0, 10.0),  
        2: (0, -10.0),  
        3: (0, 5),  
        4: (5, 0.0),   
        5: (-3, -5),   
        6: (0.0, 0.0),   
    }

    scatter_range = 1.5  # Range for random scattering around the cluster center

    # Assign random positions for nodes based on their group
    pos = {}
    for group, nodes in groups.items():
        center = cluster_centers[group]  # Get the cluster center for the group
        for node in nodes:
            # Generate random positions within the scatter range
            x = center[0] + random.uniform(-scatter_range, scatter_range)
            y = center[1] + random.uniform(-scatter_range, scatter_range)
            pos[node] = (x, y)


    return color_map, pos

def visualize_graph(G, color_map, pos):
    

    plt.figure(figsize=(12, 8))
    nx.draw(
        G,
        pos,
        with_labels=False,
        node_size=50,
        node_color=color_map,  # Apply the color map
        edge_color="lightgray",
        width=0.1
    )
    plt.title("Node-Edge Graph")
    plt.axis('on')
    plt.show()

G, group = create_node_edge_graph('selected_nodes_intetests.csv')
color_map, pos = color_position(G, group)
visualize_graph(G, color_map, pos)