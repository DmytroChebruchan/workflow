from typing import List

from fastapi import APIRouter, Depends, Response
from sqlalchemy.ext.asyncio import AsyncSession

from api.general.utils import get_elements
from api.workflows.crud import (
    get_workflow_by_id,
)
from api.workflows.schemas import (
    WorkflowFromDB,
    WorkflowCreate,
    WorkflowUpdate,
)
from api.workflows.scripts import (
    run_workflow_script,
    delete_workflow_script,
    update_workflow_script,
)
from api.workflows.utils import create_workflow_with_nodes
from core.database.database import get_async_session
from core.models.workflow import Workflow as WorkflowModel

router = APIRouter(tags=["Workflows"])


@router.get("/show_workflows/", response_model=List[WorkflowFromDB])
async def get_workflows_view(
    session: AsyncSession = Depends(get_async_session),
) -> List[WorkflowFromDB]:
    return await get_elements(session=session, element=WorkflowModel)


@router.post("/create/", response_model=WorkflowFromDB)
async def create_workflow_view(
    workflow_input: WorkflowCreate,
    session: AsyncSession = Depends(get_async_session),
):
    return await create_workflow_with_nodes(
        session=session, workflow_in=workflow_input
    )


@router.get("/read/{workflow_id}/", response_model=WorkflowFromDB)
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
    return await run_workflow_script(session, workflow_id)


@router.put("/update/{workflow_id}/", response_class=Response)
async def update_workflow_view(
    workflow_id: int,
    workflow_update: WorkflowUpdate,
    session: AsyncSession = Depends(get_async_session),
):
    return await update_workflow_script(session, workflow_id, workflow_update)


@router.delete("/delete/{workflow_id}/", response_class=Response)
async def delete_workflow_view(
    workflow_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    return await delete_workflow_script(session, workflow_id)
