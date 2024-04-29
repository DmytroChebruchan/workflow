from unittest.mock import AsyncMock, patch

from api.nodes.crud import get_node_by_id
from tests.mock_file import true_returner_mock


@patch("api.nodes.crud.get_element_by_id", true_returner_mock)
async def test_get_node_by_id():
    mock_session = AsyncMock()
    assert await get_node_by_id(session=mock_session, node_id=1) is True
