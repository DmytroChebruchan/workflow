from unittest.mock import patch

import pytest
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from api.nodes.validation.validator import ensure_unique_node_type
from tests.mock_file import true_returner_mock


@patch(
    "api.nodes.validation.validator.get_nodes_by_type",
    return_value=true_returner_mock,
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
