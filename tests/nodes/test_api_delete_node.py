# from unittest.mock import patch, AsyncMock
#
# import pytest
# from fastapi.testclient import TestClient
#
# from core.models.node import Node
# from tests.conftest import client
#
#
# @pytest.fixture
# def mock_get_async_session():
#     return AsyncMock()
#
#
# @pytest.fixture
# def get_node_by_id_mock():
#     return Node()
#
#
# @patch("api.workflows.crud.get_node_by_id", new=get_node_by_id_mock)
# # @patch("tests.conftest.override_get_async_session", new=mock_get_async_session)
# @pytest.mark.asyncio
# async def test_delete_node(client: TestClient):
#
#     node_data = {
#         "type": "Start Node",
#         "workflow_id": 1,
#         "id": 1,
#     }
#
#     create_node = client.post("/api/nodes", json=node_data)
#
#     # Delete the created node
#     delete_response = client.delete(f"/nodes/{node_data['id']}/")
#     assert delete_response.status_code == 200
#
#     # Verify that the node has been deleted
#     get_response = client.get(f"/nodes/details/{node_data['id']}/")
#     assert get_response.status_code == 404
