import pytest
from unittest.mock import AsyncMock, MagicMock
from api.workflows.schemas import WorkflowCreate, WorkflowUpdate
from api.workflows.crud_WorkflowRepo import WorkflowRepo


@pytest.mark.asyncio
async def test_workflow_repo():
    # Mock AsyncSession
    session_mock = AsyncMock()

    # Create a WorkflowCreate instance for testing
    workflow_create_data = {"title": "Test Workflow"}
    workflow_create = WorkflowCreate(**workflow_create_data)

    # Initialize WorkflowRepo with mock session
    workflow_repo = WorkflowRepo(session=session_mock, workflow_id=1)

    # Mock the save_element_into_db method
    workflow_repo.save_element_into_db = AsyncMock()

    # Test create_workflow method
    created_workflow = await workflow_repo.create_workflow(workflow_create)
    assert created_workflow.title == "Test Workflow"

    # Assert that save_element_into_db was called
    workflow_repo.save_element_into_db.assert_called_once()

    # Mock the get_element_by_id method
    workflow_repo.get_element_by_id = AsyncMock(return_value=created_workflow)

    # Test get_workflow_by_id method
    retrieved_workflow = await workflow_repo.get_workflow_by_id()
    assert retrieved_workflow.title == "Test Workflow"

    # Create a WorkflowUpdate instance for testing
    workflow_update_data = {
        "title": "Updated Workflow",
    }
    workflow_update = WorkflowUpdate(**workflow_update_data)

    # Mock the commit_and_refresh_element method
    workflow_repo.commit_and_refresh_element = AsyncMock()

    # Test update_workflow method
    updated_workflow = await workflow_repo.update_workflow(
        workflow_update, retrieved_workflow
    )
    assert updated_workflow.title == "Updated Workflow"

    # Assert that commit_and_refresh_element was called
    workflow_repo.commit_and_refresh_element.assert_called_once()

    # Mock the delete_element_from_db method
    workflow_repo.delete_element_from_db = AsyncMock()

    # Test delete_workflow_by_id method
    await workflow_repo.delete_workflow_by_id()

    # Assert that delete_element_from_db was called
    workflow_repo.delete_element_from_db.assert_called_once()
