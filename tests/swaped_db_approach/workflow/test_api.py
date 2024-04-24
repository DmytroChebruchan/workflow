from unittest.mock import patch


async def get_workflow_by_id_mock(*args, **kwargs):
    return True


async def true_returner(*args, **kwargs):
    return True


@patch(
    "api.nodes.utils.check_node_type_existence_in_workflow", new=true_returner
)
async def test_workflow_created(client):
    response = client.post(
        "/workflows/create/", json={"title": "Test Workflow"}
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["title"] == "Test Workflow"
    assert "id" in data


async def test_show_workflows(client):
    response = client.get("/workflows/show_workflows/")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data == []
