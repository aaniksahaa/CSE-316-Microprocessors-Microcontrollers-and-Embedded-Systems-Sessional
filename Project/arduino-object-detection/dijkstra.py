import math
import heapq

def euclidean_distance(p1, p2):
    # Calculate the Euclidean distance between two points
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

def dijkstra_shortest_path(graph, start, end):
    # Initialize distances with infinity for all nodes except the start node
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    parent = {node: None for node in graph}
    
    # Priority queue to store nodes with their tentative distances
    priority_queue = [(0, start)]
    
    while priority_queue:
        # Pop the node with the smallest tentative distance
        current_distance, current_node = heapq.heappop(priority_queue)
        
        # If reached the destination, return the shortest path
        if current_node == end:
            path = []
            while current_node is not None:
                path.insert(0, current_node)
                current_node = parent[current_node]
            return path
        
        # Check neighbors of the current node
        for neighbor in graph[current_node]:
            distance = current_distance + graph[current_node][neighbor]
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                parent[neighbor] = current_node
                heapq.heappush(priority_queue, (distance, neighbor))
    
    # If no path found, return an empty list
    return []

def shortest_path_sequence(points):
    # Create a graph where keys are integer indices and values are dictionaries of neighbors and distances
    n = len(points)
    graph = {i: {} for i in range(n)}
    for i in range(n):
        for j in range(n):
            if i != j:
                distance = euclidean_distance(points[i], points[j])
                graph[i][j] = distance
    
    # Find the shortest path using Dijkstra's algorithm
    shortest_path_indices = dijkstra_shortest_path(graph, 0, n - 1)
    
    # Convert indices to points
    shortest_path_points = [points[i] for i in shortest_path_indices]
    
    return shortest_path_points

# Example usage:
points = [[0, 0], [1, 1], [0, 2], [4, 0], [2, 4]]
shortest_path_points = shortest_path_sequence(points)
print("Shortest path sequence of points:", shortest_path_points)
