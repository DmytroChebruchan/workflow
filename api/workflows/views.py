from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from api.general.utils import get_elements, get_element_by_id
from api.workflows import crud
from api.workflows.run_workflow import run_workflow
from api.workflows.schemas import (
    Workflow,
    WorkflowCreate,
    WorkflowUpdate,
)
from api.workflows.validator import workflow_validator
from api.workflows.workflow_utils import create_workflow_with_nodes
from core.database.database import get_async_session

from core.models.workflow import Workflow as WorkflowModel

router = APIRouter(tags=["Workflows"])


@router.get("/show_workflows/")
async def get_workflows_view(
    session: AsyncSession = Depends(get_async_session),
):
    return await get_elements(session=session, element=WorkflowModel)


@router.post("/create/", response_model=Workflow)
async def create_workflow_view(
    workflow_input: WorkflowCreate,
    session: AsyncSession = Depends(get_async_session),
):
    return await create_workflow_with_nodes(
        session=session, workflow_in=workflow_input
    )


@router.get("/read/{workflow_id}/", response_model=Workflow)
async def get_workflow_by_id_view(
    workflow_id: int,
    session: AsyncSession = Depends(get_async_session),
) -> Workflow:
    workflow = await crud.get_workflow_by_id(
        session=session, workflow_id=workflow_id
    )
    if workflow is not None:
        return workflow

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Workflow {workflow_id} not found!",
    )


@router.get("/show_nodes_related/{workflow_id}/")
async def nodes_related_view(
    workflow_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    workflow = await crud.get_workflow_by_id(
        session=session, workflow_id=workflow_id
    )
    if workflow is not None:
        return await run_workflow(session=session, workflow_id=workflow_id)

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Workflow {workflow_id} not found!",
    )


@router.put("/update/{workflow_id}/", response_model=Workflow)
async def update_workflow_view(
    workflow_id: int,
    workflow_update: WorkflowUpdate,
    session: AsyncSession = Depends(get_async_session),
):
    workflow = await workflow_validator(
        session=session,
        workflow_id=workflow_id,
    )
    updated_workflow = await crud.update_workflow(
        session=session,
        workflow=workflow,
        workflow_update=workflow_update,
    )
    return updated_workflow


@router.delete("/delete/{workflow_id}/", response_model=None)
async def delete_workflow_view(
    workflow_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    workflow = await workflow_validator(
        session=session, workflow_id=workflow_id
    )
    await crud.delete_workflow_by_id(session=session, workflow=workflow)
