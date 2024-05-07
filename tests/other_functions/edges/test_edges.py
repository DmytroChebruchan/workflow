from unittest.mock import AsyncMock

import pytest

from api.edges.scripts import (
    creating_required_edges_script,
    delete_old_edges_script,
)


@pytest.mark.asyncio
async def test_creating_required_edges_script():
    # Mock the required objects
    session_mock = AsyncMock()
    node_id = 1
    node_from_id = 2
    nodes_destination_dict = {"True": 3, "False": 4}

    # Call the function
    await creating_required_edges_script(
        node_id, node_from_id, nodes_destination_dict, session_mock
    )

    assert len(session_mock.method_calls) == 9


@pytest.mark.asyncio
async def test_delete_old_edges_script():
    # Mock the required objects
    session_mock = AsyncMock()
    node_from_id = 1
    nodes_destination = {True: 2, False: 3}
    edge_condition_type = True

    # Call the function
    await delete_old_edges_script(
        node_from_id, nodes_destination, session_mock, edge_condition_type
    )

    # Assert that the necessary methods were called with the correct arguments
    assert len(session_mock.method_calls) == 5
