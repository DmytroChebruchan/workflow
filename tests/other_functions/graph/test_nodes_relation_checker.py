import unittest

from sqlalchemy.ext.asyncio import AsyncSession

from api.nodes.node_attr_values import NodeType
from core.graph.workflow_graph import WorkflowGraph
from core.models import Edge, Node


async def workflow_graph_generator_mock(edges, nodes):
    workflow_graph = WorkflowGraph(
        nodes=nodes, edges=edges, session=AsyncSession()
    )
    workflow_graph.graph.add_nodes_from(nodes)
    workflow_graph.graph.add_edge(nodes[0], nodes[1], condition=True)
    workflow_graph.start_node, workflow_graph.end_node = nodes[0], nodes[1]
    return workflow_graph


class TestWorkflowGraph(unittest.IsolatedAsyncioTestCase):

    nodes = [
        Node(id=1, type=NodeType.START),
        Node(id=2, type=NodeType.END),
    ]
    edges = [
        Edge(
            source_node_id=1,
            destination_node_id=2,
            condition_type=True,
        )
    ]

    async def test_has_path(self):

        # Create WorkflowGraph instance
        workflow_graph = WorkflowGraph(
            nodes=self.nodes, edges=self.edges, session=AsyncSession()
        )

        # Call has_path
        has_path = await workflow_graph.has_path()

        # Assertions
        self.assertTrue(has_path)

    async def test_path_steps_generator(self):

        # Create WorkflowGraph instance
        workflow_graph = await workflow_graph_generator_mock(
            self.edges, self.nodes
        )
        # Call path_steps_generator
        steps = await workflow_graph.path_steps_generator()

        # Assertions
        expected_steps = [
            {"type": "node", "value": self.nodes[0]},
            {"type": "edge", "value": {"condition_of_edge": True}},
            {"type": "node", "value": self.nodes[1]},
        ]
        self.assertEqual(steps, expected_steps)

        path = await workflow_graph.find_path()
        expected_path = {"has_path": True, "path": expected_steps}
        self.assertEqual(path, expected_path)
