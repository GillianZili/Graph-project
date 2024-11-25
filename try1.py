import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt



def load_data(file_path):  
    # Open the file and parse the edge list
    with open(file_path, "r") as Data:
        next(Data, None)  # Skip the first line (header)
        friends = nx.parse_edgelist(
            Data, 
            delimiter=',', 
            create_using=nx.Graph(), 
            nodetype = str
        )
    return friends


def degree_centrality(friends):
   
    deg_centrality = nx.degree_centrality(friends)
    sorted_deg_centrality = sorted(deg_centrality.items(), key=lambda x: x[1], reverse=True)[:2000]
    top_degree_centrality = pd.DataFrame(sorted_deg_centrality, columns=['Name', 'Degree Centrality'])
    
 
    # return nx.degree_centrality(friends) # used for heatmap
    
    return top_degree_centrality['Name'].tolist() #必留


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
    

    # deg_centrality = degree_centrality(friends)
    # node_colors = categorize_degree_centrality(deg_centrality)
    
    colors = [node_colors.get(node) for node in friends.nodes()]

    # Step 4: Plot the graph
    plt.figure(figsize=(12, 10))
    pos = nx.spring_layout(friends)  # Layout for positioning nodes
    nx.draw(
        friends,
        pos,
        with_labels=False,
        node_color=colors,
        node_size= [30 if color in ['red', 'lightgreen', 'lightblue'] else 1 for color in colors],
        font_size=10,
        font_weight='bold',
        edge_color='white'
    )

    # Add legend
    legend_labels = {
        'red': 'above 0.01',   # Highest group
        'green': '0.001 - 0.01',
        'blue': '0.0006 - 0.001',
        'gray': 'below 0.0006'      # Lowest group
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
        node_size = [10 if node in top_nodes else 3 for node in friends.nodes()],                 # Node size
        node_color = ['red' if node in top_nodes else 'lightblue' for node in friends.nodes()],        # Node color
        font_size=10,                  
        font_weight='bold',           
        edge_color='white'            
    )
    plt.title("Nodes-Edges Graph", fontsize=16)
    plt.show()



def create_subgraph(friends, top_people):
    '''
    After computing degree centrality, we filter out top 100 people.
    '''
    subgraph = friends.subgraph(top_people)
    plt.figure(figsize=(10, 8))
    pos = nx.spring_layout(subgraph)  # Layout for positioning nodes
    nx.draw(
        subgraph,
        pos,
        with_labels = False,              # Show labels for nodes
        node_size = 50,                 # Size of nodes
        node_color ='lightblue',        # Node color
        font_size = 10,                  # Font size for labels
        font_weight = 'bold',            # Font weight for labels
        edge_color = 'gray'              # Edge color
    )
    plt.title("Subgraph of Top 100 People", fontsize=16)
    plt.show()





file_path = 'filtered_edges.csv'
friends = load_data(file_path)  # Load the data
top_people = degree_centrality(friends)

# node_color = categorize_degree_centrality(top_nodes)
subgraph = friends.subgraph(top_people)
# plot_categorized_heatmap(friends, node_color) # include all nodes
# plot_categorized_heatmap(subgraph, node_color) # only top_node (~2000)

# print(closeness_centrality(friends,top_people))
