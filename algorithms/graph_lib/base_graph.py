from __future__ import annotations
from typing import List, Optional, Union


class BaseNode:
    """
    A base class for nodes in a graph.

    Attributes:
    - id (Union[int, str]): A unique identifier for the node.
    """
    def __init__(self, id: Union[int, str], x: Optional[float] = None, y: Optional[float] = None):
        self.id = id
        self.x = x
        self.y = y

    def __str__(self) -> str:
        return str(self.id)

    def __eq__(self, other: BaseNode) -> bool:
        """
        Check if two nodes are the same based on their IDs.

        :param other: Another node object.
        :return: True if the nodes have the same ID, False otherwise.
        """
        if isinstance(other, BaseNode):
            return self.id == other.id
        return False

    def __hash__(self):
        return hash(self.id)


class BaseEdge:
    """
    A base class for edges in a graph.

    Attributes:
    - id (Union[int, str]): A unique identifier for the edge.
    - weight (float): Weight/cost associated with traversing the edge.
    """
    def __init__(self, id: Union[int, str], weight: float = 1.0) -> None:
        self.id = id
        self.weight = weight

    def __str__(self) -> str:
        return "Edge(ID: {}, Weight: {})".format(self.id, self.weight)

    def has_nodes(self, node1: BaseNode, node2: BaseNode) -> bool:
        """
        Check if the edge connects the specified nodes.
        """
        raise NotImplementedError


class BaseGraph:
    """
    Base class for representing a graph.

    Attributes:
    - nodes (Dict[Union[int, str], BaseNode]): A dictionary mapping node IDs to node instances.
    - edges (Dict[Union[int, str], BaseEdge]): A dictionary mapping edge IDs to edge instances.
    """
    def __init__(self) -> None:
        self.nodes = {}
        self.edges = {}

    def add_node(self, node: BaseNode) -> None:
        if node.id in self.nodes:
            raise ValueError("A node with ID {} already exists.".format(node.id))
        self.nodes[node.id] = node

    def remove_node(self, node_id: Union[int, str]) -> None:
        if node_id in self.nodes:
            # TODO: implement
            pass

    def add_edge(self, edge: BaseEdge) -> None:
        """Add an edge to the graph."""
        if edge.id in self.edges:
            raise ValueError("An edge with ID {} already exists.".format(edge.id))
        self.edges[edge.id] = edge

    def remove_edge(self, edge_id: Union[int, str]) -> None:
        if edge_id in self.edges:
            # TODO: implement
            pass

    def get_node(self, node_id: Union[int, str]) -> Optional[BaseNode]:
        return self.nodes.get(node_id)

    def get_edge(self, edge_id: Union[int, str]) -> Optional[BaseEdge]:
        return self.edges.get(edge_id)

    def get_neighbors(self, node_id: Union[int, str]) -> List[BaseNode]:
        """Abstract method to be implemented by subclasses to get neighbors of a node."""
        raise NotImplementedError

    def get_edge_between(self,
                         node1: Union[int, str, BaseNode],
                         node2: Union[int, str, BaseNode]) -> Optional[BaseEdge]:
        raise NotImplementedError
