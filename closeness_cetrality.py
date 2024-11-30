import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt
import random
from matplotlib.collections import LineCollection
from data_cleaning import load_data, node_filter


def degree_centrality(friends):
    deg_centrality = nx.degree_centrality(friends)
    sorted_deg_centrality = sorted(deg_centrality.items(), key=lambda x: x[1], reverse=True)
    top_degree_centrality = pd.DataFrame(sorted_deg_centrality, columns=['Name', 'Degree Centrality'])
    
    # print(deg_centrality)
    # return nx.degree_centrality(friends)
    return top_degree_centrality['Name'].tolist() #必留


def closeness_centrality(friends, top_people):
    
    subgraph = friends.subgraph(top_people)  
    print("Subgraph created with", subgraph.number_of_nodes(), "nodes and", subgraph.number_of_edges(), "edges.")
    
    closeness_centrality = nx.closeness_centrality(subgraph)
    sorted_closeness_centrality = sorted(closeness_centrality.items(), key=lambda x: x[1], reverse=True)[:100]

    top_closeness_centrality = pd.DataFrame(sorted_closeness_centrality, columns=['Name', 'Closeness Centrality'])
    top_closeness_centrality.to_csv('top_closeness_centrality.csv', index = False)
    print('create a csv file successfully')


    return top_closeness_centrality



def plot_n_degree_connections(subgraph, source_node, degree):
    """
    Plot n-degree connections from a specific node in the subgraph.

    Parameters:
    - subgraph: NetworkX graph (subgraph to visualize)
    - source_node: Node to start from
    - degree: Degree of connections to plot (e.g., 1 for 1st-degree, 2 for 2nd-degree)
    """
    # Initialize layers of neighbors
    neighbors_at_degree = {source_node}
    visited = set()
    current_layer = {source_node}
    node_degree_map = {source_node: 0}  # Map to store degree level for nodes

    for current_degree in range(1, degree + 1):
        next_layer = set()
        for node in current_layer:
            neighbors = set(subgraph.neighbors(node)) - visited
            next_layer.update(neighbors)
            for neighbor in neighbors:
                if neighbor not in node_degree_map:
                    node_degree_map[neighbor] = current_degree
        visited.update(current_layer)
        current_layer = next_layer
        neighbors_at_degree.update(current_layer)


    node_colors = []
    widths = []
    for node in subgraph.nodes():
        if node == source_node:
            node_colors.append('red')  # Source node
        elif node_degree_map.get(node) == 1:
            node_colors.append('lightgreen')  # 1st-degree neighbors
        elif node_degree_map.get(node) == 2:
            node_colors.append('blue')  # 2nd-degree neighbors
        else:
            node_colors.append('lightgray')  # Other nodes not in the desired range



    edge_colors = []
    for edge in subgraph.edges():
    # Check if the edge connects the source node to a 1st-degree neighbor
        if edge[0] == source_node and node_degree_map.get(edge[1]) == 1:
            edge_colors.append('orange')  # Source to 1st-degree
            widths.append(1)
        elif edge[1] == source_node and node_degree_map.get(edge[0]) == 1:
            edge_colors.append('orange')  # Source to 1st-degree
            widths.append(1)
        # Check if the edge connects a 1st-degree neighbor to a 2nd-degree neighbor
        elif node_degree_map.get(edge[0]) == 1 and node_degree_map.get(edge[1]) == 2:
            edge_colors.append('purple')  # 1st-degree to 2nd-degree
            widths.append(0.5)
        elif node_degree_map.get(edge[0]) == 2 and node_degree_map.get(edge[1]) == 1:
            edge_colors.append('purple')  # 1st-degree to 2nd-degree
            widths.append(1)
        else:
            # If the edge doesn't fit into these categories, ignore or assign a default style
            edge_colors.append('lightgray')  # Optional: Use a fallback color
            widths.append(0.1)  # Minimal width for unused edges

    # Define node sizes
    node_sizes = [
        100 if node == source_node else
        20 if node in node_degree_map and node_degree_map[node] == 1 else
        10 if node in node_degree_map and node_degree_map[node] == 2 else
        5
        for node in subgraph.nodes()
    ]

    
    pos = nx.spring_layout(subgraph, pos={source_node: (0, 0)}, fixed=[source_node])
    # pos = nx.spring_layout(subgraph, seed=42)
    nx.draw_networkx_edges(
    subgraph,
    pos,
    edgelist=subgraph.edges(),
    edge_color=edge_colors,
    width=widths,
    )

    nx.draw_networkx_nodes(
        subgraph,
        pos,
        nodelist=subgraph.nodes(),
        node_color=node_colors,
        node_size=node_sizes,
    )
    
    plt.figure(figsize=(10, 10))
    plt.title(f"{degree}-Degree Connections from Node {source_node}", fontsize=16)
    plt.show()



def random_node(friends):
    # Call the original function
    
    selected_nodes = node_filter(friends)  
    selected_nodes = {str(node) for node in selected_nodes}

    # Recreate logic for classification
    isolates = list(nx.isolates(friends))
    non_isolates = list(set(friends.nodes) - set(isolates))

    # Rebuild categories based on degree
    high_degree_nodes = [node for node in non_isolates if friends.degree[node] > 1000]
    mid_degree_nodes = [node for node in non_isolates if 30 < friends.degree[node] <= 1000]
    low_degree_nodes = [node for node in non_isolates if friends.degree[node] <= 30]

    # Filter the selected_nodes back into high/mid/low samples
    high_degree_sample = [node for node in selected_nodes if node in high_degree_nodes]
    mid_degree_sample = [node for node in selected_nodes if node in mid_degree_nodes]
    low_degree_sample = [node for node in selected_nodes if node in low_degree_nodes]

    print(f'high: {high_degree_sample}' )
    print(f'mid: {mid_degree_sample}' )
    print(f'low: {low_degree_sample}' )
    # Perform further random selections
    random_high = random.choice(high_degree_sample) if high_degree_sample else None
    random_mid = random.choice(mid_degree_sample) if mid_degree_sample else None
    random_low = random.choice(low_degree_sample) if low_degree_sample else None

    print(f'high: {random_high}, mid: {random_mid}, low: {random_low}')
    return random_high, random_mid, random_low



file_path = 'filtered_edges_startified_sampling.csv'
friends = load_data(file_path)
top_nodes = degree_centrality(friends)

data = closeness_centrality(friends, top_nodes)
subgraph = friends.subgraph(top_nodes)
print(random_node(friends))
_, mid, low = random_node(friends)

# plot_n_degree_connections(friends, mid, 1)
# plot_n_degree_connections(friends, low, 1)

# plot_n_degree_connections(subgraph, low, 1) #edge = 2 已經可以連結到大部分的點