import unittest
from unittest.mock import patch

from sqlalchemy.ext.asyncio import AsyncSession

from api.workflows.schemas import WorkflowCreate
from api.workflows.utils import create_workflow_with_nodes
from core.models import Node, Workflow


class TestCreateWorkflowWithNodes(unittest.IsolatedAsyncioTestCase):
    @patch(
        "api.workflows.utils.create_node",
        return_value=Node(id=1, type="Start Node"),
    )
    @patch(
        "api.workflows.utils.create_workflow",
        return_value=Workflow(id=1, title="title"),
    )
    async def test_create_workflow_with_nodes(
        self, mock_create_workflow, mock_create_node
    ):
        result = await create_workflow_with_nodes(
            session=AsyncSession(), workflow_in=WorkflowCreate(title="title")
        )

        # Asserting that the result is an instance of Workflow
        self.assertIsInstance(result, Workflow)
        # Asserting that create_workflow and create_node were called once
        mock_create_workflow.assert_called_once()
        self.assertEqual(mock_create_node.call_count, 2)
