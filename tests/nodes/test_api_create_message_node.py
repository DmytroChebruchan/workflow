import pytest
from fastapi.testclient import TestClient
from tests.conftest import client
from unittest.mock import patch


async def get_workflow_by_id_mock(session, workflow_id):
    return True


@patch("api.workflows.crud.get_workflow_by_id", new=get_workflow_by_id_mock)
@pytest.mark.asyncio
async def test_create_message_node(client: TestClient):
    # Create message node
    node_data = {
        "type": "Message Node",
        "workflow_id": 1,
        "message_text": "Hello World",
        "status": "pending",
        "id_of_true_condition": 1,
    }
    #
    response = client.post("/nodes/create/", json=node_data)
    assert response.json() == {
        "condition": None,
        "id": 1,
        "message_text": "Hello World",
        "status": "pending",
        "type": "Message Node",
        "workflow_id": 1,
    }
    assert response.status_code == 200


@patch("api.workflows.crud.get_workflow_by_id", new=get_workflow_by_id_mock)
@pytest.mark.asyncio
async def test_create_message_node_wrong_status(client: TestClient):

    # Create message node
    node_data = {
        "type": "Message Node",
        "workflow_id": 1,
        "message_text": "Hello World",
        "status": "",
    }
    response = client.post("/nodes/create/", json=node_data)
    assert response.status_code == 422


@patch("api.workflows.crud.get_workflow_by_id", new=get_workflow_by_id_mock)
@pytest.mark.asyncio
async def test_create_message_node_without_status(client: TestClient):

    # Create message node
    node_data = {
        "type": "Message Node",
        "workflow_id": 1,
        "message_text": "Hello World",
    }
    response = client.post("/nodes/create/", json=node_data)
    assert response.status_code == 422


@patch("api.workflows.crud.get_workflow_by_id", new=get_workflow_by_id_mock)
@pytest.mark.asyncio
async def test_create_start_node_with_message(client: TestClient):
    # Try to create start node with message
    node_data = {
        "type": "Start Node",
        "workflow_id": 1,
        "message_text": "Hello",
    }
    response = client.post("/nodes/create/", json=node_data)
    assert response.status_code == 422
