from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper
from .schemas import Workflow, WorkflowCreate
from . import crud

router = APIRouter(tags=["Workflows"])


@router.get("/show_workflows/", response_model=list[Workflow])
async def get_workflows(
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    return await crud.get_workflows(session=session)


@router.post("/create/", response_model=Workflow)
async def create_workflow(
    workflow_in: WorkflowCreate,
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    return await crud.create_workflow(session=session, workflow_in=workflow_in)


@router.get("/{workflow_id}/", response_model=Workflow)
async def get_workflows(
    workflow_id: int,
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    workflow = await crud.get_workflow_by_id(
        session=session,
        workflow_id=workflow_id,
    )
    if workflow is not None:
        return workflow

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Workflow {workflow_id} not found!",
    )


@router.delete("/{workflow_id}/", response_model=None)
async def delete_workflow(
    workflow_id: int,
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    await crud.delete_workflow_by_id(session=session, workflow_id=workflow_id)

# @router.put("/update/")
# async def update_workflow(workflow: Workflow):
#     return {"message": f"Workflow with id {workflow.id} was updated."}
