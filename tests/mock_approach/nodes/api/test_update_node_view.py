from unittest.mock import AsyncMock, patch

import pytest
from fastapi.testclient import TestClient

from api.nodes.crud import create_node
from api.nodes.node_attr_values import NodeType
from api.nodes.schemas.schemas import NodeCreate, NodeUpdate
from core.models.node import Node
from tests.conftest import client


async def update_node_by_id_mock(*args, **kwargs):
    return None


@patch("api.nodes.views.update_node", new=update_node_by_id_mock)
@pytest.mark.asyncio
async def test_update_node_view(client: TestClient):
    node_update = NodeUpdate(
        workflow_id=1,
        type=NodeType.START,
        id=1,
    )
    response = client.put(
        "/nodes/1",
        json={
            **node_update.model_dump(),
            "node_id": "1",
        },
    )
    assert response.status_code == 200
    assert response.json() == {"message": "Node updated!"}
