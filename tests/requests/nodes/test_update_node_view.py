from unittest.mock import patch

import pytest

from api.nodes.node_attr_values import NodeType
from tests.mock_file import true_returner_mock


@patch("api.nodes.views.update_node", new=true_returner_mock)
@pytest.mark.asyncio
async def test_update_node_view(client):
    node_update_dict = {"workflow_id": 1, "type": NodeType.START, "id": 1}
    response = client.put("/nodes/1", json=node_update_dict)
    assert response.status_code == 200
    assert response.json() == {"message": "Node updated!"}
