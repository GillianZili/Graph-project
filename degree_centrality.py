import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt
from data_cleaning import load_data


# def load_data(file_path):  
#     # Open the file and parse the edge list
#     with open(file_path, "r") as Data:
#         next(Data, None)  # Skip the first line (header)
#         friends = nx.parse_edgelist(
#             Data, 
#             delimiter=',', 
#             create_using=nx.Graph(), 
#             nodetype = str
#         )
#     return friends


def degree_centrality(friends):
    deg_centrality = nx.degree_centrality(friends)
    sorted_deg_centrality = sorted(deg_centrality.items(), key=lambda x: x[1], reverse=True)[:200]
   

   
    top_degree_centrality = pd.DataFrame(sorted_deg_centrality, columns=['Name', 'Degree Centrality'])
    top_degree_centrality.to_csv('top_degree_centrality.csv', index=False)
  


    return nx.degree_centrality(friends) # used for heatmap
   
    # return top_degree_centrality['Name'].tolist() #必留
    

def categorize_degree_centrality(deg_centrality):
    """
    Categorize nodes by degree centrality into 5 equal ranges and assign colors.

    Returns:
    - node_colors: Dictionary of node -> color based on degree centrality ranges.
    """
   
    categories = {
        'red': (0.01, 0.1),      
        'lightgreen': (0.001, 0.01),
        'lightblue': (0.0006, 0.001),
        'gray': (0, 0.001)
    }

    
    # Categorize nodes based on centrality
    node_colors = {}
    for node, centrality in deg_centrality.items():
        for color, (low, high) in categories.items():
            if low <= centrality < high:
                node_colors[node] = color
                break

    return node_colors


def plot_categorized_heatmap(friends, node_colors):
    """
    Plot a graph with nodes colored by categorized degree centrality.
    """
    
    
    colors = [node_colors.get(node) for node in friends.nodes()]
    sizes = [
        500 if color == 'red' else
        250 if color == 'lightgreen' else
        100 if color == 'lightblue' else
        5  # Default size for other nodes
        for color in colors
    ]

    plt.figure(figsize=(12, 10))
    pos = nx.spring_layout(friends)
    nx.draw(
        friends,
        pos,
        with_labels=False,
        node_color=colors,
        node_size= sizes, #[100 if color in ['red', 'lightgreen', 'lightblue'] else 1 for color in colors],
        font_size=10,
        font_weight='bold',
        edge_color='white'
    )

    # Add legend
    legend_labels = {
        'red': 'above 0.01',  
        'green': '0.001 - 0.01',
        'blue': '0.0006 - 0.001',
        'gray': 'below 0.0006'      
    }

    for color, label in legend_labels.items():
        plt.scatter([], [], c=color, label=label)
    plt.legend(scatterpoints=1, frameon=True, labelspacing=1, title="Degree Centrality Ranges")

    # Show the plot
    plt.title("Categorized Heat Map of Nodes by Degree Centrality", fontsize=16)
    plt.show()


def create_graph(friends, top_nodes):
 
    G = nx.Graph()
    G.add_edges_from(friends.edges())

   
    plt.figure(figsize=(10, 8))
    pos = nx.spring_layout(G) 
    
    nx.draw(
        G,
        pos,
        with_labels= False,          
        node_size = [30 if node in top_nodes else 3 for node in friends.nodes()],                 # Node size
        node_color = ['red' if node in top_nodes else 'lightgray' for node in friends.nodes()],        # Node color
        font_size=10,                  
        font_weight='bold',           
        edge_color='white'            
    )
    plt.title("Nodes-Edges Graph", fontsize=16)
    plt.show()




file_path = 'filtered_edges.csv'
friends = load_data(file_path)  # Load the data
top_nodes = degree_centrality(friends)
node_colors = categorize_degree_centrality(top_nodes) # filter out for top people
subgraph = friends.subgraph(top_nodes)
plot_categorized_heatmap(subgraph, node_colors)


# create_graph(friends, top_nodes) 

