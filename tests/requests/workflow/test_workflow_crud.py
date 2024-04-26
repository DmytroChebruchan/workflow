from unittest.mock import patch

from core.models import Workflow
from tests.mock_file import true_returner_mock


async def success_workflow_mock(*args, **kwargs):
    return Workflow(id=1, title="updated title")


@patch(
    "api.nodes.utils.check_node_type_existence_in_workflow",
    new=true_returner_mock,
)
async def test_workflow_created(client):
    response = client.post(
        "/workflows/create/", json={"title": "Test Workflow"}
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["title"] == "Test Workflow"
    assert "id" in data


@patch(
    "api.workflows.views.get_workflow_by_id",
    new=true_returner_mock,
)
@patch(
    "api.workflows.views.update_workflow",
    new=success_workflow_mock,
)
async def test_workflow_update(client):
    response = client.put(
        "workflows/update/1", json={"title": "Updated Title", "id": "1"}
    )
    assert response.status_code == 200, True
    assert (
        response.content.decode("utf-8") == "Workflow with id 1 was updated."
    )


@patch(
    "api.workflows.views.get_workflow_by_id",
    new=success_workflow_mock,
)
@patch(
    "api.workflows.views.delete_workflow_by_id",
    new=true_returner_mock,
)
async def test_workflow_delete(client):
    response = client.delete("/workflows/delete/1")
    assert response.status_code == 200
    assert (
        response.content.decode("utf-8") == "Workflow with id 1 was deleted."
    )


async def test_show_workflows(client):
    response = client.get("/workflows/show_workflows/")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data == []
