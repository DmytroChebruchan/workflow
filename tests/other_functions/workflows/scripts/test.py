from unittest.mock import AsyncMock, MagicMock, patch

from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import Response

from api.workflows.crud_WorkflowRepo import WorkflowRepo
from api.workflows.schemas import WorkflowUpdate
from api.workflows.scripts import (
    delete_workflow_script,
    run_workflow_script,
    update_workflow_script,
)
from tests.mock_file import true_returner_mock


@patch(
    "api.nodes.scripts.delete_nodes_of_workflow_script", new=true_returner_mock
)
async def test_delete_workflow_script():
    # Mocking the required dependencies
    mock_session = AsyncMock(AsyncSession)

    # Mocking the return values of the functions being called
    workflow_object = WorkflowRepo(session=mock_session, workflow_id=123)
    workflow_object.delete_workflow_by_id = AsyncMock(return_value=None)

    with patch(
        "api.workflows.scripts.Response", MagicMock(Response)
    ) as mock_response:
        mock_response.return_value = None

        # Calling the function being tested
        response = await delete_workflow_script(
            session=mock_session, workflow_id=123
        )

        # Assertions
        assert response is None


@patch("api.workflows.scripts.WorkflowRepo")
@patch("api.workflows.scripts.Response")
async def test_update_workflow_script(mock_response, mock_workflow_repo):
    # Mocking the required dependencies
    mock_session = AsyncMock(AsyncSession)
    mock_workflow_update = MagicMock(WorkflowUpdate)

    # Mocking the return values of the functions being called
    mock_workflow_instance = mock_workflow_repo.return_value
    mock_workflow_instance.get_workflow_by_id = AsyncMock(
        return_value=MagicMock()
    )
    mock_workflow_instance.update_workflow = AsyncMock(return_value=None)

    mock_response.return_value = None

    # Calling the function being tested
    response = await update_workflow_script(
        session=mock_session,
        workflow_id=123,
        workflow_update=mock_workflow_update,
    )

    # Assertions
    mock_workflow_instance.get_workflow_by_id.assert_awaited_once()
    mock_workflow_instance.update_workflow.assert_awaited_once_with(
        workflow_update=mock_workflow_update,
        workflow=mock_workflow_instance.get_workflow_by_id.return_value,
    )
    assert response == mock_response.return_value


@patch("api.workflows.scripts.WorkflowRepo")
@patch("api.workflows.scripts.creating_graph_script")
@patch("api.workflows.scripts.Response")
async def test_run_workflow_script(
    mock_response, mock_creating_graph_script, mock_workflow_repo
):
    # Mocking the required dependencies
    mock_session = AsyncMock(AsyncSession)
    mock_workflow = MagicMock()
    mock_graph = MagicMock()

    # Mocking the return values of the functions being called
    mock_workflow_instance = mock_workflow_repo.return_value
    mock_workflow_instance.get_workflow_by_id = AsyncMock(
        return_value=mock_workflow
    )
    mock_creating_graph_script.return_value = mock_graph
    mock_graph.find_path = AsyncMock(return_value={"path": "details"})

    mock_response.return_value = None

    # Calling the function being tested
    result = await run_workflow_script(session=mock_session, workflow_id=123)

    # Assertions
    mock_workflow_repo.assert_called_once_with(
        session=mock_session, workflow_id=123
    )
    mock_workflow_instance.get_workflow_by_id.assert_awaited_once()
    mock_creating_graph_script.assert_awaited_once_with(
        mock_session, mock_workflow
    )
    mock_graph.find_path.assert_awaited_once()
    assert result == {"path": "details"}
