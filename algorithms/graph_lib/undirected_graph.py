from __future__ import annotations
from typing import List, Optional, Union

from algorithms.graph_lib.base_graph import BaseEdge, BaseGraph, BaseNode


class UndirectedNode(BaseNode):
    """
    A node in an undirected graph.

    Attributes:
    - id (Union[int, str]): A unique identifier for the node.
    - edges (List[UndirectedEdge]): A list of edges associated with the node.
    """
    def __init__(self, id: Union[int, str], x: Optional[float] = None, y: Optional[float] = None):
        super().__init__(id, x, y)
        self.edges = []

    def add_edge(self, edge: UndirectedEdge) -> None:
        """
        Add an undirected edge to the node.

        Args:
        - edge (UndirectedEdge): The undirected edge to add.

        Raises:
        - ValueError: If edge is not an instance of UndirectedEdge.
        """
        if not isinstance(edge, UndirectedEdge):
            raise ValueError("Only UndirectedEdge instances can be added to an UndirectedNode")
        if edge not in self.edges:
            self.edges.append(edge)

    def get_neighbors(self) -> List[BaseNode]:
        """
        Retrieve the neighboring nodes.
        """
        return [edge.get_other_node(self) for edge in self.edges]


class UndirectedEdge(BaseEdge):
    """
    Represents an undirected edge between two nodes in a graph.

    An undirected edge does not have a source or target; instead, it connects
    two nodes without implying a direction.

    Attributes:
        node1 (BaseNode): The first node connected by the edge.
        node2 (BaseNode): The second node connected by the edge.
    """
    def __init__(self, id: Union[int, str],
                 node1: UndirectedNode, node2: UndirectedNode,
                 weight: float = 1.0) -> None:
        super().__init__(id, weight)
        self.node1 = node1
        self.node2 = node2

        node1.add_edge(self)
        node2.add_edge(self)

    def __str__(self) -> str:
        return "UndirectedEdge(ID: {}, Nodes: {}-{}, Weight: {})".format(
            self.id, self.node1.id, self.node2.id, self.weight)

    def get_other_node(self, current_node: BaseNode) -> BaseNode:
        """
        Retrieve the other node connected by the edge.

        Args:
        - current_node (UndirectedNode): One of the nodes connected by the edge.

        Returns:
        - UndirectedNode: The other node connected by the edge.
        """
        if current_node == self.node1:
            return self.node2
        elif current_node == self.node2:
            return self.node1
        else:
            raise ValueError("Given node is not connected by this edge.")

    def has_nodes(self, node1: BaseNode, node2: BaseNode) -> bool:
        """
        Check if the edge connects the specified nodes.

        :param node1: First node.
        :param node2: Second node.
        :return: True if the edge connects the nodes, False otherwise.
        """
        return (self.node1 == node1 and self.node2 == node2) or (self.node1 == node2 and self.node2 == node1)


class UndirectedGraph(BaseGraph):
    """
    Represents an undirected graph.

    The graph contains a collection of nodes (represented by unique IDs)
    and undirected edges. Each edge connects two nodes bidirectionally.
    """
    def __init__(self) -> None:
        super().__init__()

    def __str__(self) -> str:
        return "UndirectedGraph with {} nodes and {} edges.".format(len(self.nodes), len(self.edges))

    def get_neighbors(self, node_id: Union[int, str]) -> List[UndirectedNode]:
        """
        Get neighbors of a node in an undirected graph.
        Neighbors here are nodes that share an edge with the given node.
        """
        node = self.get_node(node_id)
        if not node:
            raise ValueError("No node with ID {} exists in the graph.".format(node_id))
        if not isinstance(node, UndirectedNode):
            raise ValueError("The provided node ID does not correspond to an UndirectedNode instance.")

        # Extracting the nodes connected by edges
        neighbors = [edge.node1 if edge.node2 == node else edge.node2 for edge in node.edges]

        return neighbors

    def get_edge_between(self,
                         node1: Union[int, str, BaseNode],
                         node2: Union[int, str, BaseNode]) -> Optional[BaseEdge]:
        """
        Get the edge between two nodes by their IDs.

        :param node1: first node or ID of the first node.
        :param node2: second node or ID of the second node.
        :return: The edge between the two nodes or None if no edge exists.
        """
        node_1 = node1 if isinstance(node1, BaseNode) else self.get_node(node1)
        node_2 = node2 if isinstance(node2, BaseNode) else self.get_node(node2)

        if node_1 and node_2:
            for edge in self.edges.values():
                if edge.has_nodes(node_1, node_2):
                    return edge

        return None
