import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession

from tests.conftest import async_session, client, create_test_workflow


@pytest.mark.asyncio
async def test_create_message_node(
    client: TestClient, async_session: AsyncSession
):
    workflow_id = await create_test_workflow(client)

    # Create message node
    node_data = {
        "type": "Message Node",
        "workflow_id": workflow_id,
        "message_text": "Hello World",
        "status": "pending",
    }
    response = client.post("/nodes/create/", json=node_data)
    assert response.status_code == 200
    node = response.json()
    assert node["type"] == node_data["type"]
    assert node["workflow_id"] == node_data["workflow_id"]
    assert node["message_text"] == node_data["message_text"]


@pytest.mark.asyncio
async def test_create_message_node_wrong_status(
    client: TestClient, async_session: AsyncSession
):
    workflow_id = await create_test_workflow(client)

    # Create message node
    node_data = {
        "type": "Message Node",
        "workflow_id": workflow_id,
        "message_text": "Hello World",
        "status": "",
    }
    response = client.post("/nodes/create/", json=node_data)
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_create_message_node_without_status(
    client: TestClient, async_session: AsyncSession
):
    workflow_id = await create_test_workflow(client)

    # Create message node
    node_data = {
        "type": "Message Node",
        "workflow_id": workflow_id,
        "message_text": "Hello World",
    }
    response = client.post("/nodes/create/", json=node_data)
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_create_start_node_with_message(
    client: TestClient, async_session: AsyncSession
):
    workflow_id = await create_test_workflow(client)

    # Try to create start node with message
    node_data = {
        "type": "Start Node",
        "workflow_id": workflow_id,
        "message_text": "Hello",
    }
    response = client.post("/nodes/create/", json=node_data)
    assert response.status_code == 422
