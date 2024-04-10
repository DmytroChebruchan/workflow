import pytest
from fastapi.testclient import TestClient

from tests.conftest import test_client, create_test_workflow


@pytest.mark.asyncio
async def test_create_start_node(test_client: TestClient):
    workflow_id = await create_test_workflow(test_client)

    # Create start node
    node_data = {
        "type": "Start Node",
        "workflow_id": workflow_id,
        "id_of_true_condition": 1,
    }
    response = test_client.post("/nodes/create/", json=node_data)
    assert response.status_code == 200
    node = response.json()
    assert node["type"] == node_data["type"]
    assert node["workflow_id"] == node_data["workflow_id"]


@pytest.mark.asyncio
async def test_create_condition_node(test_client: TestClient):
    workflow_id = await create_test_workflow(test_client)

    # Create message node
    node_data = {
        "type": "Condition Node",
        "workflow_id": workflow_id,
        "condition": "Some condition",
        "id_of_true_condition": 1,
        "id_of_false_condition": 2,
    }
    response = test_client.post("/nodes/create/", json=node_data)
    assert response.status_code == 200
    node = response.json()
    assert node["type"] == node_data["type"]
    assert node["workflow_id"] == node_data["workflow_id"]
    assert node["condition"] == node_data["condition"]


@pytest.mark.asyncio
async def test_create_condition_node_without_condition(test_client: TestClient):
    workflow_id = await create_test_workflow(test_client)

    # Create message node
    node_data = {
        "type": "Condition Node",
        "workflow_id": workflow_id,
    }
    response = test_client.post("/nodes/create/", json=node_data)
    assert response.status_code == 422
