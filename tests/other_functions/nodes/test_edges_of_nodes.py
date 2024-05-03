from unittest import mock
from unittest.mock import AsyncMock, Mock, patch

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from api.general.utils_NodeEdgeManager import (
    EdgeDelManager,
)
from core.models import Edge, Node


@pytest.mark.asyncio
async def test_get_edges_of_node():
    # Mock the Node object
    node_mock = AsyncMock()

    # Mock the outgoing_edges and incoming_edges attributes
    node_mock.outgoing_edges = {Edge(id=1), Edge(id=2)}
    node_mock.incoming_edges = {Edge(id=3), Edge(id=4)}

    edge_del_object = EdgeDelManager(session=mock.AsyncMock(), node=node_mock)
    # Call the function
    edges = await edge_del_object.get_edges_of_node()

    # Assert that the function returns the expected list of edges
    assert len(edges) == 4  # Total number of unique edges
    assert {1, 2, 3, 4} == set([edge.id for edge in edges])


# Mock function for get_edges_of_node
async def mock_get_edges_of_node(node):
    # Return some mock edges for testing
    return [Edge(id=1), Edge(id=2)]


@pytest.mark.asyncio
async def test_delete_edges_of_node():
    # Create a mock AsyncSession
    mock_session = Mock(spec=AsyncSession)

    # Patch the get_edges_of_node function to return mock edges
    with patch(
        "api.general.utils.edges_collector",
        side_effect=mock_get_edges_of_node,
    ):
        # Create a mock Node instance
        node = Node(id=1)
        edges_del_object = EdgeDelManager(node=node, session=mock_session)
        # Call the delete_edges_of_node function
        await edges_del_object.delete_edges_of_node()
