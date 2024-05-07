from unittest.mock import patch

import pytest

from api.nodes.crud_NodeManagement import NodeManagement
from api.nodes.node_attr_values import NodeType
from core.models import Node
from tests.mock_file import true_returner_mock


async def node_mock_returner(*args, **kwargs):
    return Node(
        id=1,
        workflow_id=1,
        type="End Node",
        status="",
        message_text="",
        condition="True",
    )


@patch(
    "api.nodes.validation.script.nodes_validation_by_id",
    new=true_returner_mock,
)
@patch.object(
    NodeManagement,
    "get_element_by_id",
    new=node_mock_returner,
)
@patch.object(
    NodeManagement,
    "commit_and_refresh_element",
    new=node_mock_returner,
)
@pytest.mark.asyncio
async def test_update_node_view(client):
    node_update_dict = {"workflow_id": 1, "type": NodeType.START, "id": 1}
    response = client.put("/nodes/update/1", json=node_update_dict)
    assert response.status_code == 200
    assert response.json() == {"message": "Node updated!"}
