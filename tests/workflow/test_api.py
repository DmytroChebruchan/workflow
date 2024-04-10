from fastapi.testclient import TestClient

from tests.conftest import client


def test_workflow_created(client: TestClient):
    response = client.post(
        "/workflows/create/", json={"title": "Test Workflow"}
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["title"] == "Test Workflow"
    assert "id" in data


def test_show_workflows(client: TestClient):
    response = client.get("/workflows/show_workflows/")
    assert response.status_code == 200, response.text
