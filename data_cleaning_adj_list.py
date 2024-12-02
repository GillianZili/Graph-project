from pandas import *
import matplotlib.pyplot as plt
import bisect

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

#create bar chart of numbers of followers
nums_of_followers=[]
for i in range(len(graph)):
    nums_of_followers.append(len(graph[i]))
nums_of_followers.sort()

# use binary search to fasten the calculation
bar_categories=[0,20,30,40,60,80,100,500,1000]
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












