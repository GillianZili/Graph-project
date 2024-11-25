import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection

# from try1 import load_data, degree_centrality


def load_data(file_path):
    
    # Open the file and parse the edge list
    with open(file_path, "r") as Data:
        next(Data, None)  # Skip the first line (header)
        friends = nx.parse_edgelist(
            Data, 
            delimiter=',', 
            create_using=nx.Graph(), 
            nodetype = str  # Change to int if nodes are numeric
        )
    return friends


def degree_centrality(friends):
    deg_centrality = nx.degree_centrality(friends)
    sorted_deg_centrality = sorted(deg_centrality.items(), key=lambda x: x[1], reverse=True)[:200]
    top_degree_centrality = pd.DataFrame(sorted_deg_centrality, columns=['Name', 'Degree Centrality'])
    
    # print(deg_centrality)
    # return nx.degree_centrality(friends)
    return top_degree_centrality['Name'].tolist() #必留


def closeness_centrality(friends, top_people):
    
    subgraph = friends.subgraph(top_people)  
    print("Subgraph created with", subgraph.number_of_nodes(), "nodes and", subgraph.number_of_edges(), "edges.")

    print("Calculating closeness centrality for top 100 people...")
    closeness_centrality = nx.closeness_centrality(subgraph)
    sorted_closeness_centrality = sorted(closeness_centrality.items(), key=lambda x: x[1], reverse=True)[:50]

    top_closeness_centrality = pd.DataFrame(sorted_closeness_centrality, columns=['Name', 'Closeness Centrality'])
    top_closeness_centrality.to_csv('top_closeness_centrality.csv', index = False)
    print('create a csv file successfully')


    return top_closeness_centrality



# def plot_n_degree_connections(subgraph, source_node, degree):
    """
    Plot n-degree connections from a specific node in the subgraph.

    Parameters:
    - subgraph: NetworkX graph (subgraph to visualize)
    - source_node: Node to start from
    - degree: Degree of connections to plot (e.g., 1 for 1st-degree, 2 for 2nd-degree)
    """
    # Find neighbors up to the specified degree
    neighbors_at_degree = {source_node}
    visited = set()
    current_layer = {source_node}

    for _ in range(degree):
        next_layer = set()
        for node in current_layer:
            neighbors = set(subgraph.neighbors(node)) - visited
            next_layer.update(neighbors)
        visited.update(current_layer)
        current_layer = next_layer
        neighbors_at_degree.update(current_layer)

    # Identify edges connecting the nodes within the desired degree
    relevant_edges = [
        edge for edge in subgraph.edges() 
        if edge[0] in neighbors_at_degree and edge[1] in neighbors_at_degree
    ]

    # Define edge and node styles
    edge_colors = ['orange' if edge in relevant_edges or edge[::-1] in relevant_edges else 'white' for edge in subgraph.edges()]
    edge_widths = [1 if edge in relevant_edges or edge[::-1] in relevant_edges else 0.1 for edge in subgraph.edges()]
    node_colors = [
        'red' if node == source_node else 
        'green' if node in neighbors_at_degree else 
        'lightblue' 
        for node in subgraph.nodes()
    ]
    node_sizes = [
        100 if node == source_node else 
        30 if node in neighbors_at_degree else 
        5 
        for node in subgraph.nodes()
    ]

    # Plot the subgraph
    plt.figure(figsize=(8, 8))
    pos = nx.spring_layout(subgraph, pos={source_node: (0, 0)}, fixed=[source_node])  # Layout for positioning nodes
    nx.draw(
        subgraph,
        pos,
        with_labels=False,
        node_color=node_colors,
        node_size=node_sizes,
        edge_color=edge_colors,
        width=edge_widths,
        font_size=10,
        font_weight='bold'
    )
    plt.title(f"{degree}-Degree Connections from Node {source_node}", fontsize=16)
    plt.show()


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
            node_colors.append('green')  # 1st-degree neighbors
        elif node_degree_map.get(node) == 2:
            node_colors.append('blue')  # 2nd-degree neighbors
        else:
            node_colors.append('lightgray')  # Other nodes not in the desired range



    edge_colors = []
    for edge in subgraph.edges():
    # Check if the edge connects the source node to a 1st-degree neighbor
        if edge[0] == source_node and node_degree_map.get(edge[1]) == 1:
            edge_colors.append('orange')  # Source to 1st-degree
            widths.append(2)
        elif edge[1] == source_node and node_degree_map.get(edge[0]) == 1:
            edge_colors.append('orange')  # Source to 1st-degree
            widths.append(2)
        # Check if the edge connects a 1st-degree neighbor to a 2nd-degree neighbor
        elif node_degree_map.get(edge[0]) == 1 and node_degree_map.get(edge[1]) == 2:
            edge_colors.append('purple')  # 1st-degree to 2nd-degree
            widths.append(1)
        elif node_degree_map.get(edge[0]) == 2 and node_degree_map.get(edge[1]) == 1:
            edge_colors.append('purple')  # 1st-degree to 2nd-degree
            widths.append(1)
        else:
            # If the edge doesn't fit into these categories, ignore or assign a default style
            edge_colors.append('lightgray')  # Optional: Use a fallback color
            widths.append(0.1)  # Minimal width for unused edges

    # Define node sizes
    node_sizes = [
        300 if node == source_node else
        100 if node in node_degree_map and node_degree_map[node] == 1 else
        50 if node in node_degree_map and node_degree_map[node] == 2 else
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



file_path = 'filtered_edges.csv'
friends = load_data(file_path) 
top_people = degree_centrality(friends)

subgraph = friends.subgraph(top_people)
# print(closeness_centrality(subgraph, top_people))
plot_n_degree_connections(subgraph, '29023', 1)
plot_n_degree_connections(subgraph, '29023', 2)
# plot_n_degree_connections(subgraph, '29023', 3) #edge = 2 已經可以連結到大部分的點