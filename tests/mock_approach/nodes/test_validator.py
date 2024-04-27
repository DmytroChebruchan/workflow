from unittest.mock import patch, MagicMock

import pytest
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from api.nodes.validator import (
    ensure_unique_node_type,
    check_node_type_existence_in_workflow,
)
from tests.mock_file import true_returner_mock


@patch(
    "api.nodes.validator.get_nodes_by_type", return_value=true_returner_mock
)
async def test_ensure_unique_node_type(get_nodes_by_type):
    # Check if exception is raised
    with pytest.raises(HTTPException) as exc_info:
        await ensure_unique_node_type(
            node_type="Start Node", workflow_id=1, session=AsyncSession()
        )

    # Check the exception message or status code if needed
    assert exc_info.value.status_code == status.HTTP_400_BAD_REQUEST
    assert str(exc_info.value) == "400: Workflow with ID 1 has a Start Node"


@pytest.mark.asyncio
@patch("api.nodes.validator.get_workflow_by_id")
@patch("api.nodes.validator.ensure_unique_node_type")
async def test_check_node_type_existence_in_workflow(
    mock_ensure_unique_node_type, mock_get_workflow_by_id
):
    # Define the input data
    node_model_dict = {"workflow_id": 1, "type": "Start Node"}

    # Mocking AsyncSession
    mock_session = MagicMock(spec=AsyncSession)

    # Call the function
    await check_node_type_existence_in_workflow(node_model_dict, mock_session)

    # Assert the number of calls to get_workflow_by_id
    mock_get_workflow_by_id.assert_called_once_with(
        workflow_id=1, session=mock_session
    )

    # Assert the number of calls to ensure_unique_node_type
    mock_ensure_unique_node_type.assert_called_once_with(
        node_type="Start Node",
        workflow_id=1,
        session=mock_session,
    )
