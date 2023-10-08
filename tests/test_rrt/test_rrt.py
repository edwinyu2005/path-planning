import pytest

from algorithms.rrt import RRT
from algorithms.graph_lib.base_graph import BaseNode


class TestRRT:
    @pytest.fixture
    def basic_rrt(self):
        start_node = BaseNode(id="start", x=0, y=0)
        goal_node = BaseNode(id="goal", x=7, y=7)
        x_lim = (0, 10)
        y_lim = (0, 10)
        obstacles = [(5, 5, 1), (3, 6, 0.5), (7, 2, 1)]
        return RRT(start_node, goal_node, x_lim, y_lim, obstacles)

    def test_initial_nodes(self, basic_rrt):
        basic_rrt.plan()  # Run the RRT algorithm to grow the tree.
        assert basic_rrt.start in basic_rrt.graph.nodes

    def test_collision_check(self, basic_rrt):
        node_inside_obstacle = BaseNode(id="temp", x=5, y=5)
        node_outside_obstacle = BaseNode(id="temp2", x=6, y=6)

        assert basic_rrt._check_collision(basic_rrt.start, node_inside_obstacle)
        assert not basic_rrt._check_collision(basic_rrt.start, node_outside_obstacle)

    def test_plan_tree_growth(self, basic_rrt):
        initial_node_count = len(basic_rrt.graph.nodes)
        basic_rrt.plan()
        assert len(basic_rrt.graph.nodes) > initial_node_count
