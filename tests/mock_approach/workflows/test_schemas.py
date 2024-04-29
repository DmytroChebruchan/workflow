from api.workflows.schemas import WorkflowCreate


def test_workflow_create():
    workflow_data = {"title": "Test Workflow"}
    workflow = WorkflowCreate(**workflow_data)
    assert workflow.title == "Test Workflow"
