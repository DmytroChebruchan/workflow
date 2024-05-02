from unittest.mock import patch

import pytest

from tests.api_requests.nodes.fixture import dummy_msg_node, expected_data
from tests.mock_file import true_returner_mock


@patch(
    "api.nodes.utils.check_node_type_existence_in_workflow",
    new=true_returner_mock,
)
@pytest.mark.asyncio
async def test_create_start_node(client):
    # Create start node
    node_data = {
        "type": "Start Node",
        "workflow_id": 1,
    }
    response = client.post("/nodes/create/", json=node_data)
    assert response.status_code == 200
    node = response.json()
    assert node["type"] == node_data["type"]
    assert node["workflow_id"] == node_data["workflow_id"]


@pytest.mark.asyncio
async def test_create_condition_node_without_condition(client):
    # Create message node
    node_data = {
        "type": "Condition Node",
        "workflow_id": 1,
        "edge_condition_type": True,
    }
    response = client.post("/nodes/create/", json=node_data)
    assert response.status_code == 422


@patch("api.edges.crud.get_element_by_id", new=true_returner_mock)
@patch(
    "api.nodes.utils.check_node_type_existence_in_workflow",
    new=true_returner_mock,
)
@patch(
    "api.nodes.validation.script.nodes_validation_by_id", true_returner_mock
)
@pytest.mark.asyncio
async def test_create_message_node(client):
    # Create message node
    response = client.post("/nodes/create/", json=dummy_msg_node)

    response_data = response.json()

    assert response_data == expected_data
    assert response.status_code == 200


@patch("api.workflows.crud.get_workflow_by_id", new=true_returner_mock)
@pytest.mark.asyncio
async def test_create_message_node_wrong_status(client):

    # Create message node
    node_data = {
        "type": "Message Node",
        "workflow_id": 1,
        "message_text": "Hello World",
        "status": "",
        "from_node_id": 1,
        "nodes_dest_dict": {True: 1, False: 3},
    }
    response = client.post("/nodes/create/", json=node_data)
    assert response.status_code == 422


@patch("api.workflows.crud.get_workflow_by_id", new=true_returner_mock)
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
