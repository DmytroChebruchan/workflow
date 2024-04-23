from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

from core.models import Workflow


async def get_workflow_by_id_mock(*args, **kwargs):
    return Workflow(title="some", id=1)


async def run_workflow_mock(*args, **kwargs):
    return "Hello"


@patch("api.workflows.views.get_workflow_by_id", new=get_workflow_by_id_mock)
@patch("api.workflows.views.run_workflow", new=run_workflow_mock)
@pytest.mark.asyncio
async def test_run_workflow(client: TestClient):
    response = client.get("/workflows/run/1/")
    response_data = response.json()
    assert response_data == "Hello"
    assert response.status_code == 200
