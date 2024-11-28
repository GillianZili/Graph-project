import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt
from data_cleaning import load_data


def degree_centrality(friends):
    deg_centrality = nx.degree_centrality(friends)
    print("Graph created with", friends.number_of_nodes(), "nodes and", friends.number_of_edges(), "edges.")
    sorted_deg_centrality = sorted(deg_centrality.items(), key=lambda x: x[1], reverse=True)[:100]   
   
    # top_degree_centrality = pd.DataFrame(sorted_deg_centrality, columns=['Name', 'Degree Centrality'])
    # top_degree_centrality.to_csv('top_degree_centrality.csv', index=False)

    return dict(sorted_deg_centrality)

    

def categorize_degree_centrality(deg_centrality):
    """
    Categorize nodes by degree centrality into 5 equal ranges and assign colors.

    Returns:
    - node_colors: Dictionary of node -> color based on degree centrality ranges.
    """
   
    categories = {
        'red': (0.1, 1),      
        'green': (0.04, 0.1),
        'blue': (0.02, 0.04),
        'gray': (0, 0.02)
    }

    
    # Categorize nodes based on centrality
    node_colors = {}
    for node, centrality in deg_centrality.items():
        print(f"Node: {node}, Centrality: {centrality}")
        for color, (low, high) in categories.items():
            if low <= centrality < high:
                node_colors[node] = color
                categorized = True
                break
        if not categorized:
            print(f"Node {node} with centrality {centrality} did not fit any category.")
    return node_colors


def plot_categorized_heatmap(friends, node_colors):
    """
    Plot a graph with nodes colored by categorized degree centrality.
    """
    
    
    colors = [node_colors.get(node, 'gray') for node in friends.nodes()]
    sizes = [
        100 if color == 'red' else
        30 if color == 'green' else
        20 if color == 'blue' else
        5  # Default size for other nodes
        for color in colors
    ]

    fig, ax = plt.subplots(figsize=(10, 8))
    pos = nx.spring_layout(friends, seed = 42)
    nx.draw(
        friends,
        pos,
        with_labels=False,
        node_color=colors,
        node_size= sizes, 
        font_size=10,
        font_weight='bold',
        edge_color='white'
    )

    # Add legend
    legend_labels = {
        'red': '0.01 - 1',      
        'green': '0.005 - 0.01',
        'blue': '0.001 - 0.005',
        'gray': '0 - 0.001'   
    }

    for color, label in legend_labels.items():
        ax.scatter([], [], c=color, label=label)

    ax.set_title(" Heat Map of for 3000 edges (deg cent)", fontsize=16)
    ax.legend(scatterpoints=1, frameon=True, labelspacing=1, title="Degree Centrality Ranges")
    plt.show()


def create_graph(friends):
 
    G = nx.Graph()
    G.add_edges_from(friends.edges())

   
    plt.figure(figsize=(10, 8))
    pos = nx.spring_layout(G) 
    
    nx.draw(
        G,
        pos,
        with_labels= False,    
        node_size = 10,
        node_color = 'lightgray',      
        # node_size = [30 if node in top_nodes else 3 for node in friends.nodes()],                 # Node size
        # node_color = ['red' if node in top_nodes else 'lightgray' for node in friends.nodes()],        # Node color
        font_size=10,                  
        font_weight='bold',           
        edge_color='white'            
    )
    plt.title("Nodes-Edges Graph", fontsize=16)
    plt.show()



file_path = 'filtered_edges_startified_sampling.csv'
friends = load_data(file_path)  
top_nodes = degree_centrality(friends)
print(top_nodes)
# node_colors = categorize_degree_centrality(top_nodes) # filter out for top people
# plot_categorized_heatmap(friends, node_colors)


# create_graph(friends) 
# subgraph = friends.subgraph(top_nodes)
