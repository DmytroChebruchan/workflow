from unittest.mock import patch

import pytest

from tests.mock_file import true_returner_mock


@patch("api.nodes.views.delete_node_by_id_script", new=true_returner_mock)
@pytest.mark.asyncio
async def test_delete_node_view(client):
    response = client.delete("/nodes/1")
    assert response.status_code == 200
    assert response.json() == {"message": "Node was deleted!"}
