from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

from tests.conftest import client


async def get_workflow_by_id_mock(*args, **kwargs):
    return True


async def nodes_existing_checker_mock(*args, **kwargs):
    pass


@patch(
    "api.workflows.validator.get_workflow_by_id", new=get_workflow_by_id_mock
)
@patch(
    "api.workflows.validator.nodes_existing_checker",
    new=nodes_existing_checker_mock,
)
@pytest.mark.asyncio
async def test_create_start_node(client: TestClient):
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
    "api.workflows.validator.get_workflow_by_id", new=get_workflow_by_id_mock
)
@patch(
    "api.workflows.validator.nodes_existing_checker",
    new=nodes_existing_checker_mock,
)
@pytest.mark.asyncio
async def test_create_condition_node(client: TestClient):

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
async def test_create_condition_node_without_condition(client: TestClient):
    # Create message node
    node_data = {
        "type": "Condition Node",
        "workflow_id": 1,
    }
    response = client.post("/nodes/create/", json=node_data)
    assert response.status_code == 422
