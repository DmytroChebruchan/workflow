from unittest.mock import AsyncMock

import pytest

from core.models.node import Node


@pytest.fixture
def mock_get_async_session():
    return AsyncMock()


@pytest.fixture
def get_node_by_id_mock():
    return Node()
