from unittest.mock import patch

import pytest

from api.nodes.node_attr_values import NodeType
from api.nodes.schemas.schemas import NodeUpdate


async def update_node_by_id_mock(*args, **kwargs):
    return None


@patch("api.nodes.views.update_node", new=update_node_by_id_mock)
@pytest.mark.asyncio
async def test_update_node_view(client):
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
