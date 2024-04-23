import pytest


@pytest.mark.asyncio
async def test_health_check(client):
    response = client.post("/health_check/")
    dict_response = response.json()
    assert dict_response["message"] == "Healthy"
    assert response.status_code == 200
