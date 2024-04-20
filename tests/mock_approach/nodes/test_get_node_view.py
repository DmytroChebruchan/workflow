from unittest.mock import AsyncMock

import pytest

from api.nodes.crud import create_node
from api.nodes.schemas.schemas import NodeCreate
from core.models.node import Node


from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

from tests.conftest import client


async def get_node_by_id_mock(*args, **kwargs):
    return Node(type="Start Node", id=1, workflow_id=1)


@patch("api.nodes.views.get_node_by_id", new=get_node_by_id_mock)
@pytest.mark.asyncio
async def test_get_node_view(client: TestClient):
    response = client.get("/nodes/read/1")
    assert response.status_code == 200
