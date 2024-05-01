from unittest.mock import AsyncMock, patch

import pytest

from api.nodes.schemas.schemas import NodeCreate
from api.nodes.script import create_node_script
from core.models.node import Node
from tests.mock_file import true_returner_mock
from tests.other_functions.nodes.fixture_nodes_dicts import dummy_node


@patch(
    "api.nodes.utils.check_node_type_existence_in_workflow",
    new=true_returner_mock,
)
@pytest.mark.asyncio
async def test_create_node():
    # creating mocks
    mock_node_in = NodeCreate(**dummy_node)
    mock_session = AsyncMock()

    # Call the function
    result = await create_node_script(mock_session, mock_node_in)

    # Assertions
    assert isinstance(result, Node)
