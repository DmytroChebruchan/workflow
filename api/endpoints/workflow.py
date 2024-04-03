from fastapi import APIRouter
from api.models.schemas import WorkflowCreate, WorkflowUpdate

router = APIRouter()


@router.post("/create_workflow")
def create_workflow(workflow: WorkflowCreate):
    pass


@router.put("/update_workflow/{workflow_id}")
def update_workflow(workflow_id: int, workflow: WorkflowUpdate):
    pass


@router.delete("/delete_workflow/{workflow_id}")
def delete_workflow(workflow_id: int):
    pass
