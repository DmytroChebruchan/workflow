from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

from core.models import Workflow
from tests.conftest import client


async def get_workflow_by_id_mock(*args, **kwargs):
    return Workflow(title="some", id=1)


@patch("api.workflows.views.get_workflow_by_id", new=get_workflow_by_id_mock)
@pytest.mark.asyncio
async def test_read_workflow(client: TestClient):
    response = client.get("/workflows/read/1")
    response_data = response.json()
    assert response_data == {"id": 1, "title": "some"}
    assert response.status_code == 200
