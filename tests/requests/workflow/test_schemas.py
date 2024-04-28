import pytest
from pydantic import ValidationError

from api.workflows.schemas import WorkflowCreate, WorkflowUpdate


def test_workflow_create():
    workflow_data = {"title": "Test Workflow"}
    workflow = WorkflowCreate(**workflow_data)
    assert workflow.title == "Test Workflow"


def test_workflow_invalid_data():
    with pytest.raises(ValidationError):
        WorkflowCreate()
