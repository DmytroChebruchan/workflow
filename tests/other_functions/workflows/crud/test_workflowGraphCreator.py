import unittest
from unittest.mock import MagicMock

from sqlalchemy.ext.asyncio import AsyncSession

from core.graph.graph_classes.workflow_graph_create import WorkflowGraphCreator
from core.models import Edge, Node


class TestWorkflowGraphCreator(unittest.TestCase):

    def setUp(self):
        self.nodes = [
            Node(id=1, type="Start Node"),
            Node(id=2, type="End Node"),
        ]
        self.edges = [
            Edge(
                source_node_id=1,
                destination_node_id=2,
                condition_type=True,
            )
        ]
        self.session = MagicMock(spec=AsyncSession)

    def test_graph_creation(self):
        graph_creator = WorkflowGraphCreator(
            self.nodes, self.edges, self.session
        )
        graph = graph_creator.graph
        # Check if nodes and edges are added properly
        self.assertIn(self.nodes[0], graph.nodes)
        self.assertIn(self.nodes[1], graph.nodes)
        self.assertIn((self.nodes[0], self.nodes[1]), graph.edges)
        # Add more assertions based on your requirements

    def test_important_nodes_identification(self):
        graph_creator = WorkflowGraphCreator(
            self.nodes, self.edges, self.session
        )
        # Check if start and end nodes are correctly identified
        self.assertEqual(graph_creator.start_node, self.nodes[0])
        self.assertEqual(graph_creator.end_node, self.nodes[1])
        # Add more assertions based on your requirements

    def test_void_edges_removal(self):
        graph_creator = WorkflowGraphCreator(
            self.nodes, self.edges, self.session
        )
        # Add some void edges to the graph
        graph_creator.graph.add_edge(
            self.nodes[1], self.nodes[0], condition="Void"
        )
        initial_edge_count = len(graph_creator.graph.edges)
        # Remove void edges
        graph_creator.clean_graph_from_void_edges()
        self.assertEqual(len(graph_creator.graph.edges), initial_edge_count)
        # Add more assertions based on your requirements
