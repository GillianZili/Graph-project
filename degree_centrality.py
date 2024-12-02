import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt
from data_cleaning import load_data


def degree_centrality(friends):
    deg_centrality = nx.degree_centrality(friends)
    print("Graph created with", friends.number_of_nodes(), "nodes and", friends.number_of_edges(), "edges.")
    sorted_deg_centrality = sorted(deg_centrality.items(), key=lambda x: x[1], reverse=True)  
   
    # convert to a dp frame and create a csv file 
    top_degree_centrality = pd.DataFrame(sorted_deg_centrality, columns=['Name', 'Degree Centrality'])
    top_degree_centrality.to_csv('top_degree_centrality.csv', index=False)
    print('create a degree csv file successfully')

    return dict(sorted_deg_centrality)

    
def categorize_degree_centrality(deg_centrality):
   
    categories = {
        'red': (0.15, 1),      
        'green': (0.08, 0.15),
        'blue': (0.05, 0.08),
        'gray': (0, 0.005)
    }
    
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
        50 if color == 'green' else
        30 if color == 'blue' else
        5  
        for color in colors
    ]

    fig, ax = plt.subplots(figsize=(12, 8))
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
        'red': '0.15 - 1',      
        'green': '0.08 - 0.15',
        'blue': '0.05 - 0.08',
        'gray': '0 - 0.05'   
    }

    for color, label in legend_labels.items():
        ax.scatter([], [], c=color, label=label)

    ax.set_title(" Heat Map of degree centrality", fontsize=16)
    ax.legend(scatterpoints=1, frameon=True, labelspacing=1, title="Degree Centrality Ranges")
    plt.show()




file_path = 'filtered_edges_startified_sampling.csv'
friends = load_data(file_path)  
degree_data = degree_centrality(friends)
node_colors = categorize_degree_centrality(degree_data) 
plot_categorized_heatmap(friends, node_colors)


