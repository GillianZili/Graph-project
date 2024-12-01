import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt
import random
from matplotlib.collections import LineCollection
from data_cleaning import load_data, node_filter



def closeness_centrality(friends):
       
    closeness_centrality = nx.closeness_centrality(friends)
    sorted_closeness_centrality = sorted(closeness_centrality.items(), key=lambda x: x[1], reverse=True)[:100]

    top_closeness_centrality = pd.DataFrame(sorted_closeness_centrality, columns=['Name', 'Closeness Centrality'])
    top_closeness_centrality.to_csv('top_closeness_centrality.csv', index = False)
    print('create a closeness csv file successfully')

    return top_closeness_centrality

def get_first_degree_connections(graph, source_node):

    # create a list to store all the first degree connections of source node
    first_degree_nodes = list(graph.neighbors(source_node))
    return first_degree_nodes


def node_and_edge_styles(graph, source_nodes):
    
    neighbors = set()
    for node in source_nodes:
        if node in graph:
            neighbors.update(graph.neighbors(node))


    node_sizes = []
    for node in graph.nodes():
        if node in source_nodes:
            node_sizes.append(100) 
        elif node in neighbors:
            node_sizes.append(50)  
        else:
            node_sizes.append(20)  


    edge_widths = [
        4 if (edge[0] == source_nodes and edge[1] in neighbors) or 
             (edge[1] == source_nodes and edge[0] in neighbors) else 
        0.5
        for edge in graph.edges()
    ]

    return node_sizes, edge_widths


def plot_source_node_and_neighbors(graph, source_node):

    # we have two kinds of source_node, one is a single node, one is a list
    if isinstance(source_node, (list, set)):
        source_nodes = set(source_node)
    else:
        source_nodes = {source_node}

    # Check for invalid nodes
    invalid_nodes = [node for node in source_nodes if node not in graph]
    if invalid_nodes:
        raise ValueError(f"The following source nodes do not exist in the graph: {invalid_nodes}")
  
    
    neighbors = set()
    for node in source_nodes:
        neighbors.update(graph.neighbors(node))

    # Categorize nodes
    node_colors = []
    for node in graph.nodes():
        if node in source_nodes:
            node_colors.append("red")
        elif node in neighbors:
            node_colors.append("green") 
        else:
            node_colors.append("lightgray") 

    # Categorize edges
    edge_colors = []
    for edge in graph.edges():
        if (edge[0] in source_nodes and edge[1] in neighbors) or (edge[1] in source_nodes and edge[0] in neighbors):
            edge_colors.append("orange")  # Edges connecting source nodes to neighbors
        else:
            edge_colors.append("white")  # Other edges


    pos = nx.spring_layout(graph, seed=42)
    node_sizes, edge_widths = node_and_edge_styles(graph, source_node)


    plt.figure(figsize=(12, 8))
    nx.draw(
        graph,
        pos,
        with_labels=False,
        node_color=node_colors,
        edge_color=edge_colors,
        node_size=node_sizes,
        width=edge_widths,
        font_size=10,
    )
    # plt.title(f"Graph Highlighting {source_node} and Its Neighbors", fontsize=16)
    plt.axis('equal')
    plt.show()


def random_node(friends):
    # get the selected nodes from load data and reclassify them again
    selected_nodes = node_filter(friends)  
    selected_nodes = {str(node) for node in selected_nodes}

    # Recreate logic for classification
    isolates = list(nx.isolates(friends))
    non_isolates = list(set(friends.nodes) - set(isolates))

    # Rebuild categories based on degree
    high_degree_nodes = [node for node in non_isolates if friends.degree[node] > 200]
    mid_degree_nodes = [node for node in non_isolates if 30 < friends.degree[node] <= 200]
    low_degree_nodes = [node for node in non_isolates if friends.degree[node] <= 30]


    # Filter the selected_nodes back into high/mid/low samples
    high_degree_sample = [node for node in selected_nodes if node in high_degree_nodes]
    mid_degree_sample = [node for node in selected_nodes if node in mid_degree_nodes]
    low_degree_sample = [node for node in selected_nodes if node in low_degree_nodes]


    # choose one node from each group
    random_high = random.choice(high_degree_sample) if high_degree_sample else None
    random_mid = random.choice(mid_degree_sample) if mid_degree_sample else None
    random_low = random.choice(low_degree_sample) if low_degree_sample else None


    return random_high, random_mid, random_low


def main():
    file_path = 'filtered_edges_startified_sampling.csv'
    friends = load_data(file_path)
    
    closeness_centrality(friends) # create a closeness csv file 

    high, mid, low = random_node(friends)

    # first_degree_nodes_low = get_first_degree_connections(friends, low)
    # plot_source_node_and_neighbors(friends, low)
    # plot_source_node_and_neighbors(friends, first_degree_nodes_low)

    # first_degree_nodes_mid= get_first_degree_connections(friends, mid)
    # plot_source_node_and_neighbors(friends, mid)
    # plot_source_node_and_neighbors(friends, first_degree_nodes_mid)

    first_degree_nodes_high = get_first_degree_connections(friends, high)
    plot_source_node_and_neighbors(friends, high)
    plot_source_node_and_neighbors(friends, first_degree_nodes_high)

main()
