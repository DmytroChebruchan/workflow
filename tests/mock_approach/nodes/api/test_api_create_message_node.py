from unittest.mock import patch

import pytest

from tests.mock_file import true_returner


@patch(
    "api.nodes.utils.check_node_type_existence_in_workflow", new=true_returner
)
@pytest.mark.asyncio
async def test_create_message_node(client):
    # Create message node
    node_data = {
        "type": "Message Node",
        "workflow_id": 1,
        "message_text": "Hello World",
        "status": "pending",
    }
    #
    response = client.post("/nodes/create/", json=node_data)
    response_data = response.json()
    assert response_data == {
        "type": "Message Node",
        "workflow_id": 1,
        "message_text": "Hello World",
        "status": "pending",
        "id": 1,
        "condition": None,
    }
    assert response.status_code == 200


@patch("api.workflows.crud.get_workflow_by_id", new=true_returner)
@pytest.mark.asyncio
async def test_create_message_node_wrong_status(client):

    # Create message node
    node_data = {
        "type": "Message Node",
        "workflow_id": 1,
        "message_text": "Hello World",
        "status": "",
    }
    response = client.post("/nodes/create/", json=node_data)
    assert response.status_code == 422


@patch("api.workflows.crud.get_workflow_by_id", new=true_returner)
@pytest.mark.asyncio
async def test_create_message_node_without_status(client):

    # Create message node
    node_data = {
        "type": "Message Node",
        "workflow_id": 1,
        "message_text": "Hello World",
    }
    response = client.post("/nodes/create/", json=node_data)
    assert response.status_code == 422
