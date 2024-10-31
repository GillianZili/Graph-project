# Dijkstra example
import heapq
from typing import List, Tuple

class Solution:
    def maxProbability(self, n: int, edges: List[List[int]], 
                       succProb: List[float], start_node: int, 
                       end_node: int) -> float:
        # Create an adjacency list
        graph = [[] for _ in range(n)]
        for i in range(len(edges)):
            from_node, to_node = edges[i]
            prob = succProb[i]
            graph[from_node].append((prob, to_node))
            graph[to_node].append((prob, from_node))

        # Visited array and distance array
        visited = [False] * n
        max_prob = [0.0] * n
        max_prob[start_node] = 1.0
        
        # Priority queue for Dijkstra's algorithm
        pq = [(-max_prob[start_node], start_node)]  # Use negative to simulate max-heap
        ans = 0.0
        
        while pq:
            prob, node = heapq.heappop(pq)
            prob = -prob  # Convert back to positive
            
            if visited[node]:
                continue
            
            visited[node] = True
            
            if node == end_node:
                ans = max(ans, prob)
            
            for next_prob, next_node in graph[node]:
                if max_prob[next_node] < prob * next_prob:
                    max_prob[next_node] = prob * next_prob
                    heapq.heappush(pq, (-max_prob[next_node], next_node))
        
        return ans

# Test case
if __name__ == "__main__":
    solution = Solution()
    n = 3
    edges = [[0, 1], [1, 2], [0, 2]]
    succProb = [0.5, 0.5, 0.2]
    start_node = 0
    end_node = 2
    
    result = solution.maxProbability(n, edges, succProb, start_node, end_node)
    print(f'Maximum Probability from {start_node} to {end_node}: {result}')