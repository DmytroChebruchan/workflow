from unittest.mock import patch

import pytest


async def delete_node_by_id_mock(*args, **kwargs):
    return


@patch("api.nodes.views.delete_node_by_id", new=delete_node_by_id_mock)
@pytest.mark.asyncio
async def test_delete_node_view(client):
    response = client.delete("/nodes/1")
    assert response.status_code == 200
    assert response.json() == {"message": "Node deleted!"}
