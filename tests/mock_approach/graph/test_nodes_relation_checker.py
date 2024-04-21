import unittest
from unittest.mock import MagicMock

from core.graph.utils import nodes_relation_checker


class TestNodesRelationChecker(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.nodes = [
            MagicMock(id=1, type="Start Node"),
            MagicMock(id=2, type="Normal Node"),
            MagicMock(id=3, type="End Node"),
        ]
        self.edges = [
            MagicMock(
                source_node_id=1,
                destination_node_id=2,
                condition_type="Condition 1",
            ),
            MagicMock(
                source_node_id=2,
                destination_node_id=3,
                condition_type="Condition 2",
            ),
        ]

    async def test_has_path(self):
        result = await nodes_relation_checker(self.nodes, self.edges)
        if not result:
            print("Graph:")
            print(self.edges)
            print(
                "Start Node:",
                [node.id for node in self.nodes if node.type == "Start Node"],
            )
            print(
                "End Node:",
                [node.id for node in self.nodes if node.type == "End Node"],
            )
        self.assertTrue(result)

    # async def test_no_path(self):
    #     # Change the edges to make the graph disconnected
    #     self.edges.append(
    #         MagicMock(
    #             source_node_id=3,
    #             destination_node_id=1,
    #             condition_type="Condition 3",
    #         )
    #     )
    #     result = await nodes_relation_checker(self.nodes, self.edges)
    #     self.assertFalse(result)

    async def test_empty_graph(self):
        # Test with empty nodes and edges
        result = await nodes_relation_checker([], [])
        self.assertFalse(result)
