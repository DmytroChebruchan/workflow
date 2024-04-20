from unittest.mock import AsyncMock, patch

from api.nodes.crud import get_node_by_id


async def get_element_by_id_mock(**kwargs):
    return True


@patch("api.nodes.crud.get_element_by_id", get_element_by_id_mock)
async def test_get_node_by_id():
    mock_session = AsyncMock()
    assert await get_node_by_id(session=mock_session, node_id=1) is True
