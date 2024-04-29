import unittest
from unittest.mock import AsyncMock

from api.workflows.scripts import run_workflow_script
from core.graph.workflow_graph import WorkflowGraph


class TestRunWorkflow(unittest.IsolatedAsyncioTestCase):
    async def test_run_workflow(self):
        # generating mocks
        WorkflowGraph.async_update_graph = AsyncMock(return_value=1)
        WorkflowGraph.find_path = AsyncMock(return_value=1)

        # making request
        result = await run_workflow_script(AsyncMock(), 1)

        # assert
        self.assertEqual(result, 1)
        self.assertEqual(WorkflowGraph.async_update_graph.call_count, 1)
        self.assertEqual(WorkflowGraph.find_path.call_count, 1)
