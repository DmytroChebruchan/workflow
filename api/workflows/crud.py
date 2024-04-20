from sqlalchemy.ext.asyncio import AsyncSession

from api.general.utils import (
    delete_element_from_db,
    get_element_by_id,
    save_element_into_db,
)
from api.workflows.schemas import WorkflowUpdate
from core.models.workflow import Workflow


async def get_workflow_by_id(
    session: AsyncSession, workflow_id: int
) -> Workflow | None:
    return await get_element_by_id(
        element=Workflow,
        session=session,
        element_id=workflow_id,
    )


async def update_workflow(
    session: AsyncSession,
    workflow_update: WorkflowUpdate,
    workflow,
) -> Workflow | None:

    for field, value in workflow_update.dict(exclude_unset=True).items():
        setattr(workflow, field, value)

    await session.commit()
    await session.refresh(workflow)
    return workflow


async def delete_workflow_by_id(
    session: AsyncSession, workflow: Workflow
) -> dict[str, str]:
    await delete_element_from_db(session=session, element=workflow)
    return {"details": "Workflow deleted"}


async def create_workflow(session, workflow_in) -> Workflow:
    workflow = Workflow(**workflow_in.model_dump())
    await save_element_into_db(session=session, element=workflow)
    return workflow
