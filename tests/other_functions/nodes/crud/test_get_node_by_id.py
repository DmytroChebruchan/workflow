from unittest.mock import AsyncMock, patch

from api.nodes.crud import get_node_by_id
from tests.mock_file import true_returner_mock


@patch("api.general.utils_element_class.element_validator", true_returner_mock)
async def test_get_node_by_id():
    # Create a mock node object
    mock_node = AsyncMock()

    # Set the return value of mock_session.get() to be the mock_node
    mock_session = AsyncMock()
    mock_session.get.return_value = mock_node

    # Call get_node_by_id
    result = await get_node_by_id(session=mock_session, node_id=1)

    # Assert that the result is the same as the mock_node
    assert result == mock_node
