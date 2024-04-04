from fastapi import APIRouter
from .schemas import WorkflowBase

router = APIRouter()


@router.post("/execute_workflow/{workflow_id}")
def execute_workflow(workflow_id: int, workflow: WorkflowBase):
    pass
