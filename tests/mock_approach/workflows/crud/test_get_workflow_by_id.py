from unittest.mock import AsyncMock, patch

from api.workflows.crud import get_workflow_by_id


async def get_element_by_id_mock(**kwargs):
    return True


@patch("api.workflows.crud.get_element_by_id", get_element_by_id_mock)
async def test_get_workflow_by_id():
    mock_session = AsyncMock()
    assert (
        await get_workflow_by_id(session=mock_session, workflow_id=1) is True
    )
