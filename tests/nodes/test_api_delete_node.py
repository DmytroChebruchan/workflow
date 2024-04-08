import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from core.models import Base
from main import app

# Create an in-memory SQLite database for testing
DATABASE_URL = "sqlite+aiosqlite:///:memory:"
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
async def test_delete_node(client: TestClient, async_session: AsyncSession):

    # Create a node to be deleted
    workflow_id = await create_test_workflow(client=client)
    node_data = {
        "type": "Start Node",
        "workflow_id": workflow_id,
    }
    create_response = client.post("/nodes/create/", json=node_data)
    assert create_response.status_code == 200
    created_node = create_response.json()

    # Delete the created node
    delete_response = client.delete(f"/nodes/{created_node['id']}/")
    assert delete_response.status_code == 200

    # Verify that the node has been deleted
    get_response = client.get(f"/nodes/{created_node['id']}/")
    assert get_response.status_code == 404
