import pytest

from algorithms.astar import AStar, HeuristicType
from algorithms.graph_lib.directed_graph import DirectedEdge, DirectedGraph, DirectedNode


class TestAStarAlgorithm:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.directed_graph = DirectedGraph()
        n1 = DirectedNode(1, x=0, y=0)
        n2 = DirectedNode(2, x=1, y=0)
        n3 = DirectedNode(3, x=1, y=2)
        n4 = DirectedNode(4, x=2, y=2)

        edge_12 = DirectedEdge("edge_12", n1, n2, 1.0)
        edge_23 = DirectedEdge("edge_23", n2, n3, 2.0)
        edge_34 = DirectedEdge("edge_34", n3, n4, 1.0)

        self.directed_graph.add_node(n1)
        self.directed_graph.add_node(n2)
        self.directed_graph.add_node(n3)
        self.directed_graph.add_node(n4)
        self.directed_graph.add_edge(edge_12)
        self.directed_graph.add_edge(edge_23)
        self.directed_graph.add_edge(edge_34)

    def test_astar_search_valid_path(self):
        astar = AStar(self.directed_graph, heuristic_type=HeuristicType.MANHATTAN)
        path = astar.find_shortest_path(1, 4)
        assert path == [1, 2, 3, 4]

    def test_astar_search_no_path(self):
        n5 = DirectedNode(5, x=4, y=4)
        self.directed_graph.add_node(n5)  # Isolated node
        astar = AStar(self.directed_graph, heuristic_type=HeuristicType.MANHATTAN)
        path = astar.find_shortest_path(1, 5)
        assert path is None
