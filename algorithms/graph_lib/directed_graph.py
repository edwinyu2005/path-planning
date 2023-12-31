from __future__ import annotations
from typing import List, Optional, Union

from algorithms.graph_lib.base_graph import BaseEdge, BaseGraph, BaseNode


class DirectedNode(BaseNode):
    """
    A node in a directed graph.

    Attributes:
    - id (Union[int, str]): A unique identifier for the node.
    - outgoing_edges (List[DirectedEdge]): A list of outgoing edges from the node.
    - incoming_edges (List[DirectedEdge]): A list of incoming edges to the node.
    """
    def __init__(self, id: Union[int, str], x: Optional[float] = None, y: Optional[float] = None):
        super().__init__(id, x, y)
        self.outgoing_edges = []
        self.incoming_edges = []

    def add_outgoing_edge(self, edge: DirectedEdge) -> None:
        """
        Add an outgoing directed edge to the node.
        """
        if not isinstance(edge, DirectedEdge):
            raise ValueError(
                "Only DirectedEdge instances can be added as outgoing edges to a DirectedNode")
        if edge not in self.outgoing_edges:
            self.outgoing_edges.append(edge)

    def add_incoming_edge(self, edge: DirectedEdge) -> None:
        """
        Add an incoming directed edge to the node.
        """
        if not isinstance(edge, DirectedEdge):
            raise ValueError(
                "Only DirectedEdge instances can be added as incoming edges to a DirectedNode")
        if edge not in self.incoming_edges:
            self.incoming_edges.append(edge)

    def get_successors(self) -> List[BaseNode]:
        """
        Retrieve the neighboring nodes this node points to (i.e., successors).
        """
        return [edge.target for edge in self.outgoing_edges]

    def get_predecessors(self) -> List[BaseNode]:
        """
        Retrieve the nodes that point to this node (i.e., predecessors).
        """
        return [edge.source for edge in self.incoming_edges]


class DirectedEdge(BaseEdge):
    """
    An edge in a directed graph.

    Attributes:
    - source (DirectedNode): The source/start node of the directed edge.
    - target (DirectedNode): The target/end node of the directed edge.
    - weight (float): Weight/cost associated with traversing the edge.
    """

    def __init__(self, id: Union[int, str], source: DirectedNode, target: DirectedNode, weight: float = 1.0):
        super().__init__(id, weight)
        self.source = source
        self.target = target

        source.add_outgoing_edge(self)
        target.add_incoming_edge(self)

    def __str__(self) -> str:
        return "Directed Edge(ID: {}, Nodes: {}->{}, Weight: {})".format(
            self.id, self.source.id, self.target.id, self.weight)

    def is_source(self, node: BaseNode) -> bool:
        return node == self.source

    def is_target(self, node: BaseNode) -> bool:
        return node == self.target

    def get_other_node(self, current_node: BaseNode) -> BaseNode:
        """
        Given one of the nodes connected by this edge, return the other node.

        Note: Due to the directed nature, if the provided node is the source,
        this will return the target and vice versa.
        """
        if current_node == self.source:
            return self.target
        elif current_node == self.target:
            return self.source
        else:
            raise ValueError("Given node is not connected by this edge.")

    def has_nodes(self, node1: BaseNode, node2: BaseNode) -> bool:
        """
        Check if the edge connects the specified nodes.

        :param node1: Source node.
        :param node2: Target node.
        :return: True if the edge connects the nodes, False otherwise.
        """
        return self.source == node1 and self.target == node2


class DirectedGraph(BaseGraph):
    """
    Represents a directed graph.

    The graph contains a collection of nodes (represented by unique IDs)
    and directed edges. Each edge has a source node and a target node.
    """
    def __init__(self) -> None:
        super().__init__()

    def __str__(self) -> str:
        return "DirectedGraph with {} nodes and {} edges.".format(len(self.nodes), len(self.edges))

    def get_neighbors(self, node_id: Union[int, str]) -> List[DirectedNode]:
        """
        Get successor neighbors of a node in a directed graph.
        """
        node = self.get_node(node_id)
        if not node:
            raise ValueError("No node with ID {} exists in the graph.".format(node_id))
        if not isinstance(node, DirectedNode):
            raise ValueError("The provided node ID does not correspond to a DirectedNode instance.")

        return node.get_successors()

    def get_edge_between(self,
                         node1: Union[int, str, BaseNode],
                         node2: Union[int, str, BaseNode]) -> Optional[BaseEdge]:
        """
        Get the edge between two nodes by their IDs.

        :param node1: source node or ID of the source node.
        :param node2: target node or ID of the target node.
        :return: The edge between the two nodes or None if no edge exists.
        """
        source_node = node1 if isinstance(node1, BaseNode) else self.get_node(node1)
        target_node = node2 if isinstance(node2, BaseNode) else self.get_node(node2)

        if source_node and target_node:
            for edge in self.edges.values():
                if edge.source == source_node and edge.target == target_node:
                    return edge

        return None
