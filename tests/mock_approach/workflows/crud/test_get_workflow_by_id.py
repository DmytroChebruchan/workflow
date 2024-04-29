from unittest.mock import AsyncMock, patch

from api.workflows.crud import (
    create_workflow,
    get_workflow_by_id,
    update_workflow,
)
from api.workflows.schemas import WorkflowCreate, WorkflowUpdate
from core.models import Workflow
from tests.mock_file import true_returner_mock


@patch("api.workflows.crud.save_element_into_db", true_returner_mock)
async def test_create_workflow():
    workflow_base_mock = WorkflowCreate(title="title")
    session = AsyncMock()
    result = await create_workflow(
        session=session, workflow_in=workflow_base_mock
    )
    assert isinstance(result, Workflow)
    assert result.title == "title"


@patch("api.workflows.crud.get_element_by_id", true_returner_mock)
async def test_get_workflow_by_id():
    mock_session = AsyncMock()
    assert (
        await get_workflow_by_id(session=mock_session, workflow_id=1) is True
    )


@patch("api.workflows.crud.commit_and_refresh_element", true_returner_mock)
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
