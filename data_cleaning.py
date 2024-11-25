import pandas as pd
import numpy as np
import networkx as nx

'''
We filter out people with common interests, and extract their connections from the raw data.
'''
file1 = 'shared_interest.csv'
file2 = 'edges.csv'

df1 = pd.read_csv(file1, skiprows=1, header=None)
df2 = pd.read_csv(file2, skiprows=1, header=None)


ids_with_1 = set(df1[df1.iloc[:, 1] == 1].iloc[:, 0])


filtered_edges = df2[df2.iloc[:, 0].isin(ids_with_1) & df2.iloc[:, 1].isin(ids_with_1)]

filtered_edges.to_csv('filtered_edges.csv', index=False)


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
    sorted_deg_centrality = sorted(deg_centrality.items(), key=lambda x: x[1], reverse=True)
    df_sorted_deg_centrality = pd.DataFrame(sorted_deg_centrality, columns=['Node', 'Degree Centrality'])

    # Export the DataFrame to a CSV file
    df_sorted_deg_centrality.to_csv('sorted_deg_centrality.csv', index=False)


file_path = 'filtered_edges.csv'
friends = load_data(file_path)  
degree_data(friends)