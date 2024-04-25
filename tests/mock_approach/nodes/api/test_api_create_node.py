from unittest.mock import patch

import pytest

from tests.mock_file import true_returner


@patch(
    "api.nodes.utils.check_node_type_existence_in_workflow", new=true_returner
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


@patch(
    "api.nodes.utils.check_node_type_existence_in_workflow", new=true_returner
)
@pytest.mark.asyncio
async def test_create_condition_node(client):

    # Create message node
    node_data = {
        "type": "Condition Node",
        "workflow_id": 1,
        "condition": "Some condition",
    }
    response = client.post("/nodes/create/", json=node_data)
    assert response.status_code == 200
    node = response.json()
    assert node["type"] == node_data["type"]
    assert node["workflow_id"] == node_data["workflow_id"]
    assert node["condition"] == node_data["condition"]


@pytest.mark.asyncio
async def test_create_condition_node_without_condition(client):
    # Create message node
    node_data = {
        "type": "Condition Node",
        "workflow_id": 1,
    }
    response = client.post("/nodes/create/", json=node_data)
    assert response.status_code == 422
