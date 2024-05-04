import unittest
from unittest.mock import MagicMock

from sqlalchemy.ext.asyncio import AsyncSession

from api.nodes.node_handling import delete_nodes_of_workflow


class TestNodeFunctions(unittest.IsolatedAsyncioTestCase):

    async def test_delete_nodes_of_workflow(self):
        # Mock AsyncSession
        async_session_mock = MagicMock(spec=AsyncSession)

        # Call the function
        await delete_nodes_of_workflow(async_session_mock, 1)

        # Check if execute and commit methods were called with
        # the correct statement
        async_session_mock.execute.assert_called_once()
        async_session_mock.commit.assert_called_once()
