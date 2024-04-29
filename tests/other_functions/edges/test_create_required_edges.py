from unittest.mock import AsyncMock, patch

import pytest

from api.edges.crud import creating_required_edges
from api.nodes.schemas.schemas import NodeCreate


@pytest.fixture
def node_in_with_conditions():
    return NodeCreate(
        type="Start Node",
        workflow_id=1,
        from_node_id=1,
        nodes_dest_dict={"True": 3, "False": 4},
    )


@pytest.fixture
def node_in_without_conditions():
    return NodeCreate(
        type="Start Node",
        workflow_id=1,
        from_node_id=5,
    )


@pytest.mark.asyncio
@pytest.mark.usefixtures(
    "node_in_with_conditions", "node_in_without_conditions"
)
@patch("api.edges.crud.create_edge")
async def test_creating_required_edges(
    create_edge_mock, node_in_with_conditions, node_in_without_conditions
):
    session = AsyncMock()

    # Call the function under test
    await creating_required_edges(
        node_id=1,
        node_from_id=2,
        nodes_destination_dict={True: 3, False: 4},
        session=session,
    )

    # Assertions for node_in_with_conditions
    create_edge_mock.assert_any_call(
        session=session, from_node_id=1, to_node_id=3, condition=True
    )
    create_edge_mock.assert_any_call(
        session=session, from_node_id=1, to_node_id=4, condition=False
    )

    # Reset mock
    create_edge_mock.reset_mock()

    # Call the function under test again with node_in_without_conditions
    await creating_required_edges(
        node_id=1,
        node_from_id=node_in_without_conditions.from_node_id,
        nodes_destination_dict={True: 2, False: 3},
        session=session,
    )

    # Assertions for node_in_without_conditions
    create_edge_mock.assert_any_call(
        session=session, from_node_id=1, to_node_id=3, condition=False
    )