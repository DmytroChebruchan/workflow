from unittest.mock import AsyncMock, patch

import pytest

from api.nodes.crud import create_node
from api.nodes.schemas.schemas import NodeCreate
from core.models.node import Node


async def get_workflow_by_id_mock(*args, **kwargs):
    return True


async def nodes_existing_checker_mock(*args, **kwargs):
    pass


@patch(
    "api.workflows.validator.get_workflow_by_id", new=get_workflow_by_id_mock
)
@patch(
    "api.workflows.validator.nodes_existing_checker",
    new=nodes_existing_checker_mock,
)
@pytest.mark.asyncio
async def test_create_node():

    dummy_node = {
        "type": "Start Node",
        "workflow_id": 1,
    }
    mock_node_in = NodeCreate(**dummy_node)

    # Mock the methods of the session
    mock_session = AsyncMock()

    # Call the function
    result = await create_node(mock_session, mock_node_in)

    # Assertions
    assert isinstance(result, Node)
