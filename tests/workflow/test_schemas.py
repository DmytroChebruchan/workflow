import pytest
from pydantic import ValidationError

from api.workflows.schemas import WorkflowCreate, WorkflowUpdate, Workflow


def test_workflow_create():
    workflow_data = {"title": "Test Workflow"}
    workflow = WorkflowCreate(**workflow_data)
    assert workflow.title == "Test Workflow"


def test_workflow_update():
    workflow_data = {"title": "Updated Workflow"}
    workflow = WorkflowUpdate(**workflow_data)
    assert workflow.title == "Updated Workflow"


def test_workflow_invalid_data():
    with pytest.raises(ValidationError):
        WorkflowCreate()  # Title is required


if __name__ == "__main__":
    pytest.main([__file__])
