from fastapi import HTTPException, status
from unittest.mock import MagicMock

from api.general.validators import element_validator


async def test_element_validator():
    # Define test data
    element_id = 1
    item = MagicMock()  # Create a MagicMock object for the 'item'

    # Test case 1: item is None
    item_is_none = None
    try:
        await element_validator(element_id, item_is_none)
    except HTTPException as e:
        assert e.status_code == status.HTTP_404_NOT_FOUND
        assert e.detail == f"{item_is_none} with ID {element_id} not found"

    # Test case 2: item is not None
    item_is_not_none = (
        MagicMock()
    )  # Create another MagicMock object for the 'item'
    try:
        await element_validator(element_id, item_is_not_none)
    except HTTPException as e:
        # This test should not raise an exception, so if it does, fail the test
        assert False, f"No exception should be raised when item is not None"
