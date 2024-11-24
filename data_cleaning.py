from pandas import *

data_edge=read_csv('musae_git_edges.csv')
data_node=read_csv('musae_git_target.csv')

num_of_nodes=data_node['id'].to_list()
edge_from=data_edge['id_1'].to_list()
edge_to=data_edge['id_2'].to_list()

#create graph
graph = [[] for _ in range(len(num_of_nodes))]
for i in range(len(edge_from)):
    u = edge_from[i]
    v = edge_to[i]
    w = 1
    graph[u].append((v,w))











