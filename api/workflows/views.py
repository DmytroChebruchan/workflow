from typing import List

from fastapi import APIRouter, Depends, Response
from sqlalchemy.ext.asyncio import AsyncSession

from api.general.utils import get_elements

from api.workflows.crud import (
    delete_workflow_by_id,
    get_workflow_by_id,
    update_workflow,
)
from api.workflows.run_workflow import run_workflow
from api.workflows.schemas import Workflow, WorkflowCreate, WorkflowUpdate
from api.workflows.utils import create_workflow_with_nodes
from core.database.database import get_async_session
from core.models.workflow import Workflow as WorkflowModel

router = APIRouter(tags=["Workflows"])


@router.get("/show_workflows/", response_model=List[Workflow])
async def get_workflows_view(
    session: AsyncSession = Depends(get_async_session),
) -> List[Workflow]:
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
) -> WorkflowModel:
    return await get_workflow_by_id(session=session, workflow_id=workflow_id)


@router.get("/run/{workflow_id}/")
async def run_workflow_view(
    workflow_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    await get_workflow_by_id(session=session, workflow_id=workflow_id)
    return await run_workflow(session=session, workflow_id=workflow_id)


@router.put("/update/{workflow_id}/", response_model=Workflow)
async def update_workflow_view(
    workflow_id: int,
    workflow_update: WorkflowUpdate,
    session: AsyncSession = Depends(get_async_session),
):
    workflow = await get_workflow_by_id(
        workflow_id=workflow_id, session=session
    )
    updated_workflow = await update_workflow(
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
    workflow = await get_workflow_by_id(
        session=session, workflow_id=workflow_id
    )
    await delete_workflow_by_id(session=session, workflow=workflow)
    return Response(
        content=f"Workflow with id {str(workflow_id)} was deleted.",
        status_code=200,
    )
