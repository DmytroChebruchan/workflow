from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession

from tests.conftest import async_session, client


def test_workflow_created(client: TestClient, async_session: AsyncSession):
    response = client.post(
        "/workflows/create/", json={"title": "Test Workflow"}
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["title"] == "Test Workflow"
    assert "id" in data


def test_show_workflows(client: TestClient, async_session: AsyncSession):
    response = client.get("/workflows/show_workflows/")
    assert response.status_code == 200, response.text
