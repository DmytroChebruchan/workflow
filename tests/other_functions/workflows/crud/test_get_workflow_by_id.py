from unittest.mock import AsyncMock

from api.workflows.crud import (
    create_workflow,
    get_workflow_by_id,
    update_workflow,
)
from api.workflows.schemas import WorkflowCreate, WorkflowUpdate
from core.models import Workflow


async def test_create_workflow():
    workflow_base_mock = WorkflowCreate(title="title")
    session = AsyncMock()
    result = await create_workflow(
        session=session, workflow_in=workflow_base_mock
    )
    assert isinstance(result, Workflow)
    assert result.title == "title"


async def test_get_workflow_by_id():
    mock_session = AsyncMock()
    # Create a mock node object
    mock_workflow = AsyncMock()

    # Set the return value of mock_session.get() to be the mock_node
    mock_session = AsyncMock()
    mock_session.get.return_value = mock_workflow

    # Call get_node_by_id
    result = await get_workflow_by_id(session=mock_session, workflow_id=1)

    # Assert that the result is the same as the mock_node
    assert result == mock_workflow


async def test_update_workflow(client):
    workflow_update_mock = WorkflowUpdate(title="new title")
    workflow_base_mock = Workflow(id=1, title="title")
    session = AsyncMock()
    function_return = await update_workflow(
        workflow_update=workflow_update_mock,
        workflow=workflow_base_mock,
        session=session,
    )
    assert isinstance(function_return, Workflow)
    assert function_return.id == workflow_base_mock.id
    assert function_return.title == "new title"
