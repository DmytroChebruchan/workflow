from unittest.mock import patch

import pytest

from core.models.node import Node


async def get_node_by_id_mock(*args, **kwargs):
    return Node(type="Start Node", id=1, workflow_id=1)


@patch("api.nodes.views.get_node_by_id", new=get_node_by_id_mock)
@pytest.mark.asyncio
async def test_get_node_view(client):
    response = client.get("/nodes/read/1")
    assert response.status_code == 200
