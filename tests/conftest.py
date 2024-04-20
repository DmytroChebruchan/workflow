from unittest.mock import AsyncMock

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from core.database.database import get_async_session
from core.models.base import Base
from core.models.node import Node
from main import app

engine = create_async_engine(
    "sqlite+aiosqlite:///:memory:",
    connect_args={"check_same_thread": False},
)
SessionLocal = async_sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    class_=AsyncSession,
)
from typing import AsyncGenerator


async def override_get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    try:
        async with SessionLocal() as session:
            yield session
    finally:
        await engine.dispose()


@pytest.fixture
def client():
    app.dependency_overrides[get_async_session] = override_get_async_session
    client = TestClient(app)
    yield client


async def create_test_workflow(client: TestClient) -> int:
    response = client.post(
        "/workflows/create/", json={"title": "Test Workflow"}
    )
    data = response.json()
    return data["id"]


@pytest.fixture
def mock_get_async_session():
    return AsyncMock()


@pytest.fixture
def get_node_by_id_mock():
    return Node()
