from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

from tests.mock_file import test_workflow_mock


@patch("api.workflows.views.get_workflow_by_id", new=test_workflow_mock)
@pytest.mark.asyncio
async def test_read_workflow(client: TestClient):
    response = client.get("/workflows/read/1")
    response_data = response.json()
    assert response_data == {"id": 1, "title": "some"}
    assert response.status_code == 200
