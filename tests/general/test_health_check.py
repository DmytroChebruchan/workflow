import pytest
from fastapi.testclient import TestClient

from tests.conftest import test_client


@pytest.mark.asyncio
async def test_health_check(test_client: TestClient):
    response = test_client.post("/health_check/")
    dict_response = response.json()
    assert dict_response["message"] == "Healthy"
    assert response.status_code == 200
