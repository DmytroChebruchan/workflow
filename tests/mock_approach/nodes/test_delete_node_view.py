from unittest.mock import AsyncMock

import pytest

from api.nodes.crud import create_node
from api.nodes.schemas.schemas import NodeCreate
from core.models.node import Node


from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

from tests.conftest import client


async def delete_node_by_id_mock(*args, **kwargs):
    return


@patch("api.nodes.views.delete_node_by_id", new=delete_node_by_id_mock)
@pytest.mark.asyncio
async def test_delete_node_view(client: TestClient):
    response = client.delete("/nodes/1")
    assert response.status_code == 200
    assert response.json() == {"message": "Node deleted!"}
