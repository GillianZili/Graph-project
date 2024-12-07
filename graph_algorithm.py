import heapq
from data_cleaning_adj_list import whole_graph,strif_spl_graph

def dijkstra(graph, source):
    n = len(graph)
    dist = [float('inf')] * n
    dist[source] = 0
    pq = [(0, source)] 
    
    while pq:
        current_dist, u = heapq.heappop(pq)
        if current_dist > dist[u]:
            continue
        for v, weight in graph[u]:
            distance = current_dist + weight
            if distance < dist[v]:
                dist[v] = distance
                heapq.heappush(pq, (distance, v))
    
    return dist


def floyd_warshall(graph):
    nodes = list(graph.keys())
    n = len(nodes)  
    dist = {node: {other_node: float('inf') for other_node in nodes} for node in nodes}
    pred = {node: {other_node: None for other_node in nodes} for node in nodes}
    pass_through = {node: 0 for node in nodes}
    
    for u in nodes:
        dist[u][u] = 0  
        for v, weight in graph[u]:
            dist[u][v] = weight 
            pred[u][v] = u  
    
    for k in nodes:
        for i in nodes:
            for j in nodes:
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
                    pred[i][j] = pred[k][j]
                    pass_through[k] += 1 
    
    max_1, max_2 = sorted(pass_through, key=lambda x: pass_through[x], reverse=True)[:2]
    return max_1, max_2


def average_shortest_path_from_source(graph, source,func):
    distances = func(graph, source) 
    valid_distances = [d for d in distances if d < float('inf')]
    if valid_distances:  
        return sum(valid_distances) / len(valid_distances)
    return None  


def main():
    #test dijkstra
    d1=average_shortest_path_from_source(whole_graph,16726,dijkstra)
    d2=average_shortest_path_from_source(whole_graph,27803,dijkstra)
    d3=average_shortest_path_from_source(whole_graph,141,dijkstra)
    print (f"average_shortest_path:{round((d1+d2+d3)/3,2)}")

    #test floyd_warshall
    max_1, max_2 = floyd_warshall(strif_spl_graph)
    print(f"The two most frequently passed nodes are: {max_1} and {max_2}")

main()

 
 