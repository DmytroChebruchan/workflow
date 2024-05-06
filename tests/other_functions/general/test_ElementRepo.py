from unittest.mock import AsyncMock, MagicMock

import pytest
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession

from api.general.utils_ElementRepo import ElementRepo
from core.models import Node


@pytest.fixture
def mock_session():
    return MagicMock(spec=AsyncSession)


@pytest.fixture
def mock_model():
    return Node  # Assuming Node is the model class


@pytest.fixture
def element_repo(mock_session, mock_model):
    return ElementRepo(mock_session, mock_model)


@pytest.mark.asyncio
async def test_get_elements(element_repo, mock_session, mock_model):
    # Prepare mock result
    mock_result = MagicMock(spec=Result)
    mock_node1 = mock_model(id=1, type="Node 1")
    mock_node2 = mock_model(id=2, type="Node 2")
    mock_nodes = [mock_node1, mock_node2]
    mock_result.scalars.return_value.all.return_value = mock_nodes
    mock_session.execute.return_value = mock_result

    # Call the method under test
    elements = await element_repo.get_elements()

    # Assertions
    assert isinstance(elements, list)
    assert len(elements) == 2
    assert all(isinstance(node, Node) for node in elements)
    assert elements[0].id == 1
    assert elements[1].id == 2
    assert elements[0].type == "Node 1"
    assert elements[1].type == "Node 2"


@pytest.mark.asyncio
async def test_get_element_by_id(element_repo, mock_session, mock_model):
    # Prepare mock node
    mock_node = mock_model(id=1, type="Node 1")

    # Set up mock session's get method to return the mock node
    mock_session.get.return_value = mock_node

    # Call the method under test
    element = await element_repo.get_element_by_id(1)

    # Assertions
    assert isinstance(element, Node)
    assert element.id == 1
    assert element.type == "Node 1"


@pytest.mark.asyncio
async def test_save_element_into_db(element_repo, mock_session, mock_model):
    # Mocking commit_and_refresh_element method as an AsyncMock
    element_repo.commit_and_refresh_element = AsyncMock()

    # Call the method under test
    element_repo.object_of_class = Node(id=1, type="Node 1")
    saved_element = await element_repo.save_element_into_db()

    # Assertions
    assert isinstance(saved_element, Node)
    assert mock_session.add.called_once_with(mock_model())
    assert await element_repo.commit_and_refresh_element.called_once()
    assert saved_element == element_repo.object_of_class


@pytest.mark.asyncio
async def test_delete_element_from_db(element_repo, mock_session, mock_model):
    # Call the method under test
    await element_repo.delete_element_from_db()

    # Assertions
    assert await mock_session.delete.called_once_with(
        element_repo.object_of_class
    )
    assert await mock_session.commit.called_once()
