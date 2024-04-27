from unittest.mock import MagicMock, patch

import pytest
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from api.nodes.validator import ensure_unique_node_type


async def test_ensure_unique_node_type():
    # Mocking get_nodes_by_type
    with patch("api.nodes.validator.get_nodes_by_type") as get_nodes_by_type:
        get_nodes_by_type.return_value = True

        # Check if exception is raised
        with pytest.raises(HTTPException) as exc_info:
            await ensure_unique_node_type(
                node_type="Start Node", workflow_id=1, session=AsyncSession()
            )

        # Check the exception message or status code if needed
        assert exc_info.value.status_code == status.HTTP_400_BAD_REQUEST
        assert (
            str(exc_info.value) == "400: Workflow with ID 1 has a Start Node"
        )
