import networkx as nx
import matplotlib.pyplot as plt
import heapq
from typing import Dict, Optional, Tuple, Union

from algorithms.graph_lib.base_graph import BaseGraph
from algorithms.graph_lib.directed_graph import DirectedGraph


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
                # TODO: Refactor get_edge_between to achieve a time complexity of O(1)
                edge = self.graph.get_edge_between(current_node_id, neighbor_node)
                potential_distance = distances[current_node_id] + edge.weight
                if potential_distance < distances[neighbor_node.id]:
                    distances[neighbor_node.id] = potential_distance
                    predecessors[neighbor_node.id] = current_node_id
                    # TODO: Develop a custom priority_queue that allows for updating the priority of its existing items.
                    heapq.heappush(priority_queue, (potential_distance, neighbor_node.id))

        shortest_paths = {
            node_id: (distances[node_id], predecessors[node_id]) for node_id in distances
        }

        return shortest_paths

    def render(self, source_node_id: Union[int, str], target_node_id: Union[int, str]) -> None:
        """
        Visualize the graph and the shortest path computed by Dijkstra's algorithm.

        Parameters:
        - source_node_id: Union[int, str]
            The ID of the source node from which the shortest paths are computed.
        - target_node_id: Union[int, str]
            The ID of the target node to which the shortest path will be highlighted and displayed.

        Note:
        This method uses `networkx` and `matplotlib` to create a visual representation of
        the graph. The nodes and edges are drawn using `networkx` and `matplotlib`, and the
        computed shortest path from source_node_id to target_node_id is highlighted in red.
        """
        if isinstance(self.graph, DirectedGraph):
            G = nx.DiGraph()
        else:
            G = nx.Graph()

        # Convert graph to a networkx graph
        for node_id in self.graph.nodes.keys():
            G.add_node(node_id)
            for neighbor in self.graph.get_neighbors(node_id):
                edge = self.graph.get_edge_between(node_id, neighbor.id)
                G.add_edge(node_id, neighbor.id, weight=edge.weight)

        # Run the algorithm
        shortest_paths = self.find_shortest_paths(source_node_id)
        tree_edges = [
            (predecessor, node_id)
            for node_id, (_, predecessor) in shortest_paths.items()
            if predecessor is not None
        ]

        # Visualize
        pos = nx.spring_layout(G)
        nx.draw(G, pos, with_labels=True, node_size=700, node_color='skyblue', font_weight='bold', arrowsize=20)
        labels = nx.get_edge_attributes(G, 'weight')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
        nx.draw_networkx_edges(G, pos, edgelist=tree_edges, edge_color='r', width=2, arrowsize=20)

        # Display
        plt.title('Shortest Path from {source_node_id} to {shortest_path[-1]}: {" -> ".join(shortest_path)}')
        plt.show()
