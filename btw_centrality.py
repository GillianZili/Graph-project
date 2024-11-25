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


def betweenness_centrality(friends):
   
    # subgraph =  friends.subgraph(top_people)
    betweenness_centrality = nx.betweenness_centrality(friends)
    sorted_betweenness_centrality = sorted(betweenness_centrality.items(), key=lambda x: x[1], reverse=True)[:50]
    top_betweenness_centrality = pd.DataFrame(sorted_betweenness_centrality, columns=['Name', 'Betweenness Centrality'])
    
    # print("Betweenness centrality calculated for top 50 people!")
    # print(top_betweenness_centrality)
    top_betweenness_centrality.to_csv('top_betweenness_centrality.csv', index=False)

    return top_betweenness_centrality
    return nx.betweenness_centrality(friends)




def categorize_btw_centrality(deg_centrality):
    """
    Categorize nodes by degree centrality into 5 equal ranges and assign colors.

    Returns:
    - node_colors: Dictionary of node -> color based on degree centrality ranges.
    """
   
    categories = {
        'red': (0.1, float('inf')),      
        'lightgreen': (0.001, 0.1),
        'lightblue': (0.0001, 0.001),
        'gray': (0, 0.0001)
    }

    
    # Categorize nodes based on centrality
    node_colors = {}
    for node, centrality in deg_centrality.items():
        for color, (low, high) in categories.items():
            if low <= centrality < high:
                node_colors[node] = color
                break

    return node_colors



def plot_categorized_heatmap(friends, source_node):
    """
    Plot a graph with nodes colored by categorized degree centrality.
    """
    

    btw_centrality = betweenness_centrality(friends)
    node_colors = categorize_btw_centrality(btw_centrality)
    
    colors = [node_colors.get(node) for node in friends.nodes()]
    sizes = [100 if color in ['red', 'green', 'blue'] else 10 for color in colors]
    

    plt.figure(figsize=(12, 10))
    pos = nx.spring_layout(friends, pos={source_node: (0, 0)}, fixed=[source_node])
    nx.draw(
        friends,
        pos,
        with_labels = False,
        node_color=colors,
        node_size= sizes,
        font_size=10,
        font_weight='bold',
        edge_color='white'
    )
    red_nodes = [node for node, color in zip(friends.nodes(), colors) if color == 'red']
    labels = {node: node for node in red_nodes}  # Use node IDs as labels
    nx.draw_networkx_labels(friends, pos, labels, font_size=12, font_color='black', font_weight='bold')

    # Add legend
    legend_labels = {
        'red': 'above 0.005',   # Highest group
        'green': '0.001 - 0.005',
        'blue': '0.0001 - 0.001',
        'gray': 'below 0.0001'      # Lowest group
    }

    for color, label in legend_labels.items():
        plt.scatter([], [], c=color, label=label, s=100)  # Add dummy points for legend

    plt.legend(scatterpoints=1, frameon=True, labelspacing=1, title="Betweenness Centrality Ranges")
    plt.title("Categorized Heat Map of Nodes by Betweenness Centrality", fontsize=16)
    plt.show()




file_path = 'filtered_edges.csv'
friends = load_data(file_path) 
top_people = degree_centrality(friends)

subgraph = friends.subgraph(top_people)
print(betweenness_centrality(subgraph))