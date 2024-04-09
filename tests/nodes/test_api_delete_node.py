import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession

from tests.conftest import async_session, client, create_test_workflow


@pytest.mark.asyncio
async def test_delete_node(client: TestClient, async_session: AsyncSession):

    # Create a node to be deleted
    workflow_id = await create_test_workflow(client=client)
    node_data = {
        "type": "Start Node",
        "workflow_id": workflow_id,
    }
    create_response = client.post("/nodes/create/", json=node_data)
    assert create_response.status_code == 200
    created_node = create_response.json()

    # Delete the created node
    delete_response = client.delete(f"/nodes/{created_node['id']}/")
    assert delete_response.status_code == 200

    # Verify that the node has been deleted
    get_response = client.get(f"/nodes/{created_node['id']}/")
    assert get_response.status_code == 404
