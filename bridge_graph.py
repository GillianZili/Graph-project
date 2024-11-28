import pandas as pd
import random
import networkx as nx
import matplotlib.pyplot as plt

def initialize_counts(total_rows):
    '''Portion for each value 0, 1, 2'''
    counts = {
        0: int(total_rows * 0.15),  
        1: int(total_rows * 0.20),
        2: int(total_rows * 0.15),
        3: int(total_rows * 0.10),
        4: int(total_rows * 0.25),
        5: int(total_rows * 0.15),
        6: int(total_rows * 0.05),
    }
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

add_random_col('selected_nodes.csv', 'Interests.csv')

def create_node_edge_graph(input_file):
    # Load the CSV file
    df = pd.read_csv(input_file)
    nodes = df['Node'].iloc
    edges = df['Random_Variable']
    
    #group nodes by their values
    groups = df.groupby('Random_Variable')['Node'].apply(list).to_dict()

    group_0 = groups.get(0, [])  # Nodes with value 0
    group_1 = groups.get(1, [])  # Nodes with value 1
    group_2 = groups.get(2, [])  # Nodes with value 2
    group_3 = groups.get(3, [])
    group_4 = groups.get(4, [])
    group_5 = groups.get(5, [])
    group_6 = groups.get(6, [])
    # Create a graph
    G = nx.Graph()

    # Add nodes to the graph
    G.add_nodes_from(nodes)

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


   
    return G


def visualize_graph(G):
   
    plt.figure(figsize=(12, 8))
   
    pos = nx.spring_layout(G) 
    nx.draw(G, pos, with_labels=False, node_size=20, node_color="lightblue", edge_color = 'lightgray', width = 0.1)
    plt.title("Node-Edge Graph")
    plt.axis('on')
    plt.show()

G = create_node_edge_graph('Interests.csv')
visualize_graph(G)






# for only 2 interests, align vertically
    # only 0-2 and 1-2 edges
    # G.add_edges_from((u, v) for u in group_0 for v in group_2)
    # G.add_edges_from((u, v) for u in group_1 for v in group_2)

    # pos = {}
    # height1, height2 = 0,0
    # for i, node in enumerate(group_0):
    #     pos[node] = (-10, -1 + i * 0.5)
    #     height1 +=  i * 0.5 

    # # Position nodes with value 1 on the far right, vertically aligned at y = 1
    # for j, node in enumerate(group_1):
    #     pos[node] = (10, 1 + j * 0.5)
    #     height2 +=  j * 0.5 

    # # Position nodes with value 2 in the center, strictly at y = 0
    # for k, node in enumerate(group_2):
    #     pos[node] = (0, 5 + k * 0.5)  