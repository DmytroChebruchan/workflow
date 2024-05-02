from sqlalchemy.ext.asyncio import AsyncSession

from api.general.utils import (
    commit_and_refresh_element,
    delete_element_from_db,
    save_element_into_db,
)
from api.general.utils_element_class import ElementManagement
from api.workflows.schemas import WorkflowCreate, WorkflowUpdate
from core.models.workflow import Workflow


async def create_workflow(session, workflow_in: WorkflowCreate) -> Workflow:
    workflow = Workflow(**workflow_in.model_dump())
    await save_element_into_db(session=session, element=workflow)
    return workflow


async def get_workflow_by_id(
    session: AsyncSession, workflow_id: int
) -> Workflow:
    element = ElementManagement(session=session, model=Workflow)
    return await element.get_element_by_id(
        element_id=workflow_id,
    )


async def update_workflow(
    session: AsyncSession,
    workflow_update: WorkflowUpdate,
    workflow: Workflow,
) -> Workflow:
    for field, value in workflow_update.model_dump(exclude_unset=True).items():
        setattr(workflow, field, value)
    await commit_and_refresh_element(session=session, element=workflow)
    return workflow


async def delete_workflow_by_id(
    session: AsyncSession, workflow_id: int
) -> None:
    workflow = await get_workflow_by_id(
        session=session, workflow_id=workflow_id
    )
    await delete_element_from_db(session=session, element=workflow)
