from __future__ import annotations

from enum import Enum
from typing import List, Dict, Optional, Union
import heapq
import math
import matplotlib.pyplot as plt
import networkx as nx

from algorithms.graph_lib.base_graph import BaseGraph, BaseNode
from algorithms.graph_lib.directed_graph import DirectedEdge, DirectedGraph


class HeuristicType(Enum):
    MANHATTAN = "manhattan"
    EUCLIDEAN = "euclidean"
    CHEBYSHEV = "chebyshev"
    ZERO = "zero"


class AStar:
    """
    A* (A-star) pathfinding algorithm for graph traversal and pathfinding.

    The algorithm efficiently generates a walkable path between multiple nodes,
    or points, on a graph. It uses a heuristic estimate to prioritize nodes
    and provides the shortest path from the start node to the goal node.
    A* can be used on both directed and undirected graphs.

    Attributes:
    -----------
    - graph (Graph): An instance of the Graph class that represents the problem to be solved.
    - heuristic_type (HeuristicType): The heuristic function type used to estimate the distance
    from a node to the goal.
    - predecessors (dict): Dictionary to map from a node id to its predecessor id for
    reconstructing the shortest path for the most recent search.
    """
    def __init__(self,
                 graph: BaseGraph,
                 heuristic_type: HeuristicType = HeuristicType.MANHATTAN) -> None:
        """
        Initialize the A* algorithm.

        Parameters:
        - graph: An instance of the Graph class.
        - heuristic_type: Type of heuristic to be used. Default is Manhattan distance.
        """
        self.graph = graph
        self.heuristic_type = heuristic_type
        self.start = None
        self.goal = None
        self.predecessors = {}

    def heuristic(self, start_node: BaseNode, goal_node: BaseNode) -> float:
        """
        Compute the heuristic cost for a given node based on the chosen heuristic type.

        Parameters:
        - node: An instance of the Node class.

        Returns:
        - A float value representing the heuristic cost.
        """
        dx = abs(start_node.x - goal_node.x)
        dy = abs(start_node.y - goal_node.y)

        if self.heuristic_type == HeuristicType.MANHATTAN:
            return dx + dy
        elif self.heuristic_type == HeuristicType.EUCLIDEAN:
            return math.sqrt(dx * dx + dy * dy)
        elif self.heuristic_type == HeuristicType.CHEBYSHEV:
            return max(dx, dy)
        elif self.heuristic_type == HeuristicType.ZERO:
            return 0
        else:
            raise ValueError(f"Unknown heuristic type: {self.heuristic_type}")

    def find_shortest_path(self,
                           start_id: Union[int, str],
                           goal_id: Union[int, str]) -> Optional[Union[List[int], List[str]]]:
        """
        Perform the A* search to find the shortest path from the start node to the goal node.

        Parameters:
        - start_id: ID of the starting node.
        - goal_id: ID of the target node.

        Returns:
        - A list of node IDs forming the path if a path exists, otherwise None.
        """
        self.start = self.graph.get_node(start_id)
        self.goal = self.graph.get_node(goal_id)
        open_list = [] # List of nodes to be explored.
        closed_list = set() # Set of nodes that have already been explored
        # g_costs: Dictionary that maps nodes to their g_cost, which is the actual distance
        # from the start node
        g_costs = {node_id: float('inf') for node_id in self.graph.nodes.keys()}
        g_costs[self.start.id] = 0.0
        # Reset predecessors for this search
        self.predecessors = {}

        heapq.heappush(open_list, (0.0, self.start.id)) # (f_cost, node_id)

        while open_list:
            _, current_node_id = heapq.heappop(open_list)

            if current_node_id == goal_id:
                return self.reconstruct_path(self.predecessors)

            closed_list.add(current_node_id)

            for neighbor_node in self.graph.get_neighbors(current_node_id):
                if neighbor_node.id in closed_list:
                    continue
                edge = self.graph.get_edge_between(current_node_id, neighbor_node.id)
                tentative_g_cost = g_costs[current_node_id] + edge.weight
                if tentative_g_cost < g_costs[neighbor_node.id]:
                    g_costs[neighbor_node.id] = tentative_g_cost
                    self.predecessors[neighbor_node.id] = current_node_id
                    f_cost = tentative_g_cost + self.heuristic(neighbor_node, self.goal)
                    heapq.heappush(open_list, (f_cost, neighbor_node.id))
        # There's no path available
        return None

    def reconstruct_path(self,
                         predecessors: Union[Dict[int, int], Dict[str, str]]) -> Optional[Union[List[int], List[str]]]:
        """
        Reconstruct the path from the goal to the start using the predecessors.

        Parameters:
        - predecessors: A dictionary mapping nodes to their predecessor.

        Returns:
        - A list of node IDs forming the path.
        """
        if not predecessors:
            print("Predecessors dict is empty! Please rerun the algorithm.")
            return None
        path = []
        current = self.goal.id
        while current in predecessors:
            path.append(current)
            current = predecessors[current]
        path.append(self.start.id)
        return path[::-1]

    def render(self, path: Optional[Union[List[int], List[str]]]):
        """
        Renders the graph using networkx and matplotlib, highlighting the best path found by A*.

        Parameters:
        - path: The path found by A*, as a list of node IDs.
        """
        # Convert the graph to a networkx graph
        G = nx.DiGraph() if isinstance(self.graph, DirectedGraph) else nx.Graph()

        for node in self.graph.nodes.values():
            G.add_node(node.id, pos=(node.x, node.y))

        for edge in self.graph.edges.values():
            # TODO: improve edge API
            if isinstance(edge, DirectedEdge):
                start_node = edge.source
                end_node = edge.target
            else:
                start_node = edge.node1
                end_node = edge.node2
            G.add_edge(start_node.id, end_node.id, weight=edge.weight)

        # Extract positions
        pos = nx.get_node_attributes(G, 'pos')

        # Draw the graph
        nx.draw(G, pos, with_labels=True, node_size=700, node_color='skyblue')

        # Highlight the path, if provided
        if path:
            path_edges = [(path[i], path[i + 1]) for i in range(len(path) - 1)]
            nx.draw_networkx_nodes(G, pos, nodelist=path, node_color='r')
            nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='r', width=2)

        plt.show()
