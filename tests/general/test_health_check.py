import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from core.models import Base
from main import app
from tests.conftest import async_session, client
from tests.constants import DATABASE_URL


@pytest.mark.asyncio
async def test_health_check(client: TestClient, async_session: AsyncSession):
    response = client.post("/health_check/")
    dict_response = response.json()
    assert dict_response["message"] == "Healthy"
    assert response.status_code == 200
