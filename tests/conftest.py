from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import (
    async_sessionmaker,
    create_async_engine,
    AsyncSession,
)

from core.models.db_helper import db_helper
from main import app
from tests.constants import DATABASE_URL

# Create an in-memory SQLite database for testing
engine = create_async_engine(DATABASE_URL, echo=True)
TestingSessionLocal = async_sessionmaker(
    autocommit=False, autoflush=False, bind=engine
)


# async def async_session() -> AsyncSession:
#     async with TestingSessionLocal() as session:
#         async with engine.begin() as conn:
#             await conn.run_sync(Base.metadata.create_all)
#         yield session


async def async_session() -> AsyncSession:
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        await db.close()


def client():
    app.dependency_overrides[db_helper.session_dependency] = async_session
    return TestClient(app)


async def create_test_workflow(client: TestClient) -> int:
    response = client.post(
        "/workflows/create/", json={"title": "Test Workflow"}
    )
    data = response.json()
    return data["id"]
