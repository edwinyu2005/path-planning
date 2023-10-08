import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
from typing import List, Tuple

from algorithms.graph_lib.base_graph import BaseNode

import os
import sys
sys.path.append(os.path.join(os.path.abspath(os.path.dirname(__file__)), "../../"))


class RRT:
    """
    Rapidly-Exploring Random Tree (RRT) class for path planning.
    """

    def __init__(self, start: BaseNode, goal: BaseNode,
                 x_lim: Tuple[float, float], y_lim: Tuple[float, float],
                 obstacles: List[Tuple[float, float, float]],
                 max_extend_length: float = 0.5,
                 max_iter: int = 500):
        """
        Initialize RRT.

        Args:
        - start (BaseNode): Starting node.
        - goal (BaseNode): Goal node.
        - x_lim (Tuple[float, float]): X-axis limits.
        - y_lim (Tuple[float, float]): Y-axis limits.
        - obstacles (List[Tuple[float, float, float]]): List of obstacles, with each defined as (x, y, radius).
        - max_extend_length (float): Maximum distance to expand tree in each iteration.
        - max_iter (int): Maximum number of iterations for the algorithm.
        """
        self.start = start
        self.goal = goal
        self.x_lim = x_lim
        self.y_lim = y_lim
        self.max_extend_length = max_extend_length
        self.max_iter = max_iter
        self.obstacles = obstacles
        self.graph = nx.DiGraph()
        self.node_counter = 0  # To give each node a unique id

    def _distance(self, node1: BaseNode, node2: BaseNode) -> float:
        """Compute Euclidean distance between two nodes."""
        return np.sqrt((node1.x - node2.x)**2 + (node1.y - node2.y)**2)

    def _get_random_node(self) -> BaseNode:
        """Generate and return a random node within the defined bounds."""
        x = np.random.uniform(self.x_lim[0], self.x_lim[1])
        y = np.random.uniform(self.y_lim[0], self.y_lim[1])
        self.node_counter += 1
        return BaseNode(id=self.node_counter, x=x, y=y)

    def _nearest_node(self, node: BaseNode, nodes: List[BaseNode]) -> BaseNode:
        """Find and return the closest node from the list to the given node."""
        return min(nodes, key=lambda n: self._distance(node, n))

    def _steer(self, node_from: BaseNode, node_to: BaseNode) -> BaseNode:
        """
        Steer from node_from towards node_to, but only up to a maximum distance of max_extend_length.
        Return the new node.
        """
        if self._distance(node_from, node_to) < self.max_extend_length:
            return node_to

        theta = np.arctan2(node_to.y - node_from.y, node_to.x - node_from.x)
        x = node_from.x + self.max_extend_length * np.cos(theta)
        y = node_from.y + self.max_extend_length * np.sin(theta)
        self.node_counter += 1  # Increment the counter for the new node
        return BaseNode(id=self.node_counter, x=x, y=y)

    def _check_collision(self, node_from: BaseNode, node_to: BaseNode) -> bool:
        """
        TODO: this collision check is wrong need to fix it

        Check if the path between node_from and node_to collides with any obstacle.
        Return True if collision, else False.
        """
        for (ox, oy, size) in self.obstacles:
            obs_node = BaseNode(id="temp", x=ox, y=oy)
            d1 = self._distance(obs_node, node_from)
            d2 = self._distance(obs_node, node_to)
            if d1 <= size or d2 <= size:
                return True
        return False

    def plan(self) -> nx.DiGraph:
        """
        Generate RRT by iteratively expanding tree towards random points, while avoiding obstacles.
        Return the resulting graph.
        """
        self.graph.add_node(self.start)
        for _ in range(self.max_iter):
            rand_node = self._get_random_node()
            nearest_node = self._nearest_node(rand_node, list(self.graph.nodes))
            new_node = self._steer(nearest_node, rand_node)

            if not self._check_collision(nearest_node, new_node):
                self.graph.add_edge(nearest_node, new_node)

                if self._distance(new_node, self.goal) <= self.max_extend_length:
                    self.graph.add_edge(new_node, self.goal)
                    return self.graph

        return self.graph

    def draw(self):
        """Visualize the generated RRT and obstacles."""
        fig, ax = plt.subplots()

        # Plot the edges (connections) of the RRT
        for edge in self.graph.edges:
            start_node, end_node = edge
            plt.plot([start_node.x, end_node.x], [start_node.y, end_node.y], color='black')

        # Plot all nodes with a single color
        for node in self.graph.nodes:
            plt.scatter(node.x, node.y, color="gray", s=50)
            ax.text(node.x, node.y, str(node.id), fontsize=8, ha='right')

        # Plot the obstacles
        for (ox, oy, size) in self.obstacles:
            ax.add_patch(plt.Circle((ox, oy), size, color='r'))

        # Highlight the start and goal nodes
        plt.scatter(self.start.x, self.start.y, color="blue", s=100, label="Start")
        plt.scatter(self.goal.x, self.goal.y, color="red", s=100, label="Goal")

        plt.grid()
        plt.legend()
        plt.show()


if __name__ == "__main__":
    start_node = BaseNode(id="start", x=0, y=0)
    goal_node = BaseNode(id="goal", x=7, y=7)
    x_lim = (0, 10)
    y_lim = (0, 10)
    obstacles = [(5, 5, 1), (3, 6, 0.5), (7, 2, 1)]
    rrt = RRT(start_node, goal_node, x_lim, y_lim, obstacles)
    rrt.plan()
    rrt.draw()
