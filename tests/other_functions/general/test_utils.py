from unittest.mock import AsyncMock, patch
import pytest

from api.general.utils import edges_collector, get_edges_of_nodes
from core.models import Edge


@pytest.mark.asyncio
async def test_edges_collector():
    # Mocking a node object
    class MockNode:

        def __init__(self, incoming_edges, outgoing_edges):
            self.incoming_edges = incoming_edges
            self.outgoing_edges = outgoing_edges

    # Define mock incoming and outgoing edges
    incoming_edges = [Edge(id=1), Edge(id=2)]
    outgoing_edges = [Edge(id=3), Edge(id=4)]

    # Mocking the edges_collector function to return some edges
    with patch("api.general.utils.edges_collector") as edges_collector_mock:
        edges_collector_mock.return_value = incoming_edges + outgoing_edges

        # Simulating the call to edges_collector with the mock node
        result = await edges_collector(
            MockNode(incoming_edges, outgoing_edges)
        )

    # Asserting the result
    assert set(result) == set(incoming_edges + outgoing_edges)


@pytest.mark.asyncio
async def test_get_edges_of_nodes():
    # Mocking nodes
    nodes = [
        AsyncMock(incoming_edges=[Edge(id=1)], outgoing_edges=[Edge(id=2)]),
        AsyncMock(incoming_edges=[Edge(id=3)], outgoing_edges=[Edge(id=4)]),
    ]

    # Mocking edges_collector function to return some edges
    edges_collector.side_effect = [
        [Edge(id=1), Edge(id=2)],
        [Edge(id=3), Edge(id=4)],
    ]

    # Calling the function under test
    result = await get_edges_of_nodes(nodes)

    # Asserting the result
    ids_of_result = [edge.id for edge in result]
    assert set(ids_of_result) == {1, 2, 3, 4}


# Run the tests with pytest
if __name__ == "__main__":
    pytest.main()
