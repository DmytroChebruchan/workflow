import unittest

from sqlalchemy.ext.asyncio import AsyncSession

from api.nodes.node_attr_values import NodeType
from core.graph.graph_classes.workflow_graph import WorkflowGraph
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
        self.assertEqual(len(steps), 3)

        path = await workflow_graph.find_path()

        self.assertEqual(path["has_path"], True)
        self.assertEqual(len(path["path"]), 3)
