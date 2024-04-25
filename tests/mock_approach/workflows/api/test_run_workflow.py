from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

from tests.mock_file import run_workflow_mock, true_returner


@patch("api.workflows.views.get_workflow_by_id", new=true_returner)
@patch("api.workflows.views.run_workflow", new=run_workflow_mock)
@pytest.mark.asyncio
async def test_run_workflow(client: TestClient):
    response = client.get("/workflows/run/1/")
    response_data = response.json()
    assert response_data == "Hello"
    assert response.status_code == 200
