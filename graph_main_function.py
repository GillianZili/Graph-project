import heapq
from data_cleaning import graph


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

def average_shortest_path_from_source(graph, source):
    distances = dijkstra(graph, source) 
    valid_distances = [d for d in distances if d < float('inf')]
    if valid_distances:  
        return sum(valid_distances) / len(valid_distances)
    return None  

def main():
    print(average_shortest_path_from_source(graph,0))

main()

 