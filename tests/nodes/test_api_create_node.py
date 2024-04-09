import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession

from tests.conftest import async_session, client, create_test_workflow


@pytest.mark.asyncio
async def test_create_start_node(
    client: TestClient, async_session: AsyncSession
):
    workflow_id = await create_test_workflow(client)

    # Create start node
    node_data = {
        "type": "Start Node",
        "workflow_id": workflow_id,
        "id_of_true_condition": 1,
    }
    response = client.post("/nodes/create/", json=node_data)
    assert response.status_code == 200
    node = response.json()
    assert node["type"] == node_data["type"]
    assert node["workflow_id"] == node_data["workflow_id"]


@pytest.mark.asyncio
async def test_create_condition_node(
    client: TestClient, async_session: AsyncSession
):
    workflow_id = await create_test_workflow(client)

    # Create message node
    node_data = {
        "type": "Condition Node",
        "workflow_id": workflow_id,
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


@pytest.mark.asyncio
async def test_create_condition_node_without_condition(
    client: TestClient, async_session: AsyncSession
):
    workflow_id = await create_test_workflow(client)

    # Create message node
    node_data = {
        "type": "Condition Node",
        "workflow_id": workflow_id,
    }
    response = client.post("/nodes/create/", json=node_data)
    assert response.status_code == 422
