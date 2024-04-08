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


async def test_create_workflow(client: TestClient, async_session: AsyncSession):
    response = client.post("/workflows/health_check/")
    dict_response = response.json()
    assert dict_response["message"] == "Healthy"
    assert response.status_code == 200


def test_workflow_created(client: TestClient, async_session: AsyncSession):
    response = client.post(
        "/workflows/create/", json={"title": "Test Workflow"}
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["title"] == "Test Workflow"
    assert "id" in data


def test_get_workflows(client: TestClient, async_session: AsyncSession):
    response = client.get("/workflows/show_workflows/")
    assert response.status_code == 200, response.text
