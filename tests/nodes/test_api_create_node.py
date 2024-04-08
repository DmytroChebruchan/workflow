import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from core.models import Base
from main import app
from tests.constants import DATABASE_URL

# Create an in-memory SQLite database for testing
engine = create_async_engine(DATABASE_URL, echo=True)
TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine
)


@pytest.fixture
async def async_session():
    async with TestingSessionLocal() as session:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        yield session


@pytest.fixture
def client():
    return TestClient(app)


async def create_test_workflow(client: TestClient) -> int:
    response = client.post(
        "/workflows/create/", json={"title": "Test Workflow"}
    )
    data = response.json()
    return data["id"]


@pytest.mark.asyncio
async def test_create_start_node(
    client: TestClient, async_session: AsyncSession
):
    workflow_id = await create_test_workflow(client)

    # Create start node
    node_data = {"type": "Start Node", "workflow_id": workflow_id}
    response = client.post("/nodes/create/", json=node_data)
    assert response.status_code == 200
    node = response.json()
    assert node["type"] == node_data["type"]
    assert node["workflow_id"] == node_data["workflow_id"]


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
    }
    response = client.post("/nodes/create/", json=node_data)
    assert response.status_code == 200
    node = response.json()
    assert node["type"] == node_data["type"]
    assert node["workflow_id"] == node_data["workflow_id"]
    assert node["message_text"] == node_data["message_text"]