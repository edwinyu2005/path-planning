import pytest

from algorithms.dijkstra import Dijkstra
from algorithms.graph_lib.directed_graph import DirectedEdge, DirectedGraph, DirectedNode


class TestDijkstraAlgorithm:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.directed_graph = DirectedGraph()

        node_a = DirectedNode("A")
        node_b = DirectedNode("B")
        node_c = DirectedNode("C")
        node_d = DirectedNode("D")
        edge_ab = DirectedEdge("edge_ab", node_a, node_b, 1.0)
        edge_bc = DirectedEdge("edge_bc", node_b, node_c, 2.0)
        edge_ac = DirectedEdge("edge_ac", node_a, node_c, 4.0)
        edge_cd = DirectedEdge("edge_cd", node_c, node_d, 1.0)

        self.directed_graph.add_node(node_a)
        self.directed_graph.add_node(node_b)
        self.directed_graph.add_node(node_c)
        self.directed_graph.add_node(node_d)
        self.directed_graph.add_edge(edge_ab)
        self.directed_graph.add_edge(edge_bc)
        self.directed_graph.add_edge(edge_ac)
        self.directed_graph.add_edge(edge_cd)

        self.dijkstra_algo = Dijkstra(self.directed_graph)

    def test_find_shortest_paths(self):
        shortest_paths = self.dijkstra_algo.find_shortest_paths("A")

        assert shortest_paths["A"] == (0, None)
        assert shortest_paths["B"] == (1, "A")
        assert shortest_paths["C"] == (3, "B")
        assert shortest_paths["D"] == (4, "C")
