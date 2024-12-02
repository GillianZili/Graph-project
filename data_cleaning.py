import pandas as pd
import numpy as np
import networkx as nx
import random
import csv
'''
We filter out people with common interests, and extract their connections from the raw data.
'''

friend_all = pd.read_csv('edges.csv', skiprows=1, header=None)


def node_filter(friends):
    isolates = list(nx.isolates(friends))
    non_isolates = list(set(friends.nodes) - set(isolates))
    high_degree_nodes = [node for node in non_isolates if friends.degree[node] > 200]
    mid_degree_nodes = [node for node in non_isolates if 30 < friends.degree[node] <= 200]
    low_degree_nodes = [node for node in non_isolates if friends.degree[node] <= 30]
    high_degree_sample = random.sample(high_degree_nodes, min(len(high_degree_nodes), 200)) 
    mid_degree_sample = random.sample(mid_degree_nodes, min(len(mid_degree_nodes), 400))    
    low_degree_sample = random.sample(low_degree_nodes, min(len(low_degree_nodes), 400))    
    selected_nodes = set(high_degree_sample + mid_degree_sample + low_degree_sample)
    selected_nodes = set(map(int, selected_nodes))


    return selected_nodes



def save_selected_nodes_to_csv(selected_nodes, filename="selected_nodes.csv", limit = 200):
    '''Used for shared interests graph'''
    selected_nodes = list(selected_nodes)

    if limit is not None:
        selected_nodes = selected_nodes[:limit]

    with open(filename, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Node"]) 
        for node in selected_nodes:
            writer.writerow([node])
    print(f"Selected nodes saved to {filename}")
    return selected_nodes


def edge_filter(filter_set,name):
    filtered_edges = friend_all[friend_all.iloc[:, 0].isin(filter_set) & friend_all.iloc[:, 1].isin(filter_set)]
    file_path = f'filtered_edges_{name}.csv'
    filtered_edges.to_csv(file_path, index=False)
    return file_path

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

def degree_data(friends):

    deg_centrality = nx.degree_centrality(friends) 
    #type:dictionary, sort from big centrality to small centrality
    sorted_deg_centrality = sorted(deg_centrality.items(), key=lambda x: x[1], reverse=True)
    df_sorted_deg_centrality = pd.DataFrame(sorted_deg_centrality, columns=['Node', 'Degree Centrality'])

    # Export the DataFrame to a CSV file
    df_sorted_deg_centrality.to_csv('sorted_deg_centrality.csv', index=False)

def main():
    # filter the people by stratified sampling
    
    strat_sampling=node_filter(load_data('edges.csv'))
    edge_filter(strat_sampling,'startified_sampling')

    save_selected_nodes_to_csv(strat_sampling)
    
    target_nodes = save_selected_nodes_to_csv(strat_sampling)
    selected_nodes_edges = edge_filter(target_nodes,'selected_nodes_edges')
    print(selected_nodes_edges)


main()
