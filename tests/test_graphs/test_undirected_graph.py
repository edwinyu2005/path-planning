import pytest

from algorithms.graph_lib.undirected_graph import UndirectedEdge, UndirectedGraph, UndirectedNode

class TestUndirectedGraph:
    @pytest.fixture
    def undirected_graph(self):
        graph = UndirectedGraph()
        return graph

    def test_creation(self, undirected_graph):
        assert isinstance(undirected_graph, UndirectedGraph)
        assert len(undirected_graph.nodes) == 0
        assert len(undirected_graph.edges) == 0

    def test_add_node(self, undirected_graph):
        undirected_graph.add_node(UndirectedNode("A"))
        assert len(undirected_graph.nodes) == 1

    def test_add_edge(self, undirected_graph):
        node_a = UndirectedNode("A")
        node_b = UndirectedNode("B")
        edge_ab = UndirectedEdge("edge_ab", node_a, node_b)
        
        undirected_graph.add_node(node_a)
        undirected_graph.add_node(node_b)
        undirected_graph.add_edge(edge_ab)
        
        assert len(undirected_graph.edges) == 1
        assert len(node_a.edges) == 1
        assert len(node_b.edges) == 1

    def test_get_neighbors(self, undirected_graph):
        node_a = UndirectedNode("A")
        node_b = UndirectedNode("B")
        node_c = UndirectedNode("C")
        edge_ab = UndirectedEdge("edge_ab", node_a, node_b)
        edge_ac = UndirectedEdge("edge_ac", node_a, node_c)

        undirected_graph.add_node(node_a)
        undirected_graph.add_node(node_b)
        undirected_graph.add_node(node_c)
        undirected_graph.add_edge(edge_ab)
        undirected_graph.add_edge(edge_ac)

        neighbors_a = undirected_graph.get_neighbors("A")
        neighbors_b = undirected_graph.get_neighbors("B")
        neighbors_c = undirected_graph.get_neighbors("C")

        assert set(neighbors_a) == {node_b, node_c}
        assert set(neighbors_b) == {node_a}
        assert set(neighbors_c) == {node_a}
