import pytest
from fastapi import HTTPException, status

from api.general.utils import update_element_id_checker


@pytest.mark.asyncio
async def test_update_element_id_checker_same_id():
    original_id = 1
    update_id = 1
    try:
        await update_element_id_checker(original_id, update_id)
    except HTTPException as exc:
        assert exc.status_code == status.HTTP_400_BAD_REQUEST
        assert (
            exc.detail == "Workflow with ID in update workflow is not correct."
        )
    else:
        assert "HTTPException not raised when original_id equals update_id"


@pytest.mark.asyncio
async def test_update_element_id_checker_different_id():
    original_id = 1
    update_id = 2
    with pytest.raises(HTTPException) as exc_info:
        await update_element_id_checker(original_id, update_id)
    assert exc_info.value.status_code == status.HTTP_400_BAD_REQUEST
    assert (
        exc_info.value.detail
        == "Workflow with ID 2 in update workflow is not correct."
    )
