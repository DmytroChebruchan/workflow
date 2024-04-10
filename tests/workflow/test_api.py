from fastapi.testclient import TestClient

from tests.conftest import test_client


def test_workflow_created(test_client: TestClient):
    response = test_client.post(
        "/workflows/create/", json={"title": "Test Workflow"}
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["title"] == "Test Workflow"
    assert "id" in data


def test_show_workflows(test_client: TestClient):
    response = test_client.get("/workflows/show_workflows/")
    assert response.status_code == 200, response.text
