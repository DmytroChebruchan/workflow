import unittest
from unittest.mock import AsyncMock, MagicMock, patch

from api.nodes.scripts import delete_node_by_id_script


class TestDeleteNodeIdScript(unittest.IsolatedAsyncioTestCase):
    @patch("api.nodes.scripts.NodeManagement")
    @patch("api.edges.scripts.EdgeDelManager")
    async def test_delete_node_by_id_script(
        self, MockEdgeDelManager, MockNodeManagement
    ):
        # Create mock instances
        mock_session = MagicMock()
        mock_node = AsyncMock()

        # Create mock objects for EdgeDelManager and ElementRepo
        mock_edge_del_object = MagicMock()
        mock_element = MagicMock()

        # Configure mock objects
        mock_edge_del_object.delete_edges_of_node = (
            AsyncMock()
        )  # Mocking async method
        mock_element.delete_element_from_db = (
            AsyncMock()
        )  # Mocking async method

        # Mock return values of NodeManagement, EdgeDelManager, and ElementRepo
        MockNodeManagement.return_value = mock_node
        MockEdgeDelManager.return_value = mock_edge_del_object

        # Call the function
        await delete_node_by_id_script(session=mock_session, node_id=1)

        # Assert that methods were called with the correct arguments
        mock_edge_del_object.delete_edges_of_node.assert_awaited_once_with()
