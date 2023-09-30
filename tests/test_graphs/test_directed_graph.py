import pytest

from algorithms.graph_lib.directed_graph import DirectedEdge, DirectedGraph, DirectedNode


class TestDirectedGraph:
    @pytest.fixture
    def directed_graph(self):
        graph = DirectedGraph()
        return graph

    def test_node_eq(self):
        node_a = DirectedNode(1)
        node_b = DirectedNode(2)
        node_c = DirectedNode(1)

        assert node_a == node_c
        assert node_a != node_b

    def test_creation(self, directed_graph):
        assert isinstance(directed_graph, DirectedGraph)
        assert len(directed_graph.nodes) == 0
        assert len(directed_graph.edges) == 0

    def test_add_node(self, directed_graph):
        directed_graph.add_node(DirectedNode("A"))
        assert len(directed_graph.nodes) == 1

    def test_add_edge(self, directed_graph):
        node_a = DirectedNode("A")
        node_b = DirectedNode("B")
        edge_ab = DirectedEdge("edge_ab", node_a, node_b)

        directed_graph.add_node(node_a)
        directed_graph.add_node(node_b)
        directed_graph.add_edge(edge_ab)

        assert len(directed_graph.edges) == 1
        assert len(node_a.outgoing_edges) == 1
        assert len(node_b.incoming_edges) == 1

    def test_get_neighbors(self, directed_graph):
        node_a = DirectedNode("A")
        node_b = DirectedNode("B")
        node_c = DirectedNode("C")
        edge_ab = DirectedEdge("edge_ab", node_a, node_b)
        edge_ac = DirectedEdge("edge_ac", node_a, node_c)
        edge_bc = DirectedEdge("edge_bc", node_b, node_c)

        directed_graph.add_node(node_a)
        directed_graph.add_node(node_b)
        directed_graph.add_node(node_c)
        directed_graph.add_edge(edge_ab)
        directed_graph.add_edge(edge_ac)
        directed_graph.add_edge(edge_bc)

        neighbors_a = directed_graph.get_neighbors("A")
        neighbors_b = directed_graph.get_neighbors("B")
        neighbors_c = directed_graph.get_neighbors("C")

        assert set(node_a.outgoing_edges) == {edge_ab, edge_ac}
        assert set(neighbors_a) == {node_b, node_c}
        assert set(neighbors_b) == {node_c}
        assert len(neighbors_c) == 0

    def test_has_nodes(self):
        node_a = DirectedNode(1)
        node_b = DirectedNode(2)
        node_c = DirectedNode(3)

        edge_ab = DirectedEdge("edge_ab", node_a, node_b)
        edge_bc = DirectedEdge("edge_bc", node_b, node_c)

        assert edge_ab.has_nodes(node_a, node_b)
        assert edge_bc.has_nodes(node_b, node_c)
        assert not edge_ab.has_nodes(node_b, node_a) # Order matters
        assert not edge_ab.has_nodes(node_a, node_c)
        assert not edge_bc.has_nodes(node_a, node_b)

    def test_get_edge_between(self, directed_graph):
        node_a = DirectedNode(1)
        node_b = DirectedNode(2)
        node_c = DirectedNode(3)

        directed_graph.add_node(node_a)
        directed_graph.add_node(node_b)
        directed_graph.add_node(node_c)
        directed_graph.add_edge(DirectedEdge("edge_ab", node_a, node_b))
        directed_graph.add_edge(DirectedEdge("edge_bc", node_b, node_c))

        edge_ab = directed_graph.get_edge_between(node_a, node_b)
        edge_bc = directed_graph.get_edge_between(2, 3)
        edge_ac = directed_graph.get_edge_between(node_a, node_c)

        assert isinstance(edge_ab, DirectedEdge)
        assert edge_ab.source == node_a and edge_ab.target == node_b
        assert isinstance(edge_bc, DirectedEdge)
        assert edge_bc.source == node_b and edge_bc.target == node_c
        assert edge_ac is None
