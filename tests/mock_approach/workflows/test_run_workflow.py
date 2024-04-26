import unittest
from unittest.mock import AsyncMock, MagicMock, patch

from sqlalchemy.ext.asyncio import AsyncSession

from api.workflows.run_workflow import run_workflow
from core.graph.workflow_graph import WorkflowGraph


async def mock_async_update_graph(*_args, **_kwargs):
    return 1


class TestRunWorkflow(unittest.IsolatedAsyncioTestCase):
    async def test_run_workflow(self):
        WorkflowGraph.async_update_graph = MagicMock(
            return_value=mock_async_update_graph()
        )
        WorkflowGraph.find_path = MagicMock(
            return_value=mock_async_update_graph()
        )
        result = await run_workflow(AsyncMock(), 1)

        self.assertEqual(result, 1)
        self.assertEqual(WorkflowGraph.async_update_graph.call_count, 1)
