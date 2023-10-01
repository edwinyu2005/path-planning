import heapq
from typing import Dict, Optional, Tuple, Union

from algorithms.graph_lib.base_graph import BaseGraph


class Dijkstra:
    def __init__(self, graph: BaseGraph) -> None:
        self.graph = graph

    def find_shortest_paths(
        self,
        source_node_id: Union[int, str]
    ) -> Dict[Union[int, str], Tuple[float, Optional[Union[int, str]]]]:
        """
        Find the shortest paths from a source node to all other nodes using Dijkstra's algorithm.

        :param source_node_id: The ID of the source node.
        :return: A dictionary where keys are node IDs, and values are tuples (distance, predecessor).
                 Distance is the shortest distance from the source node to the respective node.
                 Predecessor is the previous node in the shortest path.
        """
        distances = {node_id: float('inf') for node_id in self.graph.nodes.keys()}
        predecessors = {node_id: None for node_id in self.graph.nodes.keys()}
        distances[source_node_id] = 0.0
        priority_queue = [(0, source_node_id)]
        unvisited_nodes = set(self.graph.nodes.keys())

        while unvisited_nodes:
            # Extract node with minimum distance
            _, current_node_id = heapq.heappop(priority_queue)
            if current_node_id not in unvisited_nodes:
                # current_node has been visited
                continue

            # Remove the current node from unvisited_nodes
            unvisited_nodes.remove(current_node_id)

            for neighbor_node in self.graph.get_neighbors(current_node_id):
                edge = self.graph.get_edge_between(current_node_id, neighbor_node)
                potential_distance = distances[current_node_id] + edge.weight
                if potential_distance < distances[neighbor_node.id]:
                    distances[neighbor_node.id] = potential_distance
                    predecessors[neighbor_node.id] = current_node_id
                    heapq.heappush(priority_queue, (potential_distance, neighbor_node.id))

        shortest_paths = {
            node_id: (distances[node_id], predecessors[node_id]) for node_id in distances
        }

        return shortest_paths
