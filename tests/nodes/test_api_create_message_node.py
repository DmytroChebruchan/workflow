import pytest
from fastapi.testclient import TestClient

from tests.conftest import test_client, create_test_workflow


@pytest.mark.asyncio
async def test_create_message_node(test_client: TestClient):
    workflow_id = await create_test_workflow(test_client)

    # Create message node
    node_data = {
        "type": "Message Node",
        "workflow_id": workflow_id,
        "message_text": "Hello World",
        "status": "pending",
        "id_of_true_condition": 1,
    }
    response = test_client.post("/nodes/create/", json=node_data)
    assert response.status_code == 200
    node = response.json()
    assert node["type"] == node_data["type"]
    assert node["workflow_id"] == node_data["workflow_id"]
    assert node["message_text"] == node_data["message_text"]


@pytest.mark.asyncio
async def test_create_message_node_wrong_status(test_client: TestClient):
    workflow_id = await create_test_workflow(test_client)

    # Create message node
    node_data = {
        "type": "Message Node",
        "workflow_id": workflow_id,
        "message_text": "Hello World",
        "status": "",
    }
    response = test_client.post("/nodes/create/", json=node_data)
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_create_message_node_without_status(test_client: TestClient):
    workflow_id = await create_test_workflow(test_client)

    # Create message node
    node_data = {
        "type": "Message Node",
        "workflow_id": workflow_id,
        "message_text": "Hello World",
    }
    response = test_client.post("/nodes/create/", json=node_data)
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_create_start_node_with_message(test_client: TestClient):
    workflow_id = await create_test_workflow(test_client)

    # Try to create start node with message
    node_data = {
        "type": "Start Node",
        "workflow_id": workflow_id,
        "message_text": "Hello",
    }
    response = test_client.post("/nodes/create/", json=node_data)
    assert response.status_code == 422
