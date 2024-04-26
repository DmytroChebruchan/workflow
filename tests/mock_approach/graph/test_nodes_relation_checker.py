import unittest
from unittest.mock import AsyncMock

from sqlalchemy.ext.asyncio import AsyncSession

from core.graph.workflow_graph import WorkflowGraph

from api.nodes.node_attr_values import NodeType
from core.models import Node, Edge


class TestWorkflowGraph(unittest.IsolatedAsyncioTestCase):
    async def test_async_update_graph(self):
        # Create mock nodes, edges, and session
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

        # Mock the required functions
        WorkflowGraph._add_edges = AsyncMock()
        WorkflowGraph._add_nodes = AsyncMock()
        WorkflowGraph._update_important_nodes_by_type = AsyncMock()

        # Create WorkflowGraph instance
        workflow_graph = WorkflowGraph(
            nodes=nodes, edges=edges, session=AsyncSession()
        )

        # Call async_update_graph
        await workflow_graph.async_update_graph()

        # Assertions
        WorkflowGraph._add_edges.assert_awaited_once()
        WorkflowGraph._add_nodes.assert_awaited_once()
        WorkflowGraph._update_important_nodes_by_type.assert_awaited_once()

    async def test_has_path(self):
        # Create mock nodes, edges, and session
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

        # Create WorkflowGraph instance
        workflow_graph = WorkflowGraph(
            nodes=nodes, edges=edges, session=AsyncSession()
        )

        # Call has_path
        has_path = await workflow_graph.has_path()

        # Assertions
        self.assertTrue(has_path)
