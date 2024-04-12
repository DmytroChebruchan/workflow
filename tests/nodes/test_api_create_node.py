from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

from tests.conftest import client


async def get_workflow_by_id_mock(session, workflow_id):
    return True


@patch("api.workflows.crud.get_workflow_by_id", new=get_workflow_by_id_mock)
@pytest.mark.asyncio
async def test_create_start_node(client: TestClient):
    # Create start node
    node_data = {
        "type": "Start Node",
        "workflow_id": 1,
        "id_of_true_condition": 1,
    }
    response = client.post("/nodes/create/", json=node_data)
    assert response.status_code == 200
    node = response.json()
    assert node["type"] == node_data["type"]
    assert node["workflow_id"] == node_data["workflow_id"]


@patch("api.workflows.crud.get_workflow_by_id", new=get_workflow_by_id_mock)
@pytest.mark.asyncio
async def test_create_condition_node(client: TestClient):

    # Create message node
    node_data = {
        "type": "Condition Node",
        "workflow_id": 1,
        "condition": "Some condition",
        "id_of_true_condition": 1,
        "id_of_false_condition": 2,
    }
    response = client.post("/nodes/create/", json=node_data)
    assert response.status_code == 200
    node = response.json()
    assert node["type"] == node_data["type"]
    assert node["workflow_id"] == node_data["workflow_id"]
    assert node["condition"] == node_data["condition"]


@patch("api.workflows.crud.get_workflow_by_id", new=get_workflow_by_id_mock)
@pytest.mark.asyncio
async def test_create_condition_node_without_condition(client: TestClient):
    # Create message node
    node_data = {
        "type": "Condition Node",
        "workflow_id": 1,
    }
    response = client.post("/nodes/create/", json=node_data)
    assert response.status_code == 422
