import unittest
from unittest.mock import AsyncMock, MagicMock, patch

from api.nodes.scripts import delete_node_by_id_script


class TestDeleteNodeIdScript(unittest.IsolatedAsyncioTestCase):
    @patch("api.nodes.scripts.NodeManagement")
    @patch("api.nodes.scripts.EdgeDelManager")
    @patch("api.nodes.scripts.ElementRepo")
    async def test_delete_node_by_id_script(
        self, MockElementRepo, MockEdgeDelManager, MockNodeManagement
    ):
        # Create mock instances
        mock_session = MagicMock()
        mock_node = MagicMock()

        # Create mock objects for EdgeDelManager and ElementRepo
        mock_edge_del_object = MagicMock()
        mock_element = MagicMock()

        # Configure mock objects
        mock_node.get_node_by_id = AsyncMock(
            return_value=mock_node
        )  # Mocking async method
        mock_edge_del_object.delete_edges_of_node = (
            AsyncMock()
        )  # Mocking async method
        mock_element.delete_element_from_db = (
            AsyncMock()
        )  # Mocking async method

        # Mock return values of NodeManagement, EdgeDelManager, and ElementRepo
        MockNodeManagement.return_value = mock_node
        MockEdgeDelManager.return_value = mock_edge_del_object
        MockElementRepo.return_value = mock_element

        # Call the function
        await delete_node_by_id_script(session=mock_session, node_id=1)

        # Assert that methods were called with the correct arguments
        mock_node.get_node_by_id.assert_awaited_once()
        mock_edge_del_object.delete_edges_of_node.assert_awaited_once_with()
        mock_element.delete_element_from_db.assert_awaited_once()
