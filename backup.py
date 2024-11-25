import networkx as nx
import matplotlib.pyplot as plt

# Create a symmetric graph
# G_symmetric = nx.Graph()
# G_symmetric.add_edge('Amy', 'Barbie')
# G_symmetric.add_edge('Amy', 'Ketty')
# G_symmetric.add_edge('Amy', 'Ken')

# Draw the graph
# nx.draw(G_symmetric, with_labels=True, node_color='lightblue', edge_color='gray', node_size=2000, font_size=15)
# plt.title("Graph Visualization")
# plt.show()

G_asymmetric = nx.DiGraph()
G_asymmetric.add_edge('A','B')
G_asymmetric.add_edge('A','D')
G_asymmetric.add_edge('C','A')
G_asymmetric.add_edge('D','E')

nx.draw(G_asymmetric, with_labels=True, node_color='lightblue', edge_color='gray', node_size=2000, font_size=15)
plt.title("Graph Visualization")
plt.show()


def closness_centrality(friends):
    closeness_centrality = nx.closeness_centrality(friends)


    # Sorting degree centrality and getting top 10
    sorted_closness_centrality = (sorted(closeness_centrality.items(), key=lambda x: x[1], reverse=True))[:100]

    # Creating dataframe
    top_closeness_centrality = pd.DataFrame(sorted_closness_centrality, columns = ['Name', 'Closeness Centrality'])
   
    print (top_closeness_centrality)
    return top_closeness_centrality



def plot_closeness_paths(subgraph, source_node):

    # friends = load_data(file_path)
    # subgraph = friends.subgraph(top_people)  
    
    # For a specific node, we use a dictionary to map the distance between this node and all the other nodes
    # { the specific node: lists of nodes to the other nodes}
    paths = nx.single_source_shortest_path(subgraph, source_node)
    
    path_edges = []
    for target, path in paths.items():
        path_edges += [(path[i], path[i+1]) for i in range(len(path) - 1)]


    edge_colors = ['red' if edge in path_edges or edge[::-1] in path_edges else 'lightgray' for edge in subgraph.edges()]
    edge_widths = [2 if edge in path_edges or edge[::-1] in path_edges else 0.01 for edge in subgraph.edges()]
    node_colors = ['orange' if node == source_node else 'lightblue' for node in subgraph.nodes()]
    node_sizes = [1000 if node == source_node else 30 for node in subgraph.nodes()]

    plt.figure(figsize=(12, 10))
    pos = nx.spring_layout(subgraph)  # Layout for positioning nodes
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
 
    plt.title(f"Closeness Path from Node {source_node}", fontsize=16)
    plt.show()



def plot_n_degree_connections(subgraph, source_node, degree):
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
    edge_colors = ['red' if edge in relevant_edges or edge[::-1] in relevant_edges else 'white' for edge in subgraph.edges()]
    edge_widths = [1 if edge in relevant_edges or edge[::-1] in relevant_edges else 0.1 for edge in subgraph.edges()]
    node_colors = [
        'orange' if node == source_node else 
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
    plt.figure(figsize=(12, 10))
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


def betweenness_centrality(friends, top_people):
   
    subgraph =  friends.subgraph(top_people)
    betweenness_centrality = nx.betweenness_centrality(subgraph)

    sorted_betweenness_centrality = sorted(betweenness_centrality.items(), key=lambda x: x[1], reverse=True)[:50]

    top_betweenness_centrality = pd.DataFrame(sorted_betweenness_centrality, columns=['Name', 'Betweenness Centrality'])
    
    print("Betweenness centrality calculated for top 50 people!")
    print(top_betweenness_centrality)

    return sorted_betweenness_centrality


def degree_heatmap():
       red_nodes = [node for node, color in zip(friends.nodes(), colors) if color == 'red']
    green_nodes = [node for node, color in zip(friends.nodes(), colors) if color == 'lightgreen']
    blue_nodes = [node for node, color in zip(friends.nodes(), colors) if color == 'lightblue']
    gray_nodes = [node for node, color in zip(friends.nodes(), colors) if color == 'lightgray']

    # Define sizes for each color group
    red_sizes = [300] * len(red_nodes)
    green_sizes = [100] * len(green_nodes)
    blue_sizes = [50] * len(blue_nodes)
    gray_sizes = [10] * len(gray_nodes)

    # Generate positions for nodes
    pos = nx.spring_layout(friends)  # Layout for positioning nodes

    # Plot each group layer by layer
    plt.figure(figsize=(12, 10))

    nx.draw_networkx_nodes(friends, pos, nodelist=gray_nodes, node_color='lightgray', node_size=gray_sizes, alpha=0.8)
    nx.draw_networkx_nodes(friends, pos, nodelist=blue_nodes, node_color='lightblue', node_size=blue_sizes, alpha=0.9)
    nx.draw_networkx_nodes(friends, pos, nodelist=green_nodes, node_color='lightgreen', node_size=green_sizes, alpha=1.0)
    nx.draw_networkx_nodes(friends, pos, nodelist=red_nodes, node_color='red', node_size=red_sizes, alpha=1.0)

    # Draw edges
    nx.draw_networkx_edges(friends, pos, edge_color = 'white', alpha=0.5)

    plt.title("Graph Visualization with Layered Nodes", fontsize=16)
    plt.axis('off')
    plt.show()
