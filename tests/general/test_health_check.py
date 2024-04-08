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


@pytest.mark.asyncio
async def test_health_check(client: TestClient, async_session: AsyncSession):
    response = client.post("/health_check/")
    dict_response = response.json()
    assert dict_response["message"] == "Healthy"
    assert response.status_code == 200
