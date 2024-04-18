from unittest.mock import AsyncMock, patch

import pytest

from api.edges.crud import create_edge
from core.models import Edge


async def node_validator_mock(**kwargs):
    return True


@patch("api.nodes.validators.node_validator", new=node_validator_mock)
@pytest.mark.asyncio
async def test_edge():
    edge_dict_info = {
        "from_node_id": 1,
        "to_node_id": 2,
        "session": AsyncMock(),
    }
    edge = await create_edge(**edge_dict_info)
    assert isinstance(edge, Edge)
