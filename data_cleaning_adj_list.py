from pandas import *
import matplotlib.pyplot as plt
import bisect

all_edge=read_csv('musae_git_edges.csv')
all_edge_from=all_edge['id_1'].to_list()
all_edge_to=all_edge['id_2'].to_list()

sampling_edge=read_csv('filtered_edges_startified_sampling.csv')
spl_edge_from=sampling_edge['0'].to_list()
spl_edge_to=sampling_edge['1'].to_list()

def createGraph(edge_from,edge_to):
    graph = {}
    for i in range(len(edge_from)):
        u = edge_from[i]
        v = edge_to[i]
        w = 1
        if u not in graph:
            graph[u] = []
        if v not in graph:
            graph[v] = []
        graph[u].append((v, w))
    
    return graph

def plot_barchart(graph):
    nums_of_followers=[]
    for i in range(len(graph)):
        nums_of_followers.append(len(graph[i]))
    nums_of_followers.sort()

    # use binary search to fasten the calculation
    bar_categories=[0,20,30,40,60,80,100,200,500,1000]
    bar_value=[0]*len(bar_categories)
    for num in nums_of_followers:
        idx = bisect.bisect_left(bar_categories, num)  
        if idx == len(bar_categories): 
            bar_value[-1] += 1
        else:
            bar_value[idx] += 1

    #plot bar chart
    bar_labels = [
        f"{bar_categories[i]}-{bar_categories[i+1]-1}" if i < len(bar_categories)-1 else f"{bar_categories[i]}+"
        for i in range(len(bar_categories))
    ]
    plt.bar(range(len(bar_categories)), bar_value, color='skyblue', align='center')  
    plt.title('Follower Distribution')
    plt.xlabel('Follower Categories')
    plt.ylabel('Counts')
    plt.ylim(0, 10000)
    plt.xticks(range(len(bar_categories)), bar_labels, rotation=45)  
    plt.tight_layout() 
    plt.show()

whole_graph=createGraph(all_edge_from,all_edge_to)
plot_barchart(whole_graph)
strif_spl_graph=createGraph(spl_edge_from,spl_edge_to)












