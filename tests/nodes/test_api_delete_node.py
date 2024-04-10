import pytest
from fastapi.testclient import TestClient

from tests.conftest import test_client, create_test_workflow


@pytest.mark.asyncio
async def test_delete_node(test_client: TestClient):

    # Create a node to be deleted
    workflow_id = await create_test_workflow(client=test_client)
    node_data = {
        "type": "Start Node",
        "workflow_id": workflow_id,
        "id_of_true_condition": 1,
    }
    create_response = test_client.post("/nodes/create/", json=node_data)
    assert create_response.status_code == 200
    created_node = create_response.json()

    # Delete the created node
    delete_response = test_client.delete(f"/nodes/{created_node['id']}/")
    assert delete_response.status_code == 200

    # Verify that the node has been deleted
    get_response = test_client.get(f"/nodes/details/{created_node['id']}/")
    assert get_response.status_code == 404
