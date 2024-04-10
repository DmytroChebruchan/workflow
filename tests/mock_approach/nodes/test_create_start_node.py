from unittest.mock import AsyncMock

import pytest

from api.nodes.crud import create_node
from api.nodes.schemas.schemas import NodeCreate
from core.models.node import Node


@pytest.mark.asyncio
async def test_create_node():

    dummy_node = {
        "type": "Start Node",
        "workflow_id": 1,
        "id_of_true_condition": 2,
    }
    mock_node_in = NodeCreate(**dummy_node)

    # Mock the methods of the session
    mock_session = AsyncMock()

    # Call the function
    result = await create_node(mock_session, mock_node_in)

    # Assertions
    assert isinstance(result, Node)
