import unittest
from unittest.mock import AsyncMock, MagicMock, patch

from api.workflows.crud import (
    create_workflow,
    delete_workflow_by_id,
    get_workflow_by_id,
    update_workflow,
)
from api.workflows.schemas import WorkflowUpdate
from core.models import Workflow
from tests.mock_file import true_returner_mock


async def get_element_by_id_mock(**kwargs):
    return True


@patch("api.workflows.crud.get_element_by_id", get_element_by_id_mock)
async def test_get_workflow_by_id():
    mock_session = AsyncMock()
    assert (
        await get_workflow_by_id(session=mock_session, workflow_id=1) is True
    )


@patch("api.workflows.crud.update_element_id_checker", true_returner_mock)
@patch("api.workflows.crud.commit_and_refresh_element", true_returner_mock)
async def test_update_workflow(client):
    workflow_update_mock = WorkflowUpdate(id=1, title="new title")
    workflow_base_mock = Workflow(id=1, title="title")
    session = AsyncMock()
    function_return = await update_workflow(
        workflow_update=workflow_update_mock,
        workflow=workflow_base_mock,
        session=session,
    )
    assert isinstance(function_return, Workflow)
    assert function_return.id == workflow_update_mock.id
    assert function_return.title == "new title"


@patch("api.workflows.crud.delete_element_from_db", true_returner_mock)
async def test_delete_workflow():
    workflow_base_mock = Workflow(id=1, title="title")
    session = AsyncMock()
    result = await delete_workflow_by_id(
        session=session, workflow=workflow_base_mock
    )
    assert result is None
